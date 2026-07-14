from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from dynamics.labs.interp_d1_common import (
    FrozenD1ExecutionError,
    file_sha256,
    load_exact,
    validate_json_schema,
)
from dynamics.labs.interp_d2a0_contract import (
    verify_frozen_contract as verify_predecessor_contract,
)


ROOT = Path(__file__).resolve().parents[2]
D2A0_DIR = ROOT / "research/scenarios/interp-dialogue-001/d2a0"
EXEC0_DIR = D2A0_DIR / "exec0"
PREDECESSOR_MANIFEST_SHA256 = (
    "8ee62993fbf302d8037f8cf898a0edca4fe7bbff7b01f73f6a71e8b6c04c3efd"
)
EXEC0_FROZEN_MANIFEST_SHA256 = (
    "1a7203d93a341c3b4570d4070d95457441da190e4c8ff167f86d89d0135c40f3"
)

DOCUMENT_FILES = {
    "operator_catalog": "operator-catalog-v0.json",
    "operator_golden_vectors": "operator-golden-vectors-v0.json",
    "fixture_extension": "fixture-extension-v0.json",
    "execution_unit_manifest": "execution-unit-manifest-v0.json",
    "lifecycle_processor": "lifecycle-processor-v0.json",
    "evaluator_policy": "evaluator-policy-v0.json",
    "evaluation_manifest": "evaluation-manifest-v1.json",
    "frozen_artifact_manifest": "frozen-artifact-manifest-v0.json",
}

FROZEN_FILES = {
    "contract_schema": ("contract.schema.json", "CONTRACT_AUTHORITY"),
    "operator_catalog": ("operator-catalog-v0.json", "RUNNER_VISIBLE"),
    "operator_golden_vectors": (
        "operator-golden-vectors-v0.json",
        "CONTRACT_TEST_ONLY",
    ),
    "lifecycle_processor": ("lifecycle-processor-v0.json", "RUNNER_VISIBLE"),
    "fixture_extension": ("fixture-extension-v0.json", "RUNNER_VISIBLE"),
    "execution_unit_manifest": (
        "execution-unit-manifest-v0.json",
        "RUNNER_VISIBLE",
    ),
    "trace_v1_schema": ("trace-v1.schema.json", "RUNNER_VISIBLE"),
    "run_v1_schema": ("run-v1.schema.json", "RUNNER_VISIBLE"),
    "evaluator_policy": ("evaluator-policy-v0.json", "EVALUATOR_ONLY"),
    "evaluation_manifest": ("evaluation-manifest-v1.json", "EVALUATOR_ONLY"),
}

OPERATOR_IDS = (
    "D2A-H-BIND",
    "D2A-RECEPTION-BIAS",
    "D2A-T0-CURRENT",
    "D2A-T1-GATE",
    "D2A-T2-ACCUMULATE",
    "D2A-T3-REVISE",
    "D2A-P0-DIRECT",
    "D2A-P1-ROLE",
)

GOLDEN_VECTOR_IDS = {
    "GV-H-A", "GV-H-B", "GV-H-C", "GV-R-POS", "GV-R-NEU", "GV-R-NEG",
    "GV-T0", "GV-T1-OPEN", "GV-T1-MASK", "GV-T2-BELOW", "GV-T2-LIMIT",
    "GV-T2-RESET", "GV-T3-NO-PRIOR", "GV-T3-PRIOR", "GV-P0-B", "GV-P0-A",
    "GV-P0-D", "GV-P1-PRIVATE", "GV-P1-PUBLIC-A", "GV-P1-PUBLIC-B",
}

EXTENSION_FIXTURE_IDS = {
    "FX-TRANSIENT-GATE",
    "FX-BOUNDED-ACCUMULATION",
    "FX-DECLARED-PROFILE-DISSOCIATION",
}

LIFECYCLE_ORDER = (
    "ScopedAdjudicationReceipt",
    "RevisionCandidateOccurrence",
    "RevisionEligibilityDecisionReceipt",
    "RevisionReadReceipt",
    "AccessLocalApplicationReceipt",
    "RetentionObservationReceipt",
)

LIFECYCLE_STEPS = (
    "READ_ELIGIBLE_REVISION",
    "APPLY_REVISION_FOR_ACCESS",
    "OBSERVE_RETENTION",
)

