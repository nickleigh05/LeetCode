# 226. Invert Binary Tree

**Easy** · [LeetCode](https://leetcode.com/problems/invert-binary-tree/) · [Solution file (no hints)](../../problems/0001-0499/226.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, **invert** it (mirror it left-to-right) and return the root.

```
        4                        4
      /   \                    /   \
     2     7       →          7     2
    / \   / \                / \   / \
   1   3 6   9              9   6 3   1
```

```
root = [2,1,3]  →  [2,3,1]
root = []       →  []
```

**Constraints:** `0 <= nodes <= 100` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the gateway problem for the whole unit. **The three-line recursive shape you learn here is the skeleton of nearly every tree problem that follows**, so it's worth understanding structurally rather than memorizing.

| The statement says | Which really means |
|---|---|
| "**invert** / mirror" | Every node swaps its left and right children — **at every level**, not just the root |
| "**binary** tree" | Each node has at most two children, and each child is itself the root of a subtree |
| tree can be **empty** | `None` input → `None` output, no crash |
| ≤ 100 nodes | Tiny. This is about recognizing the recursive structure |

**The key realization about trees.** A tree is **self-similar**: `root.left` isn't just a node, it's the root of a complete, smaller binary tree. So any question you can ask about a tree, you can ask about its subtrees — and the answers usually combine simply.

That gives the universal three-step shape:

```
1. BASE CASE       what's the answer for an empty tree?
2. RECURSE         get the answer for the left and right subtrees
3. COMBINE         assemble those into the answer for this tree
```

For inversion:
1. **Base:** inverting nothing gives nothing.
2. **Recurse:** invert the left subtree, invert the right subtree.
3. **Combine:** swap them.

**Assume the recursion works.** Don't trace it mentally past one level — that way lies confusion. Trust that `invertTree(root.left)` returns a correctly inverted left subtree, and just ask *"given that, what do I do here?"* That leap of faith is the actual skill this unit teaches.

🤔 **Before you open the next section:** if both subtrees come back already inverted, what single operation at the current node finishes the job?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Recursive DFS** | Invert both subtrees, then swap | **O(n)** | O(h) stack | ✅ |
| Iterative DFS (stack) | Explicit stack of nodes to swap | O(n) | O(h) | ✅ Same thing, manual stack |
| Iterative BFS (queue) | Level by level, swapping each node's children | O(n) | O(w) | ✅ Also fine |

**The decision: recursive [DFS](../algorithms/dfs.md).**

All three are O(n) and correct — you must visit every node to swap its children, and the *order* of visits is irrelevant since each swap is independent. So choose on clarity, and recursion mirrors the problem's structure exactly.

**Why recursion fits trees so naturally.** The recursive call stack *is* a stack of pending subtrees. Writing the iterative version means building that stack by hand:

```python
stack = [root]
while stack:
    node = stack.pop()
    if node:
        node.left, node.right = node.right, node.left
        stack.append(node.left)
        stack.append(node.right)
```

Identical algorithm — the recursion just manages the bookkeeping for you.

**When you'd prefer the iterative form:** very deep trees, where O(h) recursion could exceed Python's stack limit. At n ≤ 100 that's irrelevant here, but on a 10⁵-node skewed tree it matters. Worth naming.

**The base case is doing real work.** `if root is None: return None` handles both the empty-tree input *and* every leaf's missing children — one line covering what would otherwise be several checks. **Getting the base case right is usually most of a tree solution.**

**Recognize the shape.** Base → recurse → combine is the same skeleton as [Maximum Depth](104-maximum-depth-of-binary-tree.md), [Same Tree](100-same-tree.md), [Balanced Binary Tree](110-balanced-binary-tree.md) and the rest of this unit. Only the combine step changes.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if root is None:
    return None
```

**The base case.** An empty tree inverts to an empty tree.

This single line does double duty: it handles the empty-tree input, and it terminates the recursion at every leaf (whose `left` and `right` are both `None`). Without it, the recursion would try to read `.left` on `None` and crash.
→ [identity-operators](../syntax/identity-operators.md) · [none-type](../syntax/none-type.md) · [if-return](../syntax/if-return.md)

```python
left_subtree = self.invertTree(root.left)
right_subtree = self.invertTree(root.right)
```

**Recurse.** Each call returns that subtree, fully inverted.

This is the leap of faith — don't unwind these calls in your head. Assume they work, because the base case guarantees termination and each call operates on a strictly smaller tree.

Note we capture the results in variables *before* modifying anything, which makes the swap below unambiguous.
→ [recursion-basics](../syntax/recursion-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
root.left = right_subtree
root.right = left_subtree
```

**Combine — the swap**, and the only problem-specific line here. The inverted *right* subtree becomes the new left child, and vice versa.

Because the results were saved first, there's no risk of overwriting one before reading it. (Python's `root.left, root.right = root.right, root.left` would also be safe, since the right-hand side is evaluated first — but the explicit version makes the intent obvious.)
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
return root
```

Return the (now inverted) tree so the caller — which is the parent's recursive call — can attach it.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:

        if root is None:
            return None

        left_subtree = self.invertTree(root.left)
        right_subtree = self.invertTree(root.right)

        root.left = right_subtree
        root.right = left_subtree

        return root
```

