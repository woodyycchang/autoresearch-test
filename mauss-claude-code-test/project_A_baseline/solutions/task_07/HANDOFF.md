# Task 07 - Handoff

## What was built
A minimal JSON parser exposing a single function `parse(s)` that returns the
Python value corresponding to a JSON-encoded string. Implemented as a
recursive-descent parser in a `_Parser` class with an index cursor over the
input.

## Files
- `solution.py` - parser implementation (`parse` is the public API).
- `test_solution.py` - pytest suite.

## Supported features
- JSON literals: `true`, `false`, `null`.
- Numbers: signed integers, decimals, scientific notation (`1e2`, `1.5E-2`).
  Integers come back as `int`; anything with a fraction or exponent comes
  back as `float`.
- Strings with escapes: `\"`, `\\`, `\/`, `\n`, `\t`, `\r`, `\b`, `\f`,
  and `\uXXXX` (4-hex-digit) Unicode escapes.
- Arrays and objects with arbitrary nesting.
- Whitespace (` `, `\t`, `\n`, `\r`) anywhere between tokens.

## Rejection (raises `ValueError`)
- Unterminated strings, invalid escapes, control chars in strings.
- Trailing commas in arrays/objects.
- Missing values, colons, or unquoted keys.
- Extra data after a top-level value.
- Malformed numbers (`+1`, `1..2`, lone `-`).
- Bad literals (`tru`, single-quoted strings).
- Empty input or non-string input.

## Constraints honored
- No use of `json`, `ast.literal_eval`, `eval`, or `exec`.
- Standard library only; tests are pytest.
- No `output.txt` is written (per pipeline constraints).

## Running tests
```
cd solutions/task_07
pytest test_solution.py -v
```
All 32 tests pass.
