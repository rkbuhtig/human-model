"""Typed records whose existence can certify only their declared scope."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


ACTION_OPPORTUNITY_RULE_V01 = "internal-decision-window-v01"


def action_opportunity_id(event_id: str) -> str:
    return f"action-opportunity:{event_id}"


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
        denominator = self.support_mass + self.contradiction_mass + 0.20
        return 0.0 if denominator == 0.0 else self.support_mass / denominator


@dataclass(frozen=True, slots=True)
class EvidenceAssessmentState:
    """Evidence-scoped claim assessment, not belief, world truth, or warrant."""

    claims: tuple[ClaimState, ...] = ()

    def get(self, claim_id: str, scope: str = "scenario") -> ClaimState:
        for claim in self.claims:
            if claim.claim_id == claim_id and claim.scope == scope:
                return claim
        return ClaimState(claim_id=claim_id, scope=scope)

    def replace_claim(self, updated: ClaimState) -> "EvidenceAssessmentState":
        claims = [
            claim
            for claim in self.claims
            if (claim.claim_id, claim.scope) != (updated.claim_id, updated.scope)
        ]
        claims.append(updated)
        claims.sort(key=lambda item: (item.claim_id, item.scope))
        return EvidenceAssessmentState(tuple(claims))


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
class IntentDecision:
    intent_id: str
    action_kind: str
    selected_candidate_id: str
    coercion: float
    action_opportunity_id: str | None = None


@dataclass(frozen=True, slots=True)
class ActionOpportunity:
    """A typed decision surface opened by a declared protocol rule."""

    opportunity_id: str
    event_id: str
    rule_id: str

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.event_id or not self.rule_id:
            raise ValueError("action opportunity fields must be non-empty")


@dataclass(frozen=True, slots=True, init=False)
class MotorFeasibility:
    """A model-produced execution feasibility record, not authorization."""

    feasibility_id: str
    feasible: bool
    available_capacity: float
    required_capacity: float

    def __init__(
        self,
        feasibility_id: str | None = None,
        feasible: bool | None = None,
        available_capacity: float | None = None,
        required_capacity: float | None = None,
        *,
        authorization_id: str | None = None,
        allowed: bool | None = None,
    ) -> None:
        """Accept canonical and v0.1 keyword names for one compatibility line."""

        if feasibility_id is not None and authorization_id not in (None, feasibility_id):
            raise TypeError("conflicting feasibility_id and authorization_id")
        if feasible is not None and allowed not in (None, feasible):
            raise TypeError("conflicting feasible and allowed")
        resolved_id = feasibility_id if feasibility_id is not None else authorization_id
        resolved_feasible = feasible if feasible is not None else allowed
        if resolved_id is None or resolved_feasible is None:
            raise TypeError("feasibility identity and boolean result are required")
        if available_capacity is None or required_capacity is None:
            raise TypeError("available_capacity and required_capacity are required")
        object.__setattr__(self, "feasibility_id", resolved_id)
        object.__setattr__(self, "feasible", resolved_feasible)
        object.__setattr__(self, "available_capacity", available_capacity)
        object.__setattr__(self, "required_capacity", required_capacity)

    @property
    def authorization_id(self) -> str:
        """v0.1 read compatibility; removed after the compatibility window."""

        return self.feasibility_id

    @property
    def allowed(self) -> bool:
        """v0.1 read compatibility; feasibility is not normative permission."""

        return self.feasible


@dataclass(frozen=True, slots=True, init=False)
class ActionAttempt:
    attempt_id: str
    intent_id: str
    action_kind: str
    motor_feasibility: MotorFeasibility
    tick: int

    def __init__(
        self,
        attempt_id: str,
        intent_id: str,
        action_kind: str,
        motor_feasibility: MotorFeasibility | None = None,
        tick: int | None = None,
        *,
        authorization: MotorFeasibility | None = None,
    ) -> None:
        if motor_feasibility is not None and authorization not in (
            None,
            motor_feasibility,
        ):
            raise TypeError("conflicting motor_feasibility and authorization")
        resolved = (
            motor_feasibility if motor_feasibility is not None else authorization
        )
        if resolved is None or tick is None:
            raise TypeError("motor feasibility and tick are required")
        object.__setattr__(self, "attempt_id", attempt_id)
        object.__setattr__(self, "intent_id", intent_id)
        object.__setattr__(self, "action_kind", action_kind)
        object.__setattr__(self, "motor_feasibility", resolved)
        object.__setattr__(self, "tick", tick)

    @property
    def authorization(self) -> MotorFeasibility:
        """v0.1 read compatibility alias."""

        return self.motor_feasibility


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
