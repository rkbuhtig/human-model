from __future__ import annotations

from dataclasses import dataclass
import hashlib
import itertools
import json
from typing import Any, Iterable, Mapping, Sequence

PROBABILITY_SCALE = 1_000_000
GENERATOR_VERSION = "sim-rel-boundary-family-generator/1.0.0"
LATENT_STATES = tuple(f"q{i}" for i in range(6))
HISTORY_CONDITIONS = ("H-STABLE", "H-BREACH")
CONTINUATION_CONDITIONS = ("F-REPAIR", "F-DEFLECT", "F-REPEAT", "F-PUBLIC")
IMMEDIATE_ACTIONS = (
    "SEEK_CLARIFICATION",
    "EXPRESS_HURT",
    "ASSERT_BOUNDARY",
    "TEMPORARY_WITHDRAWAL",
    "PUNITIVE_ATTACK",
    "SUPPRESS_FOR_ROLE",
    "REPAIR_ATTEMPT",
    "RELATION_EXIT",
)
LONG_HORIZON_REGIONS = (
    "PARTIAL_REPAIR",
    "GUARDED_CONTINUATION",
    "CONFLICT_LOOP",
    "RELATION_EXIT",
    "UNRESOLVED_DRIFT",
)


class SourceFamilyError(ValueError):
    """Raised when public source-family inputs or generated candidates are invalid."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: bytes | str) -> str:
    payload = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.sha256(payload).hexdigest()


def _require_hex(value: str, *, length: int, name: str) -> str:
    if len(value) != length:
        raise SourceFamilyError(f"{name} must contain {length} hexadecimal characters")
    try:
        bytes.fromhex(value)
    except ValueError as error:
        raise SourceFamilyError(f"{name} must be hexadecimal") from error
    return value.lower()


def derive_family_seed(
    *,
    merge_commit_sha: str,
    generator_blob_sha: str,
    hyperprior_blob_sha: str,
    beacon_randomness_hex: str,
    family_id: str,
) -> str:
    """Derive the public family seed from post-merge randomness and frozen artifacts."""

    _require_hex(merge_commit_sha, length=40, name="merge_commit_sha")
    _require_hex(generator_blob_sha, length=40, name="generator_blob_sha")
    _require_hex(hyperprior_blob_sha, length=40, name="hyperprior_blob_sha")
    _require_hex(beacon_randomness_hex, length=64, name="beacon_randomness_hex")
    if not family_id:
        raise SourceFamilyError("family_id must be non-empty")
    material = "|".join(
        (
            GENERATOR_VERSION,
            family_id,
            merge_commit_sha.lower(),
            generator_blob_sha.lower(),
            hyperprior_blob_sha.lower(),
            beacon_randomness_hex.lower(),
        )
    )
    return sha256_hex(material)


@dataclass
class HashStream:
    seed_hex: str
    domain: str
    counter: int = 0

    def __post_init__(self) -> None:
        _require_hex(self.seed_hex, length=64, name="seed_hex")
        if not self.domain:
            raise SourceFamilyError("stream domain must be non-empty")

    def _block(self) -> bytes:
        payload = b"|".join(
            (
                bytes.fromhex(self.seed_hex),
                self.domain.encode("ascii"),
                str(self.counter).encode("ascii"),
            )
        )
        self.counter += 1
        return hashlib.sha256(payload).digest()

    def integer(self, minimum: int, maximum: int) -> int:
        if minimum > maximum:
            raise SourceFamilyError("invalid integer sampling range")
        width = maximum - minimum + 1
        limit = (1 << 64) - ((1 << 64) % width)
        while True:
            value = int.from_bytes(self._block()[:8], "big")
            if value < limit:
                return minimum + value % width


def _normalize_weights(weights: Sequence[int]) -> list[int]:
    if not weights or any(weight <= 0 for weight in weights):
        raise SourceFamilyError("weights must be non-empty positive integers")
    total = sum(weights)
    numerators = [weight * PROBABILITY_SCALE for weight in weights]
    units = [value // total for value in numerators]
    remainder = PROBABILITY_SCALE - sum(units)
    order = sorted(
        range(len(weights)),
        key=lambda index: (numerators[index] % total, -index),
        reverse=True,
    )
    for index in order[:remainder]:
        units[index] += 1
    if sum(units) != PROBABILITY_SCALE:
        raise AssertionError("normalization failed")
    return units


def total_variation(left: Sequence[int], right: Sequence[int]) -> float:
    if len(left) != len(right) or not left:
        raise SourceFamilyError("total variation requires equal non-empty vectors")
    return sum(abs(a - b) for a, b in zip(left, right)) / (2 * PROBABILITY_SCALE)


def _mean_row_tv(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> float:
    if len(left) != len(right) or not left:
        raise SourceFamilyError("matrix comparison requires equal non-empty matrices")
    return sum(total_variation(a, b) for a, b in zip(left, right)) / len(left)


def _minimum_pairwise_tv(rows: Sequence[Sequence[int]]) -> float:
    pairs = list(itertools.combinations(rows, 2))
    return min(total_variation(left, right) for left, right in pairs) if pairs else 0.0


def _minimum_condition_matrix_tv(matrices: Mapping[str, Sequence[Sequence[int]]]) -> float:
    pairs = list(itertools.combinations(matrices.values(), 2))
    return min(_mean_row_tv(left, right) for left, right in pairs) if pairs else 0.0


def _distribution_ok(
    distribution: Sequence[int], *, minimum_probability: float, maximum_probability: float
) -> bool:
    return (
        len(distribution) > 0
        and sum(distribution) == PROBABILITY_SCALE
        and min(distribution) >= round(minimum_probability * PROBABILITY_SCALE)
        and max(distribution) <= round(maximum_probability * PROBABILITY_SCALE)
    )


def _matrix_ok(
    matrix: Sequence[Sequence[int]], *, minimum_probability: float, maximum_probability: float
) -> bool:
    return len(matrix) == len(LATENT_STATES) and all(
        _distribution_ok(
            row,
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for row in matrix
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
    return _normalize_weights(weights)


def _sample_candidate(
    hyperprior: Mapping[str, Any], *, family_seed_hex: str, instance_index: int, attempt: int
) -> dict[str, Any]:
    sampling = hyperprior["sampling"]
    stream = HashStream(
        family_seed_hex,
        f"instance:{instance_index}:attempt:{attempt}",
    )
    weight_minimum = int(sampling["positive_weight_minimum"])
    weight_maximum = int(sampling["positive_weight_maximum"])
    diagonal_boost = int(sampling["transition_diagonal_weight_boost"])

    initial = {
        condition: _sample_distribution(
            stream,
            len(LATENT_STATES),
            weight_minimum=weight_minimum,
            weight_maximum=weight_maximum,
        )
        for condition in HISTORY_CONDITIONS
    }
    transitions: dict[str, list[list[int]]] = {}
    for condition in CONTINUATION_CONDITIONS:
        transitions[condition] = [
            _sample_distribution(
                stream,
                len(LATENT_STATES),
                weight_minimum=weight_minimum,
                weight_maximum=weight_maximum,
                boosts={row_index: diagonal_boost},
            )
            for row_index in range(len(LATENT_STATES))
        ]
    immediate_emissions = [
        _sample_distribution(
            stream,
            len(IMMEDIATE_ACTIONS),
            weight_minimum=weight_minimum,
            weight_maximum=weight_maximum,
        )
        for _ in LATENT_STATES
    ]
    horizon_emissions = [
        _sample_distribution(
            stream,
            len(LONG_HORIZON_REGIONS),
            weight_minimum=weight_minimum,
            weight_maximum=weight_maximum,
        )
        for _ in LATENT_STATES
    ]
    return {
        "initial_state_probabilities": initial,
        "conditioned_transition_matrices": transitions,
        "emission_parameters": {
            "immediate_action": immediate_emissions,
            "long_horizon_region": horizon_emissions,
        },
    }


def validate_candidate(candidate: Mapping[str, Any], hyperprior: Mapping[str, Any]) -> list[str]:
    acceptance = hyperprior["intrinsic_acceptance"]
    minimum_probability = float(acceptance["minimum_category_probability"])
    maximum_probability = float(acceptance["maximum_category_probability"])
    failures: list[str] = []

    initial = candidate["initial_state_probabilities"]
    if set(initial) != set(HISTORY_CONDITIONS):
        failures.append("INITIAL_CONDITION_SET")
    elif not all(
        _distribution_ok(
            initial[condition],
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for condition in HISTORY_CONDITIONS
    ):
        failures.append("INITIAL_DISTRIBUTION_BOUNDS")
    elif total_variation(initial["H-STABLE"], initial["H-BREACH"]) < float(
        acceptance["minimum_history_initial_total_variation"]
    ):
        failures.append("HISTORY_INITIAL_EFFECT_TOO_SMALL")

    transitions = candidate["conditioned_transition_matrices"]
    if set(transitions) != set(CONTINUATION_CONDITIONS):
        failures.append("TRANSITION_CONDITION_SET")
    elif not all(
        _matrix_ok(
            transitions[condition],
            minimum_probability=minimum_probability,
            maximum_probability=maximum_probability,
        )
        for condition in CONTINUATION_CONDITIONS
    ):
        failures.append("TRANSITION_DISTRIBUTION_BOUNDS")
    elif _minimum_condition_matrix_tv(transitions) < float(
        acceptance["minimum_condition_matrix_mean_row_total_variation"]
    ):
        failures.append("CONDITION_TRANSITION_EFFECT_TOO_SMALL")

    emissions = candidate["emission_parameters"]
    for channel, categories, threshold_key in (
        (
            "immediate_action",
            IMMEDIATE_ACTIONS,
            "minimum_immediate_emission_state_total_variation",
        ),
        (
            "long_horizon_region",
            LONG_HORIZON_REGIONS,
            "minimum_horizon_emission_state_total_variation",
        ),
    ):
        rows = emissions[channel]
        if len(rows) != len(LATENT_STATES) or not all(
            _distribution_ok(
                row,
                minimum_probability=minimum_probability,
                maximum_probability=maximum_probability,
            )
            and len(row) == len(categories)
            for row in rows
        ):
            failures.append(f"{channel.upper()}_EMISSION_BOUNDS")
        elif _minimum_pairwise_tv(rows) < float(acceptance[threshold_key]):
            failures.append(f"{channel.upper()}_STATE_DISCRIMINATION_TOO_SMALL")
    return failures


def generate_instance(
    hyperprior: Mapping[str, Any], *, family_seed_hex: str, instance_index: int
) -> dict[str, Any]:
    """Generate one evaluator-hidden instance without consulting any model or score."""

    _require_hex(family_seed_hex, length=64, name="family_seed_hex")
    if hyperprior.get("generator_version") != GENERATOR_VERSION:
        raise SourceFamilyError("hyperprior generator version mismatch")
    instance_count = int(hyperprior["instance_count"])
    if not 0 <= instance_index < instance_count:
        raise SourceFamilyError("instance_index outside frozen family range")
    max_attempts = int(hyperprior["intrinsic_acceptance"]["maximum_candidate_attempts"])
    for attempt in range(max_attempts):
        candidate = _sample_candidate(
            hyperprior,
            family_seed_hex=family_seed_hex,
            instance_index=instance_index,
            attempt=attempt,
        )
        failures = validate_candidate(candidate, hyperprior)
        if not failures:
            instance_seed_digest = sha256_hex(
                f"{family_seed_hex}|instance:{instance_index}|attempt:{attempt}"
            )
            return {
                "schema_version": "s0-source-instance/1.0.0",
                "family_id": hyperprior["family_id"],
                "instance_id": f"{hyperprior['family_id']}-INSTANCE-{instance_index:04d}",
                "instance_index": instance_index,
                "generator_version": GENERATOR_VERSION,
                "latent_states": list(LATENT_STATES),
                "observable_vocabularies": {
                    "immediate_action": list(IMMEDIATE_ACTIONS),
                    "long_horizon_region": list(LONG_HORIZON_REGIONS),
                },
                **candidate,
                "generation_receipt": {
                    "candidate_attempt": attempt,
                    "instance_seed_digest": instance_seed_digest,
                    "acceptance_basis": "INTRINSIC_SOURCE_VALIDITY_ONLY",
                    "model_outputs_or_scores_read": False,
                },
            }
    raise SourceFamilyError(
        f"no valid source instance found in {max_attempts} deterministic attempts"
    )


def generate_family(hyperprior: Mapping[str, Any], *, family_seed_hex: str) -> list[dict[str, Any]]:
    return [
        generate_instance(hyperprior, family_seed_hex=family_seed_hex, instance_index=index)
        for index in range(int(hyperprior["instance_count"]))
    ]


def family_manifest(instances: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    materialized = list(instances)
    if not materialized:
        raise SourceFamilyError("family manifest requires at least one instance")
    return {
        "schema_version": "s0-source-family-manifest/1.0.0",
        "family_id": materialized[0]["family_id"],
        "instance_count": len(materialized),
        "instance_digests": {
            instance["instance_id"]: sha256_hex(canonical_bytes(instance))
            for instance in materialized
        },
        "selection_rule": "ALL_GENERATED_INSTANCES_INCLUDED",
        "post_generation_model_based_selection": False,
    }
