# Task 08 Handoff

## What was built
A Roman numeral converter in `solution.py` exposing two functions:

- `to_roman(n)` — converts an integer in `[1, 3999]` to a Roman numeral
  string using standard subtractive notation (`IV`, `IX`, `XL`, `XC`,
  `CD`, `CM`). Implemented with a greedy descent through an ordered list
  of `(value, symbol)` pairs.
- `from_roman(s)` — converts a Roman numeral string back to its integer
  value. Parses right-to-left, subtracting any symbol that is smaller
  than the symbol to its right and adding otherwise. After parsing, the
  result is re-encoded with `to_roman` and compared against the input to
  reject non-canonical forms (e.g. `IIII`, `VV`, `IC`, `MMMM`).

## Validation rules
- `to_roman` raises `TypeError` for non-`int` (and bool) inputs and
  `ValueError` for values outside `[1, 3999]`.
- `from_roman` raises `TypeError` for non-`str` inputs and `ValueError`
  for empty strings, lowercase letters, unknown characters, out-of-range
  values, and non-canonical encodings.

## Tests (`test_solution.py`)
- Parametrized known-value tests for `to_roman` and `from_roman` covering
  edge cases (1, 4, 9, 40, 49, 90, 99, 400, 444, 900, 999, 1987, 2024,
  3000, 3888, 3999).
- A full round-trip test over all integers in `[1, 3999]`.
- Range / type error tests for `to_roman` (0, 4000, -3, float, str,
  bool).
- Invalid-input tests for `from_roman` (empty, non-`str`, lowercase,
  unknown character).
- Non-canonical rejection tests (`IIII`, `VV`, `IC`, `MMMM`).

## How to run
```
cd solutions/task_08
pytest test_solution.py -v
```
All 67 tests pass (`67 passed in 0.09s`).

## Notes
- Standard library only; no `output.txt` is produced.
- The canonical-form check in `from_roman` is implemented via round-trip
  through `to_roman`, which keeps the parser strict without hand-coded
  pattern rules.
