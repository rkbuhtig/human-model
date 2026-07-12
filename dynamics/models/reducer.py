"""Descriptive fast, phenomenal-readout, and slow update hypotheses."""

from __future__ import annotations

from dataclasses import replace

from ..contract.records import PerformanceReceipt
from ..interfaces import ModelInput, clamp01
from .proposals import (
    ReducerDriverChannel,
    ReducerDriverContribution,
    ReducerFieldProposal,
    ReducerStepResult,
)
from .routing import rejection_confidence
from .state import BodyState, HumanState, PhenomenalActivation


class _ProposalWriter:
    def __init__(self, stage_id: str, write_sequence_start: int) -> None:
        if type(write_sequence_start) is not int or write_sequence_start < 1:
            raise ValueError("write_sequence_start must be a positive int")
        self.stage_id = stage_id
        self.next_sequence = write_sequence_start
        self.proposals: list[ReducerFieldProposal] = []

    def commit(
        self,
        *,
        operator_id: str,
        field: str,
        basis_before: float,
        requested_after_unbounded: float,
        drivers: tuple[ReducerDriverContribution, ...],
    ) -> float:
        committed_after = clamp01(requested_after_unbounded)
        self.proposals.append(
            ReducerFieldProposal(
                write_sequence=self.next_sequence,
                stage_id=self.stage_id,
                operator_id=operator_id,
                field=field,
                basis_before=float(basis_before),
                requested_after_unbounded=float(requested_after_unbounded),
                committed_after=committed_after,
                unit="normalized_simulation_unit",
                constraint_id="clamp01",
                drivers=drivers,
            )
        )
        self.next_sequence += 1
        return committed_after


def _drivers(
    *items: tuple[ReducerDriverChannel, str, float],
) -> tuple[ReducerDriverContribution, ...]:
    return tuple(
        ReducerDriverContribution(
            channel=channel,
            label=label,
            contribution=float(value),
        )
        for channel, label, value in items
        if value != 0.0
    )


