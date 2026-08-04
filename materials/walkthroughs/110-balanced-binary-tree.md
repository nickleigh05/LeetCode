# 110. Balanced Binary Tree

**Easy** · [LeetCode](https://leetcode.com/problems/balanced-binary-tree/) · [Solution file (no hints)](../../problems/0001-0499/110.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given a binary tree, determine if it is **height-balanced** — a tree in which the left and right subtrees of **every node** differ in height by no more than 1.

```
        3           balanced ✅
      /   \
     9     20
          /  \
        15    7

        1           NOT balanced ❌
      /   \         node 2's subtrees differ by 2
     2     3
    / \
   4   4
  / \
 5   5
```

**Constraints:** `0 <= nodes <= 5000` · `-10⁴ <= Node.val <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**every** node" | ⚠️ Not just the root — the condition must hold everywhere. One bad node anywhere makes the whole tree unbalanced |
| "differ in height by no more than 1" | `abs(left_height − right_height) <= 1` |
| return `true`/`false` | A yes/no answer — so you can **bail out** the moment you find a violation |
| empty tree | Vacuously balanced → `true` |
| n up to 5000 | A naive O(n²) is 2.5·10⁷ — survivable, but the O(n) solution is the point |

The naive reading translates directly:

```python
def isBalanced(root):
    if not root: return True
    return (abs(height(root.left) - height(root.right)) <= 1
            and isBalanced(root.left) and isBalanced(root.right))
```

Correct, but **O(n²)** — `height()` re-walks each subtree once per ancestor, so nodes near the bottom get counted over and over.

**The fix, and the actual lesson.** The recursion that computes height is *already* visiting every node bottom-up. So instead of asking about height and balance separately, make one traversal answer both:

> **Return the height — unless the subtree is unbalanced, in which case return a sentinel that means "already failed."**

Overloading the return value like this lets a single `int` carry two facts. And because the sentinel propagates upward immediately, the whole recursion short-circuits at the first violation.

**Why `-1` is a safe sentinel:** heights are always ≥ 0, so `-1` can never be a legitimate height. It's unambiguous.

🤔 **Before you open the next section:** you need a function that reports both a height *and* a failure. What's the cheapest way to encode "failed" in a value that's normally a non-negative integer?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Check balance at each node with a separate `height()` | Top-down | **O(n²)** | ❌ Recomputes heights constantly |
| Return `(height, is_balanced)` tuples | Bottom-up, two values | O(n) | ✅ Explicit, slightly more code |
| **Return height, or `-1` for "unbalanced"** | Bottom-up, sentinel-encoded | **O(n)** | ✅ |

**The decision: one bottom-up DFS returning the height, using `-1` as an "unbalanced" sentinel.**

At each node:
1. Get the left height. **If it's `-1`, propagate `-1` immediately** — no point computing the right side.
2. Get the right height. Same check.
3. If `abs(left - right) > 1`, this node is the violation → return `-1`.
4. Otherwise return the real height, `max(left, right) + 1`.

**Why bottom-up beats top-down.** The naive version asks *"what's the height below me?"* at every node, recomputing shared work. The bottom-up version computes each height **exactly once** and checks the balance condition on the way back up, when both children's heights are already in hand.

That's the same instinct as [Diameter of Binary Tree](543-diameter-of-binary-tree.md): *the traversal already passes through the data you need — use it in place instead of walking again.*

**Two ways to carry two facts.** [543](543-diameter-of-binary-tree.md) used an external accumulator; here the sentinel packs both facts into the return value. A third option is returning a tuple:

```python
def check(node):
    if not node: return (0, True)
    lh, lb = check(node.left)
    rh, rb = check(node.right)
    ok = lb and rb and abs(lh - rh) <= 1
    return (max(lh, rh) + 1, ok)
```

Equivalent complexity, more explicit, no magic value. **Mention it** — some interviewers prefer it, and "I could return a tuple instead of overloading the return" is a good thing to say.

**The short-circuit is why it's O(n) rather than just "less than O(n²)".** Once `-1` appears it races to the top without exploring anything further.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def height(node):
    if not node:
        return 0
```

A nested helper returning **height in nodes** — the same base case as [Maximum Depth](104-maximum-depth-of-binary-tree.md). An empty subtree has height 0, so a leaf comes out as 1.

Its return value is overloaded: a real height, **or** `-1` meaning "an imbalance was found somewhere below."
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    left = height(node.left)
    if left == -1:
        return -1
```

Recurse left, then **check the sentinel before doing anything else**.

Propagating immediately is what makes this O(n): once any subtree is known unbalanced, the answer is settled, so the right subtree is never even visited. The failure races to the root.
→ [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    right = height(node.right)
    if right == -1:
        return -1
```

Same on the right. Note this only runs if the left side was fine — the ordering *is* the short-circuit.

```python
    if abs(left - right) > 1:
        return -1
```

**The actual balance test at this node.** `abs` makes it symmetric — a deep left or a deep right is equally disqualifying.

Returning `-1` here says "the violation is *here*", as distinct from the two checks above which say "the violation was below."
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    return max(left, right) + 1
```

**This node is fine**, so report the genuine height — `max` for the taller side, `+1` for this node. Identical to [problem 104](104-maximum-depth-of-binary-tree.md).
→ [min-max-key](../syntax/min-max-key.md)

```python
return height(root) != -1
```

Convert the sentinel back into the boolean the problem asked for. Any value other than `-1` is a real height, meaning no violation was ever found.

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it — a balanced tree** `[3,9,20,null,null,15,7]`:

| Node | `left` | `right` | `abs(diff)` | Returns |
|---|---|---|---|---|
| 9 | 0 | 0 | 0 | **1** |
| 15 | 0 | 0 | 0 | **1** |
| 7 | 0 | 0 | 0 | **1** |
| 20 | 1 | 1 | 0 | **2** |
| 3 | 1 | 2 | **1** ≤ 1 ✅ | **3** |

`3 != -1` → **`True`** ✅

**And an unbalanced one:**

```
        1
      /   \
     2     3
    / \
   4   4
  / \
 5   5
```

| Node | `left` | `right` | Check | Returns |
|---|---|---|---|---|
| 5, 5 | 0 | 0 | ok | **1** |
| 4 (left) | 1 | 1 | ok | **2** |
| 4 (right) | 0 | 0 | ok | **1** |
| **2** | 2 | 1 | ok | **3** |
| **1** | 3 | 1 | **abs(3−1) = 2 > 1** ❌ | **−1** |

`-1 != -1` is false → **`False`** ✅

Now imagine the violation had been deeper: the `-1` would propagate up through every ancestor untouched, and no further subtrees would be explored.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited **at most once**, doing O(1) work — two comparisons, an `abs`, a `max`. The heights are computed on the way back up, so nothing is recalculated.

**Versus the naive O(n²).** The top-down version calls `height()` at every node, and `height()` walks the entire subtree below it. A node at depth d is counted by all d of its ancestors — giving O(n·h), which is O(n log n) balanced and **O(n²)** skewed. At n = 5000 that's 2.5·10⁷ versus 5·10³.

**The early exit makes the common case faster still.** An imbalance near the root returns almost immediately, without exploring the rest of the tree at all. The O(n) bound is the worst case — a fully balanced tree, where everything must be checked.

**Contrast with [Diameter](543-diameter-of-binary-tree.md):** that problem has *no* early exit, since the maximum could be anywhere. Here the answer is a boolean, and a single failure is decisive — which is exactly what licenses the short-circuit. **Yes/no questions can bail; extremum questions can't.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack — **O(log n)** balanced, **O(n)** skewed.

Note the irony: the worst case for space is a **skewed** tree, which is exactly the kind this function will reject almost instantly. So the pathological space case and the pathological time case never coincide — a skewed tree short-circuits after a handful of frames.

Nothing else is allocated; the sentinel rides in the return value rather than in any structure.

At n = 5000, a skewed tree would nominally need 5000 frames — past Python's default recursion limit of 1000. In practice the `-1` short-circuit fires long before that on a genuinely skewed tree, but a **left-skewed-then-balanced** shape could still go deep before failing. Worth naming.
→ [recursion-limit](../syntax/recursion-limit.md)

**The tuple-returning variant** uses the same O(h) — a two-element tuple per frame is still O(1) per frame. **The sentinel saves no asymptotic space**, only a little allocation. Choose between them on readability, not efficiency.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The naive approach checks the height difference at every node by calling a separate height function, but that recomputes heights over and over — O(n²) on a skewed tree. Instead I do one bottom-up traversal where the recursion returns the height, and I overload that return value: `-1` means 'an imbalance was found somewhere below.' At each node I get the left height, propagate immediately if it's `-1`, do the same on the right, then check whether the difference exceeds 1. If everything's fine I return the real height. That computes each height exactly once and short-circuits at the first violation — O(n) time, O(h) space. I could also return a `(height, is_balanced)` tuple instead of using a sentinel, which is more explicit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the naive version O(n²)?" | **The question.** A node at depth d has its height recomputed by all d ancestors. On a skewed tree that's the sum 1+2+…+n = O(n²). |
| "Avoid the magic `-1`." | Return a `(height, is_balanced)` tuple. Same complexity, no sentinel, arguably cleaner. |
| "Is `-1` safe as a sentinel?" | Yes — heights are non-negative by definition, so `-1` can never be a real value. |
| "What if 'balanced' allowed a difference of k?" | Change `> 1` to `> k`. Nothing else moves. |
| "Return *where* the imbalance is?" | Return the offending node instead of `-1`, or accumulate it in an outer variable. |
| "Do it iteratively." | Postorder with an explicit stack, since a node needs both children's heights first. Fiddlier. |
| "Is this the AVL balance condition?" | Yes — this is exactly the invariant AVL trees maintain on insert and delete. See [balanced-bst](../data-structures/balanced-bst.md). |

**Traps:**

- **The top-down O(n²) version.** It's correct and it's the first thing most people write — recognize why it's wasteful.
- **Not checking the sentinel before recursing right.** You'd lose the short-circuit and do unnecessary work (though the answer stays correct).
- **Forgetting `abs`.** Checking only `left - right > 1` misses right-heavy imbalances entirely.
- **Using `>=` instead of `>`.** A difference of exactly 1 **is** balanced.
- **Checking balance only at the root.** The condition applies at every node.
- **Returning the height instead of the boolean** at the end — the caller wants `True`/`False`.

**This same move shows up in:** [Maximum Depth](104-maximum-depth-of-binary-tree.md) (the height function this overloads) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (one traversal carrying two results, via an accumulator instead) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (a validity check propagating up) · [balanced-bst](../data-structures/balanced-bst.md).

</details>
