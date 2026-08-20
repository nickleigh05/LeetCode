# 53. Maximum Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-subarray/) · [Solution file (no hints)](../../problems/0001-0499/53.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Greedy problems](../rmap-practice/16-greedy.md)

---

Given an integer array `nums`, find the **contiguous subarray** with the **largest sum** and return that sum. The subarray must contain at least one element.

```
nums = [-2,1,-3,4,-1,2,1,-5,4]   →  6      [4,-1,2,1]
nums = [1]                       →  1
nums = [5,4,-1,7,8]              →  23     the whole array
nums = [-3,-1,-2]                →  -1     all negative — the best is the least bad
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-10⁴ <= nums[i] <= 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**contiguous** subarray" | No skipping. There are O(n²) subarrays, defined by a start and an end — not 2ⁿ subsets |
| "**largest sum**" | Optimization → `max`. And sums, not products, which matters: sums don't have the sign-flip behaviour of [Maximum Product Subarray](152-maximum-product-subarray.md) |
| "at least one element" | The empty subarray (sum 0) is **not** allowed. That's why the all-negative case answers `-1`, not `0` — a real trap |
| values can be **negative** | Which is the entire problem. With all-positive input the answer is trivially the whole array |
| `n <= 10⁵` | n² = 10¹⁰ — dead. **O(n) or O(n log n) required** |

The insight comes from asking a very specific question. Consider every subarray by **where it ends**, and define:

> `best_ending_here(i)` = the largest sum of any subarray that ends exactly at index `i`.

Now, what are the options for that subarray? It either:
- **extends** the best subarray ending at `i-1`, giving `best_ending_here(i-1) + nums[i]`, or
- **starts fresh** at `i`, giving just `nums[i]`.

There is no third case, because a subarray ending at `i` and containing more than one element *must* contain `i-1`.

```
best_ending_here(i) = max( nums[i],  best_ending_here(i-1) + nums[i] )
```

And the answer is the maximum of `best_ending_here` over all `i`.

Now the greedy reading of that same recurrence, which is why this problem sits in the Greedy unit rather than DP. `cur_sum + nums[i]` beats `nums[i]` exactly when `cur_sum > 0`. So the rule is simply:

> **If the running sum ever goes negative, throw it away.**

A negative prefix can only *reduce* whatever follows it. Carrying it forward is strictly worse than starting over — so you drop it, immediately and without regret. **That's the greedy choice, and its justification is one sentence.**

🤔 **Before you open the next section:** this is [Kadane's algorithm](../algorithms/kadane-algorithm.md), and it's usually called DP. But it's also purely greedy. What makes it both — and is there a meaningful difference here?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Every subarray, summed | Two nested loops for start/end, plus a third to sum | **O(n³)** | O(1) | ❌ 10¹⁵ |
| Every subarray, running sum | Two loops, extending the sum as you go | **O(n²)** | O(1) | ❌ 10¹⁰ |
| Prefix sums | `sum(i..j) = prefix[j] - prefix[i-1]`; track the minimum prefix seen | O(n) | O(1) | ✅ Correct, and a genuinely different derivation |
| Divide and conquer | Best in left half, right half, or crossing the middle | O(n log n) | O(log n) | ⚠️ Correct and instructive — but slower, and the one they'll ask about as a follow-up |
| **[Kadane's algorithm](../algorithms/kadane-algorithm.md)** | Extend or restart at each element; drop a negative running sum | **O(n)** | **O(1)** | ✅ |

**The decision:** [Kadane's algorithm](../algorithms/kadane-algorithm.md) — one pass, two variables.

**Why the greedy is provably safe**, which is the thing to be able to justify. Suppose the running sum going into index `i` is negative. Any subarray that starts before `i` and extends past it must include that negative prefix, so it is **strictly worse** than the same subarray with the prefix removed. There is therefore never a reason to keep a negative running sum. **The local decision — drop it — can never cost you the global optimum.** That's the exchange argument, and it's what separates a valid greedy from a hopeful one.

Contrast [Maximum Product Subarray](152-maximum-product-subarray.md), where the analogous greedy **fails**: a very negative running *product* is valuable, because one more negative flips it to a large positive. **Sums have no such reversal**, which is exactly why 53 is O(1) state and 152 needs two running values.

**Is it greedy or DP?** (Section 1's question.) Both, honestly. The recurrence `best(i) = max(nums[i], best(i-1) + nums[i])` is textbook DP with a one-cell lookback — and applying the rolling-variable collapse from [Climbing Stairs](70-climbing-stairs.md) reduces it to O(1) space. But because the window is a single cell, the "table" is one number, and the decision at each step is a local, irrevocable choice. **When a DP's lookback shrinks to one cell and the choice is never revisited, it *is* a greedy algorithm.** Kadane's sits exactly on that boundary, which is why textbooks disagree about which chapter it belongs in.

**Why not divide and conquer?** It's a legitimate O(n log n) solution and a classic teaching example — split the array, and the answer is the best in the left half, the best in the right half, or the best subarray *crossing* the midpoint (computed by extending outward from the middle). Worth being able to describe, since it's a common follow-up. But it's asymptotically worse and much longer to write.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
max_sum = nums[0]
cur_sum = nums[0]
```
Two running values, both seeded with the **first element** rather than 0.

