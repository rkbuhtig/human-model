"""Build and verify the INTERP-DIALOGUE-001P0-v1 decision/freeze artifacts.

P0-v1 does not mutate the frozen 001A families, 001B trace oracle, P0-v0
instrument, or P1-v0 outputs.  Those artifacts are immutable semantic and
decision bases.  P0-v1 owns exact revision decisions, a complete
participant-facing surface, a deterministically rendered delivery catalog,
and the mapping-attempt lineage contract for a future P1-v1 replay.

semantic basis != participant realization != rendered delivery bytes
revision candidate != P0 decision != defect-resolution claim
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    loads_exact,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = ROOT / "research/scenarios/interp-dialogue-001"
ELICITATION_ROOT = SCENARIO_ROOT / "elicitation"
P0_V1_ROOT = ELICITATION_ROOT / "p0-v1"

CANONICALIZATION_PROFILE_ID = "HM-CANONICAL-JSON-PY-V1"
REVISION_BASIS_DIGEST_DOMAIN = "HM-REVISION-BASIS-JSON-V1"
RENDERER_SEMANTICS_VERSION = "INTERP-DIALOGUE-P0-V1-RENDERER-1.0.0"

FROZEN_INPUT_SHA256 = {
    "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json": (
        "52705bc686a69d43360eb0544eda59571c77dc1e29520ec4b156bcd60f413776"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/instrument.schema.json": (
        "0023386d724864c7890cdac14807782a347edc741ad5613a3687d68363f92c89"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/p1-development-pilot-v0-report.md": (
        "18e47174ecd22560f04c18a7f28f5086e1955cf02282488a5fcf93dd2af61157"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/p1/runs/artifact-manifest-v0.json": (
        "2063dfd1d099cbc04b20dcad3409a6f69ad08d6f8cb2e9092c980bf519ceeffe"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/p1/assessment/analyst-adjudication-v0.json": (
        "8a85d0a5702d99258bfcd44df779d34c40bdd830660f3cc03230c3a900192b9b"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/p1/proposals/instrument-revision-proposals-v0.json": (
        "5c1225d90bb7483102fdb29ffd8da129f11c9f300cdac625d080edc1937248b1"
    ),
    "research/scenarios/interp-dialogue-001/families/rel-boundary.json": (
        "4eb342e655ded940ab8537f4e7827692829967a35f17feb375e731a24d2750e2"
    ),
    "research/scenarios/interp-dialogue-001/families/work-feedback.json": (
        "71cedb46667d1fc2ab76ee1e9711e8f0344e3fea6cf9bd16b577643d292d5823"
    ),
    "research/scenarios/interp-dialogue-001/families/risk-footsteps.json": (
        "4fbe69cbe8bd8edb631c9012810dbf935b69f10d5afa7c670638177eabb2a256"
    ),
    "research/scenarios/interp-dialogue-001/trace-oracle-v1.json": (
        "9caefdf39b9ac41c355f8afed0f4c5d0f780499f571346ef2a7042fa30da74b9"
    ),
}

FAMILY_PATHS = {
    "REL-BOUNDARY-001": "research/scenarios/interp-dialogue-001/families/rel-boundary.json",
    "WORK-FEEDBACK-001": "research/scenarios/interp-dialogue-001/families/work-feedback.json",
    "RISK-FOOTSTEPS-001": "research/scenarios/interp-dialogue-001/families/risk-footsteps.json",
}

PROPOSAL_PATH = (
    "research/scenarios/interp-dialogue-001/elicitation/p1/proposals/"
    "instrument-revision-proposals-v0.json"
)
ADJUDICATION_PATH = (
    "research/scenarios/interp-dialogue-001/elicitation/p1/assessment/"
    "analyst-adjudication-v0.json"
)
INSTRUMENT_V0_PATH = (
    "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json"
)
TRACE_ORACLE_PATH = "research/scenarios/interp-dialogue-001/trace-oracle-v1.json"


class P0V1ContractError(ValueError):
    """Raised when a P0-v1 authority or freeze invariant is violated."""


def _fail(message: str) -> None:
    raise P0V1ContractError(message)


def _sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _pretty_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def _load(relpath: str, root: Path = ROOT) -> dict[str, Any]:
    return loads_exact((root / relpath).read_bytes())


def verify_frozen_inputs(root: Path = ROOT) -> None:
    for relpath, expected in FROZEN_INPUT_SHA256.items():
        if _sha256((root / relpath).read_bytes()) != expected:
            _fail(f"frozen semantic/P0/P1 basis drifted: {relpath}")


def _resolve_pointer(value: object, pointer: str) -> object:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        _fail(f"invalid JSON pointer: {pointer}")
    current = value
    for raw_segment in pointer[1:].split("/"):
        segment = raw_segment.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            try:
                current = current[int(segment)]
            except (ValueError, IndexError) as exc:
                raise P0V1ContractError(
                    f"JSON pointer does not resolve: {pointer}"
                ) from exc
        elif isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            _fail(f"JSON pointer does not resolve: {pointer}")
    return current


def _basis_value_sha256(value: object) -> str:
    prefix = (REVISION_BASIS_DIGEST_DOMAIN + "\0").encode("utf-8")
    return _sha256(prefix + canonical_bytes(value))


def _source_artifacts(root: Path = ROOT) -> dict[str, tuple[str, dict[str, Any]]]:
    result = {
        "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0": (
            INSTRUMENT_V0_PATH,
            _load(INSTRUMENT_V0_PATH, root),
        ),
        "INTERP-DIALOGUE-001B-TRACE-ORACLE-V1": (
            TRACE_ORACLE_PATH,
            _load(TRACE_ORACLE_PATH, root),
        ),
        "INTERP-DIALOGUE-001P1-V0-REVISION-PROPOSALS": (
            PROPOSAL_PATH,
            _load(PROPOSAL_PATH, root),
        ),
        "INTERP-DIALOGUE-001P1-V0-DEFECT-ADJUDICATION": (
            ADJUDICATION_PATH,
            _load(ADJUDICATION_PATH, root),
        ),
    }
    for family_id, relpath in FAMILY_PATHS.items():
        result[family_id] = (relpath, _load(relpath, root))
    return result


def _basis_ref(
    artifact_id: str,
    json_pointer: str,
    sources: dict[str, tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    relpath, artifact = sources[artifact_id]
    value = _resolve_pointer(artifact, json_pointer)
    return {
        "artifact_id": artifact_id,
        "artifact_path": relpath,
        "artifact_sha256": FROZEN_INPUT_SHA256[relpath],
        "json_pointer": json_pointer,
        "value_canonical_sha256": _basis_value_sha256(value),
        "canonicalization_profile_id": CANONICALIZATION_PROFILE_ID,
        "digest_domain": REVISION_BASIS_DIGEST_DOMAIN,
    }


def _binding(artifact_id: str, relpath: str, payload: bytes) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "path": relpath,
        "content_sha256": _sha256(payload),
    }


def _schema_header(title: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
    }


def _common_defs() -> dict[str, Any]:
    return {
        "nonEmptyString": {"type": "string", "minLength": 1},
        "token": {
            "type": "string",
            "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$",
        },
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "stringArray": {
            "type": "array",
            "items": {"type": "string"},
        },
    }


def _artifact_schema(
    *,
    title: str,
    schema_const: str,
    artifact_type: str,
    artifact_id: str,
    collection_name: str,
    collection_item: dict[str, Any],
    collection_min: int,
    extra_properties: dict[str, Any] | None = None,
    extra_required: list[str] | None = None,
    defs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema = _schema_header(title)
    properties: dict[str, Any] = {
        "$schema": {"const": schema_const},
        "schema_version": {"const": "1.0.0"},
        "artifact_type": {"const": artifact_type},
        "artifact_id": {"const": artifact_id},
        collection_name: {
            "type": "array",
            "minItems": collection_min,
            "items": collection_item,
        },
    }
    if extra_properties:
        properties.update(extra_properties)
    required = [
        "$schema",
        "schema_version",
        "artifact_type",
        "artifact_id",
        collection_name,
    ]
    if extra_required:
        required.extend(extra_required)
    schema.update(
        {
            "type": "object",
            "additionalProperties": False,
            "required": required,
            "properties": properties,
            "$defs": {**_common_defs(), **(defs or {})},
        }
    )
    return schema


def _revision_candidates_schema() -> dict[str, Any]:
    defs = {
        "basisRef": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "artifact_id",
                "artifact_path",
                "artifact_sha256",
                "json_pointer",
                "value_canonical_sha256",
                "canonicalization_profile_id",
                "digest_domain",
            ],
            "properties": {
                "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                "artifact_path": {"$ref": "#/$defs/nonEmptyString"},
                "artifact_sha256": {"$ref": "#/$defs/sha256"},
                "json_pointer": {"type": "string"},
                "value_canonical_sha256": {"$ref": "#/$defs/sha256"},
                "canonicalization_profile_id": {
                    "const": CANONICALIZATION_PROFILE_ID
                },
                "digest_domain": {"const": REVISION_BASIS_DIGEST_DOMAIN},
            },
        },
        "destination": {
            "type": "object",
            "additionalProperties": False,
            "required": ["artifact_id", "json_pointer", "precondition"],
            "properties": {
                "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                "json_pointer": {"$ref": "#/$defs/nonEmptyString"},
                "precondition": {"const": "MUST_BE_ABSENT"},
            },
        },
        "operation": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "operation_id",
                "operation_kind",
                "basis_refs",
                "destination",
                "replacement_value",
            ],
            "properties": {
                "operation_id": {"$ref": "#/$defs/token"},
                "operation_kind": {
                    "enum": [
                        "ADD_SURFACE_REALIZATION",
                        "ADD_MAPPING_LINEAGE_CONTRACT",
                    ]
                },
                "basis_refs": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/$defs/basisRef"},
                },
                "destination": {"$ref": "#/$defs/destination"},
                "replacement_value": {},
            },
        },
        "candidate": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "resolution_candidate_id",
                "source_proposal_id",
                "source_defect_receipt_ids",
                "semantic_change_classification",
                "operations",
                "rationale",
                "authority",
            ],
            "properties": {
                "resolution_candidate_id": {"$ref": "#/$defs/token"},
                "source_proposal_id": {"$ref": "#/$defs/token"},
                "source_defect_receipt_ids": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/$defs/token"},
                },
                "semantic_change_classification": {
                    "enum": [
                        "REFERENT_CLARIFICATION",
                        "SELF_REFERENCE_REMOVAL",
                        "PRESENTATIONAL_RESTRUCTURING",
                        "SEMANTIC_PRESERVATION_UNVERIFIED",
                        "MAPPING_LINEAGE_CONTRACT_CHANGE",
                    ]
                },
                "operations": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/$defs/operation"},
                },
                "rationale": {"$ref": "#/$defs/nonEmptyString"},
                "authority": {
                    "const": "EXACT_REVISION_CANDIDATE_ONLY_NO_ADOPTION_AUTHORITY"
                },
            },
        },
    }
    return _artifact_schema(
        title="P0-v1 exact revision resolution candidates",
        schema_const="./revision-resolution-candidates-v1.schema.json",
        artifact_type="P0_REVISION_RESOLUTION_CANDIDATE_SET",
        artifact_id="INTERP-DIALOGUE-001P0-V1-RESOLUTION-CANDIDATES",
        collection_name="candidates",
        collection_item={"$ref": "#/$defs/candidate"},
        collection_min=18,
        extra_properties={
            "source_proposal_set_binding": {"$ref": "#/$defs/binding"},
            "source_adjudication_binding": {"$ref": "#/$defs/binding"},
            "canonicalization_profile_id": {
                "const": CANONICALIZATION_PROFILE_ID
            },
            "revision_basis_digest_domain": {
                "const": REVISION_BASIS_DIGEST_DOMAIN
            },
            "authority": {
                "const": "CANDIDATES_ONLY_DECISIONS_ARE_SEPARATE"
            },
        },
        extra_required=[
            "source_proposal_set_binding",
            "source_adjudication_binding",
            "canonicalization_profile_id",
            "revision_basis_digest_domain",
            "authority",
        ],
        defs={
            **defs,
            "binding": {
                "type": "object",
                "additionalProperties": False,
                "required": ["artifact_id", "path", "content_sha256"],
                "properties": {
                    "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                    "path": {"$ref": "#/$defs/nonEmptyString"},
                    "content_sha256": {"$ref": "#/$defs/sha256"},
                },
            },
        },
    )


def _decision_schema() -> dict[str, Any]:
    receipt = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "decision_receipt_id",
            "resolution_candidate_id",
            "decision",
            "applied_operation_ids",
            "decision_basis",
            "execution_status",
            "semantic_preservation_claim",
            "authority",
        ],
        "properties": {
            "decision_receipt_id": {"$ref": "#/$defs/token"},
            "resolution_candidate_id": {"$ref": "#/$defs/token"},
            "decision": {"enum": ["ACCEPTED", "REJECTED", "DEFERRED"]},
            "applied_operation_ids": {
                "type": "array",
                "items": {"$ref": "#/$defs/token"},
            },
            "decision_basis": {"$ref": "#/$defs/nonEmptyString"},
            "execution_status": {
                "enum": [
                    "ADOPTED_IN_FROZEN_P0_V1_NOT_REPILOTED",
                    "REJECTED_NOT_APPLIED",
                    "DEFERRED_NOT_APPLIED",
                ]
            },
            "semantic_preservation_claim": {"const": "NONE"},
            "authority": {"const": "P0_VERSION_DECISION_ONLY"},
        },
    }
    return _artifact_schema(
        title="P0-v1 exact candidate decision receipts",
        schema_const="./p0-decision-receipts-v1.schema.json",
        artifact_type="P0_REVISION_CANDIDATE_DECISION_RECEIPT_SET",
        artifact_id="INTERP-DIALOGUE-001P0-V1-DECISION-RECEIPTS",
        collection_name="decision_receipts",
        collection_item=receipt,
        collection_min=18,
        extra_properties={
            "resolution_candidate_set_binding": {"$ref": "#/$defs/binding"},
            "authority": {"const": "P0_DECISIONS_NO_DEFECT_RESOLUTION_CLAIM"},
        },
        extra_required=["resolution_candidate_set_binding", "authority"],
        defs={
            "binding": {
                "type": "object",
                "additionalProperties": False,
                "required": ["artifact_id", "path", "content_sha256"],
                "properties": {
                    "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                    "path": {"$ref": "#/$defs/nonEmptyString"},
                    "content_sha256": {"$ref": "#/$defs/sha256"},
                },
            }
        },
    )


def _proposal_disposition_schema() -> dict[str, Any]:
    item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "source_proposal_id",
            "resolution_candidate_decision_refs",
            "accepted_resolution_candidate_ids",
            "rejected_resolution_candidate_ids",
            "deferred_resolution_candidate_ids",
            "coverage_status",
        ],
        "properties": {
            "source_proposal_id": {"$ref": "#/$defs/token"},
            "resolution_candidate_decision_refs": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/token"},
            },
            "accepted_resolution_candidate_ids": {"$ref": "#/$defs/stringArray"},
            "rejected_resolution_candidate_ids": {"$ref": "#/$defs/stringArray"},
            "deferred_resolution_candidate_ids": {"$ref": "#/$defs/stringArray"},
            "coverage_status": {
                "const": "COVERED_BY_EXACT_CANDIDATE_DECISIONS"
            },
        },
    }
    return _artifact_schema(
        title="P0-v1 proposal disposition lineage",
        schema_const="./proposal-disposition-record-v1.schema.json",
        artifact_type="P0_PROPOSAL_DISPOSITION_RECORD",
        artifact_id="INTERP-DIALOGUE-001P0-V1-PROPOSAL-DISPOSITIONS",
        collection_name="proposal_dispositions",
        collection_item=item,
        collection_min=8,
        extra_properties={
            "authority": {
                "const": "LINEAGE_SUMMARY_ONLY_NO_PROPOSAL_LEVEL_DECISION_ENUM"
            }
        },
        extra_required=["authority"],
    )


def _surface_schema() -> dict[str, Any]:
    basis = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "artifact_id",
            "artifact_path",
            "artifact_sha256",
            "json_pointer",
            "value_canonical_sha256",
            "canonicalization_profile_id",
            "digest_domain",
        ],
        "properties": {
            "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
            "artifact_path": {"$ref": "#/$defs/nonEmptyString"},
            "artifact_sha256": {"$ref": "#/$defs/sha256"},
            "json_pointer": {"type": "string"},
            "value_canonical_sha256": {"$ref": "#/$defs/sha256"},
            "canonicalization_profile_id": {
                "const": CANONICALIZATION_PROFILE_ID
            },
            "digest_domain": {"const": REVISION_BASIS_DIGEST_DOMAIN},
        },
    }
    surface = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "surface_realization_id",
            "family_id",
            "participant_text",
            "semantic_change_classification",
            "basis_refs",
            "resolution_candidate_refs",
            "required_semantic_elements",
            "prohibited_construct_labels",
        ],
        "properties": {
            "surface_realization_id": {"$ref": "#/$defs/token"},
            "family_id": {"$ref": "#/$defs/token"},
            "participant_text": {"$ref": "#/$defs/nonEmptyString"},
            "semantic_change_classification": {
                "enum": [
                    "UNCHANGED_SOURCE_REALIZATION",
                    "REFERENT_CLARIFICATION",
                    "SELF_REFERENCE_REMOVAL",
                    "PRESENTATIONAL_RESTRUCTURING",
                    "SEMANTIC_PRESERVATION_UNVERIFIED",
                ]
            },
            "basis_refs": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/basisRef"},
            },
            "resolution_candidate_refs": {"$ref": "#/$defs/stringArray"},
            "required_semantic_elements": {"$ref": "#/$defs/stringArray"},
            "prohibited_construct_labels": {"$ref": "#/$defs/stringArray"},
        },
    }
    schema = _schema_header("P0-v1 closed-world participant surface")
    schema.update(
        {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "$schema",
                "schema_version",
                "artifact_type",
                "artifact_id",
                "status",
                "authority",
                "canonicalization_profile_id",
                "renderer_semantics_version",
                "semantic_source_bindings",
                "rendering_grammar",
                "base_surfaces",
                "factor_level_surfaces",
                "future_option_surfaces",
                "prompt_surfaces",
                "diagnostic_surfaces",
                "prohibitions",
            ],
            "properties": {
                "$schema": {"const": "./participant-surface-v1.schema.json"},
                "schema_version": {"const": "1.0.0"},
                "artifact_type": {"const": "CLOSED_WORLD_PARTICIPANT_SURFACE"},
                "artifact_id": {"const": "PARTICIPANT-SURFACE-V1"},
                "status": {"const": "FROZEN_UNEXECUTED_DEVELOPMENT_SURFACE"},
                "authority": {
                    "const": "PARTICIPANT_REALIZATION_ONLY_NO_SEMANTIC_SOURCE_AUTHORITY"
                },
                "canonicalization_profile_id": {
                    "const": CANONICALIZATION_PROFILE_ID
                },
                "renderer_semantics_version": {
                    "const": RENDERER_SEMANTICS_VERSION
                },
                "semantic_source_bindings": {
                    "type": "array",
                    "minItems": 4,
                    "maxItems": 4,
                    "items": {"$ref": "#/$defs/binding"},
                },
                "rendering_grammar": {"$ref": "#/$defs/renderingGrammar"},
                "base_surfaces": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"$ref": "#/$defs/surface"},
                },
                "factor_level_surfaces": {
                    "type": "array",
                    "minItems": 18,
                    "maxItems": 18,
                    "items": {"$ref": "#/$defs/factorSurface"},
                },
                "future_option_surfaces": {
                    "type": "array",
                    "minItems": 6,
                    "maxItems": 6,
                    "items": {"$ref": "#/$defs/futureSurface"},
                },
                "prompt_surfaces": {
                    "type": "array",
                    "minItems": 6,
                    "maxItems": 6,
                    "items": {"$ref": "#/$defs/promptSurface"},
                },
                "diagnostic_surfaces": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {"$ref": "#/$defs/surface"},
                },
                "prohibitions": {
                    "type": "array",
                    "minItems": 6,
                    "items": {"$ref": "#/$defs/nonEmptyString"},
                },
            },
            "$defs": {
                **_common_defs(),
                "basisRef": basis,
                "binding": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["artifact_id", "path", "content_sha256"],
                    "properties": {
                        "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                        "path": {"$ref": "#/$defs/nonEmptyString"},
                        "content_sha256": {"$ref": "#/$defs/sha256"},
                    },
                },
                "surface": surface,
                "factorSurface": {
                    **surface,
                    "required": surface["required"] + ["factor_id", "level_id"],
                    "properties": {
                        **surface["properties"],
                        "factor_id": {"$ref": "#/$defs/token"},
                        "level_id": {"$ref": "#/$defs/token"},
                    },
                },
                "futureSurface": {
                    **surface,
                    "required": surface["required"] + ["future_option_id"],
                    "properties": {
                        **surface["properties"],
                        "future_option_id": {"$ref": "#/$defs/token"},
                    },
                },
                "promptSurface": {
                    **surface,
                    "required": surface["required"] + ["prompt_role"],
                    "properties": {
                        **surface["properties"],
                        "prompt_role": {
                            "enum": ["IMMEDIATE_RESPONSE", "LATER_RESPONSE"]
                        },
                    },
                },
                "renderingGrammar": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "initial_joiner",
                        "factor_line_prefix",
                        "factor_joiner",
                        "factor_order_authority",
                    ],
                    "properties": {
                        "initial_joiner": {"$ref": "#/$defs/nonEmptyString"},
                        "factor_line_prefix": {"$ref": "#/$defs/nonEmptyString"},
                        "factor_joiner": {"$ref": "#/$defs/nonEmptyString"},
                        "factor_order_authority": {
                            "const": "FROZEN_001A_FACTOR_ARRAY_ORDER"
                        },
                    },
                },
            },
        }
    )
    return schema


def _rendered_catalog_schema() -> dict[str, Any]:
    entry = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "delivery_surface_id",
            "delivery_kind",
            "family_id",
            "source_surface_refs",
            "participant_text",
            "utf8_base64",
            "utf8_byte_length",
            "utf8_sha256",
        ],
        "properties": {
            "delivery_surface_id": {"$ref": "#/$defs/token"},
            "delivery_kind": {
                "enum": [
                    "INITIAL_PRESENTATION",
                    "FUTURE_OPTION",
                    "IMMEDIATE_PROMPT",
                    "LATER_PROMPT",
                    "POST_TRACE_DIAGNOSTIC_PROMPT",
                ]
            },
            "family_id": {"$ref": "#/$defs/token"},
            "source_surface_refs": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/token"},
            },
            "participant_text": {"$ref": "#/$defs/nonEmptyString"},
            "utf8_base64": {"type": "string"},
            "utf8_byte_length": {"type": "integer", "minimum": 1},
            "utf8_sha256": {"$ref": "#/$defs/sha256"},
        },
    }
    return _artifact_schema(
        title="P0-v1 exact rendered delivery surface catalog",
        schema_const="./rendered-surface-catalog-v1.schema.json",
        artifact_type="RENDERED_PARTICIPANT_SURFACE_CATALOG",
        artifact_id="INTERP-DIALOGUE-001P0-V1-RENDERED-SURFACES",
        collection_name="deliveries",
        collection_item=entry,
        collection_min=37,
        extra_properties={
            "status": {"const": "FROZEN_DERIVED_UNEXECUTED"},
            "authority": {
                "const": "EXACT_DELIVERY_BYTES_ONLY_NO_OCCURRENCE_AUTHORITY"
            },
            "participant_surface_binding": {"$ref": "#/$defs/binding"},
            "renderer_semantics_version": {
                "const": RENDERER_SEMANTICS_VERSION
            },
            "encoding": {"const": "BASE64_OF_EXACT_UTF8_BYTES"},
        },
        extra_required=[
            "status",
            "authority",
            "participant_surface_binding",
            "renderer_semantics_version",
            "encoding",
        ],
        defs={
            "binding": {
                "type": "object",
                "additionalProperties": False,
                "required": ["artifact_id", "path", "content_sha256"],
                "properties": {
                    "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                    "path": {"$ref": "#/$defs/nonEmptyString"},
                    "content_sha256": {"$ref": "#/$defs/sha256"},
                },
            }
        },
    )


def _mapping_candidate_schema() -> dict[str, Any]:
    alternative = {
        "type": "object",
        "additionalProperties": False,
        "required": ["candidate_id", "target_coordinate", "analyst_basis"],
        "properties": {
            "candidate_id": {"$ref": "#/$defs/token"},
            "target_coordinate": {"$ref": "#/$defs/nonEmptyString"},
            "analyst_basis": {"$ref": "#/$defs/nonEmptyString"},
        },
    }
    schema = _schema_header("P0-v1 development mapping candidate set")
    schema.update(
        {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "$schema",
                "schema_version",
                "artifact_type",
                "candidate_set_id",
                "mapping_attempt_id",
                "candidate_status",
                "alternatives",
                "raw_analyst_rationale",
                "authority",
            ],
            "properties": {
                "$schema": {"const": "./development-assessment-v1.schema.json"},
                "schema_version": {"const": "1.0.0"},
                "artifact_type": {"const": "DEVELOPMENT_MAPPING_CANDIDATE_SET_V1"},
                "candidate_set_id": {"$ref": "#/$defs/token"},
                "mapping_attempt_id": {"$ref": "#/$defs/token"},
                "candidate_status": {
                    "enum": [
                        "PROPOSED",
                        "AMBIGUOUS",
                        "NO_MAPPING",
                        "OUTSIDE_VOCABULARY",
                    ]
                },
                "alternatives": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/alternative"},
                },
                "raw_analyst_rationale": {"$ref": "#/$defs/nonEmptyString"},
                "authority": {
                    "const": "DEVELOPMENT_CANDIDATE_ONLY_NOT_OBSERVATION"
                },
            },
            "$defs": {**_common_defs(), "alternative": alternative},
        }
    )
    return schema


def _mapping_attempt_schema() -> dict[str, Any]:
    attempt = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "mapping_attempt_id",
            "response_event_id",
            "response_disposition",
            "payload_evaluability",
            "attempt_disposition",
            "reason_code",
            "candidate_set_ref",
            "authority",
        ],
        "properties": {
            "mapping_attempt_id": {"$ref": "#/$defs/token"},
            "response_event_id": {"$ref": "#/$defs/nonEmptyString"},
            "response_disposition": {
                "enum": [
                    "RESPONDED",
                    "REFUSED",
                    "NO_RESPONSE",
                    "TECHNICAL_FAILURE",
                ]
            },
            "payload_evaluability": {
                "enum": [
                    "EVALUABLE",
                    "NOT_EVALUABLE_EMPTY_PAYLOAD",
                    "NOT_EVALUABLE_WHITESPACE_ONLY",
                    "NOT_EVALUABLE_ABSENT_PAYLOAD",
                    "NOT_EVALUABLE_BY_DECLARED_POLICY",
                ]
            },
            "attempt_disposition": {
                "enum": ["APPLIED", "NOT_APPLIED", "NOT_EVALUABLE"]
            },
            "reason_code": {"$ref": "#/$defs/token"},
            "candidate_set_ref": {"type": "string"},
            "authority": {
                "const": "MAPPING_ATTEMPT_LINEAGE_ONLY_NOT_OBSERVATION"
            },
        },
    }
    return _artifact_schema(
        title="P0-v1 mapping attempt lineage ledger",
        schema_const="./mapping-attempt-v1.schema.json",
        artifact_type="DEVELOPMENT_MAPPING_ATTEMPT_LEDGER_V1",
        artifact_id="INTERP-DIALOGUE-MAPPING-ATTEMPT-LEDGER-V1",
        collection_name="attempts",
        collection_item=attempt,
        collection_min=1,
        extra_properties={
            "mapping_policy_version": {
                "const": "INTERP-DIALOGUE-DEVELOPMENT-MAPPING-V1"
            },
            "candidate_set_schema_sha256": {"$ref": "#/$defs/sha256"},
            "authority": {"const": "LINEAGE_ONLY_NO_FROZEN_OBSERVATION_MAPPING"},
        },
        extra_required=[
            "mapping_policy_version",
            "candidate_set_schema_sha256",
            "authority",
        ],
    )


def _instrument_schema() -> dict[str, Any]:
    schema = _schema_header("INTERP-DIALOGUE-001P0-v1 elicitation instrument")
    schema.update(
        {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "$schema",
                "schema_version",
                "study_id",
                "instrument_id",
                "instrument_version",
                "status",
                "authority",
                "base_contract_binding",
                "base_contract_composition",
                "semantic_source_bindings",
                "revision_authority_bindings",
                "participant_surface_binding",
                "rendered_surface_catalog_binding",
                "mapping_schema_bindings",
                "renderer_contract",
                "event_schedule",
                "presentations",
                "future_options",
                "family_prompt_deliveries",
                "diagnostic_delivery_surface_id",
                "mapping_lineage_contract",
                "confirmed_defect_refs_pending_repilot",
                "open_deferred_defect_refs",
                "rejected_defect_receipt_refs",
                "defect_resolution_claims",
                "prohibitions",
            ],
            "properties": {
                "$schema": {"const": "./instrument-v1.schema.json"},
                "schema_version": {"const": "1.0.0"},
                "study_id": {"const": "INTERP-DIALOGUE-001P0"},
                "instrument_id": {
                    "const": "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V1"
                },
                "instrument_version": {"const": "1.0.0"},
                "status": {"const": "FROZEN_UNEXECUTED_DEVELOPMENT_ELICITATION_ONLY"},
                "authority": {"$ref": "#/$defs/nonEmptyString"},
                "base_contract_binding": {"$ref": "#/$defs/binding"},
                "base_contract_composition": {
                    "$ref": "#/$defs/baseContractComposition"
                },
                "semantic_source_bindings": {
                    "type": "array",
                    "minItems": 4,
                    "maxItems": 4,
                    "items": {"$ref": "#/$defs/binding"},
                },
                "revision_authority_bindings": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"$ref": "#/$defs/binding"},
                },
                "participant_surface_binding": {"$ref": "#/$defs/binding"},
                "rendered_surface_catalog_binding": {"$ref": "#/$defs/binding"},
                "mapping_schema_bindings": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"$ref": "#/$defs/binding"},
                },
                "renderer_contract": {"$ref": "#/$defs/rendererContract"},
                "event_schedule": {
                    "type": "array",
                    "minItems": 8,
                    "maxItems": 8,
                    "items": {"$ref": "#/$defs/scheduleStep"},
                },
                "presentations": {
                    "type": "array",
                    "minItems": 24,
                    "maxItems": 24,
                    "items": {"$ref": "#/$defs/presentation"},
                },
                "future_options": {
                    "type": "array",
                    "minItems": 6,
                    "maxItems": 6,
                    "items": {"$ref": "#/$defs/futureOption"},
                },
                "family_prompt_deliveries": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"$ref": "#/$defs/familyPrompts"},
                },
                "diagnostic_delivery_surface_id": {"$ref": "#/$defs/token"},
                "mapping_lineage_contract": {"$ref": "#/$defs/mappingContract"},
                "confirmed_defect_refs_pending_repilot": {
                    "type": "array",
                    "minItems": 9,
                    "maxItems": 9,
                    "items": {"$ref": "#/$defs/token"},
                },
                "open_deferred_defect_refs": {
                    "type": "array",
                    "minItems": 4,
                    "maxItems": 4,
                    "items": {"$ref": "#/$defs/token"},
                },
                "rejected_defect_receipt_refs": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1,
                    "items": {"$ref": "#/$defs/token"},
                },
                "defect_resolution_claims": {
                    "type": "array",
                    "maxItems": 0,
                    "items": {"type": "string"},
                },
                "prohibitions": {
                    "type": "array",
                    "minItems": 10,
                    "items": {"$ref": "#/$defs/nonEmptyString"},
                },
            },
            "$defs": {
                **_common_defs(),
                "binding": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["artifact_id", "path", "content_sha256"],
                    "properties": {
                        "artifact_id": {"$ref": "#/$defs/nonEmptyString"},
                        "path": {"$ref": "#/$defs/nonEmptyString"},
                        "content_sha256": {"$ref": "#/$defs/sha256"},
                    },
                },
                "rendererContract": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "semantics_version",
                        "participant_visible_output_authority",
                        "fallback_policy",
                        "semantic_source_direct_text_read",
                        "catalog_membership_policy",
                    ],
                    "properties": {
                        "semantics_version": {"const": RENDERER_SEMANTICS_VERSION},
                        "participant_visible_output_authority": {
                            "const": "RENDERED_SURFACE_CATALOG_ONLY"
                        },
                        "fallback_policy": {"const": "FORBIDDEN"},
                        "semantic_source_direct_text_read": {"const": "FORBIDDEN"},
                        "catalog_membership_policy": {
                            "const": "UNREGISTERED_OUTPUT_FORBIDDEN"
                        },
                    },
                },
                "baseContractComposition": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "inherited_sections",
                        "replaced_sections",
                        "participant_text_inheritance",
                    ],
                    "properties": {
                        "inherited_sections": {
                            "type": "array",
                            "minItems": 6,
                            "items": {"$ref": "#/$defs/token"},
                        },
                        "replaced_sections": {
                            "type": "array",
                            "minItems": 8,
                            "items": {"$ref": "#/$defs/token"},
                        },
                        "participant_text_inheritance": {"const": "FORBIDDEN"},
                    },
                },
                "scheduleStep": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "step_id",
                        "sequence_ordinal",
                        "event_kind",
                        "required",
                        "payload_source",
                    ],
                    "properties": {
                        "step_id": {"$ref": "#/$defs/token"},
                        "sequence_ordinal": {"type": "integer", "minimum": 0},
                        "event_kind": {"$ref": "#/$defs/token"},
                        "required": {"type": "boolean"},
                        "payload_source": {"$ref": "#/$defs/token"},
                    },
                },
                "presentation": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "presentation_id",
                        "family_id",
                        "source_cell_id",
                        "delivery_surface_id",
                    ],
                    "properties": {
                        "presentation_id": {"$ref": "#/$defs/token"},
                        "family_id": {"$ref": "#/$defs/token"},
                        "source_cell_id": {"$ref": "#/$defs/token"},
                        "delivery_surface_id": {"$ref": "#/$defs/token"},
                    },
                },
                "futureOption": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "future_option_id",
                        "family_id",
                        "source_probe_id",
                        "source_option_index",
                        "delivery_surface_id",
                    ],
                    "properties": {
                        "future_option_id": {"$ref": "#/$defs/token"},
                        "family_id": {"$ref": "#/$defs/token"},
                        "source_probe_id": {"$ref": "#/$defs/token"},
                        "source_option_index": {"type": "integer", "minimum": 0},
                        "delivery_surface_id": {"$ref": "#/$defs/token"},
                    },
                },
                "familyPrompts": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "family_id",
                        "immediate_delivery_surface_id",
                        "later_delivery_surface_id",
                    ],
                    "properties": {
                        "family_id": {"$ref": "#/$defs/token"},
                        "immediate_delivery_surface_id": {"$ref": "#/$defs/token"},
                        "later_delivery_surface_id": {"$ref": "#/$defs/token"},
                    },
                },
                "mappingContract": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "attempt_cardinality",
                        "attempt_dispositions",
                        "candidate_statuses",
                        "applied_candidate_set_cardinality",
                        "non_applied_candidate_set_cardinality",
                        "ambiguous_alternative_cardinality",
                        "response_disposition_is_not_evaluability",
                    ],
                    "properties": {
                        "attempt_cardinality": {
                            "const": "EXACTLY_ONE_PER_ELIGIBLE_R1_R2_EVENT"
                        },
                        "attempt_dispositions": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 3,
                            "items": {"$ref": "#/$defs/token"},
                        },
                        "candidate_statuses": {
                            "type": "array",
                            "minItems": 4,
                            "maxItems": 4,
                            "items": {"$ref": "#/$defs/token"},
                        },
                        "applied_candidate_set_cardinality": {"const": "EXACTLY_ONE"},
                        "non_applied_candidate_set_cardinality": {"const": "ZERO"},
                        "ambiguous_alternative_cardinality": {
                            "const": "AT_LEAST_TWO"
                        },
                        "response_disposition_is_not_evaluability": {"const": True},
                    },
                },
            },
        }
    )
    return schema


def _manifest_schema() -> dict[str, Any]:
    entry = {
        "type": "object",
        "additionalProperties": False,
        "required": ["path", "role", "sha256"],
        "properties": {
            "path": {"$ref": "#/$defs/nonEmptyString"},
            "role": {"$ref": "#/$defs/token"},
            "sha256": {"$ref": "#/$defs/sha256"},
        },
    }
    return _artifact_schema(
        title="P0-v1 frozen artifact manifest",
        schema_const="./frozen-artifact-manifest-v1.schema.json",
        artifact_type="P0_V1_FROZEN_ARTIFACT_MANIFEST",
        artifact_id="INTERP-DIALOGUE-001P0-V1-FREEZE",
        collection_name="artifacts",
        collection_item=entry,
        collection_min=20,
        extra_properties={
            "status": {"const": "FROZEN_UNEXECUTED"},
            "authority": {"const": "DIGEST_ACCOUNTING_ONLY_NO_CLAIM_SUPPORT"},
            "merge_basis": {
                "const": "PR17_MERGE_COMMIT_eb7f7e69afa8a78cdf0e5b5caf2ccad0a7574108"
            },
            "confirmed_defect_refs_pending_repilot": {"$ref": "#/$defs/stringArray"},
            "open_deferred_defect_refs": {"$ref": "#/$defs/stringArray"},
            "rejected_defect_receipt_refs": {"$ref": "#/$defs/stringArray"},
            "defect_resolution_claims": {
                "type": "array",
                "maxItems": 0,
                "items": {"type": "string"},
            },
        },
        extra_required=[
            "status",
            "authority",
            "merge_basis",
            "confirmed_defect_refs_pending_repilot",
            "open_deferred_defect_refs",
            "rejected_defect_receipt_refs",
            "defect_resolution_claims",
        ],
    )


def _schemas() -> dict[str, dict[str, Any]]:
    return {
        "revision-resolution-candidates-v1.schema.json": _revision_candidates_schema(),
        "p0-decision-receipts-v1.schema.json": _decision_schema(),
        "proposal-disposition-record-v1.schema.json": _proposal_disposition_schema(),
        "participant-surface-v1.schema.json": _surface_schema(),
        "rendered-surface-catalog-v1.schema.json": _rendered_catalog_schema(),
        "development-assessment-v1.schema.json": _mapping_candidate_schema(),
        "mapping-attempt-v1.schema.json": _mapping_attempt_schema(),
        "instrument-v1.schema.json": _instrument_schema(),
        "frozen-artifact-manifest-v1.schema.json": _manifest_schema(),
    }


SURFACE_OVERRIDES: dict[tuple[str, ...], tuple[str, str, str]] = {
    ("BASE", "REL-BOUNDARY-001"): (
        "The partner says: I want to be alone for a while today. I will contact you tomorrow.",
        "RC-RP002-PARTNER",
        "REFERENT_CLARIFICATION",
    ),
    ("FACTOR", "REL-BOUNDARY-001", "reported_current_mood", "reported_ordinary_mood"): (
        "Just before hearing the partner's request, the recipient says their mood feels ordinary.",
        "RC-RP006-REL-ORDINARY",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "REL-BOUNDARY-001", "reported_current_mood", "reported_low_mood"): (
        "Just before hearing the partner's request, the recipient says their mood feels low.",
        "RC-RP006-REL-LOW",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "REL-BOUNDARY-001", "externally_cued_prior_material", "cue_prior_small_care"): (
        "An earlier occasion when the partner noticed a need and followed through is mentioned again.",
        "RC-RP003-SMALL-CARE",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "REL-BOUNDARY-001", "externally_cued_prior_material", "cue_prior_unexplained_distance"): (
        "An earlier occasion when the partner became distant without explanation is mentioned again.",
        "RC-RP003-DISTANCE",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "WORK-FEEDBACK-001", "reported_evaluation_threat", "reported_low_evaluation_threat"): (
        "Just before reading the feedback, the recipient says they are not especially worried about being judged.",
        "RC-RP006-WORK-LOW",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "WORK-FEEDBACK-001", "reported_evaluation_threat", "reported_high_evaluation_threat"): (
        "Just before reading the feedback, the recipient says they are very worried about being judged.",
        "RC-RP006-WORK-HIGH",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "reported_pre_event_arousal", "reported_low_pre_event_arousal"): (
        "Just before hearing the footsteps, the walker says their body feels calm.",
        "RC-RP006-RISK-LOW",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "reported_pre_event_arousal", "reported_high_pre_event_arousal"): (
        "Just before hearing the footsteps, the walker says their body feels tense and activated.",
        "RC-RP006-RISK-HIGH",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "recent_threat_history", "no_recent_related_incident"): (
        "Nothing like being followed or threatened happened to the walker during the prior week.",
        "RC-RP004-NO-INCIDENT",
        "SELF_REFERENCE_REMOVAL",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "recent_threat_history", "recent_confirmed_following_incident"): (
        "During the prior week, a different person followed the walker across several turns. It was later confirmed that the person had been following the walker.",
        "RC-RP007-FOLLOWING",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "route_match_observation", "route_not_matched"): (
        "The footsteps do not change in number, timing, duration, or loudness. After the walker makes two turns, the source is no longer behind them.",
        "RC-RP007-PRESENTATION",
        "PRESENTATIONAL_RESTRUCTURING",
    ),
    ("FACTOR", "RISK-FOOTSTEPS-001", "route_match_observation", "route_matched"): (
        "The footsteps do not change in number, timing, duration, or loudness. After the walker makes two turns, the source is still behind them.",
        "RC-RP007-PRESENTATION",
        "PRESENTATIONAL_RESTRUCTURING",
    ),
    ("FUTURE", "FUTURE-REL-0"): (
        "Some time later, the same earlier occasion described at the start is mentioned again while the recipient says their mood feels ordinary. The partner has not said or done anything else, and no new information about the partner is provided.",
        "RC-RP005-ORDINARY",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
    ("FUTURE", "FUTURE-REL-1"): (
        "Some time later, the same earlier occasion described at the start is mentioned again while the recipient says their mood feels low. The partner has not said or done anything else, and no new information about the partner is provided.",
        "RC-RP005-LOW",
        "SEMANTIC_PRESERVATION_UNVERIFIED",
    ),
}

FAMILY_ACTOR = {
    "REL-BOUNDARY-001": "recipient",
    "WORK-FEEDBACK-001": "recipient",
    "RISK-FOOTSTEPS-001": "walker",
}


def _surface_entry(
    *,
    realization_id: str,
    family_id: str,
    participant_text: str,
    basis_refs: list[dict[str, Any]],
    classification: str = "UNCHANGED_SOURCE_REALIZATION",
    candidate_refs: list[str] | None = None,
    required_elements: list[str] | None = None,
    prohibited_labels: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "surface_realization_id": realization_id,
        "family_id": family_id,
        "participant_text": participant_text,
        "semantic_change_classification": classification,
        "basis_refs": basis_refs,
        "resolution_candidate_refs": candidate_refs or [],
        "required_semantic_elements": required_elements or [],
        "prohibited_construct_labels": prohibited_labels or [],
    }


def _build_participant_surface(root: Path = ROOT) -> dict[str, Any]:
    sources = _source_artifacts(root)
    instrument = sources["INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0"][1]
    oracle = sources["INTERP-DIALOGUE-001B-TRACE-ORACLE-V1"][1]
    base_by_family = {
        item["family_id"]: (index, item)
        for index, item in enumerate(
            instrument["rendering_policy"]["base_surface_by_family"]
        )
    }
    base_surfaces = []
    factor_surfaces = []
    future_surfaces = []
    prompt_surfaces = []

    for family_id in FAMILY_PATHS:
        index, source = base_by_family[family_id]
        override = SURFACE_OVERRIDES.get(("BASE", family_id))
        text, candidate, classification = (
            override
            if override
            else (source["participant_text"], "", "UNCHANGED_SOURCE_REALIZATION")
        )
        base_surfaces.append(
            _surface_entry(
                realization_id=f"SURFACE-BASE-{family_id}",
                family_id=family_id,
                participant_text=text,
                basis_refs=[
                    _basis_ref(
                        "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0",
                        f"/rendering_policy/base_surface_by_family/{index}/participant_text",
                        sources,
                    )
                ],
                classification=classification,
                candidate_refs=[candidate] if candidate else [],
            )
        )

        family = sources[family_id][1]
        for factor_index, factor in enumerate(family["factors"]):
            for level_index, level in enumerate(factor["levels"]):
                key = (
                    "FACTOR",
                    family_id,
                    factor["factor_id"],
                    level["level_id"],
                )
                override = SURFACE_OVERRIDES.get(key)
                text, candidate, classification = (
                    override
                    if override
                    else (
                        level["descriptor"],
                        "",
                        "UNCHANGED_SOURCE_REALIZATION",
                    )
                )
                entry = _surface_entry(
                    realization_id=f"SURFACE-FACTOR-{family_id}-{level['level_id']}",
                    family_id=family_id,
                    participant_text=text,
                    basis_refs=[
                        _basis_ref(
                            family_id,
                            f"/factors/{factor_index}/levels/{level_index}/descriptor",
                            sources,
                        )
                    ],
                    classification=classification,
                    candidate_refs=[candidate] if candidate else [],
                )
                entry["factor_id"] = factor["factor_id"]
                entry["level_id"] = level["level_id"]
                factor_surfaces.append(entry)

    probe_by_id = {}
    for oracle_item in oracle["matched_future_oracles"]:
        probe = oracle_item["source_probe_snapshot"]
        probe_by_id[probe["probe_id"]] = probe
    for option in instrument["future_option_catalog"]:
        option_id = option["future_option_id"]
        probe = probe_by_id[option["source_probe_id"]]
        original = probe["probe_options"][option["source_option_index"]]
        override = SURFACE_OVERRIDES.get(("FUTURE", option_id))
        text, candidate, classification = (
            override
            if override
            else (original, "", "UNCHANGED_SOURCE_REALIZATION")
        )
        oracle_index = next(
            index
            for index, item in enumerate(oracle["matched_future_oracles"])
            if item["source_probe_snapshot"]["probe_id"] == option["source_probe_id"]
        )
        entry = _surface_entry(
            realization_id=f"SURFACE-{option_id}",
            family_id=option["family_id"],
            participant_text=text,
            basis_refs=[
                _basis_ref(
                    "INTERP-DIALOGUE-001B-TRACE-ORACLE-V1",
                    f"/matched_future_oracles/{oracle_index}/source_probe_snapshot/probe_options/{option['source_option_index']}",
                    sources,
                )
            ],
            classification=classification,
            candidate_refs=[candidate] if candidate else [],
            required_elements=(
                [
                    "LATER_HORIZON",
                    "SAME_PRIOR_MATERIAL_CUE",
                    "NO_NEW_TARGET_EVIDENCE",
                    "REPORTED_MOOD_CONDITION",
                ]
                if option["family_id"] == "REL-BOUNDARY-001"
                else []
            ),
            prohibited_labels=(
                ["access", "prior-material cue", "external target evidence"]
                if option["family_id"] == "REL-BOUNDARY-001"
                else []
            ),
        )
        entry["future_option_id"] = option_id
        future_surfaces.append(entry)

    prompt_index = {
        prompt["prompt_id"]: index
        for index, prompt in enumerate(instrument["prompt_catalog"])
    }
    for family_id, actor in FAMILY_ACTOR.items():
        candidate = {
            "REL-BOUNDARY-001": "RC-RP001-REL",
            "WORK-FEEDBACK-001": "RC-RP001-WORK",
            "RISK-FOOTSTEPS-001": "RC-RP001-RISK",
        }[family_id]
        for role, source_prompt_id, text in (
            (
                "IMMEDIATE_RESPONSE",
                "P_GENERIC_IMMEDIATE_RESPONSE",
                f"What is the first thing the {actor} would say or do next? Respond freely; there is no single correct answer.",
            ),
            (
                "LATER_RESPONSE",
                "P_GENERIC_LATER_RESPONSE",
                f"After this additional event, what is the next thing the {actor} would say or do? Respond freely; there is no single correct answer.",
            ),
        ):
            entry = _surface_entry(
                realization_id=f"SURFACE-PROMPT-{role}-{family_id}",
                family_id=family_id,
                participant_text=text,
                basis_refs=[
                    _basis_ref(
                        "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0",
                        f"/prompt_catalog/{prompt_index[source_prompt_id]}/participant_text",
                        sources,
                    )
                ],
                classification="REFERENT_CLARIFICATION",
                candidate_refs=[candidate],
            )
            entry["prompt_role"] = role
            prompt_surfaces.append(entry)

    diagnostic_index = prompt_index["P_POST_TRACE_DIAGNOSTIC"]
    diagnostic = instrument["prompt_catalog"][diagnostic_index]
    diagnostic_surfaces = [
        _surface_entry(
            realization_id="SURFACE-PROMPT-POST-TRACE-DIAGNOSTIC",
            family_id="ALL-FAMILIES",
            participant_text=diagnostic["participant_text"],
            basis_refs=[
                _basis_ref(
                    "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0",
                    f"/prompt_catalog/{diagnostic_index}/participant_text",
                    sources,
                )
            ],
        )
    ]

    semantic_bindings = [
        _binding(
            family_id,
            relpath,
            (root / relpath).read_bytes(),
        )
        for family_id, relpath in FAMILY_PATHS.items()
    ]
    semantic_bindings.append(
        _binding(
            "INTERP-DIALOGUE-001B-TRACE-ORACLE-V1",
            TRACE_ORACLE_PATH,
            (root / TRACE_ORACLE_PATH).read_bytes(),
        )
    )
    return {
        "$schema": "./participant-surface-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "CLOSED_WORLD_PARTICIPANT_SURFACE",
        "artifact_id": "PARTICIPANT-SURFACE-V1",
        "status": "FROZEN_UNEXECUTED_DEVELOPMENT_SURFACE",
        "authority": "PARTICIPANT_REALIZATION_ONLY_NO_SEMANTIC_SOURCE_AUTHORITY",
        "canonicalization_profile_id": CANONICALIZATION_PROFILE_ID,
        "renderer_semantics_version": RENDERER_SEMANTICS_VERSION,
        "semantic_source_bindings": semantic_bindings,
        "rendering_grammar": {
            "initial_joiner": "\n\nContext:\n",
            "factor_line_prefix": "- ",
            "factor_joiner": "\n",
            "factor_order_authority": "FROZEN_001A_FACTOR_ARRAY_ORDER",
        },
        "base_surfaces": base_surfaces,
        "factor_level_surfaces": factor_surfaces,
        "future_option_surfaces": future_surfaces,
        "prompt_surfaces": prompt_surfaces,
        "diagnostic_surfaces": diagnostic_surfaces,
        "prohibitions": [
            "NO_PARTICIPANT_TEXT_FALLBACK",
            "NO_DIRECT_001A_DESCRIPTOR_DELIVERY",
            "NO_DIRECT_001B_PROBE_OPTION_DELIVERY",
            "NO_INTERNAL_CONSTRUCT_LABEL_EXPOSURE",
            "NO_SEMANTIC_PRESERVATION_CLAIM_FROM_REWORDING",
            "NO_ACTUAL_DELIVERY_OR_RESPONSE_OCCURRENCE_AUTHORITY",
        ],
    }


def _surface_pointer_map(surface: dict[str, Any]) -> dict[str, str]:
    result = {}
    for collection in (
        "base_surfaces",
        "factor_level_surfaces",
        "future_option_surfaces",
        "prompt_surfaces",
        "diagnostic_surfaces",
    ):
        for index, item in enumerate(surface[collection]):
            result[item["surface_realization_id"]] = (
                f"/{collection}/{index}/participant_text"
            )
    return result


CANDIDATE_SPECS = [
    ("RC-RP001-REL", "RP-001", ["DR-001"], "REFERENT_CLARIFICATION", ["SURFACE-PROMPT-IMMEDIATE_RESPONSE-REL-BOUNDARY-001", "SURFACE-PROMPT-LATER_RESPONSE-REL-BOUNDARY-001"]),
    ("RC-RP001-WORK", "RP-001", ["DR-001"], "REFERENT_CLARIFICATION", ["SURFACE-PROMPT-IMMEDIATE_RESPONSE-WORK-FEEDBACK-001", "SURFACE-PROMPT-LATER_RESPONSE-WORK-FEEDBACK-001"]),
    ("RC-RP001-RISK", "RP-001", ["DR-001"], "REFERENT_CLARIFICATION", ["SURFACE-PROMPT-IMMEDIATE_RESPONSE-RISK-FOOTSTEPS-001", "SURFACE-PROMPT-LATER_RESPONSE-RISK-FOOTSTEPS-001"]),
    ("RC-RP002-PARTNER", "RP-002", ["DR-002"], "REFERENT_CLARIFICATION", ["SURFACE-BASE-REL-BOUNDARY-001"]),
    ("RC-RP003-SMALL-CARE", "RP-003", ["DR-003"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-REL-BOUNDARY-001-cue_prior_small_care"]),
    ("RC-RP003-DISTANCE", "RP-003", ["DR-003"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-REL-BOUNDARY-001-cue_prior_unexplained_distance"]),
    ("RC-RP004-NO-INCIDENT", "RP-004", ["DR-003"], "SELF_REFERENCE_REMOVAL", ["SURFACE-FACTOR-RISK-FOOTSTEPS-001-no_recent_related_incident"]),
    ("RC-RP005-ORDINARY", "RP-005", ["DR-004"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FUTURE-REL-0"]),
    ("RC-RP005-LOW", "RP-005", ["DR-004"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FUTURE-REL-1"]),
    ("RC-RP006-REL-ORDINARY", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-REL-BOUNDARY-001-reported_ordinary_mood"]),
    ("RC-RP006-REL-LOW", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-REL-BOUNDARY-001-reported_low_mood"]),
    ("RC-RP006-WORK-LOW", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-WORK-FEEDBACK-001-reported_low_evaluation_threat"]),
    ("RC-RP006-WORK-HIGH", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-WORK-FEEDBACK-001-reported_high_evaluation_threat"]),
    ("RC-RP006-RISK-LOW", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-RISK-FOOTSTEPS-001-reported_low_pre_event_arousal"]),
    ("RC-RP006-RISK-HIGH", "RP-006", ["DR-005", "DR-006"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-RISK-FOOTSTEPS-001-reported_high_pre_event_arousal"]),
    ("RC-RP007-PRESENTATION", "RP-007", ["DR-007"], "PRESENTATIONAL_RESTRUCTURING", ["SURFACE-FACTOR-RISK-FOOTSTEPS-001-route_not_matched", "SURFACE-FACTOR-RISK-FOOTSTEPS-001-route_matched"]),
    ("RC-RP007-FOLLOWING", "RP-007", ["DR-008"], "SEMANTIC_PRESERVATION_UNVERIFIED", ["SURFACE-FACTOR-RISK-FOOTSTEPS-001-recent_confirmed_following_incident"]),
]


def _build_candidates(
    surface: dict[str, Any], root: Path = ROOT
) -> dict[str, Any]:
    sources = _source_artifacts(root)
    pointer_map = _surface_pointer_map(surface)
    surface_by_id = {
        item["surface_realization_id"]: item
        for collection in (
            "base_surfaces",
            "factor_level_surfaces",
            "future_option_surfaces",
            "prompt_surfaces",
            "diagnostic_surfaces",
        )
        for item in surface[collection]
    }
    candidates = []
    for candidate_id, proposal_id, defect_ids, classification, surface_ids in CANDIDATE_SPECS:
        operations = []
        for ordinal, surface_id in enumerate(surface_ids, start=1):
            entry = surface_by_id[surface_id]
            operations.append(
                {
                    "operation_id": f"OP-{candidate_id}-{ordinal:02d}",
                    "operation_kind": "ADD_SURFACE_REALIZATION",
                    "basis_refs": entry["basis_refs"],
                    "destination": {
                        "artifact_id": "PARTICIPANT-SURFACE-V1",
                        "json_pointer": pointer_map[surface_id],
                        "precondition": "MUST_BE_ABSENT",
                    },
                    "replacement_value": entry["participant_text"],
                }
            )
        candidates.append(
            {
                "resolution_candidate_id": candidate_id,
                "source_proposal_id": proposal_id,
                "source_defect_receipt_ids": defect_ids,
                "semantic_change_classification": classification,
                "operations": operations,
                "rationale": (
                    "Adopt the exact closed-world surface realization while preserving "
                    "the frozen semantic artifact as an immutable basis; any declared "
                    "semantic preservation remains subject to P1-v1 inspection."
                ),
                "authority": "EXACT_REVISION_CANDIDATE_ONLY_NO_ADOPTION_AUTHORITY",
            }
        )

    proposal_artifact = sources["INTERP-DIALOGUE-001P1-V0-REVISION-PROPOSALS"][1]
    rp8_index = next(
        index
        for index, proposal in enumerate(proposal_artifact["proposals"])
        if proposal["proposal_id"] == "RP-008"
    )
    mapping_contract = {
        "attempt_dispositions": ["APPLIED", "NOT_APPLIED", "NOT_EVALUABLE"],
        "candidate_statuses": [
            "PROPOSED",
            "AMBIGUOUS",
            "NO_MAPPING",
            "OUTSIDE_VOCABULARY",
        ],
        "attempt_cardinality": "EXACTLY_ONE_PER_ELIGIBLE_R1_R2_EVENT",
        "applied_candidate_set_cardinality": "EXACTLY_ONE",
        "non_applied_candidate_set_cardinality": "ZERO",
        "ambiguous_alternative_cardinality": "AT_LEAST_TWO",
        "response_disposition_is_not_evaluability": True,
    }
    candidates.append(
        {
            "resolution_candidate_id": "RC-RP008-MAPPING-LINEAGE",
            "source_proposal_id": "RP-008",
            "source_defect_receipt_ids": ["DR-009"],
            "semantic_change_classification": "MAPPING_LINEAGE_CONTRACT_CHANGE",
            "operations": [
                {
                    "operation_id": "OP-RC-RP008-MAPPING-LINEAGE-01",
                    "operation_kind": "ADD_MAPPING_LINEAGE_CONTRACT",
                    "basis_refs": [
                        _basis_ref(
                            "INTERP-DIALOGUE-001P1-V0-REVISION-PROPOSALS",
                            f"/proposals/{rp8_index}",
                            sources,
                        )
                    ],
                    "destination": {
                        "artifact_id": "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V1",
                        "json_pointer": "/mapping_lineage_contract",
                        "precondition": "MUST_BE_ABSENT",
                    },
                    "replacement_value": mapping_contract,
                }
            ],
            "rationale": (
                "Separate mapping-attempt disposition from candidate-set status so "
                "absent or unevaluable payloads retain lineage without being cast to "
                "surface mappings."
            ),
            "authority": "EXACT_REVISION_CANDIDATE_ONLY_NO_ADOPTION_AUTHORITY",
        }
    )
    proposal_bytes = (root / PROPOSAL_PATH).read_bytes()
    adjudication_bytes = (root / ADJUDICATION_PATH).read_bytes()
    return {
        "$schema": "./revision-resolution-candidates-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "P0_REVISION_RESOLUTION_CANDIDATE_SET",
        "artifact_id": "INTERP-DIALOGUE-001P0-V1-RESOLUTION-CANDIDATES",
        "source_proposal_set_binding": _binding(
            "INTERP-DIALOGUE-001P1-V0-REVISION-PROPOSALS",
            PROPOSAL_PATH,
            proposal_bytes,
        ),
        "source_adjudication_binding": _binding(
            "INTERP-DIALOGUE-001P1-V0-DEFECT-ADJUDICATION",
            ADJUDICATION_PATH,
            adjudication_bytes,
        ),
        "canonicalization_profile_id": CANONICALIZATION_PROFILE_ID,
        "revision_basis_digest_domain": REVISION_BASIS_DIGEST_DOMAIN,
        "authority": "CANDIDATES_ONLY_DECISIONS_ARE_SEPARATE",
        "candidates": candidates,
    }


def _build_decisions(candidates: dict[str, Any], candidate_bytes: bytes) -> dict[str, Any]:
    receipts = []
    for candidate in candidates["candidates"]:
        candidate_id = candidate["resolution_candidate_id"]
        receipts.append(
            {
                "decision_receipt_id": f"DEC-{candidate_id[3:]}",
                "resolution_candidate_id": candidate_id,
                "decision": "ACCEPTED",
                "applied_operation_ids": [
                    operation["operation_id"]
                    for operation in candidate["operations"]
                ],
                "decision_basis": (
                    "Accepted as an exact development-instrument revision for P0-v1; "
                    "the resulting surface remains unexecuted and must be re-inspected "
                    "under a separately preregistered P1-v1."
                ),
                "execution_status": "ADOPTED_IN_FROZEN_P0_V1_NOT_REPILOTED",
                "semantic_preservation_claim": "NONE",
                "authority": "P0_VERSION_DECISION_ONLY",
            }
        )
    return {
        "$schema": "./p0-decision-receipts-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "P0_REVISION_CANDIDATE_DECISION_RECEIPT_SET",
        "artifact_id": "INTERP-DIALOGUE-001P0-V1-DECISION-RECEIPTS",
        "resolution_candidate_set_binding": _binding(
            "INTERP-DIALOGUE-001P0-V1-RESOLUTION-CANDIDATES",
            "research/scenarios/interp-dialogue-001/elicitation/p0-v1/revision-resolution-candidates-v1.json",
            candidate_bytes,
        ),
        "authority": "P0_DECISIONS_NO_DEFECT_RESOLUTION_CLAIM",
        "decision_receipts": receipts,
    }


def _build_proposal_dispositions(
    candidates: dict[str, Any], decisions: dict[str, Any]
) -> dict[str, Any]:
    decision_by_candidate = {
        item["resolution_candidate_id"]: item
        for item in decisions["decision_receipts"]
    }
    dispositions = []
    for proposal_number in range(1, 9):
        proposal_id = f"RP-{proposal_number:03d}"
        proposal_candidates = [
            candidate
            for candidate in candidates["candidates"]
            if candidate["source_proposal_id"] == proposal_id
        ]
        decision_items = [
            decision_by_candidate[item["resolution_candidate_id"]]
            for item in proposal_candidates
        ]
        dispositions.append(
            {
                "source_proposal_id": proposal_id,
                "resolution_candidate_decision_refs": [
                    item["decision_receipt_id"] for item in decision_items
                ],
                "accepted_resolution_candidate_ids": [
                    item["resolution_candidate_id"]
                    for item in decision_items
                    if item["decision"] == "ACCEPTED"
                ],
                "rejected_resolution_candidate_ids": [
                    item["resolution_candidate_id"]
                    for item in decision_items
                    if item["decision"] == "REJECTED"
                ],
                "deferred_resolution_candidate_ids": [
                    item["resolution_candidate_id"]
                    for item in decision_items
                    if item["decision"] == "DEFERRED"
                ],
                "coverage_status": "COVERED_BY_EXACT_CANDIDATE_DECISIONS",
            }
        )
    return {
        "$schema": "./proposal-disposition-record-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "P0_PROPOSAL_DISPOSITION_RECORD",
        "artifact_id": "INTERP-DIALOGUE-001P0-V1-PROPOSAL-DISPOSITIONS",
        "authority": "LINEAGE_SUMMARY_ONLY_NO_PROPOSAL_LEVEL_DECISION_ENUM",
        "proposal_dispositions": dispositions,
    }


def _delivery_entry(
    delivery_id: str,
    delivery_kind: str,
    family_id: str,
    source_refs: list[str],
    text: str,
) -> dict[str, Any]:
    raw = text.encode("utf-8")
    return {
        "delivery_surface_id": delivery_id,
        "delivery_kind": delivery_kind,
        "family_id": family_id,
        "source_surface_refs": source_refs,
        "participant_text": text,
        "utf8_base64": base64.b64encode(raw).decode("ascii"),
        "utf8_byte_length": len(raw),
        "utf8_sha256": _sha256(raw),
    }


def _build_rendered_catalog(
    surface: dict[str, Any], surface_bytes: bytes, root: Path = ROOT
) -> dict[str, Any]:
    instrument = _load(INSTRUMENT_V0_PATH, root)
    families = {family_id: _load(path, root) for family_id, path in FAMILY_PATHS.items()}
    base = {item["family_id"]: item for item in surface["base_surfaces"]}
    factors = {
        (item["family_id"], item["factor_id"], item["level_id"]): item
        for item in surface["factor_level_surfaces"]
    }
    futures = {
        item["future_option_id"]: item
        for item in surface["future_option_surfaces"]
    }
    prompts = {
        (item["family_id"], item["prompt_role"]): item
        for item in surface["prompt_surfaces"]
    }
    grammar = surface["rendering_grammar"]
    deliveries = []
    for presentation in instrument["presentations"]:
        family_id = presentation["family_id"]
        source_refs = [base[family_id]["surface_realization_id"]]
        lines = []
        for factor in families[family_id]["factors"]:
            level_id = presentation["factor_level_bindings"][factor["factor_id"]]
            item = factors[(family_id, factor["factor_id"], level_id)]
            source_refs.append(item["surface_realization_id"])
            lines.append(grammar["factor_line_prefix"] + item["participant_text"])
        text = (
            base[family_id]["participant_text"]
            + grammar["initial_joiner"]
            + grammar["factor_joiner"].join(lines)
        )
        presentation_id = presentation["presentation_id"].replace("-V0", "-V1")
        deliveries.append(
            _delivery_entry(
                f"DELIVERY-{presentation_id}",
                "INITIAL_PRESENTATION",
                family_id,
                source_refs,
                text,
            )
        )
    for option in instrument["future_option_catalog"]:
        item = futures[option["future_option_id"]]
        deliveries.append(
            _delivery_entry(
                f"DELIVERY-{option['future_option_id']}-V1",
                "FUTURE_OPTION",
                option["family_id"],
                [item["surface_realization_id"]],
                item["participant_text"],
            )
        )
    for family_id in FAMILY_PATHS:
        for role, kind in (
            ("IMMEDIATE_RESPONSE", "IMMEDIATE_PROMPT"),
            ("LATER_RESPONSE", "LATER_PROMPT"),
        ):
            item = prompts[(family_id, role)]
            deliveries.append(
                _delivery_entry(
                    f"DELIVERY-PROMPT-{role}-{family_id}-V1",
                    kind,
                    family_id,
                    [item["surface_realization_id"]],
                    item["participant_text"],
                )
            )
    diagnostic = surface["diagnostic_surfaces"][0]
    deliveries.append(
        _delivery_entry(
            "DELIVERY-PROMPT-POST-TRACE-DIAGNOSTIC-V1",
            "POST_TRACE_DIAGNOSTIC_PROMPT",
            "ALL-FAMILIES",
            [diagnostic["surface_realization_id"]],
            diagnostic["participant_text"],
        )
    )
    return {
        "$schema": "./rendered-surface-catalog-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "RENDERED_PARTICIPANT_SURFACE_CATALOG",
        "artifact_id": "INTERP-DIALOGUE-001P0-V1-RENDERED-SURFACES",
        "status": "FROZEN_DERIVED_UNEXECUTED",
        "authority": "EXACT_DELIVERY_BYTES_ONLY_NO_OCCURRENCE_AUTHORITY",
        "participant_surface_binding": _binding(
            "PARTICIPANT-SURFACE-V1",
            "research/scenarios/interp-dialogue-001/elicitation/p0-v1/participant-surface-v1.json",
            surface_bytes,
        ),
        "renderer_semantics_version": RENDERER_SEMANTICS_VERSION,
        "encoding": "BASE64_OF_EXACT_UTF8_BYTES",
        "deliveries": deliveries,
    }


def _build_instrument(
    *,
    files: dict[str, bytes],
    surface: dict[str, Any],
    catalog: dict[str, Any],
    root: Path = ROOT,
) -> dict[str, Any]:
    v0 = _load(INSTRUMENT_V0_PATH, root)
    delivery_ids = {item["delivery_surface_id"] for item in catalog["deliveries"]}
    presentations = []
    for item in v0["presentations"]:
        presentation_id = item["presentation_id"].replace("-V0", "-V1")
        delivery_id = f"DELIVERY-{presentation_id}"
        if delivery_id not in delivery_ids:
            _fail(f"missing rendered initial delivery: {delivery_id}")
        presentations.append(
            {
                "presentation_id": presentation_id,
                "family_id": item["family_id"],
                "source_cell_id": item["source_cell_id"],
                "delivery_surface_id": delivery_id,
            }
        )
    future_options = []
    for item in v0["future_option_catalog"]:
        future_options.append(
            {
                **item,
                "delivery_surface_id": f"DELIVERY-{item['future_option_id']}-V1",
            }
        )
    family_prompts = [
        {
            "family_id": family_id,
            "immediate_delivery_surface_id": f"DELIVERY-PROMPT-IMMEDIATE_RESPONSE-{family_id}-V1",
            "later_delivery_surface_id": f"DELIVERY-PROMPT-LATER_RESPONSE-{family_id}-V1",
        }
        for family_id in FAMILY_PATHS
    ]
    schedule = json.loads(json.dumps(v0["event_schedule"]))
    payload_overrides = {
        "E0_INITIAL_VIGNETTE_DELIVERY": "REGISTERED_INITIAL_DELIVERY_SURFACE",
        "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY": "FAMILY_RESOLVED_IMMEDIATE_PROMPT_SURFACE",
        "E2_MATCHED_FUTURE_OPTION_DELIVERY": "REGISTERED_FUTURE_DELIVERY_SURFACE",
        "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY": "FAMILY_RESOLVED_LATER_PROMPT_SURFACE",
        "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY": "REGISTERED_DIAGNOSTIC_DELIVERY_SURFACE",
    }
    for step in schedule:
        if step["step_id"] in payload_overrides:
            step["payload_source"] = payload_overrides[step["step_id"]]

    def file_binding(artifact_id: str, filename: str) -> dict[str, str]:
        return _binding(
            artifact_id,
            f"research/scenarios/interp-dialogue-001/elicitation/p0-v1/{filename}",
            files[filename],
        )

    semantic_bindings = surface["semantic_source_bindings"]
    return {
        "$schema": "./instrument-v1.schema.json",
        "schema_version": "1.0.0",
        "study_id": "INTERP-DIALOGUE-001P0",
        "instrument_id": "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V1",
        "instrument_version": "1.0.0",
        "status": "FROZEN_UNEXECUTED_DEVELOPMENT_ELICITATION_ONLY",
        "authority": "DEVELOPMENT_ELICITATION_CONTRACT_NO_ACQUISITION_MEASUREMENT_OR_CLAIM_SUPPORT",
        "base_contract_binding": _binding(
            "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0",
            INSTRUMENT_V0_PATH,
            (root / INSTRUMENT_V0_PATH).read_bytes(),
        ),
        "base_contract_composition": {
            "inherited_sections": [
                "response_status_vocabulary",
                "development_source_kinds",
                "matched_future_comparisons",
                "response_provenance_contract",
                "processing_role_contract",
                "defect_taxonomy",
            ],
            "replaced_sections": [
                "language_policy",
                "rendering_policy",
                "prompt_catalog",
                "event_schedule",
                "presentations",
                "future_option_catalog",
                "mapping_boundary",
                "revision_proposal_contract",
                "prohibitions",
            ],
            "participant_text_inheritance": "FORBIDDEN",
        },
        "semantic_source_bindings": semantic_bindings,
        "revision_authority_bindings": [
            file_binding(
                "INTERP-DIALOGUE-001P0-V1-RESOLUTION-CANDIDATES",
                "revision-resolution-candidates-v1.json",
            ),
            file_binding(
                "INTERP-DIALOGUE-001P0-V1-DECISION-RECEIPTS",
                "p0-decision-receipts-v1.json",
            ),
            file_binding(
                "INTERP-DIALOGUE-001P0-V1-PROPOSAL-DISPOSITIONS",
                "proposal-disposition-record-v1.json",
            ),
        ],
        "participant_surface_binding": file_binding(
            "PARTICIPANT-SURFACE-V1", "participant-surface-v1.json"
        ),
        "rendered_surface_catalog_binding": file_binding(
            "INTERP-DIALOGUE-001P0-V1-RENDERED-SURFACES",
            "rendered-surface-catalog-v1.json",
        ),
        "mapping_schema_bindings": [
            file_binding(
                "DEVELOPMENT-MAPPING-CANDIDATE-SCHEMA-V1",
                "development-assessment-v1.schema.json",
            ),
            file_binding(
                "MAPPING-ATTEMPT-LINEAGE-SCHEMA-V1",
                "mapping-attempt-v1.schema.json",
            ),
        ],
        "renderer_contract": {
            "semantics_version": RENDERER_SEMANTICS_VERSION,
            "participant_visible_output_authority": "RENDERED_SURFACE_CATALOG_ONLY",
            "fallback_policy": "FORBIDDEN",
            "semantic_source_direct_text_read": "FORBIDDEN",
            "catalog_membership_policy": "UNREGISTERED_OUTPUT_FORBIDDEN",
        },
        "event_schedule": schedule,
        "presentations": presentations,
        "future_options": future_options,
        "family_prompt_deliveries": family_prompts,
        "diagnostic_delivery_surface_id": "DELIVERY-PROMPT-POST-TRACE-DIAGNOSTIC-V1",
        "mapping_lineage_contract": {
            "attempt_dispositions": ["APPLIED", "NOT_APPLIED", "NOT_EVALUABLE"],
            "candidate_statuses": [
                "PROPOSED",
                "AMBIGUOUS",
                "NO_MAPPING",
                "OUTSIDE_VOCABULARY",
            ],
            "attempt_cardinality": "EXACTLY_ONE_PER_ELIGIBLE_R1_R2_EVENT",
            "applied_candidate_set_cardinality": "EXACTLY_ONE",
            "non_applied_candidate_set_cardinality": "ZERO",
            "ambiguous_alternative_cardinality": "AT_LEAST_TWO",
            "response_disposition_is_not_evaluability": True,
        },
        "confirmed_defect_refs_pending_repilot": [f"DR-{index:03d}" for index in range(1, 10)],
        "open_deferred_defect_refs": [f"DR-{index:03d}" for index in range(10, 14)],
        "rejected_defect_receipt_refs": ["DR-014"],
        "defect_resolution_claims": [],
        "prohibitions": [
            "NO_ACTUAL_PARTICIPANT_OR_MODEL_ACQUISITION",
            "NO_RESPONSE_TO_INTERNAL_TRACE_MAPPING",
            "NO_PLACEMENT_RESULT",
            "NO_OUT_OF_MODEL_ADJUDICATION",
            "NO_DEFECT_RESOLUTION_CLAIM_BEFORE_P1_V1",
            "NO_CLOSURE_OF_DEFERRED_DEFECTS",
            "NO_SEMANTIC_SOURCE_MUTATION",
            "NO_PARTICIPANT_TEXT_FALLBACK",
            "NO_DIRECT_SEMANTIC_SOURCE_TEXT_DELIVERY",
            "NO_REGISTRY_CLAIM_SUPPORT",
        ],
    }


def _build_manifest(files: dict[str, bytes], instrument: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        {
            "path": relpath,
            "role": "IMMUTABLE_P0_P1_OR_SEMANTIC_BASIS",
            "sha256": expected,
        }
        for relpath, expected in sorted(FROZEN_INPUT_SHA256.items())
    ]
    for filename, payload in sorted(files.items()):
        artifacts.append(
            {
                "path": f"research/scenarios/interp-dialogue-001/elicitation/p0-v1/{filename}",
                "role": (
                    "P0_V1_SCHEMA"
                    if filename.endswith(".schema.json")
                    else "P0_V1_FROZEN_ARTIFACT"
                ),
                "sha256": _sha256(payload),
            }
        )
    return {
        "$schema": "./frozen-artifact-manifest-v1.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "P0_V1_FROZEN_ARTIFACT_MANIFEST",
        "artifact_id": "INTERP-DIALOGUE-001P0-V1-FREEZE",
        "status": "FROZEN_UNEXECUTED",
        "authority": "DIGEST_ACCOUNTING_ONLY_NO_CLAIM_SUPPORT",
        "merge_basis": "PR17_MERGE_COMMIT_eb7f7e69afa8a78cdf0e5b5caf2ccad0a7574108",
        "confirmed_defect_refs_pending_repilot": instrument[
            "confirmed_defect_refs_pending_repilot"
        ],
        "open_deferred_defect_refs": instrument["open_deferred_defect_refs"],
        "rejected_defect_receipt_refs": instrument[
            "rejected_defect_receipt_refs"
        ],
        "defect_resolution_claims": [],
        "artifacts": artifacts,
    }


def build_all(root: Path = ROOT) -> dict[str, bytes]:
    verify_frozen_inputs(root)
    files = {name: _pretty_bytes(schema) for name, schema in _schemas().items()}

    surface = _build_participant_surface(root)
    surface_bytes = _pretty_bytes(surface)
    candidates = _build_candidates(surface, root)
    candidate_bytes = _pretty_bytes(candidates)
    decisions = _build_decisions(candidates, candidate_bytes)
    decision_bytes = _pretty_bytes(decisions)
    dispositions = _build_proposal_dispositions(candidates, decisions)
    disposition_bytes = _pretty_bytes(dispositions)
    catalog = _build_rendered_catalog(surface, surface_bytes, root)
    catalog_bytes = _pretty_bytes(catalog)

    files.update(
        {
            "revision-resolution-candidates-v1.json": candidate_bytes,
            "p0-decision-receipts-v1.json": decision_bytes,
            "proposal-disposition-record-v1.json": disposition_bytes,
            "participant-surface-v1.json": surface_bytes,
            "rendered-surface-catalog-v1.json": catalog_bytes,
        }
    )
    instrument = _build_instrument(
        files=files,
        surface=surface,
        catalog=catalog,
        root=root,
    )
    instrument_bytes = _pretty_bytes(instrument)
    files["instrument-v1.json"] = instrument_bytes
    manifest = _build_manifest(files, instrument)
    files["frozen-artifact-manifest-v1.json"] = _pretty_bytes(manifest)
    validate_built_artifacts(files, root=root)
    return files


def _validate_file(
    files: dict[str, bytes], artifact_name: str, schema_name: str
) -> dict[str, Any]:
    artifact = loads_exact(files[artifact_name])
    schema = loads_exact(files[schema_name])
    try:
        validate_json_schema(artifact, schema)
    except ValueError as exc:
        raise P0V1ContractError(
            f"{artifact_name} schema validation failed: {exc}"
        ) from exc
    return artifact


def validate_mapping_candidate_set(value: dict[str, Any], schema: dict[str, Any]) -> None:
    validate_json_schema(value, schema)
    status = value["candidate_status"]
    count = len(value["alternatives"])
    if status == "PROPOSED" and count != 1:
        _fail("PROPOSED mapping candidate set requires exactly one alternative")
    if status == "AMBIGUOUS" and count < 2:
        _fail("AMBIGUOUS mapping candidate set requires at least two alternatives")
    if status in {"NO_MAPPING", "OUTSIDE_VOCABULARY"} and count != 0:
        _fail(f"{status} mapping candidate set requires zero alternatives")


def validate_mapping_attempt_ledger(
    value: dict[str, Any],
    schema: dict[str, Any],
    candidate_sets: dict[str, dict[str, Any]],
) -> None:
    validate_json_schema(value, schema)
    seen_events = set()
    for attempt in value["attempts"]:
        event_id = attempt["response_event_id"]
        if event_id in seen_events:
            _fail(f"mapping event has more than one attempt receipt: {event_id}")
        seen_events.add(event_id)
        disposition = attempt["attempt_disposition"]
        candidate_ref = attempt["candidate_set_ref"]
        if disposition == "APPLIED":
            if not candidate_ref or candidate_ref not in candidate_sets:
                _fail("APPLIED mapping attempt requires exactly one candidate set")
        elif candidate_ref:
            _fail(f"{disposition} mapping attempt must not reference a candidate set")
        if (
            attempt["payload_evaluability"] != "EVALUABLE"
            and disposition != "NOT_EVALUABLE"
        ):
            _fail("non-evaluable payload requires NOT_EVALUABLE attempt disposition")


def validate_built_artifacts(files: dict[str, bytes], *, root: Path = ROOT) -> None:
    surface = _validate_file(
        files, "participant-surface-v1.json", "participant-surface-v1.schema.json"
    )
    candidates = _validate_file(
        files,
        "revision-resolution-candidates-v1.json",
        "revision-resolution-candidates-v1.schema.json",
    )
    decisions = _validate_file(
        files, "p0-decision-receipts-v1.json", "p0-decision-receipts-v1.schema.json"
    )
    dispositions = _validate_file(
        files,
        "proposal-disposition-record-v1.json",
        "proposal-disposition-record-v1.schema.json",
    )
    catalog = _validate_file(
        files,
        "rendered-surface-catalog-v1.json",
        "rendered-surface-catalog-v1.schema.json",
    )
    instrument = _validate_file(
        files, "instrument-v1.json", "instrument-v1.schema.json"
    )
    manifest = _validate_file(
        files,
        "frozen-artifact-manifest-v1.json",
        "frozen-artifact-manifest-v1.schema.json",
    )

    source_artifacts = _source_artifacts(root)
    candidate_ids = set()
    operation_ids = set()
    proposal_ids = set()
    for candidate in candidates["candidates"]:
        candidate_id = candidate["resolution_candidate_id"]
        if candidate_id in candidate_ids:
            _fail(f"duplicate resolution candidate: {candidate_id}")
        candidate_ids.add(candidate_id)
        proposal_ids.add(candidate["source_proposal_id"])
        for operation in candidate["operations"]:
            operation_id = operation["operation_id"]
            if operation_id in operation_ids:
                _fail(f"duplicate revision operation: {operation_id}")
            operation_ids.add(operation_id)
            for basis in operation["basis_refs"]:
                artifact_id = basis["artifact_id"]
                if artifact_id not in source_artifacts:
                    _fail(f"unknown immutable basis artifact: {artifact_id}")
                relpath, source = source_artifacts[artifact_id]
                if basis["artifact_path"] != relpath:
                    _fail(f"basis path mismatch: {artifact_id}")
                value = _resolve_pointer(source, basis["json_pointer"])
                if basis["value_canonical_sha256"] != _basis_value_sha256(value):
                    _fail(f"basis value digest mismatch: {operation_id}")
    if proposal_ids != {f"RP-{index:03d}" for index in range(1, 9)}:
        _fail("resolution candidates do not cover all eight P1 proposals")

    decisions_by_candidate = {}
    for receipt in decisions["decision_receipts"]:
        candidate_id = receipt["resolution_candidate_id"]
        if candidate_id in decisions_by_candidate:
            _fail(f"candidate has more than one decision: {candidate_id}")
        decisions_by_candidate[candidate_id] = receipt
        candidate = next(
            item for item in candidates["candidates"]
            if item["resolution_candidate_id"] == candidate_id
        )
        expected_operations = {
            item["operation_id"] for item in candidate["operations"]
        }
        applied_operations = set(receipt["applied_operation_ids"])
        if receipt["decision"] == "ACCEPTED":
            if applied_operations != expected_operations:
                _fail(f"decision operation coverage mismatch: {candidate_id}")
            if (
                receipt["execution_status"]
                != "ADOPTED_IN_FROZEN_P0_V1_NOT_REPILOTED"
            ):
                _fail(f"accepted candidate has wrong execution status: {candidate_id}")
        else:
            if applied_operations:
                _fail(f"non-accepted candidate cannot apply operations: {candidate_id}")
            expected_status = {
                "REJECTED": "REJECTED_NOT_APPLIED",
                "DEFERRED": "DEFERRED_NOT_APPLIED",
            }[receipt["decision"]]
            if receipt["execution_status"] != expected_status:
                _fail(f"non-accepted candidate has wrong execution status: {candidate_id}")
    if set(decisions_by_candidate) != candidate_ids:
        _fail("every exact candidate must have exactly one decision receipt")

    destination_artifacts = {
        "PARTICIPANT-SURFACE-V1": surface,
        "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V1": instrument,
    }
    for candidate in candidates["candidates"]:
        receipt = decisions_by_candidate[candidate["resolution_candidate_id"]]
        if receipt["decision"] != "ACCEPTED":
            continue
        for operation in candidate["operations"]:
            destination = operation["destination"]
            artifact_id = destination["artifact_id"]
            if artifact_id not in destination_artifacts:
                _fail(f"unknown accepted destination artifact: {artifact_id}")
            actual = _resolve_pointer(
                destination_artifacts[artifact_id], destination["json_pointer"]
            )
            if canonical_bytes(actual) != canonical_bytes(
                operation["replacement_value"]
            ):
                _fail(
                    "accepted operation does not equal frozen destination value: "
                    f"{operation['operation_id']}"
                )

    disposition_proposals = {
        item["source_proposal_id"] for item in dispositions["proposal_dispositions"]
    }
    if disposition_proposals != proposal_ids:
        _fail("proposal disposition record does not cover all proposals")

    expected_factor_keys = set()
    for family_id, relpath in FAMILY_PATHS.items():
        family = _load(relpath, root)
        for factor in family["factors"]:
            for level in factor["levels"]:
                expected_factor_keys.add(
                    (family_id, factor["factor_id"], level["level_id"])
                )
    actual_factor_keys = {
        (item["family_id"], item["factor_id"], item["level_id"])
        for item in surface["factor_level_surfaces"]
    }
    if actual_factor_keys != expected_factor_keys:
        _fail("participant surface factor coverage is not closed-world")
    if {item["family_id"] for item in surface["base_surfaces"]} != set(FAMILY_PATHS):
        _fail("participant surface base coverage is not closed-world")
    if len({item["future_option_id"] for item in surface["future_option_surfaces"]}) != 6:
        _fail("participant surface future-option coverage is not closed-world")
    if len({(item["family_id"], item["prompt_role"]) for item in surface["prompt_surfaces"]}) != 6:
        _fail("participant surface family prompt coverage is not closed-world")

    forbidden = {
        "at a new access",
        "prior-material cue",
        "external target evidence",
        "evaluation threat",
        "bodily arousal",
        "the vignette",
        "independently resolved as following",
    }
    participant_texts = [
        item["participant_text"]
        for collection in (
            "base_surfaces",
            "factor_level_surfaces",
            "future_option_surfaces",
            "prompt_surfaces",
            "diagnostic_surfaces",
        )
        for item in surface[collection]
    ]
    for text in participant_texts:
        folded = text.casefold()
        leaked = [term for term in forbidden if term in folded]
        if leaked:
            _fail(f"participant surface leaks prohibited design language: {leaked}")

    rebuilt_catalog = _build_rendered_catalog(
        surface, files["participant-surface-v1.json"], root
    )
    if canonical_bytes(rebuilt_catalog) != canonical_bytes(catalog):
        _fail("rendered surface catalog is not a deterministic rebuild")
    if len(catalog["deliveries"]) != 37:
        _fail("rendered catalog must contain exactly 37 delivery surfaces")
    delivery_ids = set()
    for delivery in catalog["deliveries"]:
        delivery_id = delivery["delivery_surface_id"]
        if delivery_id in delivery_ids:
            _fail(f"duplicate rendered delivery: {delivery_id}")
        delivery_ids.add(delivery_id)
        raw = base64.b64decode(delivery["utf8_base64"], validate=True)
        if raw != delivery["participant_text"].encode("utf-8"):
            _fail(f"rendered delivery byte/text mismatch: {delivery_id}")
        if len(raw) != delivery["utf8_byte_length"]:
            _fail(f"rendered delivery byte length mismatch: {delivery_id}")
        if _sha256(raw) != delivery["utf8_sha256"]:
            _fail(f"rendered delivery digest mismatch: {delivery_id}")

    referenced_delivery_ids = {
        item["delivery_surface_id"] for item in instrument["presentations"]
    } | {
        item["delivery_surface_id"] for item in instrument["future_options"]
    } | {
        item[key]
        for item in instrument["family_prompt_deliveries"]
        for key in (
            "immediate_delivery_surface_id",
            "later_delivery_surface_id",
        )
    } | {instrument["diagnostic_delivery_surface_id"]}
    if referenced_delivery_ids != delivery_ids:
        _fail("instrument does not close exactly over the rendered delivery catalog")

    if instrument["defect_resolution_claims"]:
        _fail("P0-v1 cannot issue defect-resolution claims")
    if manifest["defect_resolution_claims"]:
        _fail("P0-v1 manifest cannot issue defect-resolution claims")
    if instrument["open_deferred_defect_refs"] != [
        "DR-010",
        "DR-011",
        "DR-012",
        "DR-013",
    ]:
        _fail("P0-v1 must preserve all four acquisition-side deferred defects")

    manifest_entries = {item["path"]: item for item in manifest["artifacts"]}
    for relpath, expected in FROZEN_INPUT_SHA256.items():
        if manifest_entries.get(relpath, {}).get("sha256") != expected:
            _fail(f"manifest lost frozen basis digest: {relpath}")
    for filename, payload in files.items():
        if filename == "frozen-artifact-manifest-v1.json":
            continue
        relpath = f"research/scenarios/interp-dialogue-001/elicitation/p0-v1/{filename}"
        if manifest_entries.get(relpath, {}).get("sha256") != _sha256(payload):
            _fail(f"manifest P0-v1 digest mismatch: {filename}")


def write_all(root: Path = ROOT) -> list[str]:
    files = build_all(root)
    written = []
    for filename, payload in files.items():
        target = root / "research/scenarios/interp-dialogue-001/elicitation/p0-v1" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        written.append(str(target.relative_to(root).as_posix()))
    return written


def verify_all(root: Path = ROOT) -> None:
    files = build_all(root)
    for filename, expected in files.items():
        target = root / "research/scenarios/interp-dialogue-001/elicitation/p0-v1" / filename
        if not target.exists():
            _fail(f"P0-v1 artifact is missing: {target.relative_to(root)}")
        if target.read_bytes() != expected:
            _fail(f"P0-v1 artifact differs from deterministic rebuild: {filename}")
