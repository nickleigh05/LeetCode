# 680. Valid Palindrome II

**Easy** · [LeetCode](https://leetcode.com/problems/valid-palindrome-ii/) · [Solution file (no hints)](../../problems/0500-0999/680.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given a string `s`, return `true` if it can be a palindrome after deleting **at most one** character.

```
s = "aba"    →  true    (already a palindrome, delete nothing)
s = "abca"   →  true    (delete 'c' → "aba")
s = "abc"    →  false   (no single deletion helps)
```

**Constraints:** `1 <= s.length <= 10⁵` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**palindrome**" | Reads the same forward and backward — the classic converging-pointers check from [Valid Palindrome](125-valid-palindrome.md) |
| "**at most one**" deletion | Zero deletions counts too, so an already-valid palindrome returns `true` |
| "**at most one**", not "exactly one" | You never need to consider two removals — which bounds the whole search |
| `s.length` up to 10⁵ | O(n²) is 10¹⁰ — dead. Trying every deletion and re-checking is **not** affordable |
| lowercase letters only | No case-folding or filtering, unlike [Valid Palindrome](125-valid-palindrome.md) |

Start from the ordinary palindrome check: two pointers at the ends, walking inward while characters match. Now ask what happens at the **first mismatch**.

At that moment you have `s[left] != s[right]`. Everything outside the pointers already matched, so the failure is right here. You get exactly **one** deletion, and it must be spent now — deleting anything else leaves this mismatch unresolved.

And there are only **two** things you could delete:

1. **`s[left]`** — hoping `s[left+1 .. right]` is a palindrome
2. **`s[right]`** — hoping `s[left .. right-1]` is a palindrome

If either works, the answer is `true`. If neither does, no single deletion can save it.

That's the whole algorithm: walk inward until a mismatch, then make **one** branching decision and verify each option with a plain palindrome check. Crucially, you don't recurse — after spending the deletion, the remainder must be a palindrome outright.

🤔 **Before you open the next section:** at the first mismatch, why is it enough to test only those two options — why can't the right character to delete be somewhere else entirely?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every deletion | For each `i`, remove it and test | O(n²) | O(n) per slice | ❌ 10¹⁰ ops, plus a new string each time |
| Reverse-compare | `s == s[::-1]`, then try deletions | O(n²) | O(n) | ❌ Same cost |
| **Two pointers + one branch** | Walk inward; at a mismatch, test both skips | **O(n)** | **O(1)** | ✅ |

**The decision: converging two pointers, with a single two-way branch at the first mismatch.**

The key realization — and this is what makes it O(n) rather than O(n²):

> **You only ever branch once, at the *first* mismatch.**

Everything before that point matched, so no deletion was needed there. Deleting a character from the already-matched region would break a pair that currently works, making things strictly worse. So the deletion must be spent at the first point of failure — and there, only two candidates exist.

After branching, each sub-check is a **plain palindrome test with no deletions remaining**, which is a simple O(n) walk. Two such checks in the worst case, so the total stays linear.

**Why the helper takes indices, not a slice.** Writing `is_palindrome(s[left+1:right+1])` would allocate a new string on every call — O(n) memory and a hidden O(n) copy. Passing `left` and `right` as *bounds* into the original string keeps it O(1) space. Small detail, real difference, and exactly the kind of thing interviewers notice.

**Why `or` is the right connective.** `is_palindrome(left+1, right) or is_palindrome(left, right-1)` — Python short-circuits, so if skipping the left character succeeds, the second check never runs. Free early exit.

**Why not recursion with a deletion counter?** You could write a general "at most k deletions" recursion, and for k = 1 it degenerates to exactly this. But the explicit two-branch version is clearer and avoids stack depth concerns at n = 10⁵. Mention the generalization; write the specific one.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def is_palindrome(left, right):
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

**The helper — a standard palindrome check over a *range* of the string.**

Taking `left` and `right` as parameters (rather than a substring) is the O(1)-space choice: no slicing, no copying. It closes over `s` from the enclosing scope.

This is exactly [Valid Palindrome](125-valid-palindrome.md)'s core loop, restricted to a window.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [while-loop](../syntax/while-loop.md)

```python
left, right = 0, len(s) - 1
```

The usual converging pointers, one at each end.
→ [multiple-return-values](../syntax/multiple-return-values.md)

```python
while left < right:
    if s[left] == s[right]:
        left += 1
        right -= 1
```

Characters match ⇒ this pair is fine ⇒ move both inward. No deletion spent.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
```

**The single branching decision, and the heart of the solution.**

- `is_palindrome(left + 1, right)` — skip the **left** character; is the rest a palindrome?
- `is_palindrome(left, right - 1)` — skip the **right** character; is the rest a palindrome?

`return` immediately, whichever way it goes. The one deletion is now spent, so there's nothing further to explore — either one of these sub-ranges is a clean palindrome or the answer is `false`.

Short-circuiting `or` means the second check is skipped when the first succeeds.
→ [logical-operators](../syntax/logical-operators.md) · [if-return](../syntax/if-return.md)

```python
return True
```

The loop completed with no mismatch ⇒ `s` is already a palindrome ⇒ zero deletions needed, which "at most one" permits.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:

        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        left, right = 0, len(s) - 1

        while left < right:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)

        return True
```

</details>

<details>
<summary>The brute force (also in the solution file)</summary>

```python
### Brute Force ###
class Solution:
    def validPalindrome(self, s: str) -> bool:
        if s == s[::-1]:
            return True
        for i in range(len(s)):
            temp = s[:i] + s[i+1:]
            if temp == temp[::-1]:
                return True
        return False
```

Correct and easy to reason about, but **O(n²)** — n deletions, each building and reversing an O(n) string. At n = 10⁵ that's 10¹⁰ character operations plus enormous allocation churn. Worth naming as your starting point, then improving.

</details>

**Trace it** — `s = "abca"`:

| `left` | `right` | `s[left]` | `s[right]` | Match? | Action |
|---|---|---|---|---|---|
| 0 | 3 | `a` | `a` | ✅ | move both inward |
| 1 | 2 | `b` | `c` | ❌ | **branch** |

Two checks on the mismatch:

| Option | Range | Substring | Palindrome? |
|---|---|---|---|
| Skip left (`b`) | `is_palindrome(2, 2)` | `"c"` | ✅ **true** |
| Skip right (`c`) | not evaluated | — | short-circuited |

Return **`true`** ✅ — deleting `b` leaves `"aca"`, or equivalently the remaining range is trivially a palindrome.

**And a failing case** — `s = "abc"`:

| `left` | `right` | Match? | Action |
|---|---|---|---|
| 0 | 2 | `a` vs `c` ❌ | branch |

| Option | Range | Substring | Palindrome? |
|---|---|---|---|
| Skip left | `is_palindrome(1, 2)` | `"bc"` | ❌ |
| Skip right | `is_palindrome(0, 1)` | `"ab"` | ❌ |

Return **`false`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The main loop walks inward, at most `n/2` iterations.
- On a mismatch, it makes **at most two** helper calls, each an O(n) scan.
- Then it returns — no further branching.

Worst case: `n/2` matching steps, then `2 × O(n)` verification = **O(n)** overall. Constants of ~2, not a higher order.

**The reason it's not O(n²):** the branch happens **exactly once**. A recursive formulation that branched at *every* mismatch would explore 2^k paths for k deletions — but with the budget fixed at one, the recursion depth is one, so it's two flat scans.

That's worth stating explicitly, because "try both options" instinctively sounds exponential. It isn't, because the budget bounds the depth.

**Compare to brute force:** O(n²) — n candidate deletions × O(n) to build and check each. The insight that mismatches can only matter *at the first failure* is what collapses it to linear.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Four integers across the main loop and the helper. **No string slicing anywhere** — that's the deliberate choice, and it's what keeps this constant-space.

The tempting-but-costly alternative:

```python
def is_palindrome(sub):        # ❌ O(n) space per call
    return sub == sub[::-1]
...
return is_palindrome(s[left+1:right+1]) or is_palindrome(s[left:right])
```

Correct, and arguably more readable — but every slice allocates a new string. Since Python strings are [immutable](../syntax/string-immutability.md), there's no way to take a cheap view of a substring the way you might with a slice type in Rust or a `string_view` in C++. Passing indices is the idiomatic workaround.

The brute-force version is worse still: O(n) space **per iteration**, n times over, hammering the allocator.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I start with the standard palindrome check — two pointers converging, moving inward while characters match. Everything that matched needed no deletion, so when I hit the first mismatch, that's where the single deletion has to be spent. There are only two options: skip the left character or skip the right one. I check whether either remaining range is a plain palindrome, with no deletions left, so each check is a simple linear walk. If the main loop finishes without a mismatch, the string was already a palindrome, which 'at most one' allows. O(n) time, O(1) space — I pass indices to the helper rather than slicing, to avoid allocating substrings."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "At most **k** deletions?" | Generalize to recursion with a remaining budget: on a mismatch, recurse both ways with `k-1`. Worst case O(n · 2^k) — or use DP on `(left, right, k)` for O(n²k). |
| "Why only check the first mismatch?" | Everything before it already pairs up. Deleting there would break a working pair, strictly worsening things. |
| "Why not recurse after branching?" | The budget is exhausted, so the remainder must be a palindrome outright — a flat check, not a recursive one. |
| "Return **which** character to delete." | Return `left` or `right` depending on which branch succeeded, or `-1` if already a palindrome. |
| "What if it were 'exactly one' deletion?" | An already-palindromic string of **even** length would become `false`; odd length stays `true` (delete the middle). Worth clarifying with the interviewer. |
| "Handle mixed case and punctuation." | Add the filter/normalize step from [Valid Palindrome](125-valid-palindrome.md), or skip non-alphanumerics as you walk. |
| "Longest palindromic subsequence instead?" | A different problem — 2-D DP, [LeetCode 516](https://leetcode.com/problems/longest-palindromic-subsequence/). |

**Traps:**

- **Slicing inside the helper.** `s[left+1:right+1]` turns O(1) space into O(n) and adds a hidden copy. Pass indices.
- **Continuing the loop after the branch.** You must `return` — the deletion is spent, and the two helper calls are the complete answer.
- **Using `and` instead of `or`.** Either option succeeding is enough; requiring both is far too strict.
- **Off-by-one in the ranges.** Skipping left is `(left+1, right)`; skipping right is `(left, right-1)`. Mixing them up produces subtly wrong answers on asymmetric inputs.
- **Forgetting the already-a-palindrome case.** `"aba"` must return `true` — the final `return True` after the loop handles it.
- **Trying every deletion.** O(n²) and unnecessary; only the first mismatch can matter.

**This same move shows up in:** [Valid Palindrome](125-valid-palindrome.md) (the base case this extends — converging pointers, no deletions) · [Reverse String](344-reverse-string.md) (the same converging-pointer skeleton, swapping instead of comparing) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (converging pointers driven by a condition) · [Is Subsequence](392-is-subsequence.md) (two pointers over two sequences with skips allowed).

</details>

---
