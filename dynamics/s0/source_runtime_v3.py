from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .source_common_v3 import (
    ACTORS,
    AUDIENCE_CONTEXTS,
    CONTEXT_KINDS,
    CONTINUATION_CONDITIONS,
    FAMILY_ID,
    FEEDBACK_CATEGORIES,
    HISTORY_CONDITIONS,
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    OBSERVABLE_PREFIX_SCHEMA_VERSION,
    OCCURRENCE_KINDS,
    PREDICTION_POINTS,
    PREDICTION_RECORD_SCHEMA_VERSION,
    PUBLIC_EVENT_SCHEMA_VERSION,
    RECEIPT_SCOPES,
    ROLE_CONTEXTS,
    RUNTIME_VERSION,
    SPLITS,
    SPLIT_TRAJECTORIES_PER_INSTANCE,
    TARGETS,
    TRAJECTORY_SCHEMA_VERSION,
    HashStream,
    SourceProcessError,
    canonical_bytes,
    derive_domain_seed,
    require_exact_keys,
    require_hex,
    sha256_hex,
)


def _validate_ordinal(ordinal: int) -> None:
    if ordinal < 1:
        raise SourceProcessError("public event ordinal must be >= 1")


@dataclass(frozen=True)
class OccurrenceEvent:
    ordinal: int
    occurrence_kind: str
    scope: str
    actor: str
    target: str
    schema_version: str = PUBLIC_EVENT_SCHEMA_VERSION
    event_type: str = "OCCURRENCE"

    def __post_init__(self) -> None:
        _validate_ordinal(self.ordinal)
        if self.occurrence_kind not in OCCURRENCE_KINDS:
            raise SourceProcessError("unknown occurrence kind")
        if self.scope not in RECEIPT_SCOPES:
            raise SourceProcessError("unknown occurrence scope")
        expected_actor, expected_target = _OCCURRENCE_COMPATIBILITY[self.occurrence_kind]
        if (self.actor, self.target) != (expected_actor, expected_target):
            raise SourceProcessError("occurrence actor/target incompatibility")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActionEvent:
    ordinal: int
    action_category: str
    actor: str = "focal"
    target: str = "interaction"
    schema_version: str = PUBLIC_EVENT_SCHEMA_VERSION
    event_type: str = "ACTION"

    def __post_init__(self) -> None:
        _validate_ordinal(self.ordinal)
        if self.action_category not in IMMEDIATE_ACTIONS:
            raise SourceProcessError("unknown action category")
        if self.actor != "focal" or self.target != "interaction":
            raise SourceProcessError("action events must be focal→interaction")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeedbackEvent:
    ordinal: int
    feedback_category: str
    actor: str = "counterpart"
    target: str = "focal"
    schema_version: str = PUBLIC_EVENT_SCHEMA_VERSION
    event_type: str = "FEEDBACK"

    def __post_init__(self) -> None:
        _validate_ordinal(self.ordinal)
        if self.feedback_category not in FEEDBACK_CATEGORIES:
            raise SourceProcessError("unknown feedback category")
        if self.actor != "counterpart" or self.target != "focal":
            raise SourceProcessError("feedback events must be counterpart→focal")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextEvent:
    ordinal: int
    context_kind: str
    actor: str = "environment"
    target: str = "interaction"
    schema_version: str = PUBLIC_EVENT_SCHEMA_VERSION
    event_type: str = "CONTEXT"

    def __post_init__(self) -> None:
        _validate_ordinal(self.ordinal)
        if self.context_kind not in CONTEXT_KINDS:
            raise SourceProcessError("unknown context kind")
        if self.actor != "environment" or self.target != "interaction":
            raise SourceProcessError("context events must be environment→interaction")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NoEvent:
    ordinal: int
    canonical_tick_count: int = 1
    schema_version: str = PUBLIC_EVENT_SCHEMA_VERSION
    event_type: str = "NO_EVENT"

    def __post_init__(self) -> None:
        _validate_ordinal(self.ordinal)
        if self.canonical_tick_count != 1:
            raise SourceProcessError("one NoEvent represents exactly one canonical process tick")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


PublicEventV3 = OccurrenceEvent | ActionEvent | FeedbackEvent | ContextEvent | NoEvent

