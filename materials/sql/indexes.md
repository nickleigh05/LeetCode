# Indexes & `EXPLAIN`

```sql
-- Orders
-- id  customer_id  order_date
-- 1   7            2024-01-05
-- 2   9            2024-01-06
-- 3   7            2024-02-11

CREATE INDEX idx_customer_date ON Orders (customer_id, order_date);
EXPLAIN SELECT * FROM Orders WHERE customer_id = 7 AND order_date >= '2024-02-01';

SELECT id FROM Orders WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';   -- can use an index on order_date
-- id
-- 1
-- 2

SELECT id FROM Orders WHERE YEAR(order_date) = 2024 AND MONTH(order_date) = 1;          -- same rows, but can't
-- id
-- 1
-- 2
```

An **index** is a sorted copy of one or more columns (a B-tree) with pointers back to the rows. It lets the engine find matching rows in O(log n) instead of scanning the whole table. Primary keys are indexed automatically. Indexes speed up reads, but every `INSERT`/`UPDATE`/`DELETE` has to maintain them, and they take space.

A composite index on `(customer_id, order_date)` follows the **leftmost-prefix rule**: it serves `customer_id = ?` and `customer_id = ? AND order_date > ?`, but not `order_date > ?` alone. Wrapping an indexed column in a function (`YEAR(order_date)`) hides it from the index, so write ranges on the raw column instead. `EXPLAIN` shows the plan: `type = ALL` means a full table scan, and `key` names the index used.

In an interview, "how would you make this faster?" usually means: index the columns in `WHERE`, `JOIN … ON` and `ORDER BY`, keep the filters index-friendly, and check with `EXPLAIN`. For the theory, see [Databases from First Principles](../system-design/00d-databases-101.md).

**Related:** [create-table-insert](create-table-insert.md) · [where](where.md) · [date-parts-format](date-parts-format.md) · [joins-overview](joins-overview.md)
