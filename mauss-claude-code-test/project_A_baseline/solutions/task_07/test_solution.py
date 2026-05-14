"""Tests for the minimal JSON parser."""

import pytest

from solution import parse


# ---- primitive values ----------------------------------------------------
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
    assert parse("1e2") == 100.0
    assert parse("1.5E-2") == 0.015


# ---- strings -------------------------------------------------------------
def test_parse_simple_string():
    assert parse('"hello"') == "hello"


def test_parse_empty_string():
    assert parse('""') == ""


def test_parse_string_with_escapes():
    assert parse(r'"line1\nline2"') == "line1\nline2"
    assert parse(r'"a\tb"') == "a\tb"
    assert parse(r'"quote: \""') == 'quote: "'
    assert parse(r'"back: \\"') == "back: \\"


def test_parse_string_unicode_escape():
    assert parse(r'"A"') == "A"


# ---- arrays --------------------------------------------------------------
def test_parse_empty_array():
    assert parse("[]") == []


def test_parse_simple_array():
    assert parse("[1, 2, 3]") == [1, 2, 3]


def test_parse_mixed_array():
    assert parse('[1, "two", true, null, 3.0]') == [1, "two", True, None, 3.0]


def test_parse_nested_array():
    assert parse("[[1, 2], [3, [4, 5]]]") == [[1, 2], [3, [4, 5]]]


# ---- objects -------------------------------------------------------------
def test_parse_empty_object():
    assert parse("{}") == {}


def test_parse_simple_object():
    assert parse('{"a": 1, "b": 2}') == {"a": 1, "b": 2}


def test_parse_nested_object():
    assert parse('{"x": {"y": [1, 2]}, "z": null}') == {
        "x": {"y": [1, 2]},
        "z": None,
    }


def test_parse_object_with_string_values():
    assert parse('{"greeting": "hi\\nthere"}') == {"greeting": "hi\nthere"}


# ---- whitespace ----------------------------------------------------------
def test_whitespace_around_value():
    assert parse("   42  ") == 42
    assert parse("\n\t[ 1 , 2 ]\n") == [1, 2]
    assert parse('  { "k" : "v" }  ') == {"k": "v"}


# ---- error cases ---------------------------------------------------------
def test_unterminated_string():
    with pytest.raises(ValueError):
        parse('"abc')


def test_invalid_escape():
    with pytest.raises(ValueError):
        parse(r'"\x"')


def test_trailing_comma_array():
    with pytest.raises(ValueError):
        parse("[1, 2, ]")


def test_trailing_comma_object():
    with pytest.raises(ValueError):
        parse('{"a": 1,}')


def test_missing_value():
    with pytest.raises(ValueError):
        parse('{"a":}')


def test_missing_colon():
    with pytest.raises(ValueError):
        parse('{"a" 1}')


def test_extra_data():
    with pytest.raises(ValueError):
        parse("1 2")


def test_unquoted_key():
    with pytest.raises(ValueError):
        parse("{a: 1}")


def test_single_quotes_not_allowed():
    with pytest.raises(ValueError):
        parse("'hello'")


def test_empty_input():
    with pytest.raises(ValueError):
        parse("")


def test_invalid_number_leading_plus():
    with pytest.raises(ValueError):
        parse("+1")


def test_invalid_number_double_dot():
    with pytest.raises(ValueError):
        parse("1..2")


def test_bad_literal():
    with pytest.raises(ValueError):
        parse("tru")


def test_non_string_input():
    with pytest.raises(ValueError):
        parse(123)


def test_control_char_in_string():
    with pytest.raises(ValueError):
        parse('"bad\x01char"')
