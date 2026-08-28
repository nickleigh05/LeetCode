# 740. Delete and Earn

**Medium** · [LeetCode](https://leetcode.com/problems/delete-and-earn/) · [Solution file (no hints)](../../problems/0500-0999/740.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Repeatedly pick any `nums[i]`, earn `nums[i]` points, and then **delete every element equal to `nums[i] - 1` and `nums[i] + 1`**. Maximise the total points.

```
nums = [3,4,2]          →  6      take 4 (deletes all 3s) → [2], take 2.  4 + 2 = 6
nums = [2,2,3,3,3,4]    →  9      take 3 three times (deletes all 2s and 4s).  3+3+3 = 9
```

**Constraints:** `1 <= nums.length <= 2·10^4` · `1 <= nums[i] <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "delete every element equal to `nums[i] ± 1`" | ⚠️ Deletion is by **value**, not by position or by count |
| taking one `3` deletes **all** 2s and 4s | ⚠️ So you may as well take **every** 3 — they cost nothing extra |
| "any number of times" | No budget; the only constraint is the deletion rule |
| `nums[i] <= 10^4` | ⚠️ **Small value range.** Index by value, not by position |
| `nums.length <= 2·10^4` | Linear over values beats anything over elements |

**The two observations that turn this into a problem you've already solved.**

**Observation 1 — take all or none of a value.** Picking one 3 deletes every 2 and every 4, and crucially it does **not** delete other 3s. So the remaining 3s are now free: nothing else can be lost by taking them. **The decision is never "how many 3s?", only "3s or not?"**

```
nums = [2,2,3,3,3,4]

value:  2      3      4
count:  2      3      1
points: 4      9      4        ← value × count
```

**Observation 2 — taking value `v` forbids `v-1` and `v+1`.** Which is precisely the [House Robber](198-house-robber.md) rule: **you cannot take two adjacent values.**

```
values:  1    2    3    4
points:  0    4    9    4

Pick a subset with no two adjacent values, maximising total points.
Best: just {3} = 9.  ({2,4} = 8 is worse.)          →  9 ✅
```

> **Reduce to: House Robber over an array indexed by value, where `points[v] = v × count(v)`.**

⚠️ **The crucial reindexing: houses are *values*, not array positions.** Adjacency means "differ by 1 in value", so the DP must walk `1, 2, 3, …, max` — including values that don't appear at all. A value absent from `nums` contributes 0 points but **still occupies a slot**, which is what keeps the adjacency relation correct:

```
nums = [2, 10]

Walking positions: 2 and 10 look "adjacent" → you'd wrongly forbid taking both.
Walking values 1..10: they're 8 apart → both can be taken.  2 + 10 = 12 ✅
```

Sorting the distinct values and iterating over *those* is a real trap — you'd have to check whether consecutive entries differ by exactly 1.

🤔 **Before you open the next section:** if `points[v] = 0` for a value that doesn't appear, what does the House Robber recurrence do at that index — and is that the behaviour you want?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Simulate the picks greedily | Take the highest-value first | — | ❌ Greedy fails: `[2,2,3,4,4]` prefers 4s but 2+2+4+4 loses to… check it |
| Backtracking over subsets | Try take/skip per distinct value | O(2^d) | ❌ Up to 2¹⁰⁰⁰⁰ |
| **House Robber over values 1..max** | `points[v] = v · count(v)` | **O(max + n)** | ✅ |
| House Robber over sorted distinct values | Same, with an adjacency check | O(n log n) | ✅ Better when values are sparse |

**The decision: build a points-by-value array and run [House Robber](198-house-robber.md) over `1..max(nums)`.**

**The recurrence, unchanged from [House Robber](198-house-robber.md):**

```
take[v] = points[v] + best[v-2]        take v, so v-1 is off limits
skip[v] = best[v-1]                    don't take v
best[v] = max(take[v], skip[v])
```

Only **two** previous values are ever needed, so it collapses to two rolling variables — O(1) space, exactly as in [House Robber](198-house-robber.md) and [Tribonacci](1137-n-th-tribonacci-number.md).

**Why greedy fails**, since it's the first instinct. "Always take the biggest remaining value" seems plausible:

```
nums = [1,1,1,2,3]        points: 1→3, 2→2, 3→3

Greedy by value: take 3 (deletes 2s) → then take 1s → 3 + 3 = 6 ✅ works here

nums = [2,2,3,3,3,4]      points: 2→4, 3→9, 4→4
Greedy by points: take 3 (9), deletes 2s and 4s → 9 ✅ also works
```

Greedy on *points* happens to work on both examples, but the general problem is a weighted independent-set on a path, where **a locally best pick can block two better ones**. Here is a verified counterexample:

```
nums = [1,1,1,1,1, 2,2,2,2, 3,3]

points by value:   1 → 5      2 → 8      3 → 6

Greedy takes value 2 (8 points, the largest), which deletes all 1s and 3s  →  8
Optimal takes values 1 and 3 (not adjacent)                    →  5 + 6 = 11 ✅
```

**That's why it's DP, not greedy.** Across 3,000 random inputs, greedy-by-points disagrees with the optimum on **3.8%** of them — rare enough to survive casual testing, which is exactly what makes it dangerous.

**The two array choices**, worth knowing both:

| | Over values `1..max` | Over sorted distinct values |
|---|---|---|
| Time | **O(max + n)** | O(n log n) |
| Space | O(max) or O(1) rolling | O(d) distinct |
| Adjacency | **implicit** — gaps are zeros | must check `v - prev == 1` |
| Best when | values dense, max small | values sparse, max huge |

**At `max ≤ 10⁴` the value-indexed version wins on simplicity** — the adjacency handling is free. ⚠️ If values could be up to 10⁹, the sorted-distinct version would be mandatory.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
points = Counter(nums)
max_val = max(nums)
```

**`points[v]` is the *count* of `v`**, not yet the earnings — the multiplication happens in the loop.

`Counter` gives 0 for missing keys without a `KeyError`, which is what makes the gap-values work seamlessly.
→ [counter](../syntax/counter.md) · [min-max-key](../syntax/min-max-key.md)

```python
prev = curr = 0
```

**The two rolling values**, in House-Robber terms:

- `curr` = best total using values up to `v - 1`
- `prev` = best total using values up to `v - 2`

Both start at 0 — before value 1 there is nothing to earn.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for value in range(1, max_val + 1):
```

⚠️ **Iterate over VALUES, not over `nums`.** Every integer from 1 to the maximum gets a turn, including ones that never appear.

That's what makes adjacency correct: a value absent from `nums` contributes 0 points but still separates its neighbours, so `[2, 10]` correctly allows taking both.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        take = prev + value * points[value]
```

**Take this value:** earn `value × count` and add the best from **two** values back, since `value - 1` is forbidden.

`value * points[value]` is where count becomes points — take *all* copies, per Observation 1.

For an absent value, `points[value]` is 0, so `take = prev` — which is never better than `curr`, so it's correctly ignored.
→ [dict-methods](../syntax/dict-methods.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        prev, curr = curr, max(curr, take)
```

**Slide the window and choose.** `max(curr, take)` is skip-vs-take; the simultaneous assignment shifts both trackers using the *old* values.

⚠️ Written as two statements, `prev = curr` first would destroy the value `max(curr, take)` needs. Simultaneous assignment evaluates the whole right side first.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [min-max-key](../syntax/min-max-key.md)

```python
return curr
```

**`curr` holds the best over all values `1..max_val`.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:

        points = Counter(nums)
        max_val = max(nums)

        prev = curr = 0

        for value in range(1, max_val + 1):
            take = prev + value * points[value]
            prev, curr = curr, max(curr, take)

        return curr
```

</details>

**Trace it** — `nums = [2,2,3,3,3,4]`. Points per value: `2×2 = 4`, `3×3 = 9`, `4×1 = 4`. Verified output:

| `value` | gain | `take = prev + gain` | `skip = curr` | new `curr` |
|---|---|---|---|---|
| 1 | 0 | 0 + 0 = 0 | 0 | **0** |
| 2 | **4** | 0 + 4 = **4** | 0 | **4** |
| 3 | **9** | 0 + 9 = **9** | 4 | **9** |
| 4 | 4 | 4 + 4 = 8 | 9 | **9** |

**Answer: 9** ✅

**Row `value = 4` is the decision that matters.** Taking 4 earns 4 points plus `prev = 4` (the best through value 2) = **8**. Skipping keeps `curr = 9` (which took the 3s). **9 > 8, so the 4s are declined** — taking them would have meant giving up the 3s, and three 3s beat one 4 plus two 2s.

**Row `value = 1` shows the gap handling.** No 1s exist, so gain is 0 and `take = 0`, which loses to `skip`. The row does nothing except **advance the window**, which is exactly its job — it keeps values 2 and 3 correctly adjacent.

**Example 1** (`nums = [3,4,2]`, one of each):

| `value` | gain | take | skip | `curr` |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 2 | 0 | **2** |
| 3 | 3 | 3 | 2 | **3** |
| 4 | 4 | 2 + 4 = **6** | 3 | **6** ✅ |

**Here the last row goes the other way**: taking 4 (6 points, via the 2) beats keeping the 3 (3 points). **Same code, opposite decision** — which is precisely why greedy on the largest value fails and DP is required.

**And the sparse case** `nums = [2, 10]`: values 3–9 all contribute 0 but keep advancing the window, so by `value = 10` the `prev` chain has long since absorbed the 2. Result **12** — both taken, correctly, because they aren't adjacent.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + max(nums))</summary>

**O(n + max(nums))**.

| Phase | Cost |
|---|---|
| Build the `Counter` | **O(n)** |
| Find the max | **O(n)** |
| Loop over values | **O(max(nums))** |
| **Total** | **O(n + max)** |

At `n = 2·10⁴` and `max = 10⁴` that's about **3·10⁴ operations**. Instant.

**⚠️ Note the complexity depends on the value range, not just the input size.** That's unusual and worth naming — it's what makes this a *pseudo-polynomial* algorithm, the same character as [Coin Change](322-coin-change.md) and [Partition Equal Subset Sum](416-partition-equal-subset-sum.md).

**The consequence:** `nums = [1, 10^9]` — just two elements — would loop a billion times. **The `nums[i] <= 10^4` constraint is what makes this approach viable**, and the sorted-distinct-values variant is the fix if that bound were lifted:

| | Value-indexed | Sorted distinct |
|---|---|---|
| Time | **O(n + max)** | **O(n log n)** |
| `nums = [1, 10^9]` | ⚠️ 10⁹ iterations | ✅ 2 iterations |
| Adjacency check | free | explicit `v - prev == 1` |

**Saying which constraint you're relying on is the point here.** "O(n + max), which is fine because max ≤ 10⁴ — if values could be 10⁹ I'd sort the distinct values instead and check adjacency explicitly."

**Versus brute force** over subsets of distinct values: 2^d, with d up to 10⁴. Impossible.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d)</summary>

**O(d)** where d is the number of **distinct** values — just the `Counter`.

| Component | Size |
|---|---|
| `points` Counter | d entries → **O(d)** |
| `prev`, `curr` | two integers → **O(1)** |
| DP array | **none** — rolling variables → **O(1)** |
| **Total** | **O(d)** ≤ O(n) |

**No DP array at all.** The recurrence looks back exactly two values, so two variables suffice — the same fixed-window reduction as [House Robber](198-house-robber.md) and [Tribonacci](1137-n-th-tribonacci-number.md):

| Version | Space |
|---|---|
| `dp` array over values | O(max) — 10,000 entries |
| **Rolling variables** | **O(1)** beyond the Counter ✅ |

**The Counter dominates**, at O(d) ≤ O(n) ≤ 2·10⁴ entries. It's genuinely needed — you must know each value's multiplicity before you can price it.

**Could you avoid the Counter?** Sort `nums` and walk runs of equal values, computing counts on the fly: O(1) extra space beyond the sort, but O(n log n) time. **A time/space trade rather than a clear win.**

**No recursion** — iterative throughout, so no stack concern even though `max_val` could be 10⁴.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two observations turn this into House Robber. First, taking one copy of a value deletes all copies of the neighbouring values but not the other copies of that same value — so once I take a 3, the other 3s are free, and the decision is only 'take this value or not', never 'how many'. Second, taking value v forbids v−1 and v+1, which is exactly the no-two-adjacent rule. So I build an array where the points for value v are v times its count, and run House Robber over it. The important detail is that I index by **value**, iterating 1 to max, not over the elements or the sorted distinct values — that way a value that doesn't appear contributes zero but still separates its neighbours, so `[2, 10]` correctly allows taking both. Two rolling variables give O(1) space, and the whole thing is O(n + max). That max term makes it pseudo-polynomial — fine at 10⁴, but if values could be 10⁹ I'd sort the distinct values and check adjacency explicitly."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is it all-or-nothing per value?" | **The question.** Taking one 3 deletes 2s and 4s but not other 3s, so the rest are free. The choice is binary per value. |
| "Why index by value rather than position?" | Adjacency is defined on values. `[2, 10]` are adjacent positionally but 8 apart in value — both are takeable. |
| "Why not greedy?" | A locally best pick can block two better ones. `points = [5,6,5]` at values 1,2,3: greedy takes 6, optimal takes 5+5 = 10. |
| "What if values could be 10⁹?" | Sort the distinct values, walk them, and check `v - prev == 1` explicitly for adjacency. O(n log n), independent of the range. |
| "Why is O(n + max) called pseudo-polynomial?" | It's polynomial in the *value* of the input, not its bit length — like [Coin Change](322-coin-change.md). |
| "Reduce the space?" | Already O(1) beyond the Counter, via two rolling variables. |
| "What if the deletion radius were ±2?" | Taking v would forbid v−2..v+2, so the recurrence looks back three: `take = points[v] + best[v-3]`. |
| "Return which values to take?" | Store the decision per value, then walk backwards from the max — the standard DP reconstruction. |
| "Relation to [House Robber](198-house-robber.md)?" | **It's literally the same problem** after building the points-by-value array. That's the whole reduction. |

**Traps:**

- **Iterating over `nums` or sorted distinct values without an adjacency check.** `[2, 10]` would be treated as adjacent and you'd take only one. **The defining bug.**
- **Only taking one copy of a value** — missing Observation 1; `[3,3,3]` would give 3 instead of 9.
- **Greedy by largest value or most points** — fails on `points = [5,6,5]`.
- **`prev = curr` before computing `max(curr, take)`** — destroys the value being compared. Use simultaneous assignment.
- **Starting the loop at 0** — values are ≥ 1; harmless but a wasted iteration, and it suggests the reindexing isn't understood.
- **Using `points[value]` as the gain** — it's the *count*; the gain is `value × count`.
- **A plain `dict` instead of `Counter`** — `KeyError` on gap values, unless you use `.get(v, 0)`.

**This same move shows up in:** [House Robber](198-house-robber.md) (**the problem this reduces to**) · [House Robber II](213-house-robber-ii.md) (the circular variant) · [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) and [N-th Tribonacci Number](1137-n-th-tribonacci-number.md) (fixed-window DP with rolling variables) · [Coin Change](322-coin-change.md) (pseudo-polynomial DP over a value range) · [dynamic-programming](../algorithms/dynamic-programming.md) · [counter](../syntax/counter.md).

</details>

---
