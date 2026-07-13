from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable

from dynamics.labs.interp_dialogue_scenario_contract import (
    ScenarioContractError,
    load_and_validate_family,
    load_family,
    loads_exact,
)
from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    file_sha256,
    validate_json_schema,
)


_ROOT = Path(__file__).resolve().parents[2]
_ORACLE_ROOT = _ROOT / "research" / "scenarios" / "interp-dialogue-001"
_DEFAULT_ORACLE_PATH = _ORACLE_ROOT / "trace-oracle-v1.json"
_DEFAULT_SCHEMA_PATH = _ORACLE_ROOT / "trace-oracle.schema.json"

_EXPECTED_FAMILY_PATHS = {
    "REL-BOUNDARY-001": "families/rel-boundary.json",
    "WORK-FEEDBACK-001": "families/work-feedback.json",
    "RISK-FOOTSTEPS-001": "families/risk-footsteps.json",
}
_REQUIRED_RELATIONS = {
    "MUST_REMAIN_EQUAL",
    "MUST_DIFFER_IF_PLACEMENT",
    "MAY_DIFFER_DOWNSTREAM",
    "MUST_DIFFER_BY_DESIGN",
    "MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT",
    "MUST_REMAIN_ABSENT",
    "NOT_EVALUABLE_WITHOUT_FROZEN_REASSESSMENT_POLICY",
    "RELATION_NOT_APPLICABLE",
}
_EXPECTED_RELATION_MEANINGS = {
    "MUST_REMAIN_EQUAL": (
        "The compared projection is equal by design or by the conditional "
        "placement definition; this is not an empirical finding."
    ),
    "MUST_DIFFER_IF_PLACEMENT": (
        "The placement is computationally defined to differ here; this is not "
        "a correct human answer."
    ),
    "MAY_DIFFER_DOWNSTREAM": (
        "A registered upstream difference may propagate here, but direct "
        "residence is not asserted."
    ),
    "MUST_DIFFER_BY_DESIGN": (
        "The declared operational factor record differs by fixture construction, "
        "independently of any placement."
    ),
    "MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT": (
        "A claim-scoped external assessment may differ because the public history "
        "or stimulus record differs; no subjective trace is granted Evidence "
        "authority."
    ),
    "MUST_REMAIN_ABSENT": (
        "The forbidden cast or writer output must be absent in both compared arms."
    ),
    "NOT_EVALUABLE_WITHOUT_FROZEN_REASSESSMENT_POLICY": (
        "The evidence-assessment relation is not evaluated until a separate "
        "claim-scoped reassessment policy is frozen."
    ),
    "RELATION_NOT_APPLICABLE": (
        "The projection is structurally outside this contrast or target scope."
    ),
}
_REQUIRED_OBSERVATIONS = {
    "EQUAL",
    "DIFFERENT",
    "NOT_OBSERVED",
    "OBSERVATION_NOT_APPLICABLE",
}
_EXPECTED_OBSERVATION_MEANINGS = {
    "EQUAL": "The frozen source-specific measurement mapping returned equality.",
    "DIFFERENT": (
        "The frozen source-specific measurement mapping returned a difference."
    ),
    "NOT_OBSERVED": (
        "The protocol did not observe or could not map this field; this is not "
        "equality or zero."
    ),
    "OBSERVATION_NOT_APPLICABLE": (
        "The field does not apply under the registered scope."
    ),
}
_REQUIRED_ADJUDICATIONS = {
    "SIGNATURE_CONFORMS",
    "SIGNATURE_DOES_NOT_CONFORM_UNDER_SCOPE",
    "NOT_EVALUABLE",
    "EMPIRICALLY_UNRESOLVED_UNDER_SCOPE",
    "NOT_IDENTIFIABLE_UNDER_HORIZON",
    "OPERATIONALLY_ALIASED",
    "OUT_OF_MODEL",
    "CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE",
}
_EXPECTED_HORIZON_RELATIONS = {
    "H_PREFIX_BEFORE_K": "PREFIX_BEFORE_K",
    "H_INITIAL_ACCESS_K": "INITIAL_ACCESS_K",
    "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1":
        "REGISTERED_FUTURE_ACCESS_K_PLUS_1",
}
_EXPECTED_HORIZON_METADATA = {
    "H_PREFIX_BEFORE_K": {
        "horizon_id": "H_PREFIX_BEFORE_K",
        "ordinal_relation": "PREFIX_BEFORE_K",
        "start_observation_point_id": "O0_INPUT_ACCEPTED_PRE_ACCESS",
        "end_observation_point_id": "O0_INPUT_ACCEPTED_PRE_ACCESS",
        "authority": "FROZEN_PREFIX_SCOPE_NOT_EMPIRICAL_RESULT",
        "future_probe_count": 0,
        "later_processing_opportunity_count": 0,
    },
    "H_INITIAL_ACCESS_K": {
        "horizon_id": "H_INITIAL_ACCESS_K",
        "ordinal_relation": "INITIAL_ACCESS_K",
        "start_observation_point_id": "O1_INITIAL_ACCESS_WINDOW_CLOSED",
        "end_observation_point_id": "O5_IMMEDIATE_SURFACE_RECORDED",
        "authority": "FROZEN_INITIAL_SCOPE_NOT_EMPIRICAL_RESULT",
        "future_probe_count": 0,
        "later_processing_opportunity_count": 0,
    },
    "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1": {
        "horizon_id": "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1",
        "ordinal_relation": "REGISTERED_FUTURE_ACCESS_K_PLUS_1",
        "start_observation_point_id":
            "O6_MATCHED_FUTURE_PROBE_ACCEPTED_PRE_ACCESS",
        "end_observation_point_id": "O10_LATER_SURFACE_RECORDED",
        "authority": "FROZEN_ONE_FUTURE_PROBE_SCOPE_NOT_EMPIRICAL_RESULT",
        "future_probe_count": 1,
        "later_processing_opportunity_count": 1,
        "same_option_requirement":
            "THE_SAME_REGISTERED_FUTURE_OPTION_ID_IS_APPLIED_TO_BOTH_PRIOR_PATHS",
    },
}
_EXPECTED_OBSERVATION_POINT_METADATA = {
    "O0_INPUT_ACCEPTED_PRE_ACCESS": (
        "H_PREFIX_BEFORE_K", 0, "PREFIX", "OBSERVATION_SLOT_NOT_RESULT"
    ),
    "O1_INITIAL_ACCESS_WINDOW_CLOSED": (
        "H_INITIAL_ACCESS_K", 1, "ACCESS", "OBSERVATION_SLOT_NOT_RESULT"
    ),
    "O2_INITIAL_ENCOUNTER_WINDOW_CLOSED": (
        "H_INITIAL_ACCESS_K", 2, "ENCOUNTER", "OBSERVATION_SLOT_NOT_RESULT"
    ),
    "O3_INITIAL_CANDIDATE_WINDOW_CLOSED": (
        "H_INITIAL_ACCESS_K", 3, "CANDIDATE", "OBSERVATION_SLOT_NOT_RESULT"
    ),
    "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED": (
        "H_INITIAL_ACCESS_K", 4, "ADJUDICATION", "OBSERVATION_SLOT_NOT_RESULT"
    ),
    "O5_IMMEDIATE_SURFACE_RECORDED": (
        "H_INITIAL_ACCESS_K", 5, "SURFACE",
        "OBSERVATION_SLOT_NOT_DESIGN_ANCHOR",
    ),
    "O6_MATCHED_FUTURE_PROBE_ACCEPTED_PRE_ACCESS": (
        "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1", 6, "FUTURE_PROBE_PREFIX",
        "OBSERVATION_SLOT_NOT_RESULT",
    ),
    "O7_LATER_ACCESS_WINDOW_CLOSED": (
        "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1", 7, "ACCESS",
        "OBSERVATION_SLOT_NOT_RESULT",
    ),
    "O8_LATER_ENCOUNTER_WINDOW_CLOSED": (
        "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1", 8, "ENCOUNTER",
        "OBSERVATION_SLOT_NOT_RESULT",
    ),
    "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED": (
        "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1", 9,
        "LATER_FUNCTIONAL_PROJECTION", "OBSERVATION_SLOT_NOT_RESULT",
    ),
    "O10_LATER_SURFACE_RECORDED": (
        "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1", 10, "SURFACE",
        "OBSERVATION_SLOT_NOT_DESIGN_ANCHOR",
    ),
}
_EXPECTED_TRACE_FIELDS = {
    "base_public_record",
    "declared_level_public_record",
    "world_unknowns",
    "prior_occurrence_prefix",
    "external_identity_or_intention_certification",
    "external_target_evidence_link_set",
    "evidence_assessment_by_claim_scope",
    "future_option_public_record",
    "pre_access_target_scoped_readout",
    "material_admission",
    "current_access_source_view",
    "subjective_encounter_form",
    "provisional_target_representation",
    "candidate_set",
    "candidate_source_usage",
    "adjudication",
    "action_affordance",
    "reorganization_projection",
    "immediate_surface",
    "later_surface",
    "action_occurrence",
    "durable_targetform_write",
    "narrative_write",
}
_EXPECTED_TRACE_FIELD_METADATA = {
    "base_public_record": (
        "BASE_PUBLIC_RECORD", "PUBLIC_RECORD_ONLY"
    ),
    "declared_level_public_record": (
        "DECLARED_LEVEL_PUBLIC_RECORD", "INTENTIONALLY_VARIED_INPUT_ONLY"
    ),
    "world_unknowns": (
        "WORLD_UNKNOWNS",
        "BOUND_001A_BASE_STIMULUS_WORLD_UNKNOWNS_ONLY_EXCLUDES_LEVEL_SPECIFIC_FACTS",
    ),
    "prior_occurrence_prefix": (
        "PREFIX_GUARD", "APPEND_ONLY_PREFIX_GUARD"
    ),
    "external_identity_or_intention_certification": (
        "FORBIDDEN_CAST_GUARD",
        "MUST_NOT_BE_CREATED_FROM_SUBJECTIVE_TRACE",
    ),
    "external_target_evidence_link_set": (
        "EVIDENCE_LINK_SET",
        "CLAIM_SCOPED_LINK_SET_SEPARATE_FROM_ASSESSMENT",
    ),
    "evidence_assessment_by_claim_scope": (
        "EVIDENCE_LEDGER", "CLAIM_SCOPED_EXTERNAL_ASSESSMENT_LANE"
    ),
    "future_option_public_record": (
        "DECLARED_FUTURE_OPTION_RECORD", "MATCHED_FUTURE_INPUT_ONLY"
    ),
    "pre_access_target_scoped_readout": (
        "FUNCTIONAL_TRACE",
        "MECHANISM_CANDIDATE_PROJECTION_NOT_OBSERVED_HUMAN_STATE",
    ),
    "material_admission": (
        "FUNCTIONAL_TRACE",
        "MECHANISM_CANDIDATE_PROJECTION_NOT_OBSERVED_HUMAN_STATE",
    ),
    "current_access_source_view": (
        "FUNCTIONAL_TRACE",
        "MECHANISM_CANDIDATE_PROJECTION_NOT_OBSERVED_HUMAN_STATE",
    ),
    "subjective_encounter_form": (
        "FUNCTIONAL_TRACE", "DESCRIPTIVE_PROXY_NOT_QUALIA"
    ),
    "provisional_target_representation": (
        "FUNCTIONAL_TRACE",
        "UNRESOLVED_CATEGORY_CANDIDATE_NOT_ENTITY_CERTIFICATION",
    ),
    "candidate_set": (
        "FUNCTIONAL_TRACE", "CANDIDATE_ONLY_NO_ADOPTION_AUTHORITY"
    ),
    "candidate_source_usage": (
        "FUNCTIONAL_TRACE", "SOURCE_LINEAGE_PROJECTION_ONLY"
    ),
    "adjudication": (
        "FUNCTIONAL_TRACE", "SCOPED_OUTCOME_NOT_WORLD_RESULT"
    ),
    "action_affordance": (
        "FUNCTIONAL_TRACE", "AFFORDANCE_NOT_INTENT_OR_ACTION_OCCURRENCE"
    ),
    "reorganization_projection": (
        "FUNCTIONAL_TRACE",
        "NON_DURABLE_PROJECTION_NO_TARGETFORM_OR_NARRATIVE_WRITE",
    ),
    "immediate_surface": (
        "FUNCTIONAL_TRACE", "OBSERVABLE_ONLY_IF_ELICITED_NOT_DESIGN_ANCHOR"
    ),
    "later_surface": (
        "FUNCTIONAL_TRACE", "OBSERVABLE_ONLY_IF_ELICITED"
    ),
    "action_occurrence": (
        "FUNCTIONAL_TRACE",
        "EXTERNAL_ACTION_OCCURRENCE_NOT_INTENT_OR_AFFORDANCE",
    ),
    "durable_targetform_write": (
        "FORBIDDEN_CAST_GUARD", "NO_WRITER_IN_THIS_STUDY"
    ),
    "narrative_write": (
        "FORBIDDEN_CAST_GUARD", "NO_WRITER_IN_THIS_STUDY"
    ),
}
_EXPECTED_PLACEMENT_CATALOG = {
    "CONDITION_LOCATION": {
        "C0_REGISTERED_TRACE_NULL",
        "CA_ACCESS_FIRST_ASSOCIATION",
        "CE_ENCOUNTER_FIRST_ASSOCIATION",
        "CT_THIRD_REGISTERED_PROJECTION_FIRST_ASSOCIATION",
        "CM_MULTIPLE_REGISTERED_LOCATIONS",
    },
    "TARGET_HISTORY_RESIDENCE": {
        "T0_REGISTERED_TRACE_NULL",
        "TA_ACTIVE_MATERIAL_READOUT",
        "TS_TARGET_SCOPED_READOUT",
        "TC_SLOW_CACHE_READOUT",
    },
    "EXTERNAL_CUE_ROLE": {
        "Q0_DELIVERY_RECORD_ONLY",
        "QA_ADMISSION_OR_ACCESS_ASSOCIATION",
        "QE_ENCOUNTER_ASSOCIATION",
        "QC_CANDIDATE_SOURCE_USE_ASSOCIATION",
    },
    "WORK_ADDENDUM_ROLE": {
        "W0_PUBLIC_RECORD_ONLY",
        "WU_INFORMATION_UPTAKE_ASSOCIATION",
        "WE_ENCOUNTER_ASSOCIATION",
        "WC_CANDIDATE_OR_REVISION_AFFORDANCE_ASSOCIATION",
    },
    "RISK_HISTORY_ROLE": {
        "RH0_CURRENT_TRACE_NULL",
        "RHA_PRIOR_MATERIAL_ACCESS_ASSOCIATION",
        "RHP_PROVISIONAL_CATEGORY_ASSOCIATION",
    },
    "RISK_ROUTE_ROLE": {
        "RR0_PUBLIC_OBSERVATION_ONLY",
        "RRE_ENCOUNTER_ASSOCIATION",
        "RRP_PROVISIONAL_REPRESENTATION_ASSOCIATION",
        "RRA_ACTION_AFFORDANCE_ASSOCIATION",
    },
}
_EXPECTED_PLACEMENT_METADATA = {
    "C0_REGISTERED_TRACE_NULL": (
        "no registered condition association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "CA_ACCESS_FIRST_ASSOCIATION": (
        "access-first association", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "CE_ENCOUNTER_FIRST_ASSOCIATION": (
        "encounter-first association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "CT_THIRD_REGISTERED_PROJECTION_FIRST_ASSOCIATION": (
        "third registered projection-first association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "CM_MULTIPLE_REGISTERED_LOCATIONS": (
        "multiple registered associations",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "T0_REGISTERED_TRACE_NULL": (
        "no registered history residence",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "TA_ACTIVE_MATERIAL_READOUT": (
        "active-material readout", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "TS_TARGET_SCOPED_READOUT": (
        "durable target-scoped state candidate",
        "HYPOTHESIS_CANDIDATE_NO_WRITER_RETENTION_OR_EXISTENCE_CLAIM",
    ),
    "TC_SLOW_CACHE_READOUT": (
        "slow-cache readout candidate",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "Q0_DELIVERY_RECORD_ONLY": (
        "delivery record only", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "QA_ADMISSION_OR_ACCESS_ASSOCIATION": (
        "admission or access association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "QE_ENCOUNTER_ASSOCIATION": (
        "encounter association", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "QC_CANDIDATE_SOURCE_USE_ASSOCIATION": (
        "candidate source-use association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "W0_PUBLIC_RECORD_ONLY": (
        "public record only", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "WU_INFORMATION_UPTAKE_ASSOCIATION": (
        "information-uptake association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "WE_ENCOUNTER_ASSOCIATION": (
        "encounter association", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "WC_CANDIDATE_OR_REVISION_AFFORDANCE_ASSOCIATION": (
        "candidate or revision-affordance association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "RH0_CURRENT_TRACE_NULL": (
        "no registered current history effect",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "RHA_PRIOR_MATERIAL_ACCESS_ASSOCIATION": (
        "prior-material access association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "RHP_PROVISIONAL_CATEGORY_ASSOCIATION": (
        "provisional-category association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "RR0_PUBLIC_OBSERVATION_ONLY": (
        "public observation only", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "RRE_ENCOUNTER_ASSOCIATION": (
        "encounter association", "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
    ),
    "RRP_PROVISIONAL_REPRESENTATION_ASSOCIATION": (
        "provisional-representation association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
    "RRA_ACTION_AFFORDANCE_ASSOCIATION": (
        "action-affordance association",
        "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
    ),
}
_EXPECTED_FACTOR_PROJECTIONS = {
    ("REL-BOUNDARY-001", "reported_current_mood"): (
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "material_admission"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "candidate_set"),
    ),
    ("REL-BOUNDARY-001", "target_history"): (
        ("O0_INPUT_ACCEPTED_PRE_ACCESS", "pre_access_target_scoped_readout"),
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
    ),
    ("REL-BOUNDARY-001", "externally_cued_prior_material"): (
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "candidate_source_usage"),
    ),
    ("WORK-FEEDBACK-001", "reported_evaluation_threat"): (
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "material_admission"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "candidate_set"),
    ),
    ("WORK-FEEDBACK-001", "evaluator_criterion_history"): (
        ("O0_INPUT_ACCEPTED_PRE_ACCESS", "pre_access_target_scoped_readout"),
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
    ),
    ("WORK-FEEDBACK-001", "public_feedback_addendum"): (
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "candidate_source_usage"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "action_affordance"),
    ),
    ("RISK-FOOTSTEPS-001", "reported_pre_event_arousal"): (
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "action_affordance"),
    ),
    ("RISK-FOOTSTEPS-001", "recent_threat_history"): (
        ("O1_INITIAL_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        (
            "O2_INITIAL_ENCOUNTER_WINDOW_CLOSED",
            "provisional_target_representation",
        ),
    ),
    ("RISK-FOOTSTEPS-001", "route_match_observation"): (
        ("O2_INITIAL_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        (
            "O2_INITIAL_ENCOUNTER_WINDOW_CLOSED",
            "provisional_target_representation",
        ),
        ("O3_INITIAL_CANDIDATE_WINDOW_CLOSED", "action_affordance"),
    ),
}
_EXPECTED_FACTOR_PLACEMENT_FAMILY = {
    ("REL-BOUNDARY-001", "reported_current_mood"): "CONDITION_LOCATION",
    ("REL-BOUNDARY-001", "target_history"): "TARGET_HISTORY_RESIDENCE",
    ("REL-BOUNDARY-001", "externally_cued_prior_material"):
        "EXTERNAL_CUE_ROLE",
    ("WORK-FEEDBACK-001", "reported_evaluation_threat"):
        "CONDITION_LOCATION",
    ("WORK-FEEDBACK-001", "evaluator_criterion_history"):
        "TARGET_HISTORY_RESIDENCE",
    ("WORK-FEEDBACK-001", "public_feedback_addendum"):
        "WORK_ADDENDUM_ROLE",
    ("RISK-FOOTSTEPS-001", "reported_pre_event_arousal"):
        "CONDITION_LOCATION",
    ("RISK-FOOTSTEPS-001", "recent_threat_history"): "RISK_HISTORY_ROLE",
    ("RISK-FOOTSTEPS-001", "route_match_observation"): "RISK_ROUTE_ROLE",
}
_EXPECTED_FACTOR_ORACLE_IDS = {
    ("REL-BOUNDARY-001", "reported_current_mood"):
        "oracle.rel.reported_current_mood",
    ("REL-BOUNDARY-001", "target_history"): "oracle.rel.target_history",
    ("REL-BOUNDARY-001", "externally_cued_prior_material"):
        "oracle.rel.externally_cued_prior_material",
    ("WORK-FEEDBACK-001", "reported_evaluation_threat"):
        "oracle.work.reported_evaluation_threat",
    ("WORK-FEEDBACK-001", "evaluator_criterion_history"):
        "oracle.work.evaluator_criterion_history",
    ("WORK-FEEDBACK-001", "public_feedback_addendum"):
        "oracle.work.public_feedback_addendum",
    ("RISK-FOOTSTEPS-001", "reported_pre_event_arousal"):
        "oracle.risk.reported_pre_event_arousal",
    ("RISK-FOOTSTEPS-001", "recent_threat_history"):
        "oracle.risk.recent_threat_history",
    ("RISK-FOOTSTEPS-001", "route_match_observation"):
        "oracle.risk.route_match_observation",
}
_EXPECTED_HYPOTHESIS_PREFIXES = {
    ("REL-BOUNDARY-001", "reported_current_mood"): "rel.mood",
    ("REL-BOUNDARY-001", "target_history"): "rel.history",
    ("REL-BOUNDARY-001", "externally_cued_prior_material"): "rel.cue",
    ("WORK-FEEDBACK-001", "reported_evaluation_threat"): "work.threat",
    ("WORK-FEEDBACK-001", "evaluator_criterion_history"): "work.history",
    ("WORK-FEEDBACK-001", "public_feedback_addendum"): "work.addendum",
    ("RISK-FOOTSTEPS-001", "reported_pre_event_arousal"): "risk.arousal",
    ("RISK-FOOTSTEPS-001", "recent_threat_history"): "risk.history",
    ("RISK-FOOTSTEPS-001", "route_match_observation"): "risk.route",
}
_EXPECTED_HYPOTHESIS_SUFFIXES = {
    "C0_REGISTERED_TRACE_NULL": "c0",
    "CA_ACCESS_FIRST_ASSOCIATION": "ca",
    "CE_ENCOUNTER_FIRST_ASSOCIATION": "ce",
    "CT_THIRD_REGISTERED_PROJECTION_FIRST_ASSOCIATION": "ct",
    "CM_MULTIPLE_REGISTERED_LOCATIONS": "cm",
    "T0_REGISTERED_TRACE_NULL": "t0",
    "TA_ACTIVE_MATERIAL_READOUT": "ta",
    "TS_TARGET_SCOPED_READOUT": "ts",
    "TC_SLOW_CACHE_READOUT": "tc",
    "Q0_DELIVERY_RECORD_ONLY": "q0",
    "QA_ADMISSION_OR_ACCESS_ASSOCIATION": "qa",
    "QE_ENCOUNTER_ASSOCIATION": "qe",
    "QC_CANDIDATE_SOURCE_USE_ASSOCIATION": "qc",
    "W0_PUBLIC_RECORD_ONLY": "w0",
    "WU_INFORMATION_UPTAKE_ASSOCIATION": "wu",
    "WE_ENCOUNTER_ASSOCIATION": "we",
    "WC_CANDIDATE_OR_REVISION_AFFORDANCE_ASSOCIATION": "wc",
    "RH0_CURRENT_TRACE_NULL": "rh0",
    "RHA_PRIOR_MATERIAL_ACCESS_ASSOCIATION": "rha",
    "RHP_PROVISIONAL_CATEGORY_ASSOCIATION": "rhp",
    "RR0_PUBLIC_OBSERVATION_ONLY": "rr0",
    "RRE_ENCOUNTER_ASSOCIATION": "rre",
    "RRP_PROVISIONAL_REPRESENTATION_ASSOCIATION": "rrp",
    "RRA_ACTION_AFFORDANCE_ASSOCIATION": "rra",
}
_EXPECTED_PLACEMENT_RELATION_PATTERNS = {
    "CONDITION_LOCATION": {
        "C0_REGISTERED_TRACE_NULL": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "CA_ACCESS_FIRST_ASSOCIATION": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "CE_ENCOUNTER_FIRST_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "CT_THIRD_REGISTERED_PROJECTION_FIRST_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL",
            "MUST_DIFFER_IF_PLACEMENT",
        ),
        "CM_MULTIPLE_REGISTERED_LOCATIONS": (
            "MUST_DIFFER_IF_PLACEMENT", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
    },
    "TARGET_HISTORY_RESIDENCE": {
        "T0_REGISTERED_TRACE_NULL": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "TA_ACTIVE_MATERIAL_READOUT": (
            "RELATION_NOT_APPLICABLE", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "TS_TARGET_SCOPED_READOUT": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "TC_SLOW_CACHE_READOUT": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
    },
    "EXTERNAL_CUE_ROLE": {
        "Q0_DELIVERY_RECORD_ONLY": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "QA_ADMISSION_OR_ACCESS_ASSOCIATION": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "QE_ENCOUNTER_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "QC_CANDIDATE_SOURCE_USE_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL",
            "MUST_DIFFER_IF_PLACEMENT",
        ),
    },
    "WORK_ADDENDUM_ROLE": {
        "W0_PUBLIC_RECORD_ONLY": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "WU_INFORMATION_UPTAKE_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "WE_ENCOUNTER_ASSOCIATION": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "WC_CANDIDATE_OR_REVISION_AFFORDANCE_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL",
            "MUST_DIFFER_IF_PLACEMENT",
        ),
    },
    "RISK_HISTORY_ROLE": {
        "RH0_CURRENT_TRACE_NULL": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "RHA_PRIOR_MATERIAL_ACCESS_ASSOCIATION": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "RHP_PROVISIONAL_CATEGORY_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MAY_DIFFER_DOWNSTREAM",
            "MUST_DIFFER_IF_PLACEMENT",
        ),
    },
    "RISK_ROUTE_ROLE": {
        "RR0_PUBLIC_OBSERVATION_ONLY": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "RRE_ENCOUNTER_ASSOCIATION": (
            "MUST_DIFFER_IF_PLACEMENT", "MAY_DIFFER_DOWNSTREAM",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "RRP_PROVISIONAL_REPRESENTATION_ASSOCIATION": (
            "MAY_DIFFER_DOWNSTREAM", "MUST_DIFFER_IF_PLACEMENT",
            "MAY_DIFFER_DOWNSTREAM",
        ),
        "RRA_ACTION_AFFORDANCE_ASSOCIATION": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL",
            "MUST_DIFFER_IF_PLACEMENT",
        ),
    },
}
_REQUIRED_ALIAS_SCOPE = {
    "probe_set_id",
    "projection_set_id",
    "horizon_id",
    "source_kind",
    "measurement_mapping_version",
}
_REQUIRED_RAW_RECORD_FIELDS = {
    "raw_observation_id",
    "source_kind",
    "source_provenance",
    "observation_point_id",
    "horizon_id",
    "measurement_mapping_status",
    "immutable_payload_or_digest",
}
_EXPECTED_SCOPE_FAILURE_REQUIREMENTS = {
    "THE_EFFECT_RECURS_UNDER_THE_SAME_REGISTERED_CONTRAST_AND_HORIZON",
    "NO_REGISTERED_PLACEMENT_CAN_REPRESENT_IT",
    "REPRESENTING_IT_IN_AN_EXISTING_DOMAIN_WOULD_REQUIRE_A_FORBIDDEN_CAST",
    "INSTRUMENT_OR_MAPPING_FAILURE_HAS_BEEN_SEPARATELY_EXCLUDED",
}
_EXPECTED_ALIAS_DEFINITION = (
    "Two placements are OPERATIONALLY_ALIASED only when their complete "
    "conditional signatures are identical for every evaluable registered "
    "contrast and matched future branch under all required scope keys."
)
_EXPECTED_DURABLE_CACHE_RULE = (
    "TS_TARGET_SCOPED_READOUT and TC_SLOW_CACHE_READOUT remain "
    "NOT_IDENTIFIABLE_UNDER_HORIZON "
    "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1; neither OPERATIONALLY_ALIASED nor "
    "placement winner, durable-state, or global alias conclusions are permitted "
    "under the current one-future horizon."
)
_EXPECTED_REL_CANDIDATE_PATTERNS = {
    "D0_NO_REGISTERED_LATER_DIFFERENCE": {
        "pattern_id": "D0_NO_REGISTERED_LATER_DIFFERENCE",
        "initial_edge_relation": "MUST_REMAIN_EQUAL",
        "later_edge_relation": "MUST_REMAIN_EQUAL",
    },
    "DC_LATER_CURRENT_CONDITION_ONLY": {
        "pattern_id": "DC_LATER_CURRENT_CONDITION_ONLY",
        "initial_edge_relation": "MUST_REMAIN_EQUAL",
        "later_edge_relation": "MUST_DIFFER_IF_PLACEMENT",
    },
    "DI_INITIAL_RESIDUE_ONLY": {
        "pattern_id": "DI_INITIAL_RESIDUE_ONLY",
        "initial_edge_relation": "MUST_DIFFER_IF_PLACEMENT",
        "later_edge_relation": "MUST_REMAIN_EQUAL",
    },
    "DX_INITIAL_BY_LATER_INTERACTION": {
        "pattern_id": "DX_INITIAL_BY_LATER_INTERACTION",
        "initial_edge_relation": "MAY_DIFFER_DOWNSTREAM",
        "later_edge_relation": "MAY_DIFFER_DOWNSTREAM",
        "aggregate_rule": (
            "AT_LEAST_ONE_EDGE_RELATION_DEPENDS_ON_THE_MATCHED_LEVEL_OF_THE_"
            "OTHER_FACTOR"
        ),
    },
}
_D2A_ONLY_FUNCTIONS = {"GHOST", "ADJUDICATOR", "ACTION_GATE"}
_D2A_CONTROL_NAMES = {"adjudication_policy"}
_EXPECTED_D2A_CHALLENGES = {
    "d2a.ghost_candidate_separation": {
        "function": "GHOST",
        "varied_input": "ghost_exploration_program",
        "clamped_fields": {
            "material_admission",
            "current_access_source_view",
            "subjective_encounter_form",
            "adjudication_policy",
        },
        "observed_field": "candidate_set",
    },
    "d2a.adjudicator_candidate_separation": {
        "function": "ADJUDICATOR",
        "varied_input": "scoped_adjudication_policy",
        "clamped_fields": {
            "material_admission",
            "current_access_source_view",
            "subjective_encounter_form",
            "candidate_set",
            "candidate_source_usage",
        },
        "observed_field": "adjudication",
    },
    "d2a.action_gate_occurrence_separation": {
        "function": "ACTION_GATE",
        "varied_input": "motor_feasibility_or_action_opportunity",
        "clamped_fields": {
            "subjective_encounter_form",
            "candidate_set",
            "adjudication",
            "action_affordance",
        },
        "observed_field": "action_occurrence",
    },
}
_GUARD_COORDINATES = {
    ("O0_INPUT_ACCEPTED_PRE_ACCESS", "base_public_record"),
    ("O0_INPUT_ACCEPTED_PRE_ACCESS", "declared_level_public_record"),
    ("O0_INPUT_ACCEPTED_PRE_ACCESS", "world_unknowns"),
    ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "external_target_evidence_link_set"),
    ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "evidence_assessment_by_claim_scope"),
    ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "external_identity_or_intention_certification"),
    ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "durable_targetform_write"),
    ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "narrative_write"),
}
_EXPECTED_FACTOR_GUARDS = {
    ("REL-BOUNDARY-001", "reported_current_mood"): "GUARD_FIRST_PERSON_CONDITION",
    ("REL-BOUNDARY-001", "target_history"): "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
    ("REL-BOUNDARY-001", "externally_cued_prior_material"): "GUARD_EXPERIMENTER_CUE",
    ("WORK-FEEDBACK-001", "reported_evaluation_threat"): "GUARD_FIRST_PERSON_CONDITION",
    ("WORK-FEEDBACK-001", "evaluator_criterion_history"):
        "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
    ("WORK-FEEDBACK-001", "public_feedback_addendum"): "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
    ("RISK-FOOTSTEPS-001", "reported_pre_event_arousal"): "GUARD_FIRST_PERSON_CONDITION",
    ("RISK-FOOTSTEPS-001", "recent_threat_history"): "GUARD_RISK_SEPARATE_HISTORY",
    ("RISK-FOOTSTEPS-001", "route_match_observation"): "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
}
_RISK_ROUTE_ADJACENT_EVIDENCE_RULE = (
    "THE_ROUTE_RECORD_MAY_CHANGE_A_SEPARATELY_FROZEN_EVIDENCE_ASSESSMENT_BUT_"
    "MUST_NOT_CERTIFY_SOURCE_IDENTITY_HOSTILE_INTENTION_OR_RESOLVED_ENTITY_STATUS"
)
_FUTURE_GUARD_RELATIONS = {
    ("O6_MATCHED_FUTURE_PROBE_ACCEPTED_PRE_ACCESS", "future_option_public_record"):
        "MUST_REMAIN_EQUAL",
    ("O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED", "external_target_evidence_link_set"):
        "MUST_REMAIN_EQUAL",
    (
        "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
        "evidence_assessment_by_claim_scope",
    ):
        "MUST_REMAIN_EQUAL",
    (
        "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
        "external_identity_or_intention_certification",
    ):
        "MUST_REMAIN_ABSENT",
    ("O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED", "durable_targetform_write"):
        "MUST_REMAIN_ABSENT",
    ("O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED", "narrative_write"):
        "MUST_REMAIN_ABSENT",
}
_EXPECTED_FUTURE_PROJECTIONS = {
    "REL-BOUNDARY-001": (
        ("O7_LATER_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O8_LATER_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        (
            "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
            "reorganization_projection",
        ),
    ),
    "WORK-FEEDBACK-001": (
        ("O7_LATER_ACCESS_WINDOW_CLOSED", "current_access_source_view"),
        ("O8_LATER_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        (
            "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
            "action_affordance",
        ),
    ),
    "RISK-FOOTSTEPS-001": (
        ("O8_LATER_ENCOUNTER_WINDOW_CLOSED", "subjective_encounter_form"),
        (
            "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
            "provisional_target_representation",
        ),
        (
            "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED",
            "action_affordance",
        ),
    ),
}
_EXPECTED_FUTURE_ORACLE_IDS = {
    "REL-BOUNDARY-001": "future.rel.same_projection",
    "WORK-FEEDBACK-001": "future.work.same_projection",
    "RISK-FOOTSTEPS-001": "future.risk.same_projection",
}
_REQUIRED_PROHIBITIONS = {
    "NO_HUMAN_LLM_OR_D2A_TRACE_RESULT_IS_RECORDED",
    "NO_CORRECT_OUTPUT_OR_PLACEMENT_WINNER_IS_RECORDED",
    "NO_001A_CANDIDATE_ANCHOR_COUNTS_AS_AN_OBSERVED_IMMEDIATE_SURFACE",
    "NO_NATURAL_CONTRAST_FIRST_DIFFERENCE_CERTIFIES_A_DIRECT_CAUSAL_EDGE",
    "ANY_DIRECT_EDGE_CLAIM_REQUIRES_AN_UNEXECUTED_D2A_NODE_CLAMP_CHALLENGE_REFERENCE",
    "NO_PRESENTED_CUE_IS_CAST_AS_ACCESS_USE_INTEGRATION_EPISODE_OR_NARRATIVE",
    "NO_PROVISIONAL_TARGET_REPRESENTATION_IS_CAST_AS_A_RESOLVED_ENTITY_IDENTITY_OR_INTENTION",
    "NO_DURABLE_TARGETFORM_EPISODE_OR_NARRATIVE_WRITER_IS_CREATED",
    "NO_DIFFERENT_FUTURE_OPTIONS_ARE_USED_TO_CLAIM_PRIOR_PATH_DISCRIMINATION",
    "NO_OBSERVED_EQUALITY_ALONE_CREATES_AN_OPERATIONAL_ALIAS",
    "NO_OUT_OF_MODEL_EFFECT_IS_SILENTLY_FORCED_INTO_A_REGISTERED_DOMAIN",
}


