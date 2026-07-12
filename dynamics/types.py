"""Typed residences used by Human Model Dynamics v0.1.

Persistent human state, momentary runtime values, evidence, action receipts,
and world-facing records are deliberately separate types.  Numeric values are
dimensionless simulation units in [0, 1], not psychological measurements.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
import math
from typing import Iterable


def clamp01(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError(f"non-finite simulation value: {value!r}")
    return min(1.0, max(0.0, float(value)))


class ProvenanceKind(str, Enum):
    DIRECT_OBSERVATION = "direct_observation"
    TESTIMONY = "testimony"
    PUBLIC_RECORD = "public_record"
    RECOLLECTION_REPORT = "recollection_report"
    INFERENCE = "inference"
    IMAGINATION = "imagination"
    PERFORMED_ACTION = "performed_action"


class EvidenceRelation(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"


class JudgmentStance(str, Enum):
    HELD = "held"
    ADOPTED = "adopted"


@dataclass(frozen=True, slots=True)
class BodyState:
    energy: float = 0.75
    arousal: float = 0.35
    action_capacity: float = 0.75

    def bounded(self) -> "BodyState":
        return BodyState(*(clamp01(v) for v in (self.energy, self.arousal, self.action_capacity)))


@dataclass(frozen=True, slots=True)
class AccessState:
    attention_budget: float = 0.75
    interference: float = 0.15
    queue_load: float = 0.0

    def bounded(self) -> "AccessState":
        return AccessState(*(clamp01(v) for v in (self.attention_budget, self.interference, self.queue_load)))


@dataclass(frozen=True, slots=True)
class AssociativeState:
    rejection_access: float = 0.30
    ambiguity_sensitivity: float = 0.35

    def bounded(self) -> "AssociativeState":
        return AssociativeState(clamp01(self.rejection_access), clamp01(self.ambiguity_sensitivity))


@dataclass(frozen=True, slots=True)
class AffectivePrior:
    residual_distress: float = 0.15
    update_rate: float = 0.12

    def bounded(self) -> "AffectivePrior":
        return AffectivePrior(clamp01(self.residual_distress), clamp01(self.update_rate))


@dataclass(frozen=True, slots=True)
class HabitPolicy:
    impulsivity: float = 0.25
    withdrawal_bias: float = 0.25

    def bounded(self) -> "HabitPolicy":
        return HabitPolicy(clamp01(self.impulsivity), clamp01(self.withdrawal_bias))


@dataclass(frozen=True, slots=True)
class NarrativeState:
    rejection_story: float = 0.20
    relational_security: float = 0.65

    def bounded(self) -> "NarrativeState":
        return NarrativeState(clamp01(self.rejection_story), clamp01(self.relational_security))


@dataclass(frozen=True, slots=True)
class RelationalProfile:
    stake: float = 0.75
    trust: float = 0.70
    boundary_strain: float = 0.15

    def bounded(self) -> "RelationalProfile":
        return RelationalProfile(*(clamp01(v) for v in (self.stake, self.trust, self.boundary_strain)))


@dataclass(frozen=True, slots=True)
class ClaimSignal:
    claim_id: str
    strength: float
    rule_id: str
    scope: str = "scenario"

    def __post_init__(self) -> None:
        if not self.claim_id or not self.rule_id or not self.scope:
            raise ValueError("claim_id, rule_id, and scope must be non-empty")
        object.__setattr__(self, "strength", clamp01(self.strength))


@dataclass(frozen=True, slots=True)
class SourceContribution:
    independence_key: str
    link_id: str
    strength: float


@dataclass(frozen=True, slots=True)
class ClaimState:
    claim_id: str
    scope: str = "scenario"
    supports: tuple[SourceContribution, ...] = ()
    contradicts: tuple[SourceContribution, ...] = ()
    stance: JudgmentStance = JudgmentStance.HELD
    grounds: tuple[str, ...] = ()

    @property
    def support_mass(self) -> float:
        return sum(item.strength for item in self.supports)

    @property
    def contradiction_mass(self) -> float:
        return sum(item.strength for item in self.contradicts)

    @property
    def confidence(self) -> float:
        # A small prior mass prevents one weak artifact from becoming certainty.
        denominator = self.support_mass + self.contradiction_mass + 0.20
        return 0.0 if denominator == 0.0 else self.support_mass / denominator


@dataclass(frozen=True, slots=True)
class EpistemicState:
    """Claim-specific internal adoption state, not world truth or authority."""

    claims: tuple[ClaimState, ...] = ()

    def get(self, claim_id: str, scope: str = "scenario") -> ClaimState:
        for claim in self.claims:
            if claim.claim_id == claim_id and claim.scope == scope:
                return claim
        return ClaimState(claim_id=claim_id, scope=scope)

    def replace_claim(self, updated: ClaimState) -> "EpistemicState":
        claims = [
            claim
            for claim in self.claims
            if (claim.claim_id, claim.scope) != (updated.claim_id, updated.scope)
        ]
        claims.append(updated)
        claims.sort(key=lambda item: (item.claim_id, item.scope))
        return EpistemicState(tuple(claims))


@dataclass(frozen=True, slots=True)
class HumanState:
    clock: int = 0
    body: BodyState = field(default_factory=BodyState)
    access: AccessState = field(default_factory=AccessState)
    associative: AssociativeState = field(default_factory=AssociativeState)
    affective: AffectivePrior = field(default_factory=AffectivePrior)
    habit: HabitPolicy = field(default_factory=HabitPolicy)
    narrative: NarrativeState = field(default_factory=NarrativeState)
    relationship: RelationalProfile = field(default_factory=RelationalProfile)
    epistemic: EpistemicState = field(default_factory=EpistemicState)

    def with_clock(self, clock: int) -> "HumanState":
        return replace(self, clock=clock)


@dataclass(frozen=True, slots=True)
class ScenarioEvent:
    event_id: str
    tick: int
    kind: str
    external: bool
    source_id: str
    provenance_kind: ProvenanceKind
    independence_key: str
    ambiguity: float = 0.0
    salience: float = 0.5
    time_pressure: float = 0.0
    memory_interference: float = 0.0
    candidate_fanout: float = 0.0
    ingress_priority: float = 0.5
    energy_delta: float = 0.0
    arousal_delta: float = 0.0
    capacity_delta: float = 0.0
    attention_delta: float = 0.0
    soothing: float = 0.0
    trust_delta: float = 0.0
    boundary_delta: float = 0.0
    action_window: bool = False
    coercion: float = 0.0
    supports: tuple[ClaimSignal, ...] = ()
    contradicts: tuple[ClaimSignal, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_id or not self.kind or not self.source_id:
            raise ValueError("event_id, kind, and source_id must be non-empty")
        if self.tick < 0:
            raise ValueError("event tick must be non-negative")
        for name in (
            "ambiguity",
            "salience",
            "time_pressure",
            "memory_interference",
            "candidate_fanout",
            "ingress_priority",
            "soothing",
            "coercion",
        ):
            object.__setattr__(self, name, clamp01(getattr(self, name)))


@dataclass(frozen=True, slots=True)
class ObservationArtifact:
    artifact_id: str
    event_id: str
    source_tick: int
    observed_tick: int
    kind: str
    source_id: str
    provenance_kind: ProvenanceKind
    external: bool


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    link_id: str
    artifact_id: str
    claim_id: str
    relation: EvidenceRelation
    strength: float
    scope: str
    independence_key: str
    provenance_kind: ProvenanceKind
    grounding_rule_id: str


@dataclass(frozen=True, slots=True)
class PhenomenalActivation:
    """Simulation-only readout; not an assertion about phenomenal ontology."""

    distress: float
    urgency: float
    ambiguity: float


@dataclass(frozen=True, slots=True)
class Candidate:
    candidate_id: str
    action_kind: str


@dataclass(frozen=True, slots=True)
class InfluenceTerm:
    channel: str
    delta: float


@dataclass(frozen=True, slots=True)
class RoutedCandidate:
    candidate: Candidate
    salience: float
    probability: float
    terms: tuple[InfluenceTerm, ...]


@dataclass(frozen=True, slots=True)
class IntentDecision:
    intent_id: str
    action_kind: str
    selected_candidate_id: str
    coercion: float


@dataclass(frozen=True, slots=True)
class BodyAuthorization:
    authorization_id: str
    allowed: bool
    available_capacity: float
    required_capacity: float


@dataclass(frozen=True, slots=True)
class ActionAttempt:
    attempt_id: str
    intent_id: str
    action_kind: str
    authorization: BodyAuthorization
    tick: int


@dataclass(frozen=True, slots=True)
class PerformanceReceipt:
    receipt_id: str
    attempt_id: str
    action_kind: str
    agency: float
    tick: int


@dataclass(frozen=True, slots=True)
class ActionOccurrence:
    occurrence_id: str
    caused_by_receipt_id: str
    action_kind: str
    tick: int


@dataclass(frozen=True, slots=True)
class StateDelta:
    field: str
    before: float
    after: float
    cause_event_id: str


@dataclass(frozen=True, slots=True)
class EpisodeTrace:
    trace_id: str
    event_id: str
    lane: str
    source_id: str
    provenance_kind: ProvenanceKind
    tick: int


@dataclass(frozen=True, slots=True)
class TickTrace:
    processed_tick: int
    observation: ObservationArtifact
    phenomenal: PhenomenalActivation
    routed: tuple[RoutedCandidate, ...]
    judgments: tuple[ClaimState, ...]
    intent: IntentDecision | None
    attempt: ActionAttempt | None
    performance: PerformanceReceipt | None
    action_occurrence: ActionOccurrence | None
    deltas: tuple[StateDelta, ...]
    state_before: HumanState
    state_after: HumanState


def iter_unit_values(state: HumanState) -> Iterable[tuple[str, float]]:
    groups = {
        "body": state.body,
        "access": state.access,
        "associative": state.associative,
        "affective": state.affective,
        "habit": state.habit,
        "narrative": state.narrative,
        "relationship": state.relationship,
    }
    for prefix, group in groups.items():
        for name in group.__dataclass_fields__:
            value = getattr(group, name)
            if isinstance(value, (int, float)):
                yield f"{prefix}.{name}", float(value)
