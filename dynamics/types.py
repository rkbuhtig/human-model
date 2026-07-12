"""v0.1 compatibility façade for the v0.1.1 typed package boundaries.

New code should import from ``dynamics.contract``, ``dynamics.models``,
``dynamics.protocol``, or ``dynamics.trace``.  The legacy names remain for one
compatibility window and do not imply their former semantics.
"""

from .contract.records import (
    ActionOpportunity,
    ActionAttempt,
    ActionOccurrence,
    ClaimState,
    EvidenceAssessmentState,
    EvidenceLink,
    EvidenceRelation,
    IntentDecision,
    JudgmentStance,
    MotorFeasibility,
    ObservationArtifact,
    PerformanceReceipt,
    ProvenanceKind,
    SourceContribution,
)
from .interfaces import ModelInput, clamp01
from .models.state import (
    AccessState,
    AffectivePrior,
    AssociativeState,
    BodyState,
    Candidate,
    HabitPolicy,
    HumanState,
    InfluenceTerm,
    NarrativeState,
    PhenomenalActivation,
    RelationalProfile,
    RoutedCandidate,
    iter_unit_values,
)
from .protocol.events import ClaimSignal, ScenarioEvent
from .trace import EpisodeTrace, StateDelta, TickTrace

# v0.1 import compatibility.  Canonical packages do not export these names.
EpistemicState = EvidenceAssessmentState
BodyAuthorization = MotorFeasibility

__all__ = [name for name in globals() if not name.startswith("_")]
