# 63. Unique Paths II

**Medium** · [LeetCode](https://leetcode.com/problems/unique-paths-ii/) · [Solution file (no hints)](../../problems/0001-0499/63.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Count paths from top-left to bottom-right moving only **down or right**, where `1` marks an **obstacle** you cannot enter.

```
grid = [[0,0,0],          →  2      RR-DD  and  DD-RR
        [0,1,0],
        [0,0,0]]

grid = [[0,1],[0,0]]      →  1
```

**Constraints:** `1 <= m, n <= 100` · cells are `0` or `1` · the answer fits in `2 × 10^9`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "only move either **down or right**" | Every path has the same length; no cycles → a clean DP over the grid |
| "cannot include any square that is an obstacle" | ⚠️ An obstacle contributes **0 paths** — not "skip it", but "zero it" |
| "**number** of possible unique paths" | Count, don't enumerate |
| "answer ≤ 2 × 10⁹" | Fits a 64-bit int; hints the count can be large |
| `1 <= m, n <= 100` | O(m·n) = 10⁴ — trivial. The difficulty is the edge cases |
| — | ⚠️ **The start or the finish can itself be an obstacle** |

**This is [Unique Paths](62-unique-paths.md) plus one rule.** There, every cell's count was `above + left`. Here that still holds — **except an obstacle has zero ways to be stood on**:

```
dp[r][c] = 0                             if grid[r][c] == 1
dp[r][c] = dp[r-1][c] + dp[r][c-1]       otherwise
```

**The obstacle rule propagates automatically.** You don't need to reason about which paths are blocked downstream — a zeroed cell contributes 0 to everything below and right of it, so the blockage spreads on its own:

```
grid          dp
0 0 0         1 1 1
0 1 0    →    1 0 1        ← the obstacle zeroes its own cell
0 0 0         1 1 2        ← and the 0 flows into everything past it
```

⚠️ **Why the closed-form binomial from [Unique Paths](62-unique-paths.md) dies here.** There the answer was `C(m+n-2, m-1)` — pure combinatorics, no DP needed. Obstacles destroy that: there's no clean formula for "paths avoiding an arbitrary set of cells". **The DP is now mandatory**, which is the real lesson of the variant.

**The edge cases that break naive implementations:**

```
grid = [[1]]           →  0    the start IS an obstacle
grid = [[0,0],[0,1]]   →  0    the FINISH is an obstacle
grid = [[0,1],[1,0]]   →  0    walled off — the DP handles this without a special case
```

The first two are worth an explicit guard; the third falls out of the recurrence.

🤔 **Before you open the next section:** in [Unique Paths](62-unique-paths.md) the entire first row is 1s. What does the first row look like here if there's an obstacle in the middle of it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Backtracking, count paths | Explore every route | O(2^(m+n)) | O(m+n) | ❌ ~10⁶⁰ at 100×100 |
| Binomial formula | `C(m+n-2, m-1)` | O(1) | O(1) | ❌ **Invalid with obstacles** |
| 2-D DP | Full `dp[m][n]` table | O(m·n) | O(m·n) | ✅ Clearest |
| **1-D rolling DP** | One row, updated in place | **O(m·n)** | **O(n)** | ✅ ← |

**The decision: a single rolling row.**

**Why one row suffices** — the observation that collapses the space. Computing `dp[r][c]` needs only `dp[r-1][c]` (directly above) and `dp[r][c-1]` (directly left). If you sweep left-to-right through a single array:

```
dp[c] before writing  =  the value from the PREVIOUS row  (above)
dp[c-1] already written =  the value from THIS row         (left)
```

**Both neighbours are available in one array at the moment you need them** — no second row required. `dp[c] += dp[c-1]` performs `above + left` in place.

⚠️ **This works only because the traversal order matches the dependencies.** Sweeping right-to-left would read `dp[c-1]` from the previous row instead of the current one, giving wrong answers.

**Seeding is the subtle part:**

```python
dp = [0] * cols
dp[0] = 1
```

**`dp[0] = 1` before any row is processed** represents "one way to be at the start". Then the very first row's sweep turns it into the correct first row automatically — including obstacle handling:

```
first row = [0,1,0],  dp starts [1,0,0]

c=0: not an obstacle, c==0 so no left neighbour  →  dp[0] stays 1
c=1: OBSTACLE                                    →  dp[1] = 0
c=2: dp[2] += dp[1]  →  0 + 0 = 0                →  everything past the wall is unreachable ✅
```

**No special-casing of the first row is needed** — the `elif c > 0` guard handles it, and the wall correctly blocks the rest of the row.

**The `if/elif` structure matters:**

```python
if grid[r][c] == 1:
    dp[c] = 0            # obstacle: zero it
elif c > 0:
    dp[c] += dp[c-1]     # otherwise: above + left
```

⚠️ **Column 0 gets no `else` branch at all** — and that's correct. It has no left neighbour, so its value should just carry down from the row above, which is exactly what "leave `dp[0]` alone" does. **Writing `dp[c] = dp[c]` explicitly would be the same thing**; omitting it is the same logic.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(obstacleGrid), len(obstacleGrid[0])

if obstacleGrid[0][0] == 1 or obstacleGrid[rows-1][cols-1] == 1:
    return 0
```

**The two guards worth writing explicitly.** If the start is blocked you can never begin; if the finish is blocked you can never arrive.

⚠️ The start guard is genuinely necessary — without it, `dp[0] = 1` would seed a path from a cell you can't stand on. The finish guard is technically redundant (the recurrence would zero it anyway) but states the intent.
→ [nested-lists](../syntax/nested-lists.md) · [if-return](../syntax/if-return.md)

```python
dp = [0] * cols
dp[0] = 1
```

**One row, seeded with "one way to be at the start".**

Everything else starts at 0 — before the first row is processed, no other column is reachable.
→ [list-basics](../syntax/list-basics.md)

```python
for r in range(rows):
    for c in range(cols):
```

**Sweep every row, left to right.** ⚠️ The left-to-right direction is load-bearing: it guarantees `dp[c-1]` already holds *this* row's value while `dp[c]` still holds the *previous* row's.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if obstacleGrid[r][c] == 1:
            dp[c] = 0
```

**An obstacle has zero paths through it.** This is the entire difference from [Unique Paths](62-unique-paths.md), and the zero propagates onward on its own.

```python
        elif c > 0:
            dp[c] += dp[c-1]
```

**`above + left`, in place.**

`dp[c]` currently holds the row above; `dp[c-1]` holds the cell to the left in this row. The `+=` combines them.

⚠️ `c > 0` skips column 0, which has no left neighbour — its value correctly carries down unchanged from the row above. **Add an `else: dp[c] = 0` and you'd wipe the first column**, breaking every downward path.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return dp[cols-1]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:

        rows, cols = len(obstacleGrid), len(obstacleGrid[0])

        if obstacleGrid[0][0] == 1 or obstacleGrid[rows-1][cols-1] == 1:
            return 0

        dp = [0] * cols
        dp[0] = 1

        for r in range(rows):
            for c in range(cols):
                if obstacleGrid[r][c] == 1:
                    dp[c] = 0
                elif c > 0:
                    dp[c] += dp[c-1]

        return dp[cols-1]
```

</details>

**Trace it** — `grid = [[0,0,0],[0,1,0],[0,0,0]]`. Verified output:

| Stage | `dp` |
|---|---|
| initial | `[1, 0, 0]` |
| after row 0 `[0,0,0]` | `[1, 1, 1]` |
| after row 1 `[0,1,0]` | `[1, 0, 1]` ⚠️ |
| after row 2 `[0,0,0]` | `[1, 1, **2**]` ✅ |

**Answer: 2** ✅

**Row 1 is where the obstacle bites.** Column 1 is zeroed, so column 2 computes `dp[2] += dp[1]` = `1 + 0` = **1** — it keeps only the path coming from directly above, losing the one that would have come through the blocked cell.

**Row 2 shows the count recovering.** Column 1 gets `0 + 1 = 1` (from the left, since above is 0), and column 2 gets `1 + 1 = 2`. **The two surviving routes are exactly RR-DD and DD-RR**, as the problem states.

**Watch column 0 across all rows** — it stays `1` throughout. There's exactly one way to reach any cell in the first column: go straight down. The `elif c > 0` guard is what preserves that.

**The `[[0,1],[0,0]]` case:**

```
initial:        [1, 0]
after row 0:    [1, 0]     ← the obstacle at (0,1) zeroes it
after row 1:    [1, 1]     ← dp[1] += dp[0] = 0 + 1 = 1
answer: 1 ✅
```

The single path is Down-Right — the top-right route is walled off, and the DP discovers that without any special reasoning.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m·n)** — one visit per cell, O(1) work each.

At 100×100 that's **10,000 operations**. Instant.

**This is optimal**: every cell must be examined, since any unread cell could be an obstacle that changes the count. **Ω(m·n) is the lower bound.**

**Versus [Unique Paths](62-unique-paths.md), which has an O(1) formula.** That problem's answer is the binomial coefficient `C(m+n-2, m-1)` — choose which of the `m+n-2` moves are "down". ⚠️ **Obstacles destroy that**: there's no closed form for paths avoiding an arbitrary cell set, so the DP is now genuinely required.

| | [Unique Paths](62-unique-paths.md) | **Unique Paths II** |
|---|---|---|
| Closed form | ✅ `C(m+n-2, m-1)` — O(1) | ❌ none |
| DP | O(m·n) | **O(m·n)** — mandatory |

**Versus backtracking:** the number of paths itself can reach 2 × 10⁹ (the problem says so), so enumerating them is hopeless. **The bound on the answer is the problem telling you to count, not list.**

**No early exit is worthwhile.** Even if `dp` becomes all zeros mid-grid (fully walled off), detecting that costs an O(n) scan per row — more than just finishing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — a single row of counts.

| Component | Size |
|---|---|
| `dp` | `cols` integers → **O(n)** |
| **Total** | **O(n)** |

At 100×100 that's 100 integers instead of 10,000.

**The reduction from O(m·n) works because each cell depends only on the row above.** Sweeping left-to-right through one array gives you both neighbours at the right moment:

| | Space |
|---|---|
| Full 2-D table | O(m·n) = 10,000 |
| **Rolling row** | **O(n) = 100** ✅ |

**A further squeeze:** use `O(min(m, n))` by rolling along the shorter dimension — transpose if `m < n`. Marginal here, but it's the honest minimum.

⚠️ **The trade:** with only one row you can't reconstruct *which* paths exist, or answer follow-up queries about intermediate cells. **Keep the full table if the caller needs more than the final count.**

**Modifying the input grid in place** would be O(1) extra space — reuse `obstacleGrid` as the DP table. Correct, and it destroys the caller's data; the rolling row is the better trade at O(n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's Unique Paths with one extra rule: an obstacle has zero paths through it. The recurrence is still `above + left`, but a blocked cell is set to 0 instead, and that zero propagates automatically to everything below and right — I don't have to reason about which downstream paths get cut. The important difference from Unique Paths is that the binomial closed form no longer applies; there's no formula for paths avoiding an arbitrary set of cells, so the DP is genuinely necessary here. I use a single rolling row instead of a full table, because sweeping left to right means `dp[c]` still holds the row above while `dp[c-1]` already holds this row — so `dp[c] += dp[c-1]` is exactly above-plus-left. Column 0 gets no addition since it has no left neighbour, and its value carries down unchanged. I guard the start and finish being obstacles explicitly. O(m·n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not the binomial formula from [Unique Paths](62-unique-paths.md)?" | **The question.** Obstacles break it — there's no closed form for paths avoiding an arbitrary cell set. |
| "How does an obstacle block downstream paths?" | Setting it to 0 is enough; the zero flows into every cell that depends on it. No extra logic needed. |
| "Why does one row work?" | Sweeping left-to-right, `dp[c]` holds the previous row and `dp[c-1]` holds the current one — both neighbours, one array. |
| "Why no `else` for column 0?" | It has no left neighbour; its value should carry down from above, which is what leaving it alone does. Adding `else: dp[c] = 0` would wipe the first column. |
| "What if the start is an obstacle?" | Return 0. Without the guard, `dp[0] = 1` would seed a path from an unreachable cell. |
| "Could you sweep right-to-left?" | No — `dp[c-1]` would then hold the previous row's value instead of this row's. The direction encodes the dependency order. |
| "Reduce space further?" | `O(min(m,n))` by rolling along the shorter side, or O(1) by mutating the input grid. |
| "What if diagonal moves were allowed?" | Add `dp[c-1]` from the previous row — you'd need to save it before overwriting, like the `prev` variable in [Maximal Square](221-maximal-square.md). |
| "Return the paths themselves?" | You'd need the full table plus a backtracking pass — and there can be 2 × 10⁹ of them. |

**Traps:**

- **Not guarding a blocked start** — `dp[0] = 1` seeds a path from a cell you can't stand on.
- **Adding `else: dp[c] = 0`** for column 0 — wipes the first column and breaks every downward path.
- **Special-casing the first row** — unnecessary; the sweep handles it, obstacles included.
- **Sweeping right-to-left** — reads the wrong row for the left neighbour.
- **Using the binomial formula** — silently ignores obstacles.
- **Initialising `dp = [1] * cols`** — copies [Unique Paths](62-unique-paths.md)'s first row without checking it for obstacles.
- **`dp[c] = dp[c-1]` instead of `+=`** — drops the contribution from above.

**This same move shows up in:** [Unique Paths](62-unique-paths.md) (the obstacle-free version, which has a closed form) · [Minimum Path Sum](64-minimum-path-sum.md) (the same grid sweep, minimising instead of counting) · [Maximal Square](221-maximal-square.md) (rolling row with a saved diagonal) · [Triangle](120-triangle.md) (the same rolling-row reduction) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
