"""Sudoku validator.

Provides ``is_valid_sudoku(board)`` which checks whether a 9x9 Sudoku board
satisfies the standard constraints: no repeated digit 1-9 in any row, column,
or 3x3 sub-box. Empty cells are represented by 0 and are ignored.

The function validates board shape strictly (exactly 9 rows of 9 ints, each
cell in 0..9) and raises ``ValueError`` for malformed input. A board that is
well-formed but violates a Sudoku rule returns False (it does not raise).
"""

from typing import List

Board = List[List[int]]


def _validate_shape(board: Board) -> None:
    """Raise ValueError if the board is not a 9x9 grid of ints in 0..9."""
    if not isinstance(board, list) or len(board) != 9:
        raise ValueError("board must be a list of 9 rows")
    for r, row in enumerate(board):
        if not isinstance(row, list) or len(row) != 9:
            raise ValueError(f"row {r} must be a list of 9 cells")
        for c, cell in enumerate(row):
            # bool is a subclass of int in Python; reject it explicitly so that
            # True/False do not slip through as 1/0.
            if isinstance(cell, bool) or not isinstance(cell, int):
                raise ValueError(f"cell ({r},{c}) must be an int")
            if cell < 0 or cell > 9:
                raise ValueError(f"cell ({r},{c})={cell} out of range 0..9")


def is_valid_sudoku(board: Board) -> bool:
    """Return True iff the 9x9 ``board`` satisfies Sudoku constraints.

    Zeros are treated as empty cells and ignored when checking duplicates.
    The board does not need to be complete; partial boards are accepted as
    long as no rule is violated.
    """
    _validate_shape(board)

    # Track seen digits per row, column, and 3x3 box.
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == 0:
                continue
            b = (r // 3) * 3 + (c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[b]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[b].add(val)
    return True
