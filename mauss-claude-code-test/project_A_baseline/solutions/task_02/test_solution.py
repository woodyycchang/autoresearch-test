"""Tests for ``is_valid_sudoku``."""

import copy

import pytest

from solution import is_valid_sudoku


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_COMPLETE_BOARD = [
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

VALID_PARTIAL_BOARD = [
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


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

def test_complete_valid_board():
    assert is_valid_sudoku(VALID_COMPLETE_BOARD) is True


def test_partial_valid_board():
    assert is_valid_sudoku(VALID_PARTIAL_BOARD) is True


def test_empty_board_is_valid():
    assert is_valid_sudoku(EMPTY_BOARD) is True


# ---------------------------------------------------------------------------
# Row / column / box violations
# ---------------------------------------------------------------------------

def test_duplicate_in_row():
    board = copy.deepcopy(VALID_PARTIAL_BOARD)
    # Place a duplicate 5 in row 0 (already has a 5 at column 0).
    board[0][2] = 5
    assert is_valid_sudoku(board) is False


def test_duplicate_in_column():
    board = copy.deepcopy(VALID_PARTIAL_BOARD)
    # Column 0 already contains 5, 6, 8, 4, 7. Place another 5 at row 8.
    board[8][0] = 5
    assert is_valid_sudoku(board) is False


def test_duplicate_in_box():
    board = copy.deepcopy(EMPTY_BOARD)
    # Top-left 3x3 box gets two 7s without sharing a row or column.
    board[0][0] = 7
    board[1][1] = 7
    assert is_valid_sudoku(board) is False


def test_duplicate_in_bottom_right_box():
    board = copy.deepcopy(EMPTY_BOARD)
    board[6][6] = 9
    board[8][8] = 9
    assert is_valid_sudoku(board) is False


def test_row_violation_in_complete_board():
    board = copy.deepcopy(VALID_COMPLETE_BOARD)
    # Swap a cell to introduce a duplicate in row 0.
    board[0][8] = 5
    assert is_valid_sudoku(board) is False


# ---------------------------------------------------------------------------
# Structural / type validation
# ---------------------------------------------------------------------------

def test_rejects_wrong_outer_length():
    board = [[0] * 9 for _ in range(8)]
    assert is_valid_sudoku(board) is False


def test_rejects_wrong_inner_length():
    board = [[0] * 9 for _ in range(9)]
    board[3] = [0] * 8
    assert is_valid_sudoku(board) is False


def test_rejects_non_list_input():
    assert is_valid_sudoku("not a board") is False
    assert is_valid_sudoku(None) is False
    assert is_valid_sudoku(42) is False


def test_rejects_non_list_row():
    board = [[0] * 9 for _ in range(9)]
    board[0] = "123456789"
    assert is_valid_sudoku(board) is False


def test_rejects_out_of_range_value():
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = 10
    assert is_valid_sudoku(board) is False


def test_rejects_negative_value():
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = -1
    assert is_valid_sudoku(board) is False


def test_rejects_non_integer_value():
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = "5"
    assert is_valid_sudoku(board) is False


def test_rejects_boolean_value():
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = True
    assert is_valid_sudoku(board) is False


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_single_filled_cell_is_valid():
    board = copy.deepcopy(EMPTY_BOARD)
    board[4][4] = 5
    assert is_valid_sudoku(board) is True


def test_zeros_can_repeat_freely():
    # Many zeros in a row/col/box must still be considered valid.
    board = copy.deepcopy(EMPTY_BOARD)
    board[0] = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    assert is_valid_sudoku(board) is True


def test_does_not_mutate_input():
    board = copy.deepcopy(VALID_PARTIAL_BOARD)
    snapshot = copy.deepcopy(board)
    is_valid_sudoku(board)
    assert board == snapshot


@pytest.mark.parametrize("row,col,val", [
    (0, 0, 1),
    (4, 4, 9),
    (8, 8, 5),
])
def test_isolated_digit_is_valid(row, col, val):
    board = copy.deepcopy(EMPTY_BOARD)
    board[row][col] = val
    assert is_valid_sudoku(board) is True
