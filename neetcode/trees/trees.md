# Trees

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 sharpens the same recursive patterns with diameter, balance checking, and right-side views. NeetCode 250 adds iterative DFS variants and tree DP problems where a single recursive call must return multiple values simultaneously. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, identify whether it needs DFS (and which order), BFS, or a DP return tuple before writing any code.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 226 | Easy | Invert Binary Tree | [Link](https://leetcode.com/problems/invert-binary-tree/) | ☐ |
| 104 | Easy | Maximum Depth of Binary Tree | [Link](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | ☐ |
| 100 | Easy | Same Tree | [Link](https://leetcode.com/problems/same-tree/) | ☐ |
| 572 | Easy | Subtree of Another Tree | [Link](https://leetcode.com/problems/subtree-of-another-tree/) | ☐ |
| 235 | Medium | Lowest Common Ancestor of a BST | [Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | ☐ |
| 102 | Medium | Binary Tree Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal/) | ☐ |
| 98 | Medium | Validate Binary Search Tree | [Link](https://leetcode.com/problems/validate-binary-search-tree/) | ☐ |
| 230 | Medium | Kth Smallest Element in a BST | [Link](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | ☐ |
| 105 | Medium | Construct Binary Tree from Preorder and Inorder Traversal | [Link](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | ☐ |
| 124 | Hard | Binary Tree Maximum Path Sum | [Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | ☐ |
| 297 | Hard | Serialize and Deserialize Binary Tree | [Link](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 543 | Easy | Diameter of Binary Tree | [Link](https://leetcode.com/problems/diameter-of-binary-tree/) | ☐ |
| 110 | Easy | Balanced Binary Tree | [Link](https://leetcode.com/problems/balanced-binary-tree/) | ☐ |
| 199 | Medium | Binary Tree Right Side View | [Link](https://leetcode.com/problems/binary-tree-right-side-view/) | ☐ |
| 1448 | Medium | Count Good Nodes in Binary Tree | [Link](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 94 | Easy | Binary Tree Inorder Traversal | [Link](https://leetcode.com/problems/binary-tree-inorder-traversal/) | ☐ | DFS iterative |
| 144 | Easy | Binary Tree Preorder Traversal | [Link](https://leetcode.com/problems/binary-tree-preorder-traversal/) | ☐ | DFS iterative |
| 145 | Easy | Binary Tree Postorder Traversal | [Link](https://leetcode.com/problems/binary-tree-postorder-traversal/) | ☐ | DFS iterative |
| 701 | Medium | Insert into a BST | [Link](https://leetcode.com/problems/insert-into-a-bst/) | ☐ | BST property traversal |
| 450 | Medium | Delete Node in a BST | [Link](https://leetcode.com/problems/delete-node-in-a-bst/) | ☐ | BST restructuring |
| 427 | Medium | Construct Quad Tree | [Link](https://leetcode.com/problems/construct-quad-tree/) | ☐ | Divide and conquer |
| 337 | Medium | House Robber III | [Link](https://leetcode.com/problems/house-robber-iii/) | ☐ | Tree DP |
| 1325 | Medium | Delete Leaves With a Given Value | [Link](https://leetcode.com/problems/delete-leaves-with-a-given-value/) | ☐ | Post-order pruning |

---

## Complexity Reference

| Operation | Binary Tree | BST (balanced) | BST (unbalanced) | Notes |
|-----------|------------|----------------|------------------|-------|
| Search by value | O(n) | O(log n) | O(n) | BST uses property to skip half |
| Insert | O(n) | O(log n) | O(n) | Must find correct position |
| Delete | O(n) | O(log n) | O(n) | Find + restructure |
| Inorder traversal | O(n) | O(n) | O(n) | Must visit all nodes |
| Find min / max | O(n) | O(log n) | O(n) | BST: go all left / all right |
| Height / depth | O(n) | O(n) | O(n) | No shortcut without metadata |
| Level order (BFS) | O(n) | O(n) | O(n) | Queue processes every node |
| Lowest Common Ancestor | O(n) | O(log n) | O(n) | BST uses val comparisons |

---

## Data Structures

### Binary Tree

Each node stores a value plus two child pointers (`left` and `right`), either of which may be `None`. Unlike a BST, there is no ordering guarantee — a node's value can be anything relative to its children. The structure is defined entirely by shape (parent-child relationships). Height of a balanced binary tree is O(log n); a degenerate tree (each node has exactly one child) has height O(n).

```
            1              ← root (depth 0)
           / \
          2   3            ← depth 1
         / \   \
        4   5   6          ← depth 2 (leaves: 4, 5, 6)
```

**When it matters:** The tree's shape determines traversal cost. A balanced tree with n nodes has at most log₂(n) levels, so path-from-root operations stay fast. An unbalanced tree can degrade to a linked list.

### Binary Search Tree (BST)

A binary tree with the invariant: for every node, all values in its left subtree are strictly less than the node's value, and all values in its right subtree are strictly greater. This lets you discard half the tree at each step during search — O(log n) on a balanced BST. Inorder traversal of a BST always produces values in ascending sorted order.

```
            8
           / \
          3   10
         / \    \
        1   6    14
           / \   /
          4   7 13

Inorder: 1, 3, 4, 6, 7, 8, 10, 13, 14  ← always sorted
```

**When it matters:** Use BST ordering during validation (#98), LCA (#235), kth smallest (#230), and insert/delete (#701, #450). When you need to check if a value belongs in the left or right subtree, compare against `node.val` and recurse in only one direction.

### Balanced BST

A BST where the height is kept at O(log n) by structural guarantees (AVL trees, Red-Black trees). Python's standard library does not include one, but the property is important conceptually: an unbalanced BST can degrade to O(n) for all operations. In interviews, "balanced" usually just means the heights of the left and right subtrees differ by at most 1 at every node (#110).

```
Balanced (height = 3):        Unbalanced (height = 5, same nodes):
        4                              1
       / \                              \
      2   6                             2
     / \ / \                             \
    1  3 5  7                             3
                                           \
                                            4
                                             \
                                              5
```

**When it matters:** Height-balanced trees guarantee O(log n) search. When a problem says "BST" without specifying balance, worst-case complexity reverts to O(n).

---

## Core Patterns

### DFS Recursive (Preorder / Inorder / Postorder)
**When to use:** Any problem that asks about paths, subtrees, or values that propagate from children to parent.  
**Complexity:** O(n) time, O(h) space (call stack depth equals tree height h)  
**Problems:** #226, #104, #100, #572, #98, #543, #110, #124, #1448, #1325  
**Common mistake:** Forgetting the base case `if not node: return`. The recursive call on `node.left` or `node.right` will always reach a `None` leaf, so the base case must handle `None`.

```python
def dfs(node):
    if not node:
        return 0             # base case — value that doesn't affect the answer

    left = dfs(node.left)   # postorder: process children before using their results
    right = dfs(node.right)

    return 1 + max(left, right)   # example: maximum depth
```

### BFS / Level Order Traversal
**When to use:** Problems that care about depth, level groupings, or the rightmost/leftmost node at each level.  
**Complexity:** O(n) time, O(n) space (queue holds at most one full level — up to n/2 nodes)  
**Problems:** #102, #199  
**Common mistake:** Using `while q` without capturing `len(q)` at the start of each level — new nodes get appended mid-iteration, corrupting the level boundary.

```python
from collections import deque
q = deque([root])
while q:
    level_size = len(q)          # snapshot before appending children
    for _ in range(level_size):
        node = q.popleft()
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    # all nodes at this depth have been processed
```

### Tree DP (Return Two Values)
**When to use:** The value you report upward differs from the answer you compute locally. Classic signs: "maximum path," "diameter," "can rob this node."  
**Complexity:** O(n) time, O(h) space  
**Problems:** #124, #543, #110, #337  
**Common mistake:** Returning the local answer (e.g. total path through the node) to the parent — the parent can only extend a path going downward in one direction, not the full through-path.

```python
res = float('-inf')             # global answer updated in-place

def dfs(node):
    if not node:
        return 0
    left  = max(dfs(node.left),  0)  # ignore negative-sum subtrees
    right = max(dfs(node.right), 0)

    nonlocal res
    res = max(res, node.val + left + right)  # best path through this node (local)
    return node.val + max(left, right)       # best path extending upward (to parent)
```

### BST Property (Bounds Passing)
**When to use:** Validating a BST, or any problem where you need to enforce the BST invariant across multiple levels, not just parent-child.  
**Complexity:** O(n) time, O(h) space  
**Problems:** #98, #235, #230, #701, #450  
**Common mistake:** Only comparing a node with its direct parent. A node in the right subtree of an ancestor must be greater than that ancestor too — pass min/max bounds downward.

```python
def validate(node, low=float('-inf'), high=float('inf')):
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return (validate(node.left,  low,       node.val) and
            validate(node.right, node.val,  high))
```

### Construct from Traversals
**When to use:** Given preorder and inorder arrays (or similar), rebuild the original tree.  
**Complexity:** O(n) time with an index map, O(n²) without  
**Problems:** #105  
**Common mistake:** Slicing arrays at each call — O(n) per level leads to O(n²) total. Use an index map into the inorder array for O(1) root lookup.

```python
def build(preorder, inorder):
    idx_map = {val: i for i, val in enumerate(inorder)}  # O(1) root lookup

    def helper(pre_l, pre_r, in_l, in_r):
        if pre_l > pre_r:
            return None
        root_val = preorder[pre_l]
        root = TreeNode(root_val)
        mid = idx_map[root_val]        # split point in inorder array
        left_size = mid - in_l
        root.left  = helper(pre_l + 1, pre_l + left_size, in_l, mid - 1)
        root.right = helper(pre_l + left_size + 1, pre_r, mid + 1, in_r)
        return root

    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)
```

---

## Syntax Reference

### TreeNode class

Standard node definition used across all LeetCode tree problems.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# build a tree manually for testing:
root = TreeNode(1, TreeNode(2), TreeNode(3))
```

### Recursive DFS skeleton

The three orderings determine when the current node is processed relative to its children.

```python
def preorder(node):   # root → left → right
    if not node: return
    visit(node)
    preorder(node.left)
    preorder(node.right)

def inorder(node):    # left → root → right (sorted for BST)
    if not node: return
    inorder(node.left)
    visit(node)
    inorder(node.right)

def postorder(node):  # left → right → root (children's results feed the parent)
    if not node: return
    postorder(node.left)
    postorder(node.right)
    visit(node)
```

### Iterative inorder traversal (stack)

Converts recursive inorder DFS to an explicit stack, avoiding Python's recursion limit on large trees.

```python
stack, curr = [], root
while curr or stack:
    while curr:                # push all left children
        stack.append(curr)
        curr = curr.left
    curr = stack.pop()         # process the leftmost unvisited node
    visit(curr)
    curr = curr.right          # move to right subtree and repeat
```

### BFS with deque

`deque.popleft()` is O(1). `list.pop(0)` is O(n) and makes BFS O(n²) — always use `deque` for queues.

```python
from collections import deque
q = deque([root])
while q:
    node = q.popleft()
    if node.left:  q.append(node.left)
    if node.right: q.append(node.right)
```

### nonlocal for shared mutable state

When a recursive helper needs to update a value in the enclosing scope (e.g. a global max), use `nonlocal`. Without it, assignment creates a new local variable and the outer value is never updated.

```python
res = float('-inf')

def dfs(node):
    nonlocal res         # without this, res = ... creates a local variable
    if not node:
        return 0
    left  = dfs(node.left)
    right = dfs(node.right)
    res = max(res, left + node.val + right)
    return node.val + max(left, right)
```

### Passing bounds downward (BST validation)

Avoids the parent-only comparison mistake by threading min/max constraints through every recursive call.

```python
def is_valid(node, lo=float('-inf'), hi=float('inf')):
    if not node:
        return True
    if not (lo < node.val < hi):   # must satisfy BOTH bounds, not just parent
        return False
    return (is_valid(node.left,  lo,       node.val) and
            is_valid(node.right, node.val, hi))
```

### Collecting right-side view (#199)

BFS makes level boundaries obvious. The last node dequeued at each level is the rightmost visible node.

```python
from collections import deque
result = []
q = deque([root])
while q:
    for i in range(len(q)):
        node = q.popleft()
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    result.append(node.val)   # node is the last popped at this level = rightmost
return result
```
