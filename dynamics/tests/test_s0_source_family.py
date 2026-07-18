from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest

from dynamics.s0.source_family import (
    GENERATOR_VERSION,
    SourceFamilyError,
    derive_family_seed,
    family_manifest,
    generate_family,
    generate_instance,
    validate_candidate,
)

ROOT = Path(__file__).resolve().parents[2]
HYPERPRIOR_PATH = (
    ROOT
    / "research"
    / "benchmarks"
    / "sources"
    / "sim-rel-boundary-family-001-hyperprior.json"
)


class SourceFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hyperprior = json.loads(HYPERPRIOR_PATH.read_text(encoding="utf-8"))
        cls.family_seed = derive_family_seed(
            merge_commit_sha="1" * 40,
            generator_blob_sha="2" * 40,
            hyperprior_blob_sha="3" * 40,
            beacon_randomness_hex="4" * 64,
            family_id=cls.hyperprior["family_id"],
        )

    def test_family_seed_is_deterministic_and_artifact_bound(self) -> None:
        same = derive_family_seed(
            merge_commit_sha="1" * 40,
            generator_blob_sha="2" * 40,
            hyperprior_blob_sha="3" * 40,
            beacon_randomness_hex="4" * 64,
            family_id=self.hyperprior["family_id"],
        )
        changed = derive_family_seed(
            merge_commit_sha="1" * 40,
            generator_blob_sha="2" * 40,
            hyperprior_blob_sha="5" * 40,
            beacon_randomness_hex="4" * 64,
            family_id=self.hyperprior["family_id"],
        )
        self.assertEqual(same, self.family_seed)
        self.assertNotEqual(changed, self.family_seed)

    def test_all_frozen_instances_generate_and_pass_intrinsic_acceptance(self) -> None:
        family = generate_family(self.hyperprior, family_seed_hex=self.family_seed)
        self.assertEqual(len(family), self.hyperprior["instance_count"])
        self.assertEqual(len({item["instance_id"] for item in family}), len(family))
        for instance in family:
            self.assertEqual(instance["generator_version"], GENERATOR_VERSION)
            self.assertEqual(validate_candidate(instance, self.hyperprior), [])
            self.assertFalse(instance["generation_receipt"]["model_outputs_or_scores_read"])
            self.assertEqual(
                instance["generation_receipt"]["acceptance_basis"],
                "INTRINSIC_SOURCE_VALIDITY_ONLY",
            )

    def test_generation_is_byte_stable_for_fixed_seed_and_index(self) -> None:
        first = generate_instance(self.hyperprior, family_seed_hex=self.family_seed, instance_index=3)
        second = generate_instance(self.hyperprior, family_seed_hex=self.family_seed, instance_index=3)
        self.assertEqual(first, second)
        other = generate_instance(self.hyperprior, family_seed_hex=self.family_seed, instance_index=4)
        self.assertNotEqual(first, other)

    def test_manifest_includes_every_generated_instance_without_selection(self) -> None:
        family = generate_family(self.hyperprior, family_seed_hex=self.family_seed)
        manifest = family_manifest(family)
        self.assertEqual(manifest["instance_count"], self.hyperprior["instance_count"])
        self.assertEqual(set(manifest["instance_digests"]), {item["instance_id"] for item in family})
        self.assertEqual(manifest["selection_rule"], "ALL_GENERATED_INSTANCES_INCLUDED")
        self.assertFalse(manifest["post_generation_model_based_selection"])

    def test_hyperprior_forbids_model_performance_acceptance(self) -> None:
        forbidden = set(self.hyperprior["forbidden_acceptance_inputs"])
        self.assertTrue(
            {
                "model_id",
                "model_output",
                "model_score",
                "B2_MINUS_H_NLL",
                "leaderboard_result",
            }
            <= forbidden
        )

    def test_generator_imports_no_candidate_model_runner_or_scorer(self) -> None:
        path = ROOT / "dynamics" / "s0" / "source_family.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
        self.assertFalse(any(name.endswith(("models", "runner", "scoring")) for name in imports))

    def test_invalid_seed_material_is_rejected(self) -> None:
        with self.assertRaises(SourceFamilyError):
            derive_family_seed(
                merge_commit_sha="not-a-sha",
                generator_blob_sha="2" * 40,
                hyperprior_blob_sha="3" * 40,
                beacon_randomness_hex="4" * 64,
                family_id=self.hyperprior["family_id"],
            )


if __name__ == "__main__":
    unittest.main()
