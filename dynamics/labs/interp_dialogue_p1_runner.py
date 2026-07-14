"""INTERP-DIALOGUE-001P1-v0 — immutable scripted development pilot runner.

P1 replays the exact frozen P0-v0 development elicitation instrument with a
frozen scripted adversarial coverage manifest and response corpus. It only
composes the frozen P0 materializer and mechanical scanner; it does not modify
the instrument, does not create actual participant/model occurrences, does not
issue OUT_OF_MODEL or defect receipts, and does not adopt revisions.

scripted replay artifact != actual acquisition occurrence
mechanical/mapping candidate != instrument defect receipt or observation
"""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from typing import Any

from dynamics.labs.interp_dialogue_elicitation_runner import (
    encode_run,
    materialize_scripted_elicitation_replay,
)
from dynamics.labs.interp_dialogue_elicitation_contract import (
    CompiledInstrumentContext,
    compile_instrument_context,
)
from dynamics.labs.interp_dialogue_elicitation_scanner import (
    FROZEN_ASSESSMENT_SCHEMA_SHA256,
    encode_candidate_set,
    scan_mechanical_defects,
)
from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    loads_exact,
    validate_json_schema,
)

_ROOT = Path(__file__).resolve().parents[2]
_SCENARIO_ROOT = _ROOT / "research" / "scenarios" / "interp-dialogue-001"
_ELICITATION_ROOT = _SCENARIO_ROOT / "elicitation"
_P1_ROOT = _ELICITATION_ROOT / "p1"

MINIMUM_SESSION_COUNT = 30

