# `UPDATE`

```sql
-- Tasks
-- id  status  points
-- 1   open    3
-- 2   done    5
-- 3   open    2

UPDATE Tasks SET points = points * 2 WHERE status = 'open';
UPDATE Tasks SET status = CASE status WHEN 'open' THEN 'done' ELSE 'open' END;    -- flip every row at once
SELECT id, status, points FROM Tasks;
-- id  status  points
-- 1   done    6
-- 2   open    5
-- 3   done    4
```

```sql
-- Pairs
-- id  a  b
-- 1   1  2

UPDATE Pairs SET a = b, b = a;
SELECT a, b FROM Pairs;
-- a  b
-- 2  2       ← not a swap: MySQL applies assignments left to right
```

`UPDATE t SET col = expr, col2 = expr2 WHERE cond` changes the matching rows in place, and the right-hand side can use the row's current values (`points * 2`). Without a `WHERE`, every row changes. A `CASE` in `SET` applies a different change to each row in a single statement. MySQL also allows `UPDATE t1 JOIN t2 ON … SET t1.col = t2.col`.

**Trap:** MySQL evaluates multiple assignments left to right, and later ones see the new values, so `SET a = b, b = a` sets both columns to `b`. Standard SQL (and Postgres) would swap them.

**Related:** [case-when](case-when.md) · [delete](delete.md) · [create-table-insert](create-table-insert.md)
