# 286. Walls and Gates

**Medium** · [LeetCode](https://leetcode.com/problems/walls-and-gates/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an `m × n` grid `rooms` initialized with three possible values:

- **`-1`** — a wall or obstacle
- **`0`** — a **gate**
- **`INF`** (`2147483647`, i.e. 2³¹−1) — an **empty room**

Fill each empty room with **the distance to its nearest gate**. If it's impossible to reach a gate, leave it as `INF`. Modify the grid **in place**.

```
before:                       after:

INF  -1   0  INF               3  -1   0   1
INF INF INF  -1                2   2   1  -1
INF  -1 INF  -1                1  -1   2  -1
  0  -1 INF INF                0  -1   3   4
```

**Constraints:** `1 <= m, n <= 250` · cells are `-1`, `0`, or `2147483647`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**distance** to its nearest gate" | ⚠️ A **shortest-path** question → BFS, not DFS |
| "**nearest** gate" | Multiple gates; each room wants the closest one |
| "leave as INF if unreachable" | Walls can seal off regions — no special handling if you only ever *overwrite* INF cells |
| "modify **in place**" | Mutate `rooms`; return nothing |
| 250 × 250 = 62,500 cells | O(m·n) expected; a per-room search would be far too slow |

**The naive approach and why it's too slow.** For each empty room, BFS outward until you hit a gate. That's O(m·n) per room across O(m·n) rooms → **O((m·n)²)** ≈ 3.9 × 10⁹.

**The inversion: search from the gates, not the rooms.** Instead of asking each room *"where's my nearest gate?"*, ask each gate *"which rooms are nearest to me?"* — and run **all gates at once**.

This is **multi-source BFS**, exactly as in [Rotting Oranges](994-rotting-oranges.md):

```
level 0:  every gate
level 1:  every room adjacent to any gate        → distance 1
level 2:  every room adjacent to those           → distance 2
   …
```

**Why this gives each room its *nearest* gate for free.** BFS expands in order of distance from the source set. So the **first** time a room is reached, it's via the shortest path from *some* gate — and since all gates started at level 0, that's the nearest one.

> **The first visit is the shortest visit.** That's the defining property of BFS, and it's why no comparison against a previous distance is ever needed.

**Why unreachable rooms need no special case.** They're never dequeued, so they're never overwritten — and they keep their initial `INF`. **The absence of a visit is the answer**, the same trick as [Surrounded Regions](130-surrounded-regions.md).

🤔 **Before you open the next section:** what serves as the `visited` marker here, given that the grid is being filled with distances anyway?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| BFS from each empty room | Search outward until a gate is found | **O((m·n)²)** | ❌ 3.9 × 10⁹ |
| BFS from each gate separately | Take the minimum per room | O(gates · m·n) | ⚠️ Correct; redundant when gates are many |
| DFS from each gate | Propagate distances recursively | O(m·n) but with rework | ⚠️ Needs re-visiting when a shorter path appears |
| **Multi-source BFS from all gates** | One traversal, all gates at level 0 | **O(m·n)** | ✅ |

**The decision: multi-source [BFS](../algorithms/bfs.md), seeded with every gate.**

Two mechanisms:

| Mechanism | Purpose |
|---|---|
| Seed the queue with **all** gates | Every room's nearest gate is found in one pass |
| Overwrite `INF` with `parent + 1` | Records the distance **and** marks the cell visited |

**Why `rooms[r][c] == INF` is the entire visited check.** Once a room is assigned a distance, it's no longer `INF` — so the test rejects walls (`-1`), gates (`0`), and already-assigned rooms in a single comparison. **No separate `visited` set, O(1) space**, the same in-place marking as [Rotting Oranges](994-rotting-oranges.md).

**Why DFS is the wrong choice.** DFS explores depth-first, so it can reach a room by a long path first and would need to *revisit* it whenever a shorter route appears — turning into a repeated-relaxation algorithm. BFS's distance-ordered expansion means **the first assignment is final**.

**Why no level-size snapshot is needed here.** [Rotting Oranges](994-rotting-oranges.md) counted elapsed minutes, so it had to separate one level from the next. Here each cell **carries its own distance** in the grid — `rooms[row][col] + 1` — so the level structure is implicit in the values. Simpler code for the same traversal.

> **Store the distance in the node, and you don't need to track levels.** Worth remembering: it's the general alternative to the snapshot idiom.

**Why unweighted BFS suffices.** Every step costs exactly 1. If moves had varying costs you'd need **Dijkstra** with a priority queue instead — see [Network Delay Time](743-network-delay-time.md) in Unit 12.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(rooms)
cols = len(rooms[0])
queue = deque()
```

`deque` for O(1) `popleft` — a list's `pop(0)` is O(n) and would silently make the BFS quadratic.
→ [from-import](../syntax/from-import.md) · [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
for row in range(rows):
    for col in range(cols):
        if rooms[row][col] == 0:
            queue.append((row, col))
```

**Seed the queue with every gate.** All of them start at level 0 together — that's what makes each room find its *nearest* gate rather than an arbitrary one.

Gates already hold `0`, which is correctly their own distance, so nothing needs initializing.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
empty = 2147483647
```

Naming the magic constant. It's 2³¹−1, the maximum 32-bit signed integer — used as "infinity" because the problem guarantees real distances stay far below it.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while queue:
    row, col = queue.popleft()
```

Standard BFS. **No level-size snapshot** — each cell already carries its distance in the grid, so levels don't need separating.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r = row + dr
        c = col + dc
        if 0 <= r < rows and 0 <= c < cols and rooms[r][c] == empty:
```

The four-neighbour check, with `0 <= r < rows` testing both bounds at once.

**`rooms[r][c] == empty` does three jobs:** it skips walls (`-1`), skips gates and already-assigned rooms (any smaller value), and serves as the visited check. **One comparison, no auxiliary structure.**
→ [chained-comparisons](../syntax/chained-comparisons.md) · [nested-lists](../syntax/nested-lists.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
            rooms[r][c] = rooms[row][col] + 1
            queue.append((r, c))
```

**Assign and enqueue.** The neighbour is one step further from the gate than the current cell, so its distance is `current + 1`.

Writing the value **immediately** — rather than when the cell is later dequeued — is what prevents it being enqueued twice: any other neighbour checking this cell now sees a real distance, not `INF`.

**And because BFS reaches it first by the shortest route, this assignment is final** — no comparison against a previous value is needed.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:

        rows = len(rooms)
        cols = len(rooms[0])
        queue = deque()

        for row in range(rows):
            for col in range(cols):
                if rooms[row][col] == 0:
                    queue.append((row, col))

        empty = 2147483647

        while queue:
            row, col = queue.popleft()

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and rooms[r][c] == empty:
                    rooms[r][c] = rooms[row][col] + 1
                    queue.append((r, c))
```

</details>

**Trace it** — the example grid (`∞` = INF, `#` = wall):

```
initial:    ∞  #  0  ∞         gates at (0,2) and (3,0)
            ∞  ∞  ∞  #
            ∞  #  ∞  #
            0  #  ∞  ∞
```

| Round | Dequeued | Assigns | Grid state |
|---|---|---|---|
| seed | — | — | queue = `[(0,2), (3,0)]` |
| 1 | (0,2)=0 | (0,3)=**1**, (1,2)=**1** | |
| 2 | (3,0)=0 | (2,0)=**1** | |
| 3 | (0,3)=1 | — ((1,3) is a wall) | |
| 4 | (1,2)=1 | (1,1)=**2**, (2,2)=**2** | |
| 5 | (2,0)=1 | (1,0)=**2** | |
| 6 | (1,1)=2 | (1,0) already 2 — skipped | |
| 7 | (2,2)=2 | (3,2)=**3** | |
| 8 | (1,0)=2 | (0,0)=**3** | |
| 9 | (3,2)=3 | (3,3)=**4** | |

Final:
```
   3  #  0  1
   2  2  1  #
   1  #  2  #
   0  #  3  4      ✅
```

**Two things worth noting:**

- **(1,0) was reached at distance 2 from the bottom gate** (round 5) before (1,1) could offer it at distance 3 (round 6). BFS's distance-ordered expansion guaranteed the shorter route won, with no comparison needed.
- **Cell (0,0) got 3**, correctly measuring around the wall at (0,1) rather than through it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Step | Cost |
|---|---|
| Scan for gates | O(m·n) |
| BFS | each cell enqueued **at most once** |
| Per cell | O(1) — four neighbour checks |

A cell is assigned a distance the moment it's enqueued, so it can never be enqueued again. Total: **O(m·n)**.

At 250 × 250 = 62,500 cells, ~250,000 operations. Instant.

**Versus BFS from each empty room: O((m·n)²)** ≈ 3.9 × 10⁹ — completely impractical. **Reversing the direction turns 62,500 searches into one.**

**Versus BFS from each gate separately:** O(gates · m·n), plus you'd have to take minimums. Multi-source does it in a single pass because all gates share the same expanding frontier.

**⚠️ Only with a `deque`.** A list's `pop(0)` is O(n), making the BFS **O((m·n)²)** — the same trap as [Rotting Oranges](994-rotting-oranges.md) and [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md).

**Optimal** — every cell must be examined at least once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)** for the queue in the worst case.

