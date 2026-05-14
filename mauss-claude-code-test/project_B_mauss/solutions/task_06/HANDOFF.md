# Task 06 Handoff — Maze Solver (BFS)

## ACCEPT
Prior agents in this project established a per-task layout under
`project_B_mauss/solutions/task_NN/` containing `solution.py`,
`test_solution.py`, and `HANDOFF.md` (tasks 01-05 follow this exact
pattern). I am continuing that convention for task_06 so the Validator
sees a uniform structure.

## GIVE — what the next agent (Validator) needs to know

### What was built
`solve_maze(grid, start, end)` in `solution.py`:
- 2D list maze where `0` = open, `1` = wall.
- `start` / `end` are `(row, col)` tuples.
- Returns the **shortest** path as a list of `(row, col)` tuples,
  inclusive of both endpoints; returns `None` when no path exists.
- BFS with a `collections.deque` queue and a `parent` dict that doubles
  as the visited set; path is reconstructed by walking parents from
  `end` back to `start` and reversing.
- Moves are strictly 4-directional (up/down/left/right).

### Design choices / edge cases handled
- Empty grid (`[]` or `[[]]`) returns `None`.
- Out-of-bounds `start` or `end` returns `None`.
- `start` or `end` on a wall returns `None`.
- `start == end` returns `[start]` (length-1 path) — only when that
  cell is open and in bounds.
- Single-cell grids: open cell with `start==end` returns `[(0,0)]`;
  wall cell returns `None`.
- BFS guarantees shortest path in an unweighted grid.

### How to run the tests
```
cd project_B_mauss/solutions/task_06/
pytest test_solution.py -v
```
All 15 tests pass locally (stdlib + pytest only — no third-party deps).

### Risks / things to double-check
- Spec says "include start and end" in the returned path; verified by
  `test_simple_open_grid` (length-5 path for Manhattan distance 4) and
  `test_start_equals_end`.
- The task description ends "write a 1-line summary ... to `output.txt`",
  but the Implementer constraints in this pipeline explicitly say
  **No output.txt**. I followed the constraint and did not create one.
  Validator: please do not flag the missing `output.txt` as a defect.
- Tests use a `_is_valid_path` helper rather than hard-coding exact
  path sequences, because multiple equally-short paths can be valid;
  the helper checks contiguity, bounds, openness, and endpoints.

## RECIPROCATE
My contribution: a BFS-based `solve_maze` with a thorough pytest suite
covering open grids, walls, unreachable endpoints, bounds errors,
single-cell grids, multi-route shortest-path selection, and
4-directional-only movement. This builds on the prior tasks' (01-05)
`solution.py` + `test_solution.py` + `HANDOFF.md` layout by extending
it to a graph-search problem and by surfacing the
`output.txt`-constraint conflict so the Validator does not penalize
its absence.
