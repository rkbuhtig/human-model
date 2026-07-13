from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unittest

from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    digest,
    load_exact,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION_PATH = BENCHMARKS / "interp-001d1-v1-execution.json"
EVALUATION_PATH = BENCHMARKS / "interp-001d1-v1-evaluation.json"
MANIFEST_SCHEMA_PATH = BENCHMARKS / "interp-001d1-manifest.schema.json"
RESULT_SCHEMA_PATH = BENCHMARKS / "interp-001d1-v1-result.schema.json"
RUN_SCHEMA_PATH = BENCHMARKS / "interp-001d1-v1-run.schema.json"
PREREG_PATH = BENCHMARKS / "interp-001d1-target-form-ghost-ablation.md"

EXPECTED_EXECUTION_MANIFEST_SHA256 = "ad627e9b27dbcf517d6dc16736974b8e8f2547ab98cb7a4bea8a4694cbcd1740"
EXPECTED_EXECUTION_CONTRACT_SHA256 = "1f49e2c89a79af5d50ff877ef9326191564d768be6af8a1904395929782513c7"
EXPECTED_EVALUATION_MANIFEST_SHA256 = "df25f49fb1b2c61ac798cfda7eb47a30c18951bd19860fa7010603004ec8c0aa"
EXPECTED_EVALUATION_CONTRACT_SHA256 = "0686be05871faa899fa76134b7d6768894bbc46b8914e1fe8b7de14aaea6aa20"
EXPECTED_OPERATOR_CATALOG_SHA256 = "a4e167dcc1e8e2773bfc42b83ce43a29ebfa57ec5ea9ea51339ebb8b232b09fb"
EXPECTED_INPUT_VIEW_CATALOG_SHA256 = "95a6240ef9de8cdb47376e2487d764f9ae469353771e1c0798b30942b007bf64"
EXPECTED_PREDICATE_CATALOG_SHA256 = "68bd6920dbb2619cf63f20eb4ffa94e2fe2118125c79d88135754fa7a9118d39"
EXPECTED_CHALLENGER_CATALOG_SHA256 = "b8fe72b671edd201a2e0043b43ca34f18900d4009cc0a1fc03e19eb57fe23d45"
EXPECTED_SIGNATURE_CATALOG_SHA256 = "271b54e72a59699e1e986a339a7b2db971677c1f2341a7502245cb681ae16990"
EXPECTED_COMPARISON_PROJECTION_SHA256 = "9290014b4dd31514741f5c555f5b5df8cb2378279042390353b9289125348cbb"
EXPECTED_RUN_SCHEMA_SHA256 = "4a993a28db36c052c5d6a81d4de8867a385523fcab972d1699049683130c73ed"

BLOCK_MODELS = {
    "SOURCE_COMPILER": ("TF0", "TF1", "TF2"),
    "ENCOUNTER_FORMATION": ("E0", "ER", "ET", "ERT"),
    "GHOST_PATH": ("G0", "GT", "GP", "GTP"),
}
BLOCK_FIXTURE_PREFIX = {
    "SOURCE_COMPILER": "srcfx",
    "ENCOUNTER_FORMATION": "encfx",
    "GHOST_PATH": "ghfx",
}
COMMON_FORBIDDEN_FIELDS = {
    "assertion_id",
    "cell_key",
    "evaluation_split",
    "evidence_strength",
    "expected_signature",
    "fixture_key",
    "model_id",
    "narrative_truth",
    "pass_fail_label",
    "raw_runtime_id",
}
EXPECTED_GUARDS = [
    "actions",
    "authority_grants",
    "episode_material_references",
    "evidence_assessments",
    "evidence_links",
    "narrative_writes",
    "observation_artifacts",
    "receipt_prefix",
    "runtime_state",
    "source_encounters",
    "source_occurrences",
    "world_outcomes",
]
BOOKKEEPING_PATHS = {
    "/semantic/source_kinds_used",
    "/semantic/contested_present",
    "/semantic/accessibility_relation",
    "/semantic/eligible_source_positions_ordered",
    "/semantic/eligible_source_position_count",
    "/semantic/reception_intervention_used",
    "/semantic/target_form_intervention_used",
    "/semantic/formation_operator_order",
    "/semantic/target_guidance_used",
    "/semantic/ghost_program_used",
    "/semantic/candidate_projection/registered_operation_relations",
    "/operator_trace/*",
}

EXPECTED_OPERATOR_PHASES = {
    "filter_scope_match": "resolve_scope",
    "require_effective_before_k": "normalize",
    "project_narrative_terrain": "source_projection",
    "project_adopted_integration": "source_projection",
    "preserve_contested_unsettled": "source_projection",
    "apply_pre_access_accessibility": "source_projection",
    "project_accessible_implicit_trace": "source_projection",
    "componentwise_max": "source_projection",
    "close_source_readout": "emit",
    "bind_opaque_sources": "bind",
    "base_profile": "formation",
    "apply_reception_eligibility": "formation",
    "apply_target_directional_compatibility": "formation",
    "emit_proxy": "emit",
    "ghost_seed": "seed",
    "canonical_traverse": "traverse",
    "broaden": "traverse",
    "contrast": "traverse",
    "counterfactual": "traverse",
    "confirmation_only": "traverse",
    "rehearsal": "traverse",
    "project_visited_direction_candidates": "traverse",
    "apply_target_candidate_eligibility": "traverse",
    "ghost_bind": "bind",
    "close_ghost_semantic": "emit",
    "d1_scoped_adjudicator_v1": "adjudicate",
}

EXPECTED_OPERATOR_ACCESS = {
    "filter_scope_match": (
        ["source_scope_rows"],
        [],
    ),
    "require_effective_before_k": (
        ["scope_matched_source_positions", "source_effective_rows"],
        [],
    ),
    "project_narrative_terrain": (
        ["effective_eligible_source_positions", "terrain_source_rows"],
        [],
    ),
    "project_adopted_integration": (
        [
            "effective_eligible_source_positions",
            "adopted_source_rows",
        ],
        [],
    ),
    "preserve_contested_unsettled": (
        [
            "effective_eligible_source_positions",
            "contested_source_metadata_rows",
        ],
        [],
    ),
    "apply_pre_access_accessibility": (
        [
            "effective_eligible_source_positions",
            "implicit_source_positions",
            "accessibility_snapshot_records",
        ],
        [],
    ),
    "project_accessible_implicit_trace": (
        ["accessible_implicit_positions", "implicit_source_rows"],
        [],
    ),
    "componentwise_max": (["contributing_direction_profiles"], []),
    "close_source_readout": (
        [
            "target_form_readout_profile",
            "accepted_source_projection_receipts",
            "unsettled_source_diagnostics",
            "accessibility_receipts",
            "declared_source_positions_ordered",
            "access_ordinal_k",
        ],
        [],
    ),
    "bind_opaque_sources": (
        ["semantic_decision"],
        ["opaque_scope_lineage"],
    ),
    "base_profile": (
        ["current_access_present", "source_materials_present", "base_encounter_profile"],
        [],
    ),
    "apply_reception_eligibility": (
        [
            "current_formation_transition_state",
            "reception_profile",
            "intervention_scope_match",
        ],
        [],
    ),
    "apply_target_directional_compatibility": (
        [
            "current_formation_transition_state",
            "target_form_profile",
            "intervention_scope_match",
        ],
        [],
    ),
    "emit_proxy": (["closed_formation_transition_state"], []),
    "ghost_seed": (
        ["current_access_present", "source_materials_present", "accessible_positions_ordered"],
        [],
    ),
    "canonical_traverse": (
        ["seed_positions", "accessible_positions_ordered", "normalized_topology_edges"],
        [],
    ),
    "broaden": (
        [
            "visited_positions_ordered",
            "positioned_material_profiles",
            "current_candidate_relation_state",
        ],
        [],
    ),
    "contrast": (["current_candidate_relation_state"], []),
    "counterfactual": (
        [
            "visited_positions_ordered",
            "positioned_material_profiles",
            "current_candidate_relation_state",
        ],
        [],
    ),
    "confirmation_only": (
        [
            "visited_positions_ordered",
            "positioned_material_profiles",
            "current_candidate_relation_state",
        ],
        [],
    ),
    "rehearsal": (["current_candidate_relation_state"], []),
    "project_visited_direction_candidates": (
        ["visited_positions_ordered", "positioned_material_profiles"],
        [],
    ),
    "apply_target_candidate_eligibility": (
        [
            "current_candidate_relation_state",
            "target_guidance_profile",
            "target_scope_match",
        ],
        [],
    ),
    "ghost_bind": (
        [
            "visited_positions_ordered",
            "current_candidate_relation_state",
        ],
        [],
    ),
    "close_ghost_semantic": (
        [
            "current_access_present",
            "source_materials_present",
            "accessible_positions_ordered",
            "visited_positions_ordered",
            "candidate_projection",
            "adjudication_projection",
            "candidate_state_stage_receipts",
        ],
        [],
    ),
    "d1_scoped_adjudicator_v1": (
        ["candidate_direction_set", "binding_relation"],
        [],
    ),
}


def _walk(value: object, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}/{index}")


def _validate_canonical_domain(envelope: dict[str, object]) -> None:
    canonical_root = envelope.get("manifest", envelope)
    for path, value in _walk(canonical_root):
        if value is None:
            raise ValueError(f"null forbidden at {path}")
        if isinstance(value, float):
            raise ValueError(f"float forbidden at {path}")
        if isinstance(value, int) and not isinstance(value, bool):
            if not 0 <= value <= 2**53 - 1:
                raise ValueError(f"integer outside canonical domain at {path}")
        if isinstance(value, dict):
            for key in value:
                if not key.isascii():
                    raise ValueError(f"non-ASCII object key at {path}")


def _ids(items: list[dict[str, object]], key: str) -> set[str]:
    values = [item[key] for item in items]
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {key}")
    return set(values)


def _require_integrity(
    envelope: dict[str, object],
    contract_key: str,
    *,
    check_integrity: bool,
) -> None:
    if not check_integrity:
        return
    manifest = envelope["manifest"]
    integrity = envelope["integrity"]
    if digest(manifest) != integrity["manifest_sha256"]:
        raise ValueError("manifest digest mismatch")
    if digest(manifest[contract_key]) != integrity["contract_sha256"]:
        raise ValueError("contract digest mismatch")


def _scope_equal(left: dict[str, object], right: dict[str, object]) -> bool:
    fields = (
        "actor_alias",
        "interpreted_target_scope_alias",
        "relation_scope_alias",
        "context_scope_alias",
    )
    return all(left[field] == right[field] for field in fields) and (
        canonical_bytes(left["target_resolution"])
        == canonical_bytes(right["target_resolution"])
    )


def _scope_mismatch_dimensions(
    left: dict[str, object], right: dict[str, object]
) -> set[str]:
    dimensions = {
        dimension
        for dimension, field in (
            ("actor", "actor_alias"),
            ("target", "interpreted_target_scope_alias"),
            ("relation", "relation_scope_alias"),
            ("context", "context_scope_alias"),
        )
        if left[field] != right[field]
    }
    if canonical_bytes(left["target_resolution"]) != canonical_bytes(
        right["target_resolution"]
    ):
        dimensions.add("target_resolution")
    return dimensions


def _eligible_accessibility_snapshots(
    fixture: dict[str, object],
) -> list[dict[str, object]]:
    return [
        record
        for record in fixture["source_records"]
        if record["source_kind"] == "pre_access_accessibility_snapshot"
        and _scope_equal(record["source_scope"], fixture["scope"])
        and record["effective_from_access_ordinal"] < fixture["access_ordinal_k"]
    ]


def _semantic_fixture_payload(
    fixture: dict[str, object],
    *,
    excluded: set[str],
) -> dict[str, object]:
    return {
        key: value
        for key, value in fixture.items()
        if key not in {"fixture_key", "isolated_ledger_key"} | excluded
    }


def _without_opaque_aliases(value: object) -> object:
    opaque_keys = {
        "actor_alias",
        "external_entity_alias",
        "fixture_key",
        "isolated_ledger_key",
        "source_alias",
    }
    if isinstance(value, dict):
        return {
            key: _without_opaque_aliases(child)
            for key, child in value.items()
            if key not in opaque_keys
        }
    if isinstance(value, list):
        return [_without_opaque_aliases(child) for child in value]
    return value


def _source_record_semantic(
    fixture: dict[str, object], record: dict[str, object]
) -> dict[str, object]:
    return {
        "source_position": record["source_position"],
        "source_kind": record["source_kind"],
        "effective_from_access_ordinal": record["effective_from_access_ordinal"],
        "direction_profile": record["direction_profile"],
        "status": record["status"],
        "exact_scope_match": _scope_equal(record["source_scope"], fixture["scope"]),
        "scope_mismatch_dimensions": sorted(
            _scope_mismatch_dimensions(record["source_scope"], fixture["scope"])
        ),
        "source_resolution_status": record["source_scope"]["target_resolution"][
            "status"
        ],
    }


def _model_catalog(contract: dict[str, object], block_id: str) -> dict[str, object]:
    key = {
        "SOURCE_COMPILER": "source_compilers",
        "ENCOUNTER_FORMATION": "formation_models",
        "GHOST_PATH": "ghost_models",
    }[block_id]
    return {item["model_id"]: item for item in contract[key]}


def _expanded_operator_sequence(
    contract: dict[str, object],
    block_id: str,
    fixture_key: str,
    model_id: str,
) -> list[str]:
    model = _model_catalog(contract, block_id)[model_id]
    sequence = list(model["operator_sequence"])
    if block_id != "GHOST_PATH":
        return sequence
    token = contract["operator_typed_dataflow_contract"][
        "ghost_sequence_expansion_token"
    ]
    uses_program = model["uses_declared_ghost_program"]
    policy = model["sequence_expansion_policy"]
    expected_policy = (
        "replace_fixture_operations_ordered_token_with_exact_fixture_declared_sequence"
        if uses_program
        else "none"
    )
    if policy != expected_policy or sequence.count(token) != int(uses_program):
        raise ValueError("Ghost sequence expansion contract changed")
    if uses_program:
        fixture = next(
            item for item in contract["ghost_fixtures"]
            if item["fixture_key"] == fixture_key
        )
        token_index = sequence.index(token)
        sequence[token_index : token_index + 1] = fixture["declared_ghost_program"][
            "operations_ordered"
        ]
    sequence.extend(contract["adjudicator_contract"]["post_candidate_tail_sequence"])
    return sequence


def _expanded_cell_sequences(
    contract: dict[str, object],
) -> dict[tuple[str, str, str], list[str]]:
    matrices = {
        item["block_id"]: item for item in contract["execution_matrices"]
    }
    return {
        (block_id, fixture_key, model_id): _expanded_operator_sequence(
            contract, block_id, fixture_key, model_id
        )
        for block_id, matrix in matrices.items()
        for fixture_key in matrix["fixture_keys"]
        for model_id in matrix["model_ids"]
    }


