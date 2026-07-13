"""Read-only MORPH-001B comparison of reducer proposals with declared bands.

The bands in this module are experimenter-declared simulation parameters.
They are not measurements of human accommodation capacity.  The resulting
profiles are proposal-envelope proxies, not deformation demand, residual
strain, morphic load, qualia, or subjective time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math

from .models.proposals import (
    REDUCER_MANDATORY_OPERATOR_SPECS,
    REDUCER_OPTIONAL_OPERATOR_SPECS,
    ReducerFieldProposal,
)
from .reducer_proposals import (
    REDUCER_PROPOSAL_MODEL_ID,
    REDUCER_PROPOSAL_MODEL_VERSION,
    ReducerProposalLedger,
    ReducerProposalReceipt,
)
from .temporal import SimTime


def _require_nonempty_string(value: object, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be an immutable string")
    if not value:
        raise ValueError(f"{name} must be non-empty")


REDUCER_ENVELOPE_COMPARISON_MODEL_ID = (
    "reducer-proposal-envelope-comparison"
)
REDUCER_ENVELOPE_COMPARISON_MODEL_VERSION = "1.0.0"
REDUCER_ENVELOPE_OPERATOR_ID = "componentwise-signed-exceedance"
REDUCER_ENVELOPE_OPERATOR_VERSION = "1.0.0"
REDUCER_ENVELOPE_AGGREGATION_WINDOW = "reducer_write"
REDUCER_ENVELOPE_INPUT_KIND = "morph-001a-reducer-proposal-proxy"
REDUCER_ENVELOPE_AVAILABLE_INFORMATION = (
    "source_reducer_proposal_receipt",
    "source_pre_update_state_projection_digest",
    "experimenter_declared_simulation_band",
)


def _ordered_unique_proposal_fields() -> tuple[str, ...]:
    fields: list[str] = []
    for spec in (
        *REDUCER_MANDATORY_OPERATOR_SPECS,
        *REDUCER_OPTIONAL_OPERATOR_SPECS,
    ):
        if spec.field not in fields:
            fields.append(spec.field)
    return tuple(fields)


REDUCER_ENVELOPE_FIELDS = _ordered_unique_proposal_fields()


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopeBand:
    """One declared signed reducer-write comparison band."""

    field: str
    lower_delta: float
    upper_delta: float
    unit: str = "normalized_simulation_unit"

    def __post_init__(self) -> None:
        _require_nonempty_string(self.field, "envelope band field")
        if self.unit != "normalized_simulation_unit":
            raise ValueError(
                "envelope band unit must be normalized_simulation_unit"
            )
        for name in ("lower_delta", "upper_delta"):
            value = getattr(self, name)
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(float(value))
            ):
                raise ValueError("envelope band deltas must be finite")
            object.__setattr__(self, name, float(value))
        if not self.lower_delta <= 0.0 <= self.upper_delta:
            raise ValueError("envelope band must contain zero")
        if self.lower_delta == self.upper_delta:
            raise ValueError("envelope band must admit a non-zero direction")


_SYNTHETIC_BAND_LIMITS = {
    "body.energy": (-0.08, 0.05),
    "body.arousal": (-0.06, 0.08),
    "body.action_capacity": (-0.08, 0.05),
    "access.attention_budget": (-0.06, 0.04),
    "access.interference": (-0.05, 0.07),
    "access.queue_load": (-0.07, 0.05),
    "relationship.trust": (-0.04, 0.025),
    "relationship.boundary_strain": (-0.05, 0.07),
    "associative.rejection_access": (-0.04, 0.06),
    "associative.ambiguity_sensitivity": (-0.05, 0.06),
    "affective.residual_distress": (-0.05, 0.07),
    "narrative.rejection_story": (-0.03, 0.05),
    "narrative.relational_security": (-0.05, 0.03),
    "habit.impulsivity": (-0.04, 0.05),
}

MORPH_001B_SYNTHETIC_FIELD_BANDS = tuple(
    ReducerProposalEnvelopeBand(
        field=field,
        lower_delta=_SYNTHETIC_BAND_LIMITS[field][0],
        upper_delta=_SYNTHETIC_BAND_LIMITS[field][1],
    )
    for field in REDUCER_ENVELOPE_FIELDS
)


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopePolicy:
    """Versioned simulation-only band and componentwise comparison policy."""

    policy_id: str = "synthetic-asymmetric-reducer-write-envelope"
    policy_version: str = "1.0.0"
    field_bands: tuple[ReducerProposalEnvelopeBand, ...] = (
        MORPH_001B_SYNTHETIC_FIELD_BANDS
    )
    measurement_model_id: str = REDUCER_ENVELOPE_COMPARISON_MODEL_ID
    measurement_model_version: str = (
        REDUCER_ENVELOPE_COMPARISON_MODEL_VERSION
    )
    source_measurement_model_id: str = REDUCER_PROPOSAL_MODEL_ID
    source_measurement_model_version: str = REDUCER_PROPOSAL_MODEL_VERSION
    comparison_operator_id: str = REDUCER_ENVELOPE_OPERATOR_ID
    comparison_operator_version: str = REDUCER_ENVELOPE_OPERATOR_VERSION
    aggregation_window: str = REDUCER_ENVELOPE_AGGREGATION_WINDOW
    input_kind: str = REDUCER_ENVELOPE_INPUT_KIND
    unit: str = "normalized_simulation_unit"
    capacity_depletion: str = "not_modeled"
    cross_write_redistribution: str = "not_modeled"
    available_information: tuple[str, ...] = (
        REDUCER_ENVELOPE_AVAILABLE_INFORMATION
    )

    def __post_init__(self) -> None:
        _require_tuple(self.field_bands, "field_bands")
        _require_tuple(self.available_information, "available_information")
        if any(
            type(band) is not ReducerProposalEnvelopeBand
            for band in self.field_bands
        ):
            raise TypeError(
                "field_bands must contain ReducerProposalEnvelopeBand values"
            )
        if tuple(band.field for band in self.field_bands) != REDUCER_ENVELOPE_FIELDS:
            raise ValueError(
                "envelope policy fields must match the exact reducer proposal scope"
            )
        _require_nonempty_string(self.policy_id, "policy_id")
        _require_nonempty_string(self.policy_version, "policy_version")
        if (
            self.measurement_model_id
            != REDUCER_ENVELOPE_COMPARISON_MODEL_ID
            or self.measurement_model_version
            != REDUCER_ENVELOPE_COMPARISON_MODEL_VERSION
        ):
            raise ValueError("envelope comparison measurement identity is fixed")
        if (
            self.source_measurement_model_id != REDUCER_PROPOSAL_MODEL_ID
            or self.source_measurement_model_version
            != REDUCER_PROPOSAL_MODEL_VERSION
        ):
            raise ValueError("envelope comparison source identity is fixed")
        if (
            self.comparison_operator_id != REDUCER_ENVELOPE_OPERATOR_ID
            or self.comparison_operator_version
            != REDUCER_ENVELOPE_OPERATOR_VERSION
        ):
            raise ValueError("envelope comparison operator identity is fixed")
        if self.aggregation_window != REDUCER_ENVELOPE_AGGREGATION_WINDOW:
            raise ValueError("envelope comparison aggregation window is fixed")
        if self.input_kind != REDUCER_ENVELOPE_INPUT_KIND:
            raise ValueError("envelope comparison input kind is fixed")
        if self.unit != "normalized_simulation_unit":
            raise ValueError("envelope comparison unit is fixed")
        if self.capacity_depletion != "not_modeled":
            raise ValueError("capacity depletion is not modeled in MORPH-001B")
        if self.cross_write_redistribution != "not_modeled":
            raise ValueError(
                "cross-write redistribution is not modeled in MORPH-001B"
            )
        if self.available_information != REDUCER_ENVELOPE_AVAILABLE_INFORMATION:
            raise ValueError("envelope comparison available information is fixed")

    def band_for(self, field: str) -> ReducerProposalEnvelopeBand:
        for band in self.field_bands:
            if band.field == field:
                return band
        raise KeyError(field)

    @property
    def policy_digest(self) -> str:
        return _stable_digest(
            {
                "policy_id": self.policy_id,
                "policy_version": self.policy_version,
                "field_bands": tuple(_band_payload(band) for band in self.field_bands),
                "measurement_model_id": self.measurement_model_id,
                "measurement_model_version": self.measurement_model_version,
                "source_measurement_model_id": self.source_measurement_model_id,
                "source_measurement_model_version": (
                    self.source_measurement_model_version
                ),
                "comparison_operator_id": self.comparison_operator_id,
                "comparison_operator_version": self.comparison_operator_version,
                "aggregation_window": self.aggregation_window,
                "input_kind": self.input_kind,
                "unit": self.unit,
                "capacity_depletion": self.capacity_depletion,
                "cross_write_redistribution": self.cross_write_redistribution,
                "available_information": self.available_information,
            }
        )


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopeSnapshot:
    """Declared bands bound to one source receipt's pre-update context."""

    snapshot_id: str
    policy_digest: str
    source_proposal_receipt_id: str
    source_state_before_digest: str
    evaluated_at: SimTime
    field_bands: tuple[ReducerProposalEnvelopeBand, ...]

    def __post_init__(self) -> None:
        _require_tuple(self.field_bands, "field_bands")
        if any(
            type(band) is not ReducerProposalEnvelopeBand
            for band in self.field_bands
        ):
            raise TypeError(
                "field_bands must contain ReducerProposalEnvelopeBand values"
            )
        if tuple(band.field for band in self.field_bands) != REDUCER_ENVELOPE_FIELDS:
            raise ValueError(
                "envelope snapshot fields must match the exact proposal scope"
            )
        _require_nonempty_string(self.snapshot_id, "snapshot_id")
        _require_nonempty_string(
            self.source_proposal_receipt_id,
            "source_proposal_receipt_id",
        )
        _validate_digest(self.policy_digest, "policy_digest")
        _validate_digest(self.source_state_before_digest, "source_state_before_digest")
        object.__setattr__(self, "evaluated_at", SimTime(self.evaluated_at))
        expected = _snapshot_id(
            self.policy_digest,
            self.source_proposal_receipt_id,
            self.source_state_before_digest,
            self.evaluated_at,
            self.field_bands,
        )
        if self.snapshot_id != expected:
            raise ValueError("snapshot_id does not match envelope snapshot content")

    def band_for(self, field: str) -> ReducerProposalEnvelopeBand:
        for band in self.field_bands:
            if band.field == field:
                return band
        raise KeyError(field)


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopeComparison:
    """One ordered componentwise comparison; no occurrence aggregate is implied."""

    write_sequence: int
    source_stage_id: str
    source_operator_id: str
    field: str
    source_constraint_id: str
    basis_before: float
    requested_delta: float
    committed_delta: float
    lower_delta: float
    upper_delta: float
    band_limited_delta: float
    signed_proxy_excess: float
    unit: str
    comparison_operator_id: str
    comparison_operator_version: str

    def __post_init__(self) -> None:
        if type(self.write_sequence) is not int or self.write_sequence < 1:
            raise ValueError("comparison write_sequence must be a positive int")
        for value, name in (
            (self.source_stage_id, "source_stage_id"),
            (self.source_operator_id, "source_operator_id"),
            (self.field, "field"),
            (self.source_constraint_id, "source_constraint_id"),
        ):
            _require_nonempty_string(value, name)
        if self.source_constraint_id != "clamp01":
            raise ValueError("source constraint identity must remain clamp01")
        if self.unit != "normalized_simulation_unit":
            raise ValueError("comparison unit must be normalized_simulation_unit")
        if (
            self.comparison_operator_id != REDUCER_ENVELOPE_OPERATOR_ID
            or self.comparison_operator_version
            != REDUCER_ENVELOPE_OPERATOR_VERSION
        ):
            raise ValueError("comparison operator identity is fixed")
        for name in (
            "basis_before",
            "requested_delta",
            "committed_delta",
            "lower_delta",
            "upper_delta",
            "band_limited_delta",
            "signed_proxy_excess",
        ):
            value = getattr(self, name)
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(float(value))
            ):
                raise ValueError("comparison values must be finite")
            object.__setattr__(self, name, float(value))
        if not self.lower_delta <= 0.0 <= self.upper_delta:
            raise ValueError("comparison band must contain zero")
        if self.lower_delta == self.upper_delta:
            raise ValueError("comparison band must admit a non-zero direction")
        expected_limited = _clip_signed(
            self.requested_delta,
            self.lower_delta,
            self.upper_delta,
        )
        if abs(self.band_limited_delta - expected_limited) > 1e-12:
            raise ValueError("band_limited_delta does not match policy clipping")
        if (
            abs(
                self.signed_proxy_excess
                - (self.requested_delta - self.band_limited_delta)
            )
            > 1e-12
        ):
            raise ValueError(
                "signed_proxy_excess must equal requested minus band-limited delta"
            )

    @property
    def absolute_proxy_excess(self) -> float:
        return abs(self.signed_proxy_excess)


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopeReceipt:
    receipt_id: str
    measurement_model_id: str
    measurement_model_version: str
    policy_digest: str
    source_proposal_policy_digest: str
    source_proposal_receipt_id: str
    source_proposal_digest: str
    source_state_before_digest: str
    captured_at: SimTime
    processing_sequence: int
    cause_occurrence_id: str
    cause_delivery_id: str
    reexposure_of_occurrence_id: str | None
    cause_occurred_at: SimTime
    became_available_at: SimTime
    processed_at: SimTime
    snapshot: ReducerProposalEnvelopeSnapshot
    comparisons: tuple[ReducerProposalEnvelopeComparison, ...]
    comparison_digest: str

    def __post_init__(self) -> None:
        _require_tuple(self.comparisons, "comparisons")
        if type(self.snapshot) is not ReducerProposalEnvelopeSnapshot:
            raise TypeError("snapshot must be ReducerProposalEnvelopeSnapshot")
        if any(
            type(item) is not ReducerProposalEnvelopeComparison
            for item in self.comparisons
        ):
            raise TypeError(
                "comparisons must contain ReducerProposalEnvelopeComparison values"
            )
        for value, name in (
            (self.receipt_id, "receipt_id"),
            (self.measurement_model_id, "measurement_model_id"),
            (self.measurement_model_version, "measurement_model_version"),
            (self.source_proposal_receipt_id, "source_proposal_receipt_id"),
            (self.cause_occurrence_id, "cause_occurrence_id"),
            (self.cause_delivery_id, "cause_delivery_id"),
        ):
            _require_nonempty_string(value, name)
        if (
            self.measurement_model_id != REDUCER_ENVELOPE_COMPARISON_MODEL_ID
            or self.measurement_model_version
            != REDUCER_ENVELOPE_COMPARISON_MODEL_VERSION
        ):
            raise ValueError("comparison receipt measurement identity is fixed")
        for name in (
            "policy_digest",
            "source_proposal_policy_digest",
            "source_proposal_digest",
            "source_state_before_digest",
            "comparison_digest",
        ):
            _validate_digest(getattr(self, name), name)
        for name in (
            "captured_at",
            "cause_occurred_at",
            "became_available_at",
            "processed_at",
        ):
            object.__setattr__(self, name, SimTime(getattr(self, name)))
        if not (
            self.cause_occurred_at
            <= self.became_available_at
            <= self.processed_at
        ):
            raise ValueError("comparison receipt temporal order is invalid")
        if self.captured_at != self.processed_at:
            raise ValueError("comparison receipt captured_at must equal processed_at")
        if type(self.processing_sequence) is not int or self.processing_sequence < 1:
            raise ValueError("processing_sequence must be a positive int")
        if self.reexposure_of_occurrence_id is not None:
            _require_nonempty_string(
                self.reexposure_of_occurrence_id,
                "reexposure_of_occurrence_id",
            )
            if self.reexposure_of_occurrence_id == self.cause_occurrence_id:
                raise ValueError("a reexposure cannot refer to its own occurrence")
        if not self.comparisons:
            raise ValueError("comparison receipt must preserve every proposal write")
        sequences = [item.write_sequence for item in self.comparisons]
        if sequences != list(range(1, len(sequences) + 1)):
            raise ValueError("comparisons must preserve complete proposal write order")
        if self.snapshot.policy_digest != self.policy_digest:
            raise ValueError("snapshot and receipt policy digests differ")
        if self.snapshot.source_proposal_receipt_id != self.source_proposal_receipt_id:
            raise ValueError("snapshot and receipt source proposal identities differ")
        if self.snapshot.source_state_before_digest != self.source_state_before_digest:
            raise ValueError("snapshot and receipt pre-update projection digests differ")
        if self.snapshot.evaluated_at != self.processed_at:
            raise ValueError("snapshot must be evaluated at source processing time")
        for item in self.comparisons:
            band = self.snapshot.band_for(item.field)
            if (
                abs(item.lower_delta - band.lower_delta) > 1e-12
                or abs(item.upper_delta - band.upper_delta) > 1e-12
                or item.unit != band.unit
            ):
                raise ValueError("comparison component does not match snapshot band")
        if self.comparison_digest != _comparison_digest(self.comparisons):
            raise ValueError("comparison_digest does not match ordered components")
        expected = _receipt_id(
            self.measurement_model_id,
            self.measurement_model_version,
            self.policy_digest,
            self.source_proposal_policy_digest,
            self.source_proposal_receipt_id,
            self.source_proposal_digest,
            self.source_state_before_digest,
            self.processing_sequence,
            self.cause_occurrence_id,
            self.cause_delivery_id,
            self.reexposure_of_occurrence_id,
            self.cause_occurred_at,
            self.became_available_at,
            self.processed_at,
            self.snapshot.snapshot_id,
            self.comparison_digest,
        )
        if self.receipt_id != expected:
            raise ValueError("receipt_id does not match canonical comparison identity")


