from __future__ import annotations

import base64
from collections.abc import Mapping
from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

from dynamics.labs.interp_d1_common import (
    FrozenD1ExecutionError,
    canonical_bytes,
    digest,
    file_sha256,
    load_exact,
    validate_json_schema,
)
from dynamics.labs.interp_d2a0_exec0_contract import (
    load_contract_bundle as load_exec0_bundle,
    validate_contract_bundle as validate_exec0_bundle,
    verify_frozen_contract as verify_exec0_contract,
)


ROOT = Path(__file__).resolve().parents[2]
D2A0_DIR = ROOT / "research/scenarios/interp-dialogue-001/d2a0"
EXEC0_DIR = D2A0_DIR / "exec0"
MAT0_DIR = D2A0_DIR / "mat0"

PREDECESSOR_MANIFEST_SHA256 = (
    "8ee62993fbf302d8037f8cf898a0edca4fe7bbff7b01f73f6a71e8b6c04c3efd"
)
EXEC0_MANIFEST_SHA256 = (
    "1a7203d93a341c3b4570d4070d95457441da190e4c8ff167f86d89d0135c40f3"
)
MAT0_MANIFEST_SHA256 = (
    "a82f3f4c31726107541dbe91654c0f3387491fd11fa984f82669186b02cbd1ef"
)

DOCUMENT_FILES = {
    "composed_runner_input": "composed-runner-input-v0.json",
    "fixture_normalization": "fixture-normalization-v0.json",
    "operator_program": "operator-program-v0.json",
    "record_materialization": "record-materialization-v0.json",
    "lifecycle_emission": "lifecycle-emission-v0.json",
    "rejection_materialization": "rejection-materialization-v0.json",
    "digest_contract": "digest-contract-v0.json",
    "source_bundle_contract": "source-bundle-contract-v0.json",
    "materialization_golden_traces": "materialization-golden-traces-v0.json",
    "frozen_artifact_manifest": "frozen-artifact-manifest-v0.json",
}

FROZEN_FILES = {
    "contract_schema": ("contract.schema.json", "CONTRACT_AUTHORITY"),
    "composed_runner_input": ("composed-runner-input-v0.json", "RUNNER_VISIBLE"),
    "fixture_normalization": ("fixture-normalization-v0.json", "RUNNER_VISIBLE"),
    "operator_program": ("operator-program-v0.json", "RUNNER_VISIBLE"),
    "record_materialization": ("record-materialization-v0.json", "RUNNER_VISIBLE"),
    "lifecycle_emission": ("lifecycle-emission-v0.json", "RUNNER_VISIBLE"),
    "rejection_materialization": ("rejection-materialization-v0.json", "RUNNER_VISIBLE"),
    "digest_contract": ("digest-contract-v0.json", "RUNNER_AND_EVALUATOR_VISIBLE"),
    "evaluation_v1_schema": ("evaluation-v1.schema.json", "EVALUATOR_ONLY"),
    "publication_v1_schema": ("publication-v1.schema.json", "PUBLICATION_ONLY"),
    "source_bundle_contract": ("source-bundle-contract-v0.json", "PUBLICATION_ONLY"),
    "materialization_golden_traces": (
        "materialization-golden-traces-v0.json",
        "CONTRACT_TEST_ONLY",
    ),
}

PREDECESSOR_INPUTS = {
    "runtime_spine": ("../runtime-spine-v0.json", "b604260073555cb1e72fb8f38eacaaee436c60593fec8f356afe89c428cc2b67"),
    "strategy_catalog": ("../strategy-catalog-v0.json", "a4f81f57d2264b2154b8464e3f32f4a91e9fd44b67508690d77be6a9112784a7"),
    "fixture_catalog": ("../fixture-catalog-v0.json", "679b252ce21e3d9040d744814ad87878788e911ad2120f67af3381e1cb771289"),
    "policy": ("../policy-v0.json", "2201c85e4287e5937138d97df2994dd2ced592d8f2c8ac375c88ebffb1e63cb7"),
}

