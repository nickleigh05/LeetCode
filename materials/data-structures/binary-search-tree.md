# Binary Search Tree (BST)

```python
#        5
#      /   \
#     3     8
#    / \   / \
#   1   4 7   9
```

A [binary tree](binary-tree.md) with an ordering invariant: for every node, everything in its left subtree is smaller and everything in its right subtree is larger. That invariant is what makes search/insert/delete O(log n) on a balanced BST — at each node you know which single subtree to descend into, the same halving idea as [binary search](../algorithms/binary-search.md) but on a tree instead of an array.

An **inorder traversal** (left, node, right) of a BST visits values in ascending sorted order — a useful fact for "kth smallest" and validation problems.

**Complexity:** search/insert/delete O(log n) balanced, O(n) worst case (degenerates into a linked list if built from sorted input without rebalancing).

**Related:** [binary-tree](binary-tree.md) · [binary-search (algorithms)](../algorithms/binary-search.md) · [tree-traversal-orders](../algorithms/tree-traversal-orders.md)
