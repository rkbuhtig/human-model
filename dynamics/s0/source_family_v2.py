from __future__ import annotations

import itertools
from typing import Any, Mapping, Sequence

from .source_common_v3 import (
    CONTINUATION_CONDITIONS,
    FAMILY_ID,
    FEEDBACK_CATEGORIES,
    GENERATOR_VERSION,
    HISTORY_CONDITIONS,
    IMMEDIATE_ACTIONS,
    LATENT_STATES,
    LONG_HORIZON_REGIONS,
    PROBABILITY_SCALE,
    HashStream,
    SourceProcessError,
    canonical_bytes,
    distribution_ok,
    normalize_weights,
    require_hex,
    sha256_hex,
    total_variation,
)


def derive_family_seed(
    *,
    merge_commit_sha: str,
    generator_blob_sha: str,
    hyperprior_blob_sha: str,
    runtime_blob_sha: str,
    beacon_randomness_hex: str,
) -> str:
    for name, value in (
        ("merge_commit_sha", merge_commit_sha),
        ("generator_blob_sha", generator_blob_sha),
        ("hyperprior_blob_sha", hyperprior_blob_sha),
        ("runtime_blob_sha", runtime_blob_sha),
    ):
        require_hex(value, length=40, name=name)
    require_hex(beacon_randomness_hex, length=64, name="beacon_randomness_hex")
    return sha256_hex(
        "|".join(
            (
                GENERATOR_VERSION,
                FAMILY_ID,
                merge_commit_sha.lower(),
                generator_blob_sha.lower(),
                hyperprior_blob_sha.lower(),
                runtime_blob_sha.lower(),
                beacon_randomness_hex.lower(),
            )
        ).encode("utf-8")
    )


def _sample_distribution(
    stream: HashStream,
    count: int,
    *,
    weight_minimum: int,
    weight_maximum: int,
    boosts: Mapping[int, int] | None = None,
) -> list[int]:
    weights = [stream.integer(weight_minimum, weight_maximum) for _ in range(count)]
    for index, boost in (boosts or {}).items():
        weights[index] += int(boost)
    return normalize_weights(weights)


