# 518. Coin Change II

**Medium** · [LeetCode](https://leetcode.com/problems/coin-change-ii/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an integer `amount` and an array of distinct coin denominations `coins`. Return the **number of combinations** that make up that amount. You have an **infinite supply** of each coin. If no combination works, return 0.

```
amount = 5, coins = [1,2,5]   →  4      5 ; 2+2+1 ; 2+1+1+1 ; 1+1+1+1+1
amount = 3, coins = [2]       →  0
amount = 10, coins = [10]     →  1
```

**Constraints:** `1 <= coins.length <= 300` · `1 <= coins[i] <= 5000` · all coins are **distinct** · `0 <= amount <= 5000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**number of combinations**" | Counting, so the combining operator is `+`. Contrast [Coin Change](322-coin-change.md), which minimized |
| "**combinations**", not permutations | `2+2+1` and `1+2+2` are the **same** answer. Order does not matter — and this single word is the entire problem |
| "**infinite supply**" | Unbounded knapsack. A coin can be reused, so you never track how many are left |
| coins are **distinct** | No duplicate denominations to worry about |
| `amount <= 5000`, `coins <= 300` | 5000 × 300 = 1.5 × 10⁶. That product is the intended complexity |

The recurrence looks like [Coin Change](322-coin-change.md) with `min` swapped for `+`:

```
ways(a) = Σ over coins c of ways(a − c)
```

**But that formula is wrong**, and seeing why is the whole point of this problem.

Run it on `amount = 3`, `coins = [1,2]`. It computes `ways(3) = ways(2) + ways(1) = 2 + 1 = 3`. Those three are `1+1+1`, `1+2`, and `2+1`. But `1+2` and `2+1` are **the same combination** — the problem counts them once. The correct answer is **2**.

The formula counts **permutations**, because "the last coin was a 1" and "the last coin was a 2" are treated as distinct histories even when the multiset is identical.

So the real question is: **how do you count each multiset exactly once?**

The standard fix is to impose an order. Decide that coins must be considered in a **fixed sequence**, and that once you move past a denomination you never come back to it. Then every combination has exactly one canonical construction — *"use some number of 1s, then some number of 2s, then some number of 5s"* — and no double-counting is possible.

That ordering is what makes this a **2-D** problem: the state becomes `(which coins are available, amount remaining)`, not just the amount.

🤔 **Before you open the next section:** if you're going to process coins one at a time and never revisit them, what does the table look like after you've processed only the first coin? And what does adding the second coin do to it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate every combination | Recurse on all coin choices | exponential | O(amount) | ❌ |
| 1-D DP, **amount outer / coin inner** | `dp[a] += dp[a-c]` sweeping amounts first | O(a·c) | O(a) | ❌ **Counts permutations.** Gives 3 instead of 2 on the example above |
| 2-D DP | `dp[i][a]` = ways using the first `i` coins to make `a` | O(a·c) | **O(a·c)** | ✅ Correct, and the clearest way to see *why* |
| **1-D DP, coin outer / amount inner** | Same table, collapsed to one row | O(a·c) | **O(amount)** | ✅ |

**The decision:** the **1-D array with coins on the outer loop** — the space-collapsed form of the 2-D table.

**The 2-D table is the honest version, so start there.** Let `dp[i][a]` = the number of ways to make amount `a` using only the first `i` coin types. Then for each new coin you have two options:

```
dp[i][a] = dp[i-1][a]          ← don't use coin i at all
         + dp[i][a - coin]     ← use at least one coin i
```

The first term skips the coin entirely; the second uses one and stays on row `i`, allowing it to be used again — that's the "unbounded" part. **Because coins are introduced in a fixed order and you never return to an earlier row, each multiset is built exactly one way.** Order-independence is enforced structurally.

**Now collapse it.** Row `i` reads only row `i-1` (same column) and row `i` (a smaller column). Two rows suffice — and in fact **one** does, if you sweep amounts **upward**: `dp[a] += dp[a - coin]` reads a smaller index that has already been updated for the *current* coin (giving the `dp[i][a-coin]` term) while `dp[a]` itself still holds the previous coin's value (giving `dp[i-1][a]`). One array, both terms, no explicit second row.

**So the loop order isn't a style choice — it's the algorithm.** Coins outer means "finish considering coin 1 everywhere before introducing coin 2," which is the fixed ordering that kills permutations. Amounts outer means "at each amount, consider every coin," which reintroduces them.

**The contrast with [Coin Change](322-coin-change.md) is the thing to remember.** There, the loop order genuinely didn't matter — you were taking a `min`, and the minimum over a set doesn't care how many times you reach it or in what order. Here you're **summing**, and a sum absolutely does care. **Counting problems are sensitive to double-counting in a way that optimization problems aren't.**

**Why the inner loop sweeps upward** (unlike [Partition Equal Subset Sum](416-partition-equal-subset-sum.md), which sweeps down): upward reuse is *wanted* here, because supply is unlimited. In the 0/1 case you sweep downward precisely to prevent it. **Same array, opposite direction, opposite meaning.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [0] * (amount + 1)
dp[0] = 1
```
`dp[a]` = the number of combinations making amount `a` with the coins processed so far.

**`dp[0] = 1` is the seed, and it's the least obvious line here.** There is exactly **one** way to make zero: take no coins. The empty combination is a real combination, and it's what every other count is ultimately built from — every completed combination bottoms out by reducing the remaining amount to 0. Seed it as 0 and the entire array stays 0.

Same "the empty case succeeds" base as `dp[n] = True` in [Word Break](139-word-break.md) and `ways("") = 1` in [Decode Ways](91-decode-ways.md).
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for coin in coins:   # coins on the outer loop so permutations aren't double-counted
```
**The outer loop, and the entire correctness of the solution.**

This says: *fully incorporate coin `c` across all amounts, then move on and never return to it.* That's the fixed ordering from section 2 — it's what makes each combination constructible exactly one way, and it's the collapsed form of "process row `i` of the 2-D table."

Swap this with the inner loop and you count permutations. Same three lines, wrong problem.
→ [for-loop](../syntax/for-loop.md)

```python
    for a in range(coin, amount + 1):
```
Sweep amounts **upward**, starting at `coin` — smaller amounts can't use this coin at all, so there's nothing to add, and starting at `coin` also removes the need for a bounds guard on `a - coin`.

**Upward is deliberate.** `dp[a - coin]` refers to a smaller amount that has *already* been updated for the current coin, which is exactly what lets the coin be used repeatedly — the unbounded behaviour. Sweeping downward would read the previous coin's values and give you 0/1 knapsack instead, where each coin is used at most once.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        dp[a] += dp[a - coin]
```
**The recurrence, with both 2-D terms hiding in one line.**

- The **`dp[a]` being added to** still holds its value from before this coin was introduced — that's `dp[i-1][a]`, the "don't use this coin" case.
- **`dp[a - coin]`** has already been updated for this coin — that's `dp[i][a - coin]`, the "use at least one of this coin" case.

`+=` performs the addition of the two, in place. **One array doing the work of two rows**, which is only possible because of the upward sweep.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [nested-lists](../syntax/nested-lists.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[amount]
```
The number of combinations making the target using all the coins. Returns 0 naturally if nothing works, since the array started at 0.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:

        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:   # coins on the outer loop so permutations aren't double-counted
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]

        return dp[amount]
```
</details>

**Trace it** — `amount = 5`, `coins = [1, 2, 5]`

Start: `dp = [1, 0, 0, 0, 0, 0]`

**After coin 1** — sweeping `a = 1..5`, each `dp[a] += dp[a-1]`:

| index | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `dp` | 1 | 1 | 1 | 1 | 1 | 1 |

One way to make every amount using only 1s. Correct.

**After coin 2** — sweeping `a = 2..5`, each `dp[a] += dp[a-2]`:

| `a` | `dp[a]` before | `+ dp[a-2]` | `dp[a]` after |
|---|---|---|---|
| 2 | 1 | `dp[0]` = 1 | **2** |
| 3 | 1 | `dp[1]` = 1 | **2** |
| 4 | 1 | `dp[2]` = **2** | **3** |
| 5 | 1 | `dp[3]` = **2** | **3** |

| index | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `dp` | 1 | 1 | 2 | 2 | 3 | 3 |

Row `a = 4` shows the unbounded behaviour: `dp[2]` was **already updated to 2** during this same sweep, so using a 2 twice is counted. That's the upward direction doing its job.

**After coin 5** — sweeping `a = 5`:

| `a` | before | `+ dp[0]` | after |
|---|---|---|---|
| 5 | 3 | 1 | **4** |

Return `dp[5]` = **4** ✅ — `5`, `2+2+1`, `2+1+1+1`, `1+1+1+1+1`.

**Now the wrong loop order**, on `amount = 3`, `coins = [1,2]`:

```python
for a in range(1, amount + 1):      # amounts OUTER — wrong
    for coin in coins:
        if coin <= a:
            dp[a] += dp[a - coin]
```

| `a` | contributions | `dp[a]` |
|---|---|---|
| 1 | `dp[0]` = 1 | 1 |
| 2 | `dp[1]` = 1, `dp[0]` = 1 | 2 |
| 3 | `dp[2]` = 2, `dp[1]` = 1 | **3** |

Returns **3** — counting `1+2` and `2+1` separately. The correct answer is **2**. Identical arithmetic, two loops swapped, different problem.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(amount × len(coins))</summary>

**O(amount · c)**, where c = `len(coins)`.

- The outer loop runs **c** times, once per denomination.
- The inner loop runs at most **`amount`** times.
- Each iteration is one array read, one addition, one write — **O(1)**.
- c × amount × O(1) = **O(amount · c)**.

At the limits: 300 × 5000 = **1.5 × 10⁶** operations. Comfortable, and clearly what the constraints were sized for.

**Same bound as [Coin Change](322-coin-change.md)** — the two problems have identical complexity and nearly identical code. The difference is entirely in the *meaning*: `min` versus `+`, and loop order irrelevant versus load-bearing.

**Against brute force:** enumerating combinations is exponential. The DP works because many different partial combinations reach the same `(coins processed, amount remaining)` state, and only that state matters — not the path taken to it.

**Pseudo-polynomial, again.** Like [Coin Change](322-coin-change.md) and [Partition Equal Subset Sum](416-partition-equal-subset-sum.md), this is linear in the *value* of `amount`, which is exponential in its bit length. Standard for the knapsack family, and worth naming.

**Faster?** Not meaningfully. There are generating-function approaches, but nothing beats O(amount · c) for the general case.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(amount)</summary>

**O(amount)** — one array of `amount + 1` integers. At the limits, 5001 entries.

| Version | Space | Why |
|---|---|---|
| Recursion + memo on `(coin index, amount)` | **O(amount · c)** | A cache entry per state, plus recursion depth |
| Full 2-D table | **O(amount · c)** | `dp[i][a]` for every coin prefix and amount — 1.5 × 10⁶ entries |
| **One rolling array** | **O(amount)** | Row `i` reads only row `i−1` and itself |

**Why one array suffices rather than two.** In [Unique Paths](62-unique-paths.md) the collapse needed a `new_row` alongside `row`, because each cell read the previous row at the *same* column. Here the "don't use this coin" term is `dp[i-1][a]` — the **same index**, which hasn't been touched yet in this sweep — and the "use this coin" term is `dp[i][a-coin]` — a **smaller index**, already updated. The two terms live at different indices in the same array, so no second row is needed.

**That's why the sweep direction is the whole implementation.** Upward: smaller indices are current-coin values → unbounded reuse. Downward: smaller indices are previous-coin values → each coin used at most once, which is exactly what [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) needs. **One direction flip converts unbounded knapsack into 0/1 knapsack.**

**Can it go below O(amount)?** No. Any amount from 0 to the target may be needed, and there's no bounded lookback window — the same reason [Coin Change](322-coin-change.md) can't collapse to variables.

**Note on integer size:** the counts can be enormous (combinations grow fast), but Python ints are arbitrary precision so nothing overflows. In Java or C++ this would need `long`, and the problem guarantees the answer fits in a signed 32-bit integer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The naive recurrence — ways(a) = sum of ways(a − coin) over all coins — counts *permutations*, not combinations. On amount 3 with coins [1,2] it gives 3, counting 1+2 and 2+1 separately, when the answer is 2. To count each multiset once I impose a fixed order on the coins: consider coin 1 across all amounts, then coin 2, and never go back. That's a 2-D state — which coins are available, and how much is left — where `dp[i][a] = dp[i-1][a] + dp[i][a-coin]`: skip this coin, or use at least one of it. Collapsed to one array, that's coins on the outer loop and amounts sweeping upward. Upward matters: `dp[a-coin]` is already updated for the current coin, which is what allows unlimited reuse — sweeping downward would give me 0/1 knapsack instead. And `dp[0] = 1`, because there's exactly one way to make zero: take nothing. O(amount × coins) time, O(amount) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if you swap the loops?" | You count permutations. On amount 3 with `[1,2]` you'd get 3 instead of 2, because `1+2` and `2+1` become distinct. |
| "Why did the loop order not matter in Coin Change?" | Because that problem takes a `min`. The minimum over a set doesn't care how many times or in what order you reach it. Summing does — double-counting corrupts a sum but not a minimum. |
| "Why `dp[0] = 1`?" | There's exactly one way to make zero — the empty combination. Every completed combination bottoms out there, so seeding 0 makes the whole array 0. |
| "Why sweep amounts upward?" | So `dp[a - coin]` already reflects the current coin, allowing it to be used repeatedly. Downward would read the previous coin's values — that's 0/1 knapsack, where each item is used at most once. |
| "Count *permutations* instead." | Swap the loops: amounts outer, coins inner. That's the [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) recurrence — misleadingly named, since it actually counts permutations. |
| "What if each coin could be used only once?" | Sweep the inner loop **downward**: `for a in range(amount, coin - 1, -1)`. Same as [Partition Equal Subset Sum](416-partition-equal-subset-sum.md). |
| "Show me the 2-D version." | `dp[i][a] = dp[i-1][a] + dp[i][a-coins[i-1]]` with `dp[*][0] = 1`. The 1-D version is that table with the row dimension collapsed away. |
| "List the combinations rather than count them." | Backtracking, not DP — the output can be exponentially large. That's [Combination Sum](39-combination-sum.md), where passing a `start` index enforces the same non-decreasing order this problem enforces via loop order. |

**Traps:**
- **Swapping the loops.** The defining bug. Everything else is identical and the answer is silently wrong.
- **Forgetting `dp[0] = 1`.** Every answer becomes 0.
- **Sweeping the inner loop downward.** Silently solves the 0/1 variant — each coin used at most once.
- Adding a `if coin <= a` guard *and* starting the range at `coin` — harmless duplication, but it suggests you haven't noticed the range already handles it.
- Assuming this is [Coin Change](322-coin-change.md) with `min` swapped for `+`. The operator changes, and so does the loop-order requirement.
- Sizing the array `amount` instead of `amount + 1` — no slot for the target or the base case.

**This same move shows up in:** [Coin Change](322-coin-change.md) (the same array and bound, minimizing — where loop order genuinely doesn't matter) · [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (the 0/1 variant, where the sweep direction reverses) · [Combination Sum](39-combination-sum.md) (enforcing non-decreasing order via a `start` index, the backtracking analogue of coins-on-the-outside) · [Target Sum](494-target-sum.md) (another counting DP over reachable sums).

</details>

---
