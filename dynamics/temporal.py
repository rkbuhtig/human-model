"""Canonical temporal identities and stamps for Dynamics v0.2 protocols."""

from __future__ import annotations

from dataclasses import dataclass


class SimTime(int):
    """A non-negative canonical simulation time.

    ``bool`` and numeric coercions are deliberately rejected.  Protocol
    loaders must not silently turn ``True`` or ``1.5`` into a time coordinate.
    """

    def __new__(cls, value: int) -> "SimTime":
        if type(value) not in (int, SimTime):
            raise TypeError("SimTime requires a non-boolean int")
        if value < 0:
            raise ValueError("SimTime must be non-negative")
        return int.__new__(cls, value)


def _require_nonempty_id(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _require_sequence(value: object, name: str, *, positive: bool) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be a non-boolean int")
    lower_bound = 1 if positive else 0
    if value < lower_bound:
        qualifier = "positive" if positive else "non-negative"
        raise ValueError(f"{name} must be {qualifier}")
    return value


@dataclass(frozen=True, slots=True)
class EventTemporalEnvelope:
    """World-occurrence and protocol-delivery identity on canonical time."""

    occurrence_id: str
    delivery_id: str
    occurred_at: SimTime
    available_at: SimTime
    reexposure_of_occurrence_id: str | None = None
    delivery_sequence: int | None = None

    def __post_init__(self) -> None:
        occurrence_id = _require_nonempty_id(self.occurrence_id, "occurrence_id")
        _require_nonempty_id(self.delivery_id, "delivery_id")
        occurred_at = SimTime(self.occurred_at)
        available_at = SimTime(self.available_at)
        if occurred_at > available_at:
            raise ValueError("occurred_at must not be later than available_at")

        reexposure = self.reexposure_of_occurrence_id
        if reexposure is not None:
            _require_nonempty_id(reexposure, "reexposure_of_occurrence_id")
            if reexposure == occurrence_id:
                raise ValueError("a reexposure cannot refer to its own occurrence_id")

        sequence = self.delivery_sequence
        if sequence is not None:
            _require_sequence(sequence, "delivery_sequence", positive=False)

        object.__setattr__(self, "occurred_at", occurred_at)
        object.__setattr__(self, "available_at", available_at)


@dataclass(frozen=True, slots=True)
class ProcessingStamp:
    """A protocol processing position for one temporal envelope."""

    envelope: EventTemporalEnvelope
    processed_at: SimTime
    processing_sequence: int

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, EventTemporalEnvelope):
            raise TypeError("envelope must be EventTemporalEnvelope")
        processed_at = SimTime(self.processed_at)
        if self.envelope.available_at > processed_at:
            raise ValueError("available_at must not be later than processed_at")
        _require_sequence(
            self.processing_sequence,
            "processing_sequence",
            positive=True,
        )
        object.__setattr__(self, "processed_at", processed_at)


def legacy_temporal_envelope(event_id: str, tick: int) -> EventTemporalEnvelope:
    """Project the v0.1 ``event_id``/``tick`` pair onto the v0.2 envelope."""

    canonical_tick = SimTime(tick)
    return EventTemporalEnvelope(
        occurrence_id=event_id,
        delivery_id=event_id,
        occurred_at=canonical_tick,
        available_at=canonical_tick,
    )


__all__ = [
    "EventTemporalEnvelope",
    "ProcessingStamp",
    "SimTime",
    "legacy_temporal_envelope",
]
