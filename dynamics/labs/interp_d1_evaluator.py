from __future__ import annotations

from collections import Counter, deque
from copy import deepcopy
import hashlib
from pathlib import Path
import re
from typing import Any, Callable

from dynamics.labs.interp_d1_challengers import (
    D1ChallengerContractError,
    adapt_model_result,
    execute_and_adapt_challenger,
)
from dynamics.labs.interp_d1_common import (
    CANONICALIZATION_ID,
    FrozenD1ExecutionError,
    canonical_bytes,
    digest,
    digest_without_nested_member,
    loads_exact,
    scope_equal,
    validate_json_schema,
)


# Frozen D1 inputs. Policy/report/implementation bindings are intentionally
# refrozen by the publishing step after all assigned source files exist.
EXECUTION_FILE_SHA256 = "fc0717e394f03f4483cd15d46a16f9a0e054298cb4b503301273698fe8433810"
EXECUTION_MANIFEST_SHA256 = "ad627e9b27dbcf517d6dc16736974b8e8f2547ab98cb7a4bea8a4694cbcd1740"
EXECUTION_CONTRACT_SHA256 = "1f49e2c89a79af5d50ff877ef9326191564d768be6af8a1904395929782513c7"
EVALUATION_FILE_SHA256 = "2cc9358de6778bfb3c1104a67d19ea166cb974d6b63cd6c1624e90371b3af15d"
EVALUATION_MANIFEST_SHA256 = "df25f49fb1b2c61ac798cfda7eb47a30c18951bd19860fa7010603004ec8c0aa"
EVALUATION_CONTRACT_SHA256 = "0686be05871faa899fa76134b7d6768894bbc46b8914e1fe8b7de14aaea6aa20"
RESULT_SCHEMA_SHA256 = "be74c90b4fc501793862097cc948c36ceb7ea1969e48a8b69290d73eca8cecb9"
RUN_SCHEMA_SHA256 = "4a993a28db36c052c5d6a81d4de8867a385523fcab972d1699049683130c73ed"
POLICY_FILE_SHA256 = "d260fc23971bafd168b2fb23a3a05e10caa1c46c468a912a9cf931103d53e623"
POLICY_SHA256 = "9364f49518f9ec636fcf0f3a9810a7d60e4968f2c17be599e8da92320474a295"
POLICY_CONTRACT_SHA256 = "24f313e4d3bfe3a9c38f9ad88e4f17491616243557c91e0ef4fcf30caa47c642"
REPORT_SCHEMA_SHA256 = "0e49a4ad5da655541fb84c18d39376bc781002343c31058414580b77701cf312"

REPORT_ID = "INTERP-001D1-V1-CONFORMANCE-REPORT"
REPORT_VERSION = "1.0.0"
EVALUATOR_ID = "INTERP-001D1-V1-CONFORMANCE-EVALUATOR"
EVALUATOR_VERSION = "1.0.0"
RUN_ID = "INTERP-001D1-V1-RUN-001"
BUNDLE_CANONICALIZATION_ID = "interp-d1-source-bundle-v1-policy-bindings-elided"
EVALUATOR_SOURCE_NORMALIZATION_ID = (
    "interp-d1-evaluator-source-v1-policy-bindings-elided"
)
BUNDLE_PATHS = {
    "runner": (
        "dynamics/__init__.py",
        "dynamics/labs/__init__.py",
        "dynamics/labs/interp_d1_common.py",
        "dynamics/labs/interp_d1_operators.py",
        "dynamics/labs/interp_d1_runner.py",
        "dynamics/labs/interp_d1_run_cli.py",
        "dynamics/labs/interp_d1_cli.py",
    ),
    "evaluator": (
        "dynamics/__init__.py",
        "dynamics/labs/__init__.py",
        "dynamics/labs/interp_d1_common.py",
        "dynamics/labs/interp_d1_challengers.py",
        "dynamics/labs/interp_d1_evaluator.py",
        "dynamics/labs/interp_d1_evaluate_cli.py",
        "dynamics/labs/interp_d1_cli.py",
    ),
}
ELIDED_POLICY_BINDINGS = (
    "POLICY_FILE_SHA256",
    "POLICY_SHA256",
    "POLICY_CONTRACT_SHA256",
    "REPORT_SCHEMA_SHA256",
)
EVALUATOR_SOURCE_NORMALIZATION_CONTRACT = {
    "normalization_id": EVALUATOR_SOURCE_NORMALIZATION_ID,
    "source_encoding": "UTF-8",
    "assignment_match_rule": (
        "for_each_elided_assignment_name_require_exactly_one_Python_re.MULTILINE_"
        "match_of_^({NAME}\\s*=\\s*)\"[^\"]+\"$"
    ),
    "replacement_rule": (
        "preserve_the_captured_assignment_prefix_and_replace_the_quoted_value_with_"
        "the_literal_<ELIDED>"
    ),
    "elided_assignment_names": list(ELIDED_POLICY_BINDINGS),
    "digest_rule": "sha256_of_UTF-8_encoded_normalized_source_bytes",
}


