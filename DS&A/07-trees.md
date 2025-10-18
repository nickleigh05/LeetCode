# Trees

## What is a Tree?
A tree is a hierarchical data structure consisting of nodes connected by edges. It has a root node and child nodes, forming a parent-child relationship. Unlike linear data structures, trees are non-linear.

## Tree Terminology

```
         1  ← Root (top node)
        /│\
       / │ \
      2  3  4  ← Children of 1
     /│     │\
    5 6     7 8  ← Leaf nodes (no children)

Terms:
- Root: Node with no parent (1)
- Parent: Node with children (1, 2, 4)
- Child: Node with a parent (2, 3, 4, 5, 6, 7, 8)
- Leaf: Node with no children (5, 6, 3, 7, 8)
- Sibling: Nodes with same parent (2, 3, 4 are siblings)
- Ancestor: All nodes on path from root to node
- Descendant: All nodes in subtree of a node

Height: Longest path from node to leaf
Depth: Distance from root to node
Level: Depth + 1
```

## Binary Tree
A tree where each node has at most 2 children (left and right).

```
         1
        / \
       2   3
      / \   \
     4   5   6

Node structure:
┌────────────┐
│   data     │
│   left  ●──┼──→ (left child)
│   right ●──┼──→ (right child)
└────────────┘
```

### Types of Binary Trees

#### 1. Full Binary Tree
Every node has 0 or 2 children:

```
       1
      / \
     2   3
    / \
   4   5

✓ Full: All nodes have 0 or 2 children

       1
      / \
     2   3
    /
   4

✗ Not Full: Node 2 has only 1 child
```

#### 2. Complete Binary Tree
All levels are filled except possibly the last, which is filled left to right:

```
✓ Complete:
       1
      / \
     2   3
    / \  /
   4  5 6

✗ Not Complete:
       1
      / \
     2   3
    /     \
   4       6
(Missing left child at level 2)
```

#### 3. Perfect Binary Tree
All internal nodes have 2 children and all leaves are at the same level:

```
✓ Perfect:
       1
      / \
     2   3
    / \ / \
   4  5 6  7

Nodes = 2^h - 1 (h = height)
```

#### 4. Balanced Binary Tree
Height difference between left and right subtrees ≤ 1 for all nodes:

```
✓ Balanced:
       1          height diff ≤ 1
      / \
     2   3
    /
   4

✗ Unbalanced:
       1
      /
     2           height diff > 1
    /
   3
   /
  4
```

## Binary Search Tree (BST)
For each node:
- All left descendants < node
- All right descendants > node

```
         8
        / \
       3   10
      / \    \
     1   6   14
        / \  /
       4  7 13

Properties:
- Inorder traversal gives sorted array
- Search: O(log n) average, O(n) worst
- Insert/Delete: O(log n) average
```

### BST Operations

#### Search
```
Search for 6 in BST:

Step 1: Start at root (8)
         8  ← 6 < 8, go left
        / \
       3   10
      / \    \
     1   6   14
        / \  /
       4  7 13

Step 2: At 3
       3  ← 6 > 3, go right
      / \
     1   6
        / \
       4  7

Step 3: At 6
       6  ← Found! ✓
      / \
     4  7
```

#### Insert
```
Insert 5 into BST:

         8  ← 5 < 8, go left
        / \
       3   10
      / \    \
     1   6   14
        / \  /
       4  7 13

     3  ← 5 > 3, go right
    / \
   1   6
      / \
     4  7

       6  ← 5 < 6, go left
      / \
     4  7

     4  ← 5 > 4, insert right
Result:
     4
      \
       5  ← New node
```

## Tree Traversals

### 1. Depth-First Search (DFS)

#### Inorder (Left → Root → Right)
```
       1
      / \
     2   3
    / \
   4   5

Traversal: 4, 2, 5, 1, 3

Visual execution:
1. Visit left: go to 2
2. Visit left of 2: go to 4
3. No left of 4: print 4 ✓
4. Back to 2: print 2 ✓
5. Visit right of 2: print 5 ✓
6. Back to 1: print 1 ✓
7. Visit right of 1: print 3 ✓

For BST: Gives sorted order!
```

#### Preorder (Root → Left → Right)
```
       1
      / \
     2   3
    / \
   4   5

Traversal: 1, 2, 4, 5, 3

Visual execution:
1. Print 1 ✓
2. Go left: print 2 ✓
3. Go left: print 4 ✓
4. Go right: print 5 ✓
5. Back to 1, go right: print 3 ✓

Used for: Tree copying, prefix expressions
```

#### Postorder (Left → Right → Root)
```
       1
      / \
     2   3
    / \
   4   5

Traversal: 4, 5, 2, 3, 1

Visual execution:
1. Go to leftmost: 4, print 4 ✓
2. Back to 2, go right: 5, print 5 ✓
3. Print 2 ✓
4. Go to 3: print 3 ✓
5. Print 1 ✓

Used for: Deleting tree, postfix expressions
```

### 2. Breadth-First Search (BFS) / Level Order

