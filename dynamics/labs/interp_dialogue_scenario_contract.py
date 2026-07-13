from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any, Iterable

from dynamics.labs.interp_m1_common import validate_json_schema


_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_SCHEMA_PATH = (
    _ROOT / "research" / "scenarios" / "interp-dialogue-001" / "scenario.schema.json"
)

_FAMILY_ID_BY_DOMAIN = {
    "REL": "REL-BOUNDARY-001",
    "WORK": "WORK-FEEDBACK-001",
    "RISK": "RISK-FOOTSTEPS-001",
}

_FACTOR_DECLARATIONS = {
    "REL": {
        "reported_current_mood": (
            "vignette_reported_current_mood",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "target_history": (
            "vignette_relational_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "externally_cued_prior_material": (
            "vignette_externally_cued_material",
            "EXPERIMENTER_CUE",
        ),
    },
    "WORK": {
        "reported_evaluation_threat": (
            "vignette_reported_evaluation_threat",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "evaluator_criterion_history": (
            "vignette_evaluator_criterion_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "public_feedback_addendum": (
            "vignette_feedback_addendum",
            "PUBLIC_STIMULUS_VARIANT",
        ),
    },
    "RISK": {
        "reported_pre_event_arousal": (
            "vignette_reported_pre_event_arousal",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "recent_threat_history": (
            "vignette_recent_threat_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "route_match_observation": (
            "vignette_route_match_observation",
            "PUBLIC_STIMULUS_VARIANT",
        ),
    },
}

_AUTHORITY_LANES = {
    "author_origin_possibilities": "AUTHOR_ORIGIN_PHENOMENOLOGICAL_POSSIBILITY",
    "phenomenological_expectations": "NONEXHAUSTIVE_POSSIBILITY_NOT_EXPECTED_OUTPUT",
    "normative_invariants": "PROGRAM_NORMATIVE_INVARIANT",
}

_FORBIDDEN_EXPERIMENT_FIELDS = {
    "activation",
    "correct_mechanism",
    "correct_output",
    "embedding",
    "engine_config",
    "episode_writer",
    "evaluation",
    "evaluator",
    "expected_mechanism",
    "expected_output",
    "expected_signature",
    "expected_trace",
    "human_data",
    "human_judgment",
    "human_response",
    "llm_activation",
    "model_id",
    "model_output",
    "narrative_writer",
    "participant",
    "run_id",
    "runner",
    "runtime_state",
    "writer",
}


class ScenarioContractError(ValueError):
    """Raised when an INTERP-DIALOGUE-001A design fixture is malformed."""


def _fail(message: str) -> None:
    raise ScenarioContractError(message)


def loads_exact(source: bytes | str) -> dict[str, Any]:
    """Load one JSON object while rejecting duplicate keys."""

    def reject_duplicate_keys(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    text = source.decode("utf-8") if isinstance(source, bytes) else source
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise ScenarioContractError(str(exc)) from exc
    if not isinstance(value, dict):
        _fail("$ must be an object")
    return value


def load_family(path: str | Path) -> dict[str, Any]:
    return loads_exact(Path(path).read_bytes())


def _reject_experiment_fields(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in _FORBIDDEN_EXPERIMENT_FIELDS:
                _fail(f"forbidden post-001A field {key!r} at {path}")
            _reject_experiment_fields(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_experiment_fields(child, f"{path}/{index}")


def _validate_schema(
    family: dict[str, Any], schema_path: str | Path | None
) -> None:
    schema = load_family(schema_path or _DEFAULT_SCHEMA_PATH)
    try:
        validate_json_schema(family, schema)
    except ValueError as exc:
        raise ScenarioContractError(f"schema validation failed: {exc}") from exc


def _validate_target_scope(family: dict[str, Any]) -> None:
    domain = family["domain"]
    scope = family["target_scope"]
    if domain == "RISK":
        expected = {
            "resolution": "unresolved",
            "stable_entity_target_form_applicability": "NOT_APPLICABLE",
            "provisional_target_representation_status": "OPEN_DISCRIMINATOR",
        }
    else:
        expected = {
            "resolution": "resolved",
            "stable_entity_target_form_applicability": "OPEN_DISCRIMINATOR",
            "provisional_target_representation_status": "OUT_OF_SCOPE",
        }
    for key, expected_value in expected.items():
        if scope[key] != expected_value:
            _fail(f"{domain} target_scope.{key} must be {expected_value}")


def _validate_factor_declarations(
    family: dict[str, Any],
) -> tuple[list[str], dict[str, tuple[str, str]]]:
    domain = family["domain"]
    if family["family_id"] != _FAMILY_ID_BY_DOMAIN[domain]:
        _fail(f"{domain} family_id changed")

    factors = family["factors"]
    by_id = {factor["factor_id"]: factor for factor in factors}
    expected = _FACTOR_DECLARATIONS[domain]
    if len(by_id) != len(factors) or set(by_id) != set(expected):
        _fail(f"{domain} factor declarations changed")

    level_ids: dict[str, tuple[str, str]] = {}
    for factor_id, (expected_kind, expected_lane) in expected.items():
        factor = by_id[factor_id]
        if factor["operational_source_kind"] != expected_kind:
            _fail(f"{factor_id} operational_source_kind changed")
        lanes = {level["source_lane"] for level in factor["levels"]}
        if lanes != {expected_lane}:
            _fail(f"{factor_id} source lane changed")
        level_ids[factor_id] = tuple(
            level["level_id"] for level in factor["levels"]
        )
    return [factor["factor_id"] for factor in factors], level_ids


def _all_public_records(family: dict[str, Any]) -> list[dict[str, str]]:
    return list(family["stimulus"]["public_record"]) + [
        record
        for factor in family["factors"]
        for level in factor["levels"]
        for record in level["level_specific_public_record"]
    ]


def _validate_authority_lanes(family: dict[str, Any]) -> None:
    shared = family["shared_contract"]
    author_statements: set[str] = set()
    for lane, expected_authority in _AUTHORITY_LANES.items():
        for entry in shared[lane]:
            if entry["authority"] != expected_authority:
                _fail(f"{lane} entry left its authority lane")
            if lane == "author_origin_possibilities":
                author_statements.add(entry["statement"])

    public_statements = {record["statement"] for record in _all_public_records(family)}
    if author_statements & public_statements:
        _fail("author-origin possibilities cannot be copied into the public record")


def _validate_factor_contrasts(
    family: dict[str, Any], factor_ids: list[str]
) -> None:
    factors = {factor["factor_id"]: factor for factor in family["factors"]}
    contracts = {
        contract["factor_id"]: contract
        for contract in family["factor_contrast_contracts"]
    }
    if (
        len(contracts) != len(family["factor_contrast_contracts"])
        or set(contracts) != set(factor_ids)
    ):
        _fail("factor contrast contracts must cover each factor exactly once")

    discriminator_ids = {
        item["id"] for item in family["shared_contract"]["open_discriminators"]
    }
    for factor_id, contract in contracts.items():
        expected_lane = _FACTOR_DECLARATIONS[family["domain"]][factor_id][1]
        if contract["source_lane"] != expected_lane:
            _fail(f"{factor_id} contrast source lane does not match its factor")
        if set(contract["held_constant_factor_ids"]) != set(factor_ids) - {factor_id}:
            _fail(f"{factor_id} held constants must be exactly the other two factors")
        unknown_refs = set(contract["open_discriminator_refs"]) - discriminator_ids
        if unknown_refs:
            _fail(f"{factor_id} contrast references unknown discriminators: {sorted(unknown_refs)}")

        records_by_level = [
            level["level_specific_public_record"]
            for level in factors[factor_id]["levels"]
        ]
        effect = contract["public_record_effect"]
        if effect == "LEVEL_SPECIFIC_PUBLIC_RECORD_ONLY" and not all(records_by_level):
            _fail(f"{factor_id} requires a public record for both factor levels")
        if effect == "UNCHANGED" and any(records_by_level):
            _fail(f"{factor_id} UNCHANGED effect forbids level-specific records")


def _cell_assignments(
    family: dict[str, Any],
    factor_ids: list[str],
    level_ids: dict[str, tuple[str, str]],
) -> dict[str, tuple[str, ...]]:
    assignments: dict[str, tuple[str, ...]] = {}
    observed: set[tuple[str, ...]] = set()
    for cell in family["cells"]:
        levels = cell["factor_levels"]
        if set(levels) != set(factor_ids):
            _fail(f"{cell['cell_id']} factor keys do not match the family")
        assignment = tuple(levels[factor_id] for factor_id in factor_ids)
        if any(
            assignment[index] not in level_ids[factor_id]
            for index, factor_id in enumerate(factor_ids)
        ):
            _fail(f"{cell['cell_id']} references an unknown factor level")
        if assignment in observed:
            _fail("cells contain a duplicate cube assignment")
        observed.add(assignment)
        assignments[cell["cell_id"]] = assignment

    expected = set(product(*(level_ids[factor_id] for factor_id in factor_ids)))
    if observed != expected:
        _fail("cells do not cover the complete 2x2x2 factor cube")
    return assignments


def _derive_pairs(
    assignments: dict[str, tuple[str, ...]], factor_ids: list[str]
) -> tuple[tuple[str, str, str], ...]:
    pairs: list[tuple[str, str, str]] = []
    for left_id, right_id in combinations(sorted(assignments), 2):
        differences = [
            index
            for index, (left, right) in enumerate(
                zip(assignments[left_id], assignments[right_id])
            )
            if left != right
        ]
        if len(differences) == 1:
            pairs.append((left_id, right_id, factor_ids[differences[0]]))
    return tuple(pairs)


def derive_hamming_one_contrasts(
    family: dict[str, Any],
) -> tuple[tuple[str, str, str], ...]:
    """Return every Hamming-one edge as (left cell, right cell, changed factor)."""

    factor_ids, level_ids = _validate_factor_declarations(family)
    assignments = _cell_assignments(family, factor_ids, level_ids)
    return _derive_pairs(assignments, factor_ids)


def _validate_same_projection(
    family: dict[str, Any],
    factor_ids: list[str],
    assignments: dict[str, tuple[str, ...]],
) -> None:
    claim = family["same_immediate_projection_claim"]
    compared = claim["compared_cell_ids"]
    if any(cell_id not in assignments for cell_id in compared):
        _fail("same-immediate-projection claim references an unknown cell")
    differences = [
        index
        for index, (left, right) in enumerate(
            zip(assignments[compared[0]], assignments[compared[1]])
        )
        if left != right
    ]
    if len(differences) != 1:
        _fail(
            "same-immediate-projection cells are not a "
            "factor-label Hamming-one contrast"
        )
    if claim["changed_factor_id"] != factor_ids[differences[0]]:
        _fail("same-immediate-projection changed factor does not match its pair")


def _validate_family_declaration_ids(family: dict[str, Any]) -> None:
    shared = family["shared_contract"]
    declarations = [family["family_id"]]
    declarations += [
        record["id"]
        for lane in ("public_record", "world_unknowns")
        for record in family["stimulus"][lane]
    ]
    declarations += [
        declared_id
        for factor in family["factors"]
        for declared_id in (
            factor["factor_id"],
            *(level["level_id"] for level in factor["levels"]),
            *(
                record["id"]
                for level in factor["levels"]
                for record in level["level_specific_public_record"]
            ),
        )
    ]
    declarations += [
        entry["id"]
        for lane in _AUTHORITY_LANES
        for entry in shared[lane]
    ]
    declarations += [item["id"] for item in shared["open_discriminators"]]
    declarations += [cell["cell_id"] for cell in family["cells"]]
    claim = family["same_immediate_projection_claim"]
    declarations += [claim["claim_id"], claim["future_probe"]["probe_id"]]

    duplicates = sorted(
        declared_id
        for declared_id, count in Counter(declarations).items()
        if count > 1
    )
    if duplicates:
        _fail(f"declaration IDs collide within the family: {duplicates}")


def validate_family(
    family: dict[str, Any],
    *,
    schema_path: str | Path | None = None,
) -> tuple[tuple[str, str, str], ...]:
    """Validate one preregistered family and return its Hamming-one edges."""

    _reject_experiment_fields(family)
    _validate_schema(family, schema_path)
    _validate_target_scope(family)
    factor_ids, level_ids = _validate_factor_declarations(family)
    _validate_authority_lanes(family)
    _validate_factor_contrasts(family, factor_ids)
    assignments = _cell_assignments(family, factor_ids, level_ids)
    _validate_same_projection(family, factor_ids, assignments)
    _validate_family_declaration_ids(family)

    pairs = _derive_pairs(assignments, factor_ids)
    if len(pairs) != 12:
        _fail(
            "complete three-factor binary cube must have 12 "
            "factor-label Hamming-one contrasts"
        )
    counts = Counter(changed_factor for _, _, changed_factor in pairs)
    if set(counts) != set(factor_ids) or set(counts.values()) != {4}:
        _fail("each factor must supply exactly four factor-label Hamming-one contrasts")
    return pairs


def load_and_validate_family(
    path: str | Path,
    *,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    family = load_family(path)
    validate_family(family, schema_path=schema_path)
    return family
