"""Versioned protocol events and their explicit model-input encoding."""

from __future__ import annotations

from dataclasses import dataclass

from ..contract.grounding import GroundingSignal, GroundingSubmission
from ..contract.records import (
    ACTION_OPPORTUNITY_RULE_V01,
    ActionOpportunity,
    EvidenceRelation,
    ProvenanceKind,
    action_opportunity_id,
)
from ..interfaces import ModelInput, clamp01
from ..temporal import EventTemporalEnvelope, SimTime, legacy_temporal_envelope


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
    temporal: EventTemporalEnvelope | None = None

    def __post_init__(self) -> None:
        if not self.event_id or not self.kind or not self.source_id:
            raise ValueError("event_id, kind, and source_id must be non-empty")
        canonical_tick = SimTime(self.tick)
        temporal = self.temporal
        if temporal is None:
            temporal = legacy_temporal_envelope(self.event_id, canonical_tick)
            object.__setattr__(self, "temporal", temporal)
        elif not isinstance(temporal, EventTemporalEnvelope):
            raise TypeError("temporal must be EventTemporalEnvelope or None")
        elif (
            temporal.delivery_id != self.event_id
            or temporal.available_at != canonical_tick
        ):
            raise ValueError(
                "ScenarioEvent event_id/tick must match delivery_id/available_at"
            )

        if temporal.reexposure_of_occurrence_id is not None:
            if self.external is not False:
                raise ValueError("reexposure events must be internal")
            if self.supports or self.contradicts:
                raise ValueError("reexposure events cannot carry evidence signals")
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

    @property
    def delivery_id(self) -> str:
        assert self.temporal is not None
        return self.temporal.delivery_id

    @property
    def occurrence_id(self) -> str:
        assert self.temporal is not None
        return self.temporal.occurrence_id

    @property
    def occurred_at(self) -> SimTime:
        assert self.temporal is not None
        return self.temporal.occurred_at

    @property
    def available_at(self) -> SimTime:
        assert self.temporal is not None
        return self.temporal.available_at

    @property
    def reexposure_of_occurrence_id(self) -> str | None:
        assert self.temporal is not None
        return self.temporal.reexposure_of_occurrence_id

    @property
    def delivery_sequence(self) -> int | None:
        assert self.temporal is not None
        return self.temporal.delivery_sequence


def encode_model_input(event: ScenarioEvent) -> ModelInput:
    """Make every protocol-to-model field transfer explicit and auditable."""

    return ModelInput(
        event_id=event.event_id,
        kind=event.kind,
        source_is_external=event.external,
        ambiguity=event.ambiguity,
        salience=event.salience,
        time_pressure=event.time_pressure,
        memory_interference=event.memory_interference,
        candidate_fanout=event.candidate_fanout,
        energy_delta=event.energy_delta,
        arousal_delta=event.arousal_delta,
        capacity_delta=event.capacity_delta,
        attention_delta=event.attention_delta,
        soothing=event.soothing,
        trust_delta=event.trust_delta,
        boundary_delta=event.boundary_delta,
        coercion=event.coercion,
    )


def encode_grounding_submission(event: ScenarioEvent) -> GroundingSubmission:
    """Narrow a scenario event to fields the certification contract accepts."""

    signals = tuple(
        GroundingSignal(
            claim_id=signal.claim_id,
            strength=signal.strength,
            rule_id=signal.rule_id,
            relation=relation,
            scope=signal.scope,
        )
        for relation, group in (
            (EvidenceRelation.SUPPORTS, event.supports),
            (EvidenceRelation.CONTRADICTS, event.contradicts),
        )
        for signal in group
    )
    return GroundingSubmission(
        event_id=event.event_id,
        kind=event.kind,
        external=event.external,
        provenance_kind=event.provenance_kind,
        independence_key=event.independence_key,
        signals=signals,
    )


def action_opportunity_from_event(
    event: ScenarioEvent,
) -> tuple[ActionOpportunity | None, str | None]:
    """Open a typed surface only for the protocol's declared decision event."""

    if not event.action_window:
        return None, None
    if not (
        event.kind == "decision_window"
        and not event.external
        and event.provenance_kind is ProvenanceKind.INFERENCE
    ):
        return None, "INVALID_ACTION_WINDOW_EVENT"
    return (
        ActionOpportunity(
            opportunity_id=action_opportunity_id(event.event_id),
            event_id=event.event_id,
            rule_id=ACTION_OPPORTUNITY_RULE_V01,
        ),
        None,
    )


def action_window_error(event: ScenarioEvent) -> str | None:
    """v0.1 compatibility helper."""

    return action_opportunity_from_event(event)[1]
