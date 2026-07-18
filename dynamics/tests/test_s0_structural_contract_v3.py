from __future__ import annotations

import unittest

from dynamics.s0.structural_contract_v3 import (
    gross_insensitivity_failure,
    matched_intervention_total_variation,
    same_category_universal_mass,
)


class StructuralContractV3Tests(unittest.TestCase):
    def test_different_dominant_categories_are_not_universal_same_category_collapse(self) -> None:
        category, mass = same_category_universal_mass(
            {
                "A": {"X": 990_000, "Y": 10_000},
                "B": {"X": 10_000, "Y": 990_000},
            }
        )
        self.assertIn(category, {"X", "Y"})
        self.assertEqual(mass, 0.01)

    def test_same_dominant_category_is_detected(self) -> None:
        category, mass = same_category_universal_mass(
            {
                "A": {"X": 990_000, "Y": 10_000},
                "B": {"X": 985_000, "Y": 15_000},
            }
        )
        self.assertEqual(category, "X")
        self.assertEqual(mass, 0.985)

    def test_only_registered_pairs_count_for_responsiveness(self) -> None:
        points = {
            "history_stable": {"X": 500_000, "Y": 500_000},
            "history_breach": {"X": 520_000, "Y": 480_000},
            "unregistered_outlier": {"X": 990_000, "Y": 10_000},
        }
        matched = matched_intervention_total_variation(
            points,
            {"history": ("history_stable", "history_breach")},
        )
        self.assertAlmostEqual(matched["history"], 0.02)
        self.assertTrue(gross_insensitivity_failure(matched, minimum_registered_pair_tv=0.05))


if __name__ == "__main__":
    unittest.main()
