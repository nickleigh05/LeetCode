# 304. Range Sum Query 2D - Immutable

**Medium** · [LeetCode](https://leetcode.com/problems/range-sum-query-2d-immutable/) · [Solution file (no hints)](../../problems/0001-0499/304.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Design a `NumMatrix` that is built once from a 2D matrix and then answers many queries: `sumRegion(row1, col1, row2, col2)` returns the sum of every cell in the rectangle with top-left `(row1, col1)` and bottom-right `(row2, col2)`, both corners **inclusive**. Each query must run in **O(1)**.

```
matrix = [[3, 0, 1, 4, 2],
          [5, 6, 3, 2, 1],
          [1, 2, 0, 1, 5],
          [4, 1, 0, 1, 7],
          [1, 0, 3, 0, 5]]

sumRegion(2, 1, 4, 3)  →  8      (2+0+1 + 1+0+1 + 0+3+0)
sumRegion(1, 1, 2, 2)  →  11
sumRegion(1, 2, 2, 4)  →  12
```

**Constraints:** `1 <= m, n <= 200` · `-10⁴ <= matrix[i][j] <= 10⁴` · up to `10⁴` queries

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "immutable" | The matrix never changes, so you can **precompute once** and reuse it |
| "many queries" (`10⁴`) | The cost of one query matters far more than the cost of building |
| "each query O(1)" | No looping over the rectangle at query time. Everything must come from stored numbers |
| rectangle, two inclusive corners | Any rectangle must be expressible from a few precomputed values |
| negative values allowed | Rules out any "only add" trick. Subtraction-based formulas are fine |

Looping over the rectangle costs O(m·n) per query, and `10⁴ × 40,000 = 4 × 10⁸`. Too slow.

The 1D version is [Range Sum Query - Immutable](303-range-sum-query-immutable.md): store running totals, and a range sum is `prefix[r+1] - prefix[l]`. The 2D version stores the sum of the **whole rectangle from the top-left corner** to every cell. Any rectangle is then a big one **minus** two overlapping ones, **plus** the overlap you subtracted twice.

🤔 **Before you open the next section:** to get the sum of a rectangle from the sum of four "from the corner" rectangles, which do you subtract and which do you add back? Draw it.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Build | Query | Verdict |
|---|---|---|---|
| Loop the rectangle each query | O(1) | O(m·n) | ❌ Up to 4×10⁸ total work |
| Row-wise 1D prefix sums | O(m·n) | O(m) | ⚠️ Better, but still loops over rows |
| **2D prefix sums** | **O(m·n)** | **O(1)** | ✅ |

**The decision: a 2D [prefix sum](../learning/01b-prefix-sums.md) table.** `prefix[r][c]` is the sum of all cells in rows `0..r-1` and columns `0..c-1` (the rectangle from the top-left corner up to, but not including, row `r` and column `c`).

An extra row and column of zeros at the top and left removes every "what if the index is -1" edge case, the same trick as the leading `0` in the 1D version.

**Two formulas to remember:**

- **Build:** `prefix[r+1][c+1] = cell + top + left - topLeft`. The top and left rectangles overlap in the top-left one, which is counted twice, so subtract it once.
- **Query:** `prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]`. Take the big corner rectangle, cut off the strip above and the strip to the left, and add back the corner that was cut twice.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self, matrix: List[List[int]]):
    rows = len(matrix)
    cols = len(matrix[0])
    self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
```

A `(rows+1) × (cols+1)` grid of zeros. The extra first row and column are the "empty" prefix, so every real cell has an upper and left neighbour to read from. The comprehension makes a **fresh list per row**. `[[0] * w] * h` would alias every row.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [init-method](../syntax/init-method.md)

```python
    for r in range(rows):
        for c in range(cols):
            self.prefix[r + 1][c + 1] = (
                matrix[r][c]
                + self.prefix[r][c + 1]
                + self.prefix[r + 1][c]
                - self.prefix[r][c]
            )
