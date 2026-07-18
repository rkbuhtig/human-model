from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

PROBABILITY_SCALE = 1_000_000
THREAT_ACTIONS = (
    "ASSERT_BOUNDARY",
    "TEMPORARY_WITHDRAWAL",
    "PUNITIVE_ATTACK",
    "RELATION_EXIT",
)
HEALTHY_REGIONS = ("PARTIAL_REPAIR", "GUARDED_CONTINUATION")


class StructuralPredicateError(ValueError):
    pass


def _probability_mass(distribution: Mapping[str, int], categories: Sequence[str]) -> int:
    if any(category not in distribution for category in categories):
        raise StructuralPredicateError("distribution is missing a registered category")
    if sum(distribution.values()) != PROBABILITY_SCALE:
        raise StructuralPredicateError("distribution must sum to probability scale")
    return sum(distribution[category] for category in categories)


def _total_variation(left: Mapping[str, int], right: Mapping[str, int]) -> float:
    if set(left) != set(right):
        raise StructuralPredicateError("total variation requires identical categories")
    return sum(abs(left[key] - right[key]) for key in left) / (2 * PROBABILITY_SCALE)


@dataclass(frozen=True)
class StructuralPoint:
    case_id: str
    match_id: str
    history_condition: str
    continuation_condition: str
    context_variant: str
    immediate_action_distribution: Mapping[str, int]
    long_horizon_region_distribution: Mapping[str, int]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "StructuralPoint":
        required = {
            "case_id",
            "match_id",
            "history_condition",
            "continuation_condition",
            "context_variant",
            "immediate_action_distribution",
            "long_horizon_region_distribution",
        }
        if set(value) != required:
            raise StructuralPredicateError("structural point keys do not match contract")
        return cls(**value)  # type: ignore[arg-type]


def _pairs(points: Iterable[StructuralPoint], field: str, left: str, right: str):
    grouped: dict[str, dict[str, StructuralPoint]] = defaultdict(dict)
    for point in points:
        grouped[point.match_id][getattr(point, field)] = point
    for match_id, group in sorted(grouped.items()):
        if left not in group or right not in group:
            raise StructuralPredicateError(
                f"matched pair {match_id} lacks {field} values {left}/{right}"
            )
        yield match_id, group[left], group[right]


def evaluate_history_sensitivity(points: Sequence[StructuralPoint]) -> dict[str, Any]:
    failures = []
    margins = []
    for match_id, stable, breach in _pairs(
        points, "history_condition", "H-STABLE", "H-BREACH"
    ):
        stable_mass = _probability_mass(stable.immediate_action_distribution, THREAT_ACTIONS)
        breach_mass = _probability_mass(breach.immediate_action_distribution, THREAT_ACTIONS)
        margin = breach_mass - stable_mass
        margins.append(margin)
        if margin < 0:
            failures.append({"match_id": match_id, "margin_units": margin})
    return {
        "predicate_id": "A-C1-HISTORY-SENSITIVITY-V2",
        "passed": not failures,
        "minimum_margin_units": min(margins) if margins else None,
        "failures": failures,
    }


def evaluate_repair_discrimination(points: Sequence[StructuralPoint]) -> dict[str, Any]:
    failures = []
    margins = []
    for match_id, repair, deflect in _pairs(
        points, "continuation_condition", "F-REPAIR", "F-DEFLECT"
    ):
        repair_mass = _probability_mass(repair.long_horizon_region_distribution, HEALTHY_REGIONS)
        deflect_mass = _probability_mass(deflect.long_horizon_region_distribution, HEALTHY_REGIONS)
        margin = repair_mass - deflect_mass
        margins.append(margin)
        if margin <= 0:
            failures.append({"match_id": match_id, "margin_units": margin})
    return {
        "predicate_id": "A-C2-REPAIR-DISCRIMINATION-V2",
        "passed": not failures,
        "minimum_margin_units": min(margins) if margins else None,
        "failures": failures,
    }


def evaluate_repetition_sensitivity(points: Sequence[StructuralPoint]) -> dict[str, Any]:
    failures = []
    margins = []
    for match_id, no_repeat, repeated in _pairs(
        points, "context_variant", "MATCHED_NO_REPEAT", "MATCHED_REPEAT"
    ):
        margin = (
            no_repeat.long_horizon_region_distribution["PARTIAL_REPAIR"]
            - repeated.long_horizon_region_distribution["PARTIAL_REPAIR"]
        )
        margins.append(margin)
        if margin < 0:
            failures.append({"match_id": match_id, "margin_units": margin})
    return {
        "predicate_id": "A-C3-REPETITION-SENSITIVITY-V2",
        "passed": not failures,
        "minimum_margin_units": min(margins) if margins else None,
        "failures": failures,
    }


def evaluate_projection_selectivity(points: Sequence[StructuralPoint]) -> dict[str, Any]:
    failures = []
    margins = []
    for match_id, private, public in _pairs(
        points, "context_variant", "PRIVATE_MATCH", "PUBLIC_MATCH"
    ):
        margin = (
            public.immediate_action_distribution["SUPPRESS_FOR_ROLE"]
            - private.immediate_action_distribution["SUPPRESS_FOR_ROLE"]
        )
        margins.append(margin)
        if margin < 0:
            failures.append({"match_id": match_id, "margin_units": margin})
    return {
        "predicate_id": "A-C4-PROJECTION-SELECTIVITY-V2",
        "passed": not failures,
        "minimum_margin_units": min(margins) if margins else None,
        "failures": failures,
    }


def evaluate_local_variation(
    points: Sequence[StructuralPoint], *, maximum_universal_category_probability: float = 0.98,
    minimum_intervention_total_variation: float = 0.05,
) -> dict[str, Any]:
    if not points:
        raise StructuralPredicateError("local variation requires points")
    universal_max = min(
        max(point.immediate_action_distribution.values()) / PROBABILITY_SCALE
        for point in points
    )
    pairwise_tv = []
    for index, left in enumerate(points):
        for right in points[index + 1 :]:
            pairwise_tv.append(
                _total_variation(
                    left.immediate_action_distribution,
                    right.immediate_action_distribution,
                )
            )
    maximum_tv = max(pairwise_tv, default=0.0)
    failures = []
    if universal_max > maximum_universal_category_probability:
        failures.append("UNIVERSAL_MODE_COLLAPSE")
    if maximum_tv < minimum_intervention_total_variation:
        failures.append("INTERVENTION_INSENSITIVITY")
    return {
        "predicate_id": "A-C5-LOCAL-VARIATION-V2",
        "passed": not failures,
        "minimum_pointwise_max_probability": universal_max,
        "maximum_pairwise_total_variation": maximum_tv,
        "failures": failures,
    }
