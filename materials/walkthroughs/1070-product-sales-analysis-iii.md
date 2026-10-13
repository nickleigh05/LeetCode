# 1070. Product Sales Analysis III

**Medium** · [LeetCode](https://leetcode.com/problems/product-sales-analysis-iii/) · [Solution file (no hints)](../../problems/1000-1499/1070.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each product, find the earliest year it sold, and return **every** sale from that year: `product_id`, `first_year`, `quantity`, `price`. Any order.

```
Table: Sales
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) is the primary key (combination of columns with unique values) of this table.
Each row records a sale of a product in a given year.
A product may have multiple sales entries in the same year.
Note that the per-unit price.
```

```
Input:
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Output:
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the "rows that match a per-group extreme" pattern. The minimum year is one value per product; the answer is the **rows** that have it — possibly several.

| The statement says | Which really means |
|---|---|
| "identify the earliest year" for each product | `MIN(year)` per `product_id` |
| "return **all** sales entries for that product in that year" | Not one row per product — every sale in that year |
| "A product may have multiple sales entries in the same year" | The example doesn't show it, but hidden tests do |
| output column `first_year` | Rename `year` |

The statement spells this out because the most common wrong answer collapses each product to one row.

🤔 **Before you open the next section:** if product 100 had two sales in 2008, how many output rows should it have?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Tuple `IN` a grouped subquery** | `WHERE (product_id, year) IN (SELECT product_id, MIN(year) … GROUP BY product_id)` | ✅ Keeps every row from each product's first year |
| `RANK()` window | `RANK() OVER (PARTITION BY product_id ORDER BY year)`, keep rank 1 | ✅ Ties share rank 1, so all first-year rows survive |
| Join to the grouped subquery | `JOIN (SELECT product_id, MIN(year) AS y …) f ON …` | ✅ Same rows |
| `GROUP BY product_id` with `MIN(year)` | `SELECT product_id, MIN(year), quantity, price … GROUP BY product_id` | ❌ One row per product — and MySQL rejects it |
| `ROW_NUMBER()` = 1 | instead of `RANK()` | ❌ Keeps only one of the first-year sales |

**The decision: the tuple `IN`.** Find the first year per product, then keep every sale that matches it.

**Why grouping fails.** `quantity` and `price` aren't aggregated, so `ONLY_FULL_GROUP_BY` rejects the query outright. Forcing it with `ANY_VALUE` returns one arbitrary sale per product. With two 2008 sales for product 100:

| `product_id` | `first_year` | `quantity` | `price` |
|---|---|---|---|
| 100 | 2008 | 10 | 5000 |
| 200 | 2011 | 15 | 9000 |

The second 2008 sale is gone. The `IN` version keeps both:

| `product_id` | `first_year` | `quantity` | `price` |
|---|---|---|---|
| 100 | 2008 | 10 | 5000 |
| 100 | 2008 | 3 | 4500 |
| 200 | 2011 | 15 | 9000 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT product_id, year AS first_year, quantity, price
```

→ [aliases](../sql/aliases.md)

```sql
FROM Sales
```

```sql
WHERE (product_id, year) IN (
    SELECT product_id, MIN(year)
    FROM Sales
    GROUP BY product_id
);
```

**Keep a sale if (its product, its year) is a (product, first year) pair.** The subquery produces one pair per product:

| `product_id` | `MIN(year)` |
|---|---|
| 100 | 2008 |
| 200 | 2011 |

The row constructor `(product_id, year)` compares two columns at once against those pairs.
→ [in-subquery](../sql/in-subquery.md) · [first-row-per-group](../sql/first-row-per-group.md) · [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT product_id, year AS first_year, quantity, price
FROM Sales
WHERE (product_id, year) IN (
    SELECT product_id, MIN(year)
    FROM Sales
    GROUP BY product_id
);
```

</details>

**Trace it** — on the example, product 100's first year is 2008 (sale 1) and product 200's is 2011 (sale 7). Sale 2 (2009) isn't from a first year.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass to compute each product's minimum year, one pass to test each sale against the hashed set of pairs.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(p)</summary>

**O(p)** for the p (product, first year) pairs.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First I find each product's earliest year with a grouped subquery. Then I return every sale whose (product, year) is in that set — so multiple sales in the first year all come back. Grouping the outer query would collapse them to one row."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "With a window function?" | `RANK() OVER (PARTITION BY product_id ORDER BY year)` and keep rank 1. `RANK`, not `ROW_NUMBER`, because ties must all survive. |
| "Each product's **latest** year?" | `MAX(year)` instead of `MIN`. |
| "Total quantity in the first year?" | Group the result: `SUM(quantity)` per product. |
| "Why does MySQL reject `GROUP BY product_id` with `quantity`?" | `ONLY_FULL_GROUP_BY`: a product has several quantities, and MySQL won't pick one silently. |

**Traps:**

- **Grouping the outer query** — returns one row per product, not every first-year sale.
- **`ROW_NUMBER() = 1`** — drops ties.
- **Matching on `year` alone** — `WHERE year IN (SELECT MIN(year) …)` mixes products.

**This same move shows up in:** [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (each customer's first order) · [Department Highest Salary](184-department-highest-salary.md) (all rows tied for a per-group maximum) · [Product Sales Analysis I](1068-product-sales-analysis-i.md) (same table, simpler question).

</details>

---