def apply_fast_update_traced(
    state: HumanState,
    model_input: ModelInput,
    *,
    processed_tick: int,
    access_pressure: float,
    write_sequence_start: int = 1,
) -> ReducerStepResult:
    """Apply the fast writer and retain its exact pre-clamp proposals."""

    writer = _ProposalWriter("fast-descriptive-update@0.1.0", write_sequence_start)
    energy_request = state.body.energy + model_input.energy_delta
    arousal_request = state.body.arousal + model_input.arousal_delta
    capacity_request = state.body.action_capacity + model_input.capacity_delta
    body = BodyState(
        energy=writer.commit(
            operator_id="fast.body.energy",
            field="body.energy",
            basis_before=state.body.energy,
            requested_after_unbounded=energy_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.energy_delta",
                    model_input.energy_delta,
                ),
            ),
        ),
        arousal=writer.commit(
            operator_id="fast.body.arousal",
            field="body.arousal",
            basis_before=state.body.arousal,
            requested_after_unbounded=arousal_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.arousal_delta",
                    model_input.arousal_delta,
                ),
            ),
        ),
        action_capacity=writer.commit(
            operator_id="fast.body.action_capacity",
            field="body.action_capacity",
            basis_before=state.body.action_capacity,
            requested_after_unbounded=capacity_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.capacity_delta",
                    model_input.capacity_delta,
                ),
            ),
        ),
    )
    attention_request = (
        state.access.attention_budget
        + model_input.attention_delta
        - 0.08 * model_input.time_pressure
        - 0.05 * access_pressure
        + 0.04 * model_input.soothing
    )
    interference_request = (
        0.82 * state.access.interference
        + 0.18 * model_input.memory_interference
        + 0.08 * access_pressure
    )
    queue_request = 0.65 * state.access.queue_load + 0.35 * access_pressure
    access = replace(
        state.access,
        attention_budget=writer.commit(
            operator_id="fast.access.attention_budget",
            field="access.attention_budget",
            basis_before=state.access.attention_budget,
            requested_after_unbounded=attention_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.attention_delta",
                    model_input.attention_delta,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.time_pressure",
                    -0.08 * model_input.time_pressure,
                ),
                (
                    ReducerDriverChannel.PROTOCOL_BRIDGE,
                    "legacy_v01_access_pressure_bridge",
                    -0.05 * access_pressure,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.soothing",
                    0.04 * model_input.soothing,
                ),
            ),
        ),
        interference=writer.commit(
            operator_id="fast.access.interference",
            field="access.interference",
            basis_before=state.access.interference,
            requested_after_unbounded=interference_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENDOGENOUS_DYNAMICS,
                    "interference_retention",
                    -0.18 * state.access.interference,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.memory_interference",
                    0.18 * model_input.memory_interference,
                ),
                (
                    ReducerDriverChannel.PROTOCOL_BRIDGE,
                    "legacy_v01_access_pressure_bridge",
                    0.08 * access_pressure,
                ),
            ),
        ),
        queue_load=writer.commit(
            operator_id="fast.access.queue_load",
            field="access.queue_load",
            basis_before=state.access.queue_load,
            requested_after_unbounded=queue_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENDOGENOUS_DYNAMICS,
                    "queue_load_retention",
                    -0.35 * state.access.queue_load,
                ),
                (
                    ReducerDriverChannel.PROTOCOL_BRIDGE,
                    "legacy_v01_access_pressure_bridge",
                    0.35 * access_pressure,
                ),
            ),
        ),
    )
    trust_input = model_input.trust_delta if model_input.source_is_external else 0.0
    boundary_input = (
        model_input.boundary_delta if model_input.source_is_external else 0.0
    )
    relationship = replace(
        state.relationship,
        trust=writer.commit(
            operator_id="fast.relationship.trust",
            field="relationship.trust",
            basis_before=state.relationship.trust,
            requested_after_unbounded=state.relationship.trust + trust_input,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "external_model_input.trust_delta",
                    trust_input,
                ),
            ),
        ),
        boundary_strain=writer.commit(
            operator_id="fast.relationship.boundary_strain",
            field="relationship.boundary_strain",
            basis_before=state.relationship.boundary_strain,
            requested_after_unbounded=(
                state.relationship.boundary_strain + boundary_input
            ),
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "external_model_input.boundary_delta",
                    boundary_input,
                ),
            ),
        ),
    )
    state_after = replace(
        state,
        clock=processed_tick,
        body=body,
        access=access,
        relationship=relationship,
    )
    return ReducerStepResult(state_after=state_after, proposals=tuple(writer.proposals))


def apply_fast_update(
    state: HumanState,
    model_input: ModelInput,
    *,
    processed_tick: int,
    access_pressure: float,
) -> HumanState:
    """Compatibility wrapper returning only the committed fast state."""

    return apply_fast_update_traced(
        state,
        model_input,
        processed_tick=processed_tick,
        access_pressure=access_pressure,
    ).state_after


def phenomenal_activation(
    state: HumanState,
    model_input: ModelInput,
) -> PhenomenalActivation:
    """Return the v0.1 simulation readout without certifying phenomenal ontology."""

    fatigue = 1.0 - state.body.energy
    interpreted_threat = (
        0.60 * state.associative.rejection_access
        + 0.40 * state.narrative.rejection_story
    ) * state.relationship.stake
    target = (
        0.24 * model_input.ambiguity
        + 0.18 * fatigue
        + 0.25 * interpreted_threat
        + 0.13 * model_input.time_pressure
        + 0.10 * state.access.interference
        + 0.10 * rejection_confidence(state)
        - 0.35 * model_input.soothing
    )
    distress = clamp01(
        0.62 * state.affective.residual_distress + 0.38 * clamp01(target)
    )
    urgency = clamp01(
        0.45 * model_input.time_pressure
        + 0.25 * state.body.arousal
        + 0.20 * distress
        + 0.10 * state.access.queue_load
    )
    ambiguity = clamp01(
        model_input.ambiguity
        + 0.20 * state.access.interference
        + 0.10 * state.access.queue_load
    )
    return PhenomenalActivation(
        distress=distress,
        urgency=urgency,
        ambiguity=ambiguity,
    )


