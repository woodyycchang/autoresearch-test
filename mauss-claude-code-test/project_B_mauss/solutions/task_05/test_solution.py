"""Pytest suite for the calculator in solution.py."""

import math

import pytest

from solution import CalculatorError, evaluate


# --- Basic arithmetic --------------------------------------------------------


def test_single_number_int():
    assert evaluate("42") == 42


def test_single_number_float():
    assert evaluate("3.14") == pytest.approx(3.14)


def test_simple_addition():
    assert evaluate("1 + 2") == 3


def test_simple_subtraction():
    assert evaluate("10 - 4") == 6


def test_simple_multiplication():
    assert evaluate("6 * 7") == 42


def test_simple_division():
    assert evaluate("20 / 4") == 5


# --- Precedence and parentheses ---------------------------------------------


def test_task_example():
    # From the task description.
    assert evaluate("3 + 4 * 2 - (1 + 1)") == 9


def test_precedence_mul_before_add():
    assert evaluate("2 + 3 * 4") == 14


def test_precedence_div_before_sub():
    assert evaluate("20 - 8 / 2") == 16


def test_parentheses_override():
    assert evaluate("(2 + 3) * 4") == 20


def test_nested_parentheses():
    assert evaluate("((1 + 2) * (3 + 4))") == 21


def test_left_associativity_subtraction():
    # 10 - 5 - 2 == (10 - 5) - 2 == 3, not 10 - (5 - 2) == 7
    assert evaluate("10 - 5 - 2") == 3


def test_left_associativity_division():
    # 100 / 10 / 2 == (100 / 10) / 2 == 5.0
    assert evaluate("100 / 10 / 2") == pytest.approx(5.0)


# --- Floats ------------------------------------------------------------------


def test_float_addition():
    assert evaluate("1.5 + 2.25") == pytest.approx(3.75)


def test_mixed_int_float():
    assert evaluate("2 * 0.5") == pytest.approx(1.0)


def test_division_produces_float():
    result = evaluate("7 / 2")
    assert result == pytest.approx(3.5)


def test_leading_dot_float():
    assert evaluate(".5 + .25") == pytest.approx(0.75)


# --- Unary operators ---------------------------------------------------------


def test_unary_minus():
    assert evaluate("-5") == -5


def test_unary_plus():
    assert evaluate("+5") == 5


def test_unary_minus_in_expression():
    assert evaluate("3 + -2") == 1


def test_unary_minus_with_parens():
    assert evaluate("-(3 + 4)") == -7


def test_double_unary_minus():
    assert evaluate("--5") == 5


# --- Whitespace tolerance ----------------------------------------------------


def test_no_whitespace():
    assert evaluate("3+4*2-(1+1)") == 9


def test_extra_whitespace():
    assert evaluate("   3   +   4  ") == 7


def test_tabs_and_spaces():
    assert evaluate("\t3 +\t4\t") == 7


# --- Error handling ----------------------------------------------------------


def test_division_by_zero_raises():
    with pytest.raises(CalculatorError):
        evaluate("1 / 0")


def test_mismatched_open_paren():
    with pytest.raises(CalculatorError):
        evaluate("(1 + 2")


def test_mismatched_close_paren():
    with pytest.raises(CalculatorError):
        evaluate("1 + 2)")


def test_empty_expression():
    with pytest.raises(CalculatorError):
        evaluate("")


def test_whitespace_only():
    with pytest.raises(CalculatorError):
        evaluate("   ")


def test_invalid_character():
    with pytest.raises(CalculatorError):
        evaluate("3 + a")


def test_missing_operand():
    with pytest.raises(CalculatorError):
        evaluate("3 +")


def test_double_dot_number():
    with pytest.raises(CalculatorError):
        evaluate("1..2 + 3")


def test_non_string_input():
    with pytest.raises(CalculatorError):
        evaluate(123)  # type: ignore[arg-type]


# --- Sanity checks: result types --------------------------------------------


def test_int_only_stays_int():
    # All int operands with +, -, * keep integer result.
    result = evaluate("2 * 3 + 4")
    assert result == 10
    assert isinstance(result, int)


def test_division_returns_float_type():
    assert isinstance(evaluate("4 / 2"), float)


# --- A few more compound cases ----------------------------------------------


def test_complex_expression():
    # Cross-check against math: (1.5 + 2) * 4 - 6 / 3 = 14 - 2 = 12.0
    assert evaluate("(1.5 + 2) * 4 - 6 / 3") == pytest.approx(12.0)


def test_deeply_nested():
    assert evaluate("(((((1 + 2)))))") == 3


def test_unary_minus_after_operator():
    assert evaluate("2 * -3") == -6


def test_floating_point_precision():
    # Just ensure no exceptions and reasonable result.
    result = evaluate("0.1 + 0.2")
    assert math.isclose(result, 0.3, rel_tol=1e-9)
