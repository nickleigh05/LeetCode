# 1004. Max Consecutive Ones III

**Medium** · [LeetCode](https://leetcode.com/problems/max-consecutive-ones-iii/) · [Solution file (no hints)](../../problems/1000-1499/1004.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given a binary array `nums` and an integer `k`, return the **maximum number of consecutive `1`s** in the array if you can flip at most `k` `0`s.

```
nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2        →  6    (flip the two 0s at indices 4,5)
nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3  →  10
```

**Constraints:** `1 <= nums.length <= 10⁵` · `nums[i]` is `0` or `1` · `0 <= k <= nums.length`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**consecutive**" | A contiguous window |
| "flip **at most `k`** zeros" | A **budget**. The window is valid while it contains ≤ `k` zeros |
| "**maximum** number" | Maximize the window length — so grow greedily and shrink only when forced |
| "at most", not "exactly" | Using fewer flips is fine; no need to consume the whole budget |
| `k` can be **0** | Then it's just the longest run of 1s — must work with no special case |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead |

**The reframe that makes this trivial.** Don't think about *flipping*. Think about what a valid window looks like:

> Find the **longest window containing at most `k` zeros.**

You never actually flip anything — a window with ≤ `k` zeros *could* be made all-1s, and its length is the answer for that window. The flipping is narrative; the constraint is a counter.

That turns it into the standard variable-size sliding window with a **budget condition**:

```
for right in range(n):
    include nums[right]                 # grow
    while budget exceeded:
        exclude nums[left]; left += 1   # shrink until valid again
    record window length                # always valid here
```

**Note the contrast with [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md).** There you *minimized*, so you recorded **inside** the shrink loop while the window was valid and shrank aggressively. Here you *maximize*, so you shrink only as much as necessary and record **after** the loop, once validity is restored. Same skeleton, mirrored bookkeeping — and getting that backwards is the most common way to break either problem.

| | Goal | Shrink when | Record |
|---|---|---|---|
| [209](209-minimum-size-subarray-sum.md) | minimize | window is **valid** | inside the `while` |
| **1004** | maximize | window is **invalid** | after the `while` |

🤔 **Before you open the next section:** if your window has too many zeros, which end do you shrink from, and how far?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(start, end)`, count zeros | O(n²) | O(1) | ❌ 10¹⁰ |
| Prefix zero-counts + binary search | For each end, binary search the furthest valid start | O(n log n) | O(n) | ⚠️ Correct, slower |
| **Sliding window** | Grow right; shrink left while zeros > `k` | **O(n)** | **O(1)** | ✅ |
| "Never shrink" window | Grow right; move left only in lockstep when invalid | **O(n)** | O(1) | ✅ A neat variant — see below |

**The decision: a variable-size sliding window tracking a zero count.**

State is just one integer: `zeros`, how many zeros are inside `[left, right]`. The rules:

- **Grow:** `right` advances; if `nums[right] == 0`, `zeros += 1`
- **Shrink:** while `zeros > k`, advance `left`, decrementing `zeros` when the departing element was a zero
- **Record:** after the shrink loop, the window is valid, so `right - left + 1` is a candidate

**Why the greedy shrink is correct.** When the window becomes invalid, you must move `left` — and moving it past a zero is the *only* thing that restores validity. Shrinking exactly until valid keeps the window as long as possible for this `right`. Any further shrink would only lose length; any less and it's still invalid.

**Why only `left` moves forward and never back.** Suppose the longest valid window ending at `right` starts at `left`. For `right + 1`, the best start can never be *earlier* than `left` — adding an element can only add zeros, never remove them. So `left` is monotonically non-decreasing, which is what makes the whole thing O(n).

**The "never shrink" variant**, worth knowing because it appears in a lot of published solutions:

```python
left = 0
for right in range(len(nums)):
    if nums[right] == 0:
        k -= 1
    if k < 0:                      # if instead of while
        if nums[left] == 0:
            k += 1
        left += 1
return len(nums) - left
```

Here the window **never shrinks** — it only ever slides or grows. Since we're maximizing, once we've achieved some length we never need a shorter window, so `left` and `right` can move in lockstep whenever validity breaks. The answer is the final window width. It's clever and O(n) with a single `if`, but the explicit `while` version is easier to explain and to get right under pressure. Mention it; write the clear one.

**Why not prefix counts + binary search?** It works — prefix zero-counts are non-decreasing, so you can binary search the earliest valid start for each end — but it's O(n log n) time and O(n) space to do what a window does in O(n)/O(1).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
zeros = 0
res = 0
```

- `left` — the window's left edge
- `zeros` — how many zeros are currently inside the window (the budget consumed)
- `res` — the longest valid window seen

Starting `res` at 0 is correct: if every window were invalid — impossible here, since a single `1` or an empty window is always valid — 0 would be the honest answer.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for right in range(len(nums)):
    if nums[right] == 0:
        zeros += 1
```

**Grow.** Extend the window; if the incoming element is a zero, it consumes budget.
→ [range-function](../syntax/range-function.md)

```python
    while zeros > k:
        if nums[left] == 0:
            zeros -= 1
        left += 1
```

**Shrink until valid.** While the budget is exceeded, drop elements from the left, recovering budget whenever a zero leaves.

**`while`, not `if`** — for the explicit version. (Since only one zero enters per step, a single shrink *would* suffice here, which is exactly why the "never shrink" variant works. But writing `while` is the habit that transfers to problems like [Fruit Into Baskets](904-fruit-into-baskets.md) where several shrinks per step are genuinely needed.)

The condition is `zeros > k`, not `>=` — a window with **exactly** `k` zeros is valid, since `k` flips are permitted.
→ [while-loop](../syntax/while-loop.md)

```python
    res = max(res, right - left + 1)
```

**Record after the shrink loop**, when the window is guaranteed valid.

`right - left + 1` is the inclusive length. Recording *inside* the shrink loop would measure invalid windows — the mirror-image mistake to [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md), where inside is correct.
→ [min-max-key](../syntax/min-max-key.md)

```python
return res
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:

        left = 0
        zeros = 0
        res = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                zeros += 1

            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1

            res = max(res, right - left + 1)

        return res
```

</details>

**Trace it** — `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`:

| `right` | `nums[r]` | `zeros` | Shrink? | `left` | Window | Length | `res` |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | no | 0 | `[1]` | 1 | 1 |
| 1 | 1 | 0 | no | 0 | `[1,1]` | 2 | 2 |
| 2 | 1 | 0 | no | 0 | `[1,1,1]` | 3 | 3 |
| 3 | **0** | 1 | no (1 ≤ 2) | 0 | `[1,1,1,0]` | 4 | 4 |
| 4 | **0** | 2 | no (2 ≤ 2) | 0 | `[1,1,1,0,0]` | 5 | 5 |
| 5 | **0** | 3 | **yes** → drop `nums[0]=1` | 1 | zeros still 3 → drop `nums[1]=1` | | |
| | | 3 | → drop `nums[2]=1`, `left=3` | 3 | zeros still 3 → drop `nums[3]=0`, `zeros=2`, `left=4` | `[0,0]` | 2 | 5 |
| 6 | 1 | 2 | no | 4 | `[0,0,1]` | 3 | 5 |
| 7 | 1 | 2 | no | 4 | `[0,0,1,1]` | 4 | 5 |
| 8 | 1 | 2 | no | 4 | `[0,0,1,1,1]` | 5 | 5 |
| 9 | 1 | 2 | no | 4 | `[0,0,1,1,1,1]` | **6** | **6** |
| 10 | **0** | 3 | yes → drop `nums[4]=0`, `zeros=2`, `left=5` | 5 | `[0,1,1,1,1,0]` | 6 | 6 |

Return **6** ✅ — the window `[0,0,1,1,1,1]` at indices 4–9, where flipping both zeros yields six consecutive 1s.

Row 5 shows the `while` shrinking four times in one step — evidence that the shrink loop can do real work even when only one zero entered.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Outer loop: exactly `n` iterations.
- Inner `while`: `left` only ever advances and never resets, so across the entire run it moves at most `n` times **in total**.

Every element enters the window once (via `right`) and leaves at most once (via `left`), giving at most `2n` pointer movements — **O(n)**.

**Say it out loud like this:** *"It looks nested, but the left pointer is monotonic — it never goes backward and never resets — so total inner work is bounded by n."*

The same amortized argument as [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md), [Longest Consecutive Sequence](128-longest-consecutive-sequence.md), and [First Missing Positive](41-first-missing-positive.md). Once you recognize the shape, you stop being fooled by nested loops.

**Compare:** brute force is O(n²) = 10¹⁰; prefix + binary search is O(n log n). The window is optimal — you must read every element.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers, regardless of `n`.

The prefix-count alternative would need O(n) for the array. The window needs nothing beyond a counter, because the only thing it must remember about the window is **how many zeros are in it** — not *which* ones, or where.

That compression is the key observation:

> **A sliding window only needs enough state to test validity and to update it as elements enter and leave.** Here that's a single integer.

Contrast with [Fruit Into Baskets](904-fruit-into-baskets.md), where validity depends on the *number of distinct values*, requiring a frequency map — O(1) there too, but only because the value set is bounded. And with [Sliding Window Maximum](239-sliding-window-maximum.md), where the maintained quantity (a maximum) can't be updated on removal at all, forcing a monotonic deque.

**Choosing the right window state is most of the work in any sliding-window problem.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'd reframe it: rather than thinking about flipping, find the longest window containing at most `k` zeros — any such window can be made all-1s. So it's a variable-size sliding window with a budget. I grow with a right pointer, incrementing a zero count when a zero enters. If the count exceeds `k`, I shrink from the left until it's valid again, recovering budget when a zero leaves. Then I record the length, after the shrink, when the window is guaranteed valid. It's O(n) because the left pointer only moves forward and never resets. O(1) space, since all I need to track is the zero count."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [209](209-minimum-size-subarray-sum.md)?" | **The key contrast.** 209 minimizes: shrink while *valid*, record *inside*. This maximizes: shrink while *invalid*, record *after*. Same skeleton, mirrored. |
| "What if `k = 0`?" | Longest run of 1s. Works unchanged — any zero immediately forces a shrink past it. |
| "Return the **indices** of the flipped zeros." | Track the best `(left, right)` and re-scan that window for zeros. |
| "Flip at most `k` ones to get consecutive **zeros**?" | Symmetric — count ones instead. |
| "Longest window with at most `k` **distinct** values?" | [Fruit Into Baskets](904-fruit-into-baskets.md) generalized — swap the counter for a frequency map. |
| "Can you avoid the shrink loop?" | Yes — the "never shrink" variant moves `left` in lockstep with `right` using a single `if`, returning `n - left`. O(n), one pass, fewer branches. |
| "What if flips were **expensive** and you wanted to minimize them?" | Different objective entirely — you'd want the shortest window achieving a target length, or a cost-based DP. |

**Traps:**

- **Recording inside the shrink loop.** Measures invalid windows. This is correct for [209](209-minimum-size-subarray-sum.md) and wrong here — know which problem you're in.
- **Using `zeros >= k` as the shrink condition.** Exactly `k` zeros is valid; `>=` shrinks one step too eagerly and under-reports by one.
- **Decrementing `zeros` unconditionally when shrinking.** Only decrement when the *departing* element is a zero.
- **Advancing `left` before checking `nums[left]`.** You must inspect the element before moving past it.
- **Resetting `left = 0`** each outer iteration — that's the O(n²) brute force.
- **Actually flipping the array.** Unnecessary and destructive; the count is all you need.

**This same move shows up in:** [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) (the minimizing mirror image) · [Longest Subarray of 1's After Deleting One Element](1493-longest-subarray-of-1s-after-deleting-one-element.md) (this problem with `k = 1` and a `-1` on the answer) · [Fruit Into Baskets](904-fruit-into-baskets.md) (same skeleton, distinct-count validity) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (same budget idea over character frequencies).

</details>

---
