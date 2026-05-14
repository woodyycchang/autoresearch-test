"""Calculator: evaluate arithmetic expressions without eval/exec.

Supports +, -, *, /, parentheses, integers, and floating-point numbers.
Uses a recursive-descent parser respecting operator precedence.
"""

from __future__ import annotations

from typing import List, Tuple, Union

Number = Union[int, float]
Token = Tuple[str, object]  # (kind, value)


class CalculatorError(ValueError):
    """Raised for any parse or evaluation error."""


def _tokenize(expression: str) -> List[Token]:
    """Convert input string into a list of (kind, value) tokens."""
    tokens: List[Token] = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "+-*/()":
            tokens.append((ch, ch))
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            dot_count = 0
            while j < n and (expression[j].isdigit() or expression[j] == "."):
                if expression[j] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise CalculatorError(
                            f"Invalid number with multiple dots at index {i}"
                        )
                j += 1
            num_str = expression[i:j]
            if num_str == ".":
                raise CalculatorError(f"Invalid number '.' at index {i}")
            value: Number
            if "." in num_str:
                value = float(num_str)
            else:
                value = int(num_str)
            tokens.append(("NUM", value))
            i = j
            continue
        raise CalculatorError(f"Unexpected character {ch!r} at index {i}")
    return tokens


class _Parser:
    """Recursive-descent parser.

    Grammar:
        expr   := term (('+' | '-') term)*
        term   := factor (('*' | '/') factor)*
        factor := ('+' | '-') factor | primary
        primary := NUM | '(' expr ')'
    """

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        if self.pos >= len(self.tokens):
            return ("EOF", None)
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self._peek()
        self.pos += 1
        return tok

    def parse(self) -> Number:
        value = self._parse_expr()
        if self.pos != len(self.tokens):
            kind, val = self._peek()
            raise CalculatorError(f"Unexpected token {val!r}")
        return value

    def _parse_expr(self) -> Number:
        value = self._parse_term()
        while self._peek()[0] in ("+", "-"):
            op = self._advance()[0]
            rhs = self._parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _parse_term(self) -> Number:
        value = self._parse_factor()
        while self._peek()[0] in ("*", "/"):
            op = self._advance()[0]
            rhs = self._parse_factor()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise CalculatorError("Division by zero")
                value = value / rhs
        return value

    def _parse_factor(self) -> Number:
        kind, _ = self._peek()
        if kind == "+":
            self._advance()
            return self._parse_factor()
        if kind == "-":
            self._advance()
            return -self._parse_factor()
        return self._parse_primary()

    def _parse_primary(self) -> Number:
        kind, value = self._peek()
        if kind == "NUM":
            self._advance()
            return value  # type: ignore[return-value]
        if kind == "(":
            self._advance()
            inner = self._parse_expr()
            close_kind, _ = self._peek()
            if close_kind != ")":
                raise CalculatorError("Missing closing parenthesis")
            self._advance()
            return inner
        if kind == "EOF":
            raise CalculatorError("Unexpected end of expression")
        raise CalculatorError(f"Unexpected token {value!r}")


def evaluate(expression: str) -> Number:
    """Evaluate an arithmetic expression and return the numeric result.

    Args:
        expression: Arithmetic expression string. Supports + - * / and ().

    Returns:
        int or float result.

    Raises:
        CalculatorError: on malformed input or division by zero.
    """
    if not isinstance(expression, str):
        raise CalculatorError("Expression must be a string")
    tokens = _tokenize(expression)
    if not tokens:
        raise CalculatorError("Empty expression")
    return _Parser(tokens).parse()
