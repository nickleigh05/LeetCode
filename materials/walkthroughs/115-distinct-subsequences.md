# 115. Distinct Subsequences

**Hard** · [LeetCode](https://leetcode.com/problems/distinct-subsequences/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two strings `s` and `t`, return the **number of distinct subsequences of `s` that equal `t`**. A subsequence is formed by deleting some or no characters without changing the order of the rest.

```
s = "rabbbit", t = "rabbit"   →  3
        rabbbit   rabbbit   rabbbit
        ^^^^ ^^    ^^^ ^^^    ^^^^^^     — three ways to choose which 'b's to keep

s = "babgbag", t = "bag"      →  5
```

**Constraints:** `1 <= s.length, t.length <= 1000` · lowercase English letters only · the answer fits in a 32-bit signed integer.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**number of** distinct subsequences" | Counting, so the combining operator is `+`. Contrast [Longest Common Subsequence](1143-longest-common-subsequence.md), which maximizes over the same grid |
| "**subsequences** of `s`" | Non-contiguous — delete freely, preserve order. 2^m candidates in `s` |
| "**distinct**" — and yet `"rabbbit"` gives 3 | The word is misleading. The three answers are all the string `"rabbit"`; they're distinct as **choices of positions**, not as strings. You're counting **index sets**, not values — so no deduplication |
| two strings, progress in each | The state is `(how far into s, how far into t)` — two positions. The Unit 14 shape |
| both up to 1000 | m × n = 10⁶ cells. Fine. 2¹⁰⁰⁰ is not |

Look closely at `"rabbbit"` → `"rabbit"`. There are three `b`s in `s` and only two needed in `t`. The three answers correspond to which two of the three `b`s you keep. **That's the whole problem: counting position choices, not distinct outputs.**

Now the recurrence. Let `dp[i][j]` = the number of ways `s[i:]` can form `t[j:]`. Stand at `(i, j)` and consider `s[i]` — the character you're deciding about:

**Whatever else is true, you may always skip `s[i]`** and try to form `t[j:]` from `s[i+1:]`. Skipping a character of the source is always allowed.

**And if `s[i] == t[j]`, you may additionally *use* it** to match `t[j]`, then continue with `s[i+1:]` forming `t[j+1:]`.

```
dp[i][j] = dp[i+1][j]                        ← skip s[i]  (always available)
         + dp[i+1][j+1]   if s[i] == t[j]    ← use s[i]   (only on a match)
```

They're **added**, not chosen between, because these are different ways of building the answer and every one counts separately.

That asymmetry is the heart of it: a **mismatch leaves one option**, a **match leaves two**. Compare [Longest Common Subsequence](1143-longest-common-subsequence.md), where a match *commits* (there's never a reason not to pair matching characters when maximizing length). Here, declining a match is a genuinely different subsequence and must be counted.

🤔 **Before you open the next section:** what is `dp[i][n]` — the number of ways `s[i:]` can form the *empty* string? Careful: it's not 0. And what about `dp[m][j]` for `j < n`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate subsequences of `s` | Generate all 2^m, count those equal to `t` | **O(2^m · n)** | O(m) | ❌ 2¹⁰⁰⁰ |
| Greedy — match left to right | Walk both strings, pair up when possible | O(m+n) | O(1) | ❌ Finds *one* subsequence, not a count. There's nothing to be greedy about when counting |
| Recursion + memo on `(i, j)` | Cache each state | O(m·n) | O(m·n) + stack | ⚠️ Correct; up to m+n stack frames |
| **Bottom-up 2-D table** | Fill an `(m+1) × (n+1)` grid | O(m·n) | **O(m·n)** | ✅ |
| One rolling row | Same recurrence, one row kept | O(m·n) | **O(n)** | ✅ Strictly better space; mention it |

**The decision:** the **bottom-up 2-D table** over suffix positions.

**Why this is a counting problem and not a search.** Greedy, backtracking with pruning, two pointers — all the usual subsequence tools find *whether* or *where* a match exists. None of them count. The moment the question is "how many," you need to sum over branches, and DP is the tool that does that without enumerating.

**Why the state is `(i, j)`.** A subproblem is fully described by how much of `s` and how much of `t` remain. The path taken to get there — which earlier characters you skipped or used — is irrelevant to how many completions exist. That's the memoization precondition, and it's why 2^m subsequences collapse into m × n states.

**The base cases, answering section 1's question.** Two of them, and they're asymmetric:

- **`dp[i][n] = 1` for every `i`.** Once `t` is fully matched, there is exactly **one** way to finish: use nothing more from `s`. Not 0 — the empty target is satisfied by the empty selection, and that's a real, countable way. This is the seed the entire table is built from.
- **`dp[m][j] = 0` for `j < n`.** If `s` is exhausted but `t` isn't, there's no way to finish. This comes free from the zero-initialized table.

Getting the first one wrong is the single most common failure: seed it as 0 and every cell stays 0.

**Why fill backwards?** Because `dp[i][j]` reads `dp[i+1][j]` and `dp[i+1][j+1]` — both at larger indices. The sweep must make those final first. A forward/prefix formulation works identically with the base cases moved to row 0 and column 0.

**Why not [Longest Common Subsequence](1143-longest-common-subsequence.md)'s recurrence?** Because that one takes `max` over "drop from `s`" and "drop from `t`". Here you can never drop a character of `t` — every character of the target must be matched. **The target is fixed; only the source is optional.** That asymmetry is what makes this a different (and slightly harder) recurrence than LCS.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m = len(s)
n = len(t)
```
`m` rows for progress through the source, `n` columns for progress through the target.
→ [string-basics](../syntax/string-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
dp = [[0] * (n + 1) for _ in range(m + 1)]
```
`dp[i][j]` = the number of ways `s[i:]` can form `t[j:]`. The `+1`s make room for the "fully consumed" positions `i = m` and `j = n`.

Zero-initializing gives one base case for free: **`dp[m][j] = 0` for `j < n`** — with `s` exhausted and `t` unfinished, there are no ways.

The [list comprehension](../syntax/list-comprehension.md) is required. `[[0] * (n+1)] * (m+1)` would make `m+1` references to a single shared row, and every write would land in all of them.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
for i in range(m + 1):
    dp[i][n] = 1   # an empty t is always formed exactly one way
```
**The seed, and the whole table depends on it.**

Once `t` is fully matched (`j == n`), there is exactly **one** way to complete the job: take nothing further from `s`. That's true no matter how much of `s` is left — hence the entire last column is 1, including `dp[m][n]`.

The intuition worth holding onto: **the empty selection is a valid selection.** Same idea as `dp[0] = 1` in [Coin Change II](518-coin-change-ii.md) and `ways("") = 1` in [Decode Ways](91-decode-ways.md). Seed it 0 and every count in the table collapses to 0.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [nested-lists](../syntax/nested-lists.md)

```python
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
```
Sweep **backwards** in both dimensions. `dp[i][j]` depends on `dp[i+1][j]` and `dp[i+1][j+1]`, both at larger indices, so those must already be final.

The loops stop at `m-1` and `n-1` because row `m` and column `n` are base cases and must not be overwritten.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        dp[i][j] = dp[i + 1][j]
```
**The skip option, and it's unconditional.** You may always decline to use `s[i]` and try to form `t[j:]` from the rest of `s`. `j` doesn't advance, because nothing was matched.

Writing this as a plain assignment before the conditional is what makes the code short: the always-available branch is the starting value, and the match branch is added on top.
→ [nested-lists](../syntax/nested-lists.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
        if s[i] == t[j]:
            dp[i][j] += dp[i + 1][j + 1]
```
**The use option, available only on a match.** If `s[i]` is the character `t` needs, you may consume it — advancing **both** positions, hence the diagonal.

**`+=`, not `=`.** This is the line that makes the problem what it is. Using the character and skipping it are two *different* subsequences, both valid, and both must be counted. Overwriting instead of adding would count only one of them and silently return a far smaller number.

That's the `"rabbbit"` example in code: at each of the three `b`s you can either use it or skip it, and the additions accumulate the three valid combinations.
→ [comparison-operators](../syntax/comparison-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[0][0]
```
The number of ways all of `s` can form all of `t`.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:

        m = len(s)
        n = len(t)

        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][n] = 1   # an empty t is always formed exactly one way

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                dp[i][j] = dp[i + 1][j]
                if s[i] == t[j]:
                    dp[i][j] += dp[i + 1][j + 1]

        return dp[0][0]
```
</details>

**Trace it** — `s = "babgbag"`, `t = "bag"` (answer should be 5)

The finished table. Rows are positions in `s` (what's left of it), columns positions in `t`:

|  | **j=0** `"bag"` | **j=1** `"ag"` | **j=2** `"g"` | **j=3** `""` |
|---|---|---|---|---|
| **i=0** `"babgbag"` | **5** | 5 | 3 | 1 |
| **i=1** `"abgbag"` | 2 | 5 | 3 | 1 |
| **i=2** `"bgbag"` | 2 | 2 | 3 | 1 |
| **i=3** `"gbag"` | 1 | 2 | 3 | 1 |
| **i=4** `"bag"` | 1 | 1 | 1 | 1 |
| **i=5** `"ag"` | 0 | 1 | 1 | 1 |
| **i=6** `"g"` | 0 | 0 | 1 | 1 |
| **i=7** `""` | 0 | 0 | 0 | 1 |

Answer: `dp[0][0]` = **5** ✅

Three cells worth reading closely:

**`dp[7][3] = 1`** — both strings exhausted. The seeded base case, and everything traces back to it.

**`dp[4][0]`**: `s[4:] = "bag"`, `t[0:] = "bag"`, and `s[4] = 'b'` matches `t[0] = 'b'`. So it's `dp[5][0]` (skip the `b`) + `dp[5][1]` (use it) = 0 + 1 = **1**. The skip branch is 0 because `"ag"` can't produce `"bag"`.

**`dp[0][0]`**: `s[0] = 'b'` matches `t[0] = 'b'`, so it's `dp[1][0]` (skip) + `dp[1][1]` (use) = 2 + 5 = **5**. Both branches contribute, and that summing is exactly what `+=` is for — replacing it with `=` would give 5 here but wrong answers elsewhere, since the skip contribution would vanish.

The five subsequences, for concreteness:

```
babgbag      babgbag      babgbag      babgbag      babgbag
^^    ^        ^ ^  ^      ^   ^^        ^  ^ ^       ^^^
b a   g        b a  g      b   ag        b  a g       bag
```

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n).**

- The seeding loop is O(m).
- The two nested loops cover **m × n cells**.
- Each cell does one array read, one comparison, and at most one addition — **O(1)**.
- **O(m · n)** total.

At the limits, 1000 × 1000 = **10⁶** cells. Comfortable.

**Against the alternatives:** enumerating all subsequences of `s` is **O(2^m · n)** — 2¹⁰⁰⁰ candidates. The DP works because those exponentially many subsequences pass through only m × n distinct `(i, j)` states. **Many objects, few states** — the same collapse as [Longest Common Subsequence](1143-longest-common-subsequence.md), [Unique Paths](62-unique-paths.md), and [Target Sum](494-target-sum.md).

**A pruning observation worth mentioning:** `dp[i][j]` is necessarily 0 whenever `m - i < n - j` — fewer characters remain in `s` than are still needed from `t`. You can skip those cells entirely, which prunes roughly the lower-left triangle. Same asymptotic bound, real constant-factor saving.

**Faster?** No. Every character of both strings can affect the count, so **Ω(m + n)** is a floor, and no sub-quadratic algorithm is known — this is in the same family as LCS, which has a conditional quadratic lower bound under SETH.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n), reducible to O(n)</summary>

**O(m · n) as written** — the full table, 10⁶ integers at the limits.

**But it collapses to O(n).** `dp[i][j]` reads only `dp[i+1][j]` and `dp[i+1][j+1]` — both in the **next row**. So one row of size `n+1` suffices:

```python
dp = [0] * (n + 1)
dp[n] = 1
for i in range(m - 1, -1, -1):
    for j in range(n):           # left to right is safe here
        if s[i] == t[j]:
            dp[j] += dp[j + 1]
return dp[0]
```

**O(n)** space, same time. Note the sweep direction changes: reading `dp[j+1]` means the *next* column must still hold the previous row's value, so `j` must move **left to right**. (The array version's `dp[j]` before the update already carries the "skip" term, which is why the standalone assignment disappears.)

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(m·n)** | One entry per state, plus up to m+n stack frames |
| Full 2-D table | **O(m·n)** | Every cell retained |
| **One rolling row** | **O(n)** | Each cell reads only the next row |

Same principle as everywhere in this unit: **keep exactly as much history as the recurrence reads.**

**A note on integer size:** the counts can be astronomically large — a string of 1000 `a`s against a target of 500 `a`s gives `C(1000, 500)`, a 300-digit number. Python handles it natively; in Java or C++ you'd overflow, which is why the problem explicitly guarantees the answer fits in 32 bits. **Intermediate cells can still exceed that**, which is a subtle trap in typed languages and worth flagging.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This counts *position choices*, not distinct strings — `"rabbbit"` gives 3 because there are three ways to pick which two of the three b's to keep. So the state is how far I am into each string, `(i, j)`, and at each cell I'm deciding about `s[i]`. I can always skip it and keep trying to build `t[j:]` from the rest. And if `s[i] == t[j]`, I can *additionally* use it, advancing both positions. Those are added, not chosen between, because using and skipping produce genuinely different subsequences. The critical base case is that an empty target is formed exactly one way — by taking nothing — so the whole last column is 1; seed it 0 and everything collapses to 0. I fill backwards since each cell depends on larger indices. O(m·n) time and space, reducible to O(n) with a rolling row."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is `dp[i][n] = 1` and not 0?" | Once `t` is fully matched there's exactly one way to finish — use nothing more from `s`. The empty selection is a real selection. It's the seed everything else is built from. |
| "Why `+=` rather than `=` on a match?" | Using the character and skipping it are two different subsequences, both valid. Overwriting counts only one and undercounts badly. |
| "How is this different from LCS?" | LCS takes `max` and may drop characters from *either* string. Here the target is fixed — you can never drop a character of `t` — and you sum instead of maximizing. |
| "Why can a match still be skipped?" | Because a different, later occurrence of the same character might be used instead. `"babgbag"` → `"bag"` relies on exactly that. |
| "Reduce the space." | One rolling row → O(n). The sweep over `j` must go left to right so `dp[j+1]` still holds the previous row's value. |
| "What about overflow?" | The answer fits in 32 bits by problem guarantee, but intermediate cells can exceed it in typed languages. Python's arbitrary-precision ints make it a non-issue. |
| "Can you prune?" | Yes — `dp[i][j]` is 0 whenever fewer characters remain in `s` than are needed from `t` (`m - i < n - j`). Skips roughly a triangle of the table. |
| "Return the actual subsequences?" | Backtracking, not DP — the output can be exponentially large, as the `C(1000,500)` case shows. |

**Traps:**
- **Seeding the last column as 0**, or forgetting it entirely. Every answer becomes 0. The defining failure.
- **Using `=` instead of `+=`** in the match branch — drops the skip contribution.
- Trying to also skip characters of `t`. The target must be matched in full; only the source is optional.
- Taking `max` instead of summing, out of habit from LCS.
- Sizing the table `m × n` instead of `(m+1) × (n+1)` — no room for the base cases.
- `[[0] * (n+1)] * (m+1)` for the table. Shared row references.
- Sweeping forwards while using a suffix recurrence.

**This same move shows up in:** [Longest Common Subsequence](1143-longest-common-subsequence.md) (the same two-string grid, maximizing — the contrast that makes the summing here meaningful) · [Interleaving String](97-interleaving-string.md) (the same grid, testing feasibility) · [Edit Distance](72-edit-distance.md) (the same grid, minimizing) · [Coin Change II](518-coin-change-ii.md) (a counting DP whose base case is "the empty choice counts once") · [Target Sum](494-target-sum.md) (counting over a two-part state).

</details>

---
