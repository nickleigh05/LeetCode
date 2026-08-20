# 102. Binary Tree Level Order Traversal

**Medium** · [LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/) · [Solution file (no hints)](../../problems/0001-0499/102.py)

[📖 08. Trees lesson](../learning/08-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Trees problems](../rmap-practice/08-trees.md)

---

Given the root of a binary tree, return the **level order traversal** of its nodes' values — level by level, from left to right.

```
        3                    →  [[3], [9,20], [15,7]]
      /   \
     9     20
          /  \
        15    7

root = [1]  →  [[1]]
root = []   →  []
```

**Constraints:** `0 <= nodes <= 2000` · `-1000 <= Node.val <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**level by level**" | ⚠️ Every previous problem in this unit went *depth*-first. This one is **breadth**-first — a different traversal entirely |
| "left to right" | Within a level, order matters — so enqueue left before right |
| output is a **list of lists** | ⚠️ You must know where one level ends and the next begins. A flat traversal isn't enough |
| tree can be empty | `[]`, not `[[]]` |
| n up to 2000 | O(n) expected |

**Why DFS doesn't fit.** Depth-first dives to the bottom of one branch before touching the next, so it visits `3, 9, 20, 15, 7` in an order that jumps between levels. You'd have to tag each value with its depth and regroup afterwards — possible, but working against the traversal instead of with it.

**Breadth-first is the natural match.** Visit all nodes at distance 0, then distance 1, then 2 — which is exactly "level by level."

The mechanism is a **queue**, and the reason is the discipline:

| Structure | Order | Traversal |
|---|---|---|
| **Stack** (LIFO) | most recently added first | depth-first — dives deep |
| **Queue** (FIFO) | earliest added first | **breadth-first** — spreads wide |

A queue processes nodes in discovery order. Since a node's children are discovered while processing that node, all of level k is queued before any of level k+1 — so they come out in level order automatically.

**The one genuine subtlety:** the queue mixes levels as you go (processing level 1 appends level 2 nodes behind it). So how do you know where a level ends?

🤔 **Before you open the next section:** at the exact moment you start a new level, what does the queue contain — and what does its *length* tell you?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| DFS, tagging each node with its depth | Recurse, append to `result[depth]` | O(n) | ✅ Works — DFS can do this |
| BFS with `(node, level)` pairs | Store the depth alongside each node | O(n) | ⚠️ Correct, more bookkeeping |
| **BFS with a level-size snapshot** | Record `len(queue)` before each level | **O(n)** | ✅ |

**The decision: [BFS](../algorithms/bfs.md) with a [queue](../data-structures/queue.md), snapshotting the queue length at the start of each level.**

**The snapshot idiom — learn this one.** At the top of each round, the queue contains *exactly* the current level and nothing else. So:

```python
level_size = len(queue)          # ← freeze it BEFORE the loop
for _ in range(level_size):
    ...                          # pop one node, maybe append its children
```

Because `level_size` is captured first, the loop runs exactly that many times — processing precisely this level, even as children are appended behind them.

⚠️ **Writing `while queue:` for the inner loop would consume everything**, because children keep arriving. The snapshot is what draws the boundary.

**This idiom is the foundation of every level-based tree problem.** It reappears directly in [Right Side View](199-binary-tree-right-side-view.md), and in BFS over grids and graphs in Unit 11 — where "level" becomes "distance from the source."

**Why `deque` and not a list.** `collections.deque` gives **O(1)** `popleft()`. A plain list's `pop(0)` is **O(n)**, because every remaining element shifts — silently turning the whole traversal into O(n²).
→ [deque](../data-structures/deque.md)

**DFS can also solve this**, and it's worth mentioning: recurse carrying the depth, and append each value to `result[depth]`, creating a new sublist when you reach a new depth. Same O(n). But BFS matches the problem's shape, and the snapshot idiom is what you want in your toolkit.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if root is None:
    return []
```

An empty tree has no levels. The guard matters — without it, `deque([None])` would enter the loop and crash on `node.val`.
→ [identity-operators](../syntax/identity-operators.md) · [if-return](../syntax/if-return.md)

```python
result = []
queue = deque([root])
```

`result` collects one sublist per level. The queue starts holding just the root — level 0.

`deque` is imported from `collections` and gives O(1) operations at both ends.
→ [from-import](../syntax/from-import.md) · [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
while queue:
```

Each iteration processes **one complete level**. The loop ends when no nodes remain — an empty deque is falsy.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    level_size = len(queue)
    current_level = []
```

**The snapshot — the key line.** Right now the queue holds exactly this level's nodes, so `len(queue)` is the level's width.

Capturing it **before** the inner loop is what keeps the boundary intact: children appended during the loop don't extend it.
→ [list-basics](../syntax/list-basics.md)

```python
    for i in range(level_size):
        node = queue.popleft()
        current_level.append(node.val)
```

Process exactly `level_size` nodes. `popleft()` takes from the **front** — the FIFO discipline that makes this breadth-first.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [list-methods](../syntax/list-methods.md)

```python
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
```

Enqueue the children at the **back**, so they're processed after everything currently ahead of them — i.e. in the next round.

**Left before right**, because the problem wants left-to-right order within a level.

The `None` checks keep empty slots out of the queue, so no `None` handling is needed anywhere else.
→ [identity-operators](../syntax/identity-operators.md)

```python
    result.append(current_level)
```

The level is complete — add it as its own sublist. This line is why the output is nested rather than flat.

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if root is None:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for i in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)

            result.append(current_level)

        return result
