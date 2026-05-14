"""Tests for the JSON-schema-like form validator."""

import re

import pytest

from validator import Validator
from errors import ValidationError, SchemaError


# ----------------------------------------------------------------- happy path

def test_happy_path_flat_object():
    schema = {
        "type": "object",
        "required": ["name", "age"],
        "fields": {
            "name": {"type": "string", "min": 1, "max": 30},
            "age": {"type": "int", "min": 0, "max": 150},
        },
    }
    ok, errs = Validator(schema).validate({"name": "Ada", "age": 36})
    assert ok is True
    assert errs == []


def test_happy_path_nested_object():
    schema = {
        "type": "object",
        "required": ["user"],
        "fields": {
            "user": {
                "type": "object",
                "required": ["address"],
                "fields": {
                    "address": {
                        "type": "object",
                        "required": ["zip"],
                        "fields": {
                            "zip": {"type": "string", "regex": r"^\d{5}$"},
                        },
                    },
                },
            },
        },
    }
    ok, errs = Validator(schema).validate(
        {"user": {"address": {"zip": "94110"}}}
    )
    assert ok is True
    assert errs == []


# ----------------------------------------------------------------- required

def test_missing_required_top_level():
    schema = {
        "type": "object",
        "required": ["name"],
        "fields": {"name": {"type": "string"}},
    }
    ok, errs = Validator(schema).validate({})
    assert ok is False
    assert len(errs) == 1
    assert errs[0].path == "name"
    assert "required" in errs[0].message.lower()


def test_optional_field_can_be_missing():
    schema = {
        "type": "object",
        "required": ["name"],
        "fields": {
            "name": {"type": "string"},
            "nickname": {"type": "string"},  # not required
        },
    }
    ok, errs = Validator(schema).validate({"name": "Ada"})
    assert ok is True
    assert errs == []


# ----------------------------------------------------------------- type mismatch

def test_type_mismatch_int_does_not_accept_string_five():
    """Failure mode: int accepts '5'.  We must reject it."""
    schema = {
        "type": "object",
        "required": ["age"],
        "fields": {"age": {"type": "int"}},
    }
    ok, errs = Validator(schema).validate({"age": "5"})
    assert ok is False
    assert len(errs) == 1
    assert errs[0].path == "age"
    assert "expected type int" in errs[0].message


def test_type_mismatch_string_does_not_accept_int():
    schema = {
        "type": "object",
        "required": ["name"],
        "fields": {"name": {"type": "string"}},
    }
    ok, errs = Validator(schema).validate({"name": 42})
    assert ok is False
    assert errs[0].path == "name"
    assert "expected type string" in errs[0].message


def test_int_rejects_bool():
    schema = {"type": "object", "fields": {"x": {"type": "int"}}, "required": ["x"]}
    ok, errs = Validator(schema).validate({"x": True})
    assert ok is False
    assert errs[0].path == "x"


def test_float_does_not_accept_int():
    schema = {"type": "object", "fields": {"r": {"type": "float"}}, "required": ["r"]}
    ok, errs = Validator(schema).validate({"r": 5})
    assert ok is False


def test_float_accepts_float():
    schema = {"type": "object", "fields": {"r": {"type": "float"}}, "required": ["r"]}
    ok, errs = Validator(schema).validate({"r": 5.0})
    assert ok is True


def test_bool_accepted():
    schema = {"type": "object", "fields": {"x": {"type": "bool"}}, "required": ["x"]}
    ok, _ = Validator(schema).validate({"x": False})
    assert ok is True


# ----------------------------------------------------------------- nested errors / paths

def test_nested_error_has_correct_path():
    schema = {
        "type": "object",
        "required": ["user"],
        "fields": {
            "user": {
                "type": "object",
                "required": ["address"],
                "fields": {
                    "address": {
                        "type": "object",
                        "required": ["zip"],
                        "fields": {
                            "zip": {"type": "string", "regex": r"^\d{5}$"},
                        },
                    },
                },
            },
        },
    }
    ok, errs = Validator(schema).validate(
        {"user": {"address": {"zip": "bad!"}}}
    )
    assert ok is False
    assert len(errs) == 1
    assert errs[0].path == "user.address.zip"
    assert "regex" in errs[0].message


