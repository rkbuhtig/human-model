"""Deterministic typed hybrid engine for Human Model Dynamics v0.1."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
import hashlib
from typing import Iterable

from .epistemics import apply_evidence_links, links_from_event
from .invariants import (
    validate_action_chain,
    validate_distribution,
    validate_epistemics,
    validate_state_bounds,
)
from .routing import route_candidates
from .types import (
    ActionAttempt,
    ActionOccurrence,
    BodyAuthorization,
    BodyState,
    EpisodeTrace,
    EpistemicState,
    EvidenceLink,
    HumanState,
    IntentDecision,
    ObservationArtifact,
    PerformanceReceipt,
    PhenomenalActivation,
    ProvenanceKind,
    RoutedCandidate,
    ScenarioEvent,
    StateDelta,
    TickTrace,
    clamp01,
    iter_unit_values,
)


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
            for claim in self.final_state.epistemic.claims
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
            validate_epistemics(
                initial_state.epistemic,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                (),
                adoption_threshold=self.config.adoption_threshold,
                release_threshold=self.config.release_threshold,
                minimum_ground_mass=self.config.minimum_ground_mass,
            )
        )
        ledger.invariant_errors.extend(f"initial:{error}" for error in initial_errors)
        arrivals: dict[int, list[ScenarioEvent]] = defaultdict(list)
        for event in ordered:
            arrivals[event.tick].append(event)
        last_arrival_tick = max((event.tick for event in ordered), default=0)

        state = initial_state
        pending: list[ScenarioEvent] = []
        seen_event_fingerprints: dict[str, str] = {}
        end_tick = last_arrival_tick + self.config.drain_ticks

        for tick in range(0, end_tick + 1):
            for event in arrivals.get(tick, ()):
                ledger.raw_received += 1
                fingerprint = self._event_fingerprint(event)
                prior_fingerprint = seen_event_fingerprints.get(event.event_id)
                if prior_fingerprint is not None:
                    if prior_fingerprint == fingerprint:
                        ledger.duplicate_event_ids.append(event.event_id)
                    else:
                        ledger.collision_event_ids.append(event.event_id)
                        ledger.invariant_errors.append(
                            f"{event.event_id}:EVENT_ID_PAYLOAD_COLLISION"
                        )
                    continue
                seen_event_fingerprints[event.event_id] = fingerprint
                ledger.unique_received += 1
                pending.append(event)

            capacity = self._capacity(state)
            if self.config.ingress_policy == "priority":
                pending.sort(
                    key=lambda event: (
                        -event.ingress_priority,
                        event.tick,
                    )
                )
            processing = pending[:capacity]
            pending = pending[capacity:]

            if pending:
                ledger.deferred_event_ids.update(event.event_id for event in pending)
            if len(pending) > self.config.queue_limit:
                overflow = pending[self.config.queue_limit :]
                ledger.dropped_event_ids.extend(event.event_id for event in overflow)
                pending = pending[: self.config.queue_limit]

            epistemic_anchor = state.epistemic
            for event in processing:
                queue_pressure = clamp01(len(pending) / self.config.queue_limit)
                state = self._process_event(
                    state,
                    event,
                    tick,
                    queue_pressure,
                    ledger,
                    epistemic_anchor,
                )
                ledger.processed += 1

        ledger.unresolved_event_ids.extend(event.event_id for event in pending)
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
            validate_epistemics(
                state.epistemic,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                (),
                adoption_threshold=self.config.adoption_threshold,
                release_threshold=self.config.release_threshold,
                minimum_ground_mass=self.config.minimum_ground_mass,
            )
        )
        ledger.invariant_errors.extend(f"final:{error}" for error in final_errors)

        return SimulationResult(initial_state=initial_state, final_state=state, ledger=ledger)

    def _capacity(self, state: HumanState) -> int:
        attention_factor = 0.35 + 0.65 * state.access.attention_budget
        body_factor = 0.45 + 0.55 * state.body.energy
        return max(1, round(self.config.base_capacity_per_tick * attention_factor * body_factor))

    @staticmethod
    def _event_fingerprint(event: ScenarioEvent) -> str:
        return hashlib.sha256(repr(event).encode("utf-8")).hexdigest()

    def _process_event(
        self,
        state: HumanState,
        event: ScenarioEvent,
        processed_tick: int,
        queue_pressure: float,
        ledger: SimulationLedger,
        epistemic_anchor: EpistemicState,
    ) -> HumanState:
        before = state
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

        links, linking_errors = links_from_event(event, artifact)
        ledger.provenance_loss_count += sum("provenance" in error.lower() for error in linking_errors)
        ledger.evidence_links.extend(links)
        ledger.evidence_links_by_id.update((link.link_id, link) for link in links)
        epistemic = apply_evidence_links(
            state.epistemic,
            links,
            stance_anchor=epistemic_anchor,
            adoption_threshold=self.config.adoption_threshold,
            release_threshold=self.config.release_threshold,
            minimum_ground_mass=self.config.minimum_ground_mass,
        )

        body = BodyState(
            energy=state.body.energy + event.energy_delta,
            arousal=state.body.arousal + event.arousal_delta,
            action_capacity=state.body.action_capacity + event.capacity_delta,
        ).bounded()
        access = replace(
            state.access,
            attention_budget=clamp01(
                state.access.attention_budget
                + event.attention_delta
                - 0.08 * event.time_pressure
                - 0.05 * queue_pressure
                + 0.04 * event.soothing
            ),
            interference=clamp01(
                0.82 * state.access.interference
                + 0.18 * event.memory_interference
                + 0.08 * queue_pressure
            ),
            queue_load=clamp01(0.65 * state.access.queue_load + 0.35 * queue_pressure),
        )
        relationship = replace(
            state.relationship,
            trust=clamp01(state.relationship.trust + (event.trust_delta if event.external else 0.0)),
            boundary_strain=clamp01(
                state.relationship.boundary_strain + (event.boundary_delta if event.external else 0.0)
            ),
        )
        state = replace(
            state,
            clock=processed_tick,
            body=body,
            access=access,
            relationship=relationship,
            epistemic=epistemic,
        )

        phenomenal = self._phenomenal(state, event)
        routed = route_candidates(
            state,
            event,
            phenomenal,
            temperature=self.config.routing_temperature,
        )
        intent, attempt, performance, occurrence = self._action_pipeline(state, event, routed)
        action_window_errors = []
        if event.action_window and not (
            event.kind == "decision_window"
            and not event.external
            and event.provenance_kind is ProvenanceKind.INFERENCE
        ):
            action_window_errors.append("INVALID_ACTION_WINDOW_EVENT")
        if attempt is not None:
            ledger.attempts.append(attempt)
        if performance is not None:
            ledger.performance_receipts.append(performance)
        if occurrence is not None:
            ledger.action_occurrences.append(occurrence)

        state = self._slow_update(state, event, phenomenal, performance)
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
            judgments=state.epistemic.claims,
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
        errors.extend(validate_distribution(routed))
        errors.extend(
            validate_epistemics(
                state.epistemic,
                ledger.evidence_links_by_id,
                ledger.observations_by_id,
                links,
                adoption_threshold=self.config.adoption_threshold,
                release_threshold=self.config.release_threshold,
                minimum_ground_mass=self.config.minimum_ground_mass,
            )
        )
        errors.extend(validate_action_chain(intent, attempt, performance, occurrence, routed))
        ledger.invariant_errors.extend(f"{event.event_id}:{error}" for error in errors)
        return state

    @staticmethod
    def _rejection_confidence(state: HumanState) -> float:
        relevant = [
            claim.confidence
            for claim in state.epistemic.claims
            if "reject" in claim.claim_id or "avoid" in claim.claim_id
        ]
        return max(relevant, default=0.0)

    def _phenomenal(self, state: HumanState, event: ScenarioEvent) -> PhenomenalActivation:
        fatigue = 1.0 - state.body.energy
        interpreted_threat = (
            0.60 * state.associative.rejection_access
            + 0.40 * state.narrative.rejection_story
        ) * state.relationship.stake
        target = (
            0.24 * event.ambiguity
            + 0.18 * fatigue
            + 0.25 * interpreted_threat
            + 0.13 * event.time_pressure
            + 0.10 * state.access.interference
            + 0.10 * self._rejection_confidence(state)
            - 0.35 * event.soothing
        )
        distress = clamp01(0.62 * state.affective.residual_distress + 0.38 * clamp01(target))
        urgency = clamp01(
            0.45 * event.time_pressure
            + 0.25 * state.body.arousal
            + 0.20 * distress
            + 0.10 * state.access.queue_load
        )
        ambiguity = clamp01(
            event.ambiguity
            + 0.20 * state.access.interference
            + 0.10 * state.access.queue_load
        )
        return PhenomenalActivation(distress=distress, urgency=urgency, ambiguity=ambiguity)

    def _action_pipeline(
        self,
        state: HumanState,
        event: ScenarioEvent,
        routed: tuple[RoutedCandidate, ...],
    ) -> tuple[
        IntentDecision | None,
        ActionAttempt | None,
        PerformanceReceipt | None,
        ActionOccurrence | None,
    ]:
        if not event.action_window or not (
            event.kind == "decision_window"
            and not event.external
            and event.provenance_kind is ProvenanceKind.INFERENCE
        ):
            return None, None, None, None
        selected = max(routed, key=lambda item: item.probability)
        action = selected.candidate.action_kind
        intent = IntentDecision(
            intent_id=f"intent:{event.event_id}",
            action_kind="hold" if action == "wait" else action,
            selected_candidate_id=selected.candidate.candidate_id,
            coercion=event.coercion,
        )
        external_actions = {"ask": 0.35, "accuse": 0.50, "withdraw": 0.30}
        if action not in external_actions:
            return intent, None, None, None

        available = clamp01(
            0.65 * state.body.energy
            + 0.35 * state.body.action_capacity
            - 0.25 * state.access.queue_load
        )
        required = external_actions[action]
        authorization = BodyAuthorization(
            authorization_id=f"body-auth:{event.event_id}",
            allowed=available >= required,
            available_capacity=available,
            required_capacity=required,
        )
        attempt = ActionAttempt(
            attempt_id=f"attempt:{event.event_id}",
            intent_id=intent.intent_id,
            action_kind=action,
            authorization=authorization,
            tick=state.clock,
        )
        if not authorization.allowed:
            return intent, attempt, None, None

        performance = PerformanceReceipt(
            receipt_id=f"performance:{event.event_id}",
            attempt_id=attempt.attempt_id,
            action_kind=action,
            agency=clamp01(1.0 - event.coercion),
            tick=state.clock,
        )
        occurrence = ActionOccurrence(
            occurrence_id=f"action-occurrence:{event.event_id}",
            caused_by_receipt_id=performance.receipt_id,
            action_kind=action,
            tick=state.clock,
        )
        return intent, attempt, performance, occurrence

    def _slow_update(
        self,
        state: HumanState,
        event: ScenarioEvent,
        phenomenal: PhenomenalActivation,
        performance: PerformanceReceipt | None,
    ) -> HumanState:
        associative = replace(
            state.associative,
            rejection_access=clamp01(
                state.associative.rejection_access
                + 0.0030 * phenomenal.distress * event.salience
                - 0.0025 * event.soothing * state.relationship.trust
            ),
            ambiguity_sensitivity=clamp01(
                state.associative.ambiguity_sensitivity
                + 0.0010 * event.ambiguity
                - 0.0010 * event.soothing
            ),
        )
        affective = replace(
            state.affective,
            residual_distress=clamp01(
                state.affective.residual_distress
                + state.affective.update_rate
                * (phenomenal.distress - state.affective.residual_distress)
                - 0.025 * event.soothing
            ),
        )
        rejected = self._rejection_confidence(state)
        narrative_target = clamp01(0.55 * phenomenal.distress + 0.45 * rejected)
        narrative = replace(
            state.narrative,
            rejection_story=clamp01(
                state.narrative.rejection_story
                + 0.0040 * (narrative_target - state.narrative.rejection_story)
            ),
            relational_security=clamp01(
                state.narrative.relational_security
                + 0.0035
                * (
                    state.relationship.trust
                    - 0.40 * phenomenal.distress
                    - state.narrative.relational_security
                )
                + 0.0020 * event.soothing
            ),
        )
        habit = state.habit
        relationship = state.relationship
        body = state.body
        if performance is not None:
            cost = {"ask": 0.025, "accuse": 0.045, "withdraw": 0.020}.get(
                performance.action_kind, 0.0
            )
            body = replace(body, energy=clamp01(body.energy - cost))
            if performance.action_kind == "accuse":
                habit = replace(habit, impulsivity=clamp01(habit.impulsivity + 0.0010))
                relationship = replace(
                    relationship,
                    trust=clamp01(relationship.trust - 0.020),
                    boundary_strain=clamp01(relationship.boundary_strain + 0.040),
                )
        if event.soothing > 0.0:
            habit = replace(habit, impulsivity=clamp01(habit.impulsivity - 0.0005 * event.soothing))

        return replace(
            state,
            body=body,
            associative=associative,
            affective=affective,
            narrative=narrative,
            habit=habit,
            relationship=relationship,
        )

    @staticmethod
    def _numeric_deltas(before: HumanState, after: HumanState, event_id: str) -> tuple[StateDelta, ...]:
        before_values = dict(iter_unit_values(before))
        after_values = dict(iter_unit_values(after))
        return tuple(
            StateDelta(field=name, before=before_values[name], after=value, cause_event_id=event_id)
            for name, value in sorted(after_values.items())
            if abs(value - before_values[name]) > 1e-12
        )