def _expected_operator_trace(
    execution: dict[str, object],
    block_id: str,
    fixture_key: str,
    model_id: str,
) -> list[dict[str, object]]:
    contract = execution["manifest"]["execution_contract"]
    declarations = {
        item["operator_id"]: item for item in contract["operator_declarations"]
    }
    adjudicator = contract["adjudicator_contract"]
    trace: list[dict[str, object]] = []
    for operator_id in _expanded_operator_sequence(
        contract, block_id, fixture_key, model_id
    ):
        if operator_id == adjudicator["policy_id"]:
            trace.append(
                {
                    "operator_id": operator_id,
                    "operator_version": adjudicator["policy_version"],
                    "phase": contract["operator_trace_phase_map"][operator_id],
                    "input_view_id": adjudicator["input_view_id"],
                    "inspected_field_ids": adjudicator["exact_inspected_field_ids"],
                    "opaque_pass_through_field_ids": adjudicator[
                        "exact_opaque_pass_through_field_ids"
                    ],
                    "output_kind": adjudicator["output_kind"],
                    "authority": adjudicator["writer_authority"],
                }
            )
            continue
        declaration = declarations[operator_id]
        trace.append(
            {
                "operator_id": operator_id,
                "operator_version": declaration["operator_version"],
                "phase": contract["operator_trace_phase_map"][operator_id],
                "input_view_id": declaration["input_view_id"],
                "inspected_field_ids": declaration["exact_inspected_field_ids"],
                "opaque_pass_through_field_ids": declaration[
                    "exact_opaque_pass_through_field_ids"
                ],
                "output_kind": declaration["output_kind"],
                "authority": declaration["authority"],
            }
        )
    return trace


def _content_digest_excluding_nested_member(
    envelope: dict[str, object],
    container_key: str,
    member_key: str,
) -> str:
    payload = deepcopy(envelope)
    del payload[container_key][member_key]
    return digest(payload)


