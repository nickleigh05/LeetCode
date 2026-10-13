# 1321. Restaurant Growth

**Medium** · [LeetCode](https://leetcode.com/problems/restaurant-growth/) · [Solution file (no hints)](../../problems/1000-1499/1321.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each day that has **six full days before it**, report the total amount paid over the 7-day window (that day plus the 6 before) and the average per day, rounded to 2 decimals. Order by `visited_on`.

```
Table: Customer
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| customer_id   | int     |
| name          | varchar |
| visited_on    | date    |
| amount        | int     |
+---------------+---------+
In SQL,(customer_id, visited_on) is the primary key for this table.
This table contains data about customer transactions in a restaurant.
visited_on is the date on which the customer with ID (customer_id) has visited the restaurant.
amount is the total paid by a customer.
```

```
Input:
Customer table:
+-------------+--------------+--------------+-------------+
| customer_id | name         | visited_on   | amount      |
+-------------+--------------+--------------+-------------+
| 1           | Jhon         | 2019-01-01   | 100         |
| 2           | Daniel       | 2019-01-02   | 110         |
| 3           | Jade         | 2019-01-03   | 120         |
| 4           | Khaled       | 2019-01-04   | 130         |
| 5           | Winston      | 2019-01-05   | 110         |
| 6           | Elvis        | 2019-01-06   | 140         |
| 7           | Anna         | 2019-01-07   | 150         |
| 8           | Maria        | 2019-01-08   | 80          |
| 9           | Jaze         | 2019-01-09   | 110         |
| 1           | Jhon         | 2019-01-10   | 130         |
| 3           | Jade         | 2019-01-10   | 150         |
+-------------+--------------+--------------+-------------+
Output:
+--------------+--------------+----------------+
| visited_on   | amount       | average_amount |
+--------------+--------------+----------------+
| 2019-01-07   | 860          | 122.86         |
| 2019-01-08   | 840          | 120            |
| 2019-01-09   | 840          | 120            |
| 2019-01-10   | 1000         | 142.86         |
+--------------+--------------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A moving window over **days**, not over customers. First collapse the table to one row per day; then slide a 7-row window along it.

| The statement says | Which really means |
|---|---|
| several customers can visit on one day | Two rows on 2019-01-10 → add them up first: one total per day |
| "seven days window (i.e., current day + 6 days before)" | A frame of 7 consecutive daily rows: `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` |
| "there will be at least one customer every day" | No missing days — 7 rows really are 7 calendar days |
| output starts at 2019-01-07 | Days without six predecessors are skipped |
| `amount` in the output | The 7-day **sum**, not the day's amount |
| `average_amount` | That sum ÷ 7, rounded |

🤔 **Before you open the next section:** why must you sum amounts per day *before* applying the 7-row window?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Daily totals, then a `ROWS` window** | CTE of daily sums; `SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` | ✅ Clear steps; one sort |
| `RANGE` window on dates | `RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW` | ✅ Correct even if days were missing |
| Self-join on a date range | each day joined to the days `BETWEEN visited_on - INTERVAL 6 DAY AND visited_on` | ✅ Works without window functions; O(d²) pairs at worst |
| Window over raw rows | `ROWS 6 PRECEDING` on the un-aggregated table | ❌ Two customers on one day make 7 rows less than 7 days |

**The decision: daily totals in a CTE, then a `ROWS` window.** The statement guarantees a row for every day, so "the last 7 rows" means "the last 7 days".

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
WITH daily AS (
    SELECT visited_on, SUM(amount) AS amount
    FROM Customer
    GROUP BY visited_on
),
```

**One row per day.** `WITH` names a subquery (a common table expression) so later steps can use it like a table. 2019-01-10 had two customers — 130 + 150 — so its daily total is 280:

| `visited_on` | `amount` |
|---|---|
| 2019-01-01 | 100 |
| 2019-01-02 | 110 |
| 2019-01-03 | 120 |
| 2019-01-04 | 130 |
| 2019-01-05 | 110 |
| 2019-01-06 | 140 |
| 2019-01-07 | 150 |
| 2019-01-08 | 80 |
| 2019-01-09 | 110 |
| 2019-01-10 | 280 |

→ [cte-with](../sql/cte-with.md) · [group-by](../sql/group-by.md)

```sql
windowed AS (
    SELECT visited_on,
           SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
           ROW_NUMBER() OVER (ORDER BY visited_on) AS day_number
    FROM daily
)
```

**Slide the window.** For each day, `SUM … OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` adds that day and the six rows before it. `ROW_NUMBER()` numbers the days 1, 2, 3, … so we can find the first day with a complete window.
→ [window-frames](../sql/window-frames.md) · [window-aggregates](../sql/window-aggregates.md) · [ranking-functions](../sql/ranking-functions.md)

```sql
SELECT visited_on, amount, ROUND(amount / 7, 2) AS average_amount
FROM windowed
WHERE day_number >= 7
ORDER BY visited_on;
```

**Keep only complete windows, and average.** Day 7 is the first with six days before it. The window sum is divided by 7 — the number of days — not by the number of customers.
→ [math-functions](../sql/math-functions.md) · [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
WITH daily AS (
    SELECT visited_on, SUM(amount) AS amount
    FROM Customer
    GROUP BY visited_on
),
windowed AS (
    SELECT visited_on,
           SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
           ROW_NUMBER() OVER (ORDER BY visited_on) AS day_number
    FROM daily
)
SELECT visited_on, amount, ROUND(amount / 7, 2) AS average_amount
FROM windowed
WHERE day_number >= 7
ORDER BY visited_on;
```

</details>

**Trace it** — the window sum for every day:

| `visited_on` | `that day` | `7-day sum` | `day_number` |
|---|---|---|---|
| 2019-01-01 | 100 | 100 | 1 |
| 2019-01-02 | 110 | 210 | 2 |
| 2019-01-03 | 120 | 330 | 3 |
| 2019-01-04 | 130 | 460 | 4 |
| 2019-01-05 | 110 | 570 | 5 |
| 2019-01-06 | 140 | 710 | 6 |
| 2019-01-07 | 150 | 860 | 7 |
| 2019-01-08 | 80 | 840 | 8 |
| 2019-01-09 | 110 | 840 | 9 |
| 2019-01-10 | 280 | 1000 | 10 |

Days 1–6 have incomplete windows (their sums are smaller because fewer days are included). From day 7 on: 860 / 7 = 122.86, 840 / 7 = 120.00, 840 / 7 = 120.00, 1000 / 7 = 142.86.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + d log d)</summary>

**O(n)** to total n rows into d days, then **O(d log d)** to sort the days for the window; the moving sum itself is maintained incrementally, O(d).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d)</summary>

**O(d)** for the daily totals.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First I total the amounts per day, since several customers can visit on one day. Then a window `SUM` over the current and six preceding days gives the 7-day total, and `ROW_NUMBER` lets me drop the first six days, whose windows are incomplete. The average is that sum over 7. Using `ROWS` is safe because every day has at least one visit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if some days had no visits?" | `ROWS` would then span more than 7 calendar days. Use `RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW` — and divide by 7 still, treating missing days as 0. |
| "Without window functions?" | Self-join the daily totals on `d2.visited_on BETWEEN d1.visited_on - INTERVAL 6 DAY AND d1.visited_on`, group by `d1`. |
| "Average per customer visit instead?" | Window-sum the visit counts too and divide sum by count. |
| "A 30-day window?" | `29 PRECEDING`, and keep days from number 30 on. |

**Traps:**

- **Windowing raw rows** — multiple customers per day break "7 rows = 7 days".
- **Reporting incomplete windows** — the first six days must be skipped.
- **Dividing by the number of rows** — the average is per day.

**This same move shows up in:** [Last Person to Fit in the Bus](1204-last-person-to-fit-in-the-bus.md) (a running total — a window with no start) · [Rising Temperature](197-rising-temperature.md) (date-based neighbours) · [Department Top Three Salaries](185-department-top-three-salaries.md) (window functions with `PARTITION BY`).

</details>

---
