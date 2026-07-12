from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import unittest

from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.scenario import load_scenario
from dynamics.types import ClaimSignal, ProvenanceKind, ScenarioEvent


SCENARIO = Path(__file__).parents[1] / "scenarios" / "delayed_reply.json"


def evidence_digest(result) -> tuple[tuple[str, str, str, float], ...]:
    return tuple(
        (link.artifact_id, link.claim_id, link.relation.value, link.strength)
        for link in result.ledger.evidence_links
    )


def route_at(result, event_id: str) -> dict[str, float]:
    trace = next(trace for trace in result.ledger.tick_traces if trace.observation.event_id == event_id)
    return {item.candidate.action_kind: item.probability for item in trace.routed}


class CounterfactualTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = load_scenario(SCENARIO)
        self.engine = DynamicsEngine(EngineConfig(base_capacity_per_tick=20))

    def test_hidden_worlds_cannot_change_preobservation_trajectory(self) -> None:
        self.assertNotEqual(
            self.scenario.hidden_worlds["busy"],
            self.scenario.hidden_worlds["avoiding"],
        )
        shared_prefix = tuple(event for event in self.scenario.events if event.tick <= 5)
        busy_stream = shared_prefix + tuple(
            event for event in self.scenario.events if event.tick > 5
        )
        avoiding_observation = ScenarioEvent(
            event_id="dr-06-avoidance-admission",
            tick=6,
            kind="counterpart_explanation_message",
            external=True,
            source_id="counterpart",
            provenance_kind=ProvenanceKind.TESTIMONY,
            independence_key="counterpart-admission",
            supports=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    0.80,
                    "testimony-avoidance",
                ),
            ),
        )
        avoiding_stream = shared_prefix + (avoiding_observation,)

        busy_pre = self.engine.run(self.scenario.initial_state, shared_prefix)
        avoiding_pre = self.engine.run(self.scenario.initial_state, shared_prefix)
        self.assertEqual(busy_pre.summary(), avoiding_pre.summary())
        self.assertEqual(busy_pre.ledger.tick_traces, avoiding_pre.ledger.tick_traces)

        busy_post = self.engine.run(self.scenario.initial_state, busy_stream)
        avoiding_post = self.engine.run(self.scenario.initial_state, avoiding_stream)
        self.assertNotEqual(busy_post.summary(), avoiding_post.summary())
        self.assertNotEqual(
            busy_post.final_state.epistemic.get(
                "C3_counterpart_intentionally_avoids"
            ).stance,
            avoiding_post.final_state.epistemic.get(
                "C3_counterpart_intentionally_avoids"
            ).stance,
        )

    def test_stake_changes_routing_not_evidence(self) -> None:
        events = tuple(event for event in self.scenario.events if event.tick <= 5)
        low = replace(
            self.scenario.initial_state,
            relationship=replace(self.scenario.initial_state.relationship, stake=0.10),
        )
        high = replace(
            self.scenario.initial_state,
            relationship=replace(self.scenario.initial_state.relationship, stake=0.98),
        )
        low_result = self.engine.run(low, events)
        high_result = self.engine.run(high, events)
        self.assertEqual(evidence_digest(low_result), evidence_digest(high_result))
        self.assertNotEqual(
            route_at(low_result, "dr-05-decision"),
            route_at(high_result, "dr-05-decision"),
        )

    def test_rejection_history_changes_routing_not_evidence(self) -> None:
        events = tuple(event for event in self.scenario.events if event.tick <= 5)
        low = replace(
            self.scenario.initial_state,
            associative=replace(self.scenario.initial_state.associative, rejection_access=0.05),
        )
        high = replace(
            self.scenario.initial_state,
            associative=replace(self.scenario.initial_state.associative, rejection_access=0.95),
        )
        low_result = self.engine.run(low, events)
        high_result = self.engine.run(high, events)
        self.assertEqual(evidence_digest(low_result), evidence_digest(high_result))
        low_route = route_at(low_result, "dr-05-decision")
        high_route = route_at(high_result, "dr-05-decision")
        self.assertGreater(
            high_route["accuse"] + high_route["withdraw"],
            low_route["accuse"] + low_route["withdraw"],
        )

    def test_correction_is_append_only_and_affect_can_lag(self) -> None:
        prefix_events = tuple(event for event in self.scenario.events if event.tick <= 5)
        prefix = self.engine.run(self.scenario.initial_state, prefix_events)
        result = self.scenario.run(self.engine)
        self.assertTrue(
            set(prefix.ledger.observations_by_id)
            <= set(result.ledger.observations_by_id)
        )
        self.assertTrue(
            set(prefix.ledger.evidence_links_by_id)
            <= set(result.ledger.evidence_links_by_id)
        )
        self.assertTrue(
            {attempt.attempt_id for attempt in prefix.ledger.attempts}
            <= {attempt.attempt_id for attempt in result.ledger.attempts}
        )
        old_link = "link:dr-03-friend:C3_counterpart_intentionally_avoids:scenario:supports"
        self.assertIn(old_link, result.ledger.evidence_links_by_id)
        claim = result.final_state.epistemic.get("C3_counterpart_intentionally_avoids")
        self.assertGreater(claim.contradiction_mass, claim.support_mass)
        self.assertGreater(result.final_state.affective.residual_distress, 0.0)
        self.assertEqual(result.authority_leak_count, 0)

    def test_action_capacity_changes_performance_not_prior_route_or_evidence(self) -> None:
        events = tuple(event for event in self.scenario.events if event.tick <= 5)
        open_state = replace(
            self.scenario.initial_state,
            body=replace(self.scenario.initial_state.body, action_capacity=0.99),
        )
        blocked_state = replace(
            self.scenario.initial_state,
            body=replace(self.scenario.initial_state.body, action_capacity=0.01),
        )
        open_result = self.engine.run(open_state, events)
        blocked_result = self.engine.run(blocked_state, events)
        self.assertEqual(evidence_digest(open_result), evidence_digest(blocked_result))
        self.assertEqual(
            route_at(open_result, "dr-05-decision"),
            route_at(blocked_result, "dr-05-decision"),
        )
        self.assertEqual(len(open_result.ledger.performance_receipts), 1)
        self.assertEqual(len(blocked_result.ledger.performance_receipts), 0)

    def test_same_tick_evidence_stance_is_independent_of_arrival_order(self) -> None:
        support = ScenarioEvent(
            event_id="same-tick-support",
            tick=0,
            kind="counterpart_explanation_message",
            external=True,
            source_id="counterpart",
            provenance_kind=ProvenanceKind.TESTIMONY,
            independence_key="same-tick-support",
            supports=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    0.80,
                    "testimony-avoidance",
                ),
            ),
        )
        contradict = ScenarioEvent(
            event_id="same-tick-contradict",
            tick=0,
            kind="counterpart_explanation_message",
            external=True,
            source_id="counterpart",
            provenance_kind=ProvenanceKind.TESTIMONY,
            independence_key="same-tick-contradict",
            contradicts=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    0.30,
                    "testimony-denies-avoidance",
                ),
            ),
        )
        first = self.engine.run(self.scenario.initial_state, (support, contradict))
        second = self.engine.run(self.scenario.initial_state, (contradict, support))
        first_claim = first.final_state.epistemic.get("C3_counterpart_intentionally_avoids")
        second_claim = second.final_state.epistemic.get("C3_counterpart_intentionally_avoids")
        self.assertAlmostEqual(first_claim.confidence, second_claim.confidence)
        self.assertEqual(first_claim.stance, second_claim.stance)


if __name__ == "__main__":
    unittest.main()
