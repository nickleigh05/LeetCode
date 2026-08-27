# 1493. Longest Subarray of 1's After Deleting One Element

**Medium** · [LeetCode](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) · [Solution file (no hints)](../../problems/1000-1499/1493.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given a binary array `nums`, you must **delete exactly one element**. Return the size of the longest non-empty subarray containing only `1`s in the resulting array. Return `0` if none exists.

```
nums = [1,1,0,1]        →  3    (delete the 0 → [1,1,1])
nums = [0,1,1,1,0,1,1,0,1]  →  5
nums = [1,1,1]          →  2    (must delete one, even though all are 1s)
```

**Constraints:** `1 <= nums.length <= 10⁵` · `nums[i]` is `0` or `1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "delete **exactly one**" | ⚠️ **Mandatory, not optional.** Even an all-1s array loses one element — that's the edge case people miss |
| "only `1`s" in the result | The remaining window must be pure 1s after the deletion |
| "**non-empty**" | Return 0 if nothing survives, e.g. `[0,0]` or `[1]` |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead |
| binary array | Only 0s and 1s, so "how many zeros" is the only state you need |

This is [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) with **`k = 1`**, plus one twist.

Reframe it the same way: a window containing **at most one zero** can be turned into all 1s by deleting that zero. So find the longest such window.

**The twist — why the answer is `length - 1`:**

You must delete exactly one element, so the surviving run is one shorter than the window. Two cases, and they unify:

| Window | Zeros | After deleting one element | Length |
|---|---|---|---|
| `[1,1,0,1]` | 1 | delete the `0` → `[1,1,1]` | `4 - 1 = 3` ✅ |
| `[1,1,1]` | 0 | must delete a `1` → `[1,1]` | `3 - 1 = 2` ✅ |

In the first case the deletion is "free" — you remove the zero that was blocking you. In the second there's no zero to remove, so the mandatory deletion costs you a real `1`. **Subtracting 1 from the window length handles both**, with no branching.

That's the elegant part: the `-1` isn't a special case for all-1s input, it's the uniform accounting for "exactly one deletion."

🤔 **Before you open the next section:** if your window has at most one zero, how long is the run of 1s you end up with — and does the answer change when the window has no zeros at all?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Delete each index, scan for the longest run | O(n²) | O(1) | ❌ 10¹⁰ |
| Track runs around each zero | For each zero, sum the runs on either side | O(n) | O(n) | ✅ Correct, more bookkeeping |
| **Sliding window, ≤ 1 zero** | Grow right, shrink while zeros > 1, record `len - 1` | **O(n)** | **O(1)** | ✅ |

**The decision: the [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) window with `k = 1` and a `-1` on the recorded length.**

Recognizing it as an instance of a problem you already know is the whole move. The skeleton is identical:

- **Grow:** `right` advances; count zeros entering
- **Shrink:** while `zeros > 1`, advance `left`, decrementing on departing zeros
- **Record:** after shrinking, `window_length - 1`

**Why `zeros > 1` and not `> 0`?** A window may contain **one** zero — that's the one you delete. Only a second zero makes it invalid.

**Why record after the shrink?** Same as [1004](1004-max-consecutive-ones-iii.md): we're maximizing, so we shrink only as far as necessary and measure once the window is valid again. (Contrast [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md), which minimizes and records inside the shrink loop.)

**Why the `-1` can't produce a wrong negative.** The smallest a valid window can be is 1 (a single element), giving `1 - 1 = 0` — exactly the "return 0" case the problem specifies for inputs like `[1]` or `[0]`. The arithmetic degrades gracefully with no guard needed.

**The alternative — runs around zeros.** Precompute, for each position, the length of the run of 1s ending there and starting there. Then for each zero, the answer candidate is `left_run + right_run`. Also O(n), also correct, but it needs two auxiliary arrays (O(n) space) and careful handling of the no-zeros case. The window is tighter and reuses machinery you already have.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
zero_count = 0
max_length = 0
```

Standard variable-window state: the left edge, the number of zeros inside, and the best answer.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for right in range(len(nums)):
    if nums[right] == 0:
        zero_count = zero_count + 1
```

**Grow.** Extend right; track a zero entering the window.
→ [range-function](../syntax/range-function.md)

```python
    while zero_count > 1:
        if nums[left] == 0:
            zero_count = zero_count - 1
        left = left + 1
```

**Shrink until at most one zero remains.**

`> 1`, not `> 0` — one zero is permitted, because that's the element you'll delete. Decrement only when the *departing* element is actually a zero.
→ [while-loop](../syntax/while-loop.md)

```python
    window_length = right - left + 1
    max_length = max(max_length, window_length - 1)
```

**Record, minus one.**

`right - left + 1` is the inclusive window length. The `- 1` accounts for the mandatory deletion — and, as shown above, it's correct whether the window contains a zero (delete it, free) or is all 1s (delete a 1, costly).

Naming `window_length` before subtracting makes the reasoning legible; folding it into one expression works but hides the `-1`, which is precisely the line a reader needs to notice.
→ [min-max-key](../syntax/min-max-key.md)

```python
return max_length
```

Starting at 0 and never going negative means the "no valid subarray" case returns 0 automatically.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:

        left = 0
        zero_count = 0
        max_length = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count = zero_count + 1

            while zero_count > 1:
                if nums[left] == 0:
                    zero_count = zero_count - 1
                left = left + 1

            window_length = right - left + 1
            max_length = max(max_length, window_length - 1)

        return max_length
```

</details>

**Trace it** — `nums = [0,1,1,1,0,1,1,0,1]`:

| `right` | `nums[r]` | `zeros` | Shrink? | `left` | Window | Len | Len−1 | `max` |
|---|---|---|---|---|---|---|---|---|
| 0 | **0** | 1 | no | 0 | `[0]` | 1 | 0 | 0 |
| 1 | 1 | 1 | no | 0 | `[0,1]` | 2 | 1 | 1 |
| 2 | 1 | 1 | no | 0 | `[0,1,1]` | 3 | 2 | 2 |
| 3 | 1 | 1 | no | 0 | `[0,1,1,1]` | 4 | 3 | 3 |
| 4 | **0** | 2 | **yes** → drop `nums[0]=0`, `zeros=1`, `left=1` | 1 | `[1,1,1,0]` | 4 | 3 | 3 |
| 5 | 1 | 1 | no | 1 | `[1,1,1,0,1]` | 5 | 4 | 4 |
| 6 | 1 | 1 | no | 1 | `[1,1,1,0,1,1]` | **6** | **5** | **5** |
| 7 | **0** | 2 | yes → drop `nums[1]=1`, `nums[2]=1`, `nums[3]=1`, `nums[4]=0` → `zeros=1`, `left=5` | 5 | `[1,1,0]` | 3 | 2 | 5 |
| 8 | 1 | 1 | no | 5 | `[1,1,0,1]` | 4 | 3 | 5 |

Return **5** ✅ — the window at indices 1–6 (`[1,1,1,0,1,1]`), where deleting the zero yields five consecutive 1s.

**The all-ones case** — `nums = [1,1,1]`:

| `right` | `zeros` | Window | Len | Len−1 | `max` |
|---|---|---|---|---|---|
| 0 | 0 | `[1]` | 1 | 0 | 0 |
| 1 | 0 | `[1,1]` | 2 | 1 | 1 |
| 2 | 0 | `[1,1,1]` | 3 | **2** | **2** |

Return **2** ✅ — the mandatory deletion costs a real `1`, and the `-1` accounts for it with no special case.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Outer loop runs `n` times. The inner `while` looks nested, but `left` only advances and never resets, so it moves at most `n` times **across the entire run**.

Every element enters via `right` once and leaves via `left` at most once — at most `2n` pointer movements, so **O(n)**.

The same amortized argument as [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) and [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md).

**Compare to brute force:** O(n²) — delete each of `n` elements and scan `n` for the longest run — 10¹⁰ at the constraint limit.

Optimal, since every element must be read.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers.

The window's entire state is a single counter, because the only validity question is *"how many zeros are inside?"* — never *which* zeros or *where*.

The runs-around-zeros alternative needs two O(n) auxiliary arrays for the same result. The window wins on both space and simplicity, which is a good illustration of the general principle:

> **Prefer the formulation whose state is smallest.** If validity can be tested with a counter, you don't need arrays.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Max Consecutive Ones III with `k = 1`, plus one adjustment. A window with at most one zero can be made all-1s by deleting that zero, so I slide a window and shrink whenever it holds two zeros. The twist is that the deletion is **mandatory**, so the answer for a window is its length minus one — which is also correct when the window has no zeros at all, since I'd then have to delete a real 1. That single `-1` handles both cases with no branching, and it can't go negative because the smallest valid window has length 1, giving 0. O(n) time — the left pointer never resets — and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if deletion were **optional**?" | Then it's exactly [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) with `k = 1` and no `-1`. `[1,1,1]` would return 3. |
| "Delete at most **`k`** elements?" | Generalize to `zeros > k` and record `length - 1`… but careful: with optional deletion it's just [1004](1004-max-consecutive-ones-iii.md). Clarify whether deletions are mandatory. |
| "Why does `-1` work for all-1s input?" | You must delete something. With no zero available, you sacrifice a 1 — and `length - 1` is exactly that. |
| "Can the answer be negative?" | No. The smallest valid window is length 1 → `0`, which is the specified return for no valid subarray. |
| "Return the deleted index." | Track the best window and locate its zero; if there is none, any index in the window works. |
| "What about `[0,0]`?" | Every window has ≤1 zero after shrinking, max length 1, so `1 - 1 = 0` ✅ |
| "Solve it without a window." | For each zero, add the run of 1s immediately before and after it. O(n) time but O(n) space and fiddlier edge cases. |

**Traps:**

- **Forgetting the `-1`.** Returns `length` and fails `[1,1,1]` (gives 3, should be 2). *The* bug for this problem.
- **Special-casing the all-1s input.** Unnecessary — the `-1` already handles it. Adding a branch usually introduces a new bug.
- **Using `zero_count > 0` as the shrink condition.** One zero is allowed; `> 0` reduces it to "longest run of 1s" and under-reports.
- **Recording inside the shrink loop.** Measures invalid windows — correct for [209](209-minimum-size-subarray-sum.md), wrong here.
- **Decrementing `zero_count` unconditionally.** Only when the departing element is a zero.
- **Worrying about a negative result.** It can't happen; no guard needed.

**This same move shows up in:** [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) (the general-`k` version this specializes) · [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) (the minimizing mirror of the same skeleton) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (a budget window over character frequencies) · [Fruit Into Baskets](904-fruit-into-baskets.md) (validity by distinct-value count).

</details>

---
