# 162. Find Peak Element

**Medium** · [LeetCode](https://leetcode.com/problems/find-peak-element/) · [Solution file (no hints)](../../problems/0001-0499/162.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

A **peak element** is strictly greater than its neighbors. Given a 0-indexed array `nums`, return the index of **any** peak. You may imagine `nums[-1] = nums[n] = -∞`, so an element is always greater than an out-of-bounds neighbor. You must write an algorithm running in **O(log n)**.

```
nums = [1,2,3,1]        →  2         (3 is a peak)
nums = [1,2,1,3,5,6,4]  →  5 (or 1)  (6 is a peak; so is 2)
```

**Constraints:** `1 <= nums.length <= 1000` · `-2³¹ <= nums[i] <= 2³¹ - 1` · **`nums[i] != nums[i+1]`** for all valid `i`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return **any** peak" | ⚠️ **The unlock.** You don't need *the* maximum — any local peak will do, which is what makes O(log n) possible |
| "**O(log n)**" | Binary search — even though the array is **not sorted** |
| `nums[i] != nums[i+1]` | ⚠️ **No adjacent duplicates.** Every comparison is strictly greater or strictly less — no plateaus to get stuck on |
| "imagine `nums[-1] = nums[n] = -∞`" | The array edges count as peaks if they beat their single neighbor. So a peak **always exists** |
| `nums.length >= 1` | A single element is trivially a peak |

**The surprising part:** binary search on an *unsorted* array. That works because binary search doesn't actually require sortedness — it requires that you can **discard half the search space with one comparison**. Here you can:

> Compare `nums[mid]` with `nums[mid + 1]`.
>
> - If `nums[mid] < nums[mid + 1]` — the array is **ascending** here. Going right, you either keep climbing forever (and hit the right edge, which is a peak because `nums[n] = -∞`) or you eventually descend, which means a peak exists somewhere to the right. **Either way, a peak exists in the right half.**
> - If `nums[mid] > nums[mid + 1]` — the array is **descending** here. By the mirror argument, a peak exists at `mid` or to its left.

**Why a peak must exist in the chosen half** — this is the argument to have ready:

Consider the ascending case. Start at `mid + 1` and walk right. Either the values keep increasing until you reach index `n - 1`, which is then a peak (its right neighbor is `-∞`), or at some point a value drops — and the element just before the drop is greater than both its neighbors, hence a peak. There is no third possibility. Duplicates would break this (a flat run gives no direction), which is exactly why the constraint forbids them.

So you're not searching for a *value*; you're following the slope uphill, halving the range each step.

🤔 **Before you open the next section:** if `nums[mid] < nums[mid+1]`, why can't the entire right half be free of peaks?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Check each element against its neighbors | O(n) | ⚠️ Correct, violates O(log n) |
| Find the global maximum | The max is always a peak | O(n) | ⚠️ Correct but overkill — you don't need *the* max |
| **Binary search on the slope** | Move toward the higher neighbor | **O(log n)** | ✅ |

**The decision: binary search comparing `nums[mid]` against `nums[mid + 1]`.**

Because you're locating a position rather than matching a value, this uses the **boundary-search convention** (as in [First Bad Version](278-first-bad-version.md)):

- `left < right` — loop until one candidate remains
- On ascending (`nums[mid] < nums[mid+1]`): `left = mid + 1` — `mid` can't be a peak, exclude it
- On descending (`nums[mid] > nums[mid+1]`): `right = mid` — `mid` **might** be the peak, keep it
- Return `left` when the pointers converge

**Why `right = mid` and not `mid - 1`.** When `nums[mid] > nums[mid+1]`, `mid` itself is a peak candidate — it beats its right neighbor, and it may well beat its left one too. Discarding it with `mid - 1` can skip the only peak in range. This is the same discipline as [First Bad Version](278-first-bad-version.md), and it's why `left < right` is the required loop condition (with `right = mid`, using `<=` would loop forever once the range hits one element).

**Why comparing with `mid + 1` is always safe.** With `left < right`, the midpoint satisfies `left <= mid < right <= n - 1`, so `mid + 1 <= n - 1` is always a valid index. No bounds check needed — the loop condition guarantees it. (Comparing with `mid - 1` instead would need a guard at `mid = 0`.)

**Why no explicit peak check.** You never verify "is this a peak?" during the loop. The invariant does the work:

> **A peak always exists within `[left, right]`.**

Each step preserves that invariant while halving the range, so when `left == right` the single remaining index must be the peak. That's a cleaner formulation than testing candidates, and it's why the code is only five lines.

**Why not just find the maximum?** The global max is certainly a peak, but finding it requires examining every element — O(n). The problem asks for *any* peak precisely to make the logarithmic solution possible. Recognizing that a weaker requirement enables a faster algorithm is the transferable lesson here.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

The full index range. Both ends are valid peak candidates, thanks to the `-∞` sentinel convention.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left < right:
```

**`<`, not `<=`** — pairs with `right = mid` below. The loop narrows until exactly one candidate remains, and that candidate is the answer.

Using `<=` here would spin forever: at `left == right`, `mid == left`, and `right = mid` wouldn't shrink anything.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = (left + right) // 2
```

Because `left < right`, this guarantees `left <= mid < right` — so `mid + 1` is always in bounds.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if nums[mid] < nums[mid + 1]:
        left = mid + 1
```

**Ascending slope — go right.**

`mid` is definitively *not* a peak (its right neighbor is bigger), so exclude it. A peak is guaranteed somewhere in `[mid+1, right]` by the argument in section 1.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        right = mid
```

**Descending slope — go left, keeping `mid`.**

`nums[mid] > nums[mid + 1]` (strict, since adjacent duplicates are forbidden), so `mid` beats its right neighbor and is a live candidate. `right = mid` retains it.
→ [elif-else](../syntax/elif-else.md)

```python
return left
```

The pointers converged. The invariant guarantees a peak exists in the range, and the range now holds exactly one index — so it's the peak. (`right` would be equally correct; they're equal.)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:

        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < nums[mid + 1]:
                left = mid + 1
            else:
                right = mid

        return left
