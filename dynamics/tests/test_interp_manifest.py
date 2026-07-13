from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import unittest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION_PATH = BENCHMARKS / "interp-001-m1-v1-execution.json"
EVALUATION_PATH = BENCHMARKS / "interp-001-m1-v1-evaluation.json"
SCHEMA_PATH = BENCHMARKS / "interp-001-manifest.schema.json"
RESULT_SCHEMA_PATH = BENCHMARKS / "interp-001-m1-v1-result.schema.json"

HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
ASCII_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]*$")
EXPECTED_PREDICATE_CATALOG_SHA256 = (
    "5aee4d567b08d251d5693ef06d62fa543603d5c3e33fdd2fae6802e1ca724634"
)
EXPECTED_EVALUATION_CATALOG_SHA256 = (
    "b3b022a32aae3fb1e7a3679b98108958359a49988f5cb99f2a09e662f264f072"
)
EXPECTED_EXECUTION_CONTRACT_SHA256 = (
    "d799c17a88ad789c2b5f43606db1838c0c345328262a4fb7baf6033e12dea4c3"
)
EXPECTED_EVALUATION_CONTRACT_SHA256 = (
    "f56cbf33ad06ac3fa769231f349521927b4c2372fe121635bc4121e9981bb528"
)


def _load(path: Path) -> dict[str, object]:
    def reject_duplicate_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _resolve_local_ref(schema: dict[str, object], ref: str) -> dict[str, object]:
    if not ref.startswith("#/"):
        raise ValueError("only local result-schema refs are allowed")
    value: object = schema
    for segment in ref[2:].split("/"):
        value = value[segment]
    if not isinstance(value, dict):
        raise ValueError("schema ref did not resolve to object")
    return value


def _validate_json_schema(
    value: object,
    schema: dict[str, object],
    *,
    root_schema: dict[str, object] | None = None,
    path: str = "$",
) -> None:
    """Validate the dependency-free Draft 2020-12 subset used by frozen schemas."""
    root_schema = root_schema or schema
    if "$ref" in schema:
        _validate_json_schema(
            value,
            _resolve_local_ref(root_schema, schema["$ref"]),
            root_schema=root_schema,
            path=path,
        )
        return
    if "oneOf" in schema:
        matches = 0
        for branch in schema["oneOf"]:
            try:
                _validate_json_schema(value, branch, root_schema=root_schema, path=path)
            except ValueError:
                continue
            matches += 1
        if matches != 1:
            raise ValueError(f"schema oneOf matched {matches} branches at {path}")
        return
    if "const" in schema and _canonical_bytes(value) != _canonical_bytes(schema["const"]):
        raise ValueError(f"schema const mismatch at {path}")
    if "enum" in schema and not any(
        _canonical_bytes(value) == _canonical_bytes(candidate) for candidate in schema["enum"]
    ):
        raise ValueError(f"schema enum mismatch at {path}")

    expected_type = schema.get("type")
    type_matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }
    if expected_type is not None and not type_matches.get(expected_type, False):
        raise ValueError(f"schema type mismatch at {path}")

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        if not required <= set(value):
            raise ValueError(f"schema required property missing at {path}")
        properties = schema.get("properties", {})
        extra_keys = set(value) - set(properties)
        additional = schema.get("additionalProperties")
        if additional is False and extra_keys:
            raise ValueError(f"schema additional property at {path}")
        if isinstance(additional, dict):
            for key in extra_keys:
                _validate_json_schema(
                    value[key],
                    additional,
                    root_schema=root_schema,
                    path=f"{path}/{key}",
                )
        for key, child in properties.items():
            if key in value:
                _validate_json_schema(
                    value[key],
                    child,
                    root_schema=root_schema,
                    path=f"{path}/{key}",
                )
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"schema minItems mismatch at {path}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValueError(f"schema maxItems mismatch at {path}")
        if schema.get("uniqueItems"):
            canonical_items = [_canonical_bytes(item) for item in value]
            if len(canonical_items) != len(set(canonical_items)):
                raise ValueError(f"schema uniqueItems mismatch at {path}")
        if "items" in schema:
            for index, item in enumerate(value):
                _validate_json_schema(
                    item,
                    schema["items"],
                    root_schema=root_schema,
                    path=f"{path}/{index}",
                )
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"schema minLength mismatch at {path}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise ValueError(f"schema pattern mismatch at {path}")
    elif isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"schema minimum mismatch at {path}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValueError(f"schema maximum mismatch at {path}")


def _schema_nodes_at_path(
    schema: dict[str, object], path: str
) -> list[dict[str, object]]:
    segments = path.split("/")[2:]

    def visit(
        node: dict[str, object], remaining: list[str]
    ) -> list[dict[str, object]]:
        if "$ref" in node:
            return visit(_resolve_local_ref(schema, node["$ref"]), remaining)
        if not remaining:
            return [node]
        if "oneOf" in node:
            return [
                resolved
                for branch in node["oneOf"]
                for resolved in visit(branch, remaining)
            ]
        segment = remaining[0]
        if node.get("type") == "array":
            return visit(node["items"], remaining[1:]) if segment == "*" else []
        if node.get("type") == "object":
            child = node.get("properties", {}).get(segment)
            return visit(child, remaining[1:]) if isinstance(child, dict) else []
        return []

    if not path.startswith("/semantic/"):
        return []
    return visit(schema["$defs"]["semantic"], segments)


def _schema_path_exists(schema: dict[str, object], path: str) -> bool:
    return bool(_schema_nodes_at_path(schema, path))


def _schema_node_types(
    schema: dict[str, object], node: dict[str, object]
) -> set[str]:
    if "$ref" in node:
        return _schema_node_types(schema, _resolve_local_ref(schema, node["$ref"]))
    if "oneOf" in node:
        return set().union(*(_schema_node_types(schema, branch) for branch in node["oneOf"]))
    if "type" in node:
        return {node["type"]}
    samples = [node["const"]] if "const" in node else node.get("enum", [])
    result: set[str] = set()
    for sample in samples:
        if isinstance(sample, bool):
            result.add("boolean")
        elif isinstance(sample, int):
            result.add("integer")
        elif isinstance(sample, str):
            result.add("string")
        elif isinstance(sample, list):
            result.add("array")
        elif isinstance(sample, dict):
            result.add("object")
    return result


def _schema_accepts_value(
    schema: dict[str, object], node: dict[str, object], value: object
) -> bool:
    try:
        _validate_json_schema(value, node, root_schema=schema)
    except ValueError:
        return False
    return True


