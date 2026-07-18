from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from dynamics.s0.source_common_v3 import FAMILY_ID, canonical_bytes
from dynamics.s0.source_family_v2 import generate_instance, validate_intrinsic_candidate

ROOT = Path(__file__).resolve().parents[2]
HYPERPRIOR = json.loads(
    (ROOT / "research/benchmarks/sources/sim-rel-boundary-family-002-hyperprior.json").read_text()
)


class SourceFamilyV2Tests(unittest.TestCase):
    def test_generation_is_byte_stable(self) -> None:
        seed = hashlib.sha256(b"family-v2-stable").hexdigest()
        left = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=3)
        right = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=3)
        self.assertEqual(canonical_bytes(left), canonical_bytes(right))

    def test_instances_are_independent_draws(self) -> None:
        seed = hashlib.sha256(b"family-v2-independent").hexdigest()
        left = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=0)
        right = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=1)
        self.assertNotEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(left["family_id"], FAMILY_ID)
        self.assertEqual(right["family_id"], FAMILY_ID)

    def test_generated_instance_passes_source_only_acceptance(self) -> None:
        seed = hashlib.sha256(b"family-v2-adequate").hexdigest()
        instance = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=0)
        self.assertEqual(validate_intrinsic_candidate(instance, HYPERPRIOR), [])
        metrics = instance["generation_receipt"]["process_adequacy"]
        self.assertGreaterEqual(
            metrics["p2_immediate_predictive_memory_gain_nats"],
            HYPERPRIOR["process_adequacy"]["minimum_p2_immediate_predictive_memory_gain_nats"],
        )
        self.assertFalse(instance["generation_receipt"]["model_outputs_or_scores_read"])

    def test_feedback_emission_is_action_conditioned(self) -> None:
        seed = hashlib.sha256(b"family-v2-feedback").hexdigest()
        instance = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=0)
        feedback = instance["emission_parameters"]["action_conditioned_feedback"]
        matrices = {canonical_bytes(value) for value in feedback.values()}
        self.assertGreater(len(matrices), 1)

    def test_hyperprior_forbids_model_performance_acceptance(self) -> None:
        forbidden = set(HYPERPRIOR["forbidden_acceptance_inputs"])
        self.assertIn("model_output", forbidden)
        self.assertIn("model_score", forbidden)
        self.assertIn("B2_MINUS_H_NLL", forbidden)
        self.assertEqual(HYPERPRIOR["instance_relation"], "INDEPENDENT_DRAWS_FROM_COMMON_PUBLIC_HYPERPRIOR")


if __name__ == "__main__":
    unittest.main()