@dataclass(frozen=True, slots=True)
class ReducerProposalEnvelopeLedger:
    policy: ReducerProposalEnvelopePolicy = field(
        default_factory=ReducerProposalEnvelopePolicy
    )
    source_proposal_policy_digest: str = ""
    receipts: tuple[ReducerProposalEnvelopeReceipt, ...] = ()

    def __post_init__(self) -> None:
        if type(self.policy) is not ReducerProposalEnvelopePolicy:
            raise TypeError("policy must be ReducerProposalEnvelopePolicy")
        _require_tuple(self.receipts, "receipts")
        if any(
            type(receipt) is not ReducerProposalEnvelopeReceipt
            for receipt in self.receipts
        ):
            raise TypeError(
                "receipts must contain ReducerProposalEnvelopeReceipt values"
            )
        if self.source_proposal_policy_digest:
            _validate_digest(
                self.source_proposal_policy_digest,
                "source_proposal_policy_digest",
            )
        elif self.receipts:
            raise ValueError("non-empty comparison ledger requires source policy digest")
        sequences = [receipt.processing_sequence for receipt in self.receipts]
        if sequences != list(range(1, len(sequences) + 1)):
            raise ValueError("comparison receipts must cover complete processing order")
        processed_times = [receipt.processed_at for receipt in self.receipts]
        if processed_times != sorted(processed_times):
            raise ValueError("comparison receipt processing time cannot regress")
        for attribute, message in (
            ("receipt_id", "comparison receipt IDs must be unique"),
            (
                "source_proposal_receipt_id",
                "source proposal receipts may be compared only once",
            ),
            ("cause_occurrence_id", "processed occurrences may be compared only once"),
            ("cause_delivery_id", "processed deliveries may be compared only once"),
        ):
            values = [getattr(receipt, attribute) for receipt in self.receipts]
            if len(values) != len(set(values)):
                raise ValueError(message)
        seen_occurrences: set[str] = set()
        for receipt in self.receipts:
            if (
                receipt.measurement_model_id != self.policy.measurement_model_id
                or receipt.measurement_model_version
                != self.policy.measurement_model_version
                or receipt.policy_digest != self.policy.policy_digest
                or receipt.source_proposal_policy_digest
                != self.source_proposal_policy_digest
                or receipt.snapshot.field_bands != self.policy.field_bands
                or any(
                    item.comparison_operator_id
                    != self.policy.comparison_operator_id
                    or item.comparison_operator_version
                    != self.policy.comparison_operator_version
                    or item.unit != self.policy.unit
                    for item in receipt.comparisons
                )
            ):
                raise ValueError("comparison receipt does not match ledger policy")
            source_occurrence = receipt.reexposure_of_occurrence_id
            if source_occurrence is not None and source_occurrence not in seen_occurrences:
                raise ValueError("reexposure must reference an earlier comparison receipt")
            seen_occurrences.add(receipt.cause_occurrence_id)


