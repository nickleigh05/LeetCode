# 209. Minimum Size Subarray Sum

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-size-subarray-sum/) · [Solution file (no hints)](../../problems/0001-0499/209.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given an array of **positive** integers `nums` and a positive integer `target`, return the **minimal length** of a contiguous subarray whose sum is **≥ `target`**. If no such subarray exists, return `0`.

```
target = 7,  nums = [2,3,1,2,4,3]        →  2    ([4,3])
target = 4,  nums = [1,4,4]              →  1    ([4])
target = 11, nums = [1,1,1,1,1,1,1,1]    →  0    (total is only 8)
```

**Constraints:** `1 <= target <= 10⁹` · `1 <= nums.length <= 10⁵` · `1 <= nums[i] <= 10⁴`

**Follow-up:** if you've solved it in O(n), try the O(n log n) version.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**positive** integers" | ⚠️ **The enabling constraint.** Sums are strictly increasing as the window grows — that monotonicity is what makes a sliding window valid |
| "sum **≥ target**" | Not equal — once you're over, you're done and can start shrinking |
| "**minimal length**" | Minimize, so shrink aggressively whenever the window is still valid |
| "return `0` if none" | Total sum below target must return 0, not crash or return infinity |
| "**contiguous**" | A window, not a subsequence |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead |
| follow-up: **O(n log n)** | Hints at prefix sums + binary search, which is *worse* here but generalizes to negatives |

**Why "positive" is the whole ballgame.** Compare with [Subarray Sum Equals K](560-subarray-sum-equals-k.md), which allows negatives and therefore *cannot* use a window. With all values positive:

- Extending the window right **always increases** the sum
- Shrinking from the left **always decreases** it

That gives you a decision rule: *sum too small ⇒ grow right; sum big enough ⇒ record and shrink left*. With negatives, extending might decrease the sum, so "too small" wouldn't tell you which way to move, and the whole technique collapses.

**The variable-size window shape.** Unlike [Maximum Average Subarray I](643-maximum-average-subarray-i.md), the window here has no fixed length. The pattern is:

```
for right in range(n):
    add nums[right] to the window
    while window is valid:
        record the answer
        shrink from the left
```

Note the `while` — not `if`. Once the window is valid, you may be able to shrink several times before it becomes invalid, and each intermediate size is a candidate.

🤔 **Before you open the next section:** once your window's sum reaches the target, why is it correct to immediately try shrinking rather than continuing to grow?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(start, end)` pair, sum it | O(n³) | O(1) | ❌ Hopeless |
| Brute force + running sum | Every start, extend accumulating | O(n²) | O(1) | ❌ 10¹⁰ |
| **Sliding window** | Grow right, shrink left while valid | **O(n)** | **O(1)** | ✅ |
| Prefix sums + binary search | For each start, binary search the end | O(n log n) | O(n) | ✅ The follow-up; generalizes to negatives |

**The decision: a variable-size sliding window with two pointers.**

- `right` grows the window, adding elements
- `left` shrinks it, removing elements — but only while the window remains valid

**Why shrinking immediately is correct.** Suppose the window `[left, right]` has sum ≥ target. Any *larger* window ending at `right` is also valid but longer, so it can't beat what you have. The only way to find something shorter ending at `right` is to move `left` inward. So shrink as far as possible, recording the length at each step, and stop when the sum drops below target — at which point no shorter window ending at `right` exists.

**Why record *before* shrinking.** In the solution's loop, `min_len` is updated at the top of the `while` body, while the window is still valid. Shrink first and you'd measure an invalid window.

**Why it's O(n) despite the nested loop** — the amortized argument, which you must be ready to give:

> `left` only ever moves **forward**, and never past `right`. Across the entire run it advances at most `n` times *in total*. So the inner `while` executes at most `n` times summed over all iterations of the outer loop — not `n` times per iteration.

Total: `n` right-moves + at most `n` left-moves = **O(n)**. Same shape of reasoning as [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) and [First Missing Positive](41-first-missing-positive.md) — a nested loop with a *global* work budget.

**The O(n log n) follow-up.** Build a prefix-sum array (strictly increasing, because values are positive), then for each start `i` binary search for the smallest `j` with `prefix[j] - prefix[i] >= target`. O(n) starts × O(log n) search = O(n log n), plus O(n) space.

It's **worse than the window here** — so why does the problem ask for it? Because it doesn't depend on the shrink rule, only on prefix sums being sorted. It's the technique that survives when the window doesn't, and knowing why one is faster while the other is more general is exactly the kind of judgment being tested.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — sliding window** (the O(n) answer)

```python
left = 0
window_sum = 0
min_len = float("inf")
```

- `left` — the window's left edge
- `window_sum` — running sum of `nums[left..right]`
- `min_len` — best length so far; **infinity** as the sentinel for "nothing found yet," so any real length beats it

Using `float("inf")` rather than a large constant makes the "no answer" case unambiguous and self-documenting.
→ [float-inf](../syntax/float-inf.md)

```python
for right in range(len(nums)):
    window_sum += nums[right]
```

**Grow.** Extend the window by one on the right and add its value.
→ [range-function](../syntax/range-function.md)

```python
    while window_sum >= target:
```

**`while`, not `if` — this is the crux of the variable-size window.**

After adding one element the window may be shrinkable **several** times before it becomes invalid. Consider `target = 4` with the window `[1,1,1,4]`: after adding `4` you can drop three elements and still be valid, and the answer is the final length of 1. An `if` would shrink once, record 4, and miss it entirely.
→ [while-loop](../syntax/while-loop.md)

```python
        min_len = min(min_len, right - left + 1)
```

**Record before shrinking**, while the window is still valid.

`right - left + 1` is the inclusive window length — the `+ 1` is the standard fencepost. For `left = 4, right = 5` that's 2 elements ✅
→ [min-max-key](../syntax/min-max-key.md)

```python
        window_sum -= nums[left]
        left += 1
```

**Shrink.** Remove the leftmost element's contribution, then advance the edge. The order matters: subtract the value at `left` *before* moving past it.

```python
return 0 if min_len == float("inf") else min_len
```

**Translate the sentinel.** If `min_len` was never updated, no valid window existed, and the problem asks for `0` rather than infinity.
→ [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        left = 0
        window_sum = 0
        min_len = float("inf")

        for right in range(len(nums)):
            window_sum += nums[right]

            while window_sum >= target:
                min_len = min(min_len, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return 0 if min_len == float("inf") else min_len
```

</details>

---

**Approach B — prefix sums + binary search** (the O(n log n) follow-up)

```python
n = len(nums)
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + nums[i]
```

Standard prefix sums with the leading-zero sentinel — see [Range Sum Query - Immutable](303-range-sum-query-immutable.md). Because all values are positive, `prefix` is **strictly increasing**, which is precisely what makes it binary-searchable.

```python
min_len = float("inf")
for i in range(n):
    needed = target + prefix[i]
    lo, hi = i + 1, n
    while lo <= hi:
        ...
```

For each start `i`, find the smallest `j` with `prefix[j] >= target + prefix[i]` — equivalent to `sum(i..j-1) >= target`. Binary search over the sorted prefix array.
→ [binary-search](../algorithms/binary-search.md) · [bisect-module](../syntax/bisect-module.md)

**Trace approach A** — `target = 7`, `nums = [2,3,1,2,4,3]`:

| `right` | `nums[right]` | `window_sum` | Window | ≥ 7? | Record | Shrink → new state |
|---|---|---|---|---|---|---|
| 0 | 2 | 2 | `[2]` | no | — | — |
| 1 | 3 | 5 | `[2,3]` | no | — | — |
| 2 | 1 | 6 | `[2,3,1]` | no | — | — |
| 3 | 2 | 8 | `[2,3,1,2]` | ✅ | len **4** | drop 2 → sum 6, `left=1` |
| 3 | — | 6 | `[3,1,2]` | no | — | — |
| 4 | 4 | 10 | `[3,1,2,4]` | ✅ | len **4** | drop 3 → sum 7, `left=2` |
| 4 | — | 7 | `[1,2,4]` | ✅ | len **3** | drop 1 → sum 6, `left=3` |
| 4 | — | 6 | `[2,4]` | no | — | — |
| 5 | 3 | 9 | `[2,4,3]` | ✅ | len 3 | drop 2 → sum 7, `left=4` |
| 5 | — | 7 | `[4,3]` | ✅ | len **2** ⭐ | drop 4 → sum 3, `left=5` |
| 5 | — | 3 | `[3]` | no | — | — |

Return **2** ✅

Rows 6–8 and 9–11 show the `while` shrinking **multiple times** per outer iteration — an `if` would have stopped at length 4 and 3 respectively, missing the answer of 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The outer `for` runs exactly `n` times.
- The inner `while` looks like it could nest — but `left` only moves **forward**, never resets, and never exceeds `right`. So across the entire run it advances at most `n` times **in total**.

Total: `n` additions + at most `n` subtractions = **O(n)**. Each element enters the window exactly once and leaves at most once.

**Say it out loud like this:** *"Nested loops, but the left pointer only moves forward and never resets, so total inner iterations are bounded by n — it's amortized O(n), not O(n²)."*

**Compare:**

| | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| **Sliding window** | **O(n)** | **O(1)** |
| Prefix + binary search | O(n log n) | O(n) |

The window is optimal on both axes — the follow-up's O(n log n) is genuinely slower, and worth being explicit about. Its value is generality, not speed.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** for the sliding window — three variables, no allocation.

**O(n)** for the prefix-sum version, which needs the full array to binary search over.

**Why the window wins here, and when it wouldn't:**

| | Requires | Handles negatives? |
|---|---|---|
| Sliding window | monotonic sums (all positive) | ❌ |
| Prefix + binary search | monotonic **prefix array** (all positive) | ❌ |
| Prefix + hash map | nothing | ✅ (but answers a different question) |

Both approaches here lean on positivity. If negatives were allowed, neither works for "minimum length with sum ≥ target" — you'd need a monotonic deque over prefix sums ([LeetCode 862](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/), which is genuinely Hard).

That's the sentence to have ready: **the sign constraint is what selects the technique**, and the same surface question becomes a much harder problem without it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "All values are positive, so growing the window strictly increases the sum and shrinking strictly decreases it — that monotonicity is what makes a sliding window valid. I grow with a right pointer, and whenever the sum reaches the target I record the length and shrink from the left, using a `while` because I may be able to shrink several times before the window becomes invalid. Recording happens before each shrink, while the window is still valid. It's O(n) because the left pointer only moves forward and never resets, so total inner iterations are bounded by n. O(1) space, and I return 0 if the sentinel infinity was never replaced. The O(n log n) follow-up uses prefix sums plus binary search — slower here, but it's the version that generalizes."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "The O(n log n) version?" | **The stated follow-up.** Prefix sums are strictly increasing with positive values, so binary search the smallest `j` with `prefix[j] - prefix[i] >= target` for each `i`. |
| "What if values can be **negative**?" | Both approaches break — sums stop being monotonic. Needs a monotonic deque over prefix sums ([LC 862](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)), a Hard problem. |
| "Sum **exactly** equal to target?" | Different problem — [Subarray Sum Equals K](560-subarray-sum-equals-k.md), prefix sums + hash map. |
| "**Maximum** length with sum ≤ target?" | Same window, inverted: shrink while the sum *exceeds* target, and record after shrinking, when the window is valid. |
| "Return the subarray itself." | Track the `(left, right)` pair whenever `min_len` improves. |
| "Why `while` and not `if`?" | Multiple shrinks can be possible after one growth. `target=4, nums=[1,1,1,4]` returns 4 with `if`, 1 with `while`. |
| "Why is it O(n) with nested loops?" | `left` moves forward only and never resets — at most `n` total advances. |

**Traps:**

- **Using `if` instead of `while`.** *The* bug for variable-size windows. Produces answers that are too large, and looks plausible.
- **Recording after shrinking.** Measures an invalid window; off by one or worse.
- **Forgetting the sentinel translation.** Returning `inf` instead of `0` when no window qualifies.
- **`right - left`** instead of `right - left + 1`. Inclusive bounds need the `+ 1`.
- **Subtracting after advancing `left`.** You must remove `nums[left]` before moving past it.
- **Resetting `left = 0`** on each outer iteration. That's the O(n²) brute force in disguise.
- **Assuming a window works with negatives.** Check the sign constraint before choosing the technique — it's the single most important line in the statement.

**This same move shows up in:** [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (variable window, shrink on a duplicate) · [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) (variable window, shrink when a budget is exceeded) · [Fruit Into Baskets](904-fruit-into-baskets.md) (variable window, shrink on too many distinct values) · [Minimum Window Substring](76-minimum-window-substring.md) (the Hard version — same grow/shrink skeleton with a frequency-match condition).

</details>

---
