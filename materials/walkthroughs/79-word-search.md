# 79. Word Search

**Medium** · [LeetCode](https://leetcode.com/problems/word-search/)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.

The word can be constructed from letters of **sequentially adjacent** cells (horizontally or vertically neighbouring), and **the same cell may not be used more than once**.

```
board = [["A","B","C","E"],       word = "ABCCED"  →  true
         ["S","F","C","S"],       word = "SEE"     →  true
         ["A","D","E","E"]]       word = "ABCB"    →  false
                                    (the B would have to be reused)
```

**Constraints:** `1 <= m, n <= 6` · `1 <= word.length <= 15` · lowercase and uppercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sequentially adjacent**" | A path through the grid, stepping up/down/left/right — a DFS over a 2-D grid |
| "may not be used **more than once**" | ⚠️ Mark cells as visited *during* a path, and **un-mark on the way back** — that's the backtracking |
| return `true`/`false` | Existence only, so you can **return at the first success** |
| the word can start **anywhere** | Try a search from every cell |
| grid ≤ 6×6, word ≤ 15 | Tiny — exponential search is expected |

**Why the "no reuse" rule needs backtracking rather than a permanent visited set.** Consider `"ABCB"` on the example board: `A → B → C` works, but then the next `B` would have to be the same cell used at step 2. That must fail.

But a cell used by *this* path must become available again to a **different** path. If you marked cells permanently, a failed exploration would poison the grid for every subsequent attempt.

So the mark is **scoped to the current path**:

```
mark  →  explore all 4 neighbours  →  UN-mark
```

That's exactly [Subsets](78-subsets.md)'s choose → explore → un-choose, but the "choice" is *"this cell is part of my current path"* rather than *"this element is in my subset"*.

**The shape of the search.** At each step you're at some grid cell, needing to match `word[i]`. You have up to 4 moves, and the word must be matched in order. That's a decision tree of depth `len(word)` with branching factor ≤ 4.

🤔 **Before you open the next section:** you need to mark a cell as "in use" without allocating a separate structure. What could you overwrite it with, given the constraints?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Enumerate all paths, compare each to the word | Generate every path of length L, test it | ❌ Explores paths that diverge from the word immediately |
| DFS + a `visited` set of coordinates | Track visited cells in a set | ✅ Correct, O(L) extra space |
| **DFS + in-place marking** | Overwrite the cell, restore on the way back | ✅ O(1) extra |

**The decision: DFS from every cell, marking visited cells in place and restoring them on backtrack.**

The recursion has three base cases, and their **order matters**:

| Check | Meaning |
|---|---|
| `i == len(word)` | **Success** — the whole word matched. Must come first |
| out of bounds | Stepped off the grid |
| `board[row][col] != word[i]` | Wrong letter (or `"#"` — already on this path) |

**Why the success check comes first.** When `i == len(word)` there is no `word[i]` to compare against — testing the letter first would raise `IndexError`. And logically, matching the full word is success regardless of where you happen to be standing.

**The `"#"` marking trick.** Overwriting a cell with a character that can't appear in the word means the `board[row][col] != word[i]` check does double duty: it rejects both *wrong letters* and *already-visited cells*, with no separate test.

That's genuinely elegant — one comparison enforcing two rules — and it costs **zero extra space**. The alternative, a `visited` set, needs O(L) and an extra condition in the guard.

⚠️ **The restore is non-negotiable.** `board[row][col] = letter` on the way out is what makes the mark path-scoped. Omit it and the grid degrades permanently: cells consumed by a failed attempt stay `"#"` forever, so later starting positions search a corrupted board. **This is the defining bug of the problem.**

**Why `or` chains the four directions.** You need the word to be findable via *some* neighbour — existence, not universality. And `or` **short-circuits**, so as soon as one direction succeeds the remaining three aren't explored. Same `any`/`or` semantics as [Subtree of Another Tree](572-subtree-of-another-tree.md) and [Design Add and Search Words](211-design-add-and-search-words-data-structure.md).

**Note the bounds check is inside the recursion**, not before the call. Both styles work; checking inside keeps the four recursive calls uniform and short.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(board)
cols = len(board[0])
```

Grid dimensions, captured once for the bounds checks.
→ [nested-lists](../syntax/nested-lists.md) · [list-basics](../syntax/list-basics.md)

```python
def dfs(row, col, i):
    if i == len(word):
        return True
```

**Success base case, and it must come first.** Every character has been matched.

Placing it before the letter comparison avoids indexing `word[i]` out of range — and it's the logically correct precedence: a fully matched word is a success no matter where the cursor sits.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [if-return](../syntax/if-return.md)

```python
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False
```

**Bounds check.** Stepping off the grid fails this path.

Doing it inside the recursion (rather than before each call) keeps the four calls below uniform.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if board[row][col] != word[i]:
        return False
```

**The letter check — doing two jobs at once.** It fails if the cell holds the wrong letter, **and** if the cell is `"#"` (already on the current path), since `"#"` never matches a letter of the word.

One comparison enforcing both the matching rule and the no-reuse rule.

```python
    letter = board[row][col]
    board[row][col] = "#"
```

**Choose.** Save the real letter so it can be restored, then mark the cell as in-use for this path.

`"#"` is safe because the word contains only letters — the constraint guarantees no collision.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    found = (dfs(row + 1, col, i + 1) or
             dfs(row - 1, col, i + 1) or
             dfs(row, col + 1, i + 1) or
             dfs(row, col - 1, i + 1))
```

**Explore all four neighbours**, each advancing to the next character.

`or` because success in **any** direction is enough — and it short-circuits, so a match down the first branch skips the other three entirely.
→ [logical-operators](../syntax/logical-operators.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    board[row][col] = letter
    return found
```

**Un-choose — restore the cell.** This must happen **before** returning, on both the success and failure paths, so the grid is left exactly as it was found.

Note `found` is computed first and stored, precisely so the restore can happen before the return. Writing `return dfs(...) or ...` directly would skip the restoration entirely.
→ [if-return](../syntax/if-return.md)

```python
for row in range(rows):
    for col in range(cols):
        if dfs(row, col, 0):
            return True
return False
```

**Try every starting cell**, since the word may begin anywhere. Return at the first success.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:

        rows = len(board)
        cols = len(board[0])

        def dfs(row, col, i):
            if i == len(word):
                return True
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            if board[row][col] != word[i]:
                return False

            letter = board[row][col]
            board[row][col] = "#"

            found = (dfs(row + 1, col, i + 1) or
                     dfs(row - 1, col, i + 1) or
                     dfs(row, col + 1, i + 1) or
                     dfs(row, col - 1, i + 1))

            board[row][col] = letter
            return found

        for row in range(rows):
            for col in range(cols):
                if dfs(row, col, 0):
                    return True
        return False
```

</details>

**Trace it** — finding `"SEE"` on the example board:

```
        col: 0    1    2    3
row 0:       A    B    C    E
row 1:       S    F    C    S
row 2:       A    D    E    E
```

Starting at `(1,3)` = `S`:

| Step | Cell | `word[i]` | Match? | Board state |
|---|---|---|---|---|
| 1 | (1,3) `S` | `S` (i=0) | ✅ | mark (1,3) = `#` |
| 2 | try (2,3) `E` | `E` (i=1) | ✅ | mark (2,3) = `#` |
| 3 | try (2,2) `E` | `E` (i=2) | ✅ | mark (2,2) = `#` |
| 4 | `i == 3 == len(word)` | | **`return True`** ✅ | |

All three cells are restored as the recursion unwinds.

**And the failure case** — `"ABCB"` starting at `(0,0)`:

| Step | Cell | `word[i]` | Result |
|---|---|---|---|
| 1 | (0,0) `A` | `A` | ✅ mark `#` |
| 2 | (0,1) `B` | `B` | ✅ mark `#` |
| 3 | (0,2) `C` | `C` | ✅ mark `#` |
| 4 | (0,1) — the B again | `B` | ❌ cell is now `"#"`, not `B` |
| | (1,2) `C`, (0,3) `E` | `B` | ❌ wrong letters |

All branches fail, every cell is restored to its original letter, and the search moves on to the next starting cell — eventually returning `False` ✅

**The restoration is what makes that work.** Without it, cells `(0,0)`, `(0,1)` and `(0,2)` would remain `"#"` and every later starting position would search a broken board.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n · 4^L)</summary>

