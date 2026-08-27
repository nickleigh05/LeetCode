# 329. Longest Increasing Path in a Matrix

**Hard** · [LeetCode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` integers `matrix`, return the length of the **longest strictly increasing path**. From each cell you may move in **four directions** — left, right, up, down — but **not diagonally** and not outside the grid.

```
matrix = [[9,9,4],
          [6,6,8],
          [2,1,1]]        →  4      the path 1 → 2 → 6 → 9

matrix = [[3,4,5],
          [3,2,6],
          [2,2,1]]        →  4      the path 3 → 4 → 5 → 6  (no diagonals allowed)

matrix = [[1]]            →  1
```

**Constraints:** `1 <= m, n <= 200` · `0 <= matrix[i][j] <= 2³¹−1`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| a grid with 4-directional moves | A **graph**. Cells are nodes, adjacency is edges — the standard grid-as-graph framing from [Number of Islands](200-number-of-islands.md) |
| "**strictly increasing**" | The constraint that changes everything. You may only move to a **strictly greater** value — so every edge points "uphill" |
| "**longest** path" | Optimization, `max`. And longest-path is normally **NP-hard** on a general graph, which should make you look hard at what makes this one tractable |
| no starting point given | The path may begin anywhere, so you have to consider all m·n starting cells |
| `m, n <= 200` | 40,000 cells. O(m·n) or O(m·n log(m·n)) is fine; exponential is not |

The critical realization is in row 3. **Longest path in a general graph is NP-hard** — because a path can wander, revisit regions, and you must avoid cycles explicitly with a visited set. So why is this problem merely Hard rather than impossible?

**Because "strictly increasing" makes the graph a DAG.** Every edge goes from a smaller value to a strictly larger one. You can never return to a cell you've left, because that would require the values to both increase and decrease around a loop. **There are no cycles, by construction.**

That has two immediate consequences worth stating explicitly:

1. **No visited set is needed.** Unlike [Word Search](79-word-search.md), where you must mark and unmark cells during backtracking, here the increasing constraint makes revisiting impossible. That's a real simplification.
2. **Longest path on a DAG is polynomial.** It's a straightforward DP.

Now the state. Define:

> `longest(r, c)` = the length of the longest increasing path **starting at** cell `(r, c)`.

Then from that cell you may step to any neighbour with a strictly larger value, and:

```
longest(r, c) = 1 + max( longest(neighbour) for each strictly-greater neighbour )
```

with `longest(r, c) = 1` when no neighbour is larger — the cell alone is a path of length 1. The answer is the max over all cells.

🤔 **Before you open the next section:** a plain DFS from every cell would explore the same sub-paths over and over — the cell containing `6` in example 1 is reached from several places. Does `longest(6's cell)` depend at all on how you arrived there? If not, what should you do about it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| DFS from every cell, no caching | Explore every increasing path from every start | **exponential** | O(m·n) | ❌ The same sub-paths are re-explored from every ancestor |
| Backtracking with a visited set | Mark and unmark cells as you go | exponential | O(m·n) | ❌ Correct but pointless — the visited set isn't even needed, and it doesn't fix the recomputation |
| **DFS + memoization** | Cache `longest(r, c)` the first time it's computed | O(m·n) | O(m·n) | ✅ |
| Topological sort (Kahn's) on the DAG | Peel off cells with no larger neighbours, layer by layer | O(m·n) | O(m·n) | ✅ Iterative, no recursion depth risk |
| Sort cells by value, DP in order | Process ascending; every larger neighbour is already done | O(m·n log(m·n)) | O(m·n) | ✅ Also correct, slightly slower due to the sort |

**The decision:** **DFS with memoization** — the recursion written directly, with a cache.

**Why memoization is the whole problem.** `longest(r, c)` depends *only* on the cell's coordinates — never on the path taken to reach it. That's the answer to section 1's question, and it's the precondition for caching. In example 1, the cell holding `6` is a neighbour of several cells, and every one of them would recompute its entire downstream path. With the cache, each cell's answer is computed **once** and read thereafter.

That collapses an exponential exploration into **O(m·n)**: there are m·n states and each does O(4) work. **The number of paths is exponential; the number of states is m·n.** Same collapse as [Target Sum](494-target-sum.md) and [Longest Common Subsequence](1143-longest-common-subsequence.md).

**Why no visited set** — worth repeating because it's the detail people get wrong by reflex. Strict increase forbids cycles, so a DFS can't loop. Adding backtracking machinery (mark on entry, unmark on exit) would be harmless but unnecessary, and it would also **break the memoization** — a cached value computed while some cells were marked visited wouldn't be reusable. **The two techniques are incompatible, and here you want the cache.**

**Why "longest starting here" rather than "longest ending here"?** Either works. "Starting here" pairs naturally with a top-down DFS that recurses into larger neighbours. "Ending here" pairs with a bottom-up sweep in ascending value order. The recursive framing is easier to derive under pressure.

**Why mention the topological-sort variant?** Because with 200 × 200 = 40,000 cells, a monotone staircase gives a recursion **40,000 frames deep** — far past Python's default limit of 1000. Kahn's algorithm on the DAG (repeatedly remove cells whose larger-neighbour count is zero, counting layers) is the same complexity with no stack. It's the genuinely more robust answer, and naming it shows you've thought about the failure mode rather than just the happy path.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(matrix)
cols = len(matrix[0])
memo = {}
```
Dimensions, and the cache keyed on `(row, col)`. `memo[(r, c)]` will hold the length of the longest increasing path starting at that cell — a value that never changes once computed, because it doesn't depend on how the cell was reached.
→ [nested-lists](../syntax/nested-lists.md) · [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dfs(row, col):
    if (row, col) in memo:
        return memo[(row, col)]
```
The cache check, and it's the first thing in the function. This single line is what turns exponential into linear — every cell after the first visit returns immediately.

Note there's **no visited-set check** here. That's deliberate: the strictly-increasing rule makes cycles impossible, so nothing else is needed to guarantee termination.
→ [membership-operators](../syntax/membership-operators.md) · [tuple-basics](../syntax/tuple-basics.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    best = 1
```
**The base case, folded into the initialization.** A single cell is itself a path of length 1, so that's the floor. If no neighbour is larger, this value survives unchanged and the recursion bottoms out naturally.

Starting at 1 rather than 0 is what makes the `1 + dfs(...)` arithmetic below come out right, and it removes the need for a separate "dead end" branch.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r = row + dr
        c = col + dc
```
The four-direction sweep, the same offset-pair idiom used throughout the grid problems in [Unit 11](../rmap-practice/11-graphs.md). Only these four — the problem explicitly excludes diagonals, which is what makes example 2's answer 4 rather than longer.
→ [for-loop](../syntax/for-loop.md) · [list-basics](../syntax/list-basics.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
        if 0 <= r < rows and 0 <= c < cols and matrix[r][c] > matrix[row][col]:
            best = max(best, 1 + dfs(r, c))
```
**The recurrence.** Three conditions, [short-circuiting](../syntax/logical-operators.md) in order: in bounds vertically, in bounds horizontally, and — the heart of it — the neighbour's value is **strictly greater**.

The bounds checks must come first; otherwise `matrix[r][c]` raises `IndexError`, or worse, Python's negative indexing silently reads a cell from the opposite edge and produces a wrong answer rather than a crash.

`>` and not `>=` is what "strictly increasing" means, and it's also what guarantees no cycles. Change it to `>=` and equal-valued neighbours form 2-cycles — the recursion never terminates.

`1 + dfs(r, c)` is "step onto the neighbour, then continue optimally from there," and the `max` keeps the best of the (up to four) directions.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [logical-operators](../syntax/logical-operators.md) · [min-max-key](../syntax/min-max-key.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
    memo[(row, col)] = best
    return best
```
Cache before returning. Every later query for this cell — from any of its smaller neighbours, or from the top-level sweep — is now O(1).
→ [dict-basics](../syntax/dict-basics.md)

```python
return max(dfs(row, col) for row in range(rows) for col in range(cols))
```
**Try every cell as a starting point** and take the best.

A nested [generator expression](../syntax/generator-expressions.md) — the doubled `for` reads as two nested loops — evaluated lazily so no intermediate list of 40,000 values is built.

This sweep looks like it should cost m·n full DFS traversals, but it doesn't: the **first** call populates a large part of the cache, and later calls mostly hit it. Total work stays O(m·n).
→ [generator-expressions](../syntax/generator-expressions.md) · [min-max-key](../syntax/min-max-key.md) · [range-function](../syntax/range-function.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        rows = len(matrix)
        cols = len(matrix[0])
        memo = {}

        def dfs(row, col):
            if (row, col) in memo:
                return memo[(row, col)]

            best = 1
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and matrix[r][c] > matrix[row][col]:
                    best = max(best, 1 + dfs(r, c))

            memo[(row, col)] = best
            return best

        return max(dfs(row, col) for row in range(rows) for col in range(cols))
```
</details>

**Trace it** — example 1:

```
9 9 4
6 6 8
2 1 1
```

Computing `longest(r, c)` for each cell — the length of the longest increasing path starting there. Listed in dependency order, largest values first, since a cell depends only on strictly larger neighbours:

| cell | value | larger neighbours | computation | `longest` |
|---|---|---|---|---|
| `(0,0)` | 9 | — | base | **1** |
| `(0,1)` | 9 | — | base | **1** |
| `(1,2)` | 8 | — (4 above is smaller, 6 left is smaller, 1 below is smaller) | base | **1** |
| `(0,2)` | 4 | `(1,2)`=8 | 1 + 1 | **2** |
| `(1,0)` | 6 | `(0,0)`=9 | 1 + 1 | **2** |
| `(1,1)` | 6 | `(0,1)`=9, `(1,2)`=8 | 1 + max(1, 1) | **2** |
| `(2,0)` | 2 | `(1,0)`=6 | 1 + 2 | **3** |
| `(2,1)` | 1 | `(1,1)`=6, `(2,0)`=2 | 1 + max(2, 3) | **4** |
| `(2,2)` | 1 | `(1,2)`=8 | 1 + 1 | **2** |

Answer: `max(...)` = **4** ✅ — the path `1 → 2 → 6 → 9`, starting at `(2,1)`.

The memoization is visible at `(2,1)`: it queries `(2,0)`, whose value of 3 was itself built from `(1,0)`, which was built from `(0,0)`. Without the cache, computing `(2,1)` would re-walk that entire chain, and so would every other cell that reaches it. With the cache, each of the nine cells is computed exactly once.

Note also that **no visited set appears anywhere** in the trace, and none is needed — every arrow points from a smaller value to a larger one, so there is no way back.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

Using **states × work per state**:

- **States:** one per cell → **m · n**.
- **Work per state:** check four neighbours, each O(1) after the recursive call is either cached or computed → **O(4) = O(1)**.
- Total: **O(m · n)**.

At the limits, 200 × 200 = **40,000** cells with four checks each — about 1.6 × 10⁵ operations. Fast.

**The subtle part** is why the outer sweep over all m·n starting cells doesn't multiply the cost. Each `dfs` call either returns instantly from the cache, or computes a cell for the first time — and a first-time computation can happen only m·n times in total, across the entire run. So the sweep is O(m·n) *including* all the recursion it triggers, not O(m·n) per start.

**Against the alternatives:** uncached DFS is exponential, because each cell re-explores every path descending from it, once per ancestor that reaches it. The number of increasing paths in a matrix can be enormous; the number of *cells* is 40,000. **Many paths, few states.**

**The value-sorting variant** is O(m·n log(m·n)) — the sort dominates. Slightly worse, and it exists mainly as a way to get an iterative solution. **Kahn's topological sort** matches O(m·n) with no sort and no recursion, which makes it the best of the three on paper.

**Faster?** No. Every cell can affect the answer, so **Ω(m·n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)**, from two sources:

- The **memo** holds one entry per cell → O(m·n), up to 40,000 entries.
- The **recursion stack** can nest once per cell along a single increasing path → up to **O(m·n)** frames in the worst case.

**The recursion depth is a genuine risk here**, not a theoretical one. A matrix laid out as a monotone snake — values increasing along a path that visits every cell — gives a chain of 40,000 nested calls, forty times past Python's default [recursion limit](../syntax/recursion-limit.md) of 1000. LeetCode's harness usually raises the limit, but **this is a real weakness of the recursive solution** and exactly the kind of thing to raise yourself rather than have pointed out.

| Version | Space | Recursion depth | Notes |
|---|---|---|---|
| **DFS + memo** | **O(m·n)** | up to O(m·n) | Simplest to derive; depth risk |
| Topological sort (Kahn's) | **O(m·n)** | none | Same time bound, iterative — the robust choice |
| Sort by value, DP ascending | **O(m·n)** | none | Iterative, but O(m·n log(m·n)) from the sort |

**Why this can't collapse the way [Unique Paths](62-unique-paths.md) did.** There, `dp[r][c]` read only the previous row, so one row sufficed. Here a cell can depend on **any** of its four neighbours — including the one *below* it — so dependencies flow in every direction, not monotonically down the grid. **There's no sweep order that makes a rolling row valid**, and the full table is genuinely needed.

The fix, if space mattered, is to store the memo in a preallocated 2-D list of ints rather than a dict of tuples — same O(m·n), meaningfully smaller constant.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Longest path is NP-hard in general, so the first thing to notice is why this one isn't: because every move must go to a strictly greater value, the graph is a DAG — you can never return to a cell you've left. That means no visited set is needed, and longest-path on a DAG is a straightforward DP. I define `longest(r, c)` as the length of the longest increasing path starting at that cell, which is 1 plus the best over all strictly-larger neighbours, or just 1 if there are none. Crucially that value doesn't depend on how I reached the cell, so I can memoize it — which is what turns an exponential exploration into O(m·n), since there are m·n states and each does constant work. Then I take the max over all starting cells. O(m·n) time and space. One caveat: the recursion can nest 40,000 deep on a monotone matrix, so if that's a concern I'd do it iteratively with a topological sort — peel off cells with no larger neighbours layer by layer, and the number of layers is the answer."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is longest path tractable here?" | Strict increase makes the graph acyclic. Longest path is NP-hard on general graphs precisely because cycles force you to track which nodes you've used; on a DAG it's a simple DP. |
| "Why no visited set?" | You can't revisit a cell — that would require values to both increase and decrease around a loop. Adding one would also break memoization, since cached values would depend on the marking state. |
| "Make it iterative." | Kahn's topological sort: count each cell's number of strictly-larger neighbours (its out-degree in the DAG), start from cells with zero, and peel layer by layer. The layer count is the answer. O(m·n), no stack. |
| "What if equal values could be stepped on?" | Then it's no longer a DAG — equal neighbours form cycles, and the recursion wouldn't terminate. You'd need a visited set and the problem becomes NP-hard. |
| "Return the actual path, not the length." | Record which neighbour gave the max at each cell, then walk from the best starting cell following those pointers. |
| "Diagonal moves too?" | Add the four diagonal offsets to the direction list. Nothing else changes — the DAG property comes from the increasing rule, not the move set. |
| "Why does the outer sweep not cost O((m·n)²)?" | Because a cell is computed from scratch at most once across the whole run. Every other call is a cache hit, so the total work is bounded by m·n first-time computations. |
| "Could you sort the cells instead?" | Yes — process in ascending value order, so every larger neighbour is already resolved. Iterative, but the sort makes it O(m·n log(m·n)). |

**Traps:**
- **Adding backtracking (mark/unmark).** Unnecessary *and* incompatible with the cache — a memoized value computed under a particular marking isn't generally reusable.
- **`>=` instead of `>`.** Equal-valued neighbours create cycles and the recursion never returns.
- **Bounds checks after the matrix access.** Negative indices wrap silently in Python, giving wrong answers instead of a clean crash.
- Initializing `best = 0` instead of 1 — every path comes out one short, and a lone cell reports 0.
- Forgetting to try *every* cell as a start. The longest path rarely begins at `(0,0)`.
- Ignoring the recursion depth. Real on a 200 × 200 monotone matrix.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (a DAG and cycle reasoning — here acyclicity is guaranteed rather than checked) · [Number of Islands](200-number-of-islands.md) (grid DFS, where a visited set *is* required because there's no ordering to prevent revisits) · [Word Search](79-word-search.md) (grid DFS *with* backtracking — the contrast that makes this problem's omission meaningful) · [Target Sum](494-target-sum.md) (memoizing a state whose value is independent of the path taken to reach it) · [Longest Increasing Subsequence](300-longest-increasing-subsequence.md) (the 1-D cousin of "longest strictly increasing chain").

</details>

---
