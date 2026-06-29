# 07. Trees & Binary Search Trees
*DFS = base → recurse → combine. BFS = level by level.*

[← Prev](06-linked-list.md) · [🗺 Roadmap](../roadmap.md) · [Next →](08-tries.md)

---

Trees are where recursion finally clicks. Almost every tree problem follows the same shape: handle the base case (usually `None`), recurse on the children, then combine their results. A **binary search tree** adds an ordering invariant that turns search into a form of binary search. Learn to *see* the recursion and the code writes itself.

## Concept

### Binary Tree

```
  Binary Tree:               Terminology:
       1                     ┌─────────────────────────┐
      / \                    │ root    = node with no   │
     2   3                   │          parent (1)       │
    / \   \                  │ leaf    = node with no   │
   4   5   6                 │          children (4,5,6) │
                             │ height  = longest path   │
  Node structure:            │          from root→leaf  │
  ┌──────┬──────┬──────┐     │ depth   = distance from  │
  │ val  │ left │ right│     │          root to node    │
  └──────┴──────┴──────┘     └─────────────────────────┘

  Traversals (on tree above):
  Inorder   (L→root→R): 4, 2, 5, 1, 3, 6
  Preorder  (root→L→R): 1, 2, 4, 5, 3, 6
  Postorder (L→R→root): 4, 5, 2, 6, 3, 1
  Level-order (BFS):    1, 2, 3, 4, 5, 6
```

**What it is:** A hierarchical structure where each node has at most two children: `left` and `right`. There are no ordering guarantees (unlike BST).

**Key Properties:**
- Height of a balanced tree: O(log n)
- Height of a skewed tree (worst case): O(n)
- Inorder traversal of a BST yields sorted order
- Most tree problems are solved with DFS (recursion) or BFS (queue)

**Complexity (balanced):**

| Operation | Time |
|-----------|------|
| Access | O(log n) |
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Traversal (all nodes) | O(n) |
| Space (balanced) | O(log n) stack space |

**Use when:**
- The problem has hierarchical or parent-child relationships
- You need to explore all paths (DFS) or process level by level (BFS)
- Representing expression trees, file systems, decision trees

**Python:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS - Inorder (recursive)
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# BFS - Level order
from collections import deque
def level_order(root):
    if not root:
        return []
    q, result = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

### Binary Search Tree

```
  Valid BST:                 BST Property:
       8                     For every node N:
      / \                    ┌─────────────────────────────────┐
     3   10                  │ All nodes in LEFT subtree  < N  │
    / \    \                 │ All nodes in RIGHT subtree > N  │
   1   6    14               │ No duplicates (by convention)   │
      / \   /                └─────────────────────────────────┘
     4   7 13
                             Inorder: 1, 3, 4, 6, 7, 8, 10, 13, 14
                             Always sorted!
```

**What it is:** A Binary Tree with the invariant that every left subtree contains only values less than the node, and every right subtree contains only values greater. Inorder traversal always yields sorted order.

**Key Properties:**
- Inorder traversal = sorted sequence (extremely useful)
- O(log n) operations when balanced (AVL, Red-Black tree); O(n) when skewed
- Python does not have a built-in balanced BST — use `sortedcontainers.SortedList` if needed

**Complexity (balanced):**

| Operation | Time |
|-----------|------|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Min / Max | O(log n) |
| Inorder traversal | O(n) |

**Use when:**
- You need sorted data with fast insert/search/delete
- Finding kth smallest/largest element
- Validating BST structure
- Range queries (find all values between lo and hi)

**Python:**
```python
# Search in BST
def search(root, target):
    if not root:
        return None
    if target == root.val:
        return root
    elif target < root.val:
        return search(root.left, target)
    else:
        return search(root.right, target)

# Inorder → sorted list
def inorder(root, result=[]):
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
```

## The Pattern — DFS on trees

Almost every tree problem is the same three lines of thought, applied recursively:

1. **Base case** — an empty subtree (`None`) returns the trivial answer (0, `True`, `None`…).
2. **Recurse** — solve the left and right children the same way.
3. **Combine** — build this node's answer from its children's answers.

```python
def solve(node):
    if not node:                 # 1. base case
        return ...
    left  = solve(node.left)     # 2. recurse
    right = solve(node.right)
    return combine(node, left, right)   # 3. combine
```

Max depth, "is this balanced", path sums, and subtree checks are all just different `combine`
steps. When you instead need to go **level by level** (e.g. level-order, shortest path), reach for
**BFS with a queue** (see [Lesson 11 — Graphs](11-graphs.md)).

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/trees/`](../appendix/templates/trees/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/trees/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Trees & Binary Search Trees problems →**](../../lists/recommended.md#7-trees-29-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Tries](08-tries.md) — prefix trees: O(k) prefix queries, the dictionary stored once.

[← Prev](06-linked-list.md) · [🗺 Roadmap](../roadmap.md) · [Next →](08-tries.md)

