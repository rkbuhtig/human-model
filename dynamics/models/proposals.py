"""Immutable descriptive-reducer proposals captured before unit clamping.

These records expose what the current simulation reducer requested at each
write boundary.  They are instrumentation artifacts, not independently
identified human deformation demand or morphic load.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

from ..interfaces import clamp01
from .state import HumanState, iter_unit_values


class ReducerDriverChannel(str, Enum):
    """Typed source lane for one contribution to a reducer proposal."""

    ENCODED_INPUT = "encoded_input"
    ENDOGENOUS_DYNAMICS = "endogenous_dynamics"
    PROTOCOL_BRIDGE = "protocol_bridge"
    PHENOMENAL_COUPLING = "phenomenal_coupling"
    EVIDENCE_ASSESSMENT_COUPLING = "evidence_assessment_coupling"
    ACTION_CONSEQUENCE = "action_consequence"


@dataclass(frozen=True, slots=True)
class ReducerOperatorSpec:
    """Versioned structural identity for one reducer write boundary."""

    stage_id: str
    operator_id: str
    field: str
    allowed_driver_identities: tuple[tuple[ReducerDriverChannel, str], ...]
    constraint_id: str = "clamp01"


REDUCER_MANDATORY_OPERATOR_SPECS = (
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.body.energy",
        "body.energy",
        ((ReducerDriverChannel.ENCODED_INPUT, "model_input.energy_delta"),),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.body.arousal",
        "body.arousal",
        ((ReducerDriverChannel.ENCODED_INPUT, "model_input.arousal_delta"),),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.body.action_capacity",
        "body.action_capacity",
        ((ReducerDriverChannel.ENCODED_INPUT, "model_input.capacity_delta"),),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.access.attention_budget",
        "access.attention_budget",
        (
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.attention_delta"),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.time_pressure"),
            (
                ReducerDriverChannel.PROTOCOL_BRIDGE,
                "legacy_v01_access_pressure_bridge",
            ),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.soothing"),
        ),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.access.interference",
        "access.interference",
        (
            (ReducerDriverChannel.ENDOGENOUS_DYNAMICS, "interference_retention"),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.memory_interference"),
            (
                ReducerDriverChannel.PROTOCOL_BRIDGE,
                "legacy_v01_access_pressure_bridge",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.access.queue_load",
        "access.queue_load",
        (
            (ReducerDriverChannel.ENDOGENOUS_DYNAMICS, "queue_load_retention"),
            (
                ReducerDriverChannel.PROTOCOL_BRIDGE,
                "legacy_v01_access_pressure_bridge",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.relationship.trust",
        "relationship.trust",
        (
            (
                ReducerDriverChannel.ENCODED_INPUT,
                "external_model_input.trust_delta",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "fast-descriptive-update@0.1.0",
        "fast.relationship.boundary_strain",
        "relationship.boundary_strain",
        (
            (
                ReducerDriverChannel.ENCODED_INPUT,
                "external_model_input.boundary_delta",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.associative.rejection_access",
        "associative.rejection_access",
        (
            (
                ReducerDriverChannel.PHENOMENAL_COUPLING,
                "phenomenal.distress_x_salience",
            ),
            (
                ReducerDriverChannel.ENCODED_INPUT,
                "soothing_x_relationship_trust",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.associative.ambiguity_sensitivity",
        "associative.ambiguity_sensitivity",
        (
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.ambiguity"),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.soothing"),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.affective.residual_distress",
        "affective.residual_distress",
        (
            (ReducerDriverChannel.PHENOMENAL_COUPLING, "affective_tracking"),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.soothing"),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.narrative.rejection_story",
        "narrative.rejection_story",
        (
            (
                ReducerDriverChannel.PHENOMENAL_COUPLING,
                "phenomenal.distress_target",
            ),
            (
                ReducerDriverChannel.EVIDENCE_ASSESSMENT_COUPLING,
                "rejection_confidence_target",
            ),
            (ReducerDriverChannel.ENDOGENOUS_DYNAMICS, "narrative_retention"),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.narrative.relational_security",
        "narrative.relational_security",
        (
            (
                ReducerDriverChannel.ENDOGENOUS_DYNAMICS,
                "relationship_x_narrative_coupling",
            ),
            (ReducerDriverChannel.PHENOMENAL_COUPLING, "phenomenal.distress"),
            (ReducerDriverChannel.ENCODED_INPUT, "model_input.soothing"),
        ),
    ),
)

REDUCER_OPTIONAL_OPERATOR_SPECS = (
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.action.body.energy",
        "body.energy",
        (
            (ReducerDriverChannel.ACTION_CONSEQUENCE, "performance.ask.energy_cost"),
            (
                ReducerDriverChannel.ACTION_CONSEQUENCE,
                "performance.accuse.energy_cost",
            ),
            (
                ReducerDriverChannel.ACTION_CONSEQUENCE,
                "performance.withdraw.energy_cost",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.action.habit.impulsivity",
        "habit.impulsivity",
        (
            (
                ReducerDriverChannel.ACTION_CONSEQUENCE,
                "performance.accuse.impulsivity",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.action.relationship.trust",
        "relationship.trust",
        (
            (ReducerDriverChannel.ACTION_CONSEQUENCE, "performance.accuse.trust"),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.action.relationship.boundary_strain",
        "relationship.boundary_strain",
        (
            (
                ReducerDriverChannel.ACTION_CONSEQUENCE,
                "performance.accuse.boundary_strain",
            ),
        ),
    ),
    ReducerOperatorSpec(
        "slow-descriptive-update@0.1.0",
        "slow.soothing.habit.impulsivity",
        "habit.impulsivity",
        ((ReducerDriverChannel.ENCODED_INPUT, "model_input.soothing"),),
    ),
)

REDUCER_ALLOWED_OPTIONAL_OPERATOR_SUFFIXES = (
    (),
    ("slow.action.body.energy",),
    ("slow.soothing.habit.impulsivity",),
    ("slow.action.body.energy", "slow.soothing.habit.impulsivity"),
    (
        "slow.action.body.energy",
        "slow.action.habit.impulsivity",
        "slow.action.relationship.trust",
        "slow.action.relationship.boundary_strain",
    ),
    (
        "slow.action.body.energy",
        "slow.action.habit.impulsivity",
        "slow.action.relationship.trust",
        "slow.action.relationship.boundary_strain",
        "slow.soothing.habit.impulsivity",
    ),
)


@dataclass(frozen=True, slots=True)
class ReducerProposalContext:
    """Minimal context needed to validate conditional reducer writes."""

    encoded_soothing: float
    performance_receipt_id: str | None
    performance_action_kind: str | None

    def __post_init__(self) -> None:
        if (
            isinstance(self.encoded_soothing, bool)
            or not isinstance(self.encoded_soothing, (int, float))
            or not math.isfinite(float(self.encoded_soothing))
            or not 0.0 <= float(self.encoded_soothing) <= 1.0
        ):
            raise ValueError("encoded_soothing must be finite and in [0, 1]")
        object.__setattr__(self, "encoded_soothing", float(self.encoded_soothing))
        if self.performance_action_kind is None:
            if self.performance_receipt_id is not None:
                raise ValueError("performance receipt and action kind must be paired")
            return
        if self.performance_action_kind not in {"ask", "accuse", "withdraw"}:
            raise ValueError("unsupported performance action in reducer context")
        if not self.performance_receipt_id:
            raise ValueError("performance receipt and action kind must be paired")


@dataclass(frozen=True, slots=True)
class ReducerDriverContribution:
    channel: ReducerDriverChannel
    label: str
    contribution: float

    def __post_init__(self) -> None:
        if type(self.channel) is not ReducerDriverChannel:
            raise TypeError("channel must be ReducerDriverChannel")
        if not self.label:
            raise ValueError("driver label must be non-empty")
        if (
            isinstance(self.contribution, bool)
            or not isinstance(self.contribution, (int, float))
            or not math.isfinite(float(self.contribution))
        ):
            raise ValueError("driver contribution must be finite")
        object.__setattr__(self, "contribution", float(self.contribution))


@dataclass(frozen=True, slots=True)
class ReducerFieldProposal:
    """One ordered pre-clamp write proposed by the current reducer."""

    write_sequence: int
    stage_id: str
    operator_id: str
    field: str
    basis_before: float
    requested_after_unbounded: float
    committed_after: float
    unit: str
    constraint_id: str
    drivers: tuple[ReducerDriverContribution, ...]

    def __post_init__(self) -> None:
        if type(self.write_sequence) is not int or self.write_sequence < 1:
            raise ValueError("write_sequence must be a positive int")
        for value, name in (
            (self.stage_id, "stage_id"),
            (self.operator_id, "operator_id"),
            (self.field, "field"),
            (self.unit, "unit"),
            (self.constraint_id, "constraint_id"),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")
        if self.unit != "normalized_simulation_unit":
            raise ValueError("reducer proposal unit must be normalized_simulation_unit")
        if self.constraint_id != "clamp01":
            raise ValueError("reducer proposal constraint must be clamp01")
        if type(self.drivers) is not tuple:
            raise TypeError("drivers must be an immutable tuple")
        if any(
            type(driver) is not ReducerDriverContribution
            for driver in self.drivers
        ):
            raise TypeError("drivers must contain ReducerDriverContribution values")
        values = (
            self.basis_before,
            self.requested_after_unbounded,
            self.committed_after,
        )
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(float(value))
            for value in values
        ):
            raise ValueError("reducer proposal values must be finite")
        object.__setattr__(self, "basis_before", float(self.basis_before))
        object.__setattr__(
            self,
            "requested_after_unbounded",
            float(self.requested_after_unbounded),
        )
        object.__setattr__(self, "committed_after", float(self.committed_after))
        if not 0.0 <= self.committed_after <= 1.0:
            raise ValueError("committed_after must be in [0, 1]")
        if abs(clamp01(self.requested_after_unbounded) - self.committed_after) > 1e-12:
            raise ValueError("committed_after must be the clamped requested target")
        driver_delta = sum(driver.contribution for driver in self.drivers)
        if abs(driver_delta - self.requested_delta) > 1e-12:
            raise ValueError("driver contributions must sum to requested_delta")

    @property
    def requested_delta(self) -> float:
        return self.requested_after_unbounded - self.basis_before

    @property
    def committed_delta(self) -> float:
        return self.committed_after - self.basis_before


@dataclass(frozen=True, slots=True)
class ReducerStepResult:
    """Committed state plus the exact ordered proposals used to produce it."""

    state_after: HumanState
    proposals: tuple[ReducerFieldProposal, ...]

    def __post_init__(self) -> None:
        if type(self.state_after) is not HumanState:
            raise TypeError("state_after must be HumanState")
        if type(self.proposals) is not tuple:
            raise TypeError("proposals must be an immutable tuple")
        if any(
            type(proposal) is not ReducerFieldProposal
            for proposal in self.proposals
        ):
            raise TypeError("proposals must contain ReducerFieldProposal values")
        sequences = [proposal.write_sequence for proposal in self.proposals]
        if sequences:
            expected = list(range(sequences[0], sequences[0] + len(sequences)))
            if sequences != expected:
                raise ValueError("reducer proposal write_sequence must be contiguous")
        last_by_field: dict[str, ReducerFieldProposal] = {}
        for proposal in self.proposals:
            previous = last_by_field.get(proposal.field)
            if previous is not None and (
                abs(previous.committed_after - proposal.basis_before) > 1e-12
            ):
                raise ValueError("repeated field proposals must preserve writer order")
            last_by_field[proposal.field] = proposal
        state_values = dict(iter_unit_values(self.state_after))
        for field, proposal in last_by_field.items():
            if field not in state_values:
                raise ValueError(f"proposal field is absent from HumanState: {field}")
            if abs(state_values[field] - proposal.committed_after) > 1e-12:
                raise ValueError("final proposal does not match committed state")


__all__ = [
    "REDUCER_ALLOWED_OPTIONAL_OPERATOR_SUFFIXES",
    "REDUCER_MANDATORY_OPERATOR_SPECS",
    "REDUCER_OPTIONAL_OPERATOR_SPECS",
    "ReducerDriverChannel",
    "ReducerDriverContribution",
    "ReducerFieldProposal",
    "ReducerOperatorSpec",
    "ReducerProposalContext",
    "ReducerStepResult",
]
