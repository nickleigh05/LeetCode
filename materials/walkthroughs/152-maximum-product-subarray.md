# 152. Maximum Product Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-product-subarray/)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an integer array `nums`, find a **contiguous** non-empty subarray with the **largest product**, and return that product.

```
nums = [2,3,-2,4]      →  6      [2,3]
nums = [-2,0,-1]       →  0      [0] — the answer is the 0 itself
nums = [-2,3,-4]       →  24     the whole array: -2 × 3 × -4
nums = [-2]            →  -2     a single negative is the best available
```

**Constraints:** `1 <= nums.length <= 2 × 10⁴` · `-10 <= nums[i] <= 10` · the answer fits in a 32-bit integer.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**contiguous** subarray" | A sliding-window / running-state problem, not a subset problem. Same shape as [Maximum Subarray](53-maximum-subarray.md) |
| "**largest product**" | Like Kadane's for sums — but multiplication behaves very differently from addition |
| values can be **negative** | The crux. A negative doesn't just reduce the product, it **flips its sign** — so the *worst* running product can become the *best* in one step |
| values can be **zero** | A zero annihilates any product it touches. It's a hard boundary: nothing before it can contribute to anything after it |
| "non-empty" | You must return something, even if every option is negative. `[-2]` → `-2`, not 0 |
| `n <= 2 × 10⁴` | n² = 4 × 10⁸ is too slow. **O(n) is required** |

