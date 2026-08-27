# 392. Is Subsequence

**Easy** · [LeetCode](https://leetcode.com/problems/is-subsequence/) · [Solution file (no hints)](../../problems/0001-0499/392.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given two strings `s` and `t`, return `true` if `s` is a **subsequence** of `t`. A subsequence is formed by deleting some (possibly zero) characters from `t` **without changing the relative order** of the remaining characters.

```
s = "abc",  t = "ahbgdc"   →  true
s = "axc",  t = "ahbgdc"   →  false
```

**Constraints:** `0 <= s.length <= 100` · `0 <= t.length <= 10⁴` · lowercase English letters

**Follow-up:** if there are ≥ 10⁹ incoming `s` values to check against the same `t`, how would you adapt?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**", not substring | ⚠️ Characters need **not** be contiguous — gaps are allowed. `"abc"` is a subsequence of `"ahbgdc"` |
| "without changing **relative order**" | Order matters. `"acb"` is *not* a subsequence of `"abc"` |
| "possibly zero" deletions | `s == t` counts, and the empty `s` is a subsequence of anything |
| `s` can be **empty** | Must return `true`, not crash |
| `|s| ≤ 100`, `|t| ≤ 10⁴` | Tiny for a single query — the follow-up is where the real design question lives |
| the **follow-up** | 10⁹ queries against one `t` ⇒ preprocess `t` once and amortize |

The core insight is that **greedy matching is optimal here**, and it's worth understanding why rather than taking it on faith:

> Walk through `t` once. Whenever the current character of `t` equals the character of `s` you're looking for, **take it** and advance in `s`. If `s` runs out, you've matched everything.

**Why is taking the earliest match always safe?** Suppose there's *some* valid way to embed `s` in `t`. Consider the first character of `s`: greedy matches it at the earliest possible position in `t`. Any other valid embedding matches it at that position or later — so greedy leaves **at least as much of `t` remaining** for the rest of `s`. By induction, greedy never does worse. There's no scenario where "saving" a character for later helps.

That exchange argument is the reason no DP or backtracking is needed, and it's exactly the sort of justification an interviewer wants to hear.

🤔 **Before you open the next section:** if you're scanning `t` looking for the characters of `s` in order, when do you advance in `t`, and when do you advance in `s`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `m = |s|`, `n = |t|`.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursive / backtracking | Try matching or skipping at each position | O(2ⁿ) | O(n) | ❌ Exponential, and unnecessary — greedy is provably optimal |
| DP table | `dp[i][j]` = is `s[:i]` a subsequence of `t[:j]` | O(m·n) | O(m·n) | ⚠️ Correct, wildly over-built |
| **Two pointers (greedy)** | Advance in `t` always, in `s` on a match | **O(n)** | **O(1)** | ✅ |
| **Preprocess + binary search** | Index positions per character; binary search forward | O(n) build, **O(m log n)** per query | O(n) | ✅ The follow-up answer |

**The decision for a single query: two pointers.**

- `i` indexes `s` (what we still need to match)
- `j` indexes `t` (where we're looking)
- `j` advances **every** iteration; `i` advances **only** on a match
- Success when `i` reaches `len(s)` — every character of `s` was found in order

The asymmetry is the whole algorithm: you consume `t` unconditionally, and consume `s` opportunistically.

**The decision for the follow-up: preprocess `t` into a per-character position index**, then binary search.

Build `index[ch] = [sorted list of positions where ch occurs in t]` once — O(n). Then for each query `s`, track your current position `pos` in `t`, and for each character of `s`, binary search that character's position list for the **first position ≥ `pos`**. If none exists, fail; otherwise jump there and continue.

Each query becomes **O(m log n)** instead of O(n). With 10⁹ queries against a fixed `t`, that's the difference between feasible and not:

| | Per query | 10⁹ queries, m=100, n=10⁴ |
|---|---|---|
| Two pointers | O(n) = 10⁴ | 10¹³ operations |
| Binary search | O(m log n) ≈ 100 × 14 = 1400 | ~10¹² — and independent of `n` growth |

This is the same **"move work to a one-time preprocessing step"** design as [Range Sum Query - Immutable](303-range-sum-query-immutable.md). The trigger is identical: many queries against unchanging data.

**Why not DP?** It computes far more than you need — the answer for every prefix pair — when a single greedy pass suffices. Mention it only to dismiss it. (DP *does* become necessary for the harder relative, [Distinct Subsequences](115-distinct-subsequences.md), where you must *count* embeddings rather than detect one.)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — two pointers** (the single-query answer)

```python
i = 0
j = 0
```

`i` walks `s`, `j` walks `t`. Both start at the front.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while i < len(s) and j < len(t):
```

Continue while there's still something to match **and** somewhere left to look. Either running out ends the search — though for different reasons, which the return statement disentangles.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if s[i] == t[j]:
        i += 1
```

**Greedy match.** Found the character we need, so consume it from `s` — take the earliest occurrence, which the exchange argument above proves is safe.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    j += 1
```

**Outside the `if` — this is the asymmetry.** `j` advances on **every** iteration, match or not: on a match we've used that character of `t`; on a mismatch we skip it (that's the "deleting characters from `t`" the problem describes).

Putting `j += 1` inside the `if` is the classic bug — the loop then spins forever on the first mismatch.

```python
return i == len(s)
```

**The verdict, and it's subtler than it looks.** The loop can exit two ways:

- **`i` reached `len(s)`** — every character matched ⇒ `true`
- **`j` reached `len(t)`** with `i` short — ran out of `t` ⇒ `false`

Comparing `i` to `len(s)` distinguishes them in one expression. It also handles empty `s` for free: the loop never runs, `i` is 0, `len(s)` is 0, and `0 == 0` is `true` ✅
→ [if-return](../syntax/if-return.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:

        i = 0
        j = 0

        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1

        return i == len(s)
```

</details>

---

**Approach B — preprocess + binary search** (the follow-up)

```python
from bisect import bisect_left
from collections import defaultdict

def preprocess(t: str):
    index = defaultdict(list)
    for i, ch in enumerate(t):
        index[ch].append(i)
    return index
```

Build once: character → **ascending** list of its positions in `t`. Ascending automatically, since we append while scanning left to right — which is what makes binary search valid.
→ [defaultdict](../syntax/defaultdict.md) · [enumerate](../syntax/enumerate.md)

```python
def isSubsequence(s: str, index: dict) -> bool:
    pos = 0
    for ch in s:
        if ch not in index:
            return False
```

`pos` is the earliest position in `t` still available. A character absent from `t` entirely is an immediate fail.
→ [membership-operators](../syntax/membership-operators.md)

```python
        positions = index[ch]
        i = bisect_left(positions, pos)
        if i == len(positions):
            return False
        pos = positions[i] + 1
```

**The jump.** `bisect_left` finds the insertion point for `pos` — i.e. the index of the first occurrence **at or after** `pos`. If that's past the end of the list, every occurrence of `ch` is behind us and the match fails.

Otherwise, take that occurrence and set `pos` to **one past it**, so the next character must appear strictly later. The `+ 1` is what enforces ordering.
→ [bisect-module](../syntax/bisect-module.md)

<details>
<summary>Approach B together</summary>

```python
### Follow up ###
from bisect import bisect_left
from collections import defaultdict


def preprocess(t: str):
    index = defaultdict(list)
    for i, ch in enumerate(t):
        index[ch].append(i)
    return index


def isSubsequence(s: str, index: dict) -> bool:
    pos = 0
    for ch in s:
        if ch not in index:
            return False
        positions = index[ch]
        i = bisect_left(positions, pos)
        if i == len(positions):
            return False
        pos = positions[i] + 1
    return True
```

</details>

**Trace approach A** — `s = "abc"`, `t = "ahbgdc"`:

| `i` | `j` | `s[i]` | `t[j]` | Match? | `i` after | `j` after |
|---|---|---|---|---|---|---|
| 0 | 0 | `a` | `a` | ✅ | 1 | 1 |
| 1 | 1 | `b` | `h` | ❌ | 1 | 2 |
| 1 | 2 | `b` | `b` | ✅ | 2 | 3 |
| 2 | 3 | `c` | `g` | ❌ | 2 | 4 |
| 2 | 4 | `c` | `d` | ❌ | 2 | 5 |
| 2 | 5 | `c` | `c` | ✅ | **3** | 6 |

Loop exits (`i == 3 == len(s)`). Return `3 == 3` → **`true`** ✅

**And a failure** — `s = "axc"`, `t = "ahbgdc"`:

| `i` | `j` | `s[i]` | `t[j]` | Match? |
|---|---|---|---|---|
| 0 | 0 | `a` | `a` | ✅ → `i=1` |
| 1 | 1..5 | `x` | `h,b,g,d,c` | ❌ ×5 |

`j` reaches 6 with `i` stuck at 1. Return `1 == 3` → **`false`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n) per query, or O(m log n) after preprocessing</summary>

**Approach A: O(n)** where `n = |t|`.

`j` advances exactly once per iteration and never resets, so the loop runs at most `n` times. `i` only ever moves forward. It's a single pass over `t` — and it can exit early once `s` is exhausted, so it's often much less.

Note it's O(n), not O(m + n) or O(m·n): the work is bounded by the length of `t`, since that's what we scan.

**Approach B: O(n) build, then O(m log n) per query.**

- Build: one pass over `t`, appending to lists — O(n).
- Query: `m` binary searches, each O(log n) over a position list.

**Why the follow-up needs B:**

| Queries | Two pointers | Preprocess + bisect |
|---|---|---|
| 1 | O(n) ✅ | O(n) build + O(m log n) — not worth it |
| 10⁹ | 10⁹ × O(n) = **10¹³** ❌ | O(n) once + 10⁹ × O(m log n) ✅ |

The break-even is roughly when query count exceeds `n / (m log n)`. Below that, the simple version wins; far above it, preprocessing dominates. **Being able to say where the crossover is** — rather than just "preprocess for many queries" — is what separates a good answer from a memorized one.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) or O(n)</summary>

