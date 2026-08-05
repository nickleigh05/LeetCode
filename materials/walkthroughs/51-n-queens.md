# 51. N-Queens

**Hard** · [LeetCode](https://leetcode.com/problems/n-queens/)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

The **n-queens puzzle** places `n` queens on an `n × n` chessboard so that **no two queens attack each other** — no two share a row, column, or diagonal.

Return **all distinct solutions**, each as a board where `'Q'` is a queen and `'.'` is empty.

```
n = 4  →  2 solutions

  . Q . .        . . Q .
  . . . Q        Q . . .
  Q . . .        . . . Q
  . . Q .        . Q . .

n = 1  →  [["Q"]]
```

**Constraints:** `1 <= n <= 9`

> **Try it yourself first.** This is the unit's hardest problem — the sections build up carefully.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "no two share a **row**" | ⚠️ Exactly one queen per row — which collapses the search space enormously |
| "…**column**" | Track which columns are taken |
| "…**diagonal**" | ⚠️ Both diagonal directions, and you need an O(1) way to test them |
| "**all** distinct solutions" | Enumerate everything → backtracking |
| **`n <= 9`** | Tiny bound. Exponential is expected |

**The first simplification, and it's a big one.** "No two queens share a row" means each of the n rows holds **exactly one** queen. So instead of choosing n squares from n² (which is C(n², n) — astronomically many), you're choosing **one column per row**: n choices for row 0, n for row 1, and so on.

That reduces the search from C(81, 9) ≈ 2.6 × 10¹¹ down to at most 9⁹ ≈ 4 × 10⁸ before pruning — and pruning cuts it far further.

**So the recursion is: one level per row.** At row `r`, try each column; if it's safe, place a queen and recurse to row `r + 1`.

**The second insight — how to test diagonals in O(1).** Scanning the board for conflicts would be O(n) per check. Instead, notice the arithmetic:

```
     col:  0    1    2    3
row 0:     0    1    2    3        ↘ diagonal:  row - col is CONSTANT
row 1:    -1    0    1    2
row 2:    -2   -1    0    1        (0,0) (1,1) (2,2) all give 0
row 3:    -3   -2   -1    0

     col:  0    1    2    3
row 0:     0    1    2    3        ↙ diagonal:  row + col is CONSTANT
row 1:     1    2    3    4
row 2:     2    3    4    5        (0,2) (1,1) (2,0) all give 2
row 3:     3    4    5    6
```

**Each diagonal has a unique identity: `row - col` for one direction, `row + col` for the other.** So a set of "attacked diagonals" makes the check a single hash lookup.

🤔 **Before you open the next section:** you now have three things to mark when placing a queen. What does that imply about the un-choose step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Try all placements of n queens on n² squares | C(n², n) combinations | ❌ Astronomically wasteful |
| One queen per row, scan the board to validate | O(n) check per candidate | ⚠️ Correct; O(n) where O(1) is available |
| **One queen per row + three sets** | O(1) safety check | ✅ |
| Bitmask version | Columns and diagonals as integers | ✅ Fastest; harder to read |

**The decision: backtrack row by row, tracking attacked columns and both diagonals in [hash sets](../data-structures/hashset.md).**

Three sets, each answering one question in O(1):

| Set | Contains | Blocks |
|---|---|---|
| `cols` | column indices | vertical attacks |
| `pos_diag` | values of `row + col` | ↙ diagonals |
| `neg_diag` | values of `row - col` | ↘ diagonals |

**Rows need no set** — the recursion places exactly one queen per row by construction, so row conflicts are impossible.

**A placement is safe iff none of the three sets already contains its key.** One `in` test each, all O(1).

**This is the unit's most demanding backtracking**, because there are now **four** pieces of state to choose and un-choose:

```
choose:      cols.add(col)          un-choose:   cols.remove(col)
             pos_diag.add(row+col)               pos_diag.remove(row+col)
             neg_diag.add(row-col)               neg_diag.remove(row-col)
             board[row][col] = "Q"               board[row][col] = "."
```

**Four adds, four removes, perfectly mirrored.** [Permutations](46-permutations.md) had two; this has four. Miss any one and the search corrupts — usually by permanently blocking a column or diagonal, so later solutions become unreachable.

**Why the diagonal formulas work.** Moving one step along a ↘ diagonal increases both `row` and `col` by 1, so `row - col` is unchanged. Along a ↙ diagonal, `row` increases while `col` decreases, so `row + col` is unchanged. **Each diagonal is uniquely identified by its constant** — turning a geometric test into a hash lookup.

**The bitmask alternative** replaces the three sets with three integers, using bit operations to test and set. Faster and O(1) space, but considerably less readable. **Mention it; write the sets version.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
cols = set()
pos_diag = set()   # row + col is constant along this diagonal
neg_diag = set()   # row - col is constant along this diagonal
board = [["."] * n for _ in range(n)]
```

Three sets tracking what's under attack, plus the board being built.

⚠️ **`[["."] * n for _ in range(n)]`** — the comprehension is required. `[["."] * n] * n` would create n references to *one* row, so writing a queen anywhere would write it to every row. The same aliasing trap as in [Valid Sudoku](36-valid-sudoku.md) and [Top K Frequent Elements](347-top-k-frequent-elements.md).

*(The inner `["."] * n` is safe, because strings are immutable.)*
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
def backtrack(row):
    if row == n:
        result.append(["".join(r) for r in board])
        return
```

**Base case: all n rows have a queen** ⇒ a complete valid solution.

`["".join(r) for r in board]` converts each row from a list of characters into a string — and **the join also acts as the copy**, since it creates new string objects. Appending `board` directly would store a reference to the shared, still-mutating board.
→ [recursion-basics](../syntax/recursion-basics.md) · [string-join-slice](../syntax/string-join-slice.md) · [if-return](../syntax/if-return.md)

```python
    for col in range(n):
        if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
            continue
```

**The O(1) safety check.** Three set lookups reject a column under vertical or diagonal attack.

No row check is needed — one queen per row is guaranteed by the recursion's structure.

`or` short-circuits, so a column conflict skips the diagonal tests.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md)