class TraceOracleContractError(ValueError):
    """Raised when the unexecuted INTERP-DIALOGUE-001B contract is malformed."""


def _fail(message: str) -> None:
    raise TraceOracleContractError(message)


def load_oracle(path: str | Path = _DEFAULT_ORACLE_PATH) -> dict[str, Any]:
    try:
        return loads_exact(Path(path).read_bytes())
    except ScenarioContractError as error:
        raise TraceOracleContractError(str(error)) from error


def _unique_index(
    records: Iterable[dict[str, Any]], key: str, label: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record[key]
        if identity in result:
            _fail(f"duplicate {label}: {identity}")
        result[identity] = record
    return result


def _validate_schema(
    oracle: dict[str, Any], schema_path: str | Path | None
) -> None:
    schema = load_family(schema_path or _DEFAULT_SCHEMA_PATH)
    try:
        validate_json_schema(oracle, schema)
    except ValueError as error:
        raise TraceOracleContractError(
            f"trace-oracle schema validation failed: {error}"
        ) from error


def _validate_vocabularies(oracle: dict[str, Any]) -> set[str]:
    relations = _unique_index(
        oracle["relation_vocabulary"], "relation", "relation vocabulary item"
    )
    observations = _unique_index(
        oracle["observation_vocabulary"],
        "observation",
        "observation vocabulary item",
    )
    adjudications = set(oracle["adjudication_vocabulary"])
    if set(relations) != _REQUIRED_RELATIONS:
        _fail("relation vocabulary changed or mixed with observation outcomes")
    if {key: item["meaning"] for key, item in relations.items()} \
            != _EXPECTED_RELATION_MEANINGS:
        _fail("relation meanings must remain exact non-empirical definitions")
    if set(observations) != _REQUIRED_OBSERVATIONS:
        _fail("observation vocabulary changed or mixed with hypothesis relations")
    if {key: item["meaning"] for key, item in observations.items()} \
            != _EXPECTED_OBSERVATION_MEANINGS:
        _fail("observation meanings must remain exact measurement definitions")
    if adjudications != _REQUIRED_ADJUDICATIONS:
        _fail("adjudication vocabulary must remain the exact frozen eight terms")
    vocabularies = (set(relations), set(observations), adjudications)
    if any(left & right for left, right in combinations(vocabularies, 2)):
        _fail("relation, observation, and adjudication vocabularies must be disjoint")
    return set(relations)


def _load_bound_families(
    oracle: dict[str, Any], oracle_path: str | Path
) -> dict[str, dict[str, Any]]:
    bindings = _unique_index(
        oracle["bound_family_files"], "family_id", "family binding"
    )
    if set(bindings) != set(_EXPECTED_FAMILY_PATHS):
        _fail("bound family set must be exactly REL, WORK, and RISK")
    oracle_root = Path(oracle_path).resolve().parent
    result: dict[str, dict[str, Any]] = {}
    for family_id, expected_relative_path in _EXPECTED_FAMILY_PATHS.items():
        binding = bindings[family_id]
        if binding["path"] != expected_relative_path:
            _fail(f"{family_id} path changed")
        path = (oracle_root / binding["path"]).resolve()
        expected_path = (_ORACLE_ROOT / expected_relative_path).resolve()
        if path != expected_path:
            _fail(f"{family_id} path leaves the frozen scenario root")
        if file_sha256(path) != binding["content_sha256"]:
            _fail(f"{family_id} content SHA-256 mismatch")
        try:
            family = load_and_validate_family(path)
        except ScenarioContractError as error:
            raise TraceOracleContractError(
                f"bound 001A family is invalid: {family_id}: {error}"
            ) from error
        if family["family_id"] != family_id:
            _fail(f"{family_id} binding points to another family")
        result[family_id] = family
    return result


def _validate_projection_catalogs(
    oracle: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    horizons = _unique_index(oracle["horizons"], "horizon_id", "horizon")
    if {
        key: value["ordinal_relation"] for key, value in horizons.items()
    } != _EXPECTED_HORIZON_RELATIONS:
        _fail("horizons must freeze exactly prefix, k, and k+1 ordinal scopes")
    if horizons != _EXPECTED_HORIZON_METADATA:
        _fail("horizon boundaries and execution metadata must remain exactly frozen")
    points = _unique_index(
        oracle["observation_points"], "observation_point_id", "observation point"
    )
    point_metadata = {
        point_id: (
            point["horizon_id"], point["ordinal"], point["stage"],
            point["authority"],
        )
        for point_id, point in points.items()
    }
    if point_metadata != _EXPECTED_OBSERVATION_POINT_METADATA:
        _fail("observation point horizon, ordinal, stage, or authority changed")
    fields = _unique_index(oracle["trace_fields"], "trace_field_id", "trace field")
    if set(fields) != _EXPECTED_TRACE_FIELDS:
        _fail("trace field catalog must remain the exact frozen 23-field set")
    metadata = {
        field_id: (field["field_role"], field["authority"])
        for field_id, field in fields.items()
    }
    if metadata != _EXPECTED_TRACE_FIELD_METADATA:
        _fail("trace field roles and authorities must remain exactly frozen")
    if {point["ordinal"] for point in points.values()} != set(range(11)):
        _fail("observation points must cover each frozen ordinal 0 through 10 once")
    for point in points.values():
        if point["horizon_id"] not in horizons:
            _fail(f"unknown horizon in observation point: {point['observation_point_id']}")
    for horizon in horizons.values():
        start = horizon["start_observation_point_id"]
        end = horizon["end_observation_point_id"]
        if start not in points or end not in points:
            _fail("horizon boundary references an unknown observation point")
        if points[start]["ordinal"] > points[end]["ordinal"]:
            _fail("horizon starts after its end")
    immediate = fields.get("immediate_surface")
    if immediate is None or immediate["authority"] \
            != "OBSERVABLE_ONLY_IF_ELICITED_NOT_DESIGN_ANCHOR":
        _fail("immediate surface must exclude the 001A design anchor")
    if fields.get("world_unknowns", {}).get("authority") \
            != "BOUND_001A_BASE_STIMULUS_WORLD_UNKNOWNS_ONLY_EXCLUDES_LEVEL_SPECIFIC_FACTS":
        _fail("world unknowns must exclude every level-specific factor fact")
    for point_id in (
        "O5_IMMEDIATE_SURFACE_RECORDED", "O10_LATER_SURFACE_RECORDED"
    ):
        if points[point_id]["authority"] != "OBSERVATION_SLOT_NOT_DESIGN_ANCHOR":
            _fail("surface slots must remain observations, never design anchors")
    return horizons, points, fields


def _validate_relation(
    relation: dict[str, Any],
    *,
    points: dict[str, dict[str, Any]],
    fields: dict[str, dict[str, Any]],
    vocabulary: set[str],
) -> tuple[str, str]:
    point_id = relation["observation_point_id"]
    field_id = relation["trace_field_id"]
    if point_id not in points:
        _fail(f"unknown observation point in projection: {point_id}")
    if field_id not in fields:
        _fail(f"unknown trace field in projection: {field_id}")
    if "relation" in relation and relation["relation"] not in vocabulary:
        _fail(f"undeclared hypothesis relation: {relation['relation']}")
    return point_id, field_id


def _validate_placement_catalog(
    oracle: dict[str, Any],
    horizons: dict[str, dict[str, Any]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    set[frozenset[str]],
]:
    placement_families = _unique_index(
        oracle["placement_catalog"], "placement_family_id", "placement family"
    )
    if set(placement_families) != set(_EXPECTED_PLACEMENT_CATALOG):
        _fail("placement families must remain the exact frozen six-family catalog")
    placements: dict[str, dict[str, Any]] = {}
    horizon_limited_pairs: set[frozenset[str]] = set()
    for family in placement_families.values():
        local = _unique_index(family["placements"], "placement_id", "placement")
        family_id = family["placement_family_id"]
        if set(local) != _EXPECTED_PLACEMENT_CATALOG[family_id]:
            _fail(f"placement IDs changed for catalog: {family_id}")
        for placement_id, placement in local.items():
            if (placement["label"], placement["authority"]) \
                    != _EXPECTED_PLACEMENT_METADATA[placement_id]:
                _fail(f"placement label or authority changed: {placement_id}")
            expected_keys = {"placement_id", "label", "authority"}
            if placement_id in {
                "TS_TARGET_SCOPED_READOUT", "TC_SLOW_CACHE_READOUT"
            }:
                expected_keys |= {"candidate_kind", "identifiability_status"}
            if set(placement) != expected_keys:
                _fail(f"placement metadata shape changed: {placement_id}")
        overlap = set(local) & set(placements)
        if overlap:
            _fail(f"placement IDs collide across catalogs: {sorted(overlap)}")
        placements.update(local)
        if "horizon_limitation" not in family:
            continue
        limitation = family["horizon_limitation"]
        pair = frozenset(limitation["placement_ids"])
        if pair != frozenset(
            {"TS_TARGET_SCOPED_READOUT", "TC_SLOW_CACHE_READOUT"}
        ):
            _fail("only durable TargetForm versus slow cache is horizon-limited")
        if not pair <= set(local):
            _fail("horizon limitation references another placement family")
        if limitation["horizon_id"] \
                != "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1":
            _fail("durable/cache limitation must stay scoped to the one-future horizon")
        if limitation["horizon_id"] not in horizons:
            _fail("horizon limitation references an unknown horizon")
        if limitation.get("precedence") \
                != "HORIZON_LIMITATION_OVERRIDES_GENERAL_ALIAS_RULE":
            _fail("durable/cache horizon limitation must override alias adjudication")
        if set(limitation["forbidden_conclusions"]) != {
            "OPERATIONALLY_ALIASED", "PLACEMENT_WINNER",
            "DURABLE_STATE_CLAIM", "GLOBAL_ALIAS_CLAIM"
        }:
            _fail("durable/cache limitation must forbid scoped alias and winner casts")
        for placement_id in pair:
            if local[placement_id].get("identifiability_status") \
                    != "NOT_IDENTIFIABLE_UNDER_CURRENT_HORIZON":
                _fail("durable/cache placements must remain horizon-insufficient")
        durable = local["TS_TARGET_SCOPED_READOUT"]
        cache = local["TC_SLOW_CACHE_READOUT"]
        if durable.get("candidate_kind") \
                != "DURABLE_TARGET_SCOPED_STATE_CANDIDATE" \
                or durable.get("authority") \
                != "HYPOTHESIS_CANDIDATE_NO_WRITER_RETENTION_OR_EXISTENCE_CLAIM":
            _fail("durable TargetForm must remain a non-assertive candidate only")
        if cache.get("candidate_kind") != "SLOW_CACHE_READOUT_CANDIDATE":
            _fail("slow cache candidate marker changed")
        horizon_limited_pairs.add(pair)
    if len(horizon_limited_pairs) != 1:
        _fail("durable/cache horizon limitation is missing")
    return placement_families, placements, horizon_limited_pairs


def _factor_contracts(family: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        contract["factor_id"]: contract
        for contract in family["factor_contrast_contracts"]
    }


def _validate_guard_policies(
    oracle: dict[str, Any],
    points: dict[str, dict[str, Any]],
    fields: dict[str, dict[str, Any]],
    vocabulary: set[str],
) -> dict[str, dict[str, Any]]:
    policies = _unique_index(
        oracle["guard_policy_catalog"], "guard_policy_id", "guard policy"
    )
    expected_ids = {
        "GUARD_FIRST_PERSON_CONDITION",
        "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
        "GUARD_EXPERIMENTER_CUE",
        "GUARD_RISK_SEPARATE_HISTORY",
    }
    if set(policies) != expected_ids:
        _fail("guard catalog must freeze all four source-sensitive policies")

    common = {
        ("O0_INPUT_ACCEPTED_PRE_ACCESS", "base_public_record"):
            "MUST_REMAIN_EQUAL",
        ("O0_INPUT_ACCEPTED_PRE_ACCESS", "declared_level_public_record"):
            "MUST_DIFFER_BY_DESIGN",
        ("O0_INPUT_ACCEPTED_PRE_ACCESS", "world_unknowns"):
            "MUST_REMAIN_EQUAL",
        ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "external_identity_or_intention_certification"):
            "MUST_REMAIN_ABSENT",
        ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "durable_targetform_write"):
            "MUST_REMAIN_ABSENT",
        ("O4_INITIAL_ADJUDICATION_WINDOW_CLOSED", "narrative_write"):
            "MUST_REMAIN_ABSENT",
    }
    evidence_coordinates = {
        "links": (
            "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED",
            "external_target_evidence_link_set",
        ),
        "assessment": (
            "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED",
            "evidence_assessment_by_claim_scope",
        ),
    }
    expected_evidence = {
        "GUARD_FIRST_PERSON_CONDITION": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
        "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS": (
            "MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT",
            "MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT",
        ),
        "GUARD_EXPERIMENTER_CUE": (
            "MUST_REMAIN_EQUAL",
            "NOT_EVALUABLE_WITHOUT_FROZEN_REASSESSMENT_POLICY",
        ),
        "GUARD_RISK_SEPARATE_HISTORY": (
            "MUST_REMAIN_EQUAL", "MUST_REMAIN_EQUAL"
        ),
    }
    expected_source_lanes = {
        "GUARD_FIRST_PERSON_CONDITION": "FIRST_PERSON_CONDITION_REPORT",
        "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS":
            "VIGNETTE_HISTORY_RECORD_OR_PUBLIC_STIMULUS_VARIANT",
        "GUARD_EXPERIMENTER_CUE": "EXPERIMENTER_CUE",
        "GUARD_RISK_SEPARATE_HISTORY":
            "VIGNETTE_HISTORY_RECORD_CURRENT_SOURCE_SEPARATE",
    }
    common_keys = {
        "guard_policy_id", "source_lane", "guard_projection_set",
        "unconditional_guard_relations",
    }
    expected_keys = {
        "GUARD_FIRST_PERSON_CONDITION": common_keys | {
            "evidence_assessment_scope"
        },
        "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS": common_keys,
        "GUARD_EXPERIMENTER_CUE": common_keys | {
            "link_equality_authority", "source_material_prerequisite"
        },
        "GUARD_RISK_SEPARATE_HISTORY": common_keys | {
            "evidence_assessment_scope"
        },
    }

    for policy_id, policy in policies.items():
        if set(policy) != expected_keys[policy_id]:
            _fail(f"guard policy metadata changed: {policy_id}")
        if policy["source_lane"] != expected_source_lanes[policy_id]:
            _fail(f"guard source lane changed: {policy_id}")
        projections: set[tuple[str, str]] = set()
        for projection in policy["guard_projection_set"]:
            coordinate = _validate_relation(
                projection, points=points, fields=fields, vocabulary=vocabulary
            )
            if coordinate in projections:
                _fail("guard projection set assigns one coordinate twice")
            projections.add(coordinate)
        if projections != _GUARD_COORDINATES:
            _fail("every guard policy must close the exact eight-coordinate vector")

        relations: dict[tuple[str, str], str] = {}
        for relation in policy["unconditional_guard_relations"]:
            coordinate = _validate_relation(
                relation, points=points, fields=fields, vocabulary=vocabulary
            )
            if coordinate in relations:
                _fail("guard relation assigns one coordinate twice")
            relations[coordinate] = relation["relation"]
        expected = dict(common)
        links, assessment = expected_evidence[policy_id]
        expected[evidence_coordinates["links"]] = links
        expected[evidence_coordinates["assessment"]] = assessment
        if relations != expected:
            _fail(f"source-sensitive evidence guard changed: {policy_id}")

    cue = policies["GUARD_EXPERIMENTER_CUE"]
    if cue.get("link_equality_authority") \
            != "EQUALITY_DOES_NOT_ASSERT_MEMBERSHIP" \
            or cue.get("source_material_prerequisite") \
            != (
                "BOTH_PRIOR_SOURCE_MATERIALS_EXIST_BY_BOUND_001A_MINIMAL_PAIR_"
                "CONTRACT_WITHOUT_ASSERTING_EVIDENCE_LINK_MEMBERSHIP"
            ):
        _fail("cue link equality must not assert EvidenceLink membership")
    first_person = policies["GUARD_FIRST_PERSON_CONDITION"]
    if first_person.get("evidence_assessment_scope") \
            != (
                "EXTERNAL_TARGET_OR_CURRENT_SOURCE_CLAIMS_ONLY_EXCLUDES_FIRST_"
                "PERSON_CONDITION_ATTESTATION"
            ):
        _fail("first-person condition attestation is outside external Evidence guards")
    risk = policies["GUARD_RISK_SEPARATE_HISTORY"]
    if risk.get("evidence_assessment_scope") \
            != (
                "CURRENT_UNRESOLVED_FOOTSTEP_SOURCE_CLAIM_ONLY_SEPARATE_PRIOR_"
                "INCIDENT_CLAIM_IS_OUTSIDE_THIS_EQUALITY_GUARD"
            ):
        _fail("risk history guard must remain scoped to the current unresolved source")
    return policies


def _validate_prefix_extension_guard(oracle: dict[str, Any]) -> None:
    guard = oracle["prefix_extension_guard"]
    expected = {
        "status": "UNEXECUTED",
        "comparison_unit":
            "SAME_ARM_SAME_O0_PREFIX_ARTIFACT_ACROSS_BASE_AND_FUTURE_EXTENSION_RUNS",
        "base_observation_point_id": "O0_INPUT_ACCEPTED_PRE_ACCESS",
        "trace_field_id": "prior_occurrence_prefix",
        "relation": "MUST_REMAIN_EQUAL",
        "cross_factor_arm_equality_required": False,
        "protected_initial_trace_observation_point_ids": [
            "O0_INPUT_ACCEPTED_PRE_ACCESS",
            "O1_INITIAL_ACCESS_WINDOW_CLOSED",
            "O2_INITIAL_ENCOUNTER_WINDOW_CLOSED",
            "O3_INITIAL_CANDIDATE_WINDOW_CLOSED",
            "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED",
            "O5_IMMEDIATE_SURFACE_RECORDED",
        ],
        "initial_trace_comparison_unit":
            "SAME_ARM_SAME_EMITTED_O0_TO_O5_TRACE_PREFIX_ACROSS_BASE_AND_FUTURE_EXTENSION_RUNS",
        "initial_trace_relation": "MUST_REMAIN_EQUAL",
        "initial_trace_digest_status_policy":
            "MISSING_OR_NOT_OBSERVED_STATUS_IS_PART_OF_FROZEN_DIGEST",
        "future_extension_append_rule":
            "FUTURE_EXTENSION_ONLY_APPENDS_AFTER_O5_WITHOUT_REWRITING_EMITTED_INITIAL_TRACE",
        "execution_source_scope":
            "D2A_OR_RUNTIME_REPLAY_ONLY_NOT_HUMAN_REEXPERIENCE",
        "future_extension_rule":
            "FUTURE_EXTENSION_RUN_MUST_PRESERVE_THE_SAME_EMITTED_O0_PREFIX_"
            "ARTIFACT_FROM_ITS_TRUNCATED_BASE_RUN",
        "forbidden_comparison":
            "O0_PREFIX_IS_NOT_COMPARED_FOR_EQUALITY_WITH_O6_PRE_FUTURE_PREFIX",
    }
    if guard != expected:
        _fail("prefix non-retroactivity must compare one arm across run extensions")


def _validate_factor_oracles(
    oracle: dict[str, Any],
    families: dict[str, dict[str, Any]],
    placement_families: dict[str, dict[str, Any]],
    placements: dict[str, dict[str, Any]],
    horizon_limited_pairs: set[frozenset[str]],
    points: dict[str, dict[str, Any]],
    fields: dict[str, dict[str, Any]],
    vocabulary: set[str],
    guard_policies: dict[str, dict[str, Any]],
) -> None:
    factor_oracles = _unique_index(
        oracle["factor_oracles"], "oracle_id", "factor oracle"
    )
    observed_keys: set[tuple[str, str]] = set()
    global_hypothesis_ids: set[str] = set()
    for item in factor_oracles.values():
        family_id = item["family_id"]
        if family_id not in families:
            _fail(f"factor oracle references unknown family: {family_id}")
        key = (family_id, item["factor_id"])
        if key in observed_keys:
            _fail(f"duplicate factor binding: {key}")
        observed_keys.add(key)
        source_contracts = _factor_contracts(families[family_id])
        if item["factor_id"] not in source_contracts:
            _fail(f"factor oracle references unknown 001A factor: {key}")
        if item["oracle_id"] != _EXPECTED_FACTOR_ORACLE_IDS[key]:
            _fail(f"factor oracle identity changed: {key}")
        if item["guard_policy_id"] not in guard_policies:
            _fail("factor oracle references an unknown guard policy")
        if item["guard_policy_id"] != _EXPECTED_FACTOR_GUARDS[key]:
            _fail(f"factor oracle uses the wrong source-sensitive guard: {key}")
        evidence_rule = item.get("adjacent_evidence_lane_rule")
        if key == ("RISK-FOOTSTEPS-001", "route_match_observation"):
            if evidence_rule != _RISK_ROUTE_ADJACENT_EVIDENCE_RULE:
                _fail("risk route adjacent Evidence rule changed")
        elif "adjacent_evidence_lane_rule" in item:
            _fail("adjacent Evidence rule is permitted only for risk route")
        expected_snapshot = {
            key: value
            for key, value in source_contracts[item["factor_id"]].items()
            if key != "factor_id"
        }
        if canonical_bytes(item["source_contract_snapshot"]) != canonical_bytes(
            expected_snapshot
        ):
            _fail(f"factor oracle does not exactly snapshot its 001A contract: {key}")

        placement_family_id = item["placement_family_id"]
        if placement_family_id not in placement_families:
            _fail("factor oracle references an unknown placement family")
        if placement_family_id != _EXPECTED_FACTOR_PLACEMENT_FAMILY[key]:
            _fail(f"factor oracle placement family changed: {key}")
        allowed_placements = {
            placement["placement_id"]
            for placement in placement_families[placement_family_id]["placements"]
        }

        projection_set: set[tuple[str, str]] = set()
        projection_sequence: list[tuple[str, str]] = []
        for projection in item["projection_set"]:
            coordinate = _validate_relation(
                projection,
                points=points,
                fields=fields,
                vocabulary=vocabulary,
            )
            if coordinate in projection_set:
                _fail("factor oracle projection set contains a duplicate coordinate")
            projection_set.add(coordinate)
            projection_sequence.append(coordinate)
        expected_projection_sequence = _EXPECTED_FACTOR_PROJECTIONS[key]
        if tuple(projection_sequence) != expected_projection_sequence:
            _fail(f"factor projection coordinates or order changed: {key}")
        if projection_set & _GUARD_COORDINATES:
            _fail("factor projections must remain disjoint from authority guards")
        if any(fields[field_id]["field_role"] != "FUNCTIONAL_TRACE"
               for _, field_id in projection_set):
            _fail("factor hypotheses can project only registered functional traces")

        hypothesis_ids: set[str] = set()
        hypothesis_placements: set[str] = set()
        vectors: dict[bytes, str] = {}
        vector_by_placement: dict[str, bytes] = {}
        for hypothesis in item["hypotheses"]:
            if hypothesis["hypothesis_id"] in hypothesis_ids:
                _fail(f"duplicate hypothesis ID in {item['oracle_id']}")
            hypothesis_ids.add(hypothesis["hypothesis_id"])
            if hypothesis["hypothesis_id"] in global_hypothesis_ids:
                _fail("hypothesis IDs must be globally unique")
            global_hypothesis_ids.add(hypothesis["hypothesis_id"])
            placement_id = hypothesis["placement_id"]
            if placement_id not in placements:
                _fail("hypothesis references an unknown placement")
            if placement_id not in allowed_placements:
                _fail("hypothesis placement is outside its declared placement family")
            if placement_id in hypothesis_placements:
                _fail("factor oracle assigns one placement more than once")
            hypothesis_placements.add(placement_id)
            expected_hypothesis_id = (
                f"{_EXPECTED_HYPOTHESIS_PREFIXES[key]}."
                f"{_EXPECTED_HYPOTHESIS_SUFFIXES[placement_id]}"
            )
            if hypothesis["hypothesis_id"] != expected_hypothesis_id:
                _fail(f"hypothesis identity changed: {key}, {placement_id}")
            coordinates: set[tuple[str, str]] = set()
            relation_by_coordinate: dict[tuple[str, str], str] = {}
            for relation in hypothesis["relations"]:
                coordinate = _validate_relation(
                    relation,
                    points=points,
                    fields=fields,
                    vocabulary=vocabulary,
                )
                if coordinate in coordinates:
                    _fail("hypothesis assigns one projection twice")
                coordinates.add(coordinate)
                relation_by_coordinate[coordinate] = relation["relation"]
            if coordinates != projection_set:
                _fail("every hypothesis must provide a total closed projection vector")
            expected_relations = dict(zip(
                expected_projection_sequence,
                _EXPECTED_PLACEMENT_RELATION_PATTERNS[placement_family_id][
                    placement_id
                ],
            ))
            if relation_by_coordinate != expected_relations:
                _fail(f"placement relation signature changed: {placement_id}")
            vector = canonical_bytes(
                sorted(
                    (
                        relation["observation_point_id"],
                        relation["trace_field_id"],
                        relation["relation"],
                    )
                    for relation in hypothesis["relations"]
                )
            )
            if vector in vectors and frozenset({vectors[vector], placement_id}) \
                    not in horizon_limited_pairs:
                _fail("two distinguishable placements have the same total vector")
            vectors[vector] = placement_id
            vector_by_placement[placement_id] = vector

            refs = set(hypothesis["d2a_challenge_refs"])
            if hypothesis["direct_edge_claim"] != "NONE" or refs:
                _fail("natural factor hypotheses cannot claim D2a direct residence")

        if hypothesis_placements != allowed_placements:
            _fail("factor hypotheses must cover every allowed placement exactly once")

        durable_pair = {
            "TS_TARGET_SCOPED_READOUT", "TC_SLOW_CACHE_READOUT"
        }
        if durable_pair <= set(vector_by_placement) \
                and vector_by_placement["TS_TARGET_SCOPED_READOUT"] \
                != vector_by_placement["TC_SLOW_CACHE_READOUT"]:
            _fail("one-future horizon cannot manufacture durable/cache separation")

    expected_keys = {
        (family_id, factor["factor_id"])
        for family_id, family in families.items()
        for factor in family["factors"]
    }
    if observed_keys != expected_keys:
        _fail("factor oracles must cover all nine 001A factors exactly once")


def _validate_d2a_challenges(
    oracle: dict[str, Any], fields: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    challenges = _unique_index(
        oracle["d2a_only_challenges"], "challenge_id", "D2a challenge"
    )
    if set(challenges) != set(_EXPECTED_D2A_CHALLENGES):
        _fail("D2a challenge set must remain exactly Ghost, adjudicator, and gate")
    if {item["function"] for item in challenges.values()} != _D2A_ONLY_FUNCTIONS:
        _fail("Ghost, adjudicator, and action gate must remain D2a-only")
    valid_clamps = set(fields) | _D2A_CONTROL_NAMES
    for challenge_id, item in challenges.items():
        clamped = set(item["clamped_fields"])
        if not clamped or not clamped <= valid_clamps:
            _fail("D2a challenge has an empty or unknown clamp")
        observed = item["observed_field"]
        if observed not in fields:
            _fail("D2a challenge observes an unknown trace field")
        if observed in clamped:
            _fail("D2a challenge cannot clamp its observed target node")
        expected = _EXPECTED_D2A_CHALLENGES[challenge_id]
        if item["function"] != expected["function"] \
                or item["varied_input"] != expected["varied_input"] \
                or clamped != expected["clamped_fields"] \
                or observed != expected["observed_field"] \
                or item["conditional_relation"] != "MUST_DIFFER_IF_PLACEMENT" \
                or item["status"] != "NO_001A_NATURAL_INTERVENTION":
            _fail(f"D2a node-clamp matrix changed: {challenge_id}")
    return challenges


def _future_probe_snapshot(claim: dict[str, Any]) -> dict[str, Any]:
    return claim["future_probe"]


def _validate_future_oracles(
    oracle: dict[str, Any],
    families: dict[str, dict[str, Any]],
    points: dict[str, dict[str, Any]],
    fields: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    items = _unique_index(
        oracle["matched_future_oracles"], "oracle_id", "future oracle"
    )
    by_family = _unique_index(items.values(), "family_id", "future-oracle family")
    if set(by_family) != set(families):
        _fail("future oracles must cover all three families exactly once")
    future_horizon = "H_REGISTERED_FUTURE_ACCESS_K_PLUS_1"
    for family_id, item in by_family.items():
        if item["oracle_id"] != _EXPECTED_FUTURE_ORACLE_IDS[family_id]:
            _fail(f"future oracle identity changed: {family_id}")
        claim = families[family_id]["same_immediate_projection_claim"]
        if item["source_probe_id"] != claim["future_probe"]["probe_id"]:
            _fail(f"future probe ID changed for {family_id}")
        if item["source_option_count"] != len(claim["future_probe"]["probe_options"]):
            _fail(f"future option count changed for {family_id}")
        if item["compared_prior_cell_ids"] != claim["compared_cell_ids"]:
            _fail(f"future compared paths changed for {family_id}")
        if item["changed_factor_id"] != claim["changed_factor_id"]:
            _fail(f"future changed factor changed for {family_id}")
        if canonical_bytes(item["source_probe_snapshot"]) != canonical_bytes(
            _future_probe_snapshot(claim)
        ):
            _fail(f"future oracle does not exactly snapshot 001A for {family_id}")
        eligibility = item["same_surface_eligibility"]
        if set(eligibility["allowed_bases"]) != {
            "ACTUAL_ELICITED_SURFACE_OBSERVED_EQUAL_UNDER_FROZEN_SOURCE_SPECIFIC_MAPPING",
            "PREREGISTERED_NO_FEEDBACK_SURFACE_CLAMP_EQUAL",
        } or set(eligibility.get("required_scope_keys", [])) != {
            "source_kind", "measurement_mapping_version",
            "elicitation_protocol_version",
        } or eligibility.get("clamp_authority") \
                != "D2A_ONLY_PREREGISTERED_NO_FEEDBACK_SURFACE_CLAMP" \
                or eligibility["forbidden_basis"] != "DESIGN_ANCHOR_ONLY" \
                or eligibility["failure_status"] != "NOT_EVALUABLE":
            _fail("same-surface path tests require observed equality or a frozen clamp")

        expected_prior = item["compared_prior_cell_ids"]
        arms = item["matched_option_arms"]
        if {arm["option_index"] for arm in arms} \
                != set(range(item["source_option_count"])):
            _fail("matched future arms must cover every registered option once")
        for arm in arms:
            option_index = arm["option_index"]
            if [arm["left_prior_cell_id"], arm["right_prior_cell_id"]] \
                    != expected_prior:
                _fail("matched future arm changed a preregistered prior path")
            if arm["left_option_index"] != option_index \
                    or arm["right_option_index"] != option_index:
                _fail("prior paths must receive the exact same future option")

        later_projection_sequence: list[tuple[str, str]] = []
        for ref in item["later_projection_refs"]:
            coordinate = _validate_relation(
                ref,
                points=points,
                fields=fields,
                vocabulary=_REQUIRED_RELATIONS,
            )
            if points[coordinate[0]]["horizon_id"] != future_horizon:
                _fail("future discriminability projection must be at k+1")
            later_projection_sequence.append(coordinate)
        if tuple(later_projection_sequence) \
                != _EXPECTED_FUTURE_PROJECTIONS[family_id]:
            _fail(f"future functional projections changed: {family_id}")
        if set(later_projection_sequence) & set(_FUTURE_GUARD_RELATIONS):
            _fail("future functional projections must be disjoint from guards")
        if any(fields[field_id]["field_role"] != "FUNCTIONAL_TRACE"
               for _, field_id in later_projection_sequence):
            _fail("future projections can contain only functional trace fields")
        guard_coordinates: set[tuple[str, str]] = set()
        for ref in item["future_guard_projection_set"]:
            coordinate = _validate_relation(
                ref,
                points=points,
                fields=fields,
                vocabulary=_REQUIRED_RELATIONS,
            )
            if coordinate in guard_coordinates:
                _fail("future guard projection contains a duplicate coordinate")
            guard_coordinates.add(coordinate)
        if guard_coordinates != set(_FUTURE_GUARD_RELATIONS):
            _fail("future oracle must close the matched-input and writer guards")
        guard_relations: dict[tuple[str, str], str] = {}
        for relation in item["future_guard_relations"]:
            coordinate = _validate_relation(
                relation,
                points=points,
                fields=fields,
                vocabulary=_REQUIRED_RELATIONS,
            )
            if coordinate in guard_relations:
                _fail("future guard relation assigns one coordinate twice")
            guard_relations[coordinate] = relation["relation"]
        if guard_relations != _FUTURE_GUARD_RELATIONS:
            _fail("future option equality and forbidden writers must remain closed")
    return by_family


def _validate_rel_factorial(
    oracle: dict[str, Any],
    rel_family: dict[str, Any],
    future_oracles: dict[str, dict[str, Any]],
) -> None:
    factorial = oracle["rel_delayed_reorganization_factorial"]
    if factorial["source_probe_id"] \
            != future_oracles["REL-BOUNDARY-001"]["source_probe_id"]:
        _fail("REL factorial is not bound to the same registered future probe")
    option_mapping = {
        item["later_option_id"]: item["source_option_index"]
        for item in factorial["later_option_mapping"]
    }
    if option_mapping != {
        "later_reported_ordinary_mood": 0,
        "later_reported_low_mood": 1,
    } or set(option_mapping.values()) != set(
        range(future_oracles["REL-BOUNDARY-001"]["source_option_count"])
    ):
        _fail("REL later mood tokens must remain bound to future option order")
    family_cells = {
        cell["cell_id"]: cell["factor_levels"] for cell in rel_family["cells"]
    }
    fixed = factorial["fixed_initial_factor_levels"]
    for factor_id, level_id in fixed.items():
        factor = next(
            item for item in rel_family["factors"] if item["factor_id"] == factor_id
        )
        if level_id not in {level["level_id"] for level in factor["levels"]}:
            _fail("REL factorial fixes an unknown initial factor level")
    mood_factor = next(
        item
        for item in rel_family["factors"]
        if item["factor_id"] == "reported_current_mood"
    )
    mood_levels = {level["level_id"] for level in mood_factor["levels"]}
    later_levels = {"later_reported_ordinary_mood", "later_reported_low_mood"}
    cells = _unique_index(
        factorial["cells"], "trajectory_cell_id", "REL factorial cell"
    )
    expected_initial_cell_ids = set(
        future_oracles["REL-BOUNDARY-001"]["compared_prior_cell_ids"]
    )
    initial_cell_counts = Counter(
        cell["initial_cell_id"] for cell in cells.values()
    )
    if set(initial_cell_counts) != expected_initial_cell_ids \
            or set(initial_cell_counts.values()) != {2}:
        _fail("REL factorial must use exactly both bound future prior paths")
    assignments: dict[str, tuple[str, str]] = {}
    for cell_id, cell in cells.items():
        initial_cell_id = cell["initial_cell_id"]
        if initial_cell_id not in family_cells:
            _fail("REL factorial references an unknown initial cell")
        source_assignment = family_cells[initial_cell_id]
        if cell["initial_reported_mood"] \
                != source_assignment["reported_current_mood"]:
            _fail("REL factorial initial mood does not match its source cell")
        if any(source_assignment[key] != value for key, value in fixed.items()):
            _fail("REL factorial source cell violates a fixed initial factor")
        assignment = (cell["initial_reported_mood"], cell["later_option_id"])
        if assignment in assignments.values():
            _fail("REL factorial contains a duplicate mood trajectory")
        assignments[cell_id] = assignment
    if set(assignments.values()) != set(product(mood_levels, later_levels)):
        _fail("REL delayed reorganization must be a complete initial-by-later 2x2")

    edge_classes = _unique_index(
        factorial["edge_classes"], "edge_class_id", "REL edge class"
    )
    expected_changed_index = {
        "INITIAL_MOOD_EDGE_AT_MATCHED_LATER_MOOD": 0,
        "LATER_MOOD_EDGE_AT_MATCHED_INITIAL_MOOD": 1,
    }
    if set(edge_classes) != set(expected_changed_index):
        _fail("REL factorial must contain both matched edge classes")
    for edge_id, changed_index in expected_changed_index.items():
        observed_pairs = {frozenset(pair) for pair in edge_classes[edge_id]["pairs"]}
        expected_pairs = {
            frozenset((left_id, right_id))
            for left_id, right_id in combinations(cells, 2)
            if assignments[left_id][changed_index]
            != assignments[right_id][changed_index]
            and assignments[left_id][1 - changed_index]
            == assignments[right_id][1 - changed_index]
        }
        if observed_pairs != expected_pairs:
            _fail(f"REL factorial {edge_id} pairs are incomplete or unmatched")
    patterns = _unique_index(
        factorial["candidate_patterns"], "pattern_id", "REL candidate pattern"
    )
    if patterns != _EXPECTED_REL_CANDIDATE_PATTERNS:
        _fail("REL candidate patterns must remain the exact frozen four patterns")
    for pattern in patterns.values():
        if pattern["initial_edge_relation"] not in _REQUIRED_RELATIONS \
                or pattern["later_edge_relation"] not in _REQUIRED_RELATIONS:
            _fail("REL candidate pattern uses an unknown relation")


def _validate_alias_out_of_model_and_prohibitions(oracle: dict[str, Any]) -> None:
    alias = oracle["operational_alias_rule"]
    if set(alias["required_scope_keys"]) != _REQUIRED_ALIAS_SCOPE:
        _fail("alias must be scoped by probe, projection, horizon, source, and mapping")
    if alias["definition"] != _EXPECTED_ALIAS_DEFINITION \
            or alias["observed_equality_status"] \
            != "EMPIRICALLY_UNRESOLVED_UNDER_SCOPE" \
            or alias["observed_equality_is_not_alias"] is not True:
        _fail("alias definition and observed-equality rule must remain exact")
    if not alias["observed_equality_is_not_alias"] or not alias["no_factor_retirement"]:
        _fail("observed equality cannot imply alias or factor retirement")
    if not all(
        token in alias["durable_cache_rule"]
        for token in (
            "TS_TARGET_SCOPED_READOUT",
            "TC_SLOW_CACHE_READOUT",
            "NOT_IDENTIFIABLE_UNDER_HORIZON",
            "OPERATIONALLY_ALIASED",
        )
    ):
        _fail("alias rule must retain durable/cache horizon insufficiency")
    if alias["durable_cache_rule"] != _EXPECTED_DURABLE_CACHE_RULE:
        _fail("durable/cache horizon precedence prose changed")

    policy = oracle["out_of_model_policy"]
    if set(policy["record_fields"]) != _REQUIRED_RAW_RECORD_FIELDS:
        _fail("out-of-model lane must preserve exact raw observation/provenance fields")
    if policy["forced_cast_to_registered_trace_field"] != "FORBIDDEN" \
            or policy["same_run_schema_expansion_and_rescoring"] != "FORBIDDEN":
        _fail("out-of-model observations cannot be coerced or rescored in-run")
    if policy["normative_invariant_violation_is_out_of_model"]:
        _fail("normative invariant violations cannot be relabeled out-of-model")
    if set(policy["scope_failure_requirements"]) \
            != _EXPECTED_SCOPE_FAILURE_REQUIREMENTS:
        _fail("out-of-model scope-failure requirements must remain exact")
    if set(oracle["prohibitions"]) != _REQUIRED_PROHIBITIONS:
        _fail("authority prohibitions must remain the exact frozen 11-item set")


def validate_trace_oracle(
    oracle: dict[str, Any],
    *,
    oracle_path: str | Path = _DEFAULT_ORACLE_PATH,
    schema_path: str | Path | None = None,
) -> None:
    """Validate the frozen declarations without executing or adjudicating them."""

    _validate_schema(oracle, schema_path)
    vocabulary = _validate_vocabularies(oracle)
    families = _load_bound_families(oracle, oracle_path)
    horizons, points, fields = _validate_projection_catalogs(oracle)
    placement_families, placements, horizon_limited_pairs = \
        _validate_placement_catalog(oracle, horizons)
    guard_policies = _validate_guard_policies(
        oracle, points, fields, vocabulary
    )
    _validate_prefix_extension_guard(oracle)
    challenges = _validate_d2a_challenges(oracle, fields)
    _validate_factor_oracles(
        oracle,
        families,
        placement_families,
        placements,
        horizon_limited_pairs,
        points,
        fields,
        vocabulary,
        guard_policies,
    )
    future_oracles = _validate_future_oracles(
        oracle, families, points, fields
    )
    _validate_rel_factorial(
        oracle, families["REL-BOUNDARY-001"], future_oracles
    )
    _validate_alias_out_of_model_and_prohibitions(oracle)


def load_and_validate_trace_oracle(
    path: str | Path = _DEFAULT_ORACLE_PATH,
    *,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    oracle = load_oracle(path)
    validate_trace_oracle(oracle, oracle_path=path, schema_path=schema_path)
    return oracle
