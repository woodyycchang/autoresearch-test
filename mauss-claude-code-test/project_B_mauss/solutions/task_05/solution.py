"""Calculator that evaluates arithmetic expressions without eval/exec.

Supports:
- Integer and floating-point numbers
- Operators: + - * /
- Parentheses for grouping
- Standard operator precedence (* / before + -)
- Unary minus and unary plus

Uses the shunting-yard algorithm to convert infix expressions to
postfix (RPN), then evaluates the RPN with a stack.
"""

from __future__ import annotations


class CalculatorError(ValueError):
    """Raised on malformed expressions or runtime errors (e.g. div by zero)."""


# --- Tokenizer ---------------------------------------------------------------

_OPERATORS = {"+", "-", "*", "/"}


def tokenize(expression: str):
    """Convert the input string to a list of tokens (numbers, ops, parens)."""
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            saw_dot = False
            while j < n and (expression[j].isdigit() or expression[j] == "."):
                if expression[j] == ".":
                    if saw_dot:
                        raise CalculatorError(
                            f"Invalid number with multiple dots at position {i}"
                        )
                    saw_dot = True
                j += 1
            num_str = expression[i:j]
            if num_str == ".":
                raise CalculatorError(f"Invalid number '.' at position {i}")
            # Use int when there's no decimal point, else float.
            num = float(num_str) if "." in num_str else int(num_str)
            tokens.append(("NUM", num))
            i = j
            continue
        if ch in _OPERATORS:
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch == "(" or ch == ")":
            tokens.append(("PAREN", ch))
            i += 1
            continue
        raise CalculatorError(f"Unexpected character {ch!r} at position {i}")
    return tokens


# --- Shunting-yard: infix -> postfix ----------------------------------------

_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3, "u+": 3}
_RIGHT_ASSOC = {"u-", "u+"}


def to_postfix(tokens):
    """Convert tokens (infix) to postfix using the shunting-yard algorithm.

    Handles unary +/- by detecting them from context: if a + or - appears at
    the start of the expression, after another operator, or after '(', it is
    unary; otherwise it is binary.
    """
    output = []
    op_stack = []
    prev_kind = None  # None | "NUM" | "OP" | "LPAREN" | "RPAREN"

    for kind, value in tokens:
        if kind == "NUM":
            output.append(("NUM", value))
            prev_kind = "NUM"
        elif kind == "OP":
            # Detect unary +/-.
            is_unary = (
                value in ("+", "-")
                and prev_kind in (None, "OP", "LPAREN")
            )
            op = ("u" + value) if is_unary else value
            while op_stack:
                top = op_stack[-1]
                if top == "(":
                    break
                if (
                    _PRECEDENCE[top] > _PRECEDENCE[op]
                    or (
                        _PRECEDENCE[top] == _PRECEDENCE[op]
                        and op not in _RIGHT_ASSOC
                    )
                ):
                    output.append(("OP", op_stack.pop()))
                else:
                    break
            op_stack.append(op)
            prev_kind = "OP"
        elif kind == "PAREN" and value == "(":
            op_stack.append("(")
            prev_kind = "LPAREN"
        elif kind == "PAREN" and value == ")":
            found = False
            while op_stack:
                top = op_stack.pop()
                if top == "(":
                    found = True
                    break
                output.append(("OP", top))
            if not found:
                raise CalculatorError("Mismatched parentheses: extra ')'")
            prev_kind = "RPAREN"

    while op_stack:
        top = op_stack.pop()
        if top == "(":
            raise CalculatorError("Mismatched parentheses: extra '('")
        output.append(("OP", top))
    return output


# --- Postfix evaluator ------------------------------------------------------


def eval_postfix(postfix):
    stack = []
    for kind, value in postfix:
        if kind == "NUM":
            stack.append(value)
        else:  # OP
            if value in ("u-", "u+"):
                if not stack:
                    raise CalculatorError(f"Missing operand for unary {value}")
                a = stack.pop()
                stack.append(-a if value == "u-" else a)
            else:
                if len(stack) < 2:
                    raise CalculatorError(
                        f"Missing operand for binary operator {value!r}"
                    )
                b = stack.pop()
                a = stack.pop()
                if value == "+":
                    stack.append(a + b)
                elif value == "-":
                    stack.append(a - b)
                elif value == "*":
                    stack.append(a * b)
                elif value == "/":
                    if b == 0:
                        raise CalculatorError("Division by zero")
                    stack.append(a / b)
    if len(stack) != 1:
        raise CalculatorError("Malformed expression")
    return stack[0]


# --- Public API -------------------------------------------------------------


def evaluate(expression: str):
    """Evaluate an arithmetic expression and return its numeric result.

    Raises CalculatorError (a ValueError) on malformed input.
    """
    if not isinstance(expression, str):
        raise CalculatorError("expression must be a string")
    tokens = tokenize(expression)
    if not tokens:
        raise CalculatorError("Empty expression")
    postfix = to_postfix(tokens)
    return eval_postfix(postfix)
