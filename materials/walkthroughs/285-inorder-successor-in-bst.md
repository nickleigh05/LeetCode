# 285. Inorder Successor in BST

**Medium** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/inorder-successor-in-bst/) · [Solution file (no hints)](../../problems/0001-0499/285.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a **binary search tree** and a node `p` in it, return the **in-order successor** of `p`: the node with the **smallest value strictly greater than `p.val`**. If `p` has no successor (it's the largest), return `None`.

```
      2
     / \
    1   3

p = 1  →  2
p = 3  →  None
```

```
          5
         / \
        3   6
       / \
      2   4
     /
    1

p = 6  →  None
p = 4  →  5       (no right subtree, so the successor is an ancestor)
p = 3  →  4       (has a right subtree, so the successor is inside it)
```

**Constraints:** `1 <= nodes <= 10⁴` · `-10⁵ <= Node.val <= 10⁵` · all values are **unique** · `p` is in the tree

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| **BST** | Left subtree < node < right subtree. The ordering lets you **steer**, so you don't search the whole tree |
| "in-order successor" | In-order traversal of a BST visits values in sorted order, so the successor is the **next value up** |
| smallest value **strictly greater** than `p.val` | Phrase it as a search: the smallest node above a threshold |
| no parent pointers | You can't walk up from `p`. Start at the root |
| values unique | No ties to break |

**The slow but obvious answer.** Do an in-order traversal into a list, find `p`, and return the next one. That's O(n), and it ignores the BST property completely.

**Reframe it as a search.** "Smallest value greater than `p.val`" is like a **ceiling** search in a sorted structure. Walk down from the root, comparing each node with `p.val`:

- **`node.val > p.val`**: this node **could** be the successor. Remember it. But there might be a smaller qualifying value, and smaller values are to the **left**, so go left.
- **`node.val <= p.val`**: this node is too small (or is `p` itself). Everything to its left is smaller still, so go **right**.

When you fall off the tree, the last node you remembered is the answer. Each time you remember a node you then move left, towards smaller values, so each remembered candidate is smaller than the one before. The last one is the smallest that qualifies.

This one walk covers both textbook cases: "if `p` has a right subtree, it's the leftmost node there," and "otherwise, it's the nearest ancestor that `p` is in the left subtree of."

🤔 **Before you open the next section:** walking down from the root of the second tree towards `p = 4`, which nodes have values greater than 4, and which of them is the last one you'd remember?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| In-order to a list | Traverse everything, find `p`, return the next | O(n) | O(n) | ❌ Ignores the BST |
| In-order with early stop | Traverse, return the node after `p` is seen | O(n) worst | O(h) | ⚠️ Still doesn't steer |
| Two cases | Right subtree's leftmost, else track ancestors from the root | O(h) | O(1) | ✅ Correct, two code paths |
| **One ceiling walk from the root** | Remember every node > `p.val`, go left there, otherwise right | **O(h)** | **O(1)** | ✅ One loop covers both cases |

**The decision: one iterative walk down the [BST](../data-structures/binary-search-tree.md)**, the same steering as [Search in a BST](700-search-in-a-binary-search-tree.md) but keeping track of a candidate.

It's like [binary search](../algorithms/binary-search.md) for the first element greater than a target, with the tree's shape giving the halving. Each comparison removes a whole subtree.

**Why the two-case version is the same thing.** If `p` has a right subtree, the walk reaches `p`, goes right (because `p.val <= p.val`), then keeps going left, remembering each node, down to the leftmost one. If it doesn't, the last remembered node is the deepest ancestor where the walk turned left, which is the nearest ancestor that has `p` in its left subtree. The single loop handles both without special cases.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
successor = None
node = root
```

`successor` is the best candidate so far. It stays `None` if no node is greater than `p`, which is the right answer when `p` is the maximum. `node` is the walking pointer.
→ [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while node is not None:
    if p.val < node.val:
        successor = node
        node = node.left
```

**This node is bigger than `p`, so it's a candidate.** Save it, then go left to look for a smaller node that's still bigger than `p`. Anything we find later down the left side will be smaller than this candidate, so overwriting `successor` is always an improvement.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        node = node.right
```

**This node is ≤ `p`, so it's not a candidate.** Its whole left subtree is smaller still, so only the right side can hold the answer. This branch also covers reaching `p` itself: its successor, if it's below `p`, is in `p`'s right subtree.
→ [elif-else](../syntax/elif-else.md)

```python
return successor
```

When the walk falls off the tree, the last candidate saved is the smallest value greater than `p.val`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        successor = None
        node = root

        while node is not None:
            if p.val < node.val:
                successor = node
                node = node.left
            else:
                node = node.right

        return successor
```

</details>

**Trace it.** The second tree, `p = 4`. Its successor should be an ancestor:

| `node` | `4 < node.val`? | Action | `successor` |
|---|---|---|---|
| 5 | yes | save, go left | **5** |
| 3 | no | go right | 5 |
| 4 | no (equal) | go right | 5 |
| `None` | — | stop | **5** ✅ |

**`p = 3`**, whose successor is in its right subtree:

| `node` | `3 < node.val`? | Action | `successor` |
|---|---|---|---|
| 5 | yes | save, go left | 5 |
| 3 | no | go right | 5 |
| 4 | yes | save, go left | **4** |
| `None` | — | stop | **4** ✅ |

**`p = 6`** (the maximum): 5 → right, 6 → right, `None`. Nothing was ever saved, so it returns **`None`** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h)</summary>

**O(h)**, where h is the tree's height. Each step moves one level down, and the walk ends when it falls off a leaf.

- Balanced BST: O(log n).
- Skewed BST (inserted in sorted order): O(n).

Compare with the in-order traversal approach, which is O(n) even on a perfectly balanced tree.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two pointers, with no recursion and no list. A recursive version would use O(h) stack, and the in-order-list approach O(n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "In-order order in a BST is sorted order, so the successor is the smallest value strictly greater than p. I'll find it with a ceiling search from the root. When a node's value is greater than p's, it's a candidate, so I save it and go left to look for something smaller that still qualifies. Otherwise I go right. When I fall off the tree, the last saved candidate is the answer, or None if p was the maximum. That one loop covers both the right-subtree case and the ancestor case. O(h) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "In-order **predecessor**?" | Mirror it: when `node.val < p.val`, save it and go right. Otherwise go left. |
| "What if nodes have parent pointers?" | LeetCode 510. If `p` has a right subtree, take its leftmost node. Otherwise climb parents until you come up from a left child. No root needed. |
| "Plain binary tree, not a BST?" | You lose the steering. Do an in-order traversal and return the node visited right after `p`, which is O(n). |
| "Is a tree a valid BST?" | [Validate BST](98-validate-binary-search-tree.md). The in-order sequence must be strictly increasing. |
| "k-th smallest?" | [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md). In-order traversal, stopping at the k-th node. |

**Traps:**

- **`<=` in the candidate check.** Saving `p` itself as its own successor. The comparison must be strict.
- **Stopping when you reach `p`.** The successor may be deeper, in `p`'s right subtree.
- **Taking `p.right` and returning it.** The successor is the **leftmost** node in that subtree, not its root.
- **Traversing the whole tree.** Correct, but it ignores the BST and is O(n).
- **Comparing nodes instead of values.** `p < node` raises a `TypeError`. Compare `.val`.

**This same move shows up in:** [Search in a Binary Search Tree](700-search-in-a-binary-search-tree.md) (the same left/right steering) · [Lowest Common Ancestor of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) (walking down from the root by comparing values) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (in-order order means sorted order) · [Search Insert Position](35-search-insert-position.md) (a ceiling-style binary search on an array).

</details>

---