_OCCURRENCE_COMPATIBILITY = {
    "CURRENT_COMMITMENT_MISSED": ("counterpart", "focal"),
    "COUNTERPART_ACKNOWLEDGES_IMPACT": ("counterpart", "focal"),
    "COUNTERPART_ACCEPTS_RESPONSIBILITY": ("counterpart", "focal"),
    "COUNTERPART_MINIMIZES_IMPACT": ("counterpart", "focal"),
    "COUNTERPART_SHIFTS_RESPONSIBILITY": ("counterpart", "focal"),
    "SIMILAR_VIOLATION_REPEATED": ("counterpart", "focal"),
}

_BRANCH_CUES: dict[str, tuple[PublicEventV3, PublicEventV3]] = {
    "F-REPAIR": (
        OccurrenceEvent(4, "COUNTERPART_ACKNOWLEDGES_IMPACT", "REGISTERED_REPORT", "counterpart", "focal"),
        OccurrenceEvent(7, "COUNTERPART_ACCEPTS_RESPONSIBILITY", "REGISTERED_REPORT", "counterpart", "focal"),
    ),
    "F-DEFLECT": (
        OccurrenceEvent(4, "COUNTERPART_MINIMIZES_IMPACT", "REGISTERED_REPORT", "counterpart", "focal"),
        OccurrenceEvent(7, "COUNTERPART_SHIFTS_RESPONSIBILITY", "REGISTERED_REPORT", "counterpart", "focal"),
    ),
    "F-REPEAT": (
        NoEvent(4),
        OccurrenceEvent(7, "SIMILAR_VIOLATION_REPEATED", "REGISTERED_REPORT", "counterpart", "focal"),
    ),
    "F-PUBLIC": (
        ContextEvent(4, "AUDIENCE_CONSTRAINT_PRESENT"),
        ContextEvent(7, "ROLE_CONSTRAINT_PRESENT"),
    ),
}


def public_event_from_dict(value: Mapping[str, Any]) -> PublicEventV3:
    event_type = str(value.get("event_type", ""))
    classes: dict[str, tuple[type[Any], tuple[str, ...]]] = {
        "OCCURRENCE": (
            OccurrenceEvent,
            ("ordinal", "occurrence_kind", "scope", "actor", "target", "schema_version", "event_type"),
        ),
        "ACTION": (
            ActionEvent,
            ("ordinal", "action_category", "actor", "target", "schema_version", "event_type"),
        ),
        "FEEDBACK": (
            FeedbackEvent,
            ("ordinal", "feedback_category", "actor", "target", "schema_version", "event_type"),
        ),
        "CONTEXT": (
            ContextEvent,
            ("ordinal", "context_kind", "actor", "target", "schema_version", "event_type"),
        ),
        "NO_EVENT": (
            NoEvent,
            ("ordinal", "canonical_tick_count", "schema_version", "event_type"),
        ),
    }
    if event_type not in classes:
        raise SourceProcessError("unknown public event discriminant")
    cls, keys = classes[event_type]
    require_exact_keys(value, keys, "public_event")
    if str(value["schema_version"]) != PUBLIC_EVENT_SCHEMA_VERSION:
        raise SourceProcessError("unsupported public event schema")
    payload = dict(value)
    payload.pop("schema_version")
    payload.pop("event_type")
    return cls(**payload)


@dataclass(frozen=True)
class ModelVisibleContextV3:
    history_condition: str
    role_context: str = "PRIVATE_RELATION"
    audience_context: str = "NO_AUDIENCE"

    def __post_init__(self) -> None:
        if self.history_condition not in HISTORY_CONDITIONS:
            raise SourceProcessError("unknown history condition")
        if self.role_context not in ROLE_CONTEXTS or self.audience_context not in AUDIENCE_CONTEXTS:
            raise SourceProcessError("unknown public role/audience context")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ObservablePrefixV3:
    context: ModelVisibleContextV3
    events: tuple[PublicEventV3, ...]
    schema_version: str = OBSERVABLE_PREFIX_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != OBSERVABLE_PREFIX_SCHEMA_VERSION:
            raise SourceProcessError("unsupported observable prefix schema")
        ordinals = [event.ordinal for event in self.events]
        if ordinals != list(range(1, len(ordinals) + 1)):
            raise SourceProcessError("public event ordinals must be exactly continuous 1..N")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "context": self.context.to_dict(),
            "events": [event.to_dict() for event in self.events],
        }

    def digest(self) -> str:
        return sha256_hex(self.to_dict())