```python
        cols.add(col)
        pos_diag.add(row + col)
        neg_diag.add(row - col)
        board[row][col] = "Q"
```

**Choose — all four pieces of state.** Mark the column, both diagonals, and place the queen on the board.
→ [set-operations](../syntax/set-operations.md)

```python
        backtrack(row + 1)
```

**Explore** — move to the next row. Nothing is passed; all state lives in the enclosing scope.
→ [closures](../syntax/closures.md)

```python
        cols.remove(col)
        pos_diag.remove(row + col)
        neg_diag.remove(row - col)
        board[row][col] = "."
```

**Un-choose — all four, mirroring the choose exactly.**

This is where N-Queens punishes carelessness. Forget `cols.remove(col)` and that column stays blocked for every subsequent branch, so most solutions vanish silently. **Four adds demand four removes.**

The symmetry is the thing to internalize: *every piece of state mutated on the way down must be restored on the way back up.*

```python
backtrack(0)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:

        result = []
        cols = set()
        pos_diag = set()   # row + col is constant along this diagonal
        neg_diag = set()   # row - col is constant along this diagonal
        board = [["."] * n for _ in range(n)]

        def backtrack(row):
            if row == n:
                result.append(["".join(r) for r in board])
                return

            for col in range(n):
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)
                board[row][col] = "Q"

                backtrack(row + 1)

                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)
                board[row][col] = "."

        backtrack(0)
        return result
```

</details>

**Trace it** — `n = 4`, following the path to the first solution:

| Row | Try col | Blocked by | Action |
|---|---|---|---|
| 0 | 0 | — | place at (0,0). `cols={0}`, `pos={0}`, `neg={0}` |
| 1 | 0 | `cols` | skip |
| 1 | 1 | `neg_diag` (1−1 = 0) | skip |
| 1 | 2 | — | place at (1,2). `cols={0,2}`, `pos={0,3}`, `neg={0,-1}` |
| 2 | 0 | `cols` | skip |
| 2 | 1 | `pos_diag` (2+1 = 3) | skip |
| 2 | 2 | `cols` | skip |
| 2 | 3 | `pos_diag` (2+3=5? no)… `neg_diag` (2−3 = −1) ✓ blocked | skip |
| | | **dead end — no safe column in row 2** | **backtrack to row 1** |

Un-place (1,2): `cols={0}`, `pos={0}`, `neg={0}` — restored ✅

| Row | Try col | Result |
|---|---|---|
| 1 | 3 | place at (1,3) |
| 2 | 1 | place at (2,1) |
| 3 | — | every column blocked → backtrack |
| | | eventually unwinds to row 0 and tries col 1 |

Starting from (0,1) the search finds:

```
. Q . .        queens at (0,1), (1,3), (2,0), (3,2)
. . . Q
Q . . .        cols   = {1,3,0,2}      all distinct ✅
. . Q .        pos    = {1,4,2,5}      all distinct ✅
               neg    = {-1,-2,2,1}    all distinct ✅
```

**And the mirror image** starting from (0,2) gives the second solution. Total: **2** ✅

The dead end at row 2 is the crucial moment — note how the un-choose restored all three sets exactly, leaving row 1 free to try a different column.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n!)</summary>

**O(n!)** roughly, and this is a genuine improvement over the naive bound.

