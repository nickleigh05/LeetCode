# 104. Maximum Depth of Binary Tree

**Easy** · [LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/) · [Solution file (no hints)](../../problems/0001-0499/104.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return its **maximum depth** — the number of nodes along the longest path from the root down to the farthest leaf.

```
        3           depth = 3
      /   \
     9     20
          /  \
        15    7

root = [3,9,20,null,null,15,7]  →  3
root = [1,null,2]               →  2
root = []                       →  0
```

**Constraints:** `0 <= nodes <= 10⁴` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**maximum** depth" | Only the **longer** of the two subtrees matters — a `max`, not a sum |
| "number of **nodes** along the path" | ⚠️ Counting nodes, not edges. A single-node tree has depth **1**, not 0 |
| "root to the **farthest leaf**" | A whole-tree property that decomposes cleanly into subtree properties |
| empty tree allowed | Depth 0 — which is also the base case |
| n up to 10⁴ | ⚠️ A skewed tree would be 10⁴ deep — beyond Python's default recursion limit of 1000 |

Apply the [three-step tree skeleton](226-invert-binary-tree.md):

1. **Base case:** an empty tree has depth **0**.
2. **Recurse:** get the depth of the left subtree and of the right subtree.
3. **Combine:** the answer is `1 + max(left, right)`.

The combine step is where the thinking is. Why `1 + max`?

- **`max`** because depth is the *longest* path — a shallow left subtree doesn't limit a deep right one.
- **`+ 1`** to count the current node itself, which sits on every path through this tree.

```
        3         ← +1 for this node
      /   \
     9     20     ← max(depth(9)=1, depth(20)=2) = 2
          /  \
        15    7

depth = 1 + 2 = 3 ✅
```

**The base returning 0 is what makes the node-counting come out right.** A leaf computes `1 + max(0, 0) = 1` — correct, since a single node is depth 1. Return 1 from the base case instead and every depth is inflated by one.

🤔 **Before you open the next section:** if you changed `max` to `min`, what would you be computing — and would the answer still be correct for a tree with a missing child?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Recursive DFS** | `1 + max(left, right)` | **O(n)** | O(h) stack | ✅ |
| Iterative DFS | Stack of `(node, depth)` pairs | O(n) | O(h) | ✅ Avoids the recursion limit |
| **BFS by levels** | Count how many levels you process | O(n) | O(w) | ✅ Often the most intuitive |

**The decision: recursive [DFS](../algorithms/dfs.md) with `1 + max(left, right)`.**

It's two lines, and it reads exactly like the definition of depth. That's the sign you've matched the algorithm to the problem's structure.

**BFS is a genuinely good alternative here**, and worth knowing because it's the natural fit for a *different* framing: if you process the tree level by level and count the levels, the count *is* the depth.

```python
from collections import deque
if not root: return 0
queue, depth = deque([root]), 0
while queue:
    depth += 1
    for _ in range(len(queue)):          # one full level
        node = queue.popleft()
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
return depth
```

That `for _ in range(len(queue))` idiom — snapshot the queue size to process exactly one level — is the foundation of [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) and [Right Side View](199-binary-tree-right-side-view.md). Learn it here.

**DFS vs BFS on space:** DFS is O(h), BFS is O(w) where w is the maximum width. For a **balanced** tree, h = log n but w = n/2 — so **DFS uses dramatically less memory**. For a **skewed** tree it's the reverse: h = n, w = 1. Neither dominates; it depends on the shape.

**⚠️ The recursion-limit caveat is real here.** With n up to 10⁴ a fully skewed tree gives depth 10⁴, exceeding Python's default limit of 1000 → `RecursionError`. LeetCode's actual test cases don't hit this, but it's a legitimate answer to "what would break?"

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if root is None:
    return 0
```

**The base case**, and the line that defines the counting convention. An empty tree has depth 0.

This value propagates: a leaf computes `1 + max(0, 0) = 1`. Return 1 here instead and every answer is off by one — a good example of how the base case *determines* the semantics, not just terminates the recursion.

It also handles the empty-tree input directly.
→ [identity-operators](../syntax/identity-operators.md) · [none-type](../syntax/none-type.md) · [if-return](../syntax/if-return.md)

```python
return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

**Recurse and combine, in one expression.** Three things happen:

- `self.maxDepth(root.left)` and `self.maxDepth(root.right)` — the recursion. Assume each returns its subtree's depth correctly.
- `max(...)` — take the **deeper** side, since depth is the longest path. A missing child returns 0 and simply loses the `max`, which is why lopsided trees need no special handling.
- `1 +` — count the current node, which lies on every path through this tree.

Written as one line it's compact; splitting it into `left = ...`, `right = ...`, `return 1 + max(left, right)` is equally good and often clearer when explaining aloud.
→ [recursion-basics](../syntax/recursion-basics.md) · [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:

        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

</details>

**Trace it** — `[3,9,20,null,null,15,7]`:

```
        3
      /   \
     9     20
          /  \
        15    7
```

Evaluated bottom-up:

| Node | left depth | right depth | `1 + max(...)` |
|---|---|---|---|
| 9 | 0 (None) | 0 (None) | **1** |
| 15 | 0 | 0 | **1** |
| 7 | 0 | 0 | **1** |
| 20 | 1 (node 15) | 1 (node 7) | **2** |
| **3** | 1 (node 9) | 2 (node 20) | **3** ✅ |

Node 3's `max(1, 2) = 2` is the key step — the shallow left branch is discarded, and only the deeper right side determines the answer.

**A lopsided check** — `[1, null, 2]`:

| Node | left | right | result |
|---|---|---|---|
| 2 | 0 | 0 | 1 |
| 1 | **0** (missing) | 1 | `1 + max(0,1)` = **2** ✅ |

The missing child contributes 0 and loses the `max` — handled with no branch.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited exactly once, doing O(1) work — one `None` check, one `max`, one addition. The two recursive calls partition the remaining nodes, so nothing is visited twice.

n × O(1) = **O(n)**, and it's optimal: you can't know the deepest path without examining every node. A node you never visit could be the deep one.

**No early exit exists.** Contrast with [Balanced Binary Tree](110-balanced-binary-tree.md), which *can* bail out early once imbalance is proven.

**BFS is also O(n)** — every node is enqueued and dequeued exactly once.

**Note the counting includes `None` calls:** a tree with n nodes makes roughly 2n+1 calls, since every missing child triggers a base case. Still O(n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack, where h is the tree's height.

| Tree shape | h | Space |
|---|---|---|
| Balanced | log₂ n | **O(log n)** |
| Skewed | n | **O(n)** |

At n = 10⁴: a balanced tree needs ~14 frames; a skewed one needs 10⁴ — which **exceeds Python's default recursion limit of 1000** and raises `RecursionError`. Worth naming as the practical failure mode.
→ [recursion-limit](../syntax/recursion-limit.md)

**DFS vs BFS space is genuinely a trade here**, not a formality:

| | Balanced tree | Skewed tree |
|---|---|---|
| **DFS** — O(h) | **O(log n)** ✅ | O(n) |
| **BFS** — O(w) | O(n/2) | **O(1)** ✅ |

Neither wins outright. DFS is better on wide balanced trees (one root-to-leaf path versus half the nodes); BFS is better on deep skewed ones (one node per level). **Pick based on the expected shape** — and say so, because that reasoning is what an interviewer is listening for.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Depth decomposes recursively: the depth of a tree is one plus the depth of its deeper subtree. So the base case is that an empty tree has depth 0, I recurse on both children, and I combine with `1 + max(left, right)` — `max` because depth is the *longest* path, and `+1` for the current node. Returning 0 from the base is what makes a leaf come out as depth 1, matching the node-counting definition. O(n) time since every node is visited once, and O(h) space for the recursion stack — O(log n) balanced, O(n) skewed. BFS counting levels is an equally valid alternative, and it's actually better on space for a deep skewed tree."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it with BFS." | Process level by level, snapshotting `len(queue)` each round, and count the levels. O(n) time, O(w) space. |
| "Which is better, DFS or BFS?" | Depends on shape: DFS is O(h), BFS is O(w). Balanced → DFS wins; skewed → BFS wins. |
| "**Minimum** depth instead?" | ⚠️ Not just swapping `max` for `min` — a node with one missing child would return 0 through the empty side. You must skip absent children. LeetCode 111, a classic trap. |
| "What if the tree is 10⁴ deep?" | Recursion blows Python's stack limit. Use iterative DFS or BFS. |
| "Return the **path**, not just the length?" | Carry the path down and compare at the leaves, or record parent pointers and walk back up. |
| "Is the tree balanced?" | Compute depths and compare siblings — but with an early exit. See [Balanced Binary Tree](110-balanced-binary-tree.md). |
| "Longest path between *any* two nodes?" | The path needn't pass through the root — that's [Diameter of Binary Tree](543-diameter-of-binary-tree.md), and it's this function with one extra line. |

**Traps:**

- **Returning 1 from the base case.** Every depth comes out one too large. The base value *defines* the convention.
- **`min` instead of `max`** — that's a different problem, and naively swapping it is wrong for the reason above.
- **Counting edges instead of nodes.** A single node is depth 1 here; some definitions say 0. Read the statement.
- **Forgetting the `None` check** — `AttributeError` at the first leaf.
- **Assuming balance** and reporting O(log n) space without qualification.
- **Adding the two depths** instead of taking the max — that computes something closer to the diameter, not the depth.

**This same move shows up in:** [Invert Binary Tree](226-invert-binary-tree.md) (the same base-recurse-combine skeleton) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (this exact function, plus a side effect) · [Balanced Binary Tree](110-balanced-binary-tree.md) (depth computed with an early exit) · [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the BFS level-snapshot idiom).

</details>
