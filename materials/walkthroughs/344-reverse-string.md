# 344. Reverse String

**Easy** · [LeetCode](https://leetcode.com/problems/reverse-string/) · [Solution file (no hints)](../../problems/0001-0499/344.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Write a function that reverses a string. The input is given as an array of characters `s`. You must do this by modifying the input array **in-place** with **O(1) extra memory**.

```
s = ["h","e","l","l","o"]          →  ["o","l","l","e","h"]
s = ["H","a","n","n","a","h"]      →  ["h","a","n","n","a","H"]
```

**Constraints:** `1 <= s.length <= 10⁵` · `s[i]` is a printable ASCII character

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "array of **characters**", not a string | ⚠️ Deliberate. Python strings are [immutable](../syntax/string-immutability.md) and couldn't be reversed in place at all — handing you a list is what makes the exercise possible |
| "**in-place**" | Mutate `s` itself. Return nothing |
| "**O(1) extra memory**" | No building a reversed copy. That rules out `s[::-1]` as a *solution* (though not as a one-liner to mention) |
| `s.length` up to 10⁵ | Needs O(n); anything quadratic is dead |
| printable ASCII | No multi-byte or surrogate-pair complications |

This is the **canonical two-pointer problem** — the one every other two-pointer problem is a variation on. Strip it down and the idea is:

> The first character must end up last, the second must end up second-to-last, and so on. So **swap the pair at the two ends, then step both pointers inward.**

Each swap places **two** characters permanently, so you only need to walk halfway before everything is done.

🤔 **Before you open the next section:** if you swap position 0 with the last, then 1 with second-to-last, when exactly should you stop — and what happens to the middle character of an odd-length string?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Build a reversed copy | `result = s[::-1]`, then assign | O(n) | **O(n)** | ❌ Violates O(1) memory |
| `s.reverse()` | Built-in, in place | O(n) | O(1) | ⚠️ Correct, but it *is* the exercise — don't submit it as your answer |
| Recursion | Swap ends, recurse inward | O(n) | **O(n)** stack | ❌ O(n) call-stack depth; overflows at 10⁵ |
| **Two pointers** | Swap from both ends, converge | **O(n)** | **O(1)** | ✅ |

**The decision: two pointers converging from the ends.**

- `left` starts at index 0, `right` at `len(s) - 1`
- Swap them, then `left += 1` and `right -= 1`
- Stop when they meet or cross

**Why halfway is enough:** each iteration places two characters in their final positions. After `n/2` swaps, all `n` are done. Running the loop the *full* length would swap every pair twice — undoing your own work and returning the original string. That's the classic bug here, and it's worth understanding rather than just avoiding.

**Odd lengths need no special case.** With `n = 5`, the pointers meet exactly at index 2 — the middle character, which is already in its correct position and needs no swap. Whether your loop condition is `left < right` or `left <= right`, that element ends up correct (in the `<=` case it's harmlessly swapped with itself).

**Why not recursion?** It's elegant and it's O(1) *auxiliary data*, but each call frame is real memory — O(n) stack depth, and Python's default recursion limit (~1000) means 10⁵ characters blows up. See [recursion-limit](../syntax/recursion-limit.md).

**Why not `s.reverse()`?** In production, absolutely use it. In an interview, the question is testing whether you can implement the mechanism — reaching for the built-in dodges the point. Mention it in one sentence, then write the loop.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(s) - 1
```

The two ends. `len(s) - 1` because indices stop one short of the length.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
```

Converge until they meet. `<=` includes the moment `left == right` (the middle of an odd-length string), where the swap is a harmless self-assignment.

`left < right` is equally correct and skips that no-op — both are fine, and knowing *why* both work is more valuable than picking one.
→ [while-loop](../syntax/while-loop.md)

```python
    s[left], s[right] = s[right], s[left]
```

**The swap, in one line.** Python evaluates the entire right-hand side into a tuple *first*, then unpacks it into the targets — so no temporary variable is needed and there's no risk of clobbering.

In a language without tuple assignment you'd need the three-line dance:
```python
tmp = s[left]; s[left] = s[right]; s[right] = tmp
```
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    left += 1
    right -= 1
```

Step inward from both sides. **Both must move** — advancing only one turns the loop into an infinite one (or a wrong answer).

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        left = 0
        right = len(s) - 1

        while left <= right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1


"""
### these also work but violates the problems restraint ###
s.reverse()
s[:] = s[::-1]
"""
```

</details>

**Trace it** — `s = ["h","e","l","l","o"]`:

| `left` | `right` | Swap | `s` after |
|---|---|---|---|
| 0 | 4 | `h` ↔ `o` | `["o","e","l","l","h"]` |
| 1 | 3 | `e` ↔ `l` | `["o","l","l","e","h"]` |
| 2 | 2 | `l` ↔ `l` (self) | unchanged |
| 3 | 1 | `left > right` → stop | — |

Result `["o","l","l","e","h"]` ✅ — three iterations for five characters, exactly `⌈n/2⌉`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

The loop runs `⌈n/2⌉` times, each doing one O(1) swap. That's `n/2` operations — and constants drop, so **O(n)**.

Worth saying precisely: it's O(n) *despite* only touching each index once across `n/2` iterations, because each iteration does work proportional to 2 elements. You can't beat linear — every character has to move.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two integer pointers. The tuple swap creates a transient 2-element tuple, which is constant-size regardless of `n`.

This is the constraint the problem exists to enforce. The tempting alternatives all fail it:

| | Space |
|---|---|
| `s[::-1]` into a new list | O(n) |
| Recursion | O(n) stack |
| **Two pointers** | **O(1)** ✅ |

Note `s[:] = s[::-1]` *does* mutate in place, but it builds the reversed copy first — so it's O(n) memory for an instant, and fails the brief on a technicality that interviewers do care about.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two pointers from both ends: swap `s[left]` and `s[right]`, then move both inward. Each swap finalizes two characters, so I only need to go halfway — `n/2` iterations. An odd-length string leaves the middle character in place, which is already correct, so no special case. O(n) time, O(1) space. `s.reverse()` or `s[::-1]` would work, but the first is the exercise and the second allocates a copy."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Reverse only the **vowels**." | [LeetCode 345](https://leetcode.com/problems/reverse-vowels-of-a-string/) — same two pointers, but advance each one until it lands on a vowel before swapping. |
| "Reverse each **word** in place." | Reverse the whole array, then reverse each word-span individually. The classic two-pass rotation trick. |
| "Reverse only the first `k`?" | [LeetCode 541](https://leetcode.com/problems/reverse-string-ii/) — same swap loop, applied to slices in a stride. |
| "Why not recursion?" | O(n) stack depth; Python's limit is ~1000, and `n` can be 10⁵. |
| "What if it were a real Python `str`?" | Impossible in place — strings are immutable. You'd have to return `s[::-1]`, which is O(n) space by necessity. |
| "Does it work on Unicode?" | Code-point reversal works, but combining characters and emoji with ZWJ sequences would be visually mangled. Grapheme-cluster-aware reversal is a different problem. |
| "Reverse a linked list instead." | [Reverse Linked List](206-reverse-linked-list.md) — no random access, so it's a pointer-rewiring walk, not a swap. |

**Traps:**

- **Looping the full length** instead of halfway. Every pair gets swapped twice and you get the original string back. Passes nothing, looks correct.
- **Advancing only one pointer.** Infinite loop, or a garbled result.
- **`s = s[::-1]`.** Rebinds the local name; the caller's list is untouched. The judge sees nothing changed.
- **Returning the array.** The signature returns `None` — mutate, don't return.
- **Off-by-one on `right`.** It's `len(s) - 1`, not `len(s)` — the latter is an immediate `IndexError`.

**This same move shows up in:** [Valid Palindrome](125-valid-palindrome.md) (converging pointers, comparing instead of swapping) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (converging pointers driven by a sum condition) · [Container With Most Water](11-container-with-most-water.md) (converging pointers driven by a greedy choice) · [Reverse Linked List](206-reverse-linked-list.md) (the same goal without random access).

</details>

---
