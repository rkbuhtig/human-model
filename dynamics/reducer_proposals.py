"""Read-only occurrence ledger for current-reducer pre-clamp proposals.

The ledger is a versioned instrumentation surface.  It does not identify a
capacity-independent deformation demand and does not calculate morphic load.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
from typing import Iterable

from .models import (
    HumanState,
    ReducerDriverChannel,
    ReducerFieldProposal,
    ReducerProposalContext,
    iter_unit_values,
)
from .models.proposals import (
    REDUCER_ALLOWED_OPTIONAL_OPERATOR_SUFFIXES,
    REDUCER_MANDATORY_OPERATOR_SPECS,
    REDUCER_OPTIONAL_OPERATOR_SPECS,
    ReducerOperatorSpec,
)
from .temporal import SimTime
from .trace import TickTrace


REDUCER_PROPOSAL_MODEL_ID = "descriptive-reducer-preclamp-proxy"
REDUCER_PROPOSAL_MODEL_VERSION = "1.0.0"
REDUCER_PROPOSAL_STAGES = (
    "fast-descriptive-update@0.1.0",
    "slow-descriptive-update@0.1.0",
)
REDUCER_STATE_PROJECTION_FIELDS = (
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
REDUCER_PROPOSAL_AVAILABLE_INFORMATION = (
    "current_encoded_model_input",
    "current_writer_basis_state",
    "current_legacy_access_pressure_bridge",
    "current_phenomenal_readout",
    "current_evidence_assessment_coupling",
    "current_performance_receipt",
)


@dataclass(frozen=True, slots=True)
class ReducerProposalTracePolicy:
    measurement_model_id: str = REDUCER_PROPOSAL_MODEL_ID
    measurement_model_version: str = REDUCER_PROPOSAL_MODEL_VERSION
    stage_ids: tuple[str, ...] = REDUCER_PROPOSAL_STAGES
    state_projection_fields: tuple[str, ...] = REDUCER_STATE_PROJECTION_FIELDS
    unit: str = "normalized_simulation_unit"
    available_information: tuple[str, ...] = (
        REDUCER_PROPOSAL_AVAILABLE_INFORMATION
    )

    def __post_init__(self) -> None:
        _require_tuple(self.stage_ids, "stage_ids")
        _require_tuple(self.state_projection_fields, "state_projection_fields")
        _require_tuple(self.available_information, "available_information")
        if (
            self.measurement_model_id != REDUCER_PROPOSAL_MODEL_ID
            or self.measurement_model_version != REDUCER_PROPOSAL_MODEL_VERSION
        ):
            raise ValueError("reducer proposal measurement identity is fixed")
        if self.stage_ids != REDUCER_PROPOSAL_STAGES:
            raise ValueError("reducer proposal stage order is fixed")
        if self.state_projection_fields != REDUCER_STATE_PROJECTION_FIELDS:
            raise ValueError("reducer proposal state projection is fixed")
        if self.unit != "normalized_simulation_unit":
            raise ValueError("reducer proposal unit is fixed")
        if self.available_information != REDUCER_PROPOSAL_AVAILABLE_INFORMATION:
            raise ValueError("reducer proposal available information is fixed")

    @property
    def policy_digest(self) -> str:
        return _stable_digest(
            {
                "measurement_model_id": self.measurement_model_id,
                "measurement_model_version": self.measurement_model_version,
                "stage_ids": self.stage_ids,
                "state_projection_fields": self.state_projection_fields,
                "unit": self.unit,
                "available_information": self.available_information,
                "operator_schema": tuple(
                    _operator_spec_payload(spec)
                    for spec in (
                        *REDUCER_MANDATORY_OPERATOR_SPECS,
                        *REDUCER_OPTIONAL_OPERATOR_SPECS,
                    )
                ),
                "allowed_optional_suffixes": (
                    REDUCER_ALLOWED_OPTIONAL_OPERATOR_SUFFIXES
                ),
                "conditional_context_fields": (
                    "encoded_soothing",
                    "performance_receipt_id",
                    "performance_action_kind",
                ),
            }
        )


@dataclass(frozen=True, slots=True)
class ReducerStateValue:
    field: str
    value: float
    unit: str = "normalized_simulation_unit"

    def __post_init__(self) -> None:
        if not self.field:
            raise ValueError("state projection field must be non-empty")
        if self.unit != "normalized_simulation_unit":
            raise ValueError("state projection unit must be normalized_simulation_unit")
        if (
            isinstance(self.value, bool)
            or not isinstance(self.value, (int, float))
            or not math.isfinite(float(self.value))
        ):
            raise ValueError("state projection value must be finite")
        object.__setattr__(self, "value", float(self.value))


@dataclass(frozen=True, slots=True)
class ReducerProposalReceipt:
    receipt_id: str
    measurement_model_id: str
    measurement_model_version: str
    policy_digest: str
    captured_at: SimTime
    processing_sequence: int
    cause_occurrence_id: str
    cause_delivery_id: str
    reexposure_of_occurrence_id: str | None
    cause_occurred_at: SimTime
    became_available_at: SimTime
    processed_at: SimTime
    available_information: tuple[str, ...]
    context: ReducerProposalContext
    context_digest: str
    proposals: tuple[ReducerFieldProposal, ...]
    proposal_digest: str
    state_before_projection: tuple[ReducerStateValue, ...]
    state_after_projection: tuple[ReducerStateValue, ...]
    state_before_digest: str
    state_after_digest: str

    def __post_init__(self) -> None:
        _require_tuple(self.available_information, "available_information")
        _require_tuple(self.proposals, "proposals")
        _require_tuple(self.state_before_projection, "state_before_projection")
        _require_tuple(self.state_after_projection, "state_after_projection")
        if type(self.context) is not ReducerProposalContext:
            raise TypeError("context must be ReducerProposalContext")
        if any(
            type(proposal) is not ReducerFieldProposal
            for proposal in self.proposals
        ):
            raise TypeError("proposals must contain ReducerFieldProposal values")
        if any(
            type(value) is not ReducerStateValue
            for value in (
                *self.state_before_projection,
                *self.state_after_projection,
            )
        ):
            raise TypeError("state projections must contain ReducerStateValue values")
        for value, name in (
            (self.receipt_id, "receipt_id"),
            (self.measurement_model_id, "measurement_model_id"),
            (self.measurement_model_version, "measurement_model_version"),
            (self.cause_occurrence_id, "cause_occurrence_id"),
            (self.cause_delivery_id, "cause_delivery_id"),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")
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
            raise ValueError("reducer proposal receipt temporal order is invalid")
        if self.captured_at != self.processed_at:
            raise ValueError("captured_at must equal processed_at")
        if type(self.processing_sequence) is not int or self.processing_sequence < 1:
            raise ValueError("processing_sequence must be a positive int")
        if self.reexposure_of_occurrence_id is not None:
            if not self.reexposure_of_occurrence_id:
                raise ValueError("reexposure_of_occurrence_id must be non-empty")
            if self.reexposure_of_occurrence_id == self.cause_occurrence_id:
                raise ValueError("a reexposure cannot refer to its own occurrence")
        if not self.proposals:
            raise ValueError("a processed occurrence must retain reducer proposals")
        sequences = [proposal.write_sequence for proposal in self.proposals]
        if sequences != list(range(1, len(sequences) + 1)):
            raise ValueError("proposal writes must cover the complete occurrence order")
        _validate_operator_schema(self.proposals, self.context)
        last_by_field: dict[str, ReducerFieldProposal] = {}
        for proposal in self.proposals:
            previous = last_by_field.get(proposal.field)
            if previous is not None and (
                abs(previous.committed_after - proposal.basis_before) > 1e-12
            ):
                raise ValueError("proposal field chain is not contiguous")
            last_by_field[proposal.field] = proposal
        if self.proposal_digest != _proposal_digest(self.proposals):
            raise ValueError("proposal_digest does not match proposals")
        if self.context_digest != _context_digest(self.context):
            raise ValueError("context_digest does not match reducer proposal context")
        before_projection = _projection_dict(self.state_before_projection)
        after_projection = _projection_dict(self.state_after_projection)
        if tuple(before_projection) != tuple(after_projection):
            raise ValueError("state projections must have identical ordered fields")
        first_by_field: dict[str, ReducerFieldProposal] = {}
        last_by_field = {}
        for proposal in self.proposals:
            first_by_field.setdefault(proposal.field, proposal)
            last_by_field[proposal.field] = proposal
        for field, proposal in first_by_field.items():
            if (
                field not in before_projection
                or abs(before_projection[field] - proposal.basis_before) > 1e-12
            ):
                raise ValueError("first proposal basis does not match state projection")
        for field, proposal in last_by_field.items():
            if (
                field not in after_projection
                or abs(after_projection[field] - proposal.committed_after) > 1e-12
            ):
                raise ValueError("last proposal commit does not match state projection")
        changed_fields = {
            field
            for field, value in after_projection.items()
            if abs(value - before_projection[field]) > 1e-12
        }
        if not changed_fields <= set(last_by_field):
            raise ValueError("descriptive state changed without a reducer proposal")
        if self.state_before_digest != _projection_digest(
            self.state_before_projection
        ):
            raise ValueError("state_before_digest does not match projection")
        if self.state_after_digest != _projection_digest(self.state_after_projection):
            raise ValueError("state_after_digest does not match projection")
        expected_receipt_id = _receipt_id(
            self.measurement_model_id,
            self.measurement_model_version,
            self.policy_digest,
            self.processing_sequence,
            self.cause_occurrence_id,
            self.cause_delivery_id,
            self.reexposure_of_occurrence_id,
            self.cause_occurred_at,
            self.became_available_at,
            self.processed_at,
            self.context_digest,
            self.proposal_digest,
            self.state_before_digest,
            self.state_after_digest,
        )
        if self.receipt_id != expected_receipt_id:
            raise ValueError("receipt_id does not match canonical proposal identity")
        _validate_digest(self.policy_digest, "policy_digest")
        _validate_digest(self.context_digest, "context_digest")
        _validate_digest(self.proposal_digest, "proposal_digest")
        _validate_digest(self.state_before_digest, "state_before_digest")
        _validate_digest(self.state_after_digest, "state_after_digest")


@dataclass(frozen=True, slots=True)
class ReducerProposalLedger:
    policy: ReducerProposalTracePolicy = field(
        default_factory=ReducerProposalTracePolicy
    )
    receipts: tuple[ReducerProposalReceipt, ...] = ()

    def __post_init__(self) -> None:
        if type(self.policy) is not ReducerProposalTracePolicy:
            raise TypeError("policy must be ReducerProposalTracePolicy")
        _require_tuple(self.receipts, "receipts")
        if any(
            type(receipt) is not ReducerProposalReceipt
            for receipt in self.receipts
        ):
            raise TypeError("receipts must contain ReducerProposalReceipt values")
        sequences = [receipt.processing_sequence for receipt in self.receipts]
        if sequences != list(range(1, len(sequences) + 1)):
            raise ValueError("proposal receipts must cover the complete processing order")
        processed_times = [receipt.processed_at for receipt in self.receipts]
        if processed_times != sorted(processed_times):
            raise ValueError("proposal receipt processing time cannot regress")
        receipt_ids = [receipt.receipt_id for receipt in self.receipts]
        occurrence_ids = [receipt.cause_occurrence_id for receipt in self.receipts]
        delivery_ids = [receipt.cause_delivery_id for receipt in self.receipts]
        if len(receipt_ids) != len(set(receipt_ids)):
            raise ValueError("reducer proposal receipt IDs must be unique")
        if len(occurrence_ids) != len(set(occurrence_ids)):
            raise ValueError("processed occurrences may have only one proposal receipt")
        if len(delivery_ids) != len(set(delivery_ids)):
            raise ValueError("processed deliveries may have only one proposal receipt")
        for previous, current in zip(self.receipts, self.receipts[1:]):
            if previous.state_after_projection != current.state_before_projection:
                raise ValueError("proposal receipt state chain is discontinuous")
        seen_occurrences: dict[str, ReducerProposalReceipt] = {}
        for receipt in self.receipts:
            if (
                receipt.measurement_model_id != self.policy.measurement_model_id
                or receipt.measurement_model_version
                != self.policy.measurement_model_version
                or receipt.policy_digest != self.policy.policy_digest
                or receipt.available_information
                != self.policy.available_information
                or any(
                    proposal.stage_id not in self.policy.stage_ids
                    or proposal.unit != self.policy.unit
                    for proposal in receipt.proposals
                )
            ):
                raise ValueError("reducer proposal receipt does not match policy")
            source_occurrence = receipt.reexposure_of_occurrence_id
            if source_occurrence is not None:
                source_receipt = seen_occurrences.get(source_occurrence)
                if source_receipt is None:
                    raise ValueError(
                        "reexposure must reference an earlier proposal receipt"
                    )
                if receipt.cause_occurred_at < source_receipt.processed_at:
                    raise ValueError(
                        "reexposure occurrence cannot predate source processing"
                    )
            seen_occurrences[receipt.cause_occurrence_id] = receipt


def build_reducer_proposal_ledger(
    traces: Iterable[TickTrace],
    policy: ReducerProposalTracePolicy | None = None,
) -> ReducerProposalLedger:
    """Project captured reducer proposals after execution without feedback."""

    trace_policy = policy or ReducerProposalTracePolicy()
    receipts: list[ReducerProposalReceipt] = []
    for trace in traces:
        observation = trace.observation
        stamp = observation.processing_stamp
        sequence = trace.processing_sequence
        if stamp is None or sequence is None:
            raise ValueError("proposal projection requires canonical processing stamps")
        if stamp.processing_sequence != sequence:
            raise ValueError("trace and observation processing sequence mismatch")
        _validate_trace_proposals(trace)
        envelope = stamp.envelope
        proposals = trace.reducer_proposals
        context = trace.reducer_proposal_context
        if context is None:
            raise ValueError("proposal projection requires reducer proposal context")
        state_before_projection = _state_projection(trace.state_before)
        state_after_projection = _state_projection(trace.state_after)
        context_digest = _context_digest(context)
        proposal_digest = _proposal_digest(proposals)
        state_before_digest = _projection_digest(state_before_projection)
        state_after_digest = _projection_digest(state_after_projection)
        receipts.append(
            ReducerProposalReceipt(
                receipt_id=_receipt_id(
                    trace_policy.measurement_model_id,
                    trace_policy.measurement_model_version,
                    trace_policy.policy_digest,
                    sequence,
                    observation.occurrence_id,
                    observation.delivery_id,
                    envelope.reexposure_of_occurrence_id,
                    observation.occurred_at,
                    observation.available_at,
                    observation.processed_at,
                    context_digest,
                    proposal_digest,
                    state_before_digest,
                    state_after_digest,
                ),
                measurement_model_id=trace_policy.measurement_model_id,
                measurement_model_version=trace_policy.measurement_model_version,
                policy_digest=trace_policy.policy_digest,
                captured_at=observation.processed_at,
                processing_sequence=sequence,
                cause_occurrence_id=observation.occurrence_id,
                cause_delivery_id=observation.delivery_id,
                reexposure_of_occurrence_id=(
                    envelope.reexposure_of_occurrence_id
                ),
                cause_occurred_at=observation.occurred_at,
                became_available_at=observation.available_at,
                processed_at=observation.processed_at,
                available_information=trace_policy.available_information,
                context=context,
                context_digest=context_digest,
                proposals=proposals,
                proposal_digest=proposal_digest,
                state_before_projection=state_before_projection,
                state_after_projection=state_after_projection,
                state_before_digest=state_before_digest,
                state_after_digest=state_after_digest,
            )
        )
    return ReducerProposalLedger(policy=trace_policy, receipts=tuple(receipts))


def _validate_trace_proposals(trace: TickTrace) -> None:
    proposals = trace.reducer_proposals
    if type(proposals) is not tuple or not proposals:
        raise ValueError("processed trace must contain immutable reducer proposals")
    if trace.reducer_proposal_context is None:
        raise ValueError("processed trace must contain reducer proposal context")
    context = trace.reducer_proposal_context
    if trace.performance is None:
        if (
            context.performance_receipt_id is not None
            or context.performance_action_kind is not None
        ):
            raise ValueError("proposal context contradicts TickTrace performance")
    elif (
        context.performance_receipt_id != trace.performance.receipt_id
        or context.performance_action_kind != trace.performance.action_kind
    ):
        raise ValueError("proposal context contradicts TickTrace performance")
    _validate_operator_schema(proposals, context)
    before = dict(iter_unit_values(trace.state_before))
    after = dict(iter_unit_values(trace.state_after))
    first_by_field: dict[str, ReducerFieldProposal] = {}
    last_by_field: dict[str, ReducerFieldProposal] = {}
    for proposal in proposals:
        first_by_field.setdefault(proposal.field, proposal)
        last_by_field[proposal.field] = proposal
    for field, proposal in first_by_field.items():
        if field not in before or abs(before[field] - proposal.basis_before) > 1e-12:
            raise ValueError("first proposal basis does not match pre-occurrence state")
    for field, proposal in last_by_field.items():
        if field not in after or abs(after[field] - proposal.committed_after) > 1e-12:
            raise ValueError("last proposal commit does not match post-occurrence state")
    changed_fields = {
        field for field, value in after.items() if abs(value - before[field]) > 1e-12
    }
    if not changed_fields <= set(last_by_field):
        raise ValueError("descriptive state changed without a reducer proposal")


def _validate_operator_schema(
    proposals: tuple[ReducerFieldProposal, ...],
    context: ReducerProposalContext,
) -> None:
    mandatory_ids = tuple(
        spec.operator_id for spec in REDUCER_MANDATORY_OPERATOR_SPECS
    )
    operator_ids = tuple(proposal.operator_id for proposal in proposals)
    if operator_ids[: len(mandatory_ids)] != mandatory_ids:
        raise ValueError("mandatory reducer proposal schema is incomplete or reordered")
    optional_suffix = operator_ids[len(mandatory_ids) :]
    if optional_suffix not in REDUCER_ALLOWED_OPTIONAL_OPERATOR_SUFFIXES:
        raise ValueError("conditional reducer proposal order is invalid")
    expected_suffix: list[str] = []
    action_kind = context.performance_action_kind
    if action_kind is not None:
        expected_suffix.append("slow.action.body.energy")
        if action_kind == "accuse":
            expected_suffix.extend(
                (
                    "slow.action.habit.impulsivity",
                    "slow.action.relationship.trust",
                    "slow.action.relationship.boundary_strain",
                )
            )
    if context.encoded_soothing > 0.0:
        expected_suffix.append("slow.soothing.habit.impulsivity")
    if optional_suffix != tuple(expected_suffix):
        raise ValueError("conditional reducer proposals do not match trace context")
    specs = {
        spec.operator_id: spec
        for spec in (
            *REDUCER_MANDATORY_OPERATOR_SPECS,
            *REDUCER_OPTIONAL_OPERATOR_SPECS,
        )
    }
    for proposal in proposals:
        spec = specs[proposal.operator_id]
        if (
            proposal.stage_id != spec.stage_id
            or proposal.field != spec.field
            or proposal.constraint_id != spec.constraint_id
        ):
            raise ValueError("reducer proposal does not match operator schema")
        driver_identities = tuple(
            (driver.channel, driver.label) for driver in proposal.drivers
        )
        if len(driver_identities) != len(set(driver_identities)):
            raise ValueError("reducer proposal driver identities must be unique")
        if not set(driver_identities) <= set(spec.allowed_driver_identities):
            raise ValueError("reducer proposal driver is not allowed by operator schema")
    proposals_by_operator = {
        proposal.operator_id: proposal for proposal in proposals
    }
    expected_optional_drivers = _expected_optional_drivers(context)
    for operator_id, expected_drivers in expected_optional_drivers.items():
        actual_drivers = proposals_by_operator[operator_id].drivers
        if len(actual_drivers) != len(expected_drivers):
            raise ValueError("conditional reducer drivers do not match trace context")
        for actual, (channel, label, contribution) in zip(
            actual_drivers,
            expected_drivers,
        ):
            if (
                actual.channel is not channel
                or actual.label != label
                or abs(actual.contribution - contribution) > 1e-12
            ):
                raise ValueError(
                    "conditional reducer drivers do not match trace context"
                )


def _expected_optional_drivers(
    context: ReducerProposalContext,
) -> dict[str, tuple[tuple[ReducerDriverChannel, str, float], ...]]:
    result: dict[
        str,
        tuple[tuple[ReducerDriverChannel, str, float], ...],
    ] = {}
    action_kind = context.performance_action_kind
    if action_kind is not None:
        cost = {"ask": 0.025, "accuse": 0.045, "withdraw": 0.020}[action_kind]
        result["slow.action.body.energy"] = (
            (
                ReducerDriverChannel.ACTION_CONSEQUENCE,
                f"performance.{action_kind}.energy_cost",
                -cost,
            ),
        )
        if action_kind == "accuse":
            result.update(
                {
                    "slow.action.habit.impulsivity": (
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.impulsivity",
                            0.0010,
                        ),
                    ),
                    "slow.action.relationship.trust": (
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.trust",
                            -0.020,
                        ),
                    ),
                    "slow.action.relationship.boundary_strain": (
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.boundary_strain",
                            0.040,
                        ),
                    ),
                }
            )
    if context.encoded_soothing > 0.0:
        result["slow.soothing.habit.impulsivity"] = (
            (
                ReducerDriverChannel.ENCODED_INPUT,
                "model_input.soothing",
                -0.0005 * context.encoded_soothing,
            ),
        )
    return result


def _operator_spec_payload(spec: ReducerOperatorSpec) -> dict[str, object]:
    return {
        "stage_id": spec.stage_id,
        "operator_id": spec.operator_id,
        "field": spec.field,
        "constraint_id": spec.constraint_id,
        "allowed_driver_identities": tuple(
            (channel.value, label)
            for channel, label in spec.allowed_driver_identities
        ),
    }


def _proposal_digest(proposals: tuple[ReducerFieldProposal, ...]) -> str:
    return _stable_digest(
        tuple(
            {
                "write_sequence": proposal.write_sequence,
                "stage_id": proposal.stage_id,
                "operator_id": proposal.operator_id,
                "field": proposal.field,
                "basis_before": proposal.basis_before,
                "requested_after_unbounded": proposal.requested_after_unbounded,
                "committed_after": proposal.committed_after,
                "unit": proposal.unit,
                "constraint_id": proposal.constraint_id,
                "drivers": tuple(
                    {
                        "channel": driver.channel.value,
                        "label": driver.label,
                        "contribution": driver.contribution,
                    }
                    for driver in proposal.drivers
                ),
            }
            for proposal in proposals
        )
    )


def _context_digest(context: ReducerProposalContext) -> str:
    return _stable_digest(
        {
            "encoded_soothing": context.encoded_soothing,
            "performance_receipt_id": context.performance_receipt_id,
            "performance_action_kind": context.performance_action_kind,
        }
    )


def _state_projection(state: HumanState) -> tuple[ReducerStateValue, ...]:
    return tuple(
        ReducerStateValue(field=field, value=value)
        for field, value in iter_unit_values(state)
    )


def _projection_dict(
    projection: tuple[ReducerStateValue, ...],
) -> dict[str, float]:
    fields = [value.field for value in projection]
    if tuple(fields) != REDUCER_STATE_PROJECTION_FIELDS:
        raise ValueError("state projection fields must match the fixed ordered scope")
    return {value.field: value.value for value in projection}


def _projection_digest(projection: tuple[ReducerStateValue, ...]) -> str:
    return _stable_digest(
        tuple(
            {"field": value.field, "value": value.value, "unit": value.unit}
            for value in projection
        )
    )


def _receipt_id(
    measurement_model_id: str,
    measurement_model_version: str,
    policy_digest: str,
    processing_sequence: int,
    occurrence_id: str,
    delivery_id: str,
    reexposure_of_occurrence_id: str | None,
    occurred_at: SimTime,
    available_at: SimTime,
    processed_at: SimTime,
    context_digest: str,
    proposal_digest: str,
    state_before_digest: str,
    state_after_digest: str,
) -> str:
    content_digest = _stable_digest(
        {
            "measurement_model_id": measurement_model_id,
            "measurement_model_version": measurement_model_version,
            "policy_digest": policy_digest,
            "processing_sequence": processing_sequence,
            "occurrence_id": occurrence_id,
            "delivery_id": delivery_id,
            "reexposure_of_occurrence_id": reexposure_of_occurrence_id,
            "occurred_at": int(occurred_at),
            "available_at": int(available_at),
            "processed_at": int(processed_at),
            "context_digest": context_digest,
            "proposal_digest": proposal_digest,
            "state_before_digest": state_before_digest,
            "state_after_digest": state_after_digest,
        }
    )
    return (
        f"reducer-proposal:{measurement_model_id}@{measurement_model_version}:"
        f"{content_digest}"
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


def _validate_digest(value: str, name: str) -> None:
    if len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


def _require_tuple(value: object, name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an immutable tuple")


__all__ = [
    "REDUCER_PROPOSAL_AVAILABLE_INFORMATION",
    "REDUCER_PROPOSAL_MODEL_ID",
    "REDUCER_PROPOSAL_MODEL_VERSION",
    "REDUCER_PROPOSAL_STAGES",
    "REDUCER_STATE_PROJECTION_FIELDS",
    "ReducerProposalLedger",
    "ReducerProposalReceipt",
    "ReducerProposalTracePolicy",
    "ReducerStateValue",
    "build_reducer_proposal_ledger",
]
