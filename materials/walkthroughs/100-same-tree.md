# 100. Same Tree

**Easy** · [LeetCode](https://leetcode.com/problems/same-tree/) · [Solution file (no hints)](../../problems/0001-0499/100.py)

[📖 08. Trees lesson](../learning/08-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Trees problems](../rmap-practice/08-trees.md)

---

Given the roots of two binary trees `p` and `q`, return `true` if they are **the same** — identical in structure **and** in node values.

```
p = [1,2,3], q = [1,2,3]      →  true
p = [1,2],   q = [1,null,2]   →  false    (same values, different structure)
p = [1,2,1], q = [1,1,2]      →  false    (same shape, different values)
```

**Constraints:** `0 <= nodes in each tree <= 100` · `-10⁴ <= Node.val <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**structure and values**" | ⚠️ Both must match. `[1,2]` vs `[1,null,2]` has identical values but different shape — and is **false** |
| **two** trees | ⚠️ New shape: recurse on **two nodes at once**, walking both trees in lockstep |
| return `true`/`false` | A yes/no answer — a single mismatch is decisive, so you can bail immediately |
| either tree can be empty | Two empty trees are the same; one empty and one not are different |

The recursion is the [three-step skeleton](226-invert-binary-tree.md), but with **two arguments moving together**:

1. **Base cases** — the interesting part, because there are now *three* of them.
2. **Recurse** — compare left-to-left and right-to-right.
3. **Combine** — both must match, so `and`.

**The three base cases, in the order they must be tested:**

| Situation | Result | Why |
|---|---|---|
| **Both** `None` | `True` | Two empty trees are identical |
| **Exactly one** `None` | `False` | Different structure |
| Values differ | `False` | Same shape, wrong contents |

⚠️ **The ordering is load-bearing.** The "both `None`" check must come first — otherwise the "exactly one `None`" test would also fire when both are `None`. And both must precede `p.val != q.val`, or you'd dereference `None`.

That sequencing is the whole lesson of this problem, and it recurs whenever you recurse on a pair.

🤔 **Before you open the next section:** why can't you write the second check as `if p is None or q is None: return False` *before* the "both None" check?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Serialize both, compare strings | Convert each tree to a string, test equality | O(n) | ⚠️ Works if the serialization marks `null`s — easy to get subtly wrong |
| BFS both in lockstep | Two queues, compare as you go | O(n) | ✅ Same idea, iterative |
| **Recursive DFS on a pair** | Compare nodes, recurse on both children | **O(n)** | ✅ |

**The decision: recursive DFS taking two nodes at once.**

The novelty here isn't the traversal, it's the **signature**: `isSameTree(p, q)` rather than the single-node functions of [226](226-invert-binary-tree.md) and [104](104-maximum-depth-of-binary-tree.md). Once you see that a comparison problem takes a *pair*, the rest follows the usual shape.

**Why `and` short-circuits usefully.** `A and B` doesn't evaluate `B` if `A` is false — so the moment the left subtrees mismatch, the right subtrees are never explored. **A mismatch anywhere aborts the whole comparison**, which is why the worst case (identical trees) is the expensive one.
→ [logical-operators](../syntax/logical-operators.md)

**Why serialization is risky.** Turning each tree into a string and comparing sounds clean, but `[1,2]` and `[1,null,2]` both serialize to `"1,2"` unless you explicitly emit null markers. Get the encoding wrong and structurally different trees compare equal — the exact bug the problem's second example is designed to catch. Mention it, but the direct comparison is safer. *(This is the same ambiguity problem as [Encode and Decode Strings](271-encode-and-decode-strings.md): a format must be unambiguous by construction.)*

**Why this problem matters beyond itself.** It's a **building block**. [Subtree of Another Tree](572-subtree-of-another-tree.md) calls this function at every node of a larger tree, and [Symmetric Tree](../learning/08-trees.md) is this function with the child pairs crossed. Learn the pair-recursion shape here.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if p is None and q is None:
    return True
```

**Base case 1 — both empty.** Two empty trees are trivially identical.

⚠️ **This must come first.** It's also what makes two leaves compare equal: after matching their values, the recursion descends into all four `None` children, and each of those calls lands here.
→ [identity-operators](../syntax/identity-operators.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

```python
if p is None or q is None:
    return False
```

**Base case 2 — exactly one empty.** Reaching this line means the first check failed, so they're *not* both `None`. Therefore if either is `None`, precisely one is — a structural difference.

This is where `[1,2]` vs `[1,null,2]` gets caught: one has a left child, the other doesn't.

**The order matters.** Written before base case 1, this would return `False` for two empty trees — wrong. The checks are a sequence, not an unordered set.
→ [if-return](../syntax/if-return.md)

```python
if p.val != q.val:
    return False
```

**Base case 3 — values differ.** Safe to dereference `.val` now, because the two checks above guarantee both nodes exist.

Ordering again: put this first and you'd get `AttributeError` on `None.val`.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**Recurse and combine.** The nodes match, so the trees are the same **only if** both subtree pairs match — hence `and`.

Note the pairing: **left with left, right with right.** Crossing them (`p.left` with `q.right`) would test for mirror symmetry instead, which is a different problem.

`and` short-circuits, so a left-subtree mismatch means the right is never examined.
→ [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — `p = [1,2,3]`, `q = [1,2,3]`:

| Call | `p` | `q` | Outcome |
|---|---|---|---|
| 1 | 1 | 1 | values match → recurse both sides |
| 2 | 2 | 2 | match → recurse |
| 3 | None | None | **True** |
| 4 | None | None | **True** |
| 5 | 3 | 3 | match → recurse |
| 6,7 | None | None | **True**, **True** |

All `and`s hold → **`True`** ✅

**The structural-difference case** — `p = [1,2]` (left child), `q = [1,null,2]` (right child):

| Call | `p` | `q` | Outcome |
|---|---|---|---|
| 1 | 1 | 1 | match → recurse left |
| 2 | **2** | **None** | base case 1 fails (not both None) → base case 2 fires → **False** |

The `and` short-circuits, so the right subtrees are never compared. Result: **`False`** ✅ — even though both trees contain exactly the values 1 and 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n is the number of nodes in the **smaller** tree.

Each recursive call does O(1) work — three comparisons — and each pair of corresponding nodes is visited at most once.

**Why "smaller":** the recursion stops as soon as the structures diverge. If `q` runs out first, the calls hit base case 2 and return, never exploring the rest of `p`.

**The worst case is identical trees.** Every node of both must be examined to confirm the match — there's nothing to short-circuit on.

**The best case is O(1):** differing root values, caught immediately.

**`and`'s short-circuit is a genuine speedup in practice**, not just an idiom. A mismatch in the leftmost branch aborts the entire comparison. It doesn't change the worst-case bound, but it makes typical mismatches very cheap.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack, where h is the height of the smaller tree — **O(log n)** balanced, **O(n)** skewed.

Nothing is allocated: the trees are only read, and no structures are built. Contrast with the serialization approach, which materializes **O(n)** strings for both trees before comparing.

| Approach | Time | Space |
|---|---|---|
| **Recursive DFS** | O(n) | **O(h)** |
| Serialize + compare | O(n) | **O(n)** |
| Iterative BFS | O(n) | O(w) — two queues |

**Note the stack holds one frame per level, not per node** — the deepest chain of pending calls follows a single root-to-leaf path in both trees simultaneously.

At n ≤ 100 none of this is a practical concern, but the reasoning carries directly to [Subtree of Another Tree](572-subtree-of-another-tree.md), where this function is called repeatedly and the costs multiply.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is the standard tree recursion, but taking two nodes at a time and walking both trees in lockstep. The interesting part is the base cases and their order: first, if both nodes are null they match; second, if exactly one is null the structures differ — and that check only works *because* the both-null case was already handled; third, if the values differ they don't match, and it's safe to read `.val` now since both nodes are known to exist. Otherwise I recurse on left-with-left and right-with-right, combined with `and`, which also short-circuits so a mismatch anywhere aborts the rest. O(n) time on the smaller tree, O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why must the base cases be in that order?" | **The question.** Both-null first, or the one-null check fires on two empty trees. Both null-checks before `.val`, or you dereference `None`. |
| "Check whether a tree is **symmetric**." | The same function with the pairs crossed: compare `(a.left, b.right)` and `(a.right, b.left)`. LeetCode 101. |
| "Is one tree a **subtree** of the other?" | Run this at every node of the bigger tree — that's [Subtree of Another Tree](572-subtree-of-another-tree.md), O(n·m). |
| "Solve it by serializing." | Works, **but** you must emit explicit null markers or `[1,2]` and `[1,null,2]` collide. O(n) space. |
| "Do it iteratively." | Two queues (or one queue of pairs), comparing nodes as you dequeue. Same complexity. |
| "What if only the *values* had to match, not the structure?" | Different problem — collect both multisets of values and compare, or compare sorted traversals. |
| "Compare n-ary trees?" | Same idea: check the children lists are the same length, then zip and recurse pairwise. |

**Traps:**

- **Wrong base-case order.** The signature bug here — either two empty trees return `False`, or you crash on `None.val`.
- **Merging the null checks** into `if not p or not q: return p is q` — clever, but easy to get wrong and harder to read.
- **Crossing the recursion pairs** (`p.left` with `q.right`) — that's the symmetry check, not equality.
- **Using `or` instead of `and`** in the combine — you'd return `True` when only one side matches.
- **Comparing values before checking for `None`** → `AttributeError`.
- **Serializing without null markers** — structurally different trees compare equal.

**This same move shows up in:** [Subtree of Another Tree](572-subtree-of-another-tree.md) (calls this at every node) · [Invert Binary Tree](226-invert-binary-tree.md) (the single-tree version of the skeleton) · [Symmetric Tree](../learning/08-trees.md) (this with crossed pairs) · [Serialize and Deserialize Binary Tree](297-serialize-and-deserialize-binary-tree.md) (why null markers matter).

</details>

---
