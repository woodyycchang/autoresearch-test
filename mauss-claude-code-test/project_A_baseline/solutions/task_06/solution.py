"""Maze solver using BFS.

A grid is a 2D list where 0 = open cell and 1 = wall. The function
``solve_maze`` finds the shortest path from ``start`` to ``end`` using
4-directional moves (up/down/left/right).
"""

from collections import deque
from typing import List, Optional, Tuple

Coord = Tuple[int, int]


def solve_maze(
    grid: List[List[int]],
    start: Coord,
    end: Coord,
) -> Optional[List[Coord]]:
    """Find the shortest path through ``grid`` from ``start`` to ``end``.

    Parameters
    ----------
    grid:
        A 2D list where ``0`` denotes an open cell and ``1`` denotes a wall.
    start:
        ``(row, col)`` starting coordinate.
    end:
        ``(row, col)`` target coordinate.

    Returns
    -------
    A list of ``(row, col)`` tuples representing the shortest path from
    ``start`` to ``end`` inclusive, or ``None`` if no path exists.
    """
    if not grid or not grid[0]:
        return None

    rows = len(grid)
    cols = len(grid[0])

    sr, sc = start
    er, ec = end

    # Validate bounds.
    if not (0 <= sr < rows and 0 <= sc < cols):
        return None
    if not (0 <= er < rows and 0 <= ec < cols):
        return None

    # Start or end is a wall -> no path.
    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return None

    # Trivial case: start == end.
    if start == end:
        return [start]

    # BFS.
    queue = deque([start])
    # parents[cell] = previous cell on shortest path; start has no parent.
    parents: dict = {start: None}

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 0 and (nr, nc) not in parents:
                    parents[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    if end not in parents:
        return None

    # Reconstruct path from end -> start, then reverse.
    path: List[Coord] = []
    cur: Optional[Coord] = end
    while cur is not None:
        path.append(cur)
        cur = parents[cur]
    path.reverse()
    return path
