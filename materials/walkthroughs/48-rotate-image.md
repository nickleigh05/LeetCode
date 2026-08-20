# 48. Rotate Image

**Medium** · [LeetCode](https://leetcode.com/problems/rotate-image/) · [Solution file (no hints)](../../problems/0001-0499/48.py)

[📖 18. Math & Geometry lesson](../learning/18-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Math & Geometry problems](../rmap-practice/18-math-geometry.md)

---

You're given an `n × n` 2-D `matrix` representing an image. Rotate it by **90 degrees clockwise**, **in place** — you must modify the input directly and may **not** allocate another 2-D matrix.

```
[[1,2,3],          [[7,4,1],
 [4,5,6],    →      [8,5,2],
 [7,8,9]]           [9,6,3]]

[[5,1,9,11],       [[15,13, 2, 5],
 [2,4,8,10],   →    [14, 3, 4, 1],
 [13,3,6,7],        [12, 6, 8, 9],
 [15,14,12,16]]     [16, 7,10,11]]
```

**Constraints:** `n == matrix.length == matrix[i].length` · `1 <= n <= 20` · `-1000 <= matrix[i][j] <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**in place**" | No second matrix. This is the entire difficulty — with O(n²) extra space it's a three-line problem |
| "**90 degrees clockwise**" | A specific direction. Counter-clockwise needs a different second step, so pin the direction down early |
| `n × n`, square | Rotation maps the matrix onto itself. A **rectangular** matrix would change shape and couldn't be rotated in place at all |
| `n <= 20` | Tiny — 400 cells. Performance is irrelevant; **correctness of the index arithmetic is the whole test** |

Start by working out where a single element goes. Under a 90° clockwise rotation:

> the element at `(row, col)` moves to `(col, n - 1 - row)`

Check it on the 3×3: `(0,0)` holds 1 and lands at `(0, 2)` — top-left goes to top-right ✓. `(2,0)` holds 7 and lands at `(0, 0)` — bottom-left goes to top-left ✓.

The direct approach is to **cycle four elements at a time**: each element and the three positions it displaces form a 4-cycle, and you rotate the whole cycle with one temporary variable. Do that for every cell in the top-left quadrant and the matrix is rotated. It works, and the index expressions are genuinely nasty.

**The much cleaner route is to factor the rotation into two simple operations.** Look at what a rotation does and ask whether two familiar flips compose into it:

**Step 1 — transpose** (reflect across the main diagonal, swapping `[i][j]` with `[j][i]`):

```
1 2 3        1 4 7
4 5 6   →    2 5 8
7 8 9        3 6 9
```

**Step 2 — reverse each row** (reflect left-right):

```
1 4 7        7 4 1
2 5 8   →    8 5 2
3 6 9        9 6 3
```

That's the answer. **Two reflections compose into a rotation** — a standard fact from geometry, and the reason this decomposition exists at all: reflecting across two lines that meet at angle θ produces a rotation by 2θ. The main diagonal and the vertical centre line meet at 45°, giving a 90° turn.

🤔 **Before you open the next section:** the transpose loop below runs `for j in range(i + 1, n)` rather than `range(n)`. What would happen if it started at 0 instead?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Build a new matrix | `result[j][n-1-i] = matrix[i][j]`, then copy back | O(n²) | **O(n²)** | ❌ Violates the in-place requirement |
| Rotate four elements at a time | For each cell in the top-left quadrant, cycle its 4 positions with one temp | O(n²) | **O(1)** | ⚠️ Correct and genuinely in place — but four gnarly index expressions, easy to botch |
| **Transpose, then reverse rows** | Two simple passes | O(n²) | **O(1)** | ✅ |
| `zip(*matrix)` then reverse | Pythonic one-liner | O(n²) | **O(n²)** | ❌ `zip` builds new tuples — not in place |

**The decision:** **transpose, then reverse each row.**

**Why it's worth decomposing.** The four-way cycle version is the "obvious" in-place approach, and it requires writing this correctly under pressure:

```python
temp = matrix[i][j]
matrix[i][j] = matrix[n-1-j][i]
matrix[n-1-j][i] = matrix[n-1-i][n-1-j]
matrix[n-1-i][n-1-j] = matrix[j][n-1-i]
matrix[j][n-1-i] = temp
```

Four index expressions, each mixing `i`, `j`, and `n-1`, in an order that must be exactly right. **The transpose-and-reverse version replaces all of that with `[i][j] ↔ [j][i]` and a call to `.reverse()`** — both of which are hard to get wrong. Same complexity, dramatically lower risk.

**Why two reflections make a rotation.** It's the composition rule from geometry: reflecting across two lines meeting at angle θ yields a rotation by 2θ. The main diagonal and the vertical mid-line meet at 45°, so transposing then flipping horizontally rotates by 90°. **Knowing that rule means you can derive the variants instead of memorizing them:**

| Target | Recipe |
|---|---|
| 90° **clockwise** | transpose, then reverse each **row** |
| 90° **counter-clockwise** | transpose, then reverse each **column** (or reverse rows first, then transpose) |
| 180° | reverse each row **and** each column (or reverse the row order and each row) |

**Why the transpose loop must start at `j = i + 1`** — the answer to section 1's question. If it started at 0, every pair would be swapped **twice**: once when visiting `(i, j)` and again at `(j, i)`. Two swaps cancel, so the matrix would come back unchanged. **Starting at `i + 1` visits each unordered pair exactly once**, and it also skips the diagonal, where `[i][i]` would swap with itself.

**Why not `zip(*matrix)`?** `list(zip(*matrix))` transposes elegantly, but it constructs new tuples — O(n²) extra space and a violation of the constraint. Fine to mention as the idiomatic non-in-place answer; not what's being asked.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(matrix)
```
The side length. Since the matrix is square, one dimension is all you need — and every index expression below relies on that squareness.
→ [nested-lists](../syntax/nested-lists.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```
**The transpose** — reflect across the main diagonal.

**`range(i + 1, n)` is the critical detail.** It restricts the sweep to the strict upper triangle, so each unordered pair `{(i,j), (j,i)}` is visited exactly once. Using `range(n)` would swap every pair twice and leave the matrix untouched — a bug that produces *no* visible change, which makes it unusually confusing to debug.

It also skips the diagonal itself (`j` starts *after* `i`), where a swap would be a no-op anyway.

The swap uses Python's [tuple assignment](../syntax/swap-tuple-assign.md): the entire right-hand side is evaluated before anything is written, so no temporary variable is needed and there's no ordering hazard.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [nested-lists](../syntax/nested-lists.md)

```python
for row in matrix:
    row.reverse()
```
**Reverse each row** — reflect left-right, completing the rotation.

[`.reverse()`](../syntax/list-methods.md) works **in place** on each row list, which is what keeps the space at O(1). The alternatives are traps: `row[::-1]` builds a *new* list and, assigned to the loop variable, wouldn't write back to the matrix at all; `reversed(row)` returns an iterator, not a list.

Iterating `for row in matrix` gives **references** to the actual row lists, so mutating them modifies the matrix directly.
→ [list-methods](../syntax/list-methods.md) · [for-loop](../syntax/for-loop.md) · [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:

        n = len(matrix)

        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for row in matrix:
            row.reverse()
```
</details>

**Trace it** — the 3×3 example

Start:

```
1 2 3
4 5 6
7 8 9
```

**Transpose.** The pairs visited, in order:

| `i` | `j` | swap | matrix after |
|---|---|---|---|
| 0 | 1 | `[0][1]`=2 ↔ `[1][0]`=4 | `1 4 3 / 2 5 6 / 7 8 9` |
| 0 | 2 | `[0][2]`=3 ↔ `[2][0]`=7 | `1 4 7 / 2 5 6 / 3 8 9` |
| 1 | 2 | `[1][2]`=6 ↔ `[2][1]`=8 | `1 4 7 / 2 5 8 / 3 6 9` |
| 2 | — | `range(3, 3)` is empty | unchanged |

```
1 4 7
2 5 8
3 6 9
```

Exactly **three** swaps for a 3×3 — one per pair above the diagonal, which is `n(n-1)/2 = 3`. The diagonal entries 1, 5, 9 never move, which is correct: **the main diagonal is the axis of reflection.**

**Reverse each row:**

| row before | row after |
|---|---|
| `1 4 7` | `7 4 1` |
| `2 5 8` | `8 5 2` |
| `3 6 9` | `9 6 3` |

```
7 4 1
8 5 2
9 6 3
```

✅ Matches the expected output.

**Spot-check the mapping:** the 7 started at `(2,0)` and ended at `(0,0)`. Using the formula `(row, col) → (col, n-1-row)`: `(2,0) → (0, 3-1-2) = (0,0)` ✓. And the 3 started at `(0,2)`, so `(0,2) → (2, 3-1-0) = (2,2)` — the bottom-right, where 3 indeed sits ✓.

**And what the `range(n)` bug would do:** the pair `{(0,1),(1,0)}` would be swapped at `i=0,j=1` and swapped **back** at `i=1,j=0`. Every pair reverts, the transpose is a no-op, and the final answer is just each row reversed — `3 2 1 / 6 5 4 / 9 8 7`. Wrong, and with no obvious symptom pointing at the loop bound.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**, where n is the side length.

- **Transpose** — the nested loops cover the strict upper triangle, which is `n(n-1)/2` pairs → **O(n²)**.
- **Reversing rows** — n rows, each reversed in O(n) → **O(n²)**.
- Total: **O(n²)**.

Note that O(n²) here means **linear in the number of cells** — there are n² of them, and each is touched a constant number of times (once by the transpose if off-diagonal, once by the reverse). Calling it "quadratic" is correct but slightly misleading; **it's optimal.**

At n = 20 that's 400 cells. Instant.

**Faster?** No. Every element must move (except the exact centre of an odd-sized matrix), so **Ω(n²)** is a hard lower bound — you cannot rotate a matrix without writing every cell.

**Constant-factor note:** the four-way cycle version touches each cell exactly **once**, while transpose-then-reverse touches most cells **twice**. So the cycle version is about 2× faster in principle. At n ≤ 20 that's irrelevant, and the readability trade is overwhelmingly worth it — but it's the honest answer if someone asks which is more efficient.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — genuinely constant. No matrix, no row, no list is allocated.

| Operation | Space | Why |
|---|---|---|
| The swap | **O(1)** | Python builds a transient 2-tuple, which is constant size |
| `row.reverse()` | **O(1)** | Reverses in place by swapping ends inward |
| `n`, `i`, `j`, `row` | O(1) | Scalars and a reference |

**The two traps that would silently break the in-place requirement**, both worth knowing:

- **`row[::-1]`** creates a new list. Assigning it to the loop variable (`row = row[::-1]`) rebinds the local name and **doesn't touch the matrix at all** — the function would return with the matrix transposed but not reversed.
- **`list(zip(*matrix))`** transposes beautifully and allocates an entirely new O(n²) structure.

Both are the kind of thing that looks Pythonic and quietly violates the constraint. **`.reverse()` and the tuple swap are the two operations that mutate rather than construct**, and that's exactly why they're the ones used.

**Why in-place is achievable at all:** the matrix is **square**, so a 90° rotation is a permutation of the existing cells — same shape, same count. For a rectangular `m × n` matrix the result would be `n × m`, a different shape, and no in-place rotation exists.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A 90° clockwise rotation sends `(row, col)` to `(col, n-1-row)`. I could rotate four elements at a time in a cycle, which is in place but means four index expressions that are easy to get wrong. Instead I'll factor the rotation into two reflections: transpose across the main diagonal, then reverse each row. That works because reflecting across two lines meeting at 45° produces a 90° rotation. The transpose loop has to start at `j = i + 1` — if it started at 0, every pair would be swapped twice and cancel out, leaving the matrix unchanged. And I use `row.reverse()` rather than slicing, because slicing builds a new list and wouldn't modify the matrix in place. O(n²) time, which is optimal since every cell has to move, and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Rotate counter-clockwise instead." | Transpose, then reverse each **column** — or equivalently reverse the row order first, then transpose. |
| "Rotate 180°." | Reverse the order of the rows and reverse each row. Or apply the 90° rotation twice. |
| "Why start the inner loop at `i + 1`?" | Otherwise every pair is swapped twice and the swaps cancel — the matrix comes out unchanged, with no obvious symptom. |
| "Why not `row[::-1]`?" | It builds a new list. Assigning it to the loop variable rebinds a local name without touching the matrix. `.reverse()` mutates in place. |
| "Do it with the four-way cycle." | For each cell in the top-left quadrant, cycle `(i,j) → (j,n-1-i) → (n-1-i,n-1-j) → (n-1-j,i)` with one temp. Same complexity, touches each cell once instead of twice, much easier to get wrong. |
| "What if the matrix were rectangular?" | You couldn't rotate in place — an `m × n` matrix becomes `n × m`, a different shape. You'd have to allocate a new matrix. |
| "Why is this O(1) space when you're moving n² elements?" | Because the moves are swaps between existing cells. Nothing new is allocated; the temporaries are constant-size. |
| "Can you beat O(n²)?" | No — every element changes position, so you must write every cell. Ω(n²) is a lower bound. |

**Traps:**
- **Starting the inner loop at 0.** Double-swaps everything, transpose becomes a no-op, and the failure is silent.
- **`row = row[::-1]`** inside the loop — rebinds the local variable and leaves the matrix half-rotated.
- Reversing the rows *before* transposing — that gives a counter-clockwise rotation, not clockwise.
- Reversing columns instead of rows after transposing — also counter-clockwise.
- Building a result matrix and returning it. The signature returns `None`; the input must be mutated.
- Using `len(matrix[0])` for the inner bound out of habit. Harmless here since the matrix is square, but it obscures that squareness is what makes the algorithm valid.

**This same move shows up in:** [Spiral Matrix](54-spiral-matrix.md) (careful index management over a 2-D grid) · [Set Matrix Zeroes](73-set-matrix-zeroes.md) (in-place matrix manipulation under an O(1)-space constraint) · [Reverse Linked List](206-reverse-linked-list.md) (in-place reversal via pointer swaps rather than rebuilding) · [Valid Sudoku](36-valid-sudoku.md) (indexing a grid by row, column, and derived coordinates).

</details>

---
