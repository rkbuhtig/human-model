from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

from dynamics.labs.interp_d1_common import (
    CANONICALIZATION_ID,
    FrozenD1ExecutionError,
    canonical_bytes,
    digest,
    digest_without_nested_member,
    loads_exact,
)
from dynamics.labs.interp_d1_operators import OPERATOR_REGISTRY, PREPROCESSOR_REGISTRY


EXECUTION_MANIFEST_ID = "INTERP-001D1-V1-EXECUTION"
EXECUTION_MANIFEST_VERSION = "1.0.0"
EXECUTION_MANIFEST_SHA256 = (
    "ad627e9b27dbcf517d6dc16736974b8e8f2547ab98cb7a4bea8a4694cbcd1740"
)
EXECUTION_CONTRACT_SHA256 = (
    "1f49e2c89a79af5d50ff877ef9326191564d768be6af8a1904395929782513c7"
)
RESULT_SCHEMA_SHA256 = (
    "be74c90b4fc501793862097cc948c36ceb7ea1969e48a8b69290d73eca8cecb9"
)
RUN_SCHEMA_SHA256 = (
    "4a993a28db36c052c5d6a81d4de8867a385523fcab972d1699049683130c73ed"
)
RUN_ID = "INTERP-001D1-V1-RUN-001"
RUN_VERSION = "1.0.0"
BUNDLE_CANONICALIZATION_ID = "interp-d1-source-bundle-v1-policy-bindings-elided"
BUNDLE_PATHS = (
    "dynamics/__init__.py",
    "dynamics/labs/__init__.py",
    "dynamics/labs/interp_d1_common.py",
    "dynamics/labs/interp_d1_operators.py",
    "dynamics/labs/interp_d1_runner.py",
    "dynamics/labs/interp_d1_run_cli.py",
    "dynamics/labs/interp_d1_cli.py",
)


# The frozen manifest names direct raw fields but omits their fixture paths.
# This implementation binding is therefore explicit, closed, and audited against
# every manifest raw binding before a cell is allowed to run.
RAW_FIXTURE_BINDINGS: dict[tuple[str, str], tuple[str, ...]] = {
    ("base_profile", "current_access_present"): ("current_access_present",),
    ("base_profile", "source_materials_present"): ("source_materials_present",),
    ("base_profile", "base_encounter_profile"): ("base_encounter_profile",),
    ("apply_reception_eligibility", "reception_profile"): (
        "declared_reception_intervention",
    ),
    ("apply_target_directional_compatibility", "target_form_profile"): (
        "declared_target_form_intervention",
    ),
    ("close_source_readout", "access_ordinal_k"): ("access_ordinal_k",),
    ("ghost_seed", "current_access_present"): ("current_access_present",),
    ("ghost_seed", "source_materials_present"): ("source_materials_present",),
    ("apply_target_candidate_eligibility", "target_guidance_profile"): (
        "target_guidance_profile",
    ),
    ("close_ghost_semantic", "current_access_present"): (
        "current_access_present",
    ),
    ("close_ghost_semantic", "source_materials_present"): (
        "source_materials_present",
    ),
}


MULTI_OUTPUT_KINDS = frozenset(
    {"source_profile_projection", "unsettled_source_diagnostic"}
)


@dataclass(frozen=True)
class _OutputRecord:
    operator_id: str
    output_kind: str
    value: Any


class _CellLedger:
    def __init__(self) -> None:
        self._records: list[_OutputRecord] = []

    @property
    def records(self) -> tuple[_OutputRecord, ...]:
        return tuple(self._records)

    def append(self, operator_id: str, output_kind: str, value: Any) -> None:
        self._records.append(
            _OutputRecord(operator_id, output_kind, deepcopy(value))
        )

    def matching(
        self, producer_ids: set[str], output_kinds: set[str]
    ) -> list[_OutputRecord]:
        return [
            item
            for item in self._records
            if item.operator_id in producer_ids and item.output_kind in output_kinds
        ]


def _source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _source_bundle_sha256() -> str:
    root = Path(__file__).resolve().parents[2]
    return digest(
        [
            {
                "path": path,
                "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
            }
            for path in BUNDLE_PATHS
        ]
    )


