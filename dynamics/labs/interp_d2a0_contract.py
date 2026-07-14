from __future__ import annotations

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


ROOT = Path(__file__).resolve().parents[2]
D2A0_RELATIVE = Path("research/scenarios/interp-dialogue-001/d2a0")
EXPECTED_FROZEN_MANIFEST_SHA256 = (
    "8ee62993fbf302d8037f8cf898a0edca4fe7bbff7b01f73f6a71e8b6c04c3efd"
)

DOCUMENT_FILES = {
    "runtime_spine": "runtime-spine-v0.json",
    "strategy_catalog": "strategy-catalog-v0.json",
    "fixture_catalog": "fixture-catalog-v0.json",
    "execution_manifest": "execution-manifest-v0.json",
    "evaluation_manifest": "evaluation-manifest-v0.json",
    "policy": "policy-v0.json",
    "frozen_artifact_manifest": "frozen-artifact-manifest-v0.json",
}

FROZEN_FILES = {
    "contract_schema": "contract.schema.json",
    "runtime_spine": "runtime-spine-v0.json",
    "strategy_catalog": "strategy-catalog-v0.json",
    "fixture_catalog": "fixture-catalog-v0.json",
    "policy": "policy-v0.json",
    "trace_schema": "trace.schema.json",
    "execution_manifest": "execution-manifest-v0.json",
    "evaluation_manifest": "evaluation-manifest-v0.json",
}

