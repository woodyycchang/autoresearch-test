# Task 05 Handoff

## What was built

`evaluate(expression: str) -> int | float` in `solution.py`:
a calculator that parses and evaluates arithmetic expression strings
(e.g. `"3 + 4 * 2 - (1 + 1)"`) without using `eval()` or `exec()`.

## Approach

- **Tokenizer**: scans the string into tokens (`NUM`, `+`, `-`, `*`, `/`, `(`, `)`),
  rejecting unexpected characters and malformed numbers.
- **Recursive-descent parser** with classic grammar:
  - `expr := term (('+' | '-') term)*`
  - `term := factor (('*' | '/') factor)*`
  - `factor := ('+' | '-') factor | primary`
  - `primary := NUM | '(' expr ')'`
- Operator precedence (`* /` over `+ -`) and parentheses are handled by grammar
  structure. Left-associativity is enforced by the iterative loops.
- Integer literals stay `int`; literals containing `.` become `float`.
  Division always produces `float` (Python `/` semantics).
- Unary `+`/`-` supported, including chained (`--5 == 5`).

## Error handling

All input errors raise `CalculatorError` (a `ValueError` subclass), including:
empty/whitespace input, division by zero, unmatched parens, invalid chars,
double dots in numbers, trailing/double operators, non-string input.

## Tests

`test_solution.py` has **37 tests** across 8 classes covering basic ops,
precedence, parentheses (incl. nested), unary operators, whitespace handling,
floating-point behavior, error cases, and a guard that the source contains
neither `eval(` nor `exec(`.

## Run

```
cd solutions/task_05/
pytest test_solution.py -v
```

Result: **37 passed**.

## Notes

- `output.txt` was intentionally not created (per pipeline constraint).
- Only Python stdlib + `pytest` used.