# P1 uses these ten artifacts and must fail before materialization if any
# byte differs from the P0-v0 / 001A / 001B freeze.
FROZEN_INPUT_SHA256: dict[str, str] = {
    "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json": (
        "52705bc686a69d43360eb0544eda59571c77dc1e29520ec4b156bcd60f413776"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/instrument.schema.json": (
        "0023386d724864c7890cdac14807782a347edc741ad5613a3687d68363f92c89"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/session-input.schema.json": (
        "2474709b767c4146d64999e73454b6bdfbcf6989984fc1e1596deeead94df71e"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/run.schema.json": (
        "8c5cca613f6bf53e925e60013e5958f29244fb236b06cf70520736ac5cbcc56d"
    ),
    "research/scenarios/interp-dialogue-001/elicitation/development-assessment.schema.json": (
        "ac7cc68fb8c9618838f99e3c1ad9c120a79df313f22828c2b395300e2473b92f"
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
    "research/scenarios/interp-dialogue-001/trace-oracle.md": (
        "81b7699d3808497c06d86ee5961278a1ec5f4c1ad71fb9f32bfbc9c07db81a67"
    ),
}

_FAMILY_SOURCE_BY_ID = {
    "REL-BOUNDARY-001": "research/scenarios/interp-dialogue-001/families/rel-boundary.json",
    "WORK-FEEDBACK-001": "research/scenarios/interp-dialogue-001/families/work-feedback.json",
    "RISK-FOOTSTEPS-001": "research/scenarios/interp-dialogue-001/families/risk-footsteps.json",
}

_SLOT_BY_PHASE = {"immediate": "IMMEDIATE", "later": "LATER"}
_RESPONSE_EVENT_STEP = {
    "immediate": "R1_IMMEDIATE_RESPONSE_EVENT",
    "later": "R2_LATER_RESPONSE_EVENT",
}
_MAPPING_COORDINATE = {
    "immediate": {
        "source_phase": "IMMEDIATE",
        "eligible_target_coordinate": {
            "observation_point_id": "O5_IMMEDIATE_SURFACE_RECORDED",
            "trace_field_id": "immediate_surface",
        },
    },
    "later": {
        "source_phase": "LATER",
        "eligible_target_coordinate": {
            "observation_point_id": "O10_LATER_SURFACE_RECORDED",
            "trace_field_id": "later_surface",
        },
    },
}
MAPPING_RULE_CANDIDATE_VERSION = "P1V0-DEVELOPMENT-MAPPING-NOTES-V0"


class P1PilotContractError(ValueError):
    """Raised when the P1 pilot violates its frozen preregistration."""


def _fail(message: str) -> None:
    raise P1PilotContractError(message)


def _sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def verify_frozen_inputs(root: Path = _ROOT) -> None:
    for relpath, expected in FROZEN_INPUT_SHA256.items():
        actual = _sha256((root / relpath).read_bytes())
        if actual != expected:
            _fail(
                "frozen P0/001A/001B input byte mismatch before "
                f"materialization: {relpath}"
            )


def _validate_against(schema_path: Path, value: dict[str, Any], label: str) -> None:
    try:
        validate_json_schema(value, loads_exact(schema_path.read_bytes()))
    except ValueError as exc:
        raise P1PilotContractError(
            f"{label} schema validation failed: {exc}"
        ) from exc


def load_response_corpus(
    path: Path = _P1_ROOT / "response-corpus-v0.json",
) -> tuple[dict[str, Any], bytes]:
    corpus_bytes = path.read_bytes()
    corpus = loads_exact(corpus_bytes)
    _validate_against(
        path.parent / "response-corpus.schema.json", corpus, "response corpus"
    )
    seen: set[str] = set()
    for script in corpus["scripts"]:
        script_id = script["script_id"]
        if script_id in seen:
            _fail(f"duplicate response script: {script_id}")
        seen.add(script_id)
        if script["response_status"] == "RESPONDED":
            raw = script["payload_utf8"].encode("utf-8")
            if script["payload_byte_length"] != len(raw):
                _fail(f"script payload byte length drifted: {script_id}")
            if script["payload_sha256"] != _sha256(raw):
                _fail(f"script payload bytes drifted: {script_id}")
    return corpus, corpus_bytes


def _script_index(corpus: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {script["script_id"]: script for script in corpus["scripts"]}


def session_binding_digest(
    session: dict[str, Any], frozen_input_digests: dict[str, Any]
) -> str:
    unsigned = {
        key: value
        for key, value in session.items()
        if key != "session_binding_sha256"
    }
    return _sha256(
        canonical_bytes(
            {
                "session": unsigned,
                "frozen_input_digests": frozen_input_digests,
            }
        )
    )


def _check_script_slot(
    scripts: dict[str, dict[str, Any]], script_id: str, slot: str, where: str
) -> dict[str, Any]:
    if script_id not in scripts:
        _fail(f"unknown response script at {where}: {script_id}")
    script = scripts[script_id]
    if slot not in script["allowed_slots"]:
        _fail(f"script {script_id} is not allowed in slot {slot} at {where}")
    return script


def load_coverage_manifest(
    path: Path = _P1_ROOT / "coverage-manifest-v0.json",
    *,
    corpus: dict[str, Any] | None = None,
    corpus_bytes: bytes | None = None,
    root: Path = _ROOT,
    compiled_context: CompiledInstrumentContext | None = None,
) -> dict[str, Any]:
    if corpus is None or corpus_bytes is None:
        corpus, corpus_bytes = load_response_corpus(
            path.parent / "response-corpus-v0.json"
        )
    manifest = loads_exact(path.read_bytes())
    _validate_against(
        path.parent / "coverage-manifest.schema.json", manifest, "coverage manifest"
    )

    digests = manifest["frozen_input_digests"]
    expected = {
        "instrument_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json"
        ],
        "instrument_schema_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/elicitation/instrument.schema.json"
        ],
        "session_input_schema_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/elicitation/session-input.schema.json"
        ],
        "run_schema_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/elicitation/run.schema.json"
        ],
        "development_assessment_schema_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/elicitation/development-assessment.schema.json"
        ],
        "scenario_family_sha256": {
            family_id: FROZEN_INPUT_SHA256[relpath]
            for family_id, relpath in _FAMILY_SOURCE_BY_ID.items()
        },
        "trace_oracle_v1_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/trace-oracle-v1.json"
        ],
        "trace_oracle_doc_sha256": FROZEN_INPUT_SHA256[
            "research/scenarios/interp-dialogue-001/trace-oracle.md"
        ],
    }
    if digests != expected:
        _fail("coverage manifest does not bind the frozen P0-v0 input digests")
    binding = manifest["response_corpus_binding"]
    if binding["corpus_id"] != corpus["corpus_id"]:
        _fail("coverage manifest binds a different response corpus id")
    if binding["content_sha256"] != _sha256(corpus_bytes):
        _fail("coverage manifest binds different response corpus bytes")

    instrument = (
        compiled_context._instrument
        if compiled_context is not None
        else loads_exact(
            (
                root
                / "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json"
            ).read_bytes()
        )
    )
    presentations = {
        item["presentation_id"]: item for item in instrument["presentations"]
    }
    options = {
        item["future_option_id"]: item
        for item in instrument["future_option_catalog"]
    }
    comparisons = {
        item["comparison_id"]: item
        for item in instrument["matched_future_comparisons"]
    }
    scripts = _script_index(corpus)

    run_ids: set[str] = set()
    session_ids: set[str] = set()
    covered_presentations: set[str] = set()
    covered_options: set[str] = set()
    covered_statuses: set[str] = set()
    diagnostic_modes: set[str] = set()
    # comparison_id -> set of (arm, future_option_id) coverage
    comparison_coverage: dict[str, set[tuple[str, str]]] = {}
    session_count = 0

    for run in manifest["runs"]:
        run_id = run["run_id"]
        if run_id in run_ids:
            _fail(f"duplicate run_id: {run_id}")
        run_ids.add(run_id)
        group_arms: dict[str, set[str]] = {}
        for session in run["sessions"]:
            session_count += 1
            session_id = session["session_id"]
            where = f"{run_id}/{session_id}"
            if session_id in session_ids:
                _fail(f"duplicate session_id: {session_id}")
            session_ids.add(session_id)
            if session["session_binding_sha256"] != session_binding_digest(
                session, digests
            ):
                _fail(f"session binding digest mismatch at {where}")
            presentation = presentations.get(session["presentation_id"])
            if presentation is None:
                _fail(f"unknown presentation at {where}")
            if presentation["source_cell_id"] != session["source_cell_id"]:
                _fail(f"session cell does not match its presentation at {where}")
            option = options.get(session["future_option_id"])
            if option is None:
                _fail(f"unknown future option at {where}")
            if option["family_id"] != presentation["family_id"]:
                _fail(f"future option family mismatch at {where}")
            covered_presentations.add(session["presentation_id"])
            covered_options.add(session["future_option_id"])

            immediate = _check_script_slot(
                scripts, session["immediate_script_id"], "IMMEDIATE", where
            )
            later = _check_script_slot(
                scripts, session["later_script_id"], "LATER", where
            )
            covered_statuses.add(immediate["response_status"])
            covered_statuses.add(later["response_status"])
            diagnostic = session["post_trace_diagnostic"]
            diagnostic_modes.add(diagnostic["mode"])
            if diagnostic["mode"] == "COLLECTED_AFTER_R2":
                _check_script_slot(scripts, diagnostic["script_id"], "D0", where)

            comparison_binding = session["comparison_binding"]
            if comparison_binding["status"] == "PRESENT":
                comparison_id = comparison_binding["comparison_id"]
                comparison = comparisons.get(comparison_id)
                if comparison is None:
                    _fail(f"unknown matched comparison at {where}")
                arm = comparison_binding["arm"]
                expected_cell = comparison[
                    "left_prior_cell_id" if arm == "LEFT" else "right_prior_cell_id"
                ]
                if session["source_cell_id"] != expected_cell:
                    _fail(f"comparison arm cell mismatch at {where}")
                comparison_coverage.setdefault(comparison_id, set()).add(
                    (arm, session["future_option_id"])
                )
                arms = group_arms.setdefault(
                    comparison_binding["comparison_group_id"], set()
                )
                if arm in arms:
                    _fail(f"comparison group repeats arm at {where}")
                arms.add(arm)
        for group_id, arms in group_arms.items():
            if arms != {"LEFT", "RIGHT"}:
                _fail(
                    "comparison group must close both arms inside one run: "
                    f"{group_id}"
                )

    if session_count < MINIMUM_SESSION_COUNT:
        _fail(
            f"coverage manifest declares {session_count} sessions; "
            f"minimum is {MINIMUM_SESSION_COUNT}"
        )
    if covered_presentations != set(presentations):
        _fail("coverage manifest does not cover all 24 presentations")
    if covered_options != set(options):
        _fail("coverage manifest does not cover all 6 registered future options")
    if covered_statuses != {
        "RESPONDED",
        "REFUSED",
        "NO_RESPONSE",
        "TECHNICAL_FAILURE",
    }:
        _fail("coverage manifest does not exercise all four response dispositions")
    if diagnostic_modes != {"OMITTED", "COLLECTED_AFTER_R2"}:
        _fail("coverage manifest must include and omit the optional diagnostic")
    for comparison_id, comparison in comparisons.items():
        coverage = comparison_coverage.get(comparison_id, set())
        registered_options = {
            option_id
            for pair in comparison["allowed_matched_option_pairs"]
            for option_id in pair
        }
        for arm in ("LEFT", "RIGHT"):
            for option_id in registered_options:
                if (arm, option_id) not in coverage:
                    _fail(
                        "matched comparison must cover both arms under both "
                        f"registered options: {comparison_id}"
                    )
    return manifest


