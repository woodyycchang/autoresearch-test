"""Tests for the schema validator."""

import pytest

from errors import SchemaError, ValidationError
from schema import field, list_of, obj, validate_schema
from validator import Validator


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------
def test_happy_path_simple_object():
    schema = obj(
        {
            "name": field("string", min=1, max=50),
            "age": field("int", min=0, max=150),
            "active": field("bool"),
        }
    )
    is_valid, errors = Validator(schema).validate(
        {"name": "Alice", "age": 30, "active": True}
    )
    assert is_valid is True
    assert errors == []


def test_happy_path_deeply_nested():
    schema = obj(
        {
            "user": obj(
                {
                    "name": field("string"),
                    "address": obj(
                        {
                            "zip": field("string", regex=r"^\d{5}$"),
                            "city": field("string"),
                        }
                    ),
                }
            )
        }
    )
    data = {
        "user": {
            "name": "Bob",
            "address": {"zip": "94110", "city": "SF"},
        }
    }
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is True
    assert errors == []


def test_happy_path_list_of_objects():
    schema = obj(
        {
            "items": list_of(
                obj(
                    {
                        "sku": field("string"),
                        "qty": field("int", min=1),
                    }
                ),
                min=1,
            )
        }
    )
    data = {"items": [{"sku": "A1", "qty": 2}, {"sku": "B2", "qty": 5}]}
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is True
    assert errors == []


# ---------------------------------------------------------------------------
# Missing required
# ---------------------------------------------------------------------------
def test_missing_required_top_level():
    schema = obj({"name": field("string"), "age": field("int")})
    is_valid, errors = Validator(schema).validate({"name": "x"})
    assert is_valid is False
    paths = [e.path for e in errors]
    assert "age" in paths


def test_missing_required_nested_path():
    schema = obj(
        {
            "user": obj(
                {
                    "address": obj(
                        {
                            "zip": field("string"),
                            "city": field("string"),
                        }
                    )
                }
            )
        }
    )
    data = {"user": {"address": {"city": "SF"}}}
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is False
    paths = [e.path for e in errors]
    assert "user.address.zip" in paths


def test_optional_field_not_required():
    schema = obj(
        {
            "name": field("string"),
            "nickname": field("string", required=False),
        }
    )
    is_valid, errors = Validator(schema).validate({"name": "Alice"})
    assert is_valid is True
    assert errors == []


# ---------------------------------------------------------------------------
# Type mismatch
# ---------------------------------------------------------------------------
def test_type_mismatch_int_does_not_accept_string():
    schema = obj({"age": field("int")})
    is_valid, errors = Validator(schema).validate({"age": "30"})
    assert is_valid is False
    assert len(errors) == 1
    assert errors[0].path == "age"
    assert "int" in errors[0].message


def test_type_mismatch_int_does_not_accept_string_5():
    # Explicit regression test: int does not coerce "5"
    schema = field("int")
    is_valid, errors = Validator(schema).validate("5")
    assert is_valid is False
    assert any("int" in e.message for e in errors)


def test_type_mismatch_bool_not_int():
    schema = field("int")
    is_valid, errors = Validator(schema).validate(True)
    assert is_valid is False
    assert any("int" in e.message for e in errors)


def test_type_mismatch_string_not_list():
    schema = list_of(field("int"))
    is_valid, errors = Validator(schema).validate("abc")
    assert is_valid is False
    assert any("list" in e.message for e in errors)


def test_type_mismatch_object_not_dict():
    schema = obj({"name": field("string")})
    is_valid, errors = Validator(schema).validate([1, 2, 3])
    assert is_valid is False
    assert any("object" in e.message for e in errors)


# ---------------------------------------------------------------------------
# Nested errors with correct paths
# ---------------------------------------------------------------------------
def test_nested_error_path_object():
    schema = obj(
        {
            "user": obj(
                {
                    "address": obj(
                        {
                            "zip": field("string", regex=r"^\d{5}$"),
                        }
                    )
                }
            )
        }
    )
    data = {"user": {"address": {"zip": "abcde"}}}
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is False
    assert len(errors) == 1
    assert errors[0].path == "user.address.zip"


