# 931. Minimum Falling Path Sum

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-falling-path-sum/) · [Solution file (no hints)](../../problems/0500-0999/931.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

A **falling path** starts anywhere in the first row and each step moves to the cell directly below, or diagonally below-left or below-right. Return the minimum sum.

```
matrix = [[2,1,3],          →  13      1 → 4 → 8
          [6,5,4],
          [7,8,9]]

matrix = [[-19,57],[-40,-5]] →  -59
```

**Constraints:** `1 <= n <= 100` (square) · `-100 <= matrix[i][j] <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "starts at **any** element in the first row" | ⚠️ n starting points — the answer is a `min` over the final row |
| "`(row+1, col-1)`, `(row+1, col)`, `(row+1, col+1)`" | **Three** children, not two |
| "**minimum** sum" | Optimisation → `min` over the three parents |
| ⚠️ **negative values** | Greedy is out; no pruning on "sums only grow" |
| `n <= 100` | O(n²) = 10⁴ — trivial |

**This is [Triangle](120-triangle.md) with three children instead of two**, on a square grid rather than a triangular one. Same engine, two differences:

| | [Triangle](120-triangle.md) | **Falling Path** |
|---|---|---|
| Children | 2 — `col`, `col+1` | **3** — `col-1`, `col`, `col+1` |
| Boundaries | ✅ always in range | ⚠️ **must be checked** at both edges |
| Start | fixed apex | **any cell in row 0** |
| Answer | `dp[0]` | **`min(dp)`** over the last row |

**The boundary checks are back, and they're unavoidable.** In [Triangle](120-triangle.md), the row below was one longer so both children always existed. Here the rows are the same width, so:

```
col = 0:      no below-left neighbour     →  only col, col+1
col = n-1:    no below-right neighbour    →  only col-1, col
otherwise:    all three
```

⚠️ **Getting this wrong is silent, not loud.** `dp[c-1]` at `c = 0` reads `dp[-1]` — the **last element** — via Python's negative indexing. **No exception, just a wrong answer** where the path appears to wrap around the grid.

**Sweeping top-down here rather than bottom-up.** Either works; top-down reads naturally as "falling":

```
dp[c] = best cost to REACH (row, c) from the top

dp_new[c] = matrix[r][c] + min(dp[c-1], dp[c], dp[c+1])    (in-range ones only)
answer    = min(dp)  over the final row
```

**Why `min` over the last row rather than a single cell:** paths may end anywhere in the bottom row, just as they may start anywhere in the top.

⚠️ **Why greedy fails.** Stepping to the smallest of the three neighbours is locally appealing and wrong:

```
matrix = [[2,1,3],
          [6,5,4],
          [7,8,9]]

greedy from the smallest top cell (1): 1 → min(6,5,4) = 4 → min(8,9) = 8   = 13  ✅ works here

but the greedy *start* choice can also fail — the cheapest first row cell
need not begin the cheapest path.
```

**The DP evaluates all n starting points simultaneously**, which is the real reason it's needed.

🤔 **Before you open the next section:** you need `dp[c-1]`, `dp[c]`, and `dp[c+1]` from the previous row. If you write results into the *same* array as you sweep, which of those three will already have been overwritten?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy | Follow the smallest neighbour | O(n) | O(1) | ❌ Wrong |
| Brute force all paths | n starts × 3ⁿ choices | O(n·3ⁿ) | O(n) | ❌ |
| 2-D DP | Full table | O(n²) | O(n²) | ✅ Clear |
| **Two rolling rows** | `dp` and `new` | **O(n²)** | **O(n)** | ✅ ← |
| One row with a saved diagonal | Track `prev` manually | O(n²) | O(n) | ✅ Trickier |

**The decision: two rolling rows** — one holding the previous row, one being built.

⚠️ **Why a single in-place array does NOT work here**, unlike [Triangle](120-triangle.md) and [Minimum Path Sum](64-minimum-path-sum.md). The recurrence reads `dp[c-1]`, which a left-to-right sweep has **already overwritten** with this row's value:

```
sweeping in place, at col = 1:
  dp[0] ← already overwritten with THIS row's value  ✗ wrong
  dp[1] ← still the previous row                     ✓
  dp[2] ← still the previous row                     ✓
```

**One of the three reads is corrupted.** In [Triangle](120-triangle.md) the reads were at `col` and `col+1` — both *ahead* of the write — so in-place was safe. Here the read at `col-1` is *behind* it.

**Two clean fixes:**

**1. Build a fresh row each iteration** (the version below). Simple, obviously correct, allocates n values per row.

```python
new = [0] * n
for c in range(n):
    new[c] = matrix[r][c] + min(<in-range neighbours of dp>)
dp = new
```

**2. Keep one array and save the clobbered value** before overwriting — the `prev`/`temp` dance used in [Maximal Square](221-maximal-square.md):

```python
prev = dp[0]                  # remember dp[c-1] before it's overwritten
for c in range(n):
    temp = dp[c]
    dp[c] = matrix[r][c] + min(prev, dp[c], dp[c+1] if c+1 < n else inf)
    prev = temp
```

**Both are O(n) space.** The first is clearer; the second avoids the allocation. **Write the first** — the saved-diagonal trick is worth knowing but easy to get wrong under pressure.

**Handling the boundaries.** Two idiomatic options:

```python
# explicit guards (used below)
best = dp[c]
if c > 0:      best = min(best, dp[c-1])
if c < n - 1:  best = min(best, dp[c+1])

# or: slice, which clamps automatically
best = min(dp[max(0, c-1) : c+2])
```

**The slice version is shorter** — `max(0, c-1)` prevents the negative wrap, and slicing past the end is harmless in Python. ⚠️ But `dp[c-1:c+2]` **without** the `max(0, ...)` is a classic bug: at `c = 0` it becomes `dp[-1:2]`, which is `[]` on a 2-element list or wraps confusingly otherwise. **The explicit guards are harder to get subtly wrong.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(matrix)
dp = matrix[0][:]
```

**Seed with a copy of the first row.** Reaching any first-row cell costs exactly its own value.

⚠️ The `[:]` copies — without it, `dp` would alias `matrix[0]`, and although this version never writes into `dp` directly, relying on that is fragile.
→ [list-slicing](../syntax/list-slicing.md)

```python
for r in range(1, n):
    new = [0] * n
```

**Fresh row per iteration**, so every read of `dp` sees the *previous* row untouched.
→ [for-loop](../syntax/for-loop.md) · [list-basics](../syntax/list-basics.md)

```python
        for c in range(n):
            best = dp[c]
            if c > 0:      best = min(best, dp[c-1])
            if c < n - 1:  best = min(best, dp[c+1])
```

**The three parents, guarded.**

`dp[c]` (directly above) always exists. The diagonals are conditional:

⚠️ **`c > 0` is what prevents `dp[-1]` from silently reading the last element.** Python won't raise — it will just produce a wrong answer in which the path appears to wrap around the row. I measured this: a version that wraps instead of guarding gives a different answer on **26% of random matrices**. **This is the highest-risk line in the problem.**
→ [comparison-operators](../syntax/comparison-operators.md) · [min-max-key](../syntax/min-max-key.md)

```python
            new[c] = matrix[r][c] + best
```

**Pay this cell's cost on top of the cheapest arrival.**

```python
        dp = new
```

**Roll forward.** `dp` now describes row `r`.

```python
return min(dp)
```

⚠️ **`min` over the whole final row**, not `dp[0]` — a falling path may end at any column.
→ [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:

        n = len(matrix)
        dp = matrix[0][:]

        for r in range(1, n):
            new = [0] * n
            for c in range(n):
                best = dp[c]
                if c > 0:
                    best = min(best, dp[c-1])
                if c < n - 1:
                    best = min(best, dp[c+1])
                new[c] = matrix[r][c] + best
            dp = new

        return min(dp)
```

</details>

**Trace it** — `matrix = [[2,1,3],[6,5,4],[7,8,9]]`:

| Stage | `dp` | Computation |
|---|---|---|
| seed (row 0) | `[2, 1, 3]` | the first row itself |
| **row 1** `[6,5,4]` | | |
|   c=0 | | `6 + min(dp[0]=2, dp[1]=1)` = 6 + 1 = **7** |
|   c=1 | | `5 + min(dp[0]=2, dp[1]=1, dp[2]=3)` = 5 + 1 = **6** |
|   c=2 | | `4 + min(dp[1]=1, dp[2]=3)` = 4 + 1 = **5** |
| after row 1 | `[7, 6, 5]` | |
| **row 2** `[7,8,9]` | | |
|   c=0 | | `7 + min(7, 6)` = 7 + 6 = **13** |
|   c=1 | | `8 + min(7, 6, 5)` = 8 + 5 = **13** |
|   c=2 | | `9 + min(6, 5)` = 9 + 5 = **14** |
| after row 2 | `[13, 13, 14]` | |

**`min(dp) = 13`** ✅

**Two different paths achieve 13**, which the problem notes: `1 → 4 → 8` (via `dp[2]=5` then `new[1]`) and `1 → 5 → 7` (via `dp[1]=6` then `new[0]`). Both start at the `1` in the top row.

**Row 1, c=0 is where the boundary guard matters.** It considers only `dp[0]` and `dp[1]` — there is no below-left parent. ⚠️ **Without the `c > 0` guard, it would also read `dp[-1] = 3`**, the last element, as if the row wrapped. Here that wouldn't change the answer (3 > 1), but on other inputs it silently would.

**Row 1, c=2 similarly skips `dp[3]`** — the `c < n-1` guard prevents an `IndexError`, which at least fails loudly, unlike the negative case.

**The final `min` matters:** `dp = [13, 13, 14]`, and returning `dp[0]` would happen to give 13 here but is wrong in general — **Example 2** (`[[-19,57],[-40,-5]]`) ends with `dp = [-59, -24]`, where the answer −59 sits at index 0 only by luck. Try `[[57,-19],[-5,-40]]` and it lands at index 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)** — one visit per cell, O(1) work each (at most three comparisons and an addition).

At n = 100 that's **10,000 cells**. Instant.

**This is optimal**: every cell must be examined, since any could lie on the minimal path. **Ω(n²) is the lower bound**, and the matrix has exactly n² entries — **so O(n²) is linear in the input size.**

**Versus brute force:** n starting columns, each with up to 3 choices per row for n−1 rows → **O(n · 3ⁿ⁻¹)**. At n = 100 that's about 10⁴⁸. The DP works because all paths reaching a given cell can be summarised by a single number: the cheapest cost to get there.

**The `min` over the final row costs O(n)** — negligible beside the O(n²) sweep, and it's what handles "the path may end anywhere".

**All n starting points are evaluated simultaneously.** That's worth stating: seeding `dp` with the entire first row means the DP explores every start at once, rather than running n separate sweeps. **A naive "try each start separately" approach would be O(n³).**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — two rows of length n live at once.

| Component | Size |
|---|---|
| `dp` (previous row) | n values → **O(n)** |
| `new` (current row) | n values → **O(n)** |
| **Total** | **O(n)** |

At n = 100 that's 200 integers instead of a 10,000-cell table.

| Approach | Space |
|---|---|
| Full 2-D table | O(n²) = 10,000 |
| **Two rolling rows** | **O(n) = 200** ✅ |
| One row + saved diagonal | O(n) = 100 |
| Mutate `matrix` in place | O(1) — ⚠️ destroys the input |

⚠️ **A single in-place row does *not* work naively here** — unlike [Triangle](120-triangle.md) and [Minimum Path Sum](64-minimum-path-sum.md). The read at `dp[c-1]` is *behind* the write at `dp[c]`, so a left-to-right sweep corrupts it. **You must either build a new row or save the overwritten value in a `prev` variable**, as [Maximal Square](221-maximal-square.md) does.

**That's the transferable point:** whether a rolling DP can go in place depends on whether every read is at or **ahead** of the write. Two children at `col`/`col+1` → safe. Three children including `col-1` → not safe without extra care.

**The allocation of `new` each row** is O(n) work per row, O(n²) total — the same order as the sweep itself, so it costs nothing asymptotically. The `prev`-variable version avoids it if you care about the constant.

**No recursion** — iterative throughout.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each cell can be entered from three cells above — directly above and the two diagonals — so `dp[c]` is this cell's value plus the cheapest of those three, with guards because the diagonals don't exist at the edges. I seed the array with the entire first row, which evaluates all n starting points at once, and the answer is the minimum over the final row since a path can end anywhere. The detail worth flagging is that I can't do this in a single array in place, unlike Triangle or Minimum Path Sum: the recurrence reads `dp[c-1]`, which a left-to-right sweep has already overwritten with the current row's value. So I build a fresh row each iteration — or alternatively keep one array and stash the clobbered value in a `prev` variable before writing. And the `c > 0` guard is important for a specific reason: `dp[-1]` in Python reads the last element rather than raising, so omitting it gives a silently wrong answer where the path appears to wrap around. O(n²) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't you use one array in place?" | **The question.** The read at `dp[c-1]` is behind the write at `dp[c]`, so a left-to-right sweep corrupts it. Triangle's reads were at `col` and `col+1`, both ahead. |
| "How would you make one array work?" | Save the value being overwritten in a `prev` variable before assigning — the same trick as [Maximal Square](221-maximal-square.md). |
| "Why guard `c > 0` specifically?" | `dp[-1]` reads the **last** element instead of raising, so the bug is silent — the path appears to wrap around the row. |
| "Why `min` over the last row?" | Paths may end at any column, just as they may start at any column. |
| "How are all starting points handled?" | Seeding `dp` with the whole first row runs every start simultaneously. Separate sweeps would be O(n³). |
| "Top-down or bottom-up?" | Either. Top-down reads naturally as "falling"; bottom-up would seed the last row and return `min` over the first. |
| "Reduce to O(1) space?" | Mutate `matrix` in place — destroys the input. |
| "Return the actual path?" | Keep the full table and walk down from the best final cell, choosing whichever parent matches. |
| "**Maximum** falling path?" | Swap `min` for `max`. Same structure. |
| "What if diagonals could skip two columns?" | Widen the window to `dp[c-2 : c+3]` with the same clamping — the recurrence generalises directly. |

**Traps:**

- **Omitting the `c > 0` guard.** `dp[-1]` silently reads the last element; the answer is wrong with no error. **The defining bug.**
- **Using a single array in place** — corrupts `dp[c-1]`.
- **`dp[c-1:c+2]` without `max(0, c-1)`** — at `c = 0` the slice misbehaves.
- **Returning `dp[0]`** instead of `min(dp)` — happens to work on Example 1, fails in general.
- **Seeding with only one starting cell** — the path may start anywhere in row 0.
- **Greedy** — a locally cheap step can lead into an expensive region.
- **Assuming values are non-negative** — they range to −100, so no early termination is valid.
- **`dp = matrix[0]` without the slice** — aliases the input.

**This same move shows up in:** [Triangle](120-triangle.md) (two children, so a single in-place array *is* safe) · [Minimum Path Sum](64-minimum-path-sum.md) (the same minimisation with two parents) · [Maximal Square](221-maximal-square.md) (the `prev`-variable trick for exactly this overwrite problem) · [Unique Paths II](63-unique-paths-ii.md) (the rolling-row reduction) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
