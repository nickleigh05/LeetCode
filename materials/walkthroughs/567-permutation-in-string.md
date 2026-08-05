# 567. Permutation in String

**Medium** · [LeetCode](https://leetcode.com/problems/permutation-in-string/) · [Solution file (no hints)](../../problems/0500-0999/567.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given two strings `s1` and `s2`, return `true` if `s2` contains a **permutation** of `s1` — in other words, if one of `s1`'s permutations appears as a **contiguous substring** of `s2`.

```
s1 = "ab", s2 = "eidbaooo"   →  true    ("ba" is a permutation of "ab")
s1 = "ab", s2 = "eidboaoo"   →  false   ("bo","oa","ao"… none work)
```

**Constraints:** `1 <= s1.length, s2.length <= 10⁴` · both consist of **lowercase English letters**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "a **permutation** of `s1`" | Same letters, same counts, any order — which is exactly [Valid Anagram](242-valid-anagram.md)'s definition |
| "**contiguous substring**" | A window over `s2`. Not a subsequence |
| a permutation has the **same length** | ⚠️ **The window is a fixed size**: `len(s1)`. It never grows or shrinks |
| "return `true`/`false`" | Existence only. Return on the first hit |
| lengths up to 10⁴ | O(n·m) = 10⁸ is borderline; **O(n)** is comfortable |
| "**lowercase** English letters" | 26-letter alphabet → a fixed 26-slot array works, and it's O(1) space |

Two ideas combine, and both are already in your toolkit:

1. **"Is this window a permutation of `s1`?"** is an anagram check — compare letter counts, exactly as in [Valid Anagram](242-valid-anagram.md).
2. **Every window has the same length**, so this is a *fixed*-size window. That's simpler than problems 3 and 424: there's no validity rule deciding when to shrink, because the window slides at a constant width.

The efficiency question: comparing counts from scratch at every position costs O(26) per window — fine, but you can do better. When the window slides one step right, only **two** letters change: one enters on the right, one leaves on the left. So the count array can be **updated in O(1)** rather than rebuilt.

🤔 **Before you open the next section:** when a fixed-size window slides one position, how many entries of its letter-count array actually change — and what does that let you avoid doing?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Generate permutations | Build all permutations of `s1`, search for each | O(m! · n) | ❌ Absurd — 10! is already 3.6 million |
| Check every window from scratch | Sort or count each window of length m | O(n·m log m) | ❌ Rebuilds work it could reuse |
| Count each window fresh | Build a 26-array per window, compare | O(26n) | ⚠️ Correct, and technically O(n) — but wasteful |
| **Fixed window, incremental counts** | Update 2 entries per slide, compare | **O(n)** | ✅ |

**The decision: a fixed-size sliding window with two 26-slot count arrays, updated incrementally.**

Build `s1_count` once. Build `window` for the first `len(s1)` characters of `s2`. Then slide: each step **adds** the incoming character and **removes** the outgoing one, then compares.

**Why arrays rather than dicts here?** The alphabet is exactly 26 lowercase letters, so `ord(ch) - ord("a")` maps each letter to a slot 0–25 directly. That gives:

- **O(1) comparison of two windows** — Python's `==` on two fixed-length lists is a 26-element check, a constant.
- No hashing overhead, and no `KeyError` edge cases.
- Automatic handling of "the window has a letter `s1` doesn't" — that slot simply differs.

A dict works too, but has one nasty wrinkle: a count that drops to **0** stays in the dict as `{'a': 0}`, which is `!=` a dict without that key. You'd have to `del` zero entries to make `==` behave. **The array sidesteps that entirely** — a real reason to prefer it when the alphabet is small and fixed.

**Why this is the easiest window in the unit.** Problems 3 and 424 needed a `while` loop to shrink until valid. Here the window is always exactly `len(s1)` wide, so each step is one add, one remove, one compare. No shrink logic at all.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(s1) > len(s2):
    return False
```

Guard first. If `s1` is longer, no window of that size exists in `s2` — and without this the slicing below would silently produce a short window and compare it wrongly.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
s1_count = [0] * 26
window = [0] * 26
```

Two fixed 26-slot tallies: the target, and the current window. `[0] * 26` is safe here — integers are immutable, so there's no shared-reference trap like `[[]] * n`.
→ [list-basics](../syntax/list-basics.md)

```python
for ch in s1:
    s1_count[ord(ch) - ord("a")] += 1
```

Tally the target once. `ord(ch) - ord("a")` maps `'a'`→0, `'b'`→1, … `'z'`→25 — turning a character into an array index.
→ [ord-chr](../syntax/ord-chr.md) · [for-loop](../syntax/for-loop.md)

```python
for ch in s2[:len(s1)]:
    window[ord(ch) - ord("a")] += 1
```

Prime the **first** window: the opening `len(s1)` characters of `s2`. The slice is exclusive at the end, so it takes exactly that many.
→ [list-slicing](../syntax/list-slicing.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
if s1_count == window:
    return True
```

Check the first window before sliding — the loop below starts *after* it, so without this you'd never test position 0.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
for right in range(len(s1), len(s2)):
```

Slide. `right` is the index of the character **entering** the window, starting just past the initial one.
→ [range-function](../syntax/range-function.md)

```python
    window[ord(s2[right]) - ord("a")] += 1
    window[ord(s2[right - len(s1)]) - ord("a")] -= 1
```

**The O(1) slide** — the heart of the solution. One character enters at `right`; one leaves at `right - len(s1)`, which is the position that just fell off the left edge.

Work through the index: with `len(s1) = 3` and `right = 5`, the new window covers indices 3, 4, 5 — so index `5 - 3 = 2` is the one departing. ✅

Two array updates, no rebuilding.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if s1_count == window:
        return True
```

Identical counts ⇒ this window is a permutation of `s1`. Return immediately.

```python
return False
```

Every window checked, none matched.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1_count = [0] * 26
        window = [0] * 26

        for ch in s1:
            s1_count[ord(ch) - ord("a")] += 1

        for ch in s2[:len(s1)]:
            window[ord(ch) - ord("a")] += 1

        if s1_count == window:
            return True

        for right in range(len(s1), len(s2)):
            window[ord(s2[right]) - ord("a")] += 1
            window[ord(s2[right - len(s1)]) - ord("a")] -= 1

            if s1_count == window:
                return True

        return False
```

</details>

**Trace it** — `s1 = "ab"`, `s2 = "eidbaooo"` (window size 2):

| Window | Contents | Counts vs `{a:1, b:1}` | Match? |
|---|---|---|---|
| `[0,1]` | `ei` | e:1, i:1 | no |
| `[1,2]` | `id` | i:1, d:1 | no |
| `[2,3]` | `db` | d:1, b:1 | no |
| `[3,4]` | `ba` | **a:1, b:1** | ✅ `return True` |

At the third slide: `b` enters at index 4… actually `a` enters at index 4 and `d` leaves at index `4 - 2 = 2`. Window becomes `"ba"` — a permutation of `"ab"`. ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n = `len(s2)`. Precisely: **O(m + 26n)** with m = `len(s1)`, which is O(n + m).

| Step | Cost |
|---|---|
| Build `s1_count` | O(m) |
| Build the first window | O(m) |
| Slide across `s2` | n − m iterations |
| Per slide: two array updates | O(1) |
| Per slide: `s1_count == window` | **O(26) = O(1)** |

The comparison is the part people mis-analyse. Comparing two lists is O(length), but the length is **fixed at 26** — it doesn't grow with the input, so it's a constant. Total: **O(n + m)**.

**Why incremental updates matter:** rebuilding the window's counts from scratch each step would be O(m) per window, giving O(n·m) — up to 10⁸ here. Recognizing that only two counts change per slide is what keeps it linear. That's the defining trick of **fixed-size** window problems.

**Early exit:** returns on the first match, so a hit near the start costs almost nothing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Two arrays of exactly 26 integers — 52 slots, always, regardless of input size. Plus a couple of loop variables.

Justify it as before: *"O(1), bounded by the 26-letter lowercase alphabet."*

**One thing to watch:** `s2[:len(s1)]` creates a temporary string of length m, so strictly there's an O(m) transient. Iterating with `range(len(s1))` and indexing `s2[i]` avoids even that. Not worth mentioning unless asked — but if an interviewer is being precise about auxiliary space, it's the honest detail.

**The array-vs-dict decision costs nothing here:** a dict would be O(26) too — but as noted in section 2, it brings the zero-count comparison wrinkle. When the alphabet is small and fixed, the array is both simpler and faster.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A permutation of `s1` has the same length and the same letter counts, so I'm looking for a **fixed**-size window over `s2` whose counts match `s1`'s. I'll build a 26-slot count array for `s1` and for the first window, then slide. The key efficiency point is that sliding one position changes only two counts — one letter enters, one leaves — so each step is O(1) instead of rebuilding the window. Comparing two 26-element arrays is also a constant. That gives O(n) time and O(1) space. I'm using arrays rather than dicts because the alphabet is fixed, and it avoids the dict wrinkle where a zero count still counts as a key."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Find **all** starting indices, not just existence." | Don't return early — append `right - len(s1) + 1` to a result list. That's LeetCode 438, Find All Anagrams. |
| "Avoid comparing 26 entries each slide." | Maintain a `matches` counter of how many of the 26 slots currently agree. Update it only for the two changed letters, and check `matches == 26`. Makes each step truly O(1). |
| "What if the alphabet were Unicode?" | Swap arrays for dicts — but then remember to `del` keys that hit zero, or `==` will misfire. |
| "What if you needed a *subsequence* instead?" | Different problem — a greedy two-pointer scan, no window at all. |
| "Why is the window a fixed size here but variable in problem 3?" | Because a permutation's length is pinned to `len(s1)`. When the target size is known up front, you get a fixed window; when you're maximizing or minimizing a range, it's variable. |
| "Could you sort each window instead?" | O(m log m) per window → O(n·m log m). Correct, much slower. |

**Traps:**

- **Forgetting to check the initial window.** The slide loop starts at `len(s1)`, so position 0 is never tested otherwise — and `s1 = "ab", s2 = "ab"` would return `False`.
- **The wrong departing index.** It's `right - len(s1)`, not `right - len(s1) + 1` or `left`. Verify it on a concrete example.
- **Omitting the length guard.** `s1` longer than `s2` then slices a short window and compares garbage.
- **Using dicts without deleting zero counts.** `{'a': 1, 'b': 0} != {'a': 1}` — a silent false negative.
- **Rebuilding the window each step.** Correct but O(n·m); you've missed the point of the pattern.
- **Generating permutations.** Factorial. Never.

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (the count-comparison this is built on) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (variable window with a count map) · [Minimum Window Substring](76-minimum-window-substring.md) (the variable-size, minimizing counterpart) · [Sliding Window Maximum](239-sliding-window-maximum.md) (another fixed-size window with incremental maintenance).

</details>

---