def apply_slow_update_traced(
    state: HumanState,
    model_input: ModelInput,
    phenomenal: PhenomenalActivation,
    performance: PerformanceReceipt | None,
    *,
    write_sequence_start: int = 1,
) -> ReducerStepResult:
    """Apply the slow writer and retain every ordered pre-clamp proposal."""

    writer = _ProposalWriter("slow-descriptive-update@0.1.0", write_sequence_start)
    rejection_request = (
        state.associative.rejection_access
        + 0.0030 * phenomenal.distress * model_input.salience
        - 0.0025 * model_input.soothing * state.relationship.trust
    )
    ambiguity_request = (
        state.associative.ambiguity_sensitivity
        + 0.0010 * model_input.ambiguity
        - 0.0010 * model_input.soothing
    )
    associative = replace(
        state.associative,
        rejection_access=writer.commit(
            operator_id="slow.associative.rejection_access",
            field="associative.rejection_access",
            basis_before=state.associative.rejection_access,
            requested_after_unbounded=rejection_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.PHENOMENAL_COUPLING,
                    "phenomenal.distress_x_salience",
                    0.0030 * phenomenal.distress * model_input.salience,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "soothing_x_relationship_trust",
                    -0.0025 * model_input.soothing * state.relationship.trust,
                ),
            ),
        ),
        ambiguity_sensitivity=writer.commit(
            operator_id="slow.associative.ambiguity_sensitivity",
            field="associative.ambiguity_sensitivity",
            basis_before=state.associative.ambiguity_sensitivity,
            requested_after_unbounded=ambiguity_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.ambiguity",
                    0.0010 * model_input.ambiguity,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.soothing",
                    -0.0010 * model_input.soothing,
                ),
            ),
        ),
    )
    affective_tracking = state.affective.update_rate * (
        phenomenal.distress - state.affective.residual_distress
    )
    residual_request = (
        state.affective.residual_distress
        + affective_tracking
        - 0.025 * model_input.soothing
    )
    affective = replace(
        state.affective,
        residual_distress=writer.commit(
            operator_id="slow.affective.residual_distress",
            field="affective.residual_distress",
            basis_before=state.affective.residual_distress,
            requested_after_unbounded=residual_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.PHENOMENAL_COUPLING,
                    "affective_tracking",
                    affective_tracking,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.soothing",
                    -0.025 * model_input.soothing,
                ),
            ),
        ),
    )
    rejected = rejection_confidence(state)
    narrative_target = clamp01(0.55 * phenomenal.distress + 0.45 * rejected)
    rejection_story_request = (
        state.narrative.rejection_story
        + 0.0040 * (narrative_target - state.narrative.rejection_story)
    )
    security_coupling = 0.0035 * (
        state.relationship.trust
        - 0.40 * phenomenal.distress
        - state.narrative.relational_security
    )
    security_request = (
        state.narrative.relational_security
        + security_coupling
        + 0.0020 * model_input.soothing
    )
    narrative = replace(
        state.narrative,
        rejection_story=writer.commit(
            operator_id="slow.narrative.rejection_story",
            field="narrative.rejection_story",
            basis_before=state.narrative.rejection_story,
            requested_after_unbounded=rejection_story_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.PHENOMENAL_COUPLING,
                    "phenomenal.distress_target",
                    0.0040 * 0.55 * phenomenal.distress,
                ),
                (
                    ReducerDriverChannel.EVIDENCE_ASSESSMENT_COUPLING,
                    "rejection_confidence_target",
                    0.0040 * 0.45 * rejected,
                ),
                (
                    ReducerDriverChannel.ENDOGENOUS_DYNAMICS,
                    "narrative_retention",
                    -0.0040 * state.narrative.rejection_story,
                ),
            ),
        ),
        relational_security=writer.commit(
            operator_id="slow.narrative.relational_security",
            field="narrative.relational_security",
            basis_before=state.narrative.relational_security,
            requested_after_unbounded=security_request,
            drivers=_drivers(
                (
                    ReducerDriverChannel.ENDOGENOUS_DYNAMICS,
                    "relationship_x_narrative_coupling",
                    0.0035
                    * (
                        state.relationship.trust
                        - state.narrative.relational_security
                    ),
                ),
                (
                    ReducerDriverChannel.PHENOMENAL_COUPLING,
                    "phenomenal.distress",
                    -0.0035 * 0.40 * phenomenal.distress,
                ),
                (
                    ReducerDriverChannel.ENCODED_INPUT,
                    "model_input.soothing",
                    0.0020 * model_input.soothing,
                ),
            ),
        ),
    )
    habit = state.habit
    relationship = state.relationship
    body = state.body
    if performance is not None:
        cost = {"ask": 0.025, "accuse": 0.045, "withdraw": 0.020}.get(
            performance.action_kind, 0.0
        )
        body = replace(
            body,
            energy=writer.commit(
                operator_id="slow.action.body.energy",
                field="body.energy",
                basis_before=body.energy,
                requested_after_unbounded=body.energy - cost,
                drivers=_drivers(
                    (
                        ReducerDriverChannel.ACTION_CONSEQUENCE,
                        f"performance.{performance.action_kind}.energy_cost",
                        -cost,
                    ),
                ),
            ),
        )
        if performance.action_kind == "accuse":
            habit = replace(
                habit,
                impulsivity=writer.commit(
                    operator_id="slow.action.habit.impulsivity",
                    field="habit.impulsivity",
                    basis_before=habit.impulsivity,
                    requested_after_unbounded=habit.impulsivity + 0.0010,
                    drivers=_drivers(
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.impulsivity",
                            0.0010,
                        ),
                    ),
                ),
            )
            relationship = replace(
                relationship,
                trust=writer.commit(
                    operator_id="slow.action.relationship.trust",
                    field="relationship.trust",
                    basis_before=relationship.trust,
                    requested_after_unbounded=relationship.trust - 0.020,
                    drivers=_drivers(
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.trust",
                            -0.020,
                        ),
                    ),
                ),
                boundary_strain=writer.commit(
                    operator_id="slow.action.relationship.boundary_strain",
                    field="relationship.boundary_strain",
                    basis_before=relationship.boundary_strain,
                    requested_after_unbounded=relationship.boundary_strain + 0.040,
                    drivers=_drivers(
                        (
                            ReducerDriverChannel.ACTION_CONSEQUENCE,
                            "performance.accuse.boundary_strain",
                            0.040,
                        ),
                    ),
                ),
            )
    if model_input.soothing > 0.0:
        habit = replace(
            habit,
            impulsivity=writer.commit(
                operator_id="slow.soothing.habit.impulsivity",
                field="habit.impulsivity",
                basis_before=habit.impulsivity,
                requested_after_unbounded=(
                    habit.impulsivity - 0.0005 * model_input.soothing
                ),
                drivers=_drivers(
                    (
                        ReducerDriverChannel.ENCODED_INPUT,
                        "model_input.soothing",
                        -0.0005 * model_input.soothing,
                    ),
                ),
            ),
        )

    state_after = replace(
        state,
        body=body,
        associative=associative,
        affective=affective,
        narrative=narrative,
        habit=habit,
        relationship=relationship,
    )
    return ReducerStepResult(state_after=state_after, proposals=tuple(writer.proposals))


def apply_slow_update(
    state: HumanState,
    model_input: ModelInput,
    phenomenal: PhenomenalActivation,
    performance: PerformanceReceipt | None,
) -> HumanState:
    """Compatibility wrapper returning only the committed slow state."""

    return apply_slow_update_traced(
        state,
        model_input,
        phenomenal,
        performance,
    ).state_after