def _validate_execution(
    execution: dict[str, object],
    *,
    check_integrity: bool = True,
) -> None:
    schema = load_exact(MANIFEST_SCHEMA_PATH)
    _validate_canonical_domain(execution)
    validate_json_schema(execution, schema)
    _require_integrity(execution, "execution_contract", check_integrity=check_integrity)

    manifest = execution["manifest"]
    contract = manifest["execution_contract"]
    if (
        manifest["manifest_id"],
        manifest["status"],
        contract["scope"]["execution_status"],
        contract["scope"]["runner_status"],
    ) != (
        "INTERP-001D1-V1-EXECUTION",
        "FROZEN_UNEXECUTED",
        "not_executed",
        "not_implemented",
    ):
        raise ValueError("D1 execution identity/status changed")
    identity_fields = {
        "actor_alias": "actor",
        "interpreted_target_scope_alias": "target",
        "relation_scope_alias": "relation",
        "context_scope_alias": "context",
        "external_entity_alias": "external",
        "source_alias": "source",
        "isolated_ledger_key": "ledger",
    }
    semantic_leak_tokens = {
        "control",
        "cycle",
        "decoy",
        "dev",
        "development",
        "future",
        "prefix",
        "scalar",
        "sealed",
        "structure",
        "terrain",
    }
    for path, value in _walk(contract):
        key = path.rsplit("/", 1)[-1]
        if key in identity_fields:
            if not isinstance(value, str) or re.fullmatch(
                rf"opaque\.{identity_fields[key]}\.[0-9]{{3}}", value
            ) is None:
                raise ValueError("execution identity alias is not role-blind")
            if any(token in value.lower() for token in semantic_leak_tokens):
                raise ValueError("execution identity alias leaks evaluator role")
    if any(
        "future_extension_probe" in fixture
        for fixture in contract["formation_fixtures"] + contract["ghost_fixtures"]
    ):
        raise ValueError("vacuous future-extension label leaked into D1")

    for document in manifest["governing_documents"]:
        source = ROOT / document["path"]
        if not source.is_file():
            raise ValueError("missing governing document")
        if hashlib.sha256(source.read_bytes()).hexdigest() != document["content_sha256"]:
            raise ValueError("governing document digest mismatch")

    matrices = {item["block_id"]: item for item in contract["execution_matrices"]}
    if set(matrices) != set(BLOCK_MODELS):
        raise ValueError("execution block catalog changed")
    expected_counts = {
        "SOURCE_COMPILER": 24,
        "ENCOUNTER_FORMATION": 32,
        "GHOST_PATH": 32,
    }
    total = 0
    for block, models in BLOCK_MODELS.items():
        matrix = matrices[block]
        expected_fixtures = [
            f"{BLOCK_FIXTURE_PREFIX[block]}{index:03d}"
            for index in range(1, 9)
        ]
        if matrix["fixture_keys"] != expected_fixtures:
            raise ValueError("fixture matrix order changed")
        if matrix["model_ids"] != list(models):
            raise ValueError("model matrix order changed")
        if matrix["cell_count"] != expected_counts[block]:
            raise ValueError("matrix cell count changed")
        total += matrix["cell_count"]
    if total != 88:
        raise ValueError("D1 total cell count changed")

    if contract["unit_contract"]["allowed_operations"] != [
        "equality",
        "ordering",
        "min",
        "max",
        "rank_threshold",
    ]:
        raise ValueError("ordinal operation contract changed")
    if not {
        "addition",
        "average",
        "difference",
        "division",
        "l1",
        "l2",
        "multiplication",
        "scalar_cancellation",
    } <= set(contract["unit_contract"]["forbidden_operations"]):
        raise ValueError("scalar arithmetic boundary weakened")
    if contract["phase_contract"] != {
        "phase_order": [
            "resolve_scope",
            "normalize_operator_input",
            "execute_detached_operator",
            "bind_opaque_lineage",
            "emit_guard_projection",
        ],
        "cross_block_data_flow": "forbidden_in_d1",
        "same_access_feedback": "forbidden",
        "source_effective_order": "source_effective_ordinal_strictly_less_than_access_ordinal_k",
        "back_edges": "forbidden",
        "future_prefix_rewrite": "forbidden",
    }:
        raise ValueError("phase/effective-order contract changed")
    if contract["identity_contract"]["scope_resolution"] != (
        "exact_actor_target_relation_context_and_canonical_target_resolution_"
        "equality_resolved_before_operator_as_boolean_or_position"
    ):
        raise ValueError("exact scope-resolution derivation changed")
    if contract["identity_contract"]["manifest_aliases"] != (
        "stable_role_blind_fixture_aliases_only_not_runtime_ids"
    ):
        raise ValueError("role-blind manifest alias contract changed")
    if contract["identity_contract"]["binder_rule"] != (
        "copy_exact_fixture_scope_object_to_scope_lineage_after_semantic_decision_"
        "without_field_inspection"
    ):
        raise ValueError("opaque scope-lineage binder rule changed")
    formation_state = contract["formation_transition_state_contract"]
    if formation_state["immutable_fields"] != [
        "current_access_present",
        "source_materials_present",
        "declared_base_encounter_profile",
    ] or formation_state["missing_reason_precedence"] != [
        "no_current_access",
        "no_source_material",
    ]:
        raise ValueError("formation transition-state closure changed")
    ghost_state = contract["ghost_candidate_state_contract"]
    if (
        ghost_state["activity_values"] != ["active", "inactive"]
        or ghost_state["inactive_reason_values"] != ["empty_traversal"]
        or ghost_state["stage_status_values"]
        != [
            "initialized_active",
            "initialized_inactive",
            "applied",
            "skipped_inactive",
            "skipped_scope_mismatch",
        ]
    ):
        raise ValueError("Ghost candidate-state activity contract changed")

    source_fixtures = contract["source_fixtures"]
    if _ids(source_fixtures, "fixture_key") != {
        f"srcfx{index:03d}" for index in range(1, 9)
    }:
        raise ValueError("source fixture catalog changed")
    source_kinds = {
        "narrative_terrain_fixture",
        "episode_integration_receipt_fixture",
        "contested_binding_receipt_fixture",
        "implicit_plastic_trace_fixture",
        "pre_access_accessibility_snapshot",
    }
    saw_future_source = False
    saw_scope_mismatch = False
    saw_withheld_accessibility = False
    saw_declared_missing_component = False
    isolated_scope_mismatch_dimensions: set[str] = set()
    for fixture in source_fixtures:
        records = fixture["source_records"]
        positions = [record["source_position"] for record in records]
        if len(positions) != len(set(positions)) or set(positions) != set(
            range(len(records))
        ):
            raise ValueError("source positions must be a complete unique zero-based set")
        if {record["source_kind"] for record in records} != source_kinds:
            raise ValueError("source kinds incomplete")
        for record in records:
            if "scope_match" in record:
                raise ValueError("derived scope-match flag must not be stored")
            computed_match = _scope_equal(record["source_scope"], fixture["scope"])
            mismatch_dimensions = _scope_mismatch_dimensions(
                record["source_scope"], fixture["scope"]
            )
            saw_scope_mismatch |= not computed_match
            if len(mismatch_dimensions) == 1:
                isolated_scope_mismatch_dimensions.update(mismatch_dimensions)
            saw_future_source |= (
                record["effective_from_access_ordinal"] >= fixture["access_ordinal_k"]
            )
            saw_withheld_accessibility |= (
                record["source_kind"] == "pre_access_accessibility_snapshot"
                and record["status"] == "withheld_fixture"
                and computed_match
                and record["effective_from_access_ordinal"]
                < fixture["access_ordinal_k"]
            )
            if (
                computed_match
                and record["effective_from_access_ordinal"]
                < fixture["access_ordinal_k"]
                and record["source_kind"] == "narrative_terrain_fixture"
                and any(
                    component["status"] == "missing"
                    for component in record["direction_profile"].values()
                )
            ):
                saw_declared_missing_component = True
        if len(_eligible_accessibility_snapshots(fixture)) != 1:
            raise ValueError(
                "source fixture must have exactly one eligible accessibility snapshot"
            )
    if not saw_scope_mismatch or not saw_future_source or not saw_withheld_accessibility:
        raise ValueError("scope/future-source controls missing")
    if isolated_scope_mismatch_dimensions != {
        "actor",
        "target",
        "relation",
        "context",
        "target_resolution",
    }:
        raise ValueError("isolated source scope-mismatch dimensions incomplete")
    if not saw_declared_missing_component:
        raise ValueError("source explicit-missing compiler control absent")
    source_by_key = {item["fixture_key"]: item for item in source_fixtures}
    accessible = deepcopy(source_by_key["srcfx005"])
    withheld = deepcopy(source_by_key["srcfx006"])
    accessible_snapshot = next(
        item for item in accessible["source_records"]
        if item["source_kind"] == "pre_access_accessibility_snapshot"
    )
    withheld_snapshot = next(
        item for item in withheld["source_records"]
        if item["source_kind"] == "pre_access_accessibility_snapshot"
    )
    if (
        accessible_snapshot["status"],
        withheld_snapshot["status"],
    ) != ("accessible_fixture", "withheld_fixture"):
        raise ValueError("accessibility matched-pair statuses changed")
    withheld_snapshot["status"] = "accessible_fixture"
    if canonical_bytes(_without_opaque_aliases(accessible)) != canonical_bytes(
        _without_opaque_aliases(withheld)
    ):
        raise ValueError("accessibility pair changes more than snapshot status")
    for fixture in (accessible, withheld):
        implicit = next(
            item for item in fixture["source_records"]
            if item["source_kind"] == "implicit_plastic_trace_fixture"
        )
        if not _scope_equal(implicit["source_scope"], fixture["scope"]):
            raise ValueError("accessibility pair implicit source is out of scope")
        if implicit["effective_from_access_ordinal"] >= fixture["access_ordinal_k"]:
            raise ValueError("accessibility pair implicit source is not pre-k")
    order_left = source_by_key["srcfx001"]
    order_right = source_by_key["srcfx002"]
    left_records = [
        _source_record_semantic(order_left, record)
        for record in order_left["source_records"]
    ]
    right_records = [
        _source_record_semantic(order_right, record)
        for record in order_right["source_records"]
    ]
    if [item["source_position"] for item in right_records] != list(
        reversed([item["source_position"] for item in left_records])
    ):
        raise ValueError("source-order mirror is not an exact reversal")
    if {
        item["source_position"]: item for item in left_records
    } != {
        item["source_position"]: item for item in right_records
    }:
        raise ValueError("source-order mirror changes semantic record content")
    prefix_left = source_by_key["srcfx007"]
    prefix_right = source_by_key["srcfx008"]
    right_pre_k = [
        record for record in prefix_right["source_records"]
        if record["effective_from_access_ordinal"] < prefix_right["access_ordinal_k"]
    ]
    right_post_k = [
        record for record in prefix_right["source_records"]
        if record["effective_from_access_ordinal"] >= prefix_right["access_ordinal_k"]
    ]
    if len(right_post_k) != 1 or not _scope_equal(
        right_post_k[0]["source_scope"], prefix_right["scope"]
    ):
        raise ValueError("source future-prefix pair lacks one exact-scope post-k source")
    if [
        _source_record_semantic(prefix_left, record)
        for record in prefix_left["source_records"]
    ] != [
        _source_record_semantic(prefix_right, record) for record in right_pre_k
    ]:
        raise ValueError("source future-prefix pair changes the pre-k semantic prefix")

    compilers = {item["model_id"]: item for item in contract["source_compilers"]}
    if set(compilers) != {"TF0", "TF1", "TF2"}:
        raise ValueError("source compiler catalog changed")
    if compilers["TF0"]["allowed_source_kinds"] != ["narrative_terrain_fixture"]:
        raise ValueError("TF0 source allowance changed")
    if not set(compilers["TF0"]["allowed_source_kinds"]) < set(
        compilers["TF1"]["allowed_source_kinds"]
    ) < set(compilers["TF2"]["allowed_source_kinds"]):
        raise ValueError("TF source model nesting changed")
    if any(item["outcome_input"] != "forbidden" for item in compilers.values()):
        raise ValueError("source compiler can inspect outcome")
    if any(
        item["operator_sequence"][-1] != "bind_opaque_sources"
        or item["operator_sequence"].count("bind_opaque_sources") != 1
        for item in compilers.values()
    ):
        raise ValueError("source lineage binder tail changed")
    dataflow = contract["source_dataflow_contract"]
    if dataflow != {
        "profile_aggregator_operator_id": "componentwise_max",
        "accepted_projection_operator_ids": [
            "project_narrative_terrain",
            "project_adopted_integration",
            "project_accessible_implicit_trace",
        ],
        "accepted_output_kind": "source_profile_projection",
        "no_present_component_output": {
            "status": "missing",
            "reason": "source_unresolved",
        },
        "forbidden_input_output_kinds": ["unsettled_source_diagnostic"],
        "unsettled_operator_id": "preserve_contested_unsettled",
        "unsettled_sink_fields": [
            "contested_present",
            "source_kinds_used",
            "eligible_source_positions_ordered",
        ],
        "accepted_projection_sink_fields": [
            "source_kinds_used",
            "eligible_source_positions_ordered",
        ],
        "accessibility_sink_fields": [
            "accessibility_relation",
            "source_kinds_used",
            "eligible_source_positions_ordered",
        ],
        "projection_receipt_cardinality": (
            "zero_or_more_exactly_one_receipt_per_joined_row"
        ),
        "empty_projection_collection_policy": (
            "valid_empty_collection_no_placeholder_receipt"
        ),
        "declared_order_input_field": "declared_source_positions_ordered",
        "ordered_union_policy": (
            "stable_filter_declared_order_by_unique_positions_from_accepted_"
            "unsettled_and_accessibility_receipts"
        ),
        "source_kind_order_policy": "duplicate_free_lexicographic",
        "contested_profile_sink": "forbidden",
        "wiring_policy": "exact_typed_edges_only_no_implicit_operator_output_flow",
    }:
        raise ValueError("source typed dataflow contract changed")

    formation = contract["formation_fixtures"]
    if _ids(formation, "fixture_key") != {
        f"encfx{index:03d}" for index in range(1, 9)
    }:
        raise ValueError("formation fixture catalog changed")
    by_key = {item["fixture_key"]: item for item in formation}
    pairs = (
        ("encfx001", "encfx002", {"declared_reception_intervention"}),
        ("encfx001", "encfx003", {"declared_target_form_intervention"}),
        ("encfx002", "encfx004", {"declared_target_form_intervention"}),
        ("encfx003", "encfx004", {"declared_reception_intervention"}),
        ("encfx005", "encfx006", {"declared_reception_intervention"}),
    )
    for left_key, right_key, factor in pairs:
        left = _semantic_fixture_payload(by_key[left_key], excluded=factor)
        right = _semantic_fixture_payload(by_key[right_key], excluded=factor)
        if canonical_bytes(left) != canonical_bytes(right):
            raise ValueError("formation matched pair changes more than one factor")
    if by_key["encfx007"]["current_access_present"] is not False:
        raise ValueError("no-current-access formation control missing")
    if by_key["encfx008"]["current_access_present"] is not True:
        raise ValueError("source-free access control missing access")
    if by_key["encfx008"]["source_materials_present"] is not False:
        raise ValueError("source-free formation control missing")
    for fixture_key in ("encfx005", "encfx006"):
        fixture = by_key[fixture_key]
        if _scope_equal(
            fixture["declared_target_form_intervention_scope"], fixture["scope"]
        ):
            raise ValueError("formation target-scope mismatch control missing")
        profile = fixture["declared_target_form_intervention"]
        ranks = {
            profile["positive_direction_support"].get("rank"),
            profile["negative_direction_support"].get("rank"),
        }
        if ranks != {0, 2}:
            raise ValueError("formation target-scope control is neutral")
    models = {item["model_id"]: item for item in contract["formation_models"]}
    expected_formation_bits = {
        "E0": (False, False),
        "ER": (True, False),
        "ET": (False, True),
        "ERT": (True, True),
    }
    for model_id, bits in expected_formation_bits.items():
        model = models[model_id]
        if (
            model["uses_reception_intervention"],
            model["uses_target_form_intervention"],
        ) != bits:
            raise ValueError("formation factor truth table changed")
        if model["cross_factor_arithmetic"] != "forbidden":
            raise ValueError("hidden R/T arithmetic enabled")
        if (
            model["operator_sequence"][-1] != "bind_opaque_sources"
            or model["operator_sequence"].count("bind_opaque_sources") != 1
        ):
            raise ValueError("formation lineage binder tail changed")

    ghost = contract["ghost_fixtures"]
    if _ids(ghost, "fixture_key") != {
        f"ghfx{index:03d}" for index in range(1, 9)
    }:
        raise ValueError("Ghost fixture catalog changed")
    ghost_by_key = {item["fixture_key"]: item for item in ghost}
    for fixture in ghost[:6]:
        positions = [
            item["position"] for item in fixture["accessible_materials_ordered"]
        ]
        if positions != [0, 1, 2, 3]:
            raise ValueError("exact-access Ghost positions changed")
        seen_edges: set[tuple[int, int]] = set()
        for edge in fixture["topology_edges"]:
            pair = tuple(sorted((edge["left_position"], edge["right_position"])))
            if pair[0] == pair[1] or pair in seen_edges:
                raise ValueError("invalid Ghost topology")
            if not set(pair) <= set(positions):
                raise ValueError("Ghost topology endpoint is not accessible")
            seen_edges.add(pair)
    if ghost_by_key["ghfx007"]["current_access_present"] is not False:
        raise ValueError("Ghost no-access control missing")
    if ghost_by_key["ghfx007"]["accessible_materials_ordered"]:
        raise ValueError("Ghost no-access control carries accessible material")
    if ghost_by_key["ghfx008"]["source_materials_present"] is not False:
        raise ValueError("Ghost source-free control missing")
    if ghost_by_key["ghfx008"]["accessible_materials_ordered"]:
        raise ValueError("Ghost source-free control carries accessible material")
    ghost_scope_control = ghost_by_key["ghfx006"]
    if ghost_scope_control["scope"]["target_resolution"]["status"] != "claimed":
        raise ValueError("Ghost unresolved-lineage preservation control missing")
    if _scope_equal(
        ghost_scope_control["target_guidance_scope"], ghost_scope_control["scope"]
    ):
        raise ValueError("Ghost target-scope mismatch control missing")
    ghost_guidance = ghost_scope_control["target_guidance_profile"]
    if {
        ghost_guidance["positive_direction_support"].get("rank"),
        ghost_guidance["negative_direction_support"].get("rank"),
    } != {0, 2}:
        raise ValueError("Ghost target-scope control is neutral")
    structural = lambda item: digest(
        _semantic_fixture_payload(item, excluded={"scope", "target_guidance_scope"})
    )
    dev_structures = {structural(item) for item in ghost[:4]}
    if any(structural(item) in dev_structures for item in ghost[4:]):
        raise ValueError("sealed Ghost fixture duplicates development structure")

    ghost_models = {item["model_id"]: item for item in contract["ghost_models"]}
    expected_ghost_bits = {
        "G0": (False, False),
        "GT": (True, False),
        "GP": (False, True),
        "GTP": (True, True),
    }
    for model_id, bits in expected_ghost_bits.items():
        model = ghost_models[model_id]
        if (
            model["uses_target_guidance"],
            model["uses_declared_ghost_program"],
        ) != bits:
            raise ValueError("Ghost factor truth table changed")
        if model["adjudication_authority"] != "none":
            raise ValueError("Ghost acquired adjudication authority")
        if "bind_opaque_sources" in model["operator_sequence"]:
            raise ValueError("Ghost model bypasses declared post-candidate tail")

    input_views = {
        item["view_id"]: item for item in contract["operator_input_views"]
    }
    if len(input_views) != len(contract["operator_input_views"]):
        raise ValueError("duplicate operator input view")
    global_inspectable = set(contract["operator_input_contract"]["inspectable_fields"])
    global_opaque = set(contract["operator_input_contract"]["opaque_pass_through_fields"])
    declared_inspectable: set[str] = set()
    declared_opaque: set[str] = set()
    for view in input_views.values():
        if set(view["forbidden_fields"]) != COMMON_FORBIDDEN_FIELDS:
            raise ValueError("operator forbidden-field closure changed")
        field_ids = _ids(view["fields"], "field_id")
        for field in view["fields"]:
            if field["operator_use"] == "inspect":
                if field["field_id"] in COMMON_FORBIDDEN_FIELDS:
                    raise ValueError("operator view exposes forbidden field")
                if field["field_id"] not in global_inspectable:
                    raise ValueError("operator view exposes undeclared inspect field")
                declared_inspectable.add(field["field_id"])
            elif field["field_id"] not in global_opaque:
                raise ValueError("undeclared opaque pass-through field")
            else:
                declared_opaque.add(field["field_id"])
        if field_ids & COMMON_FORBIDDEN_FIELDS:
            raise ValueError("identity/evaluation field in input view")
    if declared_inspectable != global_inspectable:
        raise ValueError("global inspect whitelist contains unused field")
    if declared_opaque != global_opaque:
        raise ValueError("global opaque whitelist contains unused field")

    operators = {
        item["operator_id"]: item for item in contract["operator_declarations"]
    }
    if len(operators) != len(contract["operator_declarations"]):
        raise ValueError("duplicate operator declaration")
    if contract["operator_trace_phase_map"] != EXPECTED_OPERATOR_PHASES:
        raise ValueError("operator trace phase catalog changed")
    dataflow = contract["source_dataflow_contract"]
    if any(
        operators[operator_id]["output_kind"] != dataflow["accepted_output_kind"]
        for operator_id in dataflow["accepted_projection_operator_ids"]
    ):
        raise ValueError("source contributing operator output kind changed")
    if operators[dataflow["unsettled_operator_id"]]["output_kind"] not in set(
        dataflow["forbidden_input_output_kinds"]
    ):
        raise ValueError("unsettled source output kind entered readout dataflow")
    if dataflow["declared_order_input_field"] != (
        "declared_source_positions_ordered"
    ) or dataflow["ordered_union_policy"] != (
        "stable_filter_declared_order_by_unique_positions_from_accepted_"
        "unsettled_and_accessibility_receipts"
    ):
        raise ValueError("source cross-kind declared-order closure changed")
    if (
        dataflow["projection_receipt_cardinality"]
        != "zero_or_more_exactly_one_receipt_per_joined_row"
        or dataflow["empty_projection_collection_policy"]
        != "valid_empty_collection_no_placeholder_receipt"
        or dataflow["contested_profile_sink"] != "forbidden"
    ):
        raise ValueError("source receipt cardinality or contested sink changed")
    used: set[str] = set()
    for model in contract["source_compilers"] + contract["formation_models"]:
        used.update(model["operator_sequence"])
    expansion_token = contract["operator_typed_dataflow_contract"][
        "ghost_sequence_expansion_token"
    ]
    for model in contract["ghost_models"]:
        used.update(
            operator_id for operator_id in model["operator_sequence"]
            if operator_id != expansion_token
        )
    for fixture in ghost:
        used.update(fixture["declared_ghost_program"]["operations_ordered"])
    used.update(
        operator_id
        for operator_id in contract["adjudicator_contract"][
            "post_candidate_tail_sequence"
        ]
        if operator_id != contract["adjudicator_contract"]["policy_id"]
    )
    if used != set(operators):
        raise ValueError("unknown or dead operator declaration")
    allowed_ordinal = set(contract["unit_contract"]["allowed_operations"])
    for operator in operators.values():
        if operator["input_view_id"] not in input_views:
            raise ValueError("dangling operator input view")
        expected_inspected, expected_opaque = EXPECTED_OPERATOR_ACCESS[
            operator["operator_id"]
        ]
        if operator["exact_inspected_field_ids"] != expected_inspected:
            raise ValueError("operator exact inspected-field catalog changed")
        if operator["exact_opaque_pass_through_field_ids"] != expected_opaque:
            raise ValueError("operator exact opaque pass-through catalog changed")
        view = input_views[operator["input_view_id"]]
        inspectable = {
            field["field_id"]
            for field in view["fields"]
            if field["operator_use"] == "inspect"
        }
        opaque = {
            field["field_id"]
            for field in view["fields"]
            if field["operator_use"] == "pass_through_only"
        }
        if not set(expected_inspected) <= inspectable:
            raise ValueError("operator inspected field is outside its registered view")
        if not set(expected_opaque) <= opaque:
            raise ValueError("operator opaque field is outside its registered view")
        if not set(operator["allowed_ordinal_operations"]) <= allowed_ordinal:
            raise ValueError("operator uses forbidden ordinal operation")
        if operator["identity_access"] != "forbidden":
            raise ValueError("operator can inspect identity")
        if operator["expected_output_access"] != "forbidden":
            raise ValueError("operator can inspect expected output")
        if operator["authority"] == "candidate_only" and operator["output_kind"].startswith(
            "adjudication"
        ):
            raise ValueError("candidate operator acquired adjudication output")

    adjudicator = contract["adjudicator_contract"]
    if adjudicator["writer_authority"] != "adjudication_only":
        raise ValueError("adjudicator authority changed")
    if adjudicator["ghost_model_input"] != "candidate_projection_only":
        raise ValueError("adjudicator reads beyond candidate")
    if (
        adjudicator["exact_inspected_field_ids"],
        adjudicator["exact_opaque_pass_through_field_ids"],
    ) != EXPECTED_OPERATOR_ACCESS["d1_scoped_adjudicator_v1"]:
        raise ValueError("adjudicator exact field access changed")
    if adjudicator["post_candidate_tail_sequence"] != [
        "d1_scoped_adjudicator_v1",
        "close_ghost_semantic",
        "bind_opaque_sources",
    ]:
        raise ValueError("Ghost post-candidate adjudicator/binder tail changed")

    typed = contract["operator_typed_dataflow_contract"]
    declarations = dict(operators)
    declarations[adjudicator["policy_id"]] = {
        "operator_id": adjudicator["policy_id"],
        "input_view_id": adjudicator["input_view_id"],
        "exact_inspected_field_ids": adjudicator["exact_inspected_field_ids"],
        "exact_opaque_pass_through_field_ids": adjudicator[
            "exact_opaque_pass_through_field_ids"
        ],
        "output_kind": adjudicator["output_kind"],
    }
    view_fields = {
        view_id: {field["field_id"]: field for field in view["fields"]}
        for view_id, view in input_views.items()
    }

    raw_pairs: set[tuple[str, str]] = set()
    for binding in typed["raw_input_bindings"]:
        operator_id = binding["operator_id"]
        if operator_id not in declarations:
            raise ValueError("typed raw binding references unknown operator")
        for field_id in binding["field_ids"]:
            pair = (operator_id, field_id)
            if pair in raw_pairs:
                raise ValueError("duplicate typed raw binding")
            raw_pairs.add(pair)

    preprocessors = {
        item["preprocessor_id"]: item
        for item in typed["deterministic_preprocessor_declarations"]
    }
    if len(preprocessors) != len(typed["deterministic_preprocessor_declarations"]):
        raise ValueError("duplicate deterministic preprocessor")
    expected_preprocessor_outputs = {
        "prep.source.scope_rows": "source_scope_rows",
        "prep.source.effective_rows": "source_effective_rows",
        "prep.source.terrain_rows": "terrain_source_rows",
        "prep.source.adopted_rows": "adopted_source_rows",
        "prep.source.contested_metadata_rows": "contested_source_metadata_rows",
        "prep.source.implicit_rows": "implicit_source_rows",
        "prep.source.implicit_positions": "implicit_source_positions",
        "prep.source.accessibility_snapshots": "accessibility_snapshot_records",
        "prep.source.declared_position_order": "declared_source_positions_ordered",
        "prep.formation.reception_scope_match": "intervention_scope_match",
        "prep.formation.target_scope_match": "intervention_scope_match",
        "prep.ghost.accessible_positions": "accessible_positions_ordered",
        "prep.ghost.topology": "normalized_topology_edges",
        "prep.ghost.positioned_material_profiles": "positioned_material_profiles",
        "prep.ghost.target_scope_match": "target_scope_match",
    }
    if {
        key: value["output_field_id"] for key, value in preprocessors.items()
    } != expected_preprocessor_outputs:
        raise ValueError("deterministic preprocessor catalog changed")
    declared_order_preprocessor = preprocessors[
        "prep.source.declared_position_order"
    ]
    if (
        declared_order_preprocessor["raw_source_paths"]
        != ["/fixture/source_records/*/source_position"]
        or declared_order_preprocessor["opcode_semantics"]
        != (
            "Copy every source_position exactly once in raw source-record "
            "declaration order. This order-only structural projection exposes "
            "no kind, profile, status, scope, identity, or eligibility and "
            "never sorts numerically."
        )
    ):
        raise ValueError("source declared-order preprocessor changed")
    preprocessed_pairs: set[tuple[str, str]] = set()
    for binding in typed["deterministic_preprocessor_bindings"]:
        operator_id = binding["operator_id"]
        field_id = binding["field_id"]
        preprocessor_id = binding["preprocessor_id"]
        if operator_id not in declarations or preprocessor_id not in preprocessors:
            raise ValueError("preprocessed binding references unknown declaration")
        preprocessor = preprocessors[preprocessor_id]
        if preprocessor["output_field_id"] != field_id:
            raise ValueError("preprocessor output field does not match binding")
        field = view_fields[declarations[operator_id]["input_view_id"]].get(field_id)
        if field is None or field["value_kind"] != preprocessor["output_value_kind"]:
            raise ValueError("preprocessor output kind does not match input view")
        pair = (operator_id, field_id)
        if pair in preprocessed_pairs:
            raise ValueError("duplicate preprocessed binding")
        preprocessed_pairs.add(pair)

    edge_pairs: set[tuple[str, str]] = set()
    edge_ids: set[str] = set()
    edges_by_consumer: dict[str, list[dict[str, object]]] = {}
    for edge in typed["edges"]:
        if edge["edge_id"] in edge_ids:
            raise ValueError("duplicate typed dataflow edge")
        edge_ids.add(edge["edge_id"])
        consumer_id = edge["consumer_operator_id"]
        if consumer_id not in declarations:
            raise ValueError("typed edge references unknown consumer")
        consumer_field = view_fields[
            declarations[consumer_id]["input_view_id"]
        ].get(edge["consumer_input_field_id"])
        if (
            consumer_field is None
            or consumer_field["value_kind"] != edge["consumer_value_kind"]
        ):
            raise ValueError("typed edge consumer field or value kind mismatch")
        if any(item not in declarations for item in edge["producer_operator_ids"]):
            raise ValueError("typed edge references unknown producer")
        actual_output_kinds = {
            declarations[item]["output_kind"]
            for item in edge["producer_operator_ids"]
        }
        if actual_output_kinds != set(edge["producer_output_kinds"]):
            raise ValueError("typed edge producer output kind mismatch")
        pair = (consumer_id, edge["consumer_input_field_id"])
        if pair in edge_pairs:
            raise ValueError("multiple typed edges compete for one consumer field")
        edge_pairs.add(pair)
        edges_by_consumer.setdefault(consumer_id, []).append(edge)

    inspected_pairs = {
        (operator_id, field_id)
        for operator_id, declaration in declarations.items()
        for field_id in declaration["exact_inspected_field_ids"]
    }
    if raw_pairs & preprocessed_pairs or raw_pairs & edge_pairs or preprocessed_pairs & edge_pairs:
        raise ValueError("operator input field has multiple authority sources")
    if raw_pairs | preprocessed_pairs | edge_pairs != inspected_pairs:
        raise ValueError("typed dataflow leaves hidden or unused inspected input")
    opaque_pairs: set[tuple[str, str]] = set()
    for binding in typed["raw_opaque_pass_through_bindings"]:
        pair = (binding["operator_id"], binding["field_id"])
        if pair in opaque_pairs:
            raise ValueError("duplicate opaque pass-through binding")
        opaque_pairs.add(pair)
        declaration = declarations.get(binding["operator_id"])
        if declaration is None:
            raise ValueError("opaque pass-through references unknown operator")
        field = view_fields[declaration["input_view_id"]].get(binding["field_id"])
        if (
            field is None
            or field["value_kind"] != binding["value_kind"]
            or field["operator_use"] != "pass_through_only"
        ):
            raise ValueError("opaque pass-through kind or view mismatch")
        if (
            binding["raw_source_path"] != "/fixture/scope"
            or binding["transfer_policy"]
            != "identity_pass_through_without_field_inspection"
        ):
            raise ValueError("opaque scope lineage lacks exact raw identity mapping")
    declared_opaque_pairs = {
        (operator_id, field_id)
        for operator_id, declaration in declarations.items()
        for field_id in declaration["exact_opaque_pass_through_field_ids"]
    }
    if opaque_pairs != declared_opaque_pairs:
        raise ValueError("opaque pass-through wiring is incomplete")

    pre_lineage = typed["pre_lineage_semantic_producers"]
    expected_pre_lineage = {
        "SOURCE_COMPILER": "close_source_readout",
        "ENCOUNTER_FORMATION": "emit_proxy",
        "GHOST_PATH": "close_ghost_semantic",
    }
    if pre_lineage != expected_pre_lineage:
        raise ValueError("pre-lineage semantic producer catalog changed")
    if typed["final_result_semantic_producer"] != "bind_opaque_sources":
        raise ValueError("final bound semantic producer changed")
    used_edges: set[str] = set()
    for (block_id, _fixture_key, _model_id), sequence in _expanded_cell_sequences(
        contract
    ).items():
        if any(operator_id not in declarations for operator_id in sequence):
            raise ValueError("expanded model sequence contains unknown operator")
        if sequence[-2:] != [pre_lineage[block_id], "bind_opaque_sources"]:
            raise ValueError("model sequence lacks unique closure-to-binder tail")
        for index, operator_id in enumerate(sequence):
            prior = sequence[:index]
            for edge in edges_by_consumer.get(operator_id, []):
                matches = [
                    candidate for candidate in prior
                    if candidate in edge["producer_operator_ids"]
                ]
                policy = edge["selection_policy"]
                if policy == "nearest_prior_one" and not matches:
                    raise ValueError("typed nearest-prior edge has no prior producer")
                if policy == "all_prior_matching_one_or_more" and not matches:
                    raise ValueError("typed collection edge has no prior producer")
                used_edges.add(edge["edge_id"])
    if used_edges != edge_ids:
        raise ValueError("dead typed dataflow edge")

    if contract["output_guard_contract"]["guard_ledger_names"] != EXPECTED_GUARDS:
        raise ValueError("guard ledger boundary changed")
    if contract["output_guard_contract"]["required_relation"] != (
        "before_sha256_equals_after_sha256_every_cell"
    ):
        raise ValueError("guard equality weakened")

    execution_text = json.dumps(execution, ensure_ascii=False, sort_keys=True)
    for forbidden_key in (
        '"development_fixture_keys"',
        '"sealed_fixture_keys"',
        '"semantic_signatures"',
        '"expected_by_model"',
        '"report_disclaimers"',
    ):
        if forbidden_key in execution_text:
            raise ValueError("evaluation content leaked into execution manifest")