def test_missing_required_in_nested_object_has_path():
    schema = {
        "type": "object",
        "required": ["user"],
        "fields": {
            "user": {
                "type": "object",
                "required": ["email"],
                "fields": {"email": {"type": "string"}},
            },
        },
    }
    ok, errs = Validator(schema).validate({"user": {}})
    assert ok is False
    assert any(e.path == "user.email" and "required" in e.message for e in errs)


# ----------------------------------------------------------------- list of X

def test_list_of_strings_happy():
    schema = {
        "type": "object",
        "required": ["tags"],
        "fields": {
            "tags": {"type": "list", "items": {"type": "string"}, "min": 1},
        },
    }
    ok, errs = Validator(schema).validate({"tags": ["a", "b"]})
    assert ok is True
    assert errs == []


def test_list_item_type_error_has_indexed_path():
    schema = {
        "type": "object",
        "required": ["tags"],
        "fields": {
            "tags": {"type": "list", "items": {"type": "string"}},
        },
    }
    ok, errs = Validator(schema).validate({"tags": ["a", 5, "c"]})
    assert ok is False
    assert len(errs) == 1
    assert errs[0].path == "tags[1]"
    assert "expected type string" in errs[0].message


def test_list_of_objects():
    schema = {
        "type": "object",
        "required": ["items"],
        "fields": {
            "items": {
                "type": "list",
                "items": {
                    "type": "object",
                    "required": ["id"],
                    "fields": {"id": {"type": "int"}},
                },
            },
        },
    }
    ok, errs = Validator(schema).validate({"items": [{"id": 1}, {"id": "bad"}]})
    assert ok is False
    assert any(e.path == "items[1].id" for e in errs)


def test_list_min_max():
    schema = {"type": "list", "items": {"type": "int"}, "min": 2, "max": 3}
    ok, errs = Validator(schema).validate([1])
    assert ok is False
    assert "min" in errs[0].message
    ok, errs = Validator(schema).validate([1, 2, 3, 4])
    assert ok is False
    assert "max" in errs[0].message


# ----------------------------------------------------------------- string min/max/regex

def test_string_min_violation():
    schema = {"type": "object", "fields": {"s": {"type": "string", "min": 3}}, "required": ["s"]}
    ok, errs = Validator(schema).validate({"s": "ab"})
    assert ok is False
    assert errs[0].path == "s"


def test_string_max_violation():
    schema = {"type": "object", "fields": {"s": {"type": "string", "max": 3}}, "required": ["s"]}
    ok, errs = Validator(schema).validate({"s": "abcd"})
    assert ok is False


def test_string_regex_violation():
    schema = {"type": "object", "fields": {"e": {"type": "string", "regex": r"^[^@]+@[^@]+$"}}, "required": ["e"]}
    ok, errs = Validator(schema).validate({"e": "not-an-email"})
    assert ok is False
    assert "regex" in errs[0].message


# ----------------------------------------------------------------- int/float min/max

def test_int_min_max():
    schema = {"type": "object", "fields": {"n": {"type": "int", "min": 1, "max": 10}}, "required": ["n"]}
    ok, _ = Validator(schema).validate({"n": 0})
    assert ok is False
    ok, _ = Validator(schema).validate({"n": 11})
    assert ok is False
    ok, _ = Validator(schema).validate({"n": 5})
    assert ok is True


# ----------------------------------------------------------------- custom validator

def test_custom_validator_lowercase():
    schema = {
        "type": "object",
        "required": ["slug"],
        "fields": {
            "slug": {
                "type": "string",
                "validator": lambda s: s == s.lower(),
                "validator_message": "slug must be lowercase",
            },
        },
    }
    ok, errs = Validator(schema).validate({"slug": "Hello"})
    assert ok is False
    assert errs[0].path == "slug"
    assert errs[0].message == "slug must be lowercase"

    ok, errs = Validator(schema).validate({"slug": "hello"})
    assert ok is True
    assert errs == []


