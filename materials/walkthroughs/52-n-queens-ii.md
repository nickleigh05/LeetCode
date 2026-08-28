# 52. N-Queens II

**Hard** · [LeetCode](https://leetcode.com/problems/n-queens-ii/) · [Solution file (no hints)](../../problems/0001-0499/52.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Return **how many** distinct solutions there are to the n-queens puzzle: `n` queens on an `n × n` board, no two attacking each other.

```
n = 1  →  1
n = 4  →  2
n = 8  →  92
```

**Constraints:** `1 <= n <= 9`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the **n-queens** puzzle" | You already have this: [N-Queens](51-n-queens.md) |
| "return the **number** of" | ⚠️ **Count**, don't collect. The board disappears entirely |
| "**distinct** solutions" | No symmetry-folding — reflections and rotations count separately |
| `n <= 9` | Small; the count grows fast (n=9 → 352) |

**This is [N-Queens](51-n-queens.md) with the output thrown away.** That sounds like a trivial variation, and the *code* change is trivial — but what you get to delete is the interesting part.

In [N-Queens](51-n-queens.md) the board existed for one reason: to render the answer as strings of `.` and `Q`. If you only need a count, the board is dead weight:

```python
board = [["."] * n for _ in range(n)]     # ← delete
board[row][col] = "Q"                     # ← delete
board[row][col] = "."                     # ← delete
result.append(["".join(r) for r in board])# ← becomes: return 1
```

**Three of the four pieces of state vanish.** What remains is what actually drives the search — the three attack sets:

| State | Needed to *find* solutions? | Needed to *count* them? |
|---|---|---|
| `cols` | ✅ | ✅ |
| `pos_diag` (`row + col`) | ✅ | ✅ |
| `neg_diag` (`row − col`) | ✅ | ✅ |
| `board` | ✅ — it *is* the output | ❌ **delete** |

Recognising that the board was never part of the algorithm — only of the presentation — is the point of this problem.

**The counting shape**, same as [Beautiful Arrangement](526-beautiful-arrangement.md):

```python
if row == n:
    return 1                      # one complete placement = one solution
...
count += backtrack(row + 1)       # sum what the children found
return count
```

**A quick refresher on the two diagonals**, since they're the part people forget:

```
row + col constant  (↗ anti-diagonal)     row − col constant  (↘ main diagonal)

  0 1 2 3                                   0 1 2 3
0 0 1 2 3                                 0 0 -1 -2 -3
1 1 2 3 4                                 1 1  0 -1 -2
2 2 3 4 5                                 2 2  1  0 -1
3 3 4 5 6                                 3 3  2  1  0
```

Two cells attack along a diagonal exactly when they share one of these values. **One queen per row is structural** (the recursion advances by row), so rows never need checking.

🤔 **Before you open the next section:** the recursion places one queen per row. What would have to change if you wanted to place them column by column instead — and would the answer differ?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Call [N-Queens](51-n-queens.md), return `len(result)` | Build every board, count them | O(n!) + O(n²) per solution | ⚠️ Correct; wastes all the board work |
| Check all C(n²,n) placements | Brute force | astronomically bad | ❌ |
| **Backtracking with three sets** | [N-Queens](51-n-queens.md) minus the board | **O(n!) bound, far less in practice** | ✅ |
| **Bitmask backtracking** | Three integers instead of three sets | same bound, **~3.3× faster** | ✅ ← the classic |
| Hard-coded lookup table | n ≤ 9 → nine numbers | O(1) | ❌ Answers nothing |

**The decision: backtracking with three sets** — and know the bitmask version, because on this specific problem it's the canonical optimisation.

**Why not just call [N-Queens](51-n-queens.md) and take the length?** It works. It also allocates an n×n board, writes `"Q"`, writes `"."`, and joins n strings **per solution** — at n=9 that's 352 boards built and immediately discarded. Costing O(n²) per solution to produce something you throw away is exactly what the problem is asking you to notice.

**The bitmask version** replaces the three sets with three integers, one bit per column:

```python
def backtrack(row, cols, pos, neg):
    if row == n:
        return 1
    count = 0
    available = ~(cols | pos | neg) & ((1 << n) - 1)
    while available:
        bit = available & -available          # lowest set bit
        available ^= bit                      # clear it
        count += backtrack(row + 1, cols | bit, (pos | bit) << 1, (neg | bit) >> 1)
    return count
```

**The trick that makes it work:** instead of storing diagonals as `row + col` and `row − col` keys, the masks are **shifted** as you descend a row. A diagonal threat moves one column left or right per row, so `<< 1` and `>> 1` carry the threat forward automatically — and threats shifted off the edge disappear for free.

| Piece | What it does |
|---|---|
| `~(cols \| pos \| neg) & ((1 << n) - 1)` | All safe columns at once — **one operation instead of n set lookups** |
| `available & -available` | Isolate the lowest set bit (two's-complement idiom) |
| `available ^= bit` | Clear that bit and move on |
| `(pos \| bit) << 1` | Anti-diagonal threats shift left going down a row |
| `(neg \| bit) >> 1` | Main-diagonal threats shift right |

Measured, both giving identical counts:

| n | answer | sets | bitmask | speedup |
|---|---|---|---|---|
| 11 | 2,680 | 0.087s | 0.026s | **3.4×** |
| 12 | 14,200 | 0.462s | 0.138s | **3.3×** |

**Same asymptotic bound, ~3.3× constant factor** — and it's immutable state passed down as arguments, so there's no un-choose step at all. **Write the set version, mention the bitmask one.** At n ≤ 9 the difference is invisible; the reason to know it is that it's the standard follow-up.

→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
cols = set()
pos_diag = set()   # row + col is constant along this diagonal
neg_diag = set()   # row - col is constant along this diagonal
```

**Three sets, no board.** Each records the *keys* that are already under attack.

Sets give O(1) membership, which is what makes the safety test cheap.
→ [set-basics](../syntax/set-basics.md)

```python
def backtrack(row):
    if row == n:
        return 1
```

**Base case: all n rows filled → one complete solution.**

`return 1` instead of appending a board. This is the whole difference from [N-Queens](51-n-queens.md).
→ [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md)

```python
    count = 0
    for col in range(n):
        if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
            continue
```

**Try each column in this row**, skipping any that's attacked.

Three checks, no row check — one queen per row is guaranteed by the recursion's structure, not by a test.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [break-continue](../syntax/break-continue.md)

```python
        cols.add(col)
        pos_diag.add(row + col)
        neg_diag.add(row - col)
```

**Choose — three pieces of state.**

```python
        count += backtrack(row + 1)
```

**Explore, and accumulate.** `count +=` rather than discarding the return value — the counting shape.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        cols.remove(col)
        pos_diag.remove(row + col)
        neg_diag.remove(row - col)
```

**Un-choose — all three.** ⚠️ Every mutation on the way down must be reversed on the way up. Missing one leaves a phantom queen attacking squares forever, and the count comes out too low.

Note there's **one fewer** thing to undo than in [N-Queens](51-n-queens.md), which also had to restore `board[row][col] = "."`.
→ [set-operations](../syntax/set-operations.md)

```python
    return count

return backtrack(0)
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def totalNQueens(self, n: int) -> int:

        cols = set()
        pos_diag = set()   # row + col is constant along this diagonal
        neg_diag = set()   # row - col is constant along this diagonal

        def backtrack(row):
            if row == n:
                return 1

            count = 0
            for col in range(n):
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)

                count += backtrack(row + 1)

                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)

            return count

        return backtrack(0)
```

</details>

**Trace it** — `n = 4`. The first solution found, then the blocked branch that follows. Verified output:

| Depth | Cell | Test | `cols` / `pos` / `neg` |
|---|---|---|---|
| 0 | r0c0 | ✓ place | `{0}` / `{0}` / `{0}` |
| 1 | r1c0 | ✗ column | |
| 1 | r1c1 | ✗ ↘ diag (r−c = 0) | |
| 1 | r1c2 | ✓ place | `{0,2}` / `{0,3}` / `{−1,0}` |
| 2 | r2c0 | ✗ column | |
| 2 | r2c1 | ✗ ↗ diag (r+c = 3) | |
| 2 | r2c2 | ✗ column | |
| 2 | r2c3 | ✗ ↘ diag (r−c = −1) | |
| 2 | — | **row 2 has no safe square → backtrack** ⚠️ | |
| 1 | r1c3 | ✓ place | `{0,3}` / `{0,4}` / `{−2,0}` |
| 2 | r2c1 | ✓ place | `{0,1,3}` / `{0,3,4}` / `{−2,0,1}` |
| 3 | r3c0–c3 | all ✗ | |
| … | | *(the whole c0 branch fails)* | |
| 0 | r0c1 | ✓ place | `{1}` / `{1}` / `{−1}` |
| 1 | r1c3 | ✓ place | `{1,3}` / `{1,4}` / `{−2,−1}` |
| 2 | r2c0 | ✓ place | `{0,1,3}` / `{1,2,4}` / `{−2,−1,2}` |
| 3 | r3c2 | ✓ place | `{0,1,2,3}` / `{1,2,4,5}` / `{−2,−1,1,2}` |
| 4 | — | `row == n` → **count 1** ✅ | |

Continuing, `r0c2` yields the mirror solution and `r0c3` yields nothing. **Total = 2** ✅

**The ⚠️ row is backtracking doing its job.** With queens at r0c0 and r1c2, *every* square in row 2 is attacked — the loop finishes without a single placement, `count` stays 0, and the frame returns 0. The parent then un-chooses r1c2 and tries r1c3 instead.

**Notice the diagonal keys going negative.** `neg_diag` holds `−2, −1, 1, 2` in that last solution. `row − col` ranges over `−(n−1) … (n−1)`, which is exactly why a **set** is the natural container — an array would need an offset of `n−1` to index safely. (The bitmask version handles this by shifting rather than indexing.)

**The solution counts** — worth recognising, since they don't follow any pattern:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| solutions | 1 | **0** | **0** | 2 | 10 | 4 | 40 | 92 | 352 |

**n = 2 and n = 3 have no solutions at all** — a good edge case to check your code against, and the reason `n=6` (4 solutions) dipping below `n=5` (10) isn't a bug.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n!) bound, dramatically less in practice</summary>

**O(n!)** as a bound — n choices in row 0, at most n−1 in row 1, and so on.

But the constraints prune so hard that the real work is far below it. **Measured node counts:**

| n | solutions | nodes visited | n! |
|---|---|---|---|
| 4 | 2 | 17 | 24 |
| 6 | 4 | 153 | 720 |
| 8 | 92 | 2,057 | 40,320 |
| 9 | 352 | 8,394 | 362,880 |
| 12 | 14,200 | 856,189 | 479,001,600 |

At n=12 the search visits **856K nodes against 479M permutations — 560× fewer**. The gap widens with n, because the diagonal constraints eliminate most partial placements within the first few rows.

**The honest interview answer:**

> "The bound is O(n!), but that's loose — the diagonal constraints prune heavily, so at n=12 it's under a million nodes against 479 million permutations. There's no known polynomial algorithm; counting n-queens solutions is genuinely hard, and the values are found by search, not formula."

**Per node** the cost is O(n) — scanning n columns with O(1) set lookups. The bitmask version computes all safe columns in a single machine word operation, which is where its 3.3× comes from.

**⚠️ There is no closed form.** Unlike most counting problems, n-queens solution counts have no known formula and no polynomial algorithm; known values run only into the high twenties, each requiring substantial computation. If asked "can you do better than exponential?" — **no, and saying so confidently is the right answer.**

**Why it's cheaper than [N-Queens](51-n-queens.md):** that problem additionally pays O(n²) per solution to build and join the board strings. At n=9 that's 352 × O(81) of pure formatting work this version skips.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary** — and unlike [N-Queens](51-n-queens.md), **the output is O(1)**.

| Component | Size |
|---|---|
| **Recursion depth** | exactly n — one frame per row → **O(n)** |
| `cols` | at most n entries → O(n) |
| `pos_diag` | at most n entries → O(n) |
| `neg_diag` | at most n entries → O(n) |
| Output | a single integer → **O(1)** |

**The comparison that makes the point:**

| | [N-Queens](51-n-queens.md) | **N-Queens II** |
|---|---|---|
| Auxiliary | O(n²) — the board | **O(n)** |
| Output | **O(n² · solutions)** | **O(1)** |
| At n=9 | 352 boards × 81 chars ≈ 28,500 chars | **one integer** |

Dropping the board removes both an O(n²) working buffer **and** the entire output term. That's the actual substance of this "easier variant".

**The bitmask version does better still: O(n) for the stack and nothing else** — three integers passed as arguments rather than three sets. Since they're immutable, there's no shared mutable state at all, and no un-choose step:

| Version | Auxiliary |
|---|---|
| Three sets | O(n) sets + O(n) stack |
| **Bitmask** | **O(n) stack only** |

**The recursion is n deep, not n! deep** — n! counts root-to-leaf paths; one path is on the stack at a time. With n ≤ 9 the stack is trivial.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is N-Queens with the output dropped, and what's interesting is what that lets me delete. In N-Queens the board existed only to render the answer as strings — the search itself never reads it. So here I keep just the three attack sets: occupied columns, occupied anti-diagonals keyed by `row + col`, and occupied main diagonals keyed by `row − col`. Rows need no tracking because the recursion places exactly one queen per row by construction. The base case returns 1 instead of appending a board, and each frame sums what its children return. Every choose has a matching un-choose across all three sets. The bound is O(n!), but it's loose — the constraints prune hard, about 856,000 nodes at n=12 against 479 million permutations. The standard optimisation is bitmasks: three integers instead of three sets, with the diagonal masks shifted left and right as you descend, which computes all safe columns in one operation and runs about 3.3× faster."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What changes from [N-Queens](51-n-queens.md)?" | **The question.** Delete the board, return 1 at the base case, accumulate counts. The board was presentation, never algorithm. |
| "Why no row check?" | The recursion advances one row per level, so exactly one queen per row is structural. |
| "Explain the diagonal keys." | `row + col` is constant along ↗, `row − col` along ↘. Two queens attack diagonally iff they share one of these. |
| "Why sets and not arrays?" | `row − col` ranges over `−(n−1)…(n−1)`; an array needs an `n−1` offset. Sets sidestep the indexing. |
| "Can you speed it up?" | Bitmasks — three integers, `~(cols\|pos\|neg) & ((1<<n)-1)` for all safe columns at once, diagonals shifted per row. ~3.3× measured. |
| "Exploit **symmetry**?" | Yes: solutions come in mirror pairs, so search only half the first row and double, adjusting for the centre column when n is odd. Roughly 2×. Careful — the problem wants *distinct* solutions, so you double the count rather than dedupe. |
| "Better than exponential?" | **No.** No known polynomial algorithm and no closed form. Being definite here is correct. |
| "Why do n=2 and n=3 give 0?" | Too cramped — every placement in row 0 attacks all of row 1 via column or diagonal. A good edge-case test. |
| "n = 20?" | Feasible with bitmasks and patience; the counts grow into the tens of billions. Past the high twenties it becomes a research-scale computation. |

**Traps:**

- **Keeping the board.** Correct but wasteful — O(n²) of state and O(n²) per solution to build strings nobody reads.
- **Forgetting to un-choose one of the three sets.** Leaves a phantom queen; the count comes out **too low**, which is much harder to spot than a crash.
- **Using `pos_diag` for `row − col`** and vice versa — swapping them still *runs*, and still gives 2 for n=4, but diverges at larger n. Verify against n=8 → 92.
- **Checking rows** — harmless, just dead code that suggests you haven't seen why it's unnecessary.
- **Returning `len(result)` from [N-Queens](51-n-queens.md)** — passes, but misses the entire point of the variant.
- **Using a list instead of a set** for the attack keys — turns O(1) lookups into O(n), silently slower.
- **Hard-coding the nine answers** — the constraint `n <= 9` invites it; don't.

**This same move shows up in:** [N-Queens](51-n-queens.md) (the same search, collecting boards instead of counting) · [Beautiful Arrangement](526-beautiful-arrangement.md) (the identical count-don't-collect shape, also a constrained assignment) · [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) (backtracking where symmetry between equivalent states is what to prune) · [backtracking](../algorithms/backtracking.md).

</details>

---