def _resolve_ref(schema: dict[str, object], ref: str) -> dict[str, object]:
    if not ref.startswith("#/"):
        raise ValueError("only local refs are allowed")
    value: object = schema
    for segment in ref[2:].split("/"):
        value = value[segment]
    if not isinstance(value, dict):
        raise ValueError("schema ref did not resolve to object")
    return value


def _schema_nodes(
    schema: dict[str, object],
    start: dict[str, object],
    segments: list[str],
) -> list[dict[str, object]]:
    if "$ref" in start:
        return _schema_nodes(schema, _resolve_ref(schema, start["$ref"]), segments)
    if "oneOf" in start:
        return [
            result
            for branch in start["oneOf"]
            for result in _schema_nodes(schema, branch, segments)
        ]
    if segments and "allOf" in start:
        direct = {key: value for key, value in start.items() if key != "allOf"}
        return [
            *(_schema_nodes(schema, direct, segments) if direct else []),
            *(
                result
                for branch in start["allOf"]
                for result in _schema_nodes(schema, branch, segments)
            ),
        ]
    if not segments:
        return [start]
    segment = segments[0]
    if start.get("type") == "object":
        child = start.get("properties", {}).get(segment)
        return (
            _schema_nodes(schema, child, segments[1:])
            if isinstance(child, dict)
            else []
        )
    if start.get("type") == "array" and segment == "*":
        return _schema_nodes(schema, start["items"], segments[1:])
    return []


def _result_nodes_for_path(
    result_schema: dict[str, object],
    block_id: str,
    path: str,
) -> list[dict[str, object]]:
    if path.startswith("/operator_trace/"):
        segments = path[1:].split("/")
        return _schema_nodes(result_schema, result_schema, segments)
    if not path.startswith("/semantic/"):
        return []
    semantic_def = {
        "SOURCE_COMPILER": "sourceSemantic",
        "ENCOUNTER_FORMATION": "formationSemantic",
        "GHOST_PATH": "ghostSemantic",
    }[block_id]
    segments = path[len("/semantic/") :].split("/")
    return _schema_nodes(
        result_schema,
        result_schema["$defs"][semantic_def],
        segments,
    )


def _value_accepted(
    result_schema: dict[str, object],
    node: dict[str, object],
    value: object,
) -> bool:
    try:
        validate_json_schema(value, node, root_schema=result_schema)
    except ValueError:
        return False
    return True


def _operand_matches(
    kind: str,
    value: object,
    *,
    block_id: str | None,
    fixture_ids_by_block: dict[str, set[str]],
    projection_blocks: dict[str, str],
    challenger_blocks: dict[str, str],
    comparison_target_blocks: dict[str, str],
) -> bool:
    if kind in {
        "block_id",
        "fixture_key",
        "model_id",
        "combined_model_id",
        "single_model_id",
        "projection_id",
        "comparison_target_id",
        "challenger_id",
        "factor_id",
        "cell_selector",
        "metadata_value",
    } and not isinstance(value, str):
        return False
    if kind == "block_id":
        return value in BLOCK_MODELS
    if kind == "fixture_key":
        return value in (
            fixture_ids_by_block[block_id]
            if block_id is not None
            else set().union(*fixture_ids_by_block.values())
        )
    if kind in {"model_id", "combined_model_id", "single_model_id"}:
        return value in (
            set(BLOCK_MODELS[block_id])
            if block_id is not None
            else {item for values in BLOCK_MODELS.values() for item in values}
        )
    if kind == "projection_id":
        return value in projection_blocks and (
            block_id is None or projection_blocks[value] == block_id
        )
    if kind == "comparison_target_id":
        return value in comparison_target_blocks and (
            block_id is None or comparison_target_blocks[value] == block_id
        )
    if kind == "challenger_id":
        return value in challenger_blocks and (
            block_id is None or challenger_blocks[value] == block_id
        )
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "semantic_path":
        return isinstance(value, str) and value.startswith("/semantic/")
    return isinstance(value, (str, bool, int)) and not isinstance(value, float)


def _assertion_block(
    operand_kinds: list[str],
    operands: list[object],
    *,
    fixture_ids_by_block: dict[str, set[str]],
    challenger_blocks: dict[str, str],
) -> str | None:
    candidates: set[str] = set()
    for kind, value in zip(operand_kinds, operands):
        if kind == "block_id" and isinstance(value, str) and value in BLOCK_MODELS:
            candidates.add(value)
        elif kind == "fixture_key":
            candidates.update(
                block for block, fixture_ids in fixture_ids_by_block.items()
                if value in fixture_ids
            )
        elif kind in {"model_id", "combined_model_id", "single_model_id"}:
            candidates.update(
                block for block, models in BLOCK_MODELS.items() if value in models
            )
        elif kind == "challenger_id" and value in challenger_blocks:
            candidates.add(challenger_blocks[value])
    if len(candidates) > 1:
        raise ValueError("assertion operands cross block families")
    return next(iter(candidates), None)


