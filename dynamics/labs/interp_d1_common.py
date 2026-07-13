from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any


MAX_SAFE_INTEGER = 2**53 - 1
CANONICALIZATION_ID = "interp-canonical-json-v1"


class FrozenD1ExecutionError(ValueError):
    """Raised before or during execution of the frozen D1 contract."""


def _parse_integer(token: str) -> int:
    if token == "-0" or token.startswith("-"):
        raise FrozenD1ExecutionError("negative integers and negative zero are forbidden")
    if len(token) > len(str(MAX_SAFE_INTEGER)):
        raise FrozenD1ExecutionError("integer outside the canonical safe range")
    try:
        value = int(token)
    except ValueError as error:
        raise FrozenD1ExecutionError("invalid canonical integer") from error
    if value > MAX_SAFE_INTEGER:
        raise FrozenD1ExecutionError("integer outside the canonical safe range")
    return value


def _reject_float(token: str) -> None:
    raise FrozenD1ExecutionError(f"JSON floats are forbidden: {token}")


def _reject_constant(token: str) -> None:
    raise FrozenD1ExecutionError(f"non-finite JSON number is forbidden: {token}")


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FrozenD1ExecutionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_canonical_domain(value: Any, path: str = "$") -> None:
    if value is None:
        raise FrozenD1ExecutionError(f"null is forbidden at {path}")
    if isinstance(value, float):
        raise FrozenD1ExecutionError(f"float is forbidden at {path}")
    if isinstance(value, int) and not isinstance(value, bool):
        if not 0 <= value <= MAX_SAFE_INTEGER:
            raise FrozenD1ExecutionError(f"integer outside canonical range at {path}")
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise FrozenD1ExecutionError(f"Unicode surrogate is forbidden at {path}")
        if unicodedata.normalize("NFC", value) != value:
            raise FrozenD1ExecutionError(f"non-NFC string at {path}")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or not key.isascii():
                raise FrozenD1ExecutionError(f"non-ASCII object key at {path}")
            _validate_canonical_domain(child, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _validate_canonical_domain(child, f"{path}/{index}")


def loads_exact(source: bytes | str) -> dict[str, Any]:
    try:
        text = source.decode("utf-8") if isinstance(source, bytes) else source
    except UnicodeDecodeError as error:
        raise FrozenD1ExecutionError("execution manifest is not UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_int=_parse_integer,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except FrozenD1ExecutionError:
        raise
    except (json.JSONDecodeError, UnicodeError) as error:
        raise FrozenD1ExecutionError("execution manifest is not valid JSON") from error
    if not isinstance(value, dict):
        raise FrozenD1ExecutionError("top-level JSON value must be an object")
    _validate_canonical_domain(value)
    return value


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


def load_exact(path: str | Path) -> dict[str, Any]:
    return loads_exact(Path(path).read_bytes())


def digest_without_nested_member(
    value: dict[str, Any], container_key: str, member_key: str
) -> str:
    payload = deepcopy(value)
    try:
        del payload[container_key][member_key]
    except (KeyError, TypeError) as error:
        raise FrozenD1ExecutionError(
            f"digest member missing: {container_key}.{member_key}"
        ) from error
    return digest(payload)


def scope_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    fields = (
        "actor_alias",
        "interpreted_target_scope_alias",
        "relation_scope_alias",
        "context_scope_alias",
    )
    try:
        return all(left[field] == right[field] for field in fields) and (
            canonical_bytes(left["target_resolution"])
            == canonical_bytes(right["target_resolution"])
        )
    except KeyError as error:
        raise FrozenD1ExecutionError(
            f"incomplete scope object: {error.args[0]}"
        ) from error


def _local_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise FrozenD1ExecutionError(f"schema reference is not local: {ref}")
    value: Any = root_schema
    for segment in ref[2:].split("/"):
        segment = segment.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or segment not in value:
            raise FrozenD1ExecutionError(f"schema reference does not resolve: {ref}")
        value = value[segment]
    if not isinstance(value, dict):
        raise FrozenD1ExecutionError(f"schema reference is not an object: {ref}")
    return value


def validate_json_schema(
    value: Any,
    schema: dict[str, Any],
    *,
    root_schema: dict[str, Any] | None = None,
    external_schemas: dict[str, dict[str, Any]] | None = None,
    path: str = "$",
) -> None:
    """Validate the dependency-free JSON-Schema subset frozen by D1."""
    root_schema = root_schema or schema
    external_schemas = external_schemas or {}
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/"):
            target = _local_ref(root_schema, ref)
            target_root = root_schema
        else:
            document, separator, fragment = ref.partition("#")
            if document not in external_schemas:
                raise FrozenD1ExecutionError(f"external schema is unavailable: {document}")
            target_root = external_schemas[document]
            target = (
                _local_ref(target_root, f"#/{fragment.lstrip('/')}")
                if separator and fragment
                else target_root
            )
        validate_json_schema(
            value,
            target,
            root_schema=target_root,
            external_schemas=external_schemas,
            path=path,
        )
        return
    for branch in schema.get("allOf", []):
        validate_json_schema(
            value,
            branch,
            root_schema=root_schema,
            external_schemas=external_schemas,
            path=path,
        )
    if "oneOf" in schema:
        matches = 0
        for branch in schema["oneOf"]:
            try:
                validate_json_schema(
                    value,
                    branch,
                    root_schema=root_schema,
                    external_schemas=external_schemas,
                    path=path,
                )
            except (ValueError, FrozenD1ExecutionError):
                continue
            matches += 1
        if matches != 1:
            raise FrozenD1ExecutionError(
                f"schema oneOf matched {matches} branches at {path}"
            )
        return
    if "const" in schema and canonical_bytes(value) != canonical_bytes(schema["const"]):
        raise FrozenD1ExecutionError(f"schema const mismatch at {path}")
    if "enum" in schema and not any(
        canonical_bytes(value) == canonical_bytes(candidate)
        for candidate in schema["enum"]
    ):
        raise FrozenD1ExecutionError(f"schema enum mismatch at {path}")
    expected_type = schema.get("type")
    type_matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }
    if expected_type is not None and not type_matches.get(expected_type, False):
        raise FrozenD1ExecutionError(f"schema type mismatch at {path}")
    if isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            raise FrozenD1ExecutionError(
                f"schema minProperties mismatch at {path}"
            )
        required = set(schema.get("required", []))
        if not required <= set(value):
            raise FrozenD1ExecutionError(f"schema required property missing at {path}")
        properties = schema.get("properties", {})
        extra = set(value) - set(properties)
        additional = schema.get("additionalProperties")
        if additional is False and extra:
            raise FrozenD1ExecutionError(f"schema additional property at {path}")
        if isinstance(additional, dict):
            for key in extra:
                validate_json_schema(
                    value[key], additional, root_schema=root_schema,
                    external_schemas=external_schemas, path=f"{path}/{key}"
                )
        for key, child_schema in properties.items():
            if key in value:
                validate_json_schema(
                    value[key], child_schema, root_schema=root_schema,
                    external_schemas=external_schemas, path=f"{path}/{key}"
                )
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise FrozenD1ExecutionError(f"schema minItems mismatch at {path}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise FrozenD1ExecutionError(f"schema maxItems mismatch at {path}")
        if schema.get("uniqueItems"):
            encoded = [canonical_bytes(item) for item in value]
            if len(encoded) != len(set(encoded)):
                raise FrozenD1ExecutionError(f"schema uniqueItems mismatch at {path}")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_json_schema(
                    item, schema["items"], root_schema=root_schema,
                    external_schemas=external_schemas, path=f"{path}/{index}"
                )
        if "contains" in schema:
            count = 0
            for item in value:
                try:
                    validate_json_schema(
                        item, schema["contains"], root_schema=root_schema,
                        external_schemas=external_schemas, path=path
                    )
                except (ValueError, FrozenD1ExecutionError):
                    continue
                count += 1
            if count < schema.get("minContains", 1) or (
                "maxContains" in schema and count > schema["maxContains"]
            ):
                raise FrozenD1ExecutionError(f"schema contains mismatch at {path}")
    elif isinstance(value, str):
        import re
        if len(value) < schema.get("minLength", 0):
            raise FrozenD1ExecutionError(f"schema minLength mismatch at {path}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise FrozenD1ExecutionError(f"schema pattern mismatch at {path}")
    elif isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise FrozenD1ExecutionError(f"schema minimum mismatch at {path}")
        if "maximum" in schema and value > schema["maximum"]:
            raise FrozenD1ExecutionError(f"schema maximum mismatch at {path}")
