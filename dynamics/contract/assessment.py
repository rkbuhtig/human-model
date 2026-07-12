"""Certification policy and evidence-scoped claim reduction.

This module decides what an evidence assessment may record.  It does not
describe what a person believes and it does not assert that a claim is true.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math

from .records import (
    EvidenceAssessmentState,
    EvidenceLink,
    EvidenceRelation,
    JudgmentStance,
    SourceContribution,
)


@dataclass(frozen=True, slots=True)
class EvidenceAssessmentPolicy:
    adoption_threshold: float = 0.75
    release_threshold: float = 0.55
    minimum_ground_mass: float = 0.50

    def __post_init__(self) -> None:
        if not 0.0 < self.release_threshold < self.adoption_threshold < 1.0:
            raise ValueError("invalid evidence-assessment hysteresis thresholds")
        if (
            not math.isfinite(self.minimum_ground_mass)
            or self.minimum_ground_mass < 0.0
        ):
            raise ValueError("minimum_ground_mass must be finite and non-negative")


def _upsert_contribution(
    contributions: tuple[SourceContribution, ...],
    incoming: SourceContribution,
) -> tuple[SourceContribution, ...]:
    """Do not turn repetition within one independence group into new support."""

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
    state: EvidenceAssessmentState,
    links: tuple[EvidenceLink, ...],
    *,
    stance_anchor: EvidenceAssessmentState | None = None,
    policy: EvidenceAssessmentPolicy | None = None,
    adoption_threshold: float | None = None,
    release_threshold: float | None = None,
    minimum_ground_mass: float | None = None,
) -> EvidenceAssessmentState:
    """Apply one artifact's entire link bundle before changing its stance.

    The optional scalar arguments preserve the v0.1 call surface.  New code
    should pass an ``EvidenceAssessmentPolicy``.
    """

    if policy is None:
        policy = EvidenceAssessmentPolicy(
            adoption_threshold=(0.75 if adoption_threshold is None else adoption_threshold),
            release_threshold=(0.55 if release_threshold is None else release_threshold),
            minimum_ground_mass=(
                0.50 if minimum_ground_mass is None else minimum_ground_mass
            ),
        )
    elif any(
        value is not None
        for value in (adoption_threshold, release_threshold, minimum_ground_mass)
    ):
        raise ValueError("pass policy or scalar compatibility arguments, not both")

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
            provisional.confidence >= policy.adoption_threshold
            and provisional.support_mass >= policy.minimum_ground_mass
            and grounds
        ):
            stance = JudgmentStance.ADOPTED
        elif (
            anchor_state.get(claim_id, scope).stance is JudgmentStance.ADOPTED
            and provisional.confidence >= policy.release_threshold
        ):
            stance = JudgmentStance.ADOPTED
        else:
            stance = JudgmentStance.HELD
        updated_state = updated_state.replace_claim(
            replace(provisional, stance=stance, grounds=grounds)
        )
    return updated_state
