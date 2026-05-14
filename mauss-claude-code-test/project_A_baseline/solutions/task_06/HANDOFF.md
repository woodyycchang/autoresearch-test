# Task 06 Handoff

## What was built
- `solution.py`: `solve_maze(grid, start, end)` — BFS shortest-path solver on
  a 2D grid (0 = open, 1 = wall) using 4-directional moves. Returns the path
  as a list of `(row, col)` tuples (including start and end), or `None` when
  no path exists / inputs are invalid.

## Approach
- Standard BFS from `start`, using a `deque` and a `parents` dict that
  doubles as the visited set.
- Edge cases handled: empty grid, out-of-bounds coordinates, start or end
  on a wall, `start == end`.
- No diagonal moves; only `(±1, 0)` / `(0, ±1)`.

## Tests
- `test_solution.py` covers: start==end, straight line, open grid optimality,
  detour around walls, blocked maze, walls at start/end, out-of-bounds,
  empty/single-cell grids, larger maze shortest length, return types,
  no-diagonal rule.
- Run: `pytest test_solution.py -v` from this directory.
