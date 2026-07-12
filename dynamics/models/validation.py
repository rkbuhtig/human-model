"""Validators for descriptive model outputs, not certification lineage."""

from __future__ import annotations

import math
from typing import Sequence

from ..contract.records import IntentDecision, PerformanceReceipt
from .state import HumanState, RoutedCandidate, iter_unit_values


def validate_state_bounds(state: HumanState) -> list[str]:
    errors = []
    for name, value in iter_unit_values(state):
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            errors.append(f"NUMERIC_BOUND:{name}:{value}")
    return errors


def validate_routing_distribution(routed: Sequence[RoutedCandidate]) -> list[str]:
    if not routed:
        return ["ROUTING_EMPTY"]
    probabilities = [item.probability for item in routed]
    errors = []
    if any(not math.isfinite(value) or value < 0.0 for value in probabilities):
        errors.append("ROUTING_NONFINITE")
    if abs(sum(probabilities) - 1.0) > 1e-9:
        errors.append(f"ROUTING_NOT_NORMALIZED:{sum(probabilities)}")
    return errors


def validate_intent_selection(
    intent: IntentDecision | None,
    routed: Sequence[RoutedCandidate],
) -> list[str]:
    if intent is None:
        return []
    errors = []
    selected = [
        item.candidate
        for item in routed
        if item.candidate.candidate_id == intent.selected_candidate_id
    ]
    if len(selected) != 1:
        errors.append("INTENT_CANDIDATE_NOT_ROUTED")
    else:
        expected_action_kind = (
            "hold" if selected[0].action_kind == "wait" else selected[0].action_kind
        )
        if intent.action_kind != expected_action_kind:
            errors.append("ACTION_KIND_MISMATCH_CANDIDATE_INTENT")
    return errors


def validate_agency_hypothesis(
    intent: IntentDecision | None,
    receipt: PerformanceReceipt | None,
) -> list[str]:
    if intent is None or receipt is None:
        return []
    if abs(receipt.agency - (1.0 - intent.coercion)) > 1e-12:
        return ["AGENCY_COERCION_MISMATCH"]
    return []
