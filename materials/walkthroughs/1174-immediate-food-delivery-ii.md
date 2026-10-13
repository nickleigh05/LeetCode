# 1174. Immediate Food Delivery II

**Medium** · [LeetCode](https://leetcode.com/problems/immediate-food-delivery-ii/) · [Solution file (no hints)](../../problems/1000-1499/1174.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

An order is **immediate** if its preferred delivery date equals the order date. Looking only at each customer's **first** order, what percentage are immediate? Round to 2 decimals.

```
Table: Delivery
+-----------------------------+---------+
| Column Name                 | Type    |
+-----------------------------+---------+
| delivery_id                 | int     |
| customer_id                 | int     |
| order_date                  | date    |
| customer_pref_delivery_date | date    |
+-----------------------------+---------+
delivery_id is the column of unique values of this table.
The table holds information about food delivery to customers that make orders at some date and specify a preferred delivery date (on the same order date or after it).
```

```
Input:
Delivery table:
+-------------+-------------+------------+-----------------------------+
| delivery_id | customer_id | order_date | customer_pref_delivery_date |
+-------------+-------------+------------+-----------------------------+
| 1           | 1           | 2019-08-01 | 2019-08-02                  |
| 2           | 2           | 2019-08-02 | 2019-08-02                  |
| 3           | 1           | 2019-08-11 | 2019-08-12                  |
| 4           | 3           | 2019-08-24 | 2019-08-24                  |
| 5           | 3           | 2019-08-21 | 2019-08-22                  |
| 6           | 2           | 2019-08-11 | 2019-08-13                  |
| 7           | 4           | 2019-08-09 | 2019-08-09                  |
+-------------+-------------+------------+-----------------------------+
Output:
+----------------------+
| immediate_percentage |
+----------------------+
| 50.00                |
+----------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Two steps: find each customer's first order, then compute a percentage over just those rows.

| The statement says | Which really means |
|---|---|
| "the first order … the earliest order date" | Per customer, `MIN(order_date)` |
| "precisely one first order" | No ties on the earliest date — matching on (customer, date) finds exactly one row |
| "immediate" = preferred date equals order date | A per-row flag: `order_date = customer_pref_delivery_date` |
| "percentage of immediate orders **in the first orders**" | Average that flag over first orders only, × 100 |
| output is a single number | No `GROUP BY` in the final query — one aggregate over all first orders |

🤔 **Before you open the next section:** `MIN(order_date)` per customer gives you a date, not a row. How do you get back to the *row* that has that date?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Tuple `IN` a grouped subquery** | `WHERE (customer_id, order_date) IN (SELECT customer_id, MIN(order_date) … GROUP BY customer_id)` | ✅ Picks exactly the first-order rows |
| `ROW_NUMBER()` | number each customer's orders by date, keep `rn = 1` | ✅ Generalises to "second order", "latest order" |
| Join to the grouped subquery | `JOIN (SELECT customer_id, MIN(order_date) …) f ON …` | ✅ Same rows as a join |
| Average over all orders | no first-order filter | ❌ Answers a different question — 42.86 instead of 50.00 |
| `WHERE order_date = (SELECT MIN(order_date) FROM Delivery)` | the global minimum | ❌ One date for everyone, not one per customer |

**The decision: the tuple `IN`.** MySQL can compare two columns at once against a subquery that returns two columns — "this customer, on their first date."

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2) AS immediate_percentage
```

**The percentage, as an average of a flag.** `order_date = customer_pref_delivery_date` is 1 for an immediate order, 0 otherwise. Averaging over the first orders gives the immediate fraction; `* 100` and `ROUND(…, 2)` format it.
→ [conditional-aggregation](../sql/conditional-aggregation.md) · [ratios-percentages](../sql/ratios-percentages.md)

```sql
FROM Delivery
```

```sql
WHERE (customer_id, order_date) IN (
    SELECT customer_id, MIN(order_date)
    FROM Delivery
    GROUP BY customer_id
);
```

**Keep only each customer's first order.** The subquery returns one `(customer_id, first date)` pair per customer:

| `customer_id` | `first_order` |
|---|---|
| 1 | 2019-08-01 |
| 2 | 2019-08-02 |
| 3 | 2019-08-21 |
| 4 | 2019-08-09 |

The outer `WHERE` keeps a row only if its `(customer_id, order_date)` pair is in that list.
→ [in-subquery](../sql/in-subquery.md) · [group-by](../sql/group-by.md) · [first-row-per-group](../sql/first-row-per-group.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2) AS immediate_percentage
FROM Delivery
WHERE (customer_id, order_date) IN (
    SELECT customer_id, MIN(order_date)
    FROM Delivery
    GROUP BY customer_id
);
```

</details>

**Trace it** — the four first orders that survive, and their flags:

| `delivery_id` | `customer_id` | `order_date` | `customer_pref_delivery_date` | `immediate?` |
|---|---|---|---|---|
| 1 | 1 | 2019-08-01 | 2019-08-02 | 0 |
| 2 | 2 | 2019-08-02 | 2019-08-02 | 1 |
| 5 | 3 | 2019-08-21 | 2019-08-22 | 0 |
| 7 | 4 | 2019-08-09 | 2019-08-09 | 1 |

2 of 4 are immediate → 50.00. Over **all** orders it would be different:

| `over ALL orders` |
|---|
| 42.86 |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n deliveries: one pass to compute the minimum date per customer, one pass to test each row against that set (MySQL materialises the subquery into a hashed temporary table), then a single aggregate.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(c)</summary>

**O(c)** for the c (customer, first date) pairs the subquery produces.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First I find each customer's earliest order date with a grouped subquery, and keep the rows whose (customer, date) pair matches. Over those first orders, the immediate percentage is the average of `order_date = customer_pref_delivery_date`, times 100, rounded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it with a window function." | `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)` in a subquery, keep `rn = 1`. |
| "What if a customer had two orders on their first day?" | The `IN` version would keep both. `ROW_NUMBER` with a tiebreaker (`ORDER BY order_date, delivery_id`) keeps exactly one. |
| "Immediate percentage of each customer's **latest** order?" | `MAX(order_date)`, or `ORDER BY order_date DESC` in the window. |
| "Percentage of customers whose orders were *all* immediate?" | Group by customer with `MIN(order_date = customer_pref_delivery_date) = 1`, then average that. |

**Traps:**

- **Averaging over all orders** — the problem is specifically about first orders.
- **A global `MIN`** — `(SELECT MIN(order_date) FROM Delivery)` without grouping is one date for the whole table.
- **Grouping the outer query** — the answer is one number, not one per customer.

**This same move shows up in:** [Game Play Analysis IV](550-game-play-analysis-iv.md) (each player's first day, then a fraction) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (rows from each product's first year) · [Department Highest Salary](184-department-highest-salary.md) (rows matching a per-group extreme).

</details>

---