def _response_submission(script: dict[str, Any]) -> dict[str, Any]:
    status = script["response_status"]
    if status == "RESPONDED":
        raw = script["payload_utf8"].encode("utf-8")
        return {
            "response_status": "RESPONDED",
            "raw_payload_record": {
                "status": "PRESENT",
                "encoding": "BASE64_OF_EXACT_UTF8_BYTES",
                "raw_payload_utf8_base64": base64.b64encode(raw).decode("ascii"),
                "byte_length": len(raw),
                "content_sha256": _sha256(raw),
                "normalization": "NONE",
            },
        }
    return {
        "response_status": status,
        "raw_payload_record": {"status": "ABSENT", "reason": status},
    }


def build_session_input(
    run: dict[str, Any],
    corpus: dict[str, Any],
    instrument_sha256: str,
) -> dict[str, Any]:
    scripts = _script_index(corpus)
    sessions = []
    for session in run["sessions"]:
        diagnostic = session["post_trace_diagnostic"]
        if diagnostic["mode"] == "COLLECTED_AFTER_R2":
            diagnostic_record: dict[str, Any] = {
                "mode": "COLLECTED_AFTER_R2",
                "response": _response_submission(
                    scripts[diagnostic["script_id"]]
                ),
            }
        else:
            diagnostic_record = {"mode": "OMITTED"}
        sessions.append(
            {
                "session_id": session["session_id"],
                "presentation_id": session["presentation_id"],
                "future_option_id": session["future_option_id"],
                "comparison_binding": {
                    key: value
                    for key, value in session["comparison_binding"].items()
                },
                "responses": {
                    "immediate": _response_submission(
                        scripts[session["immediate_script_id"]]
                    ),
                    "later": _response_submission(
                        scripts[session["later_script_id"]]
                    ),
                    "post_trace_diagnostic": diagnostic_record,
                },
            }
        )
    return {
        "$schema": "./session-input.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "DEVELOPMENT_ELICITATION_SCRIPT_INPUT",
        "run_id": run["run_id"],
        "instrument_binding": {
            "instrument_id": "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V0",
            "instrument_version": "0.0.0",
            "content_sha256": instrument_sha256,
        },
        "source_kind": "SCRIPTED_ADVERSARIAL_RESPONSE",
        "sessions": sessions,
    }


