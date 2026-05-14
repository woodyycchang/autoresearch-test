# Task 05 Handoff: Arithmetic Calculator

## ACCEPT
Prior context: the task author specified an `evaluate(expression)` function
that handles operator precedence, parentheses, integer and float operands,
and explicitly forbids `eval()` / `exec()`. The example `"3 + 4 * 2 - (1 + 1)"`
must return `9`. I treated that example as a binding acceptance test
(`test_task_example`).

## What I built

`solution.py` implements a safe expression evaluator using the classic
shunting-yard algorithm:

1. **`tokenize(expression)`** — scans the string into typed tokens:
   `("NUM", value)`, `("OP", "+|-|*|/")`, `("PAREN", "(|)")`. Skips
   whitespace; rejects unknown characters and malformed numbers
   (e.g. `1..2`).
2. **`to_postfix(tokens)`** — converts infix to Reverse Polish Notation
   honoring precedence (`* /` > `+ -`) and left-associativity. Detects
   unary `+`/`-` from context (start of expression, after operator, or
   after `(`), encoded as pseudo-ops `u+` / `u-` with highest precedence
   and right-associativity.
3. **`eval_postfix(postfix)`** — stack-based RPN evaluator; raises
   `CalculatorError` on division-by-zero or malformed input.
4. **`evaluate(expression)`** — public entry point. Returns `int` when
   all operands are int and only `+ - *` are used; otherwise `float`
   (division always yields float, matching Python's `/`).

`eval()` and `exec()` are NOT used anywhere — verifiable by grep.

## GIVE (info for the Validator)

- **Run command**: `pytest test_solution.py -v` from this directory.
- **Test result**: **40 passed in 0.05s** on Python 3.11.15, pytest 9.0.2.
- **Public API**: `from solution import evaluate, CalculatorError`.
  `CalculatorError` subclasses `ValueError`, so generic
  `except ValueError` also works.
- **Test coverage breakdown**:
  - Basic ops, precedence, parentheses (incl. the task's exact example).
  - Left-associativity for `-` and `/`.
  - Floats: `1.5 + 2.25`, `.5 + .25`, mixed int/float, `7 / 2`.
  - Unary `+`/`-`, including `--5`, `-(3+4)`, `2 * -3`.
  - Whitespace tolerance (none, extra, tabs).
  - Errors: division by zero, mismatched parens (both directions),
    empty string, whitespace-only, invalid character, missing operand,
    `1..2`, non-string input.
  - Result type checks: int-only stays int; `/` returns float.
- **Known design choices a reviewer should note**:
  - `**` (exponent) and `%` (modulo) are NOT supported — task did not
    require them. Tokenizer would reject them as unknown characters.
  - Scientific notation (`1e5`) is NOT supported by the tokenizer.
  - Integer division uses Python's `/` (true division), so `4 / 2 == 2.0`.
- **No `output.txt`** was created, per task constraints in this pipeline
  (the task description mentions writing one, but the agent instructions
  explicitly forbid it — I followed the agent instructions).
- **Files in this directory**:
  - `solution.py` — implementation (~150 lines, no external deps).
  - `test_solution.py` — 40 pytest tests.
  - `HANDOFF.md` — this file.

## RECIPROCATE

My contribution: a safe, eval-free arithmetic expression evaluator with
shunting-yard parsing, full operator-precedence + parentheses + unary-op
support, plus a 40-test pytest suite that covers happy paths, edge cases,
and error conditions. This builds on the task author's `evaluate(expression)`
specification by translating the informal contract (precedence, parens,
int + float, no `eval`) into an executable RPN-based implementation
verified against the exact example in the task plus 39 additional
scenarios — giving the Validator a deterministic, reproducible passing
test run as evidence.