@dataclass(frozen=True, order=True)
class PredictionKeyV3:
    source_instance_id: str
    trajectory_id: str
    step_ordinal: int
    prediction_point_id: str

    def __post_init__(self) -> None:
        if not self.source_instance_id or not self.trajectory_id:
            raise SourceProcessError("prediction key identifiers are required")
        if self.prediction_point_id not in PREDICTION_POINTS:
            raise SourceProcessError("unknown prediction point")
        if self.step_ordinal not in (1, 4, 7):
            raise SourceProcessError("prediction step must be one of 1,4,7")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PredictionRecordV3:
    key: PredictionKeyV3
    observable_prefix: ObservablePrefixV3
    immediate_target: str
    terminal_target: str
    schema_version: str = PREDICTION_RECORD_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != PREDICTION_RECORD_SCHEMA_VERSION:
            raise SourceProcessError("unsupported prediction record schema")
        if self.immediate_target not in IMMEDIATE_ACTIONS:
            raise SourceProcessError("unknown immediate target")
        if self.terminal_target not in LONG_HORIZON_REGIONS:
            raise SourceProcessError("unknown terminal target")
        if len(self.observable_prefix.events) != self.key.step_ordinal:
            raise SourceProcessError("prediction key step must match observable event count")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "key": self.key.to_dict(),
            "observable_prefix": self.observable_prefix.to_dict(),
            "observable_prefix_digest": self.observable_prefix.digest(),
            "targets": {
                "immediate_action": self.immediate_target,
                "terminal_long_horizon_region": self.terminal_target,
            },
        }


@dataclass(frozen=True)
class MaterializedTrajectoryV3:
    source_instance_id: str
    trajectory_id: str
    split: str
    history_condition: str
    evaluator_continuation_condition: str
    sample_index: int
    prediction_records: tuple[PredictionRecordV3, ...]
    schema_version: str = TRAJECTORY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != TRAJECTORY_SCHEMA_VERSION:
            raise SourceProcessError("unsupported trajectory schema")
        if self.split not in SPLITS:
            raise SourceProcessError("unknown split")
        if self.history_condition not in HISTORY_CONDITIONS:
            raise SourceProcessError("unknown history condition")
        if self.evaluator_continuation_condition not in CONTINUATION_CONDITIONS:
            raise SourceProcessError("unknown evaluator branch")
        if tuple(record.key.prediction_point_id for record in self.prediction_records) != PREDICTION_POINTS:
            raise SourceProcessError("trajectory must contain P1/P2/P3 in order")

    def to_dict(self, *, include_evaluator_metadata: bool = True) -> dict[str, Any]:
        value = {
            "schema_version": self.schema_version,
            "source_instance_id": self.source_instance_id,
            "trajectory_id": self.trajectory_id,
            "split": self.split,
            "history_condition": self.history_condition,
            "sample_index": self.sample_index,
            "prediction_records": [record.to_dict() for record in self.prediction_records],
        }
        if include_evaluator_metadata:
            value["evaluator_continuation_condition"] = self.evaluator_continuation_condition
        return value


def derive_split_seed(family_seed_hex: str, source_instance_id: str, split: str) -> str:
    require_hex(family_seed_hex, length=64, name="family_seed_hex")
    if split not in SPLITS:
        raise SourceProcessError("unknown split")
    return derive_domain_seed(family_seed_hex, RUNTIME_VERSION, source_instance_id, "split", split)


def derive_trajectory_seed(
    split_seed_hex: str,
    *,
    source_instance_id: str,
    split: str,
    history_condition: str,
    continuation_condition: str,
    sample_index: int,
) -> str:
    require_hex(split_seed_hex, length=64, name="split_seed_hex")
    if history_condition not in HISTORY_CONDITIONS or continuation_condition not in CONTINUATION_CONDITIONS:
        raise SourceProcessError("unknown trajectory condition")
    if sample_index < 0:
        raise SourceProcessError("sample_index must be non-negative")
    return derive_domain_seed(
        split_seed_hex,
        source_instance_id,
        split,
        history_condition,
        continuation_condition,
        sample_index,
    )