def _mean_row_tv(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> float:
    return sum(total_variation(a, b) for a, b in zip(left, right)) / len(left)


def _minimum_pairwise_tv(rows: Sequence[Sequence[int]]) -> float:
    pairs = list(itertools.combinations(rows, 2))
    return min(total_variation(a, b) for a, b in pairs) if pairs else 0.0


def _maximum_matrix_pair_tv(matrices: Mapping[str, Sequence[Sequence[int]]]) -> float:
    pairs = list(itertools.combinations(matrices.values(), 2))
    return max(_mean_row_tv(a, b) for a, b in pairs) if pairs else 0.0


def _sample_candidate(
    hyperprior: Mapping[str, Any],
    *,
    family_seed_hex: str,
    instance_index: int,
    attempt: int,
) -> dict[str, Any]:
    sampling = hyperprior["sampling"]
    stream = HashStream(family_seed_hex, f"family-002:instance:{instance_index}:attempt:{attempt}")
    minimum = int(sampling["positive_weight_minimum"])
    maximum = int(sampling["positive_weight_maximum"])
    diagonal_boost = int(sampling["transition_diagonal_weight_boost"])
    emission_anchor_boost = int(sampling["emission_anchor_weight_boost"])
    feedback_anchor_boost = int(sampling["feedback_anchor_weight_boost"])

    initial = {
        condition: _sample_distribution(
            stream,
            len(LATENT_STATES),
            weight_minimum=minimum,
            weight_maximum=maximum,
        )
        for condition in HISTORY_CONDITIONS
    }
    transitions = {
        condition: [
            _sample_distribution(
                stream,
                len(LATENT_STATES),
                weight_minimum=minimum,
                weight_maximum=maximum,
                boosts={row: diagonal_boost},
            )
            for row in range(len(LATENT_STATES))
        ]
        for condition in CONTINUATION_CONDITIONS
    }
    immediate = [
        _sample_distribution(
            stream,
            len(IMMEDIATE_ACTIONS),
            weight_minimum=minimum,
            weight_maximum=maximum,
            boosts={stream.integer(0, len(IMMEDIATE_ACTIONS) - 1): emission_anchor_boost},
        )
        for _ in LATENT_STATES
    ]
    feedback = {
        action: [
            _sample_distribution(
                stream,
                len(FEEDBACK_CATEGORIES),
                weight_minimum=minimum,
                weight_maximum=maximum,
                boosts={stream.integer(0, len(FEEDBACK_CATEGORIES) - 1): feedback_anchor_boost},
            )
            for _ in LATENT_STATES
        ]
        for action in IMMEDIATE_ACTIONS
    }
    horizon = [
        _sample_distribution(
            stream,
            len(LONG_HORIZON_REGIONS),
            weight_minimum=minimum,
            weight_maximum=maximum,
            boosts={stream.integer(0, len(LONG_HORIZON_REGIONS) - 1): emission_anchor_boost},
        )
        for _ in LATENT_STATES
    ]
    return {
        "initial_state_probabilities": initial,
        "conditioned_transition_matrices": transitions,
        "emission_parameters": {
            "immediate_action": immediate,
            "action_conditioned_feedback": feedback,
            "long_horizon_region": horizon,
        },
    }


def _validate_matrix(
    matrix: Sequence[Sequence[int]],
    *,
    row_count: int,
    category_count: int,
    minimum_probability: float,
    maximum_probability: float,
) -> bool:
    return len(matrix) == row_count and all(
        distribution_ok(
            row,
            category_count=category_count,
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for row in matrix
    )


def validate_intrinsic_candidate(
    candidate: Mapping[str, Any], hyperprior: Mapping[str, Any]
) -> list[str]:
    acceptance = hyperprior["intrinsic_acceptance"]
    minimum_probability = float(acceptance["minimum_category_probability"])
    maximum_probability = float(acceptance["maximum_category_probability"])
    failures: list[str] = []

    initial = candidate.get("initial_state_probabilities", {})
    if set(initial) != set(HISTORY_CONDITIONS) or not all(
        distribution_ok(
            initial[condition],
            category_count=len(LATENT_STATES),
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for condition in HISTORY_CONDITIONS
    ):
        failures.append("INITIAL_DISTRIBUTION_CONTRACT")
    elif total_variation(initial["H-STABLE"], initial["H-BREACH"]) < float(
        acceptance["minimum_history_initial_total_variation"]
    ):
        failures.append("HISTORY_INITIAL_EFFECT_TOO_SMALL")

    transitions = candidate.get("conditioned_transition_matrices", {})
    if set(transitions) != set(CONTINUATION_CONDITIONS) or not all(
        _validate_matrix(
            transitions[condition],
            row_count=len(LATENT_STATES),
            category_count=len(LATENT_STATES),
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for condition in CONTINUATION_CONDITIONS
    ):
        failures.append("TRANSITION_CONTRACT")
    elif _maximum_matrix_pair_tv(transitions) < float(
        acceptance["minimum_any_condition_matrix_mean_row_total_variation"]
    ):
        failures.append("CONTINUATION_EFFECT_TOO_SMALL")

    emissions = candidate.get("emission_parameters", {})
    immediate = emissions.get("immediate_action", ())
    if not _validate_matrix(
        immediate,
        row_count=len(LATENT_STATES),
        category_count=len(IMMEDIATE_ACTIONS),
        minimum_probability=minimum_probability,
        maximum_probability=maximum_probability,
    ):
        failures.append("IMMEDIATE_EMISSION_CONTRACT")
    elif _minimum_pairwise_tv(immediate) < float(
        acceptance["minimum_immediate_emission_state_total_variation"]
    ):
        failures.append("IMMEDIATE_STATE_DISCRIMINATION_TOO_SMALL")

    horizon = emissions.get("long_horizon_region", ())
    if not _validate_matrix(
        horizon,
        row_count=len(LATENT_STATES),
        category_count=len(LONG_HORIZON_REGIONS),
        minimum_probability=minimum_probability,
        maximum_probability=maximum_probability,
    ):
        failures.append("HORIZON_EMISSION_CONTRACT")
    elif _minimum_pairwise_tv(horizon) < float(
        acceptance["minimum_horizon_emission_state_total_variation"]
    ):
        failures.append("HORIZON_STATE_DISCRIMINATION_TOO_SMALL")

    feedback = emissions.get("action_conditioned_feedback", {})
    if set(feedback) != set(IMMEDIATE_ACTIONS) or not all(
        _validate_matrix(
            feedback[action],
            row_count=len(LATENT_STATES),
            category_count=len(FEEDBACK_CATEGORIES),
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for action in IMMEDIATE_ACTIONS
    ):
        failures.append("FEEDBACK_EMISSION_CONTRACT")
    else:
        maximum_action_effect = _maximum_matrix_pair_tv(feedback)
        if maximum_action_effect < float(
            acceptance["minimum_action_feedback_mean_row_total_variation"]
        ):
            failures.append("ACTION_FEEDBACK_EFFECT_TOO_SMALL")
        if min(_minimum_pairwise_tv(feedback[action]) for action in IMMEDIATE_ACTIONS) < float(
            acceptance["minimum_feedback_emission_state_total_variation"]
        ):
            failures.append("FEEDBACK_STATE_DISCRIMINATION_TOO_SMALL")
    return failures


def generate_instance(
    hyperprior: Mapping[str, Any],
    *,
    family_seed_hex: str,
    instance_index: int,
) -> dict[str, Any]:
    """Generate one independent process draw without consulting any candidate model."""

    require_hex(family_seed_hex, length=64, name="family_seed_hex")
    if hyperprior.get("family_id") != FAMILY_ID:
        raise SourceProcessError("family ID mismatch")
    if hyperprior.get("generator_version") != GENERATOR_VERSION:
        raise SourceProcessError("generator version mismatch")
    instance_count = int(hyperprior["instance_count"])
    if not 0 <= instance_index < instance_count:
        raise SourceProcessError("instance_index outside frozen range")
    maximum_attempts = int(hyperprior["intrinsic_acceptance"]["maximum_candidate_attempts"])

    from .source_diagnostics_v2 import process_adequacy_report

    for attempt in range(maximum_attempts):
        candidate = _sample_candidate(
            hyperprior,
            family_seed_hex=family_seed_hex,
            instance_index=instance_index,
            attempt=attempt,
        )
        failures = validate_intrinsic_candidate(candidate, hyperprior)
        diagnostic = process_adequacy_report(candidate, hyperprior["process_adequacy"])
        failures.extend(diagnostic["failures"])
        if not failures:
            return {
                "schema_version": "s0-source-instance/2.0.0",
                "family_id": FAMILY_ID,
                "instance_id": f"{FAMILY_ID}-INSTANCE-{instance_index:04d}",
                "instance_index": instance_index,
                "generator_version": GENERATOR_VERSION,
                "latent_states": list(LATENT_STATES),
                **candidate,
                "generation_receipt": {
                    "candidate_attempt": attempt,
                    "instance_seed_digest": sha256_hex(
                        f"{family_seed_hex}|instance:{instance_index}|attempt:{attempt}".encode("utf-8")
                    ),
                    "acceptance_basis": "INTRINSIC_PROCESS_VALIDITY_ONLY",
                    "model_outputs_or_scores_read": False,
                    "process_adequacy": diagnostic["metrics"],
                },
            }
    raise SourceProcessError(
        f"no valid source instance found in {maximum_attempts} deterministic attempts"
    )


def generate_family(hyperprior: Mapping[str, Any], *, family_seed_hex: str) -> list[dict[str, Any]]:
    instances = [
        generate_instance(hyperprior, family_seed_hex=family_seed_hex, instance_index=index)
        for index in range(int(hyperprior["instance_count"]))
    ]
    if len({canonical_bytes(instance) for instance in instances}) != len(instances):
        raise SourceProcessError("independent family generation produced duplicate instance bytes")
    return instances
