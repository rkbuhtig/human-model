from __future__ import annotations

from copy import deepcopy
import random
import unittest

from dynamics.s0.v2_core import IMMEDIATE_ACTIONS, LONG_HORIZON_REGIONS, PREDICTION_SCHEMA_VERSION, S0V2Error
from dynamics.s0.v2_scoring import hierarchical_paired_bootstrap, score_documents


def uniform(categories):
    base = 1_000_000 // len(categories)
    result = {category: base for category in categories}
    result[categories[0]] += 1_000_000 - sum(result.values())
    return result


def prediction(instance, trajectory, step, point="p0"):
    return {
        "schema_version": PREDICTION_SCHEMA_VERSION,
        "model_id": "B2",
        "key": {"source_instance_id": instance, "trajectory_id": trajectory, "step_ordinal": step, "prediction_point_id": point},
        "immediate_action_distribution": uniform(IMMEDIATE_ACTIONS),
        "long_horizon_region_distribution": uniform(LONG_HORIZON_REGIONS),
    }


def target(instance, trajectory, step, point="p0"):
    return {
        "key": {"source_instance_id": instance, "trajectory_id": trajectory, "step_ordinal": step, "prediction_point_id": point},
        "immediate_action": IMMEDIATE_ACTIONS[0],
        "long_horizon_region": LONG_HORIZON_REGIONS[0],
    }


class V2ScoringTests(unittest.TestCase):
    def test_permutation_invariant_identity_join(self):
        predictions = [prediction("I0", "T0", 1), prediction("I0", "T1", 1), prediction("I1", "T2", 1)]
        targets = [target("I0", "T0", 1), target("I0", "T1", 1), target("I1", "T2", 1)]
        expected = score_documents(predictions, targets)
        random.Random(3).shuffle(predictions); random.Random(9).shuffle(targets)
        self.assertEqual(expected, score_documents(predictions, targets))

    def test_duplicate_and_key_set_mismatch_fail(self):
        p = prediction("I0", "T0", 1); t = target("I0", "T0", 1)
        with self.assertRaises(S0V2Error):
            score_documents([p, deepcopy(p)], [t, target("I0", "T1", 1)])
        with self.assertRaises(S0V2Error):
            score_documents([p], [target("I0", "OTHER", 1)])

    def test_trajectory_aggregation(self):
        predictions = [prediction("I0", "T0", 1, "a"), prediction("I0", "T0", 2, "b")]
        targets = [target("I0", "T0", 1, "a"), target("I0", "T0", 2, "b")]
        scored = score_documents(predictions, targets)
        self.assertEqual(scored["pooled"]["trajectory_count"], 1)
        self.assertEqual(scored["trajectory_losses"][0]["prediction_points"], 2)

    def test_hierarchical_bootstrap_is_deterministic(self):
        left, right = [], []
        for instance in ("I0", "I1"):
            for index in range(3):
                left.append({"source_instance_id": instance, "trajectory_id": f"T{index}", "immediate_nll": 1.0 + index, "long_horizon_nll": 2.0})
                right.append({"source_instance_id": instance, "trajectory_id": f"T{index}", "immediate_nll": 0.5 + index, "long_horizon_nll": 1.5})
        a = hierarchical_paired_bootstrap(left, right, "immediate_nll", seed=7, resamples=200)
        b = hierarchical_paired_bootstrap(left, right, "immediate_nll", seed=7, resamples=200)
        self.assertEqual(a, b)
        self.assertAlmostEqual(a["mean"], 0.5)

    def test_pooled_proper_metrics_present_and_bounded(self):
        predictions = [prediction("I0", "T0", 1), prediction("I1", "T1", 1)]
        targets = [target("I0", "T0", 1), target("I1", "T1", 1)]
        pooled = score_documents(predictions, targets)["pooled"]
        for key in ("immediate_brier", "long_horizon_brier", "immediate_ece_10", "long_horizon_ece_10", "branch_occupancy_absolute_error"):
            self.assertIn(key, pooled)
            self.assertGreaterEqual(pooled[key], 0.0)
        self.assertLessEqual(pooled["branch_occupancy_absolute_error"], 1.0)


if __name__ == "__main__":
    unittest.main()
