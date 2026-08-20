# 198. House Robber

**Medium** · [LeetCode](https://leetcode.com/problems/house-robber/) · [Solution file (no hints)](../../problems/0001-0499/198.py)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

---

You're a robber planning to rob houses along a street. Each house has some money, given by `nums`. **Adjacent houses have connected security systems** — robbing two adjacent houses on the same night triggers the alarm. Return the **maximum amount** you can rob tonight without alerting the police.

```
nums = [1,2,3,1]      →  4      rob houses 0 and 2 → 1 + 3
nums = [2,7,9,3,1]    →  12     rob houses 0, 2, 4 → 2 + 9 + 1
nums = [2,1,1,2]      →  4      rob houses 0 and 3 — note they're NOT adjacent
```

**Constraints:** `1 <= nums.length <= 100` · `0 <= nums[i] <= 400`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**maximum** amount" | An optimization problem. `max` will be the combining operator |
| houses **in a line** | 1-D, and order is fixed. You're not choosing an arrangement, only a subset |
| "can't rob two **adjacent** houses" | The only constraint, and it's **local** — it relates each house to its immediate neighbour and nothing further |
| every house is rob-or-skip | A binary choice per index → 2ⁿ subsets to consider naively |
| `n <= 100` | 2¹⁰⁰ is impossible; O(n) or O(n log n) needed. But note n is *small*, so the difficulty is the reasoning, not the performance |

The constraint being **local** is the fact that unlocks everything. If robbing house `i` were forbidden by something ten houses away, you'd need much more state. But it only conflicts with `i-1` — so when you're deciding about house `i`, the **only** thing about the past that matters is whether you took `i-1`.

Now the standard DP question: *stand at house `i` and ask what your options are.*

- **Skip it.** Your total is whatever the best was through house `i-1`.
- **Rob it.** You collect `nums[i]`, but house `i-1` was then off-limits, so you add it to the best through house **`i-2`**.

You want whichever is larger:

```
best(i) = max( best(i−1),                 ← skip house i
               best(i−2) + nums[i] )      ← rob house i
```

Compare that to [Climbing Stairs](70-climbing-stairs.md): same two-cell window, same shape. The difference is that 70 **added** the two branches (counting every route) while this one takes the **max** (choosing the best route). Third problem in this unit, same skeleton.

🤔 **Before you open the next section:** the greedy "rob every other house" gives 1 + 3 = 4 on `[1,2,3,1]` — correct. Try it on `[2,1,1,2]`. What does it give, and what's the real answer? What does that tell you about fixed-stride strategies?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Rob every other house | Take all even indices, or all odd, whichever is bigger | O(n) | O(1) | ❌ **Wrong.** `[2,1,1,2]` → evens = 3, odds = 3, but the answer is 4 (houses 0 and 3, which aren't adjacent) |
| Greedy by value | Repeatedly take the largest remaining house, block its neighbours | O(n log n) | O(n) | ❌ Also wrong. `[2,3,2]` → grabs 3, blocks both 2s, yields 3; the answer is 4 |
| Try every subset | Enumerate all 2ⁿ, keep the valid max | O(2ⁿ · n) | O(n) | ❌ Correct but exponential |
| Recursion + memo | `best(i) = max(best(i-1), best(i-2) + nums[i])`, cached | O(n) | O(n) + stack | ⚠️ Correct; carries a cache and n frames |
| DP array | Same recurrence, filled left to right | O(n) | O(n) | ⚠️ Correct, and the clearest first draft |
| **Two rolling variables** | Same recurrence, keeping only the last two | O(n) | **O(1)** | ✅ |

**The decision:** the recurrence bottom-up with **two rolling variables**.

**Why both greedy ideas fail, with the counterexamples.** These are worth memorizing, because "greedy doesn't work" is much weaker than showing an input where it breaks.

- *Every other house*: `[2,1,1,2]`. Even indices give 2+1 = 3, odd give 1+2 = 3. But 0 and 3 are **not adjacent**, so 2+2 = **4** is legal and better. **The optimal subset doesn't have to alternate** — it can leave a gap of two.
- *Largest first*: `[2,3,2]`. Taking 3 blocks both neighbours for a total of 3, while taking both 2s gives **4**. A big value can be worth less than the two things it excludes.

Both failures share a cause: **a local decision has consequences you can't evaluate locally.** That's the DP signal.

