# 73. Set Matrix Zeroes

**Medium** · [LeetCode](https://leetcode.com/problems/set-matrix-zeroes/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` integer `matrix`, if an element is **0**, set its **entire row and column** to 0. Do it **in place**.

The follow-up is the real problem: a straightforward solution uses O(m·n) space, an improvement uses O(m + n). **Can you do it in O(1) space?**

```
[[1,1,1],          [[1,0,1],
 [1,0,1],    →      [0,0,0],
 [1,1,1]]           [1,0,1]]

[[0,1,2,0],        [[0,0,0,0],
 [3,4,5,2],   →     [0,4,5,0],
 [1,3,1,5]]         [0,3,1,0]]
```

**Constraints:** `m == matrix.length` · `n == matrix[0].length` · `1 <= m, n <= 200` · `-2³¹ <= matrix[i][j] <= 2³¹ − 1`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "if an element is 0, zero its row **and** column" | Every original zero triggers two full lines of zeroing |
| "**in place**" | Modify the input; no returning a new matrix |
| O(1) space follow-up | The actual challenge. O(m+n) is easy and is what most people write |
| values span the **full int range** | You **cannot** use a sentinel value like `-2³¹` to mark cells — any value you pick might legitimately appear in the input |
| `m, n <= 200` | 40,000 cells. Performance is irrelevant; this is a **correctness and space** problem |

The trap is immediate and worth stating: **you cannot zero as you go.** Walk the matrix, find a 0, zero its row and column — and now those fresh zeros look exactly like original zeros to the rest of your scan. The zeroing cascades until the entire matrix is 0.

So the problem has an inherent **two-phase** shape:

1. **Mark** which rows and columns need zeroing (reading only original values).
2. **Apply** the zeroing.

The obvious implementation is two sets — `zero_rows` and `zero_cols` — which is **O(m + n)** space. Perfectly correct, and the answer most people give.

Now, how do you get to **O(1)**? You need somewhere to store m + n flags, and you're not allowed new memory. So the storage has to come from the matrix itself.

**The insight:** the matrix's **first row** and **first column** are exactly m + n cells — precisely the number of flags needed. Use `matrix[0][col]` to mean "column `col` needs zeroing" and `matrix[row][0]` to mean "row `row` needs zeroing."

And it's self-consistent: if `matrix[r][c]` is 0, then row `r` and column `c` will both be zeroed anyway, so writing a 0 into `matrix[r][0]` and `matrix[0][c]` isn't destroying information — **those cells were destined to become 0 regardless.**

There's one collision. `matrix[0][0]` would have to serve as the flag for row 0 *and* column 0 at once, and the first row and column are themselves part of the matrix — they might contain original zeros whose meaning gets overwritten by the marking. So they need **two separate boolean variables**, recorded before any marking begins.

🤔 **Before you open the next section:** the final two steps zero the first row and first column *last*, after everything else. What would break if you zeroed them first?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Zero as you scan | Zero each row/column on encountering a 0 | O(m·n) | O(1) | ❌ **Wrong.** New zeros are indistinguishable from original ones; everything cascades to 0 |
| Copy the matrix | Read from a pristine copy, write to the original | O(m·n) | **O(m·n)** | ⚠️ Correct, and the naive baseline the problem explicitly wants improved |
| Mark with a sentinel value | Write some impossible value into affected cells, then convert | O(m·n) | O(1) | ❌ Values span the full int range — **no safe sentinel exists** |
| Two sets of indices | `zero_rows` and `zero_cols`, then apply | O(m·n) | **O(m + n)** | ⚠️ Correct and clean — the expected first answer |
| **First row/column as flags** | Reuse the matrix's own border as marker storage | O(m·n) | **O(1)** | ✅ |

**The decision:** **use the first row and first column as the marker arrays**, with two extra booleans for their own status.

**Why the sentinel idea fails, specifically.** A common instinct is to mark affected cells with something like `float('-inf')` or `-2³¹`, then convert all sentinels to 0 in a second pass. But the constraints allow **any** 32-bit integer, so any sentinel you pick could already be in the input — and you'd zero cells that shouldn't be. **The constraint on the value range is there precisely to rule this out**, which is a good reminder that unusual-looking constraints are usually load-bearing.

**Why the border works as storage.** You need m + n bits of information. The first row and first column contain exactly m + n cells (sharing one corner). And crucially, **using them is lossless**: writing a 0 into `matrix[r][0]` only happens when some `matrix[r][c]` was 0, which means row `r` is getting zeroed anyway. You're overwriting a cell with the value it was going to end up with.

**Why the corner needs special handling.** `matrix[0][0]` is in both the first row and the first column, so it can only carry one flag. Rather than resolve the ambiguity, the solution sidesteps it: **capture whether the first row and first column originally contained a zero into two separate booleans before any marking**, and apply those at the very end.

**Why the order matters — the answer to section 1's question.** The first row and column are being used as *marker storage*, so they must stay readable until every interior cell has consulted them. If you zeroed the first row early, every column flag would read as "needs zeroing" and the whole matrix would go to 0.

**So the phases are strictly ordered:**
1. Record the two booleans (read the border before touching it).
2. Mark the border from the interior.
3. Apply zeros to the **interior only**, reading the border.
4. Zero the border itself, last.

**Is O(1) worth the complexity?** Honestly, for a 200×200 matrix, the O(m+n) set version is 400 integers and completely fine. But the follow-up asks explicitly, and the technique — **storing metadata inside the data structure when the overwrite is provably harmless** — generalizes well beyond this problem.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(matrix)
cols = len(matrix[0])
first_row_zero = any(matrix[0][col] == 0 for col in range(cols))
first_col_zero = any(matrix[row][0] == 0 for row in range(rows))
```
**Capture the border's original state, before anything is modified.**

These two booleans exist because the first row and column serve double duty: they're both *markers* and *actual matrix cells*. Once marking begins, you can no longer tell whether a 0 in the border was original data or a flag written by the marking pass.

[`any()`](../syntax/any-all.md) with a [generator expression](../syntax/generator-expressions.md) short-circuits on the first zero found — a small efficiency, and it reads exactly like the question being asked.

**Order matters absolutely: these two lines must come first.**
→ [any-all](../syntax/any-all.md) · [generator-expressions](../syntax/generator-expressions.md) · [nested-lists](../syntax/nested-lists.md)

```python
for row in range(1, rows):
    for col in range(1, cols):
        if matrix[row][col] == 0:
            matrix[row][0] = 0
            matrix[0][col] = 0
```
**Phase 1 — mark.** Scan the **interior** (both loops start at 1, skipping the border) and record each zero's row and column in the border.

`matrix[row][0] = 0` means "row `row` needs zeroing"; `matrix[0][col] = 0` means "column `col` needs zeroing."

Skipping row 0 and column 0 is essential — their zeros are already captured in the booleans, and re-processing them here would confuse markers with data.

**This pass only writes to the border and only reads the interior**, so no marker is ever read before it's finalized.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
for row in range(1, rows):
    for col in range(1, cols):
        if matrix[row][0] == 0 or matrix[0][col] == 0:
            matrix[row][col] = 0
```
**Phase 2 — apply, to the interior only.** A cell is zeroed if its row flag **or** its column flag is set.

Again both loops start at 1. **The border must not be zeroed yet**, because later iterations of this very loop still need to read it. Zeroing `matrix[0][col]` here would be fine (it's already 0 or will be), but zeroing a border cell that *isn't* flagged would corrupt the markers for rows or columns not yet processed.

Note this pass is safe to run in any order over the interior, since it only ever **reads** the border and **writes** the interior — the two regions don't interfere.
→ [logical-operators](../syntax/logical-operators.md) · [nested-lists](../syntax/nested-lists.md)

```python
if first_row_zero:
    for col in range(cols):
        matrix[0][col] = 0
if first_col_zero:
    for row in range(rows):
        matrix[row][0] = 0
```
**Phase 3 — handle the border, last.**

Now that every interior cell has been decided, the markers are no longer needed and the border can be overwritten with its true values.

- If the first row originally contained a 0, the **entire first row** becomes 0.
- If the first column originally contained a 0, the **entire first column** becomes 0.

These use `range(cols)` and `range(rows)` — the **full** ranges, including index 0 — because the corner belongs to both.

Doing this first instead of last is the classic way to break the algorithm: the markers would be destroyed before phase 2 could read them.
→ [if-return](../syntax/if-return.md) · [for-loop](../syntax/for-loop.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:

        rows = len(matrix)
        cols = len(matrix[0])
        first_row_zero = any(matrix[0][col] == 0 for col in range(cols))
        first_col_zero = any(matrix[row][0] == 0 for row in range(rows))

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][col] == 0:
                    matrix[row][0] = 0
                    matrix[0][col] = 0

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][0] == 0 or matrix[0][col] == 0:
                    matrix[row][col] = 0

        if first_row_zero:
            for col in range(cols):
                matrix[0][col] = 0
        if first_col_zero:
            for row in range(rows):
                matrix[row][0] = 0
```
</details>

**Trace it** — `matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]`

**Capture the booleans:** row 0 is `[0,1,2,0]` → contains zeros → `first_row_zero = True`. Column 0 is `[0,3,1]` → contains a zero → `first_col_zero = True`.

**Phase 1 — mark** (interior is rows 1–2, cols 1–3):

| cell | value | action |
|---|---|---|
| `[1][1]`=4, `[1][2]`=5, `[1][3]`=2 | non-zero | — |
| `[2][1]`=3, `[2][2]`=1, `[2][3]`=5 | non-zero | — |

**No interior zeros**, so no new markers are written. The matrix is unchanged:

```
0 1 2 0
3 4 5 2
1 3 1 5
```

**Phase 2 — apply to the interior**, reading the border (`matrix[0] = [0,1,2,0]`, column 0 = `[0,3,1]`):

| cell | row flag `[r][0]` | col flag `[0][c]` | zero it? |
|---|---|---|---|
| `[1][1]` | `[1][0]`=3 ≠ 0 | `[0][1]`=1 ≠ 0 | no |
| `[1][2]` | 3 ≠ 0 | `[0][2]`=2 ≠ 0 | no |
| `[1][3]` | 3 ≠ 0 | **`[0][3]`=0** ✓ | **yes** |
| `[2][1]` | `[2][0]`=1 ≠ 0 | 1 ≠ 0 | no |
| `[2][2]` | 1 ≠ 0 | 2 ≠ 0 | no |
| `[2][3]` | 1 ≠ 0 | **`[0][3]`=0** ✓ | **yes** |

```
0 1 2 0
3 4 5 0
1 3 1 0
```

**Phase 3 — the border.** `first_row_zero` is True → zero all of row 0. `first_col_zero` is True → zero all of column 0.

```
0 0 0 0
0 4 5 0
0 3 1 0
```

✅ Matches the expected output.

Notice how the pre-existing zeros in the first row acted as markers **for free** — `matrix[0][3] = 0` was original data, and phase 2 correctly read it as "column 3 needs zeroing." The dual role works because a zero in the border means the same thing either way.

**And a case with interior zeros** — `matrix = [[1,1,1],[1,0,1],[1,1,1]]`:

Booleans: row 0 is `[1,1,1]` → `first_row_zero = False`. Column 0 is `[1,1,1]` → `first_col_zero = False`.

**Phase 1:** `matrix[1][1] = 0` → write `matrix[1][0] = 0` and `matrix[0][1] = 0`:

```
1 0 1
0 0 1
1 1 1
```

**Phase 2** — interior cells:

| cell | row flag | col flag | zero? |
|---|---|---|---|
| `[1][1]` | `[1][0]`=0 ✓ | — | **yes** |
| `[1][2]` | `[1][0]`=0 ✓ | — | **yes** |
| `[2][1]` | `[2][0]`=1 | **`[0][1]`=0** ✓ | **yes** |
| `[2][2]` | 1 | `[0][2]`=1 | no |

```
1 0 1
0 0 0
1 0 1
```

**Phase 3:** both booleans are False, so the border is left alone.

Return **[[1,0,1],[0,0,0],[1,0,1]]** ✅

**And here's why phase 3 must come last:** if you had zeroed the border first, `matrix[0][2]` would have become 0, and phase 2 would then zero `matrix[2][2]` as well — producing an all-zero bottom row that shouldn't be there.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)** — a constant number of passes over the matrix.

- **Capturing the booleans** — one scan of the first row (O(n)) and one of the first column (O(m)) → **O(m + n)**.
- **Phase 1 (mark)** — one full interior sweep → **O(m · n)**.
- **Phase 2 (apply)** — a second full interior sweep → **O(m · n)**.
- **Phase 3 (border)** — O(n) + O(m).
- Total: **O(m · n)**, with a constant factor of roughly 2 over the cells.

At the limits, 200 × 200 = 40,000 cells, touched twice. Instant.

**Faster?** No. In the worst case every cell must be read (a zero anywhere changes the output) and potentially written, so **Ω(m·n)** is a lower bound.

**Can it be one pass?** No, and this is the structural point: **the marking and applying phases are inherently separate.** Zeroing during the scan would make new zeros indistinguishable from original ones, cascading until the whole matrix is 0. The two-pass structure isn't an implementation detail — it's forced by the problem.

**Compared to the alternatives:** all correct approaches here are O(m·n) time. The copy version, the two-sets version, and this one differ **only in space**, which is exactly what the follow-up is asking about.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two booleans and a handful of loop indices, regardless of matrix size.

| Version | Space | Why |
|---|---|---|
| Copy the matrix | **O(m·n)** | A full duplicate to read from |
| Two sets of indices | **O(m + n)** | Up to m row indices and n column indices |
| **Border as markers** | **O(1)** | The m + n flags live inside the matrix |

**The technique, stated generally:** *store metadata inside the data structure, in locations whose original contents are provably no longer needed.* Here, writing a 0 into `matrix[r][0]` is safe precisely because row `r` is already destined to be zeroed — **you're not destroying information, you're writing the answer early.**

That reasoning is what makes it legitimate rather than a hack, and it's the part worth articulating. The same idea appears whenever you reuse an array's own cells as a hash table (marking indices by negating values) or overwrite consumed input.

**The cost of the technique** is the two booleans and the strict phase ordering — the first row and column can't be finalized until every interior cell has read them. That fragility is real, and it's why the O(m+n) version is a perfectly defensible answer if the follow-up isn't asked.

**Is O(1) actually better here?** At 200 × 200, the two-sets version uses at most 400 integers — nothing. **The O(1) version matters as a demonstration of the technique, not as a practical optimization**, and saying so is more honest than pretending the memory saving is meaningful.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The first thing to notice is that I can't zero as I scan — the new zeros would be indistinguishable from original ones and the whole matrix would cascade to zero. So it has to be two phases: mark which rows and columns need zeroing, then apply. The easy version uses two sets, which is O(m+n) space. To get O(1), I store the flags in the matrix itself: the first row and first column are exactly m + n cells, which is precisely how many flags I need. That's lossless, because writing a zero into `matrix[r][0]` only happens when row r is getting zeroed anyway. The complication is the corner — `matrix[0][0]` would have to flag both row 0 and column 0 — so I capture two booleans up front for whether the first row and first column originally contained a zero, and I apply those **last**, after every interior cell has read the markers. Zeroing the border early would destroy the flags and cascade. O(m·n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't you zero as you go?" | New zeros look identical to original ones, so the next cell you inspect triggers more zeroing. It cascades until everything is 0. |
| "Why not mark cells with a sentinel value?" | The constraints allow any 32-bit integer, so no value is guaranteed absent from the input. That constraint exists specifically to rule this out. |
| "Why do you need the two booleans?" | `matrix[0][0]` can only carry one flag but sits in both the first row and the first column. Capturing their original state separately resolves the ambiguity. |
| "Why zero the first row and column last?" | They're the marker storage. Zeroing them early would make every flag read as "needs zeroing," cascading to an all-zero matrix. |
| "Why is overwriting the border lossless?" | You only write a 0 into `matrix[r][0]` when some cell in row r was 0 — meaning that cell was going to become 0 anyway. You're writing the final answer early. |
| "Is the O(1) version worth it here?" | Practically, no — the two-sets version uses ~400 integers at these limits. It's worth it as a demonstration of storing metadata inside the data. |
| "Could you use just one boolean?" | Yes — a common variant uses `matrix[0][0]` for row 0 and a single extra boolean for column 0. Same idea, slightly tighter, slightly harder to follow. |
| "What if the matrix were 1×n or m×1?" | It still works — the interior loops simply don't execute, and the two booleans handle everything. |

**Traps:**
- **Zeroing the first row or column before phase 2.** Destroys the markers and cascades. The defining bug.
- **Starting the interior loops at 0** instead of 1 — confuses markers with data, and phase 2 would immediately propagate any border zero into everything.
- **Forgetting the two booleans**, or capturing them after marking has begun.
- Using a sentinel value to mark affected cells.
- Using `range(1, cols)` in phase 3 — the corner `matrix[0][0]` must be included when zeroing the border.
- Returning a new matrix. The signature returns `None`; the input must be mutated.

**This same move shows up in:** [Rotate Image](48-rotate-image.md) (in-place matrix manipulation under an O(1)-space constraint) · [Spiral Matrix](54-spiral-matrix.md) (avoiding an auxiliary visited grid by exploiting structure) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (another problem where the O(1)-space constraint is the entire difficulty) · [Missing Number](268-missing-number.md) (deriving the answer from the data rather than allocating a lookup).

</details>

---
