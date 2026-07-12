"""Deterministic typed hybrid engine for Human Model Dynamics v0.1.1."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
import math
from typing import Iterable

from .adapters import legacy_v01_access_pressure_bridge
from .contract import (
    ActionAttempt,
    ActionOccurrence,
    ActionOpportunity,
    EvidenceAssessmentPolicy,
    EvidenceAssessmentState,
    EvidenceLink,
    ObservationArtifact,
    PerformanceReceipt,
    ProvenanceKind,
    apply_evidence_links,
    links_from_submission,
    validate_action_lineage,
    validate_action_opportunity,
    validate_evidence_assessment,
)
from .models import (
    HumanState,
    apply_fast_update,
    apply_slow_update,
    iter_unit_values,
    phenomenal_activation,
    processing_capacity,
    route_candidates,
    run_action_pipeline,
    validate_agency_hypothesis,
    validate_intent_selection,
    validate_routing_distribution,
    validate_state_bounds,
)
from .protocol import (
    IngressQueue,
    ScenarioEvent,
    action_opportunity_from_event,
    encode_grounding_submission,
    encode_model_input,
)
from .trace import EpisodeTrace, StateDelta, TickTrace


@dataclass(frozen=True, slots=True)
class EngineConfig:
    base_capacity_per_tick: int = 6
    queue_limit: int = 64
    drain_ticks: int = 20
    routing_temperature: float = 0.62
    adoption_threshold: float = 0.75
    release_threshold: float = 0.55
    minimum_ground_mass: float = 0.50
    ingress_policy: str = "priority"

    def __post_init__(self) -> None:
        if self.base_capacity_per_tick < 1 or self.queue_limit < 1 or self.drain_ticks < 0:
            raise ValueError("capacity and queue values must be positive")
        if not 0.0 < self.release_threshold < self.adoption_threshold < 1.0:
            raise ValueError("invalid adoption hysteresis thresholds")
        if (
            not math.isfinite(self.minimum_ground_mass)
            or self.minimum_ground_mass < 0.0
        ):
            raise ValueError("minimum_ground_mass must be finite and non-negative")
        if self.ingress_policy not in {"fifo", "priority"}:
            raise ValueError("ingress_policy must be 'fifo' or 'priority'")


@dataclass(slots=True)
class SimulationLedger:
    observations: list[ObservationArtifact] = field(default_factory=list)
    observations_by_id: dict[str, ObservationArtifact] = field(default_factory=dict)
    evidence_links: list[EvidenceLink] = field(default_factory=list)
    evidence_links_by_id: dict[str, EvidenceLink] = field(default_factory=dict)
    episode_traces: list[EpisodeTrace] = field(default_factory=list)
    attempts: list[ActionAttempt] = field(default_factory=list)
    action_opportunities: list[ActionOpportunity] = field(default_factory=list)
    performance_receipts: list[PerformanceReceipt] = field(default_factory=list)
    action_occurrences: list[ActionOccurrence] = field(default_factory=list)
    tick_traces: list[TickTrace] = field(default_factory=list)
    invariant_errors: list[str] = field(default_factory=list)
    dropped_event_ids: list[str] = field(default_factory=list)
    unresolved_event_ids: list[str] = field(default_factory=list)
    duplicate_event_ids: list[str] = field(default_factory=list)
    collision_event_ids: list[str] = field(default_factory=list)
    deferred_event_ids: set[str] = field(default_factory=set)
    provenance_loss_count: int = 0
    raw_received: int = 0
    unique_received: int = 0
    processed: int = 0


@dataclass(frozen=True, slots=True)
class SimulationResult:
    initial_state: HumanState
    final_state: HumanState
    ledger: SimulationLedger

    @property
    def authority_leak_count(self) -> int:
        return sum("AUTHORITY_" in error for error in self.ledger.invariant_errors)

    @property
    def phantom_action_count(self) -> int:
        return sum("PHANTOM_" in error for error in self.ledger.invariant_errors)

    @property
    def input_accounting_ok(self) -> bool:
        return (
            self.ledger.raw_received
            == self.ledger.unique_received
            + len(self.ledger.duplicate_event_ids)
            + len(self.ledger.collision_event_ids)
            and self.ledger.unique_received
            == self.ledger.processed
            + len(self.ledger.dropped_event_ids)
            + len(self.ledger.unresolved_event_ids)
        )

    def summary(self) -> dict[str, object]:
        claims = {
            (claim.claim_id if claim.scope == "scenario" else f"{claim.claim_id}@{claim.scope}"): {
                "confidence": round(claim.confidence, 6),
                "stance": claim.stance.value,
                "support_mass": round(claim.support_mass, 6),
                "contradiction_mass": round(claim.contradiction_mass, 6),
                "grounds": list(claim.grounds),
            }
            for claim in self.final_state.evidence_assessment.claims
        }
        distress_values = [trace.phenomenal.distress for trace in self.ledger.tick_traces]
        queue_values = [
            delta.after
            for trace in self.ledger.tick_traces
            for delta in trace.deltas
            if delta.field == "access.queue_load"
        ]
        return {
            "raw_received": self.ledger.raw_received,
            "unique_received": self.ledger.unique_received,
            "processed": self.ledger.processed,
            "deferred_unique": len(self.ledger.deferred_event_ids),
            "dropped": len(self.ledger.dropped_event_ids),
            "unresolved": len(self.ledger.unresolved_event_ids),
            "duplicates_ignored": len(self.ledger.duplicate_event_ids),
            "event_id_collisions": len(self.ledger.collision_event_ids),
            "input_accounting_ok": self.input_accounting_ok,
            "evidence_links": len(self.ledger.evidence_links),
            "attempts": len(self.ledger.attempts),
            "performed_actions": len(self.ledger.performance_receipts),
            "action_occurrences": len(self.ledger.action_occurrences),
            "authority_leaks": self.authority_leak_count,
            "phantom_actions": self.phantom_action_count,
            "provenance_losses": self.ledger.provenance_loss_count,
            "invariant_errors": list(self.ledger.invariant_errors),
            "peak_distress": round(max(distress_values, default=0.0), 6),
            "final_residual_distress": round(self.final_state.affective.residual_distress, 6),
            "peak_queue_load": round(max(queue_values, default=0.0), 6),
            "claims": claims,
            "final_state": {
                "energy": round(self.final_state.body.energy, 6),
                "attention_budget": round(self.final_state.access.attention_budget, 6),
                "rejection_access": round(self.final_state.associative.rejection_access, 6),
                "rejection_story": round(self.final_state.narrative.rejection_story, 6),
                "relational_security": round(self.final_state.narrative.relational_security, 6),
                "trust": round(self.final_state.relationship.trust, 6),
                "boundary_strain": round(self.final_state.relationship.boundary_strain, 6),
            },
        }


class DynamicsEngine:
    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()

    def run(self, initial_state: HumanState, events: Iterable[ScenarioEvent]) -> SimulationResult:
        """Run only on observable events; hidden scenario truth is never accepted."""

        ordered = list(events)
        ledger = SimulationLedger()
        initial_errors = validate_state_bounds(initial_state)
        initial_errors.extend(
            validate_evidence_assessment(
                initial_state.evidence_assessment,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                (),
                policy=self._assessment_policy,
                full_audit=True,
            )
        )
        ledger.invariant_errors.extend(f"initial:{error}" for error in initial_errors)
        arrivals: dict[int, list[ScenarioEvent]] = defaultdict(list)
        for event in ordered:
            arrivals[event.tick].append(event)
        last_arrival_tick = max((event.tick for event in ordered), default=0)

        state = initial_state
        ingress = IngressQueue(
            queue_limit=self.config.queue_limit,
            policy=self.config.ingress_policy,
        )
        end_tick = last_arrival_tick + self.config.drain_ticks

        for tick in range(0, end_tick + 1):
            for event in arrivals.get(tick, ()):
                ledger.raw_received += 1
                decision = ingress.accept(event)
                if decision.disposition == "duplicate":
                    ledger.duplicate_event_ids.append(event.event_id)
                    continue
                if decision.disposition == "collision":
                    ledger.collision_event_ids.append(event.event_id)
                    ledger.invariant_errors.append(
                        f"{event.event_id}:EVENT_ID_PAYLOAD_COLLISION"
                    )
                    continue
                ledger.unique_received += 1

            capacity = processing_capacity(state, self.config.base_capacity_per_tick)
            batch = ingress.take(capacity)
            processing = batch.processing
            ledger.deferred_event_ids.update(batch.deferred_event_ids)
            ledger.dropped_event_ids.extend(batch.dropped_event_ids)

            assessment_anchor = state.evidence_assessment
            for event in processing:
                access_pressure = legacy_v01_access_pressure_bridge(
                    ingress.pressure()
                )
                state = self._process_event(
                    state,
                    event,
                    tick,
                    access_pressure,
                    ledger,
                    assessment_anchor,
                )
                ledger.processed += 1

        ledger.unresolved_event_ids.extend(ingress.unresolved_event_ids)
        if ledger.raw_received != (
            ledger.unique_received
            + len(ledger.duplicate_event_ids)
            + len(ledger.collision_event_ids)
        ):
            ledger.invariant_errors.append("RAW_INPUT_ACCOUNTING_MISMATCH")
        if ledger.unique_received != ledger.processed + len(ledger.dropped_event_ids) + len(ledger.unresolved_event_ids):
            ledger.invariant_errors.append("INPUT_ACCOUNTING_MISMATCH")

        final_errors = validate_state_bounds(state)
        final_errors.extend(
            validate_evidence_assessment(
                state.evidence_assessment,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                (),
                policy=self._assessment_policy,
                full_audit=True,
            )
        )
        ledger.invariant_errors.extend(f"final:{error}" for error in final_errors)

        return SimulationResult(initial_state=initial_state, final_state=state, ledger=ledger)

    @property
    def _assessment_policy(self) -> EvidenceAssessmentPolicy:
        return EvidenceAssessmentPolicy(
            adoption_threshold=self.config.adoption_threshold,
            release_threshold=self.config.release_threshold,
            minimum_ground_mass=self.config.minimum_ground_mass,
        )

    def _process_event(
        self,
        state: HumanState,
        event: ScenarioEvent,
        processed_tick: int,
        access_pressure: float,
        ledger: SimulationLedger,
        assessment_anchor: EvidenceAssessmentState,
    ) -> HumanState:
        before = state
        model_input = encode_model_input(event)
        artifact = ObservationArtifact(
            artifact_id=f"artifact:{event.event_id}",
            event_id=event.event_id,
            source_tick=event.tick,
            observed_tick=processed_tick,
            kind=event.kind,
            source_id=event.source_id,
            provenance_kind=event.provenance_kind,
            external=event.external,
        )
        ledger.observations.append(artifact)
        ledger.observations_by_id[artifact.artifact_id] = artifact

        links, linking_errors = links_from_submission(
            encode_grounding_submission(event),
            artifact,
        )
        ledger.provenance_loss_count += sum("provenance" in error.lower() for error in linking_errors)
        ledger.evidence_links.extend(links)
        ledger.evidence_links_by_id.update((link.link_id, link) for link in links)
        assessment = apply_evidence_links(
            state.evidence_assessment,
            links,
            stance_anchor=assessment_anchor,
            policy=self._assessment_policy,
        )
        state = apply_fast_update(
            state,
            model_input,
            processed_tick=processed_tick,
            access_pressure=access_pressure,
        )
        state = replace(state, evidence_assessment=assessment)

        phenomenal = phenomenal_activation(state, model_input)
        routed = route_candidates(
            state,
            model_input,
            phenomenal,
            temperature=self.config.routing_temperature,
        )
        opportunity, window_error = action_opportunity_from_event(event)
        if opportunity is not None:
            ledger.action_opportunities.append(opportunity)
        intent, attempt, performance, occurrence = run_action_pipeline(
            state,
            model_input,
            routed,
            opportunity,
        )
        action_window_errors = [] if window_error is None else [window_error]
        if attempt is not None:
            ledger.attempts.append(attempt)
        if performance is not None:
            ledger.performance_receipts.append(performance)
        if occurrence is not None:
            ledger.action_occurrences.append(occurrence)

        state = apply_slow_update(state, model_input, phenomenal, performance)
        deltas = self._numeric_deltas(before, state, event.event_id)

        lane = "internal" if not event.external else (
            "testimony" if event.provenance_kind is ProvenanceKind.TESTIMONY else "observation"
        )
        ledger.episode_traces.append(
            EpisodeTrace(
                trace_id=f"trace:{event.event_id}:input",
                event_id=event.event_id,
                lane=lane,
                source_id=event.source_id,
                provenance_kind=event.provenance_kind,
                tick=processed_tick,
            )
        )
        if attempt is not None:
            ledger.episode_traces.append(
                EpisodeTrace(
                    trace_id=f"trace:{event.event_id}:attempt",
                    event_id=event.event_id,
                    lane="action_attempt",
                    source_id="self",
                    provenance_kind=ProvenanceKind.INFERENCE,
                    tick=processed_tick,
                )
            )
        if performance is not None:
            ledger.episode_traces.append(
                EpisodeTrace(
                    trace_id=f"trace:{event.event_id}:performed",
                    event_id=event.event_id,
                    lane="performed_action",
                    source_id="self",
                    provenance_kind=ProvenanceKind.PERFORMED_ACTION,
                    tick=processed_tick,
                )
            )

        trace = TickTrace(
            processed_tick=processed_tick,
            observation=artifact,
            phenomenal=phenomenal,
            routed=routed,
            judgments=state.evidence_assessment.claims,
            action_opportunity=opportunity,
            intent=intent,
            attempt=attempt,
            performance=performance,
            action_occurrence=occurrence,
            deltas=deltas,
            state_before=before,
            state_after=state,
        )
        ledger.tick_traces.append(trace)

        errors = [*linking_errors, *action_window_errors]
        errors.extend(validate_state_bounds(state))
        errors.extend(validate_routing_distribution(routed))
        errors.extend(
            validate_evidence_assessment(
                state.evidence_assessment,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                links,
                policy=self._assessment_policy,
            )
        )
        errors.extend(validate_action_lineage(intent, attempt, performance, occurrence))
        errors.extend(
            validate_action_opportunity(
                opportunity,
                intent,
                event_id=event.event_id,
            )
        )
        errors.extend(validate_intent_selection(intent, routed))
        errors.extend(validate_agency_hypothesis(intent, performance))
        ledger.invariant_errors.extend(f"{event.event_id}:{error}" for error in errors)
        return state

    @staticmethod
    def _numeric_deltas(before: HumanState, after: HumanState, event_id: str) -> tuple[StateDelta, ...]:
        before_values = dict(iter_unit_values(before))
        after_values = dict(iter_unit_values(after))
        return tuple(
            StateDelta(field=name, before=before_values[name], after=value, cause_event_id=event_id)
            for name, value in sorted(after_values.items())
            if abs(value - before_values[name]) > 1e-12
        )
