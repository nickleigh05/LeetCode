# 64. Minimum Path Sum

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-path-sum/) · [Solution file (no hints)](../../problems/0001-0499/64.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Find a path from top-left to bottom-right, moving only **down or right**, minimising the sum of the numbers along it.

```
grid = [[1,3,1],          →  7      1 → 3 → 1 → 1 → 1
        [1,5,1],
        [4,2,1]]

grid = [[1,2,3],[4,5,6]]  →  12
```

**Constraints:** `1 <= m, n <= 200` · `0 <= grid[i][j] <= 200`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimizes** the sum" | Optimisation → `min` over the two incoming directions |
| "only **down or right**" | ⚠️ A DAG — each cell depends only on cells above and left |
| "**non-negative** numbers" | Greedy still fails, but there's no negative-cycle worry |
| `1 <= m, n <= 200` | O(m·n) = 4 × 10⁴ — trivial |

**This is [Unique Paths II](63-unique-paths-ii.md) with `min` instead of `+`.** The grid, the movement rules, and the sweep are identical; only the combining operation changes:

```
Unique Paths II:   dp[r][c] = dp[r-1][c] + dp[r][c-1]              count paths
Minimum Path Sum:  dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c]   minimise cost
```

**Read it as:** *to stand on this cell you must have arrived from above or from the left; take whichever was cheaper, then pay this cell's own cost.*

**Why greedy fails.** "Always step toward the smaller neighbour" is the obvious instinct, and it's wrong:

```
grid = [[1,3,1],
        [1,5,1],
        [4,2,1]]

From (0,0), greedy compares right (3) and down (1) → goes DOWN.
Then from (1,0): right is 5, down is 4 → goes DOWN.
Path 1→1→4→2→1 = 9.

Optimal is 1→3→1→1→1 = 7  ✅
```

**A locally cheap step can commit you to an expensive region.** Only the DP, which considers *all* routes into each cell, gets this right — and the problem's own Example 1 is the counterexample.

⚠️ **Why Dijkstra is overkill here.** You *could* treat this as a shortest-path problem, but the movement restriction (down/right only) makes the graph a **DAG with a known topological order** — row by row, left to right. **A DAG with a known order needs no priority queue**, so the DP is O(m·n) rather than Dijkstra's O(m·n·log(m·n)).

```
allowed moves: down, right      →  DAG, sweep order known  →  plain DP
allowed moves: all four         →  cycles possible         →  Dijkstra needed
```

That distinction is worth stating — it's exactly what separates this from [Path With Minimum Effort](1631-path-with-minimum-effort.md).

🤔 **Before you open the next section:** the first row has no cell above it and the first column has none to the left. What should `min(above, left)` produce there, and how can you arrange for it to happen without a special case?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy (step to the cheaper neighbour) | Local choice | O(m+n) | O(1) | ❌ **Wrong** — fails Example 1 |
| Backtracking over all paths | Enumerate | O(2^(m+n)) | O(m+n) | ❌ |
| Dijkstra | Priority queue | O(mn log mn) | O(mn) | ⚠️ Correct, unnecessary on a DAG |
| 2-D DP | Full table | O(m·n) | O(m·n) | ✅ Clearest |
| **1-D rolling DP** | One row in place | **O(m·n)** | **O(n)** | ✅ ← |

**The decision: a single rolling row**, same shape as [Unique Paths II](63-unique-paths-ii.md).

**The rolling trick, and the one wrinkle this problem adds.** Sweeping left-to-right through one array:

```
dp[c]    (not yet written this row)  =  the cell ABOVE
dp[c-1]  (already written this row)  =  the cell to the LEFT
```

so `dp[c] = min(dp[c], dp[c-1]) + grid[r][c]` is exactly the recurrence. **But column 0 has no left neighbour**, and `dp[c-1]` would wrap to the end of the array via negative indexing. Handle it separately:

```python
dp[0] += grid[r][0]        # column 0: only the cell above
for c in range(1, cols):
    dp[c] = min(dp[c], dp[c-1]) + grid[r][c]
```

**The initialisation is the elegant part:**

```python
dp = [float('inf')] * cols
dp[0] = 0
```

**Everything is unreachable except a virtual "before the start" position.** Then the first row's sweep produces the correct prefix sums automatically:

```
dp = [0, inf, inf],  first row = [1,3,1]

c=0: dp[0] += 1                        → 1
c=1: min(inf, 1) + 3 = 4               → 4     ← inf loses, so only "from the left" counts ✅
c=2: min(inf, 4) + 1 = 5               → 5
```

**The `inf` values mean "no path from above yet", and `min` discards them without a special case.** That's the standard trick for seeding an optimisation DP — the identity element for `min` is infinity, exactly as 0 is for sum.
→ [float-inf](../syntax/float-inf.md)

**Why not mutate the input grid?** You can — `grid[r][c] += min(grid[r-1][c], grid[r][c-1])` gives O(1) extra space. ⚠️ **It destroys the caller's data**, which is a real API concern. The rolling row costs O(n) and leaves the input intact.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(grid), len(grid[0])
dp = [float('inf')] * cols
dp[0] = 0
```

**`dp[c]` = the cheapest cost to reach column `c` of the row processed so far.**

`inf` marks "not reachable yet"; `dp[0] = 0` is the virtual starting point *before* the first cell, so the first row's costs come out right.
→ [list-basics](../syntax/list-basics.md) · [float-inf](../syntax/float-inf.md)

```python
for r in range(rows):
    dp[0] += grid[r][0]
```

**Column 0 handled separately** — it has no left neighbour, so its only predecessor is the cell above, which `dp[0]` already holds. Accumulating downward gives the first column's prefix sums.

⚠️ Without this line you'd need `dp[c-1]` at `c = 0`, which Python would read as `dp[-1]` — **the last element of the array, silently, with no error.**
→ [for-loop](../syntax/for-loop.md)

```python
    for c in range(1, cols):
        dp[c] = min(dp[c], dp[c-1]) + grid[r][c]
```

**The recurrence, in place.**

| Term | Meaning |
|---|---|
| `dp[c]` | value from the **previous row** — the cell above |
| `dp[c-1]` | value already written **this row** — the cell to the left |
| `min(...)` | take the cheaper arrival |
| `+ grid[r][c]` | pay this cell's own cost |

⚠️ **Starting at `c = 1`** is what keeps column 0 out of this loop. The left-to-right direction is load-bearing: right-to-left would read `dp[c-1]` from the previous row.
→ [min-max-key](../syntax/min-max-key.md) · [range-function](../syntax/range-function.md)

```python
return dp[cols-1]
```

**The bottom-right cell**, after every row has been swept.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:

        rows, cols = len(grid), len(grid[0])

        dp = [float('inf')] * cols
        dp[0] = 0

        for r in range(rows):
            dp[0] += grid[r][0]
            for c in range(1, cols):
                dp[c] = min(dp[c], dp[c-1]) + grid[r][c]

        return dp[cols-1]
```

</details>

**Trace it** — `grid = [[1,3,1],[1,5,1],[4,2,1]]`:

| Stage | `dp` | Notes |
|---|---|---|
| initial | `[0, inf, inf]` | |
| **row 0** `[1,3,1]` | | |
|   c=0 | `[1, inf, inf]` | `0 + 1` |
|   c=1 | `[1, 4, inf]` | `min(inf, 1) + 3` — **above is unreachable, so from the left** |
|   c=2 | `[1, 4, 5]` | `min(inf, 4) + 1` |
| **row 1** `[1,5,1]` | | |
|   c=0 | `[2, 4, 5]` | `1 + 1` |
|   c=1 | `[2, 7, 5]` | `min(4, 2) + 5` = 2 + 5 — **from above** |
|   c=2 | `[2, 7, 6]` | `min(5, 7) + 1` = 5 + 1 — **from above** |
| **row 2** `[4,2,1]` | | |
|   c=0 | `[6, 7, 6]` | `2 + 4` |
|   c=1 | `[6, 8, 6]` | `min(7, 6) + 2` = 6 + 2 — **from the left** |
|   c=2 | `[6, 8, **7**]` | `min(6, 8) + 1` = 6 + 1 — **from above** ✅ |

**Answer: 7** ✅

**Reading the path backwards from the answer:** the final cell took "from above", i.e. `(1,2)` with cost 6. That came from above too — `(0,2)` with cost 5. Which came from the left — `(0,1)` cost 4, then `(0,0)` cost 1. **So the path is `1 → 3 → 1 → 1 → 1`**, exactly as the problem states.

**Row 0 is where `inf` earns its place.** At `c=1`, the "above" value is `inf` because there is no row above — `min` discards it automatically and takes the left neighbour. **No first-row special case is written anywhere.**

**Row 1, c=1 shows the choice being made.** Coming from above costs 2, from the left costs 4 — so 2 wins, and the total becomes 7. Note the greedy path would have gone through here and been stuck; the DP keeps *both* options alive at every cell and only commits at the end.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m·n)** — one visit per cell, O(1) work each (a `min` and an addition).

