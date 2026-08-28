# 700. Search in a Binary Search Tree

**Easy** · [LeetCode](https://leetcode.com/problems/search-in-a-binary-search-tree/) · [Solution file (no hints)](../../problems/0500-0999/700.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a **binary search tree** and an integer `val`, find the node whose value equals `val` and return **the subtree rooted at that node**. If no such node exists, return `null`.

```
root = [4,2,7,1,3], val = 2  →  [2,1,3]
root = [4,2,7,1,3], val = 5  →  []
```

**Constraints:** `1 <= number of nodes <= 5000` · `1 <= Node.val <= 10⁷` · `root` is a **BST** · `1 <= val <= 10⁷`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary search tree**" | ⚠️ The whole point. Left < node < right at **every** node, so each comparison eliminates an entire subtree |
| "return the **subtree**" | Return the node itself — in a linked structure, a node *is* its subtree |
| "`null` if not found" | Falling off the bottom means absence |
| `1 <= nodes <= 5000` | A degenerate BST could be 5000 deep — near Python's recursion limit |
| tree is guaranteed a BST | No validation needed; you may trust the ordering |

**The BST property is the entire algorithm.** At any node, comparing `val` against `node.val` tells you which way to go:

| Comparison | Meaning | Action |
|---|---|---|
| `val == node.val` | found | return this node |
| `val < node.val` | the target is smaller | go **left** — the entire right subtree is too large |
| `val > node.val` | the target is larger | go **right** — the entire left subtree is too small |

Each step discards one whole subtree. On a balanced tree that halves the search space, giving **O(h) = O(log n)** — this is [binary search](../algorithms/binary-search.md) walking a tree instead of indexing an array.

```
      4          looking for 2
     / \
    2   7        2 < 4 → go left
   / \           found ✅ (and the 7-subtree was never touched)
  1   3
```

**Why this is the simplest problem in the unit.** There's no bookkeeping, no combining of subtree results, no state to carry down. It's a single downward walk — which makes it the ideal place to internalize the BST navigation rule that [Insert into a BST](701-insert-into-a-binary-search-tree.md), [Delete Node in a BST](450-delete-node-in-a-bst.md), and [LCA of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) all build on.

🤔 **Before you open the next section:** if `val` is less than the current node's value, what do you know about every node in the right subtree?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Full DFS/BFS scan | Visit every node, compare | O(n) | O(h) or O(w) | ❌ Ignores the BST property entirely |
| **Recursive BST descent** | Compare, recurse one side | **O(h)** | O(h) stack | ✅ Reads like the definition |
| **Iterative BST descent** | Same, with a `while` loop | **O(h)** | **O(1)** | ✅✅ No stack, no recursion limit |

**The decision: descend the tree, taking one branch per comparison.** Both forms are correct; the iterative one is strictly better on space.

**Why scanning every node is the mistake to avoid.** A general tree search (`search(left) or search(right)`) works — it just throws away the property that makes a BST worth having. If an interviewer sees you traverse both subtrees, the takeaway is that you didn't notice the input was ordered. Say explicitly: *"because it's a BST, one comparison rules out an entire subtree."*

**Recursive vs iterative** — a genuine trade here, unlike most tree problems:

```python
# Recursive: O(h) stack            # Iterative: O(1) space
if not root or root.val == val:    while root and root.val != val:
    return root                        root = root.left if val < root.val else root.right
if val < root.val:                 return root
    return search(root.left)
return search(root.right)
```

The recursion is **tail recursion** — the recursive call is the last thing that happens, with nothing to do afterwards. Languages with tail-call optimization compile that into a loop automatically; **Python does not**, so the frames genuinely accumulate. Converting it by hand costs two lines and removes both the stack usage and any recursion-limit risk.

At `n = 5000`, a degenerate BST (built by inserting sorted values — see [Convert Sorted Array to BST](108-convert-sorted-array-to-binary-search-tree.md)) is 5000 levels deep, past Python's ~1000-frame default. **That's a real failure mode on this problem's constraints**, so the iterative version is the one to ship.

**Why returning the node returns the subtree.** In a linked tree representation there's no separate "subtree" object — a node holds its children, which hold theirs. Returning the matching node hands back everything beneath it, which is exactly what the expected output `[2,1,3]` shows.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**The iterative version** (preferred)

```python
def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    while root and root.val != val:
```

**Loop while there's somewhere to look and we haven't found it.**

Two exit conditions, and the `and` short-circuits so `root.val` is only read when `root` is non-`None`:

- `root` becomes `None` → the value isn't in the tree
- `root.val == val` → found

→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

```python
        root = root.left if val < root.val else root.right
```

**One comparison, one branch discarded.**

`val < root.val` → the target can only be in the left subtree, so the entire right subtree is eliminated. Otherwise (`val > root.val`, since equality already exited the loop) go right.

Reassigning `root` rather than using a separate cursor is fine here — the caller's reference is unaffected, since Python passes the reference by value.
→ [ternary-expression](../syntax/ternary-expression.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    return root
```

Either the matching node, or `None` if the walk fell off the bottom. **Both outcomes are handled by the same return** — no special case needed, because the loop's exit conditions already distinguish them by what `root` holds.

<details>
<summary>The whole thing together (iterative)</summary>

```python
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:

        while root and root.val != val:
            root = root.left if val < root.val else root.right

        return root
```

</details>

<details>
<summary>The recursive version</summary>

```python
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:

        if not root or root.val == val:
            return root

        if val < root.val:
            return self.searchBST(root.left, val)

        return self.searchBST(root.right, val)
```

Reads directly as the definition, and the combined base case (`not root or root.val == val`) neatly returns `None` for "not found" and the node for "found" in one line.

It's tail-recursive, so it's exactly the loop above — but Python doesn't optimize that away, so it costs O(h) stack.

</details>

**Trace the found case** — `root = [4,2,7,1,3]`, `val = 2`:

```
      4
     / \
    2   7
   / \
  1   3
```

| Step | `root` | `root.val != val`? | Comparison | Move |
|---|---|---|---|---|
| 1 | 4 | `4 != 2` ✅ continue | `2 < 4` | go **left** |
| 2 | 2 | `2 != 2` ❌ | — | exit loop |

Return node **2**, which carries its subtree `[2,1,3]` ✅

Note node 7 and its subtree were **never examined** — a single comparison eliminated them.

**Trace the not-found case** — `val = 5`:

| Step | `root` | Comparison | Move |
|---|---|---|---|
| 1 | 4 | `5 > 4` | go **right** |
| 2 | 7 | `5 < 7` | go **left** |
| 3 | `None` | — | loop exits (`root` is falsy) |

Return **`None`** ✅ — three steps to search a five-node tree, and the entire left subtree of 4 was skipped.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h)</summary>

**O(h)**, where `h` is the tree's height — **not** O(n).

Each iteration descends exactly one level and does O(1) work, so the cost is the path length from root to target (or to the point where the search falls off).

| Tree shape | `h` | Search cost |
|---|---|---|
| Balanced | `log n` | **O(log n)** ≈ 13 at n = 5000 |
| Degenerate (a chain) | `n` | **O(n)** = 5000 |

**Why O(h) rather than O(log n).** The bound depends on the tree's *shape*, which nothing here guarantees. A BST built by inserting sorted values is a linked list, and search degrades to linear. Self-balancing variants (AVL, red-black) enforce `h = O(log n)` precisely to make this worst case impossible.

Stating the bound as **O(h)** and then noting it's O(log n) *when balanced* is the precise answer — quoting O(log n) unconditionally is a common imprecision.

**Compare to a full traversal:** O(n) always. On a balanced 5000-node tree that's 5000 comparisons versus about 13.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) iterative, O(h) recursive</summary>

| Approach | Space |
|---|---|
| **Iterative** | **O(1)** — one reassigned pointer |
| Recursive | O(h) — call frames |
| Full BFS scan | O(w) — up to O(n) for a wide tree |

**This is one of the few tree problems where iteration is genuinely, not just stylistically, better.** Most tree algorithms need to *return* to a node after processing its children — computing a height, combining subtree results — and that requires a stack. Here the search only ever goes **down**, never back up, so there's nothing to remember.

> **When a tree algorithm never needs to revisit an ancestor, it can be written iteratively in O(1) space.**

Search, insert ([701](701-insert-into-a-binary-search-tree.md)), and BST-LCA ([235](235-lowest-common-ancestor-of-a-binary-search-tree.md)) all qualify. Height, diameter, and validation do not.

**The practical consequence:** at `n = 5000`, a degenerate BST would give the recursive version a `RecursionError`. The iterative version handles it fine.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because it's a BST, one comparison at each node eliminates an entire subtree — if the target is smaller than the current node, it can only be on the left, so the whole right subtree is ruled out. So I walk down, going left or right based on the comparison, until I either find the value or fall off the bottom. That's O(h): O(log n) on a balanced tree, but O(n) if the tree is degenerate, since nothing here guarantees balance. I'd write it **iteratively** — the search only ever moves downward and never revisits an ancestor, so there's nothing to keep on a stack, making it O(1) space. That also matters practically: with 5000 nodes a degenerate BST would exceed Python's recursion limit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why O(h) and not O(log n)?" | **The precise answer.** Height depends on shape; a degenerate BST is a chain. O(log n) only holds when balanced. |
| "Recursive or iterative?" | Iterative — the recursion is tail-recursive, Python doesn't optimize it, and iteration gives O(1) space plus no recursion limit. |
| "Guarantee O(log n)?" | Use a self-balancing BST — AVL or red-black — which enforce `h = O(log n)` via rotations. |
| "**Insert** a value instead?" | [Problem 701](701-insert-into-a-binary-search-tree.md) — same descent, then attach a new node where you'd have fallen off. |
| "**Delete** a value?" | [Problem 450](450-delete-node-in-a-bst.md) — same descent to find it, then three cases depending on its children. |
| "What if it weren't a BST?" | You'd have to check every node — O(n) DFS or BFS. |
| "Find the closest value to `val`?" | Same descent, tracking the best candidate seen at each step. |

**Traps:**

- **Searching both subtrees.** Correct but O(n) — it discards the entire reason a BST exists.
- **Checking `root.val` before `root`.** `AttributeError` on `None`; order the `and` correctly.
- **Returning `root.val` or `True`.** The problem wants the **node** (hence the subtree).
- **Special-casing "not found".** The loop already exits with `root = None`; one `return root` covers both outcomes.
- **Quoting O(log n) unconditionally.** It's O(h), which is O(n) in the worst case.
- **Recursing on a degenerate 5000-node tree.** `RecursionError`.

**This same move shows up in:** [Insert into a Binary Search Tree](701-insert-into-a-binary-search-tree.md) (the same descent, ending in an attachment) · [Delete Node in a BST](450-delete-node-in-a-bst.md) (the same descent, followed by restructuring) · [Lowest Common Ancestor of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) (descending until the two targets split) · [Binary Search](704-binary-search.md) (the array form of the identical idea).

</details>

---
