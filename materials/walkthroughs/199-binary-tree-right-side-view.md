# 199. Binary Tree Right Side View

**Medium** · [LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/)

[📖 08. Trees lesson](../learning/08-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Trees problems](../rmap-practice/08-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given the root of a binary tree, imagine yourself standing on the **right side** of it. Return the values of the nodes you can see, ordered **top to bottom**.

```
        1     ←  visible
      /   \
     2     3  ←  visible
      \     \
       5     4  ←  visible

root = [1,2,3,null,5,null,4]  →  [1,3,4]
root = [1,null,3]             →  [1,3]
root = []                     →  []
```

**Constraints:** `0 <= nodes <= 100` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "from the **right side**" | ⚠️ **Not** "the rightmost path". A right child can be missing while a left child at that depth is still visible |
| "**top to bottom**" | One value per **level**, in level order |
| "the values you can **see**" | Exactly one node per level — the one furthest right at that depth |

**The trap worth spending a moment on.** The intuitive-but-wrong reading is "follow `root.right` until you fall off the end." On the example that gives `[1, 3, 4]` — which happens to be correct. But try:

```
        1
      /   \
     2     3
    /
   4              →  correct answer [1, 3, 4]
```

Following only right children gives `[1, 3]` and misses node 4 — which **is** visible, because level 2 has no other node. Node 3 has no children, so 4 is the rightmost thing at its depth.

So the real rule is:

> **For each level, take the node furthest to the right.**

Which reframes it completely: this isn't a path-following problem, it's a **level** problem. And you already have the machinery — [Level Order Traversal](102-binary-tree-level-order-traversal.md) processes exactly one level at a time.

Instead of collecting every value in a level, keep only the **last** one.

🤔 **Before you open the next section:** in the level-order loop, nodes are dequeued left to right. Which iteration index corresponds to the node you can see?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Follow `root.right` repeatedly | Walk the right spine | O(h) | ❌ **Wrong** — misses left nodes with no right sibling |
| Full level-order, then take each level's last | Build all levels, then `[level[-1] for level in levels]` | O(n) | ⚠️ Correct, but stores every value |
| **BFS, keeping only the last node per level** | Level-order with a filter | **O(n)** | ✅ |
| DFS, **right child first** | First node reached at each new depth is the visible one | O(n) | ✅ Elegant alternative |

**The decision: [BFS](../algorithms/bfs.md) with the level-size snapshot, appending only the last node of each level.**

It's [problem 102](102-binary-tree-level-order-traversal.md) with one line changed. The snapshot idiom does the work:

```python
level_size = len(queue)
for i in range(level_size):
    node = queue.popleft()
    if i == level_size - 1:      # ← the only new logic
        result.append(node.val)
```

Since nodes are dequeued left to right, index `level_size - 1` is the **rightmost node at that depth** — visible by definition. No path-following, no special cases for missing children.

**The DFS alternative is genuinely nice and worth knowing.** Traverse **right child first**, tracking depth. The *first* node you reach at any new depth must be the rightmost at that depth:

```python
def dfs(node, depth):
    if not node: return
    if depth == len(result):     # first node seen at this depth
        result.append(node.val)
    dfs(node.right, depth + 1)   # right BEFORE left
    dfs(node.left, depth + 1)
```

`depth == len(result)` is a neat trick: `result` has one entry per depth so far, so its length *is* the next unseen depth.

**BFS vs DFS here:** BFS is O(w) space, DFS is O(h). On a deep narrow tree DFS wins; on a wide shallow one BFS wins. Both are O(n) time. **BFS reads more directly as "one per level", which is why it's the primary answer** — but volunteering the DFS version shows range.

**Why not build all levels first?** Correct, but it stores O(n) values to keep O(h) of them. Filtering as you go is strictly better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if root is None:
    return []
```

No tree, nothing visible. Also prevents `deque([None])` from entering the loop and crashing.
→ [identity-operators](../syntax/identity-operators.md) · [if-return](../syntax/if-return.md)

```python
result = []
queue = deque([root])
```

`result` collects one value per level. The queue starts with level 0.

Note there's no `current_level` list here — unlike [102](102-binary-tree-level-order-traversal.md), we're keeping only one value per level, so there's nothing to accumulate.
→ [from-import](../syntax/from-import.md) · [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
while queue:
    level_size = len(queue)
```

**The snapshot idiom**, exactly as in [102](102-binary-tree-level-order-traversal.md). At this instant the queue holds precisely one level, so `len(queue)` is its width — and freezing it before the inner loop is what keeps children from bleeding into the current level.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    for i in range(level_size):
        node = queue.popleft()
```

Process exactly this level's nodes, left to right. Here `i` is genuinely used — unlike [102](102-binary-tree-level-order-traversal.md), where it was just a counter.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if i == level_size - 1:
            result.append(node.val)
```

**The one line that distinguishes this problem.** The last index of the level is the **rightmost node at that depth** — the one you can see.

This is why the missing-right-child case works for free: whichever node happens to be last in the queue for that level is recorded, regardless of whether it came from a left or right child.
→ [comparison-operators](../syntax/comparison-operators.md) · [list-methods](../syntax/list-methods.md)

```python
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
```

Enqueue children for the next level, **left before right** — preserving left-to-right order so that "last dequeued" really is "furthest right".
→ [identity-operators](../syntax/identity-operators.md)

```python
return result
```

One value per level, top to bottom.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:

        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    result.append(node.val)

                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)

        return result