def build_reducer_proposal_envelope_ledger(
    source: ReducerProposalLedger,
    policy: ReducerProposalEnvelopePolicy,
) -> ReducerProposalEnvelopeLedger:
    """Derive ordered simulation proxy comparisons without runtime feedback."""

    if type(source) is not ReducerProposalLedger:
        raise TypeError("source must be ReducerProposalLedger")
    if type(policy) is not ReducerProposalEnvelopePolicy:
        raise TypeError("policy must be ReducerProposalEnvelopePolicy")
    if (
        source.policy.measurement_model_id
        != policy.source_measurement_model_id
        or source.policy.measurement_model_version
        != policy.source_measurement_model_version
    ):
        raise ValueError("source proposal ledger does not match comparison policy")
    receipts = tuple(
        _build_receipt(source.policy.policy_digest, source_receipt, policy)
        for source_receipt in source.receipts
    )
    result = ReducerProposalEnvelopeLedger(
        policy=policy,
        source_proposal_policy_digest=source.policy.policy_digest,
        receipts=receipts,
    )
    validate_reducer_proposal_envelope_ledger(source, result)
    return result


def validate_reducer_proposal_envelope_ledger(
    source: ReducerProposalLedger,
    comparison: ReducerProposalEnvelopeLedger,
) -> None:
    """Verify the exact ordered mapping back to the source proposal ledger."""

    if type(source) is not ReducerProposalLedger:
        raise TypeError("source must be ReducerProposalLedger")
    if type(comparison) is not ReducerProposalEnvelopeLedger:
        raise TypeError("comparison must be ReducerProposalEnvelopeLedger")
    if comparison.source_proposal_policy_digest != source.policy.policy_digest:
        raise ValueError("comparison source policy digest does not match source ledger")
    if len(comparison.receipts) != len(source.receipts):
        raise ValueError("comparison ledger must map every source proposal receipt")
    for source_receipt, derived_receipt in zip(
        source.receipts,
        comparison.receipts,
    ):
        _validate_receipt_mapping(source_receipt, derived_receipt, comparison.policy)


