# 918. Maximum Sum Circular Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-sum-circular-subarray/) · [Solution file (no hints)](../../problems/0500-0999/918.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Given a **circular** integer array `nums`, return the maximum sum of a **non-empty subarray**. In a circular array the end connects back to the start, so a subarray may **wrap around**. Each element may be used at most once.

```
nums = [1, -2, 3, -2]      →  3     (just [3])
nums = [5, -3, 5]          →  10    (wrap: 5 + 5)
nums = [-3, -2, -3]        →  -2    (all negative: the largest single element)
```

**Constraints:** `1 <= nums.length <= 3 * 10⁴` · `-3 * 10⁴ <= nums[i] <= 3 * 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "maximum subarray sum" | [Maximum Subarray](53-maximum-subarray.md): **Kadane's algorithm** |
| "circular" | The best subarray is either **in the middle** (the normal case) or **wraps around** |
| "non-empty" | An all-negative array must return its largest element, not 0 |
| `n` up to `3 * 10⁴` | O(n²) is too slow (9×10⁸). O(n) required |

**Two cases:**

1. **No wrap:** an ordinary Kadane maximum, `max_sub`.
2. **Wrap:** the subarray uses a prefix and a suffix, and **leaves a contiguous block unused in the middle**. The sum is `total − (that middle block)`. To maximise it, **minimise the middle block**: that's a **minimum subarray sum** (Kadane with min), `min_sub`.

So the answer is `max(max_sub, total − min_sub)`.

**The one trap:** if **every element is negative**, then `min_sub` is the whole array, and `total − min_sub = 0` means an *empty* subarray, which is not allowed. In that case return `max_sub` (the largest single element).

🤔 **Before you open the next section:** for `[5, -3, 5]`, what are `total`, `min_sub`, and `max_sub`? Which case wins?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Try every start and length on the doubled array | O(n²) | O(1) | ❌ Too slow |
| Prefix sums + monotonic deque on the doubled array | O(n) | O(n) | ✅ Works, but heavy |
| **Kadane for max and min in one pass, plus the total** | **O(n)** | **O(1)** | ✅ |

**The decision: [Kadane's algorithm](../algorithms/kadane-algorithm.md), run for both maximum and minimum.** Both run in the same loop with the running total.

`max_sub = max(max_sub, cur_max)` where `cur_max = max(cur_max + x, x)`; and symmetric for the minimum. Then `max_sub` is the best non-wrapping answer and `total − min_sub` is the best wrapping one.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
total = 0
cur_max = cur_min = 0
best_max = best_min = nums[0]
```

`total` is the sum of everything. `cur_max` / `cur_min` are the best/worst subarray sums **ending at the current element**. `best_max` / `best_min` are the best/worst seen anywhere. Start `best_*` at `nums[0]` (not 0) so all-negative input works.
→ [variables-assignment](../syntax/variables-assignment.md) · [kadane-algorithm](../algorithms/kadane-algorithm.md)

```python
for x in nums:
    cur_max = max(cur_max + x, x)
    best_max = max(best_max, cur_max)
    cur_min = min(cur_min + x, x)
    best_min = min(best_min, cur_min)
    total += x
```

Standard Kadane twice. At each element, either **extend** the run ending here or **restart** at `x`, whichever is better (larger for the maximum, smaller for the minimum). `total` accumulates alongside.
→ [for-loop](../syntax/for-loop.md) · [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
if best_max < 0:
    return best_max
return max(best_max, total - best_min)
```

**All negative** (`best_max < 0`): any wrap would leave out the entire array's worth of negativity and reach 0, which is the empty subarray. Return the plain maximum. Otherwise take the better of the two cases.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        total = 0
        cur_max = cur_min = 0
        best_max = best_min = nums[0]

        for x in nums:
            cur_max = max(cur_max + x, x)
            best_max = max(best_max, cur_max)
            cur_min = min(cur_min + x, x)
            best_min = min(best_min, cur_min)
            total += x

        if best_max < 0:
            return best_max
        return max(best_max, total - best_min)
```

</details>

**Trace it.** `nums = [5, -3, 5]`:

| `x` | `cur_max` | `best_max` | `cur_min` | `best_min` | `total` |
|---|---|---|---|---|---|
| 5 | 5 | 5 | 5 | 5 | 5 |
| -3 | 2 | 5 | -3 | -3 | 2 |
| 5 | 7 | **7** | 2 | -3 | 7 |

`best_max = 7` (no wrap), `total − best_min = 7 − (−3) = 10` → **10** ✅ (the wrap `5 + 5`).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** a single pass with O(1) work per element.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1):** a handful of integers.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The best circular subarray either doesn't wrap, which is the ordinary Kadane maximum, or it wraps, in which case it's the total minus a contiguous block in the middle that I'd like to be as small as possible, so total minus the minimum subarray sum. I compute both Kadanes and the total in one pass and return the larger. One catch: if every number is negative, total minus the min subarray is zero, which means an empty subarray, so in that case I return the plain maximum. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why subtract the minimum subarray?" | A wrapping subarray is the whole circle minus one contiguous gap. The smaller the gap sum, the bigger the wrap |
| "Why the all-negative check?" | The min subarray would be the whole array, giving a sum of 0 for an empty selection |
| "Return the subarray itself?" | Track start and end indices in both Kadane runs |
| "Alternative?" | Double the array and use prefix sums with a sliding-window minimum (monotonic deque) over windows of length ≤ n |
| "Related?" | [Maximum Subarray](53-maximum-subarray.md) · [Maximum Product Subarray](152-maximum-product-subarray.md) |

**Traps:**

- **Forgetting the all-negative case.** It returns `0`, which isn't a valid answer.
- **Initialising `best_max` to 0.** A negative-only array then reports 0.
- **Using `total − best_min` when `best_min == total`** (the min subarray is the entire array).
- **Running Kadane on the doubled array without a length cap**, which allows more than `n` elements.

**This same move shows up in:** [Maximum Subarray](53-maximum-subarray.md) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) · [Maximum Product Subarray](152-maximum-product-subarray.md).

</details>

---
