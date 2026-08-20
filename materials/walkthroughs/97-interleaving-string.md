# 97. Interleaving String

**Medium** · [LeetCode](https://leetcode.com/problems/interleaving-string/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given strings `s1`, `s2` and `s3`, return `true` if `s3` is an **interleaving** of `s1` and `s2`. An interleaving splits both strings into blocks and alternates them, **preserving the internal order of each string**.

```
s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"   →  true
        aa + dbbc + bc + a + c   (blocks alternating from s1 and s2)

s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"   →  false

s1 = "", s2 = "", s3 = ""                       →  true
```

**Constraints:** `0 <= s1.length, s2.length <= 100` · `0 <= s3.length <= 200` · lowercase English letters only.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return true/false" | **Feasibility.** The combining operator is `or` — one valid interleaving is enough |
| "preserving the internal order of each" | You never rearrange. Each string is consumed **left to right**, so your progress through it is a single number |
| interleaving two strings | The state is **how far into `s1`** and **how far into `s2`** — two independent positions. That's the 2-D shape, same as [Longest Common Subsequence](1143-longest-common-subsequence.md) |
| every character of `s3` comes from `s1` or `s2` | At each step there are at most **two** choices: take the next character from `s1`, or from `s2` |
| lengths up to 100 and 200 | m × n = 10⁴ cells — comfortable. C(200, 100) interleavings — astronomically not |

There's a length check hiding in plain sight: **if `len(s1) + len(s2) != len(s3)`, it's immediately false.** Every character of `s3` must come from exactly one of the two, so the totals have to match. Free rejection, and it also makes the main logic safe.

Now the crucial observation, and it's the one that makes the whole thing work. Suppose you've consumed `i` characters from `s1` and `j` from `s2`. How many characters of `s3` have you built?

**Exactly `i + j`.** Always. Every character you take from either string appends one to `s3`.

So the position in `s3` is **not a third dimension** — it's determined by the other two. The state is just `(i, j)`, and `s3[i + j]` is the character you're currently trying to match. That's why this is a 2-D problem rather than a 3-D one, and it's the single most important thing to notice.

From state `(i, j)`, trying to produce `s3[i+j]`:

- **Take from `s1`** — legal if `s1[i] == s3[i+j]`, then continue from `(i+1, j)`.
- **Take from `s2`** — legal if `s2[j] == s3[i+j]`, then continue from `(i, j+1)`.

Either working is enough.

🤔 **Before you open the next section:** greedy would say "whenever `s1[i]` matches, take it." Try that on `s1 = "a"`, `s2 = "ab"`, `s3 = "aab"` — and then think about what happens when *both* strings offer the same character.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy — take from `s1` whenever it matches | Prefer one string on a tie | O(m+n) | O(1) | ❌ **Wrong.** When both strings offer the same character, the choice matters and can't be decided locally |
| Sort/count characters | Check that `s1` and `s2` together have `s3`'s multiset | O(m+n) | O(1) | ❌ Necessary but nowhere near sufficient — it ignores order entirely. Example 2 has the right counts and is still false |
| Brute-force recursion | Try both choices at every step | **O(2^(m+n))** | O(m+n) | ❌ Exponential |
| Recursion + memo on `(i, j)` | Same, cached | O(m·n) | O(m·n) + stack | ⚠️ Correct; up to 200 stack frames |
| **Bottom-up 2-D table** | Fill an `(m+1) × (n+1)` grid of booleans | O(m·n) | **O(m·n)** | ✅ |
| One rolling row | Same recurrence, keeping one row | O(m·n) | **O(n)** | ✅ Strictly better space; mention it |

**The decision:** the **bottom-up 2-D boolean table**.

**Why greedy fails.** Take `s1 = "a"`, `s2 = "ab"`, `s3 = "aab"`. At the start both `s1[0]` and `s2[0]` are `'a'`, matching `s3[0]`. Greedily taking from `s1` exhausts it, and then `s2 = "ab"` must supply `"ab"` — which works, so this case survives. But flip it: `s1 = "ab"`, `s2 = "a"`, `s3 = "aab"`. Taking from `s1` first gives `'a'`, then you need `'a'` again and only `s2` has it, then `'b'` from `s1` — fine again. The genuine failures come from longer overlaps, like `s1 = "aa"`, `s2 = "ab"`, `s3 = "aaba"`: the first `'a'` can come from either, and only one choice completes. **When both strings offer the same character, the right choice depends on everything that follows** — which is exactly the DP signal, and the same reason greedy fails in [Word Break](139-word-break.md).

**Why the state is `(i, j)` and nothing more.** Because `i + j` pins down the position in `s3`, the state is exactly two numbers. If that weren't true you'd need `(i, j, k)` and the table would be 10⁶ cells instead of 10⁴. **Recognizing that a would-be third dimension is derivable is the insight**, and it's worth saying out loud — it's the difference between a clean solution and an over-engineered one.

**Why bottom-up over memoized recursion?** Same complexity, no stack. With `len(s3)` up to 200 the recursion is safe here, but the table makes the base case and fill order explicit, and it collapses to O(n) space in an obvious way.

**Why fill backwards?** This implementation defines `dp[i][j]` over **suffixes** — "can `s1[i:]` and `s2[j:]` interleave to form `s3[i+j:]`?" — so the base case sits at `dp[m][n]` (everything consumed, success) and the fill runs from the bottom-right corner outward. A forward/prefix formulation is equally valid; the suffix version puts the single `True` seed at a corner and needs no separate first-row initialization.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m = len(s1)
n = len(s2)
if m + n != len(s3):
    return False
```
**The length check, and it's doing real work.** Every character of `s3` must come from exactly one of the two strings, so if the totals don't match no interleaving can exist.

Beyond correctness this is a guard: the rest of the code indexes `s3[i + j]` assuming that position exists, and this line is what guarantees it.
→ [string-basics](../syntax/string-basics.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
dp = [[False] * (n + 1) for _ in range(m + 1)]
dp[m][n] = True
```
`dp[i][j]` = *"can `s1[i:]` and `s2[j:]` interleave to form `s3[i+j:]`?"* — the table is `(m+1) × (n+1)` so that `i = m` and `j = n` (both strings fully consumed) are representable.

**`dp[m][n] = True` is the seed:** two empty suffixes interleave to form an empty suffix. That's the "reaching the end is success" base case again — the same idea as `dp[n] = True` in [Word Break](139-word-break.md) and `ways("") = 1` in [Decode Ways](91-decode-ways.md). Set it `False` and every cell stays `False`.

The [list comprehension](../syntax/list-comprehension.md) is mandatory: `[[False] * (n+1)] * (m+1)` would create `m+1` references to one shared row, and every write would hit all of them.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
for i in range(m, -1, -1):
    for j in range(n, -1, -1):
```
Sweep **backwards** in both dimensions, from `(m, n)` down to `(0, 0)`.

Backwards because `dp[i][j]` depends on `dp[i+1][j]` and `dp[i][j+1]` — both at *larger* indices. The fill order has to make those final before they're read, the same constraint as [Word Break](139-word-break.md)'s reverse loop and [Unique Paths](62-unique-paths.md)'s right-to-left sweep.

Both ranges include their endpoint (`m` and `n`), which harmlessly recomputes `dp[m][n]` — neither `if` fires there, since `i < m` and `j < n` are both false, so the seeded `True` survives.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if i < m and s1[i] == s3[i + j] and dp[i + 1][j]:
            dp[i][j] = True
```
**Option one: take the next character from `s1`.** Three conditions, [short-circuiting](../syntax/logical-operators.md) left to right:

1. `i < m` — there *is* a character left in `s1`. This must come first; without it `s1[i]` raises `IndexError` at the boundary.
2. `s1[i] == s3[i + j]` — it's the character `s3` needs right now. **`i + j` is the derived position in `s3`** — the observation from section 1, appearing in code.
3. `dp[i + 1][j]` — and the rest works out after consuming it.

All three must hold for this route to be viable.
→ [logical-operators](../syntax/logical-operators.md) · [string-basics](../syntax/string-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
        if j < n and s2[j] == s3[i + j] and dp[i][j + 1]:
            dp[i][j] = True
```
**Option two: take from `s2` instead.** Exactly symmetric — bounds check, character match against the same `s3[i + j]`, and the remaining suffix must work.

Two separate `if`s rather than an `or` expresses the `or` semantics directly: either route succeeding sets the cell `True`, and the second `if` can't undo the first (it only ever assigns `True`). Writing `dp[i][j] = (cond1) or (cond2)` would be equivalent and arguably tidier; two statements keep each branch readable.
→ [logical-operators](../syntax/logical-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[0][0]
```
"Can the full `s1` and full `s2` interleave to form the full `s3`?"
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False

        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True

        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i < m and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                if j < n and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True

        return dp[0][0]
```
</details>

**Trace it** — `s1 = "ab"`, `s2 = "c"`, `s3 = "acb"` (m = 2, n = 1)

Length check: 2 + 1 = 3 ✓

Filling backwards, cell by cell in the order the loops visit them:

| cell | `s3[i+j]` | take from `s1` | take from `s2` | result |
|---|---|---|---|---|
| `dp[2][1]` | — | `i = m`, skip | `j = n`, skip | **T** (seed) |
| `dp[2][0]` | `s3[2] = 'b'` | `i = m`, skip | `s2[0]='c'` ≠ `'b'` ✗ | F |
| `dp[1][1]` | `s3[2] = 'b'` | `s1[1]='b'` ✓, `dp[2][1]`=T ✓ | `j = n`, skip | **T** |
| `dp[1][0]` | `s3[1] = 'c'` | `s1[1]='b'` ≠ `'c'` ✗ | `s2[0]='c'` ✓, `dp[1][1]`=T ✓ | **T** |
| `dp[0][1]` | `s3[1] = 'c'` | `s1[0]='a'` ≠ `'c'` ✗ | `j = n`, skip | F |
| `dp[0][0]` | `s3[0] = 'a'` | `s1[0]='a'` ✓, `dp[1][0]`=T ✓ | `s2[0]='c'` ≠ `'a'` ✗ | **T** |

As a grid:

| | **j = 0** (`"c"` left) | **j = 1** (nothing left) |
|---|---|---|
| **i = 0** (`"ab"` left) | **T** | F |
| **i = 1** (`"b"` left) | **T** | **T** |
| **i = 2** (nothing left) | F | **T** (seed) |

Return `dp[0][0]` = **true** ✅ — the interleaving is `a` (from `s1`) + `c` (from `s2`) + `b` (from `s1`).

Look at `dp[1][0]`: `s1` has `"b"` left, `s2` has `"c"`, and `s3` needs `'c'`. Only the `s2` route works, and it depends on `dp[1][1]` already being known — which is why the sweep runs backwards.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

- The two loops cover **(m+1) × (n+1) cells** ≈ m·n.
- Each cell does at most two bounds checks, two character comparisons, and two table lookups — all **O(1)**.
- **O(m · n)** total.

At the limits, 100 × 100 = **10⁴** cells. Instant.

**Against the alternatives:** brute-force recursion is **O(2^(m+n))**, because at each of the m+n steps you branch two ways. More precisely, the number of possible interleavings is `C(m+n, m)` — at m = n = 100 that's `C(200,100)` ≈ 10⁵⁹. The DP works because those 10⁵⁹ interleavings pass through only 10⁴ distinct `(i, j)` states: **many paths, few states**, the same collapse as [Unique Paths](62-unique-paths.md) and [Target Sum](494-target-sum.md).

**Faster?** No. Every character of all three strings can affect the answer, so **Ω(m + n)** is a floor, and no sub-quadratic algorithm is known for the general problem — it's closely related to [LCS](1143-longest-common-subsequence.md), which has a conditional quadratic lower bound.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n), reducible to O(n)</summary>

**O(m · n) as written** — the full boolean table, ~10⁴ entries at the limits.

**But it collapses to O(n).** `dp[i][j]` reads only `dp[i+1][j]` (the next row, same column) and `dp[i][j+1]` (the same row, next column). So one row plus the row after it is all you need:

```python
dp = [False] * (n + 1)
dp[n] = True
for i in range(m, -1, -1):
    for j in range(n, -1, -1):
        res = False
        if i < m and s1[i] == s3[i + j] and dp[j]:        # dp[j] still holds row i+1
            res = True
        if j < n and s2[j] == s3[i + j] and dp[j + 1]:    # dp[j+1] already row i
            res = True
        dp[j] = res
return dp[0]
```

**O(n)** space, and by swapping the strings so `s2` is the shorter one, **O(min(m, n))**.

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(m·n)** | A cache entry per state, plus up to m+n stack frames |
| Full 2-D table | **O(m·n)** | Every cell retained |
| **One rolling row** | **O(n)** | Each cell reads only the current and next rows |

Same principle as every space reduction in this unit and the last: **keep exactly as much history as the recurrence reads.** In Unit 13 that meant a couple of variables; here it means a couple of rows.

**Why write the full table anyway?** It's clearer, it's what you'd want if asked to *reconstruct* the interleaving (walk from `dp[0][0]` following whichever branch is `True`), and at 10⁴ cells there's nothing to save. Offer the reduction; don't lead with it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First, if the lengths don't add up it's immediately false. Then the key observation: if I've consumed i characters from s1 and j from s2, I've built exactly i+j characters of s3 — so the position in s3 is *derived*, not a third dimension. The state is just `(i, j)`. From there I'm trying to produce `s3[i+j]`, and I can take it from s1 if `s1[i]` matches, or from s2 if `s2[j]` matches; either working is enough, since this is a feasibility question. Greedy doesn't work, because when both strings offer the same character the right choice depends on the whole rest of the input. I fill the table backwards from `dp[m][n] = True` — two empty suffixes interleave into an empty string — since each cell depends on cells at larger indices. O(m·n) time and space, and since each cell only reads the current and next row, I can drop it to O(min(m,n)) with a rolling row."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't the position in `s3` a third dimension?" | Because it's always `i + j` — every character consumed from either string appends exactly one to `s3`. Tracking it separately would give a 10⁶-cell table instead of 10⁴, for no extra information. |
| "Why doesn't greedy work?" | When `s1[i]` and `s2[j]` are the same character, both are locally valid and only one may lead to a complete interleaving. The choice can't be made without looking ahead. |
| "Reduce the space." | One rolling row → O(n), or O(min(m,n)) by making the shorter string the inner dimension. Each cell reads only the current and next rows. |
| "Reconstruct the actual interleaving." | Walk forward from `dp[0][0]`, at each step taking whichever branch is `True` and recording which string it came from. Needs the full table. |
| "Would checking character counts work?" | It's necessary but not sufficient — example 2 has exactly the right multiset and is still false, because the *order* is wrong. |
| "What if there were three input strings?" | The state becomes `(i, j, k)` with the position in `s4` derived as `i+j+k`. O(m·n·p) — the pattern generalizes, the cost multiplies. |
| "Can you do it forwards?" | Yes — define `dp[i][j]` over prefixes with `dp[0][0] = True` and fill top-left to bottom-right. Equivalent; the suffix version just puts the seed in a corner. |
| "Empty strings?" | `s1 = s2 = s3 = ""` → the table is 1×1 holding the seed, and `dp[0][0]` is `True`. Handled with no special case. |

**Traps:**
- **Treating the `s3` index as independent state.** Wastes a dimension and usually introduces a bug in keeping it synchronized.
- **Bounds checks after the indexing.** `s1[i] == s3[i+j] and i < m` raises `IndexError` — and Python's negative indexing can make related mistakes silently wrong rather than loud.
- **Forgetting the `m + n != len(s3)` check.** Not just an optimization: without it `s3[i + j]` can index out of range.
- Seeding `dp[m][n] = False`, or forgetting to seed it. Everything stays `False`.
- Sweeping forwards while using a suffix recurrence — the dependencies wouldn't be computed yet.
- `[[False] * (n+1)] * (m+1)` for the table. Shared row references; every write hits all rows.

**This same move shows up in:** [Longest Common Subsequence](1143-longest-common-subsequence.md) (the same two-string grid, maximizing instead of testing feasibility) · [Edit Distance](72-edit-distance.md) (the same grid, minimizing operations) · [Distinct Subsequences](115-distinct-subsequences.md) (the same grid, counting) · [Word Break](139-word-break.md) (a feasibility DP over a string with an "empty remainder succeeds" base case) · [Unique Paths](62-unique-paths.md) (a grid collapsible to one rolling row).

</details>

---
