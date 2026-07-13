from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from typing import Any

from dynamics.labs.interp_dialogue_elicitation_contract import (
    FROZEN_INSTRUMENT_SHA256,
    prompt_text,
    render_future_option,
    render_initial_presentation,
    validate_elicitation_instrument,
)
from dynamics.labs.interp_dialogue_scenario_contract import load_family, loads_exact
from dynamics.labs.interp_m1_common import canonical_bytes, validate_json_schema


_ROOT = Path(__file__).resolve().parents[2]
_ELICITATION_ROOT = (
    _ROOT / "research" / "scenarios" / "interp-dialogue-001" / "elicitation"
)
_DEFAULT_INSTRUMENT_PATH = _ELICITATION_ROOT / "instrument-v0.json"
_DEFAULT_RUN_SCHEMA_PATH = _ELICITATION_ROOT / "run.schema.json"
_DEFAULT_ASSESSMENT_SCHEMA_PATH = (
    _ELICITATION_ROOT / "development-assessment.schema.json"
)

FROZEN_RUN_SCHEMA_SHA256 = (
    "8c5cca613f6bf53e925e60013e5958f29244fb236b06cf70520736ac5cbcc56d"
)
FROZEN_ASSESSMENT_SCHEMA_SHA256 = (
    "ac7cc68fb8c9618838f99e3c1ad9c120a79df313f22828c2b395300e2473b92f"
)

_INTERNAL_LITERALS = {
    "action_affordance",
    "adjudication",
    "candidate_set",
    "durable_targetform_write",
    "evidencelink",
    "ghost",
    "material_admission",
    "narrative_write",
    "subjective_encounter_form",
    "targetform",
}

_REQUIRED_STEP_ORDER = {
    "E0_INITIAL_VIGNETTE_DELIVERY": 0,
    "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY": 1,
    "R1_IMMEDIATE_RESPONSE_EVENT": 2,
    "E2_MATCHED_FUTURE_OPTION_DELIVERY": 3,
    "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY": 4,
    "R2_LATER_RESPONSE_EVENT": 5,
    "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY": 6,
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": 7,
}

_REQUIRED_STEPS = tuple(
    step_id
    for step_id, _ in sorted(
        _REQUIRED_STEP_ORDER.items(), key=lambda item: item[1]
    )
    if _REQUIRED_STEP_ORDER[step_id] <= 5
)
_DIAGNOSTIC_STEPS = (
    "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY",
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT",
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
    "R1_IMMEDIATE_RESPONSE_EVENT": ("E0_INITIAL_VIGNETTE_DELIVERY",),
    "R2_LATER_RESPONSE_EVENT": (
        "E0_INITIAL_VIGNETTE_DELIVERY",
        "E2_MATCHED_FUTURE_OPTION_DELIVERY",
    ),
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": (
        "E0_INITIAL_VIGNETTE_DELIVERY",
        "E2_MATCHED_FUTURE_OPTION_DELIVERY",
    ),
}


class MechanicalScanInputError(ValueError):
    """Raised when the scanner cannot bind a P0 instrument or run artifact."""


def _fail(message: str) -> None:
    raise MechanicalScanInputError(message)


def _sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _frozen_schema(
    path: str | Path, expected_sha256: str, label: str
) -> dict[str, Any]:
    source = Path(path).read_bytes()
    if _sha256(source) != expected_sha256:
        _fail(f"{label} schema is not the frozen P0-v0 artifact")
    try:
        return loads_exact(source)
    except ValueError as exc:
        raise MechanicalScanInputError(str(exc)) from exc


def _candidate(
    run_id: str,
    ordinal: int,
    code: str,
    pointer: str,
    basis: str,
) -> dict[str, Any]:
    return {
        "candidate_id": f"{run_id}:mechanical:{ordinal:03d}",
        "defect_code": code,
        "artifact_pointer": pointer,
        "basis": basis,
        "authority": "MECHANICAL_DEFECT_CANDIDATE_NOT_INSTRUMENT_DEFECT_RECEIPT",
    }