def derive_prebranch_seed(
    split_seed_hex: str,
    *,
    source_instance_id: str,
    split: str,
    history_condition: str,
    sample_index: int,
) -> str:
    require_hex(split_seed_hex, length=64, name="split_seed_hex")
    if history_condition not in HISTORY_CONDITIONS or split not in SPLITS:
        raise SourceProcessError("unknown matched prebranch condition")
    if sample_index < 0:
        raise SourceProcessError("sample_index must be non-negative")
    return derive_domain_seed(
        split_seed_hex,
        source_instance_id,
        split,
        history_condition,
        "MATCHED_PREBRANCH",
        sample_index,
    )


def trajectory_id_for(
    *,
    source_instance_id: str,
    split: str,
    history_condition: str,
    continuation_condition: str,
    sample_index: int,
) -> str:
    material = {
        "family_id": FAMILY_ID,
        "source_instance_id": source_instance_id,
        "split": split,
        "history_condition": history_condition,
        "continuation_condition": continuation_condition,
        "sample_index": sample_index,
    }
    return f"TRJ-{sha256_hex(material)[:24]}"


def _sample_index(seed_hex: str, domain: str, distribution: Sequence[int]) -> int:
    return HashStream(seed_hex, domain).choice_index(distribution)


def _context_after(context: ModelVisibleContextV3, event: PublicEventV3) -> ModelVisibleContextV3:
    if isinstance(event, ContextEvent):
        if event.context_kind == "AUDIENCE_CONSTRAINT_PRESENT":
            return ModelVisibleContextV3(
                history_condition=context.history_condition,
                role_context=context.role_context,
                audience_context="AUDIENCE_PRESENT",
            )
        if event.context_kind == "ROLE_CONSTRAINT_PRESENT":
            return ModelVisibleContextV3(
                history_condition=context.history_condition,
                role_context="PUBLIC_ROLE",
                audience_context=context.audience_context,
            )
    return context


def materialize_trajectory(
    instance: Mapping[str, Any],
    *,
    split_seed_hex: str,
    split: str,
    history_condition: str,
    continuation_condition: str,
    sample_index: int,
) -> MaterializedTrajectoryV3:
    if instance.get("family_id") != FAMILY_ID:
        raise SourceProcessError("source instance does not belong to Family 002")
    source_instance_id = str(instance["instance_id"])
    trajectory_seed = derive_trajectory_seed(
        split_seed_hex,
        source_instance_id=source_instance_id,
        split=split,
        history_condition=history_condition,
        continuation_condition=continuation_condition,
        sample_index=sample_index,
    )
    prebranch_seed = derive_prebranch_seed(
        split_seed_hex,
        source_instance_id=source_instance_id,
        split=split,
        history_condition=history_condition,
        sample_index=sample_index,
    )
    trajectory_id = trajectory_id_for(
        source_instance_id=source_instance_id,
        split=split,
        history_condition=history_condition,
        continuation_condition=continuation_condition,
        sample_index=sample_index,
    )
    immediate = instance["emission_parameters"]["immediate_action"]
    feedback = instance["emission_parameters"]["action_conditioned_feedback"]
    horizon = instance["emission_parameters"]["long_horizon_region"]
    transition = instance["conditioned_transition_matrices"][continuation_condition]

    z0 = _sample_index(
        prebranch_seed,
        "initial-latent",
        instance["initial_state_probabilities"][history_condition],
    )
    context = ModelVisibleContextV3(history_condition=history_condition)
    events: list[PublicEventV3] = [
        OccurrenceEvent(1, "CURRENT_COMMITMENT_MISSED", "REGISTERED_REPORT", "counterpart", "focal")
    ]
    prefix1 = ObservablePrefixV3(context=context, events=tuple(events))
    action1_index = _sample_index(prebranch_seed, "target-action:P1", immediate[z0])
    action1 = IMMEDIATE_ACTIONS[action1_index]

    events.append(ActionEvent(2, action1))
    feedback1_index = _sample_index(
        prebranch_seed, "feedback:P1", feedback[action1][z0]
    )
    events.append(FeedbackEvent(3, FEEDBACK_CATEGORIES[feedback1_index]))
    z1 = _sample_index(trajectory_seed, "transition:P1", transition[z0])

    cue1, cue2 = _BRANCH_CUES[continuation_condition]
    events.append(cue1)
    context = _context_after(context, cue1)
    prefix2 = ObservablePrefixV3(context=context, events=tuple(events))
    action2_index = _sample_index(trajectory_seed, "target-action:P2", immediate[z1])
    action2 = IMMEDIATE_ACTIONS[action2_index]

    events.append(ActionEvent(5, action2))
    feedback2_index = _sample_index(
        trajectory_seed, "feedback:P2", feedback[action2][z1]
    )
    events.append(FeedbackEvent(6, FEEDBACK_CATEGORIES[feedback2_index]))
    z2 = _sample_index(trajectory_seed, "transition:P2", transition[z1])

    events.append(cue2)
    context = _context_after(context, cue2)
    prefix3 = ObservablePrefixV3(context=context, events=tuple(events))
    action3_index = _sample_index(trajectory_seed, "target-action:P3", immediate[z2])
    action3 = IMMEDIATE_ACTIONS[action3_index]
    z3 = _sample_index(trajectory_seed, "transition:terminal", transition[z2])
    terminal_index = _sample_index(trajectory_seed, "terminal-region", horizon[z3])
    terminal = LONG_HORIZON_REGIONS[terminal_index]

    records = tuple(
        PredictionRecordV3(
            key=PredictionKeyV3(source_instance_id, trajectory_id, ordinal, point),
            observable_prefix=prefix,
            immediate_target=action,
            terminal_target=terminal,
        )
        for point, ordinal, prefix, action in (
            ("P1", 1, prefix1, action1),
            ("P2", 4, prefix2, action2),
            ("P3", 7, prefix3, action3),
        )
    )
    return MaterializedTrajectoryV3(
        source_instance_id=source_instance_id,
        trajectory_id=trajectory_id,
        split=split,
        history_condition=history_condition,
        evaluator_continuation_condition=continuation_condition,
        sample_index=sample_index,
        prediction_records=records,
    )


