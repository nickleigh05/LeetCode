# 701. Insert into a Binary Search Tree

**Medium** · [LeetCode](https://leetcode.com/problems/insert-into-a-binary-search-tree/) · [Solution file (no hints)](../../problems/0500-0999/701.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a **binary search tree** and a value to insert, insert it into the BST and return the root. The value **does not exist** in the original tree. Any valid resulting BST is accepted.

```
root = [4,2,7,1,3], val = 5  →  [4,2,7,1,3,5]
root = [40,20,60,10,30,50,70], val = 25  →  [40,20,60,10,30,50,70,null,null,25]
root = [], val = 5  →  [5]
```

**Constraints:** `0 <= number of nodes <= 10⁴` · `-10⁸ <= Node.val <= 10⁸` · all values **unique** · `-10⁸ <= val <= 10⁸` · `val` is **not** already present

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary search tree**" | The same descent as [Search in a BST](700-search-in-a-binary-search-tree.md) — one comparison eliminates a subtree |
| "`val` **does not exist**" | ⚠️ No duplicate handling needed. The search always falls off the bottom |
| "**any valid** resulting BST" | ⚠️ Liberating — you don't have to rebalance or match a specific shape |
| "return the **root**" | Usually unchanged; only an empty tree makes the new node the root |
| `0 <= nodes` | An empty tree must return a single-node tree |
| `n` up to 10⁴ | A degenerate BST is 10⁴ deep — past Python's recursion limit |

**The insight, and it's the reason this problem is Easy-in-disguise:**

> **The correct insertion point is always where the search for `val` would fall off the bottom.**

Search for `val`. Since it isn't present, you eventually reach a `None` child. That empty slot is exactly where the value belongs — because every comparison on the way down established the ordering constraints that make it valid there.

```
      4          inserting 5
     / \
    2   7        5 > 4 → right
   / \  /        5 < 7 → left
  1  3 5 ←       7.left is None → attach here ✅
```

**Why you never need to rebalance.** The problem says "any valid BST," so a leaf insertion is fine even if it makes the tree taller and less balanced. Real self-balancing trees (AVL, red-black) perform rotations after insertion to keep `h = O(log n)`; this problem deliberately doesn't ask for that, which is what keeps it tractable.

That's worth stating explicitly — an interviewer may probe whether you know the difference between "insert into a BST" and "insert into a *balanced* BST."

🤔 **Before you open the next section:** if you search for a value that isn't in the tree, where does the search end — and what makes that spot the right place to put it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect all values, rebuild | Inorder-traverse, insert into the sorted list, rebuild | O(n) | **O(n)** | ❌ Enormously over-engineered |
| **Recursive insertion** | Descend, returning the (possibly new) subtree | **O(h)** | O(h) stack | ✅ Very clean |
| **Iterative insertion** | Descend with a loop, attach when a slot is `None` | **O(h)** | **O(1)** | ✅✅ No recursion limit |

**The decision: descend to the empty slot and attach.** The solution file uses the iterative form.

**The two structures compared:**

```python
# Recursive — "return the subtree"      # Iterative — "attach when the child is None"
if not root: return TreeNode(val)        if not root: return TreeNode(val)
if val < root.val:                       node = root
    root.left = insert(root.left, val)   while True:
else:                                        if val < node.val:
    root.right = insert(root.right, val)         if not node.left:
return root                                          node.left = TreeNode(val); break
                                                 node = node.left
                                             else: ... mirror ...
                                         return root
```

**The recursive version's trick** is that each call **returns the subtree it's responsible for**, and the parent reassigns it. Most of the time that reassignment is a no-op (`root.left = root.left`), but at the bottom the `None` case returns a brand-new node, and the reassignment is what actually attaches it. That "recurse and reassign" idiom is worth learning — it's the same shape used by [Delete Node in a BST](450-delete-node-in-a-bst.md).

**The iterative version's structure** is a `while True` loop with explicit `break`s. It checks *before* descending: if the child you'd move to is `None`, attach there and stop. That look-ahead is what lets it insert without needing a parent pointer.

**Why iterative wins here.** As in [Search in a BST](700-search-in-a-binary-search-tree.md), insertion only ever moves **downward** — it never needs to return to an ancestor — so no stack is required. At `n = 10⁴`, a BST built from sorted input is 10⁴ levels deep, well past Python's ~1000-frame limit. The recursive version would raise `RecursionError` on exactly that input.

**Why the empty-tree case must come first.** With `root = None` there's nothing to descend, so the new node *is* the tree. Both versions handle it with the same one-line guard.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return TreeNode(val)
```

**Empty tree → the new node becomes the root.**

Must come first: everything below dereferences `root`.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [class-basics](../syntax/class-basics.md)

```python
node = root
while True:
```

A separate cursor so `root` stays intact for the final return. `while True` with explicit `break`s reads more naturally here than trying to encode "stop when we've attached" as a loop condition.
→ [while-loop](../syntax/while-loop.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
    if val < node.val:
        if not node.left:
            node.left = TreeNode(val)
            break
        node = node.left
```

**Go left — but check the slot before moving into it.**

The **look-ahead** is the key structural detail. If `node.left` is `None`, this is the insertion point: create the node, attach it, and stop. Otherwise descend and repeat.

Checking before descending is what avoids needing a parent pointer — once you've moved to a `None` you'd have lost the reference needed to attach.
→ [comparison-operators](../syntax/comparison-operators.md) · [break-continue](../syntax/break-continue.md)

```python
    else:
        if not node.right:
            node.right = TreeNode(val)
            break
        node = node.right
```

The mirror case for `val > node.val`.

`else` rather than `elif val > node.val` is safe **only because the problem guarantees no duplicates** — equality never occurs. If duplicates were possible you'd need an explicit policy (go right, or keep a count), and this `else` would silently place them.
→ [elif-else](../syntax/elif-else.md)

```python
return root
```

**Return the original root**, unchanged — the tree was modified in place. Only the empty-tree case returns something different.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:

        if not root:
            return TreeNode(val)

        node = root
        while True:
            if val < node.val:
                if not node.left:
                    node.left = TreeNode(val)
                    break
                node = node.left
            else:
                if not node.right:
                    node.right = TreeNode(val)
                    break
                node = node.right

        return root
```

</details>

<details>
<summary>The recursive version</summary>

```python
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)

        return root