def _validate_evaluation(
    evaluation: dict[str, object],
    execution: dict[str, object],
    *,
    check_integrity: bool = True,
) -> None:
    schema = load_exact(MANIFEST_SCHEMA_PATH)
    result_schema = load_exact(RESULT_SCHEMA_PATH)
    _validate_canonical_domain(evaluation)
    validate_json_schema(evaluation, schema)
    _require_integrity(evaluation, "evaluation_contract", check_integrity=check_integrity)

    manifest = evaluation["manifest"]
    contract = manifest["evaluation_contract"]
    if manifest["execution_manifest_sha256"] != execution["integrity"]["manifest_sha256"]:
        raise ValueError("evaluation is not bound to execution manifest")
    if contract["runner_visibility"] != "evaluation_manifest_forbidden":
        raise ValueError("runner can inspect evaluation")
    split = contract["synthetic_split_contract"]
    if (
        split["purpose"],
        split["independent_prediction_claim"],
    ) != ("evaluator_isolation_only", False):
        raise ValueError("synthetic split overclaimed")

    matrices = {
        item["block_id"]: item
        for item in execution["manifest"]["execution_contract"]["execution_matrices"]
    }
    assignments = {item["block_id"]: item for item in split["assignments"]}
    if set(assignments) != set(BLOCK_MODELS):
        raise ValueError("split block coverage changed")
    for block, assignment in assignments.items():
        if len(assignment["development_fixture_keys"]) != 4:
            raise ValueError("development split cardinality changed")
        if len(assignment["sealed_fixture_keys"]) != 4:
            raise ValueError("sealed split cardinality changed")
        if set(assignment["development_fixture_keys"]) & set(
            assignment["sealed_fixture_keys"]
        ):
            raise ValueError("development/sealed split overlaps")
        if set(assignment["development_fixture_keys"]) | set(
            assignment["sealed_fixture_keys"]
        ) != set(matrices[block]["fixture_keys"]):
            raise ValueError("split does not partition execution fixtures")

    signatures = {
        item["signature_id"]: item for item in contract["semantic_signatures"]
    }
    if len(signatures) != 88:
        raise ValueError("signature catalog must cover exactly 88 cells")
    expanded: list[tuple[str, str, str]] = []
    referenced_signatures: list[str] = []
    for assertion in contract["cell_assertions"]:
        block = assertion["block_id"]
        if set(assertion["expected_by_model"]) != set(BLOCK_MODELS[block]):
            raise ValueError("cell assertion model coverage changed")
        for model_id, signature_id in assertion["expected_by_model"].items():
            expanded.append((block, assertion["fixture_key"], model_id))
            referenced_signatures.append(signature_id)
            if signatures[signature_id]["block_id"] != block:
                raise ValueError("signature block mismatch")
    expected_cells = {
        (block, fixture, model)
        for block, matrix in matrices.items()
        for fixture in matrix["fixture_keys"]
        for model in matrix["model_ids"]
    }
    if set(expanded) != expected_cells or len(expanded) != 88:
        raise ValueError("cell assertion matrix is incomplete")
    if set(referenced_signatures) != set(signatures):
        raise ValueError("dead or multiply-unbound semantic signature")
    if len(referenced_signatures) != len(set(referenced_signatures)):
        raise ValueError("signature reused across cells")
    for signature in signatures.values():
        relations = {
            item["path"]: item["value"]
            for item in signature["expected_relations"]
        }
        if signature["signature_id"].startswith((
            "sig-srcfx001-",
            "sig-srcfx002-",
        )):
            profile = relations["/semantic/target_form_readout_profile"]
            if profile["negative_direction_support"] != {
                "status": "missing",
                "reason": "source_unresolved",
            }:
                raise ValueError("source tagged missing was cast to a rank")
        if signature["signature_id"].startswith("sig-ghfx006-"):
            if relations[
                "/semantic/scope_lineage/target_resolution/status"
            ] != "claimed":
                raise ValueError("claimed target resolution signature changed")
            if (
                "/semantic/scope_lineage/target_resolution/external_entity_alias"
                in relations
            ):
                raise ValueError("claimed target resolution invented external alias")

    predicate_ids = _ids(contract["predicate_declarations"], "predicate_id")
    predicate_map = {
        item["predicate_id"]: item for item in contract["predicate_declarations"]
    }
    expected_target_scoped_challenger_predicates = {
        "challenger_differs_on_fixture_target": [
            "fixture_key",
            "model_id",
            "challenger_id",
            "comparison_target_id",
        ],
        "challenger_equivalent_all_fixtures_target": [
            "block_id",
            "model_id",
            "challenger_id",
            "comparison_target_id",
        ],
    }
    for predicate_id, operand_kinds in (
        expected_target_scoped_challenger_predicates.items()
    ):
        declaration = predicate_map[predicate_id]
        if (
            declaration["arity"] != 4
            or declaration["operand_kinds"] != operand_kinds
        ):
            raise ValueError("challenger predicate lost target-scoped arity")
    used_predicates: set[str] = set()
    for signature in signatures.values():
        for relation in signature["expected_relations"]:
            predicate = relation["predicate"]
            used_predicates.add(predicate)
            nodes = _result_nodes_for_path(
                result_schema,
                signature["block_id"],
                relation["path"],
            )
            if not nodes:
                raise ValueError("signature path is outside result schema")
            value = relation["value"]
            if predicate == "eq":
                if not any(_value_accepted(result_schema, node, value) for node in nodes):
                    raise ValueError("eq value incompatible with result schema")
            elif predicate in {"set_eq", "ordered_eq"}:
                if not isinstance(value, list):
                    raise ValueError("array predicate requires array value")
                if predicate == "set_eq" and (
                    len(value) != len({canonical_bytes(item) for item in value})
                    or value != sorted(value)
                ):
                    raise ValueError("set_eq value is not a canonical true set")
                if not any(_value_accepted(result_schema, node, value) for node in nodes):
                    raise ValueError("array value incompatible with result schema")
            elif predicate == "count_eq":
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    raise ValueError("count_eq requires non-negative integer")
                if not any(node.get("type") == "array" for node in nodes):
                    raise ValueError("count_eq path is not an array")
            else:
                raise ValueError("unknown signature predicate")

    projections = {
        item["projection_id"]: item
        for item in contract["substantive_comparison_projections"]
    }
    if set(projections) != {
        "SOURCE_SUBSTANTIVE",
        "FORMATION_SUBSTANTIVE",
        "GHOST_ACCESS",
        "GHOST_SUBSTANTIVE",
    }:
        raise ValueError("substantive projection catalog changed")
    for projection in projections.values():
        included = set(projection["included_result_paths"])
        excluded = set(projection["excluded_bookkeeping_paths"])
        if included & BOOKKEEPING_PATHS:
            raise ValueError("bookkeeping leaked into substantive projection")
        if not excluded <= BOOKKEEPING_PATHS:
            raise ValueError("comparison projection does not explicitly exclude bookkeeping")
        for path in included:
            if not _result_nodes_for_path(result_schema, projection["block_id"], path):
                raise ValueError("comparison projection path outside result schema")

    comparison_targets = {
        item["comparison_target_id"]: item
        for item in contract["common_comparison_targets"]
    }
    expected_target_fields = {
        "SOURCE_READOUT_TARGET": (
            "SOURCE_COMPILER",
            {"target_form_readout_profile": "direction_profile"},
        ),
        "FORMATION_DIRECTION_TARGET": (
            "ENCOUNTER_FORMATION",
            {
                "encounter_emitted": "boolean",
                "eligible_directions": "direction_set",
            },
        ),
        "GHOST_CANDIDATE_TARGET": (
            "GHOST_PATH",
            {
                "binding_candidate_directions": "direction_set",
                "binding_relation": "binding_relation",
                "adjudication_outcome": "adjudication_outcome",
            },
        ),
    }
    if set(comparison_targets) != set(expected_target_fields):
        raise ValueError("common comparison target catalog changed")
    for target_id, target in comparison_targets.items():
        expected_block, expected_fields = expected_target_fields[target_id]
        actual_fields = {
            field["field_id"]: field["value_kind"] for field in target["fields"]
        }
        if target["block_id"] != expected_block or actual_fields != expected_fields:
            raise ValueError("comparison target block or field shape mismatch")
        if set(target["model_adapter"]["output_fields"]) != set(expected_fields):
            raise ValueError("model adapter output does not close target shape")
        for path in target["model_adapter"]["input_result_paths"]:
            if not _result_nodes_for_path(result_schema, target["block_id"], path):
                raise ValueError("model adapter path outside result schema")
        if target["mismatch_policy"] != "CONTRACT_ERROR_never_substantive_difference":
            raise ValueError("comparison target mismatch can masquerade as difference")

    challenger_blocks = {
        item["challenger_id"]: item["block_id"]
        for item in contract["challenger_declarations"]
    }
    challenger_ids = _ids(contract["challenger_declarations"], "challenger_id")
    if len(challenger_ids) != 9 or len(challenger_blocks) != 9:
        raise ValueError("challenger catalog cardinality changed")
    expected_opcodes = {
        "source_kind_blind_componentwise_max",
        "material_count_or_max_profile",
        "base_encounter_passthrough",
        "dominant_direction_category",
        "fixed_rank_activation_threshold",
        "reception_target_congruence_boolean",
        "declared_rt_lookup",
        "visited_direction_set_only",
        "fixed_ghost_baseline",
    }
    if {item["opcode"] for item in contract["challenger_declarations"]} != expected_opcodes:
        raise ValueError("challenger opcode catalog changed")
    if any(not item["algorithm_steps"] for item in contract["challenger_declarations"]):
        raise ValueError("challenger lacks executable algorithm steps")
    target_blocks = {
        target_id: target["block_id"] for target_id, target in comparison_targets.items()
    }
    for challenger in contract["challenger_declarations"]:
        target_id = challenger["comparison_target_id"]
        if target_id not in comparison_targets:
            raise ValueError("challenger references unknown comparison target")
        target = comparison_targets[target_id]
        adapter = challenger["comparison_adapter"]
        expected_fields = {item["field_id"] for item in target["fields"]}
        if challenger["block_id"] != target["block_id"]:
            raise ValueError("challenger comparison target crosses blocks")
        if set(adapter["output_fields"]) != expected_fields:
            raise ValueError("challenger adapter does not emit exact target shape")
        if adapter["mismatch_policy"] != "CONTRACT_ERROR_never_substantive_difference":
            raise ValueError("challenger representation mismatch is not a contract error")
        ghost_policy = (
            "derive_only_with_D1_FIXED_ADJUDICATOR_V1"
            if challenger["block_id"] == "GHOST_PATH"
            else "none"
        )
        if adapter["adjudicator_policy"] != ghost_policy:
            raise ValueError("challenger adjudicator policy changed")
        if any("adjudication" in path for path in adapter["input_paths"]):
            raise ValueError("challenger adapter can inject adjudication")
        if adapter["expected_output_access"] != "forbidden":
            raise ValueError("challenger adapter can inspect expected output")
        if any(path.endswith("/scope_match") for path in challenger["input_paths"]):
            raise ValueError("challenger consumes stored derived scope match")
    challenger_roles = {
        item["challenger_id"]: item["challenger_role"]
        for item in contract["challenger_declarations"]
    }
    expected_challenger_roles = {
        challenger_id: "distinct_challenger" for challenger_id in challenger_ids
    }
    expected_challenger_roles.update(
        {
            "CH_RT_CONGRUENCE": "algebraic_alias_control_reference",
            "CH_DECLARED_RT_LOOKUP": "algebraic_alias_control_replica",
        }
    )
    if challenger_roles != expected_challenger_roles:
        raise ValueError("challenger role catalog changed")

    fixture_ids_by_block = {
        block: set(matrix["fixture_keys"]) for block, matrix in matrices.items()
    }
    projection_blocks = {
        projection_id: projection["block_id"]
        for projection_id, projection in projections.items()
    }
    named = contract["pair_assertions"] + contract["global_invariants"]
    for assertion in named:
        if assertion["predicate_id"] not in predicate_map:
            raise ValueError("assertion references undeclared predicate")
        declaration = predicate_map[assertion["predicate_id"]]
        if len(assertion["operands"]) != declaration["arity"]:
            raise ValueError("assertion predicate arity mismatch")
        if len(declaration["operand_kinds"]) != declaration["arity"]:
            raise ValueError("predicate operand-kind arity mismatch")
        assertion_block = _assertion_block(
            declaration["operand_kinds"],
            assertion["operands"],
            fixture_ids_by_block=fixture_ids_by_block,
            challenger_blocks=challenger_blocks,
        )
        for kind, value in zip(declaration["operand_kinds"], assertion["operands"]):
            if not _operand_matches(
                kind,
                value,
                block_id=assertion_block,
                fixture_ids_by_block=fixture_ids_by_block,
                projection_blocks=projection_blocks,
                challenger_blocks=challenger_blocks,
                comparison_target_blocks=target_blocks,
            ):
                raise ValueError("assertion predicate operand kind mismatch")
        used_predicates.add(assertion["predicate_id"])

    globals_by_predicate: dict[str, list[list[object]]] = {}
    for assertion in contract["global_invariants"]:
        globals_by_predicate.setdefault(assertion["predicate_id"], []).append(
            assertion["operands"]
        )
    exact_block_globals = {
        "guard_ledgers_unchanged_all_cells",
        "cell_integrity_exact_all_cells",
        "cell_execution_binding_exact_all_cells",
        "operator_trace_exact_all_cells",
        "operator_typed_dataflow_exact_all_cells",
        "scope_lineage_exact_all_cells",
    }
    expected_block_operands = [[block] for block in BLOCK_MODELS]
    for predicate_id in exact_block_globals:
        if globals_by_predicate.get(predicate_id) != expected_block_operands:
            raise ValueError(f"required block-global invariant changed: {predicate_id}")
    required_singletons = {
        "run_matrix_complete_exact": [[88]],
        "run_carrier_execution_binding_exact": [[88]],
        "run_carrier_runner_blinding_exact": [[False]],
        "run_carrier_integrity_exact": [["interp-canonical-json-v1"]],
        "runner_evaluation_access_absent": [["execution_manifest_only"]],
        "challenger_algebraic_alias_equal_all_fixtures_target": [[
            "CH_RT_CONGRUENCE",
            "CH_DECLARED_RT_LOOKUP",
            "FORMATION_DIRECTION_TARGET",
        ]],
    }
    for predicate_id, operands in required_singletons.items():
        if globals_by_predicate.get(predicate_id) != operands:
            raise ValueError(f"required global invariant changed: {predicate_id}")
    if globals_by_predicate.get("source_tagged_missing_preserved") != [
        ["srcfx001", "TF0"],
        ["srcfx001", "TF1"],
        ["srcfx001", "TF2"],
    ]:
        raise ValueError("source tagged-missing global coverage changed")

    for rule in contract["retirement_rules"]:
        if rule["freeze_status"] != "NOT_EVALUATED":
            raise ValueError("unexecuted retirement rule has a result")
        if rule["condition_predicate_id"] not in predicate_map:
            raise ValueError("retirement references undeclared predicate")
        declaration = predicate_map[rule["condition_predicate_id"]]
        if len(rule["condition_operands"]) != declaration["arity"]:
            raise ValueError("retirement predicate arity mismatch")
        assertion_block = _assertion_block(
            declaration["operand_kinds"],
            rule["condition_operands"],
            fixture_ids_by_block=fixture_ids_by_block,
            challenger_blocks=challenger_blocks,
        )
        for kind, value in zip(declaration["operand_kinds"], rule["condition_operands"]):
            if not _operand_matches(
                kind,
                value,
                block_id=assertion_block,
                fixture_ids_by_block=fixture_ids_by_block,
                projection_blocks=projection_blocks,
                challenger_blocks=challenger_blocks,
                comparison_target_blocks=target_blocks,
            ):
                raise ValueError("retirement operand kind mismatch")
        used_predicates.add(rule["condition_predicate_id"])

    if used_predicates != predicate_ids:
        raise ValueError("dead predicate declaration")
    disclaimers = "\n".join(contract["report_disclaimers"])
    for phrase in (
        "not an independent predictive split",
        "not executed results",
        "not a durable TargetForm state",
        "not qualia",
        "not predictive or human-empirical support",
    ):
        if phrase not in disclaimers:
            raise ValueError("required non-overclaim disclaimer missing")


