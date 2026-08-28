# 35. Search Insert Position

**Easy** · [LeetCode](https://leetcode.com/problems/search-insert-position/) · [Solution file (no hints)](../../problems/0001-0499/35.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given a **sorted** array of distinct integers and a target value, return the index if the target is found. If not, return the index where it **would be** if inserted in order. You must write an algorithm with **O(log n)** runtime.

```
nums = [1,3,5,6], target = 5  →  2    (found at index 2)
nums = [1,3,5,6], target = 2  →  1    (would insert between 1 and 3)
nums = [1,3,5,6], target = 7  →  4    (would append at the end)
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁴ <= nums[i] <= 10⁴` · `nums` sorted **ascending**, all **distinct** · `-10⁴ <= target <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted** array" | ⚠️ The precondition for binary search. Half the search space is eliminable at every step |
| "**O(log n)** runtime" | Explicitly rules out a linear scan — binary search is mandatory, not optional |
| "distinct integers" | No duplicate handling; the found case is unambiguous |
| "return the index **if found**" | Standard binary search |
| "otherwise where it **would be**" | ⚠️ The twist — you must return something meaningful on failure, not `-1` |
| target may exceed all elements | The answer can be `len(nums)` — one past the end, which is a valid insertion point |

This is textbook binary search with **one extra idea**: instead of returning `-1` when the target is absent, return the position where it belongs.

**The insight that makes it almost free:** when a standard binary search loop terminates without finding the target, `left` has already converged on exactly the insertion point.

Why? The loop invariant is:

> Everything at indices `< left` is **less than** target; everything at indices `> right` is **greater than** target.

When `left > right` the search space is empty, and `left` sits precisely at the boundary between "smaller" and "larger" — which is the definition of where the target would be inserted.

So the entire modification is changing `return -1` to `return left`. That's it.

🤔 **Before you open the next section:** when a binary search fails, what do you know about all the elements to the left of the final `left` pointer, and all those to its right?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Linear scan | Walk until `nums[i] >= target` | O(n) | O(1) | ❌ Violates the stated O(log n) |
| `bisect.bisect_left` | Standard library | O(log n) | O(1) | ⚠️ Correct one-liner; write the loop in an interview |
| **Binary search, return `left`** | Halve the range; on failure `left` is the answer | **O(log n)** | **O(1)** | ✅ |

**The decision: classic binary search, returning `left` when the loop ends.**

The three-branch structure:

| Condition | Meaning | Action |
|---|---|---|
| `nums[mid] == target` | found | `return mid` |
| `nums[mid] < target` | target is to the **right** | `left = mid + 1` |
| `nums[mid] > target` | target is to the **left** | `right = mid - 1` |

**Why `left <= right` and not `left < right`.** With `<=`, the loop continues while the range is non-empty — including when it holds exactly one element (`left == right`). Using `<` would skip that final single-element check and miss targets located there. This is the most common binary-search bug, and it's worth internalizing the rule:

> Use `left <= right` when `right` is an **inclusive** bound (initialized to `len(nums) - 1`).
> Use `left < right` when `right` is an **exclusive** bound (initialized to `len(nums)`).

Mixing the two conventions is what produces off-by-one bugs and infinite loops. Pick one and be consistent.

**Why `mid + 1` and `mid - 1` matter.** After checking `mid`, you know it isn't the answer, so exclude it. Writing `left = mid` instead of `mid + 1` can leave the range unchanged and loop forever — e.g. with `left == right == mid`.

**Why `left` is the insertion point, concretely.** Every time you do `left = mid + 1`, you've confirmed `nums[mid] < target`, so everything up to `mid` is smaller. Every time you do `right = mid - 1`, everything from `mid` onward is larger. When they cross, `left` is the first index whose value is ≥ target — exactly where the target belongs.

**Why the overflow-safe midpoint?** `(left + right) // 2` is fine in Python (arbitrary-precision integers), but in C++/Java it can overflow when both are near `INT_MAX`. The portable form is `left + (right - left) // 2`. Worth mentioning; the solution file uses the simple form since this is Python.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

**Inclusive bounds** — `right` points at the last valid index, not one past it. That choice dictates the loop condition below.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
```

`<=` because both bounds are inclusive: when `left == right` the range still holds one unexamined element.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = (left + right) // 2
```

Floor division gives the lower middle for even-sized ranges. Fine in Python; use `left + (right - left) // 2` in languages with fixed-width ints.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if nums[mid] == target:
        return mid
```

Found it. Distinct values mean this is unambiguous.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
    elif nums[mid] < target:
        left = mid + 1
```

`mid` is too small, so the answer lies strictly to its right. `mid + 1` excludes the already-checked element — and this line is what establishes "everything left of `left` is < target."

```python
    else:
        right = mid - 1
```

`mid` is too large, so the answer lies strictly to its left. This establishes "everything right of `right` is > target."
→ [elif-else](../syntax/elif-else.md)

```python
return left
```

**The one line that distinguishes this from plain binary search.**

The loop exited with `left > right`, meaning the search space is empty. By the invariant, `left` is the first index holding a value greater than target — precisely the insertion point.

It also handles the boundary cases automatically:
- target smaller than everything → `left` never moves → `0` ✅
- target larger than everything → `left` walks off the end → `len(nums)` ✅

→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return left


"""
Built in library
import bisect
return bisect.bisect_left(nums, target)
"""
```

</details>

**Trace the found case** — `nums = [1,3,5,6]`, `target = 5`:

| `left` | `right` | `mid` | `nums[mid]` | Compare | Action |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 3 | `3 < 5` | `left = 2` |
| 2 | 3 | 2 | 5 | **equal** | `return 2` ✅ |

**Trace the not-found case** — `nums = [1,3,5,6]`, `target = 2`:

| `left` | `right` | `mid` | `nums[mid]` | Compare | Action |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 3 | `3 > 2` | `right = 0` |
| 0 | 0 | 0 | 1 | `1 < 2` | `left = 1` |
| 1 | 0 | — | — | `left > right` | exit loop |

`return left` = **1** ✅ — inserting 2 at index 1 gives `[1,2,3,5,6]`, correctly ordered.

Note the second row only happened because the condition is `<=`; with `<` the loop would have exited early and returned 0 — wrong.

**And the append case** — `target = 7`:

| `left` | `right` | `mid` | `nums[mid]` | Action |
|---|---|---|---|---|
| 0 | 3 | 1 | 3 | `left = 2` |
| 2 | 3 | 2 | 5 | `left = 3` |
| 3 | 3 | 3 | 6 | `left = 4` |
| 4 | 3 | — | — | exit |

`return 4` = `len(nums)` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each iteration discards **half** the remaining range: from `n` candidates to `n/2`, then `n/4`, and so on. The number of halvings before the range is empty is `log₂ n`.

At `n = 10⁴` that's about **14 iterations** — versus up to 10⁴ for a linear scan.

| n | Binary search steps |
|---|---|
| 10³ | ~10 |
| 10⁶ | ~20 |
| 10⁹ | ~30 |

The logarithm's flatness is the whole point: a thousand-fold increase in input costs ten more steps.

**Best case** is O(1) — the target sits at the first `mid`. The bound describes the worst case, where the range shrinks all the way to empty.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers (`left`, `right`, `mid`), regardless of input size.

The iterative form is what keeps it constant. A **recursive** binary search is equally O(log n) in time but uses **O(log n) stack space** for the call frames — at `n = 10⁴` that's ~14 frames, harmless here, but the iterative version is strictly better and just as readable.

That's the general preference worth carrying:

> **Binary search is one of the cases where iteration clearly beats recursion** — there's no tree to unwind, just a shrinking interval, and a loop expresses that directly.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array is sorted and O(log n) is required, so binary search. Standard three-way comparison: if `nums[mid]` equals the target I return `mid`; if it's smaller I move `left` past `mid`; if larger I move `right` before `mid`. The only twist is what to return when the target isn't present — and it turns out `left` is already the answer. The loop invariant is that everything left of `left` is smaller than the target and everything right of `right` is larger, so when they cross, `left` is the first position holding a larger value, which is exactly the insertion point. That also handles both boundary cases: 0 if the target precedes everything, and `len(nums)` if it follows everything. O(log n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if there are **duplicates**?" | Decide which end you want. `bisect_left` finds the first ≥ target; `bisect_right` finds the first > target. Adjust by moving `right = mid` on equality (leftmost) or `left = mid + 1` (rightmost). |
| "Why `left <= right`?" | `right` is an inclusive bound, so `left == right` is still a valid one-element range that must be checked. |
| "Why is `left` the insertion point?" | Invariant: everything below `left` is smaller, everything above `right` is larger. On exit they cross, so `left` is the first larger position. |
| "Do it recursively." | Same logic, but O(log n) stack space. Iterative is preferred here. |
| "What about integer overflow?" | Not in Python. In C++/Java use `left + (right - left) // 2`. |
| "Find the **last** position ≤ target?" | Return `left - 1` after the same loop, or run a rightmost-biased variant. |
| "Can you use the standard library?" | `bisect.bisect_left(nums, target)` — identical result. Fine to mention, but write the loop. |

**Traps:**

- **Using `left < right`.** Skips the final one-element range and misses targets there. *The* binary-search bug.
- **`left = mid` or `right = mid`** with inclusive bounds. The range can stop shrinking → infinite loop.
- **Returning `-1` on failure.** This problem wants the insertion point, not a not-found sentinel.
- **Returning `right` or `mid`.** Only `left` is guaranteed to be the insertion point after the loop.
- **Mixing bound conventions.** Inclusive `right` pairs with `<=`; exclusive `right` pairs with `<`. Don't blend them.
- **Forgetting the target can exceed everything.** The answer `len(nums)` is valid and must not be clamped.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the base case, returning `-1` instead of `left`) · [First Bad Version](278-first-bad-version.md) (boundary-finding with the `left < right` convention) · [Find First and Last Position](34-find-first-and-last-position-of-element-in-sorted-array.md) (leftmost/rightmost variants, where duplicates matter) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search on the *answer* rather than an array).

</details>

---