class FrozenD1EvaluationInputError(ValueError):
    """Fail closed before report construction for invalid frozen inputs."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _sha(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _fail(code: str, message: str) -> None:
    raise FrozenD1EvaluationInputError(code, message)


def _exact_file(source: bytes, expected: str, label: str) -> dict[str, Any]:
    if _sha(source) != expected:
        _fail("ARTIFACT_BINDING_MISMATCH", f"{label} file hash mismatch")
    try:
        return loads_exact(source)
    except (FrozenD1ExecutionError, UnicodeDecodeError, ValueError) as error:
        _fail("ARTIFACT_BINDING_MISMATCH", f"{label} is not exact JSON: {error}")


def _index(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item[key]
        if value in result:
            _fail("EVALUATION_CONTRACT_ERROR", f"duplicate {key}: {value}")
        result[value] = item
    return result


def _bundle_file_sha256(relative_path: str) -> str:
    path = Path(__file__).resolve().parents[2] / relative_path
    source = path.read_bytes()
    if relative_path != "dynamics/labs/interp_d1_evaluator.py":
        return _sha(source)
    text = source.decode("utf-8")
    for name in ELIDED_POLICY_BINDINGS:
        pattern = rf'(?m)^({name}\s*=\s*)"[^"]+"$'
        text, count = re.subn(pattern, rf'\1"<ELIDED>"', text)
        if count != 1:
            raise ValueError(f"evaluator binding literal is not unique: {name}")
    return _sha(text.encode("utf-8"))


def _source_bundle_sha256(role: str) -> str:
    try:
        paths = BUNDLE_PATHS[role]
    except KeyError as error:
        raise ValueError(f"unknown implementation role: {role}") from error
    return digest(
        [{"path": path, "sha256": _bundle_file_sha256(path)} for path in paths]
    )


def _verify_envelope(
    envelope: dict[str, Any], contract_key: str, manifest_hash: str, contract_hash: str
) -> None:
    try:
        manifest = envelope["manifest"]
        integrity = envelope["integrity"]
    except KeyError as error:
        _fail("ARTIFACT_BINDING_MISMATCH", f"manifest field missing: {error.args[0]}")
    if (
        digest(manifest) != integrity.get("manifest_sha256")
        or integrity.get("manifest_sha256") != manifest_hash
    ):
        _fail("ARTIFACT_BINDING_MISMATCH", "manifest internal digest mismatch")
    if (
        digest(manifest[contract_key]) != integrity.get("contract_sha256")
        or integrity.get("contract_sha256") != contract_hash
    ):
        _fail("ARTIFACT_BINDING_MISMATCH", "contract internal digest mismatch")


def _verify_policy_bindings(
    policy: dict[str, Any], supplied_files: dict[str, bytes]
) -> tuple[dict[str, Any], dict[str, str]]:
    try:
        body = policy["policy"]
        integrity = policy["integrity"]
    except KeyError as error:
        _fail("ARTIFACT_BINDING_MISMATCH", f"policy field missing: {error.args[0]}")
    if digest(body) != POLICY_SHA256 or integrity.get("policy_sha256") != POLICY_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "policy internal digest mismatch")
    if (
        digest(body["evaluation_contract"]) != POLICY_CONTRACT_SHA256
        or integrity.get("contract_sha256") != POLICY_CONTRACT_SHA256
    ):
        _fail("ARTIFACT_BINDING_MISMATCH", "policy contract digest mismatch")
    expected = {
        "execution_manifest": EXECUTION_FILE_SHA256,
        "evaluation_manifest": EVALUATION_FILE_SHA256,
        "cell_result_schema": RESULT_SCHEMA_SHA256,
        "run_artifact_schema": RUN_SCHEMA_SHA256,
        "conformance_report_schema": REPORT_SCHEMA_SHA256,
    }
    bindings = body.get("artifact_bindings", {})
    for name, expected_hash in expected.items():
        binding = bindings.get(name)
        if not isinstance(binding, dict):
            _fail("ARTIFACT_BINDING_MISMATCH", f"policy binding missing: {name}")
        bound_hash = binding.get("file_sha256")
        if bound_hash != expected_hash:
            _fail("ARTIFACT_BINDING_MISMATCH", f"policy binding changed: {name}")
        if name in supplied_files and _sha(supplied_files[name]) != bound_hash:
            _fail("ARTIFACT_BINDING_MISMATCH", f"supplied artifact differs: {name}")
    actual_bundles: dict[str, str] = {}
    identities = body.get("implementation_identities", {})
    for role in ("runner", "evaluator"):
        identity = identities.get(role)
        bundle = identity.get("source_bundle") if isinstance(identity, dict) else None
        if not isinstance(bundle, dict):
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"bundle binding missing: {role}")
        if (
            bundle.get("canonicalization_id") != BUNDLE_CANONICALIZATION_ID
            or bundle.get("paths") != list(BUNDLE_PATHS[role])
        ):
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"bundle definition changed: {role}")
        try:
            actual_bundles[role] = _source_bundle_sha256(role)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"bundle cannot be resolved: {role}: {error}")
        frozen = bundle.get("bundle_sha256")
        if frozen != actual_bundles[role]:
            _fail("IMPLEMENTATION_BINDING_MISMATCH", f"source bundle changed: {role}")
        if role == "runner":
            source_path = identity.get("module_path")
            if source_path != "dynamics/labs/interp_d1_runner.py":
                _fail("IMPLEMENTATION_BINDING_MISMATCH", "runner module path changed")
            try:
                actual_source = _sha(
                    (Path(__file__).resolve().parents[2] / source_path).read_bytes()
                )
            except OSError as error:
                _fail(
                    "IMPLEMENTATION_BINDING_MISMATCH",
                    f"runner source cannot be resolved: {error}",
                )
            frozen_source = identity.get("source_sha256")
            if frozen_source != actual_source:
                _fail("IMPLEMENTATION_BINDING_MISMATCH", "runner source changed")
        else:
            if identity.get("module_path") != "dynamics/labs/interp_d1_evaluator.py":
                _fail("IMPLEMENTATION_BINDING_MISMATCH", "evaluator module path changed")
            if (
                identity.get("source_normalization")
                != EVALUATOR_SOURCE_NORMALIZATION_CONTRACT
            ):
                _fail(
                    "IMPLEMENTATION_BINDING_MISMATCH",
                    "evaluator source normalization contract changed",
                )
            actual_source = _bundle_file_sha256(
                "dynamics/labs/interp_d1_evaluator.py"
            )
            frozen_source = identity.get("normalized_source_sha256")
            if frozen_source != actual_source:
                _fail(
                    "IMPLEMENTATION_BINDING_MISMATCH",
                    "normalized evaluator source changed",
                )
    return body, actual_bundles


def _bind_inputs(
    execution_bytes: bytes,
    evaluation_bytes: bytes,
    result_schema_bytes: bytes,
    run_schema_bytes: bytes,
    run_bytes: bytes,
    policy_bytes: bytes,
    report_schema_bytes: bytes,
) -> dict[str, Any]:
    execution = _exact_file(execution_bytes, EXECUTION_FILE_SHA256, "execution manifest")
    evaluation = _exact_file(evaluation_bytes, EVALUATION_FILE_SHA256, "evaluation manifest")
    result_schema = _exact_file(result_schema_bytes, RESULT_SCHEMA_SHA256, "result schema")
    run_schema = _exact_file(run_schema_bytes, RUN_SCHEMA_SHA256, "run schema")
    policy = _exact_file(policy_bytes, POLICY_FILE_SHA256, "evaluator policy")
    report_schema = _exact_file(report_schema_bytes, REPORT_SCHEMA_SHA256, "report schema")
    try:
        run = loads_exact(run_bytes)
    except (FrozenD1ExecutionError, ValueError) as error:
        _fail("INPUT_INTEGRITY_FAILURE", f"run is not exact JSON: {error}")
    _verify_envelope(
        execution, "execution_contract", EXECUTION_MANIFEST_SHA256, EXECUTION_CONTRACT_SHA256
    )
    _verify_envelope(
        evaluation, "evaluation_contract", EVALUATION_MANIFEST_SHA256, EVALUATION_CONTRACT_SHA256
    )
    policy_body, bundles = _verify_policy_bindings(
        policy,
        {
            "execution_manifest": execution_bytes,
            "evaluation_manifest": evaluation_bytes,
            "cell_result_schema": result_schema_bytes,
            "run_artifact_schema": run_schema_bytes,
            "conformance_report_schema": report_schema_bytes,
        },
    )
    return {
        "execution": execution,
        "evaluation": evaluation,
        "result_schema": result_schema,
        "run_schema": run_schema,
        "run": run,
        "policy": policy,
        "policy_body": policy_body,
        "report_schema": report_schema,
        "bundles": bundles,
    }


def _expected_matrix(contract: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    return [
        (
            matrix["block_id"],
            fixture,
            model,
            matrix["cell_key_template"].format(
                block_id=matrix["block_id"], fixture_key=fixture, model_id=model
            ),
        )
        for matrix in contract["execution_matrices"]
        for fixture in matrix["fixture_keys"]
        for model in matrix["model_ids"]
    ]


def _validate_run(bound: dict[str, Any]) -> list[dict[str, Any]]:
    run = bound["run"]
    try:
        validate_json_schema(
            run,
            bound["run_schema"],
            external_schemas={
                "./interp-001d1-v1-result.schema.json": bound["result_schema"]
            },
        )
    except (FrozenD1ExecutionError, ValueError) as error:
        _fail("INPUT_INTEGRITY_FAILURE", f"run failed closed-world schema: {error}")
    if run["execution_manifest_sha256"] != EXECUTION_MANIFEST_SHA256 or run[
        "execution_contract_sha256"
    ] != EXECUTION_CONTRACT_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "run execution binding mismatch")
    if run["run_id"] != RUN_ID:
        _fail("RUN_MATRIX_MISMATCH", "run id is not the implementation-bound D1 id")
    if run["result_schema_sha256"] != RESULT_SCHEMA_SHA256:
        _fail("ARTIFACT_BINDING_MISMATCH", "run result-schema binding mismatch")
    if run["runner_input_kind"] != "execution_manifest_only" or run[
        "evaluation_manifest_visible"
    ] is not False:
        _fail("RUNNER_BLINDING_FAILURE", "run does not attest execution-only input")
    policy_runner = bound["policy_body"]["implementation_identities"]["runner"]
    module_path = Path(__file__).resolve().parents[2] / policy_runner["module_path"]
    try:
        runner_source_sha = _sha(module_path.read_bytes())
    except OSError as error:
        _fail("IMPLEMENTATION_BINDING_MISMATCH", f"runner source missing: {error}")
    frozen_source = policy_runner.get("source_sha256")
    if runner_source_sha != frozen_source:
        _fail("IMPLEMENTATION_BINDING_MISMATCH", "runner source changed")
    if run["runner_implementation_sha256"] != runner_source_sha:
        _fail("IMPLEMENTATION_BINDING_MISMATCH", "run runner-source binding mismatch")
    if run["runner_bundle_sha256"] != bound["bundles"]["runner"]:
        _fail("IMPLEMENTATION_BINDING_MISMATCH", "run runner-bundle binding mismatch")
    if run["integrity"]["run_sha256"] != digest_without_nested_member(
        run, "integrity", "run_sha256"
    ):
        _fail("INPUT_INTEGRITY_FAILURE", "run envelope integrity mismatch")
    contract = bound["execution"]["manifest"]["execution_contract"]
    expected = _expected_matrix(contract)
    actual = [
        (cell["block_id"], cell["fixture_key"], cell["model_id"], cell["cell_key"])
        for cell in run["cells"]
    ]
    if len({item[3] for item in actual}) != len(actual):
        _fail("DUPLICATE_CELL", "duplicate cell key")
    if actual != expected:
        _fail("RUN_MATRIX_MISMATCH", "run is not the exact ordered frozen matrix")
    for index, cell in enumerate(run["cells"]):
        try:
            validate_json_schema(cell, bound["result_schema"])
        except (FrozenD1ExecutionError, ValueError) as error:
            _fail("RESULT_SCHEMA_FAILURE", f"cell {index} failed schema: {error}")
        if cell["execution_manifest_sha256"] != run["execution_manifest_sha256"] or cell[
            "execution_contract_sha256"
        ] != run["execution_contract_sha256"]:
            _fail("ARTIFACT_BINDING_MISMATCH", f"cell {index} execution binding mismatch")
        if cell["integrity"]["cell_content_sha256"] != digest_without_nested_member(
            cell, "integrity", "cell_content_sha256"
        ):
            _fail("INPUT_INTEGRITY_FAILURE", f"cell {index} integrity mismatch")
    return run["cells"]


def _rank(component: dict[str, Any]) -> int:
    if component.get("status") != "present" or component.get("rank") not in (0, 1, 2):
        raise ValueError("non-present ordinal component")
    return component["rank"]


def _componentwise_max(profiles: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for axis in ("positive_direction_support", "negative_direction_support"):
        values = [
            component["rank"]
            for component in (profile[axis] for profile in profiles)
            if component["status"] == "present"
        ]
        result[axis] = (
            {"status": "present", "rank": max(values)}
            if values
            else {"status": "missing", "reason": "source_unresolved"}
        )
    return result


def _recompute_source(fixture: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    declared_order = [item["source_position"] for item in fixture["source_records"]]
    eligible = [
        item
        for item in fixture["source_records"]
        if scope_equal(item["source_scope"], fixture["scope"])
        and item["effective_from_access_ordinal"] < fixture["access_ordinal_k"]
    ]
    accepted: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    accessibility: dict[str, Any] | None = None
    for item in eligible:
        if item["source_kind"] == "narrative_terrain_fixture":
            accepted.append(item)
        elif (
            item["source_kind"] == "episode_integration_receipt_fixture"
            and "episode_integration_receipt_fixture" in model["allowed_source_kinds"]
            and item["status"] == "adopted_fixture"
        ):
            accepted.append(item)
        elif (
            item["source_kind"] == "contested_binding_receipt_fixture"
            and "contested_binding_receipt_fixture" in model["allowed_source_kinds"]
            and item["status"] == "contested_fixture"
        ):
            diagnostics.append(item)
    if "pre_access_accessibility_snapshot" in model["allowed_source_kinds"]:
        snapshots = [
            item
            for item in eligible
            if item["source_kind"] == "pre_access_accessibility_snapshot"
        ]
        if len(snapshots) != 1:
            raise ValueError("TF2 requires exactly one eligible accessibility snapshot")
        accessibility = snapshots[0]
        implicit = [
            item
            for item in eligible
            if item["source_kind"] == "implicit_plastic_trace_fixture"
        ]
        if accessibility["status"] == "accessible_fixture":
            accepted.extend(implicit)
        elif accessibility["status"] != "withheld_fixture":
            raise ValueError("unknown accessibility status")
    receipts = accepted + diagnostics + ([accessibility] if accessibility else [])
    position_set = {item["source_position"] for item in receipts}
    ordered_positions = [position for position in declared_order if position in position_set]
    support_profiles = [
        item["direction_profile"]
        for item in accepted
        if item["source_kind"] != "contested_binding_receipt_fixture"
    ]
    if accessibility is None:
        accessibility_relation = "not_applicable"
    elif accessibility["status"] == "withheld_fixture":
        accessibility_relation = "all_withheld"
    else:
        accessibility_relation = "all_eligible"
    return {
        "semantic_kind": "source_compiler",
        "scope_lineage": deepcopy(fixture["scope"]),
        "access_ordinal_k": fixture["access_ordinal_k"],
        "source_kinds_used": sorted({item["source_kind"] for item in receipts}),
        "target_form_readout_profile": _componentwise_max(support_profiles),
        "contested_present": bool(diagnostics),
        "accessibility_relation": accessibility_relation,
        "effective_before_access_ordinal": fixture["access_ordinal_k"],
        "eligible_source_position_count": len(ordered_positions),
        "eligible_source_positions_ordered": ordered_positions,
    }


def _profile_min_reception(
    profile: dict[str, Any], reception: dict[str, Any]
) -> dict[str, Any]:
    return {
        "positive_direction_fit": {"status": "present", "rank": min(_rank(profile["positive_direction_fit"]), _rank(reception["positive_direction_receptivity"]))},
        "negative_direction_fit": {"status": "present", "rank": min(_rank(profile["negative_direction_fit"]), _rank(reception["negative_direction_receptivity"]))},
        "ambiguity": {"status": "present", "rank": min(_rank(profile["ambiguity"]), _rank(reception["ambiguity_tolerance"]))},
        "activation": deepcopy(profile["activation"]),
    }


def _profile_min_target(
    profile: dict[str, Any], target: dict[str, Any]
) -> dict[str, Any]:
    return {
        "positive_direction_fit": {"status": "present", "rank": min(_rank(profile["positive_direction_fit"]), _rank(target["positive_direction_support"]))},
        "negative_direction_fit": {"status": "present", "rank": min(_rank(profile["negative_direction_fit"]), _rank(target["negative_direction_support"]))},
        "ambiguity": deepcopy(profile["ambiguity"]),
        "activation": deepcopy(profile["activation"]),
    }


def _recompute_formation(fixture: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    present = fixture["current_access_present"] and fixture["source_materials_present"]
    if present:
        profile: dict[str, Any] = deepcopy(fixture["base_encounter_profile"])
    else:
        profile = {
            "status": "missing",
            "reason": "no_current_access" if not fixture["current_access_present"] else "no_source_material",
        }
    order = ["base_profile"]
    target_used = False
    reception_used = False
    if model["uses_target_form_intervention"]:
        order.append("apply_target_directional_compatibility")
        if present and scope_equal(fixture["declared_target_form_intervention_scope"], fixture["scope"]):
            profile = _profile_min_target(profile, fixture["declared_target_form_intervention"])
            target_used = True
    if model["uses_reception_intervention"]:
        order.append("apply_reception_eligibility")
        if present and scope_equal(fixture["declared_reception_intervention_scope"], fixture["scope"]):
            profile = _profile_min_reception(profile, fixture["declared_reception_intervention"])
            reception_used = True
    order.append("emit_proxy")
    return {
        "semantic_kind": "encounter_formation",
        "scope_lineage": deepcopy(fixture["scope"]),
        "current_access_present": fixture["current_access_present"],
        "source_materials_present": fixture["source_materials_present"],
        "encounter_emitted": present,
        "base_encounter_profile": deepcopy(fixture["base_encounter_profile"]),
        "formed_encounter_profile": profile,
        "reception_intervention_used": reception_used,
        "target_form_intervention_used": target_used,
        "formation_operator_order": order,
    }


def _ghost_visit(fixture: dict[str, Any]) -> list[int]:
    positions = [item["position"] for item in fixture["accessible_materials_ordered"]]
    if not (
        fixture["current_access_present"]
        and fixture["source_materials_present"]
        and positions
    ):
        return []
    adjacency = {position: [] for position in positions}
    for edge in fixture["topology_edges"]:
        left, right = edge["left_position"], edge["right_position"]
        if left in adjacency and right in adjacency:
            adjacency[left].append(right)
            adjacency[right].append(left)
    queue: deque[int] = deque([positions[0]])
    seen = {positions[0]}
    visited: list[int] = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        for neighbour in adjacency[current]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    visited.extend(position for position in positions if position not in seen)
    return visited


def _ghost_truth(directions: list[str]) -> tuple[str, str]:
    return {
        (): ("none", "deferred"),
        ("negative",): ("single_direction", "adopted_negative"),
        ("positive",): ("single_direction", "adopted_positive"),
        ("negative", "positive"): ("contested", "contested"),
    }[tuple(directions)]


def _recompute_ghost(fixture: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    accessed = [item["position"] for item in fixture["accessible_materials_ordered"]]
    active = bool(
        fixture["current_access_present"]
        and fixture["source_materials_present"]
        and accessed
    )
    visited = _ghost_visit(fixture)
    materials = {item["position"]: item for item in fixture["accessible_materials_ordered"]}
    directions = [
        direction
        for direction in ("negative", "positive")
        if active
        and any(
            materials[position]["direction_profile"][f"{direction}_direction_support"]["status"] == "present"
            and materials[position]["direction_profile"][f"{direction}_direction_support"]["rank"] >= 1
            for position in visited
        )
    ]
    registered: list[str] = []
    if active and model["uses_declared_ghost_program"]:
        for operation in fixture["declared_ghost_program"]["operations_ordered"]:
            if operation == "confirmation_only" and visited:
                first = materials[visited[0]]["direction_profile"]
                directions = [
                    direction
                    for direction in directions
                    if first[f"{direction}_direction_support"]["status"] == "present"
                    and first[f"{direction}_direction_support"]["rank"] >= 1
                ]
            elif operation not in {
                "broaden", "contrast", "counterfactual", "rehearsal"
            }:
                raise ValueError(f"unknown Ghost program operation: {operation}")
            registered.append(operation)
    target_used = bool(
        active
        and model["uses_target_guidance"]
        and scope_equal(fixture["target_guidance_scope"], fixture["scope"])
    )
    if target_used:
        directions = [
            direction
            for direction in directions
            if fixture["target_guidance_profile"][f"{direction}_direction_support"]["status"] == "present"
            and fixture["target_guidance_profile"][f"{direction}_direction_support"]["rank"] >= 1
        ]
    directions = [direction for direction in ("negative", "positive") if direction in directions]
    relation, outcome = _ghost_truth(directions)
    return {
        "semantic_kind": "ghost_path",
        "scope_lineage": deepcopy(fixture["scope"]),
        "current_access_present": fixture["current_access_present"],
        "source_materials_present": fixture["source_materials_present"],
        "accessed_material_positions_ordered": accessed,
        "visited_material_positions_ordered": visited,
        "operation_phase_order": ["seed", "traverse", "bind"],
        "target_guidance_used": target_used,
        "ghost_program_used": bool(active and model["uses_declared_ghost_program"] and registered),
        "candidate_projection": {
            "writer_authority": "ghost_candidate_only",
            "binding_candidate_directions": directions,
            "binding_relation": relation,
            "registered_operation_relations": registered,
        },
        "adjudication_projection": {
            "writer_authority": "scoped_adjudicator_only",
            "adjudication_outcome": outcome,
        },
    }


def _catalogs(contract: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], ...]:
    return (
        _index(contract["source_fixtures"], "fixture_key"),
        _index(contract["formation_fixtures"], "fixture_key"),
        _index(contract["ghost_fixtures"], "fixture_key"),
        _index(contract["source_compilers"], "model_id"),
        _index(contract["formation_models"], "model_id"),
        _index(contract["ghost_models"], "model_id"),
    )


def _recompute_semantic(contract: dict[str, Any], cell: dict[str, Any]) -> dict[str, Any]:
    sf, ff, gf, sm, fm, gm = _catalogs(contract)
    if cell["block_id"] == "SOURCE_COMPILER":
        return _recompute_source(sf[cell["fixture_key"]], sm[cell["model_id"]])
    if cell["block_id"] == "ENCOUNTER_FORMATION":
        return _recompute_formation(ff[cell["fixture_key"]], fm[cell["model_id"]])
    return _recompute_ghost(gf[cell["fixture_key"]], gm[cell["model_id"]])


def _expected_trace_ids(
    contract: dict[str, Any], cell: dict[str, Any]
) -> list[str]:
    sf, ff, gf, sm, fm, gm = _catalogs(contract)
    if cell["block_id"] == "SOURCE_COMPILER":
        return list(sm[cell["model_id"]]["operator_sequence"])
    if cell["block_id"] == "ENCOUNTER_FORMATION":
        return list(fm[cell["model_id"]]["operator_sequence"])
    fixture = gf[cell["fixture_key"]]
    sequence: list[str] = []
    for operator_id in gm[cell["model_id"]]["operator_sequence"]:
        if operator_id == contract["operator_typed_dataflow_contract"][
            "ghost_sequence_expansion_token"
        ]:
            sequence.extend(fixture["declared_ghost_program"]["operations_ordered"])
        else:
            sequence.append(operator_id)
    sequence.extend(contract["adjudicator_contract"]["post_candidate_tail_sequence"])
    return sequence


def _operator_declaration(
    contract: dict[str, Any], operator_id: str
) -> dict[str, Any]:
    if operator_id == contract["adjudicator_contract"]["policy_id"]:
        adjudicator = contract["adjudicator_contract"]
        return {
            "operator_id": adjudicator["policy_id"],
            "operator_version": adjudicator["policy_version"],
            "input_view_id": adjudicator["input_view_id"],
            "exact_inspected_field_ids": adjudicator["exact_inspected_field_ids"],
            "exact_opaque_pass_through_field_ids": adjudicator[
                "exact_opaque_pass_through_field_ids"
            ],
            "output_kind": adjudicator["output_kind"],
            "authority": adjudicator["writer_authority"],
        }
    return _index(contract["operator_declarations"], "operator_id")[operator_id]


def _trace_exact(contract: dict[str, Any], cell: dict[str, Any]) -> bool:
    expected_ids = _expected_trace_ids(contract, cell)
    trace = cell["operator_trace"]
    if [item["operator_id"] for item in trace] != expected_ids:
        return False
    for item in trace:
        declaration = _operator_declaration(contract, item["operator_id"])
        expected = {
            "operator_id": declaration["operator_id"],
            "operator_version": declaration["operator_version"],
            "phase": contract["operator_trace_phase_map"][item["operator_id"]],
            "input_view_id": declaration["input_view_id"],
            "inspected_field_ids": declaration["exact_inspected_field_ids"],
            "opaque_pass_through_field_ids": declaration[
                "exact_opaque_pass_through_field_ids"
            ],
            "output_kind": declaration["output_kind"],
            "authority": declaration["authority"],
        }
        if item != expected:
            return False
    return True


_IDENTITY_CONSUMER_KINDS = {
    "scope_matched_source_positions": "integer_list",
    "effective_eligible_source_positions": "integer_list",
    "declared_target_form_readout_profile": "direction_profile",
    "formation_transition_state": "formation_transition_state",
    "ghost_seed_positions": "integer_list",
    "visited_positions_ordered": "integer_list",
    "candidate_relation_state": "candidate_relation_state",
    "interpretive_binding_candidate_projection": (
        "interpretive_binding_candidate_projection"
    ),
    "detached_adjudication_projection": "detached_adjudication_projection",
}


def _edge_transfer_value_kind_exact(edge: dict[str, Any]) -> bool:
    """Check the frozen transfer algebra, including list-valued receipt edges."""
    producer_kinds = edge["producer_output_kinds"]
    transfer = edge["transfer_policy"]
    selection = edge["selection_policy"]
    consumer_field = edge["consumer_input_field_id"]
    consumer_kind = edge["consumer_value_kind"]
    if transfer == "collect_receipts":
        return (
            len(producer_kinds) == 1
            and selection
            in {
                "all_prior_matching_zero_or_more",
                "all_prior_matching_one_or_more",
            }
            and consumer_kind == f"{producer_kinds[0]}_list"
        )
    if transfer == "identity":
        if selection != "nearest_prior_one":
            return False
        if set(producer_kinds) == {
            "source_semantic_without_lineage",
            "formation_semantic_without_lineage",
            "ghost_semantic_without_lineage",
        }:
            return consumer_kind == "closed_semantic_value"
        return (
            len(producer_kinds) == 1
            and _IDENTITY_CONSUMER_KINDS.get(producer_kinds[0]) == consumer_kind
        )
    if transfer == "extract_accessible_positions":
        return (
            producer_kinds == ["accessibility_projection"]
            and selection == "nearest_prior_one"
            and consumer_kind == "integer_list"
        )
    if transfer == "extract_direction_profiles":
        return (
            producer_kinds == ["source_profile_projection"]
            and selection == "all_prior_matching_zero_or_more"
            and consumer_kind == "direction_profile_list"
        )
    if transfer == "extract_candidate_fields":
        expected = {
            "candidate_direction_set": "direction_set",
            "binding_relation": "token",
        }
        return (
            producer_kinds == ["interpretive_binding_candidate_projection"]
            and selection == "nearest_prior_one"
            and expected.get(consumer_field) == consumer_kind
        )
    return False


def _typed_dataflow_static_exact(
    contract: dict[str, Any], cell: dict[str, Any]
) -> bool:
    """Validate frozen wiring; intermediate runtime values are not serialized."""
    if not _trace_exact(contract, cell):
        return False
    typed = contract["operator_typed_dataflow_contract"]
    trace = cell["operator_trace"]
    positions = {item["operator_id"]: index for index, item in enumerate(trace)}
    raw = {
        (item["operator_id"], field)
        for item in typed["raw_input_bindings"]
        for field in item["field_ids"]
    }
    preprocessed = {
        (item["operator_id"], item["field_id"])
        for item in typed["deterministic_preprocessor_bindings"]
    }
    opaque = {
        (item["operator_id"], item["field_id"])
        for item in typed["raw_opaque_pass_through_bindings"]
    }
    edges = typed["edges"]
    if len({edge["edge_id"] for edge in edges}) != len(edges):
        return False
    for edge in edges:
        if not _edge_transfer_value_kind_exact(edge):
            return False
        try:
            consumer = _operator_declaration(contract, edge["consumer_operator_id"])
            producer_kinds = {
                _operator_declaration(contract, producer)["output_kind"]
                for producer in edge["producer_operator_ids"]
            }
        except KeyError:
            return False
        if edge["consumer_input_field_id"] not in consumer["exact_inspected_field_ids"]:
            return False
        if producer_kinds != set(edge["producer_output_kinds"]):
            return False
    for invocation in trace:
        operator_id = invocation["operator_id"]
        for field in invocation["inspected_field_ids"]:
            suppliers = int((operator_id, field) in raw) + int(
                (operator_id, field) in preprocessed
            )
            for edge in edges:
                if (
                    edge["consumer_operator_id"] == operator_id
                    and edge["consumer_input_field_id"] == field
                ):
                    prior = [
                        producer
                        for producer in edge["producer_operator_ids"]
                        if producer in positions and positions[producer] < positions[operator_id]
                    ]
                    if prior or edge["selection_policy"].endswith("zero_or_more"):
                        suppliers += 1
                        for producer in prior:
                            declaration = _operator_declaration(contract, producer)
                            if declaration["output_kind"] not in edge[
                                "producer_output_kinds"
                            ]:
                                return False
            if suppliers != 1:
                return False
        for field in invocation["opaque_pass_through_field_ids"]:
            if (operator_id, field) not in opaque:
                return False
    if typed["hidden_intermediate_state"] != "forbidden":
        return False
    if typed["final_result_semantic_producer"] != "bind_opaque_sources":
        return False
    return True


def _path(root: dict[str, Any], pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise ValueError("result path is not absolute")
    value: Any = root
    for raw in pointer[1:].split("/"):
        segment = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or segment not in value:
            raise KeyError(pointer)
        value = value[segment]
    return value


def _relation_passes(relation: dict[str, Any], cell: dict[str, Any]) -> bool:
    actual = _path(cell, relation["path"])
    expected = relation["value"]
    predicate = relation["predicate"]
    if predicate == "eq":
        return canonical_bytes(actual) == canonical_bytes(expected)
    if predicate == "ordered_eq":
        return isinstance(actual, list) and canonical_bytes(actual) == canonical_bytes(expected)
    if predicate == "set_eq":
        if not isinstance(actual, list) or not isinstance(expected, list):
            return False
        if len({canonical_bytes(item) for item in actual}) != len(actual):
            return False
        if len({canonical_bytes(item) for item in expected}) != len(expected):
            return False
        return sorted(map(canonical_bytes, actual)) == sorted(map(canonical_bytes, expected))
    raise ValueError(f"unsupported signature predicate: {predicate}")


def _cell_map(cells: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(cell["fixture_key"], cell["model_id"]): cell for cell in cells}


def _projection_catalog(evaluation_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(evaluation_contract["substantive_comparison_projections"], "projection_id")


def _project(
    evaluation_contract: dict[str, Any], cell: dict[str, Any], projection_id: str
) -> dict[str, Any]:
    declaration = _projection_catalog(evaluation_contract)[projection_id]
    if declaration["block_id"] != cell["block_id"]:
        raise ValueError("projection crosses blocks")
    return {
        pointer: deepcopy(_path(cell, pointer))
        for pointer in declaration["included_result_paths"]
    }


def _fixture_catalog(contract: dict[str, Any], block_id: str) -> dict[str, dict[str, Any]]:
    source = {
        "SOURCE_COMPILER": "source_fixtures",
        "ENCOUNTER_FORMATION": "formation_fixtures",
        "GHOST_PATH": "ghost_fixtures",
    }[block_id]
    return _index(contract[source], "fixture_key")


def _model_catalog(contract: dict[str, Any], block_id: str) -> dict[str, dict[str, Any]]:
    source = {
        "SOURCE_COMPILER": "source_compilers",
        "ENCOUNTER_FORMATION": "formation_models",
        "GHOST_PATH": "ghost_models",
    }[block_id]
    return _index(contract[source], "model_id")


def _target_catalog(evaluation_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(evaluation_contract["common_comparison_targets"], "comparison_target_id")


def _challenger_catalog(evaluation_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(evaluation_contract["challenger_declarations"], "challenger_id")


def _validate_target_shape(target: dict[str, Any], value: dict[str, Any]) -> None:
    expected = [item["field_id"] for item in target["fields"]]
    if list(value) != expected and set(value) != set(expected):
        raise D1ChallengerContractError("adapted target field set mismatch")
    for field in target["fields"]:
        item = value[field["field_id"]]
        kind = field["value_kind"]
        if kind == "boolean" and not isinstance(item, bool):
            raise D1ChallengerContractError("adapted boolean type mismatch")
        if kind == "direction_set" and (
            not isinstance(item, list)
            or item != [direction for direction in ("negative", "positive") if direction in item]
            or len(item) != len(set(item))
        ):
            raise D1ChallengerContractError("adapted direction set mismatch")
        if kind == "direction_profile" and (
            not isinstance(item, dict)
            or set(item) != {"positive_direction_support", "negative_direction_support"}
        ):
            raise D1ChallengerContractError("adapted direction profile mismatch")
        if kind == "binding_relation" and item not in {"none", "single_direction", "contested"}:
            raise D1ChallengerContractError("adapted relation mismatch")
        if kind == "adjudication_outcome" and item not in {
            "deferred", "adopted_negative", "adopted_positive", "contested"
        }:
            raise D1ChallengerContractError("adapted adjudication mismatch")


def _challenger_target(
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    challenger_id: str,
    fixture_key: str,
) -> dict[str, Any]:
    challenger = _challenger_catalog(evaluation_contract)[challenger_id]
    fixture = _fixture_catalog(contract, challenger["block_id"])[fixture_key]
    value = execute_and_adapt_challenger(challenger, fixture)
    target = _target_catalog(evaluation_contract)[challenger["comparison_target_id"]]
    _validate_target_shape(target, value)
    return value


def _model_target(
    evaluation_contract: dict[str, Any],
    cells: dict[tuple[str, str], dict[str, Any]],
    fixture_key: str,
    model_id: str,
    target_id: str,
) -> dict[str, Any]:
    target = _target_catalog(evaluation_contract)[target_id]
    cell = cells[(fixture_key, model_id)]
    if cell["block_id"] != target["block_id"]:
        raise D1ChallengerContractError("model target crosses blocks")
    value = adapt_model_result(target, cell)
    _validate_target_shape(target, value)
    return value


SUPPORTED_PREDICATES = {
    "eq",
    "set_eq",
    "ordered_eq",
    "models_differ_on_fixture",
    "models_equal_on_fixture",
    "source_order_mirror_equal",
    "source_future_prefix_equal",
    "formation_factor_switch_differs",
    "ghost_same_visit_substantive_differs",
    "formation_no_access_emits_none",
    "formation_no_source_emits_none",
    "ghost_no_access_emits_none",
    "ghost_no_source_emits_none",
    "guard_ledgers_unchanged_all_cells",
    "cell_integrity_exact_all_cells",
    "cell_execution_binding_exact_all_cells",
    "operator_trace_exact_all_cells",
    "operator_typed_dataflow_exact_all_cells",
    "run_matrix_complete_exact",
    "run_carrier_execution_binding_exact",
    "run_carrier_runner_blinding_exact",
    "run_carrier_integrity_exact",
    "scope_lineage_exact_all_cells",
    "runner_evaluation_access_absent",
    "adapter_shape_closed",
    "challenger_algebraic_alias_equal_all_fixtures_target",
    "challenger_differs_on_fixture_target",
    "challenger_equivalent_all_fixtures_target",
    "source_factor_absent_all_fixtures",
    "factor_switch_absent_all_fixtures",
    "ghost_difference_explained_by_access_all_fixtures",
    "source_contested_excluded_all_cells",
    "source_tagged_missing_preserved",
}


def _block_fixtures(contract: dict[str, Any], block_id: str) -> list[str]:
    matrix = next(
        item for item in contract["execution_matrices"] if item["block_id"] == block_id
    )
    return matrix["fixture_keys"]


def _block_cells(cells: list[dict[str, Any]], block_id: str) -> list[dict[str, Any]]:
    return [cell for cell in cells if cell["block_id"] == block_id]


def _canonical_equal(left: Any, right: Any) -> bool:
    return canonical_bytes(left) == canonical_bytes(right)


def _source_record_role(record: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    scope = record["source_scope"]
    target_resolution_equal = _canonical_equal(
        scope["target_resolution"], fixture["scope"]["target_resolution"]
    )
    return {
        "source_position": record["source_position"],
        "source_kind": record["source_kind"],
        "effective_from_access_ordinal": record["effective_from_access_ordinal"],
        "direction_profile": record["direction_profile"],
        "status": record["status"],
        "scope_match_dimensions": [
            scope["actor_alias"] == fixture["scope"]["actor_alias"],
            scope["interpreted_target_scope_alias"]
            == fixture["scope"]["interpreted_target_scope_alias"],
            scope["relation_scope_alias"] == fixture["scope"]["relation_scope_alias"],
            scope["context_scope_alias"] == fixture["scope"]["context_scope_alias"],
            target_resolution_equal,
        ],
    }


def _source_order_mirror_declared(
    left: dict[str, Any], right: dict[str, Any]
) -> bool:
    if left["access_ordinal_k"] != right["access_ordinal_k"]:
        return False
    left_roles = [_source_record_role(item, left) for item in left["source_records"]]
    right_roles = [_source_record_role(item, right) for item in right["source_records"]]
    return left_roles == list(reversed(right_roles))


def _source_future_prefix_declared(
    prefix: dict[str, Any], extended: dict[str, Any]
) -> bool:
    if prefix["access_ordinal_k"] != extended["access_ordinal_k"]:
        return False
    def normalized(record: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
        value = _source_record_role(record, fixture)
        return value
    prefix_rows = [normalized(item, prefix) for item in prefix["source_records"]]
    extended_pre = [
        normalized(item, extended)
        for item in extended["source_records"]
        if item["effective_from_access_ordinal"] < extended["access_ordinal_k"]
    ]
    extended_post = [
        item
        for item in extended["source_records"]
        if item["effective_from_access_ordinal"] >= extended["access_ordinal_k"]
    ]
    return prefix_rows == extended_pre and len(extended_post) == 1


def _predicate(
    predicate_id: str,
    operands: list[Any],
    *,
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells_list: list[dict[str, Any]],
    bound: dict[str, Any],
) -> bool:
    cells = _cell_map(cells_list)
    if predicate_id in {"models_differ_on_fixture", "models_equal_on_fixture"}:
        fixture, left, right, projection = operands
        equal = _canonical_equal(
            _project(evaluation_contract, cells[(fixture, left)], projection),
            _project(evaluation_contract, cells[(fixture, right)], projection),
        )
        return not equal if predicate_id == "models_differ_on_fixture" else equal
    if predicate_id in {"source_order_mirror_equal", "source_future_prefix_equal"}:
        left_fixture, right_fixture, model, projection = operands
        fixtures = _fixture_catalog(contract, "SOURCE_COMPILER")
        declared = (
            _source_order_mirror_declared(fixtures[left_fixture], fixtures[right_fixture])
            if predicate_id == "source_order_mirror_equal"
            else _source_future_prefix_declared(fixtures[left_fixture], fixtures[right_fixture])
        )
        return declared and _canonical_equal(
            _project(evaluation_contract, cells[(left_fixture, model)], projection),
            _project(evaluation_contract, cells[(right_fixture, model)], projection),
        )
    if predicate_id == "formation_factor_switch_differs":
        fixture, left, right, projection, factor = operands
        models = _model_catalog(contract, "ENCOUNTER_FORMATION")
        factor_field = {
            "reception": "uses_reception_intervention",
            "target_form": "uses_target_form_intervention",
        }[factor]
        other_field = (
            "uses_target_form_intervention"
            if factor_field == "uses_reception_intervention"
            else "uses_reception_intervention"
        )
        if (
            models[left][factor_field] == models[right][factor_field]
            or models[left][other_field] != models[right][other_field]
        ):
            raise ValueError("formation factor switch is not adjacent")
        return not _canonical_equal(
            _project(evaluation_contract, cells[(fixture, left)], projection),
            _project(evaluation_contract, cells[(fixture, right)], projection),
        )
    if predicate_id == "ghost_same_visit_substantive_differs":
        fixture, left, right = operands
        left_cell, right_cell = cells[(fixture, left)], cells[(fixture, right)]
        access_equal = _canonical_equal(
            _project(evaluation_contract, left_cell, "GHOST_ACCESS"),
            _project(evaluation_contract, right_cell, "GHOST_ACCESS"),
        )
        substantive_equal = _canonical_equal(
            _project(evaluation_contract, left_cell, "GHOST_SUBSTANTIVE"),
            _project(evaluation_contract, right_cell, "GHOST_SUBSTANTIVE"),
        )
        return access_equal and not substantive_equal
    if predicate_id in {"formation_no_access_emits_none", "formation_no_source_emits_none"}:
        fixture = operands[0]
        reason = (
            "no_current_access"
            if predicate_id == "formation_no_access_emits_none"
            else "no_source_material"
        )
        return all(
            cell["semantic"]["encounter_emitted"] is False
            and cell["semantic"]["formed_encounter_profile"]
            == {"status": "missing", "reason": reason}
            and cell["semantic"]["reception_intervention_used"] is False
            and cell["semantic"]["target_form_intervention_used"] is False
            for (fixture_key, _), cell in cells.items()
            if fixture_key == fixture
        )
    if predicate_id in {"ghost_no_access_emits_none", "ghost_no_source_emits_none"}:
        fixture = operands[0]
        return all(
            cell["semantic"]["accessed_material_positions_ordered"] == []
            and cell["semantic"]["visited_material_positions_ordered"] == []
            and cell["semantic"]["target_guidance_used"] is False
            and cell["semantic"]["ghost_program_used"] is False
            and cell["semantic"]["candidate_projection"]["binding_candidate_directions"] == []
            and cell["semantic"]["candidate_projection"]["binding_relation"] == "none"
            and cell["semantic"]["candidate_projection"]["registered_operation_relations"] == []
            and cell["semantic"]["adjudication_projection"]["adjudication_outcome"] == "deferred"
            for (fixture_key, _), cell in cells.items()
            if fixture_key == fixture
        )
    if predicate_id == "guard_ledgers_unchanged_all_cells":
        block = operands[0]
        expected = set(contract["output_guard_contract"]["guard_ledger_names"])
        return all(
            set(cell["guard_ledgers"]) == expected
            and all(
                ledger["before_sha256"] == ledger["after_sha256"]
                for ledger in cell["guard_ledgers"].values()
            )
            for cell in _block_cells(cells_list, block)
        )
    if predicate_id == "cell_integrity_exact_all_cells":
        return all(
            cell["integrity"]["cell_content_sha256"]
            == digest_without_nested_member(cell, "integrity", "cell_content_sha256")
            for cell in _block_cells(cells_list, operands[0])
        )
    if predicate_id == "cell_execution_binding_exact_all_cells":
        return all(
            cell["execution_manifest_sha256"] == EXECUTION_MANIFEST_SHA256
            and cell["execution_contract_sha256"] == EXECUTION_CONTRACT_SHA256
            for cell in _block_cells(cells_list, operands[0])
        )
    if predicate_id == "operator_trace_exact_all_cells":
        return all(
            _trace_exact(contract, cell)
            for cell in _block_cells(cells_list, operands[0])
        )
    if predicate_id == "operator_typed_dataflow_exact_all_cells":
        return all(
            _typed_dataflow_static_exact(contract, cell)
            and _canonical_equal(cell["semantic"], _recompute_semantic(contract, cell))
            for cell in _block_cells(cells_list, operands[0])
        )
    if predicate_id == "run_matrix_complete_exact":
        return len(cells_list) == operands[0] == len(_expected_matrix(contract))
    if predicate_id == "run_carrier_execution_binding_exact":
        run = bound["run"]
        return (
            len(run["cells"]) == operands[0]
            and run["execution_manifest_sha256"] == EXECUTION_MANIFEST_SHA256
            and run["execution_contract_sha256"] == EXECUTION_CONTRACT_SHA256
            and run["result_schema_sha256"] == RESULT_SCHEMA_SHA256
        )
    if predicate_id == "run_carrier_runner_blinding_exact":
        run = bound["run"]
        return (
            run["runner_input_kind"] == "execution_manifest_only"
            and run["evaluation_manifest_visible"] is operands[0]
        )
    if predicate_id == "run_carrier_integrity_exact":
        return (
            bound["run"]["integrity"]["canonicalization_id"] == operands[0]
            and bound["run"]["integrity"]["run_sha256"]
            == digest_without_nested_member(bound["run"], "integrity", "run_sha256")
        )
    if predicate_id == "scope_lineage_exact_all_cells":
        block = operands[0]
        fixtures = _fixture_catalog(contract, block)
        return all(
            _canonical_equal(cell["semantic"]["scope_lineage"], fixtures[cell["fixture_key"]]["scope"])
            for cell in _block_cells(cells_list, block)
        )
    if predicate_id == "runner_evaluation_access_absent":
        runner = contract["runner_contract"]
        return (
            runner["runner_visibility"] == operands[0]
            and runner["evaluation_manifest_access"] == "forbidden"
        )
    if predicate_id == "adapter_shape_closed":
        target_id = operands[0]
        target = _target_catalog(evaluation_contract)[target_id]
        for cell in _block_cells(cells_list, target["block_id"]):
            _validate_target_shape(target, adapt_model_result(target, cell))
        for challenger in evaluation_contract["challenger_declarations"]:
            if challenger["comparison_target_id"] == target_id:
                for fixture in _block_fixtures(contract, target["block_id"]):
                    _challenger_target(contract, evaluation_contract, challenger["challenger_id"], fixture)
        return True
    if predicate_id == "challenger_algebraic_alias_equal_all_fixtures_target":
        left, right, target_id = operands
        block = _target_catalog(evaluation_contract)[target_id]["block_id"]
        return all(
            _canonical_equal(
                _challenger_target(contract, evaluation_contract, left, fixture),
                _challenger_target(contract, evaluation_contract, right, fixture),
            )
            for fixture in _block_fixtures(contract, block)
        )
    if predicate_id == "challenger_differs_on_fixture_target":
        fixture, model, challenger, target_id = operands
        return not _canonical_equal(
            _model_target(evaluation_contract, cells, fixture, model, target_id),
            _challenger_target(contract, evaluation_contract, challenger, fixture),
        )
    if predicate_id == "challenger_equivalent_all_fixtures_target":
        block, model, challenger, target_id = operands
        return all(
            _canonical_equal(
                _model_target(evaluation_contract, cells, fixture, model, target_id),
                _challenger_target(contract, evaluation_contract, challenger, fixture),
            )
            for fixture in _block_fixtures(contract, block)
        )
    if predicate_id == "source_factor_absent_all_fixtures":
        _factor, left, right, projection = operands
        return all(
            _canonical_equal(
                _project(evaluation_contract, cells[(fixture, left)], projection),
                _project(evaluation_contract, cells[(fixture, right)], projection),
            )
            for fixture in _block_fixtures(contract, "SOURCE_COMPILER")
        )
    if predicate_id == "factor_switch_absent_all_fixtures":
        block, _factor, model00, model10, model01, model11, projection = operands
        return all(
            _canonical_equal(
                _project(evaluation_contract, cells[(fixture, model00)], projection),
                _project(evaluation_contract, cells[(fixture, model10)], projection),
            )
            and _canonical_equal(
                _project(evaluation_contract, cells[(fixture, model01)], projection),
                _project(evaluation_contract, cells[(fixture, model11)], projection),
            )
            for fixture in _block_fixtures(contract, block)
        )
    if predicate_id == "ghost_difference_explained_by_access_all_fixtures":
        left, right, access_projection, substantive_projection = operands
        witness = False
        for fixture in _block_fixtures(contract, "GHOST_PATH"):
            substantive_differs = not _canonical_equal(
                _project(evaluation_contract, cells[(fixture, left)], substantive_projection),
                _project(evaluation_contract, cells[(fixture, right)], substantive_projection),
            )
            access_differs = not _canonical_equal(
                _project(evaluation_contract, cells[(fixture, left)], access_projection),
                _project(evaluation_contract, cells[(fixture, right)], access_projection),
            )
            witness |= substantive_differs
            if substantive_differs and not access_differs:
                return False
        return witness
    if predicate_id == "source_contested_excluded_all_cells":
        return all(
            _canonical_equal(cell["semantic"], _recompute_semantic(contract, cell))
            for cell in _block_cells(cells_list, operands[0])
        )
    if predicate_id == "source_tagged_missing_preserved":
        fixture, model = operands
        actual = cells[(fixture, model)]["semantic"]["target_form_readout_profile"]
        expected = _recompute_semantic(contract, cells[(fixture, model)])["target_form_readout_profile"]
        return _canonical_equal(actual, expected) and any(
            component == {"status": "missing", "reason": "source_unresolved"}
            for component in actual.values()
        )
    raise ValueError(f"unsupported predicate: {predicate_id}")


def _validate_predicate_catalog(evaluation_contract: dict[str, Any]) -> None:
    declared = {item["predicate_id"] for item in evaluation_contract["predicate_declarations"]}
    if declared != SUPPORTED_PREDICATES:
        missing = declared - SUPPORTED_PREDICATES
        extra = SUPPORTED_PREDICATES - declared
        _fail("UNKNOWN_PREDICATE", f"predicate dispatch mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    referenced = {
        relation["predicate"]
        for signature in evaluation_contract["semantic_signatures"]
        for relation in signature["expected_relations"]
    }
    for collection in ("pair_assertions", "global_invariants"):
        referenced.update(item["predicate_id"] for item in evaluation_contract[collection])
    referenced.update(item["condition_predicate_id"] for item in evaluation_contract["retirement_rules"])
    if referenced != declared:
        _fail("DEAD_PREDICATE_DECLARATION", "predicate declarations and references differ")


def _split_roles(evaluation_contract: dict[str, Any]) -> dict[str, str]:
    roles: dict[str, str] = {}
    for assignment in evaluation_contract["synthetic_split_contract"]["assignments"]:
        for fixture in assignment["development_fixture_keys"]:
            roles[fixture] = "development"
        for fixture in assignment["sealed_fixture_keys"]:
            roles[fixture] = "sealed"
    return roles


def _signature_results(
    evaluation_contract: dict[str, Any], cells: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    signatures = _index(evaluation_contract["semantic_signatures"], "signature_id")
    expected = {
        (item["fixture_key"], model): signature
        for item in evaluation_contract["cell_assertions"]
        for model, signature in item["expected_by_model"].items()
    }
    roles = _split_roles(evaluation_contract)
    results: list[dict[str, Any]] = []
    lookup: dict[tuple[str, str], dict[str, Any]] = {}
    for cell in cells:
        signature_id = expected[(cell["fixture_key"], cell["model_id"])]
        signature = signatures[signature_id]
        failed: list[str] = []
        for relation in signature["expected_relations"]:
            try:
                passed = _relation_passes(relation, cell)
            except (KeyError, TypeError, ValueError):
                passed = False
            if not passed:
                failed.append(relation["path"])
        result = {
            "signature_id": signature_id,
            "block_id": cell["block_id"],
            "fixture_key": cell["fixture_key"],
            "model_id": cell["model_id"],
            "evaluation_role": roles[cell["fixture_key"]],
            "status": "PASS" if not failed else "FAIL",
            "evaluated_relation_count": len(signature["expected_relations"]),
            "failed_relation_paths": failed,
            "failure_codes": [] if not failed else ["SIGNATURE_RELATION_FAILURE"],
        }
        results.append(result)
        lookup[(cell["fixture_key"], cell["model_id"])] = result
    return results, lookup


def _cell_assertion_results(
    evaluation_contract: dict[str, Any],
    signature_lookup: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    roles = _split_roles(evaluation_contract)
    results: list[dict[str, Any]] = []
    for declaration in evaluation_contract["cell_assertions"]:
        fixture = declaration["fixture_key"]
        passed = all(
            signature_lookup[(fixture, model)]["status"] == "PASS"
            and signature_lookup[(fixture, model)]["signature_id"] == signature
            for model, signature in declaration["expected_by_model"].items()
        )
        results.append(
            {
                "cell_assertion_id": f"cell.{fixture}",
                "block_id": declaration["block_id"],
                "fixture_key": fixture,
                "evaluation_role": roles[fixture],
                "status": "PASS" if passed else "FAIL",
                "failure_codes": [] if passed else ["CELL_ASSERTION_FAILURE"],
            }
        )
    return results


def _assertion_results(
    group: str,
    declarations: list[dict[str, Any]],
    *,
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells: list[dict[str, Any]],
    bound: dict[str, Any],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    roles = _split_roles(evaluation_contract)
    fixture_keys = set(roles)
    for declaration in declarations:
        try:
            passed = _predicate(
                declaration["predicate_id"],
                declaration["operands"],
                contract=contract,
                evaluation_contract=evaluation_contract,
                cells_list=cells,
                bound=bound,
            )
        except D1ChallengerContractError as error:
            _fail("ADAPTER_CONTRACT_ERROR", f"{declaration['assertion_id']}: {error}")
        except (KeyError, StopIteration, TypeError, ValueError) as error:
            _fail("EVALUATION_CONTRACT_ERROR", f"{declaration['assertion_id']}: {error}")
        operand_fixtures = [item for item in declaration["operands"] if item in fixture_keys]
        operand_roles = {roles[item] for item in operand_fixtures}
        evaluation_role = (
            next(iter(operand_roles))
            if len(operand_roles) == 1
            else "mixed" if operand_roles else "all"
        )
        results.append(
            {
                "assertion_id": declaration["assertion_id"],
                "predicate_id": declaration["predicate_id"],
                "assertion_group": group,
                "evaluation_role": evaluation_role,
                "status": "PASS" if passed else "FAIL",
                "failure_codes": [] if passed else ["ASSERTION_FAILURE"],
            }
        )
    return results


def _retirement_results(
    *,
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells: list[dict[str, Any]],
    bound: dict[str, Any],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for rule in evaluation_contract["retirement_rules"]:
        try:
            triggered = _predicate(
                rule["condition_predicate_id"],
                rule["condition_operands"],
                contract=contract,
                evaluation_contract=evaluation_contract,
                cells_list=cells,
                bound=bound,
            )
        except D1ChallengerContractError as error:
            _fail("ADAPTER_CONTRACT_ERROR", f"{rule['rule_id']}: {error}")
        except (KeyError, StopIteration, TypeError, ValueError) as error:
            _fail("RETIREMENT_EVALUATION_FAILURE", f"{rule['rule_id']}: {error}")
        results.append(
            {
                "rule_id": rule["rule_id"],
                "condition_predicate_id": rule["condition_predicate_id"],
                "condition_status": "TRIGGERED" if triggered else "NOT_TRIGGERED",
                "disposition": rule["disposition"],
                "authoritative_mutation": False,
                "failure_codes": [],
            }
        )
    return results


def _challenger_results(
    *,
    contract: dict[str, Any],
    evaluation_contract: dict[str, Any],
    cells: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    cells_map = _cell_map(cells)
    roles = _split_roles(evaluation_contract)
    reference_models = {
        "SOURCE_COMPILER": "TF2",
        "ENCOUNTER_FORMATION": "ERT",
        "GHOST_PATH": "GTP",
    }
    results: list[dict[str, Any]] = []
    for declaration in evaluation_contract["challenger_declarations"]:
        block = declaration["block_id"]
        model = reference_models[block]
        target_id = declaration["comparison_target_id"]
        for fixture in _block_fixtures(contract, block):
            try:
                model_value = _model_target(
                    evaluation_contract, cells_map, fixture, model, target_id
                )
                challenger_value = _challenger_target(
                    contract,
                    evaluation_contract,
                    declaration["challenger_id"],
                    fixture,
                )
            except D1ChallengerContractError as error:
                _fail(
                    "ADAPTER_CONTRACT_ERROR",
                    f"{declaration['challenger_id']}:{fixture}: {error}",
                )
            results.append(
                {
                    "challenger_id": declaration["challenger_id"],
                    "challenger_role": declaration["challenger_role"],
                    "block_id": block,
                    "fixture_key": fixture,
                    "evaluation_role": roles[fixture],
                    "reference_model_id": model,
                    "comparison_target_id": target_id,
                    "model_target_sha256": digest(model_value),
                    "challenger_target_sha256": digest(challenger_value),
                    "targets_equal": _canonical_equal(model_value, challenger_value),
                }
            )
    return results


def evaluate_d1(
    execution_manifest_bytes: bytes,
    evaluation_manifest_bytes: bytes,
    cell_result_schema_bytes: bytes,
    run_artifact_schema_bytes: bytes,
    run_artifact_bytes: bytes,
    evaluator_policy_bytes: bytes,
    conformance_report_schema_bytes: bytes,
) -> dict[str, Any]:
    """Evaluate one completed frozen D1 run in a separate process."""
    bound = _bind_inputs(
        execution_manifest_bytes,
        evaluation_manifest_bytes,
        cell_result_schema_bytes,
        run_artifact_schema_bytes,
        run_artifact_bytes,
        evaluator_policy_bytes,
        conformance_report_schema_bytes,
    )
    cells = _validate_run(bound)
    contract = bound["execution"]["manifest"]["execution_contract"]
    evaluation_contract = bound["evaluation"]["manifest"]["evaluation_contract"]
    _validate_predicate_catalog(evaluation_contract)
    signatures, signature_lookup = _signature_results(evaluation_contract, cells)
    cell_results = _cell_assertion_results(evaluation_contract, signature_lookup)
    pair_results = _assertion_results(
        "pair",
        evaluation_contract["pair_assertions"],
        contract=contract,
        evaluation_contract=evaluation_contract,
        cells=cells,
        bound=bound,
    )
    global_results = _assertion_results(
        "global",
        evaluation_contract["global_invariants"],
        contract=contract,
        evaluation_contract=evaluation_contract,
        cells=cells,
        bound=bound,
    )
    challenger_results = _challenger_results(
        contract=contract, evaluation_contract=evaluation_contract, cells=cells
    )
    retirement_results = _retirement_results(
        contract=contract,
        evaluation_contract=evaluation_contract,
        cells=cells,
        bound=bound,
    )
    all_assertions = cell_results + pair_results + global_results
    signature_fail = sum(item["status"] == "FAIL" for item in signatures)
    assertion_fail = sum(item["status"] == "FAIL" for item in all_assertions)
    status = "PASS" if signature_fail == assertion_fail == 0 else "FAIL"
    triggered = {
        item["rule_id"]
        for item in retirement_results
        if item["condition_status"] == "TRIGGERED"
    }
    rt_reference = "retire.challenger.ch_rt_congruence" in triggered
    rt_alias = "retire.challenger.ch_declared_rt_lookup" in triggered
    challenger_roles = {
        item["challenger_id"]: item["challenger_role"]
        for item in evaluation_contract["challenger_declarations"]
    }
    rule_by_id = {item["rule_id"]: item for item in evaluation_contract["retirement_rules"]}
    distinct_reductions = sum(
        rule_by_id[rule_id]["condition_predicate_id"]
        == "challenger_equivalent_all_fixtures_target"
        and challenger_roles.get(rule_by_id[rule_id]["condition_operands"][2])
        == "distinct_challenger"
        for rule_id in triggered
    )
    split_counts = Counter(item["evaluation_role"] for item in signatures)
    report = {
        "report_id": REPORT_ID,
        "report_version": REPORT_VERSION,
        "status": status,
        "policy_id": bound["policy_body"]["policy_id"],
        "policy_version": bound["policy_body"]["policy_version"],
        "artifact_bindings": {
            "execution_manifest_file_sha256": EXECUTION_FILE_SHA256,
            "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
            "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
            "evaluation_manifest_file_sha256": EVALUATION_FILE_SHA256,
            "evaluation_manifest_sha256": EVALUATION_MANIFEST_SHA256,
            "evaluation_contract_sha256": EVALUATION_CONTRACT_SHA256,
            "cell_result_schema_sha256": RESULT_SCHEMA_SHA256,
            "run_artifact_schema_sha256": RUN_SCHEMA_SHA256,
            "evaluator_policy_sha256": POLICY_SHA256,
            "conformance_report_schema_sha256": REPORT_SCHEMA_SHA256,
            "run_sha256": bound["run"]["integrity"]["run_sha256"],
        },
        "implementation_bindings": {
            "runner": {
                "implementation_id": bound["policy_body"]["implementation_identities"]["runner"]["implementation_id"],
                "implementation_version": bound["policy_body"]["implementation_identities"]["runner"]["implementation_version"],
                "source_sha256": bound["run"]["runner_implementation_sha256"],
                "bundle_sha256": bound["run"]["runner_bundle_sha256"],
            },
            "evaluator": {
                "implementation_id": EVALUATOR_ID,
                "implementation_version": EVALUATOR_VERSION,
                "source_sha256": _sha(Path(__file__).read_bytes()),
                "bundle_sha256": bound["bundles"]["evaluator"],
            },
        },
        "input_summary": {
            "run_id": bound["run"]["run_id"],
            "expected_cell_count": 88,
            "reported_cell_count": len(cells),
            "source_cell_count": len(_block_cells(cells, "SOURCE_COMPILER")),
            "formation_cell_count": len(_block_cells(cells, "ENCOUNTER_FORMATION")),
            "ghost_cell_count": len(_block_cells(cells, "GHOST_PATH")),
            "development_signature_count": split_counts["development"],
            "sealed_signature_count": split_counts["sealed"],
        },
        "schema_validation": {
            "status": "PASS",
            "validated_cell_count": len(cells),
            "failure_codes": [],
        },
        "signature_results": signatures,
        "cell_assertion_results": cell_results,
        "pair_assertion_results": pair_results,
        "global_assertion_results": global_results,
        "challenger_results": challenger_results,
        "retirement_results": retirement_results,
        "summary": {
            "signature_pass_count": len(signatures) - signature_fail,
            "signature_fail_count": signature_fail,
            "cell_assertion_pass_count": sum(item["status"] == "PASS" for item in cell_results),
            "cell_assertion_fail_count": sum(item["status"] == "FAIL" for item in cell_results),
            "pair_assertion_pass_count": sum(item["status"] == "PASS" for item in pair_results),
            "pair_assertion_fail_count": sum(item["status"] == "FAIL" for item in pair_results),
            "global_assertion_pass_count": sum(item["status"] == "PASS" for item in global_results),
            "global_assertion_fail_count": sum(item["status"] == "FAIL" for item in global_results),
            "retirement_triggered_count": len(triggered),
            "retirement_not_triggered_count": len(retirement_results) - len(triggered),
            "rt_equivalence_family_count": int(rt_reference),
            "rt_alias_control_confirmation_count": int(rt_alias),
            "distinct_challenger_reduction_count": distinct_reductions,
        },
        "failure_codes": (
            []
            if status == "PASS"
            else sorted(
                {
                    code
                    for item in signatures + all_assertions
                    for code in item["failure_codes"]
                }
            )
        ),
        "observability": {
            "evaluation_domain": "detached_synthetic_structural_conformance",
            "intermediate_typed_values_serialized": False,
            "typed_dataflow_claim": "static_frozen_dag_plus_independent_final_semantic_recomputation",
            "runner_blinding_claim": "implementation_bound_process_separation_not_cryptographic_non_access_proof",
            "guard_claim": "detached_digest_equality_not_runtime_ledger_observation",
            "runtime_ledgers_observed": False,
            "human_empirical_evidence": False,
            "predictive_support": False,
        },
        "disclaimers": evaluation_contract["report_disclaimers"],
    }
    envelope = {
        "$schema": "./interp-001d1-v1-conformance-report.schema.json",
        "report": report,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization_id": CANONICALIZATION_ID,
            "report_sha256": digest(report),
        },
    }
    try:
        validate_json_schema(envelope, bound["report_schema"])
    except (FrozenD1ExecutionError, ValueError) as error:
        _fail("REPORT_SCHEMA_FAILURE", f"generated report failed schema: {error}")
    return envelope


def encode_report(envelope: dict[str, Any]) -> bytes:
    return canonical_bytes(envelope) + b"\n"
