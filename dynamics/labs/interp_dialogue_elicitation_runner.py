from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

from dynamics.labs.interp_dialogue_elicitation_contract import (
    CompiledInstrumentContext,
    FROZEN_INSTRUMENT_SHA256,
    prompt_text,
    render_future_option,
    render_initial_presentation,
    validate_elicitation_instrument,
)
from dynamics.labs.interp_dialogue_scenario_contract import loads_exact
from dynamics.labs.interp_m1_common import canonical_bytes, validate_json_schema


_ROOT = Path(__file__).resolve().parents[2]
_ELICITATION_ROOT = (
    _ROOT / "research" / "scenarios" / "interp-dialogue-001" / "elicitation"
)
_DEFAULT_INSTRUMENT_PATH = _ELICITATION_ROOT / "instrument-v0.json"
_DEFAULT_SESSION_SCHEMA_PATH = _ELICITATION_ROOT / "session-input.schema.json"
_DEFAULT_RUN_SCHEMA_PATH = _ELICITATION_ROOT / "run.schema.json"

FROZEN_SESSION_SCHEMA_SHA256 = (
    "2474709b767c4146d64999e73454b6bdfbcf6989984fc1e1596deeead94df71e"
)
FROZEN_RUN_SCHEMA_SHA256 = (
    "8c5cca613f6bf53e925e60013e5958f29244fb236b06cf70520736ac5cbcc56d"
)

_FORBIDDEN_RUN_KEYS = {
    "adjudication_status",
    "defect_code",
    "defect_receipt",
    "development_mapping_candidate",
    "equal",
    "mapping",
    "observation_status",
    "out_of_model",
    "placement",
    "placement_winner",
    "revision_proposal",
    "signature_conforms",
    "trace_field_id",
}


class ScriptedReplayInputError(ValueError):
    """Raised when a scripted development replay violates the P0 contract."""


def _fail(message: str) -> None:
    raise ScriptedReplayInputError(message)


def _sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _validate_schema(
    value: dict[str, Any],
    schema_path: str | Path,
    label: str,
    expected_schema_sha256: str,
    *,
    schema_bytes: bytes | None = None,
) -> None:
    if schema_bytes is None:
        schema_bytes = Path(schema_path).read_bytes()
    if _sha256(schema_bytes) != expected_schema_sha256:
        _fail(f"{label} schema is not the frozen P0-v0 artifact")
    try:
        validate_json_schema(value, loads_exact(schema_bytes))
    except ValueError as exc:
        raise ScriptedReplayInputError(
            f"{label} schema validation failed: {exc}"
        ) from exc


def _present_payload(raw: bytes) -> dict[str, Any]:
    raw.decode("utf-8", errors="strict")
    return {
        "status": "PRESENT",
        "encoding": "BASE64_OF_EXACT_UTF8_BYTES",
        "raw_payload_utf8_base64": base64.b64encode(raw).decode("ascii"),
        "byte_length": len(raw),
        "content_sha256": _sha256(raw),
        "normalization": "NONE",
    }


def _payload_bytes(payload: dict[str, Any]) -> bytes | None:
    if payload["status"] == "ABSENT":
        return None
    encoded = payload["raw_payload_utf8_base64"]
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        _fail("raw response payload is not canonical base64")
    if base64.b64encode(raw).decode("ascii") != encoded:
        _fail("raw response payload base64 is not canonical")
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ScriptedReplayInputError(
            "raw response payload is not valid UTF-8"
        ) from exc
    if payload["byte_length"] != len(raw):
        _fail("raw response byte_length mismatch")
    if payload["content_sha256"] != _sha256(raw):
        _fail("raw response content_sha256 mismatch")
    if payload["normalization"] != "NONE":
        _fail("raw response normalization must remain NONE")
    return raw


def _validate_response_submission(submission: dict[str, Any]) -> None:
    status = submission["response_status"]
    payload = submission["raw_payload_record"]
    raw = _payload_bytes(payload)
    if status == "RESPONDED":
        if payload["status"] != "PRESENT" or raw is None:
            _fail("RESPONDED requires a present raw payload")
    else:
        if payload["status"] != "ABSENT":
            _fail(f"{status} requires an absent payload record")
        if payload["reason"] != status:
            _fail(f"{status} payload reason mismatch")


