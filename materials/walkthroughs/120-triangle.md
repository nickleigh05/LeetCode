# 120. Triangle

**Medium** · [LeetCode](https://leetcode.com/problems/triangle/) · [Solution file (no hints)](../../problems/0001-0499/120.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Return the minimum path sum from top to bottom of a triangle. From index `i` on a row you may move to index `i` or `i + 1` on the row below.

```
triangle = [[2],                    →  11      2 + 3 + 5 + 1
            [3,4],
            [6,5,7],
            [4,1,8,3]]

triangle = [[-10]]                  →  -10
```

**Constraints:** `1 <= triangle.length <= 200` · `-10^4 <= triangle[i][j] <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "move to index `i` or `i + 1`" | Two children per cell — the same shape as a grid DP |
| "minimum path sum **top to bottom**" | Optimisation over paths through a triangular DAG |
| "`triangle[i].length == triangle[i-1].length + 1`" | Row `i` has `i + 1` entries |
| ⚠️ **negative values allowed** | Greedy is definitively out; you can't prune on "costs are increasing" |
| **Follow-up: O(n) extra space** | The problem is explicitly asking for the rolling-array optimisation |

**The direction of the sweep is the whole decision.** Both work, but one is markedly cleaner:

```
TOP-DOWN                              BOTTOM-UP
dp[i] = cost to REACH cell i          dp[i] = best cost FROM cell i to the bottom
answer = min(last row)                answer = dp[0]        ← single cell ✅
edges need care (i=0, i=row)          every cell has exactly two children ✅
```

**Going bottom-up removes both awkward parts.** Sweeping upward, every cell at row `r`, index `c` has children at `(r+1, c)` and `(r+1, c+1)` — **both always exist**, because the row below is exactly one longer. No boundary checks at all.

```
row 3:  4  1  8  3        ← start here, these are their own costs
row 2:  6  5  7           6 + min(4,1)=7   5 + min(1,8)=6   7 + min(8,3)=10
row 1:  3  4              3 + min(7,6)=9   4 + min(6,10)=10
row 0:  2                 2 + min(9,10)=11  ✅
```

**And the answer is a single cell**, `dp[0]`, rather than a `min` over the final row.

⚠️ **Why greedy fails**, and the negative values make it worse. "Always step to the smaller child" is the instinct:

```
[[2],[3,4],[6,5,7],[4,1,8,3]]

greedy: 2 → 3 (3 < 4) → 5 (5 < 6) → 1 (1 < 8)  =  11    ✅ happens to work here

but:    [[1],[2,3],[100,100,1]]
greedy: 1 → 2 (2 < 3) → 100    = 103
optimal: 1 → 3 → 1             = 5   ✅
```

**A cheap step can lead into an expensive region.** The DP considers both children's *full downstream costs*, not just their face values.

🤔 **Before you open the next section:** the follow-up asks for O(n) space. If you sweep bottom-up and only ever need the row below, how many rows must you actually keep?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy (smaller child) | Local choice | O(n) | O(1) | ❌ **Wrong** |
| Brute-force all paths | Enumerate | O(2ⁿ) | O(n) | ❌ 2²⁰⁰ |
| Top-down DP | `dp[i]` = cost to reach | O(n²) | O(n) | ✅ Works, more edge cases |
| **Bottom-up rolling array** | `dp[i]` = cost from here down | **O(n²)** | **O(n)** | ✅ ← |
| In-place on the triangle | Mutate the input | O(n²) | O(1) | ⚠️ Destroys the input |

**The decision: bottom-up with a single rolling array**, which is what the follow-up is steering you toward.

**The whole algorithm is four lines:**

```python
dp = triangle[-1][:]                          # seed with the last row
for row in range(len(triangle) - 2, -1, -1):
    for col in range(row + 1):
        dp[col] = triangle[row][col] + min(dp[col], dp[col+1])
return dp[0]
```

**Three things make this clean:**

**1. No boundary checks.** At row `r`, indices run `0..r`, and the children are at `col` and `col+1` in a row of length `r+2`. **Both always exist** — the triangle's shape guarantees it. Compare a top-down sweep, where index 0 has no left parent and index `r` has no right parent, both needing guards.

**2. The array shrinks logically as you go up**, but you never resize it. After processing row `r`, only `dp[0..r]` is meaningful; the stale entries beyond that are simply never read again. **No bookkeeping needed.**

**3. Writing left-to-right is safe.** Writing `dp[col]` destroys the value the *next* iteration would want as its `dp[col]`… except the next iteration wants `dp[col+1]` and `dp[col+2]`, both still untouched. ⚠️ **This only works because you write to index `col` and read from `col` and `col+1`** — the write is always at or behind the reads.

```
processing row 2, dp = [4, 1, 8, 3]

col=0: dp[0] = 6 + min(dp[0]=4, dp[1]=1) = 7   → dp = [7, 1, 8, 3]
col=1: dp[1] = 5 + min(dp[1]=1, dp[2]=8) = 6   → dp = [7, 6, 8, 3]
                       ↑ still the old value ✅ (we overwrote dp[0], not dp[1])
col=2: dp[2] = 7 + min(dp[2]=8, dp[3]=3) = 10  → dp = [7, 6, 10, 3]
```

**Every read is of a not-yet-overwritten cell.** Sweeping right-to-left would break this.

**Why `triangle[-1][:]` and not `triangle[-1]`:** the slice **copies**. Without it you'd mutate the caller's last row, and `dp[col] = ...` would corrupt the input.
→ [list-slicing](../syntax/list-slicing.md)

**The in-place variant** writes directly into `triangle`, giving O(1) extra space — correct, and it destroys the input. **The rolling array is the better trade**, and it's what the follow-up asks for.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = triangle[-1][:]
```

**Seed with a copy of the last row.** A cell in the bottom row has no children, so its best cost from there down is just its own value.

⚠️ **The `[:]` is not optional** — it copies. Without it, `dp` aliases `triangle[-1]` and the writes below mutate the caller's data.
→ [list-slicing](../syntax/list-slicing.md) · [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md)

```python
for row in range(len(triangle) - 2, -1, -1):
```

**Sweep upward**, starting one row above the bottom (already seeded) and ending at row 0.

`range(start, -1, -1)` counts down to and including 0.

⚠️ If the triangle has a single row, `len - 2 = -1` and `range(-1, -1, -1)` is **empty** — the loop never runs and `dp[0]` is the lone value. **The `[[-10]]` case works with no special handling.**
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    for col in range(row + 1):
```

**Row `row` has `row + 1` entries**, indices `0..row`.

```python
        dp[col] = triangle[row][col] + min(dp[col], dp[col+1])
```

**The recurrence.** `dp[col]` and `dp[col+1]` currently hold the row *below*'s results — the two reachable children. Take the cheaper, then add this cell's own value.

⚠️ **`dp[col+1]` is always in range**, because `dp` still holds `row + 2` meaningful entries from the row below while `col` only reaches `row`. **This is why bottom-up needs no bounds checks.**

Left-to-right is required: the write at `col` never clobbers a value a later iteration reads.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return dp[0]
```

**A single cell** — the apex — holds the answer. No `min` over a row needed.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:

        dp = triangle[-1][:]

        for row in range(len(triangle) - 2, -1, -1):
            for col in range(row + 1):
                dp[col] = triangle[row][col] + min(dp[col], dp[col+1])

        return dp[0]
```

</details>

**Trace it** — `triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]`:

| Stage | `dp` | Computation |
|---|---|---|
| seed (row 3) | `[4, 1, 8, 3]` | the bottom row itself |
| **row 2** `[6,5,7]` | | |
|   col 0 | `[7, 1, 8, 3]` | `6 + min(4, 1)` = 6 + 1 |
|   col 1 | `[7, 6, 8, 3]` | `5 + min(1, 8)` = 5 + 1 |
|   col 2 | `[7, 6, 10, 3]` | `7 + min(8, 3)` = 7 + 3 |
| **row 1** `[3,4]` | | |
|   col 0 | `[9, 6, 10, 3]` | `3 + min(7, 6)` = 3 + 6 |
|   col 1 | `[9, 10, 10, 3]` | `4 + min(6, 10)` = 4 + 6 |
| **row 0** `[2]` | | |
|   col 0 | `[**11**, 10, 10, 3]` | `2 + min(9, 10)` = 2 + 9 ✅ |

**Answer: 11** ✅

**Reading the path forward from the answer:** the apex chose `dp[0] = 9` (left child), which chose `dp[1] = 6` (right child), which chose `dp[1] = 1` (left child). **So the path is 2 → 3 → 5 → 1**, exactly as the problem describes.

**Watch the stale entries.** After row 1 is processed, `dp = [9, 10, 10, 3]` — but only `dp[0]` and `dp[1]` are meaningful; `dp[2]` and `dp[3]` are leftovers from earlier rows. **They're never read again**, because the next row's loop only reaches `col = 0`. No cleanup required.

**Row 2, col 1 shows the left-to-right safety.** It reads `dp[1] = 1`, which is still the *original* seeded value — the previous iteration wrote to `dp[0]`, not `dp[1]`. ⚠️ **Sweeping right-to-left would have overwritten `dp[2]` before col 1 needed it.**

**The single-row case** `[[-10]]`: `dp = [-10]`, the loop body never executes, and `dp[0] = -10` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)** where `n` is the number of rows.

| Component | Cost |
|---|---|
| Row `r` | **r + 1** cells |
| Total cells | `1 + 2 + … + n` = **n(n+1)/2** → **O(n²)** |
| Work per cell | **O(1)** — one `min`, one add |

At n = 200 that's `200 × 201 / 2 = 20,100` cells. Instant.

**This is optimal** — every cell must be examined, since any could sit on the optimal path. **Ω(n²) is the lower bound**, and the triangle genuinely has Θ(n²) elements.

**Note the input size is n² even though the "length" is n** — a 200-row triangle holds 20,100 numbers. **So O(n²) is linear in the input**, which is worth saying precisely.

**Versus brute force:** every path makes n−1 binary choices, giving **2ⁿ⁻¹ paths** — 2¹⁹⁹ at the limit. The DP works because paths share suffixes, and each cell's best downstream cost is computed once.

**Top-down is also O(n²)**, so the sweep direction is about clarity and the final step, not speed:

| | Bottom-up | Top-down |
|---|---|---|
| Boundary checks | **none** ✅ | needed at both ends |
| Final answer | **`dp[0]`** ✅ | `min(dp)` over the last row |
| Complexity | O(n²) | O(n²) |

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — a single array the width of the bottom row. **This is exactly what the problem's follow-up asks for.**

| Component | Size |
|---|---|
| `dp` | n values → **O(n)** |
| **Total** | **O(n)** |

At n = 200 that's 200 integers rather than a 20,100-cell table.

| Approach | Space |
|---|---|
| Full 2-D table | O(n²) = 20,100 |
| **Rolling array** | **O(n) = 200** ✅ |
| In-place on `triangle` | O(1) — ⚠️ destroys the input |

**Why one array suffices:** computing row `r` needs only row `r+1`, and writing left-to-right guarantees each read happens before its cell is overwritten. **The array is reused for every row without ever being resized.**

**Can it be O(1)?** Only by mutating `triangle` itself. Correct, and it changes the caller's data — **name the trade rather than presenting it as free.**

⚠️ **`dp = triangle[-1][:]` versus `dp = triangle[-1]`** is the difference between O(n) extra space and accidental in-place mutation. The slice is what keeps the input intact.

**No recursion** — iterative. A memoised recursive version would be up to 200 frames deep here (safe), but the sweep avoids the question entirely.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I sweep bottom-up rather than top-down, and that choice removes two annoyances. Going upward, every cell's two children are at `col` and `col+1` in the row below, and both are guaranteed to exist because each row is exactly one longer — so there are no boundary checks. And the answer ends up in a single cell, `dp[0]`, instead of needing a `min` over the whole last row. I seed the array with a copy of the bottom row and work upward, replacing each entry with its own value plus the cheaper of its two children. One array is enough since each row only needs the one below it, and writing left to right is safe because I write to `col` while reading `col` and `col+1`, so I never clobber a value I still need. That's O(n²) time — which is linear in the input, since a triangle of n rows holds about n²/2 numbers — and O(n) space, which is what the follow-up asks for. Greedy fails: stepping to the smaller child can lead into an expensive region."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why bottom-up rather than top-down?" | **The question.** No boundary checks (both children always exist), and the answer is one cell instead of a `min` over a row. |
| "How do you get O(n) space?" | One rolling array, reused per row, written left-to-right so no needed value is overwritten. |
| "Why does left-to-right not corrupt values?" | You write to `col` and read `col` and `col+1` — the write is always at or behind the reads. Right-to-left would break it. |
| "Why the `[:]` on the seed?" | It copies. Without it you'd mutate the caller's bottom row. |
| "Why not greedy?" | A cheap child can lead into an expensive region — e.g. `[[1],[2,3],[100,100,1]]` gives 103 instead of 5. |
| "Can you do O(1) space?" | Yes, by mutating `triangle` in place — at the cost of destroying the input. |
| "Return the actual path?" | Keep the full table and walk down from the apex, choosing whichever child matches the recorded value. |
| "Does anything change with negative numbers?" | No — the DP handles them. ⚠️ It's greedy and any "costs only increase" pruning that break. |
| "**Maximum** path sum instead?" | Swap `min` for `max`. Nothing else changes. |

**Traps:**

- **`dp = triangle[-1]` without the slice** — mutates the caller's input.
- **Sweeping right-to-left** in the inner loop — overwrites `dp[col+1]` before it's read.
- **Greedy** — fails whenever a cheap step leads into an expensive region.
- **Top-down without boundary guards** — index 0 has no left parent, index `r` has no right parent.
- **Returning `min(dp)`** in the bottom-up version — the answer is `dp[0]` alone; `min` over stale entries could be smaller and wrong.
- **Resizing `dp` each row** — unnecessary; stale entries are simply never read.
- **Assuming values are positive** — they can be negative, so no early termination is valid.

**This same move shows up in:** [Minimum Falling Path Sum](931-minimum-falling-path-sum.md) (the same rolling minimisation with three children instead of two) · [Minimum Path Sum](64-minimum-path-sum.md) (the same recurrence on a rectangular grid) · [Unique Paths II](63-unique-paths-ii.md) (the rolling-row reduction, counting instead of minimising) · [Dungeon Game](174-dungeon-game.md) (another problem where sweeping backwards is what makes it tractable) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
