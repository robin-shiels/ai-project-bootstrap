#!/usr/bin/env python3
"""Validate a portable AI Bootstrap setup state (Einrichtungsstand).

The JSON Schema document ``onboarding/STATE.schema.json`` describes the
format. This module is the actual check: it reads the enums and required
field lists from that document and enforces them, plus rules a schema alone
does not express (no secret-looking values, known schema version, unknown
values written as ``"unknown"`` instead of being left out).

Standard library only. Usage::

    python3 scripts/onboarding_state.py validate <state.json>

Exit 0: valid. Exit 1: invalid (each problem on its own line). Exit 2: usage
or unreadable file.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SUPPORTED_SCHEMA_VERSIONS = (1,)

SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent / "onboarding" / "STATE.schema.json"
)

# Values that look like credentials must never be stored in a portable state.
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"(?i)\b(password|passwort|kennwort|token|secret|api[_-]?key)\s*[:=]\s*\S+"
    ),
)


def load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve(schema: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    ref = node.get("$ref")
    if ref is None:
        return node
    target: Any = schema
    for part in ref.removeprefix("#/").split("/"):
        target = target[part]
    return target


def _check_value(
    schema: dict[str, Any],
    node: dict[str, Any],
    value: Any,
    where: str,
    errors: list[str],
) -> None:
    node = _resolve(schema, node)
    if "const" in node:
        if value != node["const"] or type(value) is not type(node["const"]):
            errors.append(f"{where}: must be {node['const']!r}, got {value!r}")
        return
    if "enum" in node:
        if not isinstance(value, str) or value not in node["enum"]:
            errors.append(
                f"{where}: unknown value {value!r}; allowed: {', '.join(node['enum'])}"
            )
        return
    kind = node.get("type")
    if kind == "string":
        if not isinstance(value, str):
            errors.append(f"{where}: must be a string, got {type(value).__name__}")
            return
        if len(value) < node.get("minLength", 0):
            errors.append(f"{where}: must not be empty")
        if "maxLength" in node and len(value) > node["maxLength"]:
            errors.append(f"{where}: longer than {node['maxLength']} characters")
        if "pattern" in node and not re.search(node["pattern"], value):
            errors.append(f"{where}: {value!r} has the wrong format")
    elif kind == "array":
        if not isinstance(value, list):
            errors.append(f"{where}: must be a list, got {type(value).__name__}")
            return
        for index, item in enumerate(value):
            _check_value(schema, node["items"], item, f"{where}[{index}]", errors)
    elif kind == "object":
        _check_object(schema, node, value, where, errors)


def _check_object(
    schema: dict[str, Any],
    node: dict[str, Any],
    value: Any,
    where: str,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{where}: must be an object, got {type(value).__name__}")
        return
    properties: dict[str, Any] = node.get("properties", {})
    for key in node.get("required", []):
        if key not in value:
            errors.append(
                f'{where}.{key}: missing (write "unknown" or an empty list instead)'
            )
    if node.get("additionalProperties") is False:
        for key in value:
            if key not in properties:
                errors.append(f"{where}.{key}: unknown field")
    for key, child in properties.items():
        if key in value:
            _check_value(schema, child, value[key], f"{where}.{key}", errors)


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for k, v in value.items() for s in (*_strings(k), *_strings(v))]
    if isinstance(value, list):
        return [s for item in value for s in _strings(item)]
    return []


def validate_state(state: Any, schema: dict[str, Any] | None = None) -> list[str]:
    """Return every problem found; an empty list means the state is valid."""
    schema = schema or load_schema()
    errors: list[str] = []
    if isinstance(state, dict):
        version = state.get("schema_version")
        if isinstance(version, int) and version not in SUPPORTED_SCHEMA_VERSIONS:
            return [
                (
                    f"$.schema_version: version {version} is not supported by this tool "
                    f"(supported: {SUPPORTED_SCHEMA_VERSIONS}); do not guess, use the matching bundle"
                )
            ]
    _check_object(schema, schema, state, "$", errors)
    for text in _strings(state):
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(
                    "secret-looking value found; remove passwords, tokens and keys from the state"
                )
                return errors
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "validate":
        print("usage: onboarding_state.py validate <state.json>", file=sys.stderr)
        return 2
    try:
        state = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"cannot read state: {error}", file=sys.stderr)
        return 2
    errors = validate_state(state)
    for error in errors:
        print(error)
    if not errors:
        print("state valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
