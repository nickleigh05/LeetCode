# 1456. Maximum Number of Vowels in a Substring of Given Length

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) · [Solution file (no hints)](../../problems/1000-1499/1456.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given a string `s` and an integer `k`, return the **maximum number of vowel letters** in any substring of `s` with length `k`. Vowels are `'a'`, `'e'`, `'i'`, `'o'`, `'u'`.

```
s = "abciiidef", k = 3  →  3    ("iii")
s = "aeiou",     k = 2  →  2    (any substring of length 2)
s = "leetcode",  k = 3  →  2    ("lee", "eet", "ode")
```

**Constraints:** `1 <= s.length <= 10⁵` · `1 <= k <= s.length` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "substring of length **`k`**" | ⚠️ **Fixed-size window.** Same shape as [Maximum Average Subarray I](643-maximum-average-subarray-i.md) — no shrink logic needed |
| "**maximum** number of vowels" | Track a running best across all windows |
| "vowels are a, e, i, o, u" | A fixed 5-element membership test — a [set](../data-structures/hashset.md) gives O(1) |
| `k <= s.length` guaranteed | At least one window exists; no empty case |
| `s.length` up to 10⁵ | Recounting each window is O(n·k) = 10¹⁰ — dead |
| lowercase only | No case-folding needed |

This is the **counting** variant of the fixed sliding window. Where [Maximum Average Subarray I](643-maximum-average-subarray-i.md) maintained a running *sum*, this maintains a running *count of elements satisfying a predicate*.

That's the generalization worth extracting:

> A fixed sliding window can maintain **any quantity that supports cheap add and cheap remove**. Sums qualify. Counts-of-a-predicate qualify. Frequency maps qualify. Maximums do *not* — removing the current maximum tells you nothing about the next one, which is why [Sliding Window Maximum](239-sliding-window-maximum.md) needs a deque instead of a counter.

Here the quantity is "how many vowels are in the window," and both operations are trivial:

- character entering and it's a vowel → `count += 1`
- character leaving and it was a vowel → `count -= 1`

🤔 **Before you open the next section:** when the window slides one step, exactly two characters change status. What are they, and what does each do to the count?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each start, count vowels in `k` chars | O(n·k) | O(1) | ❌ 10¹⁰ |
| Prefix counts | `prefix[i]` = vowels in `s[:i]`; subtract | O(n) | **O(n)** | ⚠️ Correct, needless memory |
| **Fixed sliding window** | Running count; adjust by the two changing chars | **O(n)** | **O(1)** | ✅ |

**The decision: a fixed-size sliding window over a vowel counter.**

Two phases:

1. **Prime** — count vowels in the first `k` characters, once.
2. **Slide** — for each subsequent position, adjust by the entering and leaving characters, then update the best.

**Why a set for the vowel test.** `c in {'a','e','i','o','u'}` is an O(1) hash lookup. Alternatives:

| Test | Cost | Note |
|---|---|---|
| `c in {'a','e','i','o','u'}` | **O(1)** | ✅ Set — hashed |
| `c in "aeiou"` | O(5) | String scan; fine for 5 chars, but O(1) is free |
| `c == 'a' or c == 'e' or …` | O(5) | Verbose, error-prone |

With only five elements the practical difference is negligible, but the *habit* matters — on a larger character class the set is the only sensible choice. Also note the set literal is rebuilt on every call unless hoisted; defining it once outside the loop (as the solution does) avoids that.

**Why two independent `if`s, not `if/else`?** The entering and leaving characters are unrelated — both, neither, or either could be a vowel. Chaining them with `else` would miss cases where both change.

**An early-exit worth mentioning:** if `count == k`, every character in the window is a vowel and no window can do better, so you could return immediately. It doesn't change the asymptotics but is a legitimate optimization and shows you're thinking about the bound.

**Why not prefix counts?** `prefix[i+k] - prefix[i]` works and is O(n) time — but it's O(n) space for something a single integer handles. Same trade-off as in [Maximum Average Subarray I](643-maximum-average-subarray-i.md): prefix arrays earn their keep for *arbitrary* range queries, not for a window marching one step at a time.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
vowels = {'a', 'e', 'i', 'o', 'u'}
```

A set for O(1) membership, built **once** outside the loop.
→ [set-basics](../syntax/set-basics.md)

```python
count = sum(1 for c in s[:k] if c in vowels)
```

**Prime the window** — count vowels in the first `k` characters. One O(k) pass, done once.

The generator expression `sum(1 for … if …)` is the idiomatic "count matching items" construction: it yields a `1` per match and sums them, without materializing a list.
→ [generator-expressions](../syntax/generator-expressions.md) · [list-slicing](../syntax/list-slicing.md)

```python
max_count = count
```

Seed the best with the first window. Safe because `k <= len(s)` guarantees it exists. (Seeding at `0` would also happen to work here, since counts are non-negative — unlike [Maximum Average Subarray I](643-maximum-average-subarray-i.md), where negatives made it a real bug. Seeding with the first window is the habit that transfers.)

```python
for i in range(k, len(s)):
```

Start at `k` — the index of the first character to **enter** the window.
→ [range-function](../syntax/range-function.md)

```python
    if s[i] in vowels:
        count += 1
```

The **entering** character on the right edge.

```python
    if s[i - k] in vowels:
        count -= 1
```

The **leaving** character on the left edge. `i - k` is the index that just fell out — the window now spans `[i-k+1, i]`.

Two separate `if`s: both can fire in the same iteration (e.g. a vowel enters and a vowel leaves, leaving the count unchanged).
→ [membership-operators](../syntax/membership-operators.md)

```python
    max_count = max(max_count, count)
```

→ [min-max-key](../syntax/min-max-key.md)

```python
return max_count
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxVowels(self, s: str, k: int) -> int:

        vowels = {'a', 'e', 'i', 'o', 'u'}
        count = sum(1 for c in s[:k] if c in vowels)
        max_count = count

        for i in range(k, len(s)):
            if s[i] in vowels:
                count += 1
            if s[i - k] in vowels:
                count -= 1
            max_count = max(max_count, count)

        return max_count
```

</details>

**Trace it** — `s = "abciiidef"`, `k = 3`:

| Step | `i` | Window | Entering `s[i]` | Leaving `s[i-k]` | `count` | `max_count` |
|---|---|---|---|---|---|---|
| prime | — | `"abc"` | — | — | **1** (`a`) | 1 |
| 1 | 3 | `"bci"` | `i` ✅ +1 | `a` ✅ −1 | 1 | 1 |
| 2 | 4 | `"cii"` | `i` ✅ +1 | `b` ✗ | 2 | 2 |
| 3 | 5 | `"iii"` | `i` ✅ +1 | `c` ✗ | **3** | **3** |
| 4 | 6 | `"iid"` | `d` ✗ | `i` ✅ −1 | 2 | 3 |
| 5 | 7 | `"ide"` | `e` ✅ +1 | `i` ✅ −1 | 2 | 3 |
| 6 | 8 | `"def"` | `f` ✗ | `i` ✅ −1 | 1 | 3 |

Return **3** ✅

Rows 1 and 5 show both `if`s firing at once — a vowel entering *and* a vowel leaving, netting zero change. An `if/else` would have handled only one of them and produced a wrong count.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Priming: O(k)
- Sliding loop: `n - k` iterations, each doing two O(1) set lookups and a `max`

Total O(k) + O(n − k) = **O(n)**, independent of `k`.

**Compare to brute force:** O(n·k) — at `n = 10⁵` and `k = 5·10⁴`, that's 5·10⁹ operations versus 10⁵. The window does two lookups per step regardless of window size.

This is optimal; every character must be examined at least once.

**With the `count == k` early exit**, the best case can be as fast as O(k) — though the worst case is unchanged.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

The vowel set holds exactly 5 elements — a constant, not a function of input size. `count` and `max_count` are integers.

The `s[:k]` slice in the priming line allocates a temporary string of length `k`, so strictly it's O(k) for an instant. Avoid it with an explicit loop if you want unambiguous O(1):

```python
count = 0
for i in range(k):
    if s[i] in vowels:
        count += 1
```

Nobody will object to the slice, but knowing it's there is worth a sentence if an interviewer is being precise about space.

**Compare to prefix counts:** O(n) space for the same O(n) time — strictly worse here, for the same reason as in [Maximum Average Subarray I](643-maximum-average-subarray-i.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Fixed-size window, so no shrink logic — the window always spans exactly `k` characters. I prime by counting vowels in the first `k`, then slide: each step, one character enters on the right and one leaves on the left, so I adjust the count by at most one in each direction and take the max. Vowel membership is a set lookup, O(1). Two independent `if`s rather than `if/else`, because both the entering and leaving characters can be vowels in the same step. O(n) time, O(1) space. I could also return early if the count ever hits `k`, since that's the maximum possible."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Return the **substring**, not the count." | Track the index where `max_count` was achieved; slice `s[idx-k+1 : idx+1]`. |
| "Maximum vowels in a substring of length **at most** `k`?" | Trivially the same answer — a longer window can't have fewer vowels, so the best length-`k` window wins. Worth reasoning aloud rather than assuming. |
| "**At least** `k`?" | Now unbounded on the right — the answer is the total vowel count of the whole string. |
| "Longest substring with **at most** `m` vowels?" | A *variable*-size window: grow right, shrink left while the count exceeds `m`. See [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md). |
| "Maximum *character* in the window instead of a count?" | Counters don't work — removing the max tells you nothing. Needs a monotonic deque, as in [Sliding Window Maximum](239-sliding-window-maximum.md). |
| "Handle uppercase too." | Add uppercase vowels to the set, or lowercase each character as you test it. |
| "Can you exit early?" | Yes — `if count == k: return k`. Every character in the window is a vowel; nothing beats it. |

**Traps:**

- **Using `if/else` for the two edges.** Misses the case where both characters are vowels; the count drifts and the answer is wrong.
- **Wrong leaving index.** It's `s[i - k]`, not `s[i - k + 1]`. Off by one shifts the entire window.
- **Recounting the window each step.** `sum(1 for c in s[i:i+k] ...)` is the O(n·k) brute force in sliding-window clothing.
- **Rebuilding the vowel set inside the loop.** Correct but wasteful — hoist it.
- **`c in "aeiou"`.** Works, but it's a linear scan; the set states the intent and is O(1).
- **Starting the loop at `k+1` or `k-1`.** The first entering index is exactly `k`.

**This same move shows up in:** [Maximum Average Subarray I](643-maximum-average-subarray-i.md) (the same fixed window maintaining a sum) · [Contains Duplicate II](219-contains-duplicate-ii.md) (fixed window maintaining a set) · [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md) (fixed window maintaining a full frequency map) · [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) (the variable-size cousin, where a condition drives the shrink).

</details>

---
