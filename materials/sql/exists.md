# `EXISTS`

```sql
-- Customers        Orders
-- id  name         id  customer_id  amount
-- 1   Ann          10  1            30
-- 2   Bob          11  1            90
-- 3   Cat          12  3            15

SELECT name FROM Customers c
WHERE EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.id AND o.amount > 50);
-- name
-- Ann

SELECT name FROM Customers c
WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.id);
-- name
-- Bob

SELECT c.name FROM Customers c JOIN Orders o ON o.customer_id = c.id;
-- name
-- Ann
-- Ann        ← a JOIN repeats Ann once per order; EXISTS lists her once
-- Cat
```

`EXISTS (subquery)` is true when the subquery returns at least one row; what it selects doesn't matter (`SELECT 1` is the convention). It's almost always **correlated** — the inner `WHERE` refers to the outer row (`o.customer_id = c.id`) — so read it as "for this customer, is there any order such that…".

`EXISTS` never duplicates outer rows the way a `JOIN` does, and `NOT EXISTS` is the NULL-safe anti-join, immune to the `NOT IN` trap.

**Related:** [anti-join](anti-join.md) · [in-subquery](in-subquery.md) · [correlated-subquery](correlated-subquery.md) · [joins-overview](joins-overview.md)
