# 5. Longest Palindromic Substring

**Medium** · [LeetCode](https://leetcode.com/problems/longest-palindromic-substring/)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string `s`, return the **longest palindromic substring** in `s`. A substring is a *contiguous* run of characters, and a palindrome reads the same forwards and backwards.

```
s = "babad"   →  "bab"    ("aba" is also valid — either is accepted)
s = "cbbd"    →  "bb"
s = "a"       →  "a"
```

**Constraints:** `1 <= s.length <= 1000` · `s` contains only digits and English letters.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**substring**", not subsequence | **Contiguous.** That's a huge restriction and it's good news — there are only O(n²) substrings, not 2ⁿ subsequences |
| "**longest**" | Optimization. You'll examine candidates and keep a running best |
| "palindrome" | Symmetry around a center. That word should immediately make you think *two pointers moving outward*, not *compare the string to its reverse* |
| `"babad"` accepts either answer | Ties don't matter, so no tie-breaking logic is needed |
| `n <= 1000` | n² = 10⁶ — **fine**. n³ = 10⁹ — **not fine**. That gap is the whole difficulty budget: you must avoid the brute force but needn't reach O(n) |

Now the structural insight. There are O(n²) substrings, and checking each for palindromicity costs O(n) — that's the O(n³) you can't afford. So the question becomes: **how do you check many substrings without paying the check?**

The answer comes from what a palindrome *is*. It's not an arbitrary string that happens to have a property — it's a structure **built outward from a center**. `"racecar"` is `"c"` wrapped in `"e…e"`, wrapped in `"c…c"`, wrapped in `"a…a"`, wrapped in `"r…r"`. Every palindrome has exactly one center, and every palindrome contains a smaller palindrome at its heart.

So instead of picking substrings and testing them, **pick centers and grow them.** From a given center, expanding outward is O(1) per character — one comparison tells you whether the palindrome extends. You get every palindrome around that center for the price of the longest one.

The one wrinkle: `"aba"` has a center *on* a character, while `"abba"` has a center *between* two characters. Odd and even lengths need separate treatment.

🤔 **Before you open the next section:** how many centers are there in a string of length n? Count the character positions and the gaps between them — and once you have that number, what's the total cost of expanding from all of them?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Check every substring | All O(n²) substrings, each verified in O(n) | **O(n³)** | O(1) | ❌ 10⁹ at n = 1000 |
| Longest common substring with `reverse(s)` | Reverse the string and find the longest shared substring | O(n²) | O(n²) | ❌ **Subtly wrong** — it can match a substring against a *different* palindromic region elsewhere. Needs an index check to repair |
| 2-D DP table | `dp[i][j]` = "is `s[i..j]` a palindrome?", built from `dp[i+1][j-1]` | O(n²) | **O(n²)** | ⚠️ Correct, and the "textbook DP" answer — but 10⁶ booleans for information you consume immediately |
| **Expand around center** | For each of the 2n−1 centers, grow outward while characters match | O(n²) | **O(1)** | ✅ |
| [Manacher's algorithm](../algorithms/manacher.md) | Reuse previously computed palindrome radii to skip redundant comparisons | **O(n)** | O(n) | ⚠️ Optimal, but long and error-prone. Name it; don't write it |

**The decision:** **expand around center** — same O(n²) time as the DP table, but O(1) space and about ten lines.

**How many centers are there?** `n` centers on a character (odd-length palindromes) plus `n−1` centers in the gaps between characters (even-length) = **2n − 1**. Each expansion costs at most O(n). So the total is O(n²), and you never allocate a table.

**Why this beats the 2-D DP.** The DP fills `dp[i][j]` from `dp[i+1][j-1]` — "`s[i..j]` is a palindrome if its ends match and its interior is one." That's a correct recurrence and it's genuinely the same insight, but it **stores** every subproblem when the answer only needs a running maximum. Center expansion is the same recurrence evaluated in the order that makes storage unnecessary: growing outward from a center *is* walking the `dp[i+1][j-1] → dp[i][j]` chain. **Same idea, no table.**

**Why the reverse-and-match idea is a trap.** "A palindrome reads the same backwards, so find the longest common substring of `s` and `s[::-1]`" sounds airtight, and it fails on inputs like `"abacdfgdcaba"`: the reversed string shares `"abacd"`, which isn't a palindrome — it matched a *different* copy of those characters. You can repair it by verifying the indices correspond, but at that point you've added complexity and O(n²) space for nothing.

**Why not Manacher's?** It's the theoretically right answer at **O(n)** and it exists for exactly this problem. But it's a substantial piece of code with a slick invariant that's easy to get wrong from memory, and at n ≤ 1000, O(n²) is well within budget. The strong move is to write center expansion and say *"Manacher's gets this to O(n) by reusing the radii it's already computed, if the input were much larger."*

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def expand(left, right):
```
One helper, used for both odd and even cases. That's the design decision that keeps this short — rather than two loops, you parameterize the **starting** center and let the same code handle both.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
```
**Two pointers moving outward** — the opposite of the usual converging pattern from [Valid Palindrome](125-valid-palindrome.md).

Three conditions, and all three are needed: stay in bounds on the left, stay in bounds on the right, and the characters must match. Python's [`and`](../syntax/logical-operators.md) short-circuits left to right, so the bounds checks must come **before** the indexing — swap the order and you'll get an `IndexError` at the ends of the string.

The loop exits when the palindrome can't grow further, which means `left` and `right` have each stepped **one past** the valid range.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [string-basics](../syntax/string-basics.md)

```python
    return s[left + 1:right]
```
The **off-by-one that has to be right.** After the loop, `left` is one too far left and `right` is one too far right. So the palindrome is `s[left+1 .. right-1]` inclusive — and since Python slices exclude their end, that's written `s[left + 1:right]`.

The asymmetry (`+1` on one side, nothing on the other) is not a bug: it's `+1` to undo the overshoot, and the missing `-1` is absorbed by the exclusive slice bound.
→ [list-slicing](../syntax/list-slicing.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
best = ""
```
The running answer. Starting empty means the first real palindrome always wins, and it's also the correct result for an empty input.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(len(s)):
```
Sweep every position as a center. One loop covers all 2n−1 centers, because each iteration handles two of them.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    odd = expand(i, i)
    even = expand(i, i + 1)
```
**Both center types, from the same index.**

- `expand(i, i)` — both pointers on the same character. That character is trivially a palindrome, so the expansion grows an **odd**-length one: `"aba"`, `"racecar"`.
- `expand(i, i + 1)` — pointers on adjacent characters. If `s[i] != s[i+1]` the loop body never runs and it returns `""`, costing nothing. If they match, it grows an **even**-length palindrome: `"bb"`, `"abba"`.

Missing the even case is the most common way to fail this problem — it returns `"b"` for `"cbbd"` instead of `"bb"`. And `expand(i, i+1)` needs no bounds guard: when `i` is the last index, `right < len(s)` is false immediately and it returns `""`.
→ [function-basics](../syntax/function-basics.md)

```python
    best = max(best, odd, even, key=len)
```
Keep the longest of the three. [`max` with `key=len`](../syntax/min-max-key.md) compares by **length** rather than alphabetically — without the key you'd get the lexicographically largest string, which is a silent and confusing wrong answer.

`max` returns the **first** maximum on a tie, so `best` only changes on a strict improvement. That's why `"babad"` yields `"bab"` rather than `"aba"` — and the problem accepts either.
→ [min-max-key](../syntax/min-max-key.md) · [sorting-key](../syntax/sorting-key.md)

```python
return best
```
Every center has been tried, so the longest palindrome found is the longest that exists.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:

        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right]

        best = ""
        for i in range(len(s)):
            odd = expand(i, i)
            even = expand(i, i + 1)
            best = max(best, odd, even, key=len)

        return best
```
</details>

**Trace it** — `s = "babad"` (indices 0–4)

| `i` | `expand(i, i)` — odd | `expand(i, i+1)` — even | `best` after |
|---|---|---|---|
| 0 `b` | `"b"` — `left` hits −1 | `s[0]='b'` vs `s[1]='a'` → `""` | `"b"` |
| 1 `a` | `s[0]='b'` = `s[2]='b'` ✓, then `s[-1]`… bounds stop → **`"bab"`** | `'a'` vs `'b'` → `""` | **`"bab"`** |
| 2 `b` | `s[1]='a'` = `s[3]='a'` ✓, then `s[0]='b'` vs `s[4]='d'` ✗ → `"aba"` | `'b'` vs `'a'` → `""` | `"bab"` (tie, keeps first) |
| 3 `a` | `s[2]='b'` vs `s[4]='d'` ✗ → `"a"` | `'a'` vs `'d'` → `""` | `"bab"` |
| 4 `d` | `"d"` | `right = 5` out of bounds → `""` | `"bab"` |

Return **`"bab"`** ✅ (`"aba"` from `i = 2` is equally valid; `max` kept the first).

**And `s = "cbbd"`**, where the even case earns its place:

| `i` | odd | even | `best` after |
|---|---|---|---|
| 0 `c` | `"c"` | `'c'` vs `'b'` → `""` | `"c"` |
| 1 `b` | `"b"` | `s[1]='b'` = `s[2]='b'` ✓ → **`"bb"`** | **`"bb"`** |
| 2 `b` | `"b"` | `'b'` vs `'d'` → `""` | `"bb"` |
| 3 `d` | `"d"` | out of bounds → `""` | `"bb"` |

Return **`"bb"`** ✅ — a result that **only** the even-center call can produce. Drop that line and this input returns `"c"`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²).**

- The outer loop runs **n** times.
- Each iteration makes two `expand` calls, and each expansion steps outward at most **n/2** times before running out of string → **O(n)** per call.
- n × O(n) = **O(n²)**.

Counted by centers instead: there are **2n − 1** centers, each expanding O(n) → same bound.

At n = 1000 that's ~10⁶ character comparisons. Comfortable.

**One honest note on constants:** `s[left + 1:right]` builds a **new string** each time, so a successful expansion of length L costs O(L) to slice as well as O(L) to scan. Same asymptotic class, roughly double the constant. If it mattered, you'd return `(left + 1, right)` and slice once at the end — a good thing to mention, not worth doing unasked.

**Best vs worst case.** The bound is worst-case, not always-case. On `"abcdefg"` every expansion fails on its first comparison, so it's effectively **O(n)**. On `"aaaaaaa"` every expansion runs to the string's edge — the genuine worst case, and the input to test with.

**Faster?** Yes — [Manacher's algorithm](../algorithms/manacher.md) achieves **O(n)** by reusing already-computed palindrome radii to skip comparisons that are guaranteed by symmetry. It's the optimal answer and rarely the expected one.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1) extra**, beyond the output.

- `expand` uses two integer pointers → O(1).
- `best`, `odd`, `even` hold string references. The strings themselves are slices of `s`, and at most O(n) characters at a time — but they're the answer (and transient candidates), not auxiliary structure.
- No table, no memo, no recursion stack — `expand` is iterative.

The comparison that makes this the winning approach:

| Approach | Space | Why |
|---|---|---|
| 2-D DP table | **O(n²)** | An n × n boolean table — 10⁶ entries at n = 1000 |
| Longest-common-substring with the reverse | **O(n²)** | The LCS DP table |
| **Expand around center** | **O(1)** | Two pointers and a running best |
| Manacher's | **O(n)** | The radius array |

**Same O(n²) time as the DP table, but O(n²) → O(1) space.** That's the trade this problem is really testing: recognizing that the DP recurrence can be *evaluated in an order* that makes storing it unnecessary. Expanding outward from a center is exactly the chain `dp[i+1][j-1] → dp[i][j]`, walked directly.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Brute force is O(n³) — O(n²) substrings, each checked in O(n) — and at n = 1000 that's too slow. The key structural fact is that every palindrome is built outward from a center, so instead of picking substrings and testing them, I pick centers and grow them. There are 2n−1 centers: n on a character for odd-length palindromes, n−1 between characters for even-length. Each expansion is O(n), so it's O(n²) total, with O(1) space since I only track two pointers and the best found. The 2-D DP is the same complexity but needs an n² table — expanding from a center is just that recurrence evaluated in an order where nothing has to be stored. Manacher's would get it to O(n) by reusing computed radii, but it's long and this input is small."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do you need two `expand` calls?" | Odd-length palindromes center on a character; even-length ones center in the gap between two. `"cbbd"` returns `"c"` if you only handle the odd case. |
| "Can you get O(n)?" | [Manacher's algorithm](../algorithms/manacher.md). It keeps the rightmost palindrome found so far and uses its symmetry to initialize each new center's radius, so no character is compared more than a constant number of times. |
| "What about matching against the reversed string?" | Longest common substring of `s` and `s[::-1]` — but it's wrong without an index check. On `"abacdfgdcaba"` it matches `"abacd"` against a different region entirely. Fixable, but it costs O(n²) space to do worse. |
| "Write the DP version." | `dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i+1][j-1])`, filled by increasing length. O(n²) time and space. Same recurrence, materialized. |
| "Count the palindromic substrings instead." | [Palindromic Substrings](647-palindromic-substrings.md) — identical scan, but count each successful expansion step rather than tracking the longest. |
| "Longest palindromic *subsequence*?" | Different problem — non-contiguous, so center expansion doesn't apply. It's the [longest common subsequence](1143-longest-common-subsequence.md) of `s` and its reverse, O(n²) time and space. |
| "Why does `max(..., key=len)` matter?" | Without `key=len`, `max` compares strings lexicographically and returns the alphabetically largest, not the longest. A silent wrong answer. |
| "Return indices instead of the substring." | Have `expand` return `(left + 1, right)` and track the widest span. Avoids building intermediate strings — a real constant-factor win. |

**Traps:**
- **Omitting the even-length centers.** The defining bug. `"cbbd"` → `"c"` instead of `"bb"`.
- **Off-by-one in the returned slice.** Both pointers overshoot by one when the loop exits; it must be `s[left + 1:right]`. Writing `s[left:right]` or `s[left + 1:right - 1]` gives lengths off by one or two.
- **Bounds checks after the character comparison.** `s[left] == s[right] and left >= 0` raises `IndexError` — and worse, Python's negative indexing means `s[-1]` silently reads the *last* character instead of failing, producing wrong answers rather than crashes.
- Forgetting `key=len` on `max`.
- Adding a bounds guard before `expand(i, i + 1)` — unnecessary, since the `while` condition already returns `""` at the last index.
- Assuming `"babad"` must return `"bab"`. Either answer is accepted; don't add tie-breaking logic.

**This same move shows up in:** [Palindromic Substrings](647-palindromic-substrings.md) (the identical center-expansion scan, counting instead of measuring) · [Valid Palindrome](125-valid-palindrome.md) (two pointers on a palindrome, converging rather than expanding) · [Longest Common Subsequence](1143-longest-common-subsequence.md) (the 2-D table this problem lets you avoid) · [Palindrome Partitioning](131-palindrome-partitioning.md) (palindrome checks inside a backtracking search).

</details>

---
