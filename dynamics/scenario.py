"""Versioned JSON scenario loading and command-line execution."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .contract import ProvenanceKind
from .engine import DynamicsEngine, EngineConfig, SimulationResult
from .models import (
    AccessState,
    AffectivePrior,
    AssociativeState,
    BodyState,
    HabitPolicy,
    HumanState,
    NarrativeState,
    RelationalProfile,
)
from .protocol import (
    ClaimSignal,
    EventTemporalEnvelope,
    ScenarioEvent,
    SimTime,
)


@dataclass(frozen=True, slots=True)
class Scenario:
    schema_version: str
    scenario_id: str
    description: str
    hidden_worlds: dict[str, dict[str, Any]]
    initial_state: HumanState
    events: tuple[ScenarioEvent, ...]

    def run(self, engine: DynamicsEngine | None = None) -> SimulationResult:
        # hidden_worlds intentionally does not enter DynamicsEngine.run().
        return (engine or DynamicsEngine()).run(self.initial_state, self.events)


def _signals(items: list[dict[str, Any]] | None) -> tuple[ClaimSignal, ...]:
    return tuple(
        ClaimSignal(
            claim_id=str(item["claim_id"]),
            strength=float(item["strength"]),
            rule_id=str(item["rule_id"]),
            scope=str(item.get("scope", "scenario")),
        )
        for item in (items or [])
    )


def _strict_bool(item: dict[str, Any], key: str, default: bool) -> bool:
    value = item.get(key, default)
    if type(value) is not bool:
        raise TypeError(f"{key} must be a JSON boolean, got {type(value).__name__}")
    return value


def _event(item: dict[str, Any]) -> ScenarioEvent:
    return ScenarioEvent(
        event_id=str(item["event_id"]),
        tick=int(item["tick"]),
        kind=str(item["kind"]),
        external=_strict_bool(item, "external", True),
        source_id=str(item.get("source_id", "unknown")),
        provenance_kind=ProvenanceKind(item.get("provenance_kind", "direct_observation")),
        independence_key=str(item.get("independence_key", item.get("source_id", "unknown"))),
        ambiguity=float(item.get("ambiguity", 0.0)),
        salience=float(item.get("salience", 0.5)),
        time_pressure=float(item.get("time_pressure", 0.0)),
        memory_interference=float(item.get("memory_interference", 0.0)),
        candidate_fanout=float(item.get("candidate_fanout", 0.0)),
        ingress_priority=float(item.get("ingress_priority", 0.5)),
        energy_delta=float(item.get("energy_delta", 0.0)),
        arousal_delta=float(item.get("arousal_delta", 0.0)),
        capacity_delta=float(item.get("capacity_delta", 0.0)),
        attention_delta=float(item.get("attention_delta", 0.0)),
        soothing=float(item.get("soothing", 0.0)),
        trust_delta=float(item.get("trust_delta", 0.0)),
        boundary_delta=float(item.get("boundary_delta", 0.0)),
        action_window=_strict_bool(item, "action_window", False),
        coercion=float(item.get("coercion", 0.0)),
        supports=_signals(item.get("supports")),
        contradicts=_signals(item.get("contradicts")),
    )


def _canonical_id(item: dict[str, Any], key: str) -> str:
    if key not in item:
        raise KeyError(f"missing required temporal field: {key}")
    value = item[key]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _event_v02(item: dict[str, Any]) -> ScenarioEvent:
    if "temporal" in item:
        raise ValueError(
            "v0.2 temporal fields must use the flat canonical schema"
        )
    engine_owned = {"processed_at", "processing_sequence", "final_sim_time"}
    supplied_engine_fields = sorted(engine_owned.intersection(item))
    if supplied_engine_fields:
        raise ValueError(
            "engine-owned temporal fields are not scenario inputs: "
            + ", ".join(supplied_engine_fields)
        )
    delivery_id = _canonical_id(item, "delivery_id")
    occurrence_id = _canonical_id(item, "occurrence_id")
    if "occurred_at" not in item or "available_at" not in item:
        missing = "occurred_at" if "occurred_at" not in item else "available_at"
        raise KeyError(f"missing required temporal field: {missing}")
    occurred_at = SimTime(item["occurred_at"])
    available_at = SimTime(item["available_at"])

    reexposure = item.get("reexposure_of_occurrence_id")
    if reexposure is not None and (
        not isinstance(reexposure, str) or not reexposure
    ):
        raise ValueError("reexposure_of_occurrence_id must be a non-empty string")
    delivery_sequence = item.get("delivery_sequence")
    envelope = EventTemporalEnvelope(
        occurrence_id=occurrence_id,
        delivery_id=delivery_id,
        occurred_at=occurred_at,
        available_at=available_at,
        reexposure_of_occurrence_id=reexposure,
        delivery_sequence=delivery_sequence,
    )

    if "event_id" in item and item["event_id"] != delivery_id:
        raise ValueError("event_id must match canonical delivery_id")
    if "tick" in item and SimTime(item["tick"]) != available_at:
        raise ValueError("tick must match canonical available_at")

    return ScenarioEvent(
        event_id=delivery_id,
        tick=int(available_at),
        kind=str(item["kind"]),
        external=_strict_bool(item, "external", True),
        source_id=str(item.get("source_id", "unknown")),
        provenance_kind=ProvenanceKind(
            item.get("provenance_kind", "direct_observation")
        ),
        independence_key=str(
            item.get("independence_key", item.get("source_id", "unknown"))
        ),
        ambiguity=float(item.get("ambiguity", 0.0)),
        salience=float(item.get("salience", 0.5)),
        time_pressure=float(item.get("time_pressure", 0.0)),
        memory_interference=float(item.get("memory_interference", 0.0)),
        candidate_fanout=float(item.get("candidate_fanout", 0.0)),
        ingress_priority=float(item.get("ingress_priority", 0.5)),
        energy_delta=float(item.get("energy_delta", 0.0)),
        arousal_delta=float(item.get("arousal_delta", 0.0)),
        capacity_delta=float(item.get("capacity_delta", 0.0)),
        attention_delta=float(item.get("attention_delta", 0.0)),
        soothing=float(item.get("soothing", 0.0)),
        trust_delta=float(item.get("trust_delta", 0.0)),
        boundary_delta=float(item.get("boundary_delta", 0.0)),
        action_window=_strict_bool(item, "action_window", False),
        coercion=float(item.get("coercion", 0.0)),
        supports=_signals(item.get("supports")),
        contradicts=_signals(item.get("contradicts")),
        temporal=envelope,
    )


def _initial_state(item: dict[str, Any]) -> HumanState:
    return HumanState(
        body=BodyState(**item.get("body", {})).bounded(),
        access=AccessState(**item.get("access", {})).bounded(),
        associative=AssociativeState(**item.get("associative", {})).bounded(),
        affective=AffectivePrior(**item.get("affective", {})).bounded(),
        habit=HabitPolicy(**item.get("habit", {})).bounded(),
        narrative=NarrativeState(**item.get("narrative", {})).bounded(),
        relationship=RelationalProfile(**item.get("relationship", {})).bounded(),
    )


def load_scenario(path: str | Path) -> Scenario:
    source = Path(path)
    data = json.loads(source.read_text(encoding="utf-8"))
    schema_version = data.get("schema_version")
    if schema_version not in {
        "human-model-scenario/0.1",
        "human-model-scenario/0.2",
    }:
        raise ValueError(f"unsupported scenario schema: {data.get('schema_version')!r}")
    event_loader = _event if schema_version == "human-model-scenario/0.1" else _event_v02
    events = tuple(event_loader(item) for item in data.get("events", []))
    if (
        schema_version == "human-model-scenario/0.1"
        and len({event.event_id for event in events}) != len(events)
    ):
        # Duplicate IDs are allowed only in explicit idempotence tests assembled in code.
        raise ValueError("scenario source contains duplicate event_id")
    return Scenario(
        schema_version=data["schema_version"],
        scenario_id=str(data["scenario_id"]),
        description=str(data.get("description", "")),
        hidden_worlds=dict(data.get("hidden_worlds", {})),
        initial_state=_initial_state(data.get("initial_state", {})),
        events=events,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--capacity", type=int, default=6)
    parser.add_argument("--queue-limit", type=int, default=64)
    args = parser.parse_args()
    scenario = load_scenario(args.scenario)
    result = scenario.run(
        DynamicsEngine(
            EngineConfig(
                base_capacity_per_tick=args.capacity,
                queue_limit=args.queue_limit,
            )
        )
    )
    print(json.dumps({"scenario_id": scenario.scenario_id, **result.summary()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
