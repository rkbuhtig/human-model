from __future__ import annotations

import ast
import base64
from collections import Counter
from copy import deepcopy
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from dynamics.labs import interp_dialogue_elicitation_contract as contract
from dynamics.labs import interp_dialogue_elicitation_runner as runner
from dynamics.labs import interp_dialogue_elicitation_scanner as scanner
from dynamics.labs.interp_dialogue_scenario_contract import loads_exact
from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    file_sha256,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
ELICITATION_ROOT = (
    ROOT / "research" / "scenarios" / "interp-dialogue-001" / "elicitation"
)
INSTRUMENT_PATH = ELICITATION_ROOT / "instrument-v0.json"
INSTRUMENT_SCHEMA_PATH = ELICITATION_ROOT / "instrument.schema.json"
SESSION_SCHEMA_PATH = ELICITATION_ROOT / "session-input.schema.json"
RUN_SCHEMA_PATH = ELICITATION_ROOT / "run.schema.json"
ASSESSMENT_SCHEMA_PATH = (
    ELICITATION_ROOT / "development-assessment.schema.json"
)
CONTRACT_PATH = (
    ROOT / "dynamics" / "labs" / "interp_dialogue_elicitation_contract.py"
)
RUNNER_PATH = (
    ROOT / "dynamics" / "labs" / "interp_dialogue_elicitation_runner.py"
)
SCANNER_PATH = (
    ROOT / "dynamics" / "labs" / "interp_dialogue_elicitation_scanner.py"
)


def _sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def _present_payload(raw: bytes) -> dict[str, object]:
    return {
        "status": "PRESENT",
        "encoding": "BASE64_OF_EXACT_UTF8_BYTES",
        "raw_payload_utf8_base64": base64.b64encode(raw).decode("ascii"),
        "byte_length": len(raw),
        "content_sha256": _sha256(raw),
        "normalization": "NONE",
    }


def _submission(status: str, raw: bytes | None = None) -> dict[str, object]:
    if status == "RESPONDED":
        if raw is None:
            raise AssertionError("test RESPONDED submission requires raw bytes")
        payload = _present_payload(raw)
    else:
        if raw is not None:
            raise AssertionError("test absent submission cannot carry raw bytes")
        payload = {"status": "ABSENT", "reason": status}
    return {"response_status": status, "raw_payload_record": payload}


def _session(
    session_id: str,
    presentation_id: str,
    future_option_id: str,
    *,
    immediate: dict[str, object] | None = None,
    later: dict[str, object] | None = None,
    diagnostic: dict[str, object] | None = None,
    comparison_binding: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "session_id": session_id,
        "presentation_id": presentation_id,
        "future_option_id": future_option_id,
        "comparison_binding": comparison_binding or {"status": "NOT_APPLICABLE"},
        "responses": {
            "immediate": immediate or _submission("RESPONDED", b"immediate"),
            "later": later or _submission("RESPONDED", b"later"),
            "post_trace_diagnostic": diagnostic or {"mode": "OMITTED"},
        },
    }


def _session_input(
    instrument: dict[str, object],
    instrument_bytes: bytes,
    sessions: list[dict[str, object]],
    *,
    run_id: str = "elicitation-test-run",
) -> dict[str, object]:
    return {
        "$schema": "./session-input.schema.json",
        "schema_version": "1.0.0",
        "artifact_type": "DEVELOPMENT_ELICITATION_SCRIPT_INPUT",
        "run_id": run_id,
        "instrument_binding": {
            "instrument_id": instrument["instrument_id"],
            "instrument_version": instrument["instrument_version"],
            "content_sha256": _sha256(instrument_bytes),
        },
        "source_kind": "SCRIPTED_ADVERSARIAL_RESPONSE",
        "sessions": sessions,
    }


def _event(session: dict[str, object], step_id: str) -> dict[str, object]:
    return next(
        item
        for item in session["event_log"]
        if item["elicitation_step_id"] == step_id
    )


