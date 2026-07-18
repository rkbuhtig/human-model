from __future__ import annotations

from dataclasses import asdict, is_dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence

PROBABILITY_SCALE = 1_000_000
FAMILY_ID = "SIM-REL-BOUNDARY-FAMILY-002"
GENERATOR_VERSION = "sim-rel-boundary-family-generator/2.0.0"
RUNTIME_VERSION = "sim-rel-boundary-source-runtime/1.0.0"
PUBLIC_EVENT_SCHEMA_VERSION = "s0-public-event-v3/1.0.0"
OBSERVABLE_PREFIX_SCHEMA_VERSION = "s0-observable-prefix-v3/1.0.0"
PREDICTION_RECORD_SCHEMA_VERSION = "s0-source-prediction-record-v3/1.0.0"
TRAJECTORY_SCHEMA_VERSION = "s0-source-trajectory-v3/1.0.0"

LATENT_STATES = tuple(f"q{i}" for i in range(6))
HISTORY_CONDITIONS = ("H-STABLE", "H-BREACH")
CONTINUATION_CONDITIONS = ("F-REPAIR", "F-DEFLECT", "F-REPEAT", "F-PUBLIC")
SPLITS = ("development", "evaluation", "stability")
PREDICTION_POINTS = ("P1", "P2", "P3")
ROLE_CONTEXTS = ("PRIVATE_RELATION", "PUBLIC_ROLE")
AUDIENCE_CONTEXTS = ("NO_AUDIENCE", "AUDIENCE_PRESENT")
RECEIPT_SCOPES = ("REGISTERED_REPORT", "CERTIFIED_WORLD_OCCURRENCE")
ACTORS = ("focal", "counterpart", "environment")
TARGETS = ("focal", "counterpart", "interaction")

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
FEEDBACK_CATEGORIES = (
    "ACKNOWLEDGED_IMPACT",
    "ACCEPTED_RESPONSIBILITY",
    "OFFERED_COSTLY_REPAIR",
    "MINIMIZED_IMPACT",
    "SHIFTED_RESPONSIBILITY",
    "WITHHELD_RESPONSE",
)
OCCURRENCE_KINDS = (
    "CURRENT_COMMITMENT_MISSED",
    "COUNTERPART_ACKNOWLEDGES_IMPACT",
    "COUNTERPART_ACCEPTS_RESPONSIBILITY",
    "COUNTERPART_MINIMIZES_IMPACT",
    "COUNTERPART_SHIFTS_RESPONSIBILITY",
    "SIMILAR_VIOLATION_REPEATED",
)
CONTEXT_KINDS = ("AUDIENCE_CONSTRAINT_PRESENT", "ROLE_CONSTRAINT_PRESENT")

SPLIT_TRAJECTORIES_PER_INSTANCE = {
    "development": 16,
    "evaluation": 64,
    "stability": 64,
}


class SourceProcessError(ValueError):
    """Raised when frozen source-process inputs or outputs violate their contract."""


def canonical_bytes(value: object) -> bytes:
    if is_dataclass(value):
        value = asdict(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: object) -> str:
    payload = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(payload).hexdigest()


def require_hex(value: str, *, length: int, name: str) -> str:
    if len(value) != length:
        raise SourceProcessError(f"{name} must contain {length} hexadecimal characters")
    try:
        bytes.fromhex(value)
    except ValueError as error:
        raise SourceProcessError(f"{name} must be hexadecimal") from error
    return value.lower()


def normalize_weights(weights: Sequence[int]) -> list[int]:
    if not weights or any(weight <= 0 for weight in weights):
        raise SourceProcessError("weights must be non-empty positive integers")
    total = sum(weights)
    numerators = [weight * PROBABILITY_SCALE for weight in weights]
    units = [value // total for value in numerators]
    remainder = PROBABILITY_SCALE - sum(units)
    order = sorted(
        range(len(weights)),
        key=lambda index: (numerators[index] % total, -index),
        reverse=True,
    )
    for index in order[:remainder]:
        units[index] += 1
    if sum(units) != PROBABILITY_SCALE:
        raise AssertionError("probability normalization failed")
    return units


def distribution_ok(
    distribution: Sequence[int],
    *,
    category_count: int,
    minimum_probability: float,
    maximum_probability: float,
) -> bool:
    return (
        len(distribution) == category_count
        and sum(distribution) == PROBABILITY_SCALE
        and min(distribution) >= round(minimum_probability * PROBABILITY_SCALE)
        and max(distribution) <= round(maximum_probability * PROBABILITY_SCALE)
    )


def total_variation(left: Sequence[int] | Sequence[float], right: Sequence[int] | Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise SourceProcessError("total variation requires equal non-empty vectors")
    scale = PROBABILITY_SCALE if isinstance(left[0], int) else 1.0
    return sum(abs(float(a) - float(b)) for a, b in zip(left, right)) / (2.0 * scale)


def require_exact_keys(value: Mapping[str, Any], allowed: Sequence[str], path: str) -> None:
    missing = set(allowed) - set(value)
    extra = set(value) - set(allowed)
    if missing or extra:
        raise SourceProcessError(
            f"{path} key mismatch missing={sorted(missing)} extra={sorted(extra)}"
        )


class HashStream:
    """Deterministic hash-based random stream with explicit domain separation."""

    def __init__(self, seed_hex: str, domain: str) -> None:
        self.seed_hex = require_hex(seed_hex, length=64, name="seed_hex")
        if not domain:
            raise SourceProcessError("stream domain must be non-empty")
        self.domain = domain
        self.counter = 0

    def _block(self) -> bytes:
        payload = b"|".join(
            (
                bytes.fromhex(self.seed_hex),
                self.domain.encode("utf-8"),
                str(self.counter).encode("ascii"),
            )
        )
        self.counter += 1
        return hashlib.sha256(payload).digest()

    def integer(self, minimum: int, maximum: int) -> int:
        if minimum > maximum:
            raise SourceProcessError("invalid integer range")
        width = maximum - minimum + 1
        limit = (1 << 64) - ((1 << 64) % width)
        while True:
            value = int.from_bytes(self._block()[:8], "big")
            if value < limit:
                return minimum + value % width

    def choice_index(self, distribution: Sequence[int]) -> int:
        if not distribution or sum(distribution) != PROBABILITY_SCALE or min(distribution) < 0:
            raise SourceProcessError("choice distribution must be normalized non-negative units")
        draw = self.integer(0, PROBABILITY_SCALE - 1)
        cumulative = 0
        for index, units in enumerate(distribution):
            cumulative += units
            if draw < cumulative:
                return index
        raise AssertionError("normalized distribution did not select a category")


def derive_domain_seed(seed_hex: str, *parts: object) -> str:
    require_hex(seed_hex, length=64, name="seed_hex")
    material = "|".join((seed_hex.lower(), *(str(part) for part in parts)))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()