EXEC0_INPUTS = {
    "operator_catalog": ("../exec0/operator-catalog-v0.json", "ecad2ca4727eaf45a891999590ca500f64f39c20526973062138d14971308e8f"),
    "lifecycle_processor": ("../exec0/lifecycle-processor-v0.json", "9cbcffe813ef98253b8449bde5b6af2a00728955cd4e9e0c85b8b28f62046dc0"),
    "fixture_extension": ("../exec0/fixture-extension-v0.json", "23b631696bd257fd67ed48cb6c3ec3318977d833e6f7507f13734fdf1d6e0d75"),
    "execution_unit_manifest": ("../exec0/execution-unit-manifest-v0.json", "d6a5db6296fc28064055fc61a7bfa0941448b94b1d3ddd507e182a963e35a26a"),
    "trace_v1_schema": ("../exec0/trace-v1.schema.json", "bec3e60117261a793cbe9713ecd81a37eeb37ab11bc8d9744372f83ccb710237"),
    "run_v1_schema": ("../exec0/run-v1.schema.json", "f639b0064a6fe3c3ea7006aa17d6267bca0b22f407d3de9f2f6b3431c5a301f6"),
}

FIXTURE_IDS = (
    "FX-EQUAL-SURFACE-DIFFERENT-PATH",
    "FX-ROLE-PROJECTION-ONLY",
    "FX-EVIDENCE-SUBJECTIVE-PATH",
    "FX-SAME-ACCESS-REJECTION",
    "FX-REVISION-LIFECYCLE-SEPARATION",
    "FX-NON-FALSIFIABLE-ESCAPE",
    "FX-TRANSIENT-GATE",
    "FX-BOUNDED-ACCUMULATION",
    "FX-DECLARED-PROFILE-DISSOCIATION",
)

CELL_OPERATORS = {
    "D2A-T0": "D2A-T0-CURRENT",
    "D2A-T1": "D2A-T1-GATE",
    "D2A-T2": "D2A-T2-ACCUMULATE",
    "D2A-T3": "D2A-T3-REVISE",
    "D2A-P0": "D2A-P0-DIRECT",
    "D2A-P1": "D2A-P1-ROLE",
}

RECORD_TYPES = (
    "DeclaredRuntimeViewReceipt",
    "ReceptionCandidate",
    "SubjectiveEncounterFormCandidate",
    "InterpretationCandidateSet",
    "ScopedAdjudicationReceipt",
    "ImmediateSurfaceProjectionCandidate",
    "RevisionCandidateOccurrence",
    "RevisionEligibilityDecisionReceipt",
    "RevisionReadReceipt",
    "AccessLocalApplicationReceipt",
    "RetentionObservationReceipt",
)

LIFECYCLE_PROGRAMS = (
    "DEFAULT",
    "FUTURE_APPLY_NEXT_ACCESS",
    "SAME_ACCESS_READ",
    "ELIGIBLE_NOT_READ",
    "READ_NOT_APPLIED",
    "APPLIED_NOT_RETAINED",
    "RETAINED_AT_LATER_ACCESS",
)

REJECTION_ORDER = (
    "UNDECLARED_RUNTIME_VIEW_READ",
    "UNREGISTERED_FREE_CANDIDATE",
    "UNBOUNDED_OUT_OF_MODEL_ESCAPE",
    "SAME_ACCESS_REVISION_FEEDBACK",
    "REVISION_NOT_YET_EFFECTIVE",
    "CROSS_RUNTIME_REVISION_READ",
    "CROSS_TARGET_SCOPE_REVISION_READ",
    "CROSS_INTERPRETATION_SCOPE_REVISION_READ",
)

DIGEST_TARGETS = {
    "record.payload_digest",
    "SubjectiveEncounterFormCandidate.payload.subjective_path_digest",
    "trace.content_sha256",
    "run_artifact_sha256",
    "evaluation_artifact_sha256",
    "resolved_value_digest",
    "source_bundle_sha256",
}

GOLDEN_CASES = {
    "GOLDEN-COMPLETED-SINGLE-ACCESS",
    "GOLDEN-TYPED-REJECTION",
    "GOLDEN-MULTI-ACCESS-LIFECYCLE",
}


class D2A0Mat0ContractError(ValueError):
    """Raised when the frozen materialization ABI is incomplete or mutable."""


def _fail(message: str) -> None:
    raise D2A0Mat0ContractError(message)


