"""Descriptive fast, phenomenal-readout, and slow update hypotheses."""

from __future__ import annotations

from dataclasses import replace

from ..contract.records import PerformanceReceipt
from ..interfaces import ModelInput, clamp01
from .routing import rejection_confidence
from .state import BodyState, HumanState, PhenomenalActivation


def apply_fast_update(
    state: HumanState,
    model_input: ModelInput,
    *,
    processed_tick: int,
    access_pressure: float,
) -> HumanState:
    """Apply immediately available body, access, and relational input effects."""

    body = BodyState(
        energy=state.body.energy + model_input.energy_delta,
        arousal=state.body.arousal + model_input.arousal_delta,
        action_capacity=state.body.action_capacity + model_input.capacity_delta,
    ).bounded()
    access = replace(
        state.access,
        attention_budget=clamp01(
            state.access.attention_budget
            + model_input.attention_delta
            - 0.08 * model_input.time_pressure
            - 0.05 * access_pressure
            + 0.04 * model_input.soothing
        ),
        interference=clamp01(
            0.82 * state.access.interference
            + 0.18 * model_input.memory_interference
            + 0.08 * access_pressure
        ),
        queue_load=clamp01(0.65 * state.access.queue_load + 0.35 * access_pressure),
    )
    relationship = replace(
        state.relationship,
        trust=clamp01(
            state.relationship.trust
            + (model_input.trust_delta if model_input.source_is_external else 0.0)
        ),
        boundary_strain=clamp01(
            state.relationship.boundary_strain
            + (
                model_input.boundary_delta
                if model_input.source_is_external
                else 0.0
            )
        ),
    )
    return replace(
        state,
        clock=processed_tick,
        body=body,
        access=access,
        relationship=relationship,
    )


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


def apply_slow_update(
    state: HumanState,
    model_input: ModelInput,
    phenomenal: PhenomenalActivation,
    performance: PerformanceReceipt | None,
) -> HumanState:
    associative = replace(
        state.associative,
        rejection_access=clamp01(
            state.associative.rejection_access
            + 0.0030 * phenomenal.distress * model_input.salience
            - 0.0025 * model_input.soothing * state.relationship.trust
        ),
        ambiguity_sensitivity=clamp01(
            state.associative.ambiguity_sensitivity
            + 0.0010 * model_input.ambiguity
            - 0.0010 * model_input.soothing
        ),
    )
    affective = replace(
        state.affective,
        residual_distress=clamp01(
            state.affective.residual_distress
            + state.affective.update_rate
            * (phenomenal.distress - state.affective.residual_distress)
            - 0.025 * model_input.soothing
        ),
    )
    rejected = rejection_confidence(state)
    narrative_target = clamp01(0.55 * phenomenal.distress + 0.45 * rejected)
    narrative = replace(
        state.narrative,
        rejection_story=clamp01(
            state.narrative.rejection_story
            + 0.0040 * (narrative_target - state.narrative.rejection_story)
        ),
        relational_security=clamp01(
            state.narrative.relational_security
            + 0.0035
            * (
                state.relationship.trust
                - 0.40 * phenomenal.distress
                - state.narrative.relational_security
            )
            + 0.0020 * model_input.soothing
        ),
    )
    habit = state.habit
    relationship = state.relationship
    body = state.body
    if performance is not None:
        cost = {"ask": 0.025, "accuse": 0.045, "withdraw": 0.020}.get(
            performance.action_kind, 0.0
        )
        body = replace(body, energy=clamp01(body.energy - cost))
        if performance.action_kind == "accuse":
            habit = replace(
                habit,
                impulsivity=clamp01(habit.impulsivity + 0.0010),
            )
            relationship = replace(
                relationship,
                trust=clamp01(relationship.trust - 0.020),
                boundary_strain=clamp01(relationship.boundary_strain + 0.040),
            )
    if model_input.soothing > 0.0:
        habit = replace(
            habit,
            impulsivity=clamp01(
                habit.impulsivity - 0.0005 * model_input.soothing
            ),
        )

    return replace(
        state,
        body=body,
        associative=associative,
        affective=affective,
        narrative=narrative,
        habit=habit,
        relationship=relationship,
    )