REJECTION_CODES = {
    "SAME_ACCESS_REVISION_FEEDBACK",
    "REVISION_NOT_YET_EFFECTIVE",
    "CROSS_RUNTIME_REVISION_READ",
    "CROSS_TARGET_SCOPE_REVISION_READ",
    "CROSS_INTERPRETATION_SCOPE_REVISION_READ",
    "UNDECLARED_RUNTIME_VIEW_READ",
    "UNREGISTERED_FREE_CANDIDATE",
    "UNBOUNDED_OUT_OF_MODEL_ESCAPE",
}

ASSERTION_STATUSES = {
    "SATISFIED", "VIOLATED", "NOT_APPLICABLE", "NOT_EVALUABLE"
}

INTERPRETATION_CODES = {
    "NONE",
    "AUTHORITY_FAILURE",
    "HARD_INVARIANT_FAILURE",
    "STAGE_EXERCISED_AND_TRACE_CHANGED",
    "STAGE_EXERCISED_NO_REGISTERED_EFFECT",
    "NOT_EXERCISED",
    "OPERATIONALLY_ALIASED_UNDER_SCOPE",
    "NOT_IDENTIFIABLE_UNDER_FIXTURE_SET",
    "NON_FALSIFIABLE_ESCAPE_USED",
}

RUN_STATUSES = {
    "CONFORMS_WITHIN_REGISTERED_SCOPE",
    "DOES_NOT_CONFORM",
    "PARTIALLY_EVALUABLE",
}

PREDICATE_ARITY = {
    "SCALAR_RELATION": (2, 2, {"EQUAL", "NOT_EQUAL"}),
    "DIGEST_RELATION": (2, 2, {"EQUAL", "NOT_EQUAL"}),
    "TRACE_STATUS": (1, 16, {"ALL_COMPLETED", "ALL_REJECTED"}),
    "ALL_VALUES_DISTINCT": (2, 16, {"ALL_DISTINCT"}),
    "ORDINAL_RELATION": (2, 2, {"GREATER_THAN"}),
}

ASSERTION_IDS = {
    "A-T0-EQUAL-SURFACE-AT-K",
    "A-T3-EQUAL-SURFACE-AT-K",
    "A-T0-NO-FUTURE-DIVERGENCE",
    "A-T3-FUTURE-DIVERGENCE",
    "A-P1-ROLE-SURFACE-DISSOCIATION",
    "A-ROLE-NO-REVISION-FEEDBACK",
    "A-EXTERNAL-EVIDENCE-IMMUTABLE",
    "A-EVIDENCE-ASSESSMENT-IMMUTABLE",
    "A-SUBJECTIVE-PATH-DIFFERENT",
    "A-SAME-ACCESS-REJECTED",
    "A-LIFECYCLE-STATES-DISTINCT",
    "A-RETENTION-LATER-ACCESS",
    "A-CLOSED-WORLD-ESCAPES-REJECTED",
    "A-T0-GATE-IGNORED",
    "A-T1-GATE-CURRENT-DIFFERENCE",
    "A-T1-NO-LATER-CARRY",
    "A-T2-LIMIT-DISSOCIATION",
    "A-T3-COUNT-INVARIANT",
    "A-H0-H1-HET-A-EQUIVALENT",
    "A-H1-PROFILES-DISTINCT",
}

FORBIDDEN_FIXTURE_KEYS = {
    "expected_relation", "expected_signature", "assertion_id", "predicate",
    "violation_interpretation_code", "pass_fail_label",
}


class D2A0Exec0ContractError(ValueError):
    """Raised when the executable-closure freeze is malformed or over-authorized."""


def _fail(message: str) -> None:
    raise D2A0Exec0ContractError(message)


def _ids(rows: list[dict[str, Any]], key: str) -> list[str]:
    values = [row[key] for row in rows]
    if len(values) != len(set(values)):
        _fail(f"duplicate {key}")
    return values


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _walk_keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _walk_keys(child)}
    return set()


def _validate_envelopes(bundle: Mapping[str, Any]) -> None:
    schema = bundle["contract_schema"]
    for kind in DOCUMENT_FILES:
        try:
            validate_json_schema(bundle[kind], schema)
        except FrozenD1ExecutionError as error:
            raise D2A0Exec0ContractError(
                f"{kind} schema violation: {error}"
            ) from error
        if bundle[kind]["document_kind"] != kind:
            _fail(f"document kind mismatch: {kind}")