```

Six lines, and the "recurse and reassign" idiom does the attaching: most reassignments are no-ops, but the one at the bottom binds the newly created node. Costs O(h) stack.

</details>

**Trace it** — `root = [4,2,7,1,3]`, `val = 5`:

```
      4
     / \
    2   7
   / \
  1   3
```

| Step | `node` | Compare | Slot check | Action |
|---|---|---|---|---|
| 1 | 4 | `5 > 4` → right | `node.right` = 7, exists | descend to 7 |
| 2 | 7 | `5 < 7` → left | `node.left` is **`None`** | **attach 5 as 7.left**, break |

Result:

```
      4
     / \
    2   7
   / \  /
  1  3 5
```

Return the original root ✅ — and note only 2 comparisons were needed for a 5-node tree, with the left subtree never examined.

**A second trace** — `root = [40,20,60,10,30,50,70]`, `val = 25`:

| Step | `node` | Compare | Slot | Action |
|---|---|---|---|---|
| 1 | 40 | `25 < 40` → left | 20 exists | descend |
| 2 | 20 | `25 > 20` → right | 30 exists | descend |
| 3 | 30 | `25 < 30` → left | **`None`** | attach 25 as 30.left ✅ |

Verify the BST property: 25 sits below 30 (so `25 < 30` ✅), which is under 20's right (so `25 > 20` ✅), which is under 40's left (so `25 < 40` ✅). **Every comparison made on the way down is exactly the constraint that makes the position valid** — which is why the fall-off point is always correct.

**The empty case** — `root = None`, `val = 5`: the first guard fires and returns a single node `[5]` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h)</summary>

**O(h)**, where `h` is the tree height.

The descent visits one node per level until it finds an empty slot, doing O(1) work each — a comparison, a `None` check, and possibly one allocation.

| Tree shape | `h` | Insert cost |
|---|---|---|
| Balanced | `log n` | **O(log n)** ≈ 14 at n = 10⁴ |
| Degenerate | `n` | **O(n)** = 10⁴ |

**The classic degradation.** Inserting **sorted** values one at a time gives a chain: each new value is larger than everything, so it always goes right. Building an `n`-node tree that way costs `1 + 2 + … + n` = **O(n²)** and produces height `n`.

That's precisely the failure mode [Convert Sorted Array to BST](108-convert-sorted-array-to-binary-search-tree.md) exists to avoid, and the reason AVL and red-black trees perform rotations after insertion.

**This problem doesn't ask you to rebalance** — "any valid BST" is accepted — so a leaf insertion is correct even when it worsens the shape. Knowing that you *could* be asked to rebalance, and that it would require rotations, is the depth worth showing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) iterative, O(h) recursive</summary>

| Approach | Space |
|---|---|
| **Iterative** | **O(1)** — one cursor plus the new node |
| Recursive | O(h) stack |
| Rebuild from sorted values | O(n) |

The new `TreeNode` is O(1) — a single allocation regardless of tree size.

**Why O(1) is achievable**, same reasoning as [Search in a BST](700-search-in-a-binary-search-tree.md):

> Insertion only ever moves **downward** and never revisits an ancestor, so there is nothing to remember and no stack is needed.

The one thing the iterative version must do that search doesn't is **look ahead** — check whether the child slot is `None` *before* descending — because once you've moved into a `None` you've lost the parent reference needed to attach. That look-ahead is the price of dropping the stack, and it's why the loop body is slightly longer than search's.

**The practical stakes:** at `n = 10⁴`, a degenerate BST makes the recursive version raise `RecursionError`. The iterative one is unaffected.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The insertion point is wherever a search for the value would fall off the bottom — and since the problem guarantees the value isn't already present, that always happens. Every comparison made on the way down is exactly the ordering constraint that makes the final position valid, so attaching there always preserves the BST property. I write it iteratively: descend, but check whether the child slot is `None` **before** moving into it, so I still hold the parent when it's time to attach. That's O(h) time and O(1) space — no stack, because insertion never revisits an ancestor. The empty tree is the only case where the root changes. And I'd note this doesn't rebalance: the problem accepts any valid BST, so inserting sorted values would degrade it to a chain — real self-balancing trees rotate after insertion to prevent that."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Does this keep the tree **balanced**?" | **No.** It's a leaf insertion. Sorted input degrades it to a chain — O(n²) to build, height `n`. AVL/red-black trees rotate to prevent this. |
| "How would you rebalance?" | Track heights (AVL) or colours (red-black) and apply rotations on the way back up — which requires the recursive form or parent pointers. |
| "What if `val` **already exists**?" | Undefined here. Common policies: ignore it, keep a count on the node, or consistently send duplicates right. Clarify before coding. |
| "Recursive or iterative?" | Iterative — O(1) space and no recursion limit. The recursion is clean but costs O(h) frames, and 10⁴ nodes can exceed Python's limit. |
| "How does the recursive version attach the node?" | "Recurse and reassign": each call returns its subtree, and the parent rebinds it. The `None` case returns a new node, and that rebinding attaches it. |
| "**Delete** instead?" | [Problem 450](450-delete-node-in-a-bst.md) — the same descent, then three cases based on the node's children. Considerably harder. |
| "Why check the child before descending?" | Once you move into a `None` you've lost the parent, and you need the parent to attach. |

**Traps:**

- **Descending into `None` before checking.** You lose the parent reference and can't attach.
- **Forgetting the empty-tree guard.** `AttributeError` on `root.val`.
- **Returning `node` instead of `root`.** `node` ends at the insertion parent, not the tree's root.
- **Using `else` when duplicates are possible.** Safe here by constraint, but silently misplaces duplicates otherwise.
- **Assuming the tree stays balanced.** It doesn't — say so before being asked.
- **Recursing on a degenerate 10⁴-node tree.** `RecursionError`.

**This same move shows up in:** [Search in a Binary Search Tree](700-search-in-a-binary-search-tree.md) (the same descent, without the attach step) · [Delete Node in a BST](450-delete-node-in-a-bst.md) (the same descent plus restructuring, using the recurse-and-reassign idiom) · [Convert Sorted Array to BST](108-convert-sorted-array-to-binary-search-tree.md) (why sequential insertion of sorted data is the wrong approach) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (verifying the property maintained here).

</details>

---
