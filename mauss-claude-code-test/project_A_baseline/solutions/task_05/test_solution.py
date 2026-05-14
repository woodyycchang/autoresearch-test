"""Tests for the calculator solution."""

import math

import pytest

from solution import CalculatorError, evaluate


class TestBasicArithmetic:
    def test_single_integer(self):
        assert evaluate("42") == 42

    def test_single_float(self):
        assert evaluate("3.14") == 3.14

    def test_addition(self):
        assert evaluate("1 + 2") == 3

    def test_subtraction(self):
        assert evaluate("10 - 4") == 6

    def test_multiplication(self):
        assert evaluate("6 * 7") == 42

    def test_division(self):
        assert evaluate("20 / 4") == 5.0

    def test_float_arithmetic(self):
        assert evaluate("1.5 + 2.5") == 4.0


class TestPrecedence:
    def test_mul_before_add(self):
        assert evaluate("3 + 4 * 2") == 11

    def test_div_before_sub(self):
        assert evaluate("10 - 6 / 2") == 7.0

    def test_left_to_right_same_precedence(self):
        assert evaluate("10 - 3 - 2") == 5
        assert evaluate("20 / 4 / 5") == 1.0

    def test_complex_expression(self):
        assert evaluate("3 + 4 * 2 - (1 + 1)") == 9


class TestParentheses:
    def test_simple_parens(self):
        assert evaluate("(1 + 2) * 3") == 9

    def test_nested_parens(self):
        assert evaluate("((1 + 2) * (3 + 4))") == 21

    def test_deeply_nested(self):
        assert evaluate("(((((5)))))") == 5

    def test_parens_override_precedence(self):
        assert evaluate("(3 + 4) * 2") == 14


class TestUnary:
    def test_unary_minus(self):
        assert evaluate("-5") == -5

    def test_unary_plus(self):
        assert evaluate("+5") == 5

    def test_unary_minus_with_paren(self):
        assert evaluate("-(3 + 2)") == -5

    def test_double_negation(self):
        assert evaluate("--5") == 5

    def test_negative_in_expression(self):
        assert evaluate("3 + -2") == 1
        assert evaluate("3 * -2") == -6


class TestWhitespace:
    def test_no_spaces(self):
        assert evaluate("3+4*2") == 11

    def test_extra_spaces(self):
        assert evaluate("  3  +  4  ") == 7

    def test_tabs_and_spaces(self):
        assert evaluate("3\t+\t4") == 7


class TestFloatingPoint:
    def test_float_division(self):
        assert evaluate("1 / 2") == 0.5

    def test_float_precision(self):
        assert math.isclose(evaluate("0.1 + 0.2"), 0.3)

    def test_mixed_int_float(self):
        result = evaluate("2 * 3.5")
        assert result == 7.0


class TestErrors:
    def test_empty_string(self):
        with pytest.raises(CalculatorError):
            evaluate("")

    def test_whitespace_only(self):
        with pytest.raises(CalculatorError):
            evaluate("   ")

    def test_division_by_zero(self):
        with pytest.raises(CalculatorError):
            evaluate("5 / 0")

    def test_unmatched_open_paren(self):
        with pytest.raises(CalculatorError):
            evaluate("(1 + 2")

    def test_unmatched_close_paren(self):
        with pytest.raises(CalculatorError):
            evaluate("1 + 2)")

    def test_invalid_character(self):
        with pytest.raises(CalculatorError):
            evaluate("3 $ 4")

    def test_double_operator(self):
        with pytest.raises(CalculatorError):
            evaluate("3 * * 4")

    def test_trailing_operator(self):
        with pytest.raises(CalculatorError):
            evaluate("3 +")

    def test_invalid_number_two_dots(self):
        with pytest.raises(CalculatorError):
            evaluate("3.1.4")

    def test_non_string_input(self):
        with pytest.raises(CalculatorError):
            evaluate(123)  # type: ignore[arg-type]


class TestNoEvalUsed:
    def test_source_does_not_use_eval(self):
        import inspect

        import solution

        src = inspect.getsource(solution)
        # Strip docstrings/comments check: just ensure literal calls absent
        assert "eval(" not in src.replace("evaluate(", "")
        assert "exec(" not in src