def _build_receipt(
    source_policy_digest: str,
    source: ReducerProposalReceipt,
    policy: ReducerProposalEnvelopePolicy,
) -> ReducerProposalEnvelopeReceipt:
    snapshot = ReducerProposalEnvelopeSnapshot(
        snapshot_id=_snapshot_id(
            policy.policy_digest,
            source.receipt_id,
            source.state_before_digest,
            source.processed_at,
            policy.field_bands,
        ),
        policy_digest=policy.policy_digest,
        source_proposal_receipt_id=source.receipt_id,
        source_state_before_digest=source.state_before_digest,
        evaluated_at=source.processed_at,
        field_bands=policy.field_bands,
    )
    comparisons = tuple(
        _compare_proposal(proposal, policy.band_for(proposal.field), policy)
        for proposal in source.proposals
    )
    comparison_digest = _comparison_digest(comparisons)
    return ReducerProposalEnvelopeReceipt(
        receipt_id=_receipt_id(
            policy.measurement_model_id,
            policy.measurement_model_version,
            policy.policy_digest,
            source_policy_digest,
            source.receipt_id,
            source.proposal_digest,
            source.state_before_digest,
            source.processing_sequence,
            source.cause_occurrence_id,
            source.cause_delivery_id,
            source.reexposure_of_occurrence_id,
            source.cause_occurred_at,
            source.became_available_at,
            source.processed_at,
            snapshot.snapshot_id,
            comparison_digest,
        ),
        measurement_model_id=policy.measurement_model_id,
        measurement_model_version=policy.measurement_model_version,
        policy_digest=policy.policy_digest,
        source_proposal_policy_digest=source_policy_digest,
        source_proposal_receipt_id=source.receipt_id,
        source_proposal_digest=source.proposal_digest,
        source_state_before_digest=source.state_before_digest,
        captured_at=source.processed_at,
        processing_sequence=source.processing_sequence,
        cause_occurrence_id=source.cause_occurrence_id,
        cause_delivery_id=source.cause_delivery_id,
        reexposure_of_occurrence_id=source.reexposure_of_occurrence_id,
        cause_occurred_at=source.cause_occurred_at,
        became_available_at=source.became_available_at,
        processed_at=source.processed_at,
        snapshot=snapshot,
        comparisons=comparisons,
        comparison_digest=comparison_digest,
    )


