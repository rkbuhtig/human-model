"""Canonical semantic baseline for Human Model Dynamics v0.1.

The projection in this module intentionally serializes domain meaning rather
than Python implementation details.  It does not contain dataclass names,
module paths, repr output, wall-clock timings, or memory measurements.  This
allows later refactors to move and rename implementation types while retaining
an exact regression oracle for the v0.1 delayed-reply behavior.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .engine import DynamicsEngine, EngineConfig, SimulationResult
from .scenario import load_scenario
from .types import ClaimState, HumanState


BASELINE_SCHEMA = "human-model-semantic-baseline/0.1"
BASELINE_SOURCE_REVISION = "9b731b7f92700227de1fae8adc79e1d8e687d25f"
FLOAT_DIGITS = 12

PACKAGE_DIR = Path(__file__).resolve().parent
DELAYED_REPLY_SCENARIO = PACKAGE_DIR / "scenarios" / "delayed_reply.json"

# These values make the baseline independent of future changes to EngineConfig
# defaults.  They are the v0.1 defaults at the frozen source revision.
DELAYED_REPLY_ENGINE_CONFIG = EngineConfig(
    base_capacity_per_tick=6,
    queue_limit=64,
    drain_ticks=20,
    routing_temperature=0.62,
    adoption_threshold=0.75,
    release_threshold=0.55,
    minimum_ground_mass=0.50,
    ingress_policy="priority",
)


def _number(value: float) -> float:
    """Return a stable finite JSON number without negative zero."""

    if not math.isfinite(value):
        raise ValueError(f"baseline cannot serialize a non-finite value: {value!r}")
    rounded = round(float(value), FLOAT_DIGITS)
    return 0.0 if rounded == 0.0 else rounded


def _claim_projection(claim: ClaimState) -> dict[str, Any]:
    """Project subjective claim state without implementation-generated IDs."""

    return {
        "stance": claim.stance.value,
        "confidence": _number(claim.confidence),
        "support_mass": _number(claim.support_mass),
        "contradiction_mass": _number(claim.contradiction_mass),
        "supports": [
            {
                "independence_key": item.independence_key,
                "strength": _number(item.strength),
            }
            for item in sorted(claim.supports, key=lambda item: item.independence_key)
        ],
        "contradicts": [
            {
                "independence_key": item.independence_key,
                "strength": _number(item.strength),
            }
            for item in sorted(claim.contradicts, key=lambda item: item.independence_key)
        ],
        "ground_count": len(claim.grounds),
    }


def _slow_state_projection(state: HumanState) -> dict[str, float]:
    """Project only the explicitly slow or path-dependent v0.1 residences."""

    return {
        "affective.residual_distress": _number(state.affective.residual_distress),
        "affective.update_rate": _number(state.affective.update_rate),
        "associative.ambiguity_sensitivity": _number(
            state.associative.ambiguity_sensitivity
        ),
        "associative.rejection_access": _number(state.associative.rejection_access),
        "habit.impulsivity": _number(state.habit.impulsivity),
        "habit.withdrawal_bias": _number(state.habit.withdrawal_bias),
        "narrative.rejection_story": _number(state.narrative.rejection_story),
        "narrative.relational_security": _number(
            state.narrative.relational_security
        ),
        "relationship.boundary_strain": _number(
            state.relationship.boundary_strain
        ),
        "relationship.stake": _number(state.relationship.stake),
        "relationship.trust": _number(state.relationship.trust),
    }


def _evidence_digest(result: SimulationResult) -> list[dict[str, Any]]:
    artifacts = result.ledger.observations_by_id
    rows = []
    for link in result.ledger.evidence_links:
        artifact = artifacts[link.artifact_id]
        rows.append(
            {
                "event_id": artifact.event_id,
                "source_tick": artifact.source_tick,
                "observed_tick": artifact.observed_tick,
                "claim_id": link.claim_id,
                "scope": link.scope,
                "relation": link.relation.value,
                "strength": _number(link.strength),
                "provenance": link.provenance_kind.value,
                "grounding_rule": link.grounding_rule_id,
                "independence_key": link.independence_key,
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            row["observed_tick"],
            row["source_tick"],
            row["event_id"],
            row["claim_id"],
            row["scope"],
            row["relation"],
            row["grounding_rule"],
        ),
    )


def _claim_transitions(result: SimulationResult) -> list[dict[str, Any]]:
    transitions = []
    for trace in result.ledger.tick_traces:
        before = {
            (claim.claim_id, claim.scope): claim
            for claim in trace.state_before.epistemic.claims
        }
        after = {
            (claim.claim_id, claim.scope): claim
            for claim in trace.state_after.epistemic.claims
        }
        for claim_id, scope in sorted(set(before) | set(after)):
            before_claim = before.get((claim_id, scope), ClaimState(claim_id, scope))
            after_claim = after.get((claim_id, scope), ClaimState(claim_id, scope))
            before_value = _claim_projection(before_claim)
            after_value = _claim_projection(after_claim)
            if before_value == after_value:
                continue
            transitions.append(
                {
                    "event_id": trace.observation.event_id,
                    "processed_tick": trace.processed_tick,
                    "claim_id": claim_id,
                    "scope": scope,
                    "before": before_value,
                    "after": after_value,
                }
            )
    return transitions


def _decision_routes(result: SimulationResult) -> list[dict[str, Any]]:
    decisions = []
    for trace in result.ledger.tick_traces:
        if trace.intent is None:
            continue
        decisions.append(
            {
                "event_id": trace.observation.event_id,
                "processed_tick": trace.processed_tick,
                "candidates": [
                    {
                        "action": routed.candidate.action_kind,
                        "salience": _number(routed.salience),
                        "probability": _number(routed.probability),
                        "influences": [
                            {
                                "channel": term.channel,
                                "delta": _number(term.delta),
                            }
                            for term in routed.terms
                        ],
                    }
                    for routed in sorted(
                        trace.routed, key=lambda item: item.candidate.action_kind
                    )
                ],
            }
        )
    return decisions


def _action_chains(result: SimulationResult) -> list[dict[str, Any]]:
    chains = []
    for trace in result.ledger.tick_traces:
        if not any(
            (
                trace.intent,
                trace.attempt,
                trace.performance,
                trace.action_occurrence,
            )
        ):
            continue

        selected_action = None
        if trace.intent is not None:
            selected = [
                item.candidate.action_kind
                for item in trace.routed
                if item.candidate.candidate_id
                == trace.intent.selected_candidate_id
            ]
            selected_action = selected[0] if len(selected) == 1 else None

        intent = None
        if trace.intent is not None:
            intent = {
                "action": trace.intent.action_kind,
                "selected_candidate_action": selected_action,
                "coercion": _number(trace.intent.coercion),
            }

        attempt = None
        if trace.attempt is not None:
            attempt = {
                "action": trace.attempt.action_kind,
                "tick": trace.attempt.tick,
                "allowed": trace.attempt.authorization.allowed,
                "available_capacity": _number(
                    trace.attempt.authorization.available_capacity
                ),
                "required_capacity": _number(
                    trace.attempt.authorization.required_capacity
                ),
                "references_intent": (
                    trace.intent is not None
                    and trace.attempt.intent_id == trace.intent.intent_id
                ),
            }

        performance = None
        if trace.performance is not None:
            performance = {
                "action": trace.performance.action_kind,
                "tick": trace.performance.tick,
                "agency": _number(trace.performance.agency),
                "references_attempt": (
                    trace.attempt is not None
                    and trace.performance.attempt_id == trace.attempt.attempt_id
                ),
            }

        occurrence = None
        if trace.action_occurrence is not None:
            occurrence = {
                "action": trace.action_occurrence.action_kind,
                "tick": trace.action_occurrence.tick,
                "references_performance": (
                    trace.performance is not None
                    and trace.action_occurrence.caused_by_receipt_id
                    == trace.performance.receipt_id
                ),
            }

        chains.append(
            {
                "event_id": trace.observation.event_id,
                "processed_tick": trace.processed_tick,
                "intent": intent,
                "attempt": attempt,
                "performance": performance,
                "occurrence": occurrence,
            }
        )
    return chains


def semantic_projection(
    result: SimulationResult,
    *,
    scenario_id: str,
    scenario_schema: str,
    config: EngineConfig,
) -> dict[str, Any]:
    """Create the class- and file-name-independent v0.1 semantic projection."""

    return {
        "schema_version": BASELINE_SCHEMA,
        "source_revision": BASELINE_SOURCE_REVISION,
        "scenario": {
            "id": scenario_id,
            "schema_version": scenario_schema,
        },
        "engine_policy": {
            "base_capacity_per_tick": config.base_capacity_per_tick,
            "queue_limit": config.queue_limit,
            "drain_ticks": config.drain_ticks,
            "routing_temperature": _number(config.routing_temperature),
            "adoption_threshold": _number(config.adoption_threshold),
            "release_threshold": _number(config.release_threshold),
            "minimum_ground_mass": _number(config.minimum_ground_mass),
            "ingress_policy": config.ingress_policy,
        },
        "evidence_digest": _evidence_digest(result),
        "claim_transitions": _claim_transitions(result),
        "decision_routes": _decision_routes(result),
        "action_chains": _action_chains(result),
        "slow_state_trajectory": {
            "initial": _slow_state_projection(result.initial_state),
            "after_events": [
                {
                    "event_id": trace.observation.event_id,
                    "source_tick": trace.observation.source_tick,
                    "processed_tick": trace.processed_tick,
                    "state": _slow_state_projection(trace.state_after),
                }
                for trace in result.ledger.tick_traces
            ],
        },
        "input_accounting": {
            "raw_received": result.ledger.raw_received,
            "unique_received": result.ledger.unique_received,
            "processed": result.ledger.processed,
            "deferred_event_ids": sorted(result.ledger.deferred_event_ids),
            "dropped_event_ids": sorted(result.ledger.dropped_event_ids),
            "unresolved_event_ids": sorted(result.ledger.unresolved_event_ids),
            "duplicate_event_ids": sorted(result.ledger.duplicate_event_ids),
            "collision_event_ids": sorted(result.ledger.collision_event_ids),
            "accounting_ok": result.input_accounting_ok,
        },
    }


def build_delayed_reply_baseline() -> dict[str, Any]:
    """Run the frozen delayed-reply case and return its semantic projection."""

    scenario = load_scenario(DELAYED_REPLY_SCENARIO)
    engine = DynamicsEngine(DELAYED_REPLY_ENGINE_CONFIG)
    result = scenario.run(engine)
    return semantic_projection(
        result,
        scenario_id=scenario.scenario_id,
        scenario_schema=scenario.schema_version,
        config=DELAYED_REPLY_ENGINE_CONFIG,
    )


def canonical_json(projection: dict[str, Any]) -> str:
    """Render a reproducible UTF-8 JSON representation."""

    return json.dumps(
        projection,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"


def main() -> None:
    print(canonical_json(build_delayed_reply_baseline()), end="")


if __name__ == "__main__":
    main()
