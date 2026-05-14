"""Schema definition helpers.

A schema is a Python dict describing the shape of expected data. Supported
type keywords are: ``"string"``, ``"int"``, ``"float"``, ``"bool"``,
``"list"`` (with ``items``) and ``"object"`` (with ``properties``).

Common per-field keys:
    - ``type``: required type name (string)
    - ``required``: bool, defaults to True
    - ``min`` / ``max``: bounds for numbers, list length, or string length
    - ``regex``: regex pattern that string values must match
    - ``validator``: callable -> bool for custom per-field validation
    - ``validator_message``: error message used when ``validator`` returns False
    - ``items``: schema for list elements
    - ``properties``: dict of nested field schemas for objects
    - ``constraints``: list of callables(obj) -> bool for cross-field rules
    - ``constraint_messages``: list of error messages parallel to ``constraints``
"""

from errors import SchemaError

PRIMITIVE_TYPES = {"string", "int", "float", "bool"}
COMPOUND_TYPES = {"list", "object"}
VALID_TYPES = PRIMITIVE_TYPES | COMPOUND_TYPES


def validate_schema(schema: dict, path: str = "") -> None:
    """Recursively validate that *schema* itself is well-formed.

    Raises :class:`SchemaError` if the schema is malformed.
    """

    if not isinstance(schema, dict):
        raise SchemaError(f"Schema at {path or '<root>'} must be a dict")

    type_name = schema.get("type")
    if type_name is None:
        raise SchemaError(f"Schema at {path or '<root>'} is missing 'type'")
    if type_name not in VALID_TYPES:
        raise SchemaError(
            f"Schema at {path or '<root>'} has unknown type {type_name!r}"
        )

    if type_name == "object":
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            raise SchemaError(
                f"Schema at {path or '<root>'} 'properties' must be a dict"
            )
        for key, sub in properties.items():
            sub_path = f"{path}.{key}" if path else key
            validate_schema(sub, sub_path)
        constraints = schema.get("constraints", [])
        if not isinstance(constraints, (list, tuple)):
            raise SchemaError(
                f"Schema at {path or '<root>'} 'constraints' must be a list"
            )
        for c in constraints:
            if not callable(c):
                raise SchemaError(
                    f"Schema at {path or '<root>'} has non-callable constraint"
                )

    if type_name == "list":
        items = schema.get("items")
        if items is None:
            raise SchemaError(
                f"Schema at {path or '<root>'} (list) is missing 'items'"
            )
        validate_schema(items, f"{path}[]" if path else "[]")

    validator = schema.get("validator")
    if validator is not None and not callable(validator):
        raise SchemaError(
            f"Schema at {path or '<root>'} 'validator' must be callable"
        )


def field(type_name: str, **kwargs) -> dict:
    """Convenience builder for a single field schema."""

    schema = {"type": type_name}
    schema.update(kwargs)
    return schema


def obj(properties: dict, **kwargs) -> dict:
    """Convenience builder for an object schema."""

    schema = {"type": "object", "properties": properties}
    schema.update(kwargs)
    return schema


def list_of(items: dict, **kwargs) -> dict:
    """Convenience builder for a list schema."""

    schema = {"type": "list", "items": items}
    schema.update(kwargs)
    return schema