**Why n! rather than nⁿ.** Without pruning, n choices per row across n rows gives nⁿ. But the `cols` set means each column is used at most once — so row 0 has n choices, row 1 has at most n−1 remaining columns, and so on: **n × (n−1) × … × 1 = n!**

**And the diagonals prune much further.** The true node count is far below n!, because most column choices are also diagonally blocked. The trace shows this — at row 2, *every* column was already attacked.

**The actual solution counts** show how aggressive the pruning is:

| n | n! | Solutions |
|---|---|---|
| 4 | 24 | **2** |
| 6 | 720 | 4 |
| 8 | 40,320 | **92** |
| 9 | 362,880 | 352 |

At n = 9 the answer is 352 solutions from a nominal 362,880-node search — and the diagonal checks discard most branches long before a leaf.

**Per node the work is O(1)** — three set lookups — thanks to the diagonal identities. Scanning the board instead would make every check O(n), multiplying the whole runtime.

**Recording a solution is O(n²)** for the joins, but that only happens at the (few) leaves.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²)</summary>

**O(n²)**, dominated by the board.

| Component | Size |
|---|---|
| `board` | n × n characters → **O(n²)** |
| Three sets | at most n entries each → **O(n)** |
| Recursion depth | exactly n — one frame per row → **O(n)** |
| `result` | the required output, O(solutions × n²) |

So: **"O(n²) for the board, O(n) for the sets and recursion."**

**Could the board be dropped?** Yes — you only need the column chosen for each row, which is O(n):

```python
queens = []              # queens[row] = col
# reconstruct the board only when a solution is found
```

That makes auxiliary space **O(n)**, building the n×n board just once per solution rather than maintaining it throughout. A real optimization worth mentioning.

**The bitmask variant goes further:** replace the three sets with three integers, using bit `i` to mark column/diagonal `i`. **O(1) space** for the state, and the checks become single bitwise operations:

```python
if col_mask & (1 << col): continue
```

Faster and tighter, but much harder to read. **Know it exists; write the sets version** — the same judgement as Quickselect in [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md).
→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The first simplification is that no two queens share a row, so exactly one queen goes in each row — that turns 'choose n squares from n²' into 'choose one column per row', and makes the recursion one level per row. Then I need an O(1) safety check. Columns are easy — a set of used columns. For diagonals, the trick is that `row - col` is constant along one diagonal direction and `row + col` along the other, so each diagonal has a unique identity I can keep in a set. A placement is safe if none of the three sets contains its key. The demanding part is the backtracking: I'm mutating four pieces of state — three sets and the board — so all four must be undone on the way back out. Forgetting one, especially a set removal, permanently blocks a column or diagonal and silently loses solutions. Roughly O(n!) with heavy pruning; O(n²) space for the board."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do `row ± col` identify diagonals?" | **The question.** Stepping along a ↘ diagonal increments both, so the difference is invariant; along ↙ one increments and the other decrements, so the sum is invariant. |
| "Why no set for rows?" | The recursion places exactly one queen per row by construction — row conflicts are structurally impossible. |
| "Reduce the space." | Store only `queens[row] = col` (O(n)) and build the board once per solution. Or use bitmasks for O(1) state. |
| "Just **count** the solutions?" | Same search, increment a counter instead of building boards — that's LeetCode 52, and it's noticeably faster without the O(n²) joins. |
| "Exploit symmetry?" | Solutions come in mirror pairs, so you can search only the first ⌈n/2⌉ columns of row 0 and reflect. Roughly halves the work. |
| "Why is it n! and not nⁿ?" | The column set means each column is used at most once, so the choices shrink each row. |
| "How would you speed it up further?" | Bitmasks, symmetry pruning, and choosing the most-constrained row first (though here rows are processed in order by design). |

**Traps:**

- **Forgetting one of the four un-choose steps.** *The* bug of this problem — a stale set entry blocks a column or diagonal forever and solutions vanish with no error.
- **`[["."] * n] * n`** — n references to one row, so every queen appears in every row.
- **Appending `board` instead of joining** — all results alias the same mutating board.
- **Swapping the diagonal formulas.** Both `row+col` and `row-col` produce plausible-looking numbers, so the bug is silent. Verify on `(0,0)` and `(1,1)`.
- **Checking rows too** — harmless but redundant, and it signals you missed the structural guarantee.
- **Scanning the board to validate placements** — correct but O(n) per check instead of O(1).

**This same move shows up in:** [Permutations](46-permutations.md) (multiple state pieces chosen and un-chosen together) · [Valid Sudoku](36-valid-sudoku.md) (sets tracking rows/columns/boxes, and the same `[[...]] * n` trap) · [Word Search](79-word-search.md) (marking and restoring during a search) · [Subsets](78-subsets.md) (the skeleton) · [backtracking](../algorithms/backtracking.md).

</details>

---