def _validate_predecessor() -> None:
    path = D2A0_DIR / "frozen-artifact-manifest-v0.json"
    if file_sha256(path) != PREDECESSOR_MANIFEST_SHA256:
        _fail("PR #19 predecessor manifest bytes changed")
    verify_predecessor_contract(ROOT)


def _validate_operators(bundle: Mapping[str, Any]) -> None:
    payload = bundle["operator_catalog"]["payload"]
    operators = payload["operators"]
    if tuple(_ids(operators, "operator_id")) != OPERATOR_IDS:
        _fail("operator catalog or order changed")
    if payload["randomness_policy"] != "FORBIDDEN":
        _fail("operator randomness is forbidden")
    by_id = {row["operator_id"]: row for row in operators}
    expected_owner = {
        "D2A-H-BIND": "H",
        "D2A-RECEPTION-BIAS": "COMMON",
        "D2A-T0-CURRENT": "T",
        "D2A-T1-GATE": "T",
        "D2A-T2-ACCUMULATE": "T",
        "D2A-T3-REVISE": "T",
        "D2A-P0-DIRECT": "P",
        "D2A-P1-ROLE": "P",
    }
    for operator_id, owner in expected_owner.items():
        if by_id[operator_id]["axis_owner"] != owner:
            _fail(f"operator axis ownership changed: {operator_id}")
    for operator_id in ("D2A-T0-CURRENT", "D2A-T1-GATE", "D2A-T2-ACCUMULATE", "D2A-T3-REVISE"):
        operator = by_id[operator_id]
        if "role" not in operator["forbidden_reads"]:
            _fail(f"temporal operator may read role: {operator_id}")
        if "surface_code" not in operator["forbidden_writes"]:
            _fail(f"temporal operator may write surface: {operator_id}")
    for operator_id in ("D2A-P0-DIRECT", "D2A-P1-ROLE"):
        operator = by_id[operator_id]
        if "revision_decision" not in operator["forbidden_writes"]:
            _fail(f"projection operator gained revision authority: {operator_id}")
    if set(payload["record_payload_contract"]) != {
        "DeclaredRuntimeViewReceipt", "ReceptionCandidate",
        "SubjectiveEncounterFormCandidate", "InterpretationCandidateSet",
        "ScopedAdjudicationReceipt", "ImmediateSurfaceProjectionCandidate",
        "RevisionCandidateOccurrence", "RevisionEligibilityDecisionReceipt",
        "RevisionReadReceipt", "AccessLocalApplicationReceipt",
        "RetentionObservationReceipt",
    }:
        _fail("record payload contract changed")


def _validate_golden_vectors(bundle: Mapping[str, Any]) -> None:
    payload = bundle["operator_golden_vectors"]["payload"]
    if payload["visibility"] != "CONTRACT_TEST_ONLY_NOT_RUNNER_INPUT":
        _fail("operator golden vectors became runner-visible")
    vectors = payload["vectors"]
    if set(_ids(vectors, "vector_id")) != GOLDEN_VECTOR_IDS:
        _fail("operator golden vector coverage changed")
    counts = Counter(row["operator_id"] for row in vectors)
    if set(counts) != set(OPERATOR_IDS):
        _fail("every operator requires a golden vector")
    by_id = {row["vector_id"]: row for row in vectors}
    if by_id["GV-T1-MASK"]["expected"]["adjudicated_path"] != "PATH-AMBIGUOUS":
        _fail("T1 masked golden semantics changed")
    if by_id["GV-T2-BELOW"]["expected"]["revision_decision"] != "NOT_ELIGIBLE":
        _fail("T2 below-limit golden semantics changed")
    if by_id["GV-T2-LIMIT"]["expected"]["effective_from_ordinal"] != 3:
        _fail("T2 future-effective golden semantics changed")
    if by_id["GV-T3-PRIOR"]["expected"]["adjudicated_path"] != "PATH-ADVERSE":
        _fail("T3 applied-revision golden semantics changed")
    if by_id["GV-P1-PUBLIC-A"]["expected"]["surface_code"] != "SURFACE-NEUTRAL":
        _fail("P1 public projection golden semantics changed")


