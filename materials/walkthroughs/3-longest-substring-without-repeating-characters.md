# 3. Longest Substring Without Repeating Characters

**Medium** · [LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · [Solution file (no hints)](../../problems/0001-0499/3.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given a string `s`, find the length of the **longest substring** without repeating characters.

```
s = "abcabcbb"  →  3     ("abc")
s = "bbbbb"     →  1     ("b")
s = "pwwkew"    →  3     ("wke" — note "pwke" is a subsequence, not a substring)
```

**Constraints:** `0 <= s.length <= 5·10⁴` · `s` consists of English letters, digits, symbols and spaces

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**substring**" | ⚠️ **Contiguous.** Not a subsequence — you can't skip characters. The `"pwwkew"` example calls this out explicitly |
| "without **repeating** characters" | Every character in the window must be distinct — a membership question, which means a set |
| "**longest**" | Maximize the window size. Track a running best; no early exit |
| n up to 5·10⁴ | O(n²) = 2.5·10⁹ is too slow. Target **O(n)** |
| length can be **0** | Empty string → 0. Must not crash |
| "letters, digits, symbols, spaces" | The alphabet isn't just 26 — don't hard-code a small array |

**Contiguous + "longest valid range"** is the signature of a sliding window. Two pointers both moving forward, defining a range `[left, right]` that grows when it can and shrinks when it must.

The design question for any window problem is always the same three parts:

1. **What makes the window valid?** — all characters distinct.
2. **When do I grow?** — always; `right` advances every step.
3. **When and how much do I shrink?** — when adding `s[right]` creates a duplicate.

That third one is where this problem lives. If `s[right]` is already inside the window, shrinking by one from the left may not be enough — you must shrink until **that specific duplicate** is gone.

🤔 **Before you open the next section:** your window is `"abc"` and the next character is `"a"`. How far must `left` move to make the window valid again — and how would you know when to stop?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | Check every substring for uniqueness | O(n³) | ❌ Hopeless |
| Every start + set | For each start, extend until a repeat | O(n²) | ❌ Rescans the same characters repeatedly |
| **Window + hash set** | Grow right, shrink left until valid | **O(n)** | ✅ |
| Window + hash **map** of last index | On a duplicate, jump `left` straight past it | O(n) | ✅ Fewer steps; slightly more bookkeeping |

**The decision: a sliding window with a [hashset](../data-structures/hashset.md) of the characters currently inside it.**

The set answers "is this character already in my window?" in O(1) — the [Contains Duplicate](217-contains-duplicate.md) primitive again, but now applied to a *moving range* rather than the whole array.

**The shrink rule, which is the heart of it.** When `s[right]` is already in the window, remove characters from the left **one at a time until the duplicate is gone**. You can't just remove one — consider window `"abc"` and incoming `"a"`: removing only `c` or only `b` leaves the offending `a` in place. You must evict up to and including it.

The `while` loop expresses that precisely: keep shrinking *while the problem persists*. That's a much more reliable formulation than trying to compute the shrink distance.

**Why not the last-index map?** It's a genuine optimization — store `char → last index seen`, and on a duplicate jump `left` directly to `last[c] + 1` instead of stepping. Same O(n), fewer operations. Worth mentioning out loud. But the set version makes the *invariant* obvious ("the set is exactly the window"), and clarity matters more than constant factors when you're explaining under pressure.

**What makes the window pattern O(n)** is that `left` and `right` each traverse the string **at most once, forward only**. No pointer ever backtracks — that's the property to name.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
window = set()
left = 0
longest = 0
```

`window` holds exactly the characters currently in `[left, right]` — keeping that invariant true is the whole job. `left` is the window's start; `longest` is the running best, starting at 0 so an empty string returns 0 with no special case.
→ [set-basics](../syntax/set-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for right in range(len(s)):
```

`right` drives the loop, advancing one character per iteration and never going back. Every character gets its turn as the window's right edge.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    while s[right] in window:
        window.remove(s[left])
        left += 1
```

**The shrink.** While the incoming character conflicts, evict from the left. Each eviction removes `s[left]` from the set *and* advances `left`, keeping the set and the range in sync.

It's a `while`, not an `if`, because you must keep going until the specific duplicate is evicted — that could take several steps. And the loop is guaranteed to terminate: the offending character *is* somewhere in the window, so eventually `left` reaches it, removes it, and the condition goes false.
→ [while-loop](../syntax/while-loop.md) · [membership-operators](../syntax/membership-operators.md) · [set-operations](../syntax/set-operations.md)

```python
    window.add(s[right])
```

Now that the window is valid, extend it to include the new character. **After** the shrink — adding first would make the `while` condition immediately true and evict everything.
→ [set-operations](../syntax/set-operations.md)

```python
    longest = max(longest, right - left + 1)
```

Measure. `right - left + 1` is the window length — **the `+ 1` because both ends are inclusive** (a window from index 2 to 2 has length 1, not 0).

Measured *after* the shrink, so the window is guaranteed valid at this moment.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return longest
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        window = set()
        left = 0
        longest = 0

        for right in range(len(s)):
            while s[right] in window:
                window.remove(s[left])
                left += 1
            window.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
```

</details>

**Trace it** — `s = "abcabcbb"`:

| `right` | char | Conflict? | Shrink | `window` after | `left` | Length | `longest` |
|---|---|---|---|---|---|---|---|
| 0 | a | no | — | `{a}` | 0 | 1 | 1 |
| 1 | b | no | — | `{a,b}` | 0 | 2 | 2 |
| 2 | c | no | — | `{a,b,c}` | 0 | **3** | **3** |
| 3 | a | **yes** | evict `a` | `{b,c,a}` | 1 | 3 | 3 |
| 4 | b | **yes** | evict `b` | `{c,a,b}` | 2 | 3 | 3 |
| 5 | c | **yes** | evict `c` | `{a,b,c}` | 3 | 3 | 3 |
| 6 | b | **yes** | evict `a`, then `b` | `{c,b}` | 5 | 2 | 3 |
| 7 | b | **yes** | evict `c`, then `b` | `{b}` | 7 | 1 | 3 |

Answer: **3**. Note row 6 — two evictions in one step, which is exactly why the shrink must be a `while`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — and, as with everything in these two units, the nested loop is the thing to defend.

- The `for` loop: n iterations, `right` advancing once each.
- The inner `while`: advances `left`.

**The argument:** `left` starts at 0, only ever increases, and can never exceed `right` — so across the *entire* run it advances at most n times **in total**. Not n times per iteration. Every character therefore enters the window exactly once (`add`) and leaves at most once (`remove`).

Total work ≈ 2n set operations, each O(1) average → **O(n)**.

This is the defining property of the sliding-window pattern, and the sentence to have ready:

> *"Each pointer only moves forward and each element enters and leaves the window at most once, so the total work is linear even though the loops are nested."*

Same amortized reasoning as [Valid Palindrome](125-valid-palindrome.md) and [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) — it keeps recurring because it's how most O(n) solutions with inner loops justify themselves.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(min(n, m))</summary>

**O(min(n, m))**, where m is the size of the character set.

The set holds only what's currently in the window, and since every character in it is distinct, it's bounded two ways:

- It can't exceed the window, which can't exceed the string → **O(n)**.
- It can't hold more distinct characters than exist in the alphabet → **O(m)**.

Whichever is smaller binds. For ASCII, m = 128, so on a long string it's effectively **O(1)** — but stating `O(min(n, m))` is the precise answer and shows you noticed both bounds.

**Contrast with [Valid Anagram](242-valid-anagram.md)**, where O(1) was justified by the promise of lowercase-only input. Here the problem explicitly allows "letters, digits, symbols and spaces", so you *can't* claim a 26-letter bound — and hard-coding a 26-slot array would be an outright bug.

The lesson: **read the alphabet constraint before deciding your space claim.** It changes the answer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Substring means contiguous, and I want the longest valid range — that's a sliding window. I'll keep a hash set of the characters currently inside it. `right` advances every step; when the incoming character is already in the window, I shrink from the left until that duplicate is evicted, then add the new character and measure. The shrink is a `while` rather than an `if` because removing one character may not clear the specific conflict. Each pointer only moves forward and each character enters and leaves at most once, so it's O(n) time despite the nested loop, and O(min(n, m)) space for the set."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you avoid stepping `left` one at a time?" | Store `char → last index` in a map and jump `left = max(left, last[c] + 1)`. Same O(n), fewer operations. The `max` matters — never move `left` backwards. |
| "Return the substring, not the length." | Record the start index whenever you update `longest`, then slice at the end. |
| "At most **k** distinct characters?" | Same window, different validity rule: shrink while `len(count) > k`. Use a count map rather than a set. LeetCode 340. |
| "At most **two** distinct?" | The k = 2 special case. Identical code. |
| "**Longest** repeating with k replacements?" | A different validity predicate on the same skeleton — see [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md). |
| "What if it were a *subsequence*?" | Completely different — you could take every distinct character, so the answer is just the number of distinct characters. Worth confirming you read "substring" correctly. |
| "Unicode input?" | The set version already handles it. A fixed 128- or 26-slot array would not. |

**Traps:**

- **`if` instead of `while` for the shrink.** Leaves the duplicate in the window and silently returns wrong answers on inputs like `"abba"`.
- **Adding `s[right]` before shrinking** — the `while` then sees the character it just added and evicts the whole window.
- **`right - left` without the `+ 1`.** Off-by-one on every measurement; both ends are inclusive.
- **Forgetting to `remove` from the set while advancing `left`** — the set stops matching the window and the invariant breaks.
- **Moving `left` backwards** in the last-index-map variant. Guard it with `max(left, ...)`.
- **Solving for subsequences** because you skimmed the word "substring". The `"pwwkew"` example exists to catch exactly this.

**This same move shows up in:** [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (the same-direction window, simplest form) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (same skeleton, arithmetic validity rule) · [Permutation in String](567-permutation-in-string.md) (a **fixed**-size window) · [Minimum Window Substring](76-minimum-window-substring.md) (the hardest form — minimize instead of maximize).

</details>

---
