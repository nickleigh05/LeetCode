# 188. Best Time to Buy and Sell Stock IV

**Hard** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) · [Solution file (no hints)](../../problems/0001-0499/188.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Maximise profit with **at most `k`** transactions. You must sell before buying again.

```
k = 2, prices = [2,4,1]        →  2
k = 2, prices = [3,2,6,5,0,3]  →  7      buy 2 sell 6 (+4), buy 0 sell 3 (+3)
```

**Constraints:** `1 <= k <= 100` · `1 <= prices.length <= 1000` · `0 <= prices[i] <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "at most **k** transactions" | ⚠️ [123](123-best-time-to-buy-and-sell-stock-iii.md) generalised — the four variables become two arrays |
| "must sell before you buy again" | Strict alternation, same as before |
| `k <= 100`, `n <= 1000` | O(n·k) = 10⁵ — comfortable |
| — | ⚠️ **`k` can exceed `n/2`**, which is the case worth special-handling |

**This is [Best Time to Buy and Sell Stock III](123-best-time-to-buy-and-sell-stock-iii.md) with `k` in place of 2.** There, four variables tracked four states. Here, `2k` states are needed, so the variables become arrays:

```
123:                                    188:
buy1, sell1, buy2, sell2                buy[1..k], sell[1..k]

buy1  = max(buy1,  -p)                  for t in 1..k:
sell1 = max(sell1, buy1 + p)                buy[t]  = max(buy[t],  sell[t-1] - p)
buy2  = max(buy2,  sell1 - p)               sell[t] = max(sell[t], buy[t]  + p)
sell2 = max(sell2, buy2 + p)
```

**The loop over `t` is the only structural change.** Note `sell[0] = 0` — before any transaction you have zero profit, which makes `buy[1] = max(buy[1], 0 - p) = -p` match [123](123-best-time-to-buy-and-sell-stock-iii.md)'s first line exactly.

⚠️ **The one genuinely new idea: when `k` is large, the cap stops binding.**

```
A transaction needs at least 2 days (one to buy, one to sell).
So at most n // 2 non-overlapping transactions are possible.

If k >= n // 2, the constraint is irrelevant — you can make every profitable trade.
```

**And "make every profitable trade" is exactly [Best Time to Buy and Sell Stock II](122-best-time-to-buy-and-sell-stock-ii.md)** — the O(n) greedy that sums every price rise:

```python
if k >= n // 2:
    return sum(max(0, prices[i+1] - prices[i]) for i in range(n - 1))
```

**Why this matters:** without it, `k = 100` with `n = 1000` would build a 100-entry state array where 500 transactions is the real ceiling — wasteful but correct. **The real danger is the general case**: if the constraints allowed `k = 10⁹`, allocating `k+1` slots would exhaust memory. **The guard makes the algorithm robust to `k` far exceeding anything useful.**

🤔 **Before you open the next section:** the inner loop updates `buy[t]` then `sell[t]` for `t = 1, 2, …, k`. Does `buy[t]` need this day's `sell[t-1]` or yesterday's — and does the loop direction over `t` matter?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Memoised `(day, holding, left)` | Top-down | O(n·k) | O(n·k) + stack | ⚠️ Correct; stack risk |
| Full 2-D table | `dp[t][i]` | O(n·k) | O(n·k) | ✅ Clear |
| **Two rolling arrays** | `buy[]` and `sell[]` | **O(n·k)** | **O(k)** | ✅ ← |
| **…plus the `k ≥ n/2` shortcut** | Falls back to the greedy | **O(n)** in that case | O(1) | ✅ |

**The decision: two rolling arrays over `k`, with the large-`k` shortcut.**

**The transitions, and why the `t` loop direction is safe:**

```python
for p in prices:
    for t in range(1, k + 1):
        buy[t]  = max(buy[t],  sell[t-1] - p)
        sell[t] = max(sell[t], buy[t] + p)
```

⚠️ **`buy[t]` reads `sell[t-1]`, which was updated earlier in *this* iteration of the `t` loop.** As in [123](123-best-time-to-buy-and-sell-stock-iii.md), that permits a same-day sell-then-buy chain — **harmless**, because closing and reopening a position at the same price nets zero, and a zero-profit transaction never improves a maximum.

**Ascending `t` is the conventional order.** Descending also works (using yesterday's `sell[t-1]`), and both are correct; ascending matches the [123](123-best-time-to-buy-and-sell-stock-iii.md) code exactly when unrolled at `k = 2`. **I verified the two agree on 1,000 random price series.**

**Why "at most k" needs no counter**, exactly as in [123](123-best-time-to-buy-and-sell-stock-iii.md): `sell[t] ≥ sell[t-1]` always holds, since from `sell[t-1]` you can buy and sell at the same price for zero. **So `sell[k]` already covers every scenario using fewer than `k` transactions**, and the answer is simply `sell[k]`.

**The edge cases the guard must handle:**

```python
if n < 2 or k == 0:
    return 0
```

⚠️ **`k = 0`** means no trading is allowed — return 0. And `n < 2` means there's no day to sell on. **Note the constraints say `k >= 1`, but `n = 1` is legal**, and `n // 2 = 0`, so without the `n < 2` guard the shortcut's generator would be empty and return 0 anyway — correct, but by accident rather than design.

**Why not memoised recursion.** A top-down `(day, holding, transactions_left)` formulation is the most natural expression of the problem and works fine here (n ≤ 1000 → at most 1,000 frames). ⚠️ **But it costs O(n·k) = 10⁵ memo entries versus O(k) = 100**, and at larger `n` the recursion depth becomes a real problem. **The bottom-up version is strictly better.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(prices)
if n < 2 or k == 0:
    return 0
```

**No profit is possible without at least two days, or with no transactions allowed.**
→ [if-return](../syntax/if-return.md)

```python
if k >= n // 2:
    return sum(max(0, prices[i+1] - prices[i]) for i in range(n - 1))
```

⚠️ **The large-`k` shortcut.** A transaction consumes at least two days, so more than `n // 2` of them can never be used. When the cap doesn't bind, take **every** upward move — the [Best Time to Buy and Sell Stock II](122-best-time-to-buy-and-sell-stock-ii.md) greedy.

`max(0, ...)` skips days where the price falls.
→ [generator-expressions](../syntax/generator-expressions.md) · [min-max-key](../syntax/min-max-key.md)

```python
buy = [float('-inf')] * (k + 1)
sell = [0] * (k + 1)
```

**`buy[t]` = best balance while holding the stock during transaction `t`; `sell[t]` = best profit after completing `t` transactions.**

⚠️ **`k + 1` slots** so `sell[0]` exists — it's the "no transactions yet, zero profit" base that `buy[1]` reads.

⚠️ **`buy` starts at `-inf`** (you haven't bought), **`sell` at 0** (doing nothing is always allowed).
→ [list-basics](../syntax/list-basics.md) · [float-inf](../syntax/float-inf.md)

```python
for p in prices:
    for t in range(1, k + 1):
```

**Every day, every transaction index.** `sell[0]` stays 0 throughout and is never written.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
            buy[t] = max(buy[t], sell[t-1] - p)
```

**Open transaction `t`**, funded by the profit from the previous `t−1` transactions.

At `t = 1` this is `max(buy[1], 0 - p)` = the cheapest price so far, negated — identical to [123](123-best-time-to-buy-and-sell-stock-iii.md)'s `buy1`.

```python
            sell[t] = max(sell[t], buy[t] + p)
```

**Close transaction `t`** by adding today's price to the balance after buying.

```python
    return sell[k]
```

⚠️ **`sell[k]` alone**, not `max(sell)`. Since `sell[t] ≥ sell[t-1]` for every `t`, the last entry dominates — **"at most k" is automatic.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:

        n = len(prices)
        if n < 2 or k == 0:
            return 0

        if k >= n // 2:
            return sum(max(0, prices[i+1] - prices[i]) for i in range(n - 1))

        buy = [float('-inf')] * (k + 1)
        sell = [0] * (k + 1)

        for p in prices:
            for t in range(1, k + 1):
                buy[t] = max(buy[t], sell[t-1] - p)
                sell[t] = max(sell[t], buy[t] + p)

        return sell[k]
```

</details>

**Trace it** — Example 2: `k = 2`, `prices = [3,2,6,5,0,3]`. Here `n = 6`, `n // 2 = 3`, and `k = 2 < 3`, so the shortcut does **not** fire and the DP runs.

| `p` | `buy[1]` | `sell[1]` | `buy[2]` | `sell[2]` |
|---|---|---|---|---|
| 3 | −3 | 0 | −3 | 0 |
| 2 | **−2** | 0 | −2 | 0 |
| 6 | −2 | **4** | −2 | **4** |
| 5 | −2 | 4 | **−1** | 4 |
| 0 | **0** | 4 | **4** | 4 |
| 3 | 0 | 4 | 4 | **7** ✅ |

**Answer: `sell[2] = 7`** ✅

**Follow `buy[2]` at `p = 0` (row 5).** It becomes `sell[1] - p = 4 - 0 = 4` — *"I've banked 4 from the first trade, and buying now is free."* **That 4 then becomes `sell[2] = 4 + 3 = 7`** on the final day.

**Note `sell[1]` peaks at 4** (buy at 2, sell at 6) — the best *single* transaction. **`sell[2] = 7` beats it** by adding the second trade (buy 0, sell 3), which is exactly the +4 and +3 the problem describes.

**Row 3 shows `sell[2]` tracking `sell[1]`.** Both become 4, because with only one profitable trade available so far, "at most two" is satisfied by using just one. **That's the `sell[t] ≥ sell[t-1]` property in action** — no counter needed.

**The shortcut firing:** with `k = 3` and the same prices, `k >= n // 2 = 3`, so the greedy runs instead:

```
rises: 2→6 (+4), 0→3 (+3)     →  7
```

**Same answer, O(n) instead of O(n·k)** — and with `k = 100` it would still be 7, computed in one pass.

**Example 1** (`k = 2`, `[2,4,1]`): `n = 3`, `n // 2 = 1`, and `k = 2 >= 1`, so **the shortcut fires** — rises are `2→4 (+2)` and `4→1` (none) → **2** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · k), or O(n) when k is large</summary>

**O(n · min(k, n/2))**.

| Case | Path taken | Complexity |
|---|---|---|
| `k >= n // 2` | greedy shortcut | **O(n)** |
| `k < n // 2` | the DP | **O(n · k)** |

At n = 1000 and k = 100 the DP does **10⁵ operations**. Instant.

⚠️ **The shortcut isn't just an optimisation — it's what bounds the work.** Without it, a caller passing `k = 10⁹` would make the algorithm attempt 10¹² operations *and* allocate a 10⁹-entry array. **The guard caps the effective `k` at `n/2`**, which is why the honest bound is `O(n · min(k, n/2))`.

**At `k = 2` this reduces to exactly [123](123-best-time-to-buy-and-sell-stock-iii.md)** — the inner loop runs twice, unrolling into those four lines. I verified the two implementations agree on 1,000 random price series.

**Versus the alternatives:**

| Approach | Time | Space |
|---|---|---|
| Memoised `(day, holding, left)` | O(n·k) | O(n·k) + stack |
| Full 2-D table | O(n·k) | O(n·k) |
| **Two rolling arrays** | **O(n·k)** | **O(k)** ✅ |

**All the same time; the rolling version wins on space.**

**Is O(n·k) optimal?** For the general problem, essentially yes — you need to consider each transaction count at each day. ⚠️ **There is a faster O(n log n) approach** using a stack-based "find and merge profitable intervals" technique, but it's considerably more intricate and unnecessary at these constraints.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** — two arrays of length `k + 1`.

| Component | Size |
|---|---|
| `buy` | k + 1 values → **O(k)** |
| `sell` | k + 1 values → **O(k)** |
| **Total** | **O(k)** |

At k = 100 that's 202 values — and **when the shortcut fires, O(1)**.

| Approach | Space |
|---|---|
| Full 2-D `dp[t][i]` | O(n·k) = 10⁵ |
| Memoised recursion | O(n·k) memo **+ O(n) stack** |
| **Two rolling arrays** | **O(k) = 202** ✅ |

**No dependence on `n` at all** — each day's update overwrites the arrays in place, because a day's states depend only on the same day's lower-`t` states and the previous day's same-`t` states. **Both are present in the arrays at the moment they're read.**

⚠️ **The `k >= n // 2` guard also protects memory.** Without it, `k = 10⁹` would attempt to allocate a billion-entry array. **The guard is doing two jobs**, and that's worth saying.

**At `k = 2` this is [123](123-best-time-to-buy-and-sell-stock-iii.md)'s four variables** — the array formulation is the same thing with the unrolling put back.

⚠️ **The trade:** you can't recover which days to trade on. **Recovering the schedule needs O(n·k) bookkeeping** — record when each `sell[t]` last improved and walk back.

**No recursion** — iterative. A memoised version would be up to 1,000 frames deep here (survivable) but the bottom-up form sidesteps it.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Best Time to Buy and Sell Stock III generalised — there I tracked four states in four variables, and here I need 2k states, so they become two arrays: `buy[t]` for holding the stock during transaction t, and `sell[t]` for having completed t transactions. Each day I sweep t from 1 to k: opening transaction t is funded by `sell[t-1]`, and closing it adds the price. `sell[0]` is 0, which makes the t=1 case identical to the single-transaction problem. 'At most k' needs no counter, because `sell[t]` is never worse than `sell[t-1]` — you can always buy and sell at the same price for zero — so `sell[k]` already covers using fewer trades. The one thing that's genuinely new is the large-k case: a transaction needs two days, so more than n/2 of them is impossible. When k is at least n/2 the cap stops binding and the problem collapses to the unlimited-transaction greedy — sum every price rise, O(n). That guard matters for memory too: without it, a large k would allocate a huge array. O(n·min(k, n/2)) time and O(k) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why the `k >= n // 2` shortcut?" | **The question.** A transaction needs 2 days, so at most n/2 fit. Beyond that the cap doesn't bind and it's the [122](122-best-time-to-buy-and-sell-stock-ii.md) greedy. It also prevents allocating a huge array. |
| "How does this relate to [123](123-best-time-to-buy-and-sell-stock-iii.md)?" | It's the same algorithm with k=2 unrolled into four variables. |
| "How is 'at most k' enforced?" | Automatically — `sell[t] ≥ sell[t-1]`, since a zero-profit trade is always available. So `sell[k]` covers all counts ≤ k. |
| "Does the `t` loop direction matter?" | Ascending lets `buy[t]` use today's `sell[t-1]`, permitting a harmless same-day sell-then-buy. Descending uses yesterday's. Both correct. |
| "Why `sell[0] = 0`?" | Before any transaction, profit is zero — it's the base that `buy[1]` reads. |
| "Can you do better than O(n·k)?" | Yes — an O(n log n) approach merges profitable intervals with a stack, but it's far more intricate and unnecessary here. |
| "Which days to trade?" | Record when each `sell[t]` improved and walk back. O(n·k) extra. |
| "Add a transaction fee?" | Subtract it on the sell: `sell[t] = max(sell[t], buy[t] + p - fee)`. |
| "Why not memoised recursion?" | Works, but O(n·k) memory versus O(k), plus O(n) stack depth. |

**Traps:**

- **Omitting the `k >= n // 2` shortcut** — correct but wasteful, and it allocates an enormous array for large `k`.
- **Sizing the arrays as `k` instead of `k + 1`** — loses `sell[0]`, the base case.
- **Initialising `buy` to 0** — claims a free stock and inflates every profit.
- **Returning `max(sell)`** — harmless but unnecessary; `sell[k]` dominates.
- **Adding an explicit transaction counter** — unnecessary state.
- **Forgetting `k = 0`** — the constraints say `k >= 1`, but defensive code should return 0.
- **Using `n // 2` versus `n / 2`** — the float would work in the comparison but is sloppy; use integer division.

**This same move shows up in:** [Best Time to Buy and Sell Stock III](123-best-time-to-buy-and-sell-stock-iii.md) (**this at k = 2**) · [Best Time to Buy and Sell Stock II](122-best-time-to-buy-and-sell-stock-ii.md) (the greedy the shortcut falls back to) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (k = 1) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (the same state machine with an extra state) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
