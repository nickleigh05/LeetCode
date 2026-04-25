# Trees

## 7. Trees (15 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 226 | Easy | Invert Binary Tree | [Link](https://leetcode.com/problems/invert-binary-tree/) |
| 104 | Easy | Maximum Depth of Binary Tree | [Link](https://leetcode.com/problems/maximum-depth-of-binary-tree/) |
| 543 | Easy | Diameter of Binary Tree | [Link](https://leetcode.com/problems/diameter-of-binary-tree/) |
| 110 | Easy | Balanced Binary Tree | [Link](https://leetcode.com/problems/balanced-binary-tree/) |
| 100 | Easy | Same Tree | [Link](https://leetcode.com/problems/same-tree/) |
| 572 | Easy | Subtree of Another Tree | [Link](https://leetcode.com/problems/subtree-of-another-tree/) |
| 235 | Medium | Lowest Common Ancestor of a BST | [Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) |
| 102 | Medium | Binary Tree Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal/) |
| 199 | Medium | Binary Tree Right Side View | [Link](https://leetcode.com/problems/binary-tree-right-side-view/) |
| 1448 | Medium | Count Good Nodes in Binary Tree | [Link](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) |
| 98 | Medium | Validate Binary Search Tree | [Link](https://leetcode.com/problems/validate-binary-search-tree/) |
| 230 | Medium | Kth Smallest Element in a BST | [Link](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) |
| 105 | Medium | Construct Binary Tree from Preorder and Inorder Traversal | [Link](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) |
| 124 | Hard | Binary Tree Maximum Path Sum | [Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/) |
| 297 | Hard | Serialize and Deserialize Binary Tree | [Link](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) |

---

## Data Structures

### Binary Tree
Each node has a value, a `left` child, and a `right` child (either can be null). There are no ordering constraints on a general binary tree. Height can be up to O(n) in the worst case (skewed tree) or O(log n) for a balanced tree.

### Binary Search Tree (BST)
A binary tree where every node in the left subtree has a value less than the root and every node in the right subtree has a value greater than the root. This ordering means in-order traversal (left → root → right) always produces a sorted sequence. Search, insert, and delete are O(log n) average, O(n) worst case.

### Queue (for BFS)
Used in level-order traversal. Process all nodes at the current depth before moving to the next level. A `deque` (double-ended queue) with `popleft()` is the standard choice in Python.

---

## Core Patterns

### DFS — Recursive (Pre/In/Post Order)
The call stack handles traversal automatically. Pre-order: process the node before children. In-order: process between children (gives sorted order for BST). Post-order: process after children (height, diameter, path sum problems). Most tree problems use post-order DFS because you need child results before computing the parent's answer.

### DFS with Return Value
Return useful information up the call stack from each subtree (e.g. height, max path, whether it's valid). Combine left and right return values at the current node. Update a global answer variable if needed. Used in Diameter, Balanced Binary Tree, Maximum Path Sum.

### BFS — Level Order
Use a queue. At each step, process every node currently in the queue (those are all at the same level), then enqueue their children. Track level by processing in batches of `len(queue)`. Used in Level Order Traversal, Right Side View.

### BST Property Exploitation
For BST problems, use the sorted structure: go left if target < node, go right if target > node. For LCA in a BST: the split point (one value goes left, the other goes right) is the LCA. For validation: pass down `(min_val, max_val)` bounds and check each node stays within them.

### Two-Tree Recursion
Recurse on two trees simultaneously, comparing them node by node. Both must be non-null and equal, and both subtrees must match. Used in Same Tree, Subtree of Another Tree.

### Serialize / Deserialize
Convert a tree to a string (pre-order with null markers) and back. Use a queue or index pointer to reconstruct. The key insight: pre-order traversal uniquely determines the tree structure when you include null markers.
