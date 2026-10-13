# `ON` vs `WHERE` in Outer Joins

```sql
-- Customers        Orders
-- id  name         id  customer_id  order_date
-- 1   Ann          10  1            2023-12-30
-- 2   Bob          11  1            2024-02-14
-- 3   Cat          12  2            2023-06-01

SELECT c.name, COUNT(o.id) AS orders_2024
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id AND YEAR(o.order_date) = 2024
GROUP BY c.id, c.name;
-- name  orders_2024
-- Ann   1
-- Bob   0
-- Cat   0

SELECT c.name, COUNT(o.id) AS orders_2024
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id
WHERE YEAR(o.order_date) = 2024
GROUP BY c.id, c.name;
-- name  orders_2024
-- Ann   1           ← Bob's only order is from 2023 and Cat's row has a NULL date, so WHERE drops both

SELECT c.name, COUNT(o.id) AS orders
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id AND c.name = 'Ann'
GROUP BY c.id, c.name;
-- name  orders
-- Ann   2
-- Bob   0           ← still listed: a left-table test in ON only blocks matches
-- Cat   0
```

For an `INNER JOIN`, a condition in `ON` and the same condition in `WHERE` give the same result. **For a `LEFT JOIN` they don't.** `ON` decides which right rows get attached, and a left row with no qualifying match is still kept, `NULL`-filled. `WHERE` runs after the join and filters the finished rows, so a test on a right-table column discards exactly the `NULL`-filled rows you meant to keep.

The rule: conditions on the **right** table go in `ON`; conditions on the **left** table go in `WHERE`. A left-table condition placed in `ON` doesn't filter left rows at all — it only stops them from matching.

**Related:** [left-join](left-join.md) · [where](where.md) · [execution-order](execution-order.md) · [count](count.md) · [anti-join](anti-join.md)