At 200×200 that's **40,000 operations**. Instant.

**This is optimal** — every cell must be read, since any unread value could change the minimum. **Ω(m·n) is the lower bound.**

**Versus Dijkstra**, which also solves it: O(m·n·log(m·n)) ≈ 40,000 × 15 = 6 × 10⁵. **An unnecessary log factor**, because the down/right restriction makes the graph a DAG whose topological order is just "row by row, left to right". Dijkstra's priority queue exists to *discover* a safe processing order; here you already know it.

| | Graph shape | Needs a heap? |
|---|---|---|
| **Minimum Path Sum** | DAG, order known | ❌ **plain DP** |
| [Path With Minimum Effort](1631-path-with-minimum-effort.md) | 4-directional, cycles | ✅ Dijkstra |

**That's the distinction to draw** — it's the same grid, and the movement rules alone decide which algorithm applies.

**Versus backtracking:** `C(m+n-2, m-1)` paths, which at 200×200 is astronomically large. The DP works because paths share prefixes, and each cell's best cost is computed once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — a single row.

| Component | Size |
|---|---|
| `dp` | `cols` values → **O(n)** |
| **Total** | **O(n)** |

At 200×200 that's 200 values instead of 40,000.

| Approach | Space |
|---|---|
| Full 2-D table | O(m·n) = 40,000 |
| **Rolling row** | **O(n) = 200** ✅ |
| Mutate the input grid | O(1) — ⚠️ destroys the caller's data |

