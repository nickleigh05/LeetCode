# 1068. Product Sales Analysis I

**Easy** · [LeetCode](https://leetcode.com/problems/product-sales-analysis-i/) · [Solution file (no hints)](../../problems/1000-1499/1068.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For every sale, report the product's name, the year, and the price. Any order.

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
product_id is a foreign key (reference column) to Product table.
Each row of this table shows a sale on the product product_id in a certain year.
Note that the price is per unit.

Table: Product
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the product name of each product.
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
Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
Output:
+--------------+-------+-------+
| product_name | year  | price |
+--------------+-------+-------+
| Nokia        | 2008  | 5000  |
| Nokia        | 2009  | 5000  |
| Apple        | 2011  | 9000  |
+--------------+-------+-------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `product_id` is a foreign key to `Product` | Every sale points at an existing product — you can follow that pointer with a join |
| "for each `sale_id` in the Sales table" | One output row per sale — the sales table drives the result |
| `product_name` lives in `Product` | You need the second table only to turn an id into a name |
| "`product_name`, `year`, and `price`" | Three columns in that order; `quantity` isn't asked for |
| Samsung (300) has no sales | It shouldn't appear — nobody asked about products, only sales |

Because the foreign key guarantees every sale has a product, the "keep unmatched rows" question from [Replace Employee ID With The Unique Identifier](1378-replace-employee-id-with-the-unique-identifier.md) doesn't come up. A plain join is enough.

🤔 **Before you open the next section:** Samsung has no sales. Should it be in the output — and which join type keeps it out?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`JOIN … ON`** | `FROM Sales s JOIN Product p ON s.product_id = p.product_id` | ✅ The standard way to follow a foreign key |
| Comma join | `FROM Sales s, Product p WHERE s.product_id = p.product_id` | ✅ Same result; older style. Forget the `WHERE` and you get every pairing |
| Scalar subquery per row | `SELECT (SELECT product_name FROM Product p WHERE …) …` | ✅ Works, but hides the join |
| `LEFT JOIN` from `Product` | `FROM Product p LEFT JOIN Sales s …` | ❌ Adds a Samsung row with `NULL` year and price |

**The decision: an inner `JOIN`.** Every sale has exactly one product, so each sale produces exactly one output row.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT p.product_name, s.year, s.price
```

**Name from one table, year and price from the other.** Prefixing every column with its table alias makes the source of each value obvious.
→ [aliases](../sql/aliases.md)

```sql
FROM Sales s
```

```sql
JOIN Product p
    ON s.product_id = p.product_id;
```

**Follow the foreign key.** For each sale, find the product row with the same `product_id`. `JOIN` on its own means `INNER JOIN`: only pairs that match are kept.
→ [inner-join](../sql/inner-join.md) · [joins-overview](../sql/joins-overview.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT p.product_name, s.year, s.price
FROM Sales s
JOIN Product p
    ON s.product_id = p.product_id;
```

</details>

**Trace it** — each sale with the product row it matched:

| `sale_id` | `s.product_id` | `p.product_id` | `product_name` | `year` | `price` |
|---|---|---|---|---|---|
| 1 | 100 | 100 | Nokia | 2008 | 5000 |
| 2 | 100 | 100 | Nokia | 2009 | 5000 |
| 7 | 200 | 200 | Apple | 2011 | 9000 |

The two `product_id` columns always agree — that's the `ON` condition. Samsung never matches a sale, so it never appears.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)** for n sales and m products — a hash join builds a table on `Product.product_id` and probes it once per sale. With an index on `Product.product_id` (normal for a primary key), it's O(n log m) index lookups.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** for the hash table over products, plus the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each sale references a product, and I need the product's name, so I join `Sales` to `Product` on `product_id`. Every sale has a product, so an inner join returns exactly one row per sale."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Total quantity sold per product?" | `GROUP BY p.product_id, p.product_name` with `SUM(s.quantity)`. |
| "Include products that never sold." | Drive from `Product`: `Product p LEFT JOIN Sales s …`, and those rows get `NULL` sale columns. |
| "Revenue per sale?" | `s.quantity * s.price` — the price is per unit. |
| "What if a sale's `product_id` had no product?" | The inner join would silently drop it. A `LEFT JOIN` from `Sales` would keep it with a `NULL` name. |
| "Each product's first year of sales?" | That's [Product Sales Analysis III](1070-product-sales-analysis-iii.md). |

**Traps:**

- **A comma join without `WHERE`** — returns every sale paired with every product.
- **Driving from `Product` with an outer join** — adds unsold products.
- **Ambiguous `product_id`** — both tables have it; qualify it.

**This same move shows up in:** [Replace Employee ID With The Unique Identifier](1378-replace-employee-id-with-the-unique-identifier.md) (when unmatched rows must stay) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (same tables, harder question) · [Average Selling Price](1251-average-selling-price.md) (a join with a range condition).

</details>

---
