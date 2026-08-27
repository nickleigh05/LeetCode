# 74. Search a 2D Matrix

**Medium** · [LeetCode](https://leetcode.com/problems/search-a-2d-matrix/) · [Solution file (no hints)](../../problems/0001-0499/74.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

You're given an `m × n` integer matrix with two properties:

1. Each row is sorted in **non-decreasing order**.
2. The **first integer of each row is greater than the last integer of the previous row**.

Given an integer `target`, return `true` if it's in the matrix. You must write a solution in **O(log(m·n))** time.

```
matrix = [[1, 3, 5, 7],
          [10,11,16,20],
          [23,30,34,60]]

target = 3   →  true
target = 13  →  false
```

**Constraints:** `1 <= m, n <= 100` · `-10⁴ <= matrix[i][j], target <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| each row sorted | Ordered *within* a row |
| "**first of each row > last of the previous**" | ⚠️ **The critical property.** The rows chain together — reading the matrix row by row gives one **fully sorted sequence** |
| "**O(log(m·n))**" | Not O(m + log n), not O(log m + log n) — a **single** binary search over all m·n cells |
| return `true`/`false` | Existence only; no position needed |
| m, n ≤ 100 | At most 10,000 cells → 14 comparisons |

The second property is doing all the work, and it's easy to skim past. It means the matrix isn't really 2-D for search purposes:

```
[[1, 3, 5, 7],
 [10,11,16,20],   →   [1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]
 [23,30,34,60]]        a single sorted array of length m·n
```

⚠️ **Contrast with [LeetCode 240](https://leetcode.com/problems/search-a-2d-matrix-ii/)** ("Search a 2D Matrix II"), where rows and columns are each sorted but rows *don't* chain. There the flattening trick fails and you need a staircase walk from a corner, O(m + n). The two problems look identical and are solved completely differently — the chaining property is the tell.

So the question becomes purely mechanical: **can you binary search a 1-D sequence you never actually build?**

🤔 **Before you open the next section:** if the matrix were flattened into a list, index `k` would hold `matrix[?][?]`. Work out both coordinates in terms of `k` and the row width.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Scan every cell | Check all m·n | O(m·n) | ❌ Violates the stated bound |
| Actually flatten the matrix | Build a list, binary search it | O(m·n) time, O(m·n) space | ❌ Building it costs more than searching |
| Two binary searches | Find the row, then search within it | O(log m + log n) | ✅ Also correct — and equals O(log(m·n)) |
| **One binary search on a virtual index** | Treat `0..m·n−1` as a flat array | **O(log(m·n))** | ✅ Cleanest |

**The decision: standard binary search over the virtual index range `0 .. m·n − 1`, converting each index to `(row, col)` on the fly.**

The conversion, given `n` columns per row:

```
row = index // n        how many complete rows fit before this index
col = index %  n        how far into that row
```

`//` counts complete rows; `%` gives the leftover offset. Check it: with `n = 4`, index 6 → `row = 6//4 = 1`, `col = 6%4 = 2` → `matrix[1][2] = 16`. And flattening by hand, position 6 is indeed 16. ✅

**Why this beats literally flattening.** Building the flat list is O(m·n) time and space — more expensive than the search itself, which defeats the purpose. The index math gives you the *same view* at zero cost. **You're searching a structure that doesn't exist.**

**Note that `log m + log n = log(m·n)`** — the two-binary-search version is asymptotically identical, not worse. It's a perfectly good answer; it just needs two loops and careful row-boundary logic (find the row whose last element is ≥ target). The single search is less code and fewer places to get boundaries wrong.

**The transferable idea:** *"flatten via index arithmetic"* recurs constantly — same `// width` and `% width` pair as the box index in [Valid Sudoku](36-valid-sudoku.md) and throughout the [grids primer](../learning/10b-grids-primer.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m = len(matrix)
n = len(matrix[0])
```

Rows and columns. `n` — the **row width** — is the modulus for all the index math, so name it clearly.
→ [nested-lists](../syntax/nested-lists.md) · [list-basics](../syntax/list-basics.md)

```python
left = 0
right = (m * n) - 1
```

The virtual range covers **every cell**, as if the matrix were one flat array of `m·n` elements. Inclusive on both ends, same convention as [704](704-binary-search.md).
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
while left <= right:
    mid = (left + right) // 2
```

Identical machinery to [704](704-binary-search.md) — `<=` so the final single element gets checked, floor division for the midpoint.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    row = mid // n
    col = mid % n
```

**The translation step, and the only thing new in this problem.** Convert the flat index into 2-D coordinates.

Note it's `// n` and `% n` — divided by the number of **columns**, not rows. Using `m` here is the classic bug: on a square matrix it silently works, and on a non-square one it produces `IndexError` or wrong cells.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    mid_element = matrix[row][col]
```

Read the actual value — the first index selects the row, the second the column within it.

```python
    if mid_element == target:
        return True
    elif mid_element < target:
        left = mid + 1
    else:
        right = mid - 1
```

Ordinary binary search comparisons, operating on the **virtual index**. The `±1` still excludes the checked midpoint. All the 2-D-ness lives in the two translation lines above; this part doesn't know or care that it's a matrix.
→ [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md)

```python
return False
```

The range emptied out — the target isn't present.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        m = len(matrix)
        n = len(matrix[0])
        left = 0
        right = (m * n) - 1

        while left <= right:
            mid = (left + right) // 2
            row = mid // n
            col = mid % n

            mid_element = matrix[row][col]

            if mid_element == target:
                return True
            elif mid_element < target:
                left = mid + 1
            else:
                right = mid - 1

        return False
```

</details>

**Trace it** — the 3×4 matrix above (`n = 4`, so indices run 0–11), `target = 16`:

Flattened view for reference:
```
index:  0  1  2  3   4   5   6   7   8   9  10  11
value:  1  3  5  7  10  11  16  20  23  30  34  60
```

| `left` | `right` | `mid` | `row = mid//4` | `col = mid%4` | value | vs 16 | Action |
|---|---|---|---|---|---|---|---|
| 0 | 11 | 5 | 1 | 1 | 11 | too small | `left = 6` |
| 6 | 11 | 8 | 2 | 0 | 23 | too big | `right = 7` |
| 6 | 7 | 6 | 1 | 2 | **16** | **match** | `return True` ✅ |

**And a miss** — `target = 13`:

| `left` | `right` | `mid` | value | Action |
|---|---|---|---|---|
| 0 | 11 | 5 | 11 | `left = 6` |
| 6 | 11 | 8 | 23 | `right = 7` |
| 6 | 7 | 6 | 16 | `right = 5` |
| 6 | 5 | — | — | `left > right` → `return False` ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log(m·n))</summary>

**O(log(m·n))**, matching the requirement exactly.

The search space is the `m·n` virtual indices, halved every iteration → log₂(m·n) steps. Each step does O(1) work: one division, one modulo, one array lookup, one comparison.

At the maximum 100 × 100 = 10,000 cells, that's **at most 14 comparisons**.

**The equivalence worth knowing:**

```
log(m·n) = log m + log n
```

So "one search over m·n cells" and "a search for the row plus a search within it" have **identical** complexity. The single-search version isn't asymptotically better — it's just less code with fewer boundary conditions.

**Versus the alternatives:** scanning every cell is O(m·n) = 10,000 operations rather than 14. Building a flattened list first would cost O(m·n) just to prepare, making the O(log) search pointless.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Five integers: `m`, `n`, `left`, `right`, `mid` (plus the derived `row`, `col`, `mid_element`). The matrix is only ever read.

**This is the whole reason for the virtual-index trick.** The naive "flatten it first" approach:

```python
flat = [x for row in matrix for x in row]   # O(m·n) time AND space
```

costs O(m·n) on both axes — strictly worse than just scanning, since you've done linear work before the search even starts.

Computing `row` and `col` arithmetically gives you the identical logical view for **two integer operations per step**. The flattened array is never materialized; it exists only as a way of *indexing*.

That's a genuinely reusable idea: **when you need a different view of a data structure, ask whether index arithmetic can provide it instead of a copy.** Same instinct as [Product of Array Except Self](238-product-of-array-except-self.md) reusing its output array, or [Trapping Rain Water](42-trapping-rain-water.md) collapsing two arrays into two variables.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key property is that each row's first element exceeds the previous row's last — so reading the matrix row by row gives one fully sorted sequence. That means I can binary search it as if it were a flat array of m·n elements. I don't actually build that array; I search the virtual index range and convert each midpoint with `row = mid // n` and `col = mid % n`, where n is the number of columns. Everything else is the standard binary search loop. O(log(m·n)) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if rows *don't* chain — only rows and columns are individually sorted?" | **The important one.** That's LeetCode 240, and flattening fails. Start at the top-right corner: if the value is too big move left, too small move down. O(m + n). |
| "Why `// n` and not `// m`?" | The row width is the modulus. Using `m` works only on square matrices, which is what makes it a nasty bug. |
| "Solve it with two binary searches." | First find the row whose last element ≥ target, then search that row. Same O(log m + log n) = O(log(m·n)). |
| "Return the coordinates, not a boolean." | You already have them — return `[row, col]` instead of `True`. |
| "What if the matrix could have empty rows?" | `len(matrix[0])` would raise on `[[]]`. Guard with `if not matrix or not matrix[0]: return False`. Worth asking about. |
| "Duplicates allowed?" | Standard binary search still finds *an* occurrence. For the first, use the `bisect_left` style — record and keep searching left. |

**Traps:**

- **`mid // m` instead of `mid // n`.** Passes on square test matrices, fails on rectangular ones. Verify on a non-square example.
- **Actually flattening the matrix** — O(m·n) time and space, defeating the point.
- **Confusing this with LeetCode 240.** The problems look the same; only the chaining property distinguishes them.
- **`right = m * n`** instead of `m * n - 1` — an off-by-one that indexes past the end.
- **Swapping `row` and `col`** in the lookup — `matrix[col][row]` may not even raise on a square matrix, just return the wrong cell.
- **All the [704](704-binary-search.md) boundary traps** still apply: `<=`, and `mid ± 1`.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the loop this reuses verbatim) · [Valid Sudoku](36-valid-sudoku.md) (the same `// width` and `% width` flattening for box indices) · [Grids Primer](../learning/10b-grids-primer.md) (2-D indexing in general) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search over a space that isn't an array at all).

</details>

---