def _validate_result_envelope(
    result: dict[str, object],
    execution: dict[str, object] | None = None,
    *,
    check_integrity: bool = True,
) -> None:
    execution = execution or load_exact(EXECUTION_PATH)
    schema = load_exact(RESULT_SCHEMA_PATH)
    _validate_canonical_domain(result)
    validate_json_schema(result, schema)
    if result["execution_manifest_sha256"] != execution["integrity"][
        "manifest_sha256"
    ]:
        raise ValueError("result execution manifest binding mismatch")
    if result["execution_contract_sha256"] != execution["integrity"][
        "contract_sha256"
    ]:
        raise ValueError("result execution contract binding mismatch")
    block = result["block_id"]
    expected = {
        "SOURCE_COMPILER": (set(BLOCK_MODELS["SOURCE_COMPILER"]), "source_compiler", "srcfx"),
        "ENCOUNTER_FORMATION": (
            set(BLOCK_MODELS["ENCOUNTER_FORMATION"]),
            "encounter_formation",
            "encfx",
        ),
        "GHOST_PATH": (set(BLOCK_MODELS["GHOST_PATH"]), "ghost_path", "ghfx"),
    }
    models, semantic_kind, fixture_prefix = expected[block]
    if result["model_id"] not in models:
        raise ValueError("result model does not belong to result block")
    if result["semantic"]["semantic_kind"] != semantic_kind:
        raise ValueError("result semantic shape does not belong to result block")
    if not result["fixture_key"].startswith(fixture_prefix):
        raise ValueError("result fixture does not belong to result block")
    contract = execution["manifest"]["execution_contract"]
    matrices = {
        item["block_id"]: item
        for item in contract["execution_matrices"]
    }
    if result["fixture_key"] not in matrices[block]["fixture_keys"]:
        raise ValueError("result fixture is outside the frozen result block")
    if result["cell_key"] != ":".join(
        (block, result["fixture_key"], result["model_id"])
    ):
        raise ValueError("result cell key is not the exact block/fixture/model key")
    fixture_key = {
        "SOURCE_COMPILER": "source_fixtures",
        "ENCOUNTER_FORMATION": "formation_fixtures",
        "GHOST_PATH": "ghost_fixtures",
    }[block]
    fixture = next(
        item for item in contract[fixture_key]
        if item["fixture_key"] == result["fixture_key"]
    )
    semantic = result["semantic"]
    if semantic["scope_lineage"] != fixture["scope"]:
        raise ValueError("result scope lineage is not the exact fixture scope object")
    if block == "SOURCE_COMPILER":
        if (
            semantic["access_ordinal_k"] != fixture["access_ordinal_k"]
            or semantic["effective_before_access_ordinal"]
            != semantic["access_ordinal_k"]
        ):
            raise ValueError("source result effective-order boundary mismatch")
        positions = semantic["eligible_source_positions_ordered"]
        if semantic["eligible_source_position_count"] != len(positions):
            raise ValueError("source result eligible-position count mismatch")
        kinds = semantic["source_kinds_used"]
        if kinds != sorted(set(kinds)):
            raise ValueError("source kinds are not a canonical lexicographic set")
    if block == "ENCOUNTER_FORMATION":
        exact_orders = {
            "E0": ["base_profile", "emit_proxy"],
            "ER": ["base_profile", "apply_reception_eligibility", "emit_proxy"],
            "ET": [
                "base_profile",
                "apply_target_directional_compatibility",
                "emit_proxy",
            ],
            "ERT": [
                "base_profile",
                "apply_target_directional_compatibility",
                "apply_reception_eligibility",
                "emit_proxy",
            ],
        }
        if result["semantic"]["formation_operator_order"] != exact_orders[
            result["model_id"]
        ]:
            raise ValueError("formation result operator order does not match model")
        if (
            semantic["current_access_present"]
            != fixture["current_access_present"]
            or semantic["source_materials_present"]
            != fixture["source_materials_present"]
            or semantic["base_encounter_profile"]
            != fixture["base_encounter_profile"]
        ):
            raise ValueError("formation result lost immutable transition-state fields")
        if semantic["encounter_emitted"] != (
            fixture["current_access_present"]
            and fixture["source_materials_present"]
        ):
            raise ValueError("formation emitted flag contradicts access/source state")
        if result["model_id"] in {"E0", "ET"} and semantic[
            "reception_intervention_used"
        ]:
            raise ValueError("formation result used undeclared reception factor")
        if result["model_id"] in {"E0", "ER"} and semantic[
            "target_form_intervention_used"
        ]:
            raise ValueError("formation result used undeclared target factor")
    if block == "GHOST_PATH":
        if (
            semantic["current_access_present"]
            != fixture["current_access_present"]
            or semantic["source_materials_present"]
            != fixture["source_materials_present"]
        ):
            raise ValueError("Ghost result access/source flags changed")
        accessible_positions = [
            item["position"] for item in fixture["accessible_materials_ordered"]
        ]
        if semantic["accessed_material_positions_ordered"] != accessible_positions:
            raise ValueError("Ghost result lost original accessible position order")
        ghost_model = _model_catalog(contract, block)[result["model_id"]]
        active = bool(
            fixture["current_access_present"]
            and fixture["source_materials_present"]
            and accessible_positions
        )
        expected_target_used = bool(
            active
            and ghost_model["uses_target_guidance"]
            and _scope_equal(fixture["target_guidance_scope"], fixture["scope"])
        )
        expected_program_used = bool(
            active and ghost_model["uses_declared_ghost_program"]
        )
        if (
            semantic["target_guidance_used"] != expected_target_used
            or semantic["ghost_program_used"] != expected_program_used
        ):
            raise ValueError("Ghost used flags are not applied-stage semantics")
        expected_relations = (
            fixture["declared_ghost_program"]["operations_ordered"]
            if expected_program_used
            else []
        )
        candidate = semantic["candidate_projection"]
        if candidate["registered_operation_relations"] != expected_relations:
            raise ValueError("Ghost registered relations include skipped invocation")
        truth_table = {
            (): ("none", "deferred"),
            ("negative",): ("single_direction", "adopted_negative"),
            ("positive",): ("single_direction", "adopted_positive"),
            ("negative", "positive"): ("contested", "contested"),
        }
        expected_relation, expected_outcome = truth_table[
            tuple(candidate["binding_candidate_directions"])
        ]
        if (
            candidate["binding_relation"] != expected_relation
            or semantic["adjudication_projection"]["adjudication_outcome"]
            != expected_outcome
        ):
            raise ValueError("Ghost raw result violates fixed truth table")
    expected_trace = _expected_operator_trace(
        execution,
        block,
        result["fixture_key"],
        result["model_id"],
    )
    if result["operator_trace"] != expected_trace:
        raise ValueError("result operator trace is not the exact expanded trace")
    if check_integrity:
        expected_content_digest = _content_digest_excluding_nested_member(
            result, "integrity", "cell_content_sha256"
        )
        if result["integrity"]["cell_content_sha256"] != expected_content_digest:
            raise ValueError("result cell content digest mismatch")
    branches = schema["allOf"][0]["oneOf"]
    declared = {
        branch["properties"]["block_id"]["const"]: (
            set(branch["properties"]["model_id"]["enum"]),
            branch["properties"]["semantic"]["$ref"],
        )
        for branch in branches
    }
    if declared != {
        "SOURCE_COMPILER": (set(BLOCK_MODELS["SOURCE_COMPILER"]), "#/$defs/sourceSemantic"),
        "ENCOUNTER_FORMATION": (
            set(BLOCK_MODELS["ENCOUNTER_FORMATION"]),
            "#/$defs/formationSemantic",
        ),
        "GHOST_PATH": (set(BLOCK_MODELS["GHOST_PATH"]), "#/$defs/ghostSemantic"),
    }:
        raise ValueError("formal result branch coupling changed")


def _validate_adapted_target(
    evaluation: dict[str, object],
    comparison_target_id: str,
    value: dict[str, object],
) -> None:
    targets = {
        item["comparison_target_id"]: item
        for item in evaluation["manifest"]["evaluation_contract"][
            "common_comparison_targets"
        ]
    }
    target = targets[comparison_target_id]
    kinds = {item["field_id"]: item["value_kind"] for item in target["fields"]}
    if set(value) != set(kinds):
        raise ValueError("adapted target shape mismatch")
    result_schema = load_exact(RESULT_SCHEMA_PATH)
    for field, kind in kinds.items():
        item = value[field]
        if kind == "boolean" and not isinstance(item, bool):
            raise ValueError("adapted target type mismatch")
        if kind == "direction_profile":
            validate_json_schema(
                item,
                result_schema["$defs"]["directionProfile"],
                root_schema=result_schema,
            )
        if kind == "direction_set" and (
            not isinstance(item, list)
            or item != sorted(item)
            or len(item) != len(set(item))
            or not set(item) <= {"negative", "positive"}
        ):
            raise ValueError("adapted target type mismatch")
        if kind == "binding_relation" and item not in {
            "none",
            "single_direction",
            "contested",
        }:
            raise ValueError("adapted target type mismatch")
        if kind == "adjudication_outcome" and item not in {
            "deferred",
            "adopted_negative",
            "adopted_positive",
            "contested",
        }:
            raise ValueError("adapted target type mismatch")
    if (
        comparison_target_id == "FORMATION_DIRECTION_TARGET"
        and value["encounter_emitted"] is False
        and value["eligible_directions"]
    ):
        raise ValueError("formation adapted target emits directions without encounter")
    if comparison_target_id == "GHOST_CANDIDATE_TARGET":
        truth_table = {
            (): ("none", "deferred"),
            ("negative",): ("single_direction", "adopted_negative"),
            ("positive",): ("single_direction", "adopted_positive"),
            ("negative", "positive"): ("contested", "contested"),
        }
        directions = tuple(value["binding_candidate_directions"])
        expected_relation, expected_adjudication = truth_table[directions]
        if (
            value["binding_relation"],
            value["adjudication_outcome"],
        ) != (expected_relation, expected_adjudication):
            raise ValueError("Ghost adapted target violates frozen truth table")


def _adapted_targets_differ(
    evaluation: dict[str, object],
    comparison_target_id: str,
    model_value: dict[str, object],
    challenger_value: dict[str, object],
) -> bool:
    _validate_adapted_target(evaluation, comparison_target_id, model_value)
    _validate_adapted_target(evaluation, comparison_target_id, challenger_value)
    return canonical_bytes(model_value) != canonical_bytes(challenger_value)


def _formation_ert_and_lookup_targets(
    fixture: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    if not fixture["current_access_present"] or not fixture["source_materials_present"]:
        empty = {"encounter_emitted": False, "eligible_directions": []}
        return deepcopy(empty), deepcopy(empty)
    base = fixture["base_encounter_profile"]
    reception = fixture["declared_reception_intervention"]
    target = fixture["declared_target_form_intervention"]
    reception_match = _scope_equal(
        fixture["declared_reception_intervention_scope"], fixture["scope"]
    )
    target_match = _scope_equal(
        fixture["declared_target_form_intervention_scope"], fixture["scope"]
    )
    directions: list[str] = []
    lookup_directions: list[str] = []
    for direction in ("negative", "positive"):
        base_rank = base[f"{direction}_direction_fit"]["rank"]
        reception_rank = reception[f"{direction}_direction_receptivity"]["rank"]
        target_rank = target[f"{direction}_direction_support"]["rank"]
        ert_rank = min(
            base_rank,
            reception_rank if reception_match else base_rank,
            target_rank if target_match else base_rank,
        )
        if ert_rank >= 1:
            directions.append(direction)
        lookup_eligible = (
            base_rank >= 1
            and (not reception_match or reception_rank >= 1)
            and (not target_match or target_rank >= 1)
        )
        if lookup_eligible:
            lookup_directions.append(direction)
    return (
        {"encounter_emitted": True, "eligible_directions": directions},
        {"encounter_emitted": True, "eligible_directions": lookup_directions},
    )


def _result_example(
    block: str,
    *,
    fixture: str | None = None,
    model: str | None = None,
    execution: dict[str, object] | None = None,
) -> dict[str, object]:
    execution = execution or load_exact(EXECUTION_PATH)
    zero = "0" * 64
    component = {"status": "present", "rank": 1}
    direction = {
        "positive_direction_support": deepcopy(component),
        "negative_direction_support": deepcopy(component),
    }
    encounter = {
        "positive_direction_fit": deepcopy(component),
        "negative_direction_fit": deepcopy(component),
        "ambiguity": deepcopy(component),
        "activation": deepcopy(component),
    }
    contract = execution["manifest"]["execution_contract"]
    if block == "SOURCE_COMPILER":
        fixture = fixture or "srcfx001"
        model = model or "TF0"
        fixture_data = next(
            item for item in contract["source_fixtures"]
            if item["fixture_key"] == fixture
        )
        semantic = {
            "semantic_kind": "source_compiler",
            "scope_lineage": deepcopy(fixture_data["scope"]),
            "access_ordinal_k": fixture_data["access_ordinal_k"],
            "source_kinds_used": ["narrative_terrain_fixture"],
            "target_form_readout_profile": direction,
            "contested_present": False,
            "accessibility_relation": "not_applicable",
            "effective_before_access_ordinal": fixture_data["access_ordinal_k"],
            "eligible_source_position_count": 1,
            "eligible_source_positions_ordered": [0],
        }
    elif block == "ENCOUNTER_FORMATION":
        fixture = fixture or "encfx001"
        model = model or "E0"
        fixture_data = next(
            item for item in contract["formation_fixtures"]
            if item["fixture_key"] == fixture
        )
        formation_orders = {
            "E0": ["base_profile", "emit_proxy"],
            "ER": ["base_profile", "apply_reception_eligibility", "emit_proxy"],
            "ET": [
                "base_profile",
                "apply_target_directional_compatibility",
                "emit_proxy",
            ],
            "ERT": [
                "base_profile",
                "apply_target_directional_compatibility",
                "apply_reception_eligibility",
                "emit_proxy",
            ],
        }
        emitted = bool(
            fixture_data["current_access_present"]
            and fixture_data["source_materials_present"]
        )
        if emitted:
            formed: dict[str, object] = deepcopy(
                fixture_data["base_encounter_profile"]
            )
        else:
            reason = (
                "no_current_access"
                if not fixture_data["current_access_present"]
                else "no_source_material"
            )
            formed = {"status": "missing", "reason": reason}
        reception_used = bool(
            emitted
            and model in {"ER", "ERT"}
            and _scope_equal(
                fixture_data["declared_reception_intervention_scope"],
                fixture_data["scope"],
            )
        )
        target_used = bool(
            emitted
            and model in {"ET", "ERT"}
            and _scope_equal(
                fixture_data["declared_target_form_intervention_scope"],
                fixture_data["scope"],
            )
        )
        semantic = {
            "semantic_kind": "encounter_formation",
            "scope_lineage": deepcopy(fixture_data["scope"]),
            "current_access_present": fixture_data["current_access_present"],
            "source_materials_present": fixture_data["source_materials_present"],
            "encounter_emitted": emitted,
            "base_encounter_profile": deepcopy(
                fixture_data["base_encounter_profile"]
            ),
            "formed_encounter_profile": formed,
            "reception_intervention_used": reception_used,
            "target_form_intervention_used": target_used,
            "formation_operator_order": formation_orders[model],
        }
    else:
        fixture = fixture or "ghfx001"
        model = model or "G0"
        ghost_model = _model_catalog(
            contract, block
        )[model]
        ghost_fixture = next(
            item for item in contract["ghost_fixtures"]
            if item["fixture_key"] == fixture
        )
        accessible_positions = [
            item["position"]
            for item in ghost_fixture["accessible_materials_ordered"]
        ]
        active = bool(
            ghost_fixture["current_access_present"]
            and ghost_fixture["source_materials_present"]
            and accessible_positions
        )
        program_relations: list[str] = []
        if active and ghost_model["uses_declared_ghost_program"]:
            program_relations = ghost_fixture["declared_ghost_program"][
                "operations_ordered"
            ]
        target_used = bool(
            active
            and ghost_model["uses_target_guidance"]
            and _scope_equal(
                ghost_fixture["target_guidance_scope"], ghost_fixture["scope"]
            )
        )
        candidate_directions = ["positive"] if active else []
        binding_relation = "single_direction" if active else "none"
        adjudication_outcome = "adopted_positive" if active else "deferred"
        semantic = {
            "semantic_kind": "ghost_path",
            "scope_lineage": deepcopy(ghost_fixture["scope"]),
            "current_access_present": ghost_fixture["current_access_present"],
            "source_materials_present": ghost_fixture["source_materials_present"],
            "accessed_material_positions_ordered": accessible_positions,
            "visited_material_positions_ordered": accessible_positions,
            "operation_phase_order": ["seed", "traverse", "bind"],
            "target_guidance_used": target_used,
            "ghost_program_used": bool(program_relations),
            "candidate_projection": {
                "writer_authority": "ghost_candidate_only",
                "binding_candidate_directions": candidate_directions,
                "binding_relation": binding_relation,
                "registered_operation_relations": program_relations,
            },
            "adjudication_projection": {
                "writer_authority": "scoped_adjudicator_only",
                "adjudication_outcome": adjudication_outcome,
            },
        }
    guards = {
        name: {"before_sha256": zero, "after_sha256": zero}
        for name in EXPECTED_GUARDS
    }
    result = {
        "$schema": "./interp-001d1-v1-result.schema.json",
        "schema_version": "1.0.0",
        "execution_manifest_sha256": execution["integrity"]["manifest_sha256"],
        "execution_contract_sha256": execution["integrity"]["contract_sha256"],
        "cell_key": f"{block}:{fixture}:{model}",
        "block_id": block,
        "fixture_key": fixture,
        "model_id": model,
        "semantic": semantic,
        "operator_trace": _expected_operator_trace(
            execution, block, fixture, model
        ),
        "guard_ledgers": guards,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": "interp-canonical-json-v1",
            "cell_content_sha256": zero,
        },
    }
    result["integrity"]["cell_content_sha256"] = (
        _content_digest_excluding_nested_member(
            result, "integrity", "cell_content_sha256"
        )
    )
    return result


def _future_run_example(
    execution: dict[str, object] | None = None,
) -> dict[str, object]:
    execution = execution or load_exact(EXECUTION_PATH)
    cells = [
        _result_example(
            block_id,
            fixture=fixture_key,
            model=model_id,
            execution=execution,
        )
        for block_id, matrix in {
            item["block_id"]: item
            for item in execution["manifest"]["execution_contract"][
                "execution_matrices"
            ]
        }.items()
        for fixture_key in matrix["fixture_keys"]
        for model_id in matrix["model_ids"]
    ]
    run = {
        "$schema": "./interp-001d1-v1-run.schema.json",
        "schema_version": "1.0.0",
        "run_id": "INTERP-001D1-V1-RUN-future-validator-example",
        "run_version": "1.0.0",
        "status": "EXECUTED_SYNTHETIC_RESULT",
        "execution_manifest_sha256": execution["integrity"]["manifest_sha256"],
        "execution_contract_sha256": execution["integrity"]["contract_sha256"],
        "result_schema_sha256": hashlib.sha256(
            RESULT_SCHEMA_PATH.read_bytes()
        ).hexdigest(),
        "runner_implementation_sha256": "1" * 64,
        "runner_bundle_sha256": "2" * 64,
        "runner_input_kind": "execution_manifest_only",
        "evaluation_manifest_visible": False,
        "cells": cells,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": "interp-canonical-json-v1",
            "canonical_scope": (
                "whole_run_envelope_excluding_only_integrity.run_sha256"
            ),
            "run_sha256": "3" * 64,
        },
    }
    run["integrity"]["run_sha256"] = _content_digest_excluding_nested_member(
        run, "integrity", "run_sha256"
    )
    return run


