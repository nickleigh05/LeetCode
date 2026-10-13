# 1393. Capital Gain/Loss

**Medium** · [LeetCode](https://leetcode.com/problems/capital-gainloss/) · [Solution file (no hints)](../../problems/1000-1499/1393.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Every `Buy` is followed later by a `Sell`. For each stock, report the total capital gain or loss: everything received from sells minus everything paid for buys. Any order.

```
Table: Stocks
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| stock_name    | varchar |
| operation     | enum    |
| operation_day | int     |
| price         | int     |
+---------------+---------+
(stock_name, operation_day) is the primary key (combination of columns with unique values) for this table.
The operation column is an ENUM (category) of type ('Sell', 'Buy')
Each row of this table indicates that the stock which has stock_name had an operation on the day operation_day with the price.
It is guaranteed that each 'Sell' operation for a stock has a corresponding 'Buy' operation in a previous day. It is also guaranteed that each 'Buy' operation for a stock has a corresponding 'Sell' operation in an upcoming day.
```

```
Input:
Stocks table:
+---------------+-----------+---------------+--------+
| stock_name    | operation | operation_day | price  |
+---------------+-----------+---------------+--------+
| Leetcode      | Buy       | 1             | 1000   |
| Corona Masks  | Buy       | 2             | 10     |
| Leetcode      | Sell      | 5             | 9000   |
| Handbags      | Buy       | 17            | 30000  |
| Corona Masks  | Sell      | 3             | 1010   |
| Corona Masks  | Buy       | 4             | 1000   |
| Corona Masks  | Sell      | 5             | 500    |
| Corona Masks  | Buy       | 6             | 1000   |
| Handbags      | Sell      | 29            | 7000   |
| Corona Masks  | Sell      | 10            | 10000  |
+---------------+-----------+---------------+--------+
Output:
+---------------+-------------------+
| stock_name    | capital_gain_loss |
+---------------+-------------------+
| Corona Masks  | 9500              |
| Leetcode      | 8000              |
| Handbags      | -23000            |
+---------------+-------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

It looks like you need to pair each buy with its sell. You don't: the total gain is the **sum of sell prices minus the sum of buy prices**, and the guarantees make that pairing unnecessary.

| The statement says | Which really means |
|---|---|
| "each 'Sell' … has a corresponding 'Buy' in a previous day" and vice versa | Buys and sells come in complete pairs — nothing left open |
| "total gain or loss after buying and selling … one or many times" | Σ (sell − buy) over all pairs = Σ sells − Σ buys |
| `operation` is `'Buy'` or `'Sell'` | Give each row a sign: −price for a buy, +price for a sell |
| output `capital_gain_loss` | One number per stock, can be negative |

🤔 **Before you open the next section:** Corona Masks has three buy/sell pairs. Is (1010 − 10) + (500 − 1000) + (10000 − 1000) the same as (1010 + 500 + 10000) − (10 + 1000 + 1000)?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Sum a signed price** | `SUM(IF(operation = 'Buy', -price, price))` | ✅ One pass, one aggregate |
| Sells minus buys | `SUM(CASE WHEN … 'Sell' …) - SUM(CASE WHEN … 'Buy' …)` | ✅ The same arithmetic, spelled out |
| Pair each buy with its sell | a self-join or `LEAD` to match rows, then sum differences | ⚠️ Correct, much more work, and unnecessary given the guarantees |

**The decision: sum the signed price.** Addition doesn't care about order, so Σ(sell − buy) collapses to Σsells − Σbuys.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT stock_name,
       SUM(IF(operation = 'Buy', -price, price)) AS capital_gain_loss
```

**Spending is negative, income positive.** `IF(operation = 'Buy', -price, price)` flips the sign of every purchase; `SUM` adds them up per stock.
→ [if-function](../sql/if-function.md) · [conditional-aggregation](../sql/conditional-aggregation.md)

```sql
FROM Stocks
```

```sql
GROUP BY stock_name;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT stock_name,
       SUM(IF(operation = 'Buy', -price, price)) AS capital_gain_loss
FROM Stocks
GROUP BY stock_name;
```

</details>

**Trace it** — every row's signed price:

| `stock_name` | `operation` | `operation_day` | `price` | `signed price` |
|---|---|---|---|---|
| Corona Masks | Buy | 2 | 10 | -10 |
| Corona Masks | Sell | 3 | 1010 | 1010 |
| Corona Masks | Buy | 4 | 1000 | -1000 |
| Corona Masks | Sell | 5 | 500 | 500 |
| Corona Masks | Buy | 6 | 1000 | -1000 |
| Corona Masks | Sell | 10 | 10000 | 10000 |
| Handbags | Buy | 17 | 30000 | -30000 |
| Handbags | Sell | 29 | 7000 | 7000 |
| Leetcode | Buy | 1 | 1000 | -1000 |
| Leetcode | Sell | 5 | 9000 | 9000 |

Corona Masks: −10 + 1010 − 1000 + 500 − 1000 + 10000 = 9500. Handbags: −30000 + 7000 = −23000. Leetcode: −1000 + 9000 = 8000.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass, one running sum per stock.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(s)</summary>

**O(s)** for s stocks.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because every buy has a matching later sell, the total gain is just total sell prices minus total buy prices. I sum a signed price — negative for buys, positive for sells — grouped by stock."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if some stocks are still held (a buy with no sell)?" | The formula would count the open buy as a loss. Exclude it — e.g. drop each stock's last row when it's a `Buy`, found with `LEAD` or `ROW_NUMBER`. |
| "Gain per individual trade?" | Pair rows with `LEAD(price) OVER (PARTITION BY stock_name ORDER BY operation_day)` on the buy rows. |
| "Only stocks that lost money?" | `HAVING capital_gain_loss < 0`. |
| "Quantities other than one share?" | Multiply: `SUM(IF(operation = 'Buy', -1, 1) * price * quantity)`. |

**Traps:**

- **Pairing rows when you don't have to** — easy to get wrong for no benefit.
- **`SUM(price)`** — ignores whether it was a buy or a sell.

**This same move shows up in:** [Monthly Transactions I](1193-monthly-transactions-i.md) (conditional sums) · [Average Time of Process per Machine](1661-average-time-of-process-per-machine.md) (the signed-sum trick, as an alternative there) · [Count Salary Categories](1907-count-salary-categories.md) (aggregating by condition).

</details>

---
