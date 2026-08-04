# 230. Kth Smallest Element in a BST

**Medium** · [LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given the root of a **binary search tree** and an integer `k`, return the **k-th smallest value** (1-indexed) of all the node values.

```
        3            k = 1  →  1
      /   \          k = 3  →  3
     1     4
      \
       2

root = [5,3,6,2,4,null,null,1], k = 3  →  3
```

**Constraints:** `1 <= k <= n <= 10⁴` · `0 <= Node.val <= 10⁴` · **follow-up: what if the BST is modified often and you must find the k-th smallest frequently?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary search tree**" | ⚠️ The ordering is the whole point — a BST already *contains* a sorted sequence |
| "**k-th smallest**, 1-indexed" | `k = 1` is the minimum. Off-by-one risk |
| "return the value" | Not the node, not a rank |
| `k <= n` | Always valid; no "doesn't exist" case |
| the **follow-up** | Hints that repeated queries on a changing tree need a different design |

**The observation that makes this easy.** An **inorder** traversal of a BST — visit *left subtree, then node, then right subtree* — produces the values in **strictly ascending order**.

Why: at any node, everything in the left subtree is smaller and everything in the right is larger. Visiting left-first means you emit all the smaller values, then the node, then all the larger ones. Recursively, that's sorted order.

```
        3
      /   \        inorder:  1, 2, 3, 4
     1     4                 ↑        ↑
      \                    k=1      k=4
       2
```

So "the k-th smallest" becomes "**the k-th node visited in an inorder traversal**".

That's also the same fact underpinning [Validate Binary Search Tree](98-validate-binary-search-tree.md), where a tree is a BST *iff* its inorder is ascending. **Worth committing to memory: inorder + BST = sorted.**

**The efficiency point.** You don't need the whole sorted sequence — only its k-th element. So you should be able to **stop after k nodes** rather than traversing everything.

🤔 **Before you open the next section:** a recursive inorder traversal naturally visits all n nodes. How would you make it stop early — and is that awkward with recursion?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect all values, sort | Traverse, then `sort()` | O(n log n) | O(n) | ❌ Discards the BST ordering entirely |
| Full inorder into a list, index `k-1` | Traverse everything, then pick | O(n) | **O(n)** | ⚠️ Correct, but stores n values to use one |
| Recursive inorder with a counter | Count and stop | O(h + k) | O(h) | ✅ Needs a flag or exception to stop early |
| **Iterative inorder with a stack** | Explicit stack; return at the k-th pop | **O(h + k)** | **O(h)** | ✅ |

**The decision: iterative inorder traversal using an explicit stack, returning at the k-th node.**

**Why iterative here specifically.** Recursion is usually the natural fit for trees, but stopping early mid-recursion is awkward — you need a sentinel return value, a mutable flag checked at every level, or an exception. With an explicit stack the traversal is a plain loop, so `return` just… returns. **When a traversal needs to stop early, iterative is often cleaner.**

**The inorder-with-a-stack pattern**, which is worth learning as a unit:

```python
while stack or current:
    while current:              # 1. run as far LEFT as possible,
        stack.append(current)   #    stacking nodes on the way
        current = current.left
    current = stack.pop()       # 2. VISIT the leftmost unvisited node
    ...
    current = current.right     # 3. move RIGHT, then repeat
```

The inner `while` descends to the smallest unvisited node, pushing ancestors so they can be visited later. Popping yields nodes in ascending order. Then you step right and repeat — the stack remembering exactly where to resume.

**Why `while stack or current`.** Two conditions, both needed: `current` non-`None` means there's a subtree still to descend into; a non-empty `stack` means there are ancestors still awaiting their visit. The traversal is finished only when **both** are exhausted.

**Why not sort?** The BST *already* encodes the ordering. Sorting an n-element list to extract one value is paying O(n log n) for information the structure hands you for free — the same mistake as sorting in [Valid Anagram](242-valid-anagram.md) when counts suffice.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
current = root
count = 0
```

- `stack` — ancestors whose *own* visit is still pending while we explore their left subtrees.
- `current` — the node we're descending from.
- `count` — how many nodes have been visited so far, so we can stop at k.
→ [list-basics](../syntax/list-basics.md) · [stack](../data-structures/stack.md)

```python
while stack or current:
```

Keep going while there's either a subtree left to descend into (`current`) or an ancestor left to visit (`stack`). Both must be empty for the traversal to be complete.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    while current:
        stack.append(current)
        current = current.left
```

**Phase 1 — go as far left as possible.** Every node passed on the way down is pushed, because in inorder it must be visited *after* everything in its left subtree.

When this loop ends, the top of the stack is the **smallest unvisited node**.
→ [list-methods](../syntax/list-methods.md)

```python
    current = stack.pop()
    count += 1
```

**Phase 2 — visit.** Popping yields the leftmost unvisited node, so nodes come off in **ascending order**.

Increment the counter: this is the `count`-th smallest value in the tree.

```python
    if count == k:
        return current.val
```

**The early exit** — the reason for the iterative form. The moment we've visited k nodes, that node's value is the answer, and everything larger is left unexplored.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    current = current.right
```

**Phase 3 — move right.** This node is done, and everything in its left subtree was visited before it. What remains is its right subtree, which holds the next-larger values.

Setting `current` here means the outer loop's phase 1 will descend into that subtree's leftmost node next. If there's no right child, `current` becomes `None` and phase 1 is skipped — so the next pop takes the ancestor, which is correct.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:

        stack = []
        current = root
        count = 0

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            count += 1
            if count == k:
                return current.val

            current = current.right
```

</details>

**Trace it** — `k = 3` on:

```
        3
      /   \
     1     4
      \
       2
```

| Step | Action | `stack` | `current` | `count` |
|---|---|---|---|---|
| 1 | descend left from 3 | `[3, 1]` | None | 0 |
| 2 | pop **1** → visit | `[3]` | — | **1** |
| 3 | go right → 2 | `[3]` | 2 | 1 |
| 4 | descend left from 2 | `[3, 2]` | None | 1 |
| 5 | pop **2** → visit | `[3]` | — | **2** |
| 6 | go right → None | `[3]` | None | 2 |
| 7 | pop **3** → visit | `[]` | — | **3** ✅ |

`count == k` → **`return 3`** ✅

The visit order was `1, 2, 3` — ascending, as promised. And node **4 was never touched**: the early exit skipped the entire right subtree.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(h + k)</summary>

**O(h + k)**, where h is the height and k the target rank.

Two components:
- **O(h)** — the initial descent from the root to the leftmost (smallest) node.
- **O(k)** — visiting k nodes, each with O(1) amortized stack work.

**Why the traversal is amortized O(1) per node:** every node is pushed exactly once and popped exactly once across the whole run, so the inner `while` loops sum to at most n pushes total — the same amortized accounting as the monotonic stacks in [Daily Temperatures](739-daily-temperatures.md).

| Scenario | Cost |
|---|---|
| `k = 1`, balanced tree | O(log n) — descend and stop |
| `k = n` | O(n) — full traversal |
| Balanced, typical k | O(log n + k) |

**Versus the alternatives:** collecting all values is O(n) regardless of k; sorting is O(n log n). The early exit is what makes small k genuinely cheap — for `k = 1` on a balanced tree you touch ~14 nodes out of 10⁴.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the stack — **O(log n)** balanced, **O(n)** skewed.

The stack holds at most one root-to-node path: the chain of ancestors whose visits are still pending. It never holds the whole tree.

**Versus collecting all values into a list: O(n).** For `k = 1` on a 10⁴-node tree, that's storing 10,000 values to return one — the early-exit version stores ~14.

**The recursive version has the same O(h)** (call stack instead of explicit stack), but stopping early is clumsy. Compare:

```python
# recursive — needs shared state and a check at every level
def inorder(node):
    if not node or self.result is not None: return
    inorder(node.left)
    self.count += 1
    if self.count == k: self.result = node.val; return
    inorder(node.right)
```

Functional, but the `self.result is not None` guard has to be threaded through every call. **The iterative version's `return` is simply a return** — which is the practical argument for it here.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "An inorder traversal of a BST — left, node, right — visits values in ascending order, because everything left of a node is smaller and everything right is larger. So the k-th smallest is just the k-th node visited inorder. I do it iteratively with an explicit stack: descend as far left as possible pushing nodes, pop to visit the smallest unvisited one, then move right and repeat. I count visits and return at the k-th, which means I never touch anything larger. Iterative rather than recursive specifically because stopping early mid-recursion needs a flag or an exception, whereas here it's just a `return`. O(h + k) time and O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the tree is modified often and you query frequently?" | **The stated follow-up.** Augment each node with `size` = the count of nodes in its subtree. Then finding the k-th is O(h): compare k to `left.size + 1` and descend accordingly. Inserts and deletes update sizes along one path, also O(h). |
| "k-th **largest**?" | Reverse inorder — right, node, left. Same code with `left`/`right` swapped. |
| "Why iterative instead of recursive?" | Early termination. Recursion needs a shared flag checked at every level; iteration just returns. |
| "Why is inorder sorted for a BST?" | The BST invariant: everything left < node < everything right. Visiting left-first emits smaller values first, recursively. |
| "What if it weren't a BST?" | Then order means nothing — use a heap or Quickselect. See [K Closest Points to Origin](973-k-closest-points-to-origin.md), [quickselect](../algorithms/quickselect.md). |
| "Return the k-th smallest **node**?" | Return `current` instead of `current.val`. |
| "Recursive version?" | Same traversal with the call stack, plus shared state for the count and result. |

**Traps:**

- **Sorting all the values.** O(n log n) for information the BST already provides.
- **Building the full inorder list** and indexing `[k-1]`. Correct, but O(n) space and no early exit.
- **Off-by-one on k.** It's 1-indexed — `k = 1` is the minimum. Return when `count == k`, not `count == k - 1`.
- **`while stack` alone** as the outer condition. It's false at the very start (`stack` is empty, `current` is the root), so the loop never runs. You need `stack or current`.
- **Forgetting `current = current.right`** after visiting — the traversal stalls and re-pops the same ancestors.
- **Visiting before descending left** — that's *preorder*, which isn't sorted.

**This same move shows up in:** [Validate Binary Search Tree](98-validate-binary-search-tree.md) (the same inorder-is-sorted property, and the same stack skeleton) · [Lowest Common Ancestor of a BST](235-lowest-common-ancestor-of-a-binary-search-tree.md) (BST ordering for navigation) · [tree-traversal-orders](../algorithms/tree-traversal-orders.md) (preorder / inorder / postorder reference) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (the k-th question without any ordering to exploit).

</details>
