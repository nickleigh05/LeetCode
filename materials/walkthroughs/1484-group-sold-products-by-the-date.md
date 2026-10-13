# 1484. Group Sold Products By The Date

**Easy** · [LeetCode](https://leetcode.com/problems/group-sold-products-by-the-date/) · [Solution file (no hints)](../../problems/1000-1499/1484.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each date, report how many **different** products sold and their names — sorted alphabetically and joined with commas. Order by `sell_date`.

```
Table: Activities
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| sell_date   | date    |
| product     | varchar |
+-------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each row of this table contains the product name and the date it was sold in a market.
```

```
Input:
Activities table:
+------------+------------+
| sell_date  | product     |
+------------+------------+
| 2020-05-30 | Headphone  |
| 2020-06-01 | Pencil     |
| 2020-06-02 | Mask       |
| 2020-05-30 | Basketball |
| 2020-06-01 | Bible      |
| 2020-06-02 | Mask       |
| 2020-05-30 | T-Shirt    |
+------------+------------+
Output:
+------------+----------+------------------------------+
| sell_date  | num_sold | products                     |
+------------+----------+------------------------------+
| 2020-05-30 | 3        | Basketball,Headphone,T-shirt |
| 2020-06-01 | 2        | Bible,Pencil                 |
| 2020-06-02 | 1        | Mask                         |
+------------+----------+------------------------------+
```

The sample output prints `T-shirt`; the input — and the real judge — use `T-Shirt`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A grouped query where one of the aggregates **builds a string** out of the group's rows.

| The statement says | Which really means |
|---|---|
| "It may contain duplicates" | Mask sold twice on 06-02 — count it and list it once |
| "number of different products" | `COUNT(DISTINCT product)` |
| "their names … sorted lexicographically" | Join the distinct names, in alphabetical order, into one string |
| comma-separated, no spaces | `SEPARATOR ','` — which is also MySQL's default |
| "ordered by sell_date" | Checked |

🤔 **Before you open the next section:** `COUNT` turns a group into a number. Which aggregate turns a group into a comma-separated string?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`GROUP_CONCAT(DISTINCT … ORDER BY …)`** | `GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',')` | ✅ Dedupe, sort, and join in one aggregate |
| Dedupe first in a subquery | `SELECT DISTINCT sell_date, product` then group | ✅ Same result; `COUNT(*)` then counts distinct products |
| `GROUP_CONCAT(product)` | no `DISTINCT`, no `ORDER BY` | ❌ Duplicates and arbitrary order |
| `STRING_AGG` | | ❌ PostgreSQL / SQL Server; MySQL's is `GROUP_CONCAT` |

**The decision: `GROUP_CONCAT` with `DISTINCT` and `ORDER BY` inside it.**

Without them, names come out in whatever order the rows were read, with repeats:

| `sell_date` | `GROUP_CONCAT(product)` |
|---|---|
| 2020-05-30 | Headphone,Basketball,T-Shirt |
| 2020-06-01 | Pencil,Bible |
| 2020-06-02 | Mask,Mask |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT sell_date,
       COUNT(DISTINCT product) AS num_sold,
       GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') AS products
```

**Three columns per date.** `COUNT(DISTINCT product)` counts each product once. `GROUP_CONCAT` takes its own `DISTINCT`, its own `ORDER BY`, and a `SEPARATOR` — all inside the parentheses — and returns one string per group.
→ [group-concat](../sql/group-concat.md) · [count](../sql/count.md)

```sql
FROM Activities
```

```sql
GROUP BY sell_date
```

→ [group-by](../sql/group-by.md)

```sql
ORDER BY sell_date;
```

**Sort the output rows.** This `ORDER BY` sorts the dates; the one inside `GROUP_CONCAT` sorts the names within each string. They're independent.
→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT sell_date,
       COUNT(DISTINCT product) AS num_sold,
       GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') AS products
FROM Activities
GROUP BY sell_date
ORDER BY sell_date;
```

</details>

**Trace it** — 2020-05-30: Basketball, Headphone, T-Shirt → 3. 2020-06-01: Bible, Pencil → 2. 2020-06-02: Mask, sold twice, listed once → 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** — products are sorted within each group for `GROUP_CONCAT`, and the dates are sorted for the output.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the per-group sets and strings.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Group by date. Count distinct products, and build the list with `GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',')`, so duplicates are dropped and names are alphabetical. Then sort by date."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Is there a length limit?" | Yes — `group_concat_max_len`, 1024 bytes by default. Longer results are silently truncated; raise it with `SET SESSION group_concat_max_len = …`. |
| "Separate with `', '`?" | `SEPARATOR ', '`. |
| "The opposite — split a list into rows?" | Much harder in MySQL: a recursive CTE or `JSON_TABLE`. |
| "In PostgreSQL?" | `STRING_AGG(DISTINCT product, ',' ORDER BY product)`. |

**Traps:**

- **No `DISTINCT` inside `GROUP_CONCAT`** — Mask appears twice.
- **No `ORDER BY` inside `GROUP_CONCAT`** — names in arbitrary order.
- **Silent truncation** — fine here, a real risk on big groups.

**This same move shows up in:** [Number of Unique Subjects Taught by Each Teacher](2356-number-of-unique-subjects-taught-by-each-teacher.md) (`COUNT(DISTINCT …)`) · [Fix Names in a Table](1667-fix-names-in-a-table.md) (building strings) · [User Activity for the Past 30 Days I](1141-user-activity-for-the-past-30-days-i.md) (per-day aggregates).

</details>

---