def _ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    values = [row[key] for row in rows]
    if len(values) != len(set(values)):
        _fail(f"duplicate {key}")
    return values


def _validate_envelopes(bundle: Mapping[str, Any]) -> None:
    schema = bundle["contract_schema"]
    for kind in DOCUMENT_FILES:
        try:
            validate_json_schema(bundle[kind], schema)
        except FrozenD1ExecutionError as error:
            raise D2A0Mat0ContractError(f"{kind} schema violation: {error}") from error
        if bundle[kind]["document_kind"] != kind:
            _fail(f"document kind mismatch: {kind}")


def _row_bindings(rows: list[dict[str, Any]]) -> dict[str, tuple[str, str]]:
    return {
        row["document_kind"]: (row["path"], row["sha256"])
        for row in rows
    }


def _validate_composed_inputs(bundle: Mapping[str, Any]) -> None:
    payload = bundle["composed_runner_input"]["payload"]
    if _row_bindings(payload["predecessor_runner_visible_documents"]) != PREDECESSOR_INPUTS:
        _fail("predecessor runner-visible composition changed")
    if _row_bindings(payload["exec0_runner_visible_documents"]) != EXEC0_INPUTS:
        _fail("EXEC0 runner-visible composition changed")
    if "strategy_catalog" not in _row_bindings(payload["predecessor_runner_visible_documents"]):
        _fail("strategy catalog is not runner-visible")
    expected_mat0 = {
        "fixture_normalization", "operator_program", "record_materialization",
        "lifecycle_emission", "rejection_materialization", "digest_contract",
    }
    if set(payload["mat0_runner_visible_document_kinds"]) != expected_mat0:
        _fail("MAT0 runner-visible ABI inventory changed")
    forbidden = set(payload["runner_forbidden_document_kinds"])
    if not {
        "operator_golden_vectors", "evaluator_policy", "evaluation_manifest",
        "evaluation_v1_schema", "publication_v1_schema",
        "materialization_golden_traces",
    } <= forbidden:
        _fail("runner forbidden-input lane weakened")
    if expected_mat0 & forbidden:
        _fail("runner materialization and forbidden lanes overlap")
    if payload["composition_rule"] != "NO_FILENAME_DISCOVERY_NO_IMPLICIT_INHERITANCE_NO_CELL_ID_PARSING":
        _fail("composed input gained inference authority")
    superseded = {row["superseded_path"]: row["replacement_path"] for row in payload["supersession_rules"] if "superseded_path" in row}
    if superseded.get("../trace.schema.json") != "../exec0/trace-v1.schema.json":
        _fail("predecessor trace carrier supersession changed")


