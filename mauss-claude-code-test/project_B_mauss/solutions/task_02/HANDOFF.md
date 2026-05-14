# HANDOFF — Task 02 (Sudoku validator)

## What was built
A Sudoku validator: `is_valid_sudoku(board)` returns `True` iff a 9x9 board
satisfies the row / column / 3x3-box uniqueness constraints, treating `0` as
an empty cell. Partial (incomplete) boards are accepted; the function checks
*validity*, not *solvability*.

## File structure
```
solutions/task_02/
  solution.py        # is_valid_sudoku + _validate_shape helper
  test_solution.py   # 18 pytest tests
  HANDOFF.md         # this file
```

The Validator should produce `output.txt` per the task description (a 1-line
summary). I deliberately did NOT create it.

## How to run tests
```
cd /home/user/autoresearch-test/mauss-claude-code-test/project_B_mauss/solutions/task_02/
pytest test_solution.py -v
```
Result on my run: **18 passed** in ~0.03s (Python 3.11.15, pytest 9.0.2).

## Algorithm
Single pass over the 81 cells. For each filled cell, check three sets (row,
column, box) for the digit; if absent in all three, add it. Box index is
`(r // 3) * 3 + (c // 3)`. O(81) time, O(81) space.

## Edge cases covered
- Fully empty board (all zeros) → valid.
- Single filled cell → valid.
- Duplicates within row, within column, within 3x3 box (incl. a box-only
  violation where the two cells share neither row nor column — guards against
  the common bug of detecting box conflicts only because they coincide with
  a row/col conflict).
- Zeros are correctly ignored (multiple zeros in a row/col/box do not trip
  the duplicate check).
- Complete valid board accepted; same board with a single introduced
  conflict rejected.

## Input validation (non-obvious choices)
- **Raises `ValueError` for malformed shape/types** (not 9x9, non-list, cell
  out of `0..9`, non-int cell). A Sudoku-rule violation by contrast returns
  `False`. This separates "garbage input" from "well-formed but illegal
  position", which I think is the cleaner contract.
- **`bool` cells are rejected** even though `bool` is a subclass of `int` in
  Python (so `True` would otherwise sneak through as `1`). If the Validator
  decides booleans-as-ints should be allowed, that test (`test_bool_cell_raises`)
  is the one to change.
- The task said "integer 1-9 or 0"; I interpreted strictly. If a more lenient
  contract is desired (e.g. accept floats like `5.0`), the shape validator is
  the only place to change.

## Limitations / things I did NOT do
- No solver, no completeness check. A board of all zeros is "valid" per this
  function; if the Validator's `output.txt` test requires `False` for empty
  boards, that's a contract mismatch worth flagging — current behavior matches
  the standard LeetCode-style "Valid Sudoku" definition.
- No performance optimization beyond the obvious single pass; not needed for
  9x9.
- Only stdlib + pytest used, per constraints.

## RECIPROCATE
My contribution: a Sudoku validator with strict input validation, a clear
separation between malformed-input (raises) and rule-violation (returns
False), and 18 passing tests covering rows, columns, boxes, empty/partial
boards, and bad inputs. This builds on the task spec's `is_valid_sudoku(board)`
signature by making the input contract explicit and well-tested, so the
Validator can write `output.txt` and confirm correctness without needing to
guess how edge cases (zeros, malformed grids, bools) are handled.
