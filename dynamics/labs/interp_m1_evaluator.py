from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import re
from typing import Any, Callable

from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    digest,
    loads_exact,
    profile_without_key,
    validate_json_schema,
)


# This module deliberately does not import interp_m1_runner.  The evaluator is a
# second program which sees the frozen expectations only after a run exists.
EXECUTION_FILE_SHA256 = "c5531bdd31963917f18272b2327396aa5d3637680dc39ef1dcd9514c318a2e8e"
EXECUTION_MANIFEST_SHA256 = "d055ad2f3943adb616551510260700c145eeaa311d912e005729393e0d7e07c1"
EXECUTION_CONTRACT_SHA256 = "d799c17a88ad789c2b5f43606db1838c0c345328262a4fb7baf6033e12dea4c3"
EVALUATION_FILE_SHA256 = "01135e59fde93355412f15bb57f6ade62e1cb6388bfbd78973c35771086650db"
EVALUATION_MANIFEST_SHA256 = "6e7c422f7e43bf55d7e1a7c2aac0e03c382deb309f3798e09377e01d86f152e6"
EVALUATION_CONTRACT_SHA256 = "f56cbf33ad06ac3fa769231f349521927b4c2372fe121635bc4121e9981bb528"
PREDICATE_CATALOG_SHA256 = "5aee4d567b08d251d5693ef06d62fa543603d5c3e33fdd2fae6802e1ca724634"
EVALUATION_CATALOG_SHA256 = "b3b022a32aae3fb1e7a3679b98108958359a49988f5cb99f2a09e662f264f072"
CELL_SCHEMA_SHA256 = "df5faeb082fce88cbbe486660d45c4e82fc7bc4d09de76b6544d605a63652da2"
RUN_SCHEMA_SHA256 = "41580fe2729a20d0d86f9a2a1c89840aed7ef622e7a3292f7ed1b29bb595198a"
POLICY_FILE_SHA256 = "3b9ac21c2577311d004bd81c1cf8af0ab57c0f56f30a32e4a10a795045a96f17"
POLICY_SHA256 = "3e358f52982a173d7bbf20db6f556953bf1b246026b14c6cc7072d210054ebec"
POLICY_CONTRACT_SHA256 = "9050300de8ce84b25a7ffd2a7c30e9182cb444336e4a489a70b5a43d793ac04d"
REPORT_SCHEMA_SHA256 = "b2bc4ae8e6ff1c5e673888dcfef92b59d1953a67267676fe97c5d1a9b7d25cad"

REPORT_ID = "INTERP-001B-M1-CONFORMANCE-REPORT"
REPORT_VERSION = "1.0.0"
EVALUATOR_ID = "INTERP-001B-M1-CONFORMANCE-EVALUATOR"
EVALUATOR_VERSION = "1.0.0"
BUNDLE_CANONICALIZATION_ID = "interp-source-bundle-v2-policy-bindings-elided"
BUNDLE_PATHS = {
    "runner": (
        "dynamics/labs/interp_m1_common.py",
        "dynamics/labs/interp_m1_runner.py",
        "dynamics/labs/interp_m1_run_cli.py",
        "dynamics/labs/interp_m1_cli.py",
    ),
    "evaluator": (
        "dynamics/labs/interp_m1_common.py",
        "dynamics/labs/interp_m1_evaluator.py",
        "dynamics/labs/interp_m1_evaluate_cli.py",
        "dynamics/labs/interp_m1_cli.py",
    ),
}
ELIDED_EVALUATOR_POLICY_BINDINGS = (
    "POLICY_FILE_SHA256",
    "POLICY_SHA256",
    "POLICY_CONTRACT_SHA256",
)


