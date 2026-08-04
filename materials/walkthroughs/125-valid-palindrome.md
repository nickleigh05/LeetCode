# 125. Valid Palindrome

**Easy** · [LeetCode](https://leetcode.com/problems/valid-palindrome/) · [Solution file (no hints)](../../problems/0001-0499/125.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

A phrase is a **palindrome** if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forwards and backwards.

Given a string `s`, return `true` if it is a palindrome.

```
"A man, a plan, a canal: Panama"  →  true    ("amanaplanacanalpanama")
"race a car"                      →  false   ("raceacar")
" "                               →  true    ("" — an empty string is a palindrome)
```

**Constraints:** `1 <= s.length <= 2·10⁵` · `s` consists of printable ASCII

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "reads the same **forwards and backwards**" | You're comparing position `i` from the front against position `i` from the **back**. Two ends, moving inward |
| "**removing** non-alphanumeric" | Junk characters aren't data — they must be *skipped*, not compared |
| "converting to **lowercase**" | Comparisons are case-insensitive. Normalize at the moment of comparison |
| `" "` → `true` | ⚠️ After cleaning, the string can be **empty** — and empty counts as a palindrome. Don't crash, don't return false |
| n up to 2·10⁵ | O(n) is expected. Comfortable, but don't do anything quadratic |
| "printable ASCII" | Spaces, punctuation, digits all appear. Digits *are* alphanumeric and **do** count |

The shape of a palindrome check is inherently symmetric: first vs. last, second vs. second-to-last, converging on the middle. That symmetry is what makes **two pointers** the natural fit — one cursor at each end, walking toward each other.

The only complication is the junk. Rather than building a cleaned copy of the string first, you can skip junk *in place* as each pointer moves.

🤔 **Before you open the next section:** you could clean the string first and then compare it to its reverse. What does that cost you that walking two pointers doesn't?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Extra space | Verdict |
|---|---|---|---|---|
| Clean, then reverse | Build a filtered lowercase string, check `t == t[::-1]` | O(n) | **O(n)** | ⚠️ Correct and very readable — but allocates two extra strings |
| Clean, then two pointers | Filter into a new string, then converge on it | O(n) | O(n) | ⚠️ Same allocation, more code |
| **Two pointers in place** | Converge on the original, skipping junk as you go | O(n) | **O(1)** | ✅ |

**The decision: two pointers walking inward on the original string.**

`left` starts at 0, `right` at the last index. Each step: advance past any junk, compare the two characters case-insensitively, then step both inward. Stop when they meet.

**Why not clean-then-reverse?** `"".join(c.lower() for c in s if c.isalnum()) == ...[::-1]` is genuinely good Python and worth saying out loud. But it builds a full copy of the string *and* a reversed copy — O(n) extra memory to answer a yes/no question. The two-pointer version needs **two integers**.

There's also an early-exit difference that doesn't show in the complexity: two pointers can return `False` on the very first mismatch, while clean-then-reverse always processes the entire string before it can compare anything. On `"a...........b"` that's the difference between 2 character reads and 2n.

**The general move:** *comparing a sequence against itself from both ends* is the signature of the two-pointer pattern — see the [Two Pointers lesson](../learning/02-two-pointers.md). Whenever the work is symmetric around a centre, converging pointers beat building a copy.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(s) - 1
```

The two cursors, at the extreme ends. `len(s) - 1` because indices stop one short of the length.
→ [variables-assignment](../syntax/variables-assignment.md) · [string-basics](../syntax/string-basics.md)

```python
while left < right:
```

Run until the pointers meet or cross. **`<` not `<=`** — when `left == right` they're on the same single character, which is trivially equal to itself, so there's nothing left to check. This condition is also what makes an all-junk string like `" "` return `True`: the pointers cross without ever comparing anything, and we fall through to `return True`.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    while left < right and not s[left].isalnum():
        left += 1
    while right > left and not s[right].isalnum():
        right -= 1
```

Skip the junk. `.isalnum()` is `True` for letters and digits, `False` for spaces and punctuation — so these loops advance each pointer until it lands on a real character.

The `left < right` guard **inside** each inner loop is essential: without it, a string of pure punctuation would run `left` straight off the end of the string and raise `IndexError`. Never let a skip loop outrun its partner.
→ [string-methods](../syntax/string-methods.md) · [logical-operators](../syntax/logical-operators.md) · [while-loop](../syntax/while-loop.md)

```python
    if s[left].lower() != s[right].lower():
        return False
```

The comparison, normalized to lowercase at the point of use — no need to transform the whole string. One mismatch is decisive: **return immediately**.
→ [string-methods](../syntax/string-methods.md) · [if-return](../syntax/if-return.md)

```python
    else:
        left += 1
        right -= 1
```

Characters matched, so step both pointers inward and continue. Moving **both** is what keeps the comparison symmetric.

```python
return True
```

The pointers met without ever finding a mismatch ⇒ palindrome.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:

        left = 0
        right = len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while right > left and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False
            else:
                left += 1
                right -= 1
        return True
```

</details>

**Trace it** — `s = "a b,a"`:

```
index:  0 1 2 3 4
chars:  a   b , a
        ↑       ↑
      left    right
```

| `left` | `right` | After skipping | Compare | Result |
|---|---|---|---|---|
| 0 | 4 | `a` vs `a` | `a == a` ✅ | step to 1, 3 |
| 1 (`' '`) | 3 (`','`) | skip → left=2, right=2 | `left < right` fails | loop ends |
| | | | | `return True` |

**The one-liner alternative**, for comparison:

```python
t = "".join(c.lower() for c in s if c.isalnum())
return t == t[::-1]
```
→ [generator-expressions](../syntax/generator-expressions.md) · [list-slicing](../syntax/list-slicing.md) · [string-join-slice](../syntax/string-join-slice.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

The nested `while` loops look worrying, but count what actually moves: **`left` only ever increases and `right` only ever decreases**, and they stop when they meet. Every index in the string is visited by exactly one of the two pointers, at most once.

So the total number of pointer steps across the entire run — outer loop and inner skip loops combined — is bounded by n. Each step does O(1) work (`.isalnum()`, `.lower()` on a single character).

**O(n)** total.

This is the same **amortized** argument as [Longest Consecutive Sequence](128-longest-consecutive-sequence.md): nested loops don't imply quadratic time when the inner loop's total work across all iterations is bounded. The reliable way to spot it — *does any index get visited more than a constant number of times?* Here, no.

**Best case:** a mismatch at the outermost characters returns after 2 reads.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Two integers, `left` and `right`. Nothing else. The string is only ever *read* — never copied, filtered, or reversed.

**Compare to clean-then-reverse:**

| | Time | Extra space |
|---|---|---|
| Clean + reverse | O(n) | **O(n)** — the filtered string *and* its reversal |
| Two pointers | O(n) | **O(1)** |

Same time complexity, and this is why "what's the complexity?" is two questions. The two-pointer version wins on space without giving anything up — which is unusual. Most of Unit 01 traded memory *for* speed; here the pattern gets the speed for free because **the structure of the problem (symmetry) replaces the need to store anything.**

`c.lower()` does allocate a one-character string per comparison, but it's transient and constant-sized.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A palindrome check is symmetric — first against last, second against second-to-last — so I'll walk two pointers inward from both ends. Rather than building a cleaned copy, I'll skip non-alphanumeric characters in place and lowercase each character at the point of comparison. First mismatch returns false; if the pointers meet, it's a palindrome. O(n) time and O(1) space — the pointers between them visit each index at most once. Cleaning the string and comparing it to its reverse is a nice one-liner, but it costs O(n) extra memory."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if you're allowed one deletion?" | Two pointers still — on mismatch, try skipping the left char *or* the right and check whether either remainder is a palindrome. O(n). That's LeetCode 680. |
| "Find the longest palindromic substring." | Different technique: expand around each of the 2n−1 centres, O(n²). See [Longest Palindromic Substring](5-longest-palindromic-substring.md). |
| "What about Unicode?" | `.isalnum()` and `.lower()` are Unicode-aware in Python, so it mostly works — but full correctness needs normalization (`unicodedata.normalize`), since accented characters have multiple encodings. |
| "Can you do it without `.isalnum()`?" | Compare `ord()` values against the ASCII ranges for `0-9`, `a-z`, `A-Z`. See [ord-chr](../syntax/ord-chr.md). Worth knowing for languages without the helper. |
| "Is a single character a palindrome? Empty string?" | Both yes — and the `left < right` condition handles both without a special case. |
| "Recursive version?" | Compare the ends, recurse on the middle. Clean, but O(n) stack space — strictly worse than the loop. |

**Traps:**

- **Omitting the `left < right` guard in the skip loops.** On `",,,,"` the pointer runs past the end → `IndexError`. This is *the* bug in this problem.
- **`while left <= right`** in the outer loop — harmless here (a character always equals itself), but it signals you haven't thought about the meeting condition.
- **Forgetting `.lower()`** — `"Aa"` would report false.
- **Assuming digits are junk.** `.isalnum()` includes them, and `"0P"` is a real LeetCode test case that is *not* a palindrome.
- **Cleaning the whole string first** when asked for O(1) space.

**This same move shows up in:** [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (converging pointers on a sorted array) · [Container With Most Water](11-container-with-most-water.md) (converge from both ends, move the weaker side) · [Trapping Rain Water](42-trapping-rain-water.md) (two pointers plus running maxima) · [Reverse String / Reorder List](143-reorder-list.md) (the same symmetric front-and-back idea on a linked list).

</details>
