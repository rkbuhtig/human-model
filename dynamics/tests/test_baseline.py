from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from dynamics.baseline import (
    BASELINE_SCHEMA,
    BASELINE_SOURCE_REVISION,
    build_delayed_reply_baseline,
    canonical_json,
    DELAYED_REPLY_ENGINE_CONFIG,
    DELAYED_REPLY_SCENARIO,
)
from dynamics.engine import DynamicsEngine
from dynamics.scenario import load_scenario


GOLDEN = Path(__file__).parents[1] / "reports" / "baseline-v0.1.json"
MANIFEST = Path(__file__).parents[1] / "reports" / "baseline-v0.1-manifest.json"


class SemanticBaselineTests(unittest.TestCase):
    def test_delayed_reply_matches_frozen_v01_semantics(self) -> None:
        expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
        actual = build_delayed_reply_baseline()
        self.assertEqual(actual, expected)
        self.assertEqual(canonical_json(actual), GOLDEN.read_text(encoding="utf-8"))

    def test_frozen_valid_scenario_has_no_invariant_errors(self) -> None:
        scenario = load_scenario(DELAYED_REPLY_SCENARIO)
        result = scenario.run(DynamicsEngine(DELAYED_REPLY_ENGINE_CONFIG))
        self.assertEqual(result.ledger.invariant_errors, [])

    def test_projection_has_no_runtime_performance_or_python_identity(self) -> None:
        projection = build_delayed_reply_baseline()
        rendered = canonical_json(projection)

        self.assertEqual(projection["schema_version"], BASELINE_SCHEMA)
        self.assertEqual(projection["source_revision"], BASELINE_SOURCE_REVISION)
        for forbidden in (
            "elapsed_seconds",
            "processed_events_per_second",
            "peak_memory_mib",
            "__class__",
            "dynamics.engine",
            "dynamics.types",
        ):
            self.assertNotIn(forbidden, rendered)

    def test_projection_covers_required_semantic_lanes(self) -> None:
        projection = build_delayed_reply_baseline()

        self.assertTrue(projection["evidence_digest"])
        self.assertTrue(projection["claim_transitions"])
        self.assertTrue(projection["decision_routes"])
        self.assertTrue(projection["action_chains"])
        self.assertTrue(projection["slow_state_trajectory"]["after_events"])

        accounting = projection["input_accounting"]
        self.assertIn("dropped_event_ids", accounting)
        self.assertIn("unresolved_event_ids", accounting)
        self.assertTrue(accounting["accounting_ok"])

    def test_manifest_pins_golden_hash_and_source_revision(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        digest = hashlib.sha256(GOLDEN.read_bytes()).hexdigest()

        self.assertEqual(manifest["source_revision"], BASELINE_SOURCE_REVISION)
        self.assertEqual(manifest["semantic_golden"]["sha256"], digest)
        self.assertEqual(manifest["semantic_golden"]["seed"], None)
        self.assertEqual(manifest["stress_baseline"]["seed"], 20260712)
        self.assertEqual(manifest["freeze_validation"]["baseline_test_count"], 4)
        self.assertEqual(
            manifest["freeze_validation"][
                "suite_test_count_without_research_artifact_tests"
            ],
            29,
        )
        self.assertEqual(
            manifest["freeze_validation"]["current_suite_test_count_at_capture"],
            32,
        )


if __name__ == "__main__":
    unittest.main()
