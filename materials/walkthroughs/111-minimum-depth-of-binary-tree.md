# 111. Minimum Depth of Binary Tree

**Easy** · [LeetCode](https://leetcode.com/problems/minimum-depth-of-binary-tree/) · [Solution file (no hints)](../../problems/0001-0499/111.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given a binary tree, find its **minimum depth** — the number of nodes along the shortest path from the root down to the nearest **leaf**. A leaf is a node with no children.

```
root = [3,9,20,null,null,15,7]  →  2    (3 → 9)
root = [2,null,3,null,4,null,5,null,6]  →  5
root = []  →  0
```

**Constraints:** `0 <= number of nodes <= 10⁵` · `-1000 <= Node.val <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** depth" | Shortest root-to-leaf path — so it's a `min`, not a `max` |
| "nearest **leaf**" | ⚠️ **The entire difficulty.** The path must end at a node with **no children** |
| "number of **nodes**" | Depth counts nodes, not edges — a single-node tree has depth 1 |
| `0 <= nodes` | Empty tree returns **0** |
| `n` up to 10⁵ | A degenerate tree is 10⁵ deep — **well past Python's recursion limit** |

**Why this is deceptively harder than [Maximum Depth](104-maximum-depth-of-binary-tree.md).** That problem is a clean three-liner:

```python
return 0 if not root else 1 + max(maxDepth(root.left), maxDepth(root.right))
```

Swap `max` for `min` and it looks done. **It isn't** — and the failing case is small:

```
  2
   \
    3
```

Node 2 has no left child, so `minDepth(None)` returns 0, and `1 + min(0, 1)` = **1**. But node 2 is *not* a leaf — it has a right child — so the true answer is **2** (path 2 → 3).

**The bug in one sentence:** `None` is not a leaf. A missing child contributes no path at all, so it must be **ignored**, not treated as a zero-length path.

That gives three cases rather than one:

| Situation | Correct handling |
|---|---|
| Node is a **leaf** | depth 1 |
| Node has **one** child | `1 + minDepth(that child)` — the missing side is ignored |
| Node has **two** children | `1 + min(left, right)` |

The `max` version never notices this, because `max(0, k)` = `k` conveniently ignores the empty side by accident. `min(0, k)` = 0 does not.

🤔 **Before you open the next section:** if a node has only a right child, what does the *left* subtree contribute to the shortest root-to-leaf path?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Naive `1 + min(left, right)` | Mirror of max-depth | — | — | ❌ **Wrong** — treats `None` as a leaf |
| **Recursive DFS with case analysis** | Handle one-child nodes explicitly | **O(n)** | O(h) | ✅ |
| **BFS level order** | Return the depth of the first leaf found | **O(n)** worst, often far less | O(w) | ✅✅ Early exit |

**The decision depends on what you're optimizing.**

**Recursive DFS** is the direct translation of the case analysis and reads clearly. But it **always explores the entire tree** — even if a leaf sits at depth 2, it will descend a 10⁵-deep branch before finishing.

**BFS is the better algorithm here**, and the reason is worth stating precisely:

> BFS explores level by level, so the **first leaf it encounters is at the minimum depth**. It can return immediately.

That's an asymmetry with [Maximum Depth](104-maximum-depth-of-binary-tree.md): for a *maximum* you must see the whole tree, so DFS is natural. For a *minimum* you can stop at the first leaf, and BFS gets there without touching the deep branches.

```
        3
       / \
      9   20        BFS finds leaf 9 at depth 2 and stops.
         /  \       DFS would still descend into 15 and 7.
        15   7
```

On the pathological input `[2,null,3,null,4,…]` (a 10⁵-node chain), both are O(n) — but on a tree with one shallow leaf and one enormous branch, BFS is dramatically faster.

**Why the DFS version still matters:** it's what the solution file uses, it's the clearer expression of the recurrence, and it's what you'd write first. The right answer in an interview is to write it, then observe that BFS allows early termination.

**The recursion-depth hazard:** at `n = 10⁵`, a degenerate tree is 10⁵ frames deep — Python's limit is ~1000, so the recursive version raises `RecursionError` on exactly the input shape shown in example 2. BFS has no such problem. That's a second, independent reason to prefer it.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return 0
```

**Empty tree → depth 0.** This also serves as the recursion's terminating case, though — crucially — it is never reached via a one-child node, because those are intercepted below.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
if not root.left and not root.right:
    return 1
```

**Leaf → depth 1.**

`and`, not `or` — a leaf has **both** children absent. This is the only place a path legitimately terminates.
→ [logical-operators](../syntax/logical-operators.md)

```python
if not root.left:
    return 1 + self.minDepth(root.right)
```

**Only a right child — ignore the missing left side.**

This is the line that fixes the naive bug. Without it, `min(0, right)` would return 0 for the absent left subtree and report a path ending at a non-leaf.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
if not root.right:
    return 1 + self.minDepth(root.left)
```

The mirror case.

```python
return 1 + min(self.minDepth(root.left), self.minDepth(root.right))
```

**Two children — now `min` is safe**, because both subtrees genuinely contain leaves.

By this point every one-child case has been handled above, so neither recursive call can return a misleading 0.
→ [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:

        if not root:
            return 0

        if not root.left and not root.right:
            return 1

        if not root.left:
            return 1 + self.minDepth(root.right)

        if not root.right:
            return 1 + self.minDepth(root.left)

        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))
