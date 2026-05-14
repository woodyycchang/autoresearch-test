"""Tests for the minimal JSON parser in solution.py."""

import pytest

from solution import parse


# ---- primitives ----
def test_parse_true():
    assert parse("true") is True


def test_parse_false():
    assert parse("false") is False


def test_parse_null():
    assert parse("null") is None


def test_parse_integer():
    assert parse("42") == 42
    assert isinstance(parse("42"), int)


def test_parse_negative_integer():
    assert parse("-7") == -7


def test_parse_zero():
    assert parse("0") == 0


def test_parse_float():
    assert parse("3.14") == 3.14
    assert isinstance(parse("3.14"), float)


def test_parse_negative_float():
    assert parse("-0.5") == -0.5


def test_parse_exponent():
    assert parse("1e3") == 1000.0
    assert parse("2.5E-2") == 0.025


# ---- strings ----
def test_parse_simple_string():
    assert parse('"hello"') == "hello"


def test_parse_empty_string():
    assert parse('""') == ""


def test_parse_string_with_escaped_quote():
    assert parse(r'"a\"b"') == 'a"b'


def test_parse_string_with_backslash():
    assert parse(r'"a\\b"') == "a\\b"


def test_parse_string_with_newline_tab():
    assert parse(r'"line1\nline2\tend"') == "line1\nline2\tend"


def test_parse_string_with_unicode_escape():
    assert parse(r'"A"') == "A"


def test_parse_string_with_slash_escape():
    assert parse(r'"\/"') == "/"


# ---- arrays ----
def test_parse_empty_array():
    assert parse("[]") == []


def test_parse_flat_array():
    assert parse("[1, 2, 3]") == [1, 2, 3]


def test_parse_mixed_array():
    assert parse('[1, "two", true, null, 3.0]') == [1, "two", True, None, 3.0]


def test_parse_nested_array():
    assert parse("[[1, 2], [3, [4, 5]]]") == [[1, 2], [3, [4, 5]]]


# ---- objects ----
def test_parse_empty_object():
    assert parse("{}") == {}


def test_parse_simple_object():
    assert parse('{"a": 1, "b": 2}') == {"a": 1, "b": 2}


def test_parse_nested_object():
    src = '{"x": {"y": {"z": [1, 2, {"deep": true}]}}}'
    assert parse(src) == {"x": {"y": {"z": [1, 2, {"deep": True}]}}}


def test_parse_object_with_all_value_types():
    src = '{"a": 1, "b": "s", "c": true, "d": false, "e": null, "f": [1, 2], "g": {"h": 3.5}}'
    assert parse(src) == {
        "a": 1,
        "b": "s",
        "c": True,
        "d": False,
        "e": None,
        "f": [1, 2],
        "g": {"h": 3.5},
    }


# ---- whitespace handling ----
def test_parse_with_whitespace():
    assert parse('  {\n  "a" : 1 ,\n  "b" : 2\n}  ') == {"a": 1, "b": 2}


def test_parse_array_with_whitespace():
    assert parse("[ 1 , 2 , 3 ]") == [1, 2, 3]


# ---- error cases ----
@pytest.mark.parametrize(
    "bad",
    [
        "",                # empty
        "   ",             # whitespace only
        "{",               # unterminated object
        "}",               # stray close
        "[",               # unterminated array
        "]",               # stray close
        '{"a": 1,}',       # trailing comma in object
        "[1, 2,]",         # trailing comma in array
        "{'a': 1}",        # single quotes
        '{"a" 1}',         # missing colon
        '{"a": 1 "b": 2}', # missing comma
        "01",              # leading zero
        "1.",              # trailing dot
        ".5",              # missing leading digit
        "1e",              # bad exponent
        "-",               # lone minus
        "tru",             # incomplete literal
        "nul",             # incomplete null
        "False",           # wrong case
        '"unterminated',   # unterminated string
        '"\\q"',           # invalid escape
        '"\\u00"',         # short unicode escape
        '{"a": 1} extra',  # trailing junk
        "[1, 2",           # unterminated array
        '{"a"}',           # key without value
    ],
)
def test_invalid_json_raises_value_error(bad):
    with pytest.raises(ValueError):
        parse(bad)


def test_control_character_in_string_rejected():
    with pytest.raises(ValueError):
        parse('"a\nb"')  # literal newline inside string is invalid


def test_non_string_input_raises():
    with pytest.raises(ValueError):
        parse(123)  # type: ignore[arg-type]


# ---- round-trip-ish sanity ----
def test_complex_document():
    src = """
    {
      "name": "ada",
      "age": 36,
      "alive": false,
      "kids": null,
      "scores": [10, 9.5, -1, 2e2],
      "meta": {"tags": ["math", "logic"], "note": "line1\\nline2"}
    }
    """
    expected = {
        "name": "ada",
        "age": 36,
        "alive": False,
        "kids": None,
        "scores": [10, 9.5, -1, 200.0],
        "meta": {"tags": ["math", "logic"], "note": "line1\nline2"},
    }
    assert parse(src) == expected
