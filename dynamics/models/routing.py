"""Non-certifying candidate routing over an encoded model input."""

from __future__ import annotations

import math

from ..interfaces import ModelInput
from .state import (
    Candidate,
    HumanState,
    InfluenceTerm,
    PhenomenalActivation,
    RoutedCandidate,
)


BASE_ACTIONS = ("wait", "ask", "accuse", "withdraw")
FANOUT_ACTIONS = ("recheck", "ruminate", "seek_third_party", "draft_unsent")


def _softmax(scores: list[float], temperature: float) -> list[float]:
    if temperature <= 0.0:
        raise ValueError("temperature must be positive")
    scaled = [score / temperature for score in scores]
    anchor = max(scaled)
    weights = [math.exp(value - anchor) for value in scaled]
    total = sum(weights)
    if not math.isfinite(total) or total <= 0.0:
        raise ValueError("routing distribution is not normalizable")
    return [weight / total for weight in weights]


def rejection_confidence(state: HumanState) -> float:
    relevant = [
        claim.confidence
        for claim in state.evidence_assessment.claims
        if "reject" in claim.claim_id or "avoid" in claim.claim_id
    ]
    return max(relevant, default=0.0)


def route_candidates(
    state: HumanState,
    model_input: ModelInput,
    phenomenal: PhenomenalActivation,
    *,
    temperature: float,
) -> tuple[RoutedCandidate, ...]:
    extra_count = min(
        len(FANOUT_ACTIONS),
        round(model_input.candidate_fanout * len(FANOUT_ACTIONS)),
    )
    action_kinds = BASE_ACTIONS + FANOUT_ACTIONS[:extra_count]
    rejected = rejection_confidence(state)

    common = {
        "wait": (
            ("base", 0.20),
            ("trust", 0.90 * state.relationship.trust),
            ("low_distress", 0.50 * (1.0 - phenomenal.distress)),
            ("low_pressure", 0.25 * (1.0 - model_input.time_pressure)),
        ),
        "ask": (
            ("base", 0.15),
            ("ambiguity", 0.65 * phenomenal.ambiguity),
            ("distress", 0.35 * phenomenal.distress),
            ("trust", 0.35 * state.relationship.trust),
            ("access", 0.25 * (1.0 - state.access.interference)),
        ),
        "accuse": (
            ("base", -0.10),
            ("distress", 0.85 * phenomenal.distress),
            ("pressure", 0.75 * model_input.time_pressure),
            ("habit", 0.65 * state.habit.impulsivity),
            ("rejection_claim", 0.35 * rejected),
            ("trust_brake", -0.65 * state.relationship.trust),
        ),
        "withdraw": (
            ("base", 0.00),
            ("distress", 0.75 * phenomenal.distress),
            ("association", 0.60 * state.associative.rejection_access),
            ("habit", 0.45 * state.habit.withdrawal_bias),
            ("interference", 0.30 * state.access.interference),
            ("trust_brake", -0.30 * state.relationship.trust),
        ),
        "recheck": (
            ("base", 0.05),
            ("ambiguity", 0.70 * phenomenal.ambiguity),
            ("attention", 0.30 * state.access.attention_budget),
        ),
        "ruminate": (
            ("base", -0.05),
            ("distress", 0.80 * phenomenal.distress),
            ("interference", 0.55 * state.access.interference),
        ),
        "seek_third_party": (
            ("base", -0.05),
            ("ambiguity", 0.55 * phenomenal.ambiguity),
            ("stake", 0.40 * state.relationship.stake),
        ),
        "draft_unsent": (
            ("base", -0.05),
            ("urgency", 0.60 * phenomenal.urgency),
            ("distress", 0.30 * phenomenal.distress),
        ),
    }

    candidates = []
    scores = []
    terms_by_action = []
    for action in action_kinds:
        terms = tuple(
            InfluenceTerm(channel=name, delta=value) for name, value in common[action]
        )
        candidates.append(
            Candidate(
                candidate_id=f"cand:{model_input.event_id}:{action}",
                action_kind=action,
            )
        )
        scores.append(sum(term.delta for term in terms))
        terms_by_action.append(terms)
    probabilities = _softmax(scores, temperature)
    return tuple(
        RoutedCandidate(
            candidate=candidate,
            salience=score,
            probability=probability,
            terms=terms,
        )
        for candidate, score, probability, terms in zip(
            candidates, scores, probabilities, terms_by_action
        )
    )
