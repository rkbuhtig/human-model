from __future__ import annotations

from dataclasses import replace
import unittest

from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.stress import PRESETS, generate_stress_events, initial_state_for_load, run_load_case


class StressTests(unittest.TestCase):
    def test_generation_and_execution_are_reproducible(self) -> None:
        load = PRESETS["ambiguity_stake"]
        events_a = generate_stress_events(load, 12345)
        events_b = generate_stress_events(load, 12345)
        self.assertEqual(events_a, events_b)
        engine = DynamicsEngine(EngineConfig(base_capacity_per_tick=20, queue_limit=512))
        result_a = engine.run(initial_state_for_load(load), events_a)
        result_b = engine.run(initial_state_for_load(load), events_b)
        self.assertEqual(result_a.summary(), result_b.summary())
        self.assertEqual(result_a.ledger.tick_traces, result_b.ledger.tick_traces)

    def test_combined_semantic_stress_preserves_hard_invariants(self) -> None:
        _, summary = run_load_case(PRESETS["combined"], seed=20260712)
        self.assertTrue(summary["hard_pass"])
        self.assertEqual(summary["authority_leaks"], 0)
        self.assertEqual(summary["phantom_actions"], 0)
        self.assertEqual(summary["provenance_losses"], 0)
        self.assertTrue(summary["input_accounting_ok"])

    def test_overflow_is_explicitly_accounted(self) -> None:
        load = replace(PRESETS["baseline"], duration=4, recovery_ticks=1, input_rate=1.0)
        events = generate_stress_events(load, 77)
        engine = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=1, queue_limit=3, drain_ticks=0)
        )
        result = engine.run(initial_state_for_load(load), events)
        self.assertGreater(len(result.ledger.dropped_event_ids), 0)
        self.assertGreater(len(result.ledger.unresolved_event_ids), 0)
        self.assertTrue(result.input_accounting_ok)
        self.assertEqual(result.ledger.invariant_errors, [])

    def test_recovery_changes_state_without_erasing_history(self) -> None:
        result, summary = run_load_case(PRESETS["baseline"], seed=20260712)
        self.assertTrue(summary["hard_pass"])
        self.assertGreater(summary["recovery_drop"], 0.0)
        self.assertGreater(summary["plastic_residual"], 0.0)
        self.assertEqual(summary["recovery_status"], "passed_nonreset")
        self.assertNotEqual(result.initial_state, result.final_state)
        self.assertGreater(len(result.ledger.episode_traces), 0)
        self.assertGreater(len(result.ledger.evidence_links), 0)

    def test_priority_ingress_prevents_recovery_starvation(self) -> None:
        load = PRESETS["combined"]
        fifo_config = EngineConfig(
            base_capacity_per_tick=6,
            queue_limit=256,
            drain_ticks=30,
            ingress_policy="fifo",
        )
        priority_config = replace(fifo_config, ingress_policy="priority")
        _, fifo = run_load_case(load, seed=20260712, engine_config=fifo_config)
        _, priority = run_load_case(load, seed=20260712, engine_config=priority_config)
        self.assertTrue(fifo["hard_pass"])
        self.assertTrue(priority["hard_pass"])
        self.assertEqual(fifo["recovery_status"], "not_reached_due_to_backlog")
        self.assertNotEqual(priority["recovery_status"], "not_reached_due_to_backlog")
        self.assertEqual(priority["recovery_delivery_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
