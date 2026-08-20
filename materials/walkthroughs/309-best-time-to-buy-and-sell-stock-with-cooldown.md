# 309. Best Time to Buy and Sell Stock with Cooldown

**Medium** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an array `prices` where `prices[i]` is the stock price on day `i`. Find the **maximum profit** you can achieve. You may complete **as many transactions as you like**, with two restrictions:

- You may **not hold more than one share** at a time — you must sell before buying again.
- After you **sell**, you must **cool down for one day** — you cannot buy on the very next day.

```
prices = [1,2,3,0,2]   →  3      buy(1) sell(2) cooldown buy(0) sell(2)  →  1 + 2 = 3
prices = [1]           →  0      nothing to do
prices = [1,2,4]       →  3      buy(1) sell(4) — one transaction beats two here
```

**Constraints:** `1 <= prices.length <= 5000` · `0 <= prices[i] <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**as many transactions as you like**" | No transaction budget, so you don't need to count them. That keeps one dimension out of the state |
| "not more than one share at a time" | At any moment you are in one of two situations: **holding** or **not holding**. That's a boolean, and it's the second dimension |
| "**cooldown one day** after selling" | The consequence of an action reaches **two** days forward, not one. This is the constraint that breaks the simpler solutions |
| "maximum profit" | Optimization → `max` |
| `n <= 5000` | n² = 2.5 × 10⁷ is borderline; **O(n) is clearly intended** |

Start from what fails. Without the cooldown, [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) is a one-liner: sum every upward step, `max(0, p[i] - p[i-1])`, because you can capture every rise. With a cooldown that's wrong — selling costs you the *next* day's opportunity, so a small profit today can be worse than waiting.

So the day index alone doesn't describe your situation. Standing on day `i`, what you can do depends on **whether you're holding a share**:

- **Holding** → you can *sell* (collect `prices[i]`, then skip a day) or *do nothing*.
- **Not holding** → you can *buy* (pay `prices[i]`) or *do nothing*.

That gives the state: **`(day, holding)`** — a day index and a boolean. Two dimensions, which is what puts this problem in Unit 14 even though the second dimension has only two values.

And the transitions:

```
holding:      max( dfs(i+1, True),              ← keep holding
                   prices[i] + dfs(i+2, False) )  ← sell, then cooldown

not holding:  max( dfs(i+1, False),             ← keep waiting
                   -prices[i] + dfs(i+1, True) ) ← buy
```

The cooldown is that single `i+2`. Selling jumps **two** days forward instead of one — the skipped day is the cooldown, and it's expressed as an index jump rather than a third state.

🤔 **Before you open the next section:** why is *buying* recorded as a negative number rather than tracked separately as a cost to subtract later? What does it let you avoid storing in the state?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Sum every upward step | `Σ max(0, p[i] − p[i-1])` | O(n) | O(1) | ❌ **Wrong.** That's the no-cooldown problem. On `[1,2,4]` it gives 3 by chance; on `[1,2,3,0,2]` it gives 4, but the real answer is 3 |
| Greedy — buy every local min, sell every local max | Find dips and peaks | O(n) | O(1) | ❌ The cooldown can make a smaller number of larger transactions better. No local rule decides it |
| Brute force over all buy/sell schedules | Try every combination | **O(2ⁿ)** | O(n) | ❌ |
| **Memoized recursion on `(i, holding)`** | Top-down over the two-dimensional state | O(n) | O(n) | ✅ |
| Bottom-up with rolling variables | Three running values, updated per day | O(n) | **O(1)** | ✅ Strictly better space; worth mentioning |

**The decision:** **memoized recursion over `(day, holding)`** — the state machine written out directly.

**Why the "sum the rises" trick fails.** On `[1,2,3,0,2]` it computes `(2-1) + (3-2) + (2-0)` = 4. But capturing both the 1→2 and 2→3 rises requires selling on day 1 and buying on day 2 — which the cooldown forbids. The real answer is 3. **The greedy works only when transactions have no cost or consequence; the cooldown gives them one.**

**Why the state needs two dimensions.** The day index alone doesn't tell you what your legal moves are — you also need to know whether you're holding. Note this is *not* the same as needing a third "in cooldown" state: because a sell jumps directly to `i+2`, the cooldown day is skipped rather than represented. That's a genuine simplification, and it's worth calling out, since many write-ups use a three-state machine (hold / sold / rest). Both are correct; the two-state-plus-index-jump version has fewer moving parts.

**Why negative numbers for buying** (section 1's question). Recording a buy as `-prices[i]` means the running value is always **net profit so far** — one number that already accounts for the purchase. The alternative, remembering the purchase price so you can subtract it at sale time, would require **carrying that price in the state**, turning it into `(day, holding, buy_price)` and blowing up the state space. **Folding the cost in immediately keeps the state small**, and that's the trick worth internalizing.

**Why top-down here rather than bottom-up?** The recursion mirrors the decision structure exactly — at each day, list your options and take the max — so it reads like the problem statement. The bottom-up version is leaner (O(1) space) but requires reindexing the recurrence to run forwards, which is easy to get wrong under pressure. **Write the memoized version, then say you could roll it into O(1) space.** With n ≤ 5000, recursion depth is a real consideration though — see section 5.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
memo = {}
```
The cache, keyed by the full state `(i, holding)`. Without it the recursion branches twice per day and is O(2ⁿ); with it each state is computed once.

