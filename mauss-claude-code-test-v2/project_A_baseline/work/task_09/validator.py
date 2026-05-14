"""Schema-driven validator.

Usage::

    v = Validator(schema)
    is_valid, errors = v.validate(data)
"""

import re
from typing import Any, List, Tuple

from errors import ValidationError
from schema import validate_schema


_SENTINEL = object()


class Validator:
    """Validates data against a declarative schema.

    The validator aggregates all errors instead of stopping at the first
    failure. Each error has a dotted ``path`` (``user.address.zip``) and
    a human readable ``message``.
    """

    def __init__(self, schema: dict, *, validate_schema_on_init: bool = True):
        self.schema = schema
        if validate_schema_on_init:
            validate_schema(schema)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def validate(self, data: Any) -> Tuple[bool, List[ValidationError]]:
        errors: List[ValidationError] = []
        self._validate(data, self.schema, path="", errors=errors)
        return (len(errors) == 0, errors)

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------
    def _validate(
        self,
        value: Any,
        schema: dict,
        path: str,
        errors: List[ValidationError],
    ) -> None:
        type_name = schema.get("type")

        if type_name == "object":
            self._validate_object(value, schema, path, errors)
        elif type_name == "list":
            self._validate_list(value, schema, path, errors)
        elif type_name in {"string", "int", "float", "bool"}:
            self._validate_primitive(value, schema, path, errors)
        else:  # pragma: no cover - schema is pre-validated
            errors.append(ValidationError(path, f"unknown type: {type_name}"))

    # ------------------------------------------------------------------
    # Object handling
    # ------------------------------------------------------------------
    def _validate_object(
        self,
        value: Any,
        schema: dict,
        path: str,
        errors: List[ValidationError],
    ) -> None:
        if not isinstance(value, dict):
            errors.append(
                ValidationError(
                    path or "<root>",
                    f"expected object, got {type(value).__name__}",
                )
            )
            return

        properties = schema.get("properties", {})

        # Check each declared property
        for key, sub_schema in properties.items():
            sub_path = f"{path}.{key}" if path else key
            present = key in value
            required = sub_schema.get("required", True)
            if not present:
                if required:
                    errors.append(
                        ValidationError(sub_path, f"missing required field: {key}")
                    )
                continue
            self._validate(value[key], sub_schema, sub_path, errors)

        # Cross-field constraints
        constraints = schema.get("constraints", [])
        messages = schema.get("constraint_messages", [])
        for idx, constraint in enumerate(constraints):
            try:
                ok = bool(constraint(value))
            except Exception as exc:
                ok = False
                default_msg = f"constraint raised {type(exc).__name__}: {exc}"
            else:
                default_msg = "cross-field constraint failed"
            if not ok:
                msg = (
                    messages[idx]
                    if idx < len(messages) and messages[idx]
                    else default_msg
                )
                errors.append(ValidationError(path or "<root>", msg))

    # ------------------------------------------------------------------
    # List handling
    # ------------------------------------------------------------------
    def _validate_list(
        self,
        value: Any,
        schema: dict,
        path: str,
        errors: List[ValidationError],
    ) -> None:
        # Reject non-list types (and explicitly reject strings, which are iterable)
        if not isinstance(value, list):
            errors.append(
                ValidationError(
                    path or "<root>",
                    f"expected list, got {type(value).__name__}",
                )
            )
            return

        # Length bounds
        min_len = schema.get("min")
        max_len = schema.get("max")
        if min_len is not None and len(value) < min_len:
            errors.append(
                ValidationError(
                    path or "<root>",
                    f"list length {len(value)} < min {min_len}",
                )
            )
        if max_len is not None and len(value) > max_len:
            errors.append(
                ValidationError(
                    path or "<root>",
                    f"list length {len(value)} > max {max_len}",
                )
            )

        item_schema = schema["items"]
        for i, item in enumerate(value):
            sub_path = f"{path}[{i}]" if path else f"[{i}]"
            self._validate(item, item_schema, sub_path, errors)

    # ------------------------------------------------------------------
    # Primitive handling
    # ------------------------------------------------------------------
    def _validate_primitive(
        self,
        value: Any,
        schema: dict,
        path: str,
        errors: List[ValidationError],
    ) -> None:
        type_name = schema["type"]
        location = path or "<root>"

        # Strict type checks: NO coercion -- int does not accept "5",
        # and bools do not satisfy int/float (despite being subclasses).
        if type_name == "string":
            if not isinstance(value, str):
                errors.append(
                    ValidationError(
                        location,
                        f"expected string, got {type(value).__name__}",
                    )
                )
                return
        elif type_name == "int":
            if isinstance(value, bool) or not isinstance(value, int):
                errors.append(
                    ValidationError(
                        location,
                        f"expected int, got {type(value).__name__}",
                    )
                )
                return
        elif type_name == "float":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                # Accept ints transparently as floats? Spec says distinct types.
                # We accept only float instances.
                if not isinstance(value, float):
                    errors.append(
                        ValidationError(
                            location,
                            f"expected float, got {type(value).__name__}",
                        )
                    )
                    return
            elif not isinstance(value, float):
                errors.append(
                    ValidationError(
                        location,
                        f"expected float, got {type(value).__name__}",
                    )
                )
                return
        elif type_name == "bool":
            if not isinstance(value, bool):
                errors.append(
                    ValidationError(
                        location,
                        f"expected bool, got {type(value).__name__}",
                    )
                )
                return

        # min/max for numbers and strings
        min_v = schema.get("min")
        max_v = schema.get("max")
        if type_name == "string":
            if min_v is not None and len(value) < min_v:
                errors.append(
                    ValidationError(
                        location,
                        f"string length {len(value)} < min {min_v}",
                    )
                )
            if max_v is not None and len(value) > max_v:
                errors.append(
                    ValidationError(
                        location,
                        f"string length {len(value)} > max {max_v}",
                    )
                )
        elif type_name in {"int", "float"}:
            if min_v is not None and value < min_v:
                errors.append(
                    ValidationError(location, f"value {value} < min {min_v}")
                )
            if max_v is not None and value > max_v:
                errors.append(
                    ValidationError(location, f"value {value} > max {max_v}")
                )

        # Regex on strings
        if type_name == "string":
            pattern = schema.get("regex")
            if pattern is not None and not re.search(pattern, value):
                errors.append(
                    ValidationError(
                        location, f"value does not match regex {pattern!r}"
                    )
                )

        # Custom per-field validator
        validator = schema.get("validator")
        if validator is not None:
            try:
                ok = bool(validator(value))
            except Exception as exc:
                ok = False
                default_msg = (
                    f"validator raised {type(exc).__name__}: {exc}"
                )
            else:
                default_msg = "value failed custom validator"
            if not ok:
                msg = schema.get("validator_message", default_msg)
                errors.append(ValidationError(location, msg))
