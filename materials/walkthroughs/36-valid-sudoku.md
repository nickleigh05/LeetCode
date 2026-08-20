# 36. Valid Sudoku

**Medium** · [LeetCode](https://leetcode.com/problems/valid-sudoku/) · [Solution file (no hints)](../../problems/0001-0499/36.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Determine if a 9 × 9 Sudoku board is **valid**. Only the filled cells need to be checked, according to three rules:

1. Each **row** must contain the digits 1–9 without repetition.
2. Each **column** must contain the digits 1–9 without repetition.
3. Each of the nine **3 × 3 sub-boxes** must contain the digits 1–9 without repetition.

Empty cells are the character `"."`. A board can be valid without being solvable.

**Constraints:** `board.length == board[i].length == 9` · each cell is a digit `'1'`–`'9'` or `'.'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**without repetition**" | Three separate duplicate-detection problems — the same question [Contains Duplicate](217-contains-duplicate.md) asked, now asked 27 times |
| "only the **filled** cells" | `"."` is not a value. Skip it, or you'll report the second empty cell as a duplicate |
| "valid **without being solvable**" | Do **not** try to solve it. No backtracking, no inference — just check the three rules on what's already there |
| **9 × 9**, fixed | The size is a constant, not an input. This matters enormously for the complexity answer |
| cells are **characters** `'1'`–`'9'` | Strings, not ints. No conversion is needed since you're only checking equality |

The reframe: the three rules are the *same rule* applied to three different groupings of cells. Rather than three separate scans, notice that **every cell belongs to exactly one row, one column, and one box** — so a single pass can feed all three checks at once.

The only genuinely new sub-problem: given `(row, col)`, **which box is it in?**

🤔 **Before you open the next section:** you'd keep 9 sets for rows and 9 for columns, indexed by `row` and `col` directly. What arithmetic on `row` and `col` maps a cell to a box index 0–8?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

The structure is settled — [hashsets](../data-structures/hashset.md) for duplicate detection, straight from [Contains Duplicate](217-contains-duplicate.md). **The decisions are how many, and how to index the boxes.**

| Approach | How it works | Passes | Verdict |
|---|---|---|---|
| Three separate scans | Check all rows, then all columns, then all boxes | 3 | ⚠️ Correct and readable; repeats the traversal |
| Sort each group | Sort the 9 values, look for adjacent equals | 3 | ❌ More work than a set, for no gain |
| **27 sets, one pass** | 9 row + 9 col + 9 box sets, updated together | **1** | ✅ |
| One set of encoded keys | Add `(row, digit)`, `(col, digit)`, `(box, digit)` tuples to a single set | 1 | ✅ Slicker; same idea, one structure |

**The decision: 27 sets — 9 per rule — filled in a single pass.**

Each cell is visited once and checked against its row set, its column set, and its box set. Three O(1) membership tests per cell, and the first hit returns `False` immediately.

**The box index.** Boxes are laid out 3 across and 3 down, so:

```
box = (row // 3) * 3 + (col // 3)
```

`row // 3` gives the box *band* (0, 1, or 2) and `col // 3` the box *stack*. Multiplying the band by 3 and adding the stack flattens that 2-D coordinate into a single 0–8 index:

```
 cols:   0 1 2 | 3 4 5 | 6 7 8
 rows 0-2 │  0  │   1   │   2
 rows 3-5 │  3  │   4   │   5
 rows 6-8 │  6  │   7   │   8
```

That `(i // size) * width + (j // size)` flattening is a genuinely reusable trick — see [grids primer](../learning/11b-grids-primer.md).

**Why not the single-set-of-tuples version?** It's elegant — `if (row, cell) in seen: return False` — and worth mentioning. Three explicit sets make each rule visible in the code, which is easier to defend out loud and easier to debug when one rule fails.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
row_sets = [set() for _ in range(9)]
col_sets = [set() for _ in range(9)]
box_sets = [set() for _ in range(9)]
```

Nine independent sets per rule. `row_sets[3]` holds the digits seen so far in row 3, and so on.

⚠️ The comprehension is required — `[set()] * 9` would create **nine references to one set**, and every row would share the same digits. Same aliasing trap as in [Top K Frequent](347-top-k-frequent-elements.md).
→ [list-comprehension](../syntax/list-comprehension.md) · [set-basics](../syntax/set-basics.md)

```python
for row in range(9):
    for col in range(9):
        cell = board[row][col]
```

The single pass over all 81 cells. `board[row][col]` indexes the outer list to get a row, then the inner list to get a cell.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [nested-lists](../syntax/nested-lists.md)

```python
        if cell == ".":
            continue
```

Empty cells carry no constraint. `continue` skips to the next cell — without this, the second `"."` in any row would be flagged as a duplicate and every real board would fail.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        box = (row // 3) * 3 + (col // 3)
```

Map the 2-D cell coordinate to its box index 0–8. `//` is **floor division** — it discards the remainder, which is what collapses rows 0, 1, 2 all to band 0.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        if cell in row_sets[row]:
            return False
        row_sets[row].add(cell)
```

The Contains Duplicate move, applied to this cell's row: **check before adding**, so the set holds only cells seen *earlier* and a hit is a genuine repeat. Return `False` immediately — one violation is enough to invalidate the board.
→ [membership-operators](../syntax/membership-operators.md) · [set-operations](../syntax/set-operations.md) · [if-return](../syntax/if-return.md)

```python
        if cell in col_sets[col]:
            return False
        col_sets[col].add(cell)

        if cell in box_sets[box]:
            return False
        box_sets[box].add(cell)
```

The identical check against the column set and the box set. Three rules, three checks, one cell, one pass.

```python
return True
```

All 81 cells visited with no violation ⇒ the board satisfies all three rules.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        row_sets = [set() for _ in range(9)]
        col_sets = [set() for _ in range(9)]
        box_sets = [set() for _ in range(9)]

        for row in range(9):
            for col in range(9):
                cell = board[row][col]

                if cell == ".":
                    continue

                box = (row // 3) * 3 + (col // 3)

                if cell in row_sets[row]:
                    return False
                row_sets[row].add(cell)

                if cell in col_sets[col]:
                    return False
                col_sets[col].add(cell)

                if cell in box_sets[box]:
                    return False
                box_sets[box].add(cell)

        return True
```

</details>

**Check the box formula** on a few cells:

| `(row, col)` | `row // 3` | `col // 3` | `box` |
|---|---|---|---|
| (0, 0) | 0 | 0 | **0** |
| (0, 8) | 0 | 2 | **2** |
| (4, 4) | 1 | 1 | **4** (centre) |
| (8, 0) | 2 | 0 | **6** |
| (8, 8) | 2 | 2 | **8** |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(1)** — and this is the answer that surprises people, so be ready to justify it.

The board is **always** 9 × 9. There is no n. You visit 81 cells and do three O(1) set operations each — about 243 operations, every single time, regardless of input. Work that is bounded by a constant independent of any input size is O(1) by definition.

**The right way to say it:** *"O(1), because the board size is fixed at 9×9 — 81 cells is a constant. If you generalize to an n×n board with √n×√n boxes, it's O(n²) in the side length, i.e. linear in the number of cells."*

That sentence shows you understand *why* it's constant rather than having pattern-matched "nested loops ⇒ O(n²)". Both halves earn credit; only the second half alone is wrong.

**Early exit:** the first violation returns immediately, so an invalid board often costs far less than 81 cells.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

27 sets, and each can hold at most 9 digits → **243 items maximum**, always. Fixed ceiling, no dependence on input size.

**Generalized to n×n:** you'd hold 3n sets of up to n digits each → O(n²), which is proportional to the board itself. Notice that means the auxiliary space matches the input size — you can't do meaningfully better while still checking all three rules in one pass.

**The single-set variant** stores one tuple per (cell, rule) → up to 3 × 81 = 243 entries. Identical bound, one structure instead of 27.

**The genuinely O(1)-in-a-different-sense alternative:** bitmasks. Each set becomes a 9-bit integer, with bit *d* marking digit *d* as seen — 27 integers instead of 27 hash sets. Same complexity class, far smaller constant. See [bitwise-operators](../syntax/bitwise-operators.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "All three rules are the same duplicate check on different groupings, and every cell belongs to exactly one row, one column, and one box — so I can validate all three in a single pass. I'll keep nine hash sets per rule and, for each filled cell, check membership before inserting, returning false on the first repeat. The only fiddly part is mapping a cell to its box: `(row // 3) * 3 + (col // 3)` flattens the band and stack into an index 0–8. It's O(1) time and space since the board is a fixed 9×9 — generalized to n×n it'd be O(n²), linear in the number of cells."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Use one hash set instead of 27." | Add tuples: `(row, cell)`, `(col, cell)`, `(box, cell)`. Distinct namespaces prevent collisions between the rules. |
| "Reduce the memory further." | Bitmasks — one 9-bit int per set. Check with `mask & (1 << d)`, set with `mask \|= (1 << d)`. |
| "Now actually *solve* the Sudoku." | Different problem entirely: [backtracking](../algorithms/backtracking.md). Place a digit, recurse, undo on failure — and this validity check becomes the "is this placement legal?" test inside it. |
| "Generalize to n² × n² boards." | Same code with 9 → n², and the box formula becomes `(row // n) * n + (col // n)`. |
| "What if you can't use extra space at all?" | Three passes checking one rule at a time still needs a set per group. Truly O(1) auxiliary means re-scanning each group per cell — O(n³) and not worth it. |
| "Which cell is the offender?" | Return `(row, col)` instead of `False` — you're already there when you detect it. |

**Traps:**

- **`[set()] * 9`** — nine aliases of one set. Every row shares digits and almost any board fails.
- **Forgetting to skip `"."`** — the second empty cell in a row reads as a duplicate.
- **Getting the box formula backwards** (`(col // 3) * 3 + (row // 3)`). It still produces indices 0–8, so it *looks* fine and gives wrong answers on non-symmetric boards. Test it on (0, 8) vs (8, 0).
- **Using `/` instead of `//`** — true division yields floats, and `1.0` is not a valid list index.
- **Trying to solve the board.** Re-read the question; validity ≠ solvability.
- **Saying O(n²) without qualification.** Not wrong in spirit, but the board is fixed — name the constant.

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (the single-set original this is built from) · [Group Anagrams](49-group-anagrams.md) (a derived key to bucket by) · [Word Search](79-word-search.md) and [Number of Islands](200-number-of-islands.md) (the same 2-D grid indexing — see the [grids primer](../learning/11b-grids-primer.md)).

</details>

---