def test_nested_error_path_list_index():
    schema = list_of(field("int"))
    is_valid, errors = Validator(schema).validate([1, "two", 3, "four"])
    assert is_valid is False
    paths = sorted(e.path for e in errors)
    assert paths == ["[1]", "[3]"]


def test_nested_error_path_list_of_objects():
    schema = obj(
        {
            "items": list_of(
                obj({"name": field("string"), "qty": field("int")})
            )
        }
    )
    data = {
        "items": [
            {"name": "ok", "qty": 1},
            {"name": "bad", "qty": "two"},
            {"qty": 5},
        ]
    }
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is False
    paths = {e.path for e in errors}
    assert "items[1].qty" in paths
    assert "items[2].name" in paths


# ---------------------------------------------------------------------------
# Min/max and regex
# ---------------------------------------------------------------------------
def test_string_min_max():
    schema = field("string", min=3, max=5)
    too_short_valid, too_short_errs = Validator(schema).validate("ab")
    too_long_valid, too_long_errs = Validator(schema).validate("abcdef")
    just_right_valid, _ = Validator(schema).validate("abcd")
    assert too_short_valid is False
    assert too_long_valid is False
    assert just_right_valid is True
    assert any("min" in e.message for e in too_short_errs)
    assert any("max" in e.message for e in too_long_errs)


def test_int_min_max():
    schema = field("int", min=0, max=100)
    assert Validator(schema).validate(50)[0] is True
    assert Validator(schema).validate(-1)[0] is False
    assert Validator(schema).validate(101)[0] is False


def test_regex_validation():
    schema = field("string", regex=r"^[a-z]+$")
    assert Validator(schema).validate("hello")[0] is True
    is_valid, errors = Validator(schema).validate("Hello123")
    assert is_valid is False
    assert any("regex" in e.message for e in errors)


# ---------------------------------------------------------------------------
# Custom validators
# ---------------------------------------------------------------------------
def test_custom_validator_pass():
    schema = field("string", validator=lambda s: s == s.lower())
    assert Validator(schema).validate("hello")[0] is True


def test_custom_validator_fail_default_message():
    schema = field("string", validator=lambda s: s == s.lower())
    is_valid, errors = Validator(schema).validate("Hello")
    assert is_valid is False
    assert len(errors) == 1
    assert "custom validator" in errors[0].message


def test_custom_validator_fail_with_custom_message():
    schema = field(
        "string",
        validator=lambda s: s == s.lower(),
        validator_message="must be lowercase",
    )
    is_valid, errors = Validator(schema).validate("Hello")
    assert is_valid is False
    assert errors[0].message == "must be lowercase"


def test_custom_validator_raises_is_treated_as_failure():
    def bad_validator(s):
        raise ValueError("boom")

    schema = field("string", validator=bad_validator)
    is_valid, errors = Validator(schema).validate("anything")
    assert is_valid is False
    assert any("ValueError" in e.message or "boom" in e.message for e in errors)


# ---------------------------------------------------------------------------
# Cross-field constraints
# ---------------------------------------------------------------------------
def test_cross_field_constraint_pass():
    schema = obj(
        {"start": field("int"), "end": field("int")},
        constraints=[lambda o: o["start"] < o["end"]],
        constraint_messages=["start must be before end"],
    )
    is_valid, errors = Validator(schema).validate({"start": 1, "end": 10})
    assert is_valid is True
    assert errors == []


def test_cross_field_constraint_fail():
    schema = obj(
        {"start": field("int"), "end": field("int")},
        constraints=[lambda o: o["start"] < o["end"]],
        constraint_messages=["start must be before end"],
    )
    is_valid, errors = Validator(schema).validate({"start": 10, "end": 1})
    assert is_valid is False
    assert any(e.message == "start must be before end" for e in errors)


