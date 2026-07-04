# 07. Trees — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md)

---

### 226. Invert Binary Tree — Easy
[LeetCode](https://leetcode.com/problems/invert-binary-tree/)  
[Solution file (no hints)](../../problems/0001-0499/226.py)

Flip a [binary tree](../data-structures/binary-tree.md) into its mirror image. If you already knew how to invert both of a node's subtrees, what one extra step turns that into inverting the whole tree?

<details>
<summary>Hint</summary>

DFS base case + recurse: recursively invert the left and right subtrees, then swap them at the current node (see [DFS](../algorithms/dfs.md)).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:

        if root is None:
            return None

        left_subtree = self.invertTree(root.left)
        right_subtree = self.invertTree(root.right)

        root.left = right_subtree
        root.right = left_subtree

        return root
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [identity-operators](../syntax/identity-operators.md) (`is None`) · [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 104. Maximum Depth of Binary Tree — Easy
[LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/)  
[Solution file (no hints)](../../problems/0001-0499/104.py)

Find the max depth of a [binary tree](../data-structures/binary-tree.md). If you knew the depth of the left and right subtrees, how would you combine them into the depth of the whole tree?

<details>
<summary>Hint</summary>

DFS base case + recurse + combine (see [DFS](../algorithms/dfs.md)): depth of a node is 1 plus the larger of its two subtrees' depths.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:

        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 543. Diameter of Binary Tree — Easy
[LeetCode](https://leetcode.com/problems/diameter-of-binary-tree/)  
[Solution file (no hints)](../../problems/0500-0999/543.py)

Find the longest path between any two nodes in a [binary tree](../data-structures/binary-tree.md) (not necessarily through the root). Why is it not enough to just compute depth — what extra value must you track *while* computing depth?

<details>
<summary>Hint</summary>

While computing each node's depth via DFS (see [DFS](../algorithms/dfs.md)), also check whether `left_depth + right_depth` at that node beats the best diameter seen so far — the longest path always passes through some node as its "peak."
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:

        self.best = 0

        def depth(node):
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            self.best = max(self.best, left + right)
            return max(left, right) + 1

        depth(root)
        return self.best
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) (`self.best`) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 110. Balanced Binary Tree — Easy
[LeetCode](https://leetcode.com/problems/balanced-binary-tree/)  
[Solution file (no hints)](../../problems/0001-0499/110.py)

Determine if a [binary tree](../data-structures/binary-tree.md) is height-balanced (every node's subtrees differ in height by at most 1). How do you avoid recomputing height over and over by bailing out early once you find an imbalance?

<details>
<summary>Hint</summary>

Have your DFS helper (see [DFS](../algorithms/dfs.md)) return height, but use a sentinel like `-1` to mean "already found unbalanced," so an imbalance anywhere short-circuits the whole recursion.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        def height(node):
            if not node:
                return 0
            left = height(node.left)
            if left == -1:
                return -1
            right = height(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return max(left, right) + 1

        return height(root) != -1
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`abs()`, `max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once, thanks to the -1 short-circuit avoiding recomputation.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 100. Same Tree — Easy
[LeetCode](https://leetcode.com/problems/same-tree/)  
[Solution file (no hints)](../../problems/0001-0499/100.py)

Check if two [binary trees](../data-structures/binary-tree.md) are structurally identical with the same values. What are the base cases you need to handle before you can safely recurse on both children?

<details>
<summary>Hint</summary>

DFS both trees together (see [DFS](../algorithms/dfs.md)): if both nodes are `None`, they match; if only one is `None`, or the values differ, they don't; otherwise recurse on both left and right pairs.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [identity-operators](../syntax/identity-operators.md) (`is None`) · [logical-operators](../syntax/logical-operators.md) (`and`, `or`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node in the smaller tree is visited at most once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 572. Subtree of Another Tree — Easy
[LeetCode](https://leetcode.com/problems/subtree-of-another-tree/)  
[Solution file (no hints)](../../problems/0500-0999/572.py)

Determine if one tree is a subtree of another. How does reusing "are these two trees the same" ([100](#100-same-tree--easy)) at every node of the bigger tree solve this?

<details>
<summary>Hint</summary>

Walk the bigger tree with DFS (see [DFS](../algorithms/dfs.md)); at each node, check whether the subtree rooted there is identical to the target using the same-tree check from [100](#100-same-tree--easy).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:

        def same_tree(p, q):
            if not p and not q:
                return True
            if not p or not q or p.val != q.val:
                return False
            return same_tree(p.left, q.left) and same_tree(p.right, q.right)

        if not root:
            return subRoot is None
        if same_tree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md) (`or`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — in the worst case, the same-tree check (O(m)) runs at every node of the bigger tree (n nodes).
**Space: O(h)** — recursion stack depth equals the bigger tree's height h.
</details>

---

### 235. Lowest Common Ancestor of a Binary Search Tree — Medium
[LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)  
[Solution file (no hints)](../../problems/0001-0499/235.py)

Find the lowest common ancestor of two nodes in a [BST](../data-structures/binary-search-tree.md). How does the BST ordering property tell you, at any node, which direction both targets must be relative to it?

<details>
<summary>Hint</summary>

If both values are less than the current node, the answer is in the left subtree; if both are greater, it's in the right subtree; otherwise (one on each side, or a match) the current node *is* the LCA.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:

        current = root

        while current:
            if p.val < current.val and q.val < current.val:
                current = current.left
            elif p.val > current.val and q.val > current.val:
                current = current.right
            else:
                return current

        return None
```

Building blocks: [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) (`and`) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(h)** — walks down one path of the tree, h = tree height.
**Space: O(1)** — iterative, no recursion stack.
</details>

---

### 102. Binary Tree Level Order Traversal — Medium
[LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/)  
[Solution file (no hints)](../../problems/0001-0499/102.py)

Return the tree's node values level by level. Why does a queue, rather than a stack, naturally process nodes in the order they were discovered — level by level?

<details>
<summary>Hint</summary>

Run [BFS](../algorithms/bfs.md) with a [queue](../data-structures/queue.md): process one full level at a time by tracking how many nodes are already queued at the start of each level.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for i in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)

            result.append(current_level)

        return result
```

Building blocks: [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is enqueued and dequeued once.
**Space: O(n)** — the queue can hold up to a full level's worth of nodes (up to n/2 for the last level).
</details>

---

### 199. Binary Tree Right Side View — Medium
[LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/)  
Solution: not yet solved in this repo.

Return the values visible from the right side of the tree, top to bottom. In a level-order [BFS](../algorithms/bfs.md), which single node from each level is the one you can see?

<details>
<summary>Hint</summary>

Run [BFS](../algorithms/bfs.md) with a [queue](../data-structures/queue.md) level by level (same shape as [102](#102-binary-tree-level-order-traversal--medium)); the last node processed in each level is the one visible from the right.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:

        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    result.append(node.val)

                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)

        return result
```

Building blocks: [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is enqueued and dequeued once.
**Space: O(n)** — the queue can hold up to a full level's worth of nodes.
</details>

---

### 1448. Count Good Nodes in Binary Tree — Medium
[LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)  
Solution: not yet solved in this repo.

A node is "good" if no ancestor on its path from the root has a greater value. Count the good nodes. What single extra piece of information do you need to carry down the recursion from root to leaves?

<details>
<summary>Hint</summary>

DFS down the tree (see [DFS](../algorithms/dfs.md)), passing along the max value seen on the path so far. A node is good if its value is `>=` that running max; then recurse with the updated max.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:

        def dfs(node, max_so_far):
            if not node:
                return 0

            good = 1 if node.val >= max_so_far else 0
            new_max = max(max_so_far, node.val)

            good += dfs(node.left, new_max)
            good += dfs(node.right, new_max)
            return good

        return dfs(root, root.val)
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [ternary-expression](../syntax/ternary-expression.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 98. Validate Binary Search Tree — Medium
[LeetCode](https://leetcode.com/problems/validate-binary-search-tree/)  
[Solution file (no hints)](../../problems/0001-0499/98.py)

Determine if a tree is a valid [BST](../data-structures/binary-search-tree.md). Why is checking "left child < node < right child" locally at every node *not* sufficient?

<details>
<summary>Hint</summary>

Every node must fall within a valid `(low, high)` range inherited from its ancestors, not just be less than its immediate parent — DFS down while narrowing that range (see [DFS](../algorithms/dfs.md)).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        def validate(node, lower_bound, upper_bound):
            if node is None:
                return True

            if lower_bound is not None and node.val <= lower_bound:
                return False

            if upper_bound is not None and node.val >= upper_bound:
                return False

            left_valid = validate(node.left, lower_bound, node.val)
            right_valid = validate(node.right, node.val, upper_bound)

            return left_valid and right_valid

        return validate(root, None, None)
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [identity-operators](../syntax/identity-operators.md) (`is None` / `is not None`) · [logical-operators](../syntax/logical-operators.md) (`and`) · [none-type](../syntax/none-type.md) (`None` as "no bound yet")
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 230. Kth Smallest Element in a BST — Medium
[LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)  
Solution: not yet solved in this repo.

Find the kth smallest value in a [BST](../data-structures/binary-search-tree.md). What traversal order visits BST nodes in ascending sorted order automatically?

<details>
<summary>Hint</summary>

An inorder traversal (left, node, right — see [tree traversal orders](../algorithms/tree-traversal-orders.md)) of a BST visits nodes in sorted order. Count nodes as you go and stop at the kth.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:

        stack = []
        current = root
        count = 0

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            count += 1
            if count == k:
                return current.val

            current = current.right
```

Building blocks: [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(h + k)** — walk down to the leftmost node (O(h)) then visit k nodes in order.
**Space: O(h)** — the explicit stack holds at most one path's worth of nodes.
</details>

---

### 105. Construct Binary Tree from Preorder and Inorder Traversal — Medium
[LeetCode](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)  
Solution: not yet solved in this repo.

Rebuild a binary tree from its preorder and inorder traversals. Why does preorder always give you the *root* first, while inorder tells you exactly which values are in the left vs. right subtree?

<details>
<summary>Hint</summary>

The first value of preorder is always the current subtree's root (see [tree traversal orders](../algorithms/tree-traversal-orders.md)). Find that value's position in inorder — everything to its left is the left subtree, everything to its right is the right subtree. Recurse on both halves.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])

        root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])

        return root
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [list-methods](../syntax/list-methods.md) (`.index()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — naive `.index()` lookup and slicing cost O(n) at each of n nodes (an O(n) hashmap of value->index brings this to O(n)).
**Space: O(n²)** for the same reason (each recursive call copies slices); O(n) with a hashmap and index-range passing instead of slicing.
</details>

---

### 124. Binary Tree Maximum Path Sum — Hard
[LeetCode](https://leetcode.com/problems/binary-tree-maximum-path-sum/)  
Solution: not yet solved in this repo.

Find the maximum sum path between any two nodes (path need not pass through the root). Why must the value *returned* up the recursion (for the parent to use) differ from the value used to update the *global* best?

<details>
<summary>Hint</summary>

DFS (see [DFS](../algorithms/dfs.md)) returns the best single-direction path down from a node (so a parent can chain onto it), but at each node also checks `left + right + node.val` as a candidate for the best path *through* that node, updating a running global max.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:

        self.best = float("-inf")

        def dfs(node):
            if not node:
                return 0

            left = max(dfs(node.left), 0)
            right = max(dfs(node.right), 0)

            self.best = max(self.best, node.val + left + right)
            return node.val + max(left, right)

        dfs(root)
        return self.best
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) (`self.best`) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [int-float-basics](../syntax/int-float-basics.md) (`float("-inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(h)** — recursion stack depth equals the tree's height h.
</details>

---

### 297. Serialize and Deserialize Binary Tree — Hard
[LeetCode](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)  
Solution: not yet solved in this repo.

Design an algorithm to serialize a tree to a string and deserialize it back. Why does recording `None` markers during a preorder traversal make the string self-describing enough to rebuild the exact tree?

<details>
<summary>Hint</summary>

Serialize with preorder DFS (see [tree traversal orders](../algorithms/tree-traversal-orders.md)), writing `"N"` for every `None` child. Deserialize by consuming that same sequence in order — the preorder + null-markers uniquely determines the tree shape.
</details>

<details>
<summary>Solution</summary>

```python
class Codec:

    def serialize(self, root: Optional[TreeNode]) -> str:
        values = []

        def dfs(node):
            if not node:
                values.append("N")
                return
            values.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(values)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        values = iter(data.split(","))

        def dfs():
            val = next(values)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
```

Building blocks: [class-basics](../syntax/class-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [string-methods](../syntax/string-methods.md) (`.split()`) · [string-join-slice](../syntax/string-join-slice.md) (`",".join()`) · [itertools-basics](../syntax/itertools-basics.md) (`iter()`, `next()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once during both serialize and deserialize.
**Space: O(n)** — the serialized string and the recursion stack both scale with the number of nodes.
</details>
