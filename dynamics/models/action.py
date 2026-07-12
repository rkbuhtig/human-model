"""Descriptive intent selection, motor feasibility, and action production."""

from __future__ import annotations

from ..contract.records import (
    ACTION_OPPORTUNITY_RULE_V01,
    ActionOpportunity,
    ActionAttempt,
    ActionOccurrence,
    IntentDecision,
    MotorFeasibility,
    PerformanceReceipt,
    action_opportunity_id,
)
from ..interfaces import ModelInput, clamp01
from .state import HumanState, RoutedCandidate


EXTERNAL_ACTION_REQUIREMENTS = {"ask": 0.35, "accuse": 0.50, "withdraw": 0.30}


def run_action_pipeline(
    state: HumanState,
    model_input: ModelInput,
    routed: tuple[RoutedCandidate, ...],
    opportunity: ActionOpportunity | None = None,
) -> tuple[
    IntentDecision | None,
    ActionAttempt | None,
    PerformanceReceipt | None,
    ActionOccurrence | None,
]:
    if opportunity is None:
        return None, None, None, None
    if (
        opportunity.event_id != model_input.event_id
        or opportunity.opportunity_id != action_opportunity_id(model_input.event_id)
        or opportunity.rule_id != ACTION_OPPORTUNITY_RULE_V01
    ):
        raise ValueError("action opportunity does not match the model input")

    selected = max(routed, key=lambda item: item.probability)
    action = selected.candidate.action_kind
    intent = IntentDecision(
        intent_id=f"intent:{model_input.event_id}",
        action_kind="hold" if action == "wait" else action,
        selected_candidate_id=selected.candidate.candidate_id,
        coercion=model_input.coercion,
        action_opportunity_id=opportunity.opportunity_id,
    )
    if action not in EXTERNAL_ACTION_REQUIREMENTS:
        return intent, None, None, None

    available = clamp01(
        0.65 * state.body.energy
        + 0.35 * state.body.action_capacity
        - 0.25 * state.access.queue_load
    )
    required = EXTERNAL_ACTION_REQUIREMENTS[action]
    feasibility = MotorFeasibility(
        feasibility_id=f"motor-feasibility:{model_input.event_id}",
        feasible=available >= required,
        available_capacity=available,
        required_capacity=required,
    )
    attempt = ActionAttempt(
        attempt_id=f"attempt:{model_input.event_id}",
        intent_id=intent.intent_id,
        action_kind=action,
        motor_feasibility=feasibility,
        tick=state.clock,
    )
    if not feasibility.feasible:
        return intent, attempt, None, None

    performance = PerformanceReceipt(
        receipt_id=f"performance:{model_input.event_id}",
        attempt_id=attempt.attempt_id,
        action_kind=action,
        agency=clamp01(1.0 - model_input.coercion),
        tick=state.clock,
    )
    occurrence = ActionOccurrence(
        occurrence_id=f"action-occurrence:{model_input.event_id}",
        caused_by_receipt_id=performance.receipt_id,
        action_kind=action,
        tick=state.clock,
    )
    return intent, attempt, performance, occurrence