def materialize_split(
    instances: Sequence[Mapping[str, Any]],
    *,
    family_seed_hex: str,
    split: str,
) -> list[MaterializedTrajectoryV3]:
    if split not in SPLITS:
        raise SourceProcessError("unknown split")
    expected_count = SPLIT_TRAJECTORIES_PER_INSTANCE[split]
    per_cell = expected_count // (len(HISTORY_CONDITIONS) * len(CONTINUATION_CONDITIONS))
    if per_cell * len(HISTORY_CONDITIONS) * len(CONTINUATION_CONDITIONS) != expected_count:
        raise AssertionError("split count is not balanced over the condition grid")
    trajectories: list[MaterializedTrajectoryV3] = []
    for instance in sorted(instances, key=lambda item: int(item["instance_index"])):
        split_seed = derive_split_seed(family_seed_hex, str(instance["instance_id"]), split)
        for history_condition in HISTORY_CONDITIONS:
            for continuation_condition in CONTINUATION_CONDITIONS:
                for sample_index in range(per_cell):
                    trajectories.append(
                        materialize_trajectory(
                            instance,
                            split_seed_hex=split_seed,
                            split=split,
                            history_condition=history_condition,
                            continuation_condition=continuation_condition,
                            sample_index=sample_index,
                        )
                    )
    expected_total = len(instances) * expected_count
    if len(trajectories) != expected_total:
        raise AssertionError("materialized split count mismatch")
    return trajectories


def corpus_manifest(trajectories: Sequence[MaterializedTrajectoryV3]) -> dict[str, Any]:
    serialized = [trajectory.to_dict(include_evaluator_metadata=True) for trajectory in trajectories]
    keys = [
        (
            record.key.source_instance_id,
            record.key.trajectory_id,
            record.key.step_ordinal,
            record.key.prediction_point_id,
        )
        for trajectory in trajectories
        for record in trajectory.prediction_records
    ]
    if len(keys) != len(set(keys)):
        raise SourceProcessError("duplicate prediction identity in corpus")
    return {
        "runtime_version": RUNTIME_VERSION,
        "trajectory_count": len(trajectories),
        "prediction_count": len(keys),
        "corpus_sha256": sha256_hex(serialized),
        "canonical_order": "INSTANCE_HISTORY_CONTINUATION_SAMPLE_THEN_P1_P2_P3",
        "post_seed_selection": "FORBIDDEN",
    }
