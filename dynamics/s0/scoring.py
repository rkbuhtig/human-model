from __future__ import annotations

import math
import random
from typing import Any, Mapping, Sequence

from .core import (
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    PROBABILITY_SCALE,
    S0ValidationError,
    normalize_probability_units,
)


def _probability(distribution: Mapping[str, int], label: str, categories: tuple[str, ...]) -> float:
    normalized = normalize_probability_units(distribution, categories)
    if label not in normalized:
        raise S0ValidationError(f"target label outside vocabulary: {label}")
    return max(normalized[label] / PROBABILITY_SCALE, 1.0 / PROBABILITY_SCALE)


def negative_log_loss(
    distributions: Sequence[Mapping[str, int]],
    labels: Sequence[str],
    categories: tuple[str, ...],
) -> float:
    if len(distributions) != len(labels) or not labels:
        raise S0ValidationError("NLL requires equal non-empty predictions and labels")
    return sum(-math.log(_probability(dist, label, categories)) for dist, label in zip(distributions, labels)) / len(labels)


def multiclass_brier(
    distributions: Sequence[Mapping[str, int]],
    labels: Sequence[str],
    categories: tuple[str, ...],
) -> float:
    if len(distributions) != len(labels) or not labels:
        raise S0ValidationError("Brier requires equal non-empty predictions and labels")
    total = 0.0
    for distribution, label in zip(distributions, labels):
        normalized = normalize_probability_units(distribution, categories)
        for category in categories:
            probability = normalized[category] / PROBABILITY_SCALE
            target = 1.0 if category == label else 0.0
            total += (probability - target) ** 2
    return total / len(labels)


def expected_calibration_error(
    distributions: Sequence[Mapping[str, int]],
    labels: Sequence[str],
    categories: tuple[str, ...],
    *,
    bins: int = 10,
) -> float:
    if bins <= 0:
        raise S0ValidationError("ECE bins must be positive")
    if len(distributions) != len(labels) or not labels:
        raise S0ValidationError("ECE requires equal non-empty predictions and labels")
    buckets: list[list[tuple[float, float]]] = [[] for _ in range(bins)]
    for distribution, label in zip(distributions, labels):
        normalized = normalize_probability_units(distribution, categories)
        predicted = max(categories, key=lambda category: (normalized[category], -categories.index(category)))
        confidence = normalized[predicted] / PROBABILITY_SCALE
        index = min(bins - 1, int(confidence * bins))
        buckets[index].append((confidence, 1.0 if predicted == label else 0.0))
    total = len(labels)
    error = 0.0
    for bucket in buckets:
        if not bucket:
            continue
        confidence = sum(item[0] for item in bucket) / len(bucket)
        accuracy = sum(item[1] for item in bucket) / len(bucket)
        error += len(bucket) / total * abs(confidence - accuracy)
    return error


def branch_occupancy_absolute_error(
    distributions: Sequence[Mapping[str, int]],
    labels: Sequence[str],
    categories: tuple[str, ...] = LONG_HORIZON_REGIONS,
) -> float:
    if len(distributions) != len(labels) or not labels:
        raise S0ValidationError("occupancy error requires equal non-empty inputs")
    predicted = {category: 0.0 for category in categories}
    observed = {category: 0 for category in categories}
    for distribution, label in zip(distributions, labels):
        normalized = normalize_probability_units(distribution, categories)
        for category in categories:
            predicted[category] += normalized[category] / PROBABILITY_SCALE
        observed[label] += 1
    size = len(labels)
    return sum(abs(predicted[category] / size - observed[category] / size) for category in categories) / 2


def score_prediction_documents(
    predictions: Sequence[Mapping[str, Any]], targets: Sequence[Mapping[str, str]]
) -> dict[str, float]:
    if len(predictions) != len(targets) or not predictions:
        raise S0ValidationError("scoring requires equal non-empty prediction/target lists")
    immediate_distributions = [item["immediate_action_distribution"] for item in predictions]
    horizon_distributions = [item["long_horizon_region_distribution"] for item in predictions]
    immediate_labels = [item["immediate_action"] for item in targets]
    horizon_labels = [item["long_horizon_region"] for item in targets]
    return {
        "immediate_nll": negative_log_loss(immediate_distributions, immediate_labels, IMMEDIATE_ACTIONS),
        "long_horizon_nll": negative_log_loss(horizon_distributions, horizon_labels, LONG_HORIZON_REGIONS),
        "immediate_brier": multiclass_brier(immediate_distributions, immediate_labels, IMMEDIATE_ACTIONS),
        "long_horizon_brier": multiclass_brier(horizon_distributions, horizon_labels, LONG_HORIZON_REGIONS),
        "immediate_ece_10": expected_calibration_error(immediate_distributions, immediate_labels, IMMEDIATE_ACTIONS),
        "long_horizon_ece_10": expected_calibration_error(horizon_distributions, horizon_labels, LONG_HORIZON_REGIONS),
        "branch_occupancy_absolute_error": branch_occupancy_absolute_error(horizon_distributions, horizon_labels),
    }


def paired_bootstrap_mean_difference(
    left_losses: Sequence[float],
    right_losses: Sequence[float],
    *,
    seed: int,
    resamples: int = 2000,
) -> dict[str, float]:
    if len(left_losses) != len(right_losses) or not left_losses:
        raise S0ValidationError("paired bootstrap requires equal non-empty loss vectors")
    if resamples <= 0:
        raise S0ValidationError("bootstrap resamples must be positive")
    differences = [left - right for left, right in zip(left_losses, right_losses)]
    randomizer = random.Random(seed)
    size = len(differences)
    sampled_means = []
    for _ in range(resamples):
        sampled_means.append(sum(differences[randomizer.randrange(size)] for _ in range(size)) / size)
    sampled_means.sort()
    lower_index = max(0, int(0.025 * resamples) - 1)
    upper_index = min(resamples - 1, int(0.975 * resamples))
    return {
        "mean": sum(differences) / size,
        "lower_95": sampled_means[lower_index],
        "upper_95": sampled_means[upper_index],
    }
