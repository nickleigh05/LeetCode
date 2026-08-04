# 72. Edit Distance

**Hard** · [LeetCode](https://leetcode.com/problems/edit-distance/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two strings `word1` and `word2`, return the **minimum number of operations** required to convert `word1` into `word2`. You have three operations available: **insert** a character, **delete** a character, **replace** a character.

```
word1 = "horse",   word2 = "ros"     →  3
        horse → rorse (replace 'h' with 'r')
              → rose  (delete 'r')
              → ros   (delete 'e')

word1 = "intention", word2 = "execution"  →  5
word1 = "",        word2 = "abc"     →  3   (three inserts)
```

**Constraints:** `0 <= word1.length, word2.length <= 500` · lowercase English letters only.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** number of operations" | Optimization → `min`. Compare [Longest Common Subsequence](1143-longest-common-subsequence.md) (max) and [Distinct Subsequences](115-distinct-subsequences.md) (sum) over the same grid |
| **three** operations | Three branches in the recurrence, versus LCS's two. That's the only structural difference |
| two strings, converting one to the other | The state is `(position in word1, position in word2)` — the Unit 14 shape again |
| operations act on single characters | Every operation costs exactly 1 and advances at least one position, which is what makes the recursion terminate |
| lengths up to 500, possibly **0** | 500 × 500 = 2.5 × 10⁵ cells — fine. And empty strings are legal, so the base cases must handle them |

This is **Levenshtein distance**, one of the most-used algorithms in practice — spell checkers, `diff`, DNA alignment, fuzzy search all run on it. Worth knowing by name.

The derivation. Let `dp[i][j]` = the edit distance between the suffixes `word1[i:]` and `word2[j:]`. Stand there and look at the first character of each.

**If they match** — `word1[i] == word2[j]` — there is nothing to do at this position. Move past both, **free**:

```
dp[i][j] = dp[i+1][j+1]
```

**If they don't match**, you must spend one operation, and there are exactly three things you can do:

| Operation | What it does to the strings | New state |
|---|---|---|
| **Delete** `word1[i]` | Drops a character from the source | `dp[i+1][j]` |
| **Insert** `word2[j]` | Adds the needed character to the source, so it's now matched | `dp[i][j+1]` |
| **Replace** `word1[i]` with `word2[j]` | Both characters are now handled | `dp[i+1][j+1]` |

Take the cheapest and add 1:

```
dp[i][j] = 1 + min( dp[i+1][j], dp[i][j+1], dp[i+1][j+1] )
```

The mapping of operation to index movement is the part worth getting straight in your head, since it's the thing that's easy to garble under pressure. **Delete advances only `i`. Insert advances only `j`. Replace advances both** — same as a match, but costing 1.

🤔 **Before you open the next section:** what's the edit distance from `"abc"` to `""`? And from `""` to `"abc"`? Those two answers are your base cases — and unlike most problems in this unit, they're not zero.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every operation sequence | Branch three ways at every step | **O(3^(m+n))** | O(m+n) | ❌ Exponential |
| Greedy — align matching characters | Match what you can, edit the rest | O(m+n) | O(1) | ❌ **Wrong.** Which characters to align isn't locally decidable; `"intention"` → `"execution"` defeats any local rule |
| `m + n − 2 × LCS` | Delete what's not in the LCS, insert what's missing | O(m·n) | O(m·n) | ❌ Correct **only** for insert/delete. With replace available it overcounts — a replace does in one operation what a delete plus an insert does in two |
| Recursion + memo on `(i, j)` | Cache each state | O(m·n) | O(m·n) + stack | ⚠️ Correct; up to m+n frames |
| **Bottom-up 2-D table** | Fill an `(m+1) × (n+1)` grid | O(m·n) | **O(m·n)** | ✅ |
| Two rolling rows | Same recurrence, one row kept | O(m·n) | **O(n)** | ✅ Strictly better space; mention it |

**The decision:** the **bottom-up 2-D table** — the classic Levenshtein implementation.

**Why greedy fails.** The tempting move is to scan both strings and align matching characters as you meet them. But which alignment is best depends on the whole rest of both strings — the same reason greedy fails in [Word Break](139-word-break.md) and [Interleaving String](97-interleaving-string.md). `"intention"` → `"execution"` needs 5 operations, and no left-to-right rule finds that alignment.

**Why the LCS shortcut is wrong here**, which is worth being precise about because it's a tempting "clever" answer. If only insert and delete were allowed, the edit distance really is `m + n − 2·LCS(m, n)` — delete everything in `word1` outside the common subsequence, insert everything in `word2` outside it. But **replace collapses a delete-plus-insert pair into one operation**, so that formula overcounts whenever a replace is useful. On `"horse"` → `"ros"`: LCS is `"os"` (length 2), so the formula gives 5 + 3 − 4 = **4**, while the true answer using replace is **3**. Knowing *why* the shortcut fails is a stronger signal than not knowing it exists.

**The base cases, answering section 1's question.** These are the interesting part of this problem, and they're not zero:

- **`dp[m][j] = n - j`** — `word1` is exhausted, so **insert** each remaining character of `word2`. That's `n - j` operations.
- **`dp[i][n] = m - i`** — `word2` is exhausted, so **delete** each remaining character of `word1`. That's `m - i` operations.

Both corner cases meet at `dp[m][n] = 0`, consistently. Contrast the rest of the unit, where base cases were a single seeded 1 or `True`; here an entire row and column carry non-trivial values, and they're what makes empty-string inputs work with no special-casing.

**Why bottom-up over memoized recursion?** Same complexity, no stack. With lengths up to 500 the recursion could nest 1000 deep — right at Python's default limit. The table sidesteps it entirely.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m = len(word1)
n = len(word2)

dp = [[0] * (n + 1) for _ in range(m + 1)]
```
`dp[i][j]` = edit distance between `word1[i:]` and `word2[j:]`. The `+1`s make room for the exhausted positions `i = m` and `j = n`.

The [list comprehension](../syntax/list-comprehension.md) is mandatory — `[[0] * (n+1)] * (m+1)` aliases one row `m+1` times, and every write hits all of them.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [string-basics](../syntax/string-basics.md)

```python
for j in range(n + 1):
    dp[m][j] = n - j   # word1 exhausted: insert the rest of word2
```
**Base case one.** With nothing left of `word1`, the only way forward is to **insert** every remaining character of `word2` — one operation each, so `n - j`.

Note this row is not all zeros and not all the same value: it counts down to 0 at `dp[m][n]`, where both strings are done.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
for i in range(m + 1):
    dp[i][n] = m - i   # word2 exhausted: delete the rest of word1
```
**Base case two**, the mirror image. With nothing left to match in `word2`, **delete** every remaining character of `word1` — `m - i` operations.

Both loops write `dp[m][n]`, and they agree: `n - n = 0` and `m - m = 0`. The overlap is harmless.

Together these two lines are why `word1 = ""` or `word2 = ""` need no special handling — the answer is read straight out of a base case.
→ [for-loop](../syntax/for-loop.md) · [nested-lists](../syntax/nested-lists.md)

```python
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
```
Sweep **backwards** in both dimensions. Every dependency (`dp[i+1][j]`, `dp[i][j+1]`, `dp[i+1][j+1]`) sits at a larger index, so those cells must be finalized first.

The loops stop before `m` and `n` so the base rows aren't overwritten.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if word1[i] == word2[j]:
            dp[i][j] = dp[i + 1][j + 1]
```
**The match case: free.** The characters already agree, so no operation is spent — just advance past both, which is the diagonal.

No `min` and no `+1` here. And note there's no reason to consider an operation *anyway*: spending one could never beat spending none, since all costs are non-negative.
→ [comparison-operators](../syntax/comparison-operators.md) · [nested-lists](../syntax/nested-lists.md)

```python
        else:
            dp[i][j] = 1 + min(
                dp[i + 1][j],       # delete word1[i]
                dp[i][j + 1],       # insert word2[j]
                dp[i + 1][j + 1],   # replace word1[i] with word2[j]
            )
```
**The mismatch case: pay 1, take the cheapest of three.**

The comments carry the whole mapping, and it's the thing to be able to reproduce:

- **`dp[i+1][j]` — delete.** Drop `word1[i]` and try again against the same target position. Only `i` advances.
- **`dp[i][j+1]` — insert.** Put `word2[j]` into the source; that target character is now satisfied. Only `j` advances.
- **`dp[i+1][j+1]` — replace.** Overwrite `word1[i]` with `word2[j]`; both are now handled. Both advance.

The `1 +` is the operation you just spent, and it's outside the `min` because all three cost the same.
→ [min-max-key](../syntax/min-max-key.md) · [elif-else](../syntax/elif-else.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[0][0]
```
The distance between the full `word1` and the full `word2`.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for j in range(n + 1):
            dp[m][j] = n - j   # word1 exhausted: insert the rest of word2
        for i in range(m + 1):
            dp[i][n] = m - i   # word2 exhausted: delete the rest of word1

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i + 1][j],       # delete word1[i]
                        dp[i][j + 1],       # insert word2[j]
                        dp[i + 1][j + 1],   # replace word1[i] with word2[j]
                    )

        return dp[0][0]
