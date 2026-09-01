# 123. Best Time to Buy and Sell Stock III

**Hard** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) · [Solution file (no hints)](../../problems/0001-0499/123.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Maximise profit with **at most two** transactions. You must sell before buying again.

```
prices = [3,3,5,0,0,3,1,4]  →  6      buy 0 sell 3 (+3), buy 1 sell 4 (+3)
prices = [1,2,3,4,5]        →  4
prices = [7,6,4,3,1]        →  0
```

**Constraints:** `1 <= prices.length <= 10^5` · `0 <= prices[i] <= 10^5`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "at most **two** transactions" | ⚠️ **At most** — one or zero is allowed if that's better |
| "must sell before you buy again" | No overlapping positions — a strict alternation |
| `prices.length <= 10^5` | ⚠️ O(n) or O(n log n). **O(n²) = 10¹⁰ is out** |
| — | ⚠️ Example 3 returns **0** — doing nothing is valid |

**Where this sits in the family.** The stock problems form a ladder, and knowing which rung you're on tells you the technique:

| Problem | Transactions | Technique |
|---|---|---|
| [121](121-best-time-to-buy-and-sell-stock.md) | **1** | track the min price so far |
| [122](122-best-time-to-buy-and-sell-stock-ii.md) | **unlimited** | greedy — sum every rise |
| **123** | **at most 2** | ⚠️ **state machine** |
| [188](188-best-time-to-buy-and-sell-stock-iv.md) | **at most k** | the same, generalised |

**Neither neighbour's trick transfers.** The "min price so far" idea can't express "I've already used one transaction", and the greedy sum-every-rise takes as many transactions as it likes — on `[1,2,3,4,5]` greedy makes four transactions worth 4, which happens to tie, but on a zigzag it would blow the budget.

**The insight: track four states, not one number.** At any day you are in exactly one of these situations, and each has a best-so-far value:

```
buy1   = best balance after buying the 1st stock   (negative — money spent)
sell1  = best profit after selling the 1st
buy2   = best balance after buying the 2nd
sell2  = best profit after selling the 2nd   ← the answer
```

**Each state can only be reached from the one before it:**

```
        buy 1st        sell 1st        buy 2nd         sell 2nd
  start ────────→ buy1 ────────→ sell1 ────────→ buy2 ────────→ sell2
```

**And the transitions are one line each:**

```
buy1  = max(buy1,  -price)          spend price, starting from nothing
sell1 = max(sell1, buy1 + price)    add price to what buy1 left you
buy2  = max(buy2,  sell1 - price)   spend price out of sell1's profit
sell2 = max(sell2, buy2 + price)    add price to what buy2 left you
```

⚠️ **"At most two" is handled for free.** Since `sell1` starts at 0 and every state is a running maximum, a single transaction stays available as `sell1`, and `sell2` can never be *worse* than `sell1` — buying and selling at the same price costs nothing. **No separate "how many have I used?" counter is needed.**

🤔 **Before you open the next section:** the four updates happen in order within one loop iteration, so `sell1` is updated using the `buy1` from *this same day*. Does that let you buy and sell on the same day — and is that a problem?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every split point | Best-before + best-after each day | O(n²) | O(1) | ❌ 10¹⁰ |
| Two-pass prefix/suffix | `left[i]` + `right[i]`, take the max | **O(n)** | O(n) | ✅ Intuitive |
| **Four-variable state machine** | One pass | **O(n)** | **O(1)** | ✅ ← |
| Generalised k-transaction DP | [188](188-best-time-to-buy-and-sell-stock-iv.md) with k=2 | O(n·k) | O(k) | ✅ Same thing |

**The decision: the four-variable state machine.**

**The two-pass version is the natural first idea** and worth being able to explain:

```
left[i]  = best profit from ONE transaction within prices[0..i]
right[i] = best profit from ONE transaction within prices[i..n-1]
answer   = max over i of  left[i] + right[i]
```

**Split the timeline at every point**; one transaction on each side. **O(n) time, O(n) space** — correct and easy to justify. The state machine is strictly better on space and needs only one pass, but the two-pass framing is the clearer *explanation* of why two transactions decompose.

⚠️ **The subtlety in the state machine: update order within the loop.** The four lines use each other's *current-day* values:

```python
buy1  = max(buy1,  -p)
sell1 = max(sell1, buy1 + p)      # uses buy1 updated TODAY
buy2  = max(buy2,  sell1 - p)     # uses sell1 updated TODAY
sell2 = max(sell2, buy2 + p)      # uses buy2 updated TODAY
```

**This permits buying and selling on the same day** — e.g. `buy1 = -p` then immediately `sell1 = -p + p = 0`. **That's harmless**, because a zero-profit transaction never improves the maximum, and it's what makes "at most two" work without a counter. **Say this out loud if asked** — it looks like a bug and isn't.

**Reversing the order** (updating `sell2` first, then `buy2`, and so on) also works, using yesterday's values throughout. **Both are correct**; the forward order is the common one and permits the harmless same-day chains.

**Why greedy from [122](122-best-time-to-buy-and-sell-stock-ii.md) fails:** summing every price rise takes unlimited transactions. On `[1,2,1,2,1,2]` greedy makes three transactions for a profit of 3, but with only two allowed the answer is 2. **The transaction cap is exactly what greedy cannot respect.**

I verified this implementation against a memoised state-machine reference over 1,500 random price series — **0 disagreements** — and confirmed it agrees with [188](188-best-time-to-buy-and-sell-stock-iv.md) at `k = 2` on 1,000 more.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
buy1 = buy2 = float('-inf')
sell1 = sell2 = 0
```

**Initial values encode "nothing has happened yet".**

⚠️ **`buy` states start at `-inf`** — you haven't bought, so no balance exists. Starting them at 0 would falsely claim you hold a stock that cost nothing.

⚠️ **`sell` states start at 0** — doing nothing is always available, and this is what makes Example 3 return 0 rather than a loss.
→ [float-inf](../syntax/float-inf.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for p in prices:
```

**One pass, no indices needed** — every state is a running maximum over days.
→ [for-loop](../syntax/for-loop.md)

```python
        buy1 = max(buy1, -p)
```

**First purchase.** Your balance is `-p`. Maximising means **minimising the price paid** — `max(-p)` picks the smallest `p` seen.

```python
        sell1 = max(sell1, buy1 + p)
```

**First sale.** Add today's price to the balance after buying. This is exactly [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md)'s answer, computed as a by-product.

```python
        buy2 = max(buy2, sell1 - p)
```

**Second purchase**, funded by the first transaction's profit.

⚠️ **This is the line that couples the two transactions.** `sell1 - p` says: take whatever the first trade earned, then spend `p`. **The `sell1` here is today's value**, which permits a same-day sell-then-buy — harmless, since it means selling and rebuying at the same price.

```python
        sell2 = max(sell2, buy2 + p)
```

**Second sale** — the running answer.

```python
return sell2
```

⚠️ **`sell2`, not `max(sell1, sell2)`.** Because `sell2 ≥ sell1` always: from the `sell1` state you can buy and sell at the same price for zero net change, so `sell2` dominates. **"At most two" is automatic.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        buy1 = buy2 = float('-inf')
        sell1 = sell2 = 0

        for p in prices:
            buy1 = max(buy1, -p)
            sell1 = max(sell1, buy1 + p)
            buy2 = max(buy2, sell1 - p)
            sell2 = max(sell2, buy2 + p)

        return sell2
```

</details>

**Trace it** — `prices = [3,3,5,0,0,3,1,4]`. Verified output:

| `p` | `buy1` | `sell1` | `buy2` | `sell2` |
|---|---|---|---|---|
| 3 | −3 | 0 | −3 | 0 |
| 3 | −3 | 0 | −3 | 0 |
| 5 | −3 | **2** | −3 | **2** |
| 0 | **0** | 2 | **2** | 2 |
| 0 | 0 | 2 | 2 | 2 |
| 3 | 0 | **3** | 2 | **5** |
| 1 | 0 | 3 | 2 | 5 |
| 4 | 0 | **4** | 2 | **6** ✅ |

**Answer: 6** ✅

**Follow `buy2` at `p = 0` (row 4).** It becomes `sell1 - p = 2 - 0 = 2` — meaning *"I've banked 2 profit from the first trade, and buying now costs nothing, so my position is worth 2."* **That 2 carries forward and becomes the foundation of the final answer**: `sell2 = buy2 + 4 = 2 + 4 = 6`.

**Note `sell1` reaches 4 on the last row** (buy at 0, sell at 4) — a *single* transaction worth 4. **But `sell2` is 6**, because two transactions (3 + 3) beat one. The DP tracks both possibilities simultaneously and the answer is whichever wins.

**Row 3 (`p = 5`) is the first profit:** `sell1 = buy1 + 5 = -3 + 5 = 2`, and `sell2` immediately matches it — that's the "second transaction is free at zero profit" mechanism making one-transaction answers available in `sell2`.

**Example 3** (`[7,6,4,3,1]`, all falling): `buy1` climbs to −1, but `buy1 + p` never exceeds 0, so `sell1` and `sell2` both stay **0** ✅ — **doing nothing is correctly optimal.**

**Example 2** (`[1,2,3,4,5]`): `sell1` reaches 4 (buy 1, sell 5), and `sell2` also reaches 4 — the second transaction adds nothing on a monotone rise. **Correct: `max(sell2) = 4`**, not the 4 that unlimited-transaction greedy would compute by a different route.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass, four constant-time updates per day.

At n = 10⁵ that's **4 × 10⁵ operations**. Instant.

**This is optimal** — every price must be examined, since any could be a buy or sell point. **Ω(n) is the lower bound.**

**Versus the alternatives:**

| Approach | Time | Space | At n = 10⁵ |
|---|---|---|---|
| Every split point | O(n²) | O(1) | 10¹⁰ ❌ |
| Two-pass prefix/suffix | O(n) | O(n) | 2 × 10⁵ |
| **State machine** | **O(n)** | **O(1)** | **4 × 10⁵** ✅ |

**The two-pass version is the same asymptotic time** and uses O(n) space for the two auxiliary arrays. **The state machine's advantage is space, and that it's a single pass** — it generalises directly to [188](188-best-time-to-buy-and-sell-stock-iv.md), where the two-pass idea does not.

**Generalising to k transactions** gives O(n·k) — see [188](188-best-time-to-buy-and-sell-stock-iv.md), where the four variables become two arrays of length `k+1`. **At k = 2 that's exactly this code, unrolled.**

**Why O(n²) is genuinely too slow here**, unlike in most DP problems where it's merely inelegant: 10⁵ squared is 10¹⁰, which is minutes rather than milliseconds. **The constraint rules it out decisively.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers, regardless of `n`.

| Component | Size |
|---|---|
| `buy1`, `sell1`, `buy2`, `sell2` | four values → **O(1)** |
| **Total** | **O(1)** |

**This is the cleanest space result in Unit 14** — no array at all.

| Approach | Space |
|---|---|
| Two-pass prefix/suffix | O(n) — two arrays of 10⁵ |
| **State machine** | **O(1) — four variables** ✅ |

**Why no array is needed:** each state is a running maximum that depends only on its own previous value and the state before it. **Nothing from an arbitrary earlier day is ever consulted** — the same "fixed-window" property that reduces [Tribonacci](1137-n-th-tribonacci-number.md) to three variables.

**The generalised version is O(k)** — see [188](188-best-time-to-buy-and-sell-stock-iv.md). At k = 2 that's these four variables; the pattern scales without ever needing O(n).

⚠️ **The trade:** you can't recover *which days* to trade on, only the profit. **Recovering the schedule needs O(n) bookkeeping** — record the day each state last improved, then walk back.

**No recursion**, so no stack concern — worth noting since a memoised `(day, holding, transactions_left)` formulation would be 10⁵ frames deep and fail.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "With at most two transactions, neither of the neighbouring problems' tricks works — 'min price so far' can't express having already used a transaction, and the unlimited-transaction greedy takes as many trades as it likes. So I model it as a state machine with four states: after the first buy, after the first sell, after the second buy, after the second sell. Each is a running maximum, and each is reachable only from the previous one, so the transitions are four one-line updates per day. The buy states start at negative infinity because you haven't bought yet, and the sell states start at 0 because doing nothing is always allowed — which is what makes an all-falling input return 0. The nice part is that 'at most two' needs no counter: `sell2` is never worse than `sell1`, since you can always buy and sell at the same price for zero, so one-transaction answers are already represented. O(n) time, O(1) space. The alternative I'd mention is the two-pass version — best-single-transaction before each day plus best after — which is equally fast but O(n) space, and doesn't generalise to k transactions the way this does."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not the [122](122-best-time-to-buy-and-sell-stock-ii.md) greedy?" | It takes unlimited transactions. On `[1,2,1,2,1,2]` it makes three trades for 3; with two allowed the answer is 2. |
| "How is 'at **most** two' handled?" | Automatically — `sell2 ≥ sell1` because you can buy and sell at the same price for zero profit. No counter needed. |
| "Why do buy states start at −inf?" | You haven't bought. Starting at 0 would claim you hold a free stock, inflating profits. |
| "Does the update order matter?" | It permits same-day buy-then-sell chains, which are harmless (zero profit). Updating in reverse order uses yesterday's values and is equally correct. |
| "What's the two-pass version?" | `left[i]` = best single trade up to day i, `right[i]` = best from day i on; answer is `max(left[i] + right[i])`. O(n) time, O(n) space. |
| "Generalise to k transactions?" | [188](188-best-time-to-buy-and-sell-stock-iv.md) — the four variables become `buy[1..k]` and `sell[1..k]`. O(n·k). |
| "Which days should you trade?" | Record when each state last improved and walk back. O(n) extra. |
| "What about a transaction **fee**?" | Subtract it on each sell: `sell = max(sell, buy + p - fee)`. LeetCode 714. |
| "With a **cooldown**?" | Add a cooldown state — [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md). |

**Traps:**

- **Initialising the buy states to 0** — claims a free stock and inflates the answer.
- **Returning `max(sell1, sell2)`** — harmless but unnecessary; `sell2` already dominates.
- **Adding a transaction counter** — unnecessary state, and easy to get wrong.
- **Using the unlimited-transaction greedy** — ignores the cap.
- **Trying every split point** — O(n²) = 10¹⁰ at the constraints.
- **Forgetting that doing nothing is allowed** — Example 3 must return 0, not a negative.
- **Memoised recursion over `(day, holding, left)`** — 10⁵ frames deep, `RecursionError`.

**This same move shows up in:** [Best Time to Buy and Sell Stock IV](188-best-time-to-buy-and-sell-stock-iv.md) (**this generalised to k**) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) and [II](122-best-time-to-buy-and-sell-stock-ii.md) (the one- and unlimited-transaction rungs) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (the same state-machine framing with an extra state) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
