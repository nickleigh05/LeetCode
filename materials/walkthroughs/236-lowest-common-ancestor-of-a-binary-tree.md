# 236. Lowest Common Ancestor of a Binary Tree

**Medium** · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) · [Solution file (no hints)](../../problems/0001-0499/236.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given a binary tree and two nodes `p` and `q`, find their **lowest common ancestor** — the deepest node having both as descendants. **A node may be a descendant of itself.**

```
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1  →  3
root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4  →  5   (5 is an ancestor of itself)
root = [1,2], p = 1, q = 2  →  1
```

**Constraints:** `2 <= number of nodes <= 10⁵` · `-10⁹ <= Node.val <= 10⁹` · all values **unique** · `p != q` · **both `p` and `q` exist** in the tree

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary tree**", not BST | ⚠️ **No ordering to exploit.** You can't compare values to pick a direction — that's what makes this harder than [LCA of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) |
| "**lowest** common ancestor" | Deepest such node — the last point where the paths to `p` and `q` diverge |
| "a node may be a **descendant of itself**" | ⚠️ If `p` is an ancestor of `q`, the answer is **`p`** |
| "both `p` and `q` **exist**" | ⚠️ Big simplification — no "not found" case, so finding one target is enough to report it |
| values are **unique** | Node identity and value identity coincide, though comparing nodes directly is cleaner |
| `n` up to 10⁵ | A degenerate tree is 10⁵ deep — past Python's recursion limit |

**Why no BST shortcut exists.** In [LCA of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) you compare values and walk in one direction — O(h) with no recursion needed. Here there's no ordering, so you must actually **search both subtrees**.

**The insight — think about what each subtree reports back:**

> Recurse into both children. Each returns either a target it found (or the LCA of a pair it found), or `None`.
>
> - **Both sides return non-`None`** → `p` and `q` are in *different* subtrees → **this node is the LCA**
> - **Only one side returns non-`None`** → both targets are on that side → **propagate that result upward**
> - **Neither** → neither target is here → return `None`

That's the whole algorithm. The elegance is that a single return value serves two purposes: "I found a target" on the way up, and "I found the answer" once both sides report in.

**Why the self-ancestor case works for free.** If the current node *is* `p`, the code returns it immediately without descending further. That's correct precisely because `q` is guaranteed to exist: if `q` is below `p`, then `p` is the LCA; if `q` is elsewhere, this return acts as "found `p`" and the split gets detected higher up. **The existence guarantee is what makes the early return sound** — without it you'd have to verify both targets were actually present.

🤔 **Before you open the next section:** if the left subtree reports finding something and the right subtree also reports finding something, what must be true about the current node?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Find both root-to-node paths, compare | Two searches, then walk the paths in parallel | O(n) | **O(h)** for two paths | ✅ Correct, more code |
| Parent pointers + ancestor set | Map each node to its parent, walk up from `p`, then from `q` | O(n) | **O(n)** | ✅ Correct, heavier |
| **Single recursive DFS** | Return whatever was found; the split point is the answer | **O(n)** | **O(h)** | ✅✅ |

**The decision: one post-order DFS that returns "what I found" upward.**

The function's return value carries **three different meanings** depending on context, which is what makes it so compact:

| Returned | Meaning |
|---|---|
| `None` | Neither target is in this subtree |
| `p` or `q` | Exactly one target found here (and the other isn't below it) |
| some other node | That node is the LCA of both targets |

The caller doesn't need to distinguish these — it only asks *"did each side return something?"* — and that single question resolves the whole problem.

**Why `left and right` means "this is the LCA."** If both children report non-`None`, one target lies in each subtree. The current node is therefore the deepest node with both as descendants — no node below it can contain both. That's the definition of the LCA.

**Why "one side non-`None`" propagates rather than deciding.** If only the left side found something, either it found one target (and the other is elsewhere in the tree, to be resolved higher) or it already found the LCA of both. Either way, passing it up unchanged is correct — and the ambiguity never needs resolving, which is the trick.

**Why not build paths?** Recording the root-to-`p` and root-to-`q` paths and comparing them is perfectly valid, and arguably more intuitive. It costs two traversals plus O(h) storage for each path, and roughly triples the code. Worth mentioning as the more explicit alternative — especially since it generalizes to returning the *distance* between the nodes.

**The parent-pointer approach** is what you'd use if you had to answer many LCA queries on the same tree: build a parent map once, then walk up from `p` collecting ancestors into a set, then walk up from `q` until you hit one. O(n) preprocessing, O(h) per query. For a single query it's more machinery than needed.

**Recursion depth:** at `n = 10⁵`, a degenerate tree is 10⁵ frames deep — beyond Python's default limit. Mention it; an iterative reformulation (parent pointers) sidesteps it entirely.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root or root is p or root is q:
    return root
```

**Three base cases in one line.**

- `not root` → empty subtree, nothing found → returns `None`
- `root is p` or `root is q` → **found a target; stop descending and report it**

The early return on finding a target is what makes the self-ancestor case work. If `q` sits below `p`, we return `p` without ever looking for `q` — and `p` is indeed the answer.

Using `is` (identity) rather than `==` (value) states the intent precisely. Values are unique here so both work, but the problem is defined in terms of the given **nodes**.
→ [identity-operators](../syntax/identity-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
left = self.lowestCommonAncestor(root.left, p, q)
right = self.lowestCommonAncestor(root.right, p, q)
```

**Search both subtrees.** Unlike a BST, there's no way to know which side holds a target without looking.

This is **post-order**: both children are resolved before the current node decides anything. That bottom-up combination is the same shape as [Maximum Depth](104-maximum-depth-of-binary-tree.md) and [Diameter](543-diameter-of-binary-tree.md).
→ [recursion-basics](../syntax/recursion-basics.md)

```python
if left and right:
    return root
```

**The split point — this node is the LCA.**

One target in each subtree means the current node is the deepest node containing both. Nothing lower can, because each child only holds one.
→ [logical-operators](../syntax/logical-operators.md)

```python
return left if left else right
```

**Exactly one side (or neither) found something — pass it up.**

- Only `left` → return it
- Only `right` → return it
- Neither → `right` is `None`, so `None` propagates

One expression covers all three, because "the non-`None` one, or `None`" is exactly what's needed at every level.

Equivalent Pythonic form: `return left or right`.
→ [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        if not root or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root

        return left if left else right
```

</details>

**Trace the split case** — `p = 5`, `q = 1`:

```
        3
       / \
      5   1
     / \  / \
    6  2 0   8
      / \
     7   4
```

| Call | Node | Left result | Right result | Returns |
|---|---|---|---|---|
| 6 | 6 | — | — | `None` (leaf, not a target) |
| 7 | 7 | — | — | `None` |
| 8 | 4 | — | — | `None` |
| 5 | 2 | `None` (7) | `None` (4) | `None` |
| 2 | **5** | not evaluated | not evaluated | **5** (base case: `root is p`) |
| 3 | **1** | not evaluated | not evaluated | **1** (base case: `root is q`) |
| 1 | 3 | **5** | **1** | both non-`None` → **return 3** ⭐ |

Return **3** ✅

Node 5 returned immediately via the base case without exploring its children — the early return doing its job.

**Trace the self-ancestor case** — `p = 5`, `q = 4` (where 4 is a descendant of 5):

| Call | Node | Result |
|---|---|---|
| 1 | 3 | recurse both sides |
| 2 | **5** | **base case fires** → return 5 (never descends to find 4) |
| 3 | 1 | subtree contains neither → `None` |
| back at 1 | 3 | `left = 5`, `right = None` → `left and right` is false → return `left` = **5** |

Return **5** ✅ — correct, because a node counts as its own descendant.

This is the case that would break a naive "find both, then compare" implementation that assumed the LCA must be strictly above both nodes.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited at most once, doing O(1) work beyond its recursive calls.

**Often much less in practice**, because of the early return: once a target is found, its entire subtree is skipped. In the trace above, nodes 6, 2, 7, and 4 below node 5 were never visited after 5 matched.

| Case | Nodes visited |
|---|---|
| Targets near the root | O(h) |
| Targets in distant leaves | O(n) |

**Why O(n) is unavoidable in the worst case.** Without a BST's ordering, you cannot rule out any subtree without examining it. Contrast [LCA of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md), where value comparisons give **O(h)** — that's the concrete cost of losing the ordering property.

**For repeated queries** on the same tree, preprocessing changes the picture entirely: binary lifting gives O(n log n) setup and **O(log n) per query**; Tarjan's offline algorithm handles a batch in near-linear total time. See [binary-lifting-lca](../algorithms/binary-lifting-lca.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack.

| Tree shape | `h` | Space |
|---|---|---|
| Balanced | `log n` | **O(log n)** ≈ 17 at n = 10⁵ |
| Degenerate | `n` | **O(n)** = 10⁵ ⚠️ |

**The degenerate case is a genuine hazard here** — 10⁵ frames far exceeds Python's ~1000 default, giving a `RecursionError`. If raised, the parent-pointer approach is the natural escape:

```python
# build parent links via BFS/DFS, then walk up
ancestors = set()
while p: ancestors.add(p); p = parent[p]
while q not in ancestors: q = parent[q]
return q
```

That's O(n) time and O(n) space, fully iterative.

**Comparison of the three approaches:**

| | Time | Space | Notes |
|---|---|---|---|
| **Recursive DFS** | O(n) | O(h) | Shortest code; recursion-limit risk |
| Path comparison | O(n) | O(h) | Two traversals, more explicit |
| Parent map + set | O(n) | O(n) | Iterative; best if reused across queries |

**The idea worth keeping:**

> **Let each subtree report a single value upward, and let the parent's decision come from comparing what the two children reported.** The return value can encode more than one meaning as long as the caller only needs to distinguish "something" from "nothing."

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "There's no BST ordering here, so I can't pick a direction — I have to search both subtrees. I do a post-order DFS where each call returns whatever it found: `None` if neither target is in that subtree, or a node otherwise. The base case returns immediately when I hit `p` or `q`, which also handles the self-ancestor case: if `q` is below `p`, I return `p` without descending, and `p` is the right answer. At each node, if **both** children returned something, the targets are in different subtrees, so this node is the LCA. If only one side returned something, I propagate it up unchanged — it's either a single target found or an LCA already determined, and I never need to distinguish. O(n) time and O(h) space. The early return prunes a lot in practice. One caveat: with 10⁵ nodes a degenerate tree would exceed Python's recursion limit, so I'd switch to parent pointers and an ancestor set if that mattered."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [LCA of a **BST**](235-lowest-common-ancestor-of-a-binary-search-tree.md)?" | **The key comparison.** A BST lets you compare values and walk one direction — O(h), iterative, O(1) space. Without ordering you must search both subtrees — O(n). |
| "What if `p` or `q` might **not** exist?" | The early return breaks — you'd wrongly report a found node. Add flags tracking whether each was actually seen, and verify before returning. |
| "Why does the self-ancestor case work?" | Returning on `root is p` means "found p." If `q` is below, `p` is the LCA; if elsewhere, the split is detected higher up. |
| "Do it iteratively." | Build a parent map by traversal, collect `p`'s ancestors in a set, then walk up from `q` to the first match. O(n)/O(n). |
| "**Many** LCA queries on one tree?" | Preprocess: binary lifting for O(log n) per query, or Tarjan's offline union-find. |
| "Find the **distance** between `p` and `q`?" | `depth(p) + depth(q) − 2·depth(LCA)`. |
| "Why `is` rather than `==`?" | The problem is defined on nodes. Values are unique here so `==` works, but `is` states the intent. |

**Traps:**

- **Comparing values in a non-BST.** There's no ordering; you can't choose a direction.
- **Missing the self-ancestor case.** Assuming the LCA is strictly above both nodes fails on `p = 5, q = 4`.
- **Returning `root` when only one side is non-`None`.** That reports an ancestor that's too high — you must propagate the child's result.
- **Continuing to descend after finding a target.** Wasteful, and it complicates the logic for no benefit.
- **Assuming both targets exist when they might not.** The early return silently misreports. The guarantee is load-bearing.
- **Recursing on a 10⁵-node chain.** `RecursionError`.

**This same move shows up in:** [Lowest Common Ancestor of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) (the ordered version — O(h) and iterative) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (post-order combination of children's results) · [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) (each subtree returns one value while a global answer is tracked separately) · [Subtree of Another Tree](572-subtree-of-another-tree.md) (searching both subtrees when no ordering helps).

</details>

---
