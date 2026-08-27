# 1143. Longest Common Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-common-subsequence/) · [Solution file (no hints)](../../problems/1000-1499/1143.py)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Given two strings `text1` and `text2`, return the **length of their longest common subsequence**. A subsequence is formed by deleting some or no characters **without changing the relative order** of the rest. If there's no common subsequence, return 0.

```
text1 = "abcde", text2 = "ace"   →  3      "ace"
text1 = "abc",   text2 = "abc"   →  3      the whole string
text1 = "abc",   text2 = "def"   →  0      nothing in common
```

**Constraints:** `1 <= text1.length, text2.length <= 1000` · lowercase English letters only.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**", not substring | Non-contiguous — you may skip freely in both strings. 2^m × 2^n candidate pairs if you enumerate |
| "without changing the relative order" | Order is fixed. You choose *which* characters, never rearrange |
| "**common** to both" | The state has to describe progress through **two** strings at once. One index isn't enough — and that's what makes this 2-D |
| "return the **length**" | You don't have to produce the string. A simplification worth noticing, though here it doesn't change the approach |
| both lengths `<= 1000` | m × n = 10⁶ — fine. 2ⁿ is not. So the intended shape is **O(m·n)** |

Here's the reasoning that gets you to the recurrence. Since one index can't describe the state, use **two**: let `dp[i][j]` be the LCS length of the **prefixes** `text1[:i]` and `text2[:j]`.

Now stand at that state and look at the **last** character of each prefix — `text1[i-1]` and `text2[j-1]`. There are exactly two cases.

**They match.** Then that character can end the common subsequence, and there's never a reason not to use it — pairing them off can only help. So take it and solve the smaller problem with **both** prefixes shortened:

```
dp[i][j] = dp[i-1][j-1] + 1        ← the diagonal, plus one
```

**They don't match.** Then they can't *both* be the final character of the LCS, so at least one of them is useless here. You don't know which, so try both and keep the better:

```
dp[i][j] = max( dp[i-1][j],        ← discard text1's last character
                dp[i][j-1] )       ← discard text2's last character
```

That's the whole algorithm: **diagonal + 1 on a match, max of up-and-left otherwise.**

The one claim worth being able to defend is the greedy step in the match case — *why is it always safe to pair matching characters?* If two prefixes end in the same character, some optimal LCS can be rearranged to end with that pairing without getting shorter. So taking it costs nothing.

🤔 **Before you open the next section:** what is `dp[0][j]` — the LCS of an *empty* prefix and anything? Get that right and the entire table has a foundation; get it wrong and every value is off.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate subsequences | Generate all of `text1`'s, test each against `text2` | **O(2^m · n)** | O(m) | ❌ 2¹⁰⁰⁰ |
| Greedy — match characters left to right | Scan both, pair up whenever you can | O(m+n) | O(1) | ❌ **Wrong.** `"abcde"` vs `"ace"` works by luck; `"ab"` vs `"ba"` shows the failure — greedily pairing `a` blocks `b` |
| Recursion + memo | Cache on `(i, j)` | O(m·n) | O(m·n) + stack | ⚠️ Correct; recursion up to m+n deep |
| **Bottom-up 2-D table** | Fill an `(m+1) × (n+1)` grid | O(m·n) | **O(m·n)** | ✅ |
| Two rolling rows | Same recurrence, keeping only the previous row | O(m·n) | **O(n)** | ✅ Strictly better space; mention it |

**The decision:** the **bottom-up 2-D table** — the canonical form of this algorithm, and the one worth being able to write from memory.

**Why greedy fails.** "Walk both strings, pair up characters when they match" seems reasonable and breaks immediately: `text1 = "ab"`, `text2 = "ba"`. Greedy pairs the `a`s, then can't use the `b`s — answer 1. That's actually correct here, but flip to `text1 = "abcbdab"`, `text2 = "bdcaba"` and greedy's first pairing commits it to a suboptimal branch. **Whether to use a matching character depends on the entire rest of both strings**, which is unknowable locally. That's the DP signal.

