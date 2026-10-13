# 1193. Monthly Transactions I

**Medium** · [LeetCode](https://leetcode.com/problems/monthly-transactions-i/) · [Solution file (no hints)](../../problems/1000-1499/1193.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each month and country, report the number of transactions and their total amount, plus the number of **approved** transactions and their total amount. Any order.

```
Table: Transactions
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
id is the primary key of this table.
The table has information about incoming transactions.
The state column is an enum of type ["approved", "declined"].
```

```
Input:
Transactions table:
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+
Output:
+----------+---------+-------------+----------------+--------------------+-----------------------+
| month    | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+----------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12  | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01  | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01  | DE      | 1           | 1              | 2000               | 2000                  |
+----------+---------+-------------+----------------+--------------------+-----------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Four numbers per group — two over all rows, two over only the approved ones. You don't need two queries: aggregate a **conditional** value.

| The statement says | Which really means |
|---|---|
| "for each month and country" | Group by two things — and "month" isn't a column, it's derived from `trans_date` |
| month looks like `2018-12` | Format the date as year-month: `DATE_FORMAT(trans_date, '%Y-%m')` |
| "number of transactions and their total amount" | `COUNT(*)`, `SUM(amount)` |
| "number of approved transactions and their total amount" | The same two, counting only approved rows |
| `state` is an ENUM | Compare to the string `'approved'` |

🤔 **Before you open the next section:** how can one `SUM` add up only the approved amounts, while the group still contains declined rows?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Conditional aggregation** | `SUM(state = 'approved')`, `SUM(IF(state = 'approved', amount, 0))` | ✅ All four numbers in one pass |
| `CASE WHEN` inside `SUM` | `SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END)` | ✅ Same thing, standard SQL |
| `WHERE state = 'approved'` | filter, then count | ❌ Throws away the declined rows the totals need |
| Two queries joined | one for all, one for approved | ⚠️ Works, but groups with **no** approved rows vanish from the second |

**The decision: conditional aggregation.** Make the value inside the aggregate depend on the row: an approved row contributes its amount, any other row contributes 0.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT DATE_FORMAT(trans_date, '%Y-%m') AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(state = 'approved') AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(IF(state = 'approved', amount, 0)) AS approved_total_amount
```

**Six columns: the two keys, four aggregates.**

- `DATE_FORMAT(trans_date, '%Y-%m')` turns `2018-12-18` into `2018-12`. `%Y` is the 4-digit year, `%m` the 2-digit month.
- `COUNT(*)` and `SUM(amount)` cover every row in the group.
- `state = 'approved'` is 1 or 0, so `SUM` of it counts approved rows.
- `IF(state = 'approved', amount, 0)` is the amount for approved rows and 0 otherwise, so `SUM` of it totals only the approved amounts.

→ [date-parts-format](../sql/date-parts-format.md) · [conditional-aggregation](../sql/conditional-aggregation.md) · [if-function](../sql/if-function.md) · [count](../sql/count.md)

```sql
FROM Transactions
```

```sql
GROUP BY month, country;
```

**Group by the formatted month and the country.** MySQL lets `GROUP BY` use a `SELECT` alias, so `month` works. (Standard SQL — and many other databases — would need the expression repeated.)
→ [group-by](../sql/group-by.md) · [aliases](../sql/aliases.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT DATE_FORMAT(trans_date, '%Y-%m') AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(state = 'approved') AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(IF(state = 'approved', amount, 0)) AS approved_total_amount
FROM Transactions
GROUP BY month, country;
```

</details>

**Trace it** — what each row contributes:

| `id` | `country` | `state` | `amount` | `month` | `state = 'approved'` | `IF(approved, amount, 0)` |
|---|---|---|---|---|---|---|
| 121 | US | approved | 1000 | 2018-12 | 1 | 1000 |
| 122 | US | declined | 2000 | 2018-12 | 0 | 0 |
| 123 | US | approved | 2000 | 2019-01 | 1 | 2000 |
| 124 | DE | approved | 2000 | 2019-01 | 1 | 2000 |

December/US has two rows: count 2, approved 1, total 3000, approved total 1000.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass; each row updates four accumulators in its (month, country) group.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(g)</summary>

**O(g)** for g (month, country) groups.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Group by `DATE_FORMAT(trans_date, '%Y-%m')` and country. Totals are plain `COUNT(*)` and `SUM(amount)`. For the approved numbers I don't filter — I aggregate a conditional value: `SUM(state = 'approved')` counts them, and `SUM(IF(state = 'approved', amount, 0))` totals them. One pass, every group."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `WHERE state = 'approved'`?" | It removes the declined rows, so the all-transactions numbers would be wrong — and months with only declines would disappear. |
| "What if `country` is `NULL`?" | `NULL`s form their own group, reported with a `NULL` country. |
| "Add declined counts too." | `SUM(state = 'declined')` — one more column, same pass. |
| "Another way to get the month?" | `LEFT(trans_date, 7)` works because dates print as `YYYY-MM-DD`; `DATE_FORMAT` says what you mean. |
| "Months with no transactions?" | They can't appear — there are no rows to group. You'd need a calendar table to left-join from. |

**Traps:**

- **Filtering instead of conditional aggregation.**
- **`SUM(amount)` for the approved total** — that's every transaction's amount.
- **`'%Y-%M'`** — capital `M` is the month *name* (`December`), not the number.

**This same move shows up in:** [Queries Quality and Percentage](1211-queries-quality-and-percentage.md) (aggregating a flag) · [Confirmation Rate](1934-confirmation-rate.md) (`IF` inside an aggregate) · [Count Salary Categories](1907-count-salary-categories.md) (counting by condition).

</details>

---
