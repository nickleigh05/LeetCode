# 1158. Market Analysis I

**Medium** · [LeetCode](https://leetcode.com/problems/market-analysis-i/) · [Solution file (no hints)](../../problems/1000-1499/1158.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For **every** user, report their join date and how many orders they placed **as a buyer in 2019** — 0 if none. Any order.

```
Table: Users
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| join_date      | date    |
| favorite_brand | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) of this table.
This table has the info of the users of an online shopping website where users can sell and buy items.

Table: Orders
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| order_id      | int     |
| order_date    | date    |
| item_id       | int     |
| buyer_id      | int     |
| seller_id     | int     |
+---------------+---------+
order_id is the primary key (column with unique values) of this table.
item_id is a foreign key (reference column) to the Items table.
buyer_id and seller_id are foreign keys to the Users table.

Table: Items
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| item_id       | int     |
| item_brand    | varchar |
+---------------+---------+
item_id is the primary key (column with unique values) of this table.
```

```
Input:
Users table:
+---------+------------+----------------+
| user_id | join_date  | favorite_brand |
+---------+------------+----------------+
| 1       | 2018-01-01 | Lenovo         |
| 2       | 2018-02-09 | Samsung        |
| 3       | 2018-01-19 | LG             |
| 4       | 2018-05-21 | HP             |
+---------+------------+----------------+
Orders table:
+----------+------------+---------+----------+-----------+
| order_id | order_date | item_id | buyer_id | seller_id |
+----------+------------+---------+----------+-----------+
| 1        | 2019-08-01 | 4       | 1        | 2         |
| 2        | 2018-08-02 | 2       | 1        | 3         |
| 3        | 2019-08-03 | 3       | 2        | 3         |
| 4        | 2018-08-04 | 1       | 4        | 2         |
| 5        | 2018-08-04 | 1       | 3        | 4         |
| 6        | 2019-08-05 | 2       | 2        | 4         |
+----------+------------+---------+----------+-----------+
Items table:
+---------+------------+
| item_id | item_brand |
+---------+------------+
| 1       | Samsung    |
| 2       | Lenovo     |
| 3       | LG         |
| 4       | HP         |
+---------+------------+
Output:
+-----------+------------+----------------+
| buyer_id  | join_date  | orders_in_2019 |
+-----------+------------+----------------+
| 1         | 2018-01-01 | 1              |
| 2         | 2018-02-09 | 2              |
| 3         | 2018-01-19 | 0              |
| 4         | 2018-05-21 | 0              |
+-----------+------------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A left join, a count, and the `ON`-vs-`WHERE` decision — this problem exists to test exactly that decision.

| The statement says | Which really means |
|---|---|
| "for each user" | Every row of `Users` appears — users 3 and 4 have 0 |
| "orders they made **as a buyer**" | Match on `buyer_id`, not `seller_id` |
| "in 2019" | Only orders dated 2019 count |
| output column `buyer_id` | It's the user's id, renamed |
| `Items` | Not needed for this question |

🤔 **Before you open the next section:** if you `LEFT JOIN` orders and then add `WHERE order_date` is in 2019, what happens to a user with no 2019 orders?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT JOIN` with the year in `ON`** | `ON o.buyer_id = u.user_id AND o.order_date BETWEEN '2019-01-01' AND '2019-12-31'` | ✅ Users without 2019 orders keep a row with `NULL`s |
| Correlated count | `(SELECT COUNT(*) FROM Orders o WHERE o.buyer_id = u.user_id AND YEAR(o.order_date) = 2019)` | ✅ Clear, one subquery per user |
| Year filter in `WHERE` | `LEFT JOIN … WHERE o.order_date BETWEEN …` | ❌ Removes the `NULL` rows — users 3 and 4 vanish |
| `COUNT(*)` | | ❌ Counts the `NULL` row as 1 for users without orders |

**The decision: the date condition in `ON`.** In a left join, `ON` decides which orders attach to a user; `WHERE` decides which rows survive. "Users with zero orders" must survive.

With the filter in `WHERE`:

| `buyer_id` | `join_date` | `orders_in_2019` |
|---|---|---|
| 1 | 2018-01-01 | 1 |
| 2 | 2018-02-09 | 2 |

Users 3 and 4 are gone — their joined row had `NULL` dates, which fail the filter.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT u.user_id AS buyer_id, u.join_date, COUNT(o.order_id) AS orders_in_2019
```

**The user, and how many 2019 orders matched.** `COUNT(o.order_id)` counts only real matches; a user with none gets one row of `NULL`s, which counts as 0.
→ [count](../sql/count.md) · [aliases](../sql/aliases.md)

```sql
FROM Users u
```

```sql
LEFT JOIN Orders o
    ON  o.buyer_id = u.user_id
    AND o.order_date BETWEEN '2019-01-01' AND '2019-12-31'
```

**Attach each user's 2019 purchases — if any.** Both conditions are in `ON`: the order must be this user's purchase **and** dated 2019. Orders failing either simply don't attach; the user still appears.
→ [left-join](../sql/left-join.md) · [on-vs-where](../sql/on-vs-where.md) · [between](../sql/between.md)

```sql
GROUP BY u.user_id, u.join_date;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT u.user_id AS buyer_id, u.join_date, COUNT(o.order_id) AS orders_in_2019
FROM Users u
LEFT JOIN Orders o
    ON  o.buyer_id = u.user_id
    AND o.order_date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY u.user_id, u.join_date;
```

</details>

**Trace it** — the joined rows:

| `user_id` | `order_id` | `order_date` |
|---|---|---|
| 1 | 1 | 2019-08-01 |
| 2 | 6 | 2019-08-05 |
| 2 | 3 | 2019-08-03 |
| 3 | `NULL` | `NULL` |
| 4 | `NULL` | `NULL` |

User 1: one 2019 order. User 2: two. Users 3 and 4: a single `NULL` row each → 0.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(u + o)</summary>

**O(u + o)** — a hash join on `buyer_id`, the date test per matching order, and one grouping pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u + o)</summary>

**O(o)** for the hash table and **O(u)** for the counters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every user must appear, so I left-join their orders. The buyer match and the 2019 date range both go in `ON`, so orders outside 2019 just don't attach and users without any still keep a row. Then `COUNT(o.order_id)`, which is 0 for those users."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `YEAR(order_date) = 2019`?" | It works and reads well; the range form lets an index on `order_date` be used. |
| "Orders as a seller too?" | A second left join on `seller_id` — but two one-to-many joins multiply rows, so count `DISTINCT` order ids, or aggregate each side in a subquery first. |
| "Only users with at least one 2019 order?" | Then an inner join is right, or `HAVING COUNT(o.order_id) > 0`. |
| "Did the second item each user sold match their favourite brand?" | That's Market Analysis II — ranking each seller's sales by date. |

**Traps:**

- **Year filter in `WHERE`** — zero-order users disappear.
- **`COUNT(*)`** — zero-order users show 1.
- **`seller_id`** — the question is about buyers.

**This same move shows up in:** [Employee Bonus](577-employee-bonus.md) (`ON` vs `WHERE` in a left join) · [Students and Examinations](1280-students-and-examinations.md) (counts that must include zero) · [Average Selling Price](1251-average-selling-price.md) (a left join with an extra condition in `ON`).

</details>

---
