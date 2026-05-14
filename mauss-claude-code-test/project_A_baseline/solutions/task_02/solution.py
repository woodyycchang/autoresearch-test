"""Sudoku validator.

Provides ``is_valid_sudoku(board)`` which checks whether a 9x9 board
satisfies the standard Sudoku constraints, ignoring empty cells (0).
"""

from typing import List


def is_valid_sudoku(board: List[List[int]]) -> bool:
    """Return True if ``board`` is a valid (partial or complete) Sudoku.

    Rules enforced:
      * Board must be a 9x9 list of lists.
      * Each cell must be an integer in the range 0..9 (0 = empty).
      * No digit 1..9 may repeat within any row, any column, or any of the
        nine 3x3 sub-boxes.

    Zeros are treated as empty and are not checked for duplicates.
    """
    # Structural validation -------------------------------------------------
    if not isinstance(board, list) or len(board) != 9:
        return False
    for row in board:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for cell in row:
            # ``bool`` is a subclass of ``int``; reject it explicitly so
            # that True/False are not silently accepted as digits.
            if isinstance(cell, bool) or not isinstance(cell, int):
                return False
            if cell < 0 or cell > 9:
                return False

    # Constraint validation -------------------------------------------------
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if value == 0:
                continue
            box_idx = (r // 3) * 3 + (c // 3)
            if value in rows[r] or value in cols[c] or value in boxes[box_idx]:
                return False
            rows[r].add(value)
            cols[c].add(value)
            boxes[box_idx].add(value)

    return True
