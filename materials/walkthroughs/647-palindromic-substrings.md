# 647. Palindromic Substrings

**Medium** · [LeetCode](https://leetcode.com/problems/palindromic-substrings/)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string `s`, return the **number of palindromic substrings** in it. A substring is a *contiguous* run of characters, and **substrings at different positions count separately even if they're identical**.

```
s = "abc"    →  3     "a", "b", "c"
s = "aaa"    →  6     "a"×3, "aa"×2, "aaa"  — the two "aa"s are different substrings
```

**Constraints:** `1 <= s.length <= 1000` · `s` consists of lowercase English letters.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**number of**" | Counting, not optimizing. Compare [Longest Palindromic Substring](5-longest-palindromic-substring.md), which is the same scan asking for a max |
| "**substrings**" | Contiguous. O(n²) of them, not 2ⁿ |
| identical substrings at different positions **count separately** | You're counting **positions**, not distinct strings. `"aaa"` → 6, not 3. No deduplication anywhere |
| every single character is a palindrome | So the answer is always **at least n**. Useful sanity check |
| `n <= 1000` | n² = 10⁶ fine, n³ = 10⁹ not. Same budget as problem 5 |

Since this is the counting twin of [problem 5](5-longest-palindromic-substring.md), the structural insight is identical: **every palindrome is built outward from a center**, so pick centers and grow them rather than picking substrings and testing them.

But there's one extra observation that makes the counting version *even simpler* than the longest version, and it's the thing worth arriving at yourself:

**Every successful expansion step is itself a palindrome.** When you expand from a center and the characters match, you haven't just made progress toward some larger answer — you've *found a palindrome*. Expand again and you've found another one, a longer one sharing the same center.

So from center `i` in `"aaa"`: `"a"` (1 step), `"aaa"` (2 steps). Two palindromes from one center, counted by how far you got.

That turns the whole problem into: **sum the expansion depths over all centers.** No comparison, no tracking a best, no slicing — just a counter.

🤔 **Before you open the next section:** you know there are 2n−1 centers. If every one of them expanded all the way to the string's edge, what string would that be, and how many palindromic substrings would it have? Does your formula match `"aaa"` → 6?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Check every substring | All O(n²) substrings, each verified in O(n) | **O(n³)** | O(1) | ❌ 10⁹ at n = 1000 |
| 2-D DP table | `dp[i][j]` = is `s[i..j]` a palindrome; count the `True`s | O(n²) | **O(n²)** | ⚠️ Correct, and the "textbook DP" answer — but a 10⁶-entry table for a single integer |
| **Expand around center** | For each of the 2n−1 centers, count how many steps it grows | O(n²) | **O(1)** | ✅ |
| [Manacher's algorithm](../algorithms/manacher.md) | Compute every palindrome radius in linear time; sum them | **O(n)** | O(n) | ⚠️ Optimal. Radii sum directly to the answer, which is elegant — but long to write |

**The decision:** **expand around center**, counting steps.

**Why this is a strictly easier problem than [5](5-longest-palindromic-substring.md), despite the same scan.** In problem 5 you had to *return the substring*, which meant slicing (`s[left + 1:right]`) and getting a fiddly off-by-one right, then comparing candidates by length. Here you only need a **count** — so the expansion returns an integer, there's no slice, no off-by-one, and no `max`. The pointer overshoot that made problem 5's return statement subtle simply doesn't arise, because you increment the counter *inside* the loop, before the pointers move.

**Why the DP table loses.** `dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i+1][j-1])` is correct and it's the same recurrence — the number of `True` entries is the answer. But it allocates n² booleans to produce one number. Center expansion evaluates the identical recurrence in an order (**outward from each center**) that makes storage unnecessary: the chain `dp[i+1][j-1] → dp[i][j]` *is* the expansion.

**The elegant thing about Manacher's here.** For the "longest" version, Manacher's gives you the max radius. For the *counting* version, the palindrome radius at each center is **exactly the number of palindromes centered there** — so the answer is just the sum of the radius array. If you're going to name Manacher's in an interview, this is the problem where the connection is cleanest.

**Why O(n²) is fine.** n ≤ 1000, so 10⁶ operations. The gap between O(n³) and O(n²) is what's being tested; the gap between O(n²) and O(n) is not.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def count_expand(left, right):
    count = 0
```
The same helper shape as [problem 5](5-longest-palindromic-substring.md), but returning an **integer** instead of a substring. `count` will hold how many palindromes are centered here.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
    while left >= 0 and right < len(s) and s[left] == s[right]:
        count += 1
        left -= 1
        right += 1
    return count
```
**Two pointers moving outward**, with the counter incremented **inside** the loop.

That placement is the entire algorithm. The loop body runs once for every valid expansion, and each valid expansion *is a palindrome* — `s[left..right]` reads the same both ways, because its ends just matched and its interior was verified on the previous iterations. So `count += 1` isn't bookkeeping; it's the answer accumulating.

The three conditions are all load-bearing, and the order matters: [`and`](../syntax/logical-operators.md) short-circuits left to right, so the bounds checks must precede the indexing. Reversing them doesn't just risk an `IndexError` — Python's negative indexing means `s[-1]` quietly reads the *last* character and produces wrong counts instead of crashing.

Note what's **absent** compared to problem 5: no slice, no `left + 1`, no exclusive-bound reasoning. The pointers still overshoot when the loop exits, but nothing reads them afterwards, so the overshoot is harmless.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [string-basics](../syntax/string-basics.md)

```python
total = 0
for i in range(len(s)):
```
The running sum across all centers, and a sweep over every index. One loop, two centers per iteration → all 2n−1 covered.
→ [variables-assignment](../syntax/variables-assignment.md) · [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    total += count_expand(i, i)
    total += count_expand(i, i + 1)
```
**Both center types.**

- `count_expand(i, i)` — a character is its own center. Always returns **at least 1** (a single character trivially matches itself), which is why the answer is never below n. Counts `"a"`, `"aba"`, `"xabax"`, …
- `count_expand(i, i + 1)` — the gap between two characters. Returns **0** when `s[i] != s[i+1]`, costing nothing. Counts `"aa"`, `"abba"`, …

Dropping the even case gives 3 for `"aaa"` instead of 6. No bounds guard is needed on the second call: at the last index, `right < len(s)` fails immediately and it returns 0.
→ [function-basics](../syntax/function-basics.md)

```python
return total
```
Every center has been swept, and every palindrome has exactly one center — so every palindrome was counted exactly once.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def countSubstrings(self, s: str) -> int:

        def count_expand(left, right):
            count = 0
            while left >= 0 and right < len(s) and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count

        total = 0
        for i in range(len(s)):
            total += count_expand(i, i)
            total += count_expand(i, i + 1)

        return total
```
</details>

**Trace it** — `s = "aaa"` (indices 0–2)

| `i` | odd `(i, i)` | palindromes found | even `(i, i+1)` | palindromes found | `total` |
|---|---|---|---|---|---|
| 0 | 1 step (`left` → −1 stops it) | `"a"` | 1 step | `"aa"` (0–1) | 2 |
| 1 | 2 steps | `"a"`, `"aaa"` (0–2) | 1 step | `"aa"` (1–2) | 5 |
| 2 | 1 step | `"a"` | 0 (out of bounds) | — | **6** |

Return **6** ✅ — three `"a"`s, two `"aa"`s, one `"aaa"`.

Look at `i = 1`, odd: the expansion ran twice and counted **2**, because both `"a"` and `"aaa"` are centered on index 1. That's the counting insight — depth of expansion equals number of palindromes at that center.

**And `s = "abc"`:** every odd expansion stops after one step (neighbours never match), every even expansion returns 0 immediately. Total = 3 ✅ — the guaranteed minimum of n.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²).**

- The outer loop runs **n** times.
- Two `count_expand` calls per iteration, each stepping outward at most **n/2** times → **O(n)** per call.
- n × O(n) = **O(n²)**.

Equivalently: **2n − 1** centers, each expanding O(n).

At n = 1000, ~10⁶ character comparisons.

**Constant factor, versus problem 5.** This version is genuinely *faster* than [Longest Palindromic Substring](5-longest-palindromic-substring.md) despite the identical scan, because it never builds a substring. Problem 5 slices `s[left + 1:right]` on every call — O(L) extra work and an allocation per center. Here the inner loop is a comparison and two decrements. Same O(n²), noticeably smaller constant.

**Best vs worst case.** The bound is worst-case. `"abcdefg"` fails every expansion immediately → effectively **O(n)**. `"aaaaaaa"` expands every center to the edge → the true worst case, and the input to test with. It's also the input that maximizes the answer: for a string of n identical characters, the count is `n(n+1)/2` — every substring is a palindrome. (Check: n = 3 → 6 ✅.)

**Faster?** [Manacher's algorithm](../algorithms/manacher.md) gives **O(n)**, and here the connection is unusually direct — the palindrome radius at each center is precisely the number of palindromes centered there, so the answer is the sum of the radius array.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a handful of integers (`total`, `count`, `left`, `right`, `i`), no matter how long the string is.

Nothing is allocated. No table, no memo, no recursion (`count_expand` is iterative), and — unlike [problem 5](5-longest-palindromic-substring.md) — **no substrings are ever built**.

| Approach | Space | Why |
|---|---|---|
| 2-D DP table | **O(n²)** | An n × n boolean table — 10⁶ entries at n = 1000, to produce one integer |
| Expand around center (problem 5) | O(1) extra | But allocates a fresh string per expansion |
| **Expand around center (counting)** | **O(1)** | Pure integer arithmetic |
| Manacher's | **O(n)** | The radius array |

This is the leanest problem in the unit: **O(n²) time and truly O(1) space**, and the entire state is four integers. Worth stating plainly, because the DP-table solution is what many people write first and it's a 10⁶× space difference for the same running time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Checking all O(n²) substrings costs O(n) each, so brute force is O(n³) and too slow. Instead I'll use the fact that every palindrome is built outward from a center. There are 2n−1 centers — n on a character, n−1 in the gaps — and the key observation for *counting* is that every successful expansion step is itself a palindrome. So I just count the steps: expand from each center and add however far it got. That's O(n²) time and O(1) space, and it's the same recurrence as the 2-D DP table, evaluated in an order where nothing has to be stored. Manacher's would make it O(n) — and here it's especially neat, since the palindrome radius at each center *is* the count for that center, so the answer is the sum of the radius array."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does counting expansion steps work?" | Because when the loop body runs, `s[left..right]` is a palindrome — its ends just matched and its interior was confirmed on previous iterations. Each iteration is one distinct palindrome sharing that center. |
| "How does this differ from Longest Palindromic Substring?" | Identical scan. That one tracks the max and returns a slice; this one sums the depths. Counting is easier — no slicing, so no off-by-one. |
| "Count only *distinct* palindromic substrings." | Different problem. Collect them in a `set` (O(n²) space), or use a palindromic tree / Eertree for O(n). The current approach counts positions, not distinct strings. |
| "Can you do it in O(n)?" | [Manacher's](../algorithms/manacher.md) — sum the radius array. Each radius is the count of palindromes at that center. |
| "Write the DP version." | `dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i+1][j-1])`, filled by increasing substring length, counting `True`s. O(n²) both ways. |
| "What's the maximum possible answer?" | `n(n+1)/2`, achieved when all characters are identical — every substring is then a palindrome. Good for validating an implementation. |
| "What's the minimum?" | `n` — every single character is a palindrome, and a string of all-distinct characters has nothing longer. |
| "What if you also needed the longest one?" | Track `right - left - 1` at the end of each expansion alongside the count. One pass gives both answers. |

**Traps:**
- **Omitting the even-length centers.** `"aaa"` returns 3 instead of 6. The defining bug of both this problem and [5](5-longest-palindromic-substring.md).
- **Incrementing `count` after the loop instead of inside it.** You'd count one palindrome per center rather than one per expansion — `"aaa"` gives 5.
- **Bounds checks after the character comparison.** Python's negative indexing turns this into silently wrong counts rather than a crash, which is far worse to debug.
- Trying to deduplicate. The problem explicitly counts identical substrings at different positions separately.
- Double-counting single characters by initializing `total = len(s)` *and* letting the odd expansions count them.
- Reaching for the DP table by reflex. It's accepted; it's also 10⁶ booleans for one integer.

**This same move shows up in:** [Longest Palindromic Substring](5-longest-palindromic-substring.md) (the identical center-expansion scan, maximizing instead of counting) · [Valid Palindrome](125-valid-palindrome.md) (two pointers on a palindrome, converging rather than expanding) · [Palindrome Partitioning](131-palindrome-partitioning.md) (palindrome checks driving a backtracking search) · [Climbing Stairs](70-climbing-stairs.md) (the counting-vs-optimizing distinction, from the other direction).

</details>

---
