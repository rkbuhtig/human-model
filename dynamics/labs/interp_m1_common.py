from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def loads_exact(source: bytes | str) -> dict[str, Any]:
    def reject_duplicate_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    text = source.decode("utf-8") if isinstance(source, bytes) else source
    value = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def load_exact(path: str | Path) -> dict[str, Any]:
    return loads_exact(Path(path).read_bytes())


def resolve_local_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError("only local schema refs are supported")
    value: object = schema
    for segment in ref[2:].split("/"):
        if not isinstance(value, dict) or segment not in value:
            raise ValueError(f"schema ref does not resolve: {ref}")
        value = value[segment]
    if not isinstance(value, dict):
        raise ValueError(f"schema ref is not an object: {ref}")
    return value


def validate_json_schema(
    value: object,
    schema: dict[str, Any],
    *,
    root_schema: dict[str, Any] | None = None,
    path: str = "$",
) -> None:
    """Validate the dependency-free Draft 2020-12 subset used by INTERP M1."""
    root_schema = root_schema or schema
    if "$ref" in schema:
        validate_json_schema(
            value,
            resolve_local_ref(root_schema, schema["$ref"]),
            root_schema=root_schema,
            path=path,
        )
        return
    if "oneOf" in schema:
        matches = 0
        for branch in schema["oneOf"]:
            try:
                validate_json_schema(value, branch, root_schema=root_schema, path=path)
            except ValueError:
                continue
            matches += 1
        if matches != 1:
            raise ValueError(f"schema oneOf matched {matches} branches at {path}")
        return
    if "const" in schema and canonical_bytes(value) != canonical_bytes(schema["const"]):
        raise ValueError(f"schema const mismatch at {path}")
    if "enum" in schema and not any(
        canonical_bytes(value) == canonical_bytes(candidate)
        for candidate in schema["enum"]
    ):
        raise ValueError(f"schema enum mismatch at {path}")

    expected_type = schema.get("type")
    type_matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }
    if expected_type is not None and not type_matches.get(expected_type, False):
        raise ValueError(f"schema type mismatch at {path}")

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        if not required <= set(value):
            raise ValueError(f"schema required property missing at {path}")
        properties = schema.get("properties", {})
        extra_keys = set(value) - set(properties)
        additional = schema.get("additionalProperties")
        if additional is False and extra_keys:
            raise ValueError(f"schema additional property at {path}")
        if isinstance(additional, dict):
            for key in extra_keys:
                validate_json_schema(
                    value[key],
                    additional,
                    root_schema=root_schema,
                    path=f"{path}/{key}",
                )
        for key, child in properties.items():
            if key in value:
                validate_json_schema(
                    value[key],
                    child,
                    root_schema=root_schema,
                    path=f"{path}/{key}",
                )
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"schema minItems mismatch at {path}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValueError(f"schema maxItems mismatch at {path}")
        if schema.get("uniqueItems"):
            items = [canonical_bytes(item) for item in value]
            if len(items) != len(set(items)):
                raise ValueError(f"schema uniqueItems mismatch at {path}")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_json_schema(
                    item,
                    schema["items"],
                    root_schema=root_schema,
                    path=f"{path}/{index}",
                )
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"schema minLength mismatch at {path}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise ValueError(f"schema pattern mismatch at {path}")
    elif isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"schema minimum mismatch at {path}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValueError(f"schema maximum mismatch at {path}")


def present_ref(key: str | None) -> dict[str, object]:
    if key is None:
        return {"status": "missing", "reason": "not_applicable"}
    return {"status": "present", "key": key}


def profile_without_key(profile: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in profile.items() if key != "profile_key"}
