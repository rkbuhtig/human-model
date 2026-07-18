from __future__ import annotations

from collections import defaultdict
import math
import random
from typing import Any, Mapping, Sequence

from .v2_core import IMMEDIATE_ACTIONS, LONG_HORIZON_REGIONS, PredictionKey, PROBABILITY_SCALE, S0V2Error


def key_tuple(value: Mapping[str, Any]) -> tuple[str, str, int, str]:
    key = PredictionKey.from_dict(value["key"])
    return (key.source_instance_id, key.trajectory_id, key.step_ordinal, key.prediction_point_id)


def index_unique(documents: Sequence[Mapping[str, Any]], kind: str) -> dict[tuple[str, str, int, str], Mapping[str, Any]]:
    result = {}
    for document in documents:
        key = key_tuple(document)
        if key in result:
            raise S0V2Error(f"duplicate {kind} key: {key}")
        result[key] = document
    return result


def join_predictions_targets(predictions: Sequence[Mapping[str, Any]], targets: Sequence[Mapping[str, Any]]) -> list[tuple[Mapping[str, Any], Mapping[str, Any]]]:
    prediction_map = index_unique(predictions, "prediction")
    target_map = index_unique(targets, "target")
    if set(prediction_map) != set(target_map):
        missing_targets = sorted(set(prediction_map) - set(target_map))
        missing_predictions = sorted(set(target_map) - set(prediction_map))
        raise S0V2Error(f"key-set mismatch missing_targets={missing_targets} missing_predictions={missing_predictions}")
    return [(prediction_map[key], target_map[key]) for key in sorted(prediction_map)]


def probability(distribution: Mapping[str, int], label: str, categories: tuple[str, ...]) -> float:
    if set(distribution) != set(categories) or sum(distribution.values()) != PROBABILITY_SCALE:
        raise S0V2Error("invalid distribution")
    if label not in categories:
        raise S0V2Error("label outside vocabulary")
    return max(distribution[label] / PROBABILITY_SCALE, 1.0 / PROBABILITY_SCALE)


