"""Read-only qualified mental-transition audit projection.

This module measures versioned state changes after a run.  It neither updates
``HumanState`` nor claims that a qualified record is a unit of consciousness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
from typing import Iterable

from .models import HumanState, iter_unit_values
from .temporal import SimTime
from .trace import TickTrace


PERSISTENT_DESCRIPTIVE_FIELDS = (
    "body.energy",
    "body.arousal",
    "body.action_capacity",
    "access.attention_budget",
    "access.interference",
    "access.queue_load",
    "associative.rejection_access",
    "associative.ambiguity_sensitivity",
    "affective.residual_distress",
    "affective.update_rate",
    "habit.impulsivity",
    "habit.withdrawal_bias",
    "narrative.rejection_story",
    "narrative.relational_security",
    "relationship.stake",
    "relationship.trust",
    "relationship.boundary_strain",
)

DEFAULT_AVAILABLE_INFORMATION = (
    "current_observation_temporal_envelope",
    "current_state_before",
    "current_state_after",
    "current_state_delta",
)

Q_V1_QUALIFIER_ID = "persistent-descriptive-delta"
Q_V1_QUALIFIER_VERSION = "1.0.0"


class CanonicalWindowDuration(int):
    """Positive canonical-time width, distinct from transition count."""

    def __new__(cls, value: int) -> "CanonicalWindowDuration":
        if type(value) not in (int, CanonicalWindowDuration):
            raise TypeError("CanonicalWindowDuration requires a non-boolean int")
        if value <= 0:
            raise ValueError("CanonicalWindowDuration must be positive")
        return int.__new__(cls, value)


class QualifiedTransitionCount(int):
    """Non-negative count under one versioned qualifier."""

    def __new__(cls, value: int) -> "QualifiedTransitionCount":
        if type(value) not in (int, QualifiedTransitionCount):
            raise TypeError("QualifiedTransitionCount requires a non-boolean int")
        if value < 0:
            raise ValueError("QualifiedTransitionCount must be non-negative")
        return int.__new__(cls, value)


class QualifiedTransitionDensity(float):
    """Qualified count per canonical-time unit, not a subjective clock."""

    def __new__(cls, value: float) -> "QualifiedTransitionDensity":
        if type(value) not in (float, QualifiedTransitionDensity):
            raise TypeError(
                "QualifiedTransitionDensity requires a plain float from an "
                "explicit count / duration computation"
            )
        numeric = float(value)
        if not math.isfinite(numeric) or numeric < 0.0:
            raise ValueError("QualifiedTransitionDensity must be finite and non-negative")
        return float.__new__(cls, numeric)


@dataclass(frozen=True, slots=True)
class MentalTransitionQualificationPolicy:
    """Pre-registered Q for one narrow persistent-state checkpoint."""

    qualifier_id: str = Q_V1_QUALIFIER_ID
    qualifier_version: str = Q_V1_QUALIFIER_VERSION
    state_fields: tuple[str, ...] = PERSISTENT_DESCRIPTIVE_FIELDS
    minimum_absolute_delta: float = 0.01
    delta_unit: str = "normalized_simulation_unit"
    aggregation_window: str = "processed_occurrence"
    available_information: tuple[str, ...] = DEFAULT_AVAILABLE_INFORMATION

    def __post_init__(self) -> None:
        _require_tuple(self.state_fields, "state_fields")
        _require_tuple(self.available_information, "available_information")
        if (
            self.qualifier_id != Q_V1_QUALIFIER_ID
            or self.qualifier_version != Q_V1_QUALIFIER_VERSION
        ):
            raise ValueError("Q v1 qualifier identity and version are fixed")
        if not self.state_fields or len(set(self.state_fields)) != len(self.state_fields):
            raise ValueError("state_fields must be non-empty and unique")
        unknown = sorted(set(self.state_fields) - set(PERSISTENT_DESCRIPTIVE_FIELDS))
        if unknown:
            raise ValueError(f"unknown persistent descriptive fields: {unknown}")
        if (
            isinstance(self.minimum_absolute_delta, bool)
            or not isinstance(self.minimum_absolute_delta, (int, float))
            or not math.isfinite(float(self.minimum_absolute_delta))
            or not 0.0 < float(self.minimum_absolute_delta) <= 1.0
        ):
            raise ValueError("minimum_absolute_delta must be finite and in (0, 1]")
        object.__setattr__(
            self, "minimum_absolute_delta", float(self.minimum_absolute_delta)
        )
        if self.delta_unit != "normalized_simulation_unit":
            raise ValueError("Q v1 supports only normalized_simulation_unit")
        if self.aggregation_window != "processed_occurrence":
            raise ValueError("Q v1 supports only processed_occurrence aggregation")
        if self.available_information != DEFAULT_AVAILABLE_INFORMATION:
            raise ValueError(
                "Q v1 available_information is fixed to current-trace inputs"
            )

    @property
    def policy_digest(self) -> str:
        return _stable_digest(
            {
                "qualifier_id": self.qualifier_id,
                "qualifier_version": self.qualifier_version,
                "state_fields": self.state_fields,
                "minimum_absolute_delta": self.minimum_absolute_delta,
                "delta_unit": self.delta_unit,
                "aggregation_window": self.aggregation_window,
                "available_information": self.available_information,
            }
        )


@dataclass(frozen=True, slots=True)
class MentalStateDelta:
    field: str
    before: float
    after: float
    delta: float
    unit: str

    def __post_init__(self) -> None:
        if not self.field or not self.unit:
            raise ValueError("delta field and unit must be non-empty")
        values = (self.before, self.after, self.delta)
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(float(value))
            for value in values
        ):
            raise ValueError("mental-state delta values must be finite")
        object.__setattr__(self, "before", float(self.before))
        object.__setattr__(self, "after", float(self.after))
        object.__setattr__(self, "delta", float(self.delta))
        if abs((self.after - self.before) - self.delta) > 1e-12:
            raise ValueError("delta must equal after - before")

    @property
    def absolute_delta(self) -> float:
        return abs(self.delta)


@dataclass(frozen=True, slots=True)
class TransitionQualificationReceipt:
    receipt_id: str
    qualifier_id: str
    qualifier_version: str
    policy_digest: str
    qualified: bool
    processed_at: SimTime
    qualified_at: SimTime
    processing_sequence: int
    cause_occurrence_id: str
    cause_delivery_id: str
    reexposure_of_occurrence_id: str | None
    cause_occurred_at: SimTime
    became_available_at: SimTime
    state_scope: tuple[str, ...]
    aggregation_window: str
    minimum_absolute_delta: float
    delta_unit: str
    available_information: tuple[str, ...]
    typed_deltas: tuple[MentalStateDelta, ...]
    qualifying_fields: tuple[str, ...]
    before_digest: str
    after_digest: str

    def __post_init__(self) -> None:
        _require_tuple(self.state_scope, "state_scope")
        _require_tuple(self.available_information, "available_information")
        _require_tuple(self.typed_deltas, "typed_deltas")
        _require_tuple(self.qualifying_fields, "qualifying_fields")
        for value, name in (
            (self.receipt_id, "receipt_id"),
            (self.qualifier_id, "qualifier_id"),
            (self.qualifier_version, "qualifier_version"),
            (self.cause_occurrence_id, "cause_occurrence_id"),
            (self.cause_delivery_id, "cause_delivery_id"),
            (self.aggregation_window, "aggregation_window"),
            (self.delta_unit, "delta_unit"),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")
        object.__setattr__(self, "cause_occurred_at", SimTime(self.cause_occurred_at))
        object.__setattr__(self, "became_available_at", SimTime(self.became_available_at))
        object.__setattr__(self, "processed_at", SimTime(self.processed_at))
        object.__setattr__(self, "qualified_at", SimTime(self.qualified_at))
        if not (
            self.cause_occurred_at
            <= self.became_available_at
            <= self.processed_at
        ):
            raise ValueError("qualification receipt temporal order is invalid")
        if self.reexposure_of_occurrence_id is not None:
            if not self.reexposure_of_occurrence_id:
                raise ValueError("reexposure_of_occurrence_id must be non-empty")
            if self.reexposure_of_occurrence_id == self.cause_occurrence_id:
                raise ValueError("a reexposure cannot refer to its own occurrence")
        if self.qualified_at != self.processed_at:
            raise ValueError("qualified_at must equal the checkpoint processed_at")
        if type(self.processing_sequence) is not int or self.processing_sequence < 1:
            raise ValueError("processing_sequence must be positive")
        if (
            isinstance(self.minimum_absolute_delta, bool)
            or not isinstance(self.minimum_absolute_delta, (int, float))
            or not math.isfinite(float(self.minimum_absolute_delta))
            or not 0.0 < float(self.minimum_absolute_delta) <= 1.0
        ):
            raise ValueError("receipt threshold must be finite and in (0, 1]")
        if not self.state_scope or len(set(self.state_scope)) != len(self.state_scope):
            raise ValueError("state_scope must be non-empty and unique")
        if self.qualified != bool(self.qualifying_fields):
            raise ValueError("qualified must match qualifying_fields")
        deltas_by_field = {delta.field: delta for delta in self.typed_deltas}
        if len(deltas_by_field) != len(self.typed_deltas):
            raise ValueError("typed delta fields must be unique")
        delta_fields = set(deltas_by_field)
        if not delta_fields <= set(self.state_scope):
            raise ValueError("typed deltas must stay within state_scope")
        if any(delta.unit != self.delta_unit for delta in self.typed_deltas):
            raise ValueError("typed delta units must match the receipt unit")
        if not set(self.qualifying_fields) <= delta_fields:
            raise ValueError("qualifying fields must refer to typed deltas")
        expected_qualifying = tuple(
            delta.field
            for delta in self.typed_deltas
            if delta.absolute_delta + 1e-12 >= self.minimum_absolute_delta
        )
        if self.qualifying_fields != expected_qualifying:
            raise ValueError("qualifying_fields do not match the declared threshold")
        _validate_digest(self.policy_digest, "policy_digest")
        _validate_digest(self.before_digest, "before_digest")
        _validate_digest(self.after_digest, "after_digest")


@dataclass(frozen=True, slots=True)
class MentalTransition:
    transition_id: str
    qualifier_id: str
    qualifier_version: str
    policy_digest: str
    cause_occurrence_id: str
    cause_delivery_id: str
    reexposure_of_occurrence_id: str | None
    cause_occurred_at: SimTime
    became_available_at: SimTime
    transition_effective_at: SimTime
    processed_at: SimTime
    qualified_at: SimTime
    processing_sequence: int
    state_scope: tuple[str, ...]
    aggregation_window: str
    typed_deltas: tuple[MentalStateDelta, ...]
    before_digest: str
    after_digest: str
    qualification_receipt_id: str

    def __post_init__(self) -> None:
        _require_tuple(self.state_scope, "state_scope")
        _require_tuple(self.typed_deltas, "typed_deltas")
        for name in (
            "cause_occurred_at",
            "became_available_at",
            "transition_effective_at",
            "processed_at",
            "qualified_at",
        ):
            object.__setattr__(self, name, SimTime(getattr(self, name)))
        for value, name in (
            (self.transition_id, "transition_id"),
            (self.qualifier_id, "qualifier_id"),
            (self.qualifier_version, "qualifier_version"),
            (self.cause_occurrence_id, "cause_occurrence_id"),
            (self.cause_delivery_id, "cause_delivery_id"),
            (self.aggregation_window, "aggregation_window"),
            (self.qualification_receipt_id, "qualification_receipt_id"),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")
        if self.reexposure_of_occurrence_id is not None:
            if not self.reexposure_of_occurrence_id:
                raise ValueError("reexposure_of_occurrence_id must be non-empty")
            if self.reexposure_of_occurrence_id == self.cause_occurrence_id:
                raise ValueError("a reexposure cannot refer to its own occurrence")
        if not (
            self.cause_occurred_at
            <= self.became_available_at
            <= self.processed_at
        ):
            raise ValueError("mental-transition temporal order is invalid")
        if self.transition_effective_at != self.processed_at:
            raise ValueError("Q v1 transition_effective_at must equal processed_at")
        if self.qualified_at != self.processed_at:
            raise ValueError("Q v1 qualified_at must equal processed_at")
        if type(self.processing_sequence) is not int or self.processing_sequence < 1:
            raise ValueError("processing_sequence must be positive")
        _validate_digest(self.policy_digest, "policy_digest")
        _validate_digest(self.before_digest, "before_digest")
        _validate_digest(self.after_digest, "after_digest")


@dataclass(frozen=True, slots=True)
class MentalTransitionWindowReport:
    qualifier_id: str
    qualifier_version: str
    policy_digest: str
    start: SimTime
    end: SimTime
    canonical_duration: CanonicalWindowDuration
    qualified_count: QualifiedTransitionCount
    density_per_sim_time: QualifiedTransitionDensity

    def __post_init__(self) -> None:
        object.__setattr__(self, "start", SimTime(self.start))
        object.__setattr__(self, "end", SimTime(self.end))
        if type(self.canonical_duration) is not CanonicalWindowDuration:
            raise TypeError("canonical_duration must be CanonicalWindowDuration")
        if type(self.qualified_count) is not QualifiedTransitionCount:
            raise TypeError("qualified_count must be QualifiedTransitionCount")
        if type(self.density_per_sim_time) is not QualifiedTransitionDensity:
            raise TypeError(
                "density_per_sim_time must be QualifiedTransitionDensity"
            )
        if int(self.end - self.start) != int(self.canonical_duration):
            raise ValueError("canonical_duration must equal end - start")
        expected_density = float(self.qualified_count) / float(
            self.canonical_duration
        )
        if abs(float(self.density_per_sim_time) - expected_density) > 1e-12:
            raise ValueError("density must equal qualified count / duration")
        _validate_digest(self.policy_digest, "policy_digest")


@dataclass(frozen=True, slots=True)
class MentalTransitionLedger:
    policy: MentalTransitionQualificationPolicy = field(
        default_factory=MentalTransitionQualificationPolicy
    )
    receipts: tuple[TransitionQualificationReceipt, ...] = ()
    transitions: tuple[MentalTransition, ...] = ()

    def __post_init__(self) -> None:
        if type(self.policy) is not MentalTransitionQualificationPolicy:
            raise TypeError("policy must be MentalTransitionQualificationPolicy")
        _require_tuple(self.receipts, "receipts")
        _require_tuple(self.transitions, "transitions")
        if any(
            type(receipt) is not TransitionQualificationReceipt
            for receipt in self.receipts
        ):
            raise TypeError(
                "receipts must contain TransitionQualificationReceipt values"
            )
        if any(
            type(transition) is not MentalTransition
            for transition in self.transitions
        ):
            raise TypeError("transitions must contain MentalTransition values")
        sequences = [receipt.processing_sequence for receipt in self.receipts]
        if sequences != list(range(1, len(sequences) + 1)):
            raise ValueError(
                "qualification receipts must cover the complete processing order"
            )
        seen_occurrences: dict[str, TransitionQualificationReceipt] = {}
        for receipt in self.receipts:
            source_occurrence = receipt.reexposure_of_occurrence_id
            if source_occurrence is not None:
                source_receipt = seen_occurrences.get(source_occurrence)
                if source_receipt is None:
                    raise ValueError(
                        "reexposure provenance must reference an earlier processed occurrence"
                    )
                if receipt.cause_occurred_at < source_receipt.processed_at:
                    raise ValueError(
                        "reexposure occurrence cannot predate source processing"
                    )
            seen_occurrences[receipt.cause_occurrence_id] = receipt
        receipt_ids = [receipt.receipt_id for receipt in self.receipts]
        receipt_occurrence_ids = [
            receipt.cause_occurrence_id for receipt in self.receipts
        ]
        receipt_delivery_ids = [
            receipt.cause_delivery_id for receipt in self.receipts
        ]
        transition_ids = [transition.transition_id for transition in self.transitions]
        if len(receipt_ids) != len(set(receipt_ids)):
            raise ValueError("qualification receipt IDs must be unique")
        if len(receipt_occurrence_ids) != len(set(receipt_occurrence_ids)):
            raise ValueError("processed occurrences may have only one receipt")
        if len(receipt_delivery_ids) != len(set(receipt_delivery_ids)):
            raise ValueError("processed deliveries may have only one receipt")
        if len(transition_ids) != len(set(transition_ids)):
            raise ValueError("mental transition IDs must be unique")
        receipts = {receipt.receipt_id: receipt for receipt in self.receipts}
        qualified_receipt_ids = {
            receipt.receipt_id for receipt in self.receipts if receipt.qualified
        }
        transition_receipt_id_list = [
            transition.qualification_receipt_id for transition in self.transitions
        ]
        transition_receipt_ids = set(transition_receipt_id_list)
        if len(transition_receipt_id_list) != len(transition_receipt_ids):
            raise ValueError("a qualified receipt may create only one transition")
        if qualified_receipt_ids != transition_receipt_ids:
            raise ValueError("qualified receipts and transitions must be one-to-one")
        policy_digest = self.policy.policy_digest
        for receipt in self.receipts:
            if (
                receipt.qualifier_id != self.policy.qualifier_id
                or receipt.qualifier_version != self.policy.qualifier_version
                or receipt.policy_digest != policy_digest
                or receipt.state_scope != self.policy.state_fields
                or receipt.aggregation_window != self.policy.aggregation_window
                or receipt.minimum_absolute_delta
                != self.policy.minimum_absolute_delta
                or receipt.delta_unit != self.policy.delta_unit
                or receipt.available_information
                != self.policy.available_information
            ):
                raise ValueError("qualification receipt does not match ledger policy")
        for transition in self.transitions:
            receipt = receipts.get(transition.qualification_receipt_id)
            if receipt is None or not receipt.qualified:
                raise ValueError("every transition must reference a qualified receipt")
            if transition.policy_digest != policy_digest:
                raise ValueError("transition policy digest mismatch")
            if (
                transition.processing_sequence != receipt.processing_sequence
                or transition.cause_occurrence_id != receipt.cause_occurrence_id
                or transition.cause_delivery_id != receipt.cause_delivery_id
                or transition.reexposure_of_occurrence_id
                != receipt.reexposure_of_occurrence_id
                or transition.cause_occurred_at != receipt.cause_occurred_at
                or transition.became_available_at != receipt.became_available_at
                or transition.qualifier_id != receipt.qualifier_id
                or transition.qualifier_version != receipt.qualifier_version
                or transition.state_scope != receipt.state_scope
                or transition.aggregation_window != receipt.aggregation_window
                or transition.typed_deltas != receipt.typed_deltas
                or transition.before_digest != receipt.before_digest
                or transition.after_digest != receipt.after_digest
                or transition.qualified_at != receipt.qualified_at
                or transition.processed_at != receipt.processed_at
            ):
                raise ValueError("transition does not match its qualification receipt")
        transition_sequences = [
            transition.processing_sequence for transition in self.transitions
        ]
        if transition_sequences != sorted(transition_sequences):
            raise ValueError("mental transitions must follow processing order")

    def window_report(
        self,
        start: SimTime | int,
        end: SimTime | int,
    ) -> MentalTransitionWindowReport:
        canonical_start = SimTime(start)
        canonical_end = SimTime(end)
        duration = CanonicalWindowDuration(int(canonical_end - canonical_start))
        count = QualifiedTransitionCount(
            sum(
                canonical_start <= transition.transition_effective_at < canonical_end
                for transition in self.transitions
            )
        )
        density = QualifiedTransitionDensity(float(count) / float(duration))
        return MentalTransitionWindowReport(
            qualifier_id=self.policy.qualifier_id,
            qualifier_version=self.policy.qualifier_version,
            policy_digest=self.policy.policy_digest,
            start=canonical_start,
            end=canonical_end,
            canonical_duration=duration,
            qualified_count=count,
            density_per_sim_time=density,
        )


def _stable_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _require_tuple(value: object, name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an immutable tuple")


def _validate_digest(value: str, name: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


def _state_projection(
    state: HumanState,
    fields: tuple[str, ...],
) -> tuple[tuple[str, float], ...]:
    values = dict(iter_unit_values(state))
    missing = [name for name in fields if name not in values]
    if missing:
        raise ValueError(f"state projection is missing declared fields: {missing}")
    return tuple((name, values[name]) for name in fields)


def build_mental_transition_ledger(
    traces: Iterable[TickTrace],
    policy: MentalTransitionQualificationPolicy | None = None,
) -> MentalTransitionLedger:
    """Derive immutable Q receipts after execution, with no model feedback."""

    qualifier = policy or MentalTransitionQualificationPolicy()
    policy_identity = qualifier.policy_digest[:16]
    receipts: list[TransitionQualificationReceipt] = []
    transitions: list[MentalTransition] = []
    for trace in traces:
        observation = trace.observation
        stamp = observation.processing_stamp
        sequence = trace.processing_sequence
        if stamp is None or sequence is None:
            raise ValueError("mental-transition projection requires canonical processing stamps")
        if stamp.processing_sequence != sequence:
            raise ValueError("trace and observation processing sequence mismatch")

        before = _state_projection(trace.state_before, qualifier.state_fields)
        after = _state_projection(trace.state_after, qualifier.state_fields)
        deltas = tuple(
            MentalStateDelta(
                field=name,
                before=before_value,
                after=after_value,
                delta=after_value - before_value,
                unit=qualifier.delta_unit,
            )
            for (name, before_value), (_, after_value) in zip(before, after)
            if abs(after_value - before_value) > 1e-12
        )
        qualifying_fields = tuple(
            delta.field
            for delta in deltas
            if delta.absolute_delta + 1e-12 >= qualifier.minimum_absolute_delta
        )
        before_digest = _stable_digest(before)
        after_digest = _stable_digest(after)
        receipt_id = (
            f"mental-transition-q:{qualifier.qualifier_id}@"
            f"{qualifier.qualifier_version}:{policy_identity}:"
            f"{sequence}:{observation.occurrence_id}"
        )
        receipt = TransitionQualificationReceipt(
            receipt_id=receipt_id,
            qualifier_id=qualifier.qualifier_id,
            qualifier_version=qualifier.qualifier_version,
            policy_digest=qualifier.policy_digest,
            qualified=bool(qualifying_fields),
            processed_at=observation.processed_at,
            qualified_at=observation.processed_at,
            processing_sequence=sequence,
            cause_occurrence_id=observation.occurrence_id,
            cause_delivery_id=observation.delivery_id,
            reexposure_of_occurrence_id=(
                stamp.envelope.reexposure_of_occurrence_id
            ),
            cause_occurred_at=observation.occurred_at,
            became_available_at=observation.available_at,
            state_scope=qualifier.state_fields,
            aggregation_window=qualifier.aggregation_window,
            minimum_absolute_delta=qualifier.minimum_absolute_delta,
            delta_unit=qualifier.delta_unit,
            available_information=qualifier.available_information,
            typed_deltas=deltas,
            qualifying_fields=qualifying_fields,
            before_digest=before_digest,
            after_digest=after_digest,
        )
        receipts.append(receipt)
        if not receipt.qualified:
            continue
        envelope = stamp.envelope
        transitions.append(
            MentalTransition(
                transition_id=(
                    f"mental-transition:{qualifier.qualifier_id}@"
                    f"{qualifier.qualifier_version}:{policy_identity}:"
                    f"{sequence}:{observation.occurrence_id}"
                ),
                qualifier_id=qualifier.qualifier_id,
                qualifier_version=qualifier.qualifier_version,
                policy_digest=qualifier.policy_digest,
                cause_occurrence_id=observation.occurrence_id,
                cause_delivery_id=observation.delivery_id,
                reexposure_of_occurrence_id=(
                    envelope.reexposure_of_occurrence_id
                ),
                cause_occurred_at=observation.occurred_at,
                became_available_at=observation.available_at,
                transition_effective_at=observation.processed_at,
                processed_at=observation.processed_at,
                qualified_at=observation.processed_at,
                processing_sequence=sequence,
                state_scope=qualifier.state_fields,
                aggregation_window=qualifier.aggregation_window,
                typed_deltas=deltas,
                before_digest=before_digest,
                after_digest=after_digest,
                qualification_receipt_id=receipt_id,
            )
        )
    return MentalTransitionLedger(
        policy=qualifier,
        receipts=tuple(receipts),
        transitions=tuple(transitions),
    )


__all__ = [
    "CanonicalWindowDuration",
    "DEFAULT_AVAILABLE_INFORMATION",
    "MentalStateDelta",
    "MentalTransition",
    "MentalTransitionLedger",
    "MentalTransitionQualificationPolicy",
    "MentalTransitionWindowReport",
    "PERSISTENT_DESCRIPTIVE_FIELDS",
    "Q_V1_QUALIFIER_ID",
    "Q_V1_QUALIFIER_VERSION",
    "QualifiedTransitionCount",
    "QualifiedTransitionDensity",
    "TransitionQualificationReceipt",
    "build_mental_transition_ledger",
]
