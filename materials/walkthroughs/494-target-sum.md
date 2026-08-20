# 494. Target Sum

**Medium** · [LeetCode](https://leetcode.com/problems/target-sum/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an integer array `nums` and an integer `target`. Build an expression by placing either **`+`** or **`-`** before **every** number and concatenating them. Return the **number of different expressions** that evaluate to `target`.

```
nums = [1,1,1,1,1], target = 3   →  5
        -1+1+1+1+1 = 3,  +1-1+1+1+1 = 3,  +1+1-1+1+1 = 3,
        +1+1+1-1+1 = 3,  +1+1+1+1-1 = 3

nums = [1], target = 1           →  1
```

**Constraints:** `1 <= nums.length <= 20` · `0 <= nums[i] <= 1000` · `0 <= sum(nums) <= 1000` · `-1000 <= target <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**number of** different expressions" | Counting, so the combining operator is `+`. Not optimization, not feasibility |
| "`+` or `-` before **every** number" | Every element gets a choice, and none can be skipped. That's a binary decision per index → **2ⁿ** expressions |
| "different **expressions**" | Expressions are counted by their **sign pattern**, not by their value. `[1,1]` has two distinct ways to make 0, even though the two `1`s are identical. **No deduplication** |
| `n <= 20` | 2²⁰ ≈ 10⁶ — brute force actually *fits* here. But the constraint is a trap: it's small enough that the naive answer passes, so the interesting question is what you'd do if it were 40 |
| `sum(nums) <= 1000` | The real hint. Every running total lies in `[−1000, 1000]`, so there are at most ~2000 distinct totals — far fewer than 2²⁰ expressions |

The brute force writes itself: at each index, branch on `+` and `−`, and when you run out of numbers, check whether the total equals `target`. That's a binary tree of depth n with 2ⁿ leaves.

Now the DP question — **do the branches ever collide?**

Consider `nums = [1, 1, 1]`. After two decisions there are four sign patterns, but only **three** distinct running totals: `+1+1 = 2`, `+1−1 = 0`, `−1+1 = 0`, `−1−1 = −2`. Two different paths arrive at the same place.

And here's the key: **once you're at index 2 with a total of 0, it does not matter how you got there.** The number of ways to finish is identical for both. So the state that actually determines the future is just:

```
(index, running total)
```

Not the sign pattern, not the path — those are history, and history is irrelevant. That's exactly the condition for memoization, and the state having **two** components is what puts this in Unit 14.

🤔 **Before you open the next section:** with `sum(nums) <= 1000`, how many distinct `(index, total)` pairs can there be? Compare that number to 2²⁰. Which one grows when you add another element to the array?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute-force recursion | Branch `+`/`−` at every index, count the leaves that hit the target | **O(2ⁿ)** | O(n) | ⚠️ At n = 20 it's 10⁶ and *passes* — but it's the answer that stops working the moment n grows |
| **Memoized recursion on `(i, total)`** | Same recursion, cached by state | O(n · S) | O(n · S) | ✅ |
| Bottom-up over reachable totals | A dict of `total → count`, extended one number at a time | O(n · S) | O(S) | ✅ Same idea iteratively, better space |
| Reduce to subset sum | Solve for the set of `+` numbers: `sum(P) = (target + total) / 2` | O(n · S) | O(S) | ✅ The slickest — see below |

**The decision:** **memoized recursion on `(index, running_total)`** — the brute force with one dict added.

**Why memoization helps so much here.** The number of *expressions* is 2ⁿ, but the number of *states* is `n × (number of distinct totals)`. Since `sum(nums) <= 1000`, every running total lies in `[−1000, 1000]` — at most 2001 values. So there are at most 20 × 2001 ≈ **40,000 states**, versus 2²⁰ ≈ **1,048,576 expressions**.

That's the entire DP pitch on this problem: **exponentially many paths, polynomially many states.** The same collapse as [Longest Common Subsequence](1143-longest-common-subsequence.md) and [Unique Paths](62-unique-paths.md) — many histories converge on the same situation, and only the situation matters.

**Why the state is two-dimensional.** You need the index (how many decisions remain) *and* the running total (where those decisions have to get you). Neither alone is enough: the same total at different indices has different answers, and the same index with different totals does too.

**Why a dict rather than a 2-D array.** Totals can be **negative**, which a list can't index directly — you'd need to offset by `sum(nums)`. And the reachable totals are sparse: with `nums = [1000, 1000]` only a handful of the 2001 possible totals ever occur. A [dict](../data-structures/hashmap.md) keyed on the tuple handles both cleanly.

**The reduction worth knowing.** Split the numbers into the set `P` that gets `+` and the set `N` that gets `−`. Then:

```
sum(P) − sum(N) = target
sum(P) + sum(N) = total          (every number is in one set)
⟹  sum(P) = (target + total) / 2
```

So the problem becomes: **how many subsets sum to `(target + total) / 2`?** That's exactly [Partition Equal Subset Sum](416-partition-equal-subset-sum.md)'s machinery, counting instead of testing feasibility — a 0/1 knapsack with a downward sweep. It's O(n · S) time and **O(S)** space, and it returns 0 immediately when `target + total` is odd or `|target| > total`.

It's the more elegant answer. The memoized version is the one that comes to mind under pressure, and it's easier to derive from scratch — **write that, then mention the reduction.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
memo = {}
```
The cache, keyed on the **full state** `(i, total)`. Without it the recursion is O(2ⁿ); with it, each state is computed once and reused.

A dict rather than a 2-D list, because totals go negative and the reachable set is sparse.
→ [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dfs(i, total):
    if i == len(nums):
        return 1 if total == target else 0
```
**The base case, and it's where the counting actually happens.**

Once every number has a sign, the expression is complete. If it evaluates to `target`, this leaf contributes exactly **1** way; otherwise **0**. Returning a count rather than a boolean is what lets the parent calls simply add up their children.

The [ternary](../syntax/ternary-expression.md) is the whole check — no partial credit, no tolerance.
→ [function-basics](../syntax/function-basics.md) · [ternary-expression](../syntax/ternary-expression.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    if (i, total) in memo:
        return memo[(i, total)]
```
The cache lookup, keyed on **both** components. Keying on `i` alone would merge genuinely different situations and give wrong answers; keying on `total` alone would ignore how many numbers remain.

This is the line that converts 2ⁿ into n × S.
→ [membership-operators](../syntax/membership-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
    memo[(i, total)] = dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i])
    return memo[(i, total)]
```
**The recurrence, and it's one line because the two choices are symmetric.**

- `dfs(i + 1, total + nums[i])` — put a **`+`** before this number.
- `dfs(i + 1, total - nums[i])` — put a **`−`** before it.

Both advance the index by one, since every number must get a sign — there's no "skip" option here, which is what distinguishes this from a subset problem where elements can be left out.

They're **added**, not `max`'d, because you're counting: every valid completion of the `+` branch and every valid completion of the `−` branch is a distinct expression, and the branches can't overlap (they differ in this position's sign).

Assigning into the memo and returning it on the next line is a compact way to cache and return, though `result = ...; memo[...] = result; return result` reads a little more clearly.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [dict-basics](../syntax/dict-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dfs(0, 0)
```
Start at index 0 with a running total of 0 — no numbers placed, nothing accumulated.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:

        memo = {}

        def dfs(i, total):
            if i == len(nums):
                return 1 if total == target else 0
            if (i, total) in memo:
                return memo[(i, total)]

            memo[(i, total)] = dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i])
            return memo[(i, total)]

        return dfs(0, 0)
