# 62. Unique Paths

**Medium** · [LeetCode](https://leetcode.com/problems/unique-paths/) · [Solution file (no hints)](../../problems/0001-0499/62.py)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

---

A robot sits at the **top-left** corner of an `m × n` grid. It can only move **right** or **down**. How many **unique paths** are there to the **bottom-right** corner?

```
m = 3, n = 7   →  28
m = 3, n = 2   →  3      down-down-right, down-right-down, right-down-down
m = 1, n = 1   →  1      already there
```

**Constraints:** `1 <= m, n <= 100` · the answer is guaranteed to fit in a 32-bit integer.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "how many **unique paths**" | Counting, so the combining operator is `+`. Same family as [Climbing Stairs](70-climbing-stairs.md) — but now the state is two-dimensional |
| "only **right or down**" | Two choices per step, and both move you **strictly closer** to the goal. No backtracking is possible, so there are no cycles and no visited set |
| a grid, not an array | The state is a **coordinate pair** `(row, col)`, not a single index. That's what makes this 2-D DP |
| no obstacles mentioned | Every cell is passable. (Add obstacles and you get [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) — a small change to the recurrence) |
| `m, n <= 100` | m × n = 10⁴ cells. Anything polynomial is fine — but note 2^(m+n) is not, so brute-force enumeration is out |

Apply the same backwards question as every DP, just in two dimensions: **you're standing at cell `(r, c)`. Where did you come from?**

Only two possibilities, because the moves are only right and down: you arrived from **above** `(r-1, c)` or from the **left** `(r, c-1)`. Those two cases are disjoint — they differ in your last move — so the counts add:

```
paths(r, c) = paths(r−1, c) + paths(r, c−1)
```

And the base cases fall out of the geometry: **the entire first row and first column are 1**. There's exactly one way to travel in a straight line — along the top edge you can only ever go right, along the left edge you can only ever go down.

That's [Climbing Stairs](70-climbing-stairs.md) promoted to a grid. Same "sum the ways from the places you could have come from," same counting, one more dimension.

🤔 **Before you open the next section:** every path from corner to corner consists of exactly the same number of moves, no matter which route you take. How many moves, and how many of them are "down"? If you can answer that, there's a closed form hiding here.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate every path | DFS from the start, count the arrivals | **O(2^(m+n))** | O(m+n) | ❌ Exponential. The number of paths *is* the answer, and it's ~10⁵⁷ at the limits |
| Recursion + memo | Same, cached on `(r, c)` | O(m·n) | O(m·n) + stack | ⚠️ Correct; carries a cache and up to m+n frames |
| Full 2-D DP grid | Fill an `m × n` table row by row | O(m·n) | **O(m·n)** | ⚠️ Correct, and the clearest first draft — but it stores every cell when only one row is ever read |
| **One rolling row** | Keep a single row, overwrite it as you sweep | O(m·n) | **O(n)** | ✅ |
| Combinatorics | `C(m+n−2, m−1)` | **O(min(m,n))** | O(1) | ⚠️ Optimal, and genuinely correct here — but it evaporates the moment obstacles appear |

**The decision:** the recurrence with **one rolling row** — O(m·n) time, O(n) space.

**The space reduction is the point of this problem**, and it's the 2-D version of the trick from [Climbing Stairs](70-climbing-stairs.md). Look at `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Computing row `r` reads **only row `r-1`** and cells to the left within row `r` itself. Rows `r-2` and earlier are dead. So you never need the whole table — one row's worth of storage suffices, updated in place.

**The rule generalizes cleanly:** in 1-D, a fixed-width lookback meant a fixed number of *variables*; in 2-D, depending only on the previous row means a fixed number of *rows*. Same principle, one dimension up.

**The closed form, and why not to lead with it.** Every path is exactly `(m−1) + (n−1)` moves long — you must go down `m−1` times and right `n−1` times, in some order. A path is therefore just a choice of *which* of those moves are the downs:

```
paths = C(m + n − 2, m − 1)
```

For `m=3, n=7`: `C(8, 2)` = 28 ✓. It's O(min(m,n)) and exact.

So why write the DP? Because the combinatorial answer is **brittle** — it works only for a completely empty grid. Add one obstacle, make the grid non-rectangular, weight the cells, and it's gone; the DP survives all of those with a one-line change. In an interview, write the DP and *mention* the closed form. Leading with the formula risks looking like you've memorized this specific puzzle rather than understood the technique.

**Why not memoized recursion?** Same complexity, but m+n = 200 stack frames and a dict of 10⁴ entries, versus one array of 100 integers. Bottom-up is strictly leaner here.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
row = [1] * n
```
**The bottom row of the grid**, and it's all 1s.

This implementation works **backwards** — from the destination toward the start — so `row[j]` means *"how many paths from this cell to the bottom-right corner."* On the bottom row you can only move right, so there's exactly one path from every cell. Same reasoning as the forward version's first row, mirrored.
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(m - 1):
```
Move up one row at a time, `m - 1` times — the bottom row already exists, so only the other `m−1` rows need computing.

`i` is never used inside the body: it's a **counter, not an index**. That's the signal that only *one* row exists at a time, with no row index to track.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    new_row = [1] * n
```
The row being built. Initializing to 1s pre-seeds the **rightmost cell** — `new_row[n-1]` stays 1, because from the last column you can only go straight down, giving exactly one path. That's the column base case, handled by initialization rather than a special branch.
→ [list-basics](../syntax/list-basics.md)

```python
    for j in range(n - 2, -1, -1):
```
Sweep **right to left**, from the second-to-last column down to 0. The last column is skipped because its 1 is already correct.

The direction matters: `new_row[j]` depends on `new_row[j + 1]`, the cell to its **right** — so that cell must already be final. Sweeping left-to-right would read a stale value. This is the same "fill order must respect the dependency direction" constraint as [Word Break](139-word-break.md)'s backwards loop.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        new_row[j] = new_row[j + 1] + row[j]
```
**The recurrence**, in the backwards framing: paths from `(r, c)` to the corner = paths going **right** first + paths going **down** first.

- `new_row[j + 1]` — the cell to the right, in the row being built.
- `row[j]` — the cell directly below, in the previous (lower) row.

Two variables holding two rows is the whole space optimization: `row` is "the row below," `new_row` is "the row I'm computing."
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md) · [nested-lists](../syntax/nested-lists.md)