def _build_mapping_candidate_set(
    run: dict[str, Any],
    run_bytes: bytes,
    corpus: dict[str, Any],
    instrument_sha256: str,
    assessment_schema: dict[str, Any],
) -> dict[str, Any]:
    scripts = _script_index(corpus)
    candidates = []
    run_id = run["run_id"]
    for session in run["sessions"]:
        for phase in ("immediate", "later"):
            script = scripts[session[f"{phase}_script_id"]]
            judgment = script.get("mapping_judgment")
            if script["response_status"] != "RESPONDED" or judgment is None:
                # The frozen assessment schema has no candidate status for
                # absent-payload events; the gap is adjudicated in the P1
                # assessment artifacts instead of being cast to a status here.
                continue
            step = _RESPONSE_EVENT_STEP[phase]
            candidates.append(
                {
                    "mapping_candidate_id": (
                        f"{run_id}:{session['session_id']}:{step}:mapping"
                    ),
                    "response_event_id": (
                        f"{run_id}:{session['session_id']}:{step}"
                    ),
                    "source_phase": _MAPPING_COORDINATE[phase]["source_phase"],
                    "eligible_target_coordinate": _MAPPING_COORDINATE[phase][
                        "eligible_target_coordinate"
                    ],
                    "mapping_rule_candidate_version": (
                        MAPPING_RULE_CANDIDATE_VERSION
                    ),
                    "candidate_status": judgment["candidate_status"],
                    "analyst_basis": judgment["analyst_basis"],
                    "authority": (
                        "DEVELOPMENT_MAPPING_CANDIDATE_ONLY_NOT_OBSERVATION"
                    ),
                }
            )
    candidate_set = {
        "$schema": "./development-assessment.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "DEVELOPMENT_MAPPING_CANDIDATE_SET",
        "artifact_id": f"{run_id}:mapping-candidates",
        "instrument_sha256": instrument_sha256,
        "source_run_sha256": _sha256(run_bytes),
        "status": "CANDIDATES_ONLY_NO_FROZEN_MAPPING",
        "candidates": candidates,
    }
    validate_json_schema(candidate_set, assessment_schema)
    return candidate_set


