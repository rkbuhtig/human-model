"""v0.1 validator façade combining certification and descriptive checks."""

from __future__ import annotations

from typing import Mapping, Sequence

from .contract.assessment import EvidenceAssessmentPolicy
from .contract.records import (
    ActionAttempt,
    ActionOccurrence,
    EvidenceAssessmentState,
    EvidenceLink,
    IntentDecision,
    ObservationArtifact,
    PerformanceReceipt,
)
from .contract.validation import (
    validate_action_lineage,
    validate_evidence_assessment,
)
from .models.state import HumanState, RoutedCandidate
from .models.validation import (
    validate_agency_hypothesis,
    validate_intent_selection,
    validate_routing_distribution,
    validate_state_bounds,
)


def validate_distribution(routed: Sequence[RoutedCandidate]) -> list[str]:
    return validate_routing_distribution(routed)


def validate_epistemics(
    state: EvidenceAssessmentState,
    links_by_id: Mapping[str, EvidenceLink],
    artifacts_by_id: Mapping[str, ObservationArtifact],
    new_links: Sequence[EvidenceLink] = (),
    *,
    adoption_threshold: float,
    release_threshold: float,
    minimum_ground_mass: float,
) -> list[str]:
    policy = EvidenceAssessmentPolicy(
        adoption_threshold=adoption_threshold,
        release_threshold=release_threshold,
        minimum_ground_mass=minimum_ground_mass,
    )
    return validate_evidence_assessment(
        state,
        links_by_id,
        artifacts_by_id,
        new_links,
        policy=policy,
        full_audit=not new_links,
    )


def validate_action_chain(
    intent: IntentDecision | None,
    attempt: ActionAttempt | None,
    receipt: PerformanceReceipt | None,
    occurrence: ActionOccurrence | None,
    routed: Sequence[RoutedCandidate] = (),
) -> list[str]:
    return [
        *validate_action_lineage(intent, attempt, receipt, occurrence),
        *validate_intent_selection(intent, routed),
        *validate_agency_hypothesis(intent, receipt),
    ]


__all__ = [
    "validate_action_chain",
    "validate_distribution",
    "validate_epistemics",
    "validate_state_bounds",
]