</details>

**Trace it** — the recursion unwinds bottom-up on `[4,2,7,1,3,6,9]`:

```
        4                    invert(4)
      /   \                    ├─ invert(2)
     2     7                   │    ├─ invert(1) → leaf, children are None → [1]
    / \   / \                  │    ├─ invert(3) → [3]
   1   3 6   9                 │    └─ swap → 2 has left=3, right=1
                               ├─ invert(7)
                               │    ├─ invert(6) → [6]
                               │    ├─ invert(9) → [9]
                               │    └─ swap → 7 has left=9, right=6
                               └─ swap → 4 has left=7, right=2
```

Result:
```
        4
      /   \
     7     2
    / \   / \
   9   6 3   1
```
✅

Note the swaps happen **on the way back up** — the deepest nodes are swapped first, and each level's swap operates on subtrees that are already correct. That's why the leap of faith is safe.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n is the number of nodes.

Each node is visited **exactly once**, and does O(1) work: one `None` check, two assignments, one return. The two recursive calls partition the remaining nodes — no node is ever visited by both.

n × O(1) = **O(n)**.

**This is the standard bound for tree traversal**, and it holds for nearly every problem in this unit: if you visit every node once and do constant work at each, it's O(n). Watch for the exceptions — [Subtree of Another Tree](572-subtree-of-another-tree.md) does O(m) work per node, giving O(n·m).

**It can't be beaten:** every node's children must be swapped, so every node must be touched.

**No early exit** — the whole tree must be inverted.

**The `None` calls are counted too.** A tree with n nodes has n+1 `None` children, each triggering a base-case call. That's still O(n) — a constant factor, not a change of order.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)**, where **h is the height** of the tree — the recursion stack depth, since the deepest chain of pending calls follows a root-to-leaf path.

**This is the space answer for almost every problem in this unit**, so it's worth pinning down precisely:

| Tree shape | Height | Space |
|---|---|---|
| **Balanced** | log₂ n | **O(log n)** |
| **Skewed** (a linked list) | n | **O(n)** |

So the honest phrasing is: *"O(h) for the recursion stack — O(log n) if the tree is balanced, O(n) in the worst case."* Saying just "O(log n)" assumes balance the problem never promised.

**Nothing else is allocated.** The nodes are relinked in place, exactly as in Unit 06 — only the arrows change.

**The iterative version doesn't help asymptotically:** an explicit DFS stack also holds up to h nodes, and BFS holds up to the tree's maximum *width* — which for a balanced tree is n/2, actually **worse** than recursion. The reason to go iterative is avoiding Python's recursion limit, not saving memory.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A tree is self-similar — each child is the root of a smaller tree — so this is naturally recursive. Three steps: the base case is that an empty tree inverts to an empty tree; then I recursively invert the left and right subtrees; then I combine by swapping them at the current node. I don't trace the recursion mentally — I assume the subtree calls return correctly inverted subtrees and just handle the current node. Every node is visited once doing constant work, so O(n) time, and O(h) space for the recursion stack — O(log n) balanced, O(n) if the tree is skewed."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Write it iteratively." | A stack (or queue) of nodes: pop, swap its children, push both. Same O(n)/O(h). |
| "Why is space O(h) and not O(n)?" | Only one root-to-leaf path is on the stack at a time. It becomes O(n) only when the tree is a skewed chain. |
| "Does traversal order matter?" | No — each swap is independent, so preorder, postorder, and BFS all work. That's unusual; most tree problems *do* care. |
| "What if the tree were huge and deep?" | Recursion could exceed Python's limit. Use the iterative version. |
| "Check whether a tree is symmetric instead." | Compare left against right *mirrored* — recurse on `(a.left, b.right)` and `(a.right, b.left)`. LeetCode 101, and closely related. |
| "Invert an n-ary tree?" | Reverse each node's children list, then recurse on each. Same shape. |

**Traps:**

- **Forgetting the base case** — `AttributeError` on `None.left` at the first leaf.
- **Swapping before recursing** is actually fine here (order doesn't matter for this problem) — but *don't* assume that generalizes. Most tree problems need the children's results before combining.
- **Reassigning `root.left` before reading it**, without saving. `root.left = root.right` then loses the original left subtree. Save first, or use tuple assignment.
- **Returning `None`** at the end instead of `root` — the parent then attaches nothing.
- **Trying to swap values instead of nodes.** Works for this problem, but it's the wrong mental model — you're restructuring the tree, and subtrees don't move by swapping values.

**This same move shows up in:** [Maximum Depth](104-maximum-depth-of-binary-tree.md) (the same base-recurse-combine skeleton) · [Same Tree](100-same-tree.md) (recursing on two trees at once) · [Balanced Binary Tree](110-balanced-binary-tree.md) (combine step returns two facts) · [dfs](../algorithms/dfs.md) (the traversal's reference page).

</details>

---
