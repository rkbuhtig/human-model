from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

SCHEMA_VERSION = "human-dyn-adeq-s0-v2/1.0.0"
PREDICTION_SCHEMA_VERSION = "s0-v2-prediction/1.0.0"
STATE_SCHEMA_VERSION = "s0-v2-h-state/1.0.0"
PROBABILITY_SCALE = 1_000_000

HISTORY_CONDITIONS = ("H-STABLE", "H-BREACH")
CONTINUATION_CONDITIONS = ("F-REPAIR", "F-DEFLECT", "F-REPEAT", "F-PUBLIC")
RECEIPT_SCOPES = (
    "REGISTERED_REPORT",
    "INTERNAL_OCCURRENCE_REPORT",
    "CERTIFIED_WORLD_OCCURRENCE",
)
ACTORS = ("focal", "counterpart", "environment")
TARGETS = ("focal", "counterpart", "interaction")
ROLE_CONTEXTS = ("PRIVATE_RELATION", "PUBLIC_ROLE")
AUDIENCE_CONTEXTS = ("NO_AUDIENCE", "AUDIENCE_PRESENT")
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
FEEDBACK_KINDS = (
    "ACKNOWLEDGED_IMPACT",
    "ACCEPTED_RESPONSIBILITY",
    "OFFERED_COSTLY_REPAIR",
    "MINIMIZED_IMPACT",
    "SHIFTED_RESPONSIBILITY",
    "NO_RESPONSE",
)
EVENT_KINDS = (
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

EVENT_COMPATIBILITY: dict[str, dict[str, tuple[str, ...]]] = {
    "CURRENT_COMMITMENT_MISSED": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "COUNTERPART_ACKNOWLEDGES_IMPACT": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "COUNTERPART_ACCEPTS_RESPONSIBILITY": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "COUNTERPART_OFFERS_COSTLY_REPAIR": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "COUNTERPART_MINIMIZES_IMPACT": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "COUNTERPART_SHIFTS_RESPONSIBILITY": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "SIMILAR_VIOLATION_REPEATED": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("counterpart",), "targets": ("focal",)},
    "AUDIENCE_CONSTRAINT_PRESENT": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("environment",), "targets": ("interaction",)},
    "ROLE_CONSTRAINT_PRESENT": {"scopes": ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE"), "actors": ("environment",), "targets": ("interaction",)},
    "SELF_ACTION_CAUSALLY_ATTRIBUTED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT",), "actors": ("focal",), "targets": ("focal",)},
    "SELF_CONTROL_ATTRIBUTED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT",), "actors": ("focal",), "targets": ("focal",)},
    "SELF_OWNERSHIP_EXPRESSED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT", "REGISTERED_REPORT"), "actors": ("focal",), "targets": ("focal",)},
    "SELF_RESPONSIBILITY_ACCEPTED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT", "REGISTERED_REPORT"), "actors": ("focal",), "targets": ("focal",)},
    "SELF_ENDORSEMENT_EXPRESSED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT", "REGISTERED_REPORT"), "actors": ("focal",), "targets": ("focal",)},
    "SELF_REPUDIATION_EXPRESSED": {"scopes": ("INTERNAL_OCCURRENCE_REPORT", "REGISTERED_REPORT"), "actors": ("focal",), "targets": ("focal",)},
    "NO_NEW_INFORMATION": {"scopes": ("REGISTERED_REPORT",), "actors": ("environment",), "targets": ("interaction",)},
}

FORBIDDEN_INPUT_KEYS = frozenset({
    "latent_state", "hidden_state", "target_probabilities", "evaluation_label",
    "reference_state", "source_seed", "emission_parameters", "transition_matrix",
    "bootstrap_seed", "source_family_seed",
})


class S0V2Error(ValueError):
    pass