def _compare_proposal(
    proposal: ReducerFieldProposal,
    band: ReducerProposalEnvelopeBand,
    policy: ReducerProposalEnvelopePolicy,
) -> ReducerProposalEnvelopeComparison:
    limited = _clip_signed(
        proposal.requested_delta,
        band.lower_delta,
        band.upper_delta,
    )
    return ReducerProposalEnvelopeComparison(
        write_sequence=proposal.write_sequence,
        source_stage_id=proposal.stage_id,
        source_operator_id=proposal.operator_id,
        field=proposal.field,
        source_constraint_id=proposal.constraint_id,
        basis_before=proposal.basis_before,
        requested_delta=proposal.requested_delta,
        committed_delta=proposal.committed_delta,
        lower_delta=band.lower_delta,
        upper_delta=band.upper_delta,
        band_limited_delta=limited,
        signed_proxy_excess=proposal.requested_delta - limited,
        unit=band.unit,
        comparison_operator_id=policy.comparison_operator_id,
        comparison_operator_version=policy.comparison_operator_version,
    )


def _validate_receipt_mapping(
    source: ReducerProposalReceipt,
    derived: ReducerProposalEnvelopeReceipt,
    policy: ReducerProposalEnvelopePolicy,
) -> None:
    if (
        derived.source_proposal_receipt_id != source.receipt_id
        or derived.source_proposal_digest != source.proposal_digest
        or derived.source_state_before_digest != source.state_before_digest
        or derived.processing_sequence != source.processing_sequence
        or derived.cause_occurrence_id != source.cause_occurrence_id
        or derived.cause_delivery_id != source.cause_delivery_id
        or derived.reexposure_of_occurrence_id
        != source.reexposure_of_occurrence_id
        or derived.cause_occurred_at != source.cause_occurred_at
        or derived.became_available_at != source.became_available_at
        or derived.processed_at != source.processed_at
    ):
        raise ValueError("comparison receipt source lineage does not match source")
    if len(derived.comparisons) != len(source.proposals):
        raise ValueError("comparison receipt must map every ordered proposal")
    for proposal, component in zip(source.proposals, derived.comparisons):
        expected = _compare_proposal(
            proposal,
            policy.band_for(proposal.field),
            policy,
        )
        if component != expected:
            raise ValueError("comparison component does not match source proposal")


