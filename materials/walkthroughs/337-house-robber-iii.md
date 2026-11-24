# 337. House Robber III

**Medium** · [LeetCode](https://leetcode.com/problems/house-robber-iii/) · [Solution file (no hints)](../../problems/0001-0499/337.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

The houses form a **binary tree**. Each node's value is the money in that house. If you rob two **directly linked** houses (a parent and its child), the police are alerted. Return the **maximum amount** you can rob without robbing a parent and its child.

```
      3
     / \
    2   3          rob 3 + 3 + 1 = 7
     \   \
      3   1

      3
     / \
    4   5          rob 4 + 5 = 9   (skip the root)
   / \   \
  1   3   1
```

**Constraints:** `1 <= nodes <= 10⁴` · `0 <= Node.val <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| houses in a **binary tree** | The "adjacent" constraint is now parent-child, not neighbours in an array |
| "can't rob two directly linked houses" | If you take a node, you **must skip both of its children**. Their children (the grandchildren) are free again |
| "maximum amount" | An optimisation over *choices at each node*: classic DP |
| values `>= 0` | No negatives, so more houses is never worse. You never need to "skip for the sake of it" except when forced |

For one node there are exactly two choices:

- **Rob it:** `node.val` + best of the grandchildren subtrees, because both children are off-limits.
- **Skip it:** the best of the left subtree + the best of the right subtree, and each child is free to be robbed or skipped.

The trap is recomputing. A recursion that asks about grandchildren separately re-solves the same subtrees many times: exponential.

**The fix:** make each call return **both answers at once**: `(best if I rob this node, best if I skip this node)`. The parent then reads straight from its children's pairs. No memo table, no repeated work.

🤔 **Before you open the next section:** if a child returns `(rob, skip)`, what does the parent use for its own "rob" total, and what for its own "skip" total?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Plain recursion: `max(val + grandchildren, children)` | O(2ⁿ) | O(h) | ❌ Recomputes subtrees. Each node is reached through several routes |
| Recursion + memo (`dict` keyed by node) | O(n) | O(n) | ✅ Correct, with a hash map to explain |
| **Post-order DFS returning `(rob, skip)`** | **O(n)** | **O(h)** | ✅ The same DP with no table |

**The decision: a [DFS](../algorithms/dfs.md) that returns a pair.** This is [House Robber](198-house-robber.md) turned into a tree. In the array version, the DP state was "best if I rob here / best if I don't". Here the same two-state idea is computed bottom-up through the tree: it's [dynamic programming](../algorithms/dynamic-programming.md) on a [binary tree](../data-structures/binary-tree.md).

For a node with children results `(l_rob, l_skip)` and `(r_rob, r_skip)`:

- **rob this node:** `node.val + l_skip + r_skip` (children must be skipped)
- **skip this node:** `max(l_rob, l_skip) + max(r_rob, r_skip)` (each child is independent)

The answer is `max(rob, skip)` at the root.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def rob(self, root: Optional[TreeNode]) -> int:
    def dfs(node):
        if not node:
            return (0, 0)
```

`dfs` returns `(rob_this, skip_this)` for the subtree at `node`. An empty subtree has nothing to rob, so `(0, 0)`. This also lets leaf nodes work without special cases.
→ [none-type](../syntax/none-type.md) · [multiple-return-values](../syntax/multiple-return-values.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)
```

**Post-order:** solve both children *first*, so their answers exist before we compute our own. Tuple unpacking splits each pair.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [binary-tree](../data-structures/binary-tree.md)

```python
        rob_this = node.val + left_skip + right_skip
        skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)
        return (rob_this, skip_this)
```

**The two choices.** Robbing this house forces both children to be skipped, so add their `skip` totals. Skipping this house frees each child: take the better of each child's two options.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    return max(dfs(root))
```

At the root, the best overall is the larger of the two choices. `max` works directly on the tuple.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return (0, 0)

            left_rob, left_skip = dfs(node.left)
            right_rob, right_skip = dfs(node.right)

            rob_this = node.val + left_skip + right_skip
            skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)
            return (rob_this, skip_this)

        return max(dfs(root))
```

</details>

**Trace it.** The tree `3 → (4 → (1, 3), 5 → (None, 1))`:

| Node | Children's `(rob, skip)` | `rob_this` | `skip_this` |
|---|---|---|---|
| leaf 1 | `(0,0)`, `(0,0)` | 1 | 0 |
| leaf 3 | `(0,0)`, `(0,0)` | 3 | 0 |
| leaf 1 (under 5) | | 1 | 0 |
| 4 | `(1,0)`, `(3,0)` | 4 + 0 + 0 = **4** | max(1,0) + max(3,0) = **4** |
| 5 | `(0,0)`, `(1,0)` | 5 + 0 + 0 = **5** | 0 + max(1,0) = **1** |
| root 3 | `(4,4)`, `(5,1)` | 3 + 4 + 1 = **8** | max(4,4) + max(5,1) = **9** |

`max(8, 9) = 9` ✅ (rob 4 and 5, skip the root).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each node is visited exactly once, and does a constant amount of work (two additions, two `max` calls). The naive recursion visits the same subtrees repeatedly and goes exponential.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack, where `h` is the tree's height: **O(log n)** if balanced, **O(n)** for a skewed tree. The pair `(rob, skip)` is O(1) per frame, and there is no memo table.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "At each node I either rob it or I don't. If I rob it, both children are off-limits, so I add the children's skip values. If I don't, each child is independent, so I take the best of each child's two options. To avoid recomputing grandchildren, my DFS returns a pair, `(best if robbed, best if skipped)`, for every subtree. Each node is visited once, so O(n) time, and the stack is O(height)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just `max(val + grandchildren, children)`?" | It's correct but exponential, since subtrees are revisited. Memoising by node makes it O(n), and the pair-returning version avoids the table |
| "How's this related to House Robber I and II?" | [House Robber](198-house-robber.md) is the same two-state DP on an array. [House Robber II](213-house-robber-ii.md) makes the array circular |
| "Iterative version?" | Do a post-order traversal with an explicit stack and a dict from node to its pair |
| "Return the houses robbed, not the sum?" | Store the choices as you go and backtrack from the root |
| "Negative values?" | Then skipping a house can be strictly better. The formulas still hold, with `max(…, 0)` for empty subtrees already giving 0 |

**Traps:**

- **Using `max(left)` instead of the pair** for "skip this node". Children aren't forced to be robbed or skipped.
- **Using `left_rob` in `rob_this`.** Robbing a child next to a robbed parent is exactly what's forbidden.
- **Forgetting the base case.** `None` must return `(0, 0)`, not `0`, or the unpacking crashes.
- **A greedy "rob the larger level"** fails. The best choice can be an uneven mix.

**This same move shows up in:** [House Robber](198-house-robber.md) (the array version) · [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) (post-order combine of child results) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md).

</details>

---
