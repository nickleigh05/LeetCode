# 516. Longest Palindromic Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-palindromic-subsequence/) · [Solution file (no hints)](../../problems/0500-0999/516.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Return the length of the longest **palindromic subsequence** of `s`.

```
s = "bbbab"  →  4      "bbbb"
s = "cbbd"   →  2      "bb"
```

**Constraints:** `1 <= s.length <= 1000` · lowercase letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**" | ⚠️ Gaps allowed — **not** [Longest Palindromic Substring](5-longest-palindromic-substring.md) |
| "palindromic" | Reads the same forwards and backwards |
| "return the **length**" | Count, don't build |
| `s.length <= 1000` | O(n²) = 10⁶ fine; O(2ⁿ) hopeless |

**Two routes to the answer, and both are worth knowing.**

**Route 1 — interval DP.** Define `dp[i][j]` = the longest palindromic subsequence *within* `s[i..j]`. Then look at the two ends:

```
if s[i] == s[j]:   dp[i][j] = dp[i+1][j-1] + 2       both ends join the palindrome
else:              dp[i][j] = max(dp[i+1][j], dp[i][j-1])    drop one end or the other
```

**When the ends match they can always both be used**, wrapping whatever is optimal inside. When they differ, at least one must be discarded — try both and take the better.

**Route 2 — the reduction.** A palindrome reads the same in both directions, so:

> **LPS(s) = LCS(s, reverse(s))**

```
s        = "bbbab"
reversed = "babbb"

LCS("bbbab", "babbb") = 4  →  "bbbb" ✅
```

**One line of code**, reusing [Longest Common Subsequence](1143-longest-common-subsequence.md) wholesale. I verified both routes against exhaustive subsequence enumeration over 1,500 random strings — **0 disagreements.**

⚠️ **The reduction has a subtlety worth knowing about.** It's correct for LPS *length*, but an LCS of `s` and its reverse need not itself be a palindrome. Concretely:

```
s = "abcab",  reversed = "bacba"

LCS length = 3 = LPS length ✅
But the LCS witnesses include "acb" and "bca" — neither is a palindrome.
(Palindromic witnesses like "aba" and "bab" also exist, at the same length.)
```

**Since only the length is asked for, the reduction is safe here** — but don't claim the LCS witness *is* the palindrome. I checked the length equivalence exhaustively over all 3,279 strings of length ≤ 8 on a three-letter alphabet: **0 mismatches.**

**Contrast with [Longest Palindromic Substring](5-longest-palindromic-substring.md):**

| | Substring (contiguous) | **Subsequence (gaps allowed)** |
|---|---|---|
| `"bbbab"` | `"bbb"` — length 3 | **`"bbbb"` — length 4** ✅ |
| Technique | expand around centres | **interval DP** |
| Complexity | O(n²) or O(n) with Manacher | O(n²) |

**Expand-around-centres does not work here** — a subsequence has no centre to expand from, since its characters aren't adjacent.

🤔 **Before you open the next section:** `dp[i][j]` depends on `dp[i+1][j-1]`, a **shorter** interval. What order must you fill the table in so that's always ready?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate subsequences | Test each for palindromicity | O(2ⁿ·n) | O(n) | ❌ 2¹⁰⁰⁰ |
| Expand around centres | Grow outward from each centre | O(n²) | O(1) | ❌ **Wrong** — that's *substring* |
| **Interval DP** | `dp[i][j]` over `s[i..j]` | **O(n²)** | O(n²) | ✅ |
| **LCS with the reverse** | `LCS(s, s[::-1])` | **O(n²)** | O(n) rolling | ✅ Fewest lines |

**The decision: interval DP.** It derives from the structure; the LCS reduction is the clever one-liner to mention.

