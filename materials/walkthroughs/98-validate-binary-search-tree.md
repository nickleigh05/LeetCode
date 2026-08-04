# 98. Validate Binary Search Tree

**Medium** · [LeetCode](https://leetcode.com/problems/validate-binary-search-tree/) · [Solution file (no hints)](../../problems/0001-0499/98.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, determine if it is a **valid binary search tree**.

A valid BST satisfies, at **every** node:
- The **entire** left subtree contains only values **less than** the node.
- The **entire** right subtree contains only values **greater than** the node.
- Both subtrees are themselves valid BSTs.

```
        2                  valid ✅
      /   \
     1     3

        5                  INVALID ❌
      /   \                4 is in 5's right subtree
     1     4               but 4 < 5
          / \
         3   6
```

**Constraints:** `1 <= nodes <= 10⁴` · `-2³¹ <= Node.val <= 2³¹ − 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the **entire** left subtree" | ⚠️ **The whole trap.** Not just the immediate child — *every* descendant must obey the constraint |
| "**less than** / **greater than**" | Strict. Duplicates make a tree invalid |
| "both subtrees are themselves valid" | The condition is recursive, holding at every node |
| values span the **full 32-bit range** | ⚠️ Sentinels like `-2³¹` or `2³¹−1` are *legal node values*, so they can't safely mean "no bound" |
| n up to 10⁴ | O(n), and a skewed tree risks the recursion limit |

**The trap, made concrete.** The obvious check is local:

```python
node.left.val < node.val < node.right.val      # ← WRONG
```

Apply it to the invalid example:

```
        5
      /   \
     1     4          node 5: 1 < 5 < 4? → checks 1 < 5 ✅
          / \         node 4: 3 < 4 < 6 ✅
         3   6        every LOCAL check passes...
```

…yet the tree is **not** a BST. Node 3 sits in 5's right subtree but is smaller than 5. **Local checks can't see that constraint**, because it comes from an ancestor two levels up.

**The correct framing: every node inherits a valid range.**

```
                        (-∞, +∞)
        5
      /        \
 (-∞, 5)      (5, +∞)
   1              4        ← 4 is in (5, ∞)? 4 > 5 is FALSE → invalid ✅ caught
                /   \
            (5, 4)  (4, ∞)
              3               ← would need 5 < 3 < 4 → invalid
```

Descending **left** tightens the upper bound to the current value; descending **right** tightens the lower bound. A node is valid only if it falls strictly inside its inherited range.

This is a **top-down** problem — context flows from ancestors to descendants as parameters, just like [Count Good Nodes](1448-count-good-nodes-in-binary-tree.md), but carrying *two* bounds instead of one maximum.

🤔 **Before you open the next section:** when you descend into the left child, which bound changes and what does it become? What about the right?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Check `left < node < right` locally | Compare with immediate children only | O(n) | ❌ **Wrong** — misses ancestor constraints |
| Check min/max of each subtree | At each node, scan its subtrees for extremes | O(n²) | ⚠️ Correct but re-walks subtrees |
| **Inorder traversal, verify ascending** | A BST's inorder is strictly increasing | O(n) | ✅ Elegant alternative |
| **Range propagation** | Pass `(lower, upper)` down | **O(n)** | ✅ |

**The decision: propagate a valid `(lower, upper)` range down the recursion.**

At each node:
1. Verify `lower < node.val < upper`. Fail → the whole tree is invalid.
2. **Left child** gets `(lower, node.val)` — everything left must stay below this node.
3. **Right child** gets `(node.val, upper)` — everything right must stay above it.

Both bounds only ever *tighten* on the way down, which is exactly how an ancestor's constraint reaches a distant descendant.

**Why `None` for "no bound".** The root has no constraints in either direction. Using `float("-inf")` and `float("inf")` also works in Python, but `None` is safer in general: node values span the **full 32-bit range**, so `-2³¹` is a legal value and any *integer* sentinel could collide with real data. `None` is unambiguous. *(This is the same "pick a sentinel that can't be confused with data" concern as [Encode and Decode Strings](271-encode-and-decode-strings.md).)*

**The inorder alternative is genuinely good and worth naming.** A tree is a BST **if and only if** its inorder traversal (left → node → right) is strictly ascending. So traverse inorder, tracking the previously-visited value, and fail if the sequence ever doesn't increase. Same O(n), and it doubles as a neat characterization of BSTs.

**Why the subtree-min/max approach is O(n²):** at each node you'd rescan its entire subtree for the extremes — the same repeated-work problem as the naive [Balanced Binary Tree](110-balanced-binary-tree.md). Range propagation carries the constraint *down* instead of searching for it *up*.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def validate(node, lower_bound, upper_bound):
    if node is None:
        return True
```

The helper takes the node **plus its inherited range**. An empty subtree vacuously satisfies any constraint — nothing in it can violate a bound.
→ [function-basics](../syntax/function-basics.md) · [identity-operators](../syntax/identity-operators.md) · [none-type](../syntax/none-type.md)

```python
    if lower_bound is not None and node.val <= lower_bound:
        return False
```

**Check the lower bound**, if one exists. `None` means unconstrained below, so the test is skipped.

`<=` enforces **strictness** — a value equal to the bound is a duplicate, which makes the tree invalid.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if upper_bound is not None and node.val >= upper_bound:
        return False
```

Mirror check on the upper side.

Note `and` short-circuits: `node.val <= lower_bound` is only evaluated once `lower_bound` is known non-`None`, so no comparison against `None` ever happens.
→ [if-return](../syntax/if-return.md)

```python
    left_valid = validate(node.left, lower_bound, node.val)
```

**Descend left — the upper bound tightens to `node.val`.** Everything in the left subtree must be less than this node, *and* still satisfy whatever lower bound was inherited.

The lower bound passes through **unchanged**: an ancestor's "must exceed 5" still applies down here.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
    right_valid = validate(node.right, node.val, upper_bound)
```

**Descend right — the lower bound tightens to `node.val`.** Symmetric: everything right must exceed this node, and the inherited upper bound carries through.

**These two lines are the entire solution.** They're what let a constraint from node 5 reach its grandchild 3, which the local check couldn't see.

```python
    return left_valid and right_valid
```

Both subtrees must be valid. `and` short-circuits, so a failure on the left skips the right entirely.
→ [logical-operators](../syntax/logical-operators.md)

```python
return validate(root, None, None)
```

The root is unconstrained in both directions.

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it — the invalid tree** `[5,1,4,null,null,3,6]`:

```
        5
      /   \
     1     4
          / \
         3   6
```

| Node | Inherited range | Check | Result |
|---|---|---|---|
| 5 | (None, None) | unconstrained | ✅ continue |
| 1 | (None, **5**) | 1 < 5 ✅ | ✅ |
| **4** | (**5**, None) | 4 > 5? **✗** | ❌ **`False`** |

Caught at node 4 — the local check would have passed it, but the inherited lower bound of 5 exposes the violation immediately. The subtree below (3 and 6) is never even visited.

**And a valid tree** `[2,1,3]`:

| Node | Range | Check |
|---|---|---|
| 2 | (None, None) | ✅ |
| 1 | (None, 2) | 1 < 2 ✅ |
| 3 | (2, None) | 3 > 2 ✅ |

→ **`True`** ✅

**A subtler invalid case** — `[10, 5, 15, null, null, 6, 20]`:

| Node | Range | Check |
|---|---|---|
| 10 | (None, None) | ✅ |
| 15 | (10, None) | 15 > 10 ✅ |
| **6** | (**10**, 15) | 6 > 10? **✗** | ❌ |

Node 6 is a valid left child of 15 locally, but it's in 10's right subtree and must exceed 10. **The range carried the ancestor's constraint down two levels.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited at most once, doing O(1) work — two bound comparisons.

n × O(1) = **O(n)**, and it's optimal: a violation could be anywhere, so every node must be checked.

**Early exit helps in practice.** The first violation returns `False`, and `and` short-circuits all the way up — so an invalid tree often costs far less than n. The O(n) bound is the worst case, a fully valid tree.

**Versus the subtree-min/max approach.** Scanning each node's subtrees for extremes costs O(size of subtree) per node → O(n·h), i.e. **O(n²)** on a skewed tree = 10⁸ at the constraint limit. **Carrying the constraint down beats searching for it.** Same lesson as the top-down vs bottom-up contrast in [Balanced Binary Tree](110-balanced-binary-tree.md).

**The inorder alternative is also O(n)** — one traversal comparing each value to the previous.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack — **O(log n)** balanced, **O(n)** skewed.

The two bounds are O(1) per frame, so the carried context adds nothing asymptotically. Contrast with an approach that passed a *set* of ancestor constraints — that would be O(h) per frame and O(h²) overall.

At n = 10⁴ a skewed tree means 10⁴ frames, past Python's default recursion limit of 1000. Converting to iteration is easy here because the problem is **top-down**: push `(node, lower, upper)` triples onto a stack.
→ [recursion-limit](../syntax/recursion-limit.md)

**The inorder alternative has the same O(h)** — an explicit stack of pending nodes.

**A note on the iterative inorder version:** it only needs to remember **one** previous value rather than a pair of bounds, which some find simpler:

```python
stack, prev = [], None
while stack or node:
    while node: stack.append(node); node = node.left
    node = stack.pop()
    if prev is not None and node.val <= prev: return False
    prev, node = node.val, node.right
```

That's the same skeleton as [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) — worth recognizing.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The trap is that checking `left < node < right` locally isn't enough — a node deep in a right subtree still has to exceed an ancestor several levels up, and a local check can't see that. So instead I propagate a valid range down: each node must fall strictly inside `(lower, upper)`, and when I descend left the upper bound tightens to the current value, while descending right tightens the lower bound. The inherited bound on the other side passes through unchanged, which is how an ancestor's constraint reaches a distant descendant. I use `None` for 'no bound' rather than a sentinel integer, because node values span the full 32-bit range. O(n) time, O(h) space. An equally good alternative is an inorder traversal checking that values strictly increase — that's a defining property of a BST."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't the local check enough?" | **The question.** Demo with `[5,1,4,null,null,3,6]` — every local check passes but 3 and 4 violate node 5's constraint. |
| "Solve it with inorder traversal." | A BST's inorder is strictly ascending. Traverse, keep the previous value, fail if it doesn't increase. |
| "Why `None` and not `float('-inf')`?" | Works in Python, but node values span the full int32 range — in a language with fixed-width ints, a sentinel could collide with real data. |
| "What about **duplicates**?" | Invalid under this definition, enforced by `<=` and `>=`. If duplicates were allowed on one side, relax that one comparison. |
| "What if the tree is 10⁴ deep?" | Recursion overflows. Use an explicit stack of `(node, lower, upper)` — easy, since it's top-down. |
| "Find the **largest** valid BST subtree?" | Bottom-up: each node returns `(is_bst, min, max, size)`. LeetCode 333, notably harder. |
| "Recover a BST with two swapped nodes?" | Inorder traversal, find the two out-of-order positions, swap them back. LeetCode 99. |

**Traps:**

- **The local `left < node < right` check.** The defining mistake — it passes on trees that aren't BSTs.
- **Comparing against `None`** without guarding. `node.val <= None` raises `TypeError` in Python 3.
- **Passing the wrong bound when descending.** Left tightens the *upper*; right tightens the *lower*. Getting them backwards inverts the whole check.
- **Using `<` / `>` instead of `<=` / `>=`** in the failure tests — duplicates would slip through.
- **Resetting the untouched bound** to `None` when descending. The inherited constraint must carry through, or ancestor violations go undetected.
- **Assuming a valid tree and returning early on the first success.** You need *all* nodes to pass.

**This same move shows up in:** [Count Good Nodes](1448-count-good-nodes-in-binary-tree.md) (the other top-down problem — carries one max instead of two bounds) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (the inorder skeleton) · [Lowest Common Ancestor of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) (BST ordering for navigation rather than verification) · [binary-search-tree](../data-structures/binary-search-tree.md).

</details>