**Why DP works where greedy doesn't.** At each house you keep *both* possibilities alive — the best that includes this house and the best that doesn't — rather than committing. The recurrence never throws away a branch until it has enough information to know it's dominated.

**Why bottom-up over memoized recursion?** Same O(n), but no stack and no cache, and the two-cell window then collapses to O(1) space — the same reduction you did in [70](70-climbing-stairs.md) and [746](746-min-cost-climbing-stairs.md). Third time is where it stops being a trick and becomes a reflex.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
prev, curr = 0, 0
```
The rolling window, in the compact form. Think of them as the two most recent answers:
- `curr` = best loot through the previous house
- `prev` = best loot through the house before that

Both start at 0, encoding "before any houses exist, you have nothing." Because they start equal, no separate base case is needed — the recurrence handles the first house correctly on its own, which is why this version has no `if len(nums) == 1` guard.
→ [variables-assignment](../syntax/variables-assignment.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
for num in nums:
```
Iterate the **values**, not the indices. The recurrence only ever needs `nums[i]` plus the two rolling variables — it never indexes backwards into the array, because that history is already carried in `prev` and `curr`.

That's a small but real readability win: no index arithmetic means no off-by-one bugs.
→ [for-loop](../syntax/for-loop.md)

```python
    prev, curr = curr, max(curr, prev + num)
```
**The whole algorithm, in one line.** Unpack it as two simultaneous assignments:

- **New `curr`** = `max(curr, prev + num)` — the recurrence itself. `curr` is *skip this house* (keep the best so far); `prev + num` is *rob this house* (its value plus the best from two back, since the neighbour is now off-limits).
- **New `prev`** = the old `curr` — the window slides forward one position.

The reason this can be one line is Python's [tuple assignment](../syntax/swap-tuple-assign.md): **the entire right-hand side is evaluated before anything is assigned.** So `curr` on the right is the old value in *both* places, and the ordering problem that forced two careful lines in [70](70-climbing-stairs.md) disappears. Splitting this into `prev = curr` then `curr = max(curr, prev + num)` is **wrong** — the second line would read the already-updated `prev`.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [min-max-key](../syntax/min-max-key.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return curr
```
After the last iteration, `curr` is the best achievable through the final house — which is the answer, since "through house n-1" already includes the option of having skipped it.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:

        prev, curr = 0, 0
        for num in nums:
            prev, curr = curr, max(curr, prev + num)
        return curr
```
</details>

**Trace it** — `nums = [2, 7, 9, 3, 1]`

| `num` | `prev + num` (rob) | `curr` (skip) | new `curr` = max | new `prev` |
|---|---|---|---|---|
| 2 | 0 + 2 = **2** | 0 | **2** | 0 |
| 7 | 0 + 7 = **7** | 2 | **7** | 2 |
| 9 | 2 + 9 = **11** | 7 | **11** | 7 |
| 3 | 7 + 3 = 10 | **11** | **11** | 11 |
| 1 | 11 + 1 = **12** | 11 | **12** | 11 |

Return **12** ✅ — houses 0, 2, 4 → 2 + 9 + 1.

Row 4 is the interesting one: robbing house 3 would yield 10, but skipping it and keeping 11 is better, so `curr` stays put. And row 5 shows why that mattered — because house 3 was skipped, house 4 is available, and `prev` (11, the best through house 2) plus 1 wins.

**Now the greedy counterexample**, `nums = [2,1,1,2]`:

| `num` | rob | skip | new `curr` | new `prev` |
|---|---|---|---|---|
| 2 | 2 | 0 | **2** | 0 |
| 1 | 0 + 1 = 1 | **2** | **2** | 2 |
| 1 | 2 + 1 = **3** | 2 | **3** | 2 |
| 2 | 2 + 2 = **4** | 3 | **4** | 3 |

**4** ✅ — houses 0 and 3, a gap of two. No alternating strategy finds this.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over `nums` → **n iterations**.
- Each iteration is one addition, one `max`, and one tuple assignment — all **O(1)**.
- n × O(1) = **O(n)**.

**Against the alternatives:** brute force over all subsets is **O(2ⁿ · n)** — 2ⁿ subsets, each needing an O(n) validity check. The memoized recursion and this both reduce it to O(n), because there are only n distinct subproblems ("best through house i") and each is solved once.

**Can it be faster?** No. Every house's value can change the answer — flipping any single `nums[i]` can change the optimal subset — so all n values must be read. **Ω(n)** is a lower bound, and O(n) is optimal.