**Why the state is two-dimensional, and why it can't be less.** A subproblem is described by *how much of each string remains*. There's no way to compress that into one number — unlike [Coin Change](322-coin-change.md), where "how much is left" was a single value. Two independent positions → a 2-D table. **This is the defining problem of Unit 14**, and most of the unit is variations on it.

**Why prefixes rather than suffixes?** Either works. Prefixes with a 1-indexed table are the convention, because it lets row 0 and column 0 hold the base cases naturally.

**The base case, answering section 1's question: `dp[0][j] = dp[i][0] = 0`.** The LCS of anything with an empty string is 0 — there's nothing to have in common. Sizing the table `(m+1) × (n+1)` and filling with zeros gives you this for free, with no special-case branch anywhere. That's why the extra row and column exist.

**The 1-indexing offset.** Because row `i` represents the *first `i` characters*, the character it refers to is `text1[i - 1]`. That `-1` appears in every comparison and is the single most common source of bugs here. The payoff is base cases that need no code.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m = len(text1)
n = len(text2)
```
Dimensions. `m` is the number of rows (progress through `text1`), `n` the columns (progress through `text2`).
→ [string-basics](../syntax/string-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
dp = [[0] * (n + 1) for _ in range(m + 1)]
```
The table, `(m+1) × (n+1)`, all zeros. `dp[i][j]` = LCS length of `text1[:i]` and `text2[:j]`.

Two things packed in here:
- **The extra row and column** are the base cases. `dp[0][*]` and `dp[*][0]` mean "one string is empty," so the LCS is 0 — already correct from the zero-fill. No special branch needed anywhere in the loops.
- **The [list comprehension](../syntax/list-comprehension.md) is mandatory.** Writing `[[0] * (n+1)] * (m+1)` creates `m+1` references to the *same* row — mutating one mutates all of them, and the table silently produces nonsense. This is the classic Python aliasing trap for 2-D arrays.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md)

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
```
Fill the table row by row, both loops starting at **1** — row 0 and column 0 are already the base cases.

The order matters: `dp[i][j]` depends on `dp[i-1][j-1]`, `dp[i-1][j]`, and `dp[i][j-1]` — all **above or to the left**. Sweeping top-to-bottom, left-to-right guarantees each is final before it's read.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if text1[i - 1] == text2[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
```
**The match case.** The `-1`s convert from "first `i` characters" to "index of the i-th character" — the cost of the 1-indexed table.

When the two current characters are equal, pair them and add 1 to the LCS of everything before them — the **diagonal** neighbour, since both strings advance.