```
</details>

**Trace it** — `nums = [1, 1, 1]`, `target = 1` (answer should be 3)

The states reachable at each index, and how many ways each finishes:

| index | total | how it finishes | ways |
|---|---|---|---|
| 3 | 3 | `3 == 1`? no | 0 |
| 3 | 1 | `1 == 1`? **yes** | **1** |
| 3 | −1 | no | 0 |
| 3 | −3 | no | 0 |
| 2 | 2 | `dfs(3,3)` + `dfs(3,1)` = 0 + 1 | **1** |
| 2 | 0 | `dfs(3,1)` + `dfs(3,-1)` = 1 + 0 | **1** |
| 2 | −2 | `dfs(3,-1)` + `dfs(3,-3)` = 0 + 0 | 0 |
| 1 | 1 | `dfs(2,2)` + `dfs(2,0)` = 1 + 1 | **2** |
| 1 | −1 | `dfs(2,0)` + `dfs(2,-2)` = 1 + 0 | **1** |
| 0 | 0 | `dfs(1,1)` + `dfs(1,-1)` = 2 + 1 | **3** |

Return **3** ✅ — `+1+1−1`, `+1−1+1`, `−1+1+1`.

The memoization is visible in the `index = 2` rows. State `(2, 0)` is reached by **two** different paths — `+1−1` and `−1+1` — and it's computed once and reused. With three elements that saves one call; with twenty, the same collapse happens at every level and saves the bulk of a million.

Notice also that there are only **4 states at index 3, 3 at index 2, 2 at index 1** — nine states total instead of 2³ = 8 leaves plus internal nodes. The saving grows fast: at index `i` there are at most `i + 1` distinct totals for this input, so the state count is quadratic while the path count is exponential.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · S)</summary>

**O(n · S)**, where S = `sum(nums)` and the running total ranges over `[−S, S]`.

Using the standard formula for memoized DP — **number of states × work per state**:

- **States:** n index values × at most `2S + 1` distinct totals → **O(n · S)**.
- **Work per state:** two recursive calls (each O(1) after the first time), one addition, one dict write → **O(1)**.
- Total: **O(n · S)**.

With the given limits: 20 × 2001 ≈ **4 × 10⁴** states. Compare 2²⁰ ≈ **10⁶** expressions — a 25× saving, and the gap widens exponentially with n.

**The honest caveat:** at n = 20 the brute force is also fast enough. The constraints here don't *force* memoization. So the reason to reach for it isn't this input — it's that the technique is what the problem is teaching, and it's the difference between an approach that scales and one that doesn't.

**Pseudo-polynomial, again.** This is linear in the *value* of `sum(nums)`, not in its bit length — the same classification as [Coin Change](322-coin-change.md) and [Partition Equal Subset Sum](416-partition-equal-subset-sum.md). Target Sum reduces to subset sum, which is NP-complete, so a genuinely polynomial algorithm shouldn't be expected. **When you see an NP-complete problem with a fast DP, check what's actually bounded** — here it's the sum.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · S)</summary>

**O(n · S)**, from the memo, plus **O(n)** for the recursion stack (at most one frame per index — 20 here, trivially safe).

The memo dominates, though in practice it's much smaller than the bound: only *reachable* totals get keys, and for arrays with large values most of the range is never touched.

| Version | Space | Why |
|---|---|---|
| Brute-force recursion | **O(n)** | Just the stack — no cache. But O(2ⁿ) time |
| **Memoized recursion** | **O(n · S)** | One entry per `(index, total)` state |
| Bottom-up dict of `total → count` | **O(S)** | Only the current index's totals are kept |
| Subset-sum reduction | **O(S)** | A single array over sums |

**The bottom-up version drops the index dimension entirely**, which is the natural improvement:

```python
counts = {0: 1}
for num in nums:
    new_counts = defaultdict(int)
    for total, ways in counts.items():
        new_counts[total + num] += ways
        new_counts[total - num] += ways
    counts = new_counts