| Approach | Space | Note |
|---|---|---|
| Two pointers | **O(1)** | Two integers, no allocation |
| Preprocess + bisect | **O(n)** | Every position of `t` stored exactly once across the lists |

The index's total size is exactly `n` — each character of `t` contributes one entry — plus dictionary overhead bounded by the alphabet (26 here). So O(n), with a small constant.

**The trade in one line:** O(n) memory, held once, converts each query from O(n) to O(m log n). With 10⁹ queries that's overwhelmingly worth it; with one query it's pure waste.

That's the same amortization logic as [Range Sum Query - Immutable](303-range-sum-query-immutable.md) and [Implement Trie](208-implement-trie-prefix-tree.md) — build a structure once, query it cheaply forever. The precondition is always the same: **the underlying data doesn't change.**

</details>

<details>
<summary><b>6 · Talk it through</b> — thoughts & follow-ups</summary>

**Say this out loud:**

> "Two pointers, one per string. I scan `t` from left to right, and whenever the current character matches the one I need from `s`, I advance in `s`. The `t` pointer advances every step regardless — skipping a character is exactly the 'deletion' the problem allows. If `s` runs out, it's a subsequence. Greedy is safe here because taking the earliest match leaves the most of `t` available for what remains, so it never does worse than any other embedding. O(n) time, O(1) space. For the follow-up with a billion queries against the same `t`, I'd preprocess `t` into a map from character to its sorted list of positions, then binary search forward for each character — O(n) once, then O(m log n) per query."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "10⁹ queries against the same `t`?" | **The stated follow-up.** Preprocess into per-character position lists, binary search forward. O(m log n) per query. |
| "Why is greedy correct?" | Exchange argument: the earliest match leaves at least as much of `t` remaining as any alternative, so it's never worse. |
| "**Count** the distinct embeddings instead." | Now greedy fails — that's DP. See [Distinct Subsequences](115-distinct-subsequences.md), O(m·n). |
| "Longest common subsequence of `s` and `t`?" | Different problem — 2-D DP, [LCS](1143-longest-common-subsequence.md), O(m·n). |
| "Substring instead of subsequence?" | Contiguity required ⇒ `t.find(s)`, or [KMP](../algorithms/kmp.md) for guaranteed O(m+n). |
| "What if `s` is empty?" | `true`. Handled for free: the loop doesn't run and `0 == 0`. |
| "Return the matched indices?" | Record `j` each time you advance `i`. |
| "What if `t` changes between queries?" | Preprocessing is invalidated. Rebuild — or if edits are frequent, reconsider the whole design. |

**Traps:**

- **Putting `j += 1` inside the `if`.** Infinite loop on the first mismatch — the pointer never moves past it.
- **Returning `j == len(t)`.** Wrong question. You care whether **`s`** was exhausted, not `t`; trailing characters in `t` are fine.
- **Advancing `i` on a mismatch.** Skips characters of `s`, which isn't allowed — deletions come from `t` only.
- **Confusing subsequence with substring.** Subsequences allow gaps; substrings don't. `"abc"` is a subsequence but not a substring of `"ahbgdc"`.
- **Reaching for DP.** Correct but O(m·n) time and space for something a greedy pass solves in O(n)/O(1).
- **Forgetting `+ 1` when updating `pos` in the binary-search version.** Without it, the same position could be reused for two characters, breaking strict ordering.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (two pointers advancing at different rates over two sequences) · [Valid Palindrome II](680-valid-palindrome-ii.md) (two pointers with skips allowed) · [Distinct Subsequences](115-distinct-subsequences.md) (the counting version, where greedy fails and DP is required) · [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (the same preprocess-once-for-many-queries design).

</details>

---
