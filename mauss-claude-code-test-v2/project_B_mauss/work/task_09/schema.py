"""Schema definitions and supported types for the form validator."""

# Supported leaf types - mapping from schema type-name to allowed Python types.
# We deliberately keep these tight (no coercion). For "int", a Python bool is
# rejected because in Python bool is a subclass of int.
SUPPORTED_TYPES = {
    "string": (str,),
    "int": (int,),
    "float": (float,),
    "bool": (bool,),
    "list": (list,),
    "object": (dict,),
}


def is_valid_type(name: str) -> bool:
    """Return True if `name` names a supported schema type."""
    return name in SUPPORTED_TYPES


def python_types_for(name: str):
    """Return the tuple of acceptable Python types for the given schema type."""
    return SUPPORTED_TYPES[name]


def type_matches(value, type_name: str) -> bool:
    """Strict (no-coercion) type check.

    int does not accept bool (since bool is a subclass of int).
    float does not accept int (we want explicit floats).
    """
    if type_name == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "float":
        return isinstance(value, float) and not isinstance(value, bool)
    if type_name == "bool":
        return isinstance(value, bool)
    if type_name == "string":
        return isinstance(value, str)
    if type_name == "list":
        return isinstance(value, list)
    if type_name == "object":
        return isinstance(value, dict)
    return False
