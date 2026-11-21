# 179. Largest Number

**Medium** · [LeetCode](https://leetcode.com/problems/largest-number/) · [Solution file (no hints)](../../problems/0001-0499/179.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [📖 Sorting](../learning/05b-sorting.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Given a list of non-negative integers `nums`, arrange them so they form the **largest number**, and return it as a **string** (the result may be too large for an integer type).

```
nums = [10, 2]              →  "210"
nums = [3, 30, 34, 5, 9]    →  "9534330"
nums = [0, 0]               →  "0"       (not "00")
```

**Constraints:** `1 <= nums.length <= 100` · `0 <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**arrange** them" | You're choosing an **order**, which means sorting with the right comparison |
| largest **number** | Joined as digits. Earlier positions matter more |
| return a **string** | You'll be concatenating strings, so convert early |
| `[0, 0]` → `"0"` | An edge case: all zeros must collapse to a single `"0"` |

**Why normal sorting fails.**

- **Numeric descending:** `[10, 2]` → `[10, 2]` → `"102"`. But `"210"` is bigger.
- **String descending:** `["3", "30"]` sorts as `["30", "3"]` (`"30" > "3"`) → `"303"`. But `"330"` is bigger.

Neither the numbers nor their string forms are ordered the right way on their own. What matters is **how two numbers look when placed next to each other**.

**The comparison that works.** For two strings `a` and `b`, ask which order makes a bigger result:

> put `a` first if **`a + b > b + a`**

- `"3"` vs `"30"`: `"330"` vs `"303"`. `"330"` is bigger, so `"3"` goes first ✅.
- `"9"` vs `"34"`: `"934"` vs `"349"`, so `"9"` goes first ✅.

Both concatenations have the same length, so comparing them as strings compares them as numbers.

**Why sorting by this pairwise rule gives the best overall answer.** The rule is consistent: if `a` should come before `b` and `b` before `c`, then `a` before `c`. That makes it a valid sort order. And any arrangement where two neighbours are in the "wrong" order can be improved by swapping them. So the sorted order has no possible improvement left, which means it's the best.

🤔 **Before you open the next section:** using the `a + b` vs `b + a` rule, how do `"34"` and `"3"` compare, and how do `"30"` and `"3"`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every permutation | Generate all orders, keep the largest | O(n! · n) | O(n) | ❌ n = 100 |
| Sort numerically / by string | Use the built-in order | O(n log n) | O(n) | ❌ Wrong answers |
| **Custom comparator sort** | Sort strings by `a + b` vs `b + a` | **O(n log n · k)** | O(n · k) | ✅ |
| Key trick | `key=lambda s: s * 10`, reverse sort | O(n log n · k) | O(n · k) | ✅ Clever, harder to justify |

Here k is the maximum number of digits, at most 10.

**The decision: a [greedy](../learning/16-greedy.md) sort with a custom comparison.**

Python's `sort` takes a **key function**, not a two-argument comparison. `functools.cmp_to_key` converts an old-style comparison function into a key, which is exactly what you need when the ordering only makes sense **between pairs**.

**The comparison function's contract:** return a **negative** number if `a` should come first, **positive** if `b` should come first, and **0** if they're tied.

**The key trick, for interest.** Since numbers are at most 10 digits, repeating each string enough times and comparing those gives the same order: `sorted(strs, key=lambda s: s * 10, reverse=True)`. It works, but explaining *why* it works takes longer than writing the comparator.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
strs = []
for n in nums:
    strs.append(str(n))
```

Convert everything to strings first. The comparison and the final join both work on strings. `[str(n) for n in nums]` would do the same in one line.
→ [type-conversion](../syntax/type-conversion.md) · [list-methods](../syntax/list-methods.md)

```python
def compare(a, b):
    if a + b > b + a:
        return -1
    if a + b < b + a:
        return 1
    return 0
```

**The pairwise rule.** If `a` first gives the bigger result, return `-1` to say "`a` comes first." If `b` first is bigger, return `1`. Equal means they're interchangeable (for example, `"12"` and `"1212"`).

Comparing `a + b` with `b + a` as strings is safe, because both have the same length. For equal-length digit strings, alphabetical order is numeric order.
→ [function-basics](../syntax/function-basics.md) · [string-basics](../syntax/string-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
strs.sort(key=cmp_to_key(compare))
```

**Sort with the rule.** `cmp_to_key` wraps `compare` so Python's sort can use it. (It's imported with `from functools import cmp_to_key`.) After this, `strs` is in the order that makes the biggest number.
→ [sorting-key](../syntax/sorting-key.md) · [functools-cache](../syntax/functools-cache.md) · [from-import](../syntax/from-import.md)

```python
if strs[0] == "0":
    return "0"
```

**The all-zeros case.** If the biggest piece after sorting is `"0"`, every piece is `"0"`, and the join would be `"000…"`. Return a single `"0"` instead.
→ [if-return](../syntax/if-return.md)

```python
return "".join(strs)
```

Concatenate the pieces in order. `"".join` builds the result in one pass. Adding strings together in a loop would copy the result each time.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>The whole thing together</summary>

```python
from functools import cmp_to_key

class Solution:
    def largestNumber(self, nums: list[int]) -> str:

        strs = []

        for n in nums:
            strs.append(str(n))

        def compare(a, b):
            if a + b > b + a:
                return -1
            if a + b < b + a:
                return 1
            return 0

        strs.sort(key=cmp_to_key(compare))

        if strs[0] == "0":
            return "0"

        return "".join(strs)
```

</details>

**Trace it.** `nums = [3, 30, 34, 5, 9]`. Here are the key pairwise decisions:

| `a` | `b` | `a + b` | `b + a` | Who goes first |
|---|---|---|---|---|
| 9 | 5 | 95 | 59 | 9 |
| 5 | 34 | 534 | 345 | 5 |
| 34 | 3 | 343 | 334 | 34 |
| 3 | 30 | 330 | 303 | 3 |

Sorted: `["9", "5", "34", "3", "30"]` → **`"9534330"`** ✅.

Note `"3"` before `"30"` and `"34"` before `"3"`. Plain string order gets the second right (`"34" > "3"`) but the first wrong (it puts `"30"` before `"3"`).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n · k)</summary>

**O(n log n · k)**, where k is the maximum number of digits.

- The sort makes O(n log n) comparisons.
- Each comparison builds and compares two strings of length up to 2k, which is O(k).

With k ≤ 10, it's effectively O(n log n). Converting to strings and the final join are both O(n · k).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · k)</summary>

**O(n · k)** for the list of strings and the output. Each comparison makes two temporary strings of length up to 2k, but those are freed straight away. Python's sort (Timsort) uses up to O(n) extra space of its own.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Normal sorting fails: numerically, 10 comes before 2, and by string, 30 comes before 3. What matters is how two numbers look side by side, so I sort the string forms with a custom comparison: a goes before b if a + b is bigger than b + a. That rule is a consistent order, and any neighbouring pair in the wrong order could be swapped to improve the result, so the sorted order is the best. In Python I use cmp_to_key. If the first string is "0", everything is zero, so I return "0". O(n log n) comparisons of O(k) each."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the comparison valid for sorting?" | `a + b > b + a` is a consistent ordering: if a beats b and b beats c, then a beats c. And swapping any pair of neighbours that's in the wrong order makes the result bigger. |
| "Smallest number instead?" | Flip the rule: `a` first if `a + b < b + a`. Watch out for leading zeros. |
| "Without `cmp_to_key`?" | `sorted(strs, key=lambda s: s * 10, reverse=True)` works for numbers up to 10 digits. |
| "Why not compare the numbers directly?" | `10 > 2`, but `"2"` must come first. Size isn't the same as position-value. |

**Traps:**

- **Sorting numerically or by plain string.** Both give wrong answers (`[10, 2]` and `[3, 30]`).
- **Returning `"00"` for `[0, 0]`.** Check the first element after sorting.
- **Backwards return values.** Negative means `a` first. Get it the wrong way round and you build the *smallest* number.
- **Comparing as integers** (`int(a + b)`). It works, but it's needless conversion. Equal-length strings already compare correctly.
- **Building the result with `+=` in a loop.** It copies the result each time. Use `"".join`.

**This same move shows up in:** [Sort Colors](75-sort-colors.md) (sorting by a rule other than plain value) · [Top K Frequent Words](692-top-k-frequent-words.md) (sorting with a multi-part key) · [Merge Intervals](56-merge-intervals.md) (sort first, then the greedy pass is easy) · [Reorganize String](767-reorganize-string.md) (greedy ordering of pieces to build the best string).

</details>

---
