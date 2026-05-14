"""Tests for the Sudoku validator in solution.py."""

import copy
import pytest

from solution import is_valid_sudoku


# ---------- fixtures ----------

VALID_COMPLETE = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


VALID_PARTIAL = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


EMPTY_BOARD = [[0] * 9 for _ in range(9)]


# ---------- valid cases ----------

def test_valid_complete_board():
    assert is_valid_sudoku(VALID_COMPLETE) is True


def test_valid_partial_board():
    assert is_valid_sudoku(VALID_PARTIAL) is True


def test_empty_board_is_valid():
    assert is_valid_sudoku(EMPTY_BOARD) is True


def test_single_filled_cell():
    b = copy.deepcopy(EMPTY_BOARD)
    b[4][4] = 7
    assert is_valid_sudoku(b) is True


# ---------- invalid: row / column / box ----------

def test_duplicate_in_row():
    b = copy.deepcopy(EMPTY_BOARD)
    b[0][0] = 5
    b[0][8] = 5
    assert is_valid_sudoku(b) is False


def test_duplicate_in_column():
    b = copy.deepcopy(EMPTY_BOARD)
    b[0][3] = 4
    b[8][3] = 4
    assert is_valid_sudoku(b) is False


def test_duplicate_in_box():
    # Same 3x3 box, different row & column.
    b = copy.deepcopy(EMPTY_BOARD)
    b[0][0] = 9
    b[2][2] = 9
    assert is_valid_sudoku(b) is False


def test_box_violation_only_not_row_or_column():
    # Confirms box detection isn't accidentally caught by row/col check.
    b = copy.deepcopy(EMPTY_BOARD)
    b[3][3] = 2
    b[5][5] = 2  # same middle box, different row and column
    assert is_valid_sudoku(b) is False


def test_complete_board_with_introduced_conflict():
    b = copy.deepcopy(VALID_COMPLETE)
    # Swap so a row contains a duplicate.
    b[0][0] = 3  # duplicates the 3 already at b[0][1]
    assert is_valid_sudoku(b) is False


def test_partial_board_with_introduced_conflict():
    b = copy.deepcopy(VALID_PARTIAL)
    b[0][2] = 5  # conflicts with b[0][0] == 5
    assert is_valid_sudoku(b) is False


# ---------- zeros are ignored ----------

def test_multiple_zeros_do_not_conflict():
    b = copy.deepcopy(EMPTY_BOARD)
    # All zeros in row 0; should remain valid.
    assert is_valid_sudoku(b) is True


# ---------- malformed input ----------

def test_wrong_outer_length_raises():
    with pytest.raises(ValueError):
        is_valid_sudoku([[0] * 9 for _ in range(8)])


def test_wrong_row_length_raises():
    bad = [[0] * 9 for _ in range(9)]
    bad[3] = [0] * 8
    with pytest.raises(ValueError):
        is_valid_sudoku(bad)


def test_non_list_raises():
    with pytest.raises(ValueError):
        is_valid_sudoku("not a board")


def test_non_int_cell_raises():
    bad = [[0] * 9 for _ in range(9)]
    bad[0][0] = "5"
    with pytest.raises(ValueError):
        is_valid_sudoku(bad)


def test_out_of_range_cell_raises():
    bad = [[0] * 9 for _ in range(9)]
    bad[0][0] = 10
    with pytest.raises(ValueError):
        is_valid_sudoku(bad)


def test_negative_cell_raises():
    bad = [[0] * 9 for _ in range(9)]
    bad[0][0] = -1
    with pytest.raises(ValueError):
        is_valid_sudoku(bad)


def test_bool_cell_raises():
    # bool is subclass of int; explicitly rejected.
    bad = [[0] * 9 for _ in range(9)]
    bad[0][0] = True
    with pytest.raises(ValueError):
        is_valid_sudoku(bad)
