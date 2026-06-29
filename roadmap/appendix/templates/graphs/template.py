"""
Graphs — BFS and DFS Traversal Skeletons

Almost every basic graph problem is "visit every node reachable from a source,
exactly once". Two engines do the work:

  1. BFS (queue)           — explores in rings of increasing distance, so the
                             first time you reach a node is via a SHORTEST
                             unweighted path.
  2. DFS (stack/recursion) — dives deep first; ideal for connectivity, cycle
                             detection, and counting components / island areas.

A `visited` set is non-negotiable: without it any cycle loops forever and shared
nodes get re-processed.

Invariant: a node enters `visited` exactly once, at the moment it is first
discovered, so total work is O(V + E).
"""

from collections import deque
from typing import Dict, List, Set, Tuple


def bfs(graph: Dict[int, List[int]], start: int) -> int:
    """Shortest-distance / level traversal from a single source.

    Time:      O(V + E) — each node dequeued once, each edge scanned once.
    Space:     O(V) for the queue and visited set.
    Invariant: a node is marked visited at ENQUEUE time, so it is never queued
               twice; when it is dequeued its distance is already minimal.
    """

    visited: Set[int] = {start}
    queue: "deque[Tuple[int, int]]" = deque([(start, 0)])  # (node, distance)

    while queue:
        node, distance = queue.popleft()

        # TODO: problem-specific work, e.g. return `distance` on reaching a target.

        for neighbor in graph[node]:
            # Mark at enqueue time (not dequeue time): otherwise several
            # neighbors could queue the same node before it is ever processed.
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return len(visited)


def dfs(graph: Dict[int, List[int]], start: int, visited: Set[int]) -> None:
    """Depth-first exploration for connectivity / counting.

    Time:      O(V + E)
    Space:     O(V) for the recursion stack + visited set.
    Invariant: every node handed to dfs is marked visited first, so it is
               processed exactly once even with cycles or shared edges.
    """

    visited.add(start)

    # TODO: problem-specific work on `start` (count it, accumulate area, etc.).

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


# Grid graphs are implicit: a cell's neighbors are its 4 (or 8) adjacent cells.
DIRECTIONS: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def grid_dfs(grid: List[List[int]], row: int, col: int, visited: Set[Tuple[int, int]]) -> int:
    """Flood-fill a 2-D grid; return the size of the connected region.

    Time:      O(rows * cols) — each cell visited at most once.
    Space:     O(rows * cols) worst-case recursion depth + visited set.
    Invariant: a cell joins `visited` before any neighbor recurses, so the same
               cell is never counted twice.
    """

    rows, cols = len(grid), len(grid[0])

    # Bounds check FIRST, then already-seen, then the "is this traversable?" test.
    # TODO: replace `grid[row][col] != 1` with the real "blocked" condition.
    if (
        row < 0
        or row >= rows
        or col < 0
        or col >= cols
        or (row, col) in visited
        or grid[row][col] != 1
    ):
        return 0

    visited.add((row, col))

    area = 1
    for delta_row, delta_col in DIRECTIONS:
        area += grid_dfs(grid, row + delta_row, col + delta_col, visited)

    return area