```

</details>

**Trace it** — `nums = [1, 2, 1, 3, 5, 6, 4]`:

| `left` | `right` | `mid` | `nums[mid]` vs `nums[mid+1]` | Slope | Action |
|---|---|---|---|---|---|
| 0 | 6 | 3 | `3 < 5` | ascending | `left = 4` |
| 4 | 6 | 5 | `6 > 4` | descending | `right = 5` ⭐ |
| 4 | 5 | 4 | `5 < 6` | ascending | `left = 5` |
| 5 | 5 | — | — | — | `left == right` → exit |

`return 5` ✅ — `nums[5] = 6`, with neighbors 5 and 4. A valid peak.

The starred step is the crucial one: `mid = 5` was descending, so `right = mid` **kept index 5** in the range. Had the code used `right = mid - 1`, the range would have become `[4, 4]` and returned index 4 (value 5), whose right neighbor is 6 — **not a peak**. That single character is the difference between correct and wrong.

**A second trace** — `nums = [1, 2, 3, 1]`:

| `left` | `right` | `mid` | Compare | Action |
|---|---|---|---|---|
| 0 | 3 | 1 | `2 < 3` ascending | `left = 2` |
| 2 | 3 | 2 | `3 > 1` descending | `right = 2` |
| 2 | 2 | — | — | exit |

`return 2` ✅ — `nums[2] = 3`, greater than both 2 and 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each iteration halves the range, and each does exactly one comparison. At `n = 1000` that's about **10 iterations**.

**Why this beats the O(n) approaches:** finding the global maximum requires reading every element, but you don't need the maximum — any peak suffices. Weakening the requirement from "the largest" to "a local maximum" is precisely what unlocks the logarithmic bound.

That's a genuinely reusable insight:

> **When a problem says "any" rather than "the best," check whether the weaker requirement admits a faster algorithm.**

**Why the argument needs strict inequalities.** With `nums[i] != nums[i+1]` guaranteed, every comparison points definitively uphill or downhill. If plateaus were allowed (`[1,2,2,2,1]`), a comparison of equal neighbors would give no direction, and you could not safely discard half — the problem would degrade to O(n) in the worst case.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers.

Nothing is allocated, and the array is only read.

**The conceptual point worth carrying:** this problem shows that binary search's real precondition is **not sortedness** but *"one comparison lets you safely discard half the space."* Here the discardable half is determined by a local slope rather than a global ordering.

That reframing is what lets binary search apply to:

| Problem | What the comparison exploits |
|---|---|
| [Binary Search](704-binary-search.md) | global sorted order |
| [First Bad Version](278-first-bad-version.md) | a monotonic predicate |
| **Find Peak Element** | **a local slope on unsorted data** |
| [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) | a rotation pivot |
| [Koko Eating Bananas](875-koko-eating-bananas.md) | monotonic feasibility over an answer range |

An iterative loop keeps space constant; recursion would add O(log n) frames for nothing.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array isn't sorted, but binary search doesn't strictly need sortedness — it needs one comparison to let me discard half the space safely. Here I compare `nums[mid]` with `nums[mid+1]`. If it's ascending, then walking right either climbs to the last index — which is a peak because the out-of-bounds neighbor counts as −∞ — or eventually descends, and the element before the descent is a peak. Either way a peak exists to the right, so I move `left = mid + 1`. If it's descending, `mid` itself is a candidate, so I set `right = mid` to keep it. The invariant is that a peak always exists in `[left, right]`, so when they converge the single remaining index is the answer — I never need to explicitly test whether something is a peak. The no-adjacent-duplicates constraint is what makes every comparison give a direction. O(log n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does binary search work on unsorted data?" | **The key question.** It needs a rule for discarding half safely, not a global order. The local slope provides that. |
| "Why `right = mid` and not `mid - 1`?" | `mid` beats its right neighbor, so it's a live candidate. Discarding it can skip the only peak. |
| "What if adjacent duplicates were allowed?" | The slope comparison gives no direction on a plateau; you can't safely discard, and the worst case becomes O(n). |
| "Find **all** peaks?" | Requires examining everything — O(n). Binary search only finds one. |
| "2-D version?" | [LeetCode 1901](https://leetcode.com/problems/find-a-peak-element-ii/) — binary search on columns, taking the row-max in each. O(m log n). |
| "Why is a peak guaranteed to exist?" | The out-of-bounds `-∞` sentinels mean the global maximum is always a peak, so at least one exists. |
| "Return the **largest** peak?" | Then you need the global max — O(n). Binary search can't find it. |

**Traps:**

- **`right = mid - 1`.** Discards a valid candidate. The `[1,2,1,3,5,6,4]` trace shows it returning a non-peak.
- **`left <= right` with `right = mid`.** Infinite loop once the range reaches one element.
- **Comparing with `nums[mid - 1]`** without a bounds guard. `mid` can be 0; `mid + 1` is always safe under `left < right`.
- **Explicitly checking `nums[mid-1] < nums[mid] > nums[mid+1]`.** Unnecessary and adds boundary cases — the invariant already guarantees correctness.
- **Assuming the answer must be the global maximum.** Any peak is acceptable, and that's what makes O(log n) possible.
- **Not trusting the `-∞` convention.** A strictly ascending array like `[1,2,3]` has its peak at the last index — the code returns it correctly.

**This same move shows up in:** [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (binary search on a non-sorted array using a structural comparison) · [First Bad Version](278-first-bad-version.md) (the same `right = mid` boundary convention) · [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md) (deciding which half is usable from a local comparison) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search where the "array" is an answer range).

</details>

---