def _validate_future_run_envelope(
    run: dict[str, object],
    execution: dict[str, object] | None = None,
    *,
    expected_runner_implementation_sha256: str,
    expected_runner_bundle_sha256: str,
    check_integrity: bool = True,
) -> None:
    """Validate the frozen carrier contract; this does not create or authorize a run."""
    execution = execution or load_exact(EXECUTION_PATH)
    schema = load_exact(RUN_SCHEMA_PATH)
    _validate_canonical_domain(run)
    local_schema = deepcopy(schema)
    local_schema["properties"]["cells"]["items"] = {}
    validate_json_schema(run, local_schema)

    if run["execution_manifest_sha256"] != execution["integrity"][
        "manifest_sha256"
    ]:
        raise ValueError("run execution manifest binding mismatch")
    if run["execution_contract_sha256"] != execution["integrity"][
        "contract_sha256"
    ]:
        raise ValueError("run execution contract binding mismatch")
    if run["result_schema_sha256"] != hashlib.sha256(
        RESULT_SCHEMA_PATH.read_bytes()
    ).hexdigest():
        raise ValueError("run result schema content binding mismatch")
    if run["runner_implementation_sha256"] != (
        expected_runner_implementation_sha256
    ):
        raise ValueError("run runner implementation binding mismatch")
    if run["runner_bundle_sha256"] != expected_runner_bundle_sha256:
        raise ValueError("run runner bundle binding mismatch")

    contract = execution["manifest"]["execution_contract"]
    matrices = {item["block_id"]: item for item in contract["execution_matrices"]}
    expected_keys = [
        f"{block_id}:{fixture_key}:{model_id}"
        for block_id, matrix in matrices.items()
        for fixture_key in matrix["fixture_keys"]
        for model_id in matrix["model_ids"]
    ]
    actual_keys = [cell["cell_key"] for cell in run["cells"]]
    if actual_keys != expected_keys or len(set(actual_keys)) != 88:
        raise ValueError("run cell matrix is not the exact frozen ordered matrix")
    counts = {
        block_id: sum(cell["block_id"] == block_id for cell in run["cells"])
        for block_id in matrices
    }
    if counts != {
        "SOURCE_COMPILER": 24,
        "ENCOUNTER_FORMATION": 32,
        "GHOST_PATH": 32,
    }:
        raise ValueError("run block cardinalities changed")
    for cell in run["cells"]:
        if (
            cell["execution_manifest_sha256"]
            != run["execution_manifest_sha256"]
            or cell["execution_contract_sha256"]
            != run["execution_contract_sha256"]
        ):
            raise ValueError("run contains a cell bound to another execution")
        _validate_result_envelope(
            cell, execution, check_integrity=check_integrity
        )
    if check_integrity:
        expected_run_digest = _content_digest_excluding_nested_member(
            run, "integrity", "run_sha256"
        )
        if run["integrity"]["run_sha256"] != expected_run_digest:
            raise ValueError("run content digest mismatch")


