"""Descriptive human state and non-certifying runtime readouts."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Iterable

from ..contract.records import EvidenceAssessmentState
from ..interfaces import clamp01


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


@dataclass(frozen=True, slots=True, init=False)
class HumanState:
    clock: int = 0
    body: BodyState = field(default_factory=BodyState)
    access: AccessState = field(default_factory=AccessState)
    associative: AssociativeState = field(default_factory=AssociativeState)
    affective: AffectivePrior = field(default_factory=AffectivePrior)
    habit: HabitPolicy = field(default_factory=HabitPolicy)
    narrative: NarrativeState = field(default_factory=NarrativeState)
    relationship: RelationalProfile = field(default_factory=RelationalProfile)
    evidence_assessment: EvidenceAssessmentState = field(
        default_factory=EvidenceAssessmentState
    )

    def __init__(
        self,
        clock: int = 0,
        body: BodyState | None = None,
        access: AccessState | None = None,
        associative: AssociativeState | None = None,
        affective: AffectivePrior | None = None,
        habit: HabitPolicy | None = None,
        narrative: NarrativeState | None = None,
        relationship: RelationalProfile | None = None,
        evidence_assessment: EvidenceAssessmentState | None = None,
        *,
        epistemic: EvidenceAssessmentState | None = None,
    ) -> None:
        """Store the canonical field while accepting the v0.1 constructor name."""

        if evidence_assessment is not None and epistemic not in (
            None,
            evidence_assessment,
        ):
            raise TypeError("conflicting evidence_assessment and epistemic")
        assessment = (
            evidence_assessment
            if evidence_assessment is not None
            else epistemic
        )
        object.__setattr__(self, "clock", clock)
        object.__setattr__(self, "body", BodyState() if body is None else body)
        object.__setattr__(self, "access", AccessState() if access is None else access)
        object.__setattr__(
            self,
            "associative",
            AssociativeState() if associative is None else associative,
        )
        object.__setattr__(
            self,
            "affective",
            AffectivePrior() if affective is None else affective,
        )
        object.__setattr__(self, "habit", HabitPolicy() if habit is None else habit)
        object.__setattr__(
            self,
            "narrative",
            NarrativeState() if narrative is None else narrative,
        )
        object.__setattr__(
            self,
            "relationship",
            RelationalProfile() if relationship is None else relationship,
        )
        object.__setattr__(
            self,
            "evidence_assessment",
            EvidenceAssessmentState() if assessment is None else assessment,
        )

    @property
    def epistemic(self) -> EvidenceAssessmentState:
        """v0.1 read compatibility alias."""

        return self.evidence_assessment

    def with_clock(self, clock: int) -> "HumanState":
        return replace(self, clock=clock)


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