def _fixture_arm_index(bundle: Mapping[str, Any]) -> dict[str, set[str]]:
    predecessor = bundle["predecessor_fixture_catalog"]["fixtures"]
    extension = bundle["fixture_extension"]["payload"]["fixtures"]
    if set(_ids(extension, "fixture_id")) != EXTENSION_FIXTURE_IDS:
        _fail("T1/T2/H1 fixture extension changed")
    if _walk_keys(bundle["fixture_extension"]) & FORBIDDEN_FIXTURE_KEYS:
        _fail("fixture extension leaks evaluator-only content")
    index: dict[str, set[str]] = {}
    for row in [*predecessor, *extension]:
        arm_ids = _ids(row["arms"], "arm_id")
        index[row["fixture_id"]] = set(arm_ids)
    return index


def _validate_units(bundle: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    payload = bundle["execution_unit_manifest"]["payload"]
    units = payload["execution_units"]
    expected_ids = tuple(f"U{index:03d}" for index in range(1, 47))
    if tuple(_ids(units, "execution_unit_id")) != expected_ids:
        _fail("explicit execution unit inventory or order changed")
    if [row["trace_id"] for row in units] != [f"TRACE-{value}" for value in expected_ids]:
        _fail("trace identity is not a deterministic unit function")
    fixture_arms = _fixture_arm_index(bundle)
    cells = {
        row["cell_id"]: row
        for row in bundle["predecessor_strategy_catalog"]["registered_cells"]
    }
    for row in units:
        fixture_id = row["fixture_id"]
        if fixture_id not in fixture_arms or row["arm_id"] not in fixture_arms[fixture_id]:
            _fail(f"execution unit references unknown fixture arm: {row['execution_unit_id']}")
        expected_source = "EXEC0" if fixture_id in EXTENSION_FIXTURE_IDS else "PREDECESSOR"
        if row["fixture_source"] != expected_source:
            _fail(f"fixture source mismatch: {row['execution_unit_id']}")
        cell = cells.get(row["cell_id"])
        if cell is None or row["profile_id"] not in cell["profile_ids"]:
            _fail(f"execution unit references invalid cell/profile: {row['execution_unit_id']}")
    expected_counts = {
        "FX-EQUAL-SURFACE-DIFFERENT-PATH": 4,
        "FX-ROLE-PROJECTION-ONLY": 4,
        "FX-EVIDENCE-SUBJECTIVE-PATH": 8,
        "FX-SAME-ACCESS-REJECTION": 2,
        "FX-REVISION-LIFECYCLE-SEPARATION": 8,
        "FX-NON-FALSIFIABLE-ESCAPE": 8,
        "FX-TRANSIENT-GATE": 4,
        "FX-BOUNDED-ACCUMULATION": 4,
        "FX-DECLARED-PROFILE-DISSOCIATION": 4,
    }
    if Counter(row["fixture_id"] for row in units) != Counter(expected_counts):
        _fail("execution unit fixture coverage changed")
    forbidden = set(payload["runner_forbidden_inputs"])
    if not {"operator_golden_vectors", "evaluator_policy", "evaluation_manifest"} <= forbidden:
        _fail("runner forbidden-input lane weakened")
    if forbidden & set(payload["runner_visible_inputs"]):
        _fail("runner visibility lanes overlap")
    return {row["execution_unit_id"]: row for row in units}


def _validate_lifecycle(bundle: Mapping[str, Any]) -> None:
    payload = bundle["lifecycle_processor"]["payload"]
    if tuple(payload["dependency_order"]) != LIFECYCLE_ORDER:
        _fail("lifecycle dependency order changed")
    if tuple(_ids(payload["steps"], "step_id")) != LIFECYCLE_STEPS:
        _fail("lifecycle processor steps changed")
    if set(payload["typed_rejection_codes"]) != REJECTION_CODES:
        _fail("typed rejection vocabulary changed")
    if payload["terminal_semantics"]["typed_policy_rejection"] != "TERMINATE_UNIT_AND_CONTINUE_RUN":
        _fail("typed rejection no longer continues the run")
    if payload["terminal_semantics"]["malformed_contract_or_digest"] != "ABORT_WHOLE_RUN":
        _fail("malformed contract must abort the whole run")


def _validate_trace_and_run_schemas(bundle: Mapping[str, Any]) -> None:
    trace = bundle["trace_schema"]
    refs = [branch["$ref"] for branch in trace["oneOf"]]
    if refs != ["#/$defs/completedTrace", "#/$defs/rejectedTrace"]:
        _fail("trace terminal union changed")
    completed = trace["$defs"]["completedTrace"]
    rejected = trace["$defs"]["rejectedTrace"]
    if "rejection_receipt" in completed["properties"]:
        _fail("completed trace may not carry a rejection receipt")
    if "rejection_receipt" not in rejected["required"]:
        _fail("rejected trace requires a typed rejection receipt")
    codes = set(trace["$defs"]["rejectionReceipt"]["properties"]["rejection_code"]["enum"])
    if codes != REJECTION_CODES:
        _fail("trace rejection codes differ from lifecycle policy")
    run = bundle["run_schema"]
    if run["properties"]["traces"]["minItems"] != 46 or run["properties"]["traces"]["maxItems"] != 46:
        _fail("run schema no longer binds 46 explicit units")
    if run["properties"]["summary"]["properties"]["aborted_unit_count"]["const"] != 0:
        _fail("committed run may not contain an aborted unit")


def _validate_evaluation(bundle: Mapping[str, Any], units: dict[str, dict[str, Any]]) -> None:
    policy = bundle["evaluator_policy"]["payload"]
    if set(policy["assertion_evaluation_statuses"]) != ASSERTION_STATUSES:
        _fail("assertion status and interpretation code separation changed")
    if set(policy["interpretation_codes"]) != INTERPRETATION_CODES:
        _fail("interpretation code vocabulary changed")
    if set(policy["run_evaluation_statuses"]) != RUN_STATUSES:
        _fail("run evaluation status vocabulary changed")
    if policy["evaluator_role"] != "SEPARATE_POST_RUN_EVALUATOR":
        _fail("evaluator role overclaims independence or lost separation")
    predicates = {row["predicate_id"]: row for row in policy["predicates"]}
    if set(predicates) != set(PREDICATE_ARITY):
        _fail("evaluator predicate catalog changed")
    for predicate_id, (minimum, maximum, relations) in PREDICATE_ARITY.items():
        row = predicates[predicate_id]
        if (row["minimum_arity"], row["maximum_arity"], set(row["relations"])) != (
            minimum, maximum, relations
        ):
            _fail(f"evaluator predicate semantics changed: {predicate_id}")

    assertions = bundle["evaluation_manifest"]["payload"]["assertions"]
    if set(_ids(assertions, "assertion_id")) != ASSERTION_IDS:
        _fail("typed evaluation assertion inventory changed")
    fixture_ids: set[str] = set()
    payload_contract = bundle["operator_catalog"]["payload"]["record_payload_contract"]
    for assertion in assertions:
        fixture_ids.add(assertion["fixture_id"])
        predicate_id = assertion["predicate"]
        if predicate_id not in PREDICATE_ARITY:
            _fail("assertion references unknown predicate")
        minimum, maximum, relations = PREDICATE_ARITY[predicate_id]
        operands = assertion["operands"]
        if not minimum <= len(operands) <= maximum:
            _fail(f"assertion predicate arity mismatch: {assertion['assertion_id']}")
        if assertion["expected_relation"] not in relations:
            _fail(f"assertion relation mismatch: {assertion['assertion_id']}")
        if assertion["violation_interpretation_code"] not in INTERPRETATION_CODES - {"NONE"}:
            _fail("assertion uses invalid violation interpretation code")
        for selector in operands:
            if selector.get("cardinality") != "EXACTLY_ONE":
                _fail("selector cardinality must be EXACTLY_ONE")
            unit = units.get(selector.get("execution_unit_id"))
            if unit is None:
                _fail("selector references unknown execution unit")
            if unit["fixture_id"] != assertion["fixture_id"]:
                _fail("selector crosses assertion fixture")
            source_kind = selector.get("source_kind")
            pointer = selector.get("json_pointer")
            if source_kind == "TRACE":
                if set(selector) != {"execution_unit_id", "source_kind", "json_pointer", "cardinality"}:
                    _fail("trace selector has undeclared fields")
                if pointer != "/status":
                    _fail("trace selector may only read terminal status")
            elif source_kind == "RECORD":
                if set(selector) != {
                    "execution_unit_id", "source_kind", "type_id", "access_ordinal",
                    "json_pointer", "cardinality"
                }:
                    _fail("record selector shape changed")
                type_id = selector["type_id"]
                if type_id not in payload_contract:
                    _fail("selector references unknown record type")
                if pointer.startswith("/payload/"):
                    field = pointer.removeprefix("/payload/")
                    if field not in payload_contract[type_id]:
                        _fail(f"selector points outside record payload contract: {pointer}")
                elif pointer not in {"/payload_digest", "/access_ordinal"}:
                    _fail(f"selector pointer is not registered: {pointer}")
            else:
                _fail("selector source kind is invalid")
    if fixture_ids != set(_fixture_arm_index(bundle)):
        _fail("evaluation does not cover every predecessor and extension fixture")


def _validate_frozen_bindings(bundle: Mapping[str, Any]) -> None:
    if file_sha256(EXEC0_DIR / "frozen-artifact-manifest-v0.json") != (
        EXEC0_FROZEN_MANIFEST_SHA256
    ):
        _fail("EXEC0 frozen artifact manifest digest mismatch")
    rows = bundle["frozen_artifact_manifest"]["payload"]["artifacts"]
    bindings = {row["document_kind"]: row for row in rows}
    if set(bindings) != set(FROZEN_FILES):
        _fail("EXEC0 frozen artifact inventory changed")
    for kind, (filename, lane) in FROZEN_FILES.items():
        row = bindings[kind]
        if row["path"] != filename or row["visibility_lane"] != lane:
            _fail(f"artifact lane changed: {kind}")
        if file_sha256(EXEC0_DIR / filename) != row["sha256"]:
            _fail(f"EXEC0 artifact digest mismatch: {filename}")
    runner_visible = {
        kind for kind, (_, lane) in FROZEN_FILES.items() if lane == "RUNNER_VISIBLE"
    }
    if {"operator_golden_vectors", "evaluator_policy", "evaluation_manifest"} & runner_visible:
        _fail("evaluator or golden artifacts became runner-visible")


def validate_contract_bundle(bundle: Mapping[str, Any], *, verify_files: bool = False) -> dict[str, int]:
    _validate_envelopes(bundle)
    _validate_operators(bundle)
    _validate_golden_vectors(bundle)
    units = _validate_units(bundle)
    _validate_lifecycle(bundle)
    _validate_trace_and_run_schemas(bundle)
    _validate_evaluation(bundle, units)
    if verify_files:
        _validate_predecessor()
        _validate_frozen_bindings(bundle)
    return {
        "operator_count": len(bundle["operator_catalog"]["payload"]["operators"]),
        "golden_vector_count": len(bundle["operator_golden_vectors"]["payload"]["vectors"]),
        "extension_fixture_count": len(bundle["fixture_extension"]["payload"]["fixtures"]),
        "execution_unit_count": len(units),
        "assertion_count": len(bundle["evaluation_manifest"]["payload"]["assertions"]),
        "frozen_artifact_count": len(bundle["frozen_artifact_manifest"]["payload"]["artifacts"]),
    }


def load_contract_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    root = Path(repository_root)
    d2a0 = root / "research/scenarios/interp-dialogue-001/d2a0"
    exec0 = d2a0 / "exec0"
    bundle: dict[str, Any] = {
        "contract_schema": load_exact(exec0 / "contract.schema.json"),
        "trace_schema": load_exact(exec0 / "trace-v1.schema.json"),
        "run_schema": load_exact(exec0 / "run-v1.schema.json"),
        "predecessor_fixture_catalog": load_exact(d2a0 / "fixture-catalog-v0.json"),
        "predecessor_strategy_catalog": load_exact(d2a0 / "strategy-catalog-v0.json"),
    }
    for kind, filename in DOCUMENT_FILES.items():
        bundle[kind] = load_exact(exec0 / filename)
    return bundle


def verify_frozen_contract(repository_root: str | Path = ROOT) -> dict[str, int]:
    bundle = load_contract_bundle(repository_root)
    return validate_contract_bundle(bundle, verify_files=True)


def mutated_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    return deepcopy(load_contract_bundle(repository_root))