A [dict](../syntax/dict-basics.md) rather than a 2-D list because the key is a tuple and the state space is sparse — the `i+2` jumps mean not every index is reached from every state.
→ [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dfs(i, holding):
    if i >= len(prices):
        return 0
```
**The base case:** past the last day, no profit remains to be made.

The test is `>=`, not `==`, and that's essential — a sell on the final day recurses to `i + 2`, which lands **beyond** the array. `==` would miss it and recurse forever.
→ [function-basics](../syntax/function-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if (i, holding) in memo:
        return memo[(i, holding)]
```
The cache lookup. The key is the **complete** state — both the day and whether you hold. Keying on `i` alone would conflate two genuinely different situations and produce wrong answers rather than just slow ones.
→ [membership-operators](../syntax/membership-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
    cooldown = dfs(i + 1, holding)
```
**Do nothing today.** Move to tomorrow in the same state — still holding if you were, still empty if you weren't.

This option is always available regardless of state, which is why it's computed once before the branch. (The variable name is a little loose: this is "wait," which is legal on any day, not the forced post-sale cooldown.)
→ [recursion-basics](../syntax/recursion-basics.md)

```python
    if holding:
        sell = prices[i] + dfs(i + 2, False)   # selling forces a cooldown day
        best = max(cooldown, sell)
```
**Holding: sell or wait.**

Selling collects `prices[i]` — added, because it's income — and then recurses to **`i + 2`**. That jump is the entire cooldown rule: day `i+1` is skipped because you're forbidden from buying on it, and since you're not holding, there's nothing else you could do with it anyway.

State becomes `False`: after selling you hold nothing.
→ [min-max-key](../syntax/min-max-key.md) · [if-return](../syntax/if-return.md)

```python
    else:
        buy = -prices[i] + dfs(i + 1, True)
        best = max(cooldown, buy)
```
**Not holding: buy or wait.**

Buying costs `prices[i]`, recorded as **negative** so the running total stays a single net-profit figure — no purchase price needs to be carried in the state.

Recursion goes to `i + 1`, not `i + 2`: **there's no cooldown after buying**, only after selling. Getting this asymmetry backwards is one of the two classic bugs.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    memo[(i, holding)] = best
    return best
```
Cache and return. Every state is computed once and reused thereafter.
→ [dict-basics](../syntax/dict-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dfs(0, False)
```
Start on day 0 holding nothing. The `False` is the setup: you begin with no shares and no obligations.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        memo = {}

        def dfs(i, holding):
            if i >= len(prices):
                return 0
            if (i, holding) in memo:
                return memo[(i, holding)]

            cooldown = dfs(i + 1, holding)
            if holding:
                sell = prices[i] + dfs(i + 2, False)   # selling forces a cooldown day
                best = max(cooldown, sell)
            else:
                buy = -prices[i] + dfs(i + 1, True)
                best = max(cooldown, buy)

            memo[(i, holding)] = best
            return best

        return dfs(0, False)
```
</details>

**Trace it** — `prices = [1, 2, 3, 0, 2]`

Working from the last day backwards (which is the order the memo fills in):

| State | Options | Value |
|---|---|---|
| `(4, True)` | wait → `dfs(5,T)` = 0; **sell** → 2 + `dfs(6,F)` = 2 | **2** |
| `(4, False)` | wait → 0; buy → −2 + `dfs(5,T)` = −2 | **0** |
| `(3, True)` | wait → `(4,T)` = 2; sell → 0 + `dfs(5,F)` = 0 | **2** |
| `(3, False)` | wait → `(4,F)` = 0; **buy** → −0 + `(4,T)` = 2 | **2** |
| `(2, True)` | wait → `(3,T)` = 2; **sell** → 3 + `dfs(4,F)` = 3 + 0 = 3 | **3** |
| `(2, False)` | wait → `(3,F)` = 2; buy → −3 + `(3,T)` = −1 | **2** |
| `(1, True)` | wait → `(2,T)` = 3; **sell** → 2 + `dfs(3,F)` = 2 + 2 = **4** | **4** |
| `(1, False)` | wait → `(2,F)` = 2; buy → −2 + `(2,T)` = 1 | **2** |
| `(0, False)` | wait → `(1,F)` = 2; **buy** → −1 + `(1,T)` = −1 + 4 = **3** | **3** |

Return **3** ✅

Two rows are worth studying.

**`(1, True)`**: selling on day 1 for 2 lands at `dfs(3, False)` — skipping day 2 entirely. That's the cooldown. And it's still the better choice (4 beats 3), because day 3's price of 0 is such a good re-entry point.

**`(2, True)`**: here the sell recurses to `dfs(4, False)` = 0, so selling nets 3 and holding through nets 2. Note the cooldown consumed day 3 — the price-0 day, the best buying opportunity in the array. That's exactly the cost the naive "sum the rises" approach ignores when it claims 4.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The state space is `(day, holding)` → **n days × 2 boolean values = 2n states**.
- Thanks to the memo, each state's body runs **once**. Every later call is a dict lookup, O(1) average.
- Each body does at most two recursive calls, one addition, and one `max` — **O(1)** of its own work.
- 2n × O(1) = **O(n)**.

At n = 5000 that's ~10,000 state computations. Trivial.

**The pattern to name:** *number of states × work per state*. That's how you compute the complexity of any memoized DP, and it's a cleaner way to say it than describing the recursion tree. Here: 2n states, O(1) each.

**Against the alternatives:** unmemoized, the recursion branches twice per day and is **O(2ⁿ)**. The memo collapses it because the same `(day, holding)` pair is reached along exponentially many different trading histories — but the history doesn't matter, only the current state does. **That's the insight that makes DP work**, and it's the same reason [Longest Common Subsequence](1143-longest-common-subsequence.md) is polynomial.

**Faster?** No — every price can affect the answer, so **Ω(n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, from two sources:

- The **memo** holds up to 2n entries → O(n).
- The **recursion stack** can nest once per day → up to **n frames** → O(n).

Both are genuinely O(n), so the total is O(n).

**The recursion depth is a real concern here.** With n = 5000 and a price sequence where waiting is always chosen, `dfs` nests ~5000 deep — well past Python's default [recursion limit](../syntax/recursion-limit.md) of 1000. In practice this problem's tests usually pass because the memo short-circuits many paths, but **it's an honest weakness of the top-down version** and worth flagging unprompted rather than being caught by it.

**The bottom-up version fixes both, at O(1) space.** Rewrite the recurrence forwards with three running values:

```python
hold = float("-inf")   # best profit while holding a share
sold = 0               # best profit having just sold today (in cooldown tomorrow)
rest = 0               # best profit holding nothing and free to buy

for price in prices:
    prev_sold = sold
    sold = hold + price          # sell what we held
    hold = max(hold, rest - price)   # keep holding, or buy today
    rest = max(rest, prev_sold)      # stay free, or become free after yesterday's sale
return max(sold, rest)
```

**O(1) space, no recursion, no memo.** This is the three-state machine mentioned in section 2 — the cooldown becomes an explicit `sold` state instead of an `i+2` jump.

| Version | Space | Why |
|---|---|---|
| Memoized recursion | **O(n)** | 2n memo entries plus up to n stack frames |
| Bottom-up array | **O(n)** | Two arrays of n, no stack |
| **Rolling variables** | **O(1)** | Each day reads only yesterday's three values |

Same reduction as all of Unit 13 — a fixed lookback window means a fixed number of variables — and here the "window" is three values rather than two.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Without the cooldown this is just 'sum every upward step'. The cooldown breaks that, because selling costs you the next day's opportunity — on `[1,2,3,0,2]` the naive sum gives 4, but the real answer is 3. So the day index alone doesn't describe my situation; I also need to know whether I'm holding a share. That's a two-dimensional state, `(day, holding)`. If I'm holding I can sell or wait; if not, I can buy or wait. The cooldown is expressed by having a sell recurse to `i+2` instead of `i+1` — the skipped day is the cooldown, and since I'm not holding there's nothing else I'd do with it. I record a buy as negative so the running value is always net profit; otherwise I'd have to carry the purchase price in the state and the state space would blow up. There are 2n states and O(1) work each, so O(n) time, O(n) space for the memo and stack. I can roll it into a three-state bottom-up version for O(1) space and no recursion depth risk."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't you just sum the rises?" | That's the no-cooldown problem. On `[1,2,3,0,2]` it captures both the 1→2 and 2→3 rises, which would require selling on day 1 and buying on day 2 — forbidden. It gives 4; the answer is 3. |
| "Why does selling jump to `i+2`?" | Because the next day is the cooldown. You can't buy on it, and you hold nothing, so there's no decision to make — skipping it directly is equivalent and simpler than adding a third state. |
| "Why is buying negative?" | So the value is always net profit, one number. Tracking the purchase price separately would require carrying it in the state — `(day, holding, buy_price)` — which is far larger. |
| "Make it O(1) space." | Three rolling values — `hold`, `sold`, `rest` — updated per day. That's the explicit three-state machine, and it also removes the recursion depth risk. |
| "What if the cooldown were k days?" | Selling recurses to `i + k + 1`. In the bottom-up form you'd need to look back k+1 days, so O(k) rolling values instead of three. |
| "What if there were a transaction fee?" | Subtract it on each sale: `prices[i] - fee + dfs(...)`. That's [Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) — same shape, no cooldown. |
| "At most k transactions?" | Add a third dimension for transactions remaining: `(day, holding, k)`. O(n·k) states. |
| "Isn't `holding` only two values — is this really 2-D?" | Yes, it's genuinely two-dimensional; one dimension just happens to be tiny. The point is that the day index alone is insufficient to describe the state. |

**Traps:**
- **Base case `i == len(prices)` instead of `i >= len(prices)`.** A sell on the last day recurses to `i+2` and skips straight past the check — infinite recursion.
- **Applying the cooldown to buying instead of selling.** The asymmetry is deliberate: `i+2` after a sell, `i+1` after a buy.
- **Keying the memo on `i` alone.** Holding and not-holding are different states with different answers; conflating them silently corrupts the result.
- Making buying positive and trying to subtract it later — you'd need the purchase price in the state.
- Forgetting that "do nothing" is always an option. Without it you'd force a transaction every day.
- Assuming the answer can be negative. It can't — waiting forever yields 0, and that option is always in the `max`.

**This same move shows up in:** [House Robber](198-house-robber.md) (taking something now blocks the next slot — the same "action has a delayed consequence" structure) · [Maximum Product Subarray](152-maximum-product-subarray.md) (carrying several parallel running states because one number can't describe a position) · [Coin Change](322-coin-change.md) (memoized state where the history doesn't matter, only the current position) · [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md) (adding a dimension to the state because a constraint makes one number insufficient).

</details>

---
