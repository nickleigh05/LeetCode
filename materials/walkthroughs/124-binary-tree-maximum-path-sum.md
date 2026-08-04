# 124. Binary Tree Maximum Path Sum

**Hard** · [LeetCode](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

A **path** in a binary tree is a sequence of nodes where each adjacent pair is connected by an edge. A node appears **at most once**, and the path **need not pass through the root**.

The **path sum** is the sum of the node values in the path. Return the **maximum path sum** of any non-empty path.

```
        1              →  6      (the path 2 → 1 → 3)
      /   \
     2     3

       -10              →  42     (the path 15 → 20 → 7)
      /   \                       the root is excluded — it would only hurt
     9     20
          /  \
        15    7
```

**Constraints:** `1 <= nodes <= 3·10⁴` · `-1000 <= Node.val <= 1000` ⚠️ **values can be negative**

> **Try it yourself first.** This is the hardest problem in the unit — the sections build up carefully.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "need **not pass through the root**" | The best path can live entirely inside a subtree — so every node must be considered as a candidate |
| "a node appears **at most once**" | ⚠️ The path can't fork. At any node it uses **at most one** child branch going down |
| "**non-empty** path" | A single node is a valid path — so the answer can be negative if every value is |
| values can be **negative** | ⚠️ **The crux.** A subtree with a negative total is worth *excluding* rather than extending |
| n up to 3·10⁴ | O(n); a skewed tree threatens the recursion limit |

**Start from the shape of a path.** Like [Diameter of Binary Tree](543-diameter-of-binary-tree.md), every path has a **highest point** — one node where it stops ascending. Below that peak it may descend into the left subtree, the right subtree, or both:

```
        1     ← peak of the path 2→1→3
      /   \
     2     3
```

So for each node, the best path peaking there is `node.val + best_left_branch + best_right_branch`.

**Now the part that makes this Hard.** Negative values mean a branch can be a *liability*. In the second example, the root `-10` has left branch 9 and right branch 42 — but the best answer, 42, comes from ignoring the root entirely.

So each branch contributes `max(branch_value, 0)` — **take it only if it helps.** Zero means "attach nothing on that side."

**And the second, subtler point.** What a node returns to its parent is **not** the same as its own best path:

- **For the parent:** the parent will extend *through* this node, so this node can offer only **one** downward branch — otherwise the path would fork.
- **For the answer:** the best path peaking *here* can use **both** branches.

Two different quantities, from one traversal.

🤔 **Before you open the next section:** if a node returned `val + left + right` to its parent, what shape would the resulting "path" have — and why is that illegal?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Try every node as the peak, recompute branches | Depth-style search per node | **O(n²)** | ❌ Recomputes constantly |
| **One DFS: return one branch, accumulate both** | Two quantities from one traversal | **O(n)** | ✅ |

**The decision: a single DFS returning the best *one-directional* path, while recording the best *two-directional* path in an accumulator.**

This is [Diameter of Binary Tree](543-diameter-of-binary-tree.md)'s pattern, hardened by negatives. The two quantities:

| | Formula | Why |
|---|---|---|
| **Returned to the parent** | `node.val + max(left, right)` | The parent extends *through* this node, so only **one** branch may hang below — a path can't fork |
| **Recorded in the accumulator** | `node.val + left + right` | The best path *peaking here* can use **both** branches, because it stops ascending at this node |

**Why the return value must be one branch only.** If a node returned `val + left + right`, its parent would attach that to its own path — producing a Y shape that visits the node twice. Not a path. **The `max(left, right)` in the return is what enforces the no-forking rule.**

**Why `max(branch, 0)` is essential.** A negative subtree total should be dropped, not carried. Clamping at 0 encodes "attach nothing on that side" and handles the entire negative-value complication in one operation — the same instinct as the `±inf` sentinels in [Median of Two Sorted Arrays](4-median-of-two-sorted-arrays.md): **pick a value that makes the edge case behave like the normal case.**

**Why the accumulator starts at `-inf`, not 0.** The problem requires a non-empty path, so an all-negative tree must return its largest (least negative) value. Initializing to 0 would wrongly report 0 for a tree like `[-3]`.

⚠️ Note the asymmetry: **branches clamp at 0** (you may decline a branch), but **the answer does not** (you must take at least one node).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
self.best = float("-inf")
```

The accumulator for the global answer, living outside the recursion so every node can contribute.

**`-inf`, not 0** — the path must be non-empty, so an all-negative tree's answer is negative.
→ [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) · [float-inf](../syntax/float-inf.md) · [int-float-basics](../syntax/int-float-basics.md)

```python
def dfs(node):
    if not node:
        return 0
```

Returns the best **one-directional** path sum starting at this node and descending.

An empty subtree contributes **0** — which pairs with the clamping below to mean "nothing attached here."
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    left = max(dfs(node.left), 0)
    right = max(dfs(node.right), 0)
```

**The clamp — the line that handles negative values.** If a subtree's best downward path is negative, taking it would *reduce* the total, so `max(..., 0)` discards it.

Zero literally means "don't extend into that subtree." This single operation removes every negative-value special case that would otherwise be needed.
→ [min-max-key](../syntax/min-max-key.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    self.best = max(self.best, node.val + left + right)
```

**The candidate for the global answer** — the best path with **this node as its peak**, using both branches.

This runs at every node, which is how a path buried deep inside a subtree still gets considered. It answers the "need not pass through the root" requirement directly.

Note this value is **only recorded, never returned** — a two-branch path can't be extended upward.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    return node.val + max(left, right)
```

**The return value — one branch only.** The parent will extend a path *through* this node, so at most one branch may hang below it.

`max(left, right)` picks the better single branch. Both are already ≥ 0 from the clamp, so this is never negative-by-accident.

⚠️ **This is the line that distinguishes the two quantities.** Returning `left + right` here would let the parent build a forking non-path.

```python
dfs(root)
return self.best
```

Traverse for the side effect, then read the accumulated answer. The returned value of the top-level call is discarded — it's only a one-directional path from the root, which isn't the question.

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — `[-10, 9, 20, null, null, 15, 7]`:

```
       -10
      /   \
     9     20
          /  \
        15    7
```

| Node | `left` (clamped) | `right` (clamped) | Candidate `val+l+r` | `self.best` | Returns `val+max(l,r)` |
|---|---|---|---|---|---|
| 9 | 0 | 0 | 9 | **9** | **9** |
| 15 | 0 | 0 | 15 | **15** | **15** |
| 7 | 0 | 0 | 7 | 15 | **7** |
| 20 | 15 | 7 | **42** | **42** | 20 + max(15,7) = **35** |
| **−10** | 9 | 35 | −10+9+35 = 34 | **42** | — |

Answer: **42** ✅ — the path `15 → 20 → 7`.

Two things to notice:

- **Node 20 returns 35, not 42.** It records 42 as a candidate (both branches), but offers only 35 upward (one branch). If it returned 42, the root could build `9 → −10 → 15 → 20 → 7`, which visits 20 twice — not a path.
- **The root's candidate is 34**, worse than 42. The best path correctly excludes the root entirely.

**And a negative case** — `[-3]`: `left = right = 0`, candidate `−3`, so `best = −3` ✅. Initializing `best = 0` would have wrongly returned 0.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited exactly once, doing O(1) work: two recursive calls, two clamps, two `max` operations, one addition.

n × O(1) = **O(n)**, and it's optimal — the best path could peak anywhere, so every node must be examined.

**Versus the naive O(n²).** Treating each node as a peak and recomputing its branch sums re-walks each subtree once per ancestor — O(n²) on a skewed tree, ~10⁹ at n = 3·10⁴.

**Why one pass suffices:** the recursion already computes every subtree's best downward path on its way back up. The candidate check is one extra comparison at a node you were visiting anyway — **the information was already there.** Same realization as [Diameter](543-diameter-of-binary-tree.md) and [Balanced Binary Tree](110-balanced-binary-tree.md).

**No early exit** — the maximum could be anywhere, and unlike [110](110-balanced-binary-tree.md) (a boolean) there's nothing decisive to bail on.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack — **O(log n)** balanced, **O(n)** skewed.

`self.best` is a single number, O(1). Nothing else is allocated.

⚠️ At n = 3·10⁴, a skewed tree needs 3·10⁴ frames — well past Python's default recursion limit of 1000 → `RecursionError`. The iterative rewrite is genuinely awkward here, because this is a **bottom-up** problem: a node can't be processed until *both* children are done, so you'd need a postorder stack with visited markers.
→ [recursion-limit](../syntax/recursion-limit.md)

**Top-down vs bottom-up, one more time** — it's the recurring divide of this unit:

| | Direction | Iterative rewrite |
|---|---|---|
| [1448](1448-count-good-nodes-in-binary-tree.md), [98](98-validate-binary-search-tree.md) | top-down (context in parameters) | **easy** — push `(node, context)` |
| **124**, [543](543-diameter-of-binary-tree.md), [110](110-balanced-binary-tree.md) | bottom-up (results in returns) | **hard** — needs postorder bookkeeping |

**The tuple alternative:** return `(one_branch_best, global_best)` from every call instead of using `self.best`. Same O(h), no shared state, and some interviewers prefer it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every path has a highest node, so I consider each node as a potential peak. The key insight is that two different quantities are involved. What I *record* as a candidate is `node.val + left + right` — the best path peaking here, using both branches. But what I *return* to the parent is `node.val + max(left, right)` — only one branch, because the parent will extend a path through this node and a path can't fork. The second key detail is negatives: I clamp each branch with `max(branch, 0)`, so a subtree that would reduce the total is simply dropped. And I initialize the global best to negative infinity rather than zero, because the path must be non-empty — an all-negative tree has a negative answer. One traversal, O(n) time, O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does the return differ from the recorded value?" | **The question.** The parent extends *through* this node, so only one branch may hang below — otherwise the path forks and revisits a node. |
| "Why clamp branches at 0?" | A negative branch reduces the sum, so it's better to attach nothing. Zero encodes exactly that. |
| "Why is `best` initialized to `-inf`?" | The path must be non-empty. A tree of `[-3]` must return −3, not 0. |
| "Return the **path**, not the sum?" | Track the peak node and the chosen direction at each step, then reconstruct by walking down. Noticeably more bookkeeping. |
| "What if all values were positive?" | The clamps become no-ops, and the best path always spans two leaves. |
| "How does this relate to Diameter?" | Identical structure — [543](543-diameter-of-binary-tree.md) counts edges (all weight 1, no negatives); this sums values, so it needs the clamp. |
| "Path must go root-to-leaf?" | Much simpler — just take the best root-to-leaf sum, no accumulator needed. |
| "Avoid the shared state?" | Return a `(branch_best, global_best)` tuple and combine both at each node. |

**Traps:**

- **Returning `val + left + right`.** The defining bug — lets the parent construct a forking non-path.
- **Forgetting to clamp negatives.** A single negative subtree then drags down otherwise-good answers.
- **Initializing `best = 0`.** All-negative trees wrongly return 0. Use `-inf`.
- **Clamping the *answer* at 0 too.** Branches clamp; the final answer must not, since the path is non-empty.
- **Using a plain local for `best`** — assigning to it inside the nested function creates a new local. Use `self.best`, `nonlocal`, or a container.
- **Only checking at the root.** The peak can be anywhere.

**This same move shows up in:** [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (the same peak-node structure, unweighted) · [Maximum Subarray](53-maximum-subarray.md) (the same "drop it if it goes negative" clamp, on an array — Kadane's algorithm) · [Balanced Binary Tree](110-balanced-binary-tree.md) (one traversal, two facts) · [dfs](../algorithms/dfs.md).

</details>