```
</details>

**Trace it** — `word1 = "horse"`, `word2 = "ros"` (m = 5, n = 3)

The finished table. Each cell is the edit distance between the remaining suffixes:

|  | **j=0** `"ros"` | **j=1** `"os"` | **j=2** `"s"` | **j=3** `""` |
|---|---|---|---|---|
| **i=0** `"horse"` | **3** | 3 | 4 | 5 |
| **i=1** `"orse"` | 3 | 2 | 3 | 4 |
| **i=2** `"rse"` | 2 | 2 | 2 | 3 |
| **i=3** `"se"` | 3 | 2 | 1 | 2 |
| **i=4** `"e"` | 3 | 2 | 1 | 1 |
| **i=5** `""` | 3 | 2 | 1 | 0 |

Answer: `dp[0][0]` = **3** ✅

Reading the base cases first: the **bottom row** counts down 3, 2, 1, 0 — with `word1` gone, insert whatever's left of `"ros"`. The **right column** counts down 5, 4, 3, 2, 1, 0 — with `word2` gone, delete whatever's left of `"horse"`.

Now three interior cells:

**`dp[4][2]`** — `"e"` vs `"s"`, a mismatch. `1 + min(dp[5][2]=1, dp[4][3]=1, dp[5][3]=0)` = 1 + 0 = **1**. Replace wins: one operation turns `"e"` into `"s"`.

**`dp[3][2]`** — `"se"` vs `"s"`. `word1[3] = 's'` matches `word2[2] = 's'`, so it's free: `dp[4][3]` = **1**. That 1 is deleting the leftover `"e"`.

**`dp[0][0]`** — `"horse"` vs `"ros"`, and `'h' ≠ 'r'`. `1 + min(dp[1][0]=3, dp[0][1]=3, dp[1][1]=2)` = 1 + 2 = **3**. **Replace** wins again — turning `'h'` into `'r'` — which matches the worked example in the problem statement exactly.

Following the winning choices from `dp[0][0]` reconstructs the edit script: replace `h`→`r`, then at `dp[1][1]` (`"orse"` vs `"os"`) the `'o'` matches free, then `dp[2][2]` (`"rse"` vs `"s"`) deletes the `'r'`, `dp[3][2]` matches `'s'` free, and `dp[4][3]` deletes the `'e'`. **Three operations.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

- The two base-case loops are O(m) and O(n).
- The nested loops cover **m × n cells**.
- Each cell does one comparison and either a copy or a three-way `min` — **O(1)**.
- **O(m · n)** total.

At the limits, 500 × 500 = **2.5 × 10⁵** cells. Instant.

**Against the alternatives:** trying every operation sequence branches three ways at each step → **O(3^(m+n))**. The DP collapses that because all those sequences pass through only m × n distinct `(i, j)` states — many edit scripts, few states, the same story as the rest of this unit.

**Faster?** Not in general. Edit distance has a **conditional quadratic lower bound**: an O((mn)^(1−ε)) algorithm would refute the Strong Exponential Time Hypothesis. So O(m·n) is essentially optimal, and saying that is the right level of precision.

There are practical refinements worth naming:
- **Ukkonen's algorithm** — if you only need to know whether the distance is at most `k`, you can compute a band of width O(k) around the diagonal in **O(k · min(m,n))**. Very useful for spell-checking, where `k` is small.
- **Bit-parallel (Myers')** — **O(mn/w)** with word size `w`, a 64× constant-factor win in practice.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n), reducible to O(min(m, n))</summary>

**O(m · n) as written** — the full table, 2.5 × 10⁵ integers.

**But it collapses to O(n).** `dp[i][j]` reads `dp[i+1][j]`, `dp[i][j+1]`, and `dp[i+1][j+1]` — all in the current row or the one after it. Two rows suffice:

```python
nxt = list(range(n, -1, -1))          # the dp[m] base row: n-j
for i in range(m - 1, -1, -1):
    cur = [0] * (n + 1)
    cur[n] = m - i                    # the dp[i][n] base case
    for j in range(n - 1, -1, -1):
        if word1[i] == word2[j]:
            cur[j] = nxt[j + 1]
        else:
            cur[j] = 1 + min(nxt[j], cur[j + 1], nxt[j + 1])
    nxt = cur