class InterpD1ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution = load_exact(EXECUTION_PATH)
        cls.evaluation = load_exact(EVALUATION_PATH)

    def test_d1_manifests_are_schema_valid_semantically_closed_and_content_bound(self) -> None:
        _validate_execution(self.execution)
        _validate_evaluation(self.evaluation, self.execution)

    def test_exact_frozen_catalog_digests(self) -> None:
        execution_contract = self.execution["manifest"]["execution_contract"]
        evaluation_contract = self.evaluation["manifest"]["evaluation_contract"]
        self.assertEqual(
            self.execution["integrity"]["manifest_sha256"],
            EXPECTED_EXECUTION_MANIFEST_SHA256,
        )
        self.assertEqual(digest(execution_contract), EXPECTED_EXECUTION_CONTRACT_SHA256)
        self.assertEqual(
            self.evaluation["integrity"]["manifest_sha256"],
            EXPECTED_EVALUATION_MANIFEST_SHA256,
        )
        self.assertEqual(digest(evaluation_contract), EXPECTED_EVALUATION_CONTRACT_SHA256)
        self.assertEqual(
            digest(execution_contract["operator_declarations"]),
            EXPECTED_OPERATOR_CATALOG_SHA256,
        )
        self.assertEqual(
            digest(execution_contract["operator_input_views"]),
            EXPECTED_INPUT_VIEW_CATALOG_SHA256,
        )
        self.assertEqual(
            digest(evaluation_contract["predicate_declarations"]),
            EXPECTED_PREDICATE_CATALOG_SHA256,
        )
        self.assertEqual(
            digest(evaluation_contract["challenger_declarations"]),
            EXPECTED_CHALLENGER_CATALOG_SHA256,
        )
        self.assertEqual(
            digest(evaluation_contract["semantic_signatures"]),
            EXPECTED_SIGNATURE_CATALOG_SHA256,
        )
        self.assertEqual(
            digest(evaluation_contract["substantive_comparison_projections"]),
            EXPECTED_COMPARISON_PROJECTION_SHA256,
        )
        self.assertEqual(
            hashlib.sha256(RUN_SCHEMA_PATH.read_bytes()).hexdigest(),
            EXPECTED_RUN_SCHEMA_SHA256,
        )

    def test_three_blocks_freeze_exactly_24_32_32_cells(self) -> None:
        matrices = self.execution["manifest"]["execution_contract"]["execution_matrices"]
        self.assertEqual([item["cell_count"] for item in matrices], [24, 32, 32])
        self.assertEqual(sum(item["cell_count"] for item in matrices), 88)

    def test_source_scope_and_effective_order_are_recomputable(self) -> None:
        contract = self.execution["manifest"]["execution_contract"]
        mismatches = 0
        future = 0
        for fixture in contract["source_fixtures"]:
            for record in fixture["source_records"]:
                computed = _scope_equal(record["source_scope"], fixture["scope"])
                self.assertNotIn("scope_match", record)
                mismatches += int(not computed)
                future += int(
                    record["effective_from_access_ordinal"]
                    >= fixture["access_ordinal_k"]
                )
        self.assertGreaterEqual(mismatches, 2)
        self.assertGreaterEqual(future, 1)

    def test_source_cross_kind_union_preserves_declared_order(self) -> None:
        fixture = next(
            item
            for item in self.execution["manifest"]["execution_contract"][
                "source_fixtures"
            ]
            if item["fixture_key"] == "srcfx002"
        )
        declared_positions = [
            item["source_position"] for item in fixture["source_records"]
        ]
        selected_positions = {0, 4}
        stable_union = [
            position
            for position in declared_positions
            if position in selected_positions
        ]
        signature = next(
            item
            for item in self.evaluation["manifest"]["evaluation_contract"][
                "semantic_signatures"
            ]
            if item["signature_id"] == "sig-srcfx002-tf2"
        )
        expected_relation = next(
            item
            for item in signature["expected_relations"]
            if item["path"] == "/semantic/eligible_source_positions_ordered"
        )
        self.assertEqual(stable_union, [4, 0])
        self.assertNotEqual(stable_union, sorted(stable_union))
        self.assertEqual(expected_relation["value"], stable_union)

    def test_result_block_model_fixture_and_semantic_are_explicitly_coupled(self) -> None:
        for block in BLOCK_MODELS:
            _validate_result_envelope(_result_example(block))
        wrong_model = _result_example("SOURCE_COMPILER")
        wrong_model["model_id"] = "GTP"
        wrong_model["cell_key"] = "SOURCE_COMPILER:srcfx001:GTP"
        with self.assertRaisesRegex(ValueError, "model does not belong"):
            _validate_result_envelope(wrong_model)
        wrong_semantic = _result_example("SOURCE_COMPILER")
        wrong_semantic["block_id"] = "GHOST_PATH"
        wrong_semantic["model_id"] = "G0"
        wrong_semantic["fixture_key"] = "ghfx001"
        wrong_semantic["cell_key"] = "GHOST_PATH:ghfx001:G0"
        with self.assertRaisesRegex(ValueError, "semantic shape does not belong"):
            _validate_result_envelope(wrong_semantic)

    def test_result_trace_execution_binding_and_content_digest_are_exact(self) -> None:
        for block in BLOCK_MODELS:
            _validate_result_envelope(_result_example(block))

        empty_trace = _result_example("SOURCE_COMPILER")
        empty_trace["operator_trace"] = []
        with self.assertRaisesRegex(ValueError, "minItems|exact expanded trace"):
            _validate_result_envelope(empty_trace)

        wrong_trace = _result_example("GHOST_PATH")
        wrong_trace["operator_trace"][0]["phase"] = "emit"
        with self.assertRaisesRegex(ValueError, "exact expanded trace"):
            _validate_result_envelope(wrong_trace)

        hidden_field = _result_example("ENCOUNTER_FORMATION")
        hidden_field["operator_trace"][0]["expected_signature"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "additional property"):
            _validate_result_envelope(hidden_field)

        stale_execution = _result_example("SOURCE_COMPILER")
        stale_execution["execution_manifest_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "execution manifest binding"):
            _validate_result_envelope(stale_execution)

        stale_content = _result_example("SOURCE_COMPILER")
        stale_content["semantic"]["contested_present"] = True
        with self.assertRaisesRegex(ValueError, "cell content digest"):
            _validate_result_envelope(stale_content)

    def test_future_run_carrier_is_closed_but_no_run_artifact_exists(self) -> None:
        self.assertEqual(
            list(BENCHMARKS.glob("interp-001d1-v1-run*.json")),
            [RUN_SCHEMA_PATH],
        )
        run = _future_run_example(self.execution)
        runner_implementation = "1" * 64
        runner_bundle = "2" * 64
        _validate_future_run_envelope(
            run,
            self.execution,
            expected_runner_implementation_sha256=runner_implementation,
            expected_runner_bundle_sha256=runner_bundle,
        )
        with self.assertRaises(TypeError):
            _validate_future_run_envelope(run, self.execution)

        wrong_order = deepcopy(run)
        wrong_order["cells"][0], wrong_order["cells"][1] = (
            wrong_order["cells"][1],
            wrong_order["cells"][0],
        )
        with self.assertRaisesRegex(ValueError, "ordered matrix"):
            _validate_future_run_envelope(
                wrong_order,
                self.execution,
                expected_runner_implementation_sha256=runner_implementation,
                expected_runner_bundle_sha256=runner_bundle,
                check_integrity=False,
            )

        mixed_execution = deepcopy(run)
        mixed_execution["cells"][0]["execution_contract_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "another execution"):
            _validate_future_run_envelope(
                mixed_execution,
                self.execution,
                expected_runner_implementation_sha256=runner_implementation,
                expected_runner_bundle_sha256=runner_bundle,
                check_integrity=False,
            )

        stale_schema = deepcopy(run)
        stale_schema["result_schema_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "result schema content binding"):
            _validate_future_run_envelope(
                stale_schema,
                self.execution,
                expected_runner_implementation_sha256=runner_implementation,
                expected_runner_bundle_sha256=runner_bundle,
                check_integrity=False,
            )

        unverifiable_runner = deepcopy(run)
        with self.assertRaisesRegex(ValueError, "runner implementation binding"):
            _validate_future_run_envelope(
                unverifiable_runner,
                self.execution,
                expected_runner_implementation_sha256="e" * 64,
                expected_runner_bundle_sha256=runner_bundle,
                check_integrity=False,
            )

        stale_run_digest = deepcopy(run)
        stale_run_digest["run_id"] = "INTERP-001D1-V1-RUN-mutated"
        with self.assertRaisesRegex(ValueError, "run content digest"):
            _validate_future_run_envelope(
                stale_run_digest,
                self.execution,
                expected_runner_implementation_sha256=runner_implementation,
                expected_runner_bundle_sha256=runner_bundle,
            )

    def test_result_and_run_reject_integers_outside_canonical_domain(self) -> None:
        result = _result_example("SOURCE_COMPILER", execution=self.execution)
        result["semantic"]["access_ordinal_k"] = 2**60
        result["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                result, "integrity", "cell_content_sha256"
            )
        )
        with self.assertRaisesRegex(ValueError, "outside canonical domain"):
            _validate_result_envelope(result, self.execution)

        run = _future_run_example(self.execution)
        run["cells"][0]["semantic"]["access_ordinal_k"] = 2**60
        run["cells"][0]["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                run["cells"][0], "integrity", "cell_content_sha256"
            )
        )
        run["integrity"]["run_sha256"] = _content_digest_excluding_nested_member(
            run, "integrity", "run_sha256"
        )
        with self.assertRaisesRegex(ValueError, "outside canonical domain"):
            _validate_future_run_envelope(
                run,
                self.execution,
                expected_runner_implementation_sha256="1" * 64,
                expected_runner_bundle_sha256="2" * 64,
            )

    def test_source_result_closure_rejects_derived_field_drift(self) -> None:
        mutations = (
            (
                "count",
                lambda semantic: semantic.__setitem__(
                    "eligible_source_position_count", 2
                ),
                "eligible-position count",
            ),
            (
                "effective boundary",
                lambda semantic: semantic.__setitem__(
                    "effective_before_access_ordinal", 3
                ),
                "effective-order boundary",
            ),
            (
                "source kind order",
                lambda semantic: semantic.__setitem__(
                    "source_kinds_used",
                    [
                        "pre_access_accessibility_snapshot",
                        "narrative_terrain_fixture",
                    ],
                ),
                "canonical lexicographic set",
            ),
        )
        for name, mutate, message in mutations:
            with self.subTest(name=name):
                result = _result_example(
                    "SOURCE_COMPILER", execution=self.execution
                )
                mutate(result["semantic"])
                result["integrity"]["cell_content_sha256"] = (
                    _content_digest_excluding_nested_member(
                        result, "integrity", "cell_content_sha256"
                    )
                )
                with self.assertRaisesRegex(ValueError, message):
                    _validate_result_envelope(result, self.execution)

    def test_formation_result_preserves_complete_transition_state(self) -> None:
        result = _result_example(
            "ENCOUNTER_FORMATION",
            fixture="encfx007",
            model="ERT",
            execution=self.execution,
        )
        _validate_result_envelope(result, self.execution)
        result["semantic"]["base_encounter_profile"][
            "activation"
        ]["rank"] = 0
        result["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                result, "integrity", "cell_content_sha256"
            )
        )
        with self.assertRaisesRegex(ValueError, "immutable transition-state"):
            _validate_result_envelope(result, self.execution)

    def test_ghost_inactive_and_raw_projection_closure(self) -> None:
        inactive = _result_example(
            "GHOST_PATH",
            fixture="ghfx007",
            model="GTP",
            execution=self.execution,
        )
        _validate_result_envelope(inactive, self.execution)
        for field, value, message in (
            ("ghost_program_used", True, "applied-stage semantics"),
            (
                "registered_operation_relations",
                ["broaden"],
                "skipped invocation",
            ),
        ):
            with self.subTest(field=field):
                mutant = deepcopy(inactive)
                if field == "registered_operation_relations":
                    mutant["semantic"]["candidate_projection"][field] = value
                else:
                    mutant["semantic"][field] = value
                mutant["integrity"]["cell_content_sha256"] = (
                    _content_digest_excluding_nested_member(
                        mutant, "integrity", "cell_content_sha256"
                    )
                )
                with self.assertRaisesRegex(ValueError, message):
                    _validate_result_envelope(mutant, self.execution)

        reordered = _result_example(
            "GHOST_PATH",
            fixture="ghfx001",
            model="G0",
            execution=self.execution,
        )
        reordered["semantic"]["accessed_material_positions_ordered"].reverse()
        reordered["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                reordered, "integrity", "cell_content_sha256"
            )
        )
        with self.assertRaisesRegex(ValueError, "accessible position order"):
            _validate_result_envelope(reordered, self.execution)

    def test_ghost_raw_direction_order_and_truth_table_are_closed(self) -> None:
        reversed_directions = _result_example(
            "GHOST_PATH", execution=self.execution
        )
        reversed_directions["semantic"]["candidate_projection"][
            "binding_candidate_directions"
        ] = ["positive", "negative"]
        reversed_directions["semantic"]["candidate_projection"][
            "binding_relation"
        ] = "contested"
        reversed_directions["semantic"]["adjudication_projection"][
            "adjudication_outcome"
        ] = "contested"
        reversed_directions["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                reversed_directions, "integrity", "cell_content_sha256"
            )
        )
        with self.assertRaises(ValueError):
            _validate_result_envelope(reversed_directions, self.execution)

        truth_mismatch = _result_example("GHOST_PATH", execution=self.execution)
        truth_mismatch["semantic"]["adjudication_projection"][
            "adjudication_outcome"
        ] = "deferred"
        truth_mismatch["integrity"]["cell_content_sha256"] = (
            _content_digest_excluding_nested_member(
                truth_mismatch, "integrity", "cell_content_sha256"
            )
        )
        with self.assertRaises(ValueError):
            _validate_result_envelope(truth_mismatch, self.execution)

    def test_formation_absence_target_cannot_carry_directions(self) -> None:
        with self.assertRaisesRegex(ValueError, "directions without encounter"):
            _validate_adapted_target(
                self.evaluation,
                "FORMATION_DIRECTION_TARGET",
                {
                    "encounter_emitted": False,
                    "eligible_directions": ["positive"],
                },
            )

    def test_common_target_equality_is_representation_safe(self) -> None:
        profile = {
            "positive_direction_support": {"status": "present", "rank": 2},
            "negative_direction_support": {"status": "present", "rank": 0},
        }
        left = {"target_form_readout_profile": deepcopy(profile)}
        alias_adapted = {"target_form_readout_profile": deepcopy(profile)}
        self.assertFalse(
            _adapted_targets_differ(
                self.evaluation,
                "SOURCE_READOUT_TARGET",
                left,
                alias_adapted,
            )
        )
        alias_adapted["target_form_readout_profile"][
            "negative_direction_support"
        ]["rank"] = 1
        self.assertTrue(
            _adapted_targets_differ(
                self.evaluation,
                "SOURCE_READOUT_TARGET",
                left,
                alias_adapted,
            )
        )
        with self.assertRaisesRegex(ValueError, "shape mismatch"):
            _adapted_targets_differ(
                self.evaluation,
                "SOURCE_READOUT_TARGET",
                left,
                {"raw_tuple": [2, 0]},
            )

    def test_declared_rt_lookup_is_an_actual_target_level_alias_not_a_false_difference(self) -> None:
        fixtures = self.execution["manifest"]["execution_contract"][
            "formation_fixtures"
        ]
        for fixture in fixtures:
            with self.subTest(fixture=fixture["fixture_key"]):
                model_target, lookup_target = _formation_ert_and_lookup_targets(fixture)
                self.assertFalse(
                    _adapted_targets_differ(
                        self.evaluation,
                        "FORMATION_DIRECTION_TARGET",
                        model_target,
                        lookup_target,
                    )
                )

    def test_ghost_target_adapter_derives_adjudication_and_cannot_inject_it(self) -> None:
        target = {
            "binding_candidate_directions": ["negative", "positive"],
            "binding_relation": "contested",
            "adjudication_outcome": "contested",
        }
        self.assertFalse(
            _adapted_targets_differ(
                self.evaluation,
                "GHOST_CANDIDATE_TARGET",
                target,
                deepcopy(target),
            )
        )
        inconsistent = deepcopy(target)
        inconsistent["adjudication_outcome"] = "deferred"
        with self.assertRaisesRegex(ValueError, "frozen truth table"):
            _validate_adapted_target(
                self.evaluation,
                "GHOST_CANDIDATE_TARGET",
                inconsistent,
            )
        mutant = deepcopy(self.evaluation)
        ghost_challenger = next(
            item for item in mutant["manifest"]["evaluation_contract"][
                "challenger_declarations"
            ] if item["block_id"] == "GHOST_PATH"
        )
        ghost_challenger["comparison_adapter"]["input_paths"].append(
            "/raw/adjudication_outcome"
        )
        with self.assertRaisesRegex(ValueError, "inject adjudication"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_formation_has_clean_r_t_scalar_and_absence_controls(self) -> None:
        _validate_execution(self.execution, check_integrity=False)

    def test_ghost_sealed_structures_are_not_development_copies(self) -> None:
        ghost = self.execution["manifest"]["execution_contract"]["ghost_fixtures"]
        structural = lambda item: digest(
            _semantic_fixture_payload(item, excluded={"scope", "target_guidance_scope"})
        )
        self.assertTrue(
            {structural(item) for item in ghost[:4]}.isdisjoint(
                {structural(item) for item in ghost[4:]}
            )
        )

    def test_operators_and_challengers_are_executable_closed_catalogs(self) -> None:
        _validate_execution(self.execution, check_integrity=False)
        _validate_evaluation(self.evaluation, self.execution, check_integrity=False)

    def test_comparison_projections_exclude_all_registered_bookkeeping(self) -> None:
        projections = self.evaluation["manifest"]["evaluation_contract"][
            "substantive_comparison_projections"
        ]
        for projection in projections:
            self.assertTrue(
                set(projection["included_result_paths"]).isdisjoint(BOOKKEEPING_PATHS)
            )
            self.assertTrue(
                set(projection["excluded_bookkeeping_paths"]) <= BOOKKEEPING_PATHS
            )

    def test_development_sealed_split_is_evaluator_only_not_prediction(self) -> None:
        execution_text = EXECUTION_PATH.read_text(encoding="utf-8")
        self.assertNotIn('"development_fixture_keys"', execution_text)
        self.assertNotIn('"sealed_fixture_keys"', execution_text)
        split = self.evaluation["manifest"]["evaluation_contract"][
            "synthetic_split_contract"
        ]
        self.assertEqual(split["purpose"], "evaluator_isolation_only")
        self.assertIs(split["independent_prediction_claim"], False)

    def test_no_d1_runner_or_runtime_integration_was_added(self) -> None:
        self.assertEqual(
            list((ROOT / "dynamics" / "labs").glob("interp_d1*.py")),
            [],
        )
        runtime_paths = [
            ROOT / "dynamics" / "engine.py",
            *(ROOT / "dynamics" / "models").glob("*.py"),
            *(ROOT / "dynamics" / "protocol").glob("*.py"),
            *(ROOT / "dynamics" / "contract").glob("*.py"),
        ]
        for path in runtime_paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            }
            imports.update(
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            )
            self.assertFalse(
                any(name.startswith("dynamics.labs") for name in imports),
                path,
            )

    def test_mutation_stored_scope_match_flag_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        record = mutant["manifest"]["execution_contract"]["source_fixtures"][0][
            "source_records"
        ][0]
        record["scope_match"] = True
        with self.assertRaisesRegex(ValueError, "schema|scope-match"):
            _validate_execution(mutant, check_integrity=False)

    def test_scope_resolution_includes_resolution_and_external_alias(self) -> None:
        fixture = self.execution["manifest"]["execution_contract"][
            "source_fixtures"
        ][4]
        source_scope = deepcopy(fixture["scope"])
        source_scope["target_resolution"]["external_entity_alias"] = "external.decoy"
        self.assertFalse(_scope_equal(source_scope, fixture["scope"]))

    def test_mutation_opaque_alias_is_detected_by_manifest_digest(self) -> None:
        mutant = deepcopy(self.execution)
        record = mutant["manifest"]["execution_contract"]["source_fixtures"][7][
            "source_records"
        ][5]
        record["source_alias"] = "opaque.source.999"
        with self.assertRaisesRegex(ValueError, "manifest digest mismatch"):
            _validate_execution(mutant)

    def test_mutation_source_order_mirror_content_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["source_fixtures"][1][
            "source_records"
        ][-1]["direction_profile"]["positive_direction_support"]["rank"] = 1
        with self.assertRaisesRegex(ValueError, "source-order mirror"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_future_source_recast_as_current_breaks_effective_order_control(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["source_fixtures"][7][
            "source_records"
        ][5]["effective_from_access_ordinal"] = 1
        with self.assertRaisesRegex(ValueError, "future-source controls"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_unknown_or_dead_operator_is_rejected(self) -> None:
        for kind in ("unknown", "dead"):
            with self.subTest(kind=kind):
                mutant = deepcopy(self.execution)
                contract = mutant["manifest"]["execution_contract"]
                if kind == "unknown":
                    contract["ghost_models"][0]["operator_sequence"].append("not_registered")
                else:
                    extra = deepcopy(contract["operator_declarations"][0])
                    extra["operator_id"] = "unused_operator"
                    contract["operator_declarations"].append(extra)
                with self.assertRaisesRegex(ValueError, "unknown or dead operator"):
                    _validate_execution(mutant, check_integrity=False)

    def test_mutation_unsettled_projection_cannot_enter_readout_max(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["source_dataflow_contract"][
            "accepted_output_kind"
        ] = "unsettled_source_projection"
        with self.assertRaisesRegex(ValueError, "source typed dataflow|schema"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_operator_exposes_expected_signature_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        view = mutant["manifest"]["execution_contract"]["operator_input_views"][0]
        view["fields"].append(
            {
                "field_id": "expected_signature",
                "value_kind": "token",
                "operator_use": "inspect",
            }
        )
        with self.assertRaisesRegex(ValueError, "forbidden field"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_operator_exposes_unregistered_answer_field_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        view = mutant["manifest"]["execution_contract"]["operator_input_views"][0]
        view["fields"].append(
            {
                "field_id": "declared_answer",
                "value_kind": "token",
                "operator_use": "inspect",
            }
        )
        with self.assertRaisesRegex(ValueError, "undeclared inspect field"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_declared_order_state_or_opaque_binding_is_rejected(self) -> None:
        typed_key = "operator_typed_dataflow_contract"
        cases: list[tuple[str, dict[str, object], str]] = []

        order_mutant = deepcopy(self.execution)
        order_preprocessor = next(
            item
            for item in order_mutant["manifest"]["execution_contract"][
                typed_key
            ]["deterministic_preprocessor_declarations"]
            if item["preprocessor_id"] == "prep.source.declared_position_order"
        )
        order_preprocessor["raw_source_paths"] = [
            "/fixture/source_records/*/source_kind"
        ]
        cases.append(
            (
                "declared order",
                order_mutant,
                "declared-order preprocessor",
            )
        )

        state_mutant = deepcopy(self.execution)
        state_mutant["manifest"]["execution_contract"][
            "formation_transition_state_contract"
        ]["immutable_fields"].pop()
        cases.append(
            (
                "formation state",
                state_mutant,
                "formation transition-state|schema",
            )
        )

        binding_mutant = deepcopy(self.execution)
        opaque_binding = binding_mutant["manifest"]["execution_contract"][
            typed_key
        ]["raw_opaque_pass_through_bindings"][0]
        opaque_binding["raw_source_path"] = "/fixture/source_records/0/source_alias"
        cases.append(
            (
                "opaque binding",
                binding_mutant,
                "opaque scope lineage|schema",
            )
        )

        for name, mutant, message in cases:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, message):
                    _validate_execution(mutant, check_integrity=False)

    def test_mutation_assertion_cannot_cross_block_families(self) -> None:
        mutant = deepcopy(self.evaluation)
        assertion = next(
            item for item in mutant["manifest"]["evaluation_contract"][
                "pair_assertions"
            ] if item["predicate_id"] == "models_differ_on_fixture"
        )
        assertion["operands"][2] = "G0"
        with self.assertRaisesRegex(ValueError, "cross block|operand kind"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_challenger_target_wrong_block_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        challenger = mutant["manifest"]["evaluation_contract"][
            "challenger_declarations"
        ][0]
        challenger["comparison_target_id"] = "GHOST_CANDIDATE_TARGET"
        with self.assertRaisesRegex(ValueError, "crosses blocks"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_same_access_feedback_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["phase_contract"][
            "same_access_feedback"
        ] = "allowed"
        with self.assertRaisesRegex(ValueError, "phase/effective-order|schema"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_no_access_fixture_invents_material_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        ghost = mutant["manifest"]["execution_contract"]["ghost_fixtures"][6]
        ghost["accessible_materials_ordered"].append(
            deepcopy(
                mutant["manifest"]["execution_contract"]["ghost_fixtures"][0][
                    "accessible_materials_ordered"
                ][0]
            )
        )
        with self.assertRaisesRegex(ValueError, "no-access control carries"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_incomplete_matrix_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["execution_matrices"][0][
            "fixture_keys"
        ].pop()
        with self.assertRaisesRegex(ValueError, "fixture matrix"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_bookkeeping_path_in_substantive_projection_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        projection = mutant["manifest"]["evaluation_contract"][
            "substantive_comparison_projections"
        ][0]
        projection["included_result_paths"].append("/semantic/source_kinds_used")
        with self.assertRaisesRegex(ValueError, "bookkeeping leaked"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_retirement_predicate_arity_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        mutant["manifest"]["evaluation_contract"]["retirement_rules"][0][
            "condition_operands"
        ].pop()
        with self.assertRaisesRegex(ValueError, "retirement predicate arity"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_signature_path_outside_result_schema_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        mutant["manifest"]["evaluation_contract"]["semantic_signatures"][0][
            "expected_relations"
        ][0]["path"] = "/semantic/not_registered"
        with self.assertRaisesRegex(ValueError, "outside result schema"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_split_leak_or_overclaim_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        mutant["manifest"]["evaluation_contract"]["synthetic_split_contract"][
            "independent_prediction_claim"
        ] = True
        with self.assertRaisesRegex(ValueError, "synthetic split overclaimed|schema"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_guard_removal_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["output_guard_contract"][
            "guard_ledger_names"
        ].remove("authority_grants")
        with self.assertRaisesRegex(ValueError, "guard ledger boundary|schema"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_float_or_null_is_rejected(self) -> None:
        for value, message in ((1.0, "float"), (None, "null")):
            with self.subTest(value=value):
                mutant = deepcopy(self.execution)
                mutant["manifest"]["execution_contract"]["source_fixtures"][0][
                    "access_ordinal_k"
                ] = value
                with self.assertRaisesRegex(ValueError, message):
                    _validate_execution(mutant, check_integrity=False)


if __name__ == "__main__":
    unittest.main()