def test_cross_field_constraint_default_message():
    schema = obj(
        {"a": field("int"), "b": field("int")},
        constraints=[lambda o: o["a"] == o["b"]],
    )
    is_valid, errors = Validator(schema).validate({"a": 1, "b": 2})
    assert is_valid is False
    assert any("constraint" in e.message for e in errors)


def test_cross_field_constraint_multiple():
    schema = obj(
        {
            "pwd": field("string"),
            "confirm": field("string"),
            "age": field("int"),
        },
        constraints=[
            lambda o: o["pwd"] == o["confirm"],
            lambda o: o["age"] >= 18,
        ],
        constraint_messages=[
            "passwords must match",
            "must be 18+",
        ],
    )
    is_valid, errors = Validator(schema).validate(
        {"pwd": "a", "confirm": "b", "age": 12}
    )
    assert is_valid is False
    messages = [e.message for e in errors]
    assert "passwords must match" in messages
    assert "must be 18+" in messages


# ---------------------------------------------------------------------------
# Aggregation behaviour (failure mode: aggregate errors stop at first)
# ---------------------------------------------------------------------------
def test_errors_are_aggregated_not_short_circuited():
    schema = obj(
        {
            "name": field("string"),
            "age": field("int"),
            "email": field("string", regex=r".+@.+"),
        }
    )
    data = {"name": 1, "age": "young", "email": "no-at-sign"}
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is False
    paths = {e.path for e in errors}
    assert paths == {"name", "age", "email"}


def test_errors_aggregated_across_list_items():
    schema = list_of(field("int", min=0))
    is_valid, errors = Validator(schema).validate([1, -1, -2, 5, -3])
    assert is_valid is False
    bad_paths = sorted(e.path for e in errors)
    assert bad_paths == ["[1]", "[2]", "[4]"]


# ---------------------------------------------------------------------------
# Schema validation itself
# ---------------------------------------------------------------------------
def test_schema_error_on_unknown_type():
    with pytest.raises(SchemaError):
        Validator({"type": "elephant"})


def test_schema_error_on_missing_type():
    with pytest.raises(SchemaError):
        Validator({"properties": {}})


def test_schema_error_on_list_without_items():
    with pytest.raises(SchemaError):
        Validator({"type": "list"})


def test_schema_error_on_non_callable_validator():
    with pytest.raises(SchemaError):
        Validator({"type": "string", "validator": "not callable"})


# ---------------------------------------------------------------------------
# ValidationError object
# ---------------------------------------------------------------------------
def test_validation_error_equality_and_dict():
    e1 = ValidationError("a.b", "msg")
    e2 = ValidationError("a.b", "msg")
    e3 = ValidationError("a.b", "other")
    assert e1 == e2
    assert e1 != e3
    assert e1.to_dict() == {"path": "a.b", "message": "msg"}


# ---------------------------------------------------------------------------
# Combined / integration
# ---------------------------------------------------------------------------
def test_complex_schema_integration():
    schema = obj(
        {
            "user": obj(
                {
                    "name": field("string", min=1),
                    "email": field("string", regex=r".+@.+"),
                    "addresses": list_of(
                        obj(
                            {
                                "zip": field("string", regex=r"^\d{5}$"),
                                "city": field("string"),
                            }
                        ),
                        min=1,
                    ),
                }
            ),
            "range": obj(
                {"start": field("int"), "end": field("int")},
                constraints=[lambda o: o["start"] < o["end"]],
                constraint_messages=["start must be before end"],
            ),
        }
    )
    data = {
        "user": {
            "name": "",
            "email": "bademail",
            "addresses": [{"zip": "abc", "city": "SF"}],
        },
        "range": {"start": 5, "end": 1},
    }
    is_valid, errors = Validator(schema).validate(data)
    assert is_valid is False
    paths = {e.path for e in errors}
    assert "user.name" in paths
    assert "user.email" in paths
    assert "user.addresses[0].zip" in paths
    assert "range" in paths