class FrozenEvaluationInputError(ValueError):
    """Fail closed before report construction when a frozen input is invalid."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _sha(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _source_sha256() -> str:
    return _sha(Path(__file__).read_bytes())


def _bundle_file_sha256(relative_path: str) -> str:
    source = (Path(__file__).resolve().parents[2] / relative_path).read_bytes()
    if relative_path != "dynamics/labs/interp_m1_evaluator.py":
        return _sha(source)
    text = source.decode("utf-8")
    for name in ELIDED_EVALUATOR_POLICY_BINDINGS:
        pattern = rf'(?m)^({name}\s*=\s*)"[0-9a-f]{{64}}"$'
        text, count = re.subn(pattern, rf'\1"<ELIDED>"', text)
        if count != 1:
            raise ValueError(f"evaluator policy binding literal is not unique: {name}")
    return _sha(text.encode("utf-8"))


def _source_bundle_sha256(role: str) -> str:
    try:
        paths = BUNDLE_PATHS[role]
    except KeyError as error:
        raise ValueError(f"unknown source bundle role: {role}") from error
    return digest(
        [
            {"path": path, "sha256": _bundle_file_sha256(path)}
            for path in paths
        ]
    )


def _fail(code: str, message: str) -> None:
    raise FrozenEvaluationInputError(code, message)


def _exact_file(source: bytes, expected: str, label: str) -> dict[str, Any]:
    if _sha(source) != expected:
        _fail("ARTIFACT_BINDING_MISMATCH", f"{label} file hash mismatch")
    try:
        return loads_exact(source)
    except (UnicodeDecodeError, ValueError) as error:
        _fail("ARTIFACT_BINDING_MISMATCH", f"{label} is not exact JSON: {error}")


def _index(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item[key]
        if value in result:
            _fail("ARTIFACT_BINDING_MISMATCH", f"duplicate {key}: {value}")
        result[value] = item
    return result


def _verify_source_bundle_bindings(policy_body: dict[str, Any]) -> dict[str, str]:
    actual: dict[str, str] = {}
    identities = policy_body.get("implementation_identities")
    if not isinstance(identities, dict):
        _fail("ARTIFACT_BINDING_MISMATCH", "implementation identities missing")
    for role in ("runner", "evaluator"):
        identity = identities.get(role)
        binding = identity.get("source_bundle") if isinstance(identity, dict) else None
        expected_paths = list(BUNDLE_PATHS[role])
        if not isinstance(binding, dict) or set(binding) != {
            "canonicalization_id",
            "paths",
            "bundle_sha256",
        }:
            _fail("ARTIFACT_BINDING_MISMATCH", f"source bundle binding malformed: {role}")
        if (
            binding["canonicalization_id"] != BUNDLE_CANONICALIZATION_ID
            or binding["paths"] != expected_paths
        ):
            _fail("ARTIFACT_BINDING_MISMATCH", f"source bundle definition changed: {role}")
        try:
            actual[role] = _source_bundle_sha256(role)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"source bundle cannot be resolved: {role}: {error}")
        if binding["bundle_sha256"] != actual[role]:
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"source bundle differs from frozen policy: {role}")
    return actual


def _bind_inputs(
    execution_bytes: bytes,
    evaluation_bytes: bytes,
    cell_schema_bytes: bytes,
    run_schema_bytes: bytes,
    run_bytes: bytes,
    policy_bytes: bytes,
    report_schema_bytes: bytes,
) -> dict[str, Any]:
    execution = _exact_file(execution_bytes, EXECUTION_FILE_SHA256, "execution manifest")
    evaluation = _exact_file(evaluation_bytes, EVALUATION_FILE_SHA256, "evaluation manifest")
    cell_schema = _exact_file(cell_schema_bytes, CELL_SCHEMA_SHA256, "cell result schema")
    run_schema = _exact_file(run_schema_bytes, RUN_SCHEMA_SHA256, "run artifact schema")
    policy = _exact_file(policy_bytes, POLICY_FILE_SHA256, "evaluator policy")
    report_schema = _exact_file(report_schema_bytes, REPORT_SCHEMA_SHA256, "report schema")
    try:
        run = loads_exact(run_bytes)
    except (UnicodeDecodeError, ValueError) as error:
        _fail("INPUT_INTEGRITY_FAILURE", f"run is not exact JSON: {error}")
    try:
        validate_json_schema(run, run_schema)
    except ValueError as error:
        _fail("INPUT_INTEGRITY_FAILURE", f"run failed its closed-world schema: {error}")

    pairs = (
        (execution, "manifest", "execution_contract", EXECUTION_MANIFEST_SHA256, EXECUTION_CONTRACT_SHA256),
        (evaluation, "manifest", "evaluation_contract", EVALUATION_MANIFEST_SHA256, EVALUATION_CONTRACT_SHA256),
    )
    for envelope, manifest_key, contract_key, manifest_hash, contract_hash in pairs:
        try:
            manifest = envelope[manifest_key]
            integrity = envelope["integrity"]
        except KeyError as error:
            _fail("ARTIFACT_BINDING_MISMATCH", f"manifest field missing: {error.args[0]}")
        if digest(manifest) != integrity.get("manifest_sha256") or integrity.get("manifest_sha256") != manifest_hash:
            _fail("ARTIFACT_BINDING_MISMATCH", "manifest internal hash mismatch")
        if digest(manifest[contract_key]) != integrity.get("contract_sha256") or integrity.get("contract_sha256") != contract_hash:
            _fail("ARTIFACT_BINDING_MISMATCH", "contract internal hash mismatch")

    try:
        policy_body = policy["policy"]
        policy_integrity = policy["integrity"]
    except KeyError as error:
        _fail("ARTIFACT_BINDING_MISMATCH", f"policy field missing: {error.args[0]}")
    if digest(policy_body) != POLICY_SHA256 or policy_integrity.get("policy_sha256") != POLICY_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "policy internal hash mismatch")
    if digest(policy_body["evaluation_contract"]) != POLICY_CONTRACT_SHA256 or policy_integrity.get("contract_sha256") != POLICY_CONTRACT_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "policy contract hash mismatch")
    source_bundles = _verify_source_bundle_bindings(policy_body)

    bindings = policy_body["artifact_bindings"]
    expected_binding_files = {
        "execution_manifest": EXECUTION_FILE_SHA256,
        "evaluation_manifest": EVALUATION_FILE_SHA256,
        "cell_result_schema": CELL_SCHEMA_SHA256,
        "run_artifact_schema": RUN_SCHEMA_SHA256,
        "conformance_report_schema": REPORT_SCHEMA_SHA256,
    }
    for name, expected in expected_binding_files.items():
        if bindings[name]["file_sha256"] != expected:
            _fail("ARTIFACT_BINDING_MISMATCH", f"policy binding changed: {name}")

    execution_contract = execution["manifest"]["execution_contract"]
    evaluation_contract = evaluation["manifest"]["evaluation_contract"]
    if digest(evaluation_contract["predicate_declarations"]) != PREDICATE_CATALOG_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "predicate catalog hash mismatch")
    catalog = {
        key: evaluation_contract[key]
        for key in (
            "closed_world_signatures",
            "semantic_signatures",
            "cell_assertions",
            "mirror_relations",
            "pair_assertions",
            "matrix_assertions",
            "global_invariants",
            "retirement_rules",
        )
    }
    if digest(catalog) != EVALUATION_CATALOG_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "evaluation catalog hash mismatch")

    try:
        run_body = run["run"]
        run_integrity = run["integrity"]
    except KeyError as error:
        _fail("INPUT_INTEGRITY_FAILURE", f"run field missing: {error.args[0]}")
    if run_integrity != {"algorithm": "sha256", "run_sha256": digest(run_body)}:
        _fail("INPUT_INTEGRITY_FAILURE", "run envelope integrity mismatch")
    expected_run_metadata = {
        "run_id": "INTERP-001B-M1-RUN",
        "run_version": "1.0.0",
        "status": "EXECUTED_SYNTHETIC_RESULT",
        "runner_input_kind": "execution_manifest_only",
        "evaluation_manifest_visible": False,
        "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
        "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
        "fixed_factor_sha256": digest(execution_contract["fixed_factors"]),
    }
    if any(run_body.get(key) != value for key, value in expected_run_metadata.items()):
        _fail("INPUT_INTEGRITY_FAILURE", "run metadata mismatch")
    runner_path = Path(__file__).with_name("interp_m1_runner.py")
    if not runner_path.is_file() or run_body.get("runner_implementation_sha256") != _sha(runner_path.read_bytes()):
        _fail("IMPLEMENTATION_BINDING_MISMATCH", "runner source binding mismatch")
    if run_body.get("runner_bundle_sha256") != source_bundles["runner"]:
        _fail("IMPLEMENTATION_BINDING_MISMATCH", "runner source bundle binding mismatch")

    declarations = evaluation_contract["predicate_declarations"]
    declared = {item["predicate_id"] for item in declarations}
    references = {
        relation["predicate"]
        for signature in evaluation_contract["semantic_signatures"]
        for relation in signature["expected_relations"]
    }
    references.update(
        assertion["predicate"]
        for group in ("mirror_relations", "pair_assertions", "matrix_assertions", "global_invariants", "retirement_rules")
        for assertion in evaluation_contract[group]
    )
    references.update(
        relation["predicate"]
        for relation in evaluation_contract["closed_world_signatures"]["default_relations"]
    )
    if references - declared:
        _fail("UNKNOWN_PREDICATE", f"unknown predicates: {sorted(references - declared)}")
    if declared - references:
        _fail("DEAD_PREDICATE_DECLARATION", f"dead predicates: {sorted(declared - references)}")

    return {
        "execution": execution,
        "evaluation": evaluation,
        "cell_schema": cell_schema,
        "run_schema": run_schema,
        "run": run,
        "policy": policy,
        "report_schema": report_schema,
        "execution_contract": execution_contract,
        "evaluation_contract": evaluation_contract,
        "source_bundles": source_bundles,
    }


def _path_values(root: dict[str, Any], path: str) -> tuple[list[Any], bool]:
    if not path.startswith("/"):
        raise ValueError("semantic path must be absolute")
    values: list[Any] = [root]
    wildcard = False
    for part in path[1:].split("/"):
        next_values: list[Any] = []
        if part == "*":
            wildcard = True
            for value in values:
                if not isinstance(value, list):
                    raise ValueError(f"wildcard applied to non-list: {path}")
                next_values.extend(value)
        else:
            for value in values:
                if not isinstance(value, dict) or part not in value:
                    raise ValueError(f"path does not resolve: {path}")
                next_values.append(value[part])
        values = next_values
    return values, wildcard


def _profile_max(profiles: list[dict[str, Any]], neutral: dict[str, Any]) -> dict[str, Any]:
    if not profiles:
        return deepcopy(neutral)
    precedence = {
        "source_unresolved": 0,
        "withheld_control": 1,
        "not_declared_by_fixture": 2,
        "operator_undefined": 3,
        "not_applicable": 4,
    }
    result: dict[str, Any] = {}
    for axis in ("positive_direction_fit", "negative_direction_fit", "ambiguity", "activation"):
        components = [profile[axis] for profile in profiles]
        missing = [value["reason"] for value in components if value["status"] == "missing"]
        result[axis] = (
            {"status": "missing", "reason": min(missing, key=precedence.__getitem__)}
            if missing
            else {"status": "present", "rank": max(value["rank"] for value in components)}
        )
    return result


def _fixture_context(contract: dict[str, Any], fixture_key: str, protocol_step: int) -> dict[str, Any]:
    fixtures = _index(contract["fixture_declarations"], "fixture_key")
    materials = _index(contract["materials"], "material_key")
    profiles = _index(contract["source_encounter_profiles"], "profile_key")
    occurrences = _index(contract["source_occurrences"], "occurrence_key")
    fixture = fixtures[fixture_key]
    try:
        step = next(item for item in fixture["protocol_steps"] if item["step"] == protocol_step)
    except StopIteration:
        raise ValueError("fixture step missing") from None
    access = step["access"]
    keys = list(access.get("source_material_keys_ordered", [])) if access["present"] else []
    source_materials = [materials[key] for key in keys]
    source_profiles = [profile_without_key(profiles[item["source_encounter_profile_key"]]) for item in source_materials]
    source_occurrences: list[str] = []
    evidence_keys: list[str] = []
    for item in source_materials:
        occurrence = occurrences[item["source_occurrence_key"]]
        if occurrence["occurrence_key"] not in source_occurrences:
            source_occurrences.append(occurrence["occurrence_key"])
        if occurrence["evidence_projection_key"] not in evidence_keys:
            evidence_keys.append(occurrence["evidence_projection_key"])
    encounter = (
        _profile_max(source_profiles, profile_without_key(profiles["sp005"]))
        if access["present"]
        else {"status": "missing", "reason": "not_applicable"}
    )
    lineage = []
    if access["present"]:
        lineage = [{
            "current_occurrence_key": access["current_occurrence_key"],
            "source_occurrence_keys_ordered": source_occurrences,
            "relation": (
                "reexposure_to_prior_access_sources"
                if access.get("reaccess_of_access_key") is not None
                else "new_access_to_sources"
            ),
        }]
    return {
        "fixture": fixture,
        "step": step,
        "access": access,
        "material_keys": keys,
        "materials": source_materials,
        "profiles": source_profiles,
        "encounter": encounter,
        "lineage": lineage,
        "evidence_keys": evidence_keys if access["present"] else [],
    }


def _assembly_pairs(step_result: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for assembly in step_result["semantic"]["assemblies"]:
        members = [item["material_key"] for item in assembly["memberships"]]
        for edge in assembly["induced_topology_edges"]:
            pairs.add(tuple(sorted((members[edge["left_order"]], members[edge["right_order"]]))))
    return pairs


def _expected_prefix(cell: dict[str, Any], step_index: int, context: dict[str, Any]) -> str:
    if not context["access"]["present"]:
        return "unchanged"
    prior_present = [
        item for item in context["fixture"]["protocol_steps"][:step_index]
        if item["access"]["present"]
    ]
    if not prior_present:
        return "initial"
    prefix: set[tuple[str, str]] = set()
    for prior_result in cell["steps"][:step_index]:
        prefix.update(_assembly_pairs(prior_result))
    return "extended" if _assembly_pairs(cell["steps"][step_index]) - prefix else "unchanged"


def _relation_ok(
    relation: dict[str, Any],
    step_result: dict[str, Any],
    cell: dict[str, Any],
    step_index: int,
    context: dict[str, Any],
) -> bool:
    values, wildcard = _path_values(step_result, relation["path"])
    actual: Any = values if wildcard else values[0]
    predicate = relation["predicate"]
    expected = relation["value"]
    if predicate == "count_eq":
        return isinstance(actual, int) and not isinstance(actual, bool) and actual == expected or isinstance(actual, list) and len(actual) == expected
    if predicate == "eq":
        return all(digest(value) == digest(expected) for value in values) if wildcard else digest(actual) == digest(expected)
    if predicate == "list_eq":
        return isinstance(actual, list) and digest(actual) == digest(expected)
    if predicate == "set_eq":
        candidates = values if wildcard else [actual]
        return all(isinstance(value, list) and sorted(set(value)) == expected for value in candidates)
    if predicate == "same_as_fixture":
        fixture_value = {
            "encounter_policy_projection_or_not_applicable": context["encounter"],
            "current_access_lineage_or_empty": context["lineage"],
            "evidence_projection_keys_ordered": context["evidence_keys"],
            "neutral_profile_sp005": context["encounter"],
        }.get(expected)
        return fixture_value is not None and digest(actual) == digest(fixture_value)
    if predicate == "none_supplied":
        return actual == []
    if predicate == "all_supplied":
        supplied = context["material_keys"]
        if relation["path"] == "/semantic/settlement_relations":
            return actual == [{"material_key": key, "relation": expected} for key in supplied]
        return actual == supplied
    if predicate == "same_source_lineage":
        if expected is not True or not actual or not context["access"].get("reaccess_of_access_key"):
            return False
        prior = [item for item in context["fixture"]["protocol_steps"][:step_index] if item["access"]["present"]]
        if not prior:
            return False
        prior_access = prior[-1]["access"]
        # The expected current lineage was resolved above; source equality is
        # expressed by its reexposure relation and the frozen prior-access ref.
        return (
            actual == context["lineage"]
            and context["access"].get("reexposure_of_occurrence_key") == prior_access["current_occurrence_key"]
            and context["access"]["current_occurrence_key"] != prior_access["current_occurrence_key"]
        )
    if predicate == "prefix_eq":
        guards_ok = all(
            value["before_sha256"] == value["after_sha256"] and value["delta_count"] == 0
            for value in step_result["guard_ledgers"].values()
        )
        return expected is True and guards_ok and actual == _expected_prefix(cell, step_index, context)
    raise ValueError(f"unsupported signature predicate: {predicate}")


def _resolved_relations(evaluation_contract: dict[str, Any], signature_id: str, semantic_order: list[str]) -> list[dict[str, Any]]:
    signatures = _index(evaluation_contract["semantic_signatures"], "signature_id")
    signature = signatures[signature_id]
    defaults = evaluation_contract["closed_world_signatures"]["default_relations"]
    explicit = signature["expected_relations"]
    by_field: dict[str, list[dict[str, Any]]] = {}
    for relation in explicit:
        field = relation["path"].split("/")[2]
        by_field.setdefault(field, []).append(relation)
    for relation in defaults:
        field = relation["path"].split("/")[2]
        if field not in by_field:
            by_field[field] = [relation]
    return [deepcopy(relation) for field in semantic_order for relation in by_field.get(field, [])]


def _evaluate_signatures(
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cell_schema: dict[str, Any],
    cells: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, int], dict[str, Any]]]:
    expected_by_fixture = {
        item["fixture_key"]: item["expected_by_model"]
        for item in evaluation_contract["cell_assertions"]
    }
    semantic_order = list(cell_schema["$defs"]["semantic"]["properties"])
    results: list[dict[str, Any]] = []
    lookup: dict[tuple[str, str, int], dict[str, Any]] = {}
    for cell in cells:
        signatures = expected_by_fixture[cell["fixture_key"]][cell["model_id"]]
        for step_index, (step_result, signature_id) in enumerate(zip(cell["steps"], signatures)):
            context = _fixture_context(contract, cell["fixture_key"], step_result["protocol_step"])
            relations = _resolved_relations(evaluation_contract, signature_id, semantic_order)
            failed: list[str] = []
            for relation in relations:
                try:
                    passed = _relation_ok(relation, step_result, cell, step_index, context)
                except (KeyError, IndexError, TypeError, ValueError):
                    passed = False
                if not passed and relation["path"] not in failed:
                    failed.append(relation["path"])
            item = {
                "fixture_key": cell["fixture_key"],
                "model_id": cell["model_id"],
                "protocol_step": step_result["protocol_step"],
                "signature_id": signature_id,
                "status": "PASS" if not failed else "FAIL",
                "evaluated_relation_count": len(relations),
                "failed_relation_paths": failed,
                "failure_codes": [] if not failed else ["SIGNATURE_RELATION_FAILURE"],
            }
            results.append(item)
            lookup[(cell["fixture_key"], cell["model_id"], step_result["protocol_step"])] = item
    return results, lookup


def _cell_map(cells: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(cell["fixture_key"], cell["model_id"]): cell for cell in cells}


def _step(cell: dict[str, Any], protocol_step: int) -> dict[str, Any]:
    return next(item for item in cell["steps"] if item["protocol_step"] == protocol_step)


def _swap_directions(value: Any) -> Any:
    token_swap = {
        "positive": "negative",
        "negative": "positive",
        "adopted_positive": "adopted_negative",
        "adopted_negative": "adopted_positive",
    }
    if isinstance(value, str):
        return token_swap.get(value, value)
    if isinstance(value, list):
        return [_swap_directions(item) for item in value]
    if isinstance(value, dict):
        result = {key: _swap_directions(item) for key, item in value.items()}
        for left, right in (
            ("positive_direction_fit", "negative_direction_fit"),
            ("raw_positive_support", "raw_negative_support"),
        ):
            if left in result or right in result:
                result[left], result[right] = result.get(right), result.get(left)
        return result
    return value


def _normalize_step_for_mirror(
    contract: dict[str, Any], fixture_key: str, result: dict[str, Any], *, swap_sign: bool
) -> dict[str, Any]:
    context = _fixture_context(contract, fixture_key, result["protocol_step"])
    positions = {key: index for index, key in enumerate(context["material_keys"])}
    occurrence_positions = {
        material["source_occurrence_key"]: index
        for index, material in enumerate(context["materials"])
    }
    semantic = deepcopy(result["semantic"])
    semantic["accessed_material_keys_ordered"] = [positions[key] for key in semantic["accessed_material_keys_ordered"]]
    semantic["not_accessed_material_keys_ordered"] = [positions[key] for key in semantic["not_accessed_material_keys_ordered"]]
    for assembly in semantic["assemblies"]:
        for membership in assembly["memberships"]:
            membership["material_key"] = positions[membership["material_key"]]
    for settlement in semantic["settlement_relations"]:
        settlement["material_key"] = positions[settlement["material_key"]]
    semantic["encounter_source_lineage"] = [
        {
            "current_occurrence_role": context["access"].get("access_ordinal"),
            "source_occurrence_roles_ordered": [occurrence_positions[key] for key in item["source_occurrence_keys_ordered"]],
            "relation": item["relation"],
        }
        for item in semantic["encounter_source_lineage"]
    ]
    semantic["evidence_projection_keys_ordered"] = list(range(len(semantic["evidence_projection_keys_ordered"])))
    audit = {
        key: value["status"]
        for key, value in result["transport_access_audit"].items()
        if isinstance(value, dict) and "status" in value
    }
    audit.update({
        "access_present": result["transport_access_audit"]["access_present"],
        "transport_redelivery_present": result["transport_access_audit"]["transport_redelivery_present"],
    })
    normalized = {
        "protocol_step": result["protocol_step"],
        "operator_invocations": result["operator_invocations"],
        "transport_access_audit": audit,
        "semantic": semantic,
        "guard_ledgers": result["guard_ledgers"],
    }
    return _swap_directions(normalized) if swap_sign else normalized


def _access_projection(step_result: dict[str, Any]) -> object:
    semantic = step_result["semantic"]
    return [semantic["accessed_material_keys_ordered"], semantic["not_accessed_material_keys_ordered"]]


def _coherence_projection(step_result: dict[str, Any]) -> object:
    semantic = step_result["semantic"]
    return [semantic["assemblies"], semantic["binding_candidates"], semantic["adjudications"]]


def _semantic_projection(cell: dict[str, Any]) -> object:
    return [item["semantic"] for item in cell["steps"]]


def _assert_mirror(
    assertion: dict[str, Any], contract: dict[str, Any], cells: dict[tuple[str, str], dict[str, Any]]
) -> bool:
    left_fixture, right_fixture = assertion["operands"][:2]
    sign = assertion["predicate"] == "sign_mirror_eq"
    for model_id in ("R0", "R1", "R2", "R3"):
        left = cells[(left_fixture, model_id)]["steps"]
        right = cells[(right_fixture, model_id)]["steps"]
        if len(left) != len(right):
            return False
        for left_step, right_step in zip(left, right):
            if digest(_normalize_step_for_mirror(contract, left_fixture, left_step, swap_sign=False)) != digest(
                _normalize_step_for_mirror(contract, right_fixture, right_step, swap_sign=sign)
            ):
                return False
    return True


def _assembly_content_exact(
    contract: dict[str, Any], fixture_key: str, step_result: dict[str, Any]
) -> bool:
    context = _fixture_context(contract, fixture_key, step_result["protocol_step"])
    if not context["access"]["present"]:
        return step_result["semantic"]["assemblies"] == []
    accessed = step_result["semantic"]["accessed_material_keys_ordered"]
    accessed_set = set(accessed)
    topology = _index(contract["topologies"], "topology_key")[context["step"]["topology_key"]]
    adjacency = {key: set() for key in accessed}
    for edge in topology["edges"]:
        left, right = edge["left_material_key"], edge["right_material_key"]
        if left in accessed_set and right in accessed_set:
            adjacency[left].add(right)
            adjacency[right].add(left)
    components: list[list[str]] = []
    seen: set[str] = set()
    for start in accessed:
        if start in seen:
            continue
        stack = [start]
        component: list[str] = []
        seen.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            neighbours = [item for item in accessed if item in adjacency[node]]
            for neighbour in reversed(neighbours):
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        component.sort(key=accessed.index)
        if len(component) >= 2:
            components.append(component)
    expected = []
    for component in components:
        order = {key: index for index, key in enumerate(component)}
        edges = []
        for edge in topology["edges"]:
            if edge["left_material_key"] in order and edge["right_material_key"] in order:
                left, right = sorted((order[edge["left_material_key"]], order[edge["right_material_key"]]))
                edges.append({"left_order": left, "right_order": right, "strength": edge["strength"]})
        edges.sort(key=lambda item: (item["left_order"], item["right_order"], canonical_bytes(item["strength"])))
        expected.append({
            "memberships": [
                {"material_key": key, "role": "member", "order": index}
                for index, key in enumerate(component)
            ],
            "induced_topology_edges": edges,
        })
    actual = [
        {"memberships": item["memberships"], "induced_topology_edges": item["induced_topology_edges"]}
        for item in step_result["semantic"]["assemblies"]
    ]
    return digest(actual) == digest(expected)


def _candidate_profiles_exact(
    contract: dict[str, Any], fixture_key: str, step_result: dict[str, Any]
) -> bool:
    materials = _index(contract["materials"], "material_key")
    profiles = _index(contract["source_encounter_profiles"], "profile_key")
    semantic = step_result["semantic"]
    if len(semantic["assemblies"]) != len(semantic["binding_candidates"]):
        return False
    for assembly, candidate in zip(semantic["assemblies"], semantic["binding_candidates"]):
        member_profiles = [
            profile_without_key(profiles[materials[item["material_key"]]["source_encounter_profile_key"]])
            for item in assembly["memberships"]
        ]
        expected = _profile_max(member_profiles, {})
        if candidate["raw_positive_support"] != expected["positive_direction_fit"]:
            return False
        if candidate["raw_negative_support"] != expected["negative_direction_fit"]:
            return False
        if candidate["raw_ambiguity"] != expected["ambiguity"]:
            return False
    return True


def _operator_logs_exact(contract: dict[str, Any], cell: dict[str, Any]) -> bool:
    models = _index(contract["model_declarations"], "model_id")
    operators = _index(contract["operator_declarations"], "operator_id")
    views = _index(contract["operator_input_views"], "view_id")
    phase_order = contract["phase_contract"]["phase_order"]
    phase_rank = {phase: index for index, phase in enumerate(phase_order)}
    expected_ops = models[cell["model_id"]]["ordered_operator_refs"]
    fixture = _index(contract["fixture_declarations"], "fixture_key")[cell["fixture_key"]]
    for result, fixture_step in zip(cell["steps"], fixture["protocol_steps"]):
        logs = result["operator_invocations"]
        if [item["operator_id"] for item in logs] != expected_ops:
            return False
        if [phase_rank[item["phase"]] for item in logs] != sorted(phase_rank[item["phase"]] for item in logs):
            return False
        for log in logs:
            declaration = operators[log["operator_id"]]
            view = views[declaration["input_view_id"]]
            inspected = [item["field_id"] for item in view["fields"] if item["operator_use"] == "inspect"]
            passed = [item["field_id"] for item in view["fields"] if item["operator_use"] == "pass_through_only"]
            if log["input_view_id"] != view["view_id"] or log["inspected_fields"] != inspected or log["pass_through_fields"] != passed:
                return False
            if log["invocation_count"] != int(fixture_step["access"]["present"]):
                return False
    return True


def _evaluate_declared_predicate(
    predicate: str,
    operands: list[Any],
    *,
    contract: dict[str, Any],
    cells: dict[tuple[str, str], dict[str, Any]],
    signature_lookup: dict[tuple[str, str, int], dict[str, Any]],
) -> bool:
    models = contract["execution_matrix"]["model_ids"]
    fixtures = contract["execution_matrix"]["fixture_keys"]
    all_cells = list(cells.values())
    if predicate == "same_semantic_signature":
        def ref(value: str) -> dict[str, Any]:
            fixture, model, step = value.split(":")
            return signature_lookup[(fixture, model, int(step))]
        left, right = map(ref, operands)
        return left["status"] == right["status"] == "PASS" and left["signature_id"] == right["signature_id"]
    if predicate in {"access_differs_coherence_policy_same", "access_same_coherence_differs"}:
        def result(value: str) -> tuple[dict[str, Any], dict[str, Any]]:
            fixture, model, number = value.split(":")
            cell = cells[(fixture, model)]
            return cell, _step(cell, int(number))
        (left_cell, left), (right_cell, right) = map(result, operands)
        access_equal = digest(_access_projection(left)) == digest(_access_projection(right))
        coherence_equal = digest(_coherence_projection(left)) == digest(_coherence_projection(right))
        left_coherence = next(item["operator_id"] for item in left["operator_invocations"] if item["phase"] == "candidate_coherence")
        right_coherence = next(item["operator_id"] for item in right["operator_invocations"] if item["phase"] == "candidate_coherence")
        return (not access_equal and left_coherence == right_coherence) if predicate.startswith("access_differs") else (access_equal and not coherence_equal)
    if predicate == "r1_access_equals_r0_and_r3_coherence_equals_r2":
        fixture, r0, r1, r2, r3 = operands
        return all(
            digest(_access_projection(a)) == digest(_access_projection(b))
            for a, b in zip(cells[(fixture, r0)]["steps"], cells[(fixture, r1)]["steps"])
        ) and all(
            digest(_coherence_projection(a)) == digest(_coherence_projection(b))
            for a, b in zip(cells[(fixture, r2)]["steps"], cells[(fixture, r3)]["steps"])
        )
    if predicate == "all_models_adopt_fixture_direction":
        for fixture, direction in zip(operands, ("positive", "negative")):
            if any(
                any(item["outcome"] != f"adopted_{direction}" for item in cells[(fixture, model)]["steps"][0]["semantic"]["adjudications"])
                or not cells[(fixture, model)]["steps"][0]["semantic"]["adjudications"]
                for model in models
            ):
                return False
        return True
    if predicate == "step_signature_all_models":
        left, right, step_number, signature_id = operands
        return all(
            signature_lookup[(fixture, model, step_number)]["status"] == "PASS"
            and signature_lookup[(fixture, model, step_number)]["signature_id"] == signature_id
            for fixture in (left, right) for model in models
        )
    if predicate == "transport_redelivery_lineage_exact":
        left, right, prior_number, redelivery_number = operands
        for fixture in (left, right):
            fixture_decl = _index(contract["fixture_declarations"], "fixture_key")[fixture]
            prior_decl = fixture_decl["protocol_steps"][prior_number - 1]
            redelivery_decl = fixture_decl["protocol_steps"][redelivery_number - 1]
            declaration = redelivery_decl["transport_redelivery"]
            for model in models:
                audit = _step(cells[(fixture, model)], redelivery_number)["transport_access_audit"]
                if audit["access_present"] or not audit["transport_redelivery_present"]:
                    return False
                if audit["current_occurrence_key"].get("key") != prior_decl["access"]["current_occurrence_key"]:
                    return False
                if audit["transport_delivery_key"].get("key") != declaration["delivery_key"] or audit["redelivery_of_delivery_key"].get("key") != declaration["redelivery_of_delivery_key"]:
                    return False
        return True
    if predicate == "reaccess_new_encounter_same_source_prefix_unchanged":
        left, right, prior_number, reaccess_number = operands
        for fixture in (left, right):
            declaration = _index(contract["fixture_declarations"], "fixture_key")[fixture]
            prior = declaration["protocol_steps"][prior_number - 1]["access"]
            current = declaration["protocol_steps"][reaccess_number - 1]["access"]
            if current.get("reaccess_of_access_key") != prior["access_key"] or current.get("reexposure_of_occurrence_key") != prior["current_occurrence_key"]:
                return False
            if len({current["access_key"], prior["access_key"]}) != 2 or len({current["current_occurrence_key"], prior["current_occurrence_key"]}) != 2:
                return False
            for model in models:
                result = _step(cells[(fixture, model)], reaccess_number)
                if result["semantic"]["prior_prefix_relation"] not in {"unchanged", "extended"}:
                    return False
                if result["semantic"]["encounter_source_lineage"] != _fixture_context(contract, fixture, reaccess_number)["lineage"]:
                    return False
        return True
    if predicate == "all_declared_cells_reported_once":
        return len(cells) == operands[2] == operands[0] * operands[1] and set(cells) == {(f, m) for f in fixtures for m in models}
    if predicate in {"r3_access_equals_r1_for_every_step", "r2_access_equals_r0_for_every_step"}:
        left, right = operands
        return all(
            all(digest(_access_projection(a)) == digest(_access_projection(b)) for a, b in zip(cells[(fixture, left)]["steps"], cells[(fixture, right)]["steps"]))
            for fixture in fixtures
        )
    if predicate == "r3_coherence_equals_r2_given_same_assembly":
        left, right = operands
        for fixture in fixtures:
            for a, b in zip(cells[(fixture, left)]["steps"], cells[(fixture, right)]["steps"]):
                if digest(a["semantic"]["assemblies"]) == digest(b["semantic"]["assemblies"]) and digest(_coherence_projection(a)) != digest(_coherence_projection(b)):
                    return False
        return True
    if predicate == "r0_operator_access_log_excludes_reception":
        model = operands[0]
        return all(
            all("reception_profile" not in log["inspected_fields"] and log["input_view_id"] not in {"iv003", "iv007"} for step_result in cell["steps"] for log in step_result["operator_invocations"])
            for (fixture, model_id), cell in cells.items() if model_id == model
        )
    if predicate == "runner_receives_execution_manifest_only":
        return operands == ["INTERP-001A2-M1-EXECUTION", "INTERP-001A2-M1-EVALUATION"] and all(
            cell["execution_manifest_sha256"] == EXECUTION_MANIFEST_SHA256 for cell in all_cells
        )
    if predicate == "evidence_projection_prefix_equal_before_after":
        projection = operands[0]
        occurrence_by_key = _index(contract["source_occurrences"], "occurrence_key")
        material_by_key = _index(contract["materials"], "material_key")
        for cell in all_cells:
            for result in cell["steps"]:
                context = _fixture_context(contract, cell["fixture_key"], result["protocol_step"])
                expected = []
                for key in context["material_keys"]:
                    evidence = occurrence_by_key[material_by_key[key]["source_occurrence_key"]]["evidence_projection_key"]
                    if evidence not in expected:
                        expected.append(evidence)
                if result["semantic"]["evidence_projection_keys_ordered"] != expected or any(key != projection for key in expected):
                    return False
                guard = result["guard_ledgers"]["evidence_links"]
                if guard["before_sha256"] != guard["after_sha256"] or guard["delta_count"] != 0:
                    return False
        return True
    if predicate == "guard_ledgers_equal_every_step":
        return all(
            set(result["guard_ledgers"]) == set(operands)
            and all(value["before_sha256"] == value["after_sha256"] and value["delta_count"] == 0 for value in result["guard_ledgers"].values())
            for cell in all_cells for result in cell["steps"]
        )
    if predicate == "same_fixed_factor_all_cells":
        return operands[0] in {value["fixture_key"] for value in contract["fixed_factors"].values()}
    if predicate == "same_source_same_subjective_profile_across_models":
        for fixture in fixtures:
            profiles = [[step["semantic"]["subjective_form_profile"] for step in cells[(fixture, model)]["steps"]] for model in models]
            if any(digest(profile) != digest(profiles[0]) for profile in profiles[1:]):
                return False
        return True
    if predicate == "single_pass_phase_order":
        return operands == contract["phase_contract"]["phase_order"] and all(_operator_logs_exact(contract, cell) for cell in all_cells)
    if predicate == "prior_source_encounter_and_material_prefix_equal":
        for fixture in operands:
            for model in models:
                for result in cells[(fixture, model)]["steps"]:
                    if any(
                        result["guard_ledgers"][name]["before_sha256"] != result["guard_ledgers"][name]["after_sha256"]
                        for name in ("source_encounters", "source_materials", "source_occurrences")
                    ):
                        return False
        return True
    if predicate == "positive_negative_axes_preserved_separately":
        profile_fields = set(contract["source_encounter_profiles"][0])
        reception_fields = set(contract["reception_profiles"][0])
        return set(operands[:2]) <= profile_fields and set(operands[2:]) <= reception_fields and all(
            {"positive_direction_fit", "negative_direction_fit"} <= set(result["semantic"]["subjective_form_profile"])
            for cell in all_cells for result in cell["steps"] if result["semantic"]["subjective_form_profile"].get("status") != "missing"
        )
    if predicate == "assembly_identity_normalization_holds":
        for cell in all_cells:
            for result in cell["steps"]:
                for assembly in result["semantic"]["assemblies"]:
                    memberships = assembly["memberships"]
                    if len({item["material_key"] for item in memberships}) != len(memberships) or [item["order"] for item in memberships] != list(range(len(memberships))):
                        return False
                    edges = assembly["induced_topology_edges"]
                    tuples = [(e["left_order"], e["right_order"], canonical_bytes(e["strength"])) for e in edges]
                    if any(left >= right for left, right, _ in tuples) or tuples != sorted(tuples) or len(tuples) != len(set(tuples)):
                        return False
        return True
    if predicate == "assembly_membership_and_topology_equal_fixture_induced_component":
        return all(_assembly_content_exact(contract, cell["fixture_key"], result) for cell in all_cells for result in cell["steps"])
    if predicate == "candidate_raw_profile_equals_componentwise_max_of_assembly_members":
        return all(_candidate_profiles_exact(contract, cell["fixture_key"], result) for cell in all_cells for result in cell["steps"])
    if predicate == "one_binding_candidate_and_adjudication_per_emitted_assembly":
        return all(
            len(result["semantic"]["assemblies"]) == len(result["semantic"]["binding_candidates"]) == len(result["semantic"]["adjudications"]) <= 1
            for cell in all_cells for result in cell["steps"]
        )
    if predicate == "operator_access_log_excludes_evaluator_alias_fixture_key_expected_fields":
        forbidden = set(operands)
        return all(
            not (set(log["inspected_fields"]) | set(log["pass_through_fields"])) & forbidden
            and not set(log["inspected_fields"]) & set(log["pass_through_fields"])
            for cell in all_cells for result in cell["steps"] for log in result["operator_invocations"]
        ) and all(_operator_logs_exact(contract, cell) for cell in all_cells)
    raise ValueError(f"unsupported assertion predicate: {predicate}")


def _assertion_result(assertion: dict[str, Any], group: str, passed: bool) -> dict[str, Any]:
    return {
        "assertion_id": assertion["assertion_id"],
        "predicate_id": assertion["predicate"],
        "assertion_group": group,
        "status": "PASS" if passed else "FAIL",
        "failure_codes": [] if passed else [
            "MIRROR_TRANSFORM_FAILURE" if group == "mirror" else "ASSERTION_FAILURE"
        ],
    }


def _evaluate_assertions(
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells_list: list[dict[str, Any]],
    signature_lookup: dict[tuple[str, str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    cells = _cell_map(cells_list)
    results: list[dict[str, Any]] = []
    for assertion in evaluation_contract["mirror_relations"]:
        try:
            passed = _assert_mirror(assertion, contract, cells)
        except (KeyError, IndexError, StopIteration, TypeError, ValueError):
            passed = False
        results.append(_assertion_result(assertion, "mirror", passed))

    for declaration in evaluation_contract["cell_assertions"]:
        fixture = declaration["fixture_key"]
        passed = all(
            signature_lookup[(fixture, model, step_number)]["status"] == "PASS"
            and signature_lookup[(fixture, model, step_number)]["signature_id"] == signature_id
            for model, signatures in declaration["expected_by_model"].items()
            for step_number, signature_id in enumerate(signatures, start=1)
        )
        results.append(_assertion_result(
            {
                "assertion_id": f"cell-{fixture}",
                "predicate": "step_signature_all_models",
            },
            "cell",
            passed,
        ))

    for source, group in (
        ("pair_assertions", "pair"),
        ("matrix_assertions", "matrix"),
        ("global_invariants", "global"),
    ):
        for assertion in evaluation_contract[source]:
            try:
                passed = _evaluate_declared_predicate(
                    assertion["predicate"],
                    assertion["operands"],
                    contract=contract,
                    cells=cells,
                    signature_lookup=signature_lookup,
                )
            except (KeyError, IndexError, StopIteration, TypeError, ValueError):
                passed = False
            results.append(_assertion_result(assertion, group, passed))
    return results


def _all_model_projection_equal(
    fixtures: list[str], cells: dict[tuple[str, str], dict[str, Any]], left: str, right: str, projection: Callable[[dict[str, Any]], Any]
) -> bool:
    return all(
        len(cells[(fixture, left)]["steps"]) == len(cells[(fixture, right)]["steps"])
        and all(
            digest(projection(a)) == digest(projection(b))
            for a, b in zip(cells[(fixture, left)]["steps"], cells[(fixture, right)]["steps"])
        )
        for fixture in fixtures
    )


def _evaluate_retirement(
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells_list: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    cells = _cell_map(cells_list)
    fixtures = contract["execution_matrix"]["fixture_keys"]
    results: list[dict[str, Any]] = []
    for rule in evaluation_contract["retirement_rules"]:
        predicate = rule["predicate"]
        operands = rule["operands"]
        if predicate == "if_all_results_equal_single_threshold_retire_extra_degrees":
            results.append({
                "assertion_id": rule["assertion_id"],
                "predicate_id": predicate,
                "status": "NOT_EVALUABLE",
                "decision": "RETAIN",
                "targets": operands,
                "reason_code": "MISSING_SINGLE_THRESHOLD_BASELINE",
                "failure_codes": [],
            })
            continue
        if predicate == "if_r1_equals_r0_all_access_predicates_remove_op003":
            condition = _all_model_projection_equal(fixtures, cells, operands[0], operands[1], _access_projection)
            action, targets = "REMOVE_OPERATOR", [operands[2]]
        elif predicate == "if_r2_equals_r0_all_coherence_predicates_remove_op007":
            condition = _all_model_projection_equal(fixtures, cells, operands[0], operands[1], _coherence_projection)
            action, targets = "REMOVE_OPERATOR", [operands[2]]
        elif predicate == "if_r3_factorization_fails_reject_r3":
            access_ok = _all_model_projection_equal(fixtures, cells, operands[0], operands[1], _access_projection)
            coherence_ok = True
            for fixture in fixtures:
                for left_step, right_step in zip(cells[(fixture, operands[0])]["steps"], cells[(fixture, operands[2])]["steps"]):
                    if digest(left_step["semantic"]["assemblies"]) == digest(right_step["semantic"]["assemblies"]) and digest(_coherence_projection(left_step)) != digest(_coherence_projection(right_step)):
                        coherence_ok = False
            condition = not (access_ok and coherence_ok)
            action, targets = "REJECT_MODEL", [operands[0]]
        elif predicate == "if_r3_equals_r1_all_predicates_remove_coherence_contribution":
            condition = _all_model_projection_equal(fixtures, cells, operands[0], operands[1], lambda item: item["semantic"])
            action, targets = "REMOVE_CONTRIBUTION", [f"{operands[0]}:coherence"]
        elif predicate == "if_r3_equals_r2_all_predicates_remove_access_contribution":
            condition = _all_model_projection_equal(fixtures, cells, operands[0], operands[1], lambda item: item["semantic"])
            action, targets = "REMOVE_CONTRIBUTION", [f"{operands[0]}:access"]
        else:
            _fail("UNKNOWN_PREDICATE", f"unsupported retirement predicate: {predicate}")
        results.append({
            "assertion_id": rule["assertion_id"],
            "predicate_id": predicate,
            "status": "TRIGGERED" if condition else "NOT_TRIGGERED",
            "decision": action if condition else "RETAIN",
            "targets": targets,
            "reason_code": "CONDITION_TRUE" if condition else "CONDITION_FALSE",
            "failure_codes": [],
        })
    return results


def _validate_raw_run(
    contract: dict[str, Any], cell_schema: dict[str, Any], run: dict[str, Any]
) -> tuple[list[dict[str, Any]], int]:
    cells = run["run"].get("cells")
    if not isinstance(cells, list):
        _fail("RUN_MATRIX_MISMATCH", "run cells is not an array")
    validated = 0
    for cell in cells:
        try:
            validate_json_schema(cell, cell_schema)
        except ValueError as error:
            _fail("RESULT_SCHEMA_FAILURE", f"raw cell {validated} failed schema: {error}")
        validated += 1

    matrix = contract["execution_matrix"]
    expected = [
        (fixture, model)
        for fixture in matrix["fixture_keys"]
        for model in matrix["model_ids"]
    ]
    actual = [(cell["fixture_key"], cell["model_id"]) for cell in cells]
    if len(actual) != len(set(actual)):
        _fail("DUPLICATE_CELL", "duplicate fixture-model cell")
    if actual != expected:
        missing = set(expected) - set(actual)
        _fail("MISSING_CELL" if missing else "RUN_MATRIX_MISMATCH", "run matrix is not the exact ordered cartesian product")
    expected_steps = {
        fixture["fixture_key"]: [item["step"] for item in fixture["protocol_steps"]]
        for fixture in contract["fixture_declarations"]
    }
    for cell in cells:
        if [item["protocol_step"] for item in cell["steps"]] != expected_steps[cell["fixture_key"]]:
            _fail("RUN_MATRIX_MISMATCH", "cell protocol steps differ from frozen fixture")
        if cell["execution_manifest_sha256"] != EXECUTION_MANIFEST_SHA256 or cell["execution_contract_sha256"] != EXECUTION_CONTRACT_SHA256:
            _fail("ARTIFACT_BINDING_MISMATCH", "cell execution binding mismatch")
    step_count = sum(len(cell["steps"]) for cell in cells)
    if len(cells) != 64 or step_count != 88:
        _fail("RUN_MATRIX_MISMATCH", "frozen matrix must contain 64 cells and 88 steps")
    return cells, validated


def evaluate_m1(
    execution_manifest_bytes: bytes,
    evaluation_manifest_bytes: bytes,
    cell_result_schema_bytes: bytes,
    run_artifact_schema_bytes: bytes,
    run_artifact_bytes: bytes,
    evaluator_policy_bytes: bytes,
    conformance_report_schema_bytes: bytes,
) -> dict[str, Any]:
    """Evaluate one frozen M1 run after schema-validating every raw cell."""
    bound = _bind_inputs(
        execution_manifest_bytes,
        evaluation_manifest_bytes,
        cell_result_schema_bytes,
        run_artifact_schema_bytes,
        run_artifact_bytes,
        evaluator_policy_bytes,
        conformance_report_schema_bytes,
    )
    contract = bound["execution_contract"]
    evaluation_contract = bound["evaluation_contract"]
    cells, validated = _validate_raw_run(contract, bound["cell_schema"], bound["run"])
    signature_results, signature_lookup = _evaluate_signatures(
        contract, evaluation_contract, bound["cell_schema"], cells
    )
    assertion_results = _evaluate_assertions(
        contract, evaluation_contract, cells, signature_lookup
    )
    retirement_results = _evaluate_retirement(contract, evaluation_contract, cells)
    signature_fail = sum(item["status"] == "FAIL" for item in signature_results)
    assertion_fail = sum(item["status"] == "FAIL" for item in assertion_results)
    status = "PASS" if signature_fail == assertion_fail == 0 else "FAIL"
    run_body = bound["run"]["run"]
    policy_body = bound["policy"]["policy"]
    report = {
        "report_id": REPORT_ID,
        "report_version": REPORT_VERSION,
        "policy_id": policy_body["policy_id"],
        "policy_version": policy_body["policy_version"],
        "status": status,
        "artifact_bindings": {
            "execution_manifest_file_sha256": EXECUTION_FILE_SHA256,
            "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
            "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
            "evaluation_manifest_file_sha256": EVALUATION_FILE_SHA256,
            "evaluation_manifest_sha256": EVALUATION_MANIFEST_SHA256,
            "evaluation_contract_sha256": EVALUATION_CONTRACT_SHA256,
            "cell_result_schema_sha256": CELL_SCHEMA_SHA256,
            "run_artifact_schema_sha256": RUN_SCHEMA_SHA256,
            "evaluator_policy_sha256": POLICY_SHA256,
            "report_schema_sha256": REPORT_SCHEMA_SHA256,
            "run_sha256": bound["run"]["integrity"]["run_sha256"],
        },
        "implementation_bindings": {
            "runner": {
                "implementation_id": policy_body["implementation_identities"]["runner"]["implementation_id"],
                "implementation_version": policy_body["implementation_identities"]["runner"]["implementation_version"],
                "module_path": policy_body["implementation_identities"]["runner"]["module_path"],
                "source_sha256": run_body["runner_implementation_sha256"],
                "bundle_sha256": run_body["runner_bundle_sha256"],
            },
            "evaluator": {
                "implementation_id": EVALUATOR_ID,
                "implementation_version": EVALUATOR_VERSION,
                "module_path": "dynamics/labs/interp_m1_evaluator.py",
                "source_sha256": _source_sha256(),
                "bundle_sha256": bound["source_bundles"]["evaluator"],
            },
        },
        "input_summary": {
            "declared_fixture_count": len(contract["execution_matrix"]["fixture_keys"]),
            "declared_model_count": len(contract["execution_matrix"]["model_ids"]),
            "expected_cell_count": 64,
            "reported_cell_count": len(cells),
            "reported_step_count": sum(len(cell["steps"]) for cell in cells),
        },
        "schema_validation": {
            "status": "PASS",
            "validated_cell_count": validated,
            "failure_codes": [],
        },
        "signature_results": signature_results,
        "assertion_results": assertion_results,
        "retirement_results": retirement_results,
        "summary": {
            "signature_pass_count": len(signature_results) - signature_fail,
            "signature_fail_count": signature_fail,
            "assertion_pass_count": len(assertion_results) - assertion_fail,
            "assertion_fail_count": assertion_fail,
            "retirement_triggered_count": sum(item["status"] == "TRIGGERED" for item in retirement_results),
            "retirement_not_triggered_count": sum(item["status"] == "NOT_TRIGGERED" for item in retirement_results),
            "retirement_not_evaluable_count": sum(item["status"] == "NOT_EVALUABLE" for item in retirement_results),
        },
        "failure_codes": ([] if status == "PASS" else sorted({code for item in signature_results + assertion_results for code in item["failure_codes"]})),
        "observability": {
            "evaluation_domain": "detached_synthetic_structural_conformance",
            "prefix_claim_kind": "runner_implementation_bound_attestation_audit",
            "independent_cryptographic_prefix_proof": False,
            "runtime_ledgers_observed": False,
            "human_empirical_evidence": False,
        },
        "disclaimers": policy_body["evaluation_contract"]["report_disclaimers"],
    }
    envelope = {
        "$schema": "./interp-001b-m1-conformance-report.schema.json",
        "report": report,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": "interp-canonical-json-v1",
            "report_sha256": digest(report),
        },
    }
    try:
        validate_json_schema(envelope, bound["report_schema"])
    except ValueError as error:
        _fail("REPORT_SCHEMA_FAILURE", f"generated report failed schema: {error}")
    return envelope


def encode_report(report_envelope: dict[str, Any]) -> bytes:
    return canonical_bytes(report_envelope) + b"\n"