def build_all(root: Path = _ROOT) -> dict[str, bytes]:
    """Deterministically build every generated P1 artifact as bytes.

    Returns a mapping of repository-relative POSIX paths to exact bytes.
    Running this twice from the same frozen inputs must return identical
    bytes; the P1 tests assert this and compare against the checked-in
    artifacts.
    """
    verify_frozen_inputs(root)
    instrument_path = (
        root
        / "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json"
    )
    compiled_context = compile_instrument_context(
        instrument_path,
        schema_path=(
            root
            / "research/scenarios/interp-dialogue-001/elicitation/instrument.schema.json"
        ),
    )
    corpus, corpus_bytes = load_response_corpus(
        root
        / "research/scenarios/interp-dialogue-001/elicitation/p1/response-corpus-v0.json"
    )
    manifest = load_coverage_manifest(
        root
        / "research/scenarios/interp-dialogue-001/elicitation/p1/coverage-manifest-v0.json",
        corpus=corpus,
        corpus_bytes=corpus_bytes,
        root=root,
        compiled_context=compiled_context,
    )
    instrument_bytes = instrument_path.read_bytes()
    instrument_sha256 = _sha256(instrument_bytes)
    assessment_schema_bytes = (
        root
        / "research/scenarios/interp-dialogue-001/elicitation/development-assessment.schema.json"
    ).read_bytes()
    if _sha256(assessment_schema_bytes) != FROZEN_ASSESSMENT_SCHEMA_SHA256:
        _fail("development assessment schema is not the frozen P0-v0 artifact")
    assessment_schema = loads_exact(assessment_schema_bytes)
    session_schema_bytes = (
        root
        / "research/scenarios/interp-dialogue-001/elicitation/session-input.schema.json"
    ).read_bytes()
    run_schema_bytes = (
        root
        / "research/scenarios/interp-dialogue-001/elicitation/run.schema.json"
    ).read_bytes()

    base = "research/scenarios/interp-dialogue-001/elicitation/p1"
    artifacts: dict[str, bytes] = {}
    manifest_entries: list[dict[str, str]] = []

    for index, run in enumerate(manifest["runs"], start=1):
        ordinal = f"{index:04d}"
        session_input = build_session_input(run, corpus, instrument_sha256)
        session_input_bytes = canonical_bytes(session_input)
        run_artifact = materialize_scripted_elicitation_replay(
            instrument_bytes,
            session_input_bytes,
            instrument_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json",
            session_schema_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/session-input.schema.json",
            run_schema_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/run.schema.json",
            compiled_context=compiled_context,
            session_schema_bytes=session_schema_bytes,
            run_schema_bytes=run_schema_bytes,
        )
        run_bytes = encode_run(run_artifact)
        candidate_set = scan_mechanical_defects(
            instrument_bytes,
            run_bytes,
            instrument_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/instrument-v0.json",
            run_schema_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/run.schema.json",
            assessment_schema_path=root
            / "research/scenarios/interp-dialogue-001/elicitation/development-assessment.schema.json",
            compiled_context=compiled_context,
            run_schema_bytes=run_schema_bytes,
            assessment_schema_bytes=assessment_schema_bytes,
        )
        candidate_bytes = encode_candidate_set(candidate_set)
        mapping_set = _build_mapping_candidate_set(
            run, run_bytes, corpus, instrument_sha256, assessment_schema
        )
        mapping_bytes = canonical_bytes(mapping_set)

        entries = {
            f"{base}/session-inputs/session-input-{ordinal}.json": (
                session_input_bytes
            ),
            f"{base}/runs/run-{ordinal}.json": run_bytes,
            f"{base}/assessment/mechanical/mechanical-candidates-{ordinal}.json": (
                candidate_bytes
            ),
            f"{base}/assessment/mapping/mapping-candidates-{ordinal}.json": (
                mapping_bytes
            ),
        }
        for relpath, payload in entries.items():
            artifacts[relpath] = payload
            manifest_entries.append(
                {
                    "path": relpath,
                    "run_id": run["run_id"],
                    "sha256": _sha256(payload),
                }
            )

    artifact_manifest = {
        "$schema": "./artifact-manifest.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "P1_GENERATED_ARTIFACT_SHA256_MANIFEST",
        "manifest_id": "INTERP-DIALOGUE-001P1-V0-ARTIFACTS",
        "authority": (
            "CONTENT_DIGEST_ACCOUNTING_ONLY_NOT_ACQUISITION_OR_CLAIM_SUPPORT"
        ),
        "coverage_manifest_sha256": _sha256(
            (
                root
                / "research/scenarios/interp-dialogue-001/elicitation/p1/coverage-manifest-v0.json"
            ).read_bytes()
        ),
        "response_corpus_sha256": _sha256(corpus_bytes),
        "artifacts": manifest_entries,
    }
    _validate_against(
        root
        / "research/scenarios/interp-dialogue-001/elicitation/p1/runs/artifact-manifest.schema.json",
        artifact_manifest,
        "artifact manifest",
    )
    artifacts[f"{base}/runs/artifact-manifest-v0.json"] = canonical_bytes(
        artifact_manifest
    )
    return artifacts


def write_all(root: Path = _ROOT) -> list[str]:
    written = []
    for relpath, payload in build_all(root).items():
        target = root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        written.append(relpath)
    return written


def verify_all(root: Path = _ROOT) -> None:
    for relpath, payload in build_all(root).items():
        target = root / relpath
        if not target.exists():
            _fail(f"generated P1 artifact is missing from the tree: {relpath}")
        if target.read_bytes() != payload:
            _fail(
                "checked-in P1 artifact bytes differ from deterministic "
                f"rebuild: {relpath}"
            )
