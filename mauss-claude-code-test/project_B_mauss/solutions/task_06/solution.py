"""Maze solver using BFS to find shortest 4-directional path."""

from collections import deque


def solve_maze(grid, start, end):
    """Find the shortest path from start to end in a 2D maze using BFS.

    Args:
        grid: 2D list where 0 = open cell, 1 = wall.
        start: (row, col) starting coordinate.
        end: (row, col) ending coordinate.

    Returns:
        List of (row, col) tuples representing the shortest path from start
        to end (inclusive), or None if no path exists.
    """
    if not grid or not grid[0]:
        return None

    rows = len(grid)
    cols = len(grid[0])

    sr, sc = start
    er, ec = end

    # Bounds checks
    if not (0 <= sr < rows and 0 <= sc < cols):
        return None
    if not (0 <= er < rows and 0 <= ec < cols):
        return None
    # Start or end on a wall
    if grid[sr][sc] == 1 or grid[er][ec] == 1:
        return None

    if start == end:
        return [start]

    # BFS
    queue = deque([start])
    # parent maps each visited cell to the cell it was reached from
    parent = {start: None}

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            # Reconstruct path
            path = []
            cur = end
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 0 and (nr, nc) not in parent:
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return None
