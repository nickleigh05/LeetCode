# 221. Maximal Square

**Medium** · [LeetCode](https://leetcode.com/problems/maximal-square/) · [Solution file (no hints)](../../problems/0001-0499/221.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Find the largest **square** submatrix containing only `'1'`s, and return its **area**.

```
matrix = [["1","0","1","0","0"],
          ["1","0","1","1","1"],     →  4      a 2×2 square of 1s
          ["1","1","1","1","1"],
          ["1","0","0","1","0"]]

matrix = [["0","1"],["1","0"]]  →  1
matrix = [["0"]]                →  0
```

**Constraints:** `1 <= m, n <= 300` · entries are the **characters** `'0'` / `'1'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**square**", not rectangle | ⚠️ One dimension to track (the side), not two |
| "containing only 1's" | Every cell in the square must be land |
| "return its **area**" | ⚠️ Square the side length at the end — easy to forget |
| `matrix[i][j]` is `'0'` or `'1'` | ⚠️ **Characters**, not ints — compare against `'1'` |
| `1 <= m, n <= 300` | 90,000 cells; O(m·n) is comfortable, O((mn)²) is not |

**The state that makes this work:**

> **`dp[r][c]` = the side length of the largest all-1s square whose *bottom-right corner* is at `(r, c)`.**

Anchoring at the bottom-right corner is what turns a 2-D search into a 1-D quantity per cell. And then the recurrence is surprisingly tight:

```
if matrix[r][c] == '1':
    dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1
else:
    dp[r][c] = 0
```

**Why `min` of exactly those three.** For a square of side `k` to end at `(r,c)`, three squares of side `k−1` must exist — ending just above, just left, and diagonally up-left:

```
    ┌───────┬───┐
    │       │   │        the k-1 square ending at (r-1, c)      ← above
    │  ...  │   │        the k-1 square ending at (r, c-1)      ← left
    ├───────┼───┤        the k-1 square ending at (r-1, c-1)    ← diagonal
    │       │ ▓ │  ← (r, c)
    └───────┴───┘
```

**The smallest of the three is the binding constraint**, hence `min`, and this cell adds one more layer, hence `+ 1`.

⚠️ **Why the diagonal term is not redundant**, which is the question people get wrong. It's tempting to think "above and left already cover everything". They don't — here's the counterexample:

```
1 1
1 0        →  dp at the bottom-right is 0 (it's a '0'), fine

but consider:
1 1 1
1 1 1
1 1 0      at (2,2) if it were '1':  above = 2, left = 2, diagonal = 2 → 3 ✅

versus:
0 1 1
1 1 1
1 1 1      at (2,2):  above = 2, left = 2, but DIAGONAL = 1
                       min(2,2,1) + 1 = 2, not 3  ✅ correct — the top-left
                       corner is a 0, so no 3×3 square exists
```

**Without the diagonal you'd report 3 and be wrong.** The diagonal is what checks the far corner of the prospective square.

🤔 **Before you open the next section:** you need `dp[r-1][c-1]` — the diagonal. If you're sweeping a single row left to right, has that value already been overwritten by the time you need it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Check every square | For each corner, test all sizes | O((m·n)·min(m,n)²) | O(1) | ❌ ~10¹² at 300×300 |
| Prefix sums + binary search | Test size `k` in O(1) | O(m·n·log) | O(m·n) | ✅ Works, more machinery |
| **2-D DP** | Side length per corner | **O(m·n)** | O(m·n) | ✅ Clearest |
| **1-D rolling DP** | One row + saved diagonal | **O(m·n)** | **O(n)** | ✅ ← |

**The decision: the rolling 1-D DP.**

⚠️ **The rolling reduction is the tricky part here**, because the recurrence needs the diagonal. Sweeping left-to-right through one array:

```
dp[c]     not yet written  →  dp[r-1][c]     (above)     ✓
dp[c-1]   already written  →  dp[r][c-1]     (left)      ✓
dp[r-1][c-1]  the diagonal →  was in dp[c-1] BEFORE it was overwritten  ✗
```

**The diagonal is destroyed one step before you need it.** The fix is a single saved variable:

```python
prev = 0                    # holds dp[r-1][c-1]
for c in range(1, cols + 1):
    temp = dp[c]            # stash dp[r-1][c] before overwriting
    ...use prev as the diagonal...
    prev = temp             # becomes the diagonal for c+1
```

**This is exactly the `prev`/`temp` dance from [Uncrossed Lines](1035-uncrossed-lines.md) and [Maximum Length of Repeated Subarray](718-maximum-length-of-repeated-subarray.md)** — and it's the canonical answer to "how do I roll a DP that needs the diagonal?"

**The 1-offset indexing removes every boundary check.** Sizing `dp` as `cols + 1` and treating index 0 as a virtual column of zeros means:

```
dp[0] is always 0  →  the first real column correctly gets min(..., 0, ...) + 1 = 1
```

**No `if r == 0 or c == 0` special case anywhere.** ⚠️ The cost is that `matrix[r][c-1]` needs the `-1` to convert back to the 0-indexed grid — a standard but easy-to-miss offset.

**Why the `else: dp[c] = 0` is mandatory**, exactly as in [718](718-maximum-length-of-repeated-subarray.md): with a reused array, *not* writing leaves the previous row's value in place. **A `'0'` cell must actively reset, or a stale side length leaks across rows.**

**Why not the brute-force square check.** For each of 90,000 cells, testing squares of every size costs O(min(m,n)²) — about 10¹² operations total. **The DP's insight is that a square of side `k` is built from three squares of side `k−1`**, so each cell's answer is O(1) given its neighbours.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(matrix), len(matrix[0])
dp = [0] * (cols + 1)
best = 0
```

**`dp[c]` = the side of the largest square ending at column `c-1` of the row processed so far.**

`cols + 1` gives a virtual zero column at index 0, removing the left-edge special case. `best` tracks the largest side seen anywhere.
→ [list-basics](../syntax/list-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
for r in range(rows):
    prev = 0
```

⚠️ **`prev` = `dp[r-1][c-1]`, the diagonal**, reset to 0 at each row's start (the virtual column before the grid).
→ [for-loop](../syntax/for-loop.md)

```python
        for c in range(1, cols + 1):
            temp = dp[c]
```

**Stash `dp[r-1][c]` before it's overwritten** — it becomes the diagonal for the *next* column.

**Forgetting this is the defining bug**: you'd use a current-row value as the diagonal and overcount.

```python
            if matrix[r][c-1] == '1':
                dp[c] = min(dp[c], dp[c-1], prev) + 1
                best = max(best, dp[c])
```

**The recurrence.** ⚠️ Note the three arguments and where each comes from:

| Term | Which neighbour |
|---|---|
| `dp[c]` | **above** — still the previous row |
| `dp[c-1]` | **left** — already written this row |
| `prev` | **diagonal** — the saved value |

⚠️ **`matrix[r][c-1]`** — the `-1` converts from the 1-offset DP index back to the 0-indexed grid.

⚠️ **Compare against the string `'1'`**, not the integer `1`. The problem gives characters, and `matrix[r][c-1] == 1` is silently always `False` in Python — **every answer would be 0, with no error.**

`best` is updated inside the match branch, since a `'0'` cell contributes nothing.
→ [min-max-key](../syntax/min-max-key.md) · [string-basics](../syntax/string-basics.md)

```python
            else:
                dp[c] = 0
```

⚠️ **Explicit reset.** A `'0'` cell can end no square, and with a reused array the value must be actively cleared or the previous row's leaks through.

```python
            prev = temp

    return best * best
```

⚠️ **Square it** — `best` is the side length; the problem asks for **area**.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:

        rows, cols = len(matrix), len(matrix[0])
        dp = [0] * (cols + 1)
        best = 0

        for r in range(rows):
            prev = 0
            for c in range(1, cols + 1):
                temp = dp[c]
                if matrix[r][c-1] == '1':
                    dp[c] = min(dp[c], dp[c-1], prev) + 1
                    best = max(best, dp[c])
                else:
                    dp[c] = 0
                prev = temp

        return best * best
```

</details>

**Trace it** — the Example 1 matrix. Verified output, showing `dp[1..5]` after each row:

| Row | matrix row | `dp` after | best side |
|---|---|---|---|
| 0 | `10100` | `[1, 0, 1, 0, 0]` | **1** |
| 1 | `10111` | `[1, 0, 1, 1, 1]` | 1 |
| 2 | `11111` | `[1, 1, 1, **2**, **2**]` | **2** |
| 3 | `10010` | `[1, 0, 0, 1, 0]` | 2 |

**Area = 2² = 4** ✅

**Row 2 is where the 2×2 square is found.** At column 4 (grid index 3):

```
above    = dp[4] from row 1 = 1
left     = dp[3] from row 2 = 1
diagonal = prev (dp[3] from row 1) = 1
min(1,1,1) + 1 = 2  ✅
```

**All three neighbours had side 1, so a 2×2 square closes here** — the block spanning rows 1–2, columns 3–4.

**Row 2, column 3 shows the `min` doing real work.** Above is `dp[3]` from row 1 = 1, left is `dp[2]` from row 2 = 1, diagonal is 1 → gives 2. But at **column 2**: above = 0 (row 1 had `'0'` there), so `min(0, 1, 0) + 1 = 1` — **the zero above caps it at 1**, correctly, since there's no 2×2 square with that corner.

**Row 3 shows the resets.** The row is `10010`, so columns 2, 3 and 5 are `'0'` and get zeroed. ⚠️ **Without `else: dp[c] = 0`, they would still hold row 2's values of 1, 1 and 2** — and row 4 (if it existed) would build on squares that don't exist.

**Example 3** (`[["0"]]`): the single cell is `'0'`, `best` stays 0, and the answer is `0 * 0 = 0` ✅ — the area, not the side, and not 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m·n)** — one visit per cell, O(1) work each (a three-way `min` and two comparisons).

At 300×300 that's **90,000 operations**. Instant.

**This is optimal**: every cell must be read, since any could be part of the largest square. **Ω(m·n) is the lower bound.**

**Versus brute force**, checking each possible square directly:

| | Complexity | At 300×300 |
|---|---|---|
| Test every square at every corner | O(m·n·min(m,n)²) | ~8 × 10¹¹ ❌ |
| **DP** | **O(m·n)** | **9 × 10⁴** ✅ |

**Seven orders of magnitude.** The DP's leverage is that `dp[r-1][c]`, `dp[r][c-1]` and `dp[r-1][c-1]` already summarise everything about the region above-left — **a square of side `k` is exactly three squares of side `k−1` plus one cell.**

**A prefix-sum approach** also works: precompute 2-D prefix sums in O(m·n), then testing "is the `k × k` square at this corner all 1s?" is O(1), and you binary-search `k` per cell → O(m·n·log(min(m,n))). **Correct, but a log factor worse and more code.**

⚠️ **The largest *rectangle* is a genuinely harder problem** — [Maximal Rectangle](85-maximal-rectangle.md) needs a monotonic-stack histogram pass per row, because a rectangle has two independent dimensions and this single-number-per-cell trick collapses. **Squares are easy precisely because one number suffices.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — one row plus three scalars.

| Component | Size |
|---|---|
| `dp` | cols + 1 values → **O(n)** |
| `prev`, `temp`, `best` | three integers → O(1) |
| **Total** | **O(n)** |

At 300×300 that's 301 integers instead of 90,000.

| Approach | Space |
|---|---|
| Full 2-D table | O(m·n) = 90,000 |
| **Rolling row + `prev`** | **O(n) = 301** ✅ |
| Mutate the input | ⚠️ can't — it holds **characters**, not ints |

⚠️ **In-place mutation is awkward here**, unlike [Minimum Path Sum](64-minimum-path-sum.md), because the matrix holds `'0'`/`'1'` **strings**. You'd have to convert types as you go, which is messier than just keeping a row.

**The single `prev` variable replaces an entire second row** — that's the neat part, and it's the same trick as [Uncrossed Lines](1035-uncrossed-lines.md) and [718](718-maximum-length-of-repeated-subarray.md). **Whenever a rolling DP needs the diagonal, one scalar suffices.**

**Roll along the shorter dimension** for O(min(m,n)) — transpose if `m < n`.

⚠️ **The trade for O(n):** you lose the *position* of the best square. **Track the ending `(r, c)` alongside `best` if you need it** — one extra pair, still O(n).

**No recursion** — iterative throughout.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I define `dp[r][c]` as the side length of the largest all-ones square whose bottom-right corner is at that cell. That anchoring is what makes it a single number per cell instead of a 2-D search. If the cell is a 1, the side is one more than the minimum of the three neighbours — above, left, and diagonal — because a square of side k needs three squares of side k−1 at those positions. The diagonal isn't redundant: it's what verifies the far corner. If the cell is a 0, the side is 0. I roll it into a single array, which needs one saved variable, because the diagonal `dp[r-1][c-1]` gets overwritten one step before I need it — so I stash it in `prev` before each write. Two details that bite: the matrix holds character `'1'`s, not integers, so comparing to `1` silently returns 0 everywhere; and the answer is the *area*, so I square the side at the end. O(m·n) time and O(n) space. Worth noting the largest *rectangle* is much harder — you'd need a monotonic stack per row, since a rectangle has two independent dimensions."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why the **diagonal** term?" | **The question.** It verifies the far corner. With only above and left you'd report a 3×3 square when the top-left cell is a 0. |
| "Why `min` and not `max`?" | The smallest of the three neighbours is the binding constraint — the square can only be as big as its weakest supporting corner allows. |
| "What does `prev` hold?" | `dp[r-1][c-1]`, the diagonal, saved before the sweep overwrites it. One scalar replaces a whole second row. |
| "Why the explicit `else: dp[c] = 0`?" | With a reused array, not writing leaves the previous row's value. A fresh 2-D table wouldn't need it. |
| "Largest **rectangle** instead?" | Much harder — [Maximal Rectangle](85-maximal-rectangle.md), treating each row as a histogram and running a monotonic stack. The single-number trick doesn't generalise. |
| "Return the square's position?" | Track the `(r, c)` where `best` was set; the square spans back `best` rows and columns. |
| "Why `cols + 1`?" | The virtual zero column removes the left-edge boundary check. The cost is the `-1` when indexing `matrix`. |
| "Alternative approach?" | 2-D prefix sums plus binary search on the side: O(m·n·log). Correct, a log factor worse. |
| "What if it were a **cube** in 3-D?" | Same idea with seven neighbours — `min` over all of them plus one. |

**Traps:**

- **Comparing to `1` instead of `'1'`.** The matrix holds characters, so the test is silently always false and the answer is 0. **No error is raised** — the defining bug.
- **Returning `best` instead of `best * best`** — the side, not the area.
- **Omitting the diagonal from the `min`** — reports squares that don't exist.
- **Forgetting `temp`/`prev`** — the diagonal is read from the current row.
- **Omitting `else: dp[c] = 0`** — stale side lengths leak across rows.
- **Off-by-one on `matrix[r][c-1]`** — `dp` is 1-offset, the matrix is not.
- **Using `max` instead of `min`** — reports squares far larger than reality.
- **Not resetting `prev = 0`** at each row's start.

**This same move shows up in:** [Maximal Rectangle](85-maximal-rectangle.md) (the harder two-dimension version) · [Uncrossed Lines](1035-uncrossed-lines.md) and [Maximum Length of Repeated Subarray](718-maximum-length-of-repeated-subarray.md) (the same `prev`-saves-the-diagonal trick) · [Minimum Falling Path Sum](931-minimum-falling-path-sum.md) (another rolling DP where a naive in-place sweep corrupts a needed value) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
