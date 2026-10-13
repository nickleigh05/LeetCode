# `LEFT JOIN`

```sql
-- Customers        Orders
-- id  name         id  customer_id  amount
-- 1   Ann          10  1            30
-- 2   Bob          11  1            20
-- 3   Cat          12  3            50

SELECT c.name, o.amount
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id;
-- name  amount
-- Ann   30
-- Ann   20
-- Bob   NULL     ← no orders: kept, with NULL in every Orders column
-- Cat   50

SELECT c.name, COUNT(o.id) AS orders, IFNULL(SUM(o.amount), 0) AS total
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;
-- name  orders  total
-- Ann   2       50
-- Bob   0       0
-- Cat   1       50
```

`LEFT JOIN` keeps **every row of the left (first) table**. Where nothing on the right matches, the row still appears, with `NULL` in all of the right table's columns. Use it whenever the answer must include rows with zero matches — "every customer", "each student's count, including zero". `LEFT OUTER JOIN` means the same thing.

Three habits go with it. Count a right-table column (`COUNT(o.id)`, not `COUNT(*)`). Turn missing sums into 0 with `IFNULL`. And keep filters on the right table in the `ON` clause: a `WHERE` on a right-table column throws away the `NULL` rows and quietly turns the query back into an inner join — see [on-vs-where](on-vs-where.md).

**Related:** [on-vs-where](on-vs-where.md) · [anti-join](anti-join.md) · [count](count.md) · [ifnull-coalesce](ifnull-coalesce.md) · [joins-overview](joins-overview.md) · [cross-join](cross-join.md)
