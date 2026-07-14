from __future__ import annotations

import ast
import base64
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from dynamics.labs import interp_dialogue_p1_runner as p1
from dynamics.labs.interp_m1_common import loads_exact, validate_json_schema

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = ROOT / "research" / "scenarios" / "interp-dialogue-001"
ELICITATION_ROOT = SCENARIO_ROOT / "elicitation"
P1_ROOT = ELICITATION_ROOT / "p1"

RESPONSE_STEPS = {
    "R1_IMMEDIATE_RESPONSE_EVENT",
    "R2_LATER_RESPONSE_EVENT",
    "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load(path: Path) -> dict:
    return loads_exact(path.read_bytes())


class InterpDialogueP1Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = p1.build_all(ROOT)
        cls.corpus, cls.corpus_bytes = p1.load_response_corpus()
        cls.manifest = p1.load_coverage_manifest(
            corpus=cls.corpus, corpus_bytes=cls.corpus_bytes
        )
        cls.runs = [
            _load(path) for path in sorted((P1_ROOT / "runs").glob("run-*.json"))
        ]
        cls.instrument = _load(ELICITATION_ROOT / "instrument-v0.json")

    # ------------------------------------------------------------ diff guard

    def test_p1_frozen_inputs_are_byte_identical_to_p0_freeze(self) -> None:
        p1.verify_frozen_inputs(ROOT)
        protected = {
            "instrument-v0.json",
            "instrument.schema.json",
            "session-input.schema.json",
            "run.schema.json",
            "development-assessment.schema.json",
            "rel-boundary.json",
            "work-feedback.json",
            "risk-footsteps.json",
            "trace-oracle-v1.json",
            "trace-oracle.md",
        }
        self.assertEqual(
            {Path(relpath).name for relpath in p1.FROZEN_INPUT_SHA256},
            protected,
        )

    # ---------------------------------------------------------- determinism

    def test_p1_replay_is_byte_deterministic(self) -> None:
        rebuilt = p1.build_all(ROOT)
        self.assertEqual(sorted(rebuilt), sorted(self.artifacts))
        for relpath, payload in self.artifacts.items():
            self.assertEqual(
                rebuilt[relpath], payload, f"nondeterministic artifact {relpath}"
            )

    def test_p1_compiles_frozen_source_graph_once_per_build(self) -> None:
        with patch.object(
            p1,
            "compile_instrument_context",
            wraps=p1.compile_instrument_context,
        ) as compile_spy:
            p1.build_all(ROOT)

        self.assertEqual(compile_spy.call_count, 1)

    def test_p1_checked_in_artifacts_match_deterministic_rebuild(self) -> None:
        p1.verify_all(ROOT)

    def test_p1_artifact_manifest_digests_match_files(self) -> None:
        manifest = _load(P1_ROOT / "runs" / "artifact-manifest-v0.json")
        self.assertEqual(
            manifest["coverage_manifest_sha256"],
            _sha256((P1_ROOT / "coverage-manifest-v0.json").read_bytes()),
        )
        self.assertEqual(
            manifest["response_corpus_sha256"],
            _sha256((P1_ROOT / "response-corpus-v0.json").read_bytes()),
        )
        self.assertGreaterEqual(len(manifest["artifacts"]), 4 * 24)
        for entry in manifest["artifacts"]:
            self.assertEqual(
                entry["sha256"],
                _sha256((ROOT / entry["path"]).read_bytes()),
                f"artifact manifest digest mismatch for {entry['path']}",
            )

    # -------------------------------------------------------------- coverage

    def test_p1_manifest_covers_all_presentations(self) -> None:
        covered = {
            session["presentation_id"]
            for run in self.manifest["runs"]
            for session in run["sessions"]
        }
        expected = {
            item["presentation_id"] for item in self.instrument["presentations"]
        }
        self.assertEqual(covered, expected)
        self.assertEqual(len(expected), 24)

    def test_p1_manifest_covers_all_future_options(self) -> None:
        covered = {
            session["future_option_id"]
            for run in self.manifest["runs"]
            for session in run["sessions"]
        }
        expected = {
            item["future_option_id"]
            for item in self.instrument["future_option_catalog"]
        }
        self.assertEqual(covered, expected)
        self.assertEqual(len(expected), 6)

    def test_p1_matched_pairs_cover_both_arms_and_options(self) -> None:
        coverage: dict[str, set[tuple[str, str]]] = {}
        for run in self.manifest["runs"]:
            for session in run["sessions"]:
                binding = session["comparison_binding"]
                if binding["status"] != "PRESENT":
                    continue
                coverage.setdefault(binding["comparison_id"], set()).add(
                    (binding["arm"], session["future_option_id"])
                )
        for comparison in self.instrument["matched_future_comparisons"]:
            options = {
                option
                for pair in comparison["allowed_matched_option_pairs"]
                for option in pair
            }
            expected = {
                (arm, option)
                for arm in ("LEFT", "RIGHT")
                for option in options
            }
            self.assertEqual(
                coverage[comparison["comparison_id"]],
                expected,
                comparison["comparison_id"],
            )

    def test_p1_declares_at_least_thirty_unique_sessions(self) -> None:
        session_ids = [
            session["session_id"]
            for run in self.manifest["runs"]
            for session in run["sessions"]
        ]
        self.assertGreaterEqual(len(session_ids), 30)
        self.assertEqual(len(session_ids), len(set(session_ids)))
        materialized = [
            session["session_id"]
            for run in self.runs
            for session in run["sessions"]
        ]
        self.assertEqual(sorted(materialized), sorted(session_ids))

    # ------------------------------------------------------------ provenance

    def _response_events(self):
        for run in self.runs:
            for session in run["sessions"]:
                for event in session["event_log"]:
                    if event["event_kind"] == "SCRIPTED_RESPONSE_RECORD":
                        yield run, session, event

    def test_p1_preserves_empty_responded_payload(self) -> None:
        found = False
        for _, _, event in self._response_events():
            payload = event["payload_record"]
            if (
                event["response_status"] == "RESPONDED"
                and payload["byte_length"] == 0
            ):
                found = True
                self.assertEqual(payload["status"], "PRESENT")
                self.assertEqual(payload["raw_payload_utf8_base64"], "")
                self.assertEqual(payload["content_sha256"], _sha256(b""))
        self.assertTrue(found, "no empty RESPONDED payload was replayed")

    def test_p1_preserves_whitespace_payload_distinct_from_empty(self) -> None:
        whitespace = "  \t  ".encode("utf-8")
        found = False
        for _, _, event in self._response_events():
            payload = event["payload_record"]
            if (
                payload.get("status") == "PRESENT"
                and payload["content_sha256"] == _sha256(whitespace)
            ):
                found = True
                self.assertEqual(payload["byte_length"], len(whitespace))
                raw = base64.b64decode(payload["raw_payload_utf8_base64"])
                self.assertEqual(raw, whitespace)
        self.assertTrue(found, "no whitespace-only RESPONDED payload replayed")

    def test_p1_preserves_unicode_and_line_endings(self) -> None:
        lf = 'They would say: "I understand."\nThen they would wait.'.encode()
        crlf = 'They would say: "I understand."\r\nThen they would wait.'.encode()
        seen: dict[str, bytes] = {}
        for _, _, event in self._response_events():
            payload = event["payload_record"]
            if payload.get("status") != "PRESENT":
                continue
            raw = base64.b64decode(payload["raw_payload_utf8_base64"])
            self.assertEqual(len(raw), payload["byte_length"])
            self.assertEqual(_sha256(raw), payload["content_sha256"])
            if raw in (lf, crlf):
                seen[payload["content_sha256"]] = raw
            text = raw.decode("utf-8")
            if "彼女" in text:
                self.assertIn("😌👍", text)
                # the corpus deliberately stores the NFD form; NFC
                # normalization anywhere in the pipeline would erase it
                self.assertIn("café", text)
                self.assertNotIn("café", text)
        self.assertEqual(
            len(seen), 2, "LF and CRLF variants did not both survive replay"
        )

    def test_p1_keeps_response_dispositions_distinct(self) -> None:
        statuses = set()
        for _, _, event in self._response_events():
            status = event["response_status"]
            statuses.add(status)
            payload = event["payload_record"]
            if status == "RESPONDED":
                self.assertEqual(payload["status"], "PRESENT")
                self.assertEqual(payload["normalization"], "NONE")
            else:
                self.assertEqual(payload["status"], "ABSENT")
                self.assertEqual(payload["reason"], status)
        self.assertEqual(
            statuses,
            {"RESPONDED", "REFUSED", "NO_RESPONSE", "TECHNICAL_FAILURE"},
        )

    def test_p1_d0_never_precedes_r2(self) -> None:
        collected = 0
        omitted = 0
        for run in self.runs:
            for session in run["sessions"]:
                steps = {
                    event["elicitation_step_id"]: event["sequence_ordinal"]
                    for event in session["event_log"]
                }
                if "D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY" in steps:
                    collected += 1
                    self.assertGreater(
                        steps["D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY"],
                        steps["R2_LATER_RESPONSE_EVENT"],
                    )
                    self.assertGreater(
                        steps["RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT"],
                        steps["D0_POST_TRACE_DIAGNOSTIC_PROMPT_DELIVERY"],
                    )
                else:
                    omitted += 1
                    self.assertNotIn(
                        "RD0_RETROSPECTIVE_DIAGNOSTIC_RESPONSE_EVENT", steps
                    )
        self.assertGreater(collected, 0)
        self.assertGreater(omitted, 0)

    def test_p1_sequence_ordinals_are_schedule_order_only(self) -> None:
        forbidden_fragments = (
            "occurred_at",
            "available_at",
            "processed_at",
            "timestamp",
            "latency",
            "duration",
        )

        def walk(value, path="$"):
            if isinstance(value, dict):
                for key, child in value.items():
                    lowered = key.casefold()
                    for fragment in forbidden_fragments:
                        self.assertNotIn(
                            fragment, lowered, f"invented time at {path}/{key}"
                        )
                    walk(child, f"{path}/{key}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    walk(child, f"{path}/{index}")

        for run in self.runs:
            walk(run)
            for session in run["sessions"]:
                ordinals = [
                    event["sequence_ordinal"] for event in session["event_log"]
                ]
                self.assertEqual(ordinals, list(range(len(ordinals))))

    # ----------------------------------------------------------- assessments

    def test_p1_mechanical_sets_bind_their_runs(self) -> None:
        run_files = sorted((P1_ROOT / "runs").glob("run-*.json"))
        candidate_files = sorted(
            (P1_ROOT / "assessment" / "mechanical").glob(
                "mechanical-candidates-*.json"
            )
        )
        self.assertEqual(len(run_files), len(candidate_files))
        for run_file, candidate_file in zip(run_files, candidate_files):
            candidate_set = _load(candidate_file)
            self.assertEqual(
                candidate_set["source_run_sha256"],
                _sha256(run_file.read_bytes()),
            )
            self.assertEqual(
                candidate_set["status"],
                "CANDIDATES_ONLY_NO_AUTOMATIC_DEFECT_RECEIPT",
            )

    def test_p1_mapping_candidates_cover_only_responded_events(self) -> None:
        mapping_files = sorted(
            (P1_ROOT / "assessment" / "mapping").glob("mapping-candidates-*.json")
        )
        self.assertEqual(len(mapping_files), len(self.runs))
        statuses = set()
        for mapping_file, run in zip(mapping_files, self.runs):
            mapping_set = _load(mapping_file)
            self.assertEqual(
                mapping_set["status"], "CANDIDATES_ONLY_NO_FROZEN_MAPPING"
            )
            events = {
                event["event_id"]: event
                for session in run["sessions"]
                for event in session["event_log"]
            }
            for candidate in mapping_set["candidates"]:
                statuses.add(candidate["candidate_status"])
                event = events[candidate["response_event_id"]]
                self.assertEqual(event["response_status"], "RESPONDED")
                self.assertEqual(
                    candidate["authority"],
                    "DEVELOPMENT_MAPPING_CANDIDATE_ONLY_NOT_OBSERVATION",
                )
        self.assertEqual(
            statuses,
            {
                "PROPOSED_SURFACE_MAPPING",
                "AMBIGUOUS_SURFACE_MAPPING",
                "NO_SURFACE_MAPPING_PROPOSED",
                "OUTSIDE_CURRENT_MAPPING_VOCABULARY_CANDIDATE",
            },
        )

    def test_p1_assessment_artifacts_validate_against_frozen_schema(self) -> None:
        schema = _load(ELICITATION_ROOT / "development-assessment.schema.json")
        for relpath in (
            "assessment/author-walkthrough-v0.json",
            "assessment/language-comprehension-inspection-v0.json",
            "assessment/analyst-adjudication-v0.json",
            "proposals/instrument-revision-proposals-v0.json",
        ):
            artifact = _load(P1_ROOT / relpath)
            validate_json_schema(artifact, schema)

    def test_p1_inspection_payload_digests_are_exact(self) -> None:
        for relpath in (
            "assessment/author-walkthrough-v0.json",
            "assessment/language-comprehension-inspection-v0.json",
        ):
            artifact = _load(P1_ROOT / relpath)
            payload = artifact["raw_report_payload"]
            raw = base64.b64decode(payload["raw_payload_utf8_base64"])
            self.assertEqual(len(raw), payload["byte_length"])
            self.assertEqual(_sha256(raw), payload["content_sha256"])
            self.assertEqual(
                artifact["instrument_sha256"],
                _sha256((ELICITATION_ROOT / "instrument-v0.json").read_bytes()),
            )

    def test_p1_every_candidate_is_adjudicated_exactly_once(self) -> None:
        walkthrough = _load(P1_ROOT / "assessment" / "author-walkthrough-v0.json")
        language = _load(
            P1_ROOT / "assessment" / "language-comprehension-inspection-v0.json"
        )
        candidate_ids = {
            item["inspection_candidate_id"]
            for artifact in (walkthrough, language)
            for item in artifact["candidate_items"]
        }
        mechanical_ids = set()
        for path in (P1_ROOT / "assessment" / "mechanical").glob("*.json"):
            for candidate in _load(path)["candidates"]:
                mechanical_ids.add(candidate["candidate_id"])
        adjudication = _load(
            P1_ROOT / "assessment" / "analyst-adjudication-v0.json"
        )
        referenced: list[str] = []
        for receipt in adjudication["receipts"]:
            referenced.extend(receipt["candidate_refs"])
            self.assertIn(
                receipt["adjudication_status"],
                {"CONFIRMED", "REJECTED", "DEFERRED", "NOT_EVALUABLE"},
            )
        self.assertEqual(len(referenced), len(set(referenced)))
        self.assertEqual(set(referenced), candidate_ids | mechanical_ids)

    def test_p1_adjudication_preserves_source_lineage(self) -> None:
        adjudication = _load(
            P1_ROOT / "assessment" / "analyst-adjudication-v0.json"
        )
        source_digests = set(adjudication["source_artifact_sha256"])
        expected = {
            _sha256(path.read_bytes())
            for path in (P1_ROOT / "assessment" / "mechanical").glob("*.json")
        }
        expected.add(
            _sha256(
                (P1_ROOT / "assessment" / "author-walkthrough-v0.json").read_bytes()
            )
        )
        expected.add(
            _sha256(
                (
                    P1_ROOT
                    / "assessment"
                    / "language-comprehension-inspection-v0.json"
                ).read_bytes()
            )
        )
        self.assertEqual(source_digests, expected)

    def test_p1_proposals_reference_only_confirmed_receipts(self) -> None:
        adjudication = _load(
            P1_ROOT / "assessment" / "analyst-adjudication-v0.json"
        )
        status_by_receipt = {
            receipt["defect_receipt_id"]: receipt["adjudication_status"]
            for receipt in adjudication["receipts"]
        }
        proposal_set = _load(
            P1_ROOT / "proposals" / "instrument-revision-proposals-v0.json"
        )
        self.assertEqual(proposal_set["status"], "PROPOSED_NOT_ADOPTED")
        self.assertEqual(
            proposal_set["source_defect_adjudication_sha256"],
            [
                _sha256(
                    (
                        P1_ROOT / "assessment" / "analyst-adjudication-v0.json"
                    ).read_bytes()
                )
            ],
        )
        self.assertGreater(len(proposal_set["proposals"]), 0)
        for proposal in proposal_set["proposals"]:
            self.assertEqual(proposal["status"], "PROPOSED_NOT_ADOPTED")
            self.assertEqual(proposal["execution_status"], "UNEXECUTED")
            for receipt_id in proposal["defect_receipt_refs"]:
                self.assertEqual(
                    status_by_receipt[receipt_id],
                    "CONFIRMED",
                    f"{proposal['proposal_id']} grounds on {receipt_id}",
                )

    def test_p1_confirmed_receipts_keep_candidate_lineage(self) -> None:
        adjudication = _load(
            P1_ROOT / "assessment" / "analyst-adjudication-v0.json"
        )
        for receipt in adjudication["receipts"]:
            self.assertTrue(receipt["candidate_refs"])
            self.assertTrue(receipt["analyst_basis"].strip())

    # ------------------------------------------------------------- authority

    def test_p1_runner_imports_preserve_role_separation(self) -> None:
        forbidden = (
            "dynamics.engine",
            "dynamics.models",
            "dynamics.protocol",
            "dynamics.contract",
            "dynamics.epistemics",
            "dynamics.routing",
            "dynamics.types",
            "dynamics.mental_transitions",
            "dynamics.reducer_proposals",
        )
        for module in ("interp_dialogue_p1_runner", "interp_dialogue_p1_run_cli"):
            path = ROOT / "dynamics" / "labs" / f"{module}.py"
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module)
            for name in imports:
                self.assertFalse(
                    any(name.startswith(prefix) for prefix in forbidden),
                    f"{module} imports runtime module {name}",
                )

    def test_p1_emits_no_acquisition_or_adjudication_authority_in_runs(self) -> None:
        for run in self.runs:
            self.assertEqual(
                run["status"],
                "IMMUTABLE_SCRIPTED_REPLAY_NO_ACTUAL_OCCURRENCE_OR_MECHANISM_RESULT",
            )
            self.assertEqual(run["authority"]["mapping_status"], "NO_MAPPING_EMITTED")
            self.assertEqual(
                run["authority"]["defect_status"],
                "NO_DEFECT_CLASSIFICATION_EMITTED",
            )
            text = json.dumps(run)
            self.assertNotIn("OUT_OF_MODEL", text)


if __name__ == "__main__":
    unittest.main()
