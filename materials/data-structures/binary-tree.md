# Binary Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

A hierarchical structure where each node has at most two children (`left`, `right`) — unlike a [linked list](linked-list.md)'s single chain, a tree branches. Almost every tree problem is some form of "do something at this node, then recurse into `left` and `right`" — see [dfs](../algorithms/dfs.md) and [tree-traversal-orders](../algorithms/tree-traversal-orders.md).

**Complexity:** visiting every node once (any traversal) O(n) · height of a balanced tree O(log n), worst case (a chain) O(n).

**Related:** [binary-search-tree](binary-search-tree.md) · [dfs](../algorithms/dfs.md) · [bfs](../algorithms/bfs.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
