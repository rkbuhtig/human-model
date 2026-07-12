"""v0.1 compatibility façade for certification assessment and grounding."""

from __future__ import annotations

from .contract.assessment import EvidenceAssessmentPolicy, apply_evidence_links
from .contract.grounding import (
    GROUNDING_RULES,
    GroundingRule,
    links_from_submission,
)
from .contract.records import ObservationArtifact
from .protocol.events import ScenarioEvent, encode_grounding_submission


def links_from_event(
    event: ScenarioEvent,
    artifact: ObservationArtifact,
):
    """Legacy adapter; canonical contract code never imports ScenarioEvent."""

    return links_from_submission(encode_grounding_submission(event), artifact)


__all__ = [
    "EvidenceAssessmentPolicy",
    "GROUNDING_RULES",
    "GroundingRule",
    "apply_evidence_links",
    "links_from_event",
    "links_from_submission",
]