The instinct is to adapt [Kadane's algorithm](../algorithms/kadane-algorithm.md): keep a running best and either extend it or restart. But try it with only a running max on `[-2, 3, -4]`:

- At `-2`: best running product `-2`.
- At `3`: extending gives `-6`, restarting gives `3`. Take `3`.
- At `-4`: extending gives `-12`, restarting gives `-4`. Take `-4`.

Answer: 3. **But the correct answer is 24** — the whole array, `-2 × 3 × -4`. The algorithm discarded `-6` at step 2 for being small, and `-6 × -4 = 24` was the winner.

That's the entire lesson: **for sums, a small running total is useless and can be safely discarded. For products, a very negative running total is potentially the most valuable thing you have** — it only needs one more negative number to become hugely positive.

So a single running value can't work. You need **two**: the largest running product *and* the smallest, because either could become the next maximum depending on the sign of what comes next.

🤔 **Before you open the next section:** if you're tracking both a running max and a running min, and the next number is negative — what happens to those two values? Which one should become the new max?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Every subarray | All O(n²) subarrays, product computed as you extend | O(n²) | O(1) | ❌ 4 × 10⁸ at n = 2 × 10⁴ |
| [Kadane's](../algorithms/kadane-algorithm.md) with `max` only | Track the running max product, extend or restart | O(n) | O(1) | ❌ **Wrong.** `[-2,3,-4]` → 3, not 24. Discards negatives that would flip to large positives |
| Split on zeros, count negatives | For each zero-free segment, drop everything up to the first or after the last negative | O(n) | O(1) | ⚠️ Correct and clever, but fiddly — several cases to get right |
| Prefix/suffix products | Scan left-to-right and right-to-left, resetting at zeros, take the max seen | O(n) | O(1) | ✅ Correct and surprisingly short — worth knowing as an alternative |
| **Track running max *and* min** | At each step compute both, since a negative swaps their roles | O(n) | O(1) | ✅ |

**The decision:** carry **two** running values — `cur_max` and `cur_min` — and update both at every step.

**Why two values is exactly the right amount of state.** Multiplying by a positive preserves order: the biggest stays biggest. Multiplying by a **negative reverses it** — the most negative product becomes the most positive. So the best candidate after position `i` is either "the previous max × this number" or "the previous min × this number," depending on the sign. You can't know which without keeping both, and you never need more than those two, because extremes are the only candidates that can ever win.

That's the generalizable idea: **when an operation can reverse ordering, track both ends of the range, not just the end you care about.**

**Why the code doesn't branch on sign.** You could write `if num < 0: swap(cur_max, cur_min)` and then apply Kadane's. That's the same algorithm, more explicitly. The version below instead takes `max` and `min` over all three candidates — `num`, `cur_max × num`, `cur_min × num` — which handles positive, negative, and restart cases uniformly with no sign check. Fewer branches, fewer bugs.

**Why `num` itself is one of the candidates.** That's the "restart" case, inherited from Kadane's: sometimes the best subarray *starts here*, and dragging along the previous product would only hurt. Including `num` in both the `max` and the `min` handles it without a separate branch.

**Why zero needs its own handling.** Zero destroys any product it's part of, so a subarray can never span a zero. Resetting both running values to 1 makes the next element start fresh — the multiplicative identity is the natural "empty product." (The `result` is seeded from `max(nums)` so a genuine zero can still be the answer, as in `[-2,0,-1]`.)

**Why not the split-on-zeros approach?** Within a zero-free segment, if the count of negatives is even, the whole segment is the answer; if odd, you drop everything through the first negative or everything from the last negative onward, whichever is better. It's O(n) and correct — but it has more cases, more index bookkeeping, and doesn't generalize. The two-value scan is one loop.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = max(nums)
cur_max = 1
cur_min = 1
```
`result` seeds with the **largest single element**, which is doing two jobs. It guarantees a valid answer when every subarray product is negative (`[-2]` → `-2`), and it handles the case where a lone `0` is the best available (`[-2,0,-1]` → `0`). Seeding `result = 0` would be wrong for all-negative input; seeding with `nums[0]` also works but `max(nums)` is clearer about intent.

`cur_max` and `cur_min` start at **1**, the multiplicative identity — the product of an empty subarray. It's the same role `0` plays in [Maximum Subarray](53-maximum-subarray.md)'s additive version.
→ [min-max-key](../syntax/min-max-key.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for num in nums:
```
A single pass over the values. As in [House Robber](198-house-robber.md), no indices are needed — all necessary history lives in the two running variables.
→ [for-loop](../syntax/for-loop.md)

```python
    if num == 0:
        cur_max = 1
        cur_min = 1
        continue
```
**The zero barrier.** Any subarray containing this zero has product 0, so nothing before it can help anything after it. Reset both running products to the identity and [`continue`](../syntax/break-continue.md) — the next element starts a completely fresh subarray.

`result` isn't updated here, and it doesn't need to be: `max(nums)` already accounted for the zero if it's the best answer available.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    tmp = cur_max * num
```
**Save the old `cur_max` before it's overwritten.** The next line assigns to `cur_max`, and the line after that still needs the *old* value — without this temporary, `cur_min` would be computed from the already-updated `cur_max` and the algorithm silently breaks.

Same hazard as the rolling-variable slide in [Climbing Stairs](70-climbing-stairs.md): when two values update together, one must be preserved. (The alternative is a [tuple assignment](../syntax/swap-tuple-assign.md), which evaluates the whole right-hand side first.)
→ [variables-assignment](../syntax/variables-assignment.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    cur_max = max(num, tmp, cur_min * num)
    cur_min = min(num, tmp, cur_min * num)
```
**The heart of it.** Three candidates for the best subarray product ending at this position:

| Candidate | Meaning | When it wins |
|---|---|---|
| `num` | **Restart** — begin a new subarray here | The previous running products would only hurt |
| `tmp` (= old `cur_max × num`) | Extend the best-so-far | `num` is positive |
| `cur_min * num` | Extend the **worst**-so-far | `num` is negative — the most negative product flips to the most positive |

`cur_max` takes the largest, `cur_min` the smallest. The third candidate is the one Kadane's-with-max-only misses, and it's why `[-2,3,-4]` works: at `-4`, `cur_min` is `-6`, and `-6 × -4 = 24`.

Both lines consider the same three values because a negative multiplier turns the largest candidate into the smallest and vice versa — so both extremes must be recomputed from the full set.
→ [min-max-key](../syntax/min-max-key.md) · [dynamic-programming](../algorithms/dynamic-programming.md) · [kadane-algorithm](../algorithms/kadane-algorithm.md)

```python
    result = max(result, cur_max)
```
Record the best seen anywhere. `cur_max` is the best subarray *ending here*; `result` is the best **ending anywhere so far** — the same running-maximum pattern as Kadane's.

Only `cur_max` is compared, never `cur_min`: a minimum product is never the answer, it's only ever raw material for a future maximum.
→ [min-max-key](../syntax/min-max-key.md)

```python
return result
```
Every position has been considered as an ending point, so the best over all of them is the global best.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:

        result = max(nums)
        cur_max = 1
        cur_min = 1

        for num in nums:
            if num == 0:
                cur_max = 1
                cur_min = 1
                continue

            tmp = cur_max * num
            cur_max = max(num, tmp, cur_min * num)
            cur_min = min(num, tmp, cur_min * num)
            result = max(result, cur_max)

        return result
```
</details>

**Trace it** — `nums = [-2, 3, -4]`, the case that defeats single-value Kadane's.

`result` starts at `max(nums)` = **3**. `cur_max = cur_min = 1`.

| `num` | candidates: `num`, `cur_max×num`, `cur_min×num` | new `cur_max` | new `cur_min` | `result` |
|---|---|---|---|---|
| −2 | −2, 1×(−2) = −2, 1×(−2) = −2 | **−2** | **−2** | 3 |
| 3 | 3, (−2)×3 = −6, (−2)×3 = −6 | **3** | **−6** | 3 |
| −4 | −4, 3×(−4) = −12, **(−6)×(−4) = 24** | **24** | **−12** | **24** |

Return **24** ✅

Row 2 is the point of the whole algorithm. `cur_min` becomes `−6` — a value that looks worthless and that a max-only Kadane's would throw away. Row 3 cashes it in: multiplying by `−4` turns the worst product into the best one by a wide margin.

**And `nums = [-2, 0, -1]`:**

| `num` | action | `cur_max` | `cur_min` | `result` |
|---|---|---|---|---|
| — | seed `result = max(nums)` | 1 | 1 | **0** |
| −2 | candidates −2, −2, −2 | −2 | −2 | 0 |
| 0 | **reset**, skip | 1 | 1 | 0 |
| −1 | candidates −1, −1, −1 | −1 | −1 | 0 |

Return **0** ✅ — no subarray product beats the zero itself, and the `max(nums)` seed is what supplied that answer, since the loop never proposes it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- `max(nums)` for the seed is one pass → **O(n)**.
- The main loop is a second pass → **O(n)**, with each iteration doing a constant amount of work: two multiplications, a three-way `max`, a three-way `min`, and a comparison.
- O(n) + O(n) = **O(n)**.

Two passes, still linear. At n = 2 × 10⁴ that's ~40,000 operations.

**Against the alternatives:** checking every subarray is **O(n²)** — 4 × 10⁸ at the limit, too slow. The prefix/suffix approach is also two O(n) passes. Everything correct here is linear; the interesting part is that the *obvious* linear approach (max-only Kadane's) is wrong.

**Can you do it in one pass?** Yes — drop the `max(nums)` seed by initializing `result = nums[0]` and starting the loop at index 1, or seed `result` to `float("-inf")` and let the loop fill it, being careful that a lone zero still registers. The two-pass version is clearer and the same complexity; there's no reason to contort it.

**Faster than O(n)?** No. Every element can change the answer, so **Ω(n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers (`result`, `cur_max`, `cur_min`, `tmp`), regardless of input size.

No array, no recursion, no auxiliary structure. The input isn't modified.

| Approach | Space | Why |
|---|---|---|
| Brute force over subarrays | O(1) | But O(n²) time |
| DP array of max/min per index | **O(n)** | Two arrays of running extremes — the textbook framing |
| **Two rolling values** | **O(1)** | Only the previous position's extremes are ever read |

Same collapse as the rest of Unit 13, and for the same reason: **`dp[i]` depends only on `dp[i-1]`, so one position of history suffices.** The twist is that "one position of history" is *two numbers* rather than one, because the state needed to describe a position is a range, not a single value.

That's the transferable idea, and it's worth stating in an interview: **the size of your rolling state should match the information the recurrence actually needs.** Here that's both extremes; in [House Robber](198-house-robber.md) it was two consecutive answers; in [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) it's several parallel states.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "My first instinct is Kadane's, but it breaks for products. With sums, a small running total is worthless and you discard it; with products, a very *negative* running total is valuable, because one more negative flips it to a large positive. On `[-2,3,-4]`, max-only Kadane's returns 3 while the real answer is 24 — the whole array. So I track both the running max and the running min at each position. At each element the candidates are: restart with the element itself, extend the previous max, or extend the previous min — and I take the max and min over all three, which handles positive and negative multipliers without a sign check. Zeros get a special case: nothing can span a zero, so I reset both running values to 1. I seed the answer with `max(nums)` so all-negative input and a lone zero both work. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why won't plain Kadane's work?" | Because multiplication by a negative reverses ordering. `[-2,3,-4]`: max-only gives 3, the answer is 24. The discarded `−6` was the most valuable state. |
| "Why track the minimum at all?" | It's the raw material for a future maximum. Multiply the most negative product by a negative number and it becomes the most positive one. |
| "What if there were no negatives?" | Then `cur_min` is never useful and it reduces to ordinary Kadane's with multiplication — track the running max, reset at zeros. |
| "Solve it without tracking the min." | Two passes: a left-to-right running product and a right-to-left one, both resetting to 1 at zeros; the answer is the max value seen in either. Works because an odd number of negatives means the optimal segment excludes either the leftmost or the rightmost negative. |
| "Why seed `result = max(nums)`?" | For all-negative input (`[-2]` → `-2`) and for a lone zero being the best (`[-2,0,-1]` → `0`). Seeding 0 or 1 would be wrong for the former. |
| "Why reset to 1 at a zero and not 0?" | 1 is the multiplicative identity — the product of an empty subarray. Resetting to 0 would trap every future product at 0. |
| "What about integer overflow?" | Not an issue in Python — ints are arbitrary precision. In Java or C++ you'd need `long`, and the problem guarantees the answer fits in 32 bits, though intermediate products might not. |
| "What if the subarray could be empty?" | Then the answer is at least 1 (the empty product), and you'd return `max(result, 1)`. The problem says non-empty. |

**Traps:**
- **Overwriting `cur_max` before computing `cur_min`.** The `tmp` variable exists solely for this. Without it, `cur_min` is derived from the new `cur_max` and the answer is quietly wrong.
- **Tracking only the max.** The defining error, and it passes plenty of tests before failing on two negatives.
- **Initializing `result = 0`.** Breaks on all-negative input, returning 0 for `[-2]`.
- Initializing `cur_max`/`cur_min` to 0 rather than 1 — every product is then trapped at 0.
- Forgetting the zero case, or resetting to 0 instead of 1.
- Comparing `result` against `cur_min`. A minimum is never the answer, only a stepping stone.

**This same move shows up in:** [Maximum Subarray](53-maximum-subarray.md) (Kadane's for sums — the version this one has to break) · [House Robber](198-house-robber.md) (rolling state that carries just enough history) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (several parallel running states, chosen to match what the recurrence needs) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (a running extreme carried through one pass).

</details>

---