```

</details>

**Trace it** — `[3,9,20,null,null,15,7]`:

| Round | Queue at start | `level_size` | Processed | Children enqueued | `result` |
|---|---|---|---|---|---|
| 1 | `[3]` | **1** | 3 | 9, 20 | `[[3]]` |
| 2 | `[9, 20]` | **2** | 9, 20 | 15, 7 (from 20) | `[[3], [9,20]]` |
| 3 | `[15, 7]` | **2** | 15, 7 | none | `[[3], [9,20], [15,7]]` |
| 4 | `[]` | — | loop ends | | ✅ |

Watch round 2: the snapshot is **2**, so exactly nodes 9 and 20 are processed — even though 15 and 7 join the queue midway through. Without freezing the size, the loop would have swallowed them into the same level.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is **enqueued exactly once and dequeued exactly once**, doing O(1) work each: one `popleft`, one `append` to the level list, and up to two child checks.

2n queue operations + n appends = **O(n)**.

**⚠️ Only if you use a `deque`.** With a plain list, `pop(0)` shifts every remaining element — O(n) per removal, **O(n²)** overall. At n = 2000 that's 4·10⁶ instead of 2·10³. This is the single most common performance bug in BFS code.

**The nested loops are not quadratic.** The outer `while` runs once per level and the inner `for` once per node in that level, so the inner iterations sum to exactly n across all levels — the same "count the total, not the nesting" accounting used throughout Units 03–04.

**No early exit** — every node appears in the output.

**DFS with depth tagging is also O(n)**; the two approaches differ in space and in which one matches the problem's shape.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the output, **O(w)** auxiliary — where **w is the tree's maximum width**.

- `result` holds every value → O(n), the required output.
- `queue` holds at most one full level at a time → O(w).

**For a balanced tree, w = n/2** — the bottom level contains about half of all nodes. So BFS auxiliary space is **O(n)** in that case.

**This is the DFS/BFS trade, and it's a real one:**

| | Balanced tree | Skewed tree |
|---|---|---|
| **DFS** — O(h) | **O(log n)** ✅ | O(n) |
| **BFS** — O(w) | O(n/2) | **O(1)** ✅ |

Neither wins in general — it depends entirely on the tree's shape. **A wide, shallow tree favours DFS; a deep, narrow one favours BFS.** Being able to say that is what an interviewer is listening for when they ask "which would you use?"

For *this* problem, BFS is still the right choice despite the space: the level grouping falls out of the algorithm rather than being reconstructed afterwards.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Level order is breadth-first, so I use a queue — FIFO means nodes come out in discovery order, and since children are discovered while processing their parents, an entire level is queued before any of the next. The one subtlety is knowing where a level ends, because children get appended while I'm still processing the current level. The fix is to snapshot `len(queue)` before the inner loop: at that moment the queue holds exactly this level, so I process precisely that many nodes. I use `collections.deque` rather than a list, because `pop(0)` on a list is O(n) and would make the whole thing quadratic. O(n) time, and O(w) auxiliary space for the widest level — which is about n/2 on a balanced tree."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why snapshot the queue length?" | **The question.** Children are appended during the level, so `while queue` would merge levels. Freezing the count draws the boundary. |
| "Why `deque` instead of a list?" | `list.pop(0)` is O(n) — it shifts everything. `deque.popleft()` is O(1). |
| "**Zigzag** level order?" | Same traversal; reverse alternate levels before appending (or `appendleft` into the level list). LeetCode 103. |
| "Bottom-up level order?" | Build normally, then reverse `result`. LeetCode 107. |
| "Solve it with DFS." | Recurse carrying the depth; append to `result[depth]`, creating a sublist when reaching a new depth. O(n) time, O(h) space. |
| "Only the rightmost node of each level?" | That's [Right Side View](199-binary-tree-right-side-view.md) — the same loop, taking the last node per level. |
| "DFS or BFS in general?" | DFS is O(h) space, BFS is O(w). Deep-narrow favours BFS; wide-shallow favours DFS. |

**Traps:**

- **Using a list as a queue.** `pop(0)` silently makes it O(n²).
- **`while queue` for the inner loop** instead of the snapshot — levels merge into one giant list.
- **Computing `len(queue)` inside the loop** rather than before it — same merging bug.
- **Enqueuing `None` children** and then crashing on `node.val`, or emitting phantom entries.
- **Appending right before left** — the level order comes out reversed.
- **Forgetting the empty-tree guard** — `deque([None])` enters the loop and crashes.

**This same move shows up in:** [Right Side View](199-binary-tree-right-side-view.md) (the same snapshot loop, taking one node per level) · [Maximum Depth](104-maximum-depth-of-binary-tree.md) (counting levels with the same idiom) · [Rotting Oranges](994-rotting-oranges.md) and [Number of Islands](200-number-of-islands.md) (BFS on grids, where levels become distances) · [bfs](../algorithms/bfs.md).

</details>

---
