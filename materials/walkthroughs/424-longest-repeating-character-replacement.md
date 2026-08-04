# 424. Longest Repeating Character Replacement

**Medium** · [LeetCode](https://leetcode.com/problems/longest-repeating-character-replacement/) · [Solution file (no hints)](../../problems/0001-0499/424.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

You're given a string `s` and an integer `k`. You may choose **any** character in the string and change it to any other uppercase English character, and you may do this **at most `k` times**.

Return the length of the longest substring containing the **same letter** you can obtain after these changes.

```
s = "ABAB",   k = 2  →  4     (change both A's to B, or both B's to A)
s = "AABABBA", k = 1  →  4     ("AABA" → change the B → "AAAA")
```

**Constraints:** `1 <= s.length <= 10⁵` · `s` consists of **uppercase English letters** · `0 <= k <= s.length`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**substring** … same letter" | Contiguous range, all one character after edits → a **sliding window** |
| "at most **k** times" | A budget. The window is valid while the required edits fit inside it |
| "change it to **any** other character" | You never have to decide *which* letter to convert to — the best choice is always the one already most common in the window |
| "**longest**" | Maximize the window. Track a running best |
| n up to 10⁵ | Need **O(n)** |
| "**uppercase** English letters" | Alphabet fixed at **26** — so a count map is O(1) space |

The whole problem reduces to one formula. Take any window of length `L`, and let `max_count` be the frequency of its most common character. Keep those, change everything else:

```
replacements needed = L - max_count
```

So the window is **valid** exactly when:

```
(right - left + 1) - max_count <= k
```

That's it. The rest is the standard window skeleton from [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) — grow right, shrink left while invalid, measure. Only the *validity predicate* changed.

Why keeping the most frequent character is optimal: you must convert everything that isn't your target letter, so choosing the letter with the highest count minimizes the conversions. No search required — it's forced.

🤔 **Before you open the next section:** you need `max_count` for the current window. Recomputing it by scanning the 26 counts every step works — but is it even necessary to *decrease* it when the window shrinks? Think about what `longest` actually records.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | Every substring, count, check the budget | O(n³) | ❌ |
| Window, recompute `max_count` each step | Scan all 26 counts per iteration | O(26n) | ⚠️ Correct, and honestly fine — 26 is a constant |
| Window per target letter | 26 passes, one per possible target character | O(26n) | ⚠️ Also correct; more code |
| **Window with a never-decreasing `max_count`** | Track the historical maximum only | **O(n)** | ✅ |

**The decision: a sliding window with a [hash map](../data-structures/hashmap.md) of character counts, plus a `max_count` that only ever increases.**

The window skeleton is identical to problem 3. The one genuinely surprising piece:

**Why `max_count` is never decremented when the window shrinks.**

This looks like a bug. If the window shrinks and the most frequent character leaves, `max_count` becomes stale — too large. The window might then be reported valid when it isn't.

It's fine, and here's why. `max_count` records the **largest frequency ever seen in any window so far**, and `longest` records the best window length found so far. A stale (too large) `max_count` can only make the window look *more* valid than it is, so `left` doesn't advance — the window stays wide and drifts along.

But a stale `max_count` can never cause a **wrong answer**, because the window can only grow beyond `longest` if the true `max_count` genuinely increases. To beat the current best you need a genuinely better window, and that requires a real increase in some character's count — at which point `max_count` updates honestly.

So the window size never *shrinks* below the best found, and it only *expands* on legitimate improvements. The intermediate windows may be invalid, but they're never recorded as the answer.

**If that argument makes you nervous** — recompute `max_count` as `max(count.values())` each iteration. It's O(26) = O(1), so the complexity is unchanged, and it's obviously correct. Many strong candidates write it that way deliberately. Know both; know *why* the fast one works.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count = {}
left = 0
max_count = 0
longest = 0
```

`count` holds the frequencies of characters currently in the window. `max_count` is the highest frequency seen so far (never decreased — see section 2). `longest` is the running answer.
→ [dict-basics](../syntax/dict-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for right in range(len(s)):
    count[s[right]] = count.get(s[right], 0) + 1
```

Extend the window and tally the incoming character. Same `.get(char, 0)` counting idiom as [Valid Anagram](242-valid-anagram.md), avoiding a `KeyError` on first sight.
→ [for-loop](../syntax/for-loop.md) · [dict-methods](../syntax/dict-methods.md) · [range-function](../syntax/range-function.md)

```python
    max_count = max(max_count, count[s[right]])
```

Only the character just added can have raised the maximum, so a single comparison suffices — no scan of all 26 counts needed.
→ [min-max-key](../syntax/min-max-key.md)

```python
    while (right - left + 1) - max_count > k:
        count[s[left]] -= 1
        left += 1
```

**The validity check and the shrink.** `(right - left + 1)` is the window length, minus `max_count` gives the characters that would need replacing. If that exceeds the budget `k`, the window is invalid — evict from the left.

Decrement the departing character's count and advance `left`, keeping `count` in sync with the window.
→ [while-loop](../syntax/while-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    longest = max(longest, right - left + 1)
```

Measure after the shrink. The `+ 1` again because both ends are inclusive.

```python
return longest
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:

        count = {}
        left = 0
        max_count = 0
        longest = 0

        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            max_count = max(max_count, count[s[right]])

            while (right - left + 1) - max_count > k:
                count[s[left]] -= 1
                left += 1

            longest = max(longest, right - left + 1)

        return longest
```

</details>

**Trace it** — `s = "AABABBA"`, `k = 1`:

| `right` | char | `count` | `max_count` | Length | Needed | > k? | `left` | `longest` |
|---|---|---|---|---|---|---|---|---|
| 0 | A | A:1 | 1 | 1 | 0 | no | 0 | 1 |
| 1 | A | A:2 | 2 | 2 | 0 | no | 0 | 2 |
| 2 | B | A:2 B:1 | 2 | 3 | 1 | no | 0 | 3 |
| 3 | A | A:3 B:1 | 3 | **4** | 1 | no | 0 | **4** |
| 4 | B | A:3 B:2 | 3 | 5 | 2 | **yes** → evict `A` | 1 | 4 |
| 5 | B | A:2 B:3 | 3 | 5 | 2 | **yes** → evict `A` | 2 | 4 |
| 6 | A | A:2 B:3 | 3 | 5 | 2 | **yes** → evict `B` | 3 | 4 |

Answer: **4** — the window `"AABA"`, converting the single `B`.

Watch rows 4–6: the window length holds steady at 4–5 and never grows, because `max_count` never rises. That's the mechanism from section 2 in action — the window drifts rightward at a fixed size, hunting for a genuine improvement.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The `for` loop runs n times, doing O(1) work per iteration (one dict update, one `max`).
- The inner `while` advances `left`, which starts at 0, only increases, and never passes `right` — so it advances at most n times **across the entire run**.

Every character enters the window once and leaves at most once → **O(n)** total.

**The recompute variant** — `max(count.values())` each iteration — is O(26) per step, so O(26n) = **O(n)** as well. The alphabet bound makes it a constant factor, not a complexity change. Choose based on which you can explain confidently, not on speed.

Same amortized argument as every window problem: *each pointer moves forward only, each element enters and leaves at most once.*

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

The count map holds at most **26 entries** — one per uppercase English letter — regardless of whether n is 10 or 100,000. Fixed ceiling, no dependence on input size. Plus a handful of integers.

**Justify it, don't just assert it:** "O(1), bounded by the 26-letter uppercase alphabet." A bare "O(1)" reads as a guess.

**Contrast with the previous two problems** — this is the third different space answer for essentially the same window skeleton, and the alphabet constraint is what decides each one:

| Problem | Alphabet | Space |
|---|---|---|
| [Longest Substring w/o Repeating](3-longest-substring-without-repeating-characters.md) | letters, digits, symbols, spaces | **O(min(n, m))** |
| [Valid Anagram](242-valid-anagram.md) | lowercase only | **O(1)** — 26 |
| **This problem** | uppercase only | **O(1)** — 26 |

**Always read the alphabet constraint before claiming your space bound.** It's the single input detail that changes the answer here.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "For any window, the cheapest way to make it uniform is to keep whichever character is most frequent and replace the rest — so the replacements needed are `window length − max_count`, and the window is valid while that's at most k. That's a sliding window with a count map: grow right, shrink left while the window is invalid, measure. I track `max_count` incrementally, and I don't decrease it when the window shrinks — a stale max can only make the window look valid and drift along, but it can never *grow* past my current best without a genuine increase in some character's count, so the answer stays correct. O(n) time, O(1) space for the 26-letter alphabet."

**The `max_count` argument is the whole interview here.** Expect to be challenged on it — see the first follow-up.

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Isn't a stale `max_count` a bug?" | **The question.** It can make an invalid window look valid, so the window drifts at a fixed size — but beating `longest` requires a real increase in some count, which updates `max_count` honestly. Intermediate windows are never recorded. |
| "Show me the obviously-correct version." | Recompute `max(count.values())` each iteration. O(26) = O(1) per step, same overall complexity, no subtle argument needed. |
| "What if the alphabet were arbitrary?" | The map grows to O(m). Recomputing the max becomes O(m) per step — at that point track it with a max-heap or accept O(nm). |
| "Return the substring, not the length." | Record the start index whenever you update `longest`. |
| "k = 0?" | Reduces to the longest run of a single repeated character. The same code handles it. |
| "At most k distinct characters instead?" | Different predicate, same skeleton: shrink while `len(count) > k`. LeetCode 340. |
| "Longest with at most k *zeros* flipped?" | The binary version — Max Consecutive Ones III, LeetCode 1004. Identical structure. |

**Traps:**

- **Decrementing `max_count`** when the window shrinks. Not wrong in outcome, but it makes the window shrink more than necessary and it means you haven't understood the invariant. If you're going to maintain it exactly, recompute it instead.
- **Recomputing `max_count` from the wrong thing** — it's `max(count.values())`, not `max(count.keys())`.
- **`right - left` without `+ 1`.** Off-by-one on every window measurement.
- **`if` instead of `while`** for the shrink — one eviction may not restore validity.
- **Forgetting to decrement `count[s[left]]`** when advancing `left`, which desynchronizes the map from the window.
- **Trying each of the 26 target letters** in separate passes. Correct, but you've missed that the best target is forced.

**This same move shows up in:** [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (the same skeleton, set-based validity) · [Permutation in String](567-permutation-in-string.md) (fixed-size window, count comparison) · [Minimum Window Substring](76-minimum-window-substring.md) (the same count-map machinery, minimizing instead) · [Valid Anagram](242-valid-anagram.md) (the counting idiom this relies on).

</details>