**Worth noting:** there's no best/worst case distinction here. The loop always runs exactly n times with no early exit, so the bound is tight rather than merely an upper limit.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers, `prev` and `curr`, regardless of how many houses there are.

| Version | Space | Why |
|---|---|---|
| Brute force over subsets | **O(n)** | The recursion stack / current subset |
| Recursion + memo | **O(n)** | n cache entries plus up to n stack frames |
| Bottom-up DP array | **O(n)** | A `dp` array of size n |
| **Rolling variables** | **O(1)** | The recurrence reads exactly two cells back |

Third problem in a row with the same reduction, and by now the rule should be automatic: **if `dp[i]` depends only on a fixed window of previous entries, replace the array with that many variables.**

Notice this version is even leaner than [70](70-climbing-stairs.md) and [746](746-min-cost-climbing-stairs.md) — no `current` temporary and no loop index, because the tuple assignment does the computation and the slide in a single step.

**What you'd need the array for:** reporting *which houses* to rob. You'd store the decision at each index and walk backwards, or keep the full `dp` and reconstruct by comparing `dp[i]` against `dp[i-1]` — equal means house `i` was skipped.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "At each house I have two options: skip it, and keep the best total through the previous house; or rob it, which means adding its value to the best total through the house *two* back, since the neighbour is off-limits. So `best(i) = max(best(i-1), best(i-2) + nums[i])`. Greedy doesn't work — 'rob every other house' fails on `[2,1,1,2]`, where the optimal picks houses 0 and 3 with a gap of two, and 'take the largest first' fails on `[2,3,2]`. The recurrence only looks two cells back, so I keep two rolling variables instead of an array and update them with a tuple assignment, which evaluates the right-hand side before assigning so both slide correctly. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the houses are in a circle?" | That's [House Robber II](213-house-robber-ii.md). The first and last are now adjacent, so they can't both be robbed — run this same linear solve twice, once on `nums[:-1]` and once on `nums[1:]`, and take the max. |
| "Which houses did you rob?" | Keep the `dp` array and walk backwards: if `dp[i] == dp[i-1]`, house `i` was skipped; otherwise it was robbed and you jump to `i-2`. Costs the O(n) space back. |
| "What if you couldn't rob houses within k of each other?" | `best(i) = max(best(i-1), best(i-k-1) + nums[i])`. The window is now k+1 wide, so you need k+1 variables — or just the array. |
| "What if values could be negative?" | Then never robbing is an option worth keeping, so clamp with `max(0, ...)`. As stated, values are ≥ 0, so robbing is never harmful. |
| "Can you do it with O(1) space *and* recover the path?" | Not both — reconstructing requires remembering the decisions, which is inherently O(n). |
| "What's the connection to Climbing Stairs?" | Same two-cell recurrence. 70 sums the branches to *count* routes; this takes the max to *choose* one. Same skeleton, different combining operator. |
| "Why not just take all non-adjacent maximums?" | There's no local rule that identifies them — which houses are optimal depends on the whole array. `[2,3,2]` is the smallest counterexample. |
| "What if `nums` is empty?" | This code returns 0 correctly, since both variables start at 0. The constraints say `n >= 1`, but it's free robustness worth pointing out. |

**Traps:**
- **Splitting the tuple assignment into two lines.** `prev = curr` followed by `curr = max(curr, prev + num)` reads the *new* `prev` and silently computes garbage. If you write it as two lines, you must compute the new `curr` first.
- **Assuming the answer alternates.** `[2,1,1,2]` disproves it, and it's the counterexample to have ready.
- Adding a special case for `len(nums) == 1`. Unnecessary — the zero-initialized variables handle it.
- Returning `max(prev, curr)` at the end. Harmless but redundant: `curr` is already ≥ `prev` by construction, since skipping is always one of the options.
- Indexing `nums[i-2]` inside the loop instead of trusting `prev`. It works, but it reintroduces the off-by-one risk the value-iteration avoids.

**This same move shows up in:** [House Robber II](213-house-robber-ii.md) (this exact function, called twice, to handle a circle) · [Climbing Stairs](70-climbing-stairs.md) (the same window, summing instead of maximizing) · [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) (the same window, minimizing) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (rolling state where a choice now blocks the next step — the same "taking this costs me the next slot" structure) · [Maximum Subarray](53-maximum-subarray.md) (a one-cell rolling decision: extend or restart).

</details>

---
