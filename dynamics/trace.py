"""Cross-layer audit projections assembled by the engine."""

from __future__ import annotations

from dataclasses import dataclass

from .contract.records import (
    ActionOpportunity,
    ActionAttempt,
    ActionOccurrence,
    ClaimState,
    IntentDecision,
    ObservationArtifact,
    PerformanceReceipt,
    ProvenanceKind,
)
from .models.state import HumanState, PhenomenalActivation, RoutedCandidate
from .models.proposals import ReducerFieldProposal, ReducerProposalContext


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
    occurrence_id: str | None = None
    delivery_id: str | None = None
    processed_at: int | None = None
    processing_sequence: int | None = None


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
    action_opportunity: ActionOpportunity | None = None
    processing_sequence: int | None = None
    reducer_proposals: tuple[ReducerFieldProposal, ...] = ()
    reducer_proposal_context: ReducerProposalContext | None = None

    def __post_init__(self) -> None:
        if type(self.reducer_proposals) is not tuple:
            raise TypeError("reducer_proposals must be an immutable tuple")
        if any(
            type(proposal) is not ReducerFieldProposal
            for proposal in self.reducer_proposals
        ):
            raise TypeError(
                "reducer_proposals must contain ReducerFieldProposal values"
            )
        if (
            self.reducer_proposal_context is not None
            and type(self.reducer_proposal_context) is not ReducerProposalContext
        ):
            raise TypeError(
                "reducer_proposal_context must be ReducerProposalContext or None"
            )
