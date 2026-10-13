# 1164. Product Price at a Given Date

**Medium** · [LeetCode](https://leetcode.com/problems/product-price-at-a-given-date/) · [Solution file (no hints)](../../problems/1000-1499/1164.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Every product starts at price **10**. Each row is a price change. Find every product's price **on 2019-08-16**. Any order.

```
Table: Products
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| new_price     | int     |
| change_date   | date    |
+---------------+---------+
(product_id, change_date) is the primary key (combination of columns with unique values) of this table.
Each row of this table indicates that the price of some product was changed to a new price at some date.
```

```
Input:
Products table:
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
| 2          | 65        | 2019-08-17  |
| 3          | 20        | 2019-08-18  |
+------------+-----------+-------------+
Output:
+------------+-------+
| product_id | price |
+------------+-------+
| 2          | 50    |
| 1          | 35    |
| 3          | 10    |
+------------+-------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The price on a date is the **latest change on or before** that date. Products with no change by then are still at the starting price, 10 — and there's no row that says so.

| The statement says | Which really means |
|---|---|
| "Initially, all products have price 10" | A default that isn't stored anywhere |
| each row: price changed to `new_price` on `change_date` | The price in effect on a date is the most recent change up to it |
| "on the date 2019-08-16" | Changes **on** that day count: `change_date <= '2019-08-16'` |
| product 1 changed on 08-14, 08-15, 08-16 | Its price on 08-16 is the 08-16 change: 35 |
| product 3's first change is 08-18 | Nothing yet by 08-16 → 10 |
| "all products" | Every product id in the table must appear |

Two groups of products, two different rules — that's a natural fit for a `UNION`.

🤔 **Before you open the next section:** how do you find, per product, the most recent change on or before 08-16 — and then the price from that row?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`UNION` of the two cases** | latest-change rows `UNION` products whose first change is after the date, at price 10 | ✅ Each rule is a small, separate query |
| Correlated subquery with a default | `IFNULL((SELECT new_price … ORDER BY change_date DESC LIMIT 1), 10)` per product | ✅ Compact; one lookup per product |
| Window ranking | `ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY change_date DESC)` on changes up to the date | ✅ Then add the never-changed products |
| `MAX(new_price)` | the highest price ever | ❌ Prices go down too — you want the latest, not the largest |
| Filter to `<= '2019-08-16'` only | | ❌ Product 3 disappears instead of showing 10 |

**The decision: the `UNION`.** Products that changed price by the date take their latest change; products that didn't take 10.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT product_id, new_price AS price
FROM Products
WHERE (product_id, change_date) IN (
    SELECT product_id, MAX(change_date)
    FROM Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id
)
```

**Case 1: the latest change up to the date.** The subquery finds each product's latest change date on or before 08-16:

| `product_id` | `latest change ≤ 08-16` |
|---|---|
| 1 | 2019-08-16 |
| 2 | 2019-08-14 |

The outer query keeps the row matching each (product, date) pair and reads its `new_price`. Two steps — find the date, then fetch that row — because `MAX(change_date)` alone can't tell you the price on that date.
→ [in-subquery](../sql/in-subquery.md) · [first-row-per-group](../sql/first-row-per-group.md)

```sql
UNION
```

**Stack the two result sets.** The cases can't overlap — a product either has a change by 08-16 or it doesn't — so `UNION ALL` would also be correct. `UNION` removes duplicates, which is harmless here.
→ [union](../sql/union.md)

```sql
SELECT product_id, 10 AS price
FROM Products
GROUP BY product_id
HAVING MIN(change_date) > '2019-08-16';
```

**Case 2: products with no change by the date.** If even the **earliest** change is after 08-16, nothing had changed yet, so the price is the default:

| `product_id` | `first change` |
|---|---|
| 3 | 2019-08-18 |

`10 AS price` is a constant column — every row of this half gets 10.
→ [having](../sql/having.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT product_id, new_price AS price
FROM Products
WHERE (product_id, change_date) IN (
    SELECT product_id, MAX(change_date)
    FROM Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id
)
UNION
SELECT product_id, 10 AS price
FROM Products
GROUP BY product_id
HAVING MIN(change_date) > '2019-08-16';
```

</details>

**Trace it** — case 1 gives product 1 → 35 (its 08-16 change) and product 2 → 50 (its 08-14 change; the 08-17 one is in the future). Case 2 gives product 3 → 10.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — each half is a grouping pass over n rows, plus a hashed membership test for case 1.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(p)</summary>

**O(p)** for p products in the groupings and the `UNION`'s duplicate check.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The price on a date is the latest change on or before it. For products with such a change, I find the max change date up to 08-16 per product and read the price from that row. Products whose first change is after 08-16 are still at the default, so a second query returns them with 10, and I `UNION` the two."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "One query, no `UNION`?" | Per distinct product: `IFNULL((SELECT new_price FROM Products q WHERE q.product_id = p.product_id AND q.change_date <= '2019-08-16' ORDER BY q.change_date DESC LIMIT 1), 10)`. |
| "Prices on **every** date?" | Generate a calendar, and for each (product, date) pick the latest change up to it — or use window functions over the change history. |
| "Why not `MAX(new_price)`?" | The latest price isn't necessarily the highest. |
| "`UNION` or `UNION ALL`?" | The halves are disjoint, so either is correct; `UNION ALL` skips the dedupe work. |

**Traps:**

- **`< '2019-08-16'`** — misses changes made on the day itself.
- **Dropping never-changed products** — the default 10 has to be produced explicitly.
- **`MAX(new_price)`** — prices can fall.

**This same move shows up in:** [Average Selling Price](1251-average-selling-price.md) (which price applied on a date) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (rows matching a per-group extreme) · [Count Salary Categories](1907-count-salary-categories.md) (a `UNION` that produces rows the data doesn't have).

</details>

---
