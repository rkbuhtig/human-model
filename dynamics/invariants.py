"""Hard simulation-contract checks."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

from .epistemics import GROUNDING_RULES

from .types import (
    ActionAttempt,
    ActionOccurrence,
    EpistemicState,
    EvidenceLink,
    EvidenceRelation,
    HumanState,
    IntentDecision,
    JudgmentStance,
    ObservationArtifact,
    PerformanceReceipt,
    ProvenanceKind,
    RoutedCandidate,
    iter_unit_values,
)


def validate_state_bounds(state: HumanState) -> list[str]:
    errors = []
    for name, value in iter_unit_values(state):
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            errors.append(f"NUMERIC_BOUND:{name}:{value}")
    return errors


def validate_distribution(routed: Sequence[RoutedCandidate]) -> list[str]:
    if not routed:
        return ["ROUTING_EMPTY"]
    probabilities = [item.probability for item in routed]
    errors = []
    if any(not math.isfinite(value) or value < 0.0 for value in probabilities):
        errors.append("ROUTING_NONFINITE")
    if abs(sum(probabilities) - 1.0) > 1e-9:
        errors.append(f"ROUTING_NOT_NORMALIZED:{sum(probabilities)}")
    return errors


def validate_epistemics(
    state: EpistemicState,
    links_by_id: Mapping[str, EvidenceLink],
    artifacts_by_id: Mapping[str, ObservationArtifact],
    new_links: Sequence[EvidenceLink] = (),
    *,
    adoption_threshold: float,
    release_threshold: float,
    minimum_ground_mass: float,
) -> list[str]:
    errors = []
    for link in new_links:
        artifact = artifacts_by_id.get(link.artifact_id)
        if artifact is None:
            errors.append(f"PROVENANCE_MISSING_ARTIFACT:{link.link_id}")
        if link.provenance_kind is ProvenanceKind.IMAGINATION:
            errors.append(f"AUTHORITY_IMAGINATION_CAST:{link.link_id}")
        if artifact is not None and not artifact.external:
            errors.append(f"AUTHORITY_INTERNAL_ARTIFACT:{link.link_id}")
        if artifact is not None and artifact.provenance_kind is not link.provenance_kind:
            errors.append(f"PROVENANCE_KIND_MISMATCH:{link.link_id}")
        if not math.isfinite(link.strength) or not 0.0 <= link.strength <= 1.0:
            errors.append(f"AUTHORITY_INVALID_LINK_STRENGTH:{link.link_id}")
        rule = GROUNDING_RULES.get(link.grounding_rule_id)
        if rule is None:
            errors.append(f"AUTHORITY_UNKNOWN_LINK_RULE:{link.link_id}")
        elif artifact is not None:
            if (
                artifact.kind not in rule.event_kinds
                or link.claim_id not in rule.claim_ids
                or link.relation is not rule.relation
                or link.provenance_kind not in rule.provenance_kinds
                or link.strength > rule.maximum_strength + 1e-12
            ):
                errors.append(f"AUTHORITY_LINK_RULE_MISMATCH:{link.link_id}")

    for claim in state.claims:
        for relation, contributions in (
            (EvidenceRelation.SUPPORTS, claim.supports),
            (EvidenceRelation.CONTRADICTS, claim.contradicts),
        ):
            for contribution in contributions:
                link = links_by_id.get(contribution.link_id)
                if (
                    link is None
                    or link.claim_id != claim.claim_id
                    or link.scope != claim.scope
                    or link.relation is not relation
                    or link.independence_key != contribution.independence_key
                    or abs(link.strength - contribution.strength) > 1e-12
                ):
                    errors.append(
                        f"AUTHORITY_CONTRIBUTION_LINK_MISMATCH:{claim.claim_id}:{contribution.link_id}"
                    )
        expected_grounds = tuple(item.link_id for item in claim.supports)
        if claim.grounds != expected_grounds:
            errors.append(f"AUTHORITY_GROUNDS_SET_MISMATCH:{claim.claim_id}:{claim.scope}")
        if claim.stance is not JudgmentStance.ADOPTED:
            continue
        # Acquisition uses adoption_threshold in the reducer.  Once adopted,
        # hysteresis permits the stance to persist until release_threshold.
        if claim.confidence < release_threshold or claim.support_mass < minimum_ground_mass:
            errors.append(f"AUTHORITY_UNGROUNDED_ADOPTION:{claim.claim_id}")
        if not claim.grounds:
            errors.append(f"AUTHORITY_MISSING_GROUNDS:{claim.claim_id}")
        for ground in claim.grounds:
            link = links_by_id.get(ground)
            if (
                link is None
                or link.claim_id != claim.claim_id
                or link.scope != claim.scope
                or link.relation is not EvidenceRelation.SUPPORTS
            ):
                errors.append(f"AUTHORITY_INVALID_GROUND:{claim.claim_id}:{ground}")
    return errors


def validate_action_chain(
    intent: IntentDecision | None,
    attempt: ActionAttempt | None,
    receipt: PerformanceReceipt | None,
    occurrence: ActionOccurrence | None,
    routed: Sequence[RoutedCandidate] = (),
) -> list[str]:
    errors = []
    if intent is not None:
        if not math.isfinite(intent.coercion) or not 0.0 <= intent.coercion <= 1.0:
            errors.append("INTENT_COERCION_BOUND")
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
    if attempt is not None:
        if intent is None or attempt.intent_id != intent.intent_id:
            errors.append("PHANTOM_ATTEMPT")
        elif attempt.action_kind != intent.action_kind:
            errors.append("ACTION_KIND_MISMATCH_INTENT_ATTEMPT")
        authorization = attempt.authorization
        if (
            not math.isfinite(authorization.available_capacity)
            or not 0.0 <= authorization.available_capacity <= 1.0
            or not math.isfinite(authorization.required_capacity)
            or not 0.0 <= authorization.required_capacity <= 1.0
        ):
            errors.append("BODY_AUTHORIZATION_CAPACITY_BOUND")
        expected_allowed = authorization.available_capacity >= authorization.required_capacity
        if authorization.allowed != expected_allowed:
            errors.append("BODY_AUTHORIZATION_ARITHMETIC_MISMATCH")
    if receipt is not None:
        if not math.isfinite(receipt.agency) or not 0.0 <= receipt.agency <= 1.0:
            errors.append("PERFORMANCE_AGENCY_BOUND")
        if attempt is None or receipt.attempt_id != attempt.attempt_id:
            errors.append("PHANTOM_PERFORMANCE")
        elif not attempt.authorization.allowed:
            errors.append("PHANTOM_BLOCKED_PERFORMANCE")
        elif receipt.action_kind != attempt.action_kind:
            errors.append("ACTION_KIND_MISMATCH_ATTEMPT_PERFORMANCE")
        elif receipt.tick < attempt.tick:
            errors.append("ACTION_TIME_REVERSAL")
        elif intent is not None and abs(receipt.agency - (1.0 - intent.coercion)) > 1e-12:
            errors.append("AGENCY_COERCION_MISMATCH")
    if occurrence is not None:
        if receipt is None or occurrence.caused_by_receipt_id != receipt.receipt_id:
            errors.append("PHANTOM_ACTION_OCCURRENCE_WITHOUT_PERFORMANCE")
        elif occurrence.action_kind != receipt.action_kind:
            errors.append("ACTION_KIND_MISMATCH_PERFORMANCE_OCCURRENCE")
        elif occurrence.tick < receipt.tick:
            errors.append("ACTION_OCCURRENCE_TIME_REVERSAL")
    return errors