def _all_fixtures(exec0: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = [
        *exec0["predecessor_fixture_catalog"]["fixtures"],
        *exec0["fixture_extension"]["payload"]["fixtures"],
    ]
    return {row["fixture_id"]: row for row in rows}


def _raw_predecessor_paths(exec0: Mapping[str, Any]) -> set[str]:
    values: set[str] = set()
    for fixture in exec0["predecessor_fixture_catalog"]["fixtures"]:
        for item in fixture["clamped_fields"]:
            if item["field"] == "supplied_interpretation_path":
                values.add(item["value"])
        for arm in fixture["arms"]:
            for item in arm["assignments"]:
                if item["field"] == "supplied_interpretation_path":
                    values.add(item["value"])
    return values


def _validate_normalization(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["fixture_normalization"]["payload"]
    if payload["merge_precedence"] != [
        "NORMALIZATION_DEFAULTS", "FIXTURE_CLAMPS", "ARM_ASSIGNMENTS",
        "ACCESS_ORDINAL_OVERRIDES",
    ]:
        _fail("fixture merge precedence changed")
    adapters = {row["source_field"]: row for row in payload["field_adapters"]}
    path_adapter = adapters.get("supplied_interpretation_path")
    if path_adapter is None or path_adapter["targets"] != ["source_path_identity", "supplied_path"]:
        _fail("predecessor supplied path adapter is incomplete")
    mapping = payload["path_value_adapter"]
    if not _raw_predecessor_paths(exec0) <= set(mapping):
        _fail("predecessor path vocabulary is not closed")
    if mapping.get("PATH-A") != "PATH-AMBIGUOUS" or mapping.get("PATH-B") != "PATH-AMBIGUOUS":
        _fail("opaque path identities gained an inferred rank difference")
    if payload["source_identity_rule"] != "raw predecessor path token is preserved even when multiple tokens map to the same ranked supplied_path":
        _fail("raw subjective path identity is not preserved")
    programs = payload["fixture_programs"]
    if tuple(_ids(programs, "fixture_id")) != FIXTURE_IDS:
        _fail("fixture normalization program inventory changed")
    fixtures = _all_fixtures(exec0)
    for program in programs:
        fixture = fixtures[program["fixture_id"]]
        ordinals = {row["access_ordinal"] for row in fixture["access_lineage"]}
        for access in program["access_rules"]:
            ordinal = access["access_ordinal"]
            if isinstance(ordinal, int) and ordinal not in ordinals:
                _fail(f"normalization access is outside fixture lineage: {program['fixture_id']}")
    equal = programs[0]
    if equal["access_rules"][0]["surface_override"] != "SURFACE-NEUTRAL":
        _fail("equal-surface fixture lost its declared output intervention")
    if payload["undeclared_field_policy"] != "HARD_CONTRACT_FAILURE":
        _fail("normalization became open-world")


def _validate_operator_program(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["operator_program"]["payload"]
    programs = {row["cell_id"]: row for row in payload["cell_programs"]}
    cells = {row["cell_id"]: row for row in exec0["predecessor_strategy_catalog"]["registered_cells"]}
    if set(programs) != set(cells):
        _fail("exact cell program inventory changed")
    for cell_id, source in cells.items():
        row = programs[cell_id]
        expected_t = CELL_OPERATORS[source["temporal_strategy"]]
        expected_p = CELL_OPERATORS[source["projection_strategy"]]
        if row["temporal_operator"] != expected_t or row["projection_operator"] != expected_p:
            _fail(f"cell operator binding changed: {cell_id}")
        if row["operator_sequence"] != ["D2A-H-BIND", "D2A-RECEPTION-BIAS", expected_t, expected_p]:
            _fail(f"cell operator order changed: {cell_id}")
    if "PARSE_CELL_ID" not in payload["forbidden_shortcuts"]:
        _fail("runner may parse cell IDs heuristically")
    intermediate = payload["intermediate_construction"]
    if intermediate["revision_path_absence_sentinel"] != "NO-REVISION":
        _fail("absent revision representation changed")
    if intermediate["eligibility_receipt_rule"] != "emit exactly one per FULL_INTERPRETATION access even for NOT_ELIGIBLE NOT_EMITTED or NOT_APPLICABLE_TO_MODEL":
        _fail("eligibility receipt materialization is ambiguous")
    if "rank-max" not in intermediate["narrow_candidate_rule"]:
        _fail("ambiguity NARROW program is not closed")


def _validate_records(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["record_materialization"]["payload"]
    rows = payload["stage_ranks"]
    if [row["rank"] for row in rows] != list(range(1, 12)):
        _fail("record stage ranks changed")
    if tuple(row["type_id"] for row in rows) != RECORD_TYPES:
        _fail("record type order changed")
    if payload["payload_contract"] != exec0["operator_catalog"]["payload"]["record_payload_contract"]:
        _fail("record payload fields differ from EXEC0")
    rank = {row["type_id"]: row["rank"] for row in rows}
    for row in rows:
        for source in row["source_types"]:
            source_type = source.removesuffix(" when emitted").split(" at ", 1)[0]
            if source_type not in rank or rank[source_type] >= row["rank"]:
                _fail(f"record source does not precede writer: {row['type_id']}")
    if "access_ordinal_zero_padded_3" not in payload["record_id_rule"]:
        _fail("record identity is not access-stable")
    if payload["source_record_id_rule"] != "resolve source_types in listed order; conditional absent source is omitted; every resolved ID must precede the record":
        _fail("record source lineage order changed")


def _validate_selector_materializability(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    fixtures = _all_fixtures(exec0)
    units = {row["execution_unit_id"]: row for row in exec0["execution_unit_manifest"]["payload"]["execution_units"]}
    record_types = set(RECORD_TYPES)
    for assertion in exec0["evaluation_manifest"]["payload"]["assertions"]:
        for selector in assertion["operands"]:
            unit = units[selector["execution_unit_id"]]
            if selector["source_kind"] == "RECORD":
                if selector["type_id"] not in record_types:
                    _fail("evaluator selector references an unmaterialized record")
                ordinals = {row["access_ordinal"] for row in fixtures[unit["fixture_id"]]["access_lineage"]}
                if selector["access_ordinal"] not in ordinals:
                    _fail("evaluator selector access is outside fixture lineage")


def _validate_lifecycle(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["lifecycle_emission"]["payload"]
    programs = payload["programs"]
    if tuple(_ids(programs, "program_id")) != LIFECYCLE_PROGRAMS:
        _fail("lifecycle emission program inventory changed")
    by_id = {row["program_id"]: row for row in programs}
    future = by_id["FUTURE_APPLY_NEXT_ACCESS"]
    if future["read"] != [{
        "access_ordinal": 2,
        "read_status": "READ",
        "condition": "PRIOR_ELIGIBLE_REVISION_EXISTS",
    }] or future["apply"] != [{
        "access_ordinal": 2,
        "application_status": "APPLIED",
        "condition": "MATCHING_READ_EXISTS",
    }]:
        _fail("future-effective revision application program changed")
    if by_id["ELIGIBLE_NOT_READ"]["read"]:
        _fail("ELIGIBLE_NOT_READ emitted a read receipt")
    if by_id["READ_NOT_APPLIED"]["apply"]:
        _fail("READ_NOT_APPLIED emitted an application receipt")
    observed = by_id["APPLIED_NOT_RETAINED"]["observe"]
    if observed != [{"access_ordinal": 3, "observation_status": "OBSERVED_NOT_RETAINED"}]:
        _fail("negative retention observation changed")
    if payload["negative_receipt_rule"] != "absence of read or apply is represented by record omission; no NOT_READ or NOT_APPLIED receipt is invented":
        _fail("negative lifecycle receipt semantics changed")
    fixture = next(row for row in exec0["predecessor_fixture_catalog"]["fixtures"] if row["fixture_id"] == "FX-REVISION-LIFECYCLE-SEPARATION")
    arm_programs = {item["value"] for arm in fixture["arms"] for item in arm["assignments"] if item["field"] == "lifecycle_program"}
    if not arm_programs <= set(by_id):
        _fail("predecessor lifecycle arm lacks an emission program")


def _validate_rejections(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["rejection_materialization"]["payload"]
    rows = payload["rows"]
    if [row["priority"] for row in rows] != list(range(1, 9)):
        _fail("rejection precedence changed")
    if tuple(row["rejection_code"] for row in rows) != REJECTION_ORDER:
        _fail("typed rejection truth table changed")
    frozen_codes = set(exec0["lifecycle_processor"]["payload"]["typed_rejection_codes"])
    if set(REJECTION_ORDER) != frozen_codes:
        _fail("MAT0 rejection table differs from EXEC0 vocabulary")
    by_code = {row["rejection_code"]: row for row in rows}
    if by_code["SAME_ACCESS_REVISION_FEEDBACK"]["rejected_stage"] != "READ_ELIGIBLE_REVISION":
        _fail("same-access rejection stage changed")
    if by_code["UNREGISTERED_FREE_CANDIDATE"]["offending_input_refs"] != ["FIXTURE-FIELD:candidate_escape_mode:UNDECLARED_FREE_CANDIDATE"]:
        _fail("free-candidate offending input identity changed")
    if payload["terminal_rule"] != "typed rejection terminates one unit and the run continues; unknown row or missing source binding aborts the whole run":
        _fail("typed rejection terminal semantics changed")


def _validate_digests(bundle: Mapping[str, Any]) -> None:
    payload = bundle["digest_contract"]["payload"]
    if {row["target"] for row in payload["digest_rules"]} != DIGEST_TARGETS:
        _fail("digest target inventory changed")
    canonical = payload["canonicalization"]
    if canonical != {
        "canonicalization_id": "interp-canonical-json-v1",
        "parser": "UTF-8 strict JSON with duplicate object keys rejected",
        "encoding": "UTF-8",
        "object_keys": "ASCII-only keys in lexicographic order",
        "separators": "comma and colon without surrounding whitespace",
        "unicode": "NFC strings emitted without ASCII escaping; surrogate code points rejected",
        "numbers": "integers only; floating-point literals NaN and infinities rejected",
        "line_ending": "canonical value bytes contain no trailing newline",
    }:
        _fail("canonical JSON identity changed")
    if payload["serialization_rule"] != "persisted JSON artifact equals canonical value bytes plus exactly one LF":
        _fail("persisted artifact byte rule changed")
    if payload["self_digest_rule"] != "run and evaluation documents have no self digest; publication manifest carries their external raw-file digests":
        _fail("run or evaluation gained a circular self digest")


def _validate_evaluation_schema(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    schema = bundle["evaluation_schema"]
    result = schema["$defs"]["assertionResult"]
    policy = exec0["evaluator_policy"]["payload"]
    if set(result["properties"]["evaluation_status"]["enum"]) != set(policy["assertion_evaluation_statuses"]):
        _fail("evaluation result status differs from EXEC0")
    if set(result["properties"]["interpretation_code"]["enum"]) != set(policy["interpretation_codes"]):
        _fail("evaluation interpretation vocabulary differs from EXEC0")
    if set(schema["properties"]["run_evaluation_status"]["enum"]) != set(policy["run_evaluation_statuses"]):
        _fail("run evaluation status differs from EXEC0")
    if schema["properties"]["assertion_results"]["minItems"] != 20 or schema["properties"]["assertion_results"]["maxItems"] != 20:
        _fail("evaluation carrier no longer binds 20 assertions")
    status_rules = {
        row["if"]["properties"]["evaluation_status"]["const"]
        for row in result["allOf"]
    }
    if status_rules != set(policy["assertion_evaluation_statuses"]):
        _fail("assertion status-to-code rules are incomplete")
    required = set(schema["$defs"]["resolvedOperand"]["required"])
    if not {"execution_unit_id", "trace_id", "record_id", "json_pointer", "resolved_value", "resolved_value_digest"} <= required:
        _fail("resolved operand audit carrier is incomplete")
    if "mat0_manifest_sha256" not in schema["required"]:
        _fail("evaluation artifact does not bind MAT0")
    if schema.get("x-semantic-rules") != [
        "assertion_results follow frozen evaluation-manifest assertion order exactly",
        "VIOLATED interpretation_code equals the assertion violation_interpretation_code",
        "summary status counts sum to registered_assertion_count 20",
        "any NOT_EVALUABLE yields PARTIALLY_EVALUABLE unless a VIOLATED result yields DOES_NOT_CONFORM",
        "all SATISFIED yields CONFORMS_WITHIN_REGISTERED_SCOPE",
    ]:
        _fail("evaluation result semantic rules changed")


def _validate_source_bundles(bundle: Mapping[str, Any]) -> None:
    payload = bundle["source_bundle_contract"]["payload"]
    bundles = {row["role"]: row for row in payload["bundles"]}
    expected = {
        "RUNNER": [
            "dynamics/labs/interp_d2a1_common.py",
            "dynamics/labs/interp_d2a1_operators.py",
            "dynamics/labs/interp_d2a1_runner.py",
            "dynamics/labs/interp_d2a1_runner_cli.py",
        ],
        "EVALUATOR": [
            "dynamics/labs/interp_d2a1_common.py",
            "dynamics/labs/interp_d2a1_evaluator.py",
            "dynamics/labs/interp_d2a1_evaluator_cli.py",
        ],
    }
    if {role: row["paths"] for role, row in bundles.items()} != expected:
        _fail("future source bundle path inventory changed")
    for row in bundles.values():
        if row["paths"] != sorted(row["paths"]):
            _fail("source bundle paths are not canonical")
    if set(payload["cross_role_import_policy"]) != {
        "RUNNER_MUST_NOT_IMPORT_EVALUATOR",
        "EVALUATOR_MUST_NOT_IMPORT_RUNNER",
        "EVALUATOR_MUST_NOT_IMPORT_OPERATOR_IMPLEMENTATION",
    }:
        _fail("runner/evaluator import isolation changed")
    carrier = payload.get("publication_carrier")
    if carrier != {
        "schema_path": "publication-v1.schema.json",
        "source_bundle_order": ["RUNNER", "EVALUATOR"],
        "artifact_order": ["run_artifact", "evaluation_artifact"],
        "timestamp_policy": "FORBIDDEN",
    }:
        _fail("publication carrier identity changed")


def _validate_publication_schema(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    schema = bundle["publication_schema"]
    required = set(schema["required"])
    if not {
        "predecessor_manifest_sha256", "exec0_manifest_sha256",
        "mat0_manifest_sha256", "run_artifact", "evaluation_artifact",
        "source_bundles", "run_evaluation_status",
    } <= required:
        _fail("publication manifest carrier is incomplete")
    if schema["properties"]["predecessor_manifest_sha256"]["const"] != PREDECESSOR_MANIFEST_SHA256:
        _fail("publication predecessor binding changed")
    if schema["properties"]["exec0_manifest_sha256"]["const"] != EXEC0_MANIFEST_SHA256:
        _fail("publication EXEC0 binding changed")
    if set(schema["properties"]["run_evaluation_status"]["enum"]) != set(
        exec0["evaluator_policy"]["payload"]["run_evaluation_statuses"]
    ):
        _fail("publication status differs from evaluator policy")
    if schema["properties"]["source_bundles"]["minItems"] != 2 or schema["properties"]["source_bundles"]["maxItems"] != 2:
        _fail("publication no longer binds both source bundles")
    if schema.get("x-semantic-rules") != [
        "mat0_manifest_sha256 equals the merged MAT0 frozen manifest raw-file SHA-256",
        "run_artifact path is run-v1.json and evaluation_artifact path is evaluation-v1.json",
        "source_bundles order is RUNNER then EVALUATOR and entries equal the frozen source-bundle path lists",
        "every raw_file_sha256 is computed from canonical JSON plus one LF or raw source file bytes as applicable",
        "timestamps absolute paths and git working-tree metadata are forbidden",
    ]:
        _fail("publication semantic rules changed")


def _trace_without_content_digest(trace: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(trace)
    del value["content_sha256"]
    return value


def _validate_golden_traces(bundle: Mapping[str, Any], exec0: Mapping[str, Any]) -> None:
    payload = bundle["materialization_golden_traces"]["payload"]
    if payload["lane"] != "CONTRACT_TEST_ONLY":
        _fail("materialization golden traces became runner-visible")
    cases = payload["cases"]
    if set(_ids(cases, "case_id")) != GOLDEN_CASES:
        _fail("materialization golden trace inventory changed")
    for case in cases:
        trace = case["expected_trace"]
        try:
            validate_json_schema(trace, exec0["trace_schema"])
        except FrozenD1ExecutionError as error:
            raise D2A0Mat0ContractError(f"golden trace schema violation: {error}") from error
        raw = base64.b64decode(case["canonical_trace_utf8_base64"], validate=True)
        if raw != canonical_bytes(trace):
            _fail(f"golden canonical bytes changed: {case['case_id']}")
        if hashlib.sha256(raw).hexdigest() != case["canonical_trace_sha256"]:
            _fail(f"golden canonical trace digest changed: {case['case_id']}")
        if trace["content_sha256"] != digest(_trace_without_content_digest(trace)):
            _fail(f"golden trace content digest changed: {case['case_id']}")
        records = trace.get("records", trace.get("completed_prefix_records", []))
        seen: set[str] = set()
        positions: list[tuple[int, int]] = []
        for record in records:
            if record["payload_digest"] != digest(record["payload"]):
                _fail(f"golden record payload digest changed: {record['record_id']}")
            if not set(record["source_record_ids"]) <= seen:
                _fail(f"golden record source does not precede writer: {record['record_id']}")
            seen.add(record["record_id"])
            rank = RECORD_TYPES.index(record["type_id"]) + 1
            positions.append((record["access_ordinal"], rank))
        if positions != sorted(positions):
            _fail(f"golden record order changed: {case['case_id']}")


def _validate_frozen_files(bundle: Mapping[str, Any]) -> None:
    if file_sha256(D2A0_DIR / "frozen-artifact-manifest-v0.json") != PREDECESSOR_MANIFEST_SHA256:
        _fail("PR #19 frozen bytes changed")
    if file_sha256(EXEC0_DIR / "frozen-artifact-manifest-v0.json") != EXEC0_MANIFEST_SHA256:
        _fail("PR #20 frozen bytes changed")
    if file_sha256(MAT0_DIR / "frozen-artifact-manifest-v0.json") != MAT0_MANIFEST_SHA256:
        _fail("MAT0 frozen manifest bytes changed")
    rows = bundle["frozen_artifact_manifest"]["payload"]["artifacts"]
    bindings = {row["document_kind"]: row for row in rows}
    if set(bindings) != set(FROZEN_FILES):
        _fail("MAT0 frozen artifact inventory changed")
    for kind, (filename, lane) in FROZEN_FILES.items():
        row = bindings[kind]
        if row["path"] != filename or row["visibility_lane"] != lane:
            _fail(f"MAT0 artifact lane changed: {kind}")
        if file_sha256(MAT0_DIR / filename) != row["sha256"]:
            _fail(f"MAT0 artifact digest mismatch: {filename}")
    composed = bundle["composed_runner_input"]["payload"]
    for rows_key in ("predecessor_runner_visible_documents", "exec0_runner_visible_documents"):
        for row in composed[rows_key]:
            if file_sha256(MAT0_DIR / row["path"]) != row["sha256"]:
                _fail(f"composed external input digest mismatch: {row['path']}")


def validate_contract_bundle(
    bundle: Mapping[str, Any], *, verify_files: bool = False
) -> dict[str, int]:
    exec0 = bundle["exec0_bundle"]
    validate_exec0_bundle(exec0, verify_files=False)
    _validate_envelopes(bundle)
    _validate_composed_inputs(bundle)
    _validate_normalization(bundle, exec0)
    _validate_operator_program(bundle, exec0)
    _validate_records(bundle, exec0)
    _validate_selector_materializability(bundle, exec0)
    _validate_lifecycle(bundle, exec0)
    _validate_rejections(bundle, exec0)
    _validate_digests(bundle)
    _validate_evaluation_schema(bundle, exec0)
    _validate_source_bundles(bundle)
    _validate_publication_schema(bundle, exec0)
    _validate_golden_traces(bundle, exec0)
    if verify_files:
        verify_exec0_contract(ROOT)
        _validate_frozen_files(bundle)
    return {
        "composed_runner_input_count": (
            len(bundle["composed_runner_input"]["payload"]["predecessor_runner_visible_documents"])
            + len(bundle["composed_runner_input"]["payload"]["exec0_runner_visible_documents"])
            + len(bundle["composed_runner_input"]["payload"]["mat0_runner_visible_document_kinds"])
        ),
        "fixture_program_count": len(bundle["fixture_normalization"]["payload"]["fixture_programs"]),
        "cell_program_count": len(bundle["operator_program"]["payload"]["cell_programs"]),
        "record_type_count": len(bundle["record_materialization"]["payload"]["stage_ranks"]),
        "lifecycle_program_count": len(bundle["lifecycle_emission"]["payload"]["programs"]),
        "rejection_rule_count": len(bundle["rejection_materialization"]["payload"]["rows"]),
        "golden_trace_count": len(bundle["materialization_golden_traces"]["payload"]["cases"]),
        "frozen_artifact_count": len(bundle["frozen_artifact_manifest"]["payload"]["artifacts"]),
    }


def load_contract_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    root = Path(repository_root)
    mat0 = root / "research/scenarios/interp-dialogue-001/d2a0/mat0"
    bundle: dict[str, Any] = {
        "contract_schema": load_exact(mat0 / "contract.schema.json"),
        "evaluation_schema": load_exact(mat0 / "evaluation-v1.schema.json"),
        "publication_schema": load_exact(mat0 / "publication-v1.schema.json"),
        "exec0_bundle": load_exec0_bundle(root),
    }
    for kind, filename in DOCUMENT_FILES.items():
        bundle[kind] = load_exact(mat0 / filename)
    return bundle


def verify_frozen_contract(repository_root: str | Path = ROOT) -> dict[str, int]:
    return validate_contract_bundle(load_contract_bundle(repository_root), verify_files=True)


def mutated_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    return deepcopy(load_contract_bundle(repository_root))