def _band_payload(band: ReducerProposalEnvelopeBand) -> dict[str, object]:
    return {
        "field": band.field,
        "lower_delta": band.lower_delta,
        "upper_delta": band.upper_delta,
        "unit": band.unit,
    }


def _comparison_payload(
    comparison: ReducerProposalEnvelopeComparison,
) -> dict[str, object]:
    return {
        "write_sequence": comparison.write_sequence,
        "source_stage_id": comparison.source_stage_id,
        "source_operator_id": comparison.source_operator_id,
        "field": comparison.field,
        "source_constraint_id": comparison.source_constraint_id,
        "basis_before": comparison.basis_before,
        "requested_delta": comparison.requested_delta,
        "committed_delta": comparison.committed_delta,
        "lower_delta": comparison.lower_delta,
        "upper_delta": comparison.upper_delta,
        "band_limited_delta": comparison.band_limited_delta,
        "signed_proxy_excess": comparison.signed_proxy_excess,
        "unit": comparison.unit,
        "comparison_operator_id": comparison.comparison_operator_id,
        "comparison_operator_version": comparison.comparison_operator_version,
    }


def _comparison_digest(
    comparisons: tuple[ReducerProposalEnvelopeComparison, ...],
) -> str:
    return _stable_digest(tuple(_comparison_payload(item) for item in comparisons))


