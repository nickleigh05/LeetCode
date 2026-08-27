# 416. Partition Equal Subset Sum

**Medium** · [LeetCode](https://leetcode.com/problems/partition-equal-subset-sum/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an integer array `nums` containing only positive numbers, return `true` if you can partition it into **two subsets whose sums are equal**.

```
nums = [1,5,11,5]    →  true     [1,5,5] and [11], both summing to 11
nums = [1,2,3,5]     →  false    total is 11 — odd, so no equal split exists
nums = [1,2,5]       →  false    total is 8, but no subset sums to 4
```

**Constraints:** `1 <= nums.length <= 200` · `1 <= nums[i] <= 100`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**two subsets**" | Every element goes to one side or the other. A binary choice per element → 2ⁿ partitions |
| "**equal** sums" | Each side must total exactly `sum(nums) / 2`. And crucially, **you only need to find one side** — the rest is automatically the other |
| "return true/false" | Feasibility, not optimization. The combining operator is `or` |
| all numbers are **positive** | No cancellation, so sums only grow as you add elements. That's what makes the reachable-sums approach finite and monotone |
| `n <= 200`, `nums[i] <= 100` | Total sum ≤ 20,000, so the half-target ≤ 10,000. **That bound is the whole hint** — it tells you an algorithm proportional to the *target value* is intended |

Two reductions turn this into a standard problem.

**First: if the total is odd, the answer is immediately `false`.** Two equal integers sum to an even number, so an odd total can't be split. One line, and it removes a whole class of inputs.

**Second, and this is the real move: you don't need to construct two subsets. You need to find one subset summing to `total / 2`.** Whatever you don't pick forms the other side, and its sum is `total − total/2 = total/2` automatically. So the question collapses from *"can I split this into two equal halves?"* to:

> **Is there a subset of `nums` that sums to exactly `target = total // 2`?**

That's the **subset-sum problem**, which is 0/1 knapsack with weights equal to values and no separate "value" to maximize.

The "0/1" matters: **each number can be used at most once.** Contrast [Coin Change](322-coin-change.md), where supply was infinite. That difference will shape the implementation.

🤔 **Before you open the next section:** you're going to build up the set of reachable sums, element by element. If you're processing the number 5 and the sum 3 is already reachable — what new sum becomes reachable? And why would it be a bug if that newly-added 8 could then immediately be used to reach 13 *within the same element's processing*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every subset | Enumerate all 2ⁿ, check each sum | **O(2ⁿ)** | O(n) | ❌ 2²⁰⁰ |
| Greedy — sort descending, fill one side | Add each number to the side that's behind | O(n log n) | O(1) | ❌ **Wrong.** `[1,5,11,5]` → greedy puts 11 on one side, then 5, 5, 1 on the other, ending 11 vs 11 by luck; but `[3,3,3,4,5]` (total 18, target 9) defeats it |
| Recursion + memo on `(index, remaining)` | Take or skip each element | O(n · target) | O(n · target) | ⚠️ Correct; 2-D memo and recursion depth |
| Boolean DP array over sums | `dp[s]` = is sum `s` reachable; iterate sums **downwards** per element | O(n · target) | O(target) | ✅ The classic 0/1 knapsack form |
| **Set of reachable sums** | Grow a set, adding `s + num` for every currently-reachable `s` | O(n · target) | O(target) | ✅ |

**The decision:** track the **set of reachable sums**, extending it one number at a time.

**Why greedy fails.** Sorting descending and always adding to the lighter side feels reasonable and is wrong. `[3,3,3,4,5]` has total 18, target 9 — achievable as `4+5` or `3+3+3`. Greedy takes 5, then 4 (other side), then 3 → 5+3 = 8 vs 4+3 = 7, then the last 3 → 8 vs 10. It reports failure on a solvable input. **Subset sum has no greedy solution**; that's the point of the problem.

**Why the state is one-dimensional.** The only thing that matters about the elements you've already processed is **which sums they can produce**. Not which ones you chose, not how many. So the state is "the set of reachable sums," bounded by `target` — which is why this is O(target) space and not O(2ⁿ).

**The subtle part — why the new sums are computed separately.** Here's the answer to section 1's question. If `achievable = {0, 3}` and you're processing `5`, the new sums are `{5, 8}`. But if you added them into the set *while iterating it*, then `8` would immediately be available and you'd derive `13` — **using the number 5 twice**. That's the unbounded (Coin Change) behaviour, not 0/1.

The code below sidesteps this by building `new_sums` as a **separate set first** and only then merging. Same idea as the snapshot in [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md): *read from the previous state, write to a new one, so one round can't feed itself.*

**The array equivalent** — worth knowing, because it's what most references show — is a boolean `dp` over sums where the inner loop runs **downwards**: `for s in range(target, num - 1, -1): dp[s] |= dp[s - num]`. Iterating downwards means `dp[s - num]` is always still from the *previous* element's state. Going upwards would reuse `num` and silently solve the unbounded problem. **The set version makes that hazard explicit; the array version hides it in the loop direction.**

**Why a set at all?** It's naturally sparse — with few elements, few sums are reachable and you don't touch all 10,000 slots. The boolean array has a better constant factor when the space is dense. Either is a fine answer.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
total = sum(nums)
if total % 2:
    return False
```
**The parity shortcut.** Two equal integers must sum to an even number, so an odd total makes the partition impossible — return immediately.

`total % 2` is `1` for odd, which is [truthy](../syntax/truthy-falsy-values.md), so no explicit `== 1` is needed. Beyond being a correctness check, this prunes a large fraction of inputs in one line.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [if-return](../syntax/if-return.md)

```python
target = total // 2
achievable = {0}
```
`target` is what one subset must sum to. [Floor division](../syntax/integer-division-modulo.md) `//` keeps it an integer — and it's exact here, since the odd case already returned.

`achievable` holds every sum reachable using the numbers processed so far. It starts as `{0}`: **choosing nothing gives a sum of zero**, which is always reachable and is the seed everything else grows from. The same "empty case is valid" base as `dp[n] = True` in [Word Break](139-word-break.md).
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [set-basics](../syntax/set-basics.md) · [hashset](../data-structures/hashset.md)

```python
for num in nums:
```
Process one number at a time. After each iteration, `achievable` is exactly the set of sums reachable from the numbers seen so far — that's the invariant, and it's what makes the final membership test meaningful.
→ [for-loop](../syntax/for-loop.md)

```python
    new_sums = {s + num for s in achievable if s + num <= target}
```
**Take `num`, added to every sum already reachable.** A [set comprehension](../syntax/set-comprehension.md) building the sums that become newly available.

Two things it gets right:

- **It reads from `achievable` and writes to a *separate* set.** Nothing added here can be extended again during this same iteration, which is what enforces **each number used at most once**. Mutating `achievable` in place while iterating it would both raise a `RuntimeError` in Python *and* be logically wrong — that's the unbounded-knapsack behaviour.
- **The `<= target` filter** discards sums that overshoot. Since all numbers are positive, an overshooting sum can never come back down, so it's dead weight. This is what bounds the set at `target + 1` entries and keeps the space O(target) rather than O(2ⁿ).

Note there's no explicit "skip `num`" branch — skipping is implicit, because the old sums stay in `achievable` when the sets are merged.
→ [set-comprehension](../syntax/set-comprehension.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    achievable |= new_sums
```
Merge in the new sums with the [in-place union operator](../syntax/set-operations.md). After this, `achievable` holds both the sums that skip `num` (already there) and the sums that take it (just added) — the two branches of the 0/1 choice, unioned.
→ [set-operations](../syntax/set-operations.md)

```python
return target in achievable
```
Is exactly half the total reachable? If so, that subset is one side and everything else is the other, and by construction they're equal.

Set membership is **O(1) average**, and it's the payoff for having used a set rather than a list.
→ [membership-operators](../syntax/membership-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:

        total = sum(nums)
        if total % 2:
            return False

        target = total // 2
        achievable = {0}

        for num in nums:
            new_sums = {s + num for s in achievable if s + num <= target}
            achievable |= new_sums

        return target in achievable
```
</details>

**Trace it** — `nums = [1, 5, 11, 5]`, `total = 22`, `target = 11`

| `num` | `new_sums` (from current set, ≤ 11) | `achievable` after |
|---|---|---|
| — | — | `{0}` |
| 1 | `{1}` | `{0, 1}` |
| 5 | `{5, 6}` | `{0, 1, 5, 6}` |
| 11 | `{11}` — `1+11`, `5+11`, `6+11` all exceed 11 | `{0, 1, 5, 6, 11}` |
| 5 | `{5, 6, 10, 11}` | `{0, 1, 5, 6, 10, 11}` |

`11 in achievable` → **true** ✅ — via `{11}` on one side, or equally `{1,5,5}`.

Look at the `num = 5` row. `new_sums` is `{5, 6}`, computed from `{0, 1}`. If those had been merged into `achievable` *during* the comprehension, then `5` would have been available as a source and `10` would appear — using the single `5` twice. The separate set is what prevents it.

**And `nums = [1, 2, 5]`**, `total = 8`, `target = 4`:

| `num` | `new_sums` (≤ 4) | `achievable` after |
|---|---|---|
| — | — | `{0}` |
| 1 | `{1}` | `{0, 1}` |
| 2 | `{2, 3}` | `{0, 1, 2, 3}` |
| 5 | `{}` — every `s + 5` exceeds 4 | `{0, 1, 2, 3}` |

`4 in achievable` → **false** ✅ — the total is even, so the parity check passes it through, but no subset actually reaches 4. Both checks are needed: even total is necessary, not sufficient.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · target)</summary>

**O(n · target)**, where `target = sum(nums) / 2`.

- The loop runs **n** times.
- Each iteration builds `new_sums` by scanning `achievable`, which holds at most **`target + 1`** values (every sum from 0 to `target`) → **O(target)** per iteration, with O(1) set operations.
- The union is O(size of `new_sums`) = O(target).
- n × O(target) = **O(n · target)**.

With the given limits: sum ≤ 200 × 100 = 20,000, so target ≤ 10,000, giving 200 × 10,000 = **2 × 10⁶**. Comfortable — and notice how neatly the constraints were chosen to make this bound the intended one.

**Why "the constraints tell you the algorithm"** is worth saying out loud: `n ≤ 200` and `nums[i] ≤ 100` exist *specifically* to bound the target. An O(n · target) algorithm is only viable because the values are small.

**Pseudo-polynomial, again.** Like [Coin Change](322-coin-change.md), this is linear in the *value* of the target but exponential in the number of bits needed to write it. Subset sum is NP-complete in general; this DP is only efficient because the numbers are small. That's the precise statement, and it's a genuinely good thing to know: **an NP-complete problem with a polynomial-looking solution should make you check what's actually bounded.**

**Against brute force:** 2ⁿ = 2²⁰⁰ subsets. The DP works because many different subsets produce the *same sum*, and only the sum matters — collapsing 2ⁿ subsets into ≤ target distinct states.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(target)</summary>

**O(target)** — `achievable` holds at most `target + 1` distinct values (every integer from 0 to `target`), and `new_sums` is bounded the same way.

At the limits that's ~10,000 integers. The `<= target` filter is what guarantees this: without it, sums could grow to the full total and the set would be twice as large — still bounded, but pointlessly.

| Approach | Space | Why |
|---|---|---|
| Recursion + memo on `(index, sum)` | **O(n · target)** | A 2-D cache — n times bigger |
| Boolean DP array over sums | **O(target)** | `target + 1` booleans; better constant factor than a set |
| **Set of reachable sums** | **O(target)** | Sparse — only stores sums actually achievable |

**Why this can't collapse to O(1):** `achievable` may be consulted at any offset by any number, so there's no bounded lookback window — the same reason [Coin Change](322-coin-change.md) needs its full array while [House Robber](198-house-robber.md) doesn't.

**Set vs. boolean array.** The set is sparse — with few elements, only a handful of sums are reachable and you never touch the other 9,900 slots. The array is dense but has a much better constant (a bit or byte per sum, no hashing). For a `bytearray` or an integer-as-bitmask, the array wins comfortably at these sizes. Either is defensible; knowing *why* you'd pick each is the interesting part.

**The slick version worth mentioning:** represent the reachable set as a single Python integer used as a bitmask, where bit `s` means "sum `s` is reachable." Then the entire inner loop is `bits |= bits << num`. Same complexity, but it runs at word-level parallelism and is a one-liner.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two reductions. First, if the total is odd, it's impossible — two equal integers can't sum to an odd number. Second, I don't need to build both subsets: if I can find one subset summing to half the total, the rest automatically forms the other half. So this becomes subset sum, which is 0/1 knapsack. I track the set of reachable sums, starting from `{0}` since choosing nothing sums to zero, and for each number I add it to every currently reachable sum. The critical detail is that I compute the new sums into a *separate* set before merging — otherwise a newly-added sum could be extended again in the same iteration, which would use that number twice and solve the unbounded problem instead. I also discard anything over the target, since all values are positive and an overshoot can never come back. O(n · target) time and O(target) space, which is pseudo-polynomial — subset sum is NP-complete in general, and this only works because the values are capped at 100."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is finding one subset enough?" | Because the complement is everything else, and its sum is `total − target = target`. Finding one half determines both. |
| "Why the separate `new_sums` set?" | So a sum created by this number can't immediately be extended by the same number. Merging in place would allow reuse — that's unbounded knapsack, not 0/1. |
| "Write the array version." | `dp = [False]*(target+1)`; `dp[0] = True`; then for each `num`, `for s in range(target, num-1, -1): dp[s] |= dp[s-num]`. **Downwards** is essential — upwards reuses the number. |
| "Why is greedy wrong?" | `[3,3,3,4,5]`, total 18, target 9. Achievable as 4+5, but sort-descending-and-balance ends 8 vs 10 and reports false. |
| "Partition into *k* equal subsets?" | Much harder — [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/), typically backtracking with pruning or a bitmask DP over subsets. The single-target reduction doesn't generalize. |
| "What if negatives were allowed?" | The `<= target` pruning breaks, since a sum can overshoot and come back. You'd need to track the full range from `min` to `max` sum, or shift indices to keep them non-negative. |
| "Which elements form the subset?" | Store, for each sum, which number first produced it, then walk backwards from `target`. That's O(target) more space. |
| "Is this really polynomial?" | Pseudo-polynomial — linear in the target's *value*, exponential in its bit length. Subset sum is NP-complete; this is efficient only because values are small. |
| "Can you speed up the constant factor?" | Use a Python int as a bitmask: `bits |= bits << num`, with `bits = 1` initially. Word-level parallelism, and it's one line. |

**Traps:**
- **Mutating `achievable` while iterating it.** Python raises `RuntimeError`, and even the "fixed" version that adds after the loop is logically wrong if it lets sums chain within one element.
- **Running the array version's inner loop upwards.** Silently solves unbounded knapsack — you'd report `true` for `[1,2,5]` by using 1 four times.
- Forgetting the odd-total check. Not just an optimization: `total // 2` would truncate and you'd test the wrong target.
- Omitting the `<= target` filter. Still correct, but the set grows to the full total for no benefit.
- Seeding `achievable` as empty instead of `{0}`. Nothing can ever be built, and it always returns `false`.
- Assuming an even total is sufficient. `[1,2,5]` totals 8 and still fails — both checks are needed.

**This same move shows up in:** [Coin Change](322-coin-change.md) (the same DP-over-values shape, but *unbounded* — the contrast that makes the 0/1 detail concrete) · [Target Sum](494-target-sum.md) (subset sum in disguise — assigning ± signs reduces to finding a subset with a given sum) · [Word Break](139-word-break.md) (a feasibility DP where the base case is "the empty choice succeeds") · [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md) (the snapshot pattern — read from the previous state so one round can't feed itself).

</details>

---