def _participant_texts(
    instrument: dict[str, Any], instrument_path: str | Path
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for presentation in instrument["presentations"]:
        result.append(
            (
                f"/instrument/presentations/{presentation['presentation_id']}",
                render_initial_presentation(
                    instrument,
                    presentation["presentation_id"],
                    instrument_path=instrument_path,
                ),
            )
        )
    for option in instrument["future_option_catalog"]:
        result.append(
            (
                f"/instrument/future_option_catalog/{option['future_option_id']}",
                render_future_option(
                    instrument,
                    option["future_option_id"],
                    instrument_path=instrument_path,
                ),
            )
        )
    for prompt in instrument["prompt_catalog"]:
        result.append(
            (
                f"/instrument/prompt_catalog/{prompt['prompt_id']}",
                prompt_text(instrument, prompt["prompt_id"]),
            )
        )
    return result


def _candidate_anchors(
    instrument: dict[str, Any], instrument_path: str | Path
) -> set[str]:
    root = Path(instrument_path).resolve().parent
    anchors: set[str] = set()
    for source in instrument["bound_source_artifacts"]:
        if source["role"] != "SCENARIO_FAMILY":
            continue
        family = load_family((root / source["path"]).resolve())
        anchors.add(
            family["same_immediate_projection_claim"]["candidate_projection"][
                "illustration"
            ].casefold()
        )
    return anchors


def _payload_defects(
    run_id: str,
    session_index: int,
    event_index: int,
    event: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> bytes | None:
    payload = event["payload_record"]
    pointer = f"/run/sessions/{session_index}/event_log/{event_index}"
    response_status = event.get("response_status")
    if response_status == "RESPONDED" and payload["status"] != "PRESENT":
        candidates.append(
            _candidate(
                run_id,
                len(candidates),
                "MISSINGNESS_COLLAPSE",
                pointer,
                "RESPONDED was recorded without a present raw payload.",
            )
        )
    if response_status in {"REFUSED", "NO_RESPONSE", "TECHNICAL_FAILURE"}:
        if payload["status"] != "ABSENT" or payload.get("reason") != response_status:
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "MISSINGNESS_COLLAPSE",
                    pointer,
                    f"{response_status} was collapsed into a different payload state.",
                )
            )
    if payload["status"] != "PRESENT":
        return None
    try:
        raw = base64.b64decode(payload["raw_payload_utf8_base64"], validate=True)
    except (ValueError, TypeError):
        raw = b""
        mismatch = True
    else:
        mismatch = (
            base64.b64encode(raw).decode("ascii")
            != payload["raw_payload_utf8_base64"]
            or len(raw) != payload["byte_length"]
            or _sha256(raw) != payload["content_sha256"]
            or payload["normalization"] != "NONE"
        )
        try:
            raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            mismatch = True
    if mismatch:
        candidates.append(
            _candidate(
                run_id,
                len(candidates),
                "RAW_PAYLOAD_PROVENANCE_BREAK",
                pointer,
                "The recorded raw UTF-8 bytes, length, digest, or normalization policy disagree.",
            )
        )
        return None
    return raw


def _expected_delivery_text(
    instrument: dict[str, Any],
    session: dict[str, Any],
    step_id: str,
    instrument_path: str | Path,
) -> str | None:
    if step_id == "E0_INITIAL_VIGNETTE_DELIVERY":
        return render_initial_presentation(
            instrument,
            session["presentation_id"],
            instrument_path=instrument_path,
        )
    if step_id == "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY":
        return prompt_text(instrument, "P_GENERIC_IMMEDIATE_RESPONSE")
    if step_id == "E2_MATCHED_FUTURE_OPTION_DELIVERY":
        return render_future_option(
            instrument,
            session["future_option_id"],
            instrument_path=instrument_path,
        )
    if step_id == "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY":
        return prompt_text(instrument, "P_GENERIC_LATER_RESPONSE")
    if step_id == "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY":
        return prompt_text(instrument, "P_POST_TRACE_DIAGNOSTIC")
    return None