def canonical_bytes(value: object) -> bytes:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def reject_hidden_fields(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in FORBIDDEN_INPUT_KEYS:
                raise S0V2Error(f"forbidden evaluator field at {path}/{key}")
            reject_hidden_fields(child, f"{path}/{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            reject_hidden_fields(child, f"{path}/{index}")


def require_exact_keys(value: Mapping[str, Any], allowed: tuple[str, ...], path: str) -> None:
    missing = set(allowed) - set(value)
    extra = set(value) - set(allowed)
    if missing or extra:
        raise S0V2Error(f"{path} key mismatch missing={sorted(missing)} extra={sorted(extra)}")


@dataclass(frozen=True, order=True)
class PredictionKey:
    source_instance_id: str
    trajectory_id: str
    step_ordinal: int
    prediction_point_id: str

    def __post_init__(self) -> None:
        if not self.source_instance_id or not self.trajectory_id or not self.prediction_point_id:
            raise S0V2Error("prediction key strings must be non-empty")
        if self.step_ordinal < 0:
            raise S0V2Error("step ordinal must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "PredictionKey":
        require_exact_keys(value, ("source_instance_id", "trajectory_id", "step_ordinal", "prediction_point_id"), "prediction_key")
        return cls(str(value["source_instance_id"]), str(value["trajectory_id"]), int(value["step_ordinal"]), str(value["prediction_point_id"]))


@dataclass(frozen=True)
class TypedReceipt:
    receipt_id: str
    ordinal: int
    scope: str
    event_kind: str
    actor: str
    target: str

    def __post_init__(self) -> None:
        if not self.receipt_id:
            raise S0V2Error("receipt id required")
        if self.ordinal < 1:
            raise S0V2Error("receipt ordinal must be >= 1")
        if self.scope not in RECEIPT_SCOPES or self.event_kind not in EVENT_KINDS:
            raise S0V2Error("unknown scope or event")
        if self.actor not in ACTORS or self.target not in TARGETS:
            raise S0V2Error("unknown actor or target")
        rule = EVENT_COMPATIBILITY[self.event_kind]
        if self.scope not in rule["scopes"] or self.actor not in rule["actors"] or self.target not in rule["targets"]:
            raise S0V2Error(f"incompatible receipt event={self.event_kind} scope={self.scope} actor={self.actor} target={self.target}")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TypedReceipt":
        require_exact_keys(value, ("receipt_id", "ordinal", "scope", "event_kind", "actor", "target"), "receipt")
        return cls(
            receipt_id=str(value["receipt_id"]), ordinal=int(value["ordinal"]), scope=str(value["scope"]),
            event_kind=str(value["event_kind"]), actor=str(value["actor"]), target=str(value["target"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicContext:
    history_condition: str
    continuation_condition: str
    role_context: str
    audience_context: str

    def __post_init__(self) -> None:
        if self.history_condition not in HISTORY_CONDITIONS:
            raise S0V2Error("unknown history condition")
        if self.continuation_condition not in CONTINUATION_CONDITIONS:
            raise S0V2Error("unknown continuation condition")
        if self.role_context not in ROLE_CONTEXTS or self.audience_context not in AUDIENCE_CONTEXTS:
            raise S0V2Error("unknown public context")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ObservablePrefixV2:
    schema_version: str
    key: PredictionKey
    context: PublicContext
    receipts: tuple[TypedReceipt, ...]
    public_actions: tuple[str, ...]
    counterpart_feedback: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise S0V2Error("unsupported prefix schema")
        ordinals = [item.ordinal for item in self.receipts]
        if ordinals != sorted(ordinals) or len(ordinals) != len(set(ordinals)):
            raise S0V2Error("receipt ordinals must be strictly increasing")
        if ordinals and ordinals[-1] != self.key.step_ordinal:
            raise S0V2Error("last receipt ordinal must equal prediction step")
        if any(item not in IMMEDIATE_ACTIONS for item in self.public_actions):
            raise S0V2Error("unknown public action")
        if any(item not in FEEDBACK_KINDS for item in self.counterpart_feedback):
            raise S0V2Error("unknown counterpart feedback")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ObservablePrefixV2":
        reject_hidden_fields(value)
        require_exact_keys(value, ("schema_version", "key", "context", "receipts", "public_actions", "counterpart_feedback"), "prefix")
        context = value["context"]
        require_exact_keys(context, ("history_condition", "continuation_condition", "role_context", "audience_context"), "context")
        return cls(
            schema_version=str(value["schema_version"]),
            key=PredictionKey.from_dict(value["key"]),
            context=PublicContext(**{key: str(context[key]) for key in context}),
            receipts=tuple(TypedReceipt.from_dict(item) for item in value["receipts"]),
            public_actions=tuple(str(item) for item in value["public_actions"]),
            counterpart_feedback=tuple(str(item) for item in value["counterpart_feedback"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "key": self.key.to_dict(),
            "context": self.context.to_dict(),
            "receipts": [item.to_dict() for item in self.receipts],
            "public_actions": list(self.public_actions),
            "counterpart_feedback": list(self.counterpart_feedback),
        }


@dataclass(frozen=True)
class PublicDeltaV2:
    schema_version: str
    key: PredictionKey
    context: PublicContext
    receipt: TypedReceipt
    new_public_actions: tuple[str, ...] = ()
    new_counterpart_feedback: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise S0V2Error("unsupported delta schema")
        if self.receipt.ordinal != self.key.step_ordinal:
            raise S0V2Error("delta receipt ordinal/key mismatch")
        if any(item not in IMMEDIATE_ACTIONS for item in self.new_public_actions):
            raise S0V2Error("unknown action in delta")
        if any(item not in FEEDBACK_KINDS for item in self.new_counterpart_feedback):
            raise S0V2Error("unknown feedback in delta")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "key": self.key.to_dict(),
            "context": self.context.to_dict(),
            "receipt": self.receipt.to_dict(),
            "new_public_actions": list(self.new_public_actions),
            "new_counterpart_feedback": list(self.new_counterpart_feedback),
        }


@dataclass(frozen=True)
class PredictiveHState:
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

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class AuthorityProbeState:
    consent: int = 0
    fault: int = 0
    obligation: int = 0
    permission: int = 0
    authority: int = 0

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class HStateEnvelope:
    schema_version: str
    state_version: str
    trajectory_id: str
    last_step_ordinal: int
    receipt_chain_sha256: str
    predictive_state: PredictiveHState
    state_digest: str

    @classmethod
    def build(cls, *, state_version: str, trajectory_id: str, last_step_ordinal: int,
              receipt_chain_sha256: str, predictive_state: PredictiveHState) -> "HStateEnvelope":
        payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "state_version": state_version,
            "trajectory_id": trajectory_id,
            "last_step_ordinal": last_step_ordinal,
            "receipt_chain_sha256": receipt_chain_sha256,
            "predictive_state": predictive_state.to_dict(),
        }
        return cls(
            schema_version=STATE_SCHEMA_VERSION,
            state_version=state_version,
            trajectory_id=trajectory_id,
            last_step_ordinal=last_step_ordinal,
            receipt_chain_sha256=receipt_chain_sha256,
            predictive_state=predictive_state,
            state_digest=sha256(payload),
        )

    def verify(self) -> None:
        rebuilt = HStateEnvelope.build(
            state_version=self.state_version,
            trajectory_id=self.trajectory_id,
            last_step_ordinal=self.last_step_ordinal,
            receipt_chain_sha256=self.receipt_chain_sha256,
            predictive_state=self.predictive_state,
        )
        if rebuilt.state_digest != self.state_digest:
            raise S0V2Error("H state digest mismatch")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "state_version": self.state_version,
            "trajectory_id": self.trajectory_id,
            "last_step_ordinal": self.last_step_ordinal,
            "receipt_chain_sha256": self.receipt_chain_sha256,
            "predictive_state": self.predictive_state.to_dict(),
            "state_digest": self.state_digest,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "HStateEnvelope":
        require_exact_keys(value, ("schema_version", "state_version", "trajectory_id", "last_step_ordinal", "receipt_chain_sha256", "predictive_state", "state_digest"), "h_state")
        if value["schema_version"] != STATE_SCHEMA_VERSION:
            raise S0V2Error("unsupported H state schema")
        predictive = value["predictive_state"]
        expected_fields = tuple(PredictiveHState.__dataclass_fields__)
        require_exact_keys(predictive, expected_fields, "predictive_state")
        obj = cls(
            schema_version=str(value["schema_version"]), state_version=str(value["state_version"]),
            trajectory_id=str(value["trajectory_id"]), last_step_ordinal=int(value["last_step_ordinal"]),
            receipt_chain_sha256=str(value["receipt_chain_sha256"]),
            predictive_state=PredictiveHState(**{field: int(predictive[field]) for field in expected_fields}),
            state_digest=str(value["state_digest"]),
        )
        obj.verify()
        return obj


def update_chain(previous: str, receipt: TypedReceipt) -> str:
    return hashlib.sha256((previous + ":" + sha256(receipt.to_dict())).encode("ascii")).hexdigest()


def clamp(value: int) -> int:
    return max(-1000, min(1000, int(value)))
