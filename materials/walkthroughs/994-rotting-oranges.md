# 994. Rotting Oranges

**Medium** · [LeetCode](https://leetcode.com/problems/rotting-oranges/)

[📖 12. Graphs lesson](../learning/12-graphs.md) · [📖 Grids primer](../learning/11b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Graphs problems](../rmap-practice/12-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an `m × n` grid where each cell is:

- **`0`** — empty
- **`1`** — a **fresh** orange
- **`2`** — a **rotten** orange

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.

Return the **minimum number of minutes** until no cell has a fresh orange. If that's impossible, return `-1`.

```
grid = [[2,1,1],
        [1,1,0],     →  4
        [0,1,1]]

grid = [[2,1,1],
        [0,1,1],     →  -1     (the bottom-left orange is unreachable)
        [1,0,1]]

grid = [[0,2]]  →  0           (no fresh oranges at all)
```

**Constraints:** `1 <= m, n <= 10` · each cell is `0`, `1`, or `2`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**every minute**" | ⚠️ Time advances in discrete steps — you need the *number of steps*, which is a **shortest-path** question |
| "**any** fresh orange adjacent to a rotten one" | Rot spreads from **all** rotten oranges **simultaneously** |
| "**minimum** minutes" | The answer is the time for the *last* orange to rot |
| "`-1` if impossible" | Some fresh oranges may be unreachable — you must detect that |
| "no cell has a fresh orange" | An initially all-clean grid answers **0**, not −1 |

**Why this must be BFS, not DFS.** Every grid problem so far ([Number of Islands](200-number-of-islands.md), [Max Area of Island](695-max-area-of-island.md)) asked *"what's reachable?"* — and for that, DFS and BFS are interchangeable.

This one asks *"how many steps?"*, and that changes everything:

> **BFS explores in order of distance.** Everything one step away is visited before anything two steps away. So the level number *is* the minute count.

DFS dives deep first, so a cell might be reached by a long path before a short one — it can't tell you the minimum without extra work.

**The second key idea: multi-source BFS.** Rot spreads from *every* rotten orange at once. Rather than running a separate BFS per source and taking minimums, you **seed the queue with all of them**:

```
minute 0:  all initially rotten oranges
minute 1:  everything adjacent to any of them
minute 2:  everything adjacent to those
   …
```

Because they all start in the queue at level 0, BFS naturally expands them in lockstep — **simultaneous spread falls out of the algorithm for free**, with no per-source bookkeeping.

**Detecting the impossible case.** Count the fresh oranges up front and decrement as each rots. If any remain when the queue empties, they were unreachable → `-1`.

🤔 **Before you open the next section:** how does BFS know where one minute ends and the next begins, given the queue mixes cells from different levels as it grows?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Simulate minute by minute, rescanning the grid | Each minute, scan for rotten cells and rot neighbours | ⚠️ Correct but O(m·n) per minute → O((m·n)²) |
| DFS from each rotten orange | Track minimum time per cell | ❌ DFS doesn't give shortest distance without extra work |
| BFS from each source separately | Take the min over sources | ⚠️ Correct, O(sources · m·n) |
| **Multi-source BFS** | Seed all sources at level 0 | ✅ |

**The decision: multi-source [BFS](../algorithms/bfs.md), counting levels as minutes.**

Three mechanisms:

| Mechanism | Purpose |
|---|---|
| Seed the queue with **all** rotten oranges | Simultaneous spread, one pass |
| **Level-size snapshot** (`for _ in range(len(queue))`) | Separate minute k from minute k+1 |
| `fresh` counter | Detect unreachable oranges → `-1` |

**The level-size snapshot is the same idiom as [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md).** At the top of each round, the queue holds exactly the cells that rotted at the *previous* minute — so freezing `len(queue)` before the inner loop processes precisely that minute's oranges, even as newly-rotted ones are appended behind them.

> **A "level" in a tree becomes a "minute" here.** Same idiom, different meaning — and that's the generalization worth carrying: **in BFS, level number = distance from the source.**

**Why `while queue and fresh > 0`.** The `fresh > 0` guard is what makes the count correct. Without it, the loop would run one extra round after the last orange rots — processing the final level, finding nothing to infect, and still incrementing `minutes`. **The result would be off by one.**

**Why the grid is mutated instead of a `visited` set.** Setting `grid[r][c] = 2` marks the cell as rotten *and* as visited, since the neighbour check only looks for `== 1`. One assignment, two jobs, O(1) space — the same in-place marking as [Word Search](79-word-search.md), but **permanent** here rather than backtracked.

**Why counting fresh oranges beats re-scanning.** Checking "are any fresh left?" by scanning the grid would be O(m·n) per minute. A counter makes it O(1).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(grid)
cols = len(grid[0])
queue = deque()
fresh = 0
```

`deque` for O(1) `popleft` — a list's `pop(0)` is O(n) and would silently make the BFS quadratic.
→ [from-import](../syntax/from-import.md) · [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
for row in range(rows):
    for col in range(cols):
        if grid[row][col] == 2:
            queue.append((row, col))
        elif grid[row][col] == 1:
            fresh += 1
```

**One scan doing two jobs:** seed the queue with **every** initially rotten orange (that's the multi-source part), and count the fresh ones.

Seeding them all at once is what makes the spread simultaneous — they're all at "level 0" together.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [elif-else](../syntax/elif-else.md)

```python
minutes = 0
while queue and fresh > 0:
```

**Each iteration is one minute.**

⚠️ **The `fresh > 0` guard prevents an off-by-one.** Once no fresh oranges remain, the spread is over — continuing would process the final level, infect nothing, and still increment `minutes`.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    for _ in range(len(queue)):
        row, col = queue.popleft()
```

**The level-size snapshot** — captured *before* the loop, so it processes exactly the cells that rotted last minute, even as new ones are appended.

Without freezing the size, newly-rotted oranges would be consumed in the same round and minutes would collapse into one.
→ [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r = row + dr
            c = col + dc
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
```

Check the four neighbours. The chained comparison `0 <= r < rows` tests both bounds at once.

**`grid[r][c] == 1` does double duty** — it finds fresh oranges *and* excludes already-rotten ones (`2`) and empty cells (`0`), so no separate visited check is needed.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [nested-lists](../syntax/nested-lists.md)

```python
                grid[r][c] = 2
                fresh -= 1
                queue.append((r, c))
```

**Rot it, decrement the counter, enqueue it for next minute.**

Setting the cell to `2` immediately is what prevents it being enqueued twice — another rotten neighbour checking this cell will now see `2`, not `1`.
→ [set-operations](../syntax/set-operations.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    minutes += 1
```

**Increment after the whole level** — one minute has elapsed, and every orange adjacent to the previous level's rot has now turned.

```python
return minutes if fresh == 0 else -1
```

Fresh oranges remaining means they were unreachable from any rotten one → **`-1`**.

And an initially clean grid returns **0**: the `while` never runs because `fresh` is already 0. ✅
→ [ternary-expression](../syntax/ternary-expression.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])
        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh += 1

        minutes = 0
        while queue and fresh > 0:
            for _ in range(len(queue)):
                row, col = queue.popleft()

                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                        grid[r][c] = 2
                        fresh -= 1
                        queue.append((r, c))
            minutes += 1

        return minutes if fresh == 0 else -1
```

</details>

**Trace it** — the first example:

```
initial:     2  1  1        queue = [(0,0)]     fresh = 5
             1  1  0
             0  1  1
```

| Minute | Queue at start | Rots this round | Grid after | `fresh` |
|---|---|---|---|---|
| **1** | `[(0,0)]` | (0,1), (1,0) | `2 2 1 / 2 1 0 / 0 1 1` | 3 |
| **2** | `[(0,1),(1,0)]` | (0,2), (1,1) | `2 2 2 / 2 2 0 / 0 1 1` | 1 |
| **3** | `[(0,2),(1,1)]` | (2,1) | `2 2 2 / 2 2 0 / 0 2 1` | 1 → 0? |

Wait — at minute 3, (1,1)'s neighbour (2,1) rots, leaving `fresh = 1` (cell (2,2)).

| **4** | `[(2,1)]` | (2,2) | all rotten | **0** |

Loop exits (`fresh == 0`) → return **4** ✅

**And the impossible case:**

```
2  1  1        (2,0) is fresh but isolated —
0  1  1        surrounded by empty cells and the grid edge
1  0  1
```

The BFS rots everything reachable, the queue empties, but `fresh = 1` remains → **`-1`** ✅

**The `fresh > 0` guard in action:** after minute 4 rots the last orange, `fresh` is 0 and the loop exits immediately. Without the guard it would run once more — processing `[(2,2)]`, finding no fresh neighbours, and returning **5**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Step | Cost |
|---|---|
| Initial scan | O(m·n) — seed the queue and count fresh |
| BFS | each cell enters the queue **at most once** |
| Per cell | O(1) — four neighbour checks |

Since a cell is set to `2` the moment it's enqueued, no cell can be enqueued twice. Total: **O(m·n)**.

At 10 × 10 = 100 cells, trivially fast.

**⚠️ Only with a `deque`.** A list's `pop(0)` is O(n), making the whole BFS **O((m·n)²)** — the same trap as [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md).

**Versus the naive simulation:** rescanning the whole grid each minute is O(m·n) per minute, and there can be O(m·n) minutes → **O((m·n)²)**. BFS gets it in one pass because the queue tracks exactly which cells changed, rather than rediscovering them.

**Multi-source costs nothing extra.** Running a separate BFS per rotten orange would be O(sources · m·n); seeding them all at once is a single O(m·n) traversal. **That's the whole point of multi-source BFS** — many starting points, one pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)** for the queue in the worst case.

The queue holds one **level** at a time — the cells that rotted in the previous minute. In the worst case (an entire row or a fully rotten initial grid) that's O(m·n).

**No `visited` set is needed** — mutating `grid[r][c] = 2` marks the cell as both rotten and visited, since the neighbour test only accepts `1`. That's O(1) extra space.

⚠️ **It does mutate the input.** Acceptable here (the grid represents a changing state, so mutation is arguably the correct model), but worth flagging as an API consideration — the same trade as [Word Search](79-word-search.md) and [Number of Islands](200-number-of-islands.md)'s in-place variant.

**BFS versus DFS space, one more time:**

| | Holds | Worst case |
|---|---|---|
| **BFS** | one level (frontier) | O(m·n) on a wide grid |
| DFS | the recursion path | O(m·n) on a snake-shaped grid |

Neither dominates in general — but **DFS isn't an option here anyway**, because it can't produce shortest distances without additional machinery. **The requirement chose the algorithm**, and space is a secondary consideration.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The question asks for a *number of minutes*, which is a shortest-path question — so this has to be BFS rather than DFS, because BFS explores in order of distance and the level number *is* the minute count. Rot also spreads from every rotten orange simultaneously, so I seed the queue with all of them at once — multi-source BFS handles the simultaneity for free, since they're all at level zero together. I use the level-size snapshot to separate one minute from the next, exactly like level-order tree traversal. For the impossible case I count fresh oranges up front and decrement as they rot; if any remain when the queue empties they were unreachable, so I return −1. One detail: the loop condition includes `fresh > 0`, otherwise it runs an extra round after the last orange rots and the count is off by one. O(m·n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why BFS and not DFS?" | **The question.** BFS visits cells in order of distance, so the level count *is* the minimum time. DFS can reach a cell by a long path first. |
| "Why seed all rotten oranges at once?" | Rot spreads simultaneously. Multi-source BFS puts them all at level 0, so no per-source runs or minimums are needed. |
| "Why the `fresh > 0` in the loop condition?" | Without it, the loop processes one more level after the last orange rots and increments `minutes` — an off-by-one. |
| "How do you detect −1?" | Count fresh oranges initially, decrement on each rot. Any remainder was unreachable. |
| "Avoid mutating the grid." | Use a `visited` set of coordinates — O(m·n) extra space but non-destructive. |
| "What if rot spread diagonally too?" | Extend to 8 directions; nothing else changes. |
| "What if different oranges rotted at different rates?" | The uniform-cost assumption breaks — you'd need Dijkstra with a priority queue instead of a plain queue. |

**Traps:**

- **Using DFS.** It explores reachability, not distance — you'd get *a* time, not the minimum.
- **Omitting `fresh > 0`** from the loop condition — off by one on every non-trivial input.
- **Not snapshotting `len(queue)`** — minutes collapse together and the answer is far too small.
- **Using a list as a queue** — `pop(0)` is O(n), silently quadratic.
- **Forgetting the all-clean case** — `[[0,2]]` must return 0, which the `fresh > 0` guard handles.
- **Marking cells rotten when dequeued instead of when enqueued** — the same cell gets enqueued multiple times.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the level-size snapshot idiom) · [Walls and Gates](286-walls-and-gates.md) (multi-source BFS computing distances) · [Word Ladder](127-word-ladder.md) (BFS for a minimum number of steps) · [Number of Islands](200-number-of-islands.md) (grid traversal where DFS/BFS are interchangeable — the contrast) · [bfs](../algorithms/bfs.md).

</details>

---