def _all_keys(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _all_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _all_keys(child)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


class InterpDialogueElicitationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instrument_bytes = INSTRUMENT_PATH.read_bytes()
        cls.instrument = contract.load_and_validate_elicitation_instrument(
            INSTRUMENT_PATH
        )
        cls.instrument_schema = loads_exact(INSTRUMENT_SCHEMA_PATH.read_bytes())
        cls.session_schema = loads_exact(SESSION_SCHEMA_PATH.read_bytes())
        cls.run_schema = loads_exact(RUN_SCHEMA_PATH.read_bytes())
        cls.assessment_schema = loads_exact(ASSESSMENT_SCHEMA_PATH.read_bytes())

        # The decomposed accent is deliberate: provenance must preserve source
        # bytes rather than NFC-normalize them.  Internal-model vocabulary in a
        # response must likewise remain raw content rather than become a cast.
        cls.raw_immediate = (
            "e\u0301 / OUT_OF_MODEL / subjective_encounter_form / \U0001f98a"
        ).encode("utf-8")
        cls.raw_diagnostic = b"scripted diagnostic detail"
        cls.clean_sessions = [
            _session(
                "session-exact-utf8",
                "PRES-REL-000-EN-V0",
                "FUTURE-REL-0",
                immediate=_submission("RESPONDED", cls.raw_immediate),
                later=_submission("REFUSED"),
                diagnostic={
                    "mode": "COLLECTED_AFTER_R2",
                    "response": _submission("RESPONDED", cls.raw_diagnostic),
                },
            ),
            _session(
                "session-missing-statuses",
                "PRES-WORK-001-EN-V0",
                "FUTURE-WORK-0",
                immediate=_submission("NO_RESPONSE"),
                later=_submission("TECHNICAL_FAILURE"),
            ),
        ]
        cls.clean_input = _session_input(
            cls.instrument, cls.instrument_bytes, cls.clean_sessions
        )
        cls.clean_input_bytes = canonical_bytes(cls.clean_input)
        cls.clean_run = runner.materialize_scripted_elicitation_replay(
            cls.instrument_bytes, cls.clean_input_bytes
        )
        cls.clean_run_bytes = runner.encode_run(cls.clean_run)

    def _scan(self, run: dict[str, object]) -> dict[str, object]:
        return scanner.scan_mechanical_defects(
            self.instrument_bytes, canonical_bytes(run)
        )

    def _codes(self, report: dict[str, object]) -> set[str]:
        return {item["defect_code"] for item in report["candidates"]}

    def _inspection_report(self) -> dict[str, object]:
        raw_report = b"Author walkthrough notes only."
        raw_payload = _present_payload(raw_report)
        del raw_payload["status"]
        return {
            "$schema": "./development-assessment.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "DEVELOPMENT_INSTRUMENT_INSPECTION_REPORT",
            "artifact_id": "author-walkthrough-test",
            "instrument_sha256": _sha256(self.instrument_bytes),
            "inspection_identity": {
                "inspection_kind": "AUTHOR_COGNITIVE_WALKTHROUGH",
                "inspector_role": "AUTHOR_DEVELOPMENT_INSPECTOR",
            },
            "coverage_refs": ["/prompt_catalog/0"],
            "raw_report_payload": raw_payload,
            "status": "INSPECTION_SOURCE_ONLY_NO_AUTOMATIC_DEFECT_RECEIPT",
            "candidate_items": [
                {
                    "inspection_candidate_id": "inspection-candidate-1",
                    "instrument_item_ref": "/prompt_catalog/0",
                    "candidate_code": "AMBIGUOUS_ITEM",
                    "note_pointer": "/notes/0",
                    "authority": (
                        "DEVELOPMENT_INSPECTION_CANDIDATE_NOT_DEFECT_RECEIPT"
                    ),
                }
            ],
            "authority": (
                "EVALUATOR_SIDE_INSPECTION_NOT_RESPONSE_OR_MECHANISM_RESULT"
            ),
        }

    def test_frozen_instrument_has_exact_source_coverage_and_renderability(self) -> None:
        self.assertEqual(
            file_sha256(INSTRUMENT_PATH), contract.FROZEN_INSTRUMENT_SHA256
        )
        self.assertEqual(
            file_sha256(INSTRUMENT_SCHEMA_PATH),
            contract.FROZEN_INSTRUMENT_SCHEMA_SHA256,
        )
        self.assertEqual(len(self.instrument["presentations"]), 24)
        self.assertEqual(len(self.instrument["future_option_catalog"]), 6)
        self.assertEqual(len(self.instrument["matched_future_comparisons"]), 3)
        self.assertEqual(
            Counter(
                item["family_id"] for item in self.instrument["presentations"]
            ),
            Counter(
                {
                    "REL-BOUNDARY-001": 8,
                    "WORK-FEEDBACK-001": 8,
                    "RISK-FOOTSTEPS-001": 8,
                }
            ),
        )
        covered = {
            (item["family_id"], item["source_cell_id"])
            for item in self.instrument["presentations"]
        }
        self.assertEqual(len(covered), 24)
        for presentation in self.instrument["presentations"]:
            rendered = contract.render_initial_presentation(
                self.instrument, presentation["presentation_id"]
            )
            self.assertTrue(rendered)
            self.assertFalse(
                any("\uac00" <= character <= "\ud7a3" for character in rendered)
            )
        for option in self.instrument["future_option_catalog"]:
            self.assertTrue(
                contract.render_future_option(
                    self.instrument, option["future_option_id"]
                )
            )

    def test_compiled_context_reuses_verified_sources_without_file_reads(self) -> None:
        context = contract.compile_instrument_context(INSTRUMENT_PATH)
        self.assertEqual(context.instrument_sha256, _sha256(self.instrument_bytes))
        self.assertEqual(len(context.presentations), 24)
        self.assertEqual(len(context.future_options), 6)

        presentation_id = self.instrument["presentations"][0]["presentation_id"]
        future_option_id = self.instrument["future_option_catalog"][0][
            "future_option_id"
        ]
        expected_presentation = contract.render_initial_presentation(
            self.instrument, presentation_id, instrument_path=INSTRUMENT_PATH
        )
        expected_future = contract.render_future_option(
            self.instrument, future_option_id, instrument_path=INSTRUMENT_PATH
        )

        with patch.object(Path, "read_bytes", side_effect=AssertionError("hidden read")):
            self.assertEqual(
                contract.render_initial_presentation(context, presentation_id),
                expected_presentation,
            )
            self.assertEqual(
                contract.render_future_option(context, future_option_id),
                expected_future,
            )
            self.assertTrue(
                contract.prompt_text(context, "P_GENERIC_IMMEDIATE_RESPONSE")
            )

    def test_instrument_authority_mapping_and_processing_roles_are_closed(self) -> None:
        self.assertEqual(
            self.instrument["status"],
            "FROZEN_UNEXECUTED_DEVELOPMENT_ELICITATION_ONLY",
        )
        self.assertEqual(
            self.instrument["authority"],
            {
                "artifact_role": "DEVELOPMENT_ELICITATION_INSTRUMENT_CONTRACT",
                "execution_status": "UNEXECUTED",
                "measurement_status": "NO_FROZEN_RESPONSE_TO_INTERNAL_TRACE_MAPPING",
                "empirical_status": "NO_RESPONSE_DATA",
                "output_status": "NO_OBSERVATION_PLACEMENT_OR_CLAIM_RESULT",
            },
        )
        boundary = self.instrument["mapping_boundary"]
        self.assertEqual(boundary["runner_mapping_output"], "FORBIDDEN")
        self.assertEqual(
            {
                (item["observation_point_id"], item["trace_field_id"])
                for item in boundary["eligible_future_candidates"]
            },
            {
                ("O5_IMMEDIATE_SURFACE_RECORDED", "immediate_surface"),
                ("O10_LATER_SURFACE_RECORDED", "later_surface"),
            },
        )
        taxonomy = self.instrument["defect_taxonomy"]
        mechanical = set(taxonomy["mechanical_candidate_codes"])
        structural = set(taxonomy["structural_rejection_codes"])
        analyst = set(taxonomy["analyst_only_codes"])
        self.assertFalse(mechanical & structural)
        self.assertFalse(mechanical & analyst)
        self.assertFalse(structural & analyst)
        self.assertEqual(structural, {"FORCED_INTERNAL_TRACE_CAST"})
        roles = {
            item["role"]: item for item in self.instrument["processing_role_contract"]
        }
        self.assertEqual(
            roles["SCRIPTED_REPLAY_MATERIALIZER"]["may_emit"],
            "IMMUTABLE_SCRIPTED_REPLAY_AND_PROVENANCE_ONLY",
        )
        self.assertEqual(
            roles["MECHANICAL_DEFECT_SCANNER"]["may_emit"],
            "MECHANICAL_DEFECT_CANDIDATE_ONLY",
        )
        self.assertFalse(
            self.instrument["revision_proposal_contract"][
                "p1_may_execute_revised_instrument"
            ]
        )

    def test_materializer_is_scripted_replay_only_and_rejects_occurrence_claims(
        self,
    ) -> None:
        self.assertEqual(
            self.instrument["development_source_kinds"],
            ["SCRIPTED_ADVERSARIAL_RESPONSE"],
        )
        self.assertIn(
            "ACTUAL_PARTICIPANT_DELIVERY_OR_RESPONSE_OCCURRENCE",
            self.instrument["response_provenance_contract"][
                "response_does_not_prove"
            ],
        )
        self.assertEqual(
            self.clean_run["artifact_type"],
            "DEVELOPMENT_ELICITATION_SCRIPTED_REPLAY",
        )
        self.assertEqual(
            self.clean_run["status"],
            "IMMUTABLE_SCRIPTED_REPLAY_NO_ACTUAL_OCCURRENCE_OR_MECHANISM_RESULT",
        )
        self.assertEqual(
            self.clean_run["authority"],
            {
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
        )

        author_source = deepcopy(self.clean_input)
        author_source["source_kind"] = "AUTHOR_AS_RESPONDENT"
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError, "session input schema validation"
        ):
            runner.materialize_scripted_elicitation_replay(
                self.instrument_bytes, canonical_bytes(author_source)
            )

        occurrence_claims = []
        run_authority = deepcopy(self.clean_run)
        run_authority["authority"]["empirical_status"] = (
            "ACTUAL_PARTICIPANT_OCCURRENCE"
        )
        occurrence_claims.append(("run authority", run_authority))

        delivery_authority = deepcopy(self.clean_run)
        delivery = _event(
            delivery_authority["sessions"][0],
            "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY",
        )
        delivery["authority"] = "ACTUAL_PROMPT_DELIVERY_OCCURRENCE"
        occurrence_claims.append(("delivery authority", delivery_authority))

        response_authority = deepcopy(self.clean_run)
        response = _event(
            response_authority["sessions"][0],
            "R1_IMMEDIATE_RESPONSE_EVENT",
        )
        response["authority"] = "FIRST_PERSON_ATTESTATION_RECEIPT"
        occurrence_claims.append(("response authority", response_authority))

        link_authority = deepcopy(self.clean_run)
        link_authority["sessions"][0]["response_provenance_links"][0][
            "authority"
        ] = "LINKS_ACTUAL_RESPONSE_OCCURRENCE_TO_DELIVERY"
        occurrence_claims.append(("link authority", link_authority))

        for label, artifact in occurrence_claims:
            with self.subTest(label=label), self.assertRaises(ValueError):
                validate_json_schema(artifact, self.run_schema)

    def test_runner_rejects_rewritten_instrument_under_the_same_version(self) -> None:
        changed = deepcopy(self.instrument)
        changed["prompt_catalog"][0]["participant_text"] += " Changed after freeze."
        changed_bytes = canonical_bytes(changed)
        changed_input = _session_input(
            changed,
            changed_bytes,
            [
                _session(
                    "same-version-drift",
                    "PRES-REL-000-EN-V0",
                    "FUTURE-REL-0",
                )
            ],
            run_id="same-version-drift-run",
        )
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError, "frozen P0-v0 instrument"
        ):
            runner.materialize_scripted_elicitation_replay(
                changed_bytes, canonical_bytes(changed_input)
            )

    def test_raw_utf8_response_bytes_are_preserved_without_normalization(self) -> None:
        session = self.clean_run["sessions"][0]
        response = _event(session, "R1_IMMEDIATE_RESPONSE_EVENT")
        payload = response["payload_record"]
        decoded = base64.b64decode(
            payload["raw_payload_utf8_base64"], validate=True
        )
        self.assertEqual(decoded, self.raw_immediate)
        self.assertEqual(payload["byte_length"], len(self.raw_immediate))
        self.assertEqual(payload["content_sha256"], _sha256(self.raw_immediate))
        self.assertEqual(payload["normalization"], "NONE")
        self.assertIn(b"e\xcc\x81", decoded)
        self.assertNotIn("normalized", payload)

    def test_noncanonical_base64_is_rejected_at_each_payload_schema(self) -> None:
        inspection = self._inspection_report()
        validate_json_schema(inspection, self.assessment_schema)

        for encoded in ("A", "YQ=", "YQ==="):
            with self.subTest(encoded=encoded, artifact="session-input"):
                session_input = deepcopy(self.clean_input)
                session_input["sessions"][0]["responses"]["immediate"][
                    "raw_payload_record"
                ]["raw_payload_utf8_base64"] = encoded
                with self.assertRaises(ValueError):
                    validate_json_schema(session_input, self.session_schema)
                with self.assertRaisesRegex(
                    runner.ScriptedReplayInputError,
                    "session input schema validation",
                ):
                    runner.materialize_scripted_elicitation_replay(
                        self.instrument_bytes, canonical_bytes(session_input)
                    )

            with self.subTest(encoded=encoded, artifact="run"):
                run = deepcopy(self.clean_run)
                response = _event(
                    run["sessions"][0], "R1_IMMEDIATE_RESPONSE_EVENT"
                )
                response["payload_record"][
                    "raw_payload_utf8_base64"
                ] = encoded
                with self.assertRaises(ValueError):
                    validate_json_schema(run, self.run_schema)
                with self.assertRaises(scanner.MechanicalScanInputError):
                    scanner.scan_mechanical_defects(
                        self.instrument_bytes, canonical_bytes(run)
                    )

            with self.subTest(encoded=encoded, artifact="inspection"):
                invalid_inspection = deepcopy(inspection)
                invalid_inspection["raw_report_payload"][
                    "raw_payload_utf8_base64"
                ] = encoded
                with self.assertRaises(ValueError):
                    validate_json_schema(
                        invalid_inspection, self.assessment_schema
                    )

    def test_response_statuses_remain_four_distinct_recorded_states(self) -> None:
        observed = {
            event["response_status"]: event["payload_record"]
            for session in self.clean_run["sessions"]
            for event in session["event_log"]
            if event["event_kind"] == "SCRIPTED_RESPONSE_RECORD"
        }
        self.assertEqual(
            set(observed),
            {"RESPONDED", "REFUSED", "NO_RESPONSE", "TECHNICAL_FAILURE"},
        )
        self.assertEqual(observed["RESPONDED"]["status"], "PRESENT")
        for status in ("REFUSED", "NO_RESPONSE", "TECHNICAL_FAILURE"):
            self.assertEqual(
                observed[status], {"status": "ABSENT", "reason": status}
            )

    def test_inconsistent_response_status_and_payload_is_rejected(self) -> None:
        session = _session(
            "collapsed-missing-input",
            "PRES-RISK-001-EN-V0",
            "FUTURE-RISK-0",
        )
        session["responses"]["immediate"] = {
            "response_status": "NO_RESPONSE",
            "raw_payload_record": _present_payload(b"not actually missing"),
        }
        document = _session_input(
            self.instrument,
            self.instrument_bytes,
            [session],
            run_id="collapsed-missing-input-run",
        )
        with self.assertRaises(runner.ScriptedReplayInputError):
            runner.materialize_scripted_elicitation_replay(
                self.instrument_bytes, canonical_bytes(document)
            )

    def test_runner_and_encoding_are_byte_deterministic(self) -> None:
        second = runner.materialize_scripted_elicitation_replay(
            self.instrument_bytes, self.clean_input_bytes
        )
        self.assertEqual(second, self.clean_run)
        self.assertEqual(runner.encode_run(second), self.clean_run_bytes)
        self.assertEqual(loads_exact(self.clean_run_bytes), self.clean_run)
        first_scan = scanner.scan_mechanical_defects(
            self.instrument_bytes, self.clean_run_bytes
        )
        second_scan = scanner.scan_mechanical_defects(
            self.instrument_bytes, self.clean_run_bytes
        )
        self.assertEqual(first_scan, second_scan)
        self.assertEqual(
            scanner.encode_candidate_set(first_scan),
            scanner.encode_candidate_set(second_scan),
        )

    def test_prompt_delivery_events_are_not_oracle_observation_points(self) -> None:
        session = self.clean_run["sessions"][0]
        steps = [item["elicitation_step_id"] for item in session["event_log"]]
        self.assertEqual(
            steps[:6],
            [
                "E0_INITIAL_VIGNETTE_DELIVERY",
                "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY",
                "R1_IMMEDIATE_RESPONSE_EVENT",
                "E2_MATCHED_FUTURE_OPTION_DELIVERY",
                "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY",
                "R2_LATER_RESPONSE_EVENT",
            ],
        )
        self.assertTrue(all(not step.startswith("O") for step in steps))
        expected_prompt = {
            "R1_IMMEDIATE_RESPONSE_EVENT": (
                "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY"
            ),
            "R2_LATER_RESPONSE_EVENT": "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY",
            "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT": (
                "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY"
            ),
        }
        for response_step, prompt_step in expected_prompt.items():
            response = _event(session, response_step)
            prompt = _event(session, prompt_step)
            self.assertEqual(
                response["prompt_delivery_event_id"], prompt["event_id"]
            )
            self.assertEqual(
                prompt["authority"],
                (
                    "SCRIPTED_DELIVERY_RECORD_NOT_ACTUAL_OCCURRENCE_OR_"
                    "ORDINAL_OBSERVATION"
                ),
            )

    def test_post_trace_diagnostic_is_append_only_after_r2(self) -> None:
        session = self.clean_run["sessions"][0]
        r2 = _event(session, "R2_LATER_RESPONSE_EVENT")
        d0 = _event(session, "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY")
        rd0 = _event(session, "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT")
        self.assertEqual((r2["sequence_ordinal"], d0["sequence_ordinal"], rd0["sequence_ordinal"]), (5, 6, 7))
        prompt = next(
            item
            for item in self.instrument["prompt_catalog"]
            if item["prompt_id"] == "P_POST_TRACE_DIAGNOSTIC"
        )
        self.assertEqual(
            prompt["authority"],
            "RETROSPECTIVE_DIAGNOSTIC_NOT_ORDINAL_OBSERVATION",
        )
        omitted = self.clean_run["sessions"][1]
        self.assertEqual(len(omitted["event_log"]), 6)
        self.assertNotIn(
            "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY",
            {item["elicitation_step_id"] for item in omitted["event_log"]},
        )

    def test_response_provenance_links_cover_each_response_exactly(self) -> None:
        for session in self.clean_run["sessions"]:
            events = {item["event_id"]: item for item in session["event_log"]}
            responses = {
                key
                for key, item in events.items()
                if item["event_kind"] == "SCRIPTED_RESPONSE_RECORD"
            }
            links = {
                item["response_event_id"]: item
                for item in session["response_provenance_links"]
            }
            self.assertEqual(set(links), responses)
            for response_id, link in links.items():
                response = events[response_id]
                prompt = events[link["prompt_delivery_event_id"]]
                self.assertEqual(
                    response["prompt_delivery_event_id"], prompt["event_id"]
                )
                self.assertEqual(
                    link["delivered_prompt_sha256"],
                    prompt["payload_record"]["content_sha256"],
                )
                self.assertEqual(
                    link["authority"],
                    (
                        "LINKS_SCRIPTED_RESPONSE_RECORD_TO_SCRIPTED_DELIVERY_"
                        "CONTEXT_ONLY"
                    ),
                )

    def test_runner_emits_no_mapping_defect_or_out_of_model_classification(self) -> None:
        self.assertEqual(
            self.clean_run["authority"]["mapping_status"], "NO_MAPPING_EMITTED"
        )
        self.assertEqual(
            self.clean_run["authority"]["defect_status"],
            "NO_DEFECT_CLASSIFICATION_EMITTED",
        )
        keys = {key.casefold() for key in _all_keys(self.clean_run)}
        self.assertTrue(
            {
                "mapping",
                "development_mapping_candidate",
                "defect_code",
                "defect_receipt",
                "out_of_model",
                "observation_status",
                "trace_field_id",
                "placement_winner",
                "revision_proposal",
            }.isdisjoint(keys)
        )
        # The same words are allowed in exact scripted-source bytes; they do not
        # gain classification authority merely by being present in a record.
        response = _event(
            self.clean_run["sessions"][0], "R1_IMMEDIATE_RESPONSE_EVENT"
        )
        self.assertIn(
            b"OUT_OF_MODEL",
            base64.b64decode(
                response["payload_record"]["raw_payload_utf8_base64"]
            ),
        )

    def test_clean_scanner_output_is_candidate_only_and_has_no_receipt(self) -> None:
        report = scanner.scan_mechanical_defects(
            self.instrument_bytes, self.clean_run_bytes
        )
        validate_json_schema(report, self.assessment_schema)
        self.assertEqual(report["artifact_type"], "MECHANICAL_DEFECT_CANDIDATE_SET")
        self.assertEqual(
            report["status"], "CANDIDATES_ONLY_NO_AUTOMATIC_DEFECT_RECEIPT"
        )
        self.assertEqual(report["candidates"], [])
        keys = {key.casefold() for key in _all_keys(report)}
        self.assertTrue(
            {
                "defect_receipt",
                "adjudication_status",
                "placement_winner",
                "revision_proposal",
                "claim_evidence_link",
            }.isdisjoint(keys)
        )

    def test_scanner_detects_matched_future_option_mismatch(self) -> None:
        comparison_id = "future.rel.same_projection"
        sessions = [
            _session(
                "matched-left",
                "PRES-REL-000-EN-V0",
                "FUTURE-REL-0",
                comparison_binding={
                    "status": "PRESENT",
                    "comparison_group_id": "rel-group-1",
                    "comparison_id": comparison_id,
                    "arm": "LEFT",
                },
            ),
            _session(
                "matched-right",
                "PRES-REL-100-EN-V0",
                "FUTURE-REL-1",
                comparison_binding={
                    "status": "PRESENT",
                    "comparison_group_id": "rel-group-1",
                    "comparison_id": comparison_id,
                    "arm": "RIGHT",
                },
            ),
        ]
        document = _session_input(
            self.instrument,
            self.instrument_bytes,
            sessions,
            run_id="future-mismatch-run",
        )
        run = runner.materialize_scripted_elicitation_replay(
            self.instrument_bytes, canonical_bytes(document)
        )
        report = self._scan(run)
        self.assertIn("MATCHED_FUTURE_OPTION_MISMATCH", self._codes(report))
        self.assertTrue(
            all(
                item["authority"]
                == "MECHANICAL_DEFECT_CANDIDATE_NOT_INSTRUMENT_DEFECT_RECEIPT"
                for item in report["candidates"]
            )
        )

    def test_scanner_detects_order_and_unlogged_prompt_candidates(self) -> None:
        reordered = deepcopy(self.clean_run)
        log = reordered["sessions"][0]["event_log"]
        log[1], log[2] = log[2], log[1]
        self.assertIn("PROMPT_ORDER_VIOLATION", self._codes(self._scan(reordered)))

        unlogged = deepcopy(self.clean_run)
        r1 = _event(unlogged["sessions"][0], "R1_IMMEDIATE_RESPONSE_EVENT")
        r1["prompt_delivery_event_id"] = "unlogged-prompt-event"
        self.assertIn("UNLOGGED_PROMPT_DELIVERY", self._codes(self._scan(unlogged)))

    def test_step_event_kind_mismatch_is_typed_not_a_scanner_crash(self) -> None:
        mismatched = deepcopy(self.clean_run)
        session = mismatched["sessions"][0]
        e0 = _event(session, "E0_INITIAL_VIGNETTE_DELIVERY")
        e1 = _event(
            session, "E1_GENERIC_IMMEDIATE_RESPONSE_PROMPT_DELIVERY"
        )
        e0["event_kind"] = "SCRIPTED_RESPONSE_RECORD"
        e0["prompt_delivery_event_id"] = e1["event_id"]
        e0["response_status"] = "RESPONDED"
        e0["authority"] = (
            "SCRIPTED_RESPONSE_RECORD_AND_PAYLOAD_PROVENANCE_ONLY"
        )
        validate_json_schema(mismatched, self.run_schema)
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError,
            "event kinds do not match the frozen elicitation steps",
        ):
            runner.validate_run_artifact(mismatched)
        self.assertIn(
            "PROMPT_ORDER_VIOLATION", self._codes(self._scan(mismatched))
        )

    def test_wrong_but_logged_prompt_link_is_rejected_and_scanned(self) -> None:
        wrong = deepcopy(self.clean_run)
        session = wrong["sessions"][0]
        r1 = _event(session, "R1_IMMEDIATE_RESPONSE_EVENT")
        e3 = _event(session, "E3_GENERIC_LATER_RESPONSE_PROMPT_DELIVERY")
        r1["prompt_delivery_event_id"] = e3["event_id"]
        link = next(
            item
            for item in session["response_provenance_links"]
            if item["response_event_id"] == r1["event_id"]
        )
        link["prompt_delivery_event_id"] = e3["event_id"]
        link["delivered_prompt_sha256"] = e3["payload_record"]["content_sha256"]
        with self.assertRaises(runner.ScriptedReplayInputError):
            runner.validate_run_artifact(wrong)
        codes = self._codes(self._scan(wrong))
        self.assertIn("PROMPT_ORDER_VIOLATION", codes)
        self.assertIn("RESPONSE_PROVENANCE_LINK_MISMATCH", codes)

    def test_scanner_detects_self_consistent_delivery_payload_drift(self) -> None:
        drifted = deepcopy(self.clean_run)
        session = drifted["sessions"][0]
        e0 = _event(session, "E0_INITIAL_VIGNETTE_DELIVERY")
        replacement = _present_payload(b"self-consistent but wrong delivered bytes")
        e0["payload_record"] = replacement
        for link in session["response_provenance_links"]:
            for index, event_id in enumerate(link["context_delivery_event_ids"]):
                if event_id == e0["event_id"]:
                    link["context_payload_sha256"][index] = replacement[
                        "content_sha256"
                    ]
        codes = self._codes(self._scan(drifted))
        self.assertIn("DELIVERY_PAYLOAD_MISMATCH", codes)
        self.assertNotIn("RAW_PAYLOAD_PROVENANCE_BREAK", codes)

    def test_scanner_detects_session_binding_drift(self) -> None:
        drifted = deepcopy(self.clean_run)
        drifted["sessions"][0]["source_cell_id"] = "rel-111"
        self.assertIn(
            "SESSION_BINDING_MISMATCH", self._codes(self._scan(drifted))
        )

    def test_duplicate_session_and_cross_session_ids_are_typed_defects(self) -> None:
        duplicate_session = deepcopy(self.clean_run)
        duplicate_session["sessions"][1]["session_id"] = (
            duplicate_session["sessions"][0]["session_id"]
        )
        validate_json_schema(duplicate_session, self.run_schema)
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError, "run repeats session_id"
        ):
            runner.validate_run_artifact(duplicate_session)
        self.assertIn(
            "SESSION_BINDING_MISMATCH",
            self._codes(self._scan(duplicate_session)),
        )

        reused_event = deepcopy(self.clean_run)
        first_event_id = _event(
            reused_event["sessions"][0], "E0_INITIAL_VIGNETTE_DELIVERY"
        )["event_id"]
        _event(
            reused_event["sessions"][1], "E0_INITIAL_VIGNETTE_DELIVERY"
        )["event_id"] = first_event_id
        validate_json_schema(reused_event, self.run_schema)
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError,
            "run repeats an event_id across sessions",
        ):
            runner.validate_run_artifact(reused_event)
        self.assertIn(
            "RESPONSE_PROVENANCE_LINK_MISMATCH",
            self._codes(self._scan(reused_event)),
        )

        reused_link = deepcopy(self.clean_run)
        first_link_id = reused_link["sessions"][0][
            "response_provenance_links"
        ][0]["link_id"]
        reused_link["sessions"][1]["response_provenance_links"][0][
            "link_id"
        ] = first_link_id
        validate_json_schema(reused_link, self.run_schema)
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError,
            "run repeats response provenance link_id across sessions",
        ):
            runner.validate_run_artifact(reused_link)
        self.assertIn(
            "RESPONSE_PROVENANCE_LINK_MISMATCH",
            self._codes(self._scan(reused_link)),
        )

    def test_scanner_detects_missingness_and_raw_provenance_candidates(self) -> None:
        collapsed = deepcopy(self.clean_run)
        r1 = _event(collapsed["sessions"][0], "R1_IMMEDIATE_RESPONSE_EVENT")
        r1["response_status"] = "NO_RESPONSE"
        self.assertIn("MISSINGNESS_COLLAPSE", self._codes(self._scan(collapsed)))

        broken = deepcopy(self.clean_run)
        r1 = _event(broken["sessions"][0], "R1_IMMEDIATE_RESPONSE_EVENT")
        r1["payload_record"]["byte_length"] += 1
        self.assertIn("RAW_PAYLOAD_PROVENANCE_BREAK", self._codes(self._scan(broken)))

    def test_scanner_detects_diagnostic_delivery_before_r2(self) -> None:
        early = deepcopy(self.clean_run)
        log = early["sessions"][0]["event_log"]
        d0 = log.pop(6)
        log.insert(5, d0)
        codes = self._codes(self._scan(early))
        self.assertIn("POST_TRACE_DIAGNOSTIC_EARLY_DELIVERY", codes)
        self.assertIn("PROMPT_ORDER_VIOLATION", codes)

    def test_scanner_detects_incomplete_and_cross_contract_comparison_groups(
        self,
    ) -> None:
        left_only = _session_input(
            self.instrument,
            self.instrument_bytes,
            [
                _session(
                    "left-only",
                    "PRES-REL-000-EN-V0",
                    "FUTURE-REL-0",
                    comparison_binding={
                        "status": "PRESENT",
                        "comparison_group_id": "incomplete-group",
                        "comparison_id": "future.rel.same_projection",
                        "arm": "LEFT",
                    },
                )
            ],
            run_id="incomplete-comparison-run",
        )
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError, "comparison group is incomplete"
        ):
            runner.materialize_scripted_elicitation_replay(
                self.instrument_bytes, canonical_bytes(left_only)
            )
        left_run = deepcopy(self.clean_run)
        left_run["sessions"][0]["comparison_binding"] = {
            "status": "PRESENT",
            "comparison_group_id": "incomplete-group",
            "comparison_id": "future.rel.same_projection",
            "arm": "LEFT",
        }
        self.assertIn(
            "MATCHED_COMPARISON_BINDING_MISMATCH",
            self._codes(self._scan(left_run)),
        )

        cross_contract = _session_input(
            self.instrument,
            self.instrument_bytes,
            [
                _session(
                    "cross-rel-left",
                    "PRES-REL-000-EN-V0",
                    "FUTURE-REL-0",
                    comparison_binding={
                        "status": "PRESENT",
                        "comparison_group_id": "cross-contract-group",
                        "comparison_id": "future.rel.same_projection",
                        "arm": "LEFT",
                    },
                ),
                _session(
                    "cross-work-right",
                    "PRES-WORK-100-EN-V0",
                    "FUTURE-WORK-0",
                    comparison_binding={
                        "status": "PRESENT",
                        "comparison_group_id": "cross-contract-group",
                        "comparison_id": "future.work.same_projection",
                        "arm": "RIGHT",
                    },
                ),
            ],
            run_id="cross-contract-comparison-run",
        )
        with self.assertRaisesRegex(
            runner.ScriptedReplayInputError, "mixes comparison contracts"
        ):
            runner.materialize_scripted_elicitation_replay(
                self.instrument_bytes, canonical_bytes(cross_contract)
            )
        cross_run = deepcopy(self.clean_run)
        cross_run["sessions"][0]["comparison_binding"] = {
            "status": "PRESENT",
            "comparison_group_id": "cross-contract-group",
            "comparison_id": "future.rel.same_projection",
            "arm": "LEFT",
        }
        cross_run["sessions"][1]["comparison_binding"] = {
            "status": "PRESENT",
            "comparison_group_id": "cross-contract-group",
            "comparison_id": "future.work.same_projection",
            "arm": "RIGHT",
        }
        self.assertIn(
            "MATCHED_COMPARISON_BINDING_MISMATCH",
            self._codes(self._scan(cross_run)),
        )

    def test_scanner_detects_literal_leaks_as_candidates_not_receipts(self) -> None:
        cases = (
            (
                "Move toward a lit public area while continuing to observe.",
                "DESIGN_ANCHOR_LITERAL_LEAK",
            ),
            ("Ghost candidate_set", "INTERNAL_IDENTIFIER_LITERAL_LEAK"),
        )
        for text, expected in cases:
            with self.subTest(expected=expected), patch.object(
                scanner,
                "_participant_texts",
                return_value=[("/instrument/test", text)],
            ):
                report = scanner.scan_mechanical_defects(
                    self.instrument_bytes, self.clean_run_bytes
                )
                self.assertIn(expected, self._codes(report))
                self.assertNotIn("receipts", report)

    def test_forced_internal_trace_cast_is_rejected_not_scanner_laundered(self) -> None:
        cast = deepcopy(self.clean_run)
        cast["sessions"][0]["subjective_encounter_form"] = "forced"
        with self.assertRaises(ValueError):
            validate_json_schema(cast, self.run_schema)
        with self.assertRaises(scanner.MechanicalScanInputError):
            scanner.scan_mechanical_defects(
                self.instrument_bytes, canonical_bytes(cast)
            )
        taxonomy = self.instrument["defect_taxonomy"]
        self.assertIn(
            "FORCED_INTERNAL_TRACE_CAST", taxonomy["structural_rejection_codes"]
        )
        self.assertNotIn(
            "FORCED_INTERNAL_TRACE_CAST", taxonomy["mechanical_candidate_codes"]
        )
        receipt_codes = self.assessment_schema["$defs"]["defectReceipt"][
            "properties"
        ]["defect_code"]["enum"]
        self.assertNotIn("FORCED_INTERNAL_TRACE_CAST", receipt_codes)

    def test_assessment_schema_forbids_mechanism_and_placement_promotion(self) -> None:
        receipt_set = {
            "$schema": "./development-assessment.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "INSTRUMENT_DEFECT_ADJUDICATION_SET",
            "artifact_id": "defect-adjudication-test",
            "instrument_sha256": _sha256(self.instrument_bytes),
            "source_artifact_sha256": ["0" * 64],
            "status": "DEVELOPMENT_DEFECT_ADJUDICATION_ONLY",
            "receipts": [
                {
                    "defect_receipt_id": "defect-receipt-1",
                    "candidate_refs": ["candidate:1"],
                    "defect_code": "AMBIGUOUS_ITEM",
                    "adjudication_status": "CONFIRMED",
                    "analyst_basis": "The item admits two readings.",
                    "authority": (
                        "INSTRUMENT_DEFECT_ADJUDICATION_ONLY_NO_MECHANISM_RESULT"
                    ),
                }
            ],
        }
        validate_json_schema(receipt_set, self.assessment_schema)

        placement = deepcopy(receipt_set)
        placement["receipts"][0]["placement_winner"] = "TargetForm"
        with self.assertRaises(ValueError):
            validate_json_schema(placement, self.assessment_schema)

        mechanism_code = deepcopy(receipt_set)
        mechanism_code["receipts"][0]["defect_code"] = (
            "HUMAN_MECHANISM_CONFIRMED"
        )
        with self.assertRaises(ValueError):
            validate_json_schema(mechanism_code, self.assessment_schema)

        mechanism_result = deepcopy(receipt_set)
        mechanism_result["human_mechanism_result"] = "CONFIRMED"
        with self.assertRaises(ValueError):
            validate_json_schema(mechanism_result, self.assessment_schema)

    def test_author_walkthrough_is_evaluator_side_and_identity_coupled(self) -> None:
        report = self._inspection_report()
        validate_json_schema(report, self.assessment_schema)

        language_report = deepcopy(report)
        language_report["artifact_id"] = "language-inspection-test"
        language_report["inspection_identity"] = {
            "inspection_kind": "LANGUAGE_COMPREHENSION_INSPECTION",
            "inspector_role": "LANGUAGE_DEVELOPMENT_INSPECTOR",
        }
        validate_json_schema(language_report, self.assessment_schema)

        mismatched_identity = deepcopy(report)
        mismatched_identity["inspection_identity"]["inspector_role"] = (
            "LANGUAGE_DEVELOPMENT_INSPECTOR"
        )
        with self.assertRaises(ValueError):
            validate_json_schema(mismatched_identity, self.assessment_schema)

        promoted_to_response = deepcopy(report)
        promoted_to_response["authority"] = "FIRST_PERSON_RESPONSE_ATTESTATION"
        with self.assertRaises(ValueError):
            validate_json_schema(promoted_to_response, self.assessment_schema)

        participant_response = deepcopy(report)
        participant_response["participant_response"] = "not permitted"
        with self.assertRaises(ValueError):
            validate_json_schema(participant_response, self.assessment_schema)

        mechanism_result = deepcopy(report)
        mechanism_result["mechanism_result"] = "CONFIRMED"
        with self.assertRaises(ValueError):
            validate_json_schema(mechanism_result, self.assessment_schema)

    def test_mapping_candidates_are_limited_to_surface_coordinates(self) -> None:
        mapping = {
            "$schema": "./development-assessment.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "DEVELOPMENT_MAPPING_CANDIDATE_SET",
            "artifact_id": "mapping-candidates-test",
            "instrument_sha256": _sha256(self.instrument_bytes),
            "source_run_sha256": _sha256(self.clean_run_bytes),
            "status": "CANDIDATES_ONLY_NO_FROZEN_MAPPING",
            "candidates": [
                {
                    "mapping_candidate_id": "mapping-candidate-1",
                    "response_event_id": (
                        "elicitation-test-run:session-exact-utf8:"
                        "R1_IMMEDIATE_RESPONSE_EVENT"
                    ),
                    "source_phase": "IMMEDIATE",
                    "eligible_target_coordinate": {
                        "observation_point_id": "O5_IMMEDIATE_SURFACE_RECORDED",
                        "trace_field_id": "immediate_surface",
                    },
                    "mapping_rule_candidate_version": "mapping-v0",
                    "candidate_status": "PROPOSED_SURFACE_MAPPING",
                    "analyst_basis": "Development proposal only.",
                    "authority": (
                        "DEVELOPMENT_MAPPING_CANDIDATE_ONLY_NOT_OBSERVATION"
                    ),
                }
            ],
        }
        validate_json_schema(mapping, self.assessment_schema)
        forced = deepcopy(mapping)
        forced["candidates"][0]["eligible_target_coordinate"] = {
            "observation_point_id": "O8_LATER_ENCOUNTER_WINDOW_CLOSED",
            "trace_field_id": "subjective_encounter_form",
        }
        with self.assertRaises(ValueError):
            validate_json_schema(forced, self.assessment_schema)

        phase_mismatch = deepcopy(mapping)
        phase_mismatch["candidates"][0]["eligible_target_coordinate"] = {
            "observation_point_id": "O10_LATER_SURFACE_RECORDED",
            "trace_field_id": "later_surface",
        }
        with self.assertRaises(ValueError):
            validate_json_schema(phase_mismatch, self.assessment_schema)

    def test_revision_schema_permits_proposal_but_not_adoption_or_execution(self) -> None:
        proposal = {
            "$schema": "./development-assessment.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "INSTRUMENT_REVISION_PROPOSAL_SET",
            "artifact_id": "revision-proposals-test",
            "base_instrument_sha256": _sha256(self.instrument_bytes),
            "source_defect_adjudication_sha256": ["1" * 64],
            "supporting_source_artifact_sha256": [
                _sha256(self.clean_run_bytes)
            ],
            "status": "PROPOSED_NOT_ADOPTED",
            "proposals": [
                {
                    "proposal_id": "revision-proposal-1",
                    "defect_receipt_refs": ["defect-receipt-1"],
                    "target_json_pointer": "/prompt_catalog/0/participant_text",
                    "proposed_change": "Clarify the generic wording.",
                    "rationale": "Development defect only.",
                    "status": "PROPOSED_NOT_ADOPTED",
                    "execution_status": "UNEXECUTED",
                    "authority": "FUTURE_P0_VERSION_DECISION_REQUIRED",
                }
            ],
        }
        validate_json_schema(proposal, self.assessment_schema)

        no_adjudication_source = deepcopy(proposal)
        del no_adjudication_source["source_defect_adjudication_sha256"]
        with self.assertRaises(ValueError):
            validate_json_schema(no_adjudication_source, self.assessment_schema)

        no_supporting_source = deepcopy(proposal)
        del no_supporting_source["supporting_source_artifact_sha256"]
        with self.assertRaises(ValueError):
            validate_json_schema(no_supporting_source, self.assessment_schema)

        old_run_only_provenance = deepcopy(proposal)
        del old_run_only_provenance["source_defect_adjudication_sha256"]
        del old_run_only_provenance["supporting_source_artifact_sha256"]
        old_run_only_provenance["source_run_sha256"] = [
            _sha256(self.clean_run_bytes)
        ]
        with self.assertRaises(ValueError):
            validate_json_schema(
                old_run_only_provenance, self.assessment_schema
            )

        adopted = deepcopy(proposal)
        adopted["proposals"][0]["status"] = "ADOPTED"
        with self.assertRaises(ValueError):
            validate_json_schema(adopted, self.assessment_schema)

        executed = deepcopy(proposal)
        executed["proposals"][0]["execution_status"] = "EXECUTED"
        with self.assertRaises(ValueError):
            validate_json_schema(executed, self.assessment_schema)

    def test_contract_runner_and_scanner_imports_preserve_role_separation(self) -> None:
        contract_imports = _imports(CONTRACT_PATH)
        runner_imports = _imports(RUNNER_PATH)
        scanner_imports = _imports(SCANNER_PATH)
        forbidden_runtime_prefixes = (
            "dynamics.engine",
            "dynamics.models",
            "dynamics.contract",
            "dynamics.protocol",
        )
        for label, imports in (
            ("contract", contract_imports),
            ("runner", runner_imports),
            ("scanner", scanner_imports),
        ):
            with self.subTest(label=label):
                self.assertFalse(
                    any(
                        name.startswith(forbidden_runtime_prefixes)
                        for name in imports
                    ),
                    imports,
                )
        self.assertNotIn(
            "dynamics.labs.interp_dialogue_elicitation_scanner", runner_imports
        )
        self.assertNotIn(
            "dynamics.labs.interp_dialogue_elicitation_runner", scanner_imports
        )
        self.assertFalse(
            any("adjudicator" in name.casefold() for name in runner_imports)
        )
        self.assertFalse(
            any("adjudicator" in name.casefold() for name in scanner_imports)
        )


if __name__ == "__main__":
    unittest.main()
