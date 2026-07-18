from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Iterable, Mapping

PROBABILITY_SCALE = 1_000_000
SCHEMA_VERSION = "human-dyn-adeq-s0/1.0.0"

HISTORY_CONDITIONS = ("H-STABLE", "H-BREACH")
CONTINUATION_CONDITIONS = ("F-REPAIR", "F-DEFLECT", "F-REPEAT", "F-PUBLIC")
RECEIPT_SCOPES = (
    "REGISTERED_REPORT",
    "INTERNAL_OCCURRENCE_REPORT",
    "CERTIFIED_WORLD_OCCURRENCE",
)
IMMEDIATE_ACTIONS = (
    "SEEK_CLARIFICATION",
    "EXPRESS_HURT",
    "ASSERT_BOUNDARY",
    "TEMPORARY_WITHDRAWAL",
    "PUNITIVE_ATTACK",
    "SUPPRESS_FOR_ROLE",
    "REPAIR_ATTEMPT",
    "RELATION_EXIT",
)
LONG_HORIZON_REGIONS = (
    "PARTIAL_REPAIR",
    "GUARDED_CONTINUATION",
    "CONFLICT_LOOP",
    "RELATION_EXIT",
    "UNRESOLVED_DRIFT",
)
DIRECTION_VALUES = ("increase", "stable", "decrease")
DIRECTION_FIELDS = (
    "trust",
    "relationship_continuation_motive",
    "threat_interpretation",
    "action_control_capacity",
)
ROLE_CONTEXTS = ("PRIVATE_RELATION", "PUBLIC_ROLE")
AUDIENCE_CONTEXTS = ("NO_AUDIENCE", "AUDIENCE_PRESENT")
ACTOR_ALIASES = ("focal", "counterpart")
COUNTERPART_FEEDBACK_KINDS = (
    "ACKNOWLEDGED_IMPACT",
    "ACCEPTED_RESPONSIBILITY",
    "OFFERED_COSTLY_REPAIR",
    "MINIMIZED_IMPACT",
    "SHIFTED_RESPONSIBILITY",
    "NO_RESPONSE",
)
OBSERVABLE_EVENT_KINDS = (
    "CURRENT_COMMITMENT_MISSED",
    "COUNTERPART_ACKNOWLEDGES_IMPACT",
    "COUNTERPART_ACCEPTS_RESPONSIBILITY",
    "COUNTERPART_OFFERS_COSTLY_REPAIR",
    "COUNTERPART_MINIMIZES_IMPACT",
    "COUNTERPART_SHIFTS_RESPONSIBILITY",
    "SIMILAR_VIOLATION_REPEATED",
    "AUDIENCE_CONSTRAINT_PRESENT",
    "ROLE_CONSTRAINT_PRESENT",
    "SELF_ACTION_CAUSALLY_ATTRIBUTED",
    "SELF_CONTROL_ATTRIBUTED",
    "SELF_OWNERSHIP_EXPRESSED",
    "SELF_RESPONSIBILITY_ACCEPTED",
    "SELF_ENDORSEMENT_EXPRESSED",
    "SELF_REPUDIATION_EXPRESSED",
    "NO_NEW_INFORMATION",
)

FORBIDDEN_INPUT_KEYS = frozenset(
    {
        "latent_state",
        "hidden_state",
        "target_probabilities",
        "evaluation_label",
        "reference_state",
        "source_seed",
        "emission_parameters",
        "transition_matrix",
        "bootstrap_seed",
    }
)
OBSERVABLE_PREFIX_FIELDS = (
    "schema_version",
    "trajectory_id",
    "history_condition",
    "continuation_condition",
    "receipts",
    "public_actions",
    "counterpart_feedback",
    "role_context",
    "audience_context",
    "step_ordinal",
)


class S0ValidationError(ValueError):
    """Raised when an S0 artifact violates the public benchmark boundary."""


def canonical_bytes(value: object) -> bytes:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _require_exact_keys(value: Mapping[str, Any], allowed: Iterable[str], *, path: str) -> None:
    allowed_set = set(allowed)
    actual = set(value)
    missing = allowed_set - actual
    extra = actual - allowed_set
    if missing or extra:
        raise S0ValidationError(
            f"{path} keys mismatch; missing={sorted(missing)} extra={sorted(extra)}"
        )


