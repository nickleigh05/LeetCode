# 37. Sudoku Solver

**Hard** · [LeetCode](https://leetcode.com/problems/sudoku-solver/) · [Solution file (no hints)](../../problems/0001-0499/37.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Write a program to solve a Sudoku puzzle by filling the empty cells **in place**. A solution must satisfy all of these:

1. Each **row** contains the digits `1`–`9` exactly once.
2. Each **column** contains the digits `1`–`9` exactly once.
3. Each of the nine **3×3 boxes** contains the digits `1`–`9` exactly once.

Empty cells are `'.'`.

```
5 3 . | . 7 . | . . .           5 3 4 | 6 7 8 | 9 1 2
6 . . | 1 9 5 | . . .           6 7 2 | 1 9 5 | 3 4 8
. 9 8 | . . . | . 6 .           1 9 8 | 3 4 2 | 5 6 7
------+-------+------           ------+-------+------
8 . . | . 6 . | . . 3     →     8 5 9 | 7 6 1 | 4 2 3
4 . . | 8 . 3 | . . 1           4 2 6 | 8 5 3 | 7 9 1
7 . . | . 2 . | . . 6           7 1 3 | 9 2 4 | 8 5 6
------+-------+------           ------+-------+------
. 6 . | . . . | 2 8 .           9 6 1 | 5 3 7 | 2 8 4
. . . | 4 1 9 | . . 5           2 8 7 | 4 1 9 | 6 3 5
. . . | . 8 . | . 7 9           3 4 5 | 2 8 6 | 1 7 9
```

**Constraints:** `board` is 9×9 · cells are digits `'1'`–`'9'` or `'.'` · the puzzle has **exactly one** solution

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| fill **in place** | Change `board` directly. Return nothing |
| row, column and box rules | Every placement must pass **three** checks |
| exactly one solution | Once you find a full valid board, **stop**. There's nothing else to find |
| fixed 9×9 size | The search is exponential in theory, but the constraints prune it heavily in practice |

**This is a constraint-satisfaction search, which means backtracking.** For each empty cell, in some order:

1. **Try** a digit that doesn't clash with its row, column or box.
2. **Recurse** to the next empty cell.
3. If the recursion fails (some later cell has no valid digit), **undo** the placement and try the next digit.
4. If no digit works here, **return failure** so the caller can change *its* choice.

**Make the clash check O(1).** Scanning the row, column and box for every candidate is 27 reads. Instead, keep a **set** of digits already used in each row, each column and each box. Then "can I place `d` here?" is three set lookups.

**Which box is a cell in?** Boxes are numbered 0–8, left to right and top to bottom:

```
box = (row // 3) * 3 + (col // 3)
```

`row // 3` picks the band of three rows (0, 1, 2), and `col // 3` picks the stack of three columns. So cell `(4, 7)` is in box `1 * 3 + 2 = 5`.

🤔 **Before you open the next section:** when a placement fails deeper down and you undo it, which four things have to be reversed?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Speed | Verdict |
|---|---|---|---|
| Brute force | Try every digit in every empty cell, check at the end | 9^(empties): astronomical | ❌ |
| Backtracking, scan to validate | Check row/column/box by scanning each time | Works, ~27 reads per check | ⚠️ Slower |
| **Backtracking + used-digit sets** | O(1) validity checks; undo on failure | Fast for any valid puzzle | ✅ |
| + "fewest options first" | Always fill the cell with the fewest candidates next | Much faster on hard puzzles | ✅ An optimisation |
| Dancing Links (Algorithm X) | Exact-cover formulation | Fastest | ⚠️ Overkill for an interview |

**The decision: [backtracking](../algorithms/backtracking.md) with [sets](../data-structures/hashset.md) of used digits** per row, column and box.

**Collect the empty cells once.** Scan the board at the start and list every `'.'` position. The recursion then works through that list by index (`k`), so there's no rescanning for "the next empty cell" on each call.

**Return `True` to stop everything.** Since there's exactly one solution, the moment the last empty cell is filled, return `True`, and every caller passes that straight up without undoing anything. The board is left solved.

**The optimisation worth mentioning.** Choose the next cell as the one with the **fewest** legal digits, and fill forced cells first. That's how human solvers work, and it cuts the search dramatically on hard puzzles. It's more code, so mention it rather than write it, unless you're asked.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = [set() for _ in range(9)]
cols = [set() for _ in range(9)]
boxes = [set() for _ in range(9)]
empty = []
```

**The constraint state.** `rows[r]` holds the digits already used in row `r`, and the same for columns and boxes. `empty` will list the cells to fill.

Use the comprehension. `[set()] * 9` would make all nine rows share a single set.
→ [list-comprehension](../syntax/list-comprehension.md) · [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
for r in range(9):
    for c in range(9):
        ch = board[r][c]
        if ch == '.':
            empty.append((r, c))
        else:
            rows[r].add(ch)
            cols[c].add(ch)
            boxes[(r // 3) * 3 + c // 3].add(ch)
```

**Read the givens.** Each filled cell records its digit in its row, column and box. Each empty cell goes on the to-do list. Digits stay as strings (`'5'`), since that's what the board stores.
→ [range-function](../syntax/range-function.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
def backtrack(k):
    if k == len(empty):
        return True
    r, c = empty[k]
    b = (r // 3) * 3 + c // 3
```

**The recursive search over the k-th empty cell.** If `k` has reached the end of the list, every cell is filled validly, so the puzzle is solved. Otherwise, look up this cell's row, column and box.
→ [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for ch in '123456789':
        if ch in rows[r] or ch in cols[c] or ch in boxes[b]:
            continue
```

**Try each digit, skipping clashes.** Three O(1) set lookups decide whether `ch` is allowed here. Iterating over the string `'123456789'` gives the digits as characters, which matches the board.
→ [membership-operators](../syntax/membership-operators.md) · [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md)

```python
        board[r][c] = ch
        rows[r].add(ch)
        cols[c].add(ch)
        boxes[b].add(ch)
```

**Choose.** Write the digit and record it in all three sets.
→ [set-operations](../syntax/set-operations.md)

```python
        if backtrack(k + 1):
            return True
```

**Explore.** Try to fill the rest. If that succeeds, the whole board is solved. Return `True` straight away, *without* undoing, so the board keeps its digits.

```python
        board[r][c] = '.'
        rows[r].remove(ch)
        cols[c].remove(ch)
        boxes[b].remove(ch)
    return False
```

**Un-choose.** The rest of the board couldn't be completed with `ch` here, so reverse all four changes and try the next digit. If no digit works, return `False` so the previous cell tries its next option.

```python
backtrack(0)
```

The search changes `board` in place. The method returns nothing, as required.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empty = []

        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == '.':
                    empty.append((r, c))
                else:
                    rows[r].add(ch)
                    cols[c].add(ch)
                    boxes[(r // 3) * 3 + c // 3].add(ch)

        def backtrack(k):
            if k == len(empty):
                return True
            r, c = empty[k]
            b = (r // 3) * 3 + c // 3
            for ch in '123456789':
                if ch in rows[r] or ch in cols[c] or ch in boxes[b]:
                    continue
                board[r][c] = ch
                rows[r].add(ch)
                cols[c].add(ch)
                boxes[b].add(ch)
                if backtrack(k + 1):
                    return True
                board[r][c] = '.'
                rows[r].remove(ch)
                cols[c].remove(ch)
                boxes[b].remove(ch)
            return False

        backtrack(0)
```

</details>

**Trace it.** The first empty cell in the example is `(0, 2)`, in box 0:

| Set | Digits already used |
|---|---|
| row 0 | 5, 3, 7 |
| column 2 | 8 |
| box 0 | 5, 3, 6, 9, 8 |

Ruling those out leaves **1, 2 and 4** as candidates. The search tries `'1'` first. Several cells later, something has no legal digit, so the search comes back and undoes `'1'`. Then it tries `'2'`, which also fails further down. Finally `'4'` works all the way to the end, matching the solution's `4` at `(0, 2)` ✅.

This is the pattern for every cell: try, go deeper, and undo when a later cell has no options left.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(9^m) worst case, fast in practice</summary>

**O(9^m)** in theory, where m is the number of empty cells (at most 81). Each empty cell could try up to 9 digits.

In practice it's far smaller. The row, column and box constraints rule out most digits at most cells, and wrong branches fail quickly. On a 9×9 board the board size is fixed, so some people describe it as O(1), which is technically true and not very useful.

Each step inside the search is O(1): three set lookups, plus three adds and three removes.

**The "fewest options first" heuristic** can cut hard puzzles from millions of steps to thousands.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** for the recursion stack (one frame per empty cell, at most 81) and the `empty` list. The 27 sets together hold at most 81 digits. On a fixed 9×9 board, all of this is O(1).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's a constraint search, so backtracking. I keep a set of used digits for each row, column and box, with box index `(r // 3) * 3 + c // 3`, so each placement check is O(1). I list the empty cells once, then recurse through them. For each cell, I try every digit that isn't in its row, column or box set, place it, update the sets, and recurse. If the recursion succeeds I return True straight away, leaving the board solved. If not, I undo all four changes and try the next digit. Worst case is exponential in the number of empty cells, but the constraints prune it heavily. A useful improvement is to fill the cell with the fewest candidates first."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Speed it up?" | Pick the empty cell with the fewest legal digits next. Use bitmasks instead of sets. Fill forced cells first. |
| "Just check whether a board is valid?" | [Valid Sudoku](36-valid-sudoku.md). The same three set families, in a single pass with no search. |
| "Count all solutions?" | Don't stop at the first one: count at `k == len(empty)`, and always undo. |
| "N² × N² Sudoku?" | Same code with N² digits and N×N boxes. It's NP-complete in general, so expect it to slow down. |
| "Fastest known approach?" | Knuth's Algorithm X with Dancing Links, treating Sudoku as an exact-cover problem. |

**Traps:**

- **Not undoing every change.** Forgetting one of the three sets, or the board cell, corrupts the later search.
- **Undoing after success.** The solved board gets wiped. Return `True` *before* the undo lines.
- **The wrong box formula.** `r // 3 + c // 3` collides boxes. You need `(r // 3) * 3 + c // 3`.
- **`[set()] * 9`.** All nine sets are the same object.
- **Mixing ints and strings.** The board holds `'5'`, not `5`. Keep everything as strings, or convert consistently.

**This same move shows up in:** [Valid Sudoku](36-valid-sudoku.md) (the same row, column and box sets, with no search) · [N-Queens](51-n-queens.md) (backtracking with O(1) conflict sets) · [Word Search](79-word-search.md) (choose, explore and undo on a grid) · [Combination Sum](39-combination-sum.md) (the general backtracking template).

</details>

---