return nxt[0]
```

**O(n)** space, same time — and by running the loops so the *shorter* string is the inner dimension, **O(min(m, n))**.

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(m·n)** | One entry per state, plus up to m+n stack frames |
| Full 2-D table | **O(m·n)** | Every cell retained |
| **Two rolling rows** | **O(n)** | Each cell reads only the current and next rows |
| Hirschberg's algorithm | **O(min(m,n))** | Linear space *and* reconstructs the edit script, via divide-and-conquer. O(m·n) time still |

**Why keep the full table?** Because it's what lets you **reconstruct the edit script** — walk from `dp[0][0]`, at each step taking whichever branch matched the recorded value, and record the operation. The rolling-row version returns only the count. That's a real trade, and it's the answer to "which would you use" — if a `diff` tool needs to *show* the changes, you need the table (or Hirschberg's, which gets the script in linear space at the cost of a more intricate algorithm).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Levenshtein distance. The state is how far into each string I am, so `dp[i][j]` is the edit distance between the two suffixes. If the current characters match, there's nothing to do — move diagonally for free. If they don't, I spend one operation and take the cheapest of three: delete from word1, which advances only i; insert word2's character, which advances only j; or replace, which advances both. The base cases are the interesting part — if word1 is exhausted I insert everything left of word2, and if word2 is exhausted I delete everything left of word1, so an entire row and column carry counts rather than zeros. That's also why empty-string inputs need no special-casing. I fill backwards since every dependency is at a larger index. O(m·n) time and space, reducible to O(min(m,n)) with rolling rows — though I'd keep the full table if I needed to output the actual edit script."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Which index movement corresponds to which operation?" | Delete advances `i` only, insert advances `j` only, replace advances both. A match also advances both, but free. |
| "Can't you just use `m + n − 2·LCS`?" | Only if replace isn't allowed. Replace does in one operation what delete-plus-insert does in two, so the formula overcounts. On `"horse"`→`"ros"` it gives 4; the answer is 3. |
| "What if the operations had different costs?" | Replace `1 +` with the specific cost per branch: `min(del_cost + dp[i+1][j], ins_cost + dp[i][j+1], rep_cost + dp[i+1][j+1])`. The structure is unchanged. Note that if replace costs more than 2, it's never used and the LCS formula becomes valid again. |
| "Output the actual edit script." | Walk from `dp[0][0]` following whichever branch produced the stored value, recording each operation. Needs the full table — or Hirschberg's algorithm for O(min(m,n)) space. |
| "Reduce the space." | Two rolling rows → O(n), or O(min(m,n)) by putting the shorter string on the inner loop. |
| "Only need to know if the distance is ≤ k?" | Ukkonen's banded algorithm — compute only a diagonal band of width O(k), giving O(k · min(m,n)). Standard for spell-checkers. |
| "What if transpositions were allowed?" | Damerau–Levenshtein: add a fourth branch checking whether swapping two adjacent characters helps. One more term in the `min`. |
| "Can you beat O(m·n)?" | Not in the worst case — an O((mn)^(1−ε)) algorithm would refute SETH. Bit-parallel methods give O(mn/w), a constant-factor win. |

**Traps:**
- **Getting the three index movements wrong.** The most common error, and it produces plausible-but-wrong numbers. Delete = `i+1`, insert = `j+1`, replace = both.
- **Base cases as zeros.** They must be `n - j` and `m - i`; zeroing them means "converting anything to an empty string is free," and every answer comes out too small.
- Adding `1 +` in the match case. Matching is free.
- Including the match branch in the mismatch `min` — `dp[i+1][j+1]` is already there as *replace*; it just costs 1 here instead of 0.
- Reaching for the LCS formula without checking whether replace is available.
- `[[0] * (n+1)] * (m+1)` for the table. Shared row references.
- Forgetting that lengths can be 0. Handled by the base cases, but only if you wrote them.

**This same move shows up in:** [Longest Common Subsequence](1143-longest-common-subsequence.md) (the same grid, maximizing matches — and `m + n − 2·LCS` is the insert/delete-only version of this problem) · [Distinct Subsequences](115-distinct-subsequences.md) (the same grid, counting) · [Interleaving String](97-interleaving-string.md) (the same grid, feasibility) · [Regular Expression Matching](10-regular-expression-matching.md) (a two-string grid where one side is a pattern rather than text) · [Coin Change](322-coin-change.md) (minimize over several branches, each costing 1).

</details>

---