TYPE_IDS = (
    "ExternalOccurrence",
    "CurrentAccessOccurrence",
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

STAGE_IDS = (
    "MATERIALIZE_DECLARED_VIEW",
    "FORM_RECEPTION_CANDIDATE",
    "FORM_SUBJECTIVE_ENCOUNTER",
    "EMIT_INTERPRETATION_CANDIDATES",
    "ADJUDICATE_SCOPED_CANDIDATES",
    "PROJECT_IMMEDIATE_SURFACE",
    "DECIDE_REVISION_ELIGIBILITY",
)

RUNTIME_VIEW_FIELDS = {
    "current_access_occurrence",
    "evidence_assessment_digest",
    "external_evidence_link_set_digest",
    "interpretation_scope_id",
    "prior_eligible_revision_receipts",
    "runtime_id",
    "target_scope_id",
}

REVISION_STATUSES = {
    "ELIGIBLE_FROM_FUTURE_ACCESS",
    "NOT_EMITTED",
    "NOT_ELIGIBLE",
    "REJECTED_BY_POLICY",
    "NOT_APPLICABLE_TO_MODEL",
}

LIFECYCLE_TYPES = (
    "RevisionCandidateOccurrence",
    "ScopedAdjudicationReceipt",
    "RevisionEligibilityDecisionReceipt",
    "RevisionReadReceipt",
    "AccessLocalApplicationReceipt",
    "RetentionObservationReceipt",
)

TEMPORAL_STRATEGIES = {"D2A-T0", "D2A-T1", "D2A-T2", "D2A-T3"}
PROJECTION_STRATEGIES = {"D2A-P0", "D2A-P1"}
HETEROGENEITY_STRATEGIES = {"D2A-H0", "D2A-H1"}
PROFILE_IDS = {"HET-A", "HET-B", "HET-C"}

FIXTURE_IDS = {
    "FX-EQUAL-SURFACE-DIFFERENT-PATH",
    "FX-ROLE-PROJECTION-ONLY",
    "FX-EVIDENCE-SUBJECTIVE-PATH",
    "FX-SAME-ACCESS-REJECTION",
    "FX-REVISION-LIFECYCLE-SEPARATION",
    "FX-NON-FALSIFIABLE-ESCAPE",
}

RETIREMENT_VOCABULARY = {
    "STAGE_EXERCISED_AND_TRACE_CHANGED",
    "STAGE_EXERCISED_NO_REGISTERED_EFFECT",
    "NOT_EXERCISED",
    "OPERATIONALLY_ALIASED_UNDER_SCOPE",
    "NOT_IDENTIFIABLE_UNDER_FIXTURE_SET",
    "AUTHORITY_FAILURE",
    "HARD_INVARIANT_FAILURE",
    "NON_FALSIFIABLE_ESCAPE_USED",
}

FORBIDDEN_STAGE_WRITES = {"Evidence", "HumanState", "Narrative", "Episode", "TargetForm"}
FORBIDDEN_FIXTURE_KEYS = {
    "assertion_id",
    "expected_relation",
    "expected_signature",
    "failure_status",
    "pass_fail_label",
    "predicate",
    "retirement_decision",
}
FORBIDDEN_RANDOM_KEYS = {"prng", "random_seed", "sampling_distribution", "seed"}


class D2A0ContractError(ValueError):
    """Raised when the frozen D2a0 contract is malformed or over-authorized."""


def _fail(message: str) -> None:
    raise D2A0ContractError(message)


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


def _field_map(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [row["field"] for row in rows]
    if len(fields) != len(set(fields)):
        _fail("duplicate assignment field")
    return {row["field"]: row["value"] for row in rows}


def _fixture_map(bundle: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = bundle["fixture_catalog"]["fixtures"]
    _ids(rows, "fixture_id")
    return {row["fixture_id"]: row for row in rows}


def _validate_json_documents(bundle: Mapping[str, Any]) -> None:
    schema = bundle["contract_schema"]
    for kind in DOCUMENT_FILES:
        try:
            validate_json_schema(bundle[kind], schema)
        except FrozenD1ExecutionError as error:
            raise D2A0ContractError(f"{kind} schema violation: {error}") from error


def _validate_runtime_spine(runtime: dict[str, Any]) -> None:
    if tuple(_ids(runtime["type_catalog"], "type_id")) != TYPE_IDS:
        _fail("runtime type catalog or order changed")
    if tuple(_ids(runtime["stages"], "stage_id")) != STAGE_IDS:
        _fail("runtime stage catalog or order changed")
    if set(runtime["runtime_view"]["allowed_fields"]) != RUNTIME_VIEW_FIELDS:
        _fail("declared runtime view field allowlist changed")
    if runtime["runtime_view"]["human_state_read_policy"] != "NO_WHOLE_STATE_READ":
        _fail("whole HumanState reads are forbidden")
    for stage in runtime["stages"]:
        if not FORBIDDEN_STAGE_WRITES <= set(stage["must_not_write"]):
            _fail(f"stage write boundary weakened: {stage['stage_id']}")
        if set(stage["may_write"]) != {"detached_trace"}:
            _fail(f"stage may write outside detached trace: {stage['stage_id']}")
    lifecycle = runtime["revision_lifecycle"]
    if set(lifecycle["decision_statuses"]) != REVISION_STATUSES:
        _fail("revision decision vocabulary changed")
    if tuple(lifecycle["ordered_types"]) != LIFECYCLE_TYPES:
        _fail("revision lifecycle collapsed or reordered")
    invariant_ids = set(_ids(runtime["temporal_invariants"], "invariant_id"))
    expected_invariants = {
        "SAME_RUNTIME",
        "SAME_TARGET_SCOPE",
        "SAME_INTERPRETATION_SCOPE",
        "FUTURE_ACCESS_ONLY",
        "EFFECTIVE_BEFORE_READ",
        "NO_SAME_ACCESS_FEEDBACK",
    }
    if invariant_ids != expected_invariants:
        _fail("temporal lineage invariants changed")


def _validate_strategies(catalog: dict[str, Any]) -> None:
    if _walk_keys(catalog) & FORBIDDEN_RANDOM_KEYS:
        _fail("random sampling contract is forbidden")
    temporal = {row["strategy_id"]: row for row in catalog["temporal_strategies"]}
    projection = {row["strategy_id"]: row for row in catalog["projection_strategies"]}
    heterogeneity = {row["strategy_id"]: row for row in catalog["heterogeneity_strategies"]}
    if set(temporal) != TEMPORAL_STRATEGIES:
        _fail("temporal strategy axis changed")
    if set(projection) != PROJECTION_STRATEGIES:
        _fail("projection strategy axis changed")
    if set(heterogeneity) != HETEROGENEITY_STRATEGIES:
        _fail("heterogeneity strategy axis changed")
    for strategy_id in ("D2A-T0", "D2A-T1"):
        if "ELIGIBLE_FROM_FUTURE_ACCESS" in temporal[strategy_id]["revision_decisions"]:
            _fail(f"{strategy_id} may not emit a future revision")
    for strategy_id in ("D2A-T2", "D2A-T3"):
        if "ELIGIBLE_FROM_FUTURE_ACCESS" not in temporal[strategy_id]["revision_decisions"]:
            _fail(f"{strategy_id} lost future-revision expressivity")
    for row in [*projection.values(), *heterogeneity.values()]:
        if row["revision_decisions"] != ["NOT_APPLICABLE_TO_MODEL"]:
            _fail("non-temporal strategy gained revision authority")
    profiles = {row["profile_id"]: row for row in catalog["declared_profiles"]}
    if set(profiles) != PROFILE_IDS:
        _fail("declared heterogeneity profiles changed")
    cells = catalog["registered_cells"]
    _ids(cells, "cell_id")
    for cell in cells:
        if cell["temporal_strategy"] not in temporal:
            _fail("cell references unknown temporal strategy")
        if cell["projection_strategy"] not in projection:
            _fail("cell references unknown projection strategy")
        if cell["heterogeneity_strategy"] not in heterogeneity:
            _fail("cell references unknown heterogeneity strategy")
        expected_id = "-".join(
            (
                cell["temporal_strategy"].split("-")[-1],
                cell["projection_strategy"].split("-")[-1],
                cell["heterogeneity_strategy"].split("-")[-1],
            )
        )
        if cell["cell_id"] != expected_id:
            _fail(f"cell id does not encode its axes: {cell['cell_id']}")
        expected_profiles = {"HET-A"} if cell["heterogeneity_strategy"] == "D2A-H0" else PROFILE_IDS
        if set(cell["profile_ids"]) != expected_profiles:
            _fail(f"cell has invalid explicit profiles: {cell['cell_id']}")


def _validate_fixture_lineage(fixture: dict[str, Any]) -> None:
    lineage = fixture["access_lineage"]
    _ids(lineage, "access_id")
    ordinals = [row["access_ordinal"] for row in lineage]
    if ordinals != sorted(set(ordinals)):
        _fail(f"fixture lineage is not strictly ordered: {fixture['fixture_id']}")
    for field in ("runtime_id", "target_scope_id", "interpretation_scope_id"):
        if len({row[field] for row in lineage}) != 1:
            _fail(f"fixture crosses {field}: {fixture['fixture_id']}")
    _ids(fixture["arms"], "arm_id")
    _field_map(fixture["clamped_fields"])
    for arm in fixture["arms"]:
        _field_map(arm["assignments"])


def _validate_fixtures(catalog: dict[str, Any]) -> None:
    if _walk_keys(catalog) & FORBIDDEN_FIXTURE_KEYS:
        _fail("fixture catalog leaks evaluator-only content")
    fixtures = {row["fixture_id"]: row for row in catalog["fixtures"]}
    if set(fixtures) != FIXTURE_IDS:
        _fail("fixture catalog changed")
    for fixture in fixtures.values():
        _validate_fixture_lineage(fixture)

    role = _field_map(fixtures["FX-ROLE-PROJECTION-ONLY"]["clamped_fields"])
    expected_role_clamps = {
        "role_scope": "SURFACE_PROJECTION_ONLY",
        "action_feedback": "CLAMPED_ABSENT",
        "self_observation_feedback": "CLAMPED_ABSENT",
        "world_outcome": "CLAMPED_ABSENT",
    }
    for field, value in expected_role_clamps.items():
        if role.get(field) != value:
            _fail(f"role fixture missing clamp: {field}")

    evidence = _field_map(fixtures["FX-EVIDENCE-SUBJECTIVE-PATH"]["clamped_fields"])
    expected_evidence_clamps = {
        "public_information_policy": "NO_NEW_PUBLIC_INFORMATION",
        "reassessment_policy": "NO_REASSESSMENT_POLICY",
        "evidence_writer_authority": "NO_EVIDENCE_WRITER_AUTHORITY",
    }
    for field, value in expected_evidence_clamps.items():
        if evidence.get(field) != value:
            _fail(f"evidence fixture missing clamp: {field}")

    same_k = fixtures["FX-SAME-ACCESS-REJECTION"]
    same_k_clamps = _field_map(same_k["clamped_fields"])
    same_k_arm = _field_map(same_k["arms"][0]["assignments"])
    if same_k_clamps.get("revision_source_access_ordinal") != 1:
        _fail("same-access fixture source ordinal changed")
    if same_k_clamps.get("revision_effective_from_ordinal") != 2:
        _fail("same-access fixture effective ordinal changed")
    if same_k_arm.get("revision_read_access_ordinal") != 1:
        _fail("same-access fixture no longer attempts a same-k read")

    lifecycle_arm_ids = set(
        _ids(fixtures["FX-REVISION-LIFECYCLE-SEPARATION"]["arms"], "arm_id")
    )
    if lifecycle_arm_ids != {
        "ELIGIBLE-NOT-READ",
        "READ-NOT-APPLIED",
        "APPLIED-NOT-RETAINED",
        "RETAINED-AT-LATER-ACCESS",
    }:
        _fail("revision lifecycle fixture collapsed states")


def _validate_policy(policy: dict[str, Any]) -> None:
    if set(policy["retirement_vocabulary"]) != RETIREMENT_VOCABULARY:
        _fail("retirement vocabulary changed or overclaims necessity")
    if "STAGE_UNNECESSARY" in policy["retirement_vocabulary"]:
        _fail("fixture-local result may not retire a stage globally")


def _validate_execution_and_evaluation(bundle: Mapping[str, Any]) -> None:
    execution = bundle["execution_manifest"]
    evaluation = bundle["evaluation_manifest"]
    strategies = bundle["strategy_catalog"]
    fixtures = _fixture_map(bundle)
    cells = {row["cell_id"] for row in strategies["registered_cells"]}
    if set(execution["registered_cells"]) != cells:
        _fail("execution manifest cell set differs from strategy catalog")
    if set(execution["registered_fixtures"]) != set(fixtures):
        _fail("execution manifest fixture set differs from fixture catalog")
    isolation = execution["runner_isolation"]
    if "evaluation_manifest" in isolation["permitted_input_kinds"]:
        _fail("runner may not receive the evaluation manifest")
    if "--evaluation" not in isolation["forbidden_argument_names"]:
        _fail("runner CLI does not forbid evaluation input")
    required_forbidden_outputs = {
        "evaluation_manifest_sha256",
        "expected_relation",
        "expected_signature",
        "pass_fail_label",
        "retirement_decision",
    }
    if not required_forbidden_outputs <= set(isolation["forbidden_output_fields"]):
        _fail("runner output boundary lost evaluator-only fields")
    if _walk_keys(execution) & FORBIDDEN_FIXTURE_KEYS:
        _fail("execution manifest contains evaluator-only fields")
    assertions = evaluation["assertions"]
    _ids(assertions, "assertion_id")
    if {row["fixture_id"] for row in assertions} != set(fixtures):
        _fail("evaluation manifest does not cover every fixture")
    for assertion in assertions:
        if assertion["failure_status"] not in RETIREMENT_VOCABULARY:
            _fail("evaluation assertion uses undeclared failure status")
        if not set(assertion["applies_to"]) <= (
            TEMPORAL_STRATEGIES | PROJECTION_STRATEGIES | HETEROGENEITY_STRATEGIES | cells
        ):
            _fail("evaluation assertion references unknown strategy or cell")
    if set(evaluation["required_input_digests"]) != {
        "execution_manifest_sha256",
        "run_artifact_sha256",
        "evaluation_manifest_sha256",
    }:
        _fail("evaluation receipt does not bind all three artifacts")


def _validate_trace_schema(trace_schema: dict[str, Any]) -> None:
    required = set(trace_schema["required"])
    if required != {
        "trace_id",
        "contract_id",
        "execution_manifest_sha256",
        "cell_id",
        "fixture_id",
        "arm_id",
        "status",
        "records",
    }:
        _fail("trace envelope changed")
    properties = set(trace_schema["properties"])
    if "evaluation_manifest_sha256" in properties or "expected_signature" in properties:
        _fail("trace schema leaks evaluator-only content")
    record_branches = trace_schema["$defs"]["record"]["oneOf"]
    if len(record_branches) != 6:
        _fail("trace lifecycle record branches changed")


def _validate_bindings(bundle: Mapping[str, Any], artifact_dir: Path) -> None:
    if file_sha256(artifact_dir / "frozen-artifact-manifest-v0.json") != (
        EXPECTED_FROZEN_MANIFEST_SHA256
    ):
        _fail("frozen artifact manifest digest mismatch")
    execution_rows = bundle["execution_manifest"]["artifact_bindings"]
    execution_bindings = {row["document_kind"]: row for row in execution_rows}
    expected_execution = {
        key: value
        for key, value in FROZEN_FILES.items()
        if key in {"contract_schema", "runtime_spine", "strategy_catalog", "fixture_catalog", "policy", "trace_schema"}
    }
    if {key: row["path"] for key, row in execution_bindings.items()} != expected_execution:
        _fail("execution artifact bindings changed")
    frozen_rows = bundle["frozen_artifact_manifest"]["artifacts"]
    frozen_bindings = {row["document_kind"]: row for row in frozen_rows}
    if {key: row["path"] for key, row in frozen_bindings.items()} != FROZEN_FILES:
        _fail("frozen artifact manifest inventory changed")
    for bindings in (execution_bindings, frozen_bindings):
        for row in bindings.values():
            path = artifact_dir / row["path"]
            if not path.is_file():
                _fail(f"bound artifact is missing: {row['path']}")
            actual = file_sha256(path)
            if actual != row["sha256"]:
                _fail(f"bound artifact digest mismatch: {row['path']}")


def validate_contract_bundle(
    bundle: Mapping[str, Any], *, artifact_dir: Path | None = None
) -> dict[str, int]:
    """Validate schema, authority, strategy, fixture and isolation contracts."""

    _validate_json_documents(bundle)
    _validate_runtime_spine(bundle["runtime_spine"])
    _validate_strategies(bundle["strategy_catalog"])
    _validate_fixtures(bundle["fixture_catalog"])
    _validate_policy(bundle["policy"])
    _validate_execution_and_evaluation(bundle)
    _validate_trace_schema(bundle["trace_schema"])
    if artifact_dir is not None:
        _validate_bindings(bundle, artifact_dir)
    return {
        "type_count": len(bundle["runtime_spine"]["type_catalog"]),
        "stage_count": len(bundle["runtime_spine"]["stages"]),
        "cell_count": len(bundle["strategy_catalog"]["registered_cells"]),
        "fixture_count": len(bundle["fixture_catalog"]["fixtures"]),
        "assertion_count": len(bundle["evaluation_manifest"]["assertions"]),
        "frozen_artifact_count": len(bundle["frozen_artifact_manifest"]["artifacts"]),
    }


def load_contract_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    root = Path(repository_root)
    artifact_dir = root / D2A0_RELATIVE
    bundle: dict[str, Any] = {
        "contract_schema": load_exact(artifact_dir / "contract.schema.json"),
        "trace_schema": load_exact(artifact_dir / "trace.schema.json"),
    }
    for kind, filename in DOCUMENT_FILES.items():
        bundle[kind] = load_exact(artifact_dir / filename)
    return bundle


def verify_frozen_contract(repository_root: str | Path = ROOT) -> dict[str, int]:
    root = Path(repository_root)
    bundle = load_contract_bundle(root)
    return validate_contract_bundle(bundle, artifact_dir=root / D2A0_RELATIVE)


def mutated_bundle(repository_root: str | Path = ROOT) -> dict[str, Any]:
    """Return an isolated bundle for adversarial contract tests."""

    return deepcopy(load_contract_bundle(repository_root))


def validate_trace_document(
    trace: dict[str, Any], bundle: Mapping[str, Any]
) -> None:
    """Validate a future D2a1 trace without evaluating expected signatures."""

    try:
        validate_json_schema(trace, bundle["trace_schema"])
    except FrozenD1ExecutionError as error:
        raise D2A0ContractError(f"trace schema violation: {error}") from error
    if trace["cell_id"] not in set(bundle["execution_manifest"]["registered_cells"]):
        _fail("trace references an unregistered cell")
    fixtures = _fixture_map(bundle)
    if trace["fixture_id"] not in fixtures:
        _fail("trace references an unregistered fixture")
    fixture = fixtures[trace["fixture_id"]]
    arm_ids = {row["arm_id"] for row in fixture["arms"]}
    if trace["arm_id"] not in arm_ids:
        _fail("trace references an unregistered fixture arm")
    records: dict[str, dict[str, Any]] = {}
    for record in trace["records"]:
        record_id = record["record_id"]
        if record_id in records:
            _fail("trace contains duplicate record identity")
        missing_sources = set(record["source_record_ids"]) - set(records)
        if missing_sources:
            _fail("trace source record is missing or forward-referenced")
        if record["type_id"] == "RevisionReadReceipt":
            if record["source_access_ordinal"] >= record["access_ordinal"]:
                _fail("same-access revision read is forbidden")
            if record["effective_from_ordinal"] > record["access_ordinal"]:
                _fail("revision read occurs before effective access")
            revision = records.get(record["revision_record_id"])
            if revision is None:
                _fail("revision read does not bind an earlier revision")
            for field in ("runtime_id", "target_scope_id", "interpretation_scope_id"):
                if revision[field] != record[field]:
                    _fail(f"revision read crosses {field}")
        if record["type_id"] == "RetentionObservationReceipt":
            application = records.get(record["prior_application_record_id"])
            if application is None:
                _fail("retention observation lacks an earlier application")
            if application["access_ordinal"] >= record["access_ordinal"]:
                _fail("retention may only be observed at a later access")
        records[record_id] = record