```
       1
      / \
     2   3
    / \   \
   4   5   6

Level 0: 1
Level 1: 2, 3
Level 2: 4, 5, 6

Traversal: 1, 2, 3, 4, 5, 6

Using Queue:
Start: [1]
Pop 1, add children: [2, 3]
Pop 2, add children: [3, 4, 5]
Pop 3, add children: [4, 5, 6]
Pop 4: [5, 6]
Pop 5: [6]
Pop 6: []

Result: 1, 2, 3, 4, 5, 6
```

## Common Tree Problems

### 1. Maximum Depth
```
       1
      / \
     2   3
    /
   4

Depth calculation:
At 4: depth = 1 (leaf)
At 2: depth = 1 + max(left, right) = 1 + 1 = 2
At 3: depth = 1 (leaf)
At 1: depth = 1 + max(2, 1) = 3

Maximum depth = 3
```

### 2. Validate BST
```
Check if valid BST:

       5
      / \
     3   7
    / \
   2   4

For each node, check:
- left subtree max < node
- right subtree min > node

At 5:
  Left max (4) < 5 ✓
  Right min (7) > 5 ✓

At 3:
  Left max (2) < 3 ✓
  Right min (4) > 3 ✓

Valid BST ✓

Invalid example:
       5
      / \
     3   7
    / \
   2   6  ← 6 > 5, but in left subtree!

Invalid BST ✗
```

### 3. Lowest Common Ancestor (LCA)
```
       1
      / \
     2   3
    / \
   4   5

Find LCA of 4 and 5:

Path to 4: 1 → 2 → 4
Path to 5: 1 → 2 → 5

Common ancestors: 1, 2
Lowest: 2 ✓

Find LCA of 4 and 3:

Path to 4: 1 → 2 → 4
Path to 3: 1 → 3

Common ancestors: 1
Lowest: 1 ✓
```

### 4. Serialize and Deserialize
```
Tree:
       1
      / \
     2   3
        / \
       4   5

Serialize (Preorder): "1,2,null,null,3,4,null,null,5,null,null"

Visual:
1 → add "1"
├─ 2 → add "2"
│  ├─ null → add "null"
│  └─ null → add "null"
└─ 3 → add "3"
   ├─ 4 → add "4"
   │  ├─ null → add "null"
   │  └─ null → add "null"
   └─ 5 → add "5"
      ├─ null → add "null"
      └─ null → add "null"

Deserialize: Build tree from string
```

### 5. Path Sum
```
Find if path sum equals target (22):

       5
      / \
     4   8
    /   / \
   11  13  4
   / \      \
  7   2      1

Path 5→4→11→2:
5 + 4 + 11 + 2 = 22 ✓

Path 5→8→4→1:
5 + 8 + 4 + 1 = 18 ✗
```

## Advanced Tree Structures

### AVL Tree (Self-Balancing BST)
```
Maintains balance factor: |height(left) - height(right)| ≤ 1

Imbalanced (needs rotation):
     3
      \
       4
        \
         5

After right rotation:
       4
      / \
     3   5

Balance factor at each node:
4: |1 - 1| = 0 ✓
3: |0 - 0| = 0 ✓
5: |0 - 0| = 0 ✓
```

### Red-Black Tree
```
Properties:
1. Every node is red or black
2. Root is black
3. Leaves (null) are black
4. Red nodes have black children
5. All paths from root to leaves have same # of black nodes

Example:
       B(10)
       /    \
    R(5)    R(15)
    / \      / \
  B(3) B(7) B(12) B(17)
```

### Trie (Prefix Tree)
See separate Tries section for details.

## Binary Tree vs Binary Search Tree

```
Binary Tree (any structure):
       5
      / \
     3   8
    / \
   9   1

Binary Search Tree (ordered):
       5
      / \
     3   8
    / \
   1   4

BST advantages:
- Fast search: O(log n) average
- Inorder gives sorted array
- Efficient insert/delete
```

## Time Complexity

| Operation | Average | Worst (unbalanced) |
|-----------|---------|-------------------|
| Search    | O(log n)| O(n)             |
| Insert    | O(log n)| O(n)             |
| Delete    | O(log n)| O(n)             |
| Traversal | O(n)    | O(n)             |

Balanced trees (AVL, Red-Black): O(log n) guaranteed

## Space Complexity

- Tree storage: O(n)
- DFS (recursion): O(h) where h = height
- BFS (queue): O(w) where w = max width
- Balanced tree: h = O(log n)
- Skewed tree: h = O(n)

## Python Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Inorder traversal
def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

# Level order traversal
from collections import deque

def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result

# BST insert
def insert_bst(root, val):
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)

    return root

# BST search
def search_bst(root, val):
    if not root or root.val == val:
        return root

    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)
```

## Key Takeaways

1. **Structure**: Hierarchical, non-linear
2. **Types**: Binary, BST, AVL, Red-Black, etc.
3. **Traversals**:
   - DFS: Inorder, Preorder, Postorder
   - BFS: Level order

4. **BST Properties**:
   - Left < Root < Right
   - Inorder → sorted
   - O(log n) operations (if balanced)

5. **Common Patterns**:
   - Recursion for tree problems
   - Two pointers (in linked list form)
   - Level order with queue
   - Path problems with backtracking

6. **When to Use**:
   - Hierarchical data (file systems, org charts)
   - Fast search/insert/delete (BST)
   - Priority queues (heap)
   - Routing algorithms