- `cur_sum` — the best sum of a subarray **ending at the current index**.
- `max_sum` — the best sum seen **anywhere** so far.

Seeding with `nums[0]` rather than `0` is what makes the all-negative case work. With `[-3,-1,-2]`, starting `max_sum` at 0 would return 0 — an empty subarray, which the problem forbids. Starting at `nums[0]` guarantees the answer is a real, non-empty subarray.

This is the trap most people hit on this problem, and it's a one-character fix that's easy to get wrong.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
for i in range(1, len(nums)):
```
Start at index **1**, since index 0 is already accounted for in the seeds. Iterating from 0 would double-count the first element into `cur_sum`.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    cur_sum = max(nums[i], cur_sum + nums[i])
```
**The whole algorithm.** Two candidates for the best subarray ending here:

- **`nums[i]`** — start fresh, discarding everything before.
- **`cur_sum + nums[i]`** — extend the best subarray that ended at `i-1`.

Take the larger. And note what this expression *quietly* does: it picks `nums[i]` precisely when `cur_sum < 0`, which is the greedy rule from section 1 — **drop a negative running sum** — expressed without an explicit `if`.

You could equally write `if cur_sum < 0: cur_sum = 0` before adding `nums[i]`. Same algorithm; the `max` form is more compact and makes the "extend or restart" choice explicit.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [kadane-algorithm](../algorithms/kadane-algorithm.md)

```python
    max_sum = max(max_sum, cur_sum)
```
Record the best seen anywhere. `cur_sum` is the best *ending here*; `max_sum` is the best **over all endings so far**.

Keeping these separate is essential. `cur_sum` can fall — it must, whenever the array turns negative — but `max_sum` never does. Returning `cur_sum` at the end would give the best subarray ending at the *last* index, which is a different and usually wrong answer.
→ [min-max-key](../syntax/min-max-key.md)

```python
return max_sum
```
Every index has been considered as an ending point, so the best across all of them is the global best.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        max_sum = nums[0]
        cur_sum = nums[0]

        for i in range(1, len(nums)):
            cur_sum = max(nums[i], cur_sum + nums[i])
            max_sum = max(max_sum, cur_sum)

        return max_sum
```
</details>

**Trace it** — `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

Seeds: `cur_sum = max_sum = -2`.

| `i` | `nums[i]` | restart (`nums[i]`) | extend (`cur_sum + nums[i]`) | new `cur_sum` | `max_sum` |
|---|---|---|---|---|---|
| 1 | 1 | **1** | −2 + 1 = −1 | **1** ← restart | 1 |
| 2 | −3 | −3 | 1 − 3 = **−2** | **−2** ← extend | 1 |
| 3 | 4 | **4** | −2 + 4 = 2 | **4** ← restart | 4 |
| 4 | −1 | −1 | 4 − 1 = **3** | **3** | 4 |
| 5 | 2 | 2 | 3 + 2 = **5** | **5** | 5 |
| 6 | 1 | 1 | 5 + 1 = **6** | **6** | **6** |
| 7 | −5 | −5 | 6 − 5 = **1** | **1** | 6 |
| 8 | 4 | 4 | 1 + 4 = **5** | **5** | 6 |

Return **6** ✅ — the subarray `[4,-1,2,1]`.

Two rows show the greedy at work. At `i = 1`, `cur_sum` was `-2` — negative — so restarting at `1` beats extending to `-1`. At `i = 3`, `cur_sum` was `-2` again, so the algorithm abandons everything and starts fresh at `4`. **Both restarts happen exactly when the running sum had gone negative**, which is the rule, and neither decision is ever revisited.

Row 7 is worth noting too: `cur_sum` drops from 6 to 1, but `max_sum` stays at 6. That's why the two variables can't be merged.

**And the all-negative case**, `nums = [-3, -1, -2]`:

| `i` | restart | extend | `cur_sum` | `max_sum` |
|---|---|---|---|---|
| — | — | — | −3 (seed) | −3 |
| 1 | **−1** | −3 − 1 = −4 | **−1** | **−1** |
| 2 | −2 | −1 − 2 = −3 | **−2** | −1 |

Return **−1** ✅ — the least-bad single element. Seeding `max_sum = 0` would have returned 0 here, which is the empty subarray and not allowed.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the array → **n − 1 iterations**.
- Each iteration does one addition and two `max` comparisons — all **O(1)**.
- **O(n)** total.

At n = 10⁵ that's a hundred thousand operations. Instant.

