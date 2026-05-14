"""Tests for the maze solver in solution.py."""

import pytest

from solution import solve_maze


def _is_valid_path(grid, path, start, end):
    """Helper: confirm ``path`` is a valid 4-connected open-cell path."""
    if not path:
        return False
    if path[0] != start or path[-1] != end:
        return False
    rows = len(grid)
    cols = len(grid[0])
    for r, c in path:
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if grid[r][c] != 0:
            return False
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
    return True


def test_start_equals_end():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (0, 0), (0, 0)) == [(0, 0)]


def test_simple_straight_line():
    grid = [[0, 0, 0, 0]]
    path = solve_maze(grid, (0, 0), (0, 3))
    assert path == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_simple_open_grid_shortest_length():
    # 3x3 fully open; manhattan distance from (0,0) to (2,2) = 4 -> 5 cells.
    grid = [[0] * 3 for _ in range(3)]
    path = solve_maze(grid, (0, 0), (2, 2))
    assert path is not None
    assert len(path) == 5
    assert _is_valid_path(grid, path, (0, 0), (2, 2))


def test_path_around_wall():
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    path = solve_maze(grid, (0, 0), (0, 2))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (0, 2))
    # Must detour: 7 cells (down, down, right, right, up, up = 6 moves).
    assert len(path) == 7


def test_no_path_blocked():
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    assert solve_maze(grid, (0, 0), (0, 2)) is None


def test_start_on_wall():
    grid = [[1, 0], [0, 0]]
    assert solve_maze(grid, (0, 0), (1, 1)) is None


def test_end_on_wall():
    grid = [[0, 0], [0, 1]]
    assert solve_maze(grid, (0, 0), (1, 1)) is None


def test_out_of_bounds_start():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (-1, 0), (1, 1)) is None
    assert solve_maze(grid, (2, 0), (1, 1)) is None


def test_out_of_bounds_end():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (0, 0), (1, 2)) is None
    assert solve_maze(grid, (0, 0), (-1, 1)) is None


def test_empty_grid():
    assert solve_maze([], (0, 0), (0, 0)) is None
    assert solve_maze([[]], (0, 0), (0, 0)) is None


def test_single_cell_open():
    assert solve_maze([[0]], (0, 0), (0, 0)) == [(0, 0)]


def test_single_cell_wall():
    assert solve_maze([[1]], (0, 0), (0, 0)) is None


def test_larger_maze_finds_shortest():
    # 5x5 maze with corridors. Only path: top row -> down right col -> left
    # along row 2 -> down left col -> right along bottom row.
    grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    path = solve_maze(grid, (0, 0), (4, 4))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (4, 4))
    # Manhattan distance is 8, but walls force a detour through (2,0)->(3,0)
    # then back across row 4. Total cells = 17.
    assert len(path) == 17


def test_returns_tuples():
    grid = [[0, 0], [0, 0]]
    path = solve_maze(grid, (0, 0), (1, 1))
    assert path is not None
    for step in path:
        assert isinstance(step, tuple)
        assert len(step) == 2


def test_no_diagonal_moves():
    # Diagonal-only opening should be unreachable.
    grid = [
        [0, 1],
        [1, 0],
    ]
    assert solve_maze(grid, (0, 0), (1, 1)) is None


def test_path_only_uses_open_cells():
    grid = [
        [0, 0, 1, 0, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    # (2, 3) is open and reachable; (2, 4) is a wall.
    path = solve_maze(grid, (0, 0), (2, 3))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (2, 3))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
