from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from dynamics.labs.interp_dialogue_scenario_contract import (
    load_and_validate_family,
    loads_exact,
)
from dynamics.labs.interp_dialogue_trace_oracle_contract import (
    load_and_validate_trace_oracle,
)
from dynamics.labs.interp_m1_common import (
    digest,
    file_sha256,
    validate_json_schema,
)


_ROOT = Path(__file__).resolve().parents[2]
_ELICITATION_ROOT = (
    _ROOT / "research" / "scenarios" / "interp-dialogue-001" / "elicitation"
)
_DEFAULT_INSTRUMENT_PATH = _ELICITATION_ROOT / "instrument-v0.json"
_DEFAULT_SCHEMA_PATH = _ELICITATION_ROOT / "instrument.schema.json"

FROZEN_INSTRUMENT_SHA256 = (
    "52705bc686a69d43360eb0544eda59571c77dc1e29520ec4b156bcd60f413776"
)
FROZEN_INSTRUMENT_SCHEMA_SHA256 = (
    "0023386d724864c7890cdac14807782a347edc741ad5613a3687d68363f92c89"
)

_EXPECTED_SOURCES = {
    "REL-BOUNDARY-001": (
        "SCENARIO_FAMILY",
        "../families/rel-boundary.json",
        "4eb342e655ded940ab8537f4e7827692829967a35f17feb375e731a24d2750e2",
    ),
    "WORK-FEEDBACK-001": (
        "SCENARIO_FAMILY",
        "../families/work-feedback.json",
        "71cedb46667d1fc2ab76ee1e9711e8f0344e3fea6cf9bd16b577643d292d5823",
    ),
    "RISK-FOOTSTEPS-001": (
        "SCENARIO_FAMILY",
        "../families/risk-footsteps.json",
        "4fbe69cbe8bd8edb631c9012810dbf935b69f10d5afa7c670638177eabb2a256",
    ),
    "INTERP-DIALOGUE-001B-TRACE-ORACLE-V1": (
        "TRACE_ORACLE",
        "../trace-oracle-v1.json",
        "9caefdf39b9ac41c355f8afed0f4c5d0f780499f571346ef2a7042fa30da74b9",
    ),
}

_EXPECTED_PROMPTS = {
    "P_GENERIC_IMMEDIATE_RESPONSE": (
        "GENERIC_IMMEDIATE_RESPONSE",
        "ELICITS_SURFACE_RESPONSE_NOT_INTERNAL_STATE",
    ),
    "P_GENERIC_LATER_RESPONSE": (
        "GENERIC_LATER_RESPONSE",
        "ELICITS_SURFACE_RESPONSE_NOT_INTERNAL_STATE",
    ),
    "P_POST_TRACE_DIAGNOSTIC": (
        "POST_TRACE_DIAGNOSTIC",
        "RETROSPECTIVE_DIAGNOSTIC_NOT_ORDINAL_OBSERVATION",
    ),
}

_EXPECTED_SCHEDULE = (
    ("E0_INITIAL_VIGNETTE_DELIVERY", 0, "STIMULUS_DELIVERY", True,
     "RENDERED_INITIAL_PRESENTATION"),
    ("E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY", 1, "PROMPT_DELIVERY",
     True, "P_GENERIC_IMMEDIATE_RESPONSE"),
    ("R1_IMMEDIATE_RESPONSE_EVENT", 2, "SCRIPTED_RESPONSE_RECORD", True,
     "SESSION_IMMEDIATE_RESPONSE"),
    ("E2_MATCHED_FUTURE_OPTION_DELIVERY", 3, "STIMULUS_DELIVERY", True,
     "SELECTED_REGISTERED_FUTURE_OPTION"),
    ("E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY", 4, "PROMPT_DELIVERY", True,
     "P_GENERIC_LATER_RESPONSE"),
    ("R2_LATER_RESPONSE_EVENT", 5, "SCRIPTED_RESPONSE_RECORD", True,
     "SESSION_LATER_RESPONSE"),
    ("D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY", 6, "PROMPT_DELIVERY", False,
     "P_POST_TRACE_DIAGNOSTIC"),
    ("RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT", 7,
     "SCRIPTED_RESPONSE_RECORD", False,
     "SESSION_POST_TRACE_DIAGNOSTIC_RESPONSE"),
)

