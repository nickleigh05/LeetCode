"""
Union-Find (Disjoint Set Union) — Path Compression + Union by Rank Skeleton

Union-Find maintains a partition of n elements into disjoint sets and answers
two questions fast: "which set is x in?" (find) and "merge the sets of x and y"
(union). With both optimizations each operation is effectively O(1) (inverse
Ackermann) — the go-to for undirected connectivity, cycle detection, and
Kruskal's MST.

Invariant: every element points (directly or transitively) at the single
representative ("root") of its set; two elements share a set iff they share a
root. `rank` upper-bounds a tree's height and keeps the trees shallow.
"""

from typing import List


class UnionFind:
    """Disjoint-set forest with path compression and union by rank."""

    def __init__(self, size: int) -> None:
        # Each element starts in its own singleton set (it is its own parent).
        self.parent: List[int] = list(range(size))
        # Rank approximates tree height; all singletons start at 0.
        self.rank: List[int] = [0] * size
        # Number of disjoint sets — handy for "count components" problems.
        self.count: int = size

    def find(self, x: int) -> int:
        """Return the root of x's set, compressing the path on the way.

        Time: ~O(1) amortized (inverse Ackermann).
        """

        # First climb to the root.
        root = x
        while self.parent[root] != root:
            root = self.parent[root]

        # Path compression: re-point every node on the path straight at the root
        # so future finds are flat. Done iteratively to avoid deep recursion.
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]

        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets of x and y. Returns False if they were already joined.

        That False return powers cycle detection: an edge whose endpoints
        already share a root would close a cycle.
        """

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # already connected -> this edge would form a cycle

        # Union by rank: hang the shorter tree under the taller one so the height
        # grows as slowly as possible.
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        self.count -= 1  # two sets just became one
        return True

    def connected(self, x: int, y: int) -> bool:
        """True iff x and y currently belong to the same set."""

        return self.find(x) == self.find(y)