def point_losses(predictions: Sequence[Mapping[str, Any]], targets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for prediction, target in join_predictions_targets(predictions, targets):
        result.append({
            "key": prediction["key"],
            "immediate_nll": -math.log(probability(prediction["immediate_action_distribution"], target["immediate_action"], IMMEDIATE_ACTIONS)),
            "long_horizon_nll": -math.log(probability(prediction["long_horizon_region_distribution"], target["long_horizon_region"], LONG_HORIZON_REGIONS)),
        })
    return result


def aggregate_trajectory_losses(losses: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for item in losses:
        key = PredictionKey.from_dict(item["key"])
        grouped[(key.source_instance_id, key.trajectory_id)].append(item)
    result = []
    for (instance_id, trajectory_id), rows in sorted(grouped.items()):
        result.append({
            "source_instance_id": instance_id,
            "trajectory_id": trajectory_id,
            "immediate_nll": sum(row["immediate_nll"] for row in rows) / len(rows),
            "long_horizon_nll": sum(row["long_horizon_nll"] for row in rows) / len(rows),
            "prediction_points": len(rows),
        })
    return result


def multiclass_brier(distribution: Mapping[str, int], label: str, categories: tuple[str, ...]) -> float:
    probability(distribution, label, categories)
    return sum(((distribution[category] / PROBABILITY_SCALE) - (1.0 if category == label else 0.0)) ** 2 for category in categories)


def expected_calibration_error(rows: Sequence[tuple[Mapping[str, int], str]], categories: tuple[str, ...], bins: int = 10) -> float:
    if bins <= 0 or not rows:
        raise S0V2Error("ECE requires positive bins and rows")
    buckets: list[list[tuple[float, float]]] = [[] for _ in range(bins)]
    for distribution, label in rows:
        probability(distribution, label, categories)
        predicted = max(categories, key=lambda item: (distribution[item], -categories.index(item)))
        confidence = distribution[predicted] / PROBABILITY_SCALE
        bucket = min(bins - 1, int(confidence * bins))
        buckets[bucket].append((confidence, 1.0 if predicted == label else 0.0))
    total = len(rows)
    return sum(
        len(bucket) / total * abs(
            sum(item[0] for item in bucket) / len(bucket) - sum(item[1] for item in bucket) / len(bucket)
        )
        for bucket in buckets if bucket
    )


def branch_occupancy_absolute_error(rows: Sequence[tuple[Mapping[str, int], str]]) -> float:
    if not rows:
        raise S0V2Error("occupancy requires rows")
    predicted = {category: 0.0 for category in LONG_HORIZON_REGIONS}
    observed = {category: 0 for category in LONG_HORIZON_REGIONS}
    for distribution, label in rows:
        probability(distribution, label, LONG_HORIZON_REGIONS)
        for category in LONG_HORIZON_REGIONS:
            predicted[category] += distribution[category] / PROBABILITY_SCALE
        observed[label] += 1
    count = len(rows)
    return sum(abs(predicted[category] / count - observed[category] / count) for category in LONG_HORIZON_REGIONS) / 2


def score_documents(predictions: Sequence[Mapping[str, Any]], targets: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    joined = join_predictions_targets(predictions, targets)
    trajectories = aggregate_trajectory_losses(point_losses(predictions, targets))
    immediate_rows = [(prediction["immediate_action_distribution"], target["immediate_action"]) for prediction, target in joined]
    horizon_rows = [(prediction["long_horizon_region_distribution"], target["long_horizon_region"]) for prediction, target in joined]
    per_instance: dict[str, dict[str, float]] = {}
    by_instance: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in trajectories:
        by_instance[row["source_instance_id"]].append(row)
    for instance, rows in sorted(by_instance.items()):
        per_instance[instance] = {
            "trajectory_count": len(rows),
            "immediate_nll": sum(row["immediate_nll"] for row in rows) / len(rows),
            "long_horizon_nll": sum(row["long_horizon_nll"] for row in rows) / len(rows),
        }
    return {
        "trajectory_losses": trajectories,
        "per_instance": per_instance,
        "pooled": {
            "trajectory_count": len(trajectories),
            "immediate_nll": sum(row["immediate_nll"] for row in trajectories) / len(trajectories),
            "long_horizon_nll": sum(row["long_horizon_nll"] for row in trajectories) / len(trajectories),
            "immediate_brier": sum(multiclass_brier(distribution, label, IMMEDIATE_ACTIONS) for distribution, label in immediate_rows) / len(immediate_rows),
            "long_horizon_brier": sum(multiclass_brier(distribution, label, LONG_HORIZON_REGIONS) for distribution, label in horizon_rows) / len(horizon_rows),
            "immediate_ece_10": expected_calibration_error(immediate_rows, IMMEDIATE_ACTIONS, 10),
            "long_horizon_ece_10": expected_calibration_error(horizon_rows, LONG_HORIZON_REGIONS, 10),
            "branch_occupancy_absolute_error": branch_occupancy_absolute_error(horizon_rows),
        },
    }


def hierarchical_paired_bootstrap(left: Sequence[Mapping[str, Any]], right: Sequence[Mapping[str, Any]], metric: str, *, seed: int, resamples: int = 2000) -> dict[str, float]:
    left_map = {(row["source_instance_id"], row["trajectory_id"]): row for row in left}
    right_map = {(row["source_instance_id"], row["trajectory_id"]): row for row in right}
    if set(left_map) != set(right_map) or not left_map:
        raise S0V2Error("paired trajectory key mismatch")
    instances: dict[str, list[str]] = defaultdict(list)
    for instance_id, trajectory_id in left_map:
        instances[instance_id].append(trajectory_id)
    instance_ids = sorted(instances)
    rng = random.Random(seed)
    sampled_means = []
    for _ in range(resamples):
        sampled_diffs = []
        for _instance_draw in range(len(instance_ids)):
            instance_id = instance_ids[rng.randrange(len(instance_ids))]
            trajectory_ids = sorted(instances[instance_id])
            for _trajectory_draw in range(len(trajectory_ids)):
                trajectory_id = trajectory_ids[rng.randrange(len(trajectory_ids))]
                key = (instance_id, trajectory_id)
                sampled_diffs.append(left_map[key][metric] - right_map[key][metric])
        sampled_means.append(sum(sampled_diffs) / len(sampled_diffs))
    sampled_means.sort()
    observed = sum(left_map[key][metric] - right_map[key][metric] for key in left_map) / len(left_map)
    return {
        "mean": observed,
        "lower_95": sampled_means[max(0, int(0.025 * resamples) - 1)],
        "upper_95": sampled_means[min(resamples - 1, int(0.975 * resamples))],
        "resamples": resamples,
    }