_EXPECTED_RESPONSE_STATUSES = {
    "RESPONDED",
    "REFUSED",
    "NO_RESPONSE",
    "TECHNICAL_FAILURE",
}

_EXPECTED_RESPONSE_STATUS_MEANINGS = {
    "RESPONDED": (
        "The scripted development source includes an explicit response record "
        "and its exact raw UTF-8 payload is preserved."
    ),
    "REFUSED": (
        "The scripted development source explicitly marks refusal; refusal is "
        "not inferred from response text."
    ),
    "NO_RESPONSE": (
        "The scripted development source explicitly represents a closed response "
        "window with no submit or refusal record."
    ),
    "TECHNICAL_FAILURE": (
        "The scripted development source explicitly represents response collection "
        "or recording failure; this is not refusal, no response, or an "
        "internal-state value."
    ),
}

_EXPECTED_SOURCE_KINDS = {"SCRIPTED_ADVERSARIAL_RESPONSE"}

_EXPECTED_MECHANICAL_CODES = {
    "DESIGN_ANCHOR_LITERAL_LEAK",
    "INTERNAL_IDENTIFIER_LITERAL_LEAK",
    "DELIVERY_PAYLOAD_MISMATCH",
    "SESSION_BINDING_MISMATCH",
    "MATCHED_FUTURE_OPTION_MISMATCH",
    "MATCHED_COMPARISON_BINDING_MISMATCH",
    "UNLOGGED_PROMPT_DELIVERY",
    "PROMPT_ORDER_VIOLATION",
    "MISSINGNESS_COLLAPSE",
    "RAW_PAYLOAD_PROVENANCE_BREAK",
    "RESPONSE_PROVENANCE_LINK_MISMATCH",
    "POST_TRACE_DIAGNOSTIC_EARLY_DELIVERY",
}

_EXPECTED_STRUCTURAL_REJECTION_CODES = {"FORCED_INTERNAL_TRACE_CAST"}

_EXPECTED_ANALYST_CODES = {
    "AMBIGUOUS_ITEM",
    "MULTI_FACTOR_WORDING",
    "PARTICIPANT_BURDEN",
    "UNNATURAL_LANGUAGE",
    "ANCHORING_RISK",
    "MAPPING_UNDERSPECIFIED",
    "TRANSLATION_SEMANTIC_DRIFT",
    "PERSPECTIVE_AMBIGUITY",
    "TEMPORAL_ORDER_UNCLEAR",
}

_EXPECTED_PROHIBITIONS = {
    "NO_MEASUREMENT_CLAIM",
    "NO_RESPONSE_TO_INTERNAL_TRACE_DIRECT_CAST",
    "NO_FIRST_PERSON_ATTESTATION_FROM_SCENARIO_JUDGMENT",
    "NO_EXTERNAL_IDENTITY_OR_INTENTION_CERTIFICATION",
    "NO_CANDIDATE_ANCHOR_EXPOSURE",
    "NO_STRUCTURED_OR_RETROSPECTIVE_PROMPT_BEFORE_R2",
    "NO_DIFFERENT_FUTURE_OPTION_IN_MATCHED_COMPARISON",
    "NO_OUT_OF_MODEL_CLASSIFICATION_BY_RUNNER",
    "NO_DEFECT_CLASSIFICATION_BY_RUNNER",
    "NO_ORACLE_OBSERVATION_STATUS_WITHOUT_FROZEN_MAPPING",
    "NO_PLACEMENT_WINNER",
    "NO_CLAIM_EVIDENCE_OR_SUPPORT_PROMOTION",
    "NO_DURABLE_TARGETFORM_EPISODE_OR_NARRATIVE_WRITE",
    "NO_RAW_RESPONSE_NORMALIZATION_OR_DISCARD",
    "NO_RESPONSE_STATUS_COLLAPSE",
    "NO_INSTRUMENT_REVISION_ADOPTION_IN_P1",
}


