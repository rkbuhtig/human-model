from __future__ import annotations

from typing import Mapping, Sequence

from .source_common_v3 import PROBABILITY_SCALE, SourceProcessError, total_variation


def same_category_universal_mass(
    points: Mapping[str, Mapping[str, int]],
) -> tuple[str, float]:
    if not points:
        raise SourceProcessError("at least one structural point is required")
    categories = set(next(iter(points.values())))
    if not categories:
        raise SourceProcessError("structural distributions must be non-empty")
    for point_id, distribution in points.items():
        if set(distribution) != categories:
            raise SourceProcessError(f"category mismatch at {point_id}")
        if min(distribution.values()) < 0 or sum(distribution.values()) != PROBABILITY_SCALE:
            raise SourceProcessError(f"invalid distribution at {point_id}")
    category, units = max(
        (
            (category, min(distribution[category] for distribution in points.values()))
            for category in categories
        ),
        key=lambda item: (item[1], item[0]),
    )
    return category, units / PROBABILITY_SCALE


def matched_intervention_total_variation(
    points: Mapping[str, Mapping[str, int]],
    pairs: Mapping[str, Sequence[str]],
) -> dict[str, float]:
    results: dict[str, float] = {}
    for pair_id, pair in pairs.items():
        if len(pair) != 2:
            raise SourceProcessError(f"matched pair {pair_id} must contain exactly two point IDs")
        left_id, right_id = pair
        if left_id not in points or right_id not in points:
            raise SourceProcessError(f"matched pair {pair_id} references an unknown point")
        left = points[left_id]
        right = points[right_id]
        if set(left) != set(right):
            raise SourceProcessError(f"matched pair {pair_id} category mismatch")
        categories = sorted(left)
        results[pair_id] = total_variation(
            [left[category] for category in categories],
            [right[category] for category in categories],
        )
    return results


def gross_insensitivity_failure(
    matched_tv: Mapping[str, float], *, minimum_registered_pair_tv: float
) -> bool:
    if not matched_tv:
        raise SourceProcessError("registered matched-pair results are required")
    return max(matched_tv.values()) < minimum_registered_pair_tv