def _index(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item[key]
        if value in result:
            raise FrozenD1ExecutionError(f"duplicate catalog key {key}: {value}")
        result[value] = item
    return result


def _governing_hash(manifest: dict[str, Any], document_id: str, path: str) -> str:
    matches = [
        item
        for item in manifest["governing_documents"]
        if item["document_id"] == document_id and item["path"] == path
    ]
    if len(matches) != 1:
        raise FrozenD1ExecutionError(f"governing document binding missing: {document_id}")
    return matches[0]["content_sha256"]


def _declared_raw_bindings(contract: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        (binding["operator_id"], field_id)
        for binding in contract["operator_typed_dataflow_contract"]["raw_input_bindings"]
        for field_id in binding["field_ids"]
    }


def _validate_execution(document: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(document, dict) or set(document) != {
        "$schema",
        "manifest",
        "integrity",
    }:
        raise FrozenD1ExecutionError("execution envelope is not closed")
    if document["$schema"] != "./interp-001d1-manifest.schema.json":
        raise FrozenD1ExecutionError("execution envelope schema identity mismatch")
    manifest = document["manifest"]
    integrity = document["integrity"]
    if not isinstance(manifest, dict):
        raise FrozenD1ExecutionError("execution manifest must be an object")
    try:
        contract = manifest["execution_contract"]
    except KeyError as error:
        raise FrozenD1ExecutionError(
            f"execution manifest field missing: {error.args[0]}"
        ) from error
    if not isinstance(integrity, dict) or set(integrity) != {
        "algorithm",
        "canonicalization_id",
        "manifest_sha256",
        "contract_sha256",
    }:
        raise FrozenD1ExecutionError("execution integrity envelope is not closed")
    if integrity.get("algorithm") != "sha256":
        raise FrozenD1ExecutionError("execution integrity algorithm mismatch")
    if manifest.get("manifest_id") != EXECUTION_MANIFEST_ID:
        raise FrozenD1ExecutionError("execution manifest identity mismatch")
    if manifest.get("manifest_version") != EXECUTION_MANIFEST_VERSION:
        raise FrozenD1ExecutionError("execution manifest version mismatch")
    if manifest.get("status") != "FROZEN_UNEXECUTED":
        raise FrozenD1ExecutionError("execution manifest freeze status mismatch")
    if integrity.get("canonicalization_id") != CANONICALIZATION_ID:
        raise FrozenD1ExecutionError("execution canonicalization identity mismatch")
    if digest(manifest) != integrity.get("manifest_sha256"):
        raise FrozenD1ExecutionError("execution manifest integrity mismatch")
    if digest(contract) != integrity.get("contract_sha256"):
        raise FrozenD1ExecutionError("execution contract integrity mismatch")
    if integrity.get("manifest_sha256") != EXECUTION_MANIFEST_SHA256:
        raise FrozenD1ExecutionError("execution manifest is not frozen D1 v1")
    if integrity.get("contract_sha256") != EXECUTION_CONTRACT_SHA256:
        raise FrozenD1ExecutionError("execution contract is not frozen D1 v1")
    if _governing_hash(
        manifest,
        "INTERP-001D1-RESULT-SCHEMA",
        "research/benchmarks/interp-001d1-v1-result.schema.json",
    ) != RESULT_SCHEMA_SHA256:
        raise FrozenD1ExecutionError("result schema governing hash mismatch")
    if _governing_hash(
        manifest,
        "INTERP-001D1-RUN-SCHEMA",
        "research/benchmarks/interp-001d1-v1-run.schema.json",
    ) != RUN_SCHEMA_SHA256:
        raise FrozenD1ExecutionError("run schema governing hash mismatch")
    if _declared_raw_bindings(contract) != set(RAW_FIXTURE_BINDINGS):
        raise FrozenD1ExecutionError("raw fixture binding map is not exact")
    declared_preprocessors = {
        item["preprocessor_id"]
        for item in contract["operator_typed_dataflow_contract"][
            "deterministic_preprocessor_declarations"
        ]
    }
    if declared_preprocessors != set(PREPROCESSOR_REGISTRY):
        raise FrozenD1ExecutionError("preprocessor implementation catalog mismatch")
    declared_operators = {
        item["operator_id"] for item in contract["operator_declarations"]
    } | {contract["adjudicator_contract"]["policy_id"]}
    if declared_operators != set(OPERATOR_REGISTRY):
        raise FrozenD1ExecutionError("operator implementation catalog mismatch")
    expected_guards = {
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
    }
    if set(contract["output_guard_contract"]["guard_ledger_names"]) != expected_guards:
        raise FrozenD1ExecutionError("output guard catalog mismatch")
    return deepcopy(manifest), deepcopy(contract)


def _catalogs(contract: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    return {
        "SOURCE_COMPILER": _index(contract["source_fixtures"], "fixture_key"),
        "ENCOUNTER_FORMATION": _index(
            contract["formation_fixtures"], "fixture_key"
        ),
        "GHOST_PATH": _index(contract["ghost_fixtures"], "fixture_key"),
        "source_models": _index(contract["source_compilers"], "model_id"),
        "formation_models": _index(contract["formation_models"], "model_id"),
        "ghost_models": _index(contract["ghost_models"], "model_id"),
        "operators": _index(contract["operator_declarations"], "operator_id"),
        "views": _index(contract["operator_input_views"], "view_id"),
    }


def _model(catalogs: dict[str, Any], block_id: str, model_id: str) -> dict[str, Any]:
    key = {
        "SOURCE_COMPILER": "source_models",
        "ENCOUNTER_FORMATION": "formation_models",
        "GHOST_PATH": "ghost_models",
    }[block_id]
    try:
        return catalogs[key][model_id]
    except KeyError as error:
        raise FrozenD1ExecutionError(
            f"model {model_id} does not belong to {block_id}"
        ) from error


def _expanded_sequence(
    contract: dict[str, Any], block_id: str, fixture: dict[str, Any], model: dict[str, Any]
) -> list[str]:
    sequence = list(model["operator_sequence"])
    if block_id != "GHOST_PATH":
        return sequence
    token = contract["operator_typed_dataflow_contract"][
        "ghost_sequence_expansion_token"
    ]
    uses_program = model["uses_declared_ghost_program"]
    if sequence.count(token) != int(uses_program):
        raise FrozenD1ExecutionError("Ghost program expansion token mismatch")
    if uses_program:
        index = sequence.index(token)
        sequence[index : index + 1] = fixture["declared_ghost_program"][
            "operations_ordered"
        ]
    sequence.extend(contract["adjudicator_contract"]["post_candidate_tail_sequence"])
    return sequence


def _operator_declaration(
    contract: dict[str, Any], catalogs: dict[str, Any], operator_id: str
) -> dict[str, Any]:
    adjudicator = contract["adjudicator_contract"]
    if operator_id == adjudicator["policy_id"]:
        return {
            "operator_id": operator_id,
            "operator_version": adjudicator["policy_version"],
            "input_view_id": adjudicator["input_view_id"],
            "exact_inspected_field_ids": adjudicator["exact_inspected_field_ids"],
            "exact_opaque_pass_through_field_ids": adjudicator[
                "exact_opaque_pass_through_field_ids"
            ],
            "output_kind": adjudicator["output_kind"],
            "authority": adjudicator["writer_authority"],
        }
    try:
        return catalogs["operators"][operator_id]
    except KeyError as error:
        raise FrozenD1ExecutionError(f"unknown operator: {operator_id}") from error


def _read_fixture_path(fixture: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = fixture
    for segment in path:
        if not isinstance(value, dict) or segment not in value:
            raise FrozenD1ExecutionError(
                f"raw fixture binding path missing: {'/'.join(path)}"
            )
        value = value[segment]
    return deepcopy(value)


def _transfer_edge(
    edge: dict[str, Any], matches: list[_OutputRecord]
) -> Any:
    policy = edge["selection_policy"]
    if policy == "nearest_prior_one":
        if not matches:
            raise FrozenD1ExecutionError(f"typed edge has no producer: {edge['edge_id']}")
        values = [matches[-1].value]
    elif policy == "all_prior_matching_zero_or_more":
        values = [item.value for item in matches]
    elif policy == "all_prior_matching_one_or_more":
        if not matches:
            raise FrozenD1ExecutionError(f"typed edge has no producer: {edge['edge_id']}")
        values = [item.value for item in matches]
    else:
        raise FrozenD1ExecutionError(f"unknown edge selection policy: {policy}")
    transfer = edge["transfer_policy"]
    if transfer == "identity":
        if len(values) != 1:
            raise FrozenD1ExecutionError("identity edge did not resolve one value")
        return deepcopy(values[0])
    if transfer == "extract_accessible_positions":
        if len(values) != 1:
            raise FrozenD1ExecutionError("accessibility edge did not resolve one receipt")
        return deepcopy(values[0]["accessible_implicit_positions"])
    if transfer == "extract_direction_profiles":
        return [deepcopy(item["direction_profile"]) for item in values]
    if transfer == "extract_candidate_fields":
        if len(values) != 1:
            raise FrozenD1ExecutionError("candidate edge did not resolve one projection")
        field = edge["consumer_input_field_id"]
        source_field = {
            "candidate_direction_set": "binding_candidate_directions",
            "binding_relation": "binding_relation",
        }[field]
        return deepcopy(values[0][source_field])
    if transfer == "collect_receipts":
        return deepcopy(values)
    raise FrozenD1ExecutionError(f"unknown edge transfer policy: {transfer}")


def _bind_inputs(
    *,
    contract: dict[str, Any],
    declaration: dict[str, Any],
    fixture: dict[str, Any],
    ledger: _CellLedger,
    preprocessor_cache: dict[str, Any],
) -> dict[str, Any]:
    operator_id = declaration["operator_id"]
    required = [
        *declaration["exact_inspected_field_ids"],
        *declaration["exact_opaque_pass_through_field_ids"],
    ]
    typed = contract["operator_typed_dataflow_contract"]
    preprocessor_bindings = {
        (item["operator_id"], item["field_id"]): item["preprocessor_id"]
        for item in typed["deterministic_preprocessor_bindings"]
    }
    opaque_bindings = {
        (item["operator_id"], item["field_id"]): item
        for item in typed["raw_opaque_pass_through_bindings"]
    }
    edges_by_input: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for edge in typed["edges"]:
        edges_by_input.setdefault(
            (edge["consumer_operator_id"], edge["consumer_input_field_id"]), []
        ).append(edge)
    result: dict[str, Any] = {}
    for field_id in required:
        key = (operator_id, field_id)
        authorities = sum(
            (
                key in RAW_FIXTURE_BINDINGS,
                key in preprocessor_bindings,
                key in opaque_bindings,
                key in edges_by_input,
            )
        )
        if authorities != 1:
            raise FrozenD1ExecutionError(
                f"operator input has {authorities} authority sources: {operator_id}.{field_id}"
            )
        if key in RAW_FIXTURE_BINDINGS:
            result[field_id] = _read_fixture_path(
                fixture, RAW_FIXTURE_BINDINGS[key]
            )
        elif key in preprocessor_bindings:
            preprocessor_id = preprocessor_bindings[key]
            if preprocessor_id not in preprocessor_cache:
                try:
                    preprocessor_cache[preprocessor_id] = PREPROCESSOR_REGISTRY[
                        preprocessor_id
                    ](fixture)
                except KeyError as error:
                    raise FrozenD1ExecutionError(
                        f"preprocessor is not implemented: {preprocessor_id}"
                    ) from error
            result[field_id] = deepcopy(preprocessor_cache[preprocessor_id])
        elif key in opaque_bindings:
            binding = opaque_bindings[key]
            if binding["raw_source_path"] != "/fixture/scope":
                raise FrozenD1ExecutionError("opaque binder path changed")
            result[field_id] = deepcopy(fixture["scope"])
        else:
            edges = edges_by_input[key]
            if len(edges) != 1:
                raise FrozenD1ExecutionError(
                    f"operator input has multiple typed edges: {operator_id}.{field_id}"
                )
            edge = edges[0]
            matches = ledger.matching(
                set(edge["producer_operator_ids"]), set(edge["producer_output_kinds"])
            )
            result[field_id] = _transfer_edge(edge, matches)
    if set(result) != set(required):
        raise FrozenD1ExecutionError("operator input binder did not close exactly")
    return result


def _append_output(
    ledger: _CellLedger, declaration: dict[str, Any], output: Any
) -> None:
    output_kind = declaration["output_kind"]
    if output_kind in MULTI_OUTPUT_KINDS:
        if not isinstance(output, list):
            raise FrozenD1ExecutionError("multi-output operator did not emit a list")
        for item in output:
            ledger.append(declaration["operator_id"], output_kind, item)
    else:
        ledger.append(declaration["operator_id"], output_kind, output)


def _operator_trace(
    contract: dict[str, Any], catalogs: dict[str, Any], sequence: list[str]
) -> list[dict[str, Any]]:
    result = []
    for operator_id in sequence:
        declaration = _operator_declaration(contract, catalogs, operator_id)
        result.append(
            {
                "operator_id": operator_id,
                "operator_version": declaration["operator_version"],
                "phase": contract["operator_trace_phase_map"][operator_id],
                "input_view_id": declaration["input_view_id"],
                "inspected_field_ids": deepcopy(
                    declaration["exact_inspected_field_ids"]
                ),
                "opaque_pass_through_field_ids": deepcopy(
                    declaration["exact_opaque_pass_through_field_ids"]
                ),
                "output_kind": declaration["output_kind"],
                "authority": declaration["authority"],
            }
        )
    return result


def _detached_guards(contract: dict[str, Any]) -> dict[str, dict[str, str]]:
    # D1 loads no runtime ledgers.  Each named guard is therefore a fresh empty
    # detached ledger; fixture immutability is checked separately in _run_cell.
    empty_sha = digest([])
    return {
        name: {"before_sha256": empty_sha, "after_sha256": empty_sha}
        for name in contract["output_guard_contract"]["guard_ledger_names"]
    }


def _run_cell(
    *,
    manifest: dict[str, Any],
    contract: dict[str, Any],
    catalogs: dict[str, Any],
    block_id: str,
    fixture_key: str,
    model_id: str,
) -> dict[str, Any]:
    try:
        fixture = deepcopy(catalogs[block_id][fixture_key])
    except KeyError as error:
        raise FrozenD1ExecutionError(
            f"fixture {fixture_key} does not belong to {block_id}"
        ) from error
    fixture_before = digest(fixture)
    model = _model(catalogs, block_id, model_id)
    sequence = _expanded_sequence(contract, block_id, fixture, model)
    ledger = _CellLedger()
    cache: dict[str, Any] = {}
    for operator_id in sequence:
        declaration = _operator_declaration(contract, catalogs, operator_id)
        inputs = _bind_inputs(
            contract=contract,
            declaration=declaration,
            fixture=fixture,
            ledger=ledger,
            preprocessor_cache=cache,
        )
        output = OPERATOR_REGISTRY[operator_id](inputs)
        _append_output(ledger, declaration, output)
    if digest(fixture) != fixture_before:
        raise FrozenD1ExecutionError("operator mutated its detached fixture input")
    semantic_records = [
        item
        for item in ledger.records
        if item.operator_id == "bind_opaque_sources"
        and item.output_kind == "block_semantic_with_bound_lineage"
    ]
    if len(semantic_records) != 1:
        raise FrozenD1ExecutionError("cell did not close exactly one semantic output")
    cell = {
        "$schema": "./interp-001d1-v1-result.schema.json",
        "schema_version": "1.0.0",
        "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
        "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
        "cell_key": f"{block_id}:{fixture_key}:{model_id}",
        "block_id": block_id,
        "fixture_key": fixture_key,
        "model_id": model_id,
        "semantic": deepcopy(semantic_records[0].value),
        "operator_trace": _operator_trace(contract, catalogs, sequence),
        "guard_ledgers": _detached_guards(contract),
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": CANONICALIZATION_ID,
            "cell_content_sha256": "",
        },
    }
    cell["integrity"]["cell_content_sha256"] = digest_without_nested_member(
        cell, "integrity", "cell_content_sha256"
    )
    return cell


def run_d1(execution_manifest_bytes: bytes) -> dict[str, Any]:
    """Execute the frozen 88-cell D1 matrix from execution bytes only."""
    document = loads_exact(execution_manifest_bytes)
    manifest, contract = _validate_execution(document)
    contract_before = digest(contract)
    catalogs = _catalogs(contract)
    cells: list[dict[str, Any]] = []
    declared_count = 0
    for matrix in contract["execution_matrices"]:
        block_id = matrix["block_id"]
        matrix_count = len(matrix["fixture_keys"]) * len(matrix["model_ids"])
        if matrix["matrix_kind"] != "cartesian_product" or matrix["cell_count"] != matrix_count:
            raise FrozenD1ExecutionError("execution matrix cardinality mismatch")
        declared_count += matrix["cell_count"]
        for fixture_key in matrix["fixture_keys"]:
            for model_id in matrix["model_ids"]:
                cells.append(
                    _run_cell(
                        manifest=manifest,
                        contract=contract,
                        catalogs=catalogs,
                        block_id=block_id,
                        fixture_key=fixture_key,
                        model_id=model_id,
                    )
                )
    cell_keys = [cell["cell_key"] for cell in cells]
    if declared_count != 88 or len(cells) != 88 or len(cell_keys) != len(set(cell_keys)):
        raise FrozenD1ExecutionError("run did not emit the exact 88-cell matrix")
    if digest(contract) != contract_before:
        raise FrozenD1ExecutionError("run mutated the frozen execution contract")
    run = {
        "$schema": "./interp-001d1-v1-run.schema.json",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "run_version": RUN_VERSION,
        "status": "EXECUTED_SYNTHETIC_RESULT",
        "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
        "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
        "result_schema_sha256": RESULT_SCHEMA_SHA256,
        "runner_implementation_sha256": _source_sha256(),
        "runner_bundle_sha256": _source_bundle_sha256(),
        "runner_input_kind": "execution_manifest_only",
        "evaluation_manifest_visible": False,
        "cells": cells,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": CANONICALIZATION_ID,
            "canonical_scope": (
                "whole_run_envelope_excluding_only_integrity.run_sha256"
            ),
            "run_sha256": "",
        },
    }
    run["integrity"]["run_sha256"] = digest_without_nested_member(
        run, "integrity", "run_sha256"
    )
    return run


def encode_run(run: dict[str, Any]) -> bytes:
    return canonical_bytes(run) + b"\n"
