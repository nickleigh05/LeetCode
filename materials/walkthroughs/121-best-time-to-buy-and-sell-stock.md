# 121. Best Time to Buy and Sell Stock

**Easy** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · [Solution file (no hints)](../../problems/0001-0499/121.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

You're given an array `prices` where `prices[i]` is the price of a stock on day `i`.

You want to maximize profit by choosing **one day to buy** and a **different, later day to sell**. Return the maximum profit — or `0` if no profit is possible.

```
prices = [7,1,5,3,6,4]  →  5     (buy day 1 at 1, sell day 4 at 6)
prices = [7,6,4,3,1]    →  0     (only losses — don't trade)
```

**Constraints:** `1 <= prices.length <= 10⁵` · `0 <= prices[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "buy … and a **different, later** day to sell" | Order is enforced: **buy index < sell index**. You can't sell before you buy — that's what makes this directional rather than just max−min |
| "**one** buy, **one** sell" | A single transaction. No re-buying, no stacking gains |
| "**maximum** profit" | An optimization over all valid `(buy, sell)` pairs — n²/2 of them |
| "**0** if no profit" | Not trading is allowed. Never return a negative |
| n up to 10⁵ | O(n²) = 10¹⁰ → dead. Target **O(n)** |

The trap worth naming: this is **not** `max(prices) − min(prices)`. On `[7,1,5,3,6,4]` that would be right by luck, but on `[5,1]`… actually let's use a clearer one: `[3,10,1,2]`. Max−min gives `10 − 1 = 9`, but the 10 comes *before* the 1 — you can't sell before buying. The real answer is `7`.

So the reframe: walk forward, and at each day ask **"if I sold today, what's the best I could have done?"** That's today's price minus the *cheapest price seen so far*. Take the best of those over all days.

And notice what that means — **the only thing you need to remember about the entire past is one number**: the minimum so far.

🤔 **Before you open the next section:** if you're standing on day `i` and want the best profit from selling today, what exactly do you need to know about days `0..i-1`? How much of that history must you actually store?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(buy, sell)` pair with `buy < sell` | O(n²) | O(1) | ❌ 10¹⁰ ops |
| `max − min` | Take the range of the array | O(n) | O(1) | ❌ **Wrong** — ignores the ordering constraint |
| Precompute max-to-the-right | For each day, the best future price | O(n) | **O(n)** | ⚠️ Correct, but stores an array it doesn't need |
| **Sliding window / running min** | One pass, carry the cheapest so far | **O(n)** | **O(1)** | ✅ |

**The decision: one forward pass carrying the minimum price seen so far.**

Two pointers moving in the **same direction** — `left` marks the buy day (the cheapest so far), `right` scans forward as the sell day. That's the shape of a **sliding window**, and it's the difference from Unit 02: there the pointers *converged*, here they both travel left to right.

The rule at each step:

- If today's price is **lower** than the buy price, this is a better day to buy → move `left` here. (Any future sale profits more from a cheaper buy.)
- Otherwise, today is a candidate sell day → record `prices[right] - prices[left]`.

**Why it's safe to abandon the old buy day.** When you find a cheaper price, every future sell day would rather have bought *here* than at the old, higher price — the profit is strictly larger for the same sell. The old buy day can never be part of a better answer, so discard it. That's the same **discard argument** as [Container With Most Water](11-container-with-most-water.md), just travelling one direction.

**Why not precompute the max-to-the-right array?** It's a perfectly correct O(n) — for each day, look up the best future price. But it needs an n-element array to hold what a single running variable can carry if you walk the other way. Same collapse as [Product of Array Except Self](238-product-of-array-except-self.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left, right = 0, 1
max_profit = 0
```

`left` is the **buy** day, `right` the **sell** day. `right` starts at 1 because selling requires a strictly later day — starting both at 0 would allow a same-day trade.

`max_profit = 0` encodes "don't trade" as the fallback, which is exactly what the problem asks for when every price only falls.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while right < len(prices):
```

Scan every remaining day as a potential sell day. Unlike Unit 02, **only `right` advances the loop** — `left` jumps opportunistically. Both move forward, never backward.
→ [while-loop](../syntax/while-loop.md)

```python
    if prices[right] < prices[left]:
        left = right
```

Found a cheaper buy. Jump `left` straight to `right` — not `left += 1`. There's no reason to step: every day between the old buy and here is more expensive than `prices[right]`, so none of them could be a better buy day either.

Note this is a *reset*, and it's why the window never needs to look backward.
→ [comparison-operators](../syntax/comparison-operators.md) · [list-basics](../syntax/list-basics.md)

```python
    else:
        max_profit = max(max_profit, prices[right] - prices[left])
```

Today's price is at or above the buy price, so selling today is a legitimate (possibly zero-profit) trade. Record it if it beats the best so far.

Because this is the `else`, the subtraction can never be negative — we only reach it when `prices[right] >= prices[left]`.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    right += 1
```

Advance the sell day. This runs on **both** branches — the window always moves forward, which is what guarantees termination.

```python
return max_profit
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        left, right = 0, 1
        max_profit = 0

        while right < len(prices):
            if prices[right] < prices[left]:
                left = right
            else:
                max_profit = max(max_profit, prices[right] - prices[left])
            right += 1

        return max_profit
```

</details>

**Trace it** — `prices = [7,1,5,3,6,4]`:

| `right` | `prices[right]` | vs buy `prices[left]` | Action | `left` | `max_profit` |
|---|---|---|---|---|---|
| 1 | 1 | 1 < 7 | cheaper buy → jump | 1 | 0 |
| 2 | 5 | 5 ≥ 1 | profit 4 | 1 | **4** |
| 3 | 3 | 3 ≥ 1 | profit 2 | 1 | 4 |
| 4 | 6 | 6 ≥ 1 | profit **5** | 1 | **5** |
| 5 | 4 | 4 ≥ 1 | profit 3 | 1 | 5 |

Answer: **5**.

And the all-losses case, `prices = [7,6,4,3,1]`: every day is cheaper than the last, so `left` jumps every iteration, the `else` never runs, and `max_profit` stays **0** ✅

**The same algorithm, stated as a running minimum** — many people find this phrasing clearer:

```python
min_price = prices[0]
for price in prices[1:]:
    max_profit = max(max_profit, price - min_price)
    min_price = min(min_price, price)
```
→ [list-slicing](../syntax/list-slicing.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

`right` advances by exactly 1 every iteration and never resets, so the loop runs n−1 times with O(1) work each. `left` only ever jumps *forward*, so it contributes no extra work — it's not a nested loop, it's a reassignment.

**O(n)** total, one pass.

**Versus the brute force:** O(n²) → O(n). The repeated work eliminated is *re-scanning the past for the cheapest price*. The running minimum carries that answer forward instead of recomputing it — the same principle as [prefix sums](../learning/01b-prefix-sums.md) and [Trapping Rain Water](42-trapping-rain-water.md)'s running maxima.

No early exit — the best profit could be on the last day, so all n steps always run.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers: `left`, `right`, `max_profit`.

**Where the O(n) alternative went.** The "precompute the best future price for each day" solution needs an n-element array. This version doesn't, because of a directional trick worth internalizing:

> Scanning **forward**, the best *buy* price is a running minimum — knowable from the past alone.
> Scanning **backward**, the best *sell* price would be a running maximum — knowable from the future alone.

Either direction collapses one of the two arrays into a single variable. You only need an array if you insist on having *both* halves available at every index simultaneously — and here you don't, because you can just fix one end as you go.

That's the same collapse as [Product of Array Except Self](238-product-of-array-except-self.md): *"do I need this whole array, or just its running value?"*

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Checking every buy-sell pair is O(n²). The key constraint is that the buy has to come before the sell, so this isn't just max minus min — on `[3,10,1,2]` that'd wrongly give 9. Instead I'll walk forward once and, at each day, ask what I'd make selling today: today's price minus the cheapest price I've seen so far. If today is cheaper than my current buy price, I move the buy there, because every future sale would profit more from the cheaper entry. So I only ever need to remember one number about the past. O(n) time, O(1) space, and it naturally returns 0 when prices only fall."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Unlimited** transactions?" | Take every upward step: sum `max(0, prices[i] - prices[i-1])`. Greedy, O(n). That's LeetCode 122. |
| "At most **two** transactions?" | Now it's DP — track best-after-first-buy/sell/second-buy/sell. LeetCode 123. |
| "At most **k** transactions?" | Generalized DP over k states, O(nk). LeetCode 188. |
| "With a **cooldown** after selling?" | State-machine DP: holding / sold / resting. See [Best Time with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md). |
| "Return the buy and sell **days**." | Store the indices whenever you update `max_profit`. |
| "What if it's a **stream**?" | Works unchanged — this is an online algorithm. It only ever looks at the current price and one remembered minimum. |
| "Is this really a sliding window?" | Both pointers move forward and the window is `[buy, sell]`, so yes in shape — though it's just as fair to call it a running-minimum scan. Don't get religious about the label. |

**Traps:**

- **`max(prices) - min(prices)`.** The defining mistake — it ignores that the buy must precede the sell.
- **`left += 1` instead of `left = right`.** Slow and wrong-headed; every day in between is more expensive, so stepping wastes iterations.
- **Initializing `max_profit` to `float('-inf')`** — then a losing market returns a negative instead of 0.
- **Starting `right = 0`** — permits a same-day buy and sell.
- **Updating the minimum before computing the profit** in the running-min variant — you'd allow selling on the same day you bought.
- **Reaching for DP.** Overkill for a single transaction; save it for the k-transaction variants.

**This same move shows up in:** [Maximum Subarray](53-maximum-subarray.md) (a running "best so far" in one forward pass — Kadane's algorithm is structurally the twin of this) · [Trapping Rain Water](42-trapping-rain-water.md) (running extremes replacing precomputed arrays) · [Product of Array Except Self](238-product-of-array-except-self.md) (collapsing an array into a running variable) · [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (the same-direction two-pointer window, with a real shrink rule).

</details>

---
