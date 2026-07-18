from __future__ import annotations

import math
import unittest

from dynamics.s0.core import IMMEDIATE_ACTIONS, LONG_HORIZON_REGIONS, PROBABILITY_SCALE, S0ValidationError
from dynamics.s0.scoring import (
    branch_occupancy_absolute_error,
    expected_calibration_error,
    multiclass_brier,
    negative_log_loss,
    paired_bootstrap_mean_difference,
    score_prediction_documents,
)


def distribution(categories: tuple[str, ...], chosen: str, confidence: int = 800_000) -> dict[str, int]:
    remainder = PROBABILITY_SCALE - confidence
    others = [item for item in categories if item != chosen]
    base = remainder // len(others)
    result = {item: base for item in others}
    result[chosen] = confidence
    result[others[0]] += PROBABILITY_SCALE - sum(result.values())
    return {item: result[item] for item in categories}


class S0ScoringTests(unittest.TestCase):
    def test_perfecter_predictions_improve_nll_and_brier(self) -> None:
        labels = ["ASSERT_BOUNDARY", "REPAIR_ATTEMPT"]
        strong = [distribution(IMMEDIATE_ACTIONS, label, 900_000) for label in labels]
        weak = [distribution(IMMEDIATE_ACTIONS, label, 300_000) for label in labels]
        self.assertLess(negative_log_loss(strong, labels, IMMEDIATE_ACTIONS), negative_log_loss(weak, labels, IMMEDIATE_ACTIONS))
        self.assertLess(multiclass_brier(strong, labels, IMMEDIATE_ACTIONS), multiclass_brier(weak, labels, IMMEDIATE_ACTIONS))

    def test_ece_and_occupancy_are_bounded(self) -> None:
        labels = ["PARTIAL_REPAIR", "RELATION_EXIT", "PARTIAL_REPAIR"]
        predictions = [distribution(LONG_HORIZON_REGIONS, label, 700_000) for label in labels]
        ece = expected_calibration_error(predictions, labels, LONG_HORIZON_REGIONS)
        occupancy = branch_occupancy_absolute_error(predictions, labels)
        self.assertGreaterEqual(ece, 0.0); self.assertLessEqual(ece, 1.0)
        self.assertGreaterEqual(occupancy, 0.0); self.assertLessEqual(occupancy, 1.0)

    def test_detached_score_report_contains_preregistered_metrics(self) -> None:
        predictions = [{
            "immediate_action_distribution": distribution(IMMEDIATE_ACTIONS, "ASSERT_BOUNDARY"),
            "long_horizon_region_distribution": distribution(LONG_HORIZON_REGIONS, "CONFLICT_LOOP"),
        }]
        targets = [{"immediate_action": "ASSERT_BOUNDARY", "long_horizon_region": "CONFLICT_LOOP"}]
        report = score_prediction_documents(predictions, targets)
        self.assertEqual(set(report), {
            "immediate_nll", "long_horizon_nll", "immediate_brier", "long_horizon_brier",
            "immediate_ece_10", "long_horizon_ece_10", "branch_occupancy_absolute_error",
        })
        self.assertTrue(all(math.isfinite(value) for value in report.values()))

    def test_paired_bootstrap_is_deterministic_and_directional(self) -> None:
        b2 = [0.8, 0.9, 1.0, 0.7, 0.85]
        h = [0.5, 0.6, 0.7, 0.4, 0.55]
        first = paired_bootstrap_mean_difference(b2, h, seed=17, resamples=500)
        second = paired_bootstrap_mean_difference(b2, h, seed=17, resamples=500)
        self.assertEqual(first, second)
        self.assertGreater(first["mean"], 0.0)
        self.assertGreater(first["lower_95"], 0.0)

    def test_invalid_probability_sum_fails_closed(self) -> None:
        invalid = distribution(IMMEDIATE_ACTIONS, "ASSERT_BOUNDARY")
        invalid["ASSERT_BOUNDARY"] -= 1
        with self.assertRaises(S0ValidationError):
            negative_log_loss([invalid], ["ASSERT_BOUNDARY"], IMMEDIATE_ACTIONS)


if __name__ == "__main__":
    unittest.main()