def _index(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        value = record[key]
        if value in result:
            _fail(f"duplicate {key}: {value}")
        result[value] = record
    return result


def _validate_session_input(
    session_input: dict[str, Any],
    instrument: dict[str, Any],
    instrument_bytes: bytes,
) -> None:
    binding = session_input["instrument_binding"]
    if binding != {
        "instrument_id": instrument["instrument_id"],
        "instrument_version": instrument["instrument_version"],
        "content_sha256": _sha256(instrument_bytes),
    }:
        _fail("session input instrument binding mismatch")
    if session_input["source_kind"] not in instrument["development_source_kinds"]:
        _fail("session input source kind is not allowed by P0")

    presentations = _index(instrument["presentations"], "presentation_id")
    options = _index(instrument["future_option_catalog"], "future_option_id")
    comparisons = _index(
        instrument["matched_future_comparisons"], "comparison_id"
    )
    session_ids: set[str] = set()
    comparison_groups: dict[str, dict[str, Any]] = {}
    for session in session_input["sessions"]:
        session_id = session["session_id"]
        if session_id in session_ids:
            _fail(f"duplicate session_id: {session_id}")
        session_ids.add(session_id)
        if session["presentation_id"] not in presentations:
            _fail(f"unknown presentation: {session['presentation_id']}")
        if session["future_option_id"] not in options:
            _fail(f"unknown future option: {session['future_option_id']}")
        presentation = presentations[session["presentation_id"]]
        option = options[session["future_option_id"]]
        if presentation["family_id"] != option["family_id"]:
            _fail("presentation and future option families differ")

        binding_record = session["comparison_binding"]
        if binding_record["status"] == "PRESENT":
            comparison_id = binding_record["comparison_id"]
            if comparison_id not in comparisons:
                _fail(f"unknown matched comparison: {comparison_id}")
            comparison = comparisons[comparison_id]
            expected_cell = comparison[
                "left_prior_cell_id"
                if binding_record["arm"] == "LEFT"
                else "right_prior_cell_id"
            ]
            if presentation["source_cell_id"] != expected_cell:
                _fail("comparison arm does not bind the declared source cell")
            group_id = binding_record["comparison_group_id"]
            group = comparison_groups.setdefault(
                group_id, {"comparison_id": comparison_id, "arms": set()}
            )
            if group["comparison_id"] != comparison_id:
                _fail("comparison group mixes comparison contracts")
            if binding_record["arm"] in group["arms"]:
                _fail("comparison group repeats the same arm")
            group["arms"].add(binding_record["arm"])

        _validate_response_submission(session["responses"]["immediate"])
        _validate_response_submission(session["responses"]["later"])
        diagnostic = session["responses"]["post_trace_diagnostic"]
        if diagnostic["mode"] == "COLLECTED_AFTER_R2":
            _validate_response_submission(diagnostic["response"])

    for group_id, group in comparison_groups.items():
        if group["arms"] != {"LEFT", "RIGHT"}:
            _fail(f"comparison group is incomplete: {group_id}")


def _delivery_event(
    run_id: str,
    session_id: str,
    step_id: str,
    ordinal: int,
    event_kind: str,
    text: str,
) -> dict[str, Any]:
    return {
        "event_id": f"{run_id}:{session_id}:{step_id}",
        "elicitation_step_id": step_id,
        "sequence_ordinal": ordinal,
        "event_kind": event_kind,
        "payload_record": _present_payload(text.encode("utf-8")),
        "authority": (
            "SCRIPTED_DELIVERY_RECORD_NOT_ACTUAL_OCCURRENCE_OR_ORDINAL_OBSERVATION"
        ),
    }


def _response_event(
    run_id: str,
    session_id: str,
    step_id: str,
    ordinal: int,
    prompt_event_id: str,
    submission: dict[str, Any],
) -> dict[str, Any]:
    return {
        "event_id": f"{run_id}:{session_id}:{step_id}",
        "elicitation_step_id": step_id,
        "sequence_ordinal": ordinal,
        "event_kind": "SCRIPTED_RESPONSE_RECORD",
        "prompt_delivery_event_id": prompt_event_id,
        "response_status": submission["response_status"],
        "payload_record": deepcopy(submission["raw_payload_record"]),
        "authority": "SCRIPTED_RESPONSE_RECORD_AND_PAYLOAD_PROVENANCE_ONLY",
    }


def _provenance_link(
    run_id: str,
    session_id: str,
    response: dict[str, Any],
    prompt: dict[str, Any],
    context: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "link_id": f"{run_id}:{session_id}:link:{response['elicitation_step_id']}",
        "response_event_id": response["event_id"],
        "prompt_delivery_event_id": prompt["event_id"],
        "context_delivery_event_ids": [item["event_id"] for item in context],
        "delivered_prompt_sha256": prompt["payload_record"]["content_sha256"],
        "context_payload_sha256": [
            item["payload_record"]["content_sha256"] for item in context
        ],
        "authority": (
            "LINKS_SCRIPTED_RESPONSE_RECORD_TO_SCRIPTED_DELIVERY_CONTEXT_ONLY"
        ),
    }


def _record_session(
    instrument: dict[str, Any],
    run_id: str,
    session: dict[str, Any],
    *,
    instrument_path: str | Path,
    compiled_context: CompiledInstrumentContext | None = None,
) -> dict[str, Any]:
    session_id = session["session_id"]
    presentations = _index(instrument["presentations"], "presentation_id")
    presentation = presentations[session["presentation_id"]]
    e0 = _delivery_event(
        run_id,
        session_id,
        "E0_INITIAL_VIGNETTE_DELIVERY",
        0,
        "STIMULUS_DELIVERY",
        render_initial_presentation(
            compiled_context or instrument,
            session["presentation_id"],
            instrument_path=instrument_path,
        ),
    )
    e1 = _delivery_event(
        run_id,
        session_id,
        "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY",
        1,
        "PROMPT_DELIVERY",
        prompt_text(
            compiled_context or instrument, "P_GENERIC_IMMEDIATE_RESPONSE"
        ),
    )
    r1 = _response_event(
        run_id,
        session_id,
        "R1_IMMEDIATE_RESPONSE_EVENT",
        2,
        e1["event_id"],
        session["responses"]["immediate"],
    )
    e2 = _delivery_event(
        run_id,
        session_id,
        "E2_MATCHED_FUTURE_OPTION_DELIVERY",
        3,
        "STIMULUS_DELIVERY",
        render_future_option(
            compiled_context or instrument,
            session["future_option_id"],
            instrument_path=instrument_path,
        ),
    )
    e3 = _delivery_event(
        run_id,
        session_id,
        "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY",
        4,
        "PROMPT_DELIVERY",
        prompt_text(compiled_context or instrument, "P_GENERIC_LATER_RESPONSE"),
    )
    r2 = _response_event(
        run_id,
        session_id,
        "R2_LATER_RESPONSE_EVENT",
        5,
        e3["event_id"],
        session["responses"]["later"],
    )
    events = [e0, e1, r1, e2, e3, r2]
    links = [
        _provenance_link(run_id, session_id, r1, e1, [e0]),
        _provenance_link(run_id, session_id, r2, e3, [e0, e2]),
    ]

    diagnostic = session["responses"]["post_trace_diagnostic"]
    if diagnostic["mode"] == "COLLECTED_AFTER_R2":
        d0 = _delivery_event(
            run_id,
            session_id,
            "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY",
            6,
            "PROMPT_DELIVERY",
            prompt_text(compiled_context or instrument, "P_POST_TRACE_DIAGNOSTIC"),
        )
        rd0 = _response_event(
            run_id,
            session_id,
            "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT",
            7,
            d0["event_id"],
            diagnostic["response"],
        )
        events.extend([d0, rd0])
        links.append(
            _provenance_link(run_id, session_id, rd0, d0, [e0, e2])
        )

    return {
        "session_id": session_id,
        "presentation_id": session["presentation_id"],
        "source_cell_id": presentation["source_cell_id"],
        "future_option_id": session["future_option_id"],
        "comparison_binding": deepcopy(session["comparison_binding"]),
        "event_log": events,
        "response_provenance_links": links,
    }


def materialize_scripted_elicitation_replay(
    instrument_bytes: bytes,
    session_input_bytes: bytes,
    *,
    instrument_path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    session_schema_path: str | Path = _DEFAULT_SESSION_SCHEMA_PATH,
    run_schema_path: str | Path = _DEFAULT_RUN_SCHEMA_PATH,
    compiled_context: CompiledInstrumentContext | None = None,
    session_schema_bytes: bytes | None = None,
    run_schema_bytes: bytes | None = None,
) -> dict[str, Any]:
    try:
        instrument = (
            compiled_context._instrument
            if compiled_context is not None
            else loads_exact(instrument_bytes)
        )
        session_input = loads_exact(session_input_bytes)
    except ValueError as exc:
        raise ScriptedReplayInputError(str(exc)) from exc
    if _sha256(instrument_bytes) != FROZEN_INSTRUMENT_SHA256:
        _fail("materializer accepts only the frozen P0-v0 instrument bytes")
    if compiled_context is not None:
        if compiled_context.instrument_sha256 != _sha256(instrument_bytes):
            _fail("compiled context does not bind the supplied instrument bytes")
    else:
        validate_elicitation_instrument(instrument, instrument_path=instrument_path)
    _validate_schema(
        session_input,
        session_schema_path,
        "session input",
        FROZEN_SESSION_SCHEMA_SHA256,
        schema_bytes=session_schema_bytes,
    )
    _validate_session_input(session_input, instrument, instrument_bytes)

    run = {
        "$schema": "./run.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "DEVELOPMENT_ELICITATION_SCRIPTED_REPLAY",
        "run_id": session_input["run_id"],
        "status": (
            "IMMUTABLE_SCRIPTED_REPLAY_NO_ACTUAL_OCCURRENCE_OR_MECHANISM_RESULT"
        ),
        "authority": {
            "artifact_role": (
                "DEVELOPMENT_ELICITATION_SCRIPTED_REPLAY_ARTIFACT"
            ),
            "response_authority": (
                "SCRIPTED_RESPONSE_RECORD_AND_PAYLOAD_PROVENANCE_ONLY"
            ),
            "mapping_status": "NO_MAPPING_EMITTED",
            "defect_status": "NO_DEFECT_CLASSIFICATION_EMITTED",
            "empirical_status": (
                "NO_ACTUAL_PARTICIPANT_OCCURRENCE_OR_HUMAN_MECHANISM_SUPPORT"
            ),
        },
        "instrument_binding": deepcopy(session_input["instrument_binding"]),
        "session_input_sha256": _sha256(session_input_bytes),
        "source_kind": session_input["source_kind"],
        "sessions": [
            _record_session(
                instrument,
                session_input["run_id"],
                session,
                instrument_path=instrument_path,
                compiled_context=compiled_context,
            )
            for session in session_input["sessions"]
        ],
    }
    _validate_schema(
        run,
        run_schema_path,
        "run",
        FROZEN_RUN_SCHEMA_SHA256,
        schema_bytes=run_schema_bytes,
    )
    validate_run_artifact(run)
    return run


def _walk_forbidden_keys(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in _FORBIDDEN_RUN_KEYS:
                _fail(f"forbidden materializer output key {key!r} at {path}")
            _walk_forbidden_keys(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden_keys(child, f"{path}/{index}")


def validate_run_artifact(run: dict[str, Any]) -> None:
    _walk_forbidden_keys(run)
    session_ids: set[str] = set()
    global_event_ids: set[str] = set()
    global_link_ids: set[str] = set()
    for session in run["sessions"]:
        if session["session_id"] in session_ids:
            _fail("run repeats session_id")
        session_ids.add(session["session_id"])
        events = session["event_log"]
        expected_steps = list(_EXPECTED_REQUIRED_STEPS)
        if len(events) == 8:
            expected_steps += [
                "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY",
                "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT",
            ]
        if [item["elicitation_step_id"] for item in events] != expected_steps:
            _fail("run event schedule changed")
        if [item["sequence_ordinal"] for item in events] != list(range(len(events))):
            _fail("run event ordinals are not append-only")
        if [
            (item["elicitation_step_id"], item["event_kind"])
            for item in events
        ] != [
            (step_id, _EXPECTED_EVENT_KIND_BY_STEP[step_id])
            for step_id in expected_steps
        ]:
            _fail("run event kinds do not match the frozen elicitation steps")
        event_by_id = _index(events, "event_id")
        if global_event_ids & set(event_by_id):
            _fail("run repeats an event_id across sessions")
        global_event_ids.update(event_by_id)
        event_by_step = _index(events, "elicitation_step_id")
        for event in events:
            payload = event["payload_record"]
            if payload["status"] == "PRESENT":
                _payload_bytes(payload)
            if event["event_kind"] == "SCRIPTED_RESPONSE_RECORD":
                _validate_response_submission(
                    {
                        "response_status": event["response_status"],
                        "raw_payload_record": payload,
                    }
                )
                prompt_id = event["prompt_delivery_event_id"]
                if prompt_id not in event_by_id:
                    _fail("response refers to an unlogged prompt delivery")
                if event_by_id[prompt_id]["event_kind"] != "PROMPT_DELIVERY":
                    _fail("response prompt reference is not a prompt delivery")
                expected_prompt_step = _EXPECTED_PROMPT_STEP_BY_RESPONSE[
                    event["elicitation_step_id"]
                ]
                expected_prompt = event_by_step[expected_prompt_step]
                if prompt_id != expected_prompt["event_id"]:
                    _fail("response is not linked to its frozen prompt step")
                if expected_prompt["sequence_ordinal"] >= event["sequence_ordinal"]:
                    _fail("response prompt delivery is not earlier than the response")
        links = _index(session["response_provenance_links"], "response_event_id")
        link_ids = {
            link["link_id"] for link in session["response_provenance_links"]
        }
        if len(link_ids) != len(session["response_provenance_links"]):
            _fail("session repeats response provenance link_id")
        if global_link_ids & link_ids:
            _fail("run repeats response provenance link_id across sessions")
        global_link_ids.update(link_ids)
        response_ids = {
            item["event_id"]
            for item in events
            if item["event_kind"] == "SCRIPTED_RESPONSE_RECORD"
        }
        if set(links) != response_ids:
            _fail("response provenance coverage mismatch")
        for response_id, link in links.items():
            response = event_by_id[response_id]
            if link["prompt_delivery_event_id"] not in event_by_id:
                _fail("response provenance refers to an unlogged prompt")
            prompt = event_by_id[link["prompt_delivery_event_id"]]
            if response["prompt_delivery_event_id"] != prompt["event_id"]:
                _fail("response provenance prompt mismatch")
            if link["delivered_prompt_sha256"] != prompt["payload_record"]["content_sha256"]:
                _fail("response provenance prompt digest mismatch")
            expected_context_steps = _EXPECTED_CONTEXT_STEPS_BY_RESPONSE[
                response["elicitation_step_id"]
            ]
            expected_context_ids = [
                event_by_step[step_id]["event_id"]
                for step_id in expected_context_steps
            ]
            if link["context_delivery_event_ids"] != expected_context_ids:
                _fail("response provenance context binding mismatch")
            contexts = [event_by_id[item] for item in expected_context_ids]
            if link["context_payload_sha256"] != [
                item["payload_record"]["content_sha256"] for item in contexts
            ]:
                _fail("response provenance context digest mismatch")


_EXPECTED_REQUIRED_STEPS = (
    "E0_INITIAL_VIGNETTE_DELIVERY",
    "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY",
    "R1_IMMEDIATE_RESPONSE_EVENT",
    "E2_MATCHED_FUTURE_OPTION_DELIVERY",
    "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY",
    "R2_LATER_RESPONSE_EVENT",
)

_EXPECTED_PROMPT_STEP_BY_RESPONSE = {
    "R1_IMMEDIATE_RESPONSE_EVENT": (
        "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY"
    ),
    "R2_LATER_RESPONSE_EVENT": "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY",
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": (
        "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY"
    ),
}

_EXPECTED_EVENT_KIND_BY_STEP = {
    "E0_INITIAL_VIGNETTE_DELIVERY": "STIMULUS_DELIVERY",
    "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY": "PROMPT_DELIVERY",
    "R1_IMMEDIATE_RESPONSE_EVENT": "SCRIPTED_RESPONSE_RECORD",
    "E2_MATCHED_FUTURE_OPTION_DELIVERY": "STIMULUS_DELIVERY",
    "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY": "PROMPT_DELIVERY",
    "R2_LATER_RESPONSE_EVENT": "SCRIPTED_RESPONSE_RECORD",
    "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY": "PROMPT_DELIVERY",
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": (
        "SCRIPTED_RESPONSE_RECORD"
    ),
}

_EXPECTED_CONTEXT_STEPS_BY_RESPONSE = {
    "R1_IMMEDIATE_RESPONSE_EVENT": ["E0_INITIAL_VIGNETTE_DELIVERY"],
    "R2_LATER_RESPONSE_EVENT": [
        "E0_INITIAL_VIGNETTE_DELIVERY",
        "E2_MATCHED_FUTURE_OPTION_DELIVERY",
    ],
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": [
        "E0_INITIAL_VIGNETTE_DELIVERY",
        "E2_MATCHED_FUTURE_OPTION_DELIVERY",
    ],
}


def encode_run(run: dict[str, Any]) -> bytes:
    return canonical_bytes(run)
