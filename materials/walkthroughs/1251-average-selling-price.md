# 1251. Average Selling Price

**Easy** · [LeetCode](https://leetcode.com/problems/average-selling-price/) · [Solution file (no hints)](../../problems/1000-1499/1251.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Prices change over time. For each product, find the **average selling price** — total revenue ÷ total units — using the price that was in effect on each purchase date. Round to 2 decimals; a product with no sales averages **0**. Any order.

```
Table: Prices
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| start_date    | date    |
| end_date      | date    |
| price         | int     |
+---------------+---------+
(product_id, start_date, end_date) is the primary key (combination of columns with unique values) for this table.
Each row of this table indicates the price of the product_id in the period from start_date to end_date.
For each product_id there will be no two overlapping periods. That means there will be no two intersecting periods for the same product_id.

Table: UnitsSold
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| purchase_date | date    |
| units         | int     |
+---------------+---------+
This table may contain duplicate rows.
Each row of this table indicates the date, units, and product_id of each product sold. 
```

```
Input:
Prices table:
+------------+------------+------------+--------+
| product_id | start_date | end_date   | price  |
+------------+------------+------------+--------+
| 1          | 2019-02-17 | 2019-02-28 | 5      |
| 1          | 2019-03-01 | 2019-03-22 | 20     |
| 2          | 2019-02-01 | 2019-02-20 | 15     |
| 2          | 2019-02-21 | 2019-03-31 | 30     |
+------------+------------+------------+--------+
UnitsSold table:
+------------+---------------+-------+
| product_id | purchase_date | units |
+------------+---------------+-------+
| 1          | 2019-02-25    | 100   |
| 1          | 2019-03-01    | 15    |
| 2          | 2019-02-10    | 200   |
| 2          | 2019-03-22    | 30    |
+------------+---------------+-------+
Output:
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 1          | 6.96          |
| 2          | 16.96         |
+------------+---------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The join condition isn't "same id" — it's "same product **and** the purchase date falls inside the price's period."

| The statement says | Which really means |
|---|---|
| price rows have `start_date` and `end_date` | Each sale matches the price row whose period contains its date |
| "no two overlapping periods" | Each sale matches **exactly one** price row — no double counting |
| "average selling price" | Weighted by units: `SUM(units × price) / SUM(units)` — not `AVG(price)` |
| "if a product does not have any sold units … 0" | Products with no sales must appear, with 0 → `LEFT JOIN` from `Prices`, then turn `NULL` into 0 |
| `UnitsSold` "may contain duplicate rows" | Duplicates are separate sales; sum them all |

🤔 **Before you open the next section:** product 1 sold 100 units at 5 and 15 units at 20. Why isn't the answer (5 + 20) / 2 = 12.5?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Range join, weighted average** | `ON product matches AND purchase_date BETWEEN start_date AND end_date`, then `SUM(units*price)/SUM(units)` | ✅ Each sale priced correctly, weighted by units |
| `>=` / `<=` instead of `BETWEEN` | `purchase_date >= start_date AND purchase_date <= end_date` | ✅ Identical — `BETWEEN` is inclusive at both ends |
| `AVG(price)` | the average of the prices that occurred | ❌ Ignores how many units sold at each price |
| Date condition in `WHERE` | `LEFT JOIN … ON product_id … WHERE purchase_date BETWEEN …` | ❌ Removes products with no sales — see below |

**The decision: a range join with a weighted average.** "Average selling price" means revenue per unit sold, so each unit counts once:

| `product_id` | `ROUND(AVG(p.price), 2)` |
|---|---|
| 1 | 12.50 |
| 2 | 22.50 |

That's the average of the *price list*, not of what customers paid. The right answers are 6.96 and 16.96.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT p.product_id,
       IFNULL(ROUND(SUM(u.units * p.price) / SUM(u.units), 2), 0) AS average_price
```

**Revenue ÷ units, rounded, with 0 for no sales.** `SUM(u.units * p.price)` is the money taken in; `SUM(u.units)` is the units sold. For a product with no sales both are `NULL`, so the division is `NULL` — `IFNULL(…, 0)` turns that into the 0 the statement asks for.
→ [aggregate-functions](../sql/aggregate-functions.md) · [ifnull-coalesce](../sql/ifnull-coalesce.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Prices p
```

**Start from `Prices`,** so every product appears even if it never sold.

```sql
LEFT JOIN UnitsSold u
    ON  u.product_id = p.product_id
    AND u.purchase_date BETWEEN p.start_date AND p.end_date
```

**Match each sale to the price in effect on its date.** Two conditions: same product, and the purchase date inside the price's period. `BETWEEN` includes both endpoints, so a sale on `2019-03-01` matches the period starting that day.

Both conditions sit in `ON`. In a left join, that matters — see the trap below.
→ [non-equi-join](../sql/non-equi-join.md) · [between](../sql/between.md) · [left-join](../sql/left-join.md)

```sql
GROUP BY p.product_id;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT p.product_id,
       IFNULL(ROUND(SUM(u.units * p.price) / SUM(u.units), 2), 0) AS average_price
FROM Prices p
LEFT JOIN UnitsSold u
    ON  u.product_id = p.product_id
    AND u.purchase_date BETWEEN p.start_date AND p.end_date
GROUP BY p.product_id;
```

</details>

**Trace it** — every sale matched to its price period:

| `product_id` | `start_date` | `end_date` | `price` | `purchase_date` | `units` | `revenue` |
|---|---|---|---|---|---|---|
| 1 | 2019-02-17 | 2019-02-28 | 5 | 2019-02-25 | 100 | 500 |
| 1 | 2019-03-01 | 2019-03-22 | 20 | 2019-03-01 | 15 | 300 |
| 2 | 2019-02-01 | 2019-02-20 | 15 | 2019-02-10 | 200 | 3000 |
| 2 | 2019-02-21 | 2019-03-31 | 30 | 2019-03-22 | 30 | 900 |

Product 1: (500 + 300) / (100 + 15) = 6.96. Product 2: (3000 + 900) / (200 + 30) = 16.96.

**The no-sales case.** The example doesn't include one, so here's a small dataset where product 3 never sold. Without `IFNULL`, its average is `NULL`:

| `product_id` | `average_price` |
|---|---|
| 1 | 5.00 |
| 3 | `NULL` |

Move the date test into `WHERE`, and product 3 disappears entirely — its `NULL` purchase date fails `BETWEEN`:

| `product_id` | `average_price` |
|---|---|
| 1 | 5.00 |

With the date test in `ON` and `IFNULL` around the result:

| `product_id` | `average_price` |
|---|---|
| 1 | 5.00 |
| 3 | 0.00 |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(p · s) worst case</summary>

The join condition is a range, not an equality, so MySQL can hash only on `product_id` and then test the date range for each candidate pair. For one product with p price periods and s sales, that's **O(p · s)** comparisons. Grouping afterwards is linear.

With an index on `UnitsSold (product_id, purchase_date)`, each price period becomes an index range scan.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(s)</summary>

**O(s)** for the join's hash table, plus one running sum per product.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each sale needs the price in effect on its date, so I join on product and `purchase_date BETWEEN start_date AND end_date`. The average selling price is weighted, so it's total revenue over total units. It's a left join from `Prices` with the date range in `ON`, so unsold products survive, and `IFNULL` turns their `NULL` average into 0."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `AVG(price)`?" | It weights every price period equally, regardless of how many units sold at that price. |
| "What if periods could overlap?" | A sale would match two price rows and be counted twice. You'd need a rule — latest start date wins — and a ranking to apply it. |
| "Products that appear only in `UnitsSold`?" | Driving from `Prices` drops them. Here every sold product has prices; otherwise, drive from a list of all products. |
| "Total revenue per product?" | Just `SUM(u.units * p.price)`. |

**Traps:**

- **`AVG(price)`** — the unweighted average.
- **Date range in `WHERE`** — turns the left join into an inner join and loses unsold products.
- **No `IFNULL`** — unsold products show `NULL` instead of 0.
- **Joining on `product_id` only** — every sale gets every price.

**This same move shows up in:** [Product Price at a Given Date](1164-product-price-at-a-given-date.md) (which price was in effect on a date) · [Employee Bonus](577-employee-bonus.md) (`ON` vs `WHERE` in a left join) · [Confirmation Rate](1934-confirmation-rate.md) (turning a missing group's `NULL` into 0).

</details>

---