return counts[target]
```

**O(S)** space, no recursion. The index disappears because you process numbers in order and only ever need the *current* layer of totals — the same "keep only what the recurrence reads" principle as [Unique Paths](62-unique-paths.md)'s rolling row, one dimension down.

Note the structural echo of [Partition Equal Subset Sum](416-partition-equal-subset-sum.md): build `new_counts` separately rather than mutating `counts` in place, so a total created by this number can't be extended again by the same number.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every number gets a sign, so there are 2ⁿ expressions and the brute force is a binary recursion. But many different sign patterns arrive at the same running total at the same index — and once I'm at index i with total t, how I got there doesn't affect how many ways I can finish. So the state is `(index, running_total)`, and I memoize on that. Since `sum(nums)` is capped at 1000, there are at most about 20 × 2000 = 40,000 states versus a million expressions. I use a dict rather than an array because totals go negative and the reachable set is sparse. O(n · sum) time and space. Two refinements: I can drop the index dimension with a bottom-up dict of total-to-count for O(sum) space, and there's a neat reduction — if P is the set of positives, `sum(P) = (target + total) / 2`, so this is just counting subsets with a given sum, which is 0/1 knapsack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does memoizing help if n is only 20?" | It doesn't strictly need to here — 2²⁰ passes. But the state count is polynomial while the path count is exponential, so it's the version that survives n = 40. |
| "Show me the subset-sum reduction." | Let P be the `+` numbers and N the `−` ones. `sum(P) − sum(N) = target` and `sum(P) + sum(N) = total`, so `sum(P) = (target + total) / 2`. Count subsets summing to that. Return 0 if it's not a non-negative integer. |
| "When does the reduction return 0 immediately?" | If `target + total` is odd (no integer solution), or if `abs(target) > total` (unreachable even with all signs aligned). |
| "Make it O(sum) space." | Bottom-up: a dict mapping running total → number of ways, rebuilt for each number. The index dimension vanishes. |
| "What if zeros are in the array?" | Each zero doubles the count, since `+0` and `−0` are different *expressions* with the same value. The DP handles it automatically — both branches recurse to the same state and their counts add. |
| "Why not deduplicate identical expressions?" | The problem counts sign patterns, not distinct values. `[1,1]` reaching 0 two ways is two expressions. |
| "Could you use `@cache` instead of a manual dict?" | Yes — decorate `dfs` with `functools.cache`. Same complexity, less code, and it keys on the arguments automatically. |
| "Is this really polynomial?" | Pseudo-polynomial — linear in the *value* of the sum. Target Sum reduces to subset sum, which is NP-complete, so no truly polynomial algorithm is expected. |

**Traps:**
- **Keying the memo on `i` alone.** The most damaging bug — it merges different totals and returns confidently wrong counts.
- Returning a boolean from the base case instead of `1`/`0`. You'd be testing feasibility, not counting.
- Using `max` instead of `+` in the recurrence. Counting problems sum their branches; only optimization problems take extremes.
- Trying to skip numbers. Every element must receive a sign — this is not a subset-selection problem in its original form.
- Assuming zeros can be ignored. They double the answer each time.
- Indexing a plain list by the running total without offsetting by `sum(nums)` — negative totals wrap around silently in Python.

**This same move shows up in:** [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (the same reachable-sums machinery, testing feasibility rather than counting — and what this problem reduces to) · [Coin Change II](518-coin-change-ii.md) (counting over sums, where loop order prevents double-counting) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (memoizing on a two-part state where history is irrelevant) · [Longest Common Subsequence](1143-longest-common-subsequence.md) (exponentially many objects, polynomially many states).

</details>

---