def reject_hidden_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in FORBIDDEN_INPUT_KEYS:
                raise S0ValidationError(f"hidden/evaluator field forbidden at {path}/{key}")
            reject_hidden_fields(child, path=f"{path}/{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            reject_hidden_fields(child, path=f"{path}/{index}")


@dataclass(frozen=True)
class ObservableReceipt:
    receipt_id: str
    ordinal: int
    scope: str
    event_kind: str
    actor: str
    target: str
    public_value: str

    def __post_init__(self) -> None:
        if not self.receipt_id:
            raise S0ValidationError("receipt_id must be non-empty")
        if self.ordinal < 0:
            raise S0ValidationError("receipt ordinal must be non-negative")
        if self.scope not in RECEIPT_SCOPES:
            raise S0ValidationError(f"unknown receipt scope: {self.scope}")
        if self.event_kind not in OBSERVABLE_EVENT_KINDS:
            raise S0ValidationError(f"unknown observable event kind: {self.event_kind}")
        if self.actor not in ACTOR_ALIASES or self.target not in ACTOR_ALIASES:
            raise S0ValidationError("receipt actor and target must be registered aliases")
        if self.public_value != self.event_kind:
            raise S0ValidationError("public_value must equal the registered event_kind code")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ObservableReceipt":
        _require_exact_keys(
            value,
            ("receipt_id", "ordinal", "scope", "event_kind", "actor", "target", "public_value"),
            path="receipt",
        )
        return cls(
            receipt_id=str(value["receipt_id"]),
            ordinal=int(value["ordinal"]),
            scope=str(value["scope"]),
            event_kind=str(value["event_kind"]),
            actor=str(value["actor"]),
            target=str(value["target"]),
            public_value=str(value["public_value"]),
        )


@dataclass(frozen=True)
class ObservableEpisodePrefix:
    schema_version: str
    trajectory_id: str
    history_condition: str
    continuation_condition: str
    receipts: tuple[ObservableReceipt, ...]
    public_actions: tuple[str, ...]
    counterpart_feedback: tuple[str, ...]
    role_context: str
    audience_context: str
    step_ordinal: int

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise S0ValidationError(f"unsupported prefix schema: {self.schema_version}")
        if not self.trajectory_id:
            raise S0ValidationError("trajectory_id must be non-empty")
        if self.history_condition not in HISTORY_CONDITIONS:
            raise S0ValidationError(f"unknown history condition: {self.history_condition}")
        if self.continuation_condition not in CONTINUATION_CONDITIONS:
            raise S0ValidationError(
                f"unknown continuation condition: {self.continuation_condition}"
            )
        if self.step_ordinal < 0:
            raise S0ValidationError("step_ordinal must be non-negative")
        ordinals = [receipt.ordinal for receipt in self.receipts]
        if ordinals != sorted(ordinals) or len(ordinals) != len(set(ordinals)):
            raise S0ValidationError("receipt ordinals must be strictly increasing")
        if ordinals and ordinals[-1] > self.step_ordinal:
            raise S0ValidationError("receipt ordinal exceeds current step")
        if self.role_context not in ROLE_CONTEXTS:
            raise S0ValidationError(f"unknown role context: {self.role_context}")
        if self.audience_context not in AUDIENCE_CONTEXTS:
            raise S0ValidationError(f"unknown audience context: {self.audience_context}")
        if any(action not in IMMEDIATE_ACTIONS for action in self.public_actions):
            raise S0ValidationError("public_actions contains an unregistered action")
        if any(item not in COUNTERPART_FEEDBACK_KINDS for item in self.counterpart_feedback):
            raise S0ValidationError("counterpart_feedback contains an unregistered code")
        if any(token in self.trajectory_id.lower() for token in ("q0", "q1", "q2", "q3", "q4", "q5", "latent", "target")):
            raise S0ValidationError("trajectory_id exposes a forbidden hidden-source token")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ObservableEpisodePrefix":
        reject_hidden_fields(value)
        _require_exact_keys(value, OBSERVABLE_PREFIX_FIELDS, path="prefix")
        receipts_raw = value["receipts"]
        if not isinstance(receipts_raw, list):
            raise S0ValidationError("receipts must be a list")
        actions = value["public_actions"]
        feedback = value["counterpart_feedback"]
        if not isinstance(actions, list) or not all(isinstance(item, str) for item in actions):
            raise S0ValidationError("public_actions must be a string list")
        if not isinstance(feedback, list) or not all(isinstance(item, str) for item in feedback):
            raise S0ValidationError("counterpart_feedback must be a string list")
        return cls(
            schema_version=str(value["schema_version"]),
            trajectory_id=str(value["trajectory_id"]),
            history_condition=str(value["history_condition"]),
            continuation_condition=str(value["continuation_condition"]),
            receipts=tuple(ObservableReceipt.from_dict(item) for item in receipts_raw),
            public_actions=tuple(actions),
            counterpart_feedback=tuple(feedback),
            role_context=str(value["role_context"]),
            audience_context=str(value["audience_context"]),
            step_ordinal=int(value["step_ordinal"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "trajectory_id": self.trajectory_id,
            "history_condition": self.history_condition,
            "continuation_condition": self.continuation_condition,
            "receipts": [asdict(item) for item in self.receipts],
            "public_actions": list(self.public_actions),
            "counterpart_feedback": list(self.counterpart_feedback),
            "role_context": self.role_context,
            "audience_context": self.audience_context,
            "step_ordinal": self.step_ordinal,
        }

    @property
    def current_event_kind(self) -> str:
        return self.receipts[-1].event_kind if self.receipts else "NO_NEW_INFORMATION"


@dataclass(frozen=True)
class TrainingExample:
    prefix: ObservableEpisodePrefix
    immediate_label: str
    horizon_label: str

    def __post_init__(self) -> None:
        if self.immediate_label not in IMMEDIATE_ACTIONS:
            raise S0ValidationError(f"unknown immediate target: {self.immediate_label}")
        if self.horizon_label not in LONG_HORIZON_REGIONS:
            raise S0ValidationError(f"unknown horizon target: {self.horizon_label}")


@dataclass(frozen=True)
class HState:
    threat: int
    approach: int
    control_capacity: int
    unresolved_breach: int
    repair_progress: int
    trust_expectation: int
    continuation_commitment: int
    counterpart_reliability: int
    expected_repair: int
    causal_attribution: int
    control_attribution: int
    reflective_ownership: int
    endorsement: int
    responsibility_acceptance: int
    consent: int
    fault: int
    obligation: int
    permission: int
    authority: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def clamp_state(value: int) -> int:
    return max(-1000, min(1000, int(value)))


def normalize_probability_units(values: Mapping[str, int], categories: tuple[str, ...]) -> dict[str, int]:
    if set(values) != set(categories):
        raise S0ValidationError("probability category set mismatch")
    if any(not isinstance(value, int) or value < 0 for value in values.values()):
        raise S0ValidationError("probability units must be non-negative integers")
    if sum(values.values()) != PROBABILITY_SCALE:
        raise S0ValidationError("probability units must sum to scale")
    return {category: values[category] for category in categories}


def logits_to_probability_units(
    logits: Mapping[str, float], categories: tuple[str, ...]
) -> dict[str, int]:
    if set(logits) != set(categories):
        raise S0ValidationError("logit category set mismatch")
    if not all(math.isfinite(value) for value in logits.values()):
        raise S0ValidationError("logits must be finite")
    maximum = max(logits.values())
    weights = [math.exp(logits[category] - maximum) for category in categories]
    total = sum(weights)
    raw = [weight / total * PROBABILITY_SCALE for weight in weights]
    units = [int(value) for value in raw]
    remainder = PROBABILITY_SCALE - sum(units)
    order = sorted(
        range(len(categories)),
        key=lambda index: (raw[index] - units[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        units[index] += 1
    return normalize_probability_units(dict(zip(categories, units)), categories)
