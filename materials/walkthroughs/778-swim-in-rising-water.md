# 778. Swim in Rising Water

**Hard** · [LeetCode](https://leetcode.com/problems/swim-in-rising-water/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an `n × n` grid where `grid[r][c]` is the elevation at that square. Rain falls: at time `t`, the water depth everywhere is `t`. You start at `(0, 0)` and want to reach `(n-1, n-1)`. You may swim from a square to any 4-directionally adjacent square **if both squares' elevations are at most `t`**, and swimming takes no time. Return the least time before you can reach the bottom-right square.

```
grid = [[0,2],[1,3]]                          →  3
        you can't leave (0,0) until t=2 (to reach elevation 2),
        and (1,1) itself is elevation 3, so t=3

grid = [[0,1,2,3,4],
        [24,23,22,21,5],
        [12,13,14,15,16],
        [11,17,18,19,20],
        [10,9,8,7,6]]                         →  16
```

**Constraints:** `n == grid.length == grid[i].length` · `1 <= n <= 50` · `0 <= grid[i][j] < n²` · every value in the grid is **unique**.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| grid, 4-directional moves | A **graph**. Cells are nodes, adjacency is edges. Standard grid-as-graph framing |
| "swimming takes **no time**" | The cost is **not** path length. Distance travelled is free — so this is not a normal shortest-path problem |
| "you can move if both elevations are `<= t`" | At time `t` the passable cells are exactly those with elevation ≤ `t`. So a whole *path* is usable at time `t` iff **every cell on it** is ≤ `t` |
| "the **least** time to reach the end" | Minimize `t`. And a path is available at time `t` = the **maximum elevation on that path** |
| put those together | **Minimize, over all paths, the maximum elevation on the path.** That's a *minimax path* — the bottleneck shortest path |
| elevations are unique, `0 .. n²−1` | The grid is a permutation. The answer is one of the grid values, and it is at least `max(grid[0][0], grid[n-1][n-1])` |
| `n <= 50` | 2500 cells. Almost anything reasonable fits |

The reframing in row 5 is the whole problem. Everything else follows.

Cost is usually **additive** — you sum edge weights. Here it's a **maximum**: a path's cost is its worst cell, and adding a cheap cell to a path doesn't change the cost at all. That single change is what makes this a Hard.

🤔 **Before you open the next section:** Dijkstra's works by keeping a running total and adding each edge's weight to it. If a path's cost were the *maximum* of its cells rather than the sum, what would you change in Dijkstra's? Would the greedy still be valid?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| DFS every path, take min of maxes | Enumerate all routes | exponential | O(n²) | ❌ |
| Plain BFS | Fewest cells to the end | O(n²) | O(n²) | ❌ Minimizes path *length*, and length is explicitly free here |
| **Binary search + flood fill** | Guess `t`, DFS using only cells ≤ `t`, check if the end is reachable; binary search on `t` over `0 .. n²−1` | O(n² log n) | O(n²) | ✅ Also correct, and very natural |
| [Union-find](../data-structures/union-find.md) | Add cells in elevation order, union with already-added neighbours; the answer is when `(0,0)` and `(n-1,n-1)` connect | O(n² α) | O(n²) | ✅ Fastest, and elegant given unique values |
| **Modified Dijkstra's** | Min-heap keyed on *max elevation seen so far* instead of a running sum | O(n² log n) | O(n²) | ✅ |

**The decision:** modified [Dijkstra's](../algorithms/dijkstra.md) — a min-heap where the key is `max(cost_so_far, next_cell)` rather than `cost_so_far + weight`.

**Why the greedy still works.** Dijkstra's correctness needs one property: **extending a path can never make it cheaper.** For sums, that's true because weights are non-negative. For maximums, it's true for a stronger reason — `max(a, b) >= a` *always*, for any values at all. So the finalize-on-pop guarantee holds just as firmly. You're swapping the combining operator, and the proof survives intact.

This is worth saying explicitly in an interview: *"Dijkstra's isn't really about addition — it works for any path-cost function that's monotonically non-decreasing as you extend the path. Max is one of those."* That's the observation that turns a Hard into a two-line edit of a template you already know.

**Why not binary search + flood fill?** It's genuinely a fine answer, and arguably easier to *invent* under pressure — "I can check a fixed `t` easily, so I'll binary search the answer." Same complexity. The Dijkstra version wins on being a single pass with no outer loop, and it directly *computes* the answer rather than testing candidates. Mention both; write one.

**Why not union-find?** Because unique elevations mean you can add cells in sorted order and stop when the corners connect — O(n² α(n²)), the best bound of the three. It's the most elegant answer here, but it leans on the uniqueness guarantee, and the heap version generalizes to any minimax-path problem.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
```
The min-heap that always hands back the reachable cell with the smallest path-maximum.
→ [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
n = len(grid)
visited = set()
min_heap = [(grid[0][0], 0, 0)]   # (max elevation on path so far, row, col)
```
The heap entry is a 3-tuple with the cost **first**, so tuple comparison orders by cost. Seeding with `grid[0][0]` encodes the fact that you can't even be standing on the start square until the water reaches its elevation — which is why example 1 answers 3 and not 2.

`visited` is the finalized set: a cell in it has its optimal path-maximum already determined.
→ [set-basics](../syntax/set-basics.md) · [tuple-basics](../syntax/tuple-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
while min_heap:
    time, row, col = heapq.heappop(min_heap)
    if (row, col) in visited:
        continue
    visited.add((row, col))
```
Pop the globally best cell and finalize it. Same **lazy deletion** as ordinary Dijkstra's: a cell gets pushed once per neighbour that reaches it, and only the first (cheapest) pop counts — the rest are skipped.

Coordinates go into the set as a `(row, col)` tuple, since tuples are hashable and lists aren't.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [break-continue](../syntax/break-continue.md)

```python
    if row == n - 1 and col == n - 1:
        return time
```
**Early exit**, and it's safe *because* of the finalize-on-pop guarantee. The moment the destination is popped, its cost is optimal — no later route can beat it. Checking on pop rather than on push is what makes this correct; on push it would be a guess.
→ [if-return](../syntax/if-return.md) · [logical-operators](../syntax/logical-operators.md)

```python
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r = row + dr
        c = col + dc
```
The four-direction sweep — the standard grid-traversal idiom. Encoding the moves as offset pairs beats four copy-pasted blocks.
→ [for-loop](../syntax/for-loop.md) · [list-basics](../syntax/list-basics.md)

```python
        if 0 <= r < n and 0 <= c < n and (r, c) not in visited:
            heapq.heappush(min_heap, (max(time, grid[r][c]), r, c))
```
Bounds check, then **relaxation** — and `max(time, grid[r][c])` is the entire adaptation. Ordinary Dijkstra's would write `time + weight`; here the cost of extending a path to a new cell is the worse of *what you've already had to survive* and *this new cell's elevation*.

Note what this means: stepping onto a **low** cell costs nothing at all. The running cost only rises when you're forced over a new high point. That's exactly the physics of the problem.

The [chained comparison](../syntax/chained-comparisons.md) `0 <= r < n` is the Pythonic bounds check.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [min-max-key](../syntax/min-max-key.md) · [membership-operators](../syntax/membership-operators.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:

        n = len(grid)
        visited = set()
        min_heap = [(grid[0][0], 0, 0)]   # (max elevation on path so far, row, col)

        while min_heap:
            time, row, col = heapq.heappop(min_heap)
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if row == n - 1 and col == n - 1:
                return time

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < n and 0 <= c < n and (r, c) not in visited:
                    heapq.heappush(min_heap, (max(time, grid[r][c]), r, c))
```
</details>

**Trace it** — `grid = [[0,2],[1,3]]`

| Pop | Stale? | `visited` | At end? | Pushed |
|---|---|---|---|---|
| `(0, 0,0)` | no | `{(0,0)}` | no | `(max(0,1)=1, 1,0)`, `(max(0,2)=2, 0,1)` |
| `(1, 1,0)` | no | `+(1,0)` | no | `(max(1,3)=3, 1,1)` |
| `(2, 0,1)` | no | `+(0,1)` | no | `(max(2,3)=3, 1,1)` |
| `(3, 1,1)` | no | `+(1,1)` | **yes** → return **3** | |

**3** ✅

Look at rows 2 and 3: cell `(1,1)` was pushed twice, at cost 3 both times — via `(1,0)` and via `(0,1)`. Both routes are dominated by the destination's own elevation of 3, and neither could do better. The second copy would have been discarded by the `continue` had the first not returned already.

And notice the first pop cost **0**, not 3 — you begin at the start cell for free-ish, and the cost only ratchets up as you're forced across higher ground.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n² log n)</summary>

**O(n² log n)** for an n × n grid.

- There are **n² cells**, and each is finalized at most once.
- Each finalized cell pushes at most 4 neighbours → at most **4n² pushes** overall, i.e. O(n²) heap entries.
- Each push and pop costs O(log(heap size)) = O(log n²) = O(2 log n) = **O(log n)**.
- O(n²) operations × O(log n) = **O(n² log n)**.

If you prefer the graph form: V = n², E = 4n², so O(E log V) = O(n² log n²) — same thing.

At n = 50 that's 2500 × ~11 ≈ 3 × 10⁴ operations. Trivial.

**Comparing the three approaches** at this size, all pass, but the bounds differ:
- Binary search + flood fill: **O(n² log n)** — log n² guesses, each an O(n²) flood fill.
- Modified Dijkstra's: **O(n² log n)**.
- Union-find in sorted elevation order: **O(n² α(n²))** ≈ O(n²) — the best, exploiting unique values.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²)</summary>

**O(n²).**

- `visited` holds at most one entry per cell → O(n²).
- `min_heap` holds up to 4 entries per cell before lazy deletion clears them → O(n²).
- `n`, `time`, `row`, `col`, the direction list → O(1).

Total O(n²), which for a grid problem is the floor: you can't track visited cells in less than one bit per cell.

**Can you do better?** Slightly — instead of a `visited` set of tuples you could mutate the grid in place (mark a visited cell as `-1`). Same asymptotic class, meaningfully smaller constant, but it destroys the input. Worth offering, not worth doing unprompted.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Swimming is free, so path length doesn't matter — what matters is the highest cell I'm forced to cross. A path is usable at time t exactly when its maximum elevation is ≤ t, so I want to minimize the maximum elevation over all paths. That's a minimax path problem. It's Dijkstra's with one change: instead of the heap key being `cost + weight` it's `max(cost, next_cell)`. The greedy still holds, because Dijkstra's really only needs that extending a path can't make it cheaper — and `max(a,b) >= a` always. Pop the destination and its cost is final, so I return immediately. O(n² log n) time, O(n²) space. Binary searching t with a flood fill is the same complexity, and union-find adding cells in elevation order is O(n² α) — the best of the three, since the values are unique."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it with binary search." | Binary search `t` over `0 .. n²−1`. For each guess, DFS/BFS from `(0,0)` using only cells with elevation ≤ `t`, and test whether the end is reachable. Reachability is monotone in `t`, which is what makes binary search valid. O(n² log n). |
| "Solve it with union-find." | Sort cells by elevation (or bucket them, since values are a permutation of `0..n²−1`). Add them one at a time, unioning each with already-added neighbours. The answer is the elevation at which `(0,0)` and `(n-1,n-1)` first share a root. O(n² α). |
| "Why can you return on pop but not on push?" | On push the value is a candidate; a cheaper route may still be pending in the heap. On pop it's finalized, because everything remaining costs at least as much and extending only ever raises the max. |
| "What if swimming *did* take time?" | Then cost is a mix of hops and elevation, and you'd need a combined key — or a multi-objective formulation. The pure minimax trick no longer applies. |
| "8-directional movement?" | Add the four diagonals to the direction list. Nothing else changes. |
| "Why does this work but plain BFS doesn't?" | BFS's queue orders by insertion, which encodes hop count. Here hop count is irrelevant, so you need an explicit priority — the heap. |
| "What if elevations weren't unique?" | The Dijkstra and binary-search versions are unaffected. Union-find needs a tweak: process all cells of equal elevation together before testing connectivity. |

**Traps:**
- **`time + grid[r][c]` instead of `max(...)`.** The single most likely bug — it silently solves a different (additive) problem and gives plausible-looking wrong answers.
- Seeding the heap with `(0, 0, 0)` instead of `(grid[0][0], 0, 0)`. Fails example 1 whenever the start cell isn't the grid's minimum.
- Checking for the destination on **push** rather than pop — returns the first route found, not the best.
- Omitting the `if (row, col) in visited: continue` — a stale entry re-finalizes a cell at a worse cost.
- Adding to `visited` at push time instead of pop time. That's correct for BFS and **wrong** for Dijkstra's, because it locks in the first cost seen rather than the smallest.
- Forgetting that the destination's own elevation counts. `max()` handles it automatically, which is easy to under-appreciate.

**This same move shows up in:** [Network Delay Time](743-network-delay-time.md) (the same heap skeleton with the standard additive key) · [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md) (same skeleton again, key is the raw edge weight) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary searching the *answer* on a monotone feasibility test — the alternative solution here) · [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (grid traversal driven by elevation comparisons).

</details>

---