Note there's no `max` here and no alternative considered: pairing a match is always safe, so this branch commits outright.
→ [comparison-operators](../syntax/comparison-operators.md) · [nested-lists](../syntax/nested-lists.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
```
**The mismatch case.** The two characters differ, so they can't both end the LCS — at least one is unusable at this position. Since you can't tell which, try both:

- `dp[i - 1][j]` — **drop `text1`'s last character** (move up).
- `dp[i][j - 1]` — **drop `text2`'s last character** (move left).

Take the better. Nothing is added, because no new pairing was made.

You might wonder about a third option, `dp[i-1][j-1]` (drop both). It's never needed — it can't exceed either of the other two, since both already include it as a sub-case.
→ [min-max-key](../syntax/min-max-key.md) · [elif-else](../syntax/elif-else.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[m][n]
```
The bottom-right cell: the LCS of the full `text1` and the full `text2`.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        m = len(text1)
        n = len(text2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]
```
</details>

**Trace it** — `text1 = "abcde"`, `text2 = "ace"`

The finished table, with row 0 and column 0 as the zero base cases:

|  | – | **a** | **c** | **e** |
|---|---|---|---|---|
| **–** | 0 | 0 | 0 | 0 |
| **a** | 0 | **1** | 1 | 1 |
| **b** | 0 | 1 | 1 | 1 |
| **c** | 0 | 1 | **2** | 2 |
| **d** | 0 | 1 | 2 | 2 |
| **e** | 0 | 1 | 2 | **3** |

Answer: `dp[5][3]` = **3** ✅ — `"ace"`.

The three bolded cells are the matches, and they sit on a staircase running down-right. Each took its diagonal neighbour and added 1: `dp[1][1] = dp[0][0]+1 = 1`, `dp[3][2] = dp[2][1]+1 = 2`, `dp[5][3] = dp[4][2]+1 = 3`.

Everything else is a mismatch, inheriting the max of its up and left neighbours — which is why the values spread rightwards and downwards in plateaus. Row `b` is entirely inherited from row `a`: `b` matches nothing in `"ace"`, so it contributes nothing, and the row is copied down unchanged.

**And `text1 = "ab"`, `text2 = "ba"`:**

|  | – | **b** | **a** |
|---|---|---|---|
| **–** | 0 | 0 | 0 |
| **a** | 0 | 0 | **1** |
| **b** | 0 | **1** | 1 |

`dp[2][2]` = **1** ✅ — you can take `"a"` or `"b"`, but not both, because using both would require reversing their order. Notice how the two match cells sit on *opposite* diagonals and neither can build on the other; the final cell takes `max(1, 1) = 1` rather than summing them. That's the table correctly refusing to combine incompatible pairings.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

- The outer loop runs **m** times, the inner **n** times → **m × n cells**.
- Each cell does one character comparison and either an addition or a two-way `max` — all **O(1)**.
- m × n × O(1) = **O(m · n)**.

At the limits, 1000 × 1000 = **10⁶** cells. Fast enough, and clearly what the constraints were chosen for.

**Against the alternatives:** enumerating all of `text1`'s subsequences is **O(2^m · n)** — 2¹⁰⁰⁰ candidates. The DP works because the number of distinct *states* is only m × n, even though the number of subsequence pairs is astronomical. Same collapse as [Unique Paths](62-unique-paths.md): **exponentially many objects, polynomially many states.**

**Can you beat O(m·n)?** Not in general — LCS has a conditional lower bound: an O((mn)^(1−ε)) algorithm would refute the Strong Exponential Time Hypothesis. There are practical improvements (the Hunt–Szymanski algorithm is fast when few character pairs match, and bit-parallel methods give O(mn/w) with word size w), but no better worst-case bound is known. **"O(m·n) is essentially optimal"** is the right thing to say.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n), reducible to O(min(m, n))</summary>

**O(m · n) as written** — the full table is `(m+1) × (n+1)` integers, about 10⁶ at the limits.

**But it collapses to O(n).** Look at what `dp[i][j]` reads: `dp[i-1][j-1]`, `dp[i-1][j]`, and `dp[i][j-1]` — all in the **current row or the one immediately above**. Rows `i-2` and earlier are dead the moment row `i-1` is finished. So two rows suffice:

```python
prev = [0] * (n + 1)
for i in range(1, m + 1):
    curr = [0] * (n + 1)
    for j in range(1, n + 1):
        if text1[i - 1] == text2[j - 1]:
            curr[j] = prev[j - 1] + 1
        else:
            curr[j] = max(prev[j], curr[j - 1])
    prev = curr
return prev[n]
```

**O(n)** space, same time. And by running the loops over the shorter string, you get **O(min(m, n))**.

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(m·n)** | A cache entry per state, plus up to m+n stack frames |
| Full 2-D table | **O(m·n)** | Every cell retained |
| **Two rolling rows** | **O(n)** | Each cell reads only the current and previous rows |
| One row, in place | **O(n)** | Possible, but needs a temporary to save the diagonal before overwriting it |

Same principle as [Unique Paths](62-unique-paths.md) and the rolling variables of Unit 13: **keep exactly as much history as the recurrence reads.**

**Why write the full table anyway?** Because it's what lets you **reconstruct the actual subsequence** — walk backwards from `dp[m][n]`, moving diagonally on matches and toward the larger neighbour otherwise. The rolling-row version returns only the length. That's a genuine trade, not just laziness, and it's worth saying which you'd pick and why.

</details>

<details>
<summary><b>6 · Talk it through</b> — thinking, trade-offs & follow-ups</summary>

**Say this out loud:**

> "A subproblem here is 'how much of each string is left', and that's two independent positions — so the state is two-dimensional. I define `dp[i][j]` as the LCS of the first i characters of one string and the first j of the other. Looking at the last character of each prefix: if they match, I pair them off — that's always safe — and add 1 to the diagonal. If they don't match, they can't both end the LCS, so I drop one or the other and take the better of up and left. The table is (m+1) × (n+1) so row 0 and column 0 hold the base case that anything paired with an empty string has an LCS of 0 — that means no special-casing in the loops. O(m·n) time and space, though since each cell only reads the current and previous rows, I can drop it to O(n) with two rolling rows. I'd keep the full table if I needed to reconstruct the actual subsequence."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Return the actual subsequence, not the length." | Walk backwards from `dp[m][n]`: on a match, record the character and move diagonally; otherwise move toward whichever of up/left is larger. Reverse at the end. Needs the full table. |
| "Reduce the space." | Two rolling rows → O(n), or O(min(m,n)) by iterating over the shorter string. Each cell reads only the current and previous rows. |
| "Longest common *substring* instead?" | Different recurrence: `dp[i][j] = dp[i-1][j-1] + 1` on a match and **0** on a mismatch, and the answer is the max cell rather than the corner. Contiguity means a mismatch resets. |
| "Why is pairing a match always safe?" | If both prefixes end in the same character, any optimal LCS can be rewritten to end with that pairing without shortening it. So committing to it never loses. |
| "How does this relate to edit distance?" | [Edit Distance](72-edit-distance.md) is the same grid with `min` and three operations instead of `max` and two. For insert/delete only, edit distance = `m + n − 2·LCS`. |
| "How does it relate to LIS?" | LIS of an array equals the LCS of the array and its sorted, deduplicated copy. Correct, but O(n²) time and space — much worse than the [O(n log n) tails method](300-longest-increasing-subsequence.md). |
| "Can you beat O(m·n)?" | Not in the worst case under SETH. Hunt–Szymanski is faster when matches are sparse; bit-parallel methods give O(mn/w). No better worst-case bound is known. |
| "What if there are more than two strings?" | The state gains a dimension per string — O(n^k) for k strings. It becomes NP-hard when k is part of the input. |

**Traps:**
- **`[[0] * (n+1)] * (m+1)`** for the table. Every row is the same object; writing to one writes to all. Use the list comprehension.
- **Dropping the `-1` in `text1[i-1]`.** The table is 1-indexed against 0-indexed strings; forgetting the offset either compares the wrong characters or raises `IndexError` at the last row.
- Sizing the table `m × n` instead of `(m+1) × (n+1)` — no room for the base cases, and every access to `dp[i-1]` at `i = 0` wraps around to the last row in Python.
- Adding 1 in the mismatch branch. Nothing was paired, so nothing is added.
- Taking `max` in the match branch, or including `dp[i-1][j-1]` in the mismatch `max`. Neither is wrong exactly — the first is unnecessary, the second is redundant — but both suggest you don't know why the recurrence has the shape it does.
- Confusing this with longest common **substring**, where a mismatch resets to 0.

**This same move shows up in:** [Edit Distance](72-edit-distance.md) (the same two-string grid, minimizing operations instead of maximizing matches) · [Distinct Subsequences](115-distinct-subsequences.md) (the same grid, counting instead of maximizing) · [Interleaving String](97-interleaving-string.md) (a grid over two strings answering feasibility) · [Unique Paths](62-unique-paths.md) (a grid whose cells depend on up-and-left, collapsible to one row) · [Longest Increasing Subsequence](300-longest-increasing-subsequence.md) (reducible to this, though the direct method is far better).

</details>

---
