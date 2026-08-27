# 643. Maximum Average Subarray I

**Easy** · [LeetCode](https://leetcode.com/problems/maximum-average-subarray-i/) · [Solution file (no hints)](../../problems/0500-0999/643.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given an integer array `nums` and an integer `k`, find a contiguous subarray of length **exactly `k`** that has the maximum average value, and return that average.

```
nums = [1,12,-5,-6,50,3], k = 4  →  12.75    ((12 - 5 - 6 + 50) / 4)
nums = [5], k = 1                →  5.00000
```

**Constraints:** `n == nums.length` · `1 <= k <= n <= 10⁵` · `-10⁴ <= nums[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "length **exactly `k`**" | ⚠️ A **fixed-size** window — the simplest sliding-window variety. No growing or shrinking logic needed |
| "**contiguous**" | A window, not a subsequence |
| "maximum **average**" | Since every candidate has the same length `k`, **maximizing the average is identical to maximizing the sum**. Divide once at the end |
| `k <= n` guaranteed | At least one valid window exists; no empty-case handling |
| `n` up to 10⁵ | Recomputing each window's sum from scratch is O(n·k) = 10⁹ — too slow |
| values can be negative | So you can't assume sums grow, and you can't skip windows on a "getting worse" heuristic |

**The first simplification:** all windows have the same length, so `sum / k` is maximized exactly when `sum` is. Track sums, divide once at the end. Doing the division inside the loop is `n` needless floating-point operations and invites precision drift.

**The second, and the actual point of the problem:** consecutive windows overlap heavily.

```
nums = [1, 12, -5, -6, 50, 3],  k = 4

window at 0:  [1, 12, -5, -6]           sum = 2
window at 1:      [12, -5, -6, 50]      sum = 51
                   └────┬─────┘
              these three are shared — why re-add them?
```

Sliding the window one step **removes exactly one element and adds exactly one element**. So instead of recomputing `k` additions per window, do:

```
new_sum = old_sum + nums[entering] - nums[leaving]
```

Two operations per step instead of `k`. That's the entire sliding-window idea in its purest form.

🤔 **Before you open the next section:** if you know the sum of `nums[i..i+k-1]`, what's the cheapest way to get the sum of `nums[i+1..i+k]`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each start, sum `k` elements | O(n·k) | O(1) | ❌ 10⁹ at n = k = 10⁵ |
| Prefix sums | Build prefix array, each window is a subtraction | O(n) | **O(n)** | ⚠️ Correct, but O(n) memory for no benefit |
| **Fixed sliding window** | Maintain a running sum; add one, drop one | **O(n)** | **O(1)** | ✅ |

**The decision: a fixed-size sliding window with a running sum.**

Two phases, and keeping them mentally separate prevents most bugs:

1. **Prime the window.** Compute the sum of the first `k` elements once — `sum(nums[:k])`. This is your starting candidate.
2. **Slide.** For each subsequent position, add the incoming element and subtract the outgoing one, then update the best.

**Why the window never changes size.** This is a *fixed* window, which is genuinely easier than the variable-size kind you'll meet in [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) or [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md). There's no condition to check, no `while` loop to shrink — every step moves both edges in lockstep. Recognizing "exactly k" as the signal for the simple variant saves you from over-engineering.

**Why not prefix sums?** They'd work: build `prefix`, then each window is `prefix[i+k] - prefix[i]`, giving O(n) time. But it's O(n) *space* for something a single running scalar handles. Prefix sums earn their memory when you need **arbitrary** range queries ([Range Sum Query](303-range-sum-query-immutable.md)) or when ranges are found by lookup ([Subarray Sum Equals K](560-subarray-sum-equals-k.md)). Here the ranges march predictably, so a scalar suffices.

**A note on floating point.** Divide **once**, at the end. Accumulating in integers and doing a single division keeps the result exact up to one rounding step. Maintaining a running *average* instead would compound error across 10⁵ updates — a real precision bug, not a theoretical one. See [float-precision-notes](../syntax/float-precision-notes.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
window_sum = sum(nums[:k])
```

**Prime the window** with the first `k` elements. One O(k) operation, done once — this is the only place a full summation happens.
→ [list-slicing](../syntax/list-slicing.md)

```python
max_sum = window_sum
```

Seed the best with the first window's sum — **not** with `0` or `float('-inf')`.

`0` would be an outright bug: with all-negative input like `[-5, -3]`, the true answer is negative, and seeding at 0 returns a sum no window achieves. Since `k <= n` guarantees a first window exists, seeding with it is both safe and correct.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(k, len(nums)):
```

Start at `k` — the index of the **first element that enters** the window on the first slide. Everything before it is already accounted for in the priming step.
→ [range-function](../syntax/range-function.md)

```python
    window_sum += nums[i] - nums[i - k]
```

**The slide, in one line — this is the whole optimization.**

- `nums[i]` — the element **entering** on the right
- `nums[i - k]` — the element **leaving** on the left

Why `i - k`? The window covers the `k` positions ending at `i`, i.e. `[i-k+1, i]`. The element that just fell out is the one immediately before that range: `i - k`. Draw it once for `k = 4, i = 4`: the window becomes `[1,2,3,4]` and the departing element is index `0`. ✅
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    max_sum = max(max_sum, window_sum)
```

Track the best sum seen.
→ [min-max-key](../syntax/min-max-key.md)

```python
return max_sum / k
```

**Divide once, at the very end.** `/` is true division in Python 3, so this yields a float even when both operands are integers.
→ [int-float-basics](../syntax/int-float-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:

        window_sum = sum(nums[:k])
        max_sum = window_sum

        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)

        return max_sum / k
```

</details>

**Trace it** — `nums = [1, 12, -5, -6, 50, 3]`, `k = 4`:

| Step | `i` | Window | Entering `nums[i]` | Leaving `nums[i-k]` | `window_sum` | `max_sum` |
|---|---|---|---|---|---|---|
| prime | — | `[1,12,-5,-6]` | — | — | **2** | 2 |
| 1 | 4 | `[12,-5,-6,50]` | `nums[4]=50` | `nums[0]=1` | `2 + 50 - 1 =` **51** | **51** |
| 2 | 5 | `[-5,-6,50,3]` | `nums[5]=3` | `nums[1]=12` | `51 + 3 - 12 =` **42** | 51 |

Return `51 / 4` = **12.75** ✅

Note step 1 computed a 4-element sum with **two** arithmetic operations instead of four additions — and the saving grows linearly with `k`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Priming: O(k)
- Sliding loop: `n - k` iterations, each O(1)

Total O(k) + O(n − k) = **O(n)**, and note `k` cancels out entirely — the runtime is independent of window size.

**That independence is the headline.** Brute force is O(n·k), which at `n = k = 10⁵` is ~10⁹ operations. The sliding window is 10⁵ regardless of whether `k` is 1 or 10⁵.

| | n = 10⁵, k = 5·10⁴ |
|---|---|
| Brute force O(n·k) | ~5·10⁹ |
| **Sliding window O(n)** | **10⁵** |

This is optimal — you must read every element at least once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two numeric variables (`window_sum`, `max_sum`) plus the loop index.

The `nums[:k]` slice in the priming step allocates a temporary list of size `k` — technically O(k) for an instant. Avoid it entirely if you want strict O(1):

```python
window_sum = 0
for i in range(k):
    window_sum += nums[i]
```

Nobody will fault the slice, but knowing it's there is the sort of detail that distinguishes a careful answer.

**Compare to prefix sums:** O(n) space for the same O(n) time. Strictly worse *here*, because the windows are contiguous and predictable. Prefix sums win when ranges are arbitrary or discovered dynamically — a distinction worth being able to articulate:

| | Best when |
|---|---|
| **Sliding window** | ranges move predictably by one |
| **Prefix sums** | ranges are arbitrary, or found by lookup |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every candidate has the same length `k`, so maximizing the average is the same as maximizing the sum — I'll track sums and divide once at the end for precision. Consecutive windows overlap in `k−1` elements, so instead of recomputing each sum in O(k), I slide: add the entering element and subtract the leaving one, two operations per step. I prime with the first `k` elements and seed the maximum with that sum rather than zero, since values can be negative. O(n) time, O(1) space — and the runtime doesn't depend on `k` at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Maximum average with length **at least** `k`?" | [LeetCode 644](https://leetcode.com/problems/maximum-average-subarray-ii/) — much harder. Binary search on the answer plus a prefix-sum feasibility check. |
| "Return the **subarray**, not the average." | Track the index where `max_sum` was achieved; the window is `[idx-k+1, idx]`. |
| "Maximum sum with **any** length?" | Different problem — [Kadane's algorithm](../algorithms/kadane-algorithm.md), see [Maximum Subarray](53-maximum-subarray.md). |
| "Why divide at the end?" | Precision. A running average compounds rounding error over `n` updates; one division at the end rounds once. |
| "What if `k` could exceed `n`?" | Return 0 or raise — but the constraints guarantee `k <= n`, so no guard is needed here. |
| "Minimum average instead?" | Swap `max` for `min` and seed accordingly. |
| "Could you use prefix sums?" | Yes — `prefix[i+k] - prefix[i]` — but that's O(n) space for the same O(n) time. Worse here. |

**Traps:**

- **Seeding `max_sum = 0`.** Wrong on all-negative input. Use the first window's sum.
- **Getting `i - k` wrong.** Using `i - k + 1` or `i - k - 1` shifts the window by one and quietly produces wrong sums. Draw the indices once.
- **Dividing inside the loop.** Wasteful and imprecise; and comparing floats where you could compare exact integers is a needless risk.
- **Recomputing `sum(nums[i:i+k])` each step.** That's the O(n·k) brute force wearing a sliding-window disguise.
- **Starting the loop at `k+1` or `k-1`.** The first entering index is exactly `k`.
- **Returning an integer.** Python 3's `/` gives a float, but `//` would truncate — an easy slip.

**This same move shows up in:** [Maximum Number of Vowels in a Substring](1456-maximum-number-of-vowels-in-a-substring-of-given-length.md) (the same fixed window, counting instead of summing) · [Contains Duplicate II](219-contains-duplicate-ii.md) (fixed window maintaining a set) · [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md) (fixed window maintaining a frequency map) · [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) (the *variable*-size cousin, for contrast).

</details>

---