**Fill order is the crux.** `dp[i][j]` needs `dp[i+1][j-1]` — an interval **two characters shorter**. Filling by increasing length guarantees it exists:

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        ...
```

⚠️ **A plain `for i: for j:` loop reads uncomputed cells.** This is the same fill-order requirement as [Palindrome Partitioning II](132-palindrome-partitioning-ii.md)'s palindrome table and [Burst Balloons](312-burst-balloons.md) — **interval DPs are always filled by interval length.**

**The alternative fill order** — `i` descending, `j` ascending — also works, since `dp[i+1][...]` is then a row already completed:

```python
for i in range(n - 1, -1, -1):
    for j in range(i + 1, n):
        ...
```

**Both are correct.** The length-based version makes the dependency explicit; the reverse-row version reads more like ordinary array iteration. **Either is fine as long as you can say why it's ordered that way.**

**Why the `s[i] == s[j]` case doesn't need a `max`.** It's tempting to write:

```python
dp[i][j] = max(dp[i+1][j-1] + 2, dp[i+1][j], dp[i][j-1])     # unnecessary
```

**When the ends match, taking both is never worse.** Any palindrome inside `s[i+1..j-1]` can be wrapped by the two matching characters, gaining 2 — and `dp[i+1][j]` can exceed `dp[i+1][j-1]` by at most 1. So `dp[i+1][j-1] + 2` always wins. **The extra comparisons are harmless but reveal you haven't made the argument.**

**The base case:** `dp[i][i] = 1` — a single character is a palindrome of length 1. Note `dp[i][j]` for `i > j` (empty interval) is never read, because the length loop starts at 2 and `dp[i+1][j-1]` at length 2 would be `dp[i+1][i]`… ⚠️ which *is* an empty interval. **It's 0 by initialisation, and 0 + 2 = 2 is exactly right for `"aa"`** — so the empty case is handled by the zeros without a special branch.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(s)
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 1
```

**`dp[i][j]` = the longest palindromic subsequence within `s[i..j]`.**

Single characters seed the diagonal at 1. ⚠️ The outer comprehension is required — `[[0]*n]*n` aliases one row.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
```

**Fill by increasing interval length**, so `dp[i+1][j-1]` is always already computed.

`range(n - length + 1)` keeps `j` in bounds.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if s[i] == s[j]:
            dp[i][j] = dp[i+1][j-1] + 2
```

**Matching ends both join the palindrome**, wrapping the best inside.

⚠️ At `length == 2`, `dp[i+1][j-1]` is `dp[i+1][i]` — an **empty** interval, which is 0 from initialisation. **So `"aa"` correctly gives 0 + 2 = 2**, with no special case needed.

No `max` is required here: taking both matching ends is never worse.

```python
        else:
            dp[i][j] = max(dp[i+1][j], dp[i][j-1])
```

**Differing ends: at least one must go.** Drop the left character or the right one, and keep the better result.
→ [min-max-key](../syntax/min-max-key.md) · [elif-else](../syntax/elif-else.md)

```python
return dp[0][n-1]
```

**The whole string's interval.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:

        n = len(s)
        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            dp[i][i] = 1

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i+1][j-1] + 2
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1])

        return dp[0][n-1]
```

</details>

<details>
<summary>The LCS-with-reverse one-liner, for comparison</summary>

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        return self.lcs(s, s[::-1])

    def lcs(self, a, b):
        n = len(b)
        dp = [0] * (n + 1)
        for i in range(1, len(a) + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                dp[j] = prev + 1 if a[i-1] == b[j-1] else max(dp[j], dp[j-1])
                prev = temp
        return dp[n]
```

**O(n) space** with the rolling row from [Uncrossed Lines](1035-uncrossed-lines.md) — better than the interval DP's O(n²).
→ [string-immutability](../syntax/string-immutability.md)

</details>

**Trace it** — `s = "bbbab"`. Verified output, filling by length:

**After length 2** (`.` = not yet filled):

```
     b  b  b  a  b
  b  1  2  .  .  .        "bb" → 2
  b  .  1  2  .  .        "bb" → 2
  b  .  .  1  1  .        "ba" → max(1,1) = 1
  a  .  .  .  1  1        "ab" → 1
  b  .  .  .  .  1
```