The queue holds the current frontier — the cells at the same distance from the nearest gate. On a wide open grid that can approach O(m·n).

**No `visited` set is needed**, which is the space win: the distance written into `rooms[r][c]` marks the cell as visited, since it's no longer `INF`. **O(1) extra**, versus O(m·n) for a separate structure.

⚠️ **It mutates the input** — but that's exactly what the problem asks for ("modify in place"), so it's the intended design rather than a compromise.

**BFS versus DFS space here** doesn't arise, because **DFS isn't a valid choice** — it can't guarantee shortest distances without repeated relaxation. **The requirement picked the algorithm**, and space is secondary.

**Compared with [Rotting Oranges](994-rotting-oranges.md):** that problem needed an extra `fresh` counter to detect unreachable cells. Here unreachable rooms simply keep their `INF`, so **no counter is required** — the sentinel value doubles as the "not reached" marker.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Searching outward from each empty room is O((m·n)²) — far too slow. So I invert it: instead of each room looking for its nearest gate, I search from the gates and let the distances spread out. I seed a BFS queue with *every* gate at once, which is what makes each room find its nearest one — BFS expands in order of distance, so the first time a room is reached is via the shortest path from the closest gate, and that assignment is final with no comparison needed. I write the distance directly into the grid, which also serves as the visited marker since the cell is no longer INF. Unreachable rooms are never dequeued, so they keep their INF automatically. O(m·n) time, O(m·n) for the queue. DFS wouldn't work here — it can reach a room by a long path first and would need repeated relaxation."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why BFS from the gates, not from the rooms?" | **The question.** Many rooms, few gates — searching from the gates is one traversal instead of m·n. |
| "Why does the first visit give the *shortest* distance?" | BFS expands in distance order, and all gates start at level 0, so the first arrival is via the nearest gate. |
| "Why is no `visited` set needed?" | An assigned room is no longer `INF`, so the `== INF` check rejects walls, gates, and visited rooms at once. |
| "Why not DFS?" | DFS can reach a cell by a long path first, requiring revisits when shorter ones appear. BFS's first assignment is final. |
| "What if moves had different costs?" | BFS assumes uniform cost. Use **Dijkstra** with a priority queue — see [Network Delay Time](743-network-delay-time.md). |
| "How does this differ from [Rotting Oranges](994-rotting-oranges.md)?" | Same multi-source BFS. There you count *elapsed levels*, so you snapshot the queue size; here each cell stores its own distance, so levels are implicit. |
| "What if you couldn't modify the grid?" | Keep a separate `dist` matrix and a `visited` set — O(m·n) extra space. |

**Traps:**

- **BFS from each room** — correct but O((m·n)²).
- **Using DFS** — produces *a* distance, not the minimum, without extra relaxation logic.
- **Assigning the distance when a cell is dequeued** rather than enqueued — the cell gets enqueued multiple times.
- **Using a list as the queue** — `pop(0)` is O(n), silently quadratic.
- **Adding a level-size snapshot** — harmless but unnecessary, since distances are stored per cell.
- **Overwriting walls or gates** — the `== INF` check must be exact; `!= -1` would clobber gates.

**This same move shows up in:** [Rotting Oranges](994-rotting-oranges.md) (multi-source BFS with explicit level counting) · [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (searching inward from the boundary) · [Word Ladder](127-word-ladder.md) (BFS for a shortest path) · [Network Delay Time](743-network-delay-time.md) (Dijkstra, when edges have weights) · [bfs](../algorithms/bfs.md).

</details>
