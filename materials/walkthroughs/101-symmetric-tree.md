# 101. Symmetric Tree

**Easy** · [LeetCode](https://leetcode.com/problems/symmetric-tree/) · [Solution file (no hints)](../../problems/0001-0499/101.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, check whether it is a **mirror of itself** — symmetric around its centre.

```
root = [1,2,2,3,4,4,3]        →  true
root = [1,2,2,null,3,null,3]  →  false
```

**Constraints:** `1 <= number of nodes <= 1000` · `-100 <= Node.val <= 100`

**Follow-up:** could you solve it both recursively and iteratively?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**mirror of itself**" | ⚠️ Symmetry is about the **shape and values** of the two subtrees reflected, not about any single subtree |
| "symmetric **around its centre**" | Compare `root.left` against `root.right`, mirrored |
| structure matters | `[1,2,2,null,3,null,3]` is `false` even though both sides contain a 3 — the *positions* differ |
| `1 <= nodes` | Never empty, so the root always exists |
| `n` up to 1000 | Any O(n) approach is fine |

**The key reframing.** You can't check symmetry by examining one subtree — symmetry is a relationship *between two* trees. So generalize the question:

> Instead of *"is this tree symmetric?"*, ask *"are these two trees mirror images of each other?"* — then call it with `root.left` and `root.right`.

That's the standard move when a recursive definition doesn't fit the given signature: **write a helper with the arguments the recursion actually needs.**

**What "mirror" means precisely.** Two trees `a` and `b` are mirrors when:

1. Both are `None` — trivially mirrored ✅
2. Exactly one is `None` — shapes differ ❌
3. `a.val == b.val` **and** `a.left` mirrors `b.right` **and** `a.right` mirrors `b.left`

Case 3 is where the mirroring lives: **outer pairs with outer, inner pairs with inner**.

```
        1
      /   \
     2     2
    / \   / \
   3   4 4   3
   ↑         ↑        outer pair: a.left ↔ b.right
       ↑  ↑           inner pair: a.right ↔ b.left
```

Compare `a.left` with `b.left` (the intuitive but wrong pairing) and you're testing whether the subtrees are **identical**, not mirrored — which is [Same Tree](100-same-tree.md), a different problem.

🤔 **Before you open the next section:** if you're comparing the left and right subtrees, which child of the left should line up with which child of the right?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Inorder traversal, check palindrome | Serialize and compare with its reverse | O(n) | O(n) | ❌ **Wrong** — different trees can share a traversal |
| Mirror the tree, then compare | Build a reversed copy, run [Same Tree](100-same-tree.md) | O(n) | **O(n)** | ⚠️ Correct, allocates a whole tree |
| **Recursive mirror check** | Compare outer/inner pairs | **O(n)** | **O(h)** | ✅ |
| **Iterative with a queue/stack** | Enqueue pairs to compare | **O(n)** | O(w) | ✅ Answers the follow-up |

**The decision: a recursive helper comparing two nodes for mirror-ness.**

**Why the traversal-palindrome idea fails**, since it's a tempting shortcut: an inorder traversal doesn't uniquely determine a tree's shape. Both of these produce the inorder sequence `[2, 1, 2]`:

```
    1              1
   / \            / \
  2   2          2   2      ← symmetric ✅
```
versus a tree where the `null` positions differ — the values line up but the structure doesn't. Even including `null` markers, the palindrome check is fiddly to get right. Structural comparison is both simpler and obviously correct.

**Why `None` handling needs three cases, not two.** You must distinguish:

- **both `None`** → mirrored (two empty subtrees match)
- **one `None`** → not mirrored (shapes differ)

Collapsing these into `if not a or not b: return False` is wrong — it rejects two empty subtrees, which are perfectly symmetric. Getting this ordering right is the most common source of bugs here.

**The iterative version** (for the follow-up) enqueues **pairs** rather than single nodes:

```python
queue = deque([(root.left, root.right)])
while queue:
    a, b = queue.popleft()
    if not a and not b: continue
    if not a or not b or a.val != b.val: return False
    queue.append((a.left, b.right))    # outer
    queue.append((a.right, b.left))    # inner
return True
```

The insight is that the *pairing* is what gets queued, not individual nodes — and the same outer/inner rule applies. A stack works identically; only the traversal order changes, not the result.

**Why not build a mirrored copy?** It works and reuses [Same Tree](100-same-tree.md), but allocates `n` new nodes for a question answerable by comparison alone.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def isSymmetric(self, root: Optional[TreeNode]) -> bool:
    if not root:
        return True
    return self.isMirror(root.left, root.right)
```

**Reduce the problem to the helper.** The public signature takes one tree; the recursion needs two, so the entry point immediately delegates.

An empty tree is vacuously symmetric (the constraints exclude it, but the guard costs nothing).
→ [function-basics](../syntax/function-basics.md)

---

**The helper — are these two trees mirrors?**

```python
def isMirror(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if not a and not b:
        return True
```

**Both empty → mirrored.** Two absent subtrees match perfectly.

This case must come **first**. Testing `if not a or not b` first would reject this valid case.
→ [logical-operators](../syntax/logical-operators.md)

```python
    if not a or not b:
        return False
```

**Exactly one empty → not mirrored.** Reaching this line means at least one is non-`None` (the previous check ruled out both being `None`), so if either is `None` the shapes differ.

The ordering of these two checks is the crux: *both-empty* before *one-empty*.

```python
    return (a.val == b.val
            and self.isMirror(a.left, b.right)
            and self.isMirror(a.right, b.left))
```

**The mirror condition, in three parts:**

1. `a.val == b.val` — the reflected nodes hold the same value
2. `a.left` ↔ `b.right` — the **outer** pair
3. `a.right` ↔ `b.left` — the **inner** pair

The crossed pairing in lines 2–3 is what makes this a *mirror* test rather than an *equality* test. Pair `a.left` with `b.left` and you've written [Same Tree](100-same-tree.md).

`and` short-circuits, so a value mismatch skips both recursive calls.
→ [recursion-basics](../syntax/recursion-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        return self.isMirror(root.left, root.right)

    def isMirror(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if not a and not b:
            return True
        if not a or not b:
            return False
        return (a.val == b.val
                and self.isMirror(a.left, b.right)
                and self.isMirror(a.right, b.left))
```

</details>

<details>
<summary>The iterative version (the follow-up)</summary>

```python
from collections import deque

class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        queue = deque([(root.left, root.right)])
        while queue:
            a, b = queue.popleft()

            if not a and not b:
                continue
            if not a or not b or a.val != b.val:
                return False

            queue.append((a.left, b.right))   # outer pair
            queue.append((a.right, b.left))   # inner pair

        return True
```

Queues **pairs** to compare rather than individual nodes. Same outer/inner rule, no recursion.

</details>

**Trace the symmetric case** — `[1,2,2,3,4,4,3]`:

```
        1
      /   \
     2     2
    / \   / \
   3   4 4   3
```

| Call | `a` | `b` | Check | Recurses into |
|---|---|---|---|---|
| 1 | 2 (left) | 2 (right) | `2 == 2` ✅ | (3, 3) outer · (4, 4) inner |
| 2 | 3 | 3 | `3 == 3` ✅ | (None, None) ×2 |
| 3 | 4 | 4 | `4 == 4` ✅ | (None, None) ×2 |
| 4–7 | `None` | `None` | both empty ✅ | — |

Return **`true`** ✅

Note call 1's pairing: `a.left = 3` with `b.right = 3`, and `a.right = 4` with `b.left = 4`. Pairing left-with-left would have compared 3 against 4 and returned `false`.

**Trace the asymmetric case** — `[1,2,2,null,3,null,3]`:

```
      1
     / \
    2   2
     \   \
      3   3
```

| Call | `a` | `b` | Check | Result |
|---|---|---|---|---|
| 1 | 2 | 2 | values match ✅ | recurse (a.left=None, b.right=3) and (a.right=3, b.left=None) |
| 2 | `None` | 3 | not both empty; **one is `None`** | **`false`** ❌ |

Return **`false`** ✅ — and correctly so: both 3s hang off the *right* side of their parents, so the tree leans rather than mirrors. A value-only check would have been fooled.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited at most once as part of exactly one comparison pair. With `n` nodes there are at most `n/2` pairs, each doing O(1) work — **O(n)**.

**Better in practice** thanks to short-circuiting `and`: a mismatch near the top returns immediately without exploring the rest. The `[1,2,2,null,3,null,3]` trace above terminated after two comparisons.

| Case | Nodes examined |
|---|---|
| Mismatch near the root | O(1) |
| Fully symmetric | O(n) |

You can't do better than O(n) in the worst case — confirming symmetry requires checking every node.

**Both the recursive and iterative versions are O(n)**; they differ only in traversal order and where the pending work is stored.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h) or O(w)</summary>

| Approach | Space | Worst case |
|---|---|---|
| **Recursive** | O(h) — call stack | O(n) for a degenerate tree |
| **Iterative (queue)** | O(w) — pending pairs | O(n) for a wide tree |

At `n <= 1000` both are comfortably safe — a degenerate tree is 1000 frames deep, right at Python's default limit but typically fine, and the iterative version avoids the question entirely.

**Compare with building a mirrored copy:** that's **O(n)** space for `n` new nodes, plus the traversal cost — strictly worse for a question that only needs comparison.

**The transferable idea:**

> **When the recursion needs more arguments than the given signature provides, write a helper.** Here the public API takes one tree but the natural recursion compares two.

The same pattern appears in [Same Tree](100-same-tree.md) (two trees by definition), [Validate BST](98-validate-binary-search-tree.md) (a node plus min/max bounds), and [Subtree of Another Tree](572-subtree-of-another-tree.md) (which calls a two-tree comparison at every node).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Symmetry is a relationship between two subtrees, not a property of one — so I generalize to a helper that asks 'are these two trees mirror images?' and call it with `root.left` and `root.right`. Two trees mirror when both are empty, or when their values match and — the key part — `a.left` mirrors `b.right` while `a.right` mirrors `b.left`. That crossed pairing is what makes it a mirror test; pairing left with left would be Same Tree. The base cases must be ordered: both-`None` returns true first, then exactly-one-`None` returns false — collapsing them would reject two empty subtrees. O(n) time, O(h) space. Iteratively I'd queue **pairs** of nodes rather than single nodes, applying the same outer/inner rule."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it iteratively." | **The stated follow-up** — queue `(a, b)` pairs, enqueue `(a.left, b.right)` and `(a.right, b.left)`. |
| "Why crossed pairing?" | Mirroring reflects positions: outer-with-outer, inner-with-inner. Left-with-left tests equality, not symmetry. |
| "Why not compare an inorder traversal to its reverse?" | Traversals don't uniquely determine structure, so different trees can produce the same sequence. |
| "How does this relate to [Same Tree](100-same-tree.md)?" | Identical skeleton; Same Tree pairs left-left and right-right, this pairs left-right and right-left. |
| "Mirror the tree in place?" | [Invert Binary Tree](226-invert-binary-tree.md) — then symmetry is `isSameTree(root.left, inverted_right)`. |
| "What if values could be `None`?" | Compare with `is` / explicit sentinels; `==` on `None` still works but state your assumption. |
| "Does it handle a single node?" | Yes — `isMirror(None, None)` returns `true`. |

**Traps:**

- **Pairing `a.left` with `b.left`.** *The* bug — that's an equality check, not a mirror check.
- **Checking `if not a or not b: return False` first.** Rejects two empty subtrees, which are symmetric. Order matters.
- **Comparing only values, ignoring structure.** `[1,2,2,null,3,null,3]` has matching values on both sides but is asymmetric.
- **Recursing on `root` itself instead of its two children.** The helper needs two subtrees to compare.
- **Serializing to a list and reversing.** Traversals don't capture shape uniquely.
- **Enqueuing single nodes in the iterative version.** The *pair* is the unit of work.

**This same move shows up in:** [Same Tree](100-same-tree.md) (the same two-tree recursion with straight pairing) · [Subtree of Another Tree](572-subtree-of-another-tree.md) (runs a two-tree comparison at every node) · [Invert Binary Tree](226-invert-binary-tree.md) (constructs the mirror this problem detects) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (another helper carrying extra arguments the public signature lacks).

</details>

---
