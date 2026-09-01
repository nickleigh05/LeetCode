# 122. Best Time to Buy and Sell Stock II

**Medium** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) · [Solution file (no hints)](../../problems/0001-0499/122.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

You may buy and sell **as often as you like** (holding at most one share at a time). Return the maximum profit.

```
prices = [7,1,5,3,6,4]  →  7      buy 1 sell 5 (+4), buy 3 sell 6 (+3)
prices = [1,2,3,4,5]    →  4      buy 1 sell 5
prices = [7,6,4,3,1]    →  0      never buy
```

**Constraints:** `1 <= prices.length <= 3·10^4` · `0 <= prices[i] <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "buy and/or sell **on each day**" | ⚠️ **Unlimited** transactions — no cap to reason about |
| "hold **at most one** share at any time" | Must sell before buying again |
| "sell and buy on the **same day**" | Positions can be closed and reopened instantly |
| "**maximum** profit" | Optimisation — but with no cap, it collapses |
| Example 3 returns **0** | Doing nothing is allowed |

**The unlimited cap is what makes this easy — and it's the *whole* difference from its neighbours.** Compare:

| Problem | Transactions | Technique |
|---|---|---|
| [121](121-best-time-to-buy-and-sell-stock.md) | 1 | track the minimum price so far |
| **122** | **unlimited** | ⚠️ **sum every rise — greedy** |
| [123](123-best-time-to-buy-and-sell-stock-iii.md) | at most 2 | four-state machine |
| [188](188-best-time-to-buy-and-sell-stock-iv.md) | at most k | 2k-state machine |

**With no cap, there is no trade-off to optimise.** Any profitable move can be taken, so take all of them.

**The key identity — a long hold telescopes into daily steps:**

```
buy on day 1 at 1, sell on day 5 at 5    →  profit 5 − 1 = 4

is exactly equal to

(2−1) + (3−2) + (4−3) + (5−4)  =  4      buying and selling every single day
```

**Because same-day sell-then-buy is free**, holding through a rise and trading every day give **identical profit**. So instead of deciding *when* to hold, just:

> **Sum every positive day-to-day difference.**

```
prices = [7,1,5,3,6,4]

diffs:  −6, +4, −2, +3, −2
keep the positives:  4 + 3 = 7 ✅
```

⚠️ **And you skip the negatives**, which is what makes it optimal — a falling day is simply one you're not holding through.

**Why this is provably optimal, not just plausible.** Any strategy's profit is a sum of `sell − buy` over disjoint intervals, and each interval telescopes into its daily differences. **The best possible sum of daily differences is obtained by taking exactly the positive ones** — you can't do better than including every gain and excluding every loss.

🤔 **Before you open the next section:** the greedy "buys" and "sells" on nearly every day. Does the answer change if you're told transactions have a fee?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every buy/sell schedule | Brute force | O(2ⁿ) | — | ❌ |
| Peak-valley scanning | Find each local min, then the next local max | O(n) | O(1) | ✅ Correct, more code |
| **Sum positive differences** | One pass | **O(n)** | **O(1)** | ✅ ← |
| DP state machine | `hold` / `free` states | O(n) | O(1) | ✅ Generalises better |

**The decision: sum every positive day-to-day difference.** It's three lines and provably optimal.

**The peak-valley version** is the same idea expressed literally — walk down to a local minimum, buy, walk up to a local maximum, sell, repeat. **Identical answer, more bookkeeping**, and it obscures the telescoping insight. **Mention it as the "what you're actually doing" framing.**

**The DP state machine is worth knowing** because it's the one that survives added constraints:

```python
hold, free = float('-inf'), 0
for p in prices:
    hold, free = max(hold, free - p), max(free, hold + p)
return free
```

**Two states: holding a share, or not.** ⚠️ **Same O(n)/O(1), and it's the version to reach for the moment a fee or cooldown appears** — the greedy identity breaks then, while this only needs an extra term. **That's the real reason to know it.**

**Why the [121](121-best-time-to-buy-and-sell-stock.md) trick doesn't transfer.** There you track the minimum price seen and the best single `price − min`. Here that would find only the *largest single* rise:

```
prices = [7,1,5,3,6,4]
121's answer: 5      (buy 1, sell 6)
122's answer: 7      (buy 1 sell 5, buy 3 sell 6) ✅
```

**Splitting into two trades beats one big one**, because the dip at 3 lets you re-enter lower. **The unlimited cap is exactly what makes splitting free.**

**And why the greedy fails for [123](123-best-time-to-buy-and-sell-stock-iii.md)/[188](188-best-time-to-buy-and-sell-stock-iv.md):** summing every rise takes as many transactions as there are rises. With a cap of 2:

```
prices = [1,2,1,2,1,2]
greedy (unlimited): 1 + 1 + 1 = 3     three transactions
at most 2:                       2     ⚠️ the cap binds
```

**Knowing which rung of the ladder you're on decides the technique** — that's the transferable lesson.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
max_profit = 0
```

**Start at zero** — ⚠️ doing nothing is always allowed, which is what makes Example 3 return 0 rather than a loss.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(1, len(prices)):
```

**Compare each day to the one before**, so start at index 1.

⚠️ With a single-element list this loop never runs and the function returns 0 — **correct, and no special case needed.**
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    if prices[i] > prices[i - 1]:
        max_profit += prices[i] - prices[i - 1]
```

**Capture every rise; ignore every fall.**

**Each `+=` is conceptually "buy yesterday, sell today"** — and because same-day trading is free, consecutive rises merge into one long hold with the same total. **You never need to decide where a hold begins or ends.**

The `if` is what discards losses. An equivalent one-liner:

```python
return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
```
→ [comparison-operators](../syntax/comparison-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return max_profit
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0

        for i in range(1, len(prices)):

            if prices[i] > prices[i - 1]:
                max_profit += prices[i] - prices[i - 1]

        return max_profit
```

</details>

<details>
<summary>The DP state-machine version, for comparison</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold, free = float('-inf'), 0
        for p in prices:
            hold, free = max(hold, free - p), max(free, hold + p)
        return free
```

**Same O(n) and O(1)**, but it extends directly to transaction fees (LeetCode 714) and cooldowns ([309](309-best-time-to-buy-and-sell-stock-with-cooldown.md)), where the greedy identity no longer holds.
→ [float-inf](../syntax/float-inf.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)

</details>

**Trace it** — `prices = [7,1,5,3,6,4]`:

| `i` | `prices[i-1]` → `prices[i]` | Difference | Action | `max_profit` |
|---|---|---|---|---|
| 1 | 7 → 1 | **−6** | fall, skip | 0 |
| 2 | 1 → 5 | **+4** | ✅ take | **4** |
| 3 | 5 → 3 | **−2** | fall, skip | 4 |
| 4 | 3 → 6 | **+3** | ✅ take | **7** |
| 5 | 6 → 4 | **−2** | fall, skip | 7 |

**Answer: 7** ✅ — matching the problem's stated trades (buy 1 sell 5, buy 3 sell 6).

**Note the greedy never explicitly "chose" those trades.** It just added `+4` and `+3`. **The rows it skipped are the days you weren't holding**, which is where the optimality comes from.

**Example 2** (`[1,2,3,4,5]`) shows the telescoping most clearly:

| `i` | Difference | `max_profit` |
|---|---|---|
| 1 | +1 | 1 |
| 2 | +1 | 2 |
| 3 | +1 | 3 |
| 4 | +1 | **4** ✅ |

**Four separate "trades" totalling 4** — identical to the single trade "buy at 1, sell at 5" that the problem describes. ⚠️ **The problem explicitly warns you can't hold two shares at once**, but that's irrelevant here: these trades are sequential, not simultaneous.

**Example 3** (`[7,6,4,3,1]`) has every difference negative, so nothing is ever added → **0** ✅ — **not a negative number**, because you simply never buy.

**A single-day input** `[5]`: `range(1, 1)` is empty, the loop never runs, and the answer is **0** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass, a comparison and an addition per day.

At n = 3 × 10⁴ that's **30,000 operations**. Instant.

**This is optimal**: every price must be examined, since any could be part of a profitable move. **Ω(n) is the lower bound**, and one pass matches it.

**No sorting, no data structures, no second pass.** The greedy needs nothing beyond adjacent comparisons — **which is unusual and worth noting**, since most optimisation problems need at least a DP table.

**Versus the alternatives:**

| Approach | Time | Space |
|---|---|---|
| Brute force over schedules | O(2ⁿ) | — |
| Peak-valley scan | O(n) | O(1) |
| **Sum positive differences** | **O(n)** | **O(1)** ✅ |
| DP state machine | O(n) | O(1) |

**All the sensible ones are O(n)** — the choice is about clarity, and about which generalises.

⚠️ **The contrast with [123](123-best-time-to-buy-and-sell-stock-iii.md) and [188](188-best-time-to-buy-and-sell-stock-iv.md) is the point.** Those are O(n) and O(n·k) respectively because a transaction *cap* forces you to track how many you've used. **Removing the cap removes the state entirely** — that's why this is the easiest rung despite looking like the most permissive.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a single accumulator.

| Component | Size |
|---|---|
| `max_profit` | one integer → **O(1)** |
| **Total** | **O(1)** |

**No array, no DP table, no auxiliary structure.** The input is read once and never modified.

| Approach | Space |
|---|---|
| **Sum positive differences** | **O(1)** ✅ |
| DP state machine | O(1) — two variables |
| Peak-valley scan | O(1) |
| [188](188-best-time-to-buy-and-sell-stock-iv.md) generalisation at large k | O(k) |

**Every reasonable approach here is O(1)** — which is itself informative: **with no transaction cap there is no state to carry**, so nothing needs storing.

⚠️ **The trade:** you can't report *which* days to trade on. **Recovering the schedule needs O(n)** — record the start of each rising run and its end.

**The input is not mutated**, unlike several other greedy problems in this unit that sort in place. **Nothing to caveat about the caller's data.**

**No recursion.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because transactions are unlimited, there's no trade-off to optimise — any profitable move can be taken, so take all of them. The key identity is that a long hold telescopes into daily steps: buying at 1 and selling at 5 gives exactly the same profit as buying and selling every day in between, since same-day sell-then-buy is free. So the answer is just the sum of every positive day-to-day difference, skipping the falls. That's provably optimal because any strategy's profit decomposes into daily differences, and the best sum takes every gain and no loss. O(n) time, O(1) space, one pass. Worth noting where this sits: with one transaction you'd track the minimum price so far, and with a cap of two or k you need a state machine, because the cap forces you to track how many you've used. Removing the cap removes the state entirely — which is why the most permissive version is the easiest. If a transaction fee were added the greedy would break, and I'd switch to the two-state DP."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is summing every rise optimal?" | **The question.** Any strategy's profit telescopes into daily differences; the best sum includes every gain and excludes every loss. |
| "Doesn't that make far too many transactions?" | It's fine — unlimited is allowed, and consecutive rises merge into one hold with identical profit. |
| "Why doesn't [121](121-best-time-to-buy-and-sell-stock.md)'s approach work?" | It finds only the largest single rise. On `[7,1,5,3,6,4]` that's 5; splitting into two trades gives 7. |
| "Why does this greedy fail for [123](123-best-time-to-buy-and-sell-stock-iii.md)?" | It takes as many transactions as there are rises. On `[1,2,1,2,1,2]` it makes 3 for a profit of 3; capped at 2 the answer is 2. |
| "Add a **transaction fee**?" | ⚠️ The greedy breaks — small rises stop being worth taking. Use the two-state DP: `free = max(free, hold + p − fee)`. LeetCode 714. |
| "Add a **cooldown**?" | Add a third state — [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md). |
| "Which days should you trade?" | Record the start and end of each rising run. O(n) extra. |
| "What if you could hold multiple shares?" | Different problem — you'd buy at every local minimum in quantity, and the answer becomes unbounded without a budget. |
| "Same-day buy and sell?" | Explicitly allowed, and it's what makes the telescoping identity exact. |

**Traps:**

- **Using the [121](121-best-time-to-buy-and-sell-stock.md) min-price approach** — finds one trade, not many. Gives 5 instead of 7 on Example 1.
- **Applying this greedy to [123](123-best-time-to-buy-and-sell-stock-iii.md)/[188](188-best-time-to-buy-and-sell-stock-iv.md)** — ignores the transaction cap.
- **Starting `max_profit` below 0** — Example 3 must return 0, not a loss.
- **Starting the loop at `i = 0`** — `prices[-1]` reads the last element silently.
- **Over-thinking "at most one share"** — the trades are sequential, so it's never violated.
- **Tracking explicit buy/sell days** — unnecessary; the sum of differences is the whole answer.
- **Assuming a fee changes nothing** — it breaks the greedy entirely.

**This same move shows up in:** [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (one transaction) · [Best Time to Buy and Sell Stock III](123-best-time-to-buy-and-sell-stock-iii.md) and [IV](188-best-time-to-buy-and-sell-stock-iv.md) (capped — where this greedy fails, and which fall back to *this* when k is large) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (the state-machine extension) · [Maximum Subarray](53-maximum-subarray.md) (another one-pass greedy over adjacent differences).

</details>

---
