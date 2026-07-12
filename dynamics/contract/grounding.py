"""Typed claim-grounding allowlist and protocol-neutral submissions."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .records import (
    EvidenceLink,
    EvidenceRelation,
    ObservationArtifact,
    ProvenanceKind,
)


@dataclass(frozen=True, slots=True)
class GroundingRule:
    rule_id: str
    event_kinds: frozenset[str]
    claim_ids: frozenset[str]
    relation: EvidenceRelation
    provenance_kinds: frozenset[ProvenanceKind]
    maximum_strength: float


@dataclass(frozen=True, slots=True)
class GroundingSignal:
    claim_id: str
    strength: float
    rule_id: str
    relation: EvidenceRelation
    scope: str = "scenario"

    def __post_init__(self) -> None:
        if not self.claim_id or not self.rule_id or not self.scope:
            raise ValueError("claim_id, rule_id, and scope must be non-empty")
        if not isinstance(self.relation, EvidenceRelation):
            raise TypeError("relation must be EvidenceRelation")
        if not math.isfinite(self.strength) or not 0.0 <= self.strength <= 1.0:
            raise ValueError("grounding strength must be finite and in [0, 1]")


@dataclass(frozen=True, slots=True)
class GroundingSubmission:
    event_id: str
    kind: str
    external: bool
    provenance_kind: ProvenanceKind
    independence_key: str
    signals: tuple[GroundingSignal, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_id or not self.kind or not self.independence_key:
            raise ValueError("event_id, kind, and independence_key must be non-empty")
        if not isinstance(self.external, bool):
            raise TypeError("external must be bool")
        if not isinstance(self.provenance_kind, ProvenanceKind):
            raise TypeError("provenance_kind must be ProvenanceKind")


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


def links_from_submission(
    submission: GroundingSubmission,
    artifact: ObservationArtifact,
) -> tuple[tuple[EvidenceLink, ...], tuple[str, ...]]:
    """Certify only signals accepted by the explicit grounding catalog."""

    if not submission.signals or not submission.external:
        return (), ()

    mismatches = []
    if submission.event_id != artifact.event_id:
        mismatches.append("event_id")
    if submission.kind != artifact.kind:
        mismatches.append("kind")
    if submission.external != artifact.external:
        mismatches.append("external")
    if submission.provenance_kind is not artifact.provenance_kind:
        mismatches.append("provenance")
    if mismatches:
        return (), (
            "PROVENANCE_SUBMISSION_ARTIFACT_MISMATCH:"
            + ",".join(mismatches),
        )

    links: list[EvidenceLink] = []
    errors: list[str] = []
    seen_link_ids: set[str] = set()
    for signal in submission.signals:
        rule = GROUNDING_RULES.get(signal.rule_id)
        if rule is None:
            errors.append(f"AUTHORITY_UNKNOWN_GROUNDING_RULE:{signal.rule_id}")
            continue
        violations = []
        if submission.kind not in rule.event_kinds:
            violations.append("event_kind")
        if signal.claim_id not in rule.claim_ids:
            violations.append("claim")
        if signal.relation is not rule.relation:
            violations.append("relation")
        if submission.provenance_kind not in rule.provenance_kinds:
            violations.append("provenance")
        if (
            not math.isfinite(signal.strength)
            or not 0.0 <= signal.strength <= 1.0
            or signal.strength > rule.maximum_strength + 1e-12
        ):
            violations.append("strength")
        if violations:
            errors.append(
                f"AUTHORITY_INVALID_GROUNDING:{signal.rule_id}:{','.join(violations)}"
            )
            continue

        link_id = (
            f"link:{submission.event_id}:{signal.claim_id}:"
            f"{signal.scope}:{signal.relation.value}"
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
                relation=signal.relation,
                strength=signal.strength,
                scope=signal.scope,
                independence_key=submission.independence_key,
                provenance_kind=submission.provenance_kind,
                grounding_rule_id=signal.rule_id,
            )
        )
    return tuple(links), tuple(errors)
