from __future__ import annotations

import ast
import base64
import copy
import hashlib
from pathlib import Path
import unittest

from dynamics.labs import interp_dialogue_p0_v1_builder as p0v1
from dynamics.labs.interp_m1_common import loads_exact


ROOT = Path(__file__).resolve().parents[2]
P0_V1_ROOT = (
    ROOT
    / "research/scenarios/interp-dialogue-001/elicitation/p0-v1"
)


def _load(name: str) -> dict:
    return loads_exact((P0_V1_ROOT / name).read_bytes())


class InterpDialogueP0V1Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.files = p0v1.build_all(ROOT)
        cls.surface = _load("participant-surface-v1.json")
        cls.catalog = _load("rendered-surface-catalog-v1.json")
        cls.candidates = _load("revision-resolution-candidates-v1.json")
        cls.decisions = _load("p0-decision-receipts-v1.json")
        cls.dispositions = _load("proposal-disposition-record-v1.json")
        cls.instrument = _load("instrument-v1.json")
        cls.manifest = _load("frozen-artifact-manifest-v1.json")
        cls.mapping_candidate_schema = _load(
            "development-assessment-v1.schema.json"
        )
        cls.mapping_attempt_schema = _load("mapping-attempt-v1.schema.json")

    def test_p0_v1_checked_in_artifacts_match_deterministic_rebuild(self) -> None:
        p0v1.verify_all(ROOT)

    def test_p0_v1_frozen_bases_are_byte_identical(self) -> None:
        p0v1.verify_frozen_inputs(ROOT)
        self.assertEqual(len(p0v1.FROZEN_INPUT_SHA256), 10)

    def test_every_proposal_has_exact_candidates_and_every_candidate_one_decision(
        self,
    ) -> None:
        candidates = self.candidates["candidates"]
        candidate_ids = {
            candidate["resolution_candidate_id"] for candidate in candidates
        }
        self.assertEqual(len(candidates), 18)
        self.assertEqual(
            {candidate["source_proposal_id"] for candidate in candidates},
            {f"RP-{index:03d}" for index in range(1, 9)},
        )
        decision_candidate_ids = [
            receipt["resolution_candidate_id"]
            for receipt in self.decisions["decision_receipts"]
        ]
        self.assertEqual(set(decision_candidate_ids), candidate_ids)
        self.assertEqual(len(decision_candidate_ids), len(set(decision_candidate_ids)))

    def test_candidates_have_no_decision_authority(self) -> None:
        for candidate in self.candidates["candidates"]:
            self.assertNotIn("decision", candidate)
            self.assertEqual(
                candidate["authority"],
                "EXACT_REVISION_CANDIDATE_ONLY_NO_ADOPTION_AUTHORITY",
            )
        for receipt in self.decisions["decision_receipts"]:
            self.assertEqual(receipt["decision"], "ACCEPTED")
            self.assertEqual(receipt["semantic_preservation_claim"], "NONE")

    def test_proposal_disposition_is_lineage_not_partial_decision_enum(self) -> None:
        self.assertEqual(len(self.dispositions["proposal_dispositions"]), 8)
        for disposition in self.dispositions["proposal_dispositions"]:
            self.assertNotIn("decision", disposition)
            self.assertNotIn("PARTIALLY_ACCEPTED", disposition.values())
            self.assertEqual(
                disposition["coverage_status"],
                "COVERED_BY_EXACT_CANDIDATE_DECISIONS",
            )

    def test_revision_operations_project_from_basis_without_mutating_it(self) -> None:
        for candidate in self.candidates["candidates"]:
            for operation in candidate["operations"]:
                destination = operation["destination"]
                self.assertEqual(destination["precondition"], "MUST_BE_ABSENT")
                for basis in operation["basis_refs"]:
                    self.assertNotEqual(
                        basis["artifact_id"], destination["artifact_id"]
                    )
                    self.assertEqual(
                        basis["digest_domain"],
                        p0v1.REVISION_BASIS_DIGEST_DOMAIN,
                    )
                    self.assertEqual(
                        basis["canonicalization_profile_id"],
                        p0v1.CANONICALIZATION_PROFILE_ID,
                    )

    def test_accepted_operations_equal_the_frozen_destination_values(self) -> None:
        destination_artifacts = {
            "PARTICIPANT-SURFACE-V1": self.surface,
            "INTERP-DIALOGUE-001P0-ELICITATION-INSTRUMENT-V1": self.instrument,
        }
        for candidate in self.candidates["candidates"]:
            for operation in candidate["operations"]:
                destination = operation["destination"]
                actual = p0v1._resolve_pointer(
                    destination_artifacts[destination["artifact_id"]],
                    destination["json_pointer"],
                )
                self.assertEqual(actual, operation["replacement_value"])

    def test_participant_surface_is_closed_world(self) -> None:
        self.assertEqual(len(self.surface["base_surfaces"]), 3)
        self.assertEqual(len(self.surface["factor_level_surfaces"]), 18)
        self.assertEqual(len(self.surface["future_option_surfaces"]), 6)
        self.assertEqual(len(self.surface["prompt_surfaces"]), 6)
        self.assertEqual(len(self.surface["diagnostic_surfaces"]), 1)
        self.assertEqual(
            self.surface["authority"],
            "PARTICIPANT_REALIZATION_ONLY_NO_SEMANTIC_SOURCE_AUTHORITY",
        )

    def test_participant_surface_excludes_registered_design_language(self) -> None:
        texts = [
            item["participant_text"]
            for collection in (
                "base_surfaces",
                "factor_level_surfaces",
                "future_option_surfaces",
                "prompt_surfaces",
                "diagnostic_surfaces",
            )
            for item in self.surface[collection]
        ]
        combined = "\n".join(texts).casefold()
        for term in (
            "at a new access",
            "prior-material cue",
            "external target evidence",
            "evaluation threat",
            "bodily arousal",
            "the vignette",
            "independently resolved as following",
        ):
            self.assertNotIn(term, combined)

    def test_rel_cue_surface_does_not_claim_actual_access(self) -> None:
        cue_texts = [
            item["participant_text"]
            for item in self.surface["factor_level_surfaces"]
            if item["family_id"] == "REL-BOUNDARY-001"
            and item["factor_id"] == "externally_cued_prior_material"
        ]
        self.assertEqual(len(cue_texts), 2)
        for text in cue_texts:
            self.assertIn("is mentioned again", text)
            self.assertNotIn("comes to mind", text)

    def test_rendered_catalog_freezes_all_final_delivery_bytes(self) -> None:
        deliveries = self.catalog["deliveries"]
        self.assertEqual(len(deliveries), 37)
        self.assertEqual(
            len({item["delivery_surface_id"] for item in deliveries}), 37
        )
        for delivery in deliveries:
            raw = base64.b64decode(delivery["utf8_base64"], validate=True)
            self.assertEqual(raw, delivery["participant_text"].encode("utf-8"))
            self.assertEqual(len(raw), delivery["utf8_byte_length"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(), delivery["utf8_sha256"]
            )

    def test_instrument_closes_exactly_over_catalog_with_no_fallback(self) -> None:
        renderer = self.instrument["renderer_contract"]
        self.assertEqual(renderer["fallback_policy"], "FORBIDDEN")
        self.assertEqual(renderer["semantic_source_direct_text_read"], "FORBIDDEN")
        composition = self.instrument["base_contract_composition"]
        self.assertEqual(composition["participant_text_inheritance"], "FORBIDDEN")
        self.assertTrue(
            {
                "language_policy",
                "rendering_policy",
                "prompt_catalog",
                "presentations",
                "future_option_catalog",
            }
            <= set(composition["replaced_sections"])
        )
        catalog_ids = {
            item["delivery_surface_id"] for item in self.catalog["deliveries"]
        }
        instrument_ids = {
            item["delivery_surface_id"]
            for item in self.instrument["presentations"]
        } | {
            item["delivery_surface_id"]
            for item in self.instrument["future_options"]
        } | {
            item[key]
            for item in self.instrument["family_prompt_deliveries"]
            for key in (
                "immediate_delivery_surface_id",
                "later_delivery_surface_id",
            )
        } | {self.instrument["diagnostic_delivery_surface_id"]}
        self.assertEqual(instrument_ids, catalog_ids)

    def test_p0_v1_preserves_defect_status_without_resolution_claim(self) -> None:
        self.assertEqual(
            self.instrument["confirmed_defect_refs_pending_repilot"],
            [f"DR-{index:03d}" for index in range(1, 10)],
        )
        self.assertEqual(
            self.instrument["open_deferred_defect_refs"],
            ["DR-010", "DR-011", "DR-012", "DR-013"],
        )
        self.assertEqual(
            self.instrument["rejected_defect_receipt_refs"], ["DR-014"]
        )
        self.assertEqual(self.instrument["defect_resolution_claims"], [])
        self.assertEqual(self.manifest["defect_resolution_claims"], [])

    def _candidate_set(self, status: str, alternatives: int) -> dict:
        return {
            "$schema": "./development-assessment-v1.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "DEVELOPMENT_MAPPING_CANDIDATE_SET_V1",
            "candidate_set_id": "SET-001",
            "mapping_attempt_id": "ATTEMPT-001",
            "candidate_status": status,
            "alternatives": [
                {
                    "candidate_id": f"ALT-{index}",
                    "target_coordinate": f"O5:surface:{index}",
                    "analyst_basis": "development-only mapping alternative",
                }
                for index in range(alternatives)
            ],
            "raw_analyst_rationale": "development-only cardinality fixture",
            "authority": "DEVELOPMENT_CANDIDATE_ONLY_NOT_OBSERVATION",
        }

    def test_mapping_candidate_set_cardinality_is_typed(self) -> None:
        valid = {
            "PROPOSED": 1,
            "AMBIGUOUS": 2,
            "NO_MAPPING": 0,
            "OUTSIDE_VOCABULARY": 0,
        }
        for status, alternatives in valid.items():
            p0v1.validate_mapping_candidate_set(
                self._candidate_set(status, alternatives),
                self.mapping_candidate_schema,
            )
        for status, alternatives in {
            "PROPOSED": 0,
            "AMBIGUOUS": 1,
            "NO_MAPPING": 1,
            "OUTSIDE_VOCABULARY": 1,
        }.items():
            with self.assertRaises(p0v1.P0V1ContractError):
                p0v1.validate_mapping_candidate_set(
                    self._candidate_set(status, alternatives),
                    self.mapping_candidate_schema,
                )

    def _attempt_ledger(self, attempt: dict) -> dict:
        return {
            "$schema": "./mapping-attempt-v1.schema.json",
            "schema_version": "1.0.0",
            "artifact_type": "DEVELOPMENT_MAPPING_ATTEMPT_LEDGER_V1",
            "artifact_id": "INTERP-DIALOGUE-MAPPING-ATTEMPT-LEDGER-V1",
            "mapping_policy_version": "INTERP-DIALOGUE-DEVELOPMENT-MAPPING-V1",
            "candidate_set_schema_sha256": hashlib.sha256(
                (P0_V1_ROOT / "development-assessment-v1.schema.json").read_bytes()
            ).hexdigest(),
            "authority": "LINEAGE_ONLY_NO_FROZEN_OBSERVATION_MAPPING",
            "attempts": [attempt],
        }

    def test_mapping_attempt_keeps_empty_responded_payload_lineage(self) -> None:
        attempt = {
            "mapping_attempt_id": "ATTEMPT-EMPTY",
            "response_event_id": "RUN:SESSION:R1",
            "response_disposition": "RESPONDED",
            "payload_evaluability": "NOT_EVALUABLE_EMPTY_PAYLOAD",
            "attempt_disposition": "NOT_EVALUABLE",
            "reason_code": "PRESENT_ZERO_BYTE_PAYLOAD",
            "candidate_set_ref": "",
            "authority": "MAPPING_ATTEMPT_LINEAGE_ONLY_NOT_OBSERVATION",
        }
        p0v1.validate_mapping_attempt_ledger(
            self._attempt_ledger(attempt), self.mapping_attempt_schema, {}
        )

    def test_mapping_attempt_rejects_silent_candidate_omission(self) -> None:
        applied = {
            "mapping_attempt_id": "ATTEMPT-APPLIED",
            "response_event_id": "RUN:SESSION:R1",
            "response_disposition": "RESPONDED",
            "payload_evaluability": "EVALUABLE",
            "attempt_disposition": "APPLIED",
            "reason_code": "POLICY_APPLIED",
            "candidate_set_ref": "",
            "authority": "MAPPING_ATTEMPT_LINEAGE_ONLY_NOT_OBSERVATION",
        }
        with self.assertRaises(p0v1.P0V1ContractError):
            p0v1.validate_mapping_attempt_ledger(
                self._attempt_ledger(applied), self.mapping_attempt_schema, {}
            )

        skipped = copy.deepcopy(applied)
        skipped["mapping_attempt_id"] = "ATTEMPT-SKIPPED"
        skipped["attempt_disposition"] = "NOT_APPLIED"
        skipped["candidate_set_ref"] = "SET-001"
        with self.assertRaises(p0v1.P0V1ContractError):
            p0v1.validate_mapping_attempt_ledger(
                self._attempt_ledger(skipped),
                self.mapping_attempt_schema,
                {"SET-001": self._candidate_set("PROPOSED", 1)},
            )

    def test_manifest_binds_every_p0_v1_artifact_except_itself(self) -> None:
        entries = {item["path"]: item for item in self.manifest["artifacts"]}
        for filename, payload in self.files.items():
            if filename == "frozen-artifact-manifest-v1.json":
                continue
            relpath = (
                "research/scenarios/interp-dialogue-001/elicitation/p0-v1/"
                + filename
            )
            self.assertEqual(entries[relpath]["sha256"], hashlib.sha256(payload).hexdigest())

    def test_p0_v1_builder_has_no_runtime_model_authority_imports(self) -> None:
        source = (
            ROOT / "dynamics/labs/interp_dialogue_p0_v1_builder.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        forbidden = {
            "dynamics.engine",
            "dynamics.models",
            "dynamics.protocol",
            "dynamics.routing",
            "dynamics.contract",
        }
        self.assertTrue(imports.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
