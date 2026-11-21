# 383. Ransom Note

**Easy** · [LeetCode](https://leetcode.com/problems/ransom-note/) · [Solution file (no hints)](../../problems/0001-0499/383.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given two strings `ransomNote` and `magazine`, return `True` if `ransomNote` can be built from the letters in `magazine`, and `False` otherwise. **Each letter in `magazine` can be used only once.**

```
ransomNote = "a",   magazine = "b"    →  False
ransomNote = "aa",  magazine = "ab"   →  False    (only one 'a' to cut out)
ransomNote = "aa",  magazine = "aab"  →  True
```

**Constraints:** `1 <= ransomNote.length, magazine.length <= 10⁵` · both strings contain **lowercase English letters only**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**built from** the letters" | Order doesn't matter. You're cutting letters out of a magazine, not matching a substring |
| "**used only once**" | It's about **counts**, not just presence. Two `'a'`s in the note need two `'a'`s in the magazine |
| **lowercase English letters only** | There are exactly 26 possible characters, so a fixed array of 26 counters can replace a hash map |
| lengths up to 10⁵ | You need O(n). Rescanning the magazine for every note letter would be O(n·m) |

**The reframe:** for every letter, *need ≤ have*. That's a frequency-comparison problem, the same family as [Valid Anagram](242-valid-anagram.md). The difference is that an anagram needs the counts to be **equal**, while here you only need the magazine's counts to **cover** the note's.

**A cheap early exit:** if the note is longer than the magazine, there aren't enough letters in total, so the answer is `False` before you count anything.

🤔 **Before you open the next section:** if you count the magazine's letters first, what should happen to a counter each time the note uses that letter, and what value tells you you've run out?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Remove-as-you-go | For each note letter, find and delete it from a list of magazine letters | O(n·m) | O(m) | ❌ Linear search per letter |
| Sort both | Sort, then walk two pointers | O(m log m) | O(m) | ⚠️ Works, slower than needed |
| Two hash maps, compare | Count both, then check `note[c] <= mag[c]` for each `c` | O(n + m) | O(1)* | ✅ Fine |
| **One count array, decrement** | Count the magazine, then *spend* counts on the note | **O(n + m)** | **O(1)** | ✅ Simplest |

\* At most 26 keys either way.

**The decision: one [array](../data-structures/array.md) of 26 counters.**

Count what the magazine has, then walk the note and **spend** one count per letter. The first time a counter drops below zero, the note needed a letter the magazine didn't have enough of, so return `False` straight away.

**Why an array instead of a dict?** The alphabet is fixed at 26 lowercase letters, so `ord(char) - ord('a')` maps each letter to an index 0–25. That gives you a direct slot with no hashing. A [hash map](../data-structures/hashmap.md) (or a `Counter`) would also be completely correct; the array is just the tighter fit when the key space is small and known.

**Why the single-array "spend" pattern beats two maps:** you check as you go, so you can bail out on the first shortfall instead of building the note's full count and comparing afterwards.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(ransomNote) > len(magazine):
    return False
```

**The early exit.** If the note needs more letters than the magazine contains in total, no arrangement can work. It's O(1), and it skips all the counting on the obvious failures.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
counts = [0] * 26
```

One counter per lowercase letter, all starting at zero. Index 0 is `'a'`, index 25 is `'z'`.
→ [list-basics](../syntax/list-basics.md)

```python
for char in magazine:
    counts[ord(char) - ord('a')] += 1
```

**Stock the shelf.** `ord` gives a character's code point, and subtracting `ord('a')` shifts `'a'..'z'` down to `0..25`. After this loop, `counts[i]` is how many copies of that letter the magazine offers.
→ [ord-chr](../syntax/ord-chr.md) · [for-loop](../syntax/for-loop.md)

```python
for char in ransomNote:
    counts[ord(char) - ord('a')] -= 1
    if counts[ord(char) - ord('a')] < 0:
        return False
```

**Spend the letters.** Each note letter uses one copy. If a counter goes **negative**, the note has now asked for more of that letter than the magazine had, so return `False` immediately. There's no need to look at the rest of the note.

Check `< 0`, not `== 0`. Reaching zero just means you used the last copy, which is fine.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
return True
```

The note's letters ran out before any counter went negative, so every letter was covered.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        counts = [0] * 26

        for char in magazine:
            counts[ord(char) - ord('a')] += 1

        for char in ransomNote:
            counts[ord(char) - ord('a')] -= 1
            if counts[ord(char) - ord('a')] < 0:
                return False

        return True
```

</details>

**Trace it.** `ransomNote = "aab"`, `magazine = "baa"` (showing only the letters that matter):

| Step | char | `a` | `b` | Note |
|---|---|---|---|---|
| after magazine | — | 2 | 1 | stocked |
| note 1 | `a` | 1 | 1 | |
| note 2 | `a` | 0 | 1 | last `a` used, still fine |
| note 3 | `b` | 0 | 0 | |
| end | — | | | nothing went negative → **True** ✅ |

**And the failing case.** `ransomNote = "aa"`, `magazine = "ab"`: after stocking, `a = 1`. The first `a` brings it to 0, and the second brings it to **−1**, so the function returns **False** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, where `m = len(magazine)` and `n = len(ransomNote)`.

One pass over the magazine to count, and at most one pass over the note to spend. Each step is an O(1) array index.

The early exit makes the common failure case even cheaper. If the note is longer, the function returns in O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** The `counts` array is always exactly 26 slots, however long the strings are.

That's the payoff for using a fixed array. A dict or `Counter` would also be O(1) here, because there are at most 26 distinct keys, but the array makes it obvious.

**If the alphabet weren't fixed** (say, any Unicode character), the bound becomes O(k) for k distinct characters, and you'd switch to a dict.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Order doesn't matter, only how many of each letter, so this is a frequency problem. If the note's longer than the magazine I can return False straight away. Otherwise I count the magazine's letters in a 26-slot array, then walk the note and decrement. The first time a count goes negative, the magazine is short of that letter, so I return False. If I finish the note, return True. O(n + m) time, O(1) space since the array is fixed at 26."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the input can be any Unicode?" | Swap the array for a dict or `collections.Counter`. Same algorithm, O(k) space. |
| "Can you do it in one line?" | `return not (Counter(ransomNote) - Counter(magazine))`. Counter subtraction drops non-positive counts, so an empty result means everything was covered. Know it, but explain the loop version. |
| "How is this different from Valid Anagram?" | Anagram needs counts **equal**. This needs magazine counts **≥** note counts. |
| "Magazine is huge and reused for many notes?" | Count the magazine once, then check each note against a copy of the counts. |

**Traps:**

- **Checking presence instead of counts.** `all(c in magazine for c in ransomNote)` passes `"aa"` vs `"ab"`, which is wrong.
- **Testing `== 0` instead of `< 0`.** Hitting zero means you used the last copy, which is still valid.
- **Comparing two full count maps for equality.** That's the anagram check, and it fails whenever the magazine has spare letters.
- **Using `str.replace` or `list.remove` in a loop.** Correct, but O(n·m).

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (equal counts rather than covering counts) · [Group Anagrams](49-group-anagrams.md) (a 26-slot count as a hash key) · [Permutation in String](567-permutation-in-string.md) (the same count array, sliding) · [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md) (counts compared across a window).

</details>

---
