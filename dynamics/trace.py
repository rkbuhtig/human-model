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
