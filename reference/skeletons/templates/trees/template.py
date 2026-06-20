"""
Trees — DFS Recursion and BFS Level-Order Skeletons

Most tree problems are one of two traversals in disguise:

  1. DFS recursion   — solve each node from its children's answers. The shape is
                       always: base case -> recurse left -> recurse right ->
                       combine. WHEN you touch the node's value (before, between,
                       or after the recursive calls) gives pre-, in-, post-order.
  2. BFS level-order — a queue processes the tree one full level at a time, which
                       is what you want for shortest paths and "per level" work.

Invariant (DFS): each call returns a fully-correct answer for the subtree rooted
at `node`, assuming its recursive calls did the same for the children.
"""

from collections import deque
from typing import List, Optional


class TreeNode:
    """Binary tree node (matches the LeetCode definition)."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def dfs(node: Optional[TreeNode]) -> int:
    """Solve a subtree from its children's answers (post-order shape).

    Time:      O(n) — every node is visited exactly once.
    Space:     O(h) — the recursion stack, h = height (O(n) if the tree is skewed).
    Invariant: dfs(child) returns the correct answer for that child's subtree, so
               `node` only has to combine those with its own value.
    """

    # BASE CASE: the empty subtree. Returning an identity value here (0, True,
    # None, -inf...) is what lets the parent combine without special-casing.
    if node is None:
        return 0  # TODO: problem-specific identity for an empty subtree

    # RECURSE: collect the children's answers first (post-order).
    left_result = dfs(node.left)
    right_result = dfs(node.right)

    # COMBINE: build this node's answer from the children plus node.val.
    # TODO: problem-specific combine, e.g. max(left, right) + 1 for height, or
    # left_result + right_result + node.val for a subtree sum.
    return max(left_result, right_result) + 1


def bfs_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """Visit the tree one complete level at a time using a queue.

    Time:      O(n)
    Space:     O(w) — the queue holds at most one level; w = max width.
    Invariant: at the top of the outer loop the queue holds exactly the nodes of
               the current level, left to right, and nothing else.
    """

    levels: List[List[int]] = []
    if root is None:
        return levels

    queue: "deque[TreeNode]" = deque([root])

    while queue:
        # Snapshot the level size NOW, before this iteration enqueues the next
        # level — that frozen count is what bounds the inner loop.
        level_size = len(queue)
        current_level: List[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)  # TODO: problem-specific per-node work

            # Enqueue children for the next level, left before right.
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        levels.append(current_level)

    return levels
