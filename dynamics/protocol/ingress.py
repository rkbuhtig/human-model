"""Experimental ingress identity, ordering, deferral, and overflow policy."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any

from .events import ScenarioEvent
from ..temporal import SimTime


@dataclass(frozen=True, slots=True)
class IngressDecision:
    """One raw delivery's canonical identity disposition."""

    disposition: str
    delivery_id: str
    occurrence_id: str

    @property
    def event_id(self) -> str:
        """v0.1 compatibility alias for delivery identity."""

        return self.delivery_id


@dataclass(frozen=True, slots=True)
class IngressBatch:
    processing: tuple[ScenarioEvent, ...]
    deferred_event_ids: tuple[str, ...]
    dropped_event_ids: tuple[str, ...]
    same_timestamp_order_debts: tuple[tuple[str, ...], ...] = ()


def _canonical_value(value: Any) -> Any:
    """Project protocol values to a stable JSON-compatible representation."""

    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {
            item.name: _canonical_value(getattr(value, item.name))
            for item in fields(value)
        }
    if isinstance(value, tuple):
        return [_canonical_value(item) for item in value]
    if isinstance(value, list):
        return [_canonical_value(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): _canonical_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    return value


def _digest(value: Any) -> str:
    encoded = json.dumps(
        _canonical_value(value),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _occurrence_projection(event: ScenarioEvent) -> dict[str, Any]:
    """Fields that define one source occurrence, excluding transport metadata."""

    excluded = {"event_id", "tick", "temporal", "ingress_priority"}
    payload = {
        item.name: getattr(event, item.name)
        for item in fields(event)
        if item.name not in excluded
    }
    payload.update(
        {
            "occurrence_id": event.occurrence_id,
            "occurred_at": int(event.occurred_at),
            "reexposure_of_occurrence_id": event.reexposure_of_occurrence_id,
        }
    )
    return payload


def _delivery_projection(event: ScenarioEvent) -> dict[str, Any]:
    """Fields that define one transport delivery of an occurrence."""

    return {
        "delivery_id": event.delivery_id,
        "occurrence_id": event.occurrence_id,
        "occurred_at": int(event.occurred_at),
        "available_at": int(event.available_at),
        "reexposure_of_occurrence_id": event.reexposure_of_occurrence_id,
        "delivery_sequence": event.delivery_sequence,
        "ingress_priority": event.ingress_priority,
        "occurrence_payload": _occurrence_projection(event),
    }


@dataclass(slots=True)
class IngressQueue:
    """Protocol queue; it is not a claim about human memory storage."""

    queue_limit: int
    policy: str = "priority"
    _pending: list[ScenarioEvent] = field(default_factory=list)
    _delivery_fingerprints: dict[str, str] = field(default_factory=dict)
    _occurrence_fingerprints: dict[str, str] = field(default_factory=dict)
    _active_occurrence_ids: set[str] = field(default_factory=set)
    _committed_occurrence_ids: set[str] = field(default_factory=set)
    _leased_deliveries_by_occurrence: dict[str, str] = field(default_factory=dict)
    _committed_processing_times: dict[str, SimTime] = field(default_factory=dict)
    _reported_order_debt_keys: set[tuple[int | float, ...]] = field(
        default_factory=set
    )

    def __post_init__(self) -> None:
        if self.queue_limit < 1:
            raise ValueError("queue_limit must be positive")
        if self.policy not in {"fifo", "priority"}:
            raise ValueError("policy must be 'fifo' or 'priority'")

    @staticmethod
    def _delivery_fingerprint(event: ScenarioEvent) -> str:
        return _digest(_delivery_projection(event))

    @staticmethod
    def _occurrence_fingerprint(event: ScenarioEvent) -> str:
        return _digest(_occurrence_projection(event))

    def accept(self, event: ScenarioEvent) -> IngressDecision:
        delivery_fingerprint = self._delivery_fingerprint(event)
        occurrence_fingerprint = self._occurrence_fingerprint(event)
        prior_delivery = self._delivery_fingerprints.get(event.delivery_id)
        if prior_delivery is not None:
            return IngressDecision(
                "duplicate" if prior_delivery == delivery_fingerprint else "delivery_collision",
                event.delivery_id,
                event.occurrence_id,
            )

        self._delivery_fingerprints[event.delivery_id] = delivery_fingerprint
        prior_occurrence = self._occurrence_fingerprints.get(event.occurrence_id)
        if prior_occurrence is not None and prior_occurrence != occurrence_fingerprint:
            return IngressDecision(
                "occurrence_collision",
                event.delivery_id,
                event.occurrence_id,
            )

        reference = event.reexposure_of_occurrence_id
        if reference is not None and reference not in self._committed_occurrence_ids:
            return IngressDecision(
                "dangling_reexposure",
                event.delivery_id,
                event.occurrence_id,
            )
        if (
            reference is not None
            and event.occurred_at < self._committed_processing_times[reference]
        ):
            return IngressDecision(
                "invalid_reexposure_time",
                event.delivery_id,
                event.occurrence_id,
            )

        if prior_occurrence is not None and event.occurrence_id in (
            self._active_occurrence_ids | self._committed_occurrence_ids
        ):
            return IngressDecision(
                "redundant_delivery",
                event.delivery_id,
                event.occurrence_id,
            )

        if prior_occurrence is None:
            self._occurrence_fingerprints[event.occurrence_id] = occurrence_fingerprint
        self._active_occurrence_ids.add(event.occurrence_id)
        self._pending.append(event)
        return IngressDecision("accepted", event.delivery_id, event.occurrence_id)

    @staticmethod
    def _priority_key(event: ScenarioEvent) -> tuple[float, int, int, int]:
        sequence = event.delivery_sequence
        return (
            -event.ingress_priority,
            int(event.available_at),
            1 if sequence is None else 0,
            0 if sequence is None else sequence,
        )

    @staticmethod
    def _fifo_key(event: ScenarioEvent) -> tuple[int, int, int]:
        sequence = event.delivery_sequence
        return (
            int(event.available_at),
            1 if sequence is None else 0,
            0 if sequence is None else sequence,
        )

    def _ordering_debts(
        self,
        processing: tuple[ScenarioEvent, ...],
    ) -> tuple[tuple[str, ...], ...]:
        groups: dict[tuple[int | float, ...], list[ScenarioEvent]] = {}
        for event in processing:
            key: tuple[int | float, ...]
            if self.policy == "priority":
                key = (int(event.available_at), event.ingress_priority)
            else:
                key = (int(event.available_at),)
            groups.setdefault(key, []).append(event)
        debts: list[tuple[str, ...]] = []
        for key, group in sorted(groups.items()):
            sequences = [event.delivery_sequence for event in group]
            ambiguous = len(group) > 1 and (
                any(sequence is None for sequence in sequences)
                or len(set(sequences)) != len(sequences)
            )
            if ambiguous and key not in self._reported_order_debt_keys:
                debts.append(tuple(event.delivery_id for event in group))
                self._reported_order_debt_keys.add(key)
        return tuple(debts)

    def take(self, capacity: int) -> IngressBatch:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        if self.policy == "priority":
            self._pending.sort(key=self._priority_key)
        else:
            self._pending.sort(key=self._fifo_key)
        order_debts = self._ordering_debts(tuple(self._pending))
        processing = tuple(self._pending[:capacity])
        for event in processing:
            self._leased_deliveries_by_occurrence[event.occurrence_id] = (
                event.delivery_id
            )
        self._pending = self._pending[capacity:]
        deferred = tuple(event.delivery_id for event in self._pending)
        dropped: tuple[str, ...] = ()
        if len(self._pending) > self.queue_limit:
            dropped_events = tuple(self._pending[self.queue_limit :])
            dropped = tuple(event.delivery_id for event in dropped_events)
            for event in dropped_events:
                self._active_occurrence_ids.discard(event.occurrence_id)
            self._pending = self._pending[: self.queue_limit]
        return IngressBatch(
            processing,
            deferred,
            dropped,
            order_debts,
        )

    def mark_processed(
        self,
        event: ScenarioEvent,
        *,
        processed_at: SimTime | int | None = None,
    ) -> None:
        """Commit an accepted occurrence after the engine actually processes it."""

        leased_delivery = self._leased_deliveries_by_occurrence.get(
            event.occurrence_id
        )
        if leased_delivery != event.delivery_id:
            raise ValueError("cannot commit an occurrence without its processing lease")
        expected_fingerprint = self._delivery_fingerprints[event.delivery_id]
        if self._delivery_fingerprint(event) != expected_fingerprint:
            raise ValueError("processed event does not match its accepted delivery")
        canonical_processed_at = SimTime(
            int(event.available_at) if processed_at is None else processed_at
        )
        if canonical_processed_at < event.available_at:
            raise ValueError("processed_at must not precede available_at")
        del self._leased_deliveries_by_occurrence[event.occurrence_id]
        self._active_occurrence_ids.discard(event.occurrence_id)
        self._committed_occurrence_ids.add(event.occurrence_id)
        self._committed_processing_times[event.occurrence_id] = (
            canonical_processed_at
        )

    def pressure(self) -> float:
        return min(1.0, max(0.0, len(self._pending) / self.queue_limit))

    @property
    def has_pending(self) -> bool:
        return bool(self._pending)

    @property
    def unresolved_event_ids(self) -> tuple[str, ...]:
        return tuple(event.delivery_id for event in self._pending)