```

Fill in reading order. The rectangle ending at cell `(r, c)` is: the cell itself, plus everything above it (`prefix[r][c+1]`), plus everything to its left (`prefix[r+1][c]`), minus the region above-and-left which both of those include (`prefix[r][c]`). Every term on the right has already been computed.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
    return (
        self.prefix[row2 + 1][col2 + 1]
        - self.prefix[row1][col2 + 1]
        - self.prefix[row2 + 1][col1]
        + self.prefix[row1][col1]
    )
```

The `+1`s convert inclusive corners into the table's "up to, not including" indexing. Start with the rectangle from the origin to the bottom-right corner, subtract the strip **above** the query (`row1`), subtract the strip **left** of it (`col1`), and add back the top-left block that both subtractions removed.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [multiple-return-values](../syntax/multiple-return-values.md)

<details>
<summary>The whole thing together</summary>

```python
class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        rows = len(matrix)
        cols = len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )
```

</details>

**Trace it.** A 2×3 matrix `[[1, 2, 3], [4, 5, 6]]`. The prefix table:

| | c=0 | c=1 | c=2 | c=3 |
|---|---|---|---|---|
| r=0 | 0 | 0 | 0 | 0 |
| r=1 | 0 | 1 | 3 | 6 |
| r=2 | 0 | 5 | 12 | 21 |

`prefix[2][2] = 5 + prefix[1][2] (3) + prefix[2][1] (5) - prefix[1][1] (1)`, which is `5 + 3 + 5 - 1 = 12` ✅ (1+2+4+5).

Query `sumRegion(1, 1, 1, 2)` (cells 5 and 6): `prefix[2][3] - prefix[1][3] - prefix[2][1] + prefix[1][1] = 21 - 6 - 5 + 1 = 11` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m·n) build, O(1) per query</summary>

- **Build:** one pass over every cell, each with four array reads. **O(m·n)**, once.
- **Query:** four lookups and three additions or subtractions. **O(1)**, regardless of the rectangle's size.

For `10⁴` queries, that is about `4 × 10⁴` operations of query work instead of up to `4 × 10⁸`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m·n)</summary>

**O(m·n)** for the prefix table, `(m+1) × (n+1)` integers. It is the price of constant-time queries. Since the matrix is never modified, you could in principle prefix-sum **in place** to avoid the copy, but that would destroy the input.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Queries are many and the matrix never changes, so I'll precompute. I build a 2D prefix table where `prefix[r][c]` is the sum of the rectangle from the origin to just before `(r, c)`. Each cell is the value plus the prefix above plus the prefix to the left, minus the overlap counted twice. A query is then inclusion-exclusion on four corners: big rectangle, minus the strip above, minus the strip to the left, plus the corner removed twice. O(m·n) to build, O(1) per query, O(m·n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the matrix can be updated?" | A 2D [Fenwick tree](../data-structures/fenwick-tree.md) or segment tree gives O(log² n) for both update and query. This is the *Range Sum Query 2D - Mutable* problem |
| "The 1D version?" | [Range Sum Query - Immutable](303-range-sum-query-immutable.md): `prefix[r+1] - prefix[l]` |
| "Mutable 1D?" | [Range Sum Query - Mutable](307-range-sum-query-mutable.md) |
| "Count of cells instead of sum?" | Same technique, with a 0/1 matrix |
| "Why the extra row and column of zeros?" | So `row1 - 1` or `col1 - 1` never goes negative. Without the padding you'd need `if` checks on every query |

**Traps:**

- **Off-by-one between inclusive corners and the padded table.** The `+1`s on `row2` and `col2` are the whole point.
- **Forgetting to add back `prefix[row1][col1]`.** You subtracted that corner twice.
- **`[[0] * w] * h`** aliasing every row to the same list.
- **Using the input matrix as the table** and reading indices that were never filled in.

**This same move shows up in:** [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (1D) · [Subarray Sum Equals K](560-subarray-sum-equals-k.md) (prefix sums plus a hash map) · [Maximal Square](221-maximal-square.md) (another 2D table built from top/left/top-left neighbours).

</details>

---
