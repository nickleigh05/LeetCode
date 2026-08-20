# 322. Coin Change

**Medium** · [LeetCode](https://leetcode.com/problems/coin-change/) · [Solution file (no hints)](../../problems/0001-0499/322.py)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

---

You're given an array `coins` of coin denominations and an integer `amount`. Return the **fewest number of coins** needed to make up that amount. If it can't be made from any combination, return `-1`. You have an **infinite supply** of each coin.

```
coins = [1,2,5],  amount = 11   →  3      5 + 5 + 1
coins = [2],      amount = 3    →  -1
coins = [1],      amount = 0    →  0
coins = [1,3,4],  amount = 6    →  2      3 + 3  (greedy would say 4+1+1 = 3 coins)
```

**Constraints:** `1 <= coins.length <= 12` · `1 <= coins[i] <= 2³¹−1` · `0 <= amount <= 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**fewest** number of coins" | Minimization. The combining operator is `min` |
| "**infinite supply** of each coin" | This is the **unbounded** knapsack shape. A coin can be reused, so subproblems don't need to track which coins are left — that's what keeps the state one-dimensional |
| order doesn't matter | `5+5+1` and `1+5+5` are the same answer. You're counting coins, not arrangements |
| "`-1` if impossible" | Some amounts are unreachable — `[2]` can never make 3. You need a sentinel that survives the arithmetic |
| `amount <= 10⁴`, `len(coins) <= 12` | 10⁴ × 12 = 1.2 × 10⁵ operations. Tiny. That product is a strong hint at the intended shape: **O(amount × coins)** |
| coins can be up to 2³¹−1 | A coin can exceed the amount, so every use must be guarded |

The DP question, asked as always by standing at the goal and looking back: **you need to make `amount`. What was the last coin you used?**

It was one of the coins in the array. If it was coin `c`, then before placing it you had made `amount - c`, using the fewest coins possible for *that* amount. So:

```
minCoins(amount) = 1 + min( minCoins(amount − c) for every coin c ≤ amount )
```

The `1 +` is the coin you just placed. The `min` picks the best last coin — and crucially you **try all of them**, because there's no way to know in advance which leads to the best total.

That last point is the crux of this problem. Example 4 is there on purpose: with `coins = [1,3,4]` and `amount = 6`, taking the biggest coin first (4) leaves 2, needing 1+1 — three coins total. Taking 3+3 needs only two. **The locally largest coin is not always part of the best answer.**

🤔 **Before you open the next section:** with US coins (1, 5, 10, 25), grabbing the largest coin that fits always gives the optimal answer. With `[1,3,4]` it doesn't. What's different about those two coin systems — and can you tell which kind you have just by looking at it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy — largest coin first | Repeatedly take the biggest coin that fits | O(amount) | O(1) | ❌ **Wrong.** `[1,3,4]`, amount 6 → greedy gives 3 coins, optimal is 2 |
| Try every combination | Recurse on every coin at every step | **O(cᵃᵐᵒᵘⁿᵗ)** | O(amount) | ❌ Exponential |
| Recursion + memo (top-down) | Same, cached by amount | O(amount · c) | O(amount) + stack | ⚠️ Correct — but recursion depth can hit 10⁴ with `coins = [1]`, risking a stack overflow |
| **Bottom-up DP array** | Solve every amount from 1 up to the target, in order | O(amount · c) | O(amount) | ✅ |
| BFS on amounts | Levels = coin count; first time you reach `amount` is the fewest | O(amount · c) | O(amount) | ✅ Also correct, and a nice reframing — the level *is* the answer |

**The decision:** **bottom-up DP** over an array indexed by amount.

**Why greedy fails, and how to explain it.** Greedy works on so-called *canonical* coin systems — real currencies are designed to be canonical, which is exactly why the intuition feels so reliable. `[1,3,4]` isn't canonical: taking the 4 leaves a remainder that can only be paid in 1s. There's no quick test for canonicity (checking it is itself a nontrivial algorithm), so **with arbitrary denominations you cannot assume greedy is safe**. Having `[1,3,4]` and `amount = 6` ready is worth more than any amount of arguing.

**Why the state is one-dimensional.** This is the detail that separates this from [Coin Change II](518-coin-change-ii.md) and other knapsack variants. Because supply is infinite and order doesn't matter, the *only* thing that describes a subproblem is **how much is left to make**. You don't need to know which coins you've used or how many — so `dp` is indexed by amount alone, and it's O(amount) rather than O(amount × coins).

**Why bottom-up over memoized recursion?** Same complexity, but with `coins = [1]` and `amount = 10⁴` the top-down version recurses 10,000 deep and blows Python's default limit of 1000. Bottom-up has no stack at all. That's a concrete, defensible reason — better than "I prefer iterative."

**Worth knowing: this is BFS in disguise.** Treat amounts as nodes and coins as edges of weight 1. The fewest coins is the shortest path from 0 to `amount` on an unweighted graph — so BFS finds it, and the level at which you first reach `amount` *is* the answer. Same complexity, and it can exit early. Naming this connection is a strong signal; the DP is still the cleaner thing to write.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [0] + [float("inf")] * amount
```
`dp[i]` = the fewest coins that make amount `i`. The array is `amount + 1` long, so it's indexed 0 through `amount` inclusive.

Two seeds in one line:
- **`dp[0] = 0`** — making zero takes zero coins. The base case everything is built from, and it's also why `amount = 0` correctly returns 0 with no special case.
- **Everything else is `inf`** — meaning *not yet known to be reachable*. [`float("inf")`](../syntax/float-inf.md) is the right sentinel because it compares greater than any real count, so `min` naturally ignores it, and `inf + 1` is still `inf` — an unreachable amount can't accidentally become reachable through arithmetic. Using `-1` or `0` as the sentinel here would break both properties.
→ [float-inf](../syntax/float-inf.md) · [list-basics](../syntax/list-basics.md) · [list-methods](../syntax/list-methods.md)

```python
for i in range(1, amount + 1):
```
The outer loop: solve **every** amount from 1 up to the target, in increasing order.

That order is what makes it work — when you compute `dp[i]`, every smaller amount is already final, so `dp[i - coin]` is a finished answer rather than a guess. This is the bottom-up guarantee, and it's why no recursion is needed.

Solving *all* intermediate amounts may feel wasteful when you only want one, but it's exactly what removes the exponential blowup: each of the `amount` subproblems is solved once instead of being rediscovered down countless paths.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    for coin in coins:
        if coin <= i:
```
The inner loop tries **every coin as the last coin placed**. There's no way to know which is best, so you check them all — that's the direct repudiation of greedy.

The guard `coin <= i` prevents a negative index. Without it, `dp[i - coin]` with a coin larger than `i` would wrap around to the end of the list in Python and silently read a garbage value — a wrong answer rather than a crash, which is the worst kind of bug. Given coins can be up to 2³¹−1, this fires often.
→ [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
            dp[i] = min(dp[i], dp[i - coin] + 1)
```
**The recurrence.** Compare what you already have (`dp[i]`, the best found so far from previously-tried coins) against a new candidate: solve `i - coin` optimally, then add **one** coin to reach `i`.

The `min` against `dp[i]` is how the loop accumulates a best across all coins — each iteration either improves it or leaves it alone.

And the `inf` sentinel earns its place here: if `dp[i - coin]` is `inf`, the candidate is `inf + 1` = `inf`, which never wins the `min`. Unreachability propagates correctly with no special-case branch.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[amount] if dp[amount] != float("inf") else -1
```
Still `inf` means no combination of coins reaches the target → `-1`. Otherwise it's the fewest coins.

This translation at the boundary is why `inf` was the right internal sentinel: it behaves correctly in arithmetic *and* is unambiguous to test for at the end.
→ [ternary-expression](../syntax/ternary-expression.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        dp = [0] + [float("inf")] * amount

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float("inf") else -1
```
</details>

**Trace it** — `coins = [1, 3, 4]`, `amount = 6` (the anti-greedy case)

| `i` | coin 1 | coin 3 | coin 4 | `dp[i]` |
|---|---|---|---|---|
| 0 | — | — | — | **0** |
| 1 | `dp[0]+1` = 1 | too big | too big | **1** |
| 2 | `dp[1]+1` = 2 | too big | too big | **2** |
| 3 | `dp[2]+1` = 3 | `dp[0]+1` = **1** | too big | **1** |
| 4 | `dp[3]+1` = 2 | `dp[1]+1` = 2 | `dp[0]+1` = **1** | **1** |
| 5 | `dp[4]+1` = **2** | `dp[2]+1` = 3 | `dp[1]+1` = 2 | **2** |
| 6 | `dp[5]+1` = 3 | `dp[3]+1` = **2** | `dp[2]+1` = 3 | **2** |

Return **2** ✅ — that's 3 + 3.

The last row is the whole lesson. Greedy would take the 4 (`dp[2]+1` = 3 coins) because 4 is the biggest coin that fits. The DP evaluates all three options and finds that going through `dp[3]` — itself a single 3-coin — gives **2**. The winning path never uses the largest coin at all.

**And `coins = [2]`, `amount = 3`:**

| `i` | coin 2 | `dp[i]` |
|---|---|---|
| 1 | too big | `inf` |
| 2 | `dp[0]+1` = 1 | **1** |
| 3 | `dp[1]+1` = `inf + 1` = `inf` | **`inf`** |

`dp[3]` is still `inf` → **-1** ✅. Notice how the unreachability of amount 1 propagated to amount 3 through the arithmetic, with no explicit check.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(amount × len(coins))</summary>

**O(amount × c)**, where c = `len(coins)`.

- The outer loop runs **`amount`** times.
- The inner loop runs **c** times, doing O(1) work each — a comparison, an array read, an addition, a `min`.
- amount × c × O(1) = **O(amount · c)**.

At the constraint limits: 10⁴ × 12 = **1.2 × 10⁵** operations. Instant.

**Against the alternatives:** brute-force recursion is **O(c^amount)** — every position branches c ways with no caching. Memoization or bottom-up bring it to O(amount · c), because there are only `amount` distinct subproblems and each costs O(c) to solve.

**A note on "pseudo-polynomial".** This is polynomial in the *value* of `amount`, not in its *input size* — `amount` takes only log(amount) bits to write down, so an algorithm linear in `amount` is exponential in its bit length. That's the standard classification for knapsack-family problems, and mentioning it is the kind of precision interviewers notice. It also explains why this approach would be hopeless if `amount` were 10¹⁸.

**Can you exit early?** Not in this formulation, since every amount must be solved anyway. The BFS variant *can* — it stops the moment it reaches `amount`, which is often much sooner, though the worst case is unchanged.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(amount)</summary>

**O(amount)** — the `dp` array holds `amount + 1` values.

At the limit that's 10,001 entries. Nothing else is allocated: no recursion, no auxiliary structures, and the loop variables are O(1).

**Why can't this collapse to O(1) like the rest of Unit 13?** Because the dependency window isn't fixed. In [Climbing Stairs](70-climbing-stairs.md) and [House Robber](198-house-robber.md), `dp[i]` looked exactly two cells back, so two variables sufficed. Here `dp[i]` reads `dp[i - coin]` for **every coin**, and coins can be as large as the amount itself. With `coins = [1, 9999]`, computing `dp[10000]` needs `dp[1]` — a value from 9,999 positions back.

**So the rule from earlier in the unit still holds, it just doesn't apply:** *replace the array with variables only when the lookback distance is bounded by a constant.* Here it's bounded by `max(coins)`, which isn't constant. This is a good problem to be able to say that about — it shows you understood *why* the optimization worked before, rather than pattern-matching it.

**What you'd need beyond the array:** to report *which* coins were used, store the winning coin per amount and walk backwards from `amount`. That's another O(amount) array.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Greedy is the obvious first idea and it's wrong — with coins `[1,3,4]` and amount 6, taking the largest coin gives 4+1+1 = three coins, but 3+3 is two. Real currencies are designed so greedy works, but arbitrary denominations aren't. So: to make `amount`, the last coin was one of the coins, and before it I'd made `amount - coin` optimally. That gives `dp[i] = min over coins of dp[i - coin] + 1`. I build bottom-up from 0 so every smaller amount is final when I need it. Since supply is infinite and order doesn't matter, the only state is how much is left, which keeps it one-dimensional. I use infinity for unreachable amounts because `inf + 1` is still `inf`, so unreachability propagates for free, and I convert it to −1 at the end. O(amount × coins) time, O(amount) space. Bottom-up rather than memoized recursion specifically because with `coins = [1]` and amount 10⁴ the recursion would be 10,000 deep."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why doesn't greedy work?" | `coins = [1,3,4]`, `amount = 6`. Greedy takes the 4 and needs three coins; the optimum is 3+3. Greedy is only safe on *canonical* systems, and you can't assume arbitrary denominations are canonical. |
| "Count the number of *ways* instead of the fewest coins." | [Coin Change II](518-coin-change-ii.md). Swap `min` for `+`, and — critically — put the coin loop **outside** the amount loop, so each combination is counted once regardless of order. |
| "Which coins did you use?" | Store the winning coin at each amount in a parallel array, then walk back from `amount`, subtracting each recorded coin. O(amount) extra space. |
| "Solve it with BFS." | Amounts are nodes, coins are weight-1 edges. BFS from 0; the level at which you first reach `amount` is the answer. Same complexity, but it can exit early. |
| "What if each coin could be used only once?" | That's 0/1 knapsack. Iterate amounts **downwards** in the inner loop so each coin is consumed at most once per item. |
| "Can you get O(1) space?" | No. `dp[i]` depends on `dp[i - coin]` for every coin, and coins can be nearly as large as the amount — the lookback window isn't bounded by a constant. |
| "Why `inf` rather than −1 as the sentinel?" | `inf` compares correctly in `min` and survives `+1`, so unreachability propagates automatically. With −1 you'd need explicit checks everywhere. |
| "Is this really polynomial?" | It's *pseudo*-polynomial — linear in the value of `amount`, which is exponential in the number of bits needed to write it. Standard for knapsack-family problems. |

**Traps:**
- **Reaching for greedy.** The most common wrong answer, and it passes many test cases before failing.
- **Omitting the `coin <= i` guard.** Python's negative indexing makes `dp[i - coin]` read from the end of the array instead of raising — a silently wrong answer.
- Using `0` or `-1` as the "unreachable" sentinel. Both break `min` and break `+1` propagation.
- Forgetting `dp[0] = 0`. Nothing can ever be built, and every answer is −1.
- Sizing the array `amount` instead of `amount + 1` — an `IndexError` at the very last step.
- Returning `dp[amount]` without converting `inf` to −1.
- Confusing this with [Coin Change II](518-coin-change-ii.md) and swapping the loop order. Here the order doesn't matter (you're taking a min); there it's the whole problem.

**This same move shows up in:** [Coin Change II](518-coin-change-ii.md) (the same array, counting combinations instead of minimizing — and loop order suddenly matters) · [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) (the same `min`-over-branches shape with a fixed two-cell window) · [Word Break](139-word-break.md) (an unbounded-knapsack shape over a string, asking whether *any* split works) · [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (the 0/1 variant, where each item is used at most once).

</details>

---