def test_custom_validator_raises_is_caught():
    schema = {
        "type": "object",
        "required": ["x"],
        "fields": {
            "x": {
                "type": "string",
                "validator": lambda s: 1 / 0,  # always raises
                "validator_message": "boom",
            },
        },
    }
    ok, errs = Validator(schema).validate({"x": "anything"})
    assert ok is False
    assert errs[0].path == "x"


# ----------------------------------------------------------------- cross-field constraints

def test_cross_field_start_lt_end_passes():
    schema = {
        "type": "object",
        "required": ["start", "end"],
        "fields": {
            "start": {"type": "int"},
            "end": {"type": "int"},
        },
        "constraints": [lambda obj: obj["start"] < obj["end"]],
        "constraint_messages": ["start must be < end"],
    }
    ok, errs = Validator(schema).validate({"start": 1, "end": 2})
    assert ok is True


def test_cross_field_start_lt_end_fails():
    schema = {
        "type": "object",
        "required": ["start", "end"],
        "fields": {
            "start": {"type": "int"},
            "end": {"type": "int"},
        },
        "constraints": [lambda obj: obj["start"] < obj["end"]],
        "constraint_messages": ["start must be < end"],
    }
    ok, errs = Validator(schema).validate({"start": 5, "end": 2})
    assert ok is False
    assert any(e.message == "start must be < end" for e in errs)


def test_cross_field_skipped_if_required_missing():
    """If a required field is missing, the cross-field check should NOT fire
    with a KeyError-flavored error -- we should see the 'required' error only."""
    schema = {
        "type": "object",
        "required": ["start", "end"],
        "fields": {
            "start": {"type": "int"},
            "end": {"type": "int"},
        },
        "constraints": [lambda obj: obj["start"] < obj["end"]],
        "constraint_messages": ["start must be < end"],
    }
    ok, errs = Validator(schema).validate({"start": 5})
    assert ok is False
    paths = [e.path for e in errs]
    assert "end" in paths
    # the constraint must not raise / produce an error here
    assert all(e.message != "start must be < end" for e in errs)


# ----------------------------------------------------------------- aggregate semantics

def test_errors_aggregate_does_not_stop_at_first():
    """Failure mode: 'aggregate errors stop at first'.  We must collect them all."""
    schema = {
        "type": "object",
        "required": ["a", "b", "c"],
        "fields": {
            "a": {"type": "int"},
            "b": {"type": "string"},
            "c": {"type": "bool"},
        },
    }
    ok, errs = Validator(schema).validate({"a": "x", "b": 1, "c": "no"})
    assert ok is False
    assert len(errs) == 3
    paths = {e.path for e in errs}
    assert paths == {"a", "b", "c"}


def test_errors_aggregate_mix_of_failures():
    schema = {
        "type": "object",
        "required": ["name", "tags"],
        "fields": {
            "name": {"type": "string", "min": 3},
            "tags": {"type": "list", "items": {"type": "string"}},
        },
    }
    ok, errs = Validator(schema).validate({"name": "ab", "tags": ["ok", 7]})
    assert ok is False
    paths = {e.path for e in errs}
    assert "name" in paths
    assert "tags[1]" in paths


# ----------------------------------------------------------------- schema errors

def test_schema_with_unknown_type_raises():
    schema = {"type": "object", "fields": {"x": {"type": "nope"}}, "required": ["x"]}
    with pytest.raises(SchemaError):
        Validator(schema).validate({"x": 1})


def test_top_level_non_dict_schema_raises():
    with pytest.raises(SchemaError):
        Validator("not a schema")


# ----------------------------------------------------------------- ValidationError shape

def test_validation_error_has_path_and_message():
    err = ValidationError("user.name", "required")
    assert err.path == "user.name"
    assert err.message == "required"
    assert err.to_dict() == {"path": "user.name", "message": "required"}