**O(m · n · 4^L)**, more precisely **O(m · n · 3^L)** after the first step, where L is the word length.

- **m · n starting cells** — the word can begin anywhere.
- **Each path branches up to 4 ways**, but after the first step one neighbour is the cell you just came from (now `"#"`), so it's really **3** onward.
- **Depth L** — the path length equals the word length.

With m, n ≤ 6 and L ≤ 15 the bound is large in theory but tiny in practice, because **most branches die at the very first letter comparison**.

**Why the real cost is far below the bound.** The letter check `board[row][col] != word[i]` prunes immediately — a path only continues while it's still spelling the word. On a random board, the vast majority of the m·n starting cells fail on step 1.

**No memoization is possible.** Whether a cell can continue the word depends on which cells are *currently marked*, which differs per path — so results can't be cached. That's characteristic of backtracking problems: **the state includes the path, not just the position.**

**Compare with [Word Search II](212-word-search-ii.md):** searching for many words, running this once per word is hopeless. There a trie merges the searches so shared prefixes are explored once — the same grid DFS, with the word list restructured.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(L)</summary>

**O(L)** for the recursion stack — one frame per character matched, so the depth equals the word length. With L ≤ 15, trivially small.

**The in-place marking costs nothing.** Overwriting cells and restoring them uses **O(1)** extra space, versus a `visited` set which would hold up to L coordinates:

| Approach | Extra space | Note |
|---|---|---|
| **In-place `"#"` marking** | **O(1)** | ⚠️ Mutates the input during the search |
| `visited` set of `(row, col)` | **O(L)** | Non-destructive |

**The trade is real.** In-place marking is free and lets one comparison enforce two rules — but it **temporarily corrupts the caller's board**. If the grid were shared across threads, or the caller inspected it mid-search, that would be a genuine bug.

The board *is* fully restored by the time the function returns, so the mutation is invisible to a single-threaded caller. **Worth raising as an API consideration** — it's the kind of detail that distinguishes "it works" from "I know what it costs".

**Why `"#"` is safe here:** the constraints guarantee the board and word contain only letters, so the marker can never be mistaken for data. With arbitrary characters you'd need the `visited` set instead — the same "pick a sentinel that can't collide with data" concern as [Encode and Decode Strings](271-encode-and-decode-strings.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The word can start anywhere, so I DFS from every cell, matching one character per step and branching to the four neighbours. The no-reuse rule is what makes it backtracking rather than plain DFS: a cell used by the current path must be blocked, but it has to become available again to other paths — so I mark it, explore, and restore it on the way back. I mark by overwriting the cell with `#`, which is safe because the word is letters only, and that makes one comparison enforce two rules at once: wrong letter *or* already on this path. The restore has to happen before returning on both the success and failure paths, otherwise a failed attempt leaves the board permanently corrupted. The four directions are chained with `or`, so it short-circuits on the first success. O(m·n·4^L) worst case, O(L) space for the recursion."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why un-mark the cell?" | **The question.** The mark is scoped to the current path. Without the restore, a failed attempt poisons the grid for every later starting cell. |
| "Why does the success check come first?" | At `i == len(word)` there's no `word[i]` to compare — checking the letter first raises `IndexError`. |
| "Avoid mutating the input." | Use a `visited` set of coordinates — O(L) extra space, and the guard needs an extra condition. |
| "What if the board could contain `#`?" | The marker would collide with data. Use a `visited` set instead. |
| "Now find **many** words." | Running this per word is hopeless — build a trie of all words and walk it alongside the grid. That's [Word Search II](212-word-search-ii.md). |
| "Can you memoize?" | No — whether a cell can extend the word depends on which cells are currently marked, which varies per path. |
| "Allow diagonal moves?" | Extend to 8 directions. Everything else is unchanged. |

**Traps:**

- **Forgetting to restore the cell.** *The* bug of this problem — the board degrades and later searches fail mysteriously.
- **Restoring after `return`**, so it never executes. Compute `found` into a variable first, restore, *then* return.
- **Checking the letter before the length.** `word[i]` raises `IndexError` when `i == len(word)`.
- **Using `and` instead of `or`** across the directions — you'd require the word to be findable in all four.
- **Marking with a character that could appear in the word** — the check would wrongly reject valid cells.
- **A permanent global `visited`** shared across starting cells — same corruption as forgetting the restore.

**This same move shows up in:** [Word Search II](212-word-search-ii.md) (this DFS with a trie, for many words at once) · [Subsets](78-subsets.md) (choose → explore → un-choose) · [Number of Islands](200-number-of-islands.md) (grid DFS, but with *permanent* marking since revisiting is never needed) · [grids primer](../learning/10b-grids-primer.md) · [backtracking](../algorithms/backtracking.md).

</details>
