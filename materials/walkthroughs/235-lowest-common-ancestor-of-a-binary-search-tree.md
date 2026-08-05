# 235. Lowest Common Ancestor of a Binary Search Tree

**Medium** · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · [Solution file (no hints)](../../problems/0001-0499/235.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given a **binary search tree**, find the **lowest common ancestor** (LCA) of two given nodes `p` and `q`.

The LCA is the lowest node that has **both** `p` and `q` as descendants — and a node is allowed to be a descendant of itself.

```
        6
      /   \
     2     8
    / \   / \
   0   4 7   9
      / \
     3   5

p = 2, q = 8  →  6      (they're on opposite sides)
p = 2, q = 4  →  2      (a node can be its own descendant)
```

**Constraints:** `2 <= nodes <= 10⁵` · all values **unique** · `p != q` · both exist in the tree

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary search tree**" | ⚠️ **The whole point.** Not just any tree — left subtree < node < right subtree, everywhere. That ordering is navigational information |
| "**lowest** common ancestor" | The deepest node that still has both below it |
| "a node can be a descendant of **itself**" | If `p` is an ancestor of `q`, the answer is `p` — an easy case to miss |
| values are **unique** | No ambiguity about which node a value refers to |
| both nodes **exist** | No "not found" case to handle |
| n up to 10⁵ | O(n) works, but the BST structure gives you **O(h)** — much better |

**The BST property is the entire solution.** In a BST, comparing a value to a node tells you *which subtree it must be in*. So standing at any node, there are exactly three possibilities:

```
        6            p=2, q=4:  both < 6  →  both in the LEFT subtree,
      /   \                                  so 6 is an ancestor but not the LOWEST
     2     8         p=7, q=9:  both > 6  →  both RIGHT
    / \   / \
   0   4 7   9       p=2, q=8:  one each side  →  6 is where they SPLIT
```

| At the current node | What it means |
|---|---|
| **Both values smaller** | Both are in the left subtree → descend left |
| **Both values larger** | Both are in the right subtree → descend right |
| **They split** (or one *is* this node) | ⚠️ **This node is the LCA** — stop |

That third case is the insight: **the LCA is exactly the node where the two search paths diverge.** Above it, both paths go the same way; at it, they part. And if one target *is* the current node, it can't be beaten — nothing lower could still have it as a descendant.

🤔 **Before you open the next section:** why does "the paths split here" guarantee this is the *lowest* such node, not just *a* common ancestor?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Find both root-to-node paths, compare | Two searches, then walk the paths in parallel | O(h) | **O(h)** | ⚠️ Correct, needs to store paths |
| General-tree LCA recursion | Ignore the BST property, search both subtrees | **O(n)** | O(h) | ⚠️ Works, but throws away the ordering |
| **Walk down using the BST property** | One comparison per level | **O(h)** | **O(1)** iterative | ✅ |

**The decision: a single downward walk from the root, guided by comparisons.**

At each node, compare both target values against it and take one of the three branches above. The loop ends the moment the values split — that node is the answer.

**Why splitting means *lowest*.** Suppose the paths to `p` and `q` diverge at node `X`. Every node **above** `X` is also a common ancestor, but strictly higher. Every node **below** `X` lies in one subtree only — so it can contain at most one of the targets. Therefore `X` is the deepest node containing both. **The divergence point is the LCA by construction**, which is why you can return the instant you detect it and never look further.

**Why the general-tree solution is worth knowing but wrong here.** For an arbitrary binary tree ([LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)) you must search both subtrees and combine — O(n), because without ordering you can't tell where a value lives. That solution *also works* on a BST, and using it here isn't incorrect — it just wastes the structure and costs O(n) instead of O(h). **Interviewers notice.**

**Why iterative rather than recursive.** The recursion here is *tail*-recursive — nothing happens after the recursive call — so it converts to a `while` loop with no stack at all. That takes the space from O(h) to **O(1)**. Most tree problems can't do this because they need to combine children's results on the way back up; this one only ever descends.

**The `else` covers three situations at once**: `p` is on the left and `q` on the right, the reverse, or one of them equals the current node. All three mean "stop here" — no separate checks needed.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
current = root
```

Start at the top and walk down. A plain variable, not a stack — this traversal never needs to come back up.
→ [variables-assignment](../syntax/variables-assignment.md) · [binary-search-tree](../data-structures/binary-search-tree.md)

```python
while current:
```

Descend until the answer is found. Given the problem's guarantee that both nodes exist, the loop always exits via the `return` inside — but the condition keeps it safe.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    if p.val < current.val and q.val < current.val:
        current = current.left
```

**Both targets are smaller** ⇒ by the BST property both live in the left subtree ⇒ the current node is a common ancestor but *not the lowest*. Descend left.

Note it must be `and` — if only one is smaller, they've split and this node is the answer.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    elif p.val > current.val and q.val > current.val:
        current = current.right
```

Mirror image: both larger ⇒ both in the right subtree.
→ [elif-else](../syntax/elif-else.md)

```python
    else:
        return current
```

**The answer.** Reaching this means one of three things, all with the same conclusion:

- `p` is below-left and `q` below-right (or vice versa) — the paths **split here**.
- `p.val == current.val` — `p` is this node, and it's its own descendant.
- `q.val == current.val` — likewise.

In every case, no node lower down can contain both. **Return immediately.**
→ [if-return](../syntax/if-return.md)

```python
return None
```

Unreachable given the problem's guarantees, but a sensible fallback if a target weren't present.
→ [none-type](../syntax/none-type.md)

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — the tree above, `p = 2`, `q = 8`:

| `current` | `p.val` vs | `q.val` vs | Branch |
|---|---|---|---|
| **6** | 2 < 6 | 8 > 6 | **split** → `return 6` ✅ |

One comparison. The root is already the answer because the targets sit on opposite sides.

**A deeper case** — `p = 3`, `q = 5`:

| `current` | 3 vs node | 5 vs node | Branch |
|---|---|---|---|
| 6 | < | < | both left → `current = 2` |
| 2 | > | > | both right → `current = 4` |
| **4** | 3 < 4 | 5 > 4 | **split** → `return 4` ✅ |

**And the self-descendant case** — `p = 2`, `q = 4`:

| `current` | 2 vs node | 4 vs node | Branch |
|---|---|---|---|
| 6 | < | < | both left → `current = 2` |
| **2** | **equal** | > | neither `and` holds → `else` → `return 2` ✅ |

Node 2 is `p` itself, and it's the ancestor of 4 — correctly returned with no special-case code.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h)</summary>

**O(h)**, where h is the tree's height — **O(log n)** for a balanced BST, **O(n)** for a degenerate (chain-shaped) one.

Each iteration does two comparisons and moves down exactly one level. You never revisit a node, never backtrack, and never explore a sibling.

At n = 10⁵ balanced: about **17 iterations**.

**Compare to ignoring the BST property:** the general-tree LCA algorithm searches both subtrees at every node — O(n) = 10⁵. **The ordering turns a full search into a single descent**, the same leverage binary search gets over a linear scan in [problem 704](704-binary-search.md).

Really, this *is* binary search — on a tree instead of an array, with the tree's shape doing the halving.

**Best case O(1):** the targets split at the root, as in the first trace.

**Early exit is guaranteed**, not merely possible: the loop returns at the divergence point rather than descending to a leaf.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — one pointer variable. **This is the only problem in Unit 07 with constant space**, and it's worth understanding why.

Every other tree problem here recurses and pays **O(h)** for the stack, because a node's answer depends on its children's answers — so frames must stay alive while the subtrees are computed.

Here, nothing happens after the descent. The recursive version:

```python
def lca(node, p, q):
    if p.val < node.val and q.val < node.val:
        return lca(node.left, p, q)      # ← nothing after this
    ...
```

is **tail-recursive** — the recursive call's result is returned unchanged. There's no pending work, so no frame needs preserving, and the recursion collapses into a loop.

**The general rule worth taking away:** *if a recursion does work only on the way **down**, it can be a loop with O(1) space. If it needs results on the way **back up**, it needs the stack.*

| Problem | Direction | Space |
|---|---|---|
| [104](104-maximum-depth-of-binary-tree.md), [543](543-diameter-of-binary-tree.md), [110](110-balanced-binary-tree.md) | combine on the way up | **O(h)** |
| **235** | decide on the way down | **O(1)** |

*(Python doesn't optimize tail calls automatically, so the recursive version really would use O(h) — you have to write the loop yourself.)*

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's a BST, so comparing a value against a node tells me which subtree it's in — I don't have to search. Standing at any node there are three cases: both targets smaller means both are in the left subtree, so I descend left; both larger, descend right; otherwise they split — one on each side, or one of them *is* this node — and that's the LCA. It's the lowest because everything below the split point lies in only one subtree and can contain at most one target. Since I only ever move down, it's a plain loop rather than recursion: O(h) time and O(1) space. Using the general-tree LCA algorithm would also be correct but O(n) — it would throw away the ordering."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if it's **not** a BST?" | **The key follow-up.** LeetCode 236: recurse both subtrees; if a node finds `p` on one side and `q` on the other, it's the LCA. O(n) time, O(h) space. |
| "Why is the split point the *lowest*?" | Anything below it lies entirely in one subtree, so it can hold at most one target. Anything above is higher. |
| "What if a node might not exist in the tree?" | Verify both are present first (two O(h) searches), or the answer may be wrong. The constraints here guarantee it. |
| "Recursive version?" | Same three cases, but the recursion is tail-recursive — Python won't optimize it, so the loop is strictly better. |
| "What if nodes had parent pointers?" | Walk up from both nodes to find their depths, align them, then ascend together — O(h), no root needed. |
| "LCA of **k** nodes in a BST?" | Descend while all k values are on the same side. Same idea, wider comparison. |
| "Many repeated LCA queries?" | Preprocess with [binary lifting](../algorithms/binary-lifting-lca.md) — O(n log n) build, O(log n) per query. |

**Traps:**

- **Ignoring the BST property** and writing the O(n) general solution. Correct, but it misses the point of the problem.
- **Using `or` instead of `and`** — you'd descend when only one target is on that side and walk right past the LCA.
- **Forgetting the self-descendant case.** Handled here by the `else`, but if you write explicit `<`/`>`/`==` branches it's easy to miss.
- **Recursing when a loop suffices** — costs O(h) space for nothing.
- **Comparing node objects instead of values.** Compare `.val`; the problem gives you nodes but the BST order is on values.
- **Descending past the split point.** Return immediately — the first divergence is the answer.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the same halve-by-comparison idea, on an array) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (the BST property used for verification instead of navigation) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (BST ordering exploited again) · [binary-search-tree](../data-structures/binary-search-tree.md).

</details>

---
