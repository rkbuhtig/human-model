from __future__ import annotations

import unittest

from dynamics.s0.structural import (
    StructuralPoint,
    evaluate_history_sensitivity,
    evaluate_local_variation,
    evaluate_projection_selectivity,
    evaluate_repair_discrimination,
    evaluate_repetition_sensitivity,
)

IMMEDIATE_CATEGORIES = (
    "SEEK_CLARIFICATION",
    "EXPRESS_HURT",
    "ASSERT_BOUNDARY",
    "TEMPORARY_WITHDRAWAL",
    "PUNITIVE_ATTACK",
    "SUPPRESS_FOR_ROLE",
    "REPAIR_ATTEMPT",
    "RELATION_EXIT",
)
HORIZON_CATEGORIES = (
    "PARTIAL_REPAIR",
    "GUARDED_CONTINUATION",
    "CONFLICT_LOOP",
    "RELATION_EXIT",
    "UNRESOLVED_DRIFT",
)


def dist(categories, **values):
    result = {category: 0 for category in categories}
    result.update(values)
    remainder = 1_000_000 - sum(result.values())
    zero_categories = [category for category in categories if result[category] == 0]
    share, extra = divmod(remainder, len(zero_categories))
    for index, category in enumerate(zero_categories):
        result[category] = share + (1 if index < extra else 0)
    return result


def point(
    *,
    case_id,
    match_id,
    history="H-STABLE",
    continuation="F-DEFLECT",
    context="BASE",
    threat=200_000,
    suppress=50_000,
    healthy=300_000,
    partial=150_000,
):
    immediate = dist(
        IMMEDIATE_CATEGORIES,
        ASSERT_BOUNDARY=threat // 2,
        TEMPORARY_WITHDRAWAL=threat // 2,
        SUPPRESS_FOR_ROLE=suppress,
    )
    horizon = dist(
        HORIZON_CATEGORIES,
        PARTIAL_REPAIR=partial,
        GUARDED_CONTINUATION=healthy - partial,
    )
    return StructuralPoint(
        case_id=case_id,
        match_id=match_id,
        history_condition=history,
        continuation_condition=continuation,
        context_variant=context,
        immediate_action_distribution=immediate,
        long_horizon_region_distribution=horizon,
    )


class StructuralPredicateTests(unittest.TestCase):
    def test_history_sensitivity_is_exact_and_has_no_undefined_exception(self):
        result = evaluate_history_sensitivity(
            [
                point(case_id="stable", match_id="m", history="H-STABLE", threat=180_000),
                point(case_id="breach", match_id="m", history="H-BREACH", threat=260_000),
            ]
        )
        self.assertTrue(result["passed"])
        self.assertGreater(result["minimum_margin_units"], 0)

    def test_repair_discrimination_uses_registered_healthy_region_mass(self):
        result = evaluate_repair_discrimination(
            [
                point(case_id="repair", match_id="m", continuation="F-REPAIR", healthy=600_000),
                point(case_id="deflect", match_id="m", continuation="F-DEFLECT", healthy=250_000),
            ]
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["minimum_margin_units"], 350_000)

    def test_repetition_and_projection_use_explicit_matched_context_roles(self):
        repeated = evaluate_repetition_sensitivity(
            [
                point(case_id="base", match_id="r", context="MATCHED_NO_REPEAT", partial=300_000),
                point(case_id="repeat", match_id="r", context="MATCHED_REPEAT", partial=100_000),
            ]
        )
        projection = evaluate_projection_selectivity(
            [
                point(case_id="private", match_id="p", context="PRIVATE_MATCH", suppress=50_000),
                point(case_id="public", match_id="p", context="PUBLIC_MATCH", suppress=220_000),
            ]
        )
        self.assertTrue(repeated["passed"])
        self.assertTrue(projection["passed"])

    def test_local_variation_detects_intervention_insensitivity(self):
        same = point(case_id="a", match_id="a")
        duplicate = point(case_id="b", match_id="b")
        result = evaluate_local_variation([same, duplicate])
        self.assertFalse(result["passed"])
        self.assertIn("INTERVENTION_INSENSITIVITY", result["failures"])


if __name__ == "__main__":
    unittest.main()