```

</details>

**Trace it** — `[1,2,3,null,5,null,4]`:

```
        1
      /   \
     2     3
      \     \
       5     4
```

| Round | Queue | `level_size` | Dequeued (i) | Recorded | `result` |
|---|---|---|---|---|---|
| 1 | `[1]` | 1 | 1 (i=0 = last) | **1** | `[1]` |
| 2 | `[2, 3]` | 2 | 2 (i=0), **3** (i=1) | **3** | `[1,3]` |
| 3 | `[5, 4]` | 2 | 5 (i=0), **4** (i=1) | **4** | `[1,3,4]` ✅ |

**The case that breaks the right-spine approach:**

```
        1
      /   \
     2     3
    /
   4
```

| Round | Queue | Dequeued | Recorded |
|---|---|---|---|
| 1 | `[1]` | 1 | **1** |
| 2 | `[2, 3]` | 2, **3** | **3** |
| 3 | `[4]` | **4** (only node) | **4** |

Result `[1,3,4]` ✅

Node 4 is a **left** child, and it's visible because level 2 contains nothing else. Following `root.right` would have stopped at node 3 and returned `[1,3]` — wrong.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is enqueued once and dequeued once, doing O(1) work — a comparison, up to two child checks, and occasionally an append.

**O(n)** total.

**You must visit every node**, even though only h of them appear in the output. There's no way to know which node is rightmost at a given depth without examining the whole level — a node buried in the left subtree can be the visible one, as the second trace shows.

**⚠️ `deque` matters again.** A list's `pop(0)` is O(n), making this O(n²). Same trap as [102](102-binary-tree-level-order-traversal.md).

**The DFS alternative is also O(n)** — it visits every node too, just in a different order.

**No early exit** — the deepest level could be anywhere.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(w)</summary>

**O(w)** auxiliary, where w is the maximum width — plus **O(h)** for the output (one value per level).

The queue holds at most one full level. For a balanced tree that's **n/2**, so O(n) in practice.

**Compare with the DFS version, which is O(h):**

| Approach | Time | Auxiliary space |
|---|---|---|
| **BFS** | O(n) | **O(w)** — n/2 balanced, 1 skewed |
| DFS (right-first) | O(n) | **O(h)** — log n balanced, n skewed |

Neither dominates. For a **wide, shallow** tree DFS is dramatically better; for a **deep, narrow** one BFS is. Say which you'd pick and why — that reasoning is the substance of the follow-up.

**Note the output is only O(h)** — one value per level, so at most the height. That's much smaller than [102](102-binary-tree-level-order-traversal.md)'s O(n) output, and it's why filtering during the traversal (rather than building all levels and slicing) is worth doing: you never hold more than one level plus h results.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The tempting answer is to follow right children down the spine, but that's wrong — if a node has no right child, a node in its left subtree can still be the rightmost at that depth. The correct rule is one node per level: the furthest right at each depth. So it's level-order BFS with the queue-size snapshot, and instead of collecting every value in a level I keep only the last one dequeued — since nodes come out left to right, the last is the rightmost. O(n) time, O(w) space for the queue. I could also DFS visiting the right child first and record the first node seen at each new depth, which is O(h) space instead — better on a deep narrow tree."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just follow right children?" | **The question.** A node with no right child can have a visible left descendant. Demo with `[1,2,3,4]` where 4 is a left child. |
| "Solve it with DFS." | Visit right before left, tracking depth; the first node at a new depth is visible. Use `depth == len(result)` as the test. O(h) space. |
| "**Left** side view?" | BFS taking `i == 0` instead, or DFS visiting left first. |
| "BFS or DFS here?" | BFS is O(w), DFS is O(h). Wide-shallow → DFS; deep-narrow → BFS. Same time either way. |
| "The **largest** value per level?" | Same loop, track a running max instead of the last node. LeetCode 515. |
| "Average value per level?" | Sum each level and divide by `level_size`. LeetCode 637. |
| "Why is the output O(h), not O(n)?" | Exactly one value per level, and the number of levels is the height. |

**Traps:**

- **Following the right spine.** The defining mistake — it's wrong whenever a right child is missing but the level isn't empty.
- **Recording `i == 0`** — that's the left side view.
- **Not snapshotting `level_size`**, so levels merge and the "last" node is the last of *everything*.
- **Using a list as a queue** → O(n²).
- **In the DFS version, visiting left first** — you'd record the leftmost node at each depth.
- **Appending right before left** in BFS, reversing the within-level order.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the snapshot loop this specializes) · [Maximum Depth](104-maximum-depth-of-binary-tree.md) (counting levels with BFS) · [Rotting Oranges](994-rotting-oranges.md) (BFS levels as time steps) · [bfs](../algorithms/bfs.md).

</details>

---
