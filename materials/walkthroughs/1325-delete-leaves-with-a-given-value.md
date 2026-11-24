# 1325. Delete Leaves With a Given Value

**Medium** · [LeetCode](https://leetcode.com/problems/delete-leaves-with-a-given-value/) · [Solution file (no hints)](../../problems/1000-1499/1325.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a binary tree and an integer `target`, delete **every leaf whose value equals `target`**. Deleting a leaf can turn its parent into a new leaf. If that parent's value is also `target`, delete it too. Keep going until no such leaf remains. Return the root of the resulting tree.

```
root = [1, 2, 3, 2, null, 2, 4],  target = 2  →  [1, null, 3, null, 4]

        1                      1
       / \                      \
      2   3        becomes       3
     /   / \                      \
    2   2   4                      4
```

The two leaf `2`s go first. That turns the left `2` into a leaf, so it goes too.

**Constraints:** `1 <= nodes <= 3000` · `1 <= Node.val, target <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "delete **leaves** with value `target`" | A leaf is a node with no children. Only those can be removed directly |
| "deleting a leaf may create a **new leaf**" | A parent's fate depends on **what happened to its children**. Children must be processed first |
| "keep going until none remain" | You don't need to loop. One bottom-up pass handles every cascade |
| "return the root" | The *root itself* may be deleted, so the function must **return the (possibly new) subtree root** |

The shape of the solution follows from the cascade. A node becomes deletable only after its children have been cleaned. That's a **post-order** traversal: left, right, then the node.

**The trick for deleting in a tree:** a node can't delete itself. Its parent has to drop the reference. So make the function **return** what should be there: either the node (keep it) or `None` (delete it). The parent writes the answer back with `node.left = f(node.left)`.

🤔 **Before you open the next section:** after cleaning both children, what exactly makes the current node a deletable leaf?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Repeat: scan for target leaves, delete, until none change | Each pass removes one layer | O(n · h) | O(h) | ❌ Wasteful and fiddly |
| Pre-order (check the node first) | You'd test "is leaf" before the children are cleaned: **wrong**, the cascade is missed | | | ❌ |
| **Post-order recursion that returns the new subtree** | Clean children, then decide about self | **O(n)** | O(h) | ✅ |

**The decision: [DFS](../algorithms/dfs.md) in post-order, returning the (possibly `None`) replacement.** See [tree traversal orders](../algorithms/tree-traversal-orders.md) for why post-order is the one that fits "children first".

Each call does three things, in this order:

1. If the node is `None`, return `None`.
2. Recursively clean the left and right subtrees, **assigning the results back**.
3. If the node is now a leaf and its value is `target`, return `None`. Otherwise return the node.

Step 2's assignment is what makes the cascade work: if both children vanish, the node's `left` and `right` are `None` by the time step 3 runs, so it counts as a leaf.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
    if root is None:
        return None
```

**Base case.** Nothing to clean in an empty subtree. Returning `None` also means "no child here", which the parent stores as is.
→ [none-type](../syntax/none-type.md) · [if-return](../syntax/if-return.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    root.left = self.removeLeafNodes(root.left, target)
    root.right = self.removeLeafNodes(root.right, target)
```

**Clean the children first, and keep the result.** If the left child was a target leaf, the call returns `None` and `root.left` becomes `None`: the deletion happens right here, performed by the parent. Both subtrees are fully cleaned before we look at the current node.
→ [binary-tree](../data-structures/binary-tree.md) · [tree-traversal-orders](../algorithms/tree-traversal-orders.md)

```python
    if root.left is None and root.right is None and root.val == target:
        return None
```

**Now decide about this node.** After the children are cleaned, "no children" is checked on the *updated* pointers, so a parent whose only children were deleted counts as a leaf. If its value is `target`, delete it by returning `None`.
→ [logical-operators](../syntax/logical-operators.md) · [identity-operators](../syntax/identity-operators.md)

```python
    return root
```

Otherwise keep the node, with its cleaned subtrees attached.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        if root is None:
            return None

        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        if root.left is None and root.right is None and root.val == target:
            return None

        return root
```

</details>

**Trace it.** Tree `1 → (2 → (2, None), 3 → (2, 4))`, `target = 2`:

| Call | After children | Leaf and `== 2`? | Returns |
|---|---|---|---|
| inner `2` (left of left) | no children | leaf, value 2: yes | `None` |
| outer `2` (left child of 1) | `left = None`, `right = None` | now a leaf, value 2: yes | `None` |
| `2` (left of 3) | no children | yes | `None` |
| `4` | no children | leaf, but 4 ≠ 2 | the node |
| `3` | `left = None`, `right = 4` | not a leaf | the node |
| `1` | `left = None`, `right = 3` | not a leaf | the node |

Result: `1 → (None, 3 → (None, 4))` ✅. The outer `2` only disappeared **because** its child did first.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Every node is visited exactly once, with O(1) work each. The cascading deletions come for free from the post-order. The repeated-scan alternative is O(n · h).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** recursion stack, where `h` is the height: O(log n) for a balanced tree, O(n) for a chain. No extra data structures.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Deleting a leaf can expose a new leaf above it, so children have to be processed before parents: post-order. A node can't remove itself, so the function returns what should occupy that slot, the node or `None`, and the parent assigns it back. For each node I clean the left and right subtrees, reassign them, and then if it has no children and its value equals the target, I return `None`. One pass, O(n) time, O(height) stack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Iterative version?" | Post-order with a stack and a parent map, or process nodes in reverse level order and prune |
| "What if the whole tree is deleted?" | The root call returns `None`, and the caller must handle an empty tree |
| "Delete *all* nodes with the target value, not just leaves?" | That's a different problem: removing an inner node requires re-attaching its children |
| "Why not check the leaf condition before recursing?" | The children haven't been cleaned yet, so you'd miss cascades like `2 → 2` |
| "Related?" | [Invert Binary Tree](226-invert-binary-tree.md) · [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) · [Delete Node in a BST](450-delete-node-in-a-bst.md) |

**Traps:**

- **Not assigning the recursive results** (`self.removeLeafNodes(root.left, target)` on its own line). Nothing is ever detached.
- **Checking the leaf condition before recursing.** The cascade disappears.
- **Forgetting that the root can be deleted.** Return the result of the call, not the original `root`.
- **Testing `root.left` instead of `root.left is None`**: a `TreeNode` is always truthy, but be explicit.

**This same move shows up in:** [Invert Binary Tree](226-invert-binary-tree.md) · [Delete Node in a BST](450-delete-node-in-a-bst.md) (return the replacement subtree) · [Balanced Binary Tree](110-balanced-binary-tree.md) (children first, then decide).

</details>

---