**Rolling along the shorter dimension** gives O(min(m,n)) — transpose the sweep if `m < n`. Marginal here.

⚠️ **The trade for O(n):** you can't reconstruct the actual path afterwards, only its cost. **Keep the full table if the path is wanted** — then walk back from the bottom-right, at each step moving to whichever neighbour's value plus the current cell's cost matches.

**In-place mutation is genuinely O(1) extra** and a fine answer when the grid is disposable — but say the caveat rather than presenting it as strictly better.

**No recursion** — iterative, so no stack concern. A memoised recursive version would be up to 400 frames deep at 200×200, which is safe, but the iterative sweep avoids the question.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each cell can only be entered from above or from the left, so the cheapest way to reach it is the cheaper of those two, plus its own value. Greedy fails — the problem's first example is the counterexample, where stepping toward the smaller neighbour commits you to an expensive region and costs 9 instead of 7. I use a single rolling row: sweeping left to right, `dp[c]` still holds the row above while `dp[c-1]` holds this row, so `min(dp[c], dp[c-1]) + grid[r][c]` is exactly the recurrence. Column 0 is handled separately since it has no left neighbour, and I initialise the row to infinity with `dp[0] = 0`, which makes the first row come out right without a special case — infinity loses every `min`. O(m·n) time and O(n) space. Worth noting: Dijkstra would also work but is overkill, because restricting movement to down and right makes this a DAG with a known topological order, so no priority queue is needed."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not greedy?" | **The question.** A locally cheap step can commit you to an expensive region. Example 1 gives 9 instead of 7. |
| "Why not Dijkstra?" | Down/right movement makes it a DAG with a known order, so the heap is unnecessary — O(m·n) instead of O(m·n·log(m·n)). |
| "When *would* you need Dijkstra?" | If all four directions were allowed — cycles become possible and the processing order is no longer obvious. |
| "Why initialise to infinity?" | It's the identity for `min`, so the first row's missing "above" neighbour is discarded automatically. No special case. |
| "Why handle column 0 separately?" | It has no left neighbour, and `dp[-1]` would silently read the array's last element. |
| "Reduce space further?" | Mutate the input grid for O(1), or roll along the shorter dimension for O(min(m,n)). |
| "Return the actual path?" | Keep the full table and walk back from the bottom-right, choosing the neighbour whose value plus this cell equals the current one. |
| "What if values could be negative?" | The DP still works — it's a DAG, so no negative cycles are possible. ⚠️ Dijkstra would break. |
| "What if you could also move up and left?" | Then it's a genuine shortest-path problem — Dijkstra, or BFS if unweighted. |

**Traps:**

- **Greedy.** Fails on the problem's own first example.
- **Not handling column 0 separately** — `dp[-1]` reads the array's last element with no error.
- **Initialising `dp` to zeros** — the first row would take `min(0, left)` = 0 and undercount everything.
- **Sweeping right-to-left** — reads the previous row for the left neighbour.
- **Forgetting `+ grid[r][c]`** — you'd be minimising over path *choices* without paying for cells.
- **Using Dijkstra** — correct but adds a log factor for nothing.
- **Mutating the input without saying so** — fine for LeetCode, a real concern in an API.

**This same move shows up in:** [Unique Paths II](63-unique-paths-ii.md) (the same sweep, summing counts instead of minimising) · [Triangle](120-triangle.md) and [Minimum Falling Path Sum](931-minimum-falling-path-sum.md) (the same rolling-row minimisation with different neighbour sets) · [Dungeon Game](174-dungeon-game.md) (the same grid, swept **backwards**) · [Path With Minimum Effort](1631-path-with-minimum-effort.md) (four-directional, so Dijkstra is required) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