```

</details>

<details>
<summary>The BFS version (early exit, no recursion limit)</summary>

```python
from collections import deque

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        queue = deque([(root, 1)])
        while queue:
            node, depth = queue.popleft()

            if not node.left and not node.right:
                return depth                      # first leaf = minimum depth

            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
```

Level-order traversal returning at the **first leaf reached**. No case analysis is needed — only real children are enqueued, so `None` never enters the queue. Immune to recursion limits, and it skips deep branches entirely.

</details>

**Trace the DFS** — `root = [3,9,20,null,null,15,7]`:

```
    3
   / \
  9   20
     /  \
    15   7
```

| Call | Node | Children | Branch taken | Returns |
|---|---|---|---|---|
| 1 | 3 | both | last case: `1 + min(…)` | `1 + min(1, 2)` = **2** |
| 2 | 9 | none | leaf | **1** |
| 3 | 20 | both | `1 + min(…)` | `1 + min(1, 1)` = **2** |
| 4 | 15 | none | leaf | **1** |
| 5 | 7 | none | leaf | **1** |

Return **2** ✅ — the path `3 → 9`.

Note DFS visited all five nodes; BFS would have returned at node 9 after examining three.

**The case that breaks the naive version** — `[2,null,3,null,4,null,5,null,6]`:

```
2 → 3 → 4 → 5 → 6   (each node has only a right child)
```

| Call | Node | Children | Branch | Returns |
|---|---|---|---|---|
| 1 | 2 | right only | `1 + minDepth(3)` | `1 + 4` = **5** |
| 2 | 3 | right only | `1 + minDepth(4)` | `1 + 3` = 4 |
| 3 | 4 | right only | `1 + minDepth(5)` | `1 + 2` = 3 |
| 4 | 5 | right only | `1 + minDepth(6)` | `1 + 1` = 2 |
| 5 | 6 | none | leaf | **1** |

Return **5** ✅

With the naive `1 + min(left, right)`, call 1 would compute `1 + min(0, 4)` = **1** — wrong, because the absent left child was counted as a zero-length path.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n) worst case** for both approaches — every node may need visiting.

But the *typical* behaviour differs sharply:

| | Best case | Worst case |
|---|---|---|
| **DFS (recursive)** | O(n) — always visits everything | O(n) |
| **BFS** | **O(1)** — root is a leaf | O(n) |

For a tree with a leaf at depth 2 and a 10⁵-node branch elsewhere, BFS returns after examining a handful of nodes; DFS traverses all 10⁵.

**The general principle worth extracting:**

> **DFS for maximum depth, BFS for minimum depth.** A maximum requires seeing everything; a minimum can stop at the first qualifying node, and BFS reaches the shallowest one first.

The same reasoning makes BFS the right tool for shortest paths in unweighted graphs — [Rotting Oranges](994-rotting-oranges.md), [Word Ladder](127-word-ladder.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h) or O(w)</summary>

| Approach | Space | Worst case |
|---|---|---|
| **DFS** | O(h) — recursion stack | **O(n)** for a degenerate tree ⚠️ |
| **BFS** | O(w) — queue holds one level | **O(n)** for a complete tree's last level |

They fail in *opposite* shapes, which is a nice detail to notice:

- A **degenerate** tree (a chain) has `h = n` but width 1 → DFS is O(n), BFS is O(1).
- A **complete** tree has `h = log n` but width `n/2` → DFS is O(log n), BFS is O(n).

**The recursion limit makes this concrete.** At `n = 10⁵`, example 2's chain is 10⁵ deep — the recursive solution raises `RecursionError` before producing an answer, while BFS handles it in constant queue space.

That's not a theoretical concern; it's the given example. Worth saying aloud: *"the recursive version is clearer, but on this problem's constraints a degenerate tree would blow the stack, so I'd ship the BFS version."*

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The trap is that this isn't just Maximum Depth with `min` swapped in. `min(0, k)` treats a missing child as a zero-length path, but `None` isn't a leaf — a node with one child can't end a root-to-leaf path. So I handle three cases: a leaf returns 1, a node with one child returns `1 + minDepth` of the child that exists, ignoring the missing side, and only a node with two children uses `1 + min(left, right)`. That's O(n) time and O(h) space. But BFS is the better algorithm here: level-order means the **first leaf I reach is at the minimum depth**, so I can return immediately and skip deep branches. It also avoids the recursion limit — with 10⁵ nodes a degenerate tree is 10⁵ frames deep, which Python won't allow, and that's exactly the shape of the second example."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't you just swap `max` for `min`?" | **The key question.** `min(0, k)` treats a missing child as a valid zero-length path. `[2,null,3]` returns 1 instead of 2. |
| "Which is better, DFS or BFS?" | BFS — it returns at the first leaf found and skips deep branches. DFS always traverses everything. |
| "What about very deep trees?" | Recursive DFS hits Python's ~1000-frame limit at 10⁵ nodes. BFS is unaffected. |
| "Maximum depth instead?" | [Problem 104](104-maximum-depth-of-binary-tree.md) — there `1 + max(left, right)` **is** correct, because `max(0, k) = k` ignores the empty side harmlessly. |
| "Depth in **edges** rather than nodes?" | Subtract 1 from the result (for a non-empty tree). |
| "Iterative DFS?" | Push `(node, depth)` pairs and track the minimum over all leaves — correct, but it loses BFS's early exit. |
| "What does BFS cost on a wide tree?" | O(w) queue space, up to `n/2` for a complete tree's last level — the opposite failure mode from DFS. |

**Traps:**

- **`1 + min(minDepth(left), minDepth(right))` unguarded.** *The* bug. Fails on any node with exactly one child.
- **Using `or` in the leaf test.** A one-child node would be misclassified as a leaf.
- **Returning 0 for a leaf.** Depth counts nodes, so a leaf is 1.
- **Forgetting the empty-tree case.** `minDepth(None)` must be 0.
- **Recursing on a 10⁵-node chain.** `RecursionError` — and that's example 2.
- **Enqueuing `None` children in BFS.** Then `node.left` raises; only enqueue real children.

**This same move shows up in:** [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) (the sibling where the naive recurrence *is* correct — the instructive contrast) · [Path Sum](112-path-sum.md) (the same "`None` is not a leaf" distinction) · [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the BFS machinery this borrows) · [Balanced Binary Tree](110-balanced-binary-tree.md) (depth computed bottom-up with early termination).

</details>

---
