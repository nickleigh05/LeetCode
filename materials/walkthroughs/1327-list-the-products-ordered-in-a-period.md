# 1327. List the Products Ordered in a Period

**Easy** · [LeetCode](https://leetcode.com/problems/list-the-products-ordered-in-a-period/) · [Solution file (no hints)](../../problems/1000-1499/1327.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find products with **at least 100 units** ordered in **February 2020**, with their total units. Any order.

```
Table: Products
+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| product_id       | int     |
| product_name     | varchar |
| product_category | varchar |
+------------------+---------+
product_id is the primary key (column with unique values) for this table.
This table contains data about the company's products.

Table: Orders
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| order_date    | date    |
| unit          | int     |
+---------------+---------+
This table may have duplicate rows.
product_id is a foreign key (reference column) to the Products table.
unit is the number of products ordered in order_date.
```

```
Input:
Products table:
+-------------+-----------------------+------------------+
| product_id  | product_name          | product_category |
+-------------+-----------------------+------------------+
| 1           | Leetcode Solutions    | Book             |
| 2           | Jewels of Stringology | Book             |
| 3           | HP                    | Laptop           |
| 4           | Lenovo                | Laptop           |
| 5           | Leetcode Kit          | T-shirt          |
+-------------+-----------------------+------------------+
Orders table:
+--------------+--------------+----------+
| product_id   | order_date   | unit     |
+--------------+--------------+----------+
| 1            | 2020-02-05   | 60       |
| 1            | 2020-02-10   | 70       |
| 2            | 2020-01-18   | 30       |
| 2            | 2020-02-11   | 80       |
| 3            | 2020-02-17   | 2        |
| 3            | 2020-02-24   | 3        |
| 4            | 2020-03-01   | 20       |
| 4            | 2020-03-04   | 30       |
| 4            | 2020-03-04   | 60       |
| 5            | 2020-02-25   | 50       |
| 5            | 2020-02-27   | 50       |
| 5            | 2020-03-01   | 50       |
+--------------+--------------+----------+
Output:
+--------------------+---------+
| product_name       | unit    |
+--------------------+---------+
| Leetcode Solutions | 130     |
| Leetcode Kit       | 100     |
+--------------------+---------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Filter rows by date, total per product, filter totals — the full `WHERE` → `GROUP BY` → `HAVING` pipeline, plus a join for the name.

| The statement says | Which really means |
|---|---|
| "ordered in February 2020" | Row filter on `order_date` — before grouping, in `WHERE` |
| "at least 100 units" | A condition on the **total** — after grouping, in `HAVING` |
| `unit` per order row; "may have duplicate rows" | Sum every row; duplicates are separate orders |
| "names of products" | Join `Products` for `product_name` |
| output column `unit` | The February total, aliased to `unit` |

Product 5 has 50 + 50 in February plus 50 on March 1 — only February counts: exactly 100, which qualifies.

🤔 **Before you open the next section:** which condition goes in `WHERE` and which in `HAVING` — and why can't they swap?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Join, `WHERE` dates, `GROUP BY`, `HAVING`** | half-open February range, `HAVING SUM(o.unit) >= 100` | ✅ Each clause does one job |
| Aggregate in a subquery, then join | group `Orders` first, join the qualifying ids to `Products` | ✅ Same result; joins fewer rows |
| `DATE_FORMAT(order_date, '%Y-%m') = '2020-02'` | | ✅ Correct, but wraps the column in a function, so an index can't help |
| Date filter in `HAVING` | | ❌ After grouping there's no single `order_date` to test |

**The decision: the straight pipeline.** Rows out (`WHERE`), group, groups out (`HAVING`).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT p.product_name, SUM(o.unit) AS unit
```

**Name and February total.**
→ [aggregate-functions](../sql/aggregate-functions.md) · [aliases](../sql/aliases.md)

```sql
FROM Orders o
```

```sql
JOIN Products p ON p.product_id = o.product_id
```

→ [inner-join](../sql/inner-join.md)

```sql
WHERE o.order_date >= '2020-02-01' AND o.order_date < '2020-03-01'
```

**Only February 2020.** The half-open range — on or after Feb 1, before Mar 1 — covers the whole month without naming its last day.
→ [where](../sql/where.md) · [date-arithmetic](../sql/date-arithmetic.md)

```sql
GROUP BY p.product_id, p.product_name
```

→ [group-by](../sql/group-by.md)

```sql
HAVING SUM(o.unit) >= 100;
```

**Only products whose February total reaches 100.**
→ [having](../sql/having.md) · [execution-order](../sql/execution-order.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT p.product_name, SUM(o.unit) AS unit
FROM Orders o
JOIN Products p ON p.product_id = o.product_id
WHERE o.order_date >= '2020-02-01' AND o.order_date < '2020-03-01'
GROUP BY p.product_id, p.product_name
HAVING SUM(o.unit) >= 100;
```

</details>

**Trace it** — February totals before `HAVING`:

| `product_name` | `February units` |
|---|---|
| Leetcode Solutions | 130 |
| Jewels of Stringology | 80 |
| HP | 5 |
| Leetcode Kit | 100 |

Leetcode Solutions (130) and Leetcode Kit (100) pass `>= 100`. Lenovo's orders are all in March, so it never reaches the grouping.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + p)</summary>

**O(n)** to filter and group n orders, plus a hash join on p products.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(p)</summary>

**O(p)** — one running total per product.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Join orders to products, keep February 2020 rows with a half-open date range in `WHERE`, group by product, and keep groups with `HAVING SUM(unit) >= 100`. The date test is per row, so it's `WHERE`; the 100-unit test is per group, so it's `HAVING`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `HAVING order_date …`?" | After grouping, a product has many dates; MySQL rejects a non-aggregated column there. |
| "Every month, not just February?" | `GROUP BY product_id, DATE_FORMAT(order_date, '%Y-%m')`. |
| "Top product in February?" | `ORDER BY SUM(o.unit) DESC LIMIT 1` — mind ties. |
| "Why is the range better than `MONTH(order_date) = 2`?" | `MONTH()` also matches February of other years — and functions on the column defeat indexes. |

**Traps:**

- **`BETWEEN '2020-02-01' AND '2020-02-28'`** — 2020 is a leap year; that misses Feb 29.
- **Summing before filtering by date** — March orders inflate the total.
- **`> 100`** — "at least" includes 100.

**This same move shows up in:** [Classes With at Least 5 Students](596-classes-with-at-least-5-students.md) (`HAVING` on an aggregate) · [Movie Rating](1341-movie-rating.md) (the same February filter) · [User Activity for the Past 30 Days I](1141-user-activity-for-the-past-30-days-i.md) (a date range in `WHERE`).

</details>

---