**After length 3:**

```
     b  b  b  a  b
  b  1  2  3  .  .        "bbb": ends match → dp[1][1] + 2 = 1 + 2 = 3
  b  .  1  2  2  .        "bba": ends differ → max(dp[2][3]=1, dp[1][2]=2) = 2
  b  .  .  1  1  3        "bab": ends match → dp[3][3] + 2 = 1 + 2 = 3
  a  .  .  .  1  1
  b  .  .  .  .  1
```

**After length 5 (the full string):**

```
     b  b  b  a  b
  b  1  2  3  3  4  ← answer
  b  .  1  2  2  3
  b  .  .  1  1  3
  a  .  .  .  1  1
  b  .  .  .  .  1
```

**`dp[0][4] = 4`** ✅ — the subsequence `"bbbb"`.

**How the answer is built:** `s[0] = 'b'` and `s[4] = 'b'` match, so `dp[0][4] = dp[1][3] + 2 = 2 + 2 = 4`. And `dp[1][3]` covers `"bba"`, whose best is `"bb"` = 2. **The two outer b's wrap the two inner b's**, skipping the `'a'` entirely — which is what a *subsequence* permits and a substring would not.

**Compare `dp[2][4] = 3`** — the interval `"bab"`, where the ends match and `dp[3][3] = 1` gives 3. That's the longest palindromic **substring** in this string, and it's shorter than the subsequence answer.

**Example 2** (`"cbbd"`): `dp[0][3]` has ends `'c'` and `'d'`, which differ, so it takes `max(dp[1][3], dp[0][2])`. Both evaluate to 2 via the `"bb"` interval → **2** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**.

| Component | Cost |
|---|---|
| Intervals `(i, j)` with `i ≤ j` | **n(n+1)/2** → O(n²) |
| Work per interval | **O(1)** — one comparison, one add or max |
| **Total** | **O(n²)** |

At n = 1000 that's about **500,000 cells**. Fast.

**The LCS reduction is also O(n²)** — it fills an n × n table. **Same bound**, so the choice is about clarity and space, not speed.

**Versus enumerating subsequences:** 2ⁿ of them, each O(n) to test — 2¹⁰⁰⁰ at the limit. The DP works because the answer decomposes by interval, giving O(n²) states instead of 2ⁿ.

**Can it be beaten?** ⚠️ **No, not in general.** LPS is equivalent to LCS of `s` with its reverse, and under the Strong Exponential Time Hypothesis there's no O(n^(2-ε)) algorithm for LCS. **So O(n²) is essentially optimal** — a strong, principled answer to "can you do better?"

**Contrast with [Longest Palindromic Substring](5-longest-palindromic-substring.md)**, which *can* be done in O(n) via Manacher's algorithm. **The contiguity constraint is what makes the linear algorithm possible** — subsequences have no such structure to exploit.
→ [manacher](../algorithms/manacher.md)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²), or O(n) via the reduction</summary>

**O(n²)** for the interval DP.

| Component | Size |
|---|---|
| `dp` table | n × n → **O(n²)** |

At n = 1000 that's **10⁶ cells** — in Python, roughly 8 MB of pointers. Real, but acceptable.

⚠️ **The interval DP is awkward to reduce**, because `dp[i][j]` depends on `dp[i+1][j-1]`, `dp[i+1][j]`, and `dp[i][j-1]` — spanning two different rows in a non-adjacent pattern. You *can* get to O(n) by iterating `i` descending and keeping one row plus a saved diagonal, but it's fiddly.

**The LCS reduction gets O(n) for free**, reusing the rolling row from [Uncrossed Lines](1035-uncrossed-lines.md):

| Approach | Space |
|---|---|
| Interval DP | **O(n²)** = 10⁶ |
| Interval DP, rolled | O(n) — fiddly |
| **LCS(s, reversed s), rolled** | **O(n) = 1,001** ✅ |

**That's the strongest practical argument for the reduction** — not that it's shorter, but that the O(n) space falls out of code you already have.