def _snapshot_id(
    policy_digest: str,
    source_receipt_id: str,
    source_state_before_digest: str,
    evaluated_at: SimTime,
    bands: tuple[ReducerProposalEnvelopeBand, ...],
) -> str:
    digest = _stable_digest(
        {
            "policy_digest": policy_digest,
            "source_receipt_id": source_receipt_id,
            "source_state_before_digest": source_state_before_digest,
            "evaluated_at": int(evaluated_at),
            "field_bands": tuple(_band_payload(band) for band in bands),
        }
    )
    return f"reducer-envelope-snapshot:{digest}"


def _receipt_id(
    measurement_model_id: str,
    measurement_model_version: str,
    policy_digest: str,
    source_policy_digest: str,
    source_receipt_id: str,
    source_proposal_digest: str,
    source_state_before_digest: str,
    processing_sequence: int,
    occurrence_id: str,
    delivery_id: str,
    reexposure_of_occurrence_id: str | None,
    occurred_at: SimTime,
    available_at: SimTime,
    processed_at: SimTime,
    snapshot_id: str,
    comparison_digest: str,
) -> str:
    digest = _stable_digest(
        {
            "measurement_model_id": measurement_model_id,
            "measurement_model_version": measurement_model_version,
            "policy_digest": policy_digest,
            "source_policy_digest": source_policy_digest,
            "source_receipt_id": source_receipt_id,
            "source_proposal_digest": source_proposal_digest,
            "source_state_before_digest": source_state_before_digest,
            "processing_sequence": processing_sequence,
            "occurrence_id": occurrence_id,
            "delivery_id": delivery_id,
            "reexposure_of_occurrence_id": reexposure_of_occurrence_id,
            "occurred_at": int(occurred_at),
            "available_at": int(available_at),
            "processed_at": int(processed_at),
            "snapshot_id": snapshot_id,
            "comparison_digest": comparison_digest,
        }
    )
    return (
        f"reducer-envelope:{measurement_model_id}@"
        f"{measurement_model_version}:{digest}"
    )


def _clip_signed(value: float, lower: float, upper: float) -> float:
    return min(max(float(value), float(lower)), float(upper))


def _stable_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _validate_digest(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be an immutable string")
    if len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


def _require_tuple(value: object, name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an immutable tuple")


__all__ = [
    "MORPH_001B_SYNTHETIC_FIELD_BANDS",
    "REDUCER_ENVELOPE_AGGREGATION_WINDOW",
    "REDUCER_ENVELOPE_COMPARISON_MODEL_ID",
    "REDUCER_ENVELOPE_COMPARISON_MODEL_VERSION",
    "REDUCER_ENVELOPE_FIELDS",
    "REDUCER_ENVELOPE_OPERATOR_ID",
    "REDUCER_ENVELOPE_OPERATOR_VERSION",
    "ReducerProposalEnvelopeBand",
    "ReducerProposalEnvelopeComparison",
    "ReducerProposalEnvelopeLedger",
    "ReducerProposalEnvelopePolicy",
    "ReducerProposalEnvelopeReceipt",
    "ReducerProposalEnvelopeSnapshot",
    "build_reducer_proposal_envelope_ledger",
    "validate_reducer_proposal_envelope_ledger",
]
