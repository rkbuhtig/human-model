"""Claim-specific evidence grounding and atomic factual adjudication."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import chain

from .types import (
    ClaimState,
    EpistemicState,
    EvidenceLink,
    EvidenceRelation,
    JudgmentStance,
    ObservationArtifact,
    ProvenanceKind,
    ScenarioEvent,
    SourceContribution,
)


@dataclass(frozen=True, slots=True)
class GroundingRule:
    rule_id: str
    event_kinds: frozenset[str]
    claim_ids: frozenset[str]
    relation: EvidenceRelation
    provenance_kinds: frozenset[ProvenanceKind]
    maximum_strength: float


def _rule(
    rule_id: str,
    event_kinds: tuple[str, ...],
    claim_ids: tuple[str, ...],
    relation: EvidenceRelation,
    provenance_kinds: tuple[ProvenanceKind, ...],
    maximum_strength: float,
) -> GroundingRule:
    return GroundingRule(
        rule_id=rule_id,
        event_kinds=frozenset(event_kinds),
        claim_ids=frozenset(claim_ids),
        relation=relation,
        provenance_kinds=frozenset(provenance_kinds),
        maximum_strength=maximum_strength,
    )


# Simulation-contract allowlist.  A source artifact cannot link to an arbitrary
# claim merely because a scenario payload says ``supports``.
GROUNDING_RULES = {
    rule.rule_id: rule
    for rule in (
        _rule(
            "self-performed-send",
            ("performed_message_send",),
            ("C_SENT_message_was_sent",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.PERFORMED_ACTION,),
            1.0,
        ),
        _rule(
            "observe-no-reply",
            ("no_reply_observed", "ambiguous_no_reply_cue"),
            ("C0_no_reply_observed_by_t1", "C0_no_reply_observed"),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.DIRECT_OBSERVATION,),
            0.95,
        ),
        _rule(
            "observe-platform-online",
            ("platform_online_indicator",),
            ("C1_platform_displayed_online",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.DIRECT_OBSERVATION,),
            0.90,
        ),
        _rule(
            "observe-friend-speech",
            ("friend_interpretation",),
            ("C5_friend_said_avoidance",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.TESTIMONY,),
            0.95,
        ),
        _rule(
            "testimony-avoidance",
            (
                "friend_interpretation",
                "repeated_adversarial_rumor",
                "conflicting_testimony",
                "counterpart_explanation_message",
            ),
            ("C3_counterpart_intentionally_avoids",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.TESTIMONY,),
            0.80,
        ),
        _rule(
            "testimony-busy-statement",
            ("counterpart_explanation_message",),
            ("C6_counterpart_stated_busy",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.TESTIMONY,),
            0.99,
        ),
        _rule(
            "testimony-causal-explanation",
            ("counterpart_explanation_message",),
            ("C8_busy_was_actual_cause",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.TESTIMONY,),
            0.60,
        ),
        _rule(
            "testimony-denies-avoidance",
            ("counterpart_explanation_message",),
            ("C3_counterpart_intentionally_avoids",),
            EvidenceRelation.CONTRADICTS,
            (ProvenanceKind.TESTIMONY,),
            0.70,
        ),
        _rule(
            "testimony-denies-rejection",
            ("counterpart_explanation_message",),
            ("C4_counterpart_rejects_relationship",),
            EvidenceRelation.CONTRADICTS,
            (ProvenanceKind.TESTIMONY,),
            0.65,
        ),
        _rule(
            "public-schedule-record",
            ("independent_schedule_confirmation", "independent_confirmation"),
            ("C7_schedule_conflict_existed",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.PUBLIC_RECORD,),
            0.95,
        ),
        _rule(
            "schedule-weighs-against-avoidance",
            ("independent_schedule_confirmation", "independent_confirmation"),
            ("C3_counterpart_intentionally_avoids",),
            EvidenceRelation.CONTRADICTS,
            (ProvenanceKind.PUBLIC_RECORD,),
            0.75,
        ),
        _rule(
            "testimony-schedule-conflict",
            ("conflicting_testimony",),
            ("C7_schedule_conflict_existed",),
            EvidenceRelation.SUPPORTS,
            (ProvenanceKind.TESTIMONY,),
            0.30,
        ),
        _rule(
            "testimony-against-avoidance",
            ("conflicting_testimony",),
            ("C3_counterpart_intentionally_avoids",),
            EvidenceRelation.CONTRADICTS,
            (ProvenanceKind.TESTIMONY,),
            0.30,
        ),
    )
}


def links_from_event(
    event: ScenarioEvent,
    artifact: ObservationArtifact,
) -> tuple[tuple[EvidenceLink, ...], tuple[str, ...]]:
    """Apply typed grounding rules to an observable artifact.

    Internal events never enter the evidence lane.  Invalid external casts are
    quarantined and reported as HARD authority errors.
    """

    signals = tuple(
        chain(
            ((EvidenceRelation.SUPPORTS, signal) for signal in event.supports),
            ((EvidenceRelation.CONTRADICTS, signal) for signal in event.contradicts),
        )
    )
    if not signals or not event.external:
        return (), ()

    links: list[EvidenceLink] = []
    errors: list[str] = []
    seen_link_ids: set[str] = set()
    for relation, signal in signals:
        rule = GROUNDING_RULES.get(signal.rule_id)
        if rule is None:
            errors.append(f"AUTHORITY_UNKNOWN_GROUNDING_RULE:{signal.rule_id}")
            continue
        violations = []
        if event.kind not in rule.event_kinds:
            violations.append("event_kind")
        if signal.claim_id not in rule.claim_ids:
            violations.append("claim")
        if relation is not rule.relation:
            violations.append("relation")
        if event.provenance_kind not in rule.provenance_kinds:
            violations.append("provenance")
        if signal.strength > rule.maximum_strength + 1e-12:
            violations.append("strength")
        if violations:
            errors.append(
                f"AUTHORITY_INVALID_GROUNDING:{signal.rule_id}:{','.join(violations)}"
            )
            continue

        link_id = (
            f"link:{event.event_id}:{signal.claim_id}:{signal.scope}:{relation.value}"
        )
        if link_id in seen_link_ids:
            errors.append(f"AUTHORITY_DUPLICATE_EVIDENCE_LINK:{link_id}")
            continue
        seen_link_ids.add(link_id)
        links.append(
            EvidenceLink(
                link_id=link_id,
                artifact_id=artifact.artifact_id,
                claim_id=signal.claim_id,
                relation=relation,
                strength=signal.strength,
                scope=signal.scope,
                independence_key=event.independence_key,
                provenance_kind=event.provenance_kind,
                grounding_rule_id=signal.rule_id,
            )
        )
    return tuple(links), tuple(errors)


def _upsert_contribution(
    contributions: tuple[SourceContribution, ...],
    incoming: SourceContribution,
) -> tuple[SourceContribution, ...]:
    """Repeated artifacts in one independence group do not launder evidence."""

    result = []
    inserted = False
    for current in contributions:
        if current.independence_key != incoming.independence_key:
            result.append(current)
            continue
        result.append(incoming if incoming.strength > current.strength else current)
        inserted = True
    if not inserted:
        result.append(incoming)
    result.sort(key=lambda item: item.independence_key)
    return tuple(result)


def apply_evidence_links(
    state: EpistemicState,
    links: tuple[EvidenceLink, ...],
    *,
    stance_anchor: EpistemicState | None = None,
    adoption_threshold: float,
    release_threshold: float,
    minimum_ground_mass: float,
) -> EpistemicState:
    """Apply one event's entire evidence bundle before changing stance."""

    grouped: dict[tuple[str, str], list[EvidenceLink]] = {}
    for link in links:
        grouped.setdefault((link.claim_id, link.scope), []).append(link)

    updated_state = state
    anchor_state = stance_anchor or state
    for (claim_id, scope), claim_links in sorted(grouped.items()):
        original = updated_state.get(claim_id, scope)
        supports = original.supports
        contradicts = original.contradicts
        for link in claim_links:
            contribution = SourceContribution(
                independence_key=link.independence_key,
                link_id=link.link_id,
                strength=link.strength,
            )
            if link.relation is EvidenceRelation.SUPPORTS:
                supports = _upsert_contribution(supports, contribution)
            else:
                contradicts = _upsert_contribution(contradicts, contribution)

        provisional = replace(original, supports=supports, contradicts=contradicts)
        grounds = tuple(item.link_id for item in provisional.supports)
        if (
            provisional.confidence >= adoption_threshold
            and provisional.support_mass >= minimum_ground_mass
            and grounds
        ):
            stance = JudgmentStance.ADOPTED
        elif (
            anchor_state.get(claim_id, scope).stance is JudgmentStance.ADOPTED
            and provisional.confidence >= release_threshold
        ):
            stance = JudgmentStance.ADOPTED
        else:
            stance = JudgmentStance.HELD
        updated_state = updated_state.replace_claim(
            replace(provisional, stance=stance, grounds=grounds)
        )
    return updated_state
