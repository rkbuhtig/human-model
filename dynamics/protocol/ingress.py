"""Experimental ingress identity, ordering, deferral, and overflow policy."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib

from .events import ScenarioEvent


@dataclass(frozen=True, slots=True)
class IngressDecision:
    disposition: str
    event_id: str


@dataclass(frozen=True, slots=True)
class IngressBatch:
    processing: tuple[ScenarioEvent, ...]
    deferred_event_ids: tuple[str, ...]
    dropped_event_ids: tuple[str, ...]


@dataclass(slots=True)
class IngressQueue:
    """Protocol queue; it is not a claim about human memory storage."""

    queue_limit: int
    policy: str = "priority"
    _pending: list[ScenarioEvent] = field(default_factory=list)
    _fingerprints: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.queue_limit < 1:
            raise ValueError("queue_limit must be positive")
        if self.policy not in {"fifo", "priority"}:
            raise ValueError("policy must be 'fifo' or 'priority'")

    @staticmethod
    def _fingerprint(event: ScenarioEvent) -> str:
        return hashlib.sha256(repr(event).encode("utf-8")).hexdigest()

    def accept(self, event: ScenarioEvent) -> IngressDecision:
        fingerprint = self._fingerprint(event)
        prior = self._fingerprints.get(event.event_id)
        if prior is not None:
            return IngressDecision(
                "duplicate" if prior == fingerprint else "collision",
                event.event_id,
            )
        self._fingerprints[event.event_id] = fingerprint
        self._pending.append(event)
        return IngressDecision("accepted", event.event_id)

    def take(self, capacity: int) -> IngressBatch:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        if self.policy == "priority":
            self._pending.sort(
                key=lambda event: (-event.ingress_priority, event.tick)
            )
        processing = tuple(self._pending[:capacity])
        self._pending = self._pending[capacity:]
        deferred = tuple(event.event_id for event in self._pending)
        dropped: tuple[str, ...] = ()
        if len(self._pending) > self.queue_limit:
            dropped = tuple(
                event.event_id for event in self._pending[self.queue_limit :]
            )
            self._pending = self._pending[: self.queue_limit]
        return IngressBatch(processing, deferred, dropped)

    def pressure(self) -> float:
        return min(1.0, max(0.0, len(self._pending) / self.queue_limit))

    @property
    def unresolved_event_ids(self) -> tuple[str, ...]:
        return tuple(event.event_id for event in self._pending)