```python
    row = new_row
```
Slide up. What was just computed becomes "the row below" for the next iteration — the 2-D analogue of the rolling-variable slide in [Climbing Stairs](70-climbing-stairs.md).
→ [variables-assignment](../syntax/variables-assignment.md)

```python
return row[0]
```
After all `m−1` iterations, `row` is the **top** row, and `row[0]` is the top-left cell — the number of paths from the start to the corner.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        row = [1] * n

        for i in range(m - 1):
            new_row = [1] * n
            for j in range(n - 2, -1, -1):
                new_row[j] = new_row[j + 1] + row[j]
            row = new_row
        return row[0]
```
</details>

**Trace it** — `m = 3`, `n = 3` (answer should be 6)

Start: `row = [1, 1, 1]` — the bottom row.

**Iteration 1** (building the middle row), sweeping `j = 1, 0`:

| `j` | `new_row[j+1]` (right) | `row[j]` (below) | `new_row[j]` |
|---|---|---|---|
| 2 | — | — | 1 (pre-seeded) |
| 1 | 1 | 1 | **2** |
| 0 | 2 | 1 | **3** |

`row` becomes `[3, 2, 1]`.

**Iteration 2** (building the top row):

| `j` | right | below | `new_row[j]` |
|---|---|---|---|
| 2 | — | — | 1 |
| 1 | 1 | 2 | **3** |
| 0 | 3 | 3 | **6** |

`row` becomes `[6, 3, 1]`, and `row[0]` = **6** ✅

Laid out as the full grid — each cell showing paths from there to the corner — the shape is easy to see:

```
6  3  1
3  2  1
1  1  1
```

The bottom row and right column are all 1s (straight-line paths), and every other cell is the sum of its right and below neighbours. Reading it as a forward grid instead gives the mirrored triangle, which is Pascal's triangle rotated — the visual reason the closed form is a binomial coefficient.

**Check the formula:** `C(m+n−2, m−1)` = `C(4, 2)` = **6** ✓

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

- The outer loop runs **m − 1** times.
- The inner loop runs **n − 1** times.
- Each inner iteration does one addition and one assignment — **O(1)**.
- Allocating `new_row` is O(n) per outer iteration, which totals O(m·n) and doesn't change the class.
- (m−1) × (n−1) × O(1) = **O(m · n)**.

At the limits, 100 × 100 = **10⁴** operations. Instant.

**Against the alternatives:** enumerating paths is **O(2^(m+n))** — and note the number of paths is itself astronomically large (`C(198, 99)` ≈ 10⁵⁸ at the limits), so *any* approach that visits each path individually is doomed regardless of cleverness. The DP works because it counts paths **without enumerating them**, collapsing 10⁵⁸ routes into 10⁴ cells.

That's a good sentence to have ready: **the answer being astronomically large doesn't mean computing it has to be.**

**Faster?** Yes — the closed form `C(m+n−2, m−1)` computes in **O(min(m,n))** multiplications and divisions, with no table at all. It's strictly better *for this exact problem* and useless the moment the grid gains an obstacle.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — two rows of `n` integers exist at a time (`row` and `new_row`), and 2 × O(n) is O(n).

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(m·n)** | A cache entry per cell, plus up to m+n stack frames |
| Full 2-D DP grid | **O(m·n)** | The whole table — 10⁴ integers at the limits |
| **One rolling row** | **O(n)** | Row `r` reads only row `r−1`, so older rows are dead |
| Combinatorics | **O(1)** | No table at all |

**The generalization worth carrying forward.** In Unit 13, `dp[i]` depending on a *fixed window of previous entries* meant you could replace the array with that many variables. Here, `dp[r][c]` depends only on the **previous row** — so you can replace the table with that many rows. **Same rule, one dimension up:** keep exactly as much history as the recurrence reads.

This applies to most of Unit 14. [Longest Common Subsequence](1143-longest-common-subsequence.md) reads only the previous row, so it collapses from O(m·n) to O(n) the same way.

**One more step is possible:** you can drop `new_row` entirely and update `row` in place, since each cell only needs its right neighbour (already updated) and its below neighbour (not yet overwritten at that index). That halves the memory to a single array. Slightly harder to read, and a good thing to offer rather than to write first.

**Can you pick which dimension to pay for?** Yes — keeping a rolling *column* instead gives O(m). So the honest bound is **O(min(m, n))** if you orient the loops to sweep along the longer side.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "To reach any cell you either came from above or from the left, and those cases are disjoint, so the counts add: `paths(r,c) = paths(r-1,c) + paths(r,c-1)`. The first row and column are all 1, since there's exactly one straight-line path along each edge. That's Climbing Stairs in two dimensions. The full table is O(m·n) space, but computing a row only ever reads the previous row — so I keep one rolling row and get O(n). I sweep in a direction that guarantees the neighbour I depend on is already final. O(m·n) time. There's also a closed form: every path is exactly m+n−2 moves of which m−1 are down, so the answer is `C(m+n-2, m-1)` — O(min(m,n)) and exact. I'd still write the DP, because the formula breaks as soon as there are obstacles."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it in O(1) space?" | With the closed form, yes: `C(m+n−2, m−1)`, computed multiplicatively to avoid huge factorials. But it only works on an empty rectangular grid. |
| "What if some cells are blocked?" | [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/). Set blocked cells to 0 instead of applying the recurrence, and be careful that a blocked cell in the first row/column zeroes everything after it. The closed form dies; the DP needs one extra line. |
| "Why is the answer a binomial coefficient?" | Every path is a sequence of m−1 downs and n−1 rights in some order. Choosing a path *is* choosing which positions in that sequence are downs — hence `C(m+n−2, m−1)`. |
| "Can you halve the space again?" | Yes — update a single row in place. Each cell needs its right neighbour (already updated this pass) and its below neighbour (not yet overwritten). One array instead of two. |
| "What if diagonal moves were allowed?" | Add a third term: `dp[r][c] = above + left + diagonal`. That's the Delannoy numbers, and the closed form no longer applies. |
| "Minimum path *sum* instead of a count?" | Swap `+` for `min` and add the cell's own cost — that's [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/). Same grid recurrence, different combining operator, exactly like counting-vs-optimizing in Unit 13. |
| "Why sweep right to left here?" | Because `new_row[j]` reads `new_row[j+1]`. The fill order has to make the dependency already-final; left to right would read stale values. |
| "What about overflow?" | Python ints are arbitrary precision, so nothing to do. In Java/C++ you'd need care — the problem guarantees the answer fits in 32 bits, but a naive factorial in the closed form would overflow long before that. |

**Traps:**
- **Sweeping the inner loop in the wrong direction.** With `new_row[j+1]` as a dependency you must go right-to-left. This is the kind of bug that produces plausible-looking wrong numbers.
- Forgetting that the first row *and* first column are both all 1s. Setting only one gives zeros propagating through the table.
- Looping `range(m)` instead of `range(m - 1)` — one row too many, and the answer is the count for an `m+1` grid.
- Reaching for the combinatorial formula first and being stuck when the follow-up adds obstacles.
- Trying to enumerate paths, even with memo-free recursion. The answer can be ~10⁵⁸; you cannot touch each path.
- Confusing `m` and `n` in the closed form. `C(m+n−2, m−1)` and `C(m+n−2, n−1)` are equal by symmetry, so this one is forgiving — but the DP's dimensions are not.

**This same move shows up in:** [Climbing Stairs](70-climbing-stairs.md) (the same counting recurrence in one dimension) · [Longest Common Subsequence](1143-longest-common-subsequence.md) (a grid DP that collapses to one rolling row the same way) · [Coin Change II](518-coin-change-ii.md) (counting combinations where the *loop order* carries meaning) · [Interleaving String](97-interleaving-string.md) (a 2-D grid over two strings, with the same previous-row dependency).

</details>

---
