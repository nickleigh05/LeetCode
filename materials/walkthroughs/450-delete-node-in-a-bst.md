# 450. Delete Node in a BST

**Medium** · [LeetCode](https://leetcode.com/problems/delete-node-in-a-bst/) · [Solution file (no hints)](../../problems/0001-0499/450.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a **BST** and a `key`, delete the node with that value and return the (possibly new) root. Deletion is two stages: find the node, then remove it while preserving the BST property.

```
root = [5,3,6,2,4,null,7], key = 3  →  [5,4,6,2,null,null,7]   (one valid answer)
root = [5,3,6,2,4,null,7], key = 0  →  unchanged (key not present)
root = [], key = 0  →  []
```

**Constraints:** `0 <= number of nodes <= 10⁴` · `-10⁵ <= Node.val <= 10⁵` · values are **unique** · `root` is a valid BST

**Follow-up:** could you solve it in **O(height)** time?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**BST**" | The search half is the familiar O(h) descent from [Search in a BST](700-search-in-a-binary-search-tree.md) |
| "**delete** the node" | ⚠️ The hard half — removing a node can orphan **two** subtrees |
| "return the **root**" | The root itself may be deleted, so the return can differ from the input |
| key may **not exist** | Then return the tree unchanged — no error |
| `0 <= nodes` | Empty tree is valid input |
| follow-up: **O(height)** | The natural solution already achieves this |

**Why deletion is the hardest of the three BST operations.** [Search](700-search-in-a-binary-search-tree.md) just walks down. [Insert](701-insert-into-a-binary-search-tree.md) walks down and attaches at an empty slot. Deletion has to **repair the tree** after removing a node — and the repair depends on how many children the doomed node has.

**The three cases:**

| Children | What to do |
|---|---|
| **0** (leaf) | Just remove it — return `None` |
| **1** | Splice: return the single child, which takes the node's place |
| **2** | ⚠️ **The hard case** — you can't return two subtrees |

**Case 3, the two-child problem.** You can't simply promote a child; the other subtree would be orphaned. The standard fix:

> Replace the node's **value** with its **inorder successor** — the smallest value in its right subtree — then delete that successor from the right subtree.

Why the inorder successor works: it's the next value in sorted order, so it's **greater than everything in the left subtree** and **less than everything else in the right subtree**. Dropping it into the node's position preserves the BST property exactly.

```
delete 3 from:        5                    5
                     / \                  / \
                    3   6      →         4   6      ← 4 is 3's inorder successor
                   / \   \              /     \        (min of 3's right subtree)
                  2   4   7            2       7
```

And crucially, **the successor always has at most one child** — it's the leftmost node of the right subtree, so it has no left child by definition. So deleting it recursively hits case 1 or 2, never case 3 again. The recursion terminates after one extra step.

The **inorder predecessor** (largest in the left subtree) works equally well by symmetry — both give valid BSTs.

🤔 **Before you open the next section:** if you must remove a node with two children, which remaining value could take its place without violating the ordering?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect values, rebuild | Inorder-traverse, drop the key, rebuild | O(n) | **O(n)** | ❌ Discards the structure entirely |
| **Recursive "recurse and reassign"** | Descend, handle three cases, return the subtree | **O(h)** | O(h) stack | ✅ |
| Iterative with parent tracking | Same logic, manual parent pointers | O(h) | **O(1)** | ✅ Correct, considerably fiddlier |

**The decision: recursion using the "recurse and reassign" idiom** — the same shape as [Insert into a BST](701-insert-into-a-binary-search-tree.md).

Each call **returns the subtree it is responsible for**, and the parent rebinds it:

```python
root.left = self.deleteNode(root.left, key)   # most of the time a no-op
```

Usually that reassignment changes nothing. But when the deleted node *was* `root.left`, the call returns the replacement — and the reassignment is what actually splices it in. That single idiom eliminates all parent-pointer bookkeeping.

**Why recursion is preferable here** — the opposite conclusion from [search](700-search-in-a-binary-search-tree.md) and [insert](701-insert-into-a-binary-search-tree.md), where iteration won:

Search and insert only move **downward**, so no stack is needed. Deletion must **modify a parent's child pointer** after the recursive call returns, which means returning up the tree. Doing that iteratively requires explicitly tracking the parent and which side the child was on — genuinely messier for no asymptotic gain.

**Why the two-child case recurses rather than rewires.** Copying the successor's value and then calling `deleteNode(root.right, successor_value)` looks like it might loop forever. It doesn't:

- The successor is the **leftmost** node of the right subtree
- Leftmost means **no left child**
- So its deletion falls into case 1 (leaf) or case 2 (one right child) — never case 3

Exactly one extra descent, bounded by `h`.

**Why finding the minimum is a simple loop.** The smallest value in a subtree is reached by going left until you can't:

```python
while node.left:
    node = node.left
```

O(h) worst case, and no recursion needed.

**Why not rebuild?** Collecting all values and reconstructing is O(n) time and space for an operation that should be O(h) — and it throws away the tree you were given.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return None
```

**Base case: empty subtree.** Also handles "key not found" — the descent runs off the bottom and returns `None`, which the parent harmlessly rebinds to the same `None`.
→ [none-type](../syntax/none-type.md)

```python
if key < root.val:
    root.left = self.deleteNode(root.left, key)
    return root

if key > root.val:
    root.right = self.deleteNode(root.right, key)
    return root
```

**The BST descent, with reassignment.**

The `root.left = ...` pattern is the crux: normally it rebinds the same subtree (a no-op), but if the deletion happened one level down, it splices in the returned replacement.

Returning `root` unchanged afterwards is correct — this node isn't the one being deleted.
→ [comparison-operators](../syntax/comparison-operators.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
# key == root.val — this is the node to delete
if not root.left:
    return root.right

if not root.right:
    return root.left
```

**Cases 1 and 2, handled together.**

- No left child → return the right child (which may itself be `None`, covering the leaf case)
- No right child → return the left child

Whatever is returned becomes the parent's new child via the reassignment above. **A leaf is covered automatically**: both children are `None`, the first check fires, and `None` is returned — the node vanishes.

That's why there's no explicit third branch for leaves.

```python
successor = root.right
while successor.left:
    successor = successor.left
```

**Case 3: find the inorder successor** — the leftmost node of the right subtree, i.e. the smallest value greater than `root.val`.
→ [while-loop](../syntax/while-loop.md)

```python
root.val = successor.val
root.right = self.deleteNode(root.right, successor.val)

return root
```

**Copy the value up, then delete the successor from the right subtree.**

Note only the **value** moves — the node object stays in place, so nothing else needs rewiring.

The recursive delete terminates quickly because the successor has no left child, so it falls into case 1 or 2.
→ [recursion-basics](../syntax/recursion-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        if not root:
            return None

        if key < root.val:
            root.left = self.deleteNode(root.left, key)
            return root

        if key > root.val:
            root.right = self.deleteNode(root.right, key)
            return root

        # found the node to delete
        if not root.left:
            return root.right

        if not root.right:
            return root.left

        # two children: replace with the inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left

        root.val = successor.val
        root.right = self.deleteNode(root.right, successor.val)

        return root
```

</details>

**Trace the two-child case** — delete `3` from:

```
      5
     / \
    3   6
   / \   \
  2   4   7
```

| Step | Call | Action |
|---|---|---|
| 1 | `delete(5, 3)` | `3 < 5` → `root.left = delete(node3, 3)` |
| 2 | `delete(3, 3)` | match; **two children** → find successor |
| 3 | successor search | `root.right` = 4; `4.left` is `None` → successor = **4** |
| 4 | copy value | node 3 becomes node **4** |
| 5 | `delete(subtree at 4, 4)` | match; no left child → return `4.right` = `None` |
| 6 | reassign | the node's `.right` becomes `None` |

Result:

```
      5
     / \
    4   6
   /     \
  2       7
```

Inorder check: `2, 4, 5, 6, 7` — sorted ✅, and 3 is gone ✅

Step 5 shows why the recursion terminates: node 4 had no left child, so it hit case 1 immediately.

**The one-child case** — delete `6` from the original tree: node 6 has only a right child (7), so `not root.left` fires and returns 7. Node 5's `.right` is rebound to 7:

```
      5
     / \
    3   7
   / \
  2   4
```

Inorder: `2, 3, 4, 5, 7` ✅

**The key-not-found case** — delete `0`: the descent goes left from 5, left from 3, left from 2 → `None` → returns `None`, which node 2's `.left` is harmlessly rebound to. Tree unchanged ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h)</summary>

**O(h)**, satisfying the follow-up.

Breaking it down:

- **Descent to the node:** O(h)
- **Finding the successor:** O(h) worst case (walking left from the right child)
- **Deleting the successor:** O(h), but it terminates within one or two steps since the successor has no left child

Each phase is bounded by the height, and they're sequential, so the total is **O(h)** — not O(h²).

| Tree shape | `h` | Cost |
|---|---|---|
| Balanced | `log n` | **O(log n)** ≈ 14 at n = 10⁴ |
| Degenerate | `n` | **O(n)** = 10⁴ |

**As with search and insert**, the bound is O(h), and O(log n) only when the tree is balanced. This operation doesn't rebalance — repeated deletions can degrade the shape, which is exactly what AVL and red-black trees add rotations to prevent.

**Compare to rebuilding:** O(n) time and space. The O(h) approach is the point of using a BST at all.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack.

At `n = 10⁴`, a degenerate BST is 10⁴ frames deep — past Python's ~1000-frame default, so a `RecursionError` is possible on adversarial input. The iterative version avoids this but needs explicit parent tracking:

```python
# sketch: track parent and which side, then splice manually
parent, node = None, root
while node and node.val != key:
    parent = node
    node = node.left if key < node.val else node.right
# ... then handle the three cases, updating parent.left or parent.right
```

Correct and O(1) space, but noticeably more code — and every case must remember whether the node was a left or right child.

**Why recursion is the better default here**, unlike [search](700-search-in-a-binary-search-tree.md) and [insert](701-insert-into-a-binary-search-tree.md):

> Deletion must **update a parent's child pointer after the child is resolved**. That's inherently a "return up the tree" operation, which recursion expresses naturally via `root.left = delete(root.left, key)`.

Search and insert only ever move down, so they can drop the stack. Deletion cannot, without reintroducing the bookkeeping by hand.

**Only values are copied**, never nodes — the two-child case moves a single integer, so no allocation occurs at all.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Deletion is two stages: find the node with the standard BST descent, then repair the tree. There are three cases. A leaf just disappears. A node with one child is replaced by that child. The hard case is two children — I can't return two subtrees, so I replace the node's **value** with its inorder successor, the smallest value in the right subtree, then recursively delete that successor. The successor works because it's the next value in sorted order, so it's larger than everything on the left and smaller than everything remaining on the right. And the recursion terminates immediately, because the leftmost node has no left child, so deleting it hits the zero- or one-child case. I use the 'recurse and reassign' idiom — `root.left = deleteNode(root.left, key)` — which splices in replacements without needing parent pointers. O(h) time and O(h) stack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why the inorder successor?" | **The key question.** It's the next value in sorted order — greater than the whole left subtree, less than the rest of the right — so it preserves the BST property exactly. |
| "Could you use the **predecessor** instead?" | Yes — the largest value in the left subtree. Symmetric and equally valid. |
| "Why doesn't the recursion loop forever?" | The successor is leftmost, so it has no left child; deleting it hits the zero- or one-child case. |
| "Do it iteratively in O(1) space." | Track the parent and which side the node hangs off, then splice manually. Correct, but much fiddlier. |
| "Does it stay **balanced**?" | No. Repeated deletions can degrade the shape. AVL/red-black trees rotate after deletion to maintain O(log n) height. |
| "What if the key isn't present?" | The descent reaches `None` and returns it; the parent's reassignment is a harmless no-op. |
| "What if the **root** is deleted?" | Handled — the top-level call returns the replacement, which the caller uses as the new root. |

**Traps:**

- **Forgetting the reassignment.** Calling `deleteNode(root.left, key)` without `root.left = ...` discards the result and changes nothing.
- **Trying to promote one child in the two-child case.** The other subtree is orphaned.
- **Using the wrong successor.** It's the **leftmost** node of the right subtree, not just `root.right`.
- **Copying the node instead of its value.** Copying the value is enough and avoids rewiring; swapping node objects invites pointer bugs.
- **Deleting the successor from the whole tree** rather than from `root.right`. With unique values it happens to work, but it re-searches from the top — wasteful and conceptually wrong.
- **Recursing on a degenerate 10⁴-node tree.** `RecursionError`.

**This same move shows up in:** [Insert into a Binary Search Tree](701-insert-into-a-binary-search-tree.md) (the same recurse-and-reassign idiom, without the repair) · [Search in a Binary Search Tree](700-search-in-a-binary-search-tree.md) (the descent this builds on) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (inorder order, which is what the successor argument relies on) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (checking the invariant this must preserve).

</details>

---
