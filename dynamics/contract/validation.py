"""Validators for certification provenance and action-record lineage."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

from .assessment import EvidenceAssessmentPolicy
from .grounding import GROUNDING_RULES
from .records import (
    ACTION_OPPORTUNITY_RULE_V01,
    ActionOpportunity,
    ActionAttempt,
    ActionOccurrence,
    EvidenceAssessmentState,
    EvidenceLink,
    EvidenceRelation,
    IntentDecision,
    JudgmentStance,
    ObservationArtifact,
    PerformanceReceipt,
    ProvenanceKind,
    action_opportunity_id,
)


def validate_action_opportunity(
    opportunity: ActionOpportunity | None,
    intent: IntentDecision | None,
    *,
    event_id: str,
) -> list[str]:
    """Validate the protocol-writer → opportunity → intent lineage."""

    if intent is not None and opportunity is None:
        return ["PHANTOM_INTENT_WITHOUT_ACTION_OPPORTUNITY"]
    if opportunity is None:
        return []
    errors = []
    if opportunity.event_id != event_id:
        errors.append("ACTION_OPPORTUNITY_EVENT_MISMATCH")
    if opportunity.opportunity_id != action_opportunity_id(event_id):
        errors.append("ACTION_OPPORTUNITY_IDENTITY_MISMATCH")
    if opportunity.rule_id != ACTION_OPPORTUNITY_RULE_V01:
        errors.append("ACTION_OPPORTUNITY_RULE_MISMATCH")
    if intent is not None and intent.action_opportunity_id != opportunity.opportunity_id:
        errors.append("INTENT_ACTION_OPPORTUNITY_MISMATCH")
    return errors


def validate_evidence_assessment(
    state: EvidenceAssessmentState,
    links_by_id: Mapping[str, EvidenceLink],
    artifacts_by_id: Mapping[str, ObservationArtifact],
    new_links: Sequence[EvidenceLink] = (),
    *,
    policy: EvidenceAssessmentPolicy,
    full_audit: bool = False,
) -> list[str]:
    errors = []
    links_to_validate = dict(links_by_id) if full_audit else {}
    for link in new_links:
        links_to_validate.setdefault(link.link_id, link)
    if full_audit:
        for index_id, link in links_by_id.items():
            if index_id != link.link_id:
                errors.append(f"AUTHORITY_LINK_INDEX_MISMATCH:{index_id}")
    for link in links_to_validate.values():
        artifact = artifacts_by_id.get(link.artifact_id)
        if not link.link_id or not link.claim_id or not link.scope or not link.independence_key:
            errors.append(f"AUTHORITY_INCOMPLETE_LINK:{link.link_id}")
        if artifact is None:
            errors.append(f"PROVENANCE_MISSING_ARTIFACT:{link.link_id}")
        if link.provenance_kind is ProvenanceKind.IMAGINATION:
            errors.append(f"AUTHORITY_IMAGINATION_CAST:{link.link_id}")
        if artifact is not None and not artifact.external:
            errors.append(f"AUTHORITY_INTERNAL_ARTIFACT:{link.link_id}")
        if artifact is not None and artifact.provenance_kind is not link.provenance_kind:
            errors.append(f"PROVENANCE_KIND_MISMATCH:{link.link_id}")
        if artifact is not None:
            expected_link_id = (
                f"link:{artifact.event_id}:{link.claim_id}:"
                f"{link.scope}:{link.relation.value}"
            )
            if link.link_id != expected_link_id:
                errors.append(f"AUTHORITY_LINK_IDENTITY_MISMATCH:{link.link_id}")
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

    claim_keys: set[tuple[str, str]] = set()
    for claim in state.claims:
        claim_key = (claim.claim_id, claim.scope)
        if claim_key in claim_keys:
            errors.append(f"AUTHORITY_DUPLICATE_CLAIM_KEY:{claim.claim_id}:{claim.scope}")
        claim_keys.add(claim_key)
        if not claim.claim_id or not claim.scope:
            errors.append(f"AUTHORITY_INCOMPLETE_CLAIM:{claim.claim_id}:{claim.scope}")
        if not math.isfinite(claim.confidence):
            errors.append(f"AUTHORITY_NONFINITE_CLAIM:{claim.claim_id}:{claim.scope}")
        for relation, contributions in (
            (EvidenceRelation.SUPPORTS, claim.supports),
            (EvidenceRelation.CONTRADICTS, claim.contradicts),
        ):
            independence_keys: set[str] = set()
            for contribution in contributions:
                if contribution.independence_key in independence_keys:
                    errors.append(
                        "AUTHORITY_DUPLICATE_INDEPENDENCE_KEY:"
                        f"{claim.claim_id}:{relation.value}:"
                        f"{contribution.independence_key}"
                    )
                independence_keys.add(contribution.independence_key)
                link = links_by_id.get(contribution.link_id)
                if (
                    link is None
                    or link.claim_id != claim.claim_id
                    or link.scope != claim.scope
                    or link.relation is not relation
                    or link.independence_key != contribution.independence_key
                    or not math.isfinite(contribution.strength)
                    or not 0.0 <= contribution.strength <= 1.0
                    or not math.isfinite(link.strength)
                    or abs(link.strength - contribution.strength) > 1e-12
                ):
                    errors.append(
                        "AUTHORITY_CONTRIBUTION_LINK_MISMATCH:"
                        f"{claim.claim_id}:{contribution.link_id}"
                    )
        expected_grounds = tuple(item.link_id for item in claim.supports)
        if claim.grounds != expected_grounds:
            errors.append(
                f"AUTHORITY_GROUNDS_SET_MISMATCH:{claim.claim_id}:{claim.scope}"
            )
        if claim.stance is not JudgmentStance.ADOPTED:
            continue
        if (
            claim.confidence < policy.release_threshold
            or claim.support_mass < policy.minimum_ground_mass
        ):
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


def validate_action_lineage(
    intent: IntentDecision | None,
    attempt: ActionAttempt | None,
    receipt: PerformanceReceipt | None,
    occurrence: ActionOccurrence | None,
) -> list[str]:
    errors = []
    if intent is not None and (
        not math.isfinite(intent.coercion) or not 0.0 <= intent.coercion <= 1.0
    ):
        errors.append("INTENT_COERCION_BOUND")
    if attempt is not None:
        if intent is None or attempt.intent_id != intent.intent_id:
            errors.append("PHANTOM_ATTEMPT")
        elif attempt.action_kind != intent.action_kind:
            errors.append("ACTION_KIND_MISMATCH_INTENT_ATTEMPT")
        feasibility = attempt.motor_feasibility
        if (
            not math.isfinite(feasibility.available_capacity)
            or not 0.0 <= feasibility.available_capacity <= 1.0
            or not math.isfinite(feasibility.required_capacity)
            or not 0.0 <= feasibility.required_capacity <= 1.0
        ):
            # Preserve the v0.1 error vocabulary during the compatibility window.
            errors.append("BODY_AUTHORIZATION_CAPACITY_BOUND")
        expected_feasible = (
            feasibility.available_capacity >= feasibility.required_capacity
        )
        if feasibility.feasible != expected_feasible:
            errors.append("BODY_AUTHORIZATION_ARITHMETIC_MISMATCH")
    if receipt is not None:
        if not math.isfinite(receipt.agency) or not 0.0 <= receipt.agency <= 1.0:
            errors.append("PERFORMANCE_AGENCY_BOUND")
        if attempt is None or receipt.attempt_id != attempt.attempt_id:
            errors.append("PHANTOM_PERFORMANCE")
        elif not attempt.motor_feasibility.feasible:
            errors.append("PHANTOM_BLOCKED_PERFORMANCE")
        elif receipt.action_kind != attempt.action_kind:
            errors.append("ACTION_KIND_MISMATCH_ATTEMPT_PERFORMANCE")
        elif receipt.tick < attempt.tick:
            errors.append("ACTION_TIME_REVERSAL")
    if occurrence is not None:
        if receipt is None or occurrence.caused_by_receipt_id != receipt.receipt_id:
            errors.append("PHANTOM_ACTION_OCCURRENCE_WITHOUT_PERFORMANCE")
        elif occurrence.action_kind != receipt.action_kind:
            errors.append("ACTION_KIND_MISMATCH_PERFORMANCE_OCCURRENCE")
        elif occurrence.tick < receipt.tick:
            errors.append("ACTION_OCCURRENCE_TIME_REVERSAL")
    return errors