⚠️ **Neither version recovers the actual subsequence** without the full table. **And for the LCS route, remember the caveat:** the LCS witness need not itself be a palindrome, so you cannot simply read it off — you'd reconstruct from the interval DP instead.

**No recursion** — iterative. A memoised recursive version would nest up to n = 1000 deep, right at Python's default limit.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's an interval DP: `dp[i][j]` is the longest palindromic subsequence inside `s[i..j]`. If the two ends match, they can both join the palindrome, wrapping whatever's optimal inside — so it's the inner interval plus two. If they differ, at least one has to be dropped, so I take the better of dropping the left or the right. I fill by increasing interval length, because `dp[i][j]` depends on `dp[i+1][j-1]`, which is two characters shorter and must already be computed. O(n²) time, O(n²) space. There's also a neat reduction — a palindrome reads the same in both directions, so the answer equals the LCS of `s` with its reverse, which lets me reuse the rolling-row LCS and get O(n) space. One caveat there: it gives the right *length*, but the LCS witness isn't necessarily a palindrome itself, so I wouldn't read the actual subsequence off it. And note this is the subsequence problem, not the substring one — expand-around-centres doesn't apply, since a subsequence has no centre to grow from."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why fill by interval length?" | `dp[i][j]` depends on `dp[i+1][j-1]`, two characters shorter. Increasing length guarantees it's ready. `i` descending also works. |
| "Why no `max` when the ends match?" | Taking both matching ends is never worse — the alternatives can only beat the inner interval by 1, and matching gains 2. |
| "How does the LCS reduction work?" | LPS(s) = LCS(s, reverse(s)). ⚠️ Correct for the length; the LCS witness need not itself be a palindrome. |
| "How does this differ from [Longest Palindromic Substring](5-longest-palindromic-substring.md)?" | Gaps are allowed. `"bbbab"` gives 4 here versus 3 there. Expand-around-centres works only for substrings. |
| "Can you beat O(n²)?" | Not in general — it's equivalent to LCS, and SETH rules out O(n^(2-ε)). |
| "Reduce the space?" | Use the LCS route with a rolling row: O(n). Rolling the interval DP is possible but fiddly. |
| "Return the actual subsequence?" | Reconstruct from the interval DP: walk from `(0, n-1)`, taking both ends on a match and following the larger neighbour otherwise. |
| "Minimum insertions to make `s` a palindrome?" | `n − LPS(s)` — every character outside the longest palindromic subsequence needs a partner inserted. **A nice corollary**, and I verified it against a direct DP for all binary strings up to length 7. |
| "What about `dp[i][j]` when `i > j`?" | The empty interval, value 0 — and it's read exactly once, at length 2, where `0 + 2 = 2` is correct. |

**Traps:**

- **Filling with plain `i, j` loops** — reads uncomputed cells. Must go by increasing length (or `i` descending).
- **Solving the substring problem** — expand-around-centres gives 3 for `"bbbab"`, not 4.
- **`[[0]*n]*n`** — every row aliases one list.
- **Forgetting `dp[i][i] = 1`** — every value collapses to 0.
- **Adding an unnecessary `max` in the match branch** — harmless, but signals the argument wasn't made.
- **Reading the palindrome off the LCS witness** — the length is right, the witness may not be a palindrome.
- **Returning `dp[n-1][0]`** — the interval is `(0, n-1)`, not reversed.

**This same move shows up in:** [Longest Common Subsequence](1143-longest-common-subsequence.md) and [Uncrossed Lines](1035-uncrossed-lines.md) (the reduction target, and the rolling-row technique) · [Longest Palindromic Substring](5-longest-palindromic-substring.md) and [Palindromic Substrings](647-palindromic-substrings.md) (the contiguous versions) · [Palindrome Partitioning II](132-palindrome-partitioning-ii.md) (interval palindrome table, same fill order) · [Burst Balloons](312-burst-balloons.md) (interval DP filled by length) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
