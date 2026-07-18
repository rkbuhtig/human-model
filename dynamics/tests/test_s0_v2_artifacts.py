from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "research" / "benchmarks" / "models" / "s0"


class V2ArtifactTests(unittest.TestCase):
    def test_artifacts_parse_and_versions_align(self):
        cards = json.loads((ARTIFACT / "model-cards-v2.json").read_text())
        parameters = json.loads((ARTIFACT / "initial-parameters-v2.json").read_text())
        kernel = json.loads((ARTIFACT / "h-state-kernel-v2.json").read_text())
        compatibility = json.loads((ARTIFACT / "receipt-compatibility-v2.json").read_text())
        self.assertEqual(cards["freeze_id"], "HUMAN-DYN-ADEQ-S0-MODEL-FREEZE-INITIAL-002")
        self.assertFalse(cards["source_eligibility"]["INITIAL-001"])
        self.assertTrue(cards["source_eligibility"]["INITIAL-002"])
        self.assertEqual({item["model_id"]: item["model_version"] for item in cards["models"]}, {key: value["model_version"] for key, value in parameters["models"].items()})
        self.assertEqual(kernel["state_version"], "s0-h-incremental-2")
        self.assertEqual(kernel["online_state_contract"]["source_instance"], "EXACT_MATCH")
        self.assertEqual(compatibility["validation_stage"], "PARSE_BEFORE_TRANSITION")

    def test_no_source_materialization_artifact(self):
        cards = json.loads((ARTIFACT / "model-cards-v2.json").read_text())
        self.assertIn("SOURCE_SEED", cards["explicit_absences"])
        self.assertIn("SOURCE_INSTANCE", cards["explicit_absences"])
        self.assertIn("SCORE", cards["explicit_absences"])


if __name__ == "__main__":
    unittest.main()
