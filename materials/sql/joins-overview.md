# Joins Overview

| Join | Keeps | Typical question |
|---|---|---|
| [`INNER JOIN`](inner-join.md) | only the pairs that match | "each order with its customer's name" |
| [`LEFT JOIN`](left-join.md) | every left row, with `NULL`s where nothing matched | "every customer with their order count, 0 if none" |
| [`RIGHT` / `FULL OUTER JOIN`](right-full-outer-join.md) | every right row / every row of both | rarely needed; MySQL has no `FULL OUTER` |
| [`CROSS JOIN`](cross-join.md) | every combination | "every store × every product" |
| [self-join](self-join.md) | a table paired with itself | "employees who earn more than their manager" |
| [anti-join](anti-join.md) | left rows with no match | "customers who never ordered" |
| [non-equi join](non-equi-join.md) | pairs matched by a range or an inequality | "which tier does each score fall in?" |

```sql
-- Customers            Orders
-- id  name  credit     id  customer_id  amount
-- 1   Ann   100        10  1            30
-- 2   Bob   50         11  1            20
--                      12  9            70

SELECT c.name, o.amount
FROM Customers c
JOIN Orders o ON o.customer_id = c.id;
-- name  amount
-- Ann   30
-- Ann   20      ← one Ann row per matching order; Bob and order 12 have no partner

SELECT SUM(c.credit) AS total_credit
FROM Customers c
JOIN Orders o ON o.customer_id = c.id;
-- total_credit
-- 200           ← Ann's 100 is counted once per order
```

A join builds rows by pairing each row of the left table with every row of the right table for which the `ON` condition is true. A row with k matches appears k times, so **joins multiply rows**, and anything summed after a one-to-many join counts the "one" side once per match. Aggregate the many side first (in a subquery or CTE), then join.

Give each table a short alias, qualify every column (`c.name`, `o.amount`), and put the matching condition in `ON`. Rows without a partner disappear in an inner join; the outer joins keep them, and [on-vs-where](on-vs-where.md) covers where a filter belongs when they do.

**Related:** [inner-join](inner-join.md) · [left-join](left-join.md) · [on-vs-where](on-vs-where.md) · [aliases](aliases.md) · [execution-order](execution-order.md)