def _scan_provenance_links(
    run_id: str,
    session_index: int,
    session: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> None:
    pointer = f"/run/sessions/{session_index}/response_provenance_links"
    events = session["event_log"]
    event_ids = [event["event_id"] for event in events]
    step_ids = [event["elicitation_step_id"] for event in events]
    if len(event_ids) != len(set(event_ids)) or len(step_ids) != len(set(step_ids)):
        candidates.append(
            _candidate(
                run_id,
                len(candidates),
                "RESPONSE_PROVENANCE_LINK_MISMATCH",
                pointer,
                "Event identifiers or elicitation step identifiers are not unique.",
            )
        )
        return

    event_by_id = {event["event_id"]: event for event in events}
    event_by_step = {event["elicitation_step_id"]: event for event in events}
    response_events = {
        event["event_id"]: event
        for event in events
        if event["event_kind"] == "SCRIPTED_RESPONSE_RECORD"
    }
    links = session["response_provenance_links"]
    linked_response_ids = [link["response_event_id"] for link in links]
    if (
        len(linked_response_ids) != len(set(linked_response_ids))
        or set(linked_response_ids) != set(response_events)
    ):
        candidates.append(
            _candidate(
                run_id,
                len(candidates),
                "RESPONSE_PROVENANCE_LINK_MISMATCH",
                pointer,
                "Response-provenance coverage is not exact and one-to-one.",
            )
        )

    for link_index, link in enumerate(links):
        link_pointer = f"{pointer}/{link_index}"
        response = response_events.get(link["response_event_id"])
        prompt = event_by_id.get(link["prompt_delivery_event_id"])
        if response is None or prompt is None:
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    link_pointer,
                    "The provenance link refers to an absent response or prompt event.",
                )
            )
            continue
        response_step = response["elicitation_step_id"]
        expected_context_steps = _EXPECTED_CONTEXT_STEPS_BY_RESPONSE.get(
            response_step
        )
        expected_prompt_step = _EXPECTED_PROMPT_STEP_BY_RESPONSE.get(response_step)
        if expected_context_steps is None or expected_prompt_step is None:
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    link_pointer,
                    "The response step has no frozen provenance contract.",
                )
            )
            continue
        expected_prompt = event_by_step.get(expected_prompt_step)
        expected_context = [event_by_step.get(step) for step in expected_context_steps]
        if expected_prompt is None or any(item is None for item in expected_context):
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    link_pointer,
                    "The frozen prompt or context delivery is absent.",
                )
            )
            continue
        context_events = [item for item in expected_context if item is not None]
        if (
            expected_prompt["event_kind"] != "PROMPT_DELIVERY"
            or expected_prompt["payload_record"]["status"] != "PRESENT"
            or any(
                item["event_kind"] != "STIMULUS_DELIVERY"
                or item["payload_record"]["status"] != "PRESENT"
                for item in context_events
            )
        ):
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    link_pointer,
                    "The frozen prompt or context step is not a present delivery record.",
                )
            )
            continue
        expected_context_ids = [item["event_id"] for item in context_events]
        expected_context_digests = [
            item["payload_record"]["content_sha256"] for item in context_events
        ]
        mismatch = (
            response["prompt_delivery_event_id"] != expected_prompt["event_id"]
            or link["prompt_delivery_event_id"] != expected_prompt["event_id"]
            or link["delivered_prompt_sha256"]
            != expected_prompt["payload_record"]["content_sha256"]
            or link["context_delivery_event_ids"] != expected_context_ids
            or link["context_payload_sha256"] != expected_context_digests
        )
        if mismatch:
            candidates.append(
                _candidate(
                    run_id,
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    link_pointer,
                    "The link disagrees with the frozen prompt or context provenance.",
                )
            )