**Against the alternatives:** the naive triple loop is **O(n³)** — 10¹⁵ at this size. Fixing the inner sum with a running total gives **O(n²)** = 10¹⁰, still far too slow. Divide and conquer gets **O(n log n)**. Kadane's is **O(n)**, and it's optimal.

**Faster?** No. Every element can change the answer — flipping any single value can shift where the best subarray lies — so all n must be read. **Ω(n) is a hard lower bound**, and O(n) meets it.

**No best/worst case distinction.** The loop always runs exactly n−1 times with no early exit, so the bound is tight rather than merely an upper limit.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers, `cur_sum` and `max_sum`, regardless of input size. The input array is not modified and nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| Divide and conquer | **O(log n)** | The recursion stack |
| Prefix-sum array | **O(n)** | If you materialize the prefixes (though a running minimum makes it O(1)) |
| DP array of `best_ending_here` | **O(n)** | The textbook DP framing, one cell per index |
| **Kadane's** | **O(1)** | The recurrence looks back exactly **one** cell |

This is the extreme case of the rolling-variable reduction from Unit 13: [Climbing Stairs](70-climbing-stairs.md) needed two variables because its recurrence looked two cells back; here the lookback is a **single** cell, so one variable suffices (plus one to hold the running answer).

**And that's precisely why this reads as greedy rather than DP.** A one-cell lookback means there's no table to consult and no decision to revisit — you make a local choice at each element and move on. **The DP has degenerated into a greedy scan.**

**What you'd need more space for:** returning the subarray's *indices* rather than its sum. Track where the current run started (reset it whenever you restart) and record the start/end whenever `max_sum` improves — still O(1) space, just a few more variables.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'll think about subarrays by where they *end*. The best subarray ending at index i either extends the best one ending at i−1, or starts fresh at i — there's no third option, since a longer subarray ending at i must contain i−1. So `cur = max(nums[i], cur + nums[i])`, and I track the running maximum separately. The greedy reading is simpler: if the running sum ever goes negative, throw it away, because a negative prefix can only hurt anything that follows it. That's an exchange argument — dropping it is never worse. One detail that matters: I seed both variables with `nums[0]`, not 0, because the subarray must be non-empty, so an all-negative array has to return its least-negative element rather than 0. O(n) time, O(1) space. Divide and conquer also works at O(n log n) if they want to see it."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if all numbers are negative?" | The answer is the largest single element. This works because both variables are seeded with `nums[0]` rather than 0 — seeding 0 would return the empty subarray, which isn't allowed. |
| "Return the subarray, not just the sum." | Track the start of the current run (reset it on a restart) and record start/end whenever `max_sum` improves. Still O(1) space. |
| "Solve it with divide and conquer." | Split at the midpoint. The answer is the best in the left half, the best in the right half, or the best subarray *crossing* the midpoint — the latter found by extending outward from the middle in both directions. O(n log n). |
| "Solve it with prefix sums." | `sum(i..j) = prefix[j] − prefix[i−1]`. To maximize, track the **minimum prefix seen so far** and subtract it from the current prefix. One pass, O(1) space — a different derivation, same bound. |
| "What if the empty subarray were allowed?" | Then the answer is `max(result, 0)`, and you could seed both variables at 0. |
| "How does this differ from Maximum Product Subarray?" | Multiplication by a negative *reverses* ordering, so a very negative running product is valuable and can't be discarded. [152](152-maximum-product-subarray.md) has to track both a running max and a running min; sums never reverse, so one value suffices. |
| "Is this greedy or DP?" | Both. The recurrence is DP with a one-cell lookback; because the lookback is a single cell and the choice is never revisited, it reduces to a greedy scan. |
| "What about a circular array?" | Either the best subarray is normal (Kadane's), or it wraps — in which case the *complement* is the minimum subarray, so the answer is `total − minSubarray`. Take the max of the two, with a special case when all values are negative. |

**Traps:**
- **Seeding `max_sum = 0`.** Returns 0 for all-negative input. The single most common failure on this problem.
- **Returning `cur_sum` instead of `max_sum`.** Gives the best subarray ending at the *last* index, not the best overall.
- Starting the loop at index 0 after seeding with `nums[0]` — double-counts the first element.
- Merging the two variables. `cur_sum` must be allowed to fall; `max_sum` must not.
- Resetting `cur_sum` to 0 when it goes negative *and* seeding `max_sum` at 0 — the reset itself is fine, but the seed breaks all-negative input.
- Assuming the answer is contiguous *and* maximal-length. It's often a short slice in the middle.

**This same move shows up in:** [Maximum Product Subarray](152-maximum-product-subarray.md) (the same scan, where negatives break the greedy and force two running values) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (a running extreme in one pass — and it's Kadane's in disguise, on the array of daily differences) · [Jump Game](55-jump-game.md) (a greedy running frontier, justified by the same "a local choice can't hurt" argument) · [Climbing Stairs](70-climbing-stairs.md) (the rolling-variable collapse, here taken to a single cell).

</details>

---