class ElicitationInstrumentContractError(ValueError):
    """Raised when the frozen P0-v0 elicitation contract drifts."""


def _fail(message: str) -> None:
    raise ElicitationInstrumentContractError(message)


@dataclass(frozen=True, slots=True)
class CompiledInstrumentContext:
    """Process-local compiled view of one verified frozen instrument graph.

    The context is an execution optimization and carries no research or claim
    authority. Parsed source objects stay private; callers receive only
    read-only indexes and use the rendering helpers below.
    """

    context_id: str
    compiler_semantics_version: str
    canonicalization_profile_id: str
    instrument_sha256: str
    source_bindings: tuple[tuple[str, str, str], ...]
    _instrument: dict[str, Any]
    _families: Mapping[str, dict[str, Any]]
    _oracle: dict[str, Any]
    _presentations: Mapping[str, dict[str, Any]]
    _future_options: Mapping[str, dict[str, Any]]
    _prompts: Mapping[str, dict[str, Any]]
    _comparisons: Mapping[str, dict[str, Any]]

    @property
    def instrument(self) -> Mapping[str, Any]:
        return MappingProxyType(self._instrument)

    @property
    def families(self) -> Mapping[str, dict[str, Any]]:
        return self._families

    @property
    def oracle(self) -> Mapping[str, Any]:
        return MappingProxyType(self._oracle)

    @property
    def presentations(self) -> Mapping[str, dict[str, Any]]:
        return self._presentations

    @property
    def future_options(self) -> Mapping[str, dict[str, Any]]:
        return self._future_options

    @property
    def prompts(self) -> Mapping[str, dict[str, Any]]:
        return self._prompts

    @property
    def comparisons(self) -> Mapping[str, dict[str, Any]]:
        return self._comparisons


def load_instrument(
    path: str | Path = _DEFAULT_INSTRUMENT_PATH,
) -> dict[str, Any]:
    try:
        return loads_exact(Path(path).read_bytes())
    except ValueError as exc:
        raise ElicitationInstrumentContractError(str(exc)) from exc