def scan_mechanical_defects(
    instrument_bytes: bytes,
    run_bytes: bytes,
    *,
    instrument_path: str | Path = _DEFAULT_INSTRUMENT_PATH,
    run_schema_path: str | Path = _DEFAULT_RUN_SCHEMA_PATH,
    assessment_schema_path: str | Path = _DEFAULT_ASSESSMENT_SCHEMA_PATH,
) -> dict[str, Any]:
    try:
        instrument = loads_exact(instrument_bytes)
        run = loads_exact(run_bytes)
    except ValueError as exc:
        raise MechanicalScanInputError(str(exc)) from exc
    if _sha256(instrument_bytes) != FROZEN_INSTRUMENT_SHA256:
        _fail("scanner accepts only the frozen P0-v0 instrument bytes")
    validate_elicitation_instrument(instrument, instrument_path=instrument_path)
    if run.get("instrument_binding", {}).get("content_sha256") != _sha256(
        instrument_bytes
    ):
        _fail("run instrument binding mismatch")
    try:
        validate_json_schema(
            run,
            _frozen_schema(
                run_schema_path, FROZEN_RUN_SCHEMA_SHA256, "run"
            ),
        )
    except ValueError as exc:
        raise MechanicalScanInputError(
            f"run schema validation failed: {exc}"
        ) from exc

    candidates: list[dict[str, Any]] = []
    participant_texts = _participant_texts(instrument, instrument_path)
    anchors = _candidate_anchors(instrument, instrument_path)
    for pointer, text in participant_texts:
        folded = text.casefold()
        for anchor in sorted(anchors):
            if anchor and anchor in folded:
                candidates.append(
                    _candidate(
                        run["run_id"],
                        len(candidates),
                        "DESIGN_ANCHOR_LITERAL_LEAK",
                        pointer,
                        "A design-only candidate anchor appears in participant-facing content.",
                    )
                )
                break
        leaked = sorted(token for token in _INTERNAL_LITERALS if token in folded)
        if leaked:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "INTERNAL_IDENTIFIER_LITERAL_LEAK",
                    pointer,
                    "Participant-facing content exposes internal identifiers: "
                    + ", ".join(leaked),
                )
            )

    presentations = {
        item["presentation_id"]: item for item in instrument["presentations"]
    }
    future_options = {
        item["future_option_id"]: item
        for item in instrument["future_option_catalog"]
    }
    comparison_groups: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    comparison_catalog = {
        item["comparison_id"]: item
        for item in instrument["matched_future_comparisons"]
    }
    seen_session_ids: set[str] = set()
    seen_event_ids: set[str] = set()
    seen_link_ids: set[str] = set()
    for session_index, session in enumerate(run["sessions"]):
        if session["session_id"] in seen_session_ids:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "SESSION_BINDING_MISMATCH",
                    f"/run/sessions/{session_index}/session_id",
                    "The replay repeats a session_id.",
                )
            )
        seen_session_ids.add(session["session_id"])
        events = session["event_log"]
        session_event_ids = [event["event_id"] for event in events]
        session_link_ids = [
            link["link_id"] for link in session["response_provenance_links"]
        ]
        if (
            len(session_link_ids) != len(set(session_link_ids))
            or seen_event_ids & set(session_event_ids)
            or seen_link_ids & set(session_link_ids)
        ):
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "RESPONSE_PROVENANCE_LINK_MISMATCH",
                    f"/run/sessions/{session_index}",
                    "Event or provenance-link identifiers repeat within or "
                    "across sessions.",
                )
            )
        seen_event_ids.update(session_event_ids)
        seen_link_ids.update(session_link_ids)
        event_by_id = {event["event_id"]: event for event in events}
        event_by_step = {
            event["elicitation_step_id"]: event for event in events
        }
        ordinals = [event["sequence_ordinal"] for event in events]
        step_ids = [event["elicitation_step_id"] for event in events]
        expected_steps = _REQUIRED_STEPS
        if len(events) == 8:
            expected_steps += _DIAGNOSTIC_STEPS
        known_steps = all(step_id in _REQUIRED_STEP_ORDER for step_id in step_ids)
        expected_ordinals = (
            [_REQUIRED_STEP_ORDER[step_id] for step_id in step_ids]
            if known_steps
            else []
        )
        if (
            tuple(step_ids) != expected_steps
            or ordinals != list(range(len(events)))
            or ordinals != expected_ordinals
            or any(
                _EXPECTED_EVENT_KIND_BY_STEP.get(event["elicitation_step_id"])
                != event["event_kind"]
                for event in events
            )
        ):
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "PROMPT_ORDER_VIOLATION",
                    f"/run/sessions/{session_index}/event_log",
                    "The event log is not in the frozen append-only elicitation order.",
                )
            )
        if (
            "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY" in step_ids
            and "R2_LATER_RESPONSE_EVENT" in step_ids
        ):
            if step_ids.index(
                "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY"
            ) < step_ids.index("R2_LATER_RESPONSE_EVENT"):
                candidates.append(
                    _candidate(
                        run["run_id"],
                        len(candidates),
                        "POST_TRACE_DIAGNOSTIC_EARLY_DELIVERY",
                        f"/run/sessions/{session_index}/event_log",
                        "The diagnostic prompt was delivered before the later response event.",
                    )
                )
        known_presentation = session["presentation_id"] in presentations
        known_future = session["future_option_id"] in future_options
        session_binding_valid = known_presentation and known_future
        if session_binding_valid:
            presentation = presentations[session["presentation_id"]]
            future_option = future_options[session["future_option_id"]]
            session_binding_valid = (
                session["source_cell_id"] == presentation["source_cell_id"]
                and presentation["family_id"] == future_option["family_id"]
            )
        if not session_binding_valid:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "SESSION_BINDING_MISMATCH",
                    f"/run/sessions/{session_index}",
                    "Session metadata does not bind one frozen presentation, "
                    "cell, and same-family future option.",
                )
            )
        for event_index, event in enumerate(events):
            raw = _payload_defects(
                run["run_id"], session_index, event_index, event, candidates
            )
            pointer = f"/run/sessions/{session_index}/event_log/{event_index}"
            if event["event_kind"] == "SCRIPTED_RESPONSE_RECORD":
                prompt_id = event["prompt_delivery_event_id"]
                if prompt_id not in event_by_id:
                    candidates.append(
                        _candidate(
                            run["run_id"],
                            len(candidates),
                            "UNLOGGED_PROMPT_DELIVERY",
                            pointer,
                            "A response refers to a prompt delivery absent from the event log.",
                        )
                    )
                expected_prompt_step = _EXPECTED_PROMPT_STEP_BY_RESPONSE.get(
                    event["elicitation_step_id"]
                )
                expected_prompt = event_by_step.get(expected_prompt_step)
                actual_prompt = event_by_id.get(prompt_id)
                if (
                    expected_prompt is None
                    or actual_prompt is None
                    or actual_prompt["event_kind"] != "PROMPT_DELIVERY"
                    or actual_prompt["event_id"] != expected_prompt["event_id"]
                    or actual_prompt["sequence_ordinal"]
                    >= event["sequence_ordinal"]
                ):
                    candidates.append(
                        _candidate(
                            run["run_id"],
                            len(candidates),
                            "PROMPT_ORDER_VIOLATION",
                            pointer,
                            "The response is not linked to its earlier frozen prompt delivery.",
                        )
                    )
            if event["event_kind"] not in {
                "STIMULUS_DELIVERY",
                "PROMPT_DELIVERY",
            }:
                continue
            if (
                event["elicitation_step_id"]
                == "E0_INITIAL_VIGNETTE_DELIVERY"
                and not known_presentation
            ) or (
                event["elicitation_step_id"]
                == "E2_MATCHED_FUTURE_OPTION_DELIVERY"
                and not known_future
            ):
                candidates.append(
                    _candidate(
                        run["run_id"],
                        len(candidates),
                        "DELIVERY_PAYLOAD_MISMATCH",
                        pointer,
                        "The delivery cannot bind to a frozen presentation or future option.",
                    )
                )
                continue
            expected_text = _expected_delivery_text(
                instrument,
                session,
                event["elicitation_step_id"],
                instrument_path,
            )
            if expected_text is not None and raw != expected_text.encode("utf-8"):
                candidates.append(
                    _candidate(
                        run["run_id"],
                        len(candidates),
                        "DELIVERY_PAYLOAD_MISMATCH",
                        pointer,
                        "Delivered bytes differ from the frozen rendered instrument payload.",
                    )
                )

        _scan_provenance_links(
            run["run_id"], session_index, session, candidates
        )

        binding = session["comparison_binding"]
        if binding["status"] == "PRESENT":
            comparison_groups.setdefault(
                binding["comparison_group_id"], []
            ).append((binding, session))

    for group_id, members in sorted(comparison_groups.items()):
        comparison_ids = {binding["comparison_id"] for binding, _ in members}
        arms = [binding["arm"] for binding, _ in members]
        if len(comparison_ids) != 1 or sorted(arms) != ["LEFT", "RIGHT"]:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "MATCHED_COMPARISON_BINDING_MISMATCH",
                    f"/run/comparison_groups/{group_id}",
                    "A comparison group must bind one contract with exactly "
                    "one LEFT and one RIGHT arm.",
                )
            )
            continue
        comparison_id = next(iter(comparison_ids))
        if comparison_id not in comparison_catalog:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "MATCHED_COMPARISON_BINDING_MISMATCH",
                    f"/run/comparison_groups/{group_id}",
                    "The comparison group names no frozen comparison contract.",
                )
            )
            continue
        comparison = comparison_catalog[comparison_id]
        sessions_by_arm = {
            binding["arm"]: session for binding, session in members
        }
        expected_cells = {
            "LEFT": comparison["left_prior_cell_id"],
            "RIGHT": comparison["right_prior_cell_id"],
        }
        if any(
            sessions_by_arm[arm]["source_cell_id"] != expected_cells[arm]
            for arm in ("LEFT", "RIGHT")
        ):
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "MATCHED_COMPARISON_BINDING_MISMATCH",
                    f"/run/comparison_groups/{group_id}",
                    "A comparison arm does not bind its frozen prior cell.",
                )
            )
        pair = [
            sessions_by_arm["LEFT"]["future_option_id"],
            sessions_by_arm["RIGHT"]["future_option_id"],
        ]
        if pair not in comparison["allowed_matched_option_pairs"]:
            candidates.append(
                _candidate(
                    run["run_id"],
                    len(candidates),
                    "MATCHED_FUTURE_OPTION_MISMATCH",
                    f"/run/comparison_groups/{group_id}",
                    "The compared prior paths received different registered future options.",
                )
            )

    report = {
        "$schema": "./development-assessment.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "MECHANICAL_DEFECT_CANDIDATE_SET",
        "artifact_id": f"{run['run_id']}:mechanical-candidates",
        "instrument_sha256": _sha256(instrument_bytes),
        "source_run_sha256": _sha256(run_bytes),
        "status": "CANDIDATES_ONLY_NO_AUTOMATIC_DEFECT_RECEIPT",
        "candidates": candidates,
    }
    try:
        validate_json_schema(
            report,
            _frozen_schema(
                assessment_schema_path,
                FROZEN_ASSESSMENT_SCHEMA_SHA256,
                "development assessment",
            ),
        )
    except ValueError as exc:
        raise MechanicalScanInputError(
            f"mechanical candidate schema validation failed: {exc}"
        ) from exc
    return report


def encode_candidate_set(report: dict[str, Any]) -> bytes:
    return canonical_bytes(report)
