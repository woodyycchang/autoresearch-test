# Handoff — Task 02

## What I built

`solution.py` exposes `is_valid_sudoku(board)` which validates a 9x9 Sudoku
board. The board is a list of 9 lists, each holding 9 integers in 0..9 where
0 means "empty". The function returns `True` iff:

1. The structure is exactly 9x9 with integer cells in `0..9`
   (booleans are explicitly rejected even though they are `int` subclasses).
2. No digit 1..9 repeats within any row, any column, or any 3x3 box.

Zeros are skipped during constraint checks. The input is not mutated.

## Algorithm

Single O(81) pass using three lists of nine sets (rows, columns, boxes).
Box index for cell `(r, c)` is `(r // 3) * 3 + (c // 3)`.

## Tests

`test_solution.py` covers:
- Valid complete board, valid partial board, fully empty board.
- Row, column, and 3x3 box duplicate violations (including parametrized
  positions and a duplicate introduced into an otherwise-complete board).
- Structural rejections: wrong outer length, wrong inner length, non-list
  input, non-list rows.
- Value rejections: out-of-range, negative, non-integer (`str`), boolean.
- Edge cases: single filled cell, many zeros, input-mutation guard.

## How to run

```
cd solutions/task_02/
pytest test_solution.py -v
```

All tests pass locally with only the standard library + pytest.

## Notes for the Validator

- Only `solution.py` and `test_solution.py` are needed at runtime.
- `is_valid_sudoku` lives in `solution.py` and is imported by the tests.
- I deliberately did NOT write `output.txt` — per instructions that's your job.
