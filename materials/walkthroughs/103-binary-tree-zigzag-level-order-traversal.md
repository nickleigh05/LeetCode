# 103. Binary Tree Zigzag Level Order Traversal

**Medium** · [LeetCode](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) · [Solution file (no hints)](../../problems/0001-0499/103.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return the **zigzag level order** traversal of its values — left to right on the first level, right to left on the next, alternating thereafter.

```
root = [3,9,20,null,null,15,7]  →  [[3],[20,9],[15,7]]
root = [1]  →  [[1]]
root = []   →  []
```

**Constraints:** `0 <= number of nodes <= 2000` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**level order**" | BFS — process the tree one full level at a time |
| "**zigzag**" | ⚠️ The only twist: alternate the *output* direction per level |
| grouped per level | The result is a list of lists, so you must know where each level ends |
| `0 <= nodes` | Empty tree returns `[]` |
| `n` up to 2000 | Any O(n) approach is comfortable |

**This is [Level Order Traversal](102-binary-tree-level-order-traversal.md) plus one line.** The BFS machinery is identical; only the direction of each level's output flips.

**The critical realization — don't change the traversal, change the output.**

The tempting mistake is to reverse the *enqueue order* on alternating levels, pushing right-child-first sometimes. That corrupts everything: BFS relies on a consistent enqueue order to produce correct levels, and flipping it scrambles which nodes land in which level.

> **Always traverse left-to-right. Reverse only the collected values for odd levels.**

Traversal stays uniform; presentation alternates.

```
level 0:  [3]           collect [3]        → [3]
level 1:  [9, 20]       collect [9,20]     → reverse → [20,9]
level 2:  [15, 7]       collect [15,7]     → [15,7]
```

**The level-boundary technique.** BFS with a single queue mixes levels together unless you delimit them. The standard fix, and the one worth internalizing:

> At the top of each iteration, record `size = len(queue)`. Those are exactly the nodes of the current level — process precisely that many, and everything enqueued during the pass belongs to the *next* level.

That snapshot is what turns a flat BFS into a level-grouped one.

🤔 **Before you open the next section:** if you flipped the order in which you enqueued children on alternating levels, what would happen to the *next* level's grouping?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Alternate enqueue order | Push right-first on odd levels | — | — | ❌ **Wrong** — corrupts level grouping |
| DFS with a depth parameter | Append to `result[depth]`, reverse odd levels at the end | O(n) | O(h) + O(n) | ✅ Correct, less natural |
| **BFS + reverse odd levels** | Standard level order, flip the output | **O(n)** | **O(w)** | ✅ |
| **BFS + `deque` per level** | `appendleft` on odd levels instead of reversing | **O(n)** | O(w) | ✅ Avoids the reverse |

**The decision: standard BFS with a level-size snapshot, reversing odd levels' collected values.**

The skeleton:

```python
while queue:
    size = len(queue)                    # ← snapshot the level boundary
    level = []
    for _ in range(size):
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    if left_to_right:
        result.append(level)
    else:
        result.append(level[::-1])       # ← the only zigzag-specific line
    left_to_right = not left_to_right
```

**Why the `size` snapshot is essential.** Without it you'd have no idea where one level ends. Taking `len(queue)` *before* the inner loop captures exactly the current level's node count; the children appended during the loop grow the queue but don't affect `size`, so they're correctly deferred to the next iteration.

**Why `deque` and not a list.** BFS needs FIFO — remove from the front. `list.pop(0)` is **O(n)** because every remaining element shifts; `deque.popleft()` is **O(1)**. With 2000 nodes the difference is small, but using a list turns an O(n) algorithm into O(n²) and it's a habit worth having right.

**The `deque`-per-level variant** avoids the reversal entirely:

```python
level = deque()
...
    if left_to_right: level.append(node.val)
    else:             level.appendleft(node.val)
result.append(list(level))
```

Each `appendleft` is O(1), so the level is built in the right order directly rather than being reversed afterwards. Same asymptotics — `level[::-1]` is O(k) for a level of size `k`, and those sum to O(n) overall — so this is a constant-factor refinement, not a complexity one. Worth knowing; either is fine.

**Why DFS is awkward here.** You *can* do it: recurse with a depth argument, append to `result[depth]`, then reverse the odd-indexed lists at the end. It works, but level order is BFS's natural shape, and the DFS version needs the extra "grow the result list when reaching a new depth" bookkeeping.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return []
```

**Empty tree → empty result.** Also prevents enqueuing `None` at the start.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
result = []
queue = deque([root])
left_to_right = True
```

- `queue` — a `deque` for O(1) `popleft`
- `left_to_right` — the direction flag, starting `True` since level 0 goes left-to-right

→ [deque-basics](../syntax/deque-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while queue:
    size = len(queue)
    level = []
```

**Snapshot the level boundary.**

`size` is the exact number of nodes on the current level. Capturing it *before* the inner loop is what keeps levels separate — children enqueued below will be processed on the next outer iteration.
→ [while-loop](../syntax/while-loop.md)

```python
    for _ in range(size):
        node = queue.popleft()
        level.append(node.val)
```

Process exactly this level's nodes, collecting values **always left-to-right**.
→ [range-function](../syntax/range-function.md) · [deque-basics](../syntax/deque-basics.md)

```python
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

**Enqueue children in consistent left-then-right order — never flipped.**

This uniformity is what keeps the level grouping correct. The zigzag is handled purely at output time.

Guarding on existence keeps `None` out of the queue, so no filtering is needed on removal.

```python
    if left_to_right:
        result.append(level)
    else:
        result.append(level[::-1])
```

**The only zigzag-specific logic.** Even levels go in as collected; odd levels are reversed.

`level[::-1]` creates a reversed copy — appropriate here since `level` is being handed to `result` anyway.
→ [list-slicing](../syntax/list-slicing.md)

```python
    left_to_right = not left_to_right
```

Flip the direction for the next level.
→ [boolean-basics](../syntax/boolean-basics.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True

        while queue:
            size = len(queue)
            level = []

            for _ in range(size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            if left_to_right:
                result.append(level)
            else:
                result.append(level[::-1])

            left_to_right = not left_to_right

        return result
```

</details>

<details>
<summary>The deque-per-level variant (no reversal)</summary>

```python
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True

        while queue:
            level = deque()
            for _ in range(len(queue)):
                node = queue.popleft()
                if left_to_right:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)

            result.append(list(level))
            left_to_right = not left_to_right

        return result
```

Builds each level in its final order via O(1) `appendleft`, avoiding the reversal pass.

</details>

**Trace it** — `root = [3,9,20,null,null,15,7]`:

```
    3
   / \
  9   20
     /  \
    15   7
```

| Iteration | `size` | Nodes popped | `level` collected | `left_to_right` | Appended |
|---|---|---|---|---|---|
| 1 | 1 | 3 | `[3]` | `True` | `[3]` |
| 2 | 2 | 9, 20 | `[9, 20]` | `False` | **`[20, 9]`** (reversed) |
| 3 | 2 | 15, 7 | `[15, 7]` | `True` | `[15, 7]` |

Return **`[[3],[20,9],[15,7]]`** ✅

**Queue evolution:**

| After iteration | Queue contents |
|---|---|
| start | `[3]` |
| 1 | `[9, 20]` — 3's children, enqueued left-then-right |
| 2 | `[15, 7]` — 9 has none; 20's children |
| 3 | `[]` — both are leaves |

Note iteration 2: nodes were **popped** as 9 then 20 (left-to-right, preserving correct BFS order), and only the *collected list* was reversed. Had the enqueue order been flipped instead, 20's children would have entered the queue before 9's, and level 2 would have been grouped wrongly.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each node is enqueued once and dequeued once, doing O(1) work — one `popleft`, one append, up to two enqueues.

**The reversals add O(n) total, not O(n) per level.** Reversing a level of size `k` costs O(k), and the level sizes sum to `n` across the whole tree, so all reversals together are O(n).

Total: O(n) traversal + O(n) reversals = **O(n)**.

The `deque`-per-level variant eliminates the reversal constant by using O(1) `appendleft`, but the asymptotic class is unchanged.

**The one way to break this:** using a list as the queue and calling `pop(0)`. That's O(n) per removal, making the whole thing **O(n²)**. Use `collections.deque`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(w)</summary>

**O(w)** where `w` is the tree's maximum **width** — the largest number of nodes on any single level.

For a complete binary tree the last level holds about `n/2` nodes, so worst case is **O(n)**.

**Excluding the output**, which is O(n) and required.

**The DFS/BFS space contrast**, which is worth having ready:

| | Space | Worst shape |
|---|---|---|
| **BFS (this)** | O(w) | **O(n)** for a wide/complete tree |
| DFS | O(h) | **O(n)** for a degenerate chain |

They fail on *opposite* tree shapes:

- A **complete** tree: `h = log n` but `w = n/2` → DFS is cheap, BFS is expensive.
- A **degenerate** chain: `h = n` but `w = 1` → BFS is cheap, DFS is expensive.

Neither dominates. Choose by which property the problem needs — and level-grouped output is fundamentally BFS-shaped, so O(w) is the natural cost here.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is standard level-order BFS with one extra line. I use a `deque` for O(1) `popleft`, and at the top of each iteration I snapshot `len(queue)` — that's exactly the current level's node count, so processing that many pops gives me one clean level while the children I enqueue belong to the next. The zigzag part is purely presentational: I **always** traverse and enqueue left-to-right, and only reverse the collected values on odd levels. Flipping the enqueue order instead would corrupt the level grouping, because BFS depends on consistent ordering. O(n) time — the reversals sum to O(n) across all levels — and O(w) space for the queue. I could also build each level in a `deque` and `appendleft` on odd levels to skip the reversal entirely."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not flip the enqueue order?" | **The key question.** BFS needs consistent enqueue order; flipping it scrambles which nodes land on which level. Reverse the *output*, not the traversal. |
| "How do you know where a level ends?" | Snapshot `len(queue)` before the inner loop — that's the current level's exact size. |
| "Avoid the reversal?" | Use a `deque` per level and `appendleft` on odd levels — O(1) each, built in final order. |
| "Solve it with DFS." | Recurse with a depth argument, append to `result[depth]`, then reverse odd-indexed lists. Works, but level order is BFS's natural shape. |
| "Plain [level order](102-binary-tree-level-order-traversal.md)?" | Delete the flag and the reversal — the rest is identical. |
| "Bottom-up level order?" | [LeetCode 107](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) — same BFS, reverse the outer `result` at the end. |
| "Why `deque` over a list?" | `list.pop(0)` is O(n) from shifting, making the whole thing O(n²). `deque.popleft()` is O(1). |

**Traps:**

- **Alternating the enqueue order.** *The* bug — produces wrongly grouped levels that can look plausible on small trees.
- **Forgetting the `size` snapshot.** Levels merge into one flat list.
- **Computing `size` inside the inner loop.** The queue is growing, so the boundary moves and levels blur.
- **Using `list.pop(0)`.** O(n) per removal → O(n²) overall.
- **Enqueuing `None` children.** Then `node.val` raises. Guard on existence.
- **Forgetting to flip the flag.** Every level comes out left-to-right.
- **Reversing `result` instead of each level.** That's the bottom-up variant, a different problem.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (this problem without the zigzag) · [Binary Tree Right Side View](199-binary-tree-right-side-view.md) (same BFS, take the last node of each level) · [Minimum Depth of Binary Tree](111-minimum-depth-of-binary-tree.md) (BFS with early exit at the first leaf) · [Rotting Oranges](994-rotting-oranges.md) (level-by-level BFS where levels represent elapsed time).

</details>

---