def _unique_index(
    records: Iterable[dict[str, Any]], key: str, label: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        value = record[key]
        if value in result:
            _fail(f"duplicate {label}: {value}")
        result[value] = record
    return result


def _validate_schema(
    instrument: dict[str, Any], schema_path: str | Path | None
) -> None:
    resolved_schema_path = Path(schema_path or _DEFAULT_SCHEMA_PATH)
    if file_sha256(resolved_schema_path) != FROZEN_INSTRUMENT_SCHEMA_SHA256:
        _fail("instrument schema is not the frozen P0-v0 schema")
    schema = load_instrument(resolved_schema_path)
    try:
        validate_json_schema(instrument, schema)
    except ValueError as exc:
        raise ElicitationInstrumentContractError(
            f"schema validation failed: {exc}"
        ) from exc


def _load_bound_sources(
    instrument: dict[str, Any], instrument_path: str | Path
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    source_records = _unique_index(
        instrument["bound_source_artifacts"], "source_id", "source binding"
    )
    if set(source_records) != set(_EXPECTED_SOURCES):
        _fail("bound source IDs changed")

    root = Path(instrument_path).resolve().parent
    families: dict[str, dict[str, Any]] = {}
    oracle: dict[str, Any] | None = None
    for source_id, (role, relative_path, expected_sha) in _EXPECTED_SOURCES.items():
        record = source_records[source_id]
        if (
            record["role"] != role
            or record["path"] != relative_path
            or record["content_sha256"] != expected_sha
        ):
            _fail(f"{source_id} binding changed")
        path = (root / relative_path).resolve()
        if file_sha256(path) != expected_sha:
            _fail(f"{source_id} raw-byte digest mismatch")
        if role == "SCENARIO_FAMILY":
            family = load_and_validate_family(path)
            if family["family_id"] != source_id:
                _fail(f"{source_id} family identity mismatch")
            families[source_id] = family
        else:
            oracle = load_and_validate_trace_oracle(path)

    if oracle is None:
        _fail("trace oracle binding missing")
    oracle_bindings = {
        item["family_id"]: item["content_sha256"]
        for item in oracle["bound_family_files"]
    }
    expected_family_digests = {
        source_id: source[2]
        for source_id, source in _EXPECTED_SOURCES.items()
        if source[0] == "SCENARIO_FAMILY"
    }
    if oracle_bindings != expected_family_digests:
        _fail("oracle and instrument family bindings disagree")
    return families, oracle


def _validate_prompts_and_schedule(instrument: dict[str, Any]) -> None:
    prompts = _unique_index(instrument["prompt_catalog"], "prompt_id", "prompt")
    if set(prompts) != set(_EXPECTED_PROMPTS):
        _fail("prompt catalog changed")
    for prompt_id, (role, authority) in _EXPECTED_PROMPTS.items():
        prompt = prompts[prompt_id]
        if prompt["role"] != role or prompt["authority"] != authority:
            _fail(f"{prompt_id} role or authority changed")
        if not prompt["participant_text"].isascii():
            _fail(f"{prompt_id} is not an English-v0 ASCII rendering")

    schedule = tuple(
        (
            step["step_id"],
            step["sequence_ordinal"],
            step["event_kind"],
            step["required"],
            step["payload_source"],
        )
        for step in instrument["event_schedule"]
    )
    if schedule != _EXPECTED_SCHEDULE:
        _fail("elicitation schedule changed")
    if any(step_id.startswith("O") for step_id, *_ in schedule):
        _fail("elicitation steps cannot use the oracle O namespace")

    statuses = {
        item["status"] for item in instrument["response_status_vocabulary"]
    }
    if statuses != _EXPECTED_RESPONSE_STATUSES:
        _fail("response status vocabulary changed")
    meanings = {
        item["status"]: item["meaning"]
        for item in instrument["response_status_vocabulary"]
    }
    if meanings != _EXPECTED_RESPONSE_STATUS_MEANINGS:
        _fail("response status meanings changed")
    if set(instrument["development_source_kinds"]) != _EXPECTED_SOURCE_KINDS:
        _fail("development source kinds changed")


def _validate_presentations(
    instrument: dict[str, Any], families: dict[str, dict[str, Any]]
) -> None:
    presentations = _unique_index(
        instrument["presentations"], "presentation_id", "presentation"
    )
    if len(presentations) != 24:
        _fail("presentations must cover exactly 24 source cells")

    covered: set[tuple[str, str]] = set()
    for presentation in presentations.values():
        family_id = presentation["family_id"]
        if family_id not in families:
            _fail(f"unknown presentation family: {family_id}")
        cells = {
            cell["cell_id"]: cell for cell in families[family_id]["cells"]
        }
        cell_id = presentation["source_cell_id"]
        if cell_id not in cells:
            _fail(f"unknown source cell: {cell_id}")
        coordinate = (family_id, cell_id)
        if coordinate in covered:
            _fail(f"source cell covered more than once: {coordinate}")
        covered.add(coordinate)
        if presentation["factor_level_bindings"] != cells[cell_id]["factor_levels"]:
            _fail(f"{presentation['presentation_id']} factor binding drifted")

    expected = {
        (family_id, cell["cell_id"])
        for family_id, family in families.items()
        for cell in family["cells"]
    }
    if covered != expected:
        _fail("presentation coverage does not equal the 24 source cells")


def _validate_rendering_policy(
    instrument: dict[str, Any], families: dict[str, dict[str, Any]]
) -> None:
    policy = instrument["rendering_policy"]
    if policy["initial_block_order"] != [
        "BASE_SURFACE", "FACTOR_LEVELS_IN_SOURCE_ORDER"
    ]:
        _fail("initial rendering order changed")
    bases = _unique_index(
        policy["base_surface_by_family"], "family_id", "base-surface rendering"
    )
    if set(bases) != set(families):
        _fail("base-surface rendering coverage changed")
    if instrument["language_policy"] != {
        "participant_locale": "en",
        "source_descriptor_policy": "VERBATIM_BOUND_SOURCE_TEXT",
        "source_future_option_policy": "VERBATIM_BOUND_SOURCE_TEXT",
        "base_surface_translation_authority":
            "AUTHOR_RENDERED_INSTRUMENT_TEXT_NOT_CERTIFIED_EQUIVALENCE",
        "mixed_locale_source_text_forbidden": True,
    }:
        _fail("language policy changed")
    for presentation in instrument["presentations"]:
        text = render_initial_presentation(
            instrument,
            presentation["presentation_id"],
            families=families,
        )
        if not text.isascii():
            _fail("English v0 initial rendering contains non-ASCII source text")


def _validate_future_options(
    instrument: dict[str, Any], oracle: dict[str, Any]
) -> None:
    oracle_futures = _unique_index(
        oracle["matched_future_oracles"], "family_id", "oracle future family"
    )
    options = _unique_index(
        instrument["future_option_catalog"], "future_option_id", "future option"
    )
    if len(options) != 6:
        _fail("future option catalog must contain six entries")
    expected_options: set[tuple[str, str, int]] = set()
    for future in oracle_futures.values():
        for index in range(future["source_option_count"]):
            expected_options.add(
                (future["family_id"], future["source_probe_id"], index)
            )
    actual_options = {
        (item["family_id"], item["source_probe_id"], item["source_option_index"])
        for item in options.values()
    }
    if actual_options != expected_options:
        _fail("future option catalog drifted from 001B")
    for future in oracle_futures.values():
        if any(
            not option.isascii()
            for option in future["source_probe_snapshot"]["probe_options"]
        ):
            _fail("English v0 future option contains non-ASCII source text")

    comparisons = _unique_index(
        instrument["matched_future_comparisons"], "comparison_id", "comparison"
    )
    expected_comparison_ids = {
        item["oracle_id"] for item in oracle["matched_future_oracles"]
    }
    if set(comparisons) != expected_comparison_ids:
        _fail("matched future comparison IDs changed")
    option_lookup = {
        (item["family_id"], item["source_option_index"]): item["future_option_id"]
        for item in options.values()
    }
    for future in oracle["matched_future_oracles"]:
        comparison = comparisons[future["oracle_id"]]
        expected_pairs = [
            [
                option_lookup[(future["family_id"], arm["left_option_index"])],
                option_lookup[(future["family_id"], arm["right_option_index"])],
            ]
            for arm in future["matched_option_arms"]
        ]
        if comparison != {
            "comparison_id": future["oracle_id"],
            "family_id": future["family_id"],
            "left_prior_cell_id": future["compared_prior_cell_ids"][0],
            "right_prior_cell_id": future["compared_prior_cell_ids"][1],
            "allowed_matched_option_pairs": expected_pairs,
        }:
            _fail(f"{future['oracle_id']} comparison binding drifted")


def _validate_authority_boundaries(instrument: dict[str, Any]) -> None:
    if instrument["authority"] != {
        "artifact_role": "DEVELOPMENT_ELICITATION_INSTRUMENT_CONTRACT",
        "execution_status": "UNEXECUTED",
        "measurement_status": "NO_FROZEN_RESPONSE_TO_INTERNAL_TRACE_MAPPING",
        "empirical_status": "NO_RESPONSE_DATA",
        "output_status": "NO_OBSERVATION_PLACEMENT_OR_CLAIM_RESULT",
    }:
        _fail("instrument authority changed")
    if instrument["response_provenance_contract"] != {
        "payload_encoding": "BASE64_OF_EXACT_UTF8_BYTES",
        "normalization": "NONE",
        "receipt_authority": (
            "SCRIPTED_RESPONSE_RECORD_AND_PAYLOAD_PROVENANCE_ONLY"
        ),
        "response_proves": [
            "A_SCRIPTED_RESPONSE_RECORD_WITH_THIS_STATUS_FOLLOWS_THE_RECORDED_"
            "PROMPT_DELIVERY_IN_THE_MATERIALIZED_TRANSCRIPT",
            "A_PRESENT_RAW_PAYLOAD_HAS_THE_RECORDED_BYTE_LENGTH_AND_SHA256",
        ],
        "response_does_not_prove": [
            "ACTUAL_PARTICIPANT_DELIVERY_OR_RESPONSE_OCCURRENCE",
            "INTERNAL_TRACE_RESIDENCE",
            "TARGETFORM_OR_GHOST_STATE",
            "EXTERNAL_TARGET_IDENTITY_INTENTION_OR_TRUTH",
            "GENERAL_HUMAN_MECHANISM",
        ],
    }:
        _fail("response provenance authority changed")
    roles = _unique_index(
        instrument["processing_role_contract"], "role", "processing role"
    )
    expected_roles = {
        "SCRIPTED_REPLAY_MATERIALIZER": {
            "role": "SCRIPTED_REPLAY_MATERIALIZER",
            "may_emit": "IMMUTABLE_SCRIPTED_REPLAY_AND_PROVENANCE_ONLY",
            "may_not_emit": [
                "ACTUAL_PARTICIPANT_OCCURRENCE",
                "MAPPING",
                "DEFECT",
                "OUT_OF_MODEL",
                "OBSERVATION_STATUS",
                "PLACEMENT_RESULT",
            ],
        },
        "MECHANICAL_DEFECT_SCANNER": {
            "role": "MECHANICAL_DEFECT_SCANNER",
            "may_emit": "MECHANICAL_DEFECT_CANDIDATE_ONLY",
            "may_not_emit": [
                "INSTRUMENT_DEFECT_RECEIPT",
                "PASS_FAIL",
                "PLACEMENT_RESULT",
                "REVISION_ADOPTION",
            ],
        },
        "ANALYST_ADJUDICATOR": {
            "role": "ANALYST_ADJUDICATOR",
            "may_emit": (
                "EXPLICIT_INSTRUMENT_DEFECT_RECEIPT_UNDER_FUTURE_P1_ARTIFACT"
            ),
            "may_not_emit": [
                "AUTOMATIC_MECHANISM_TRUTH",
                "INSTRUMENT_REVISION_ADOPTION",
            ],
        },
    }
    if roles != expected_roles:
        _fail("processing role authority changed")
    if set(instrument["prohibitions"]) != _EXPECTED_PROHIBITIONS:
        _fail("prohibition set changed")
    taxonomy = instrument["defect_taxonomy"]
    mechanical = set(taxonomy["mechanical_candidate_codes"])
    structural = set(taxonomy["structural_rejection_codes"])
    analyst = set(taxonomy["analyst_only_codes"])
    if mechanical != _EXPECTED_MECHANICAL_CODES:
        _fail("mechanical defect candidate vocabulary changed")
    if structural != _EXPECTED_STRUCTURAL_REJECTION_CODES:
        _fail("structural rejection vocabulary changed")
    if analyst != _EXPECTED_ANALYST_CODES:
        _fail("analyst-only defect vocabulary changed")
    if mechanical & analyst or mechanical & structural or analyst & structural:
        _fail("defect and rejection vocabularies overlap")
    if taxonomy["scanner_output_authority"] != (
        "CANDIDATE_ONLY_NO_AUTOMATIC_DEFECT_RECEIPT"
    ):
        _fail("scanner authority changed")

    boundary = instrument["mapping_boundary"]
    if boundary["runner_mapping_output"] != "FORBIDDEN":
        _fail("runner gained mapping authority")
    expected_candidates = {
        (
            "R1_IMMEDIATE_RESPONSE_EVENT",
            "O5_IMMEDIATE_SURFACE_RECORDED",
            "immediate_surface",
        ),
        (
            "R2_LATER_RESPONSE_EVENT",
            "O10_LATER_SURFACE_RECORDED",
            "later_surface",
        ),
    }
    actual_candidates = {
        (
            item["response_step_id"],
            item["observation_point_id"],
            item["trace_field_id"],
        )
        for item in boundary["eligible_future_candidates"]
    }
    if actual_candidates != expected_candidates:
        _fail("eligible future mapping candidate coordinates changed")
    if any(
        item["authority"] != "DEVELOPMENT_MAPPING_CANDIDATE_ONLY"
        for item in boundary["eligible_future_candidates"]
    ):
        _fail("mapping candidate authority changed")
    if instrument["revision_proposal_contract"] != {
        "allowed_status": "PROPOSED_NOT_ADOPTED",
        "allowed_execution_status": "UNEXECUTED",
        "adoption_authority": "FUTURE_P0_VERSION_ONLY",
        "p1_may_execute_revised_instrument": False,
    }:
        _fail("revision proposal authority changed")


def validate_elicitation_instrument(
    instrument: dict[str, Any],
    *,
    instrument_path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    schema_path: str | Path | None = None,
) -> None:
    _validate_schema(instrument, schema_path)
    families, oracle = _load_bound_sources(instrument, instrument_path)
    _validate_instrument_with_bound_sources(instrument, families, oracle)


def _validate_instrument_with_bound_sources(
    instrument: dict[str, Any],
    families: dict[str, dict[str, Any]],
    oracle: dict[str, Any],
) -> None:
    _validate_prompts_and_schedule(instrument)
    _validate_presentations(instrument, families)
    _validate_rendering_policy(instrument, families)
    _validate_future_options(instrument, oracle)
    _validate_authority_boundaries(instrument)


def load_and_validate_elicitation_instrument(
    path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    *,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    if file_sha256(path) != FROZEN_INSTRUMENT_SHA256:
        _fail("instrument is not the frozen P0-v0 raw-byte artifact")
    instrument = load_instrument(path)
    validate_elicitation_instrument(
        instrument, instrument_path=path, schema_path=schema_path
    )
    return instrument


def compile_instrument_context(
    path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    *,
    schema_path: str | Path | None = None,
) -> CompiledInstrumentContext:
    """Read and verify the frozen source graph once, then build runtime indexes."""

    resolved_path = Path(path)
    if file_sha256(resolved_path) != FROZEN_INSTRUMENT_SHA256:
        _fail("instrument is not the frozen P0-v0 raw-byte artifact")
    instrument = load_instrument(resolved_path)
    _validate_schema(instrument, schema_path)
    families, oracle = _load_bound_sources(instrument, resolved_path)
    _validate_instrument_with_bound_sources(instrument, families, oracle)

    source_bindings = tuple(
        sorted(
            (
                item["role"],
                item["source_id"],
                item["content_sha256"],
            )
            for item in instrument["bound_source_artifacts"]
        )
    )
    compiler_semantics_version = "INTERP-DIALOGUE-CONTEXT-1.0.0"
    canonicalization_profile_id = "HM-CANONICAL-JSON-PY-V1"
    context_id = digest(
        {
            "domain": "COMPILED_INTERP_DIALOGUE_INSTRUMENT_CONTEXT",
            "compiler_semantics_version": compiler_semantics_version,
            "canonicalization_profile_id": canonicalization_profile_id,
            "instrument_sha256": FROZEN_INSTRUMENT_SHA256,
            "instrument_schema_sha256": FROZEN_INSTRUMENT_SCHEMA_SHA256,
            "source_bindings": [list(item) for item in source_bindings],
        }
    )
    return CompiledInstrumentContext(
        context_id=context_id,
        compiler_semantics_version=compiler_semantics_version,
        canonicalization_profile_id=canonicalization_profile_id,
        instrument_sha256=FROZEN_INSTRUMENT_SHA256,
        source_bindings=source_bindings,
        _instrument=instrument,
        _families=MappingProxyType(dict(families)),
        _oracle=oracle,
        _presentations=MappingProxyType(
            _unique_index(instrument["presentations"], "presentation_id", "presentation")
        ),
        _future_options=MappingProxyType(
            _unique_index(
                instrument["future_option_catalog"],
                "future_option_id",
                "future option",
            )
        ),
        _prompts=MappingProxyType(
            _unique_index(instrument["prompt_catalog"], "prompt_id", "prompt")
        ),
        _comparisons=MappingProxyType(
            _unique_index(
                instrument["matched_future_comparisons"],
                "comparison_id",
                "matched comparison",
            )
        ),
    )


def render_initial_presentation(
    instrument: dict[str, Any] | CompiledInstrumentContext,
    presentation_id: str,
    *,
    instrument_path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    families: dict[str, dict[str, Any]] | None = None,
) -> str:
    context = (
        instrument if isinstance(instrument, CompiledInstrumentContext) else None
    )
    raw_instrument = context._instrument if context is not None else instrument
    if context is not None:
        families = dict(context._families)
        presentations = context._presentations
    elif families is None:
        families, _ = _load_bound_sources(instrument, instrument_path)
        presentations = {
            item["presentation_id"]: item for item in instrument["presentations"]
        }
    else:
        presentations = {
            item["presentation_id"]: item for item in instrument["presentations"]
        }
    if presentation_id not in presentations:
        _fail(f"unknown presentation: {presentation_id}")
    presentation = presentations[presentation_id]
    family = families[presentation["family_id"]]
    factors = {item["factor_id"]: item for item in family["factors"]}
    descriptors: list[str] = []
    for factor in family["factors"]:
        level_id = presentation["factor_level_bindings"][factor["factor_id"]]
        levels = {item["level_id"]: item for item in factors[factor["factor_id"]]["levels"]}
        descriptors.append(levels[level_id]["descriptor"])
    bases = {
        item["family_id"]: item["participant_text"]
        for item in raw_instrument["rendering_policy"]["base_surface_by_family"]
    }
    policy = raw_instrument["rendering_policy"]
    factor_text = policy["factor_joiner"].join(
        policy["factor_line_prefix"] + descriptor for descriptor in descriptors
    )
    return bases[family["family_id"]] + policy["initial_joiner"] + factor_text


def render_future_option(
    instrument: dict[str, Any] | CompiledInstrumentContext,
    future_option_id: str,
    *,
    instrument_path: str | Path = _DEFAULT_INSTRUMENT_PATH,
) -> str:
    if isinstance(instrument, CompiledInstrumentContext):
        oracle = instrument._oracle
        options = instrument._future_options
    else:
        _, oracle = _load_bound_sources(instrument, instrument_path)
        options = {
            item["future_option_id"]: item
            for item in instrument["future_option_catalog"]
        }
    if future_option_id not in options:
        _fail(f"unknown future option: {future_option_id}")
    option = options[future_option_id]
    future = next(
        item
        for item in oracle["matched_future_oracles"]
        if item["family_id"] == option["family_id"]
    )
    return future["source_probe_snapshot"]["probe_options"][
        option["source_option_index"]
    ]


def prompt_text(
    instrument: dict[str, Any] | CompiledInstrumentContext, prompt_id: str
) -> str:
    prompts = (
        instrument._prompts
        if isinstance(instrument, CompiledInstrumentContext)
        else {item["prompt_id"]: item for item in instrument["prompt_catalog"]}
    )
    if prompt_id not in prompts:
        _fail(f"unknown prompt: {prompt_id}")
    return prompts[prompt_id]["participant_text"]
