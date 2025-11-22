from __future__ import annotations

import importlib.util
from json import loads
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _has_jsonschema() -> bool:
    return importlib.util.find_spec("jsonschema") is not None


if _has_jsonschema():
    from jsonschema import Draft7Validator, exceptions
else:
    class _SimpleError:
        def __init__(self, path: List[str], message: str) -> None:
            self.path = path
            self.message = message

    class _SimpleDraft7Validator:
        def __init__(self, schema: Dict[str, Any]) -> None:
            self.schema = schema

        def iter_errors(self, payload: Dict[str, Any]) -> Iterable[_SimpleError]:
            if not isinstance(payload, dict):
                yield _SimpleError([], "Payload must be an object")
                return

            required_fields = self.schema.get("required", [])
            for field in required_fields:
                if field not in payload:
                    yield _SimpleError([field], "Missing required field")

            properties = self.schema.get("properties", {})
            for field, rules in properties.items():
                if field not in payload:
                    continue
                expected_type = rules.get("type")
                if expected_type == "string" and not isinstance(payload[field], str):
                    yield _SimpleError([field], "Expected a string")

            if not self.schema.get("additionalProperties", True):
                allowed = set(properties.keys())
                for field in payload.keys():
                    if field not in allowed:
                        yield _SimpleError([field], "Unexpected property")

    class exceptions:  # type: ignore[no-redef]
        class ValidationError(Exception):
            pass

    Draft7Validator = _SimpleDraft7Validator


class SchemaRegistry:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).parent
        self._validators: Dict[str, Draft7Validator] = {}

    def _load_schema(self, topic: str) -> Draft7Validator:
        if topic in self._validators:
            return self._validators[topic]

        schema_path = self.base_path / f"{topic}.schema.json"
        if not schema_path.exists():
            raise FileNotFoundError(f"No schema found for topic {topic} at {schema_path}")

        schema = loads(schema_path.read_text())
        if _has_jsonschema():  # pragma: no cover - passthrough when dependency available
            Draft7Validator.check_schema(schema)
        validator = Draft7Validator(schema)
        self._validators[topic] = validator
        return validator

    def validate(self, topic: str, payload: Dict[str, Any]) -> None:
        validator = self._load_schema(topic)
        errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            message = "; ".join([f"{'.'.join(map(str, err.path))}: {err.message}" for err in errors])
            raise exceptions.ValidationError(message)


def validate_message(topic: str, payload: Dict[str, Any]) -> None:
    registry = SchemaRegistry()
    registry.validate(topic, payload)
