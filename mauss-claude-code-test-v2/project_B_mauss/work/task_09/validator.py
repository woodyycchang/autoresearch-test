"""Form validator: walks a JSON-schema-like spec and aggregates errors."""

from __future__ import annotations

import re
from typing import Any, List, Tuple

from errors import ValidationError, SchemaError
from schema import is_valid_type, type_matches


_SENTINEL_MISSING = object()


class Validator:
    """Walk `schema` against `data` and aggregate every error encountered."""

    def __init__(self, schema: dict):
        if not isinstance(schema, dict):
            raise SchemaError("Top-level schema must be a dict")
        self.schema = schema

    def validate(self, data: Any) -> Tuple[bool, List[ValidationError]]:
        errors: List[ValidationError] = []
        self._walk(self.schema, data, path="", errors=errors)
        return (len(errors) == 0, errors)

    # ------------------------------------------------------------------ walk

    def _walk(self, schema: dict, value: Any, path: str, errors: List[ValidationError]) -> None:
        type_name = schema.get("type")
        if type_name is None or not is_valid_type(type_name):
            raise SchemaError(f"Invalid or missing 'type' at schema path {path!r}: {type_name!r}")

        # 1. type check
        if not type_matches(value, type_name):
            errors.append(ValidationError(
                path=path or "<root>",
                message=f"expected type {type_name}, got {self._py_type_name(value)}",
            ))
            # If the type is wrong, deeper structural checks would produce
            # noisy/incorrect errors -- bail out for this subtree, but the
            # caller continues with sibling fields (aggregate semantics).
            return

        # 2. leaf-specific constraint checks
        if type_name == "string":
            self._check_string(schema, value, path, errors)
        elif type_name in ("int", "float"):
            self._check_number(schema, value, path, errors)
        elif type_name == "list":
            self._check_list(schema, value, path, errors)
        elif type_name == "object":
            self._check_object(schema, value, path, errors)

        # 3. custom field-level validator (applies after the type/structure is OK)
        custom = schema.get("validator")
        if custom is not None:
            try:
                ok = custom(value)
            except Exception as exc:
                ok = False
                msg = schema.get("validator_message", f"custom validator raised {exc!r}")
                errors.append(ValidationError(path or "<root>", msg))
                return
            if not ok:
                msg = schema.get("validator_message", "failed custom validator")
                errors.append(ValidationError(path or "<root>", msg))

    # ------------------------------------------------------------------ leaves

    def _check_string(self, schema, value, path, errors):
        if "min" in schema and len(value) < schema["min"]:
            errors.append(ValidationError(
                path or "<root>",
                f"string shorter than min length {schema['min']}",
            ))
        if "max" in schema and len(value) > schema["max"]:
            errors.append(ValidationError(
                path or "<root>",
                f"string longer than max length {schema['max']}",
            ))
        if "regex" in schema:
            pattern = schema["regex"]
            if not re.search(pattern, value):
                errors.append(ValidationError(
                    path or "<root>",
                    f"string does not match regex {pattern!r}",
                ))

    def _check_number(self, schema, value, path, errors):
        if "min" in schema and value < schema["min"]:
            errors.append(ValidationError(
                path or "<root>",
                f"value {value} is below min {schema['min']}",
            ))
        if "max" in schema and value > schema["max"]:
            errors.append(ValidationError(
                path or "<root>",
                f"value {value} is above max {schema['max']}",
            ))

    def _check_list(self, schema, value, path, errors):
        if "min" in schema and len(value) < schema["min"]:
            errors.append(ValidationError(
                path or "<root>",
                f"list shorter than min length {schema['min']}",
            ))
        if "max" in schema and len(value) > schema["max"]:
            errors.append(ValidationError(
                path or "<root>",
                f"list longer than max length {schema['max']}",
            ))
        item_schema = schema.get("items")
        if item_schema is not None:
            for i, item in enumerate(value):
                child_path = f"{path}[{i}]" if path else f"[{i}]"
                self._walk(item_schema, item, child_path, errors)

    def _check_object(self, schema, value, path, errors):
        fields = schema.get("fields", {}) or {}
        required = set(schema.get("required", []) or [])
        # validate declared fields
        for field_name, field_schema in fields.items():
            child_path = f"{path}.{field_name}" if path else field_name
            child_value = value.get(field_name, _SENTINEL_MISSING)
            if child_value is _SENTINEL_MISSING:
                if field_name in required:
                    errors.append(ValidationError(
                        child_path,
                        "required field missing",
                    ))
                # not required + missing -> silently ok
                continue
            self._walk(field_schema, child_value, child_path, errors)

        # cross-field / object-level constraints, evaluated only if every
        # required field is present *and* well-typed; otherwise these constraints
        # would explode with KeyError.
        constraints = schema.get("constraints", []) or []
        if constraints and self._object_is_safe_for_constraints(value, fields, required, errors, path):
            for idx, fn in enumerate(constraints):
                try:
                    ok = fn(value)
                except Exception as exc:
                    ok = False
                    msg = self._constraint_message(schema, idx, default=f"constraint raised {exc!r}")
                    errors.append(ValidationError(path or "<root>", msg))
                    continue
                if not ok:
                    msg = self._constraint_message(schema, idx, default="failed cross-field constraint")
                    errors.append(ValidationError(path or "<root>", msg))

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _constraint_message(schema, idx, default):
        msgs = schema.get("constraint_messages") or []
        if 0 <= idx < len(msgs):
            return msgs[idx]
        return default

    @staticmethod
    def _object_is_safe_for_constraints(value, fields, required, errors, path) -> bool:
        # only run cross-field if no error has been added for *this* object
        # AND every required field is present in the data.
        prefix = (path + ".") if path else ""
        for err in errors:
            if err.path.startswith(prefix) and "." not in err.path[len(prefix):]:
                # a direct-child error - skip cross-field
                return False
        for r in required:
            if r not in value:
                return False
        return True

    @staticmethod
    def _py_type_name(value) -> str:
        if isinstance(value, bool):
            return "bool"
        return type(value).__name__