def _walk(value: object, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _walk(item, f"{path}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, f"{path}/{index}")


def _ids(items: list[dict[str, object]], key: str) -> set[str]:
    values = [item[key] for item in items]
    if not all(isinstance(value, str) for value in values):
        raise ValueError(f"non-string {key}")
    if not all(ASCII_TOKEN.fullmatch(value) for value in values):
        raise ValueError(f"invalid token {key}")
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {key}")
    return set(values)


def _require_keys(
    value: dict[str, object],
    required: set[str],
    optional: set[str] | None = None,
    *,
    label: str,
) -> None:
    optional = optional or set()
    actual = set(value)
    if actual != required | (actual & optional):
        missing = required - actual
        unknown = actual - required - optional
        raise ValueError(f"{label} shape mismatch missing={sorted(missing)} unknown={sorted(unknown)}")


def _validate_canonical_domain(envelope: dict[str, object]) -> None:
    for path, value in _walk(envelope["manifest"]):
        if value is None:
            raise ValueError(f"null is forbidden at {path}")
        if isinstance(value, float):
            raise ValueError(f"float is forbidden at {path}")
        if isinstance(value, int) and not isinstance(value, bool):
            if not 0 <= value <= 2**53 - 1:
                raise ValueError(f"integer out of range at {path}")
        if isinstance(value, str) and value != unicodedata.normalize("NFC", value):
            raise ValueError(f"non-NFC string at {path}")
        if isinstance(value, dict):
            for key in value:
                if key != unicodedata.normalize("NFC", key) or not key.isascii():
                    raise ValueError(f"non-canonical object key at {path}/{key}")


def _validate_integrity(envelope: dict[str, object], contract_key: str) -> None:
    integrity = envelope["integrity"]
    manifest = envelope["manifest"]
    if integrity["manifest_sha256"] != _digest(manifest):
        raise ValueError("manifest digest mismatch")
    if integrity["contract_sha256"] != _digest(manifest[contract_key]):
        raise ValueError("contract digest mismatch")


def _validate_component(value: dict[str, object]) -> None:
    if not isinstance(value, dict):
        raise ValueError("component must use explicit tagged object")
    if value.get("status") == "present":
        if set(value) != {"status", "rank"}:
            raise ValueError("present component shape")
        if value["rank"] not in (0, 1, 2):
            raise ValueError("rank outside frozen ordinal domain")
    elif value.get("status") == "missing":
        if set(value) != {"status", "reason"}:
            raise ValueError("missing component shape")
        if value["reason"] not in {
            "not_applicable",
            "source_unresolved",
            "not_declared_by_fixture",
            "withheld_control",
            "operator_undefined",
        }:
            raise ValueError("unknown missing reason")
    else:
        raise ValueError("component must be tagged")


def _validate_execution(envelope: dict[str, object], *, check_integrity: bool = True) -> None:
    _require_keys(envelope, {"$schema", "manifest", "integrity"}, label="execution envelope")
    if envelope["$schema"] != "./interp-001-manifest.schema.json":
        raise ValueError("execution schema ref changed")
    if envelope["manifest"]["manifest_kind"] != "execution":
        raise ValueError("not execution manifest")
    _validate_canonical_domain(envelope)
    if check_integrity:
        _validate_integrity(envelope, "execution_contract")

    manifest = envelope["manifest"]
    contract = manifest["execution_contract"]
    _require_keys(
        manifest,
        {
            "manifest_kind",
            "schema_version",
            "manifest_id",
            "manifest_version",
            "status",
            "frozen_at",
            "implementation_base_revision",
            "governing_documents",
            "canonicalization_contract",
            "no_retuning_rule",
            "execution_contract",
        },
        label="execution manifest",
    )
    _require_keys(
        envelope["integrity"],
        {"algorithm", "canonicalization_id", "manifest_sha256", "contract_sha256"},
        label="execution integrity",
    )
    if (
        manifest["manifest_kind"],
        manifest["schema_version"],
        manifest["manifest_id"],
        manifest["manifest_version"],
        manifest["status"],
    ) != ("execution", "1.0.0", "INTERP-001A2-M1-EXECUTION", "1.0.0", "FROZEN_UNEXECUTED"):
        raise ValueError("execution manifest identity or frozen status changed")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", manifest["frozen_at"]):
        raise ValueError("invalid frozen_at")
    if envelope["integrity"]["algorithm"] != "sha256" or envelope["integrity"]["canonicalization_id"] != "interp-canonical-json-v1":
        raise ValueError("execution integrity algorithm changed")
    _require_keys(
        contract,
        {
            "scope",
            "unit_definition",
            "axis_definitions",
            "fixed_factors",
            "reception_profiles",
            "source_encounter_profiles",
            "evidence_projections",
            "source_occurrences",
            "materials",
            "topologies",
            "identity_contracts",
            "operator_input_views",
            "operator_declarations",
            "model_declarations",
            "fixture_declarations",
            "execution_matrix",
            "missingness_contract",
            "phase_contract",
            "prior_prefix_contract",
            "output_guard_contract",
            "semantic_comparison_view",
            "non_outputs",
        },
        label="execution contract",
    )
    _require_keys(
        manifest["canonicalization_contract"],
        {"canonicalization_id", "encoding", "rules"},
        label="canonicalization contract",
    )
    _require_keys(
        manifest["no_retuning_rule"],
        {
            "rule_id",
            "post_freeze_change_requires",
            "prior_run_preservation",
            "predecessor_status",
            "immutable_versioned_filename_required",
            "successor_required_fields",
        },
        label="no-retuning rule",
    )
    _require_keys(
        contract["scope"],
        {"isolated_effects", "fixed_effects", "execution_status", "evaluation_kind", "human_empirical_status"},
        label="scope",
    )
    _require_keys(
        contract["unit_definition"],
        {"unit_id", "allowed_ranks", "allowed_operations", "forbidden_operations", "missing_value_encoding"},
        label="unit definition",
    )
    no_retuning = manifest["no_retuning_rule"]
    if no_retuning["rule_id"] != "version-bump-required-after-freeze":
        raise ValueError("no-retuning rule identity changed")
    if no_retuning["post_freeze_change_requires"] != "new-manifest-version-and-digest":
        raise ValueError("post-freeze version requirement changed")
    if no_retuning["prior_run_preservation"] is not True:
        raise ValueError("prior run preservation disabled")
    if no_retuning["immutable_versioned_filename_required"] is not True:
        raise ValueError("immutable versioned filename disabled")
    if no_retuning["predecessor_status"] != "none_initial_version":
        raise ValueError("v1 unexpectedly claims a predecessor")
    if no_retuning["successor_required_fields"] != [
        "supersedes_manifest_id",
        "supersedes_manifest_version",
        "supersedes_manifest_sha256",
    ]:
        raise ValueError("successor lineage contract changed")
    if EXECUTION_PATH.name != "interp-001-m1-v1-execution.json":
        raise ValueError("frozen manifest filename is not versioned")
    if not HEX_40.fullmatch(manifest["implementation_base_revision"]):
        raise ValueError("invalid base revision")
    for document in manifest["governing_documents"]:
        _require_keys(document, {"document_id", "path", "content_sha256"}, label="governing document")
        if not HEX_64.fullmatch(document["content_sha256"]):
            raise ValueError("invalid document digest")
        source = ROOT / document["path"]
        if not source.is_file():
            raise ValueError("missing governing document")
        if hashlib.sha256(source.read_bytes()).hexdigest() != document["content_sha256"]:
            raise ValueError("governing document digest mismatch")

    unit = contract["unit_definition"]
    if unit["allowed_ranks"] != [0, 1, 2]:
        raise ValueError("ordinal domain changed")
    if set(unit["allowed_operations"]) != {
        "equality",
        "ordering",
        "min",
        "max",
        "rank_threshold",
    }:
        raise ValueError("ordinal operation set changed")
    if not {
        "addition",
        "average",
        "difference",
        "division",
        "multiplication",
        "scalar_cancellation",
    } <= set(unit["forbidden_operations"]):
        raise ValueError("ordinal arithmetic not fully forbidden")

    reception_axis = {
        "positive_direction_receptivity",
        "negative_direction_receptivity",
        "ambiguity_tolerance",
        "exploration_bandwidth",
    }
    encounter_axis = {
        "positive_direction_fit",
        "negative_direction_fit",
        "ambiguity",
        "activation",
    }
    axes = contract["axis_definitions"]
    for axis in axes:
        _require_keys(axis, {"profile_kind", "axis_id", "unit_id", "aggregation"}, label="axis")
    if {
        item["axis_id"] for item in axes if item["profile_kind"] == "reception_state"
    } != reception_axis:
        raise ValueError("reception axes changed")
    if {
        item["axis_id"]
        for item in axes
        if item["profile_kind"] == "subjective_encounter_form_proxy"
    } != encounter_axis:
        raise ValueError("encounter axes changed")
    if any(item["aggregation"] != "no_cross_axis_cancellation" for item in axes):
        raise ValueError("cross-axis cancellation enabled")

    for profile in contract["reception_profiles"]:
        _require_keys(profile, {"profile_key"} | reception_axis, label="reception profile")
        for axis in reception_axis:
            _validate_component(profile[axis])
    for profile in contract["source_encounter_profiles"]:
        _require_keys(profile, {"profile_key"} | encounter_axis, label="encounter profile")
        for axis in encounter_axis:
            _validate_component(profile[axis])
    _require_keys(
        contract["fixed_factors"],
        {"target_form", "ghost", "encounter_formation", "topology_generation"},
        label="fixed factors",
    )
    for fixed_factor in contract["fixed_factors"].values():
        _require_keys(
            fixed_factor,
            {"fixture_key", "version", "operation", "reception_contribution"},
            label="fixed factor",
        )
    for projection in contract["evidence_projections"]:
        _require_keys(projection, {"projection_key", "content_tokens_ordered"}, label="evidence projection")
    for occurrence in contract["source_occurrences"]:
        _require_keys(occurrence, {"occurrence_key", "evidence_projection_key"}, label="source occurrence")
    for material in contract["materials"]:
        _require_keys(
            material,
            {"material_key", "source_occurrence_key", "source_encounter_profile_key", "source_order", "relevant"},
            label="material",
        )
    for topology in contract["topologies"]:
        _require_keys(topology, {"topology_key", "edges"}, label="topology")
        seen_undirected_edges: set[tuple[str, str]] = set()
        for edge in topology["edges"]:
            _require_keys(edge, {"left_material_key", "right_material_key", "strength"}, label="topology edge")
            _validate_component(edge["strength"])
            undirected = tuple(sorted((edge["left_material_key"], edge["right_material_key"])))
            if undirected in seen_undirected_edges:
                raise ValueError("duplicate or reversed duplicate topology edge")
            seen_undirected_edges.add(undirected)

    reception_keys = _ids(contract["reception_profiles"], "profile_key")
    encounter_keys = _ids(contract["source_encounter_profiles"], "profile_key")
    evidence_keys = _ids(contract["evidence_projections"], "projection_key")
    occurrence_keys = _ids(contract["source_occurrences"], "occurrence_key")
    material_keys = _ids(contract["materials"], "material_key")
    topology_keys = _ids(contract["topologies"], "topology_key")
    operator_ids = _ids(contract["operator_declarations"], "operator_id")
    model_ids = _ids(contract["model_declarations"], "model_id")
    fixture_keys = _ids(contract["fixture_declarations"], "fixture_key")

    for occurrence in contract["source_occurrences"]:
        if occurrence["evidence_projection_key"] not in evidence_keys:
            raise ValueError("dangling evidence projection")
    for material in contract["materials"]:
        if material["source_occurrence_key"] not in occurrence_keys:
            raise ValueError("dangling source occurrence")
        if material["source_encounter_profile_key"] not in encounter_keys:
            raise ValueError("dangling source encounter profile")
    for topology in contract["topologies"]:
        for edge in topology["edges"]:
            if edge["left_material_key"] not in material_keys:
                raise ValueError("dangling topology endpoint")
            if edge["right_material_key"] not in material_keys:
                raise ValueError("dangling topology endpoint")
            if edge["left_material_key"] == edge["right_material_key"]:
                raise ValueError("self topology edge")

    if operator_ids != {f"op{index:03d}" for index in range(1, 12)}:
        raise ValueError("operator set changed")
    input_view_ids = _ids(contract["operator_input_views"], "view_id")
    if input_view_ids != {f"iv{index:03d}" for index in range(1, 12)}:
        raise ValueError("operator input view set changed")
    input_views = {item["view_id"]: item for item in contract["operator_input_views"]}
    expected_view_fields = {
        "iv001": [
            ("ordered_source_profiles", "subjective_profile_list", "inspect"),
            ("neutral_profile", "subjective_profile", "inspect"),
            ("opaque_source_lineage_refs", "opaque_ref_list", "pass_through_only"),
        ],
        "iv002": [
            ("ordered_material_profiles", "subjective_profile_list", "inspect"),
            ("ordered_relevant_flags", "boolean_list", "inspect"),
            ("opaque_material_refs", "opaque_ref_list", "pass_through_only"),
        ],
        "iv003": [
            ("ordered_material_profiles", "subjective_profile_list", "inspect"),
            ("ordered_relevant_flags", "boolean_list", "inspect"),
            ("reception_profile", "reception_profile", "inspect"),
            ("opaque_material_refs", "opaque_ref_list", "pass_through_only"),
        ],
        "iv004": [
            ("accessible_positions_ordered", "integer_list", "inspect"),
            ("induced_topology_edges_by_position", "normalized_edge_list", "inspect"),
            ("opaque_material_refs", "opaque_ref_list", "pass_through_only"),
        ],
        "iv005": [
            ("assembly_member_profiles_ordered", "subjective_profile_list", "inspect"),
            ("assembly_membership_positions", "integer_list", "inspect"),
        ],
        "iv006": [("raw_direction_profile", "direction_profile", "inspect")],
        "iv007": [
            ("raw_direction_profile", "direction_profile", "inspect"),
            ("reception_profile", "reception_profile", "inspect"),
            ("assembly_member_profiles_ordered", "subjective_profile_list", "inspect"),
            ("induced_topology_edges_by_position", "normalized_edge_list", "inspect"),
        ],
        "iv008": [("eligible_directions", "direction_set", "inspect")],
        "iv009": [("adjudication_outcome", "adjudication_outcome", "inspect")],
        "iv010": [
            ("current_source_lineage_pair_set", "opaque_pair_set", "inspect"),
            ("prior_assembly_source_lineage_pair_set", "opaque_pair_set", "inspect"),
            ("frozen_edge_present", "boolean", "inspect"),
        ],
        "iv011": [
            ("adjudication_outcome", "adjudication_outcome", "inspect"),
            ("episode_integration_present", "boolean", "inspect"),
        ],
    }
    common_forbidden = {
        "cell_key",
        "expected_signature",
        "fixture_key",
        "ledger_key",
        "material_key",
        "model_id",
        "pass_fail_label",
        "policy_id",
        "profile_key",
        "semantic_alias",
    }
    for view in input_views.values():
        _require_keys(view, {"view_id", "view_version", "fields", "forbidden_fields"}, label="operator input view")
        if set(view["forbidden_fields"]) != common_forbidden:
            raise ValueError("operator input view identity branch surface changed")
        field_ids = _ids(view["fields"], "field_id")
        for field in view["fields"]:
            _require_keys(field, {"field_id", "value_kind", "operator_use"}, label="operator input field")
        if not field_ids:
            raise ValueError("empty operator input view")
        actual_fields = [
            (field["field_id"], field["value_kind"], field["operator_use"])
            for field in view["fields"]
        ]
        if actual_fields != expected_view_fields[view["view_id"]]:
            raise ValueError("operator input view capability changed")
        if field_ids & set(view["forbidden_fields"]):
            raise ValueError("operator input view exposes forbidden identity field")
    operators = {item["operator_id"]: item for item in contract["operator_declarations"]}
    expected_operator_semantics = {
        "op001": (
            "componentwise_max_or_neutral",
            {"empty_profile_key": "sp005", "preserve_source_lineage": True},
        ),
        "op002": (
            "filter_activation_threshold",
            {"activation_rank_at_least": 1, "require_relevant": True},
        ),
        "op003": (
            "filter_activation_override_or_direction_match",
            {
                "activation_rank_at_least": 1,
                "strong_activation_override_rank": 2,
                "direction_fit_rank_above": 0,
                "receptivity_rank_at_least": 1,
                "ambiguity_rank_requires_tolerance_at_least": 1,
                "require_relevant": True,
            },
        ),
        "op004": (
            "connected_components_min_nodes",
            {
                "minimum_node_count": 2,
                "singleton_relation": "accessible_unassembled",
                "not_accessed_relation": "not_accessed_currently",
            },
        ),
        "op005": (
            "componentwise_directional_max",
            {"aggregate_within_axis": "max", "cross_axis_aggregation": "forbidden"},
        ),
        "op006": (
            "base_direction_eligibility",
            {"raw_support_rank_at_least": 1},
        ),
        "op007": (
            "reception_direction_eligibility_with_strong_override",
            {
                "raw_support_rank_at_least": 1,
                "receptivity_rank_at_least": 1,
                "strong_edge_rank": 2,
                "strong_endpoint_activation_rank": 2,
                "strong_endpoint_direction_fit_rank": 2,
            },
        ),
        "op008": (
            "direction_set_adjudication",
            {
                "empty_set": "deferred",
                "negative_only": "adopted_negative",
                "positive_and_negative": "contested",
                "positive_only": "adopted_positive",
                "rejected_in_m1": False,
            },
        ),
        "op009": (
            "adopted_only_integration",
            {"adopted_emits_receipt": True, "contested_deferred_emit_receipt": False},
        ),
        "op010": (
            "first_pair_assembly_ignition",
            {"require_frozen_edge": True, "require_pair_absent_from_prior_assemblies": True},
        ),
        "op011": (
            "adopted_integration_binding_ignition",
            {"require_adopted": True, "require_episode_integration_receipt": True},
        ),
    }
    expected_dependencies = {
        "op001": [],
        "op002": [],
        "op003": [],
        "op004": [],
        "op005": ["op004"],
        "op006": ["op005"],
        "op007": ["op005"],
        "op008": [],
        "op009": ["op008"],
        "op010": ["op004"],
        "op011": ["op008", "op009"],
    }
    for operator in operators.values():
        _require_keys(
            operator,
            {
                "operator_id",
                "operator_version",
                "kind",
                "opcode",
                "input_view_id",
                "allowed_input_paths",
                "ordered_operator_refs",
                "parameters",
                "missing_policy",
                "tie_break_policy",
                "randomness_policy",
            },
            label="operator",
        )
        if operator["randomness_policy"] != "none":
            raise ValueError("M1 must be deterministic")
        if operator["input_view_id"] not in input_view_ids:
            raise ValueError("dangling operator input view")
        expected_view_id = "iv" + operator["operator_id"][2:]
        if operator["input_view_id"] != expected_view_id:
            raise ValueError("operator bound to wrong resolved input view")
        expected_paths = {
            f"/resolved_operator_input/{field['field_id']}"
            for field in input_views[operator["input_view_id"]]["fields"]
        }
        if set(operator["allowed_input_paths"]) != expected_paths:
            raise ValueError("operator allowlist is not exact input-view closure")
        if len(operator["allowed_input_paths"]) != len(set(operator["allowed_input_paths"])):
            raise ValueError("duplicate operator input path")
        if any(not path.startswith("/resolved_operator_input/") for path in operator["allowed_input_paths"]):
            raise ValueError("operator input escaped resolved view")
        if any(token in path for path in operator["allowed_input_paths"] for token in ("evaluation", "expected", "alias")):
            raise ValueError("evaluation leakage into operator")
        if not set(operator["ordered_operator_refs"]) <= operator_ids:
            raise ValueError("dangling operator ref")
        if operator["operator_id"] in operator["ordered_operator_refs"]:
            raise ValueError("operator self-cycle")
        if operator["ordered_operator_refs"] != expected_dependencies[operator["operator_id"]]:
            raise ValueError("operator dependency graph changed")
        expected_opcode, expected_parameters = expected_operator_semantics[operator["operator_id"]]
        if operator["opcode"] != expected_opcode or _canonical_bytes(
            operator["parameters"]
        ) != _canonical_bytes(expected_parameters):
            raise ValueError("operator semantics changed without manifest version")
        expected_missing_policy = "propagate_missing" if operator["operator_id"] in {"op001", "op005"} else "reject_cell"
        if operator["missing_policy"] != expected_missing_policy:
            raise ValueError("operator missingness policy changed")
        if operator["operator_id"] in {"op002", "op003", "op004"}:
            expected_tie_break = "preserve_declared_order"
        elif operator["operator_id"] == "op010":
            expected_tie_break = "stable_semantic_key"
        else:
            expected_tie_break = "not_applicable"
        if operator["tie_break_policy"] != expected_tie_break:
            raise ValueError("operator tie-break policy changed")

    if model_ids != {"R0", "R1", "R2", "R3"}:
        raise ValueError("reception model set changed")
    models = {item["model_id"]: item for item in contract["model_declarations"]}
    expected_model_operators = {
        "R0": ["op001", "op002", "op004", "op005", "op006", "op008", "op009", "op010", "op011"],
        "R1": ["op001", "op003", "op004", "op005", "op006", "op008", "op009", "op010", "op011"],
        "R2": ["op001", "op002", "op004", "op005", "op007", "op008", "op009", "op010", "op011"],
        "R3": ["op001", "op003", "op004", "op005", "op007", "op008", "op009", "op010", "op011"],
    }
    for model in models.values():
        _require_keys(
            model,
            {
                "model_id",
                "model_version",
                "family",
                "ordered_operator_refs",
                "allowed_input_paths",
                "emitted_artifact_kinds",
                "ablation_parent_model_ids",
                "complexity_rank",
                "semantic_view_version",
                "determinism",
                "randomness_policy",
            },
            label="model",
        )
        if not set(model["ordered_operator_refs"]) <= operator_ids:
            raise ValueError("dangling model operator")
        if len(model["ordered_operator_refs"]) != len(set(model["ordered_operator_refs"])):
            raise ValueError("model invokes an operator more than once")
        if model["ordered_operator_refs"] != expected_model_operators[model["model_id"]]:
            raise ValueError("active model operator sequence changed")
        expected_model_views = {
            f"/resolved_operator_input_view/{operators[operator_id]['input_view_id']}"
            for operator_id in model["ordered_operator_refs"]
        }
        if set(model["allowed_input_paths"]) != expected_model_views:
            raise ValueError("model input views do not equal active operator closure")
        if len(model["allowed_input_paths"]) != len(set(model["allowed_input_paths"])):
            raise ValueError("duplicate model input view")
        if any(not path.startswith("/resolved_operator_input_view/iv") for path in model["allowed_input_paths"]):
            raise ValueError("model input escaped resolved views")
        if any(token in path for path in model["allowed_input_paths"] for token in ("evaluation", "expected", "alias")):
            raise ValueError("evaluation leakage into model")
        position = {operator_id: index for index, operator_id in enumerate(model["ordered_operator_refs"])}
        for operator_id in model["ordered_operator_refs"]:
            for dependency in operators[operator_id]["ordered_operator_refs"]:
                if dependency in position and position[dependency] >= position[operator_id]:
                    raise ValueError("operator dependency cycle or back edge")

    if "/resolved_operator_input_view/iv003" in models["R0"]["allowed_input_paths"] or "/resolved_operator_input_view/iv007" in models["R0"]["allowed_input_paths"]:
        raise ValueError("R0 reads reception")
    if "op003" not in models["R1"]["ordered_operator_refs"] or "op007" in models["R1"]["ordered_operator_refs"]:
        raise ValueError("R1 is not access-only")
    if "op002" not in models["R2"]["ordered_operator_refs"] or "op007" not in models["R2"]["ordered_operator_refs"]:
        raise ValueError("R2 is not coherence-only")
    if "op003" not in models["R3"]["ordered_operator_refs"] or "op007" not in models["R3"]["ordered_operator_refs"]:
        raise ValueError("R3 is not factorized access plus coherence")
    r1_without_access = [op for op in models["R1"]["ordered_operator_refs"] if op != "op003"]
    r3_without_access = [op for op in models["R3"]["ordered_operator_refs"] if op != "op003"]
    if ["op007" if op == "op006" else op for op in r1_without_access] != r3_without_access:
        raise ValueError("R3 contains a hidden interaction operator")

    _require_keys(
        contract["phase_contract"],
        {"phase_order", "present_access_invocation", "absent_access_invocation", "back_edges", "reentry"},
        label="phase contract",
    )
    if contract["phase_contract"] != {
        "phase_order": [
            "encounter_formation",
            "access_selection",
            "episode_assembly",
            "candidate_profile",
            "candidate_coherence",
            "binding_adjudication",
            "episode_integration",
            "ignition_projection",
        ],
        "present_access_invocation": "each_active_model_operator_exactly_once",
        "absent_access_invocation": "all_active_model_operator_invocation_counts_zero",
        "back_edges": "forbidden",
        "reentry": "forbidden_within_access_ordinal",
    }:
        raise ValueError("phase execution contract changed")
    phase_index = {phase: index for index, phase in enumerate(contract["phase_contract"]["phase_order"])}
    kind_phase = {
        "encounter_formation": "encounter_formation",
        "access_selection": "access_selection",
        "episode_assembly": "episode_assembly",
        "candidate_profile": "candidate_profile",
        "candidate_coherence": "candidate_coherence",
        "binding_adjudication": "binding_adjudication",
        "episode_integration": "episode_integration",
        "assembly_ignition_projection": "ignition_projection",
        "binding_ignition_projection": "ignition_projection",
    }
    for model in models.values():
        phases = [phase_index[kind_phase[operators[operator_id]["kind"]]] for operator_id in model["ordered_operator_refs"]]
        if phases != sorted(phases):
            raise ValueError("active operator order violates phase DAG")

    fixed_factors = contract["fixed_factors"]
    if any(item["reception_contribution"] != "none" for item in fixed_factors.values()):
        raise ValueError("fixed factor reads reception")
    fixed_target = fixed_factors["target_form"]["fixture_key"]
    fixed_ghost = fixed_factors["ghost"]["fixture_key"]

    access_keys: set[str] = set()
    current_occurrence_keys: set[str] = set()
    delivery_keys: set[str] = set()
    for fixture in contract["fixture_declarations"]:
        _require_keys(
            fixture,
            {
                "fixture_key",
                "fixture_version",
                "isolated_ledger_key",
                "actor_key",
                "interpreted_target_scope_key",
                "target_form_fixture_key",
                "ghost_fixture_key",
                "protocol_steps",
            },
            label="fixture",
        )
        if fixture["target_form_fixture_key"] != fixed_target:
            raise ValueError("target form varies inside M1")
        if fixture["ghost_fixture_key"] != fixed_ghost:
            raise ValueError("Ghost varies inside M1")
        expected_step = 1
        last_ordinal = 0
        for step in fixture["protocol_steps"]:
            _require_keys(
                step,
                {"step", "reception_profile_key", "topology_key", "access"},
                {"transport_redelivery"},
                label="protocol step",
            )
            if step["step"] != expected_step:
                raise ValueError("non-contiguous protocol step")
            expected_step += 1
            if step["reception_profile_key"] not in reception_keys:
                raise ValueError("dangling reception profile")
            if step["topology_key"] not in topology_keys:
                raise ValueError("dangling topology")
            access = step["access"]
            if access["present"]:
                _require_keys(
                    access,
                    {
                        "present",
                        "access_key",
                        "access_ordinal",
                        "current_occurrence_key",
                        "current_delivery_key",
                        "trigger_mode",
                        "source_resolution_status",
                        "source_material_keys_ordered",
                    },
                    {"reaccess_of_access_key", "reexposure_of_occurrence_key"},
                    label="present access",
                )
                if access["access_key"] in access_keys:
                    raise ValueError("duplicate access key")
                if access["current_occurrence_key"] in current_occurrence_keys:
                    raise ValueError("current access reused occurrence identity")
                if access["current_delivery_key"] in delivery_keys:
                    raise ValueError("current access reused delivery identity")
                if len({access["access_key"], access["current_occurrence_key"], access["current_delivery_key"]}) != 3:
                    raise ValueError("occurrence delivery and access identities collapsed")
                access_keys.add(access["access_key"])
                current_occurrence_keys.add(access["current_occurrence_key"])
                delivery_keys.add(access["current_delivery_key"])
                if access["access_ordinal"] <= last_ordinal:
                    raise ValueError("non-monotonic access ordinal")
                last_ordinal = access["access_ordinal"]
                if not set(access["source_material_keys_ordered"]) <= material_keys:
                    raise ValueError("dangling access material")
                if "reaccess_of_access_key" in access and access["reaccess_of_access_key"] not in access_keys:
                    raise ValueError("dangling reaccess lineage")
                if access.get("reaccess_of_access_key") == access["access_key"]:
                    raise ValueError("self reaccess lineage")
                if access["trigger_mode"] == "protocol_reexposure":
                    if "reaccess_of_access_key" not in access or "reexposure_of_occurrence_key" not in access:
                        raise ValueError("protocol reexposure lacks access or occurrence lineage")
                    if access["reexposure_of_occurrence_key"] not in current_occurrence_keys:
                        raise ValueError("dangling reexposure occurrence")
                    if access["reexposure_of_occurrence_key"] == access["current_occurrence_key"]:
                        raise ValueError("self reexposure lineage")
                elif "reexposure_of_occurrence_key" in access:
                    raise ValueError("non-reexposure access claims reexposure lineage")
            elif set(access) != {"present"}:
                raise ValueError("absent access invents identity")
            if "transport_redelivery" in step:
                redelivery = step["transport_redelivery"]
                _require_keys(
                    redelivery,
                    {"occurrence_key", "delivery_key", "redelivery_of_delivery_key", "canonical_payload_unchanged"},
                    label="transport redelivery",
                )
                if access["present"]:
                    raise ValueError("transport redelivery created current access")
                if redelivery["occurrence_key"] not in current_occurrence_keys:
                    raise ValueError("dangling redelivery current occurrence")
                if redelivery["redelivery_of_delivery_key"] not in delivery_keys:
                    raise ValueError("dangling prior delivery")
                if redelivery["delivery_key"] in delivery_keys:
                    raise ValueError("redelivery reused delivery identity")
                if redelivery["delivery_key"] in {redelivery["occurrence_key"], redelivery["redelivery_of_delivery_key"]}:
                    raise ValueError("redelivery identity collapsed")
                delivery_keys.add(redelivery["delivery_key"])

    matrix = contract["execution_matrix"]
    _require_keys(matrix, {"matrix_kind", "cell_key_template", "fixture_keys", "model_ids"}, label="execution matrix")
    if set(matrix["fixture_keys"]) != fixture_keys or len(matrix["fixture_keys"]) != 16:
        raise ValueError("fixture matrix incomplete")
    if matrix["model_ids"] != ["R0", "R1", "R2", "R3"]:
        raise ValueError("model matrix incomplete")

    identity = contract["identity_contracts"]
    _require_keys(identity, {"manifest_keys", "assembly_candidate", "membership", "semantic_normalization"}, label="identity contracts")
    _require_keys(
        identity["manifest_keys"],
        {"stable_aliases_only", "runtime_artifact_ids_forbidden"},
        label="manifest identity keys",
    )
    _require_keys(
        identity["assembly_candidate"],
        {
            "identity_model_id",
            "identity_model_version",
            "ordered_payload_fields",
            "membership_spec_fields",
            "role_enum",
            "assembly_operator_binding",
            "topology_normalization",
            "constraints",
        },
        label="assembly identity",
    )
    _require_keys(
        identity["assembly_candidate"]["assembly_operator_binding"],
        {"selected_operator_id", "declaration_digest_boundary"},
        label="assembly operator binding",
    )
    _require_keys(
        identity["assembly_candidate"]["topology_normalization"],
        {"edge_direction", "endpoint_order", "edge_order", "duplicates", "reversed_duplicates"},
        label="topology normalization",
    )
    _require_keys(
        identity["membership"],
        {"identity_model_id", "identity_model_version", "ordered_payload_fields"},
        label="membership identity",
    )
    _require_keys(
        identity["semantic_normalization"],
        {"requires_recorded_provenance", "untraceable_runtime_id", "preserve_semantic_order", "sort_true_sets_only"},
        label="semantic normalization",
    )
    assembly_fields = identity["assembly_candidate"]["ordered_payload_fields"]
    required_assembly_fields = [
        "identity_model_id",
        "identity_model_version",
        "actor_id",
        "interpreted_target_scope",
        "access_occurrence_id",
        "access_ordinal",
        "assembly_operator_declaration_digest",
        "ordered_membership_specs",
        "induced_topology_projection",
    ]
    if assembly_fields != required_assembly_fields:
        raise ValueError("assembly identity omits topology, operator, scope, or access")
    if identity["assembly_candidate"]["membership_spec_fields"] != ["material_ref_id", "role", "order"]:
        raise ValueError("MembershipSpec changed")
    if identity["semantic_normalization"]["untraceable_runtime_id"] != "error":
        raise ValueError("post-hoc semantic alias allowed")
    if identity["assembly_candidate"]["role_enum"] != ["member"]:
        raise ValueError("assembly membership role enum changed")
    if identity["assembly_candidate"]["assembly_operator_binding"] != {
        "selected_operator_id": "op004",
        "declaration_digest_boundary": "canonical_full_operator_declaration",
    }:
        raise ValueError("assembly operator digest boundary changed")
    if identity["assembly_candidate"]["topology_normalization"] != {
        "edge_direction": "undirected",
        "endpoint_order": "ascending_membership_order",
        "edge_order": "lexicographic_left_right_strength",
        "duplicates": "reject",
        "reversed_duplicates": "reject",
    }:
        raise ValueError("topology identity normalization changed")

    semantic_view = contract["semantic_comparison_view"]
    _require_keys(
        semantic_view,
        {"view_id", "result_schema_path", "semantic_root", "ordered_fields", "true_set_paths", "excluded_fields"},
        label="semantic view",
    )
    result_schema = _load(ROOT / semantic_view["result_schema_path"])
    semantic_fields = set(result_schema["$defs"]["semantic"]["properties"])
    if set(semantic_view["ordered_fields"]) != semantic_fields:
        raise ValueError("semantic view and frozen result schema differ")
    if semantic_view["true_set_paths"] != ["/semantic/binding_candidates/*/eligible_directions"]:
        raise ValueError("semantic true-set path catalog changed")
    required_view = {
        "encounter_count_delta",
        "subjective_form_profile",
        "encounter_source_lineage",
        "assemblies",
        "binding_candidates",
        "adjudications",
        "settlement_relations",
        "episode_integration_count",
        "assembly_ignition_count",
        "binding_ignition_count",
    }
    if not required_view <= set(semantic_view["ordered_fields"]):
        raise ValueError("semantic view cannot observe a frozen predicate")
    if not {"run_id", "artifact_id", "model_id", "policy_id", "content_digest"} <= set(semantic_view["excluded_fields"]):
        raise ValueError("run-local metadata entered semantic comparison")

    _require_keys(
        contract["missingness_contract"],
        {"missing_reason_precedence", "componentwise_propagation", "zero_imputation", "axis_skipping"},
        label="missingness contract",
    )
    if contract["missingness_contract"]["missing_reason_precedence"] != [
        "source_unresolved",
        "withheld_control",
        "not_declared_by_fixture",
        "operator_undefined",
        "not_applicable",
    ]:
        raise ValueError("missing reason precedence changed")
    if contract["missingness_contract"]["zero_imputation"] != "forbidden":
        raise ValueError("missing values can be zero-imputed")
    _require_keys(
        contract["prior_prefix_contract"],
        {"pair_basis", "included_assemblies", "cell_isolation", "redelivery_effect", "append_timing"},
        label="prior prefix contract",
    )
    if contract["prior_prefix_contract"]["included_assemblies"] != "all_emitted_episode_assembly_candidates_regardless_of_adjudication":
        raise ValueError("deferred assemblies omitted from ignition prefix")
    _require_keys(
        contract["output_guard_contract"],
        {"result_schema_path", "guard_ledger_names", "required_relation"},
        label="output guard contract",
    )
    expected_guards = {
        "action_occurrences",
        "authority_outputs",
        "evidence_assessment",
        "evidence_links",
        "narrative_writes",
        "observation_artifacts",
        "source_encounters",
        "source_materials",
        "source_occurrences",
        "world_outcomes",
    }
    if set(contract["output_guard_contract"]["guard_ledger_names"]) != expected_guards:
        raise ValueError("authority/evidence/source output guard set changed")
    if contract["output_guard_contract"]["required_relation"] != "before_sha256_equals_after_sha256_and_delta_count_zero_for_every_step":
        raise ValueError("output guard relation weakened")
    result_guard_fields = set(result_schema["$defs"]["guardLedgers"]["properties"])
    if result_guard_fields != expected_guards:
        raise ValueError("result schema guard ledgers differ from execution contract")

    expected_non_outputs = {
        "ActionOccurrence",
        "actual_qualia",
        "EvidenceAssessment_change",
        "EvidenceLink_change",
        "human_mood_score",
        "MorphicLoadProfile",
        "Narrative_Field_write",
        "predictive_accuracy",
        "recovery_quantity",
        "TargetFormReadoutChangeReceipt",
        "WorldOutcome",
    }
    if set(contract["non_outputs"]) != expected_non_outputs:
        raise ValueError("non-output boundary changed")

    forbidden_keys = {"expected_by_model", "semantic_signatures", "pass", "fail", "mirror_relations"}
    for path, value in _walk(contract):
        if isinstance(value, dict) and forbidden_keys & set(value):
            raise ValueError(f"expected output leaked into execution at {path}")
    _validate_json_schema(envelope, _load(SCHEMA_PATH))
    if _digest(contract) != EXPECTED_EXECUTION_CONTRACT_SHA256:
        raise ValueError("frozen execution contract changed")


def _validate_evaluation(
    envelope: dict[str, object],
    execution: dict[str, object],
    *,
    check_integrity: bool = True,
) -> None:
    _require_keys(envelope, {"$schema", "manifest", "integrity"}, label="evaluation envelope")
    if envelope["$schema"] != "./interp-001-manifest.schema.json":
        raise ValueError("evaluation schema ref changed")
    if envelope["manifest"]["manifest_kind"] != "evaluation":
        raise ValueError("not evaluation manifest")
    _validate_canonical_domain(envelope)
    if check_integrity:
        _validate_integrity(envelope, "evaluation_contract")
    manifest = envelope["manifest"]
    _require_keys(
        manifest,
        {
            "manifest_kind",
            "schema_version",
            "manifest_id",
            "manifest_version",
            "status",
            "frozen_at",
            "execution_manifest_sha256",
            "canonicalization_id",
            "evaluation_contract",
        },
        label="evaluation manifest",
    )
    _require_keys(
        envelope["integrity"],
        {"algorithm", "canonicalization_id", "manifest_sha256", "contract_sha256"},
        label="evaluation integrity",
    )
    if (
        manifest["manifest_kind"],
        manifest["schema_version"],
        manifest["manifest_id"],
        manifest["manifest_version"],
        manifest["status"],
    ) != ("evaluation", "1.0.0", "INTERP-001A2-M1-EVALUATION", "1.0.0", "FROZEN_UNEXECUTED"):
        raise ValueError("evaluation manifest identity or frozen status changed")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", manifest["frozen_at"]):
        raise ValueError("invalid evaluation frozen_at")
    if envelope["integrity"]["algorithm"] != "sha256" or envelope["integrity"]["canonicalization_id"] != "interp-canonical-json-v1":
        raise ValueError("evaluation integrity algorithm changed")
    if manifest["execution_manifest_sha256"] != execution["integrity"]["manifest_sha256"]:
        raise ValueError("evaluation is not bound to execution manifest")

    execution_contract = execution["manifest"]["execution_contract"]
    evaluation_contract = manifest["evaluation_contract"]
    _require_keys(
        evaluation_contract,
        {
            "evaluation_kind",
            "human_empirical_status",
            "predicate_language_version",
            "predicate_declarations",
            "closed_world_signatures",
            "runner_visibility",
            "evaluator_aliases",
            "lineage_normalization",
            "mirror_relations",
            "semantic_signatures",
            "cell_assertions",
            "pair_assertions",
            "matrix_assertions",
            "global_invariants",
            "retirement_rules",
            "report_disclaimers",
        },
        label="evaluation contract",
    )
    expected_lineage_normalization = {
        "current_occurrence_role": "fixture_local_access_ordinal",
        "source_occurrence_role": "source_material_position",
        "reexposure_role": "prior_current_occurrence_ordinal",
        "sign_mirror_rule": "compare_role_graph_after_direction_swap",
        "order_mirror_rule": "reverse_source_positions_with_material_order",
        "raw_cross_ledger_key_equality": "forbidden",
    }
    if evaluation_contract["lineage_normalization"] != expected_lineage_normalization:
        raise ValueError("mirror lineage normalization changed")
    fixture_steps = {
        fixture["fixture_key"]: len(fixture["protocol_steps"])
        for fixture in execution_contract["fixture_declarations"]
    }
    fixture_keys = set(fixture_steps)
    result_schema = _load(RESULT_SCHEMA_PATH)
    semantic_fields = set(result_schema["$defs"]["semantic"]["properties"])

    predicate_ids = _ids(evaluation_contract["predicate_declarations"], "predicate_id")
    if _digest(evaluation_contract["predicate_declarations"]) != EXPECTED_PREDICATE_CATALOG_SHA256:
        raise ValueError("predicate catalog semantics changed")
    predicates = {
        item["predicate_id"]: item for item in evaluation_contract["predicate_declarations"]
    }
    for declaration in predicates.values():
        _require_keys(
            declaration,
            {
                "predicate_id",
                "predicate_version",
                "minimum_arity",
                "maximum_arity",
                "operand_kinds",
                "opcode_semantics",
            },
            label="predicate declaration",
        )
        if declaration["minimum_arity"] != declaration["maximum_arity"]:
            raise ValueError("M1 predicate arity must be exact")
        if len(declaration["operand_kinds"]) != declaration["maximum_arity"]:
            raise ValueError("predicate operand kind arity mismatch")
        if not declaration["opcode_semantics"].strip():
            raise ValueError("predicate semantics are empty")

    model_domain = set(execution_contract["execution_matrix"]["model_ids"])
    operator_domain = {item["operator_id"] for item in execution_contract["operator_declarations"]}
    guard_domain = set(execution_contract["output_guard_contract"]["guard_ledger_names"])
    phase_domain = set(execution_contract["phase_contract"]["phase_order"])
    axis_domain = {item["axis_id"] for item in execution_contract["axis_definitions"]}
    projection_domain = {item["projection_key"] for item in execution_contract["evidence_projections"]}
    fixed_factor_domain = {
        value["fixture_key"] for value in execution_contract["fixed_factors"].values()
    }
    normalization_domain = {
        "unique_material_membership",
        "contiguous_zero_based_order",
        "left_order_less_than_right_order",
        "lexicographic_edge_order",
        "no_duplicate_or_reversed_edge",
    }
    forbidden_field_domain = {"fixture_key", "alias", "expected_by_model", "semantic_signatures"}

    def validate_operand(kind: str, value: object) -> None:
        if kind in {"integer", "fixture_count", "model_count", "cell_count"}:
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError("predicate integer operand type mismatch")
            exact_counts = {"fixture_count": 16, "model_count": 4, "cell_count": 64}
            if kind in exact_counts and value != exact_counts[kind]:
                raise ValueError("predicate matrix cardinality operand outside domain")
            return
        if kind in {"protocol_step", "prior_step", "reaccess_step", "redelivery_step"}:
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= max(fixture_steps.values()):
                raise ValueError("predicate step operand outside domain")
            return
        if kind == "boolean":
            if not isinstance(value, bool):
                raise ValueError("predicate boolean operand type mismatch")
            return
        if kind in {"ordered_list", "canonical_set"}:
            if not isinstance(value, list):
                raise ValueError("predicate collection operand type mismatch")
            if kind == "canonical_set" and value != sorted(set(value)):
                raise ValueError("set_eq expected value is not unique stable-key sorted")
            return
        if kind == "expected_value":
            if not isinstance(value, (str, int, bool)):
                raise ValueError("predicate expected value type mismatch")
            return
        if kind == "relation_value":
            if not isinstance(value, (str, bool)):
                raise ValueError("predicate relation value type mismatch")
            return
        if not isinstance(value, str):
            raise ValueError("predicate string operand type mismatch")
        if kind == "model_id" and value not in model_domain:
            raise ValueError("predicate model operand outside domain")
        if kind == "operator_id" and value not in operator_domain:
            raise ValueError("predicate operator operand outside domain")
        if kind == "fixture_key" and value not in fixture_keys:
            raise ValueError("predicate fixture operand outside domain")
        if kind == "guard_ledger" and value not in guard_domain:
            raise ValueError("predicate guard operand outside domain")
        if kind == "phase" and value not in phase_domain:
            raise ValueError("predicate phase operand outside domain")
        if kind == "axis_id" and value not in axis_domain:
            raise ValueError("predicate axis operand outside domain")
        if kind == "direction" and value not in {"negative", "positive"}:
            raise ValueError("predicate direction operand outside domain")
        if kind == "signature_id" and value not in signature_ids:
            raise ValueError("predicate signature operand outside domain")
        if kind == "execution_manifest_id" and value != "INTERP-001A2-M1-EXECUTION":
            raise ValueError("predicate execution manifest operand outside domain")
        if kind == "evaluation_manifest_id" and value != "INTERP-001A2-M1-EVALUATION":
            raise ValueError("predicate evaluation manifest operand outside domain")
        if kind == "projection_key" and value not in projection_domain:
            raise ValueError("predicate projection operand outside domain")
        if kind == "fixed_factor_key" and value not in fixed_factor_domain:
            raise ValueError("predicate fixed-factor operand outside domain")
        if kind == "formation_fixture_key" and value != execution_contract["fixed_factors"]["encounter_formation"]["fixture_key"]:
            raise ValueError("predicate encounter-formation operand outside domain")
        if kind == "forbidden_field" and value not in forbidden_field_domain:
            raise ValueError("predicate forbidden-field operand outside domain")
        if kind == "normalization_rule" and value not in normalization_domain:
            raise ValueError("predicate normalization operand outside domain")
        if kind == "cell_domain" and value != "all_64_cells":
            raise ValueError("predicate cell-domain operand outside domain")
        if kind == "fixture_projection" and value not in {
            "current_access_lineage_or_empty",
            "encounter_policy_projection_or_not_applicable",
            "evidence_projection_keys_ordered",
            "neutral_profile_sp005",
        }:
            raise ValueError("predicate fixture-projection operand outside domain")
        if kind == "semantic_path" and not _schema_path_exists(result_schema, value):
            raise ValueError("predicate path is outside semantic result schema")
        if kind == "cell_ref":
            parts = value.split(":")
            if len(parts) != 3 or parts[0] not in fixture_keys or parts[1] not in model_domain or not parts[2].isdigit():
                raise ValueError("predicate cell ref outside domain")
            if not 1 <= int(parts[2]) <= fixture_steps[parts[0]]:
                raise ValueError("predicate cell step outside fixture domain")

    signature_ids = _ids(evaluation_contract["semantic_signatures"], "signature_id")
    if len(signature_ids) != 10:
        raise ValueError("signature catalog changed")

    def validate_semantic_relation(relation: dict[str, object], *, label: str) -> None:
        _require_keys(relation, {"path", "predicate", "value"}, label=label)
        predicate_id = relation["predicate"]
        if predicate_id not in predicates:
            raise ValueError("semantic relation uses undeclared predicate")
        declaration = predicates[predicate_id]
        if declaration["minimum_arity"] != 2:
            raise ValueError("semantic relation predicate arity mismatch")
        if declaration["operand_kinds"][0] != "semantic_path":
            raise ValueError("semantic relation first operand is not a path")
        validate_operand(declaration["operand_kinds"][0], relation["path"])
        validate_operand(declaration["operand_kinds"][1], relation["value"])
        terminal_nodes = _schema_nodes_at_path(result_schema, relation["path"])
        terminal_types = set().union(
            *(_schema_node_types(result_schema, node) for node in terminal_nodes)
        )
        allowed_terminal_types = {
            "count_eq": {"array", "integer"},
            "list_eq": {"array"},
            "set_eq": {"array"},
            "all_supplied": {"array"},
            "none_supplied": {"array"},
            "prefix_eq": {"string"},
            "same_as_fixture": {"array", "object"},
            "same_source_lineage": {"array"},
        }
        predicate_id = relation["predicate"]
        if predicate_id in {"eq", "list_eq", "set_eq"}:
            if not any(
                _schema_accepts_value(result_schema, node, relation["value"])
                for node in terminal_nodes
            ):
                raise ValueError("expected value is incompatible with result path schema")
        elif predicate_id in allowed_terminal_types and not (
            terminal_types & allowed_terminal_types[predicate_id]
        ):
            raise ValueError("semantic predicate is incompatible with result path schema")
        symbolic_relation_domains = {
            ("same_as_fixture", "/semantic/subjective_form_profile"): {
                "encounter_policy_projection_or_not_applicable",
                "neutral_profile_sp005",
            },
            ("same_as_fixture", "/semantic/encounter_source_lineage"): {
                "current_access_lineage_or_empty"
            },
            ("same_as_fixture", "/semantic/evidence_projection_keys_ordered"): {
                "evidence_projection_keys_ordered"
            },
            ("all_supplied", "/semantic/accessed_material_keys_ordered"): {True},
            ("all_supplied", "/semantic/not_accessed_material_keys_ordered"): {True},
            ("all_supplied", "/semantic/settlement_relations"): {
                "assembled_without_adopted_binding",
                "not_accessed_currently",
            },
            ("none_supplied", "/semantic/accessed_material_keys_ordered"): {True},
            ("prefix_eq", "/semantic/prior_prefix_relation"): {True},
            ("same_source_lineage", "/semantic/encounter_source_lineage"): {True},
        }
        symbolic_key = (predicate_id, relation["path"])
        if symbolic_key in symbolic_relation_domains and relation["value"] not in symbolic_relation_domains[
            symbolic_key
        ]:
            raise ValueError("semantic symbolic value is outside the exact path domain")

    closed_world = evaluation_contract["closed_world_signatures"]
    _require_keys(
        closed_world,
        {"unspecified_field_policy", "default_relations", "override_rule"},
        label="closed-world signature contract",
    )
    default_roots: list[str] = []
    for relation in closed_world["default_relations"]:
        validate_semantic_relation(relation, label="default semantic relation")
        root = relation["path"].split("/")[2]
        if root not in semantic_fields or not _schema_path_exists(result_schema, relation["path"]):
            raise ValueError("default predicate path is outside semantic result schema")
        default_roots.append(root)
    if len(default_roots) != len(semantic_fields) or set(default_roots) != semantic_fields:
        raise ValueError("closed-world defaults do not cover every semantic field exactly once")

    used_predicates: set[str] = set()
    used_predicates.update(item["predicate"] for item in closed_world["default_relations"])
    for signature in evaluation_contract["semantic_signatures"]:
        _require_keys(signature, {"signature_id", "expected_relations"}, label="semantic signature")
        relation_paths = [relation["path"] for relation in signature["expected_relations"]]
        if len(relation_paths) != len(set(relation_paths)):
            raise ValueError("semantic signature contains duplicate or conflicting path relation")
        for relation in signature["expected_relations"]:
            validate_semantic_relation(relation, label="semantic relation")
            if not _schema_path_exists(result_schema, relation["path"]):
                raise ValueError("expected path is outside semantic result schema")
            if relation["predicate"] == "set_eq":
                if not isinstance(relation["value"], list) or relation["value"] != sorted(set(relation["value"])):
                    raise ValueError("set_eq expected value is not unique stable-key sorted")
                if relation["path"] not in execution_contract["semantic_comparison_view"]["true_set_paths"]:
                    raise ValueError("set_eq used outside declared true-set path")
            used_predicates.add(relation["predicate"])
        if signature["signature_id"] not in {"sig-no-access", "sig-empty-access", "sig-noop"}:
            exact_counts = {
                (relation["path"], relation["predicate"], relation["value"])
                for relation in signature["expected_relations"]
                if isinstance(relation["value"], (str, int, bool))
            }
            for path in ("/semantic/assemblies", "/semantic/binding_candidates", "/semantic/adjudications"):
                if (path, "count_eq", 1) not in exact_counts:
                    raise ValueError("nonempty signature does not close assembly candidate adjudication cardinality")
    assertions = evaluation_contract["cell_assertions"]
    if _ids(assertions, "fixture_key") != fixture_keys:
        raise ValueError("cell assertions do not cover all fixtures")
    for assertion in assertions:
        _require_keys(assertion, {"fixture_key", "expected_by_model"}, label="cell assertion")
        if set(assertion["expected_by_model"]) != {"R0", "R1", "R2", "R3"}:
            raise ValueError("cell assertion does not cover R0-R3")
        for signatures in assertion["expected_by_model"].values():
            if len(signatures) != fixture_steps[assertion["fixture_key"]]:
                raise ValueError("one signature per protocol step required")
            if not set(signatures) <= signature_ids:
                raise ValueError("dangling semantic signature")

    assertion_sections = (
        "mirror_relations",
        "pair_assertions",
        "matrix_assertions",
        "global_invariants",
        "retirement_rules",
    )
    all_named_assertions = [
        assertion
        for section in assertion_sections
        for assertion in evaluation_contract[section]
    ]
    _ids(all_named_assertions, "assertion_id")
    for section in assertion_sections:
        for assertion in evaluation_contract[section]:
            _require_keys(assertion, {"assertion_id", "predicate", "operands"}, label=section)
            predicate_id = assertion["predicate"]
            used_predicates.add(predicate_id)
            if predicate_id not in predicate_ids:
                raise ValueError("assertion uses undeclared predicate")
            declaration = predicates[predicate_id]
            if len(assertion["operands"]) != declaration["minimum_arity"]:
                raise ValueError("assertion operand arity mismatch")
            for kind, operand in zip(declaration["operand_kinds"], assertion["operands"]):
                validate_operand(kind, operand)
            assertion_fixture_keys = [
                operand
                for kind, operand in zip(declaration["operand_kinds"], assertion["operands"])
                if kind == "fixture_key"
            ]
            assertion_steps = [
                operand
                for kind, operand in zip(declaration["operand_kinds"], assertion["operands"])
                if kind in {"protocol_step", "prior_step", "reaccess_step", "redelivery_step"}
            ]
            if assertion_fixture_keys and any(
                step > fixture_steps[fixture_key]
                for fixture_key in assertion_fixture_keys
                for step in assertion_steps
            ):
                raise ValueError("predicate step exceeds paired fixture domain")
    if used_predicates != predicate_ids:
        raise ValueError("predicate catalog has undeclared use or dead semantics")

    alias_keys: set[str] = set()
    alias_values: set[str] = set()
    for alias in evaluation_contract["evaluator_aliases"]:
        _require_keys(alias, {"semantic_key", "alias"}, label="evaluator alias")
        if alias["semantic_key"] in alias_keys or alias["alias"] in alias_values:
            raise ValueError("duplicate evaluator alias")
        alias_keys.add(alias["semantic_key"])
        alias_values.add(alias["alias"])

    mirrors = evaluation_contract["mirror_relations"]
    mirrored_fixtures: list[str] = []
    for relation in mirrors:
        left, right = relation["operands"][:2]
        if left not in fixture_keys or right not in fixture_keys:
            raise ValueError("dangling mirror fixture")
        mirrored_fixtures.extend((left, right))
    if len(mirrored_fixtures) != 16 or set(mirrored_fixtures) != fixture_keys:
        raise ValueError("mirror matrix is not a partition")

    if evaluation_contract["runner_visibility"] != "forbidden":
        raise ValueError("runner can see evaluation contract")
    if not any(item["assertion_id"] == "complete-cartesian-run-matrix" and item["operands"] == [16, 4, 64] for item in evaluation_contract["matrix_assertions"]):
        raise ValueError("64-cell completeness assertion missing")
    if not any(item["assertion_id"] == "transport-redelivery-noop" for item in evaluation_contract["pair_assertions"]):
        raise ValueError("transport redelivery control missing")
    if not any(item["assertion_id"] == "current-reaccess-distinct-lineage" for item in evaluation_contract["pair_assertions"]):
        raise ValueError("current reaccess control missing")
    guard_assertions = [
        item
        for item in evaluation_contract["global_invariants"]
        if item["predicate"] == "guard_ledgers_equal_every_step"
    ]
    expected_guards = set(execution_contract["output_guard_contract"]["guard_ledger_names"])
    if len(guard_assertions) != 1 or set(guard_assertions[0]["operands"]) != expected_guards:
        raise ValueError("every authority/evidence/source guard ledger is not asserted")

    disclaimers = " ".join(evaluation_contract["report_disclaimers"])
    for boundary in (
        "not measured human mood",
        "not qualia or a first-person report",
        "not a human law",
    ):
        if boundary not in disclaimers:
            raise ValueError("human-empirical disclaimer missing")
    frozen_evaluation_catalog = {
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
    if _digest(frozen_evaluation_catalog) != EXPECTED_EVALUATION_CATALOG_SHA256:
        raise ValueError("evaluation expectation catalog changed")
    _validate_json_schema(envelope, _load(SCHEMA_PATH))
    if _digest(evaluation_contract) != EXPECTED_EVALUATION_CONTRACT_SHA256:
        raise ValueError("frozen evaluation contract changed")


class InterpManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution = _load(EXECUTION_PATH)
        cls.evaluation = _load(EVALUATION_PATH)

    def test_manifests_are_frozen_valid_and_content_bound(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file())
        _validate_execution(self.execution)
        _validate_evaluation(self.evaluation, self.execution)

    def test_execution_and_evaluation_are_separate_runner_surfaces(self) -> None:
        execution_text = EXECUTION_PATH.read_text(encoding="utf-8")
        evaluation_text = EVALUATION_PATH.read_text(encoding="utf-8")
        self.assertNotIn('"expected_by_model"', execution_text)
        self.assertNotIn('"semantic_signatures"', execution_text)
        self.assertIn('"expected_by_model"', evaluation_text)
        self.assertEqual(
            self.evaluation["manifest"]["execution_manifest_sha256"],
            self.execution["integrity"]["manifest_sha256"],
        )

    def test_reception_models_freeze_access_and_coherence_as_separate_effects(self) -> None:
        contract = self.execution["manifest"]["execution_contract"]
        models = {item["model_id"]: item for item in contract["model_declarations"]}
        self.assertNotIn("op003", models["R0"]["ordered_operator_refs"])
        self.assertNotIn("op007", models["R0"]["ordered_operator_refs"])
        self.assertIn("op003", models["R1"]["ordered_operator_refs"])
        self.assertNotIn("op007", models["R1"]["ordered_operator_refs"])
        self.assertNotIn("op003", models["R2"]["ordered_operator_refs"])
        self.assertIn("op007", models["R2"]["ordered_operator_refs"])
        self.assertIn("op003", models["R3"]["ordered_operator_refs"])
        self.assertIn("op007", models["R3"]["ordered_operator_refs"])

    def test_fixture_and_expectation_matrix_freezes_all_64_cells(self) -> None:
        contract = self.execution["manifest"]["execution_contract"]
        fixtures = contract["execution_matrix"]["fixture_keys"]
        models = contract["execution_matrix"]["model_ids"]
        self.assertEqual(len(fixtures) * len(models), 64)
        expected = self.evaluation["manifest"]["evaluation_contract"]["cell_assertions"]
        self.assertEqual(len(expected), 16)
        self.assertTrue(all(set(item["expected_by_model"]) == set(models) for item in expected))

    def test_state_change_and_transport_redelivery_do_not_create_current_access(self) -> None:
        fixtures = {
            item["fixture_key"]: item
            for item in self.execution["manifest"]["execution_contract"]["fixture_declarations"]
        }
        for fixture_key in ("fx013", "fx014"):
            self.assertFalse(fixtures[fixture_key]["protocol_steps"][1]["access"]["present"])
            self.assertNotIn("transport_redelivery", fixtures[fixture_key]["protocol_steps"][1])
        for fixture_key in ("fx015", "fx016"):
            redelivery = fixtures[fixture_key]["protocol_steps"][1]
            reaccess = fixtures[fixture_key]["protocol_steps"][2]
            self.assertFalse(redelivery["access"]["present"])
            self.assertIn("transport_redelivery", redelivery)
            self.assertTrue(reaccess["access"]["present"])
            self.assertEqual(reaccess["access"]["trigger_mode"], "protocol_reexposure")
            self.assertEqual(reaccess["access"]["access_ordinal"], 2)

    def test_assembly_identity_binds_topology_operator_scope_and_access(self) -> None:
        identity = self.execution["manifest"]["execution_contract"]["identity_contracts"]
        fields = set(identity["assembly_candidate"]["ordered_payload_fields"])
        self.assertTrue(
            {
                "actor_id",
                "interpreted_target_scope",
                "access_occurrence_id",
                "access_ordinal",
                "assembly_operator_declaration_digest",
                "ordered_membership_specs",
                "induced_topology_projection",
            }
            <= fields
        )
        self.assertEqual(
            identity["assembly_candidate"]["membership_spec_fields"],
            ["material_ref_id", "role", "order"],
        )

    def test_ordinal_values_are_not_treated_as_interval_arithmetic(self) -> None:
        unit = self.execution["manifest"]["execution_contract"]["unit_definition"]
        self.assertEqual(unit["allowed_ranks"], [0, 1, 2])
        self.assertTrue(
            {"addition", "average", "difference", "division", "multiplication"}
            <= set(unit["forbidden_operations"])
        )
        for _, value in _walk(self.execution["manifest"]):
            self.assertNotIsInstance(value, float)

    def test_mutation_reception_leak_into_r0_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        models = mutant["manifest"]["execution_contract"]["model_declarations"]
        next(item for item in models if item["model_id"] == "R0")["allowed_input_paths"].append(
            "/execution_contract/reception_profiles"
        )
        with self.assertRaisesRegex(ValueError, "model input views|R0 reads reception"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_expected_output_in_execution_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["expected_by_model"] = {}
        with self.assertRaisesRegex(ValueError, "execution contract shape|expected output leaked"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_float_component_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["reception_profiles"][0][
            "positive_direction_receptivity"
        ]["rank"] = 1.0
        with self.assertRaisesRegex(ValueError, "float is forbidden"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_incomplete_expected_matrix_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        mutant["manifest"]["evaluation_contract"]["cell_assertions"].pop()
        with self.assertRaisesRegex(ValueError, "cell assertions do not cover"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_digest_mismatch_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["scope"]["execution_status"] = "executed"
        with self.assertRaisesRegex(ValueError, "manifest digest mismatch"):
            _validate_execution(mutant)

    def test_mutation_schema_forbidden_unknown_field_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["totally_unknown_but_schema_forbidden"] = 1
        with self.assertRaisesRegex(ValueError, "execution contract shape"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_frozen_manifest_identity_is_rejected(self) -> None:
        mutations = {
            "schema_version": "9.9.9",
            "manifest_id": "WRONG",
            "status": "DRAFT",
            "frozen_at": "not-a-time",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                mutant = deepcopy(self.execution)
                mutant["manifest"][field] = value
                with self.assertRaisesRegex(ValueError, "identity or frozen status|invalid frozen_at"):
                    _validate_execution(mutant, check_integrity=False)

    def test_mutation_duplicate_operator_input_path_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        paths = mutant["manifest"]["execution_contract"]["operator_declarations"][0]["allowed_input_paths"]
        paths.append(paths[0])
        with self.assertRaisesRegex(ValueError, "duplicate operator input path"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_predicate_semantics_is_rejected(self) -> None:
        for predicate_id, semantics in (
            ("guard_ledgers_equal_every_step", "always true"),
            ("runner_receives_execution_manifest_only", "runner may read evaluation"),
        ):
            with self.subTest(predicate_id=predicate_id):
                mutant = deepcopy(self.evaluation)
                declaration = next(
                    item
                    for item in mutant["manifest"]["evaluation_contract"]["predicate_declarations"]
                    if item["predicate_id"] == predicate_id
                )
                declaration["opcode_semantics"] = semantics
                with self.assertRaisesRegex(ValueError, "predicate catalog semantics"):
                    _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_predicate_operand_kind_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        assertion = next(
            item
            for item in mutant["manifest"]["evaluation_contract"]["matrix_assertions"]
            if item["assertion_id"] == "r3-access-factorization"
        )
        assertion["operands"][0] = 7
        with self.assertRaisesRegex(ValueError, "predicate string operand type"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_fixture_identity_branch_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        operator = mutant["manifest"]["execution_contract"]["operator_declarations"][2]
        operator["allowed_input_paths"].append("/resolved_operator_input/fixture_key")
        with self.assertRaisesRegex(ValueError, "exact input-view closure"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_input_view_exposes_fixture_identity_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        view = mutant["manifest"]["execution_contract"]["operator_input_views"][2]
        view["fields"].append(
            {"field_id": "fixture_key", "value_kind": "opaque_ref", "operator_use": "inspect"}
        )
        operator = mutant["manifest"]["execution_contract"]["operator_declarations"][2]
        operator["allowed_input_paths"].append("/resolved_operator_input/fixture_key")
        with self.assertRaisesRegex(ValueError, "capability changed|forbidden identity"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_opaque_lineage_ref_becomes_inspectable_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        field = mutant["manifest"]["execution_contract"]["operator_input_views"][1]["fields"][2]
        field["operator_use"] = "inspect"
        with self.assertRaisesRegex(ValueError, "capability changed"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_operator_self_cycle_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        operator = mutant["manifest"]["execution_contract"]["operator_declarations"][0]
        operator["ordered_operator_refs"].append("op001")
        with self.assertRaisesRegex(ValueError, "self-cycle"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_phase_back_edge_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["phase_contract"]["back_edges"] = "allowed"
        with self.assertRaisesRegex(ValueError, "phase execution contract"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_output_guard_relation_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["output_guard_contract"]["required_relation"] = "no_requirement"
        with self.assertRaisesRegex(ValueError, "output guard relation"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_no_retuning_safety_is_rejected(self) -> None:
        for field in ("prior_run_preservation", "immutable_versioned_filename_required"):
            with self.subTest(field=field):
                mutant = deepcopy(self.execution)
                mutant["manifest"]["no_retuning_rule"][field] = False
                with self.assertRaisesRegex(ValueError, "prior run preservation|immutable versioned filename"):
                    _validate_execution(mutant, check_integrity=False)

    def test_mutation_forbidden_output_removal_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["non_outputs"].remove("EvidenceLink_change")
        with self.assertRaisesRegex(ValueError, "non-output boundary"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_guard_ledger_removal_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        guards = mutant["manifest"]["execution_contract"]["output_guard_contract"]["guard_ledger_names"]
        guards.remove("narrative_writes")
        with self.assertRaisesRegex(ValueError, "output guard set"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_missing_as_zero_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        mutant["manifest"]["execution_contract"]["reception_profiles"][0]["ambiguity_tolerance"] = 0
        with self.assertRaisesRegex(ValueError, "explicit tagged object"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_mirror_partition_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        mutant["manifest"]["evaluation_contract"]["mirror_relations"].pop()
        with self.assertRaisesRegex(ValueError, "mirror matrix"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_semantic_path_outside_result_schema_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        signature = mutant["manifest"]["evaluation_contract"]["semantic_signatures"][0]
        signature["expected_relations"][0]["path"] = "/semantic/not_a_frozen_field"
        with self.assertRaisesRegex(ValueError, "outside semantic result schema"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_nested_semantic_path_outside_result_schema_is_rejected(self) -> None:
        mutant = deepcopy(self.evaluation)
        signature = mutant["manifest"]["evaluation_contract"]["semantic_signatures"][0]
        signature["expected_relations"][0]["path"] = "/semantic/accessed_material_keys_ordered/not_a_field"
        with self.assertRaisesRegex(ValueError, "outside semantic result schema"):
            _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_duplicate_or_reversed_topology_edge_is_rejected(self) -> None:
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                mutant = deepcopy(self.execution)
                topology = mutant["manifest"]["execution_contract"]["topologies"][0]
                edge = deepcopy(topology["edges"][0])
                if reverse:
                    edge["left_material_key"], edge["right_material_key"] = (
                        edge["right_material_key"],
                        edge["left_material_key"],
                    )
                topology["edges"].append(edge)
                with self.assertRaisesRegex(ValueError, "duplicate or reversed"):
                    _validate_execution(mutant, check_integrity=False)

    def test_mutation_true_set_not_canonical_is_rejected(self) -> None:
        for value in (["negative", "positive", "positive"], ["positive", "negative"]):
            with self.subTest(value=value):
                mutant = deepcopy(self.evaluation)
                signature = next(
                    item
                    for item in mutant["manifest"]["evaluation_contract"]["semantic_signatures"]
                    if item["signature_id"] == "sig-contested-new"
                )
                relation = next(
                    item for item in signature["expected_relations"] if item["predicate"] == "set_eq"
                )
                relation["value"] = value
                with self.assertRaisesRegex(ValueError, "unique stable-key sorted"):
                    _validate_evaluation(mutant, self.execution, check_integrity=False)

    def test_mutation_redelivery_as_access_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        fixture = next(
            item
            for item in mutant["manifest"]["execution_contract"]["fixture_declarations"]
            if item["fixture_key"] == "fx015"
        )
        fixture["protocol_steps"][1]["access"] = deepcopy(fixture["protocol_steps"][0]["access"])
        with self.assertRaisesRegex(ValueError, "transport redelivery created current access|duplicate access key"):
            _validate_execution(mutant, check_integrity=False)

    def test_mutation_reexposure_without_occurrence_lineage_is_rejected(self) -> None:
        mutant = deepcopy(self.execution)
        fixture = next(
            item
            for item in mutant["manifest"]["execution_contract"]["fixture_declarations"]
            if item["fixture_key"] == "fx015"
        )
        del fixture["protocol_steps"][2]["access"]["reexposure_of_occurrence_key"]
        with self.assertRaisesRegex(ValueError, "protocol reexposure lacks"):
            _validate_execution(mutant, check_integrity=False)

    def test_manifest_schema_keywords_are_enforced_dependency_free(self) -> None:
        schema = _load(SCHEMA_PATH)
        execution_cases = [
            (("manifest", "canonicalization_contract", "canonicalization_id"), "other"),
            (("manifest", "canonicalization_contract", "encoding"), "UTF-16"),
            (("manifest", "execution_contract", "scope", "execution_status"), "executed"),
            (("manifest", "execution_contract", "unit_definition", "unit_id"), "other"),
            (("manifest", "execution_contract", "unit_definition", "missing_value_encoding"), "zero"),
            (("manifest", "execution_contract", "axis_definitions", 0, "unit_id"), "other"),
            (("manifest", "execution_contract", "operator_declarations", 0, "operator_version"), "9"),
            (("manifest", "execution_contract", "model_declarations", 0, "family"), "other"),
            (("manifest", "execution_contract", "execution_matrix", "matrix_kind"), "zip"),
        ]
        for path, value in execution_cases:
            with self.subTest(path=path):
                mutant = deepcopy(self.execution)
                cursor = mutant
                for segment in path[:-1]:
                    cursor = cursor[segment]
                cursor[path[-1]] = value
                with self.assertRaises(ValueError):
                    _validate_json_schema(mutant, schema)
        duplicate_rule = deepcopy(self.execution)
        rules = duplicate_rule["manifest"]["canonicalization_contract"]["rules"]
        rules.append(rules[0])
        with self.assertRaises(ValueError):
            _validate_json_schema(duplicate_rule, schema)
        bool_as_integer = deepcopy(self.execution)
        bool_as_integer["manifest"]["execution_contract"]["reception_profiles"][0][
            "positive_direction_receptivity"
        ]["rank"] = True
        with self.assertRaises(ValueError):
            _validate_json_schema(bool_as_integer, schema)
        integer_as_bool = deepcopy(self.execution)
        integer_as_bool["manifest"]["no_retuning_rule"]["prior_run_preservation"] = 1
        with self.assertRaises(ValueError):
            _validate_json_schema(integer_as_bool, schema)
        invalid_parameter_value = deepcopy(self.execution)
        invalid_parameter_value["manifest"]["execution_contract"]["operator_declarations"][1][
            "parameters"
        ]["require_relevant"] = {}
        with self.assertRaises(ValueError):
            _validate_json_schema(invalid_parameter_value, schema)

        evaluation_cases = [
            (("manifest", "canonicalization_id"), "other"),
            (("manifest", "evaluation_contract", "evaluation_kind"), "human_trial"),
            (("manifest", "evaluation_contract", "predicate_language_version"), "9"),
            (
                ("manifest", "evaluation_contract", "closed_world_signatures", "unspecified_field_policy"),
                "ignore",
            ),
        ]
        for path, value in evaluation_cases:
            with self.subTest(path=path):
                mutant = deepcopy(self.evaluation)
                cursor = mutant
                for segment in path[:-1]:
                    cursor = cursor[segment]
                cursor[path[-1]] = value
                with self.assertRaises(ValueError):
                    _validate_json_schema(mutant, schema)
        duplicate_disclaimer = deepcopy(self.evaluation)
        disclaimers = duplicate_disclaimer["manifest"]["evaluation_contract"]["report_disclaimers"]
        disclaimers.append(disclaimers[0])
        with self.assertRaises(ValueError):
            _validate_json_schema(duplicate_disclaimer, schema)

    def test_semantic_relation_predicate_arity_and_value_kind_are_enforced(self) -> None:
        wrong_value = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in wrong_value["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["predicate"] == "count_eq"
        )
        relation["value"] = "one"
        with self.assertRaisesRegex(ValueError, "integer operand"):
            _validate_evaluation(wrong_value, self.execution, check_integrity=False)

        wrong_arity = deepcopy(self.evaluation)
        relation = wrong_arity["manifest"]["evaluation_contract"]["semantic_signatures"][0][
            "expected_relations"
        ][0]
        relation["predicate"] = "step_signature_all_models"
        with self.assertRaisesRegex(ValueError, "semantic relation predicate arity"):
            _validate_evaluation(wrong_arity, self.execution, check_integrity=False)

        count_on_scalar = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in count_on_scalar["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["path"] == "/semantic/adjudications/*/outcome"
        )
        relation["predicate"] = "count_eq"
        relation["value"] = 1
        with self.assertRaisesRegex(ValueError, "incompatible with result path schema"):
            _validate_evaluation(count_on_scalar, self.execution, check_integrity=False)

        equality_on_array = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in equality_on_array["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["path"] == "/semantic/assemblies"
        )
        relation["predicate"] = "eq"
        relation["value"] = 1
        with self.assertRaisesRegex(ValueError, "incompatible with result path schema"):
            _validate_evaluation(equality_on_array, self.execution, check_integrity=False)

        wrong_list_element = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in wrong_list_element["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["predicate"] == "list_eq"
        )
        relation["value"] = [1]
        with self.assertRaisesRegex(ValueError, "incompatible with result path schema"):
            _validate_evaluation(wrong_list_element, self.execution, check_integrity=False)

        wrong_set_element = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in wrong_set_element["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["predicate"] == "set_eq"
        )
        relation["value"] = [1]
        with self.assertRaisesRegex(ValueError, "incompatible with result path schema"):
            _validate_evaluation(wrong_set_element, self.execution, check_integrity=False)

        duplicate_relation_path = deepcopy(self.evaluation)
        relations = duplicate_relation_path["manifest"]["evaluation_contract"][
            "semantic_signatures"
        ][0]["expected_relations"]
        relations.append(deepcopy(relations[0]))
        with self.assertRaisesRegex(ValueError, "duplicate or conflicting path relation"):
            _validate_evaluation(duplicate_relation_path, self.execution, check_integrity=False)

    def test_named_predicate_domains_and_result_content_rules_are_closed(self) -> None:
        invalid_cell = deepcopy(self.evaluation)
        assertion = next(
            item
            for section in ("pair_assertions", "matrix_assertions")
            for item in invalid_cell["manifest"]["evaluation_contract"][section]
            if any(str(operand).startswith("fx") and ":" in str(operand) for operand in item["operands"])
        )
        cell_index = next(
            index for index, operand in enumerate(assertion["operands"]) if ":" in str(operand)
        )
        assertion["operands"][cell_index] = "fx001:R0:999"
        with self.assertRaisesRegex(ValueError, "cell step outside fixture domain"):
            _validate_evaluation(invalid_cell, self.execution, check_integrity=False)

        invalid_paired_step = deepcopy(self.evaluation)
        assertion = next(
            item
            for item in invalid_paired_step["manifest"]["evaluation_contract"]["pair_assertions"]
            if item["assertion_id"] == "state-change-without-access-noop"
        )
        assertion["operands"][2] = 3
        with self.assertRaisesRegex(ValueError, "step exceeds paired fixture domain"):
            _validate_evaluation(invalid_paired_step, self.execution, check_integrity=False)

        invalid_normalization = deepcopy(self.evaluation)
        assertion = next(
            item
            for item in invalid_normalization["manifest"]["evaluation_contract"]["global_invariants"]
            if item["predicate"] == "assembly_identity_normalization_holds"
        )
        assertion["operands"][0] = "allow_duplicate_membership"
        with self.assertRaisesRegex(ValueError, "normalization operand outside domain"):
            _validate_evaluation(invalid_normalization, self.execution, check_integrity=False)

        duplicate_assertion_id = deepcopy(self.evaluation)
        pair_assertions = duplicate_assertion_id["manifest"]["evaluation_contract"][
            "pair_assertions"
        ]
        pair_assertions[1]["assertion_id"] = pair_assertions[0]["assertion_id"]
        with self.assertRaisesRegex(ValueError, "duplicate assertion_id"):
            _validate_evaluation(duplicate_assertion_id, self.execution, check_integrity=False)

        invalid_projection = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in invalid_projection["manifest"]["evaluation_contract"]["semantic_signatures"]
            for item in signature["expected_relations"]
            if item["predicate"] == "same_as_fixture"
        )
        relation["value"] = "does_not_exist"
        with self.assertRaisesRegex(ValueError, "fixture-projection operand outside domain"):
            _validate_evaluation(invalid_projection, self.execution, check_integrity=False)

        crossed_projection = deepcopy(self.evaluation)
        relation = next(
            item
            for item in crossed_projection["manifest"]["evaluation_contract"][
                "closed_world_signatures"
            ]["default_relations"]
            if item["path"] == "/semantic/evidence_projection_keys_ordered"
        )
        relation["value"] = "neutral_profile_sp005"
        with self.assertRaisesRegex(ValueError, "exact path domain"):
            _validate_evaluation(crossed_projection, self.execution, check_integrity=False)

        crossed_all_supplied = deepcopy(self.evaluation)
        relation = next(
            item
            for signature in crossed_all_supplied["manifest"]["evaluation_contract"][
                "semantic_signatures"
            ]
            for item in signature["expected_relations"]
            if item["predicate"] == "all_supplied"
            and item["path"] == "/semantic/accessed_material_keys_ordered"
        )
        relation["value"] = "assembled_without_adopted_binding"
        with self.assertRaisesRegex(ValueError, "exact path domain"):
            _validate_evaluation(crossed_all_supplied, self.execution, check_integrity=False)

        for predicate_id in ("none_supplied", "prefix_eq", "same_source_lineage"):
            with self.subTest(predicate_id=predicate_id):
                false_symbolic_relation = deepcopy(self.evaluation)
                relation = next(
                    item
                    for signature in false_symbolic_relation["manifest"]["evaluation_contract"][
                        "semantic_signatures"
                    ]
                    for item in signature["expected_relations"]
                    if item["predicate"] == predicate_id
                )
                relation["value"] = False
                with self.assertRaisesRegex(ValueError, "exact path domain"):
                    _validate_evaluation(
                        false_symbolic_relation,
                        self.execution,
                        check_integrity=False,
                    )

        required_exact_predicates = {
            "assembly_membership_and_topology_equal_fixture_induced_component",
            "candidate_raw_profile_equals_componentwise_max_of_assembly_members",
            "one_binding_candidate_and_adjudication_per_emitted_assembly",
        }
        global_predicates = {
            item["predicate"]
            for item in self.evaluation["manifest"]["evaluation_contract"]["global_invariants"]
        }
        self.assertTrue(required_exact_predicates <= global_predicates)

        result_schema = _load(RESULT_SCHEMA_PATH)
        eligible_schema = result_schema["$defs"]["bindingCandidate"]["properties"][
            "eligible_directions"
        ]
        with self.assertRaises(ValueError):
            _validate_json_schema(
                ["positive", "negative"],
                eligible_schema,
                root_schema=result_schema,
                path="$/eligible_directions",
            )

    def test_operator_parameter_json_types_are_semantically_exact(self) -> None:
        mutant = deepcopy(self.execution)
        operator = next(
            item
            for item in mutant["manifest"]["execution_contract"]["operator_declarations"]
            if item["operator_id"] == "op002"
        )
        operator["parameters"]["require_relevant"] = 1
        with self.assertRaisesRegex(ValueError, "operator semantics changed"):
            _validate_execution(mutant, check_integrity=False)

    def test_evaluation_expectation_catalog_content_is_frozen(self) -> None:
        missing_assertion = deepcopy(self.evaluation)
        pair_assertions = missing_assertion["manifest"]["evaluation_contract"]["pair_assertions"]
        pair_assertions.remove(
            next(
                item
                for item in pair_assertions
                if item["assertion_id"] == "r0-reception-blind-positive"
            )
        )
        with self.assertRaisesRegex(ValueError, "evaluation expectation catalog changed"):
            _validate_evaluation(missing_assertion, self.execution, check_integrity=False)

        missing_signature_relation = deepcopy(self.evaluation)
        signature = next(
            item
            for item in missing_signature_relation["manifest"]["evaluation_contract"][
                "semantic_signatures"
            ]
            if item["signature_id"] == "sig-adopt-positive-new"
        )
        signature["expected_relations"].remove(
            next(
                relation
                for relation in signature["expected_relations"]
                if relation["path"] == "/semantic/adjudications/*/outcome"
            )
        )
        with self.assertRaisesRegex(ValueError, "evaluation expectation catalog changed"):
            _validate_evaluation(
                missing_signature_relation,
                self.execution,
                check_integrity=False,
            )

        changed_cell_mapping = deepcopy(self.evaluation)
        cell = next(
            item
            for item in changed_cell_mapping["manifest"]["evaluation_contract"]["cell_assertions"]
            if item["fixture_key"] == "fx001"
        )
        cell["expected_by_model"]["R0"][0] = "sig-noop"
        with self.assertRaisesRegex(ValueError, "evaluation expectation catalog changed"):
            _validate_evaluation(changed_cell_mapping, self.execution, check_integrity=False)


if __name__ == "__main__":
    unittest.main()
