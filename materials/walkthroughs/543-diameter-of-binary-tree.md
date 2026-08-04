# 543. Diameter of Binary Tree

**Easy** · [LeetCode](https://leetcode.com/problems/diameter-of-binary-tree/) · [Solution file (no hints)](../../problems/0500-0999/543.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return the length of its **diameter** — the length of the **longest path between any two nodes**, which **may or may not pass through the root**.

The length of a path is the **number of edges** between its endpoints.

```
        1              diameter = 3
      /   \            the path 4 → 2 → 1 → 3
     2     3
    / \
   4   5

root = [1,2,3,4,5]  →  3
root = [1,2]        →  1
```

**Constraints:** `1 <= nodes <= 10⁴` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "between **any two nodes**" | Not root-to-leaf. The path can run between two leaves in different subtrees |
| "**may not pass through the root**" | ⚠️ So you can't just measure at the root — the answer could be buried deep inside one subtree |
| "number of **edges**" | ⚠️ Edges, not nodes. A two-node path has length **1**. This differs from [Maximum Depth](104-maximum-depth-of-binary-tree.md), which counts nodes |
| n up to 10⁴ | O(n) expected; an O(n²) approach would be 10⁸ |

**The observation that cracks it.** Any path in a binary tree has a **highest point** — a single node where it stops going up and starts going down. Below that node, the path descends into the left subtree on one side and the right subtree on the other.

```
        1     ← the peak of the path 4→2→1→3
      /   \
     2     3
    / \
   4   5
```

So for **each node**, the longest path peaking there is:

```
left_depth + right_depth        (in edges)
```

And the diameter is the maximum of that over **every** node — you don't know in advance which node is the peak, so you check them all.

**Now the efficiency insight.** Computing depth at every node independently is O(n) per node → O(n²). But a single DFS already computes every subtree's depth on its way back up. **So compute the depth as usual, and while you're there, also check whether this node's `left + right` beats the best seen so far.**

One traversal, two results: the returned value (depth) and an accumulated side effect (the best diameter).

🤔 **Before you open the next section:** the function needs to *return* a depth but also *record* a maximum. Where can that maximum live, given that recursion returns only one value?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| For each node, compute both depths | Call `maxDepth` at every node | **O(n²)** | ❌ Recomputes depths constantly |
| **One DFS, depth + running max** | Compute depth; record `left+right` en route | **O(n)** | ✅ |

**The decision: one DFS that returns depth while accumulating the best diameter in an outer variable.**

This is the unit's second big idea, and it's genuinely important: **a recursive function can produce two kinds of answer at once.**

- **The return value** — what the *parent* needs. Here: this subtree's depth.
- **The accumulator** — a global fact being maximized across all nodes. Here: the diameter.

The parent doesn't need the diameter (the best path might not involve the parent at all), so it can't be the return value. But every node must contribute a *candidate*. Storing that outside the recursion is the clean resolution.

**Why the O(n²) version is wasteful.** Calling `maxDepth(node)` at every node re-walks each subtree once per ancestor. The single-pass version gets the same depths for free, because the recursion is already visiting bottom-up.

**Why `left + right` and not `left + right + 1`.** The depths are counted in **nodes** (a leaf returns 1), but the answer is in **edges**. For a node with depths `l` and `r`, the path has `l + r` edges — the +1s cancel exactly. Check it on the example: node 1 has `left=2, right=1`, so `2 + 1 = 3` edges ✅ — the path `4→2→1→3`.

**Where to store the accumulator.** `self.best` is used here — an instance attribute, visible to the nested function. Alternatives: a `nonlocal` variable, or a one-element list. All equivalent; `self.` is the most common in interviews.

*(A plain `best = 0` inside the method **won't work** — assigning to it inside the nested function creates a new local. You need `nonlocal best`, `self.best`, or a mutable container.)*

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
self.best = 0
```

**The accumulator**, living outside the recursion so every node can contribute to it. Starting at 0 is correct — a single-node tree has diameter 0 (no edges).

Using `self.` rather than a plain local is deliberate: the nested function can *read* a local, but assigning to it would shadow it. `self.best` is mutable shared state.
→ [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) · [scope-legb](../syntax/scope-legb.md)

```python
def depth(node):
    if not node:
        return 0
```

A nested helper — a **closure** that can see `self`. It returns **depth in nodes**, exactly as in [problem 104](104-maximum-depth-of-binary-tree.md); the base case of 0 for an empty subtree makes a leaf come out as 1.
→ [closures](../syntax/closures.md) · [function-basics](../syntax/function-basics.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    left = depth(node.left)
    right = depth(node.right)
```

Recurse both sides, capturing the depths — you need **both** values, one for the diameter check and both for the return.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
    self.best = max(self.best, left + right)
```

**The extra line that turns depth into diameter.** The longest path *peaking at this node* has `left + right` edges. Compare it against the best found anywhere so far.

This runs at **every** node, which is how a path buried deep in a subtree still gets considered — answering the "may not pass through the root" requirement directly.

The +1s cancel: node depths minus the shared node give exactly the edge count.
→ [min-max-key](../syntax/min-max-key.md)

```python
    return max(left, right) + 1
```

**The return value is still just the depth** — unchanged from [104](104-maximum-depth-of-binary-tree.md).

This is the crux of the two-results pattern: the parent gets a *depth*, because that's what it needs to compute its own depth and its own diameter candidate. The diameter itself never travels up the return path.
→ [min-max-key](../syntax/min-max-key.md)

```python
depth(root)
return self.best
```

Run the traversal purely for its side effect, then read the accumulated answer. The returned depth of the whole tree is discarded — it was never the question.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:

        self.best = 0

        def depth(node):
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            self.best = max(self.best, left + right)
            return max(left, right) + 1

        depth(root)
        return self.best
```

</details>

**Trace it** — `[1,2,3,4,5]`:

```
        1
      /   \
     2     3
    / \
   4   5
```

Bottom-up:

| Node | `left` | `right` | `left+right` (candidate) | `self.best` | returns `max+1` |
|---|---|---|---|---|---|
| 4 | 0 | 0 | 0 | 0 | **1** |
| 5 | 0 | 0 | 0 | 0 | **1** |
| 2 | 1 | 1 | **2** | **2** | **2** |
| 3 | 0 | 0 | 0 | 2 | **1** |
| **1** | 2 | 1 | **3** | **3** | 3 |

Answer: **3** ✅ — the path `4 → 2 → 1 → 3`, three edges.

**And a case where the diameter avoids the root** — a tree whose left subtree is deep and bushy while the right is a single node:

```
        1
      /   \
     2     9
    / \
   4   5
  /     \
 6       7
```

At node 2: `left = 2, right = 2` → candidate **4** (path `6→4→2→5→7`).
At node 1: `left = 3, right = 1` → candidate **4**.

Both give 4, but note the winning *path* never touches node 1 — it was recorded when the recursion was at node 2. That's exactly why the check runs at every node.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited **exactly once**, doing O(1) work: two recursive calls, one addition, two `max` operations.

n × O(1) = **O(n)**.

**Versus the naive O(n²).** Calling `maxDepth(node)` at every node re-traverses each subtree once per ancestor — on a balanced tree that's O(n log n), and on a skewed one O(n²) → 10⁸ at the constraint limit.

**Why one pass suffices:** the recursion *already* computes every subtree's depth on its way back up. The diameter check is one extra comparison at a node you were visiting anyway. **The information was free; you just had to notice it was there.**

That's a broadly useful instinct: before adding a second traversal, ask whether the first one already passes through the data you need.

**No early exit** — the deepest path could peak anywhere, so every node must be checked.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack — O(log n) for a balanced tree, **O(n)** for a skewed one.

`self.best` is a single integer, O(1). Nothing else is allocated.

At n = 10⁴, a skewed tree means 10⁴ stack frames, past Python's default limit of 1000 → `RecursionError`. The iterative rewrite (an explicit postorder stack) is fiddlier here than in [104](104-maximum-depth-of-binary-tree.md), because you need both children's results before processing a node.
→ [recursion-limit](../syntax/recursion-limit.md)

**Why BFS doesn't help.** Level-order gives you nodes in the wrong order — you need children's depths *before* the parent, which is inherently bottom-up (postorder). BFS is top-down. **Any problem where a node's answer depends on its subtrees' answers is a DFS problem**, and that covers most of this unit.

**On the accumulator's cost:** `self.best` is O(1). An alternative that returns tuples — `(depth, diameter)` from every call — avoids shared state at the same complexity, and some interviewers prefer it as cleaner functional style. Worth mentioning.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every path has a highest node, and at that node the path is just `left depth + right depth` in edges. Since the diameter may not pass through the root, I have to consider every node as a potential peak. The naive way — computing depths at each node separately — is O(n²), but a single DFS already computes every subtree's depth on the way back up. So I run the standard depth recursion and add one line: at each node, compare `left + right` against a running maximum stored outside the recursion. The function still *returns* the depth, because that's what the parent needs; the diameter accumulates as a side effect. O(n) time, O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't the function just return the diameter?" | **The question.** The parent needs the *depth* to compute its own depth and its own candidate. The diameter is a global maximum, not something that composes upward — so it lives in an accumulator. |
| "Why `left + right` and not `+1`?" | Depths count nodes, the answer counts edges, and the +1s cancel. Verify on a two-node tree: depths 1 and 0 → 1 edge ✅ |
| "Avoid the shared state." | Return a tuple `(depth, best_diameter)` from every call and combine both at each node. Same complexity, purely functional. |
| "What if edges had **weights**?" | Same structure, but return the maximum weighted depth and add the two branch weights. |
| "Longest path by node **values** rather than length?" | That's [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) — the same peak-node insight, with a `max(0, …)` to discard negative branches. |
| "Do it iteratively." | Postorder with an explicit stack, since a node needs both children's results first. Noticeably fiddlier than the recursive form. |
| "Diameter of a general graph?" | Very different — BFS from every node, or two BFS passes for a tree-shaped graph. |

**Traps:**

- **Returning `left + right + 1`** as the depth. That mixes the two quantities and breaks every ancestor's calculation.
- **Trying to return the diameter** instead of accumulating it. It doesn't compose — a parent's diameter isn't a function of its children's diameters alone.
- **Only checking at the root.** Fails whenever the longest path is inside a subtree.
- **Using a plain local `best = 0`** and assigning to it in the nested function — Python creates a new local. Use `self.best`, `nonlocal`, or a mutable container.
- **Counting nodes instead of edges.** A two-node tree has diameter 1, not 2.
- **Recomputing depth per node** — correct but O(n²).

**This same move shows up in:** [Maximum Depth](104-maximum-depth-of-binary-tree.md) (the depth function this extends) · [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) (the same peak-node idea with values) · [Balanced Binary Tree](110-balanced-binary-tree.md) (one traversal returning depth *and* a validity flag) · [dfs](../algorithms/dfs.md).

</details>
