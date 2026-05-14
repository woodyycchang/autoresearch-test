"""Tests for solve_maze BFS implementation."""

import pytest

from solution import solve_maze


def _is_valid_path(grid, path, start, end):
    """Helper: verify path is contiguous, in-bounds, on open cells, and connects start->end."""
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


def test_simple_open_grid():
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    path = solve_maze(grid, (0, 0), (2, 2))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (2, 2))
    # Manhattan distance is 4, so shortest path has 5 cells.
    assert len(path) == 5


def test_start_equals_end():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (0, 0), (0, 0)) == [(0, 0)]


def test_no_path_walled_off():
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    assert solve_maze(grid, (0, 0), (0, 2)) is None


def test_start_on_wall():
    grid = [
        [1, 0],
        [0, 0],
    ]
    assert solve_maze(grid, (0, 0), (1, 1)) is None


def test_end_on_wall():
    grid = [
        [0, 0],
        [0, 1],
    ]
    assert solve_maze(grid, (0, 0), (1, 1)) is None


def test_out_of_bounds_start():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (-1, 0), (1, 1)) is None
    assert solve_maze(grid, (2, 0), (1, 1)) is None


def test_out_of_bounds_end():
    grid = [[0, 0], [0, 0]]
    assert solve_maze(grid, (0, 0), (5, 5)) is None


def test_path_must_navigate_walls():
    grid = [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
    ]
    path = solve_maze(grid, (0, 0), (4, 3))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (4, 3))


def test_single_cell_open():
    grid = [[0]]
    assert solve_maze(grid, (0, 0), (0, 0)) == [(0, 0)]


def test_single_cell_wall():
    grid = [[1]]
    assert solve_maze(grid, (0, 0), (0, 0)) is None


def test_empty_grid():
    assert solve_maze([], (0, 0), (0, 0)) is None
    assert solve_maze([[]], (0, 0), (0, 0)) is None


def test_shortest_path_when_two_routes_exist():
    # Two equally-long detours around a center wall; both length 5.
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    path = solve_maze(grid, (0, 0), (2, 2))
    assert path is not None
    assert len(path) == 5
    assert _is_valid_path(grid, path, (0, 0), (2, 2))


def test_4_directional_only_no_diagonals():
    # If diagonals were allowed, path length would be 2; with 4-dir it must be 3.
    grid = [
        [0, 0],
        [0, 0],
    ]
    path = solve_maze(grid, (0, 0), (1, 1))
    assert path is not None
    assert len(path) == 3


def test_returns_tuples():
    grid = [[0, 0], [0, 0]]
    path = solve_maze(grid, (0, 0), (1, 1))
    assert all(isinstance(step, tuple) and len(step) == 2 for step in path)


def test_larger_maze():
    grid = [
        [0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
    ]
    path = solve_maze(grid, (0, 0), (5, 5))
    assert path is not None
    assert _is_valid_path(grid, path, (0, 0), (5, 5))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
