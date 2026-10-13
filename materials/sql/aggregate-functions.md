# Aggregate Functions

```sql
-- Orders
-- id  customer  amount
-- 1   Ann       30
-- 2   Ann       NULL
-- 3   Bob       50

SELECT COUNT(*), COUNT(amount), SUM(amount), AVG(amount), MIN(amount), MAX(amount) FROM Orders;
-- COUNT(*)  COUNT(amount)  SUM(amount)  AVG(amount)  MIN(amount)  MAX(amount)
-- 3         2              80           40.0000      30           50           ← AVG = 80 / 2: the NULL is skipped

SELECT COUNT(*), SUM(amount), MAX(amount) FROM Orders WHERE customer = 'Zed';
-- COUNT(*)  SUM(amount)  MAX(amount)
-- 0         NULL         NULL         ← no rows still gives one row: COUNT is 0, the rest are NULL

SELECT customer, SUM(amount) FROM Orders;
-- ERROR 1140: In aggregated query without GROUP BY, expression #1 of SELECT list contains nonaggregated column
```

An aggregate collapses many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. Without `GROUP BY`, the whole filtered table is one group, so the result is **exactly one row** — even when no rows matched, in which case `COUNT` is 0 and the others are `NULL`. That makes `SELECT MAX(x) …` a natural way to return `NULL` for "no answer".

All aggregates **skip `NULL`s**: `AVG(amount)` above is 80 / 2, not 80 / 3. `AVG` of integers returns a `DECIMAL`, and `MIN`/`MAX` work on strings and dates too. A plain column next to an aggregate needs a `GROUP BY` — the last query has no single "customer" to show.

**Related:** [count](count.md) · [group-by](group-by.md) · [having](having.md) · [ifnull-coalesce](ifnull-coalesce.md) · [window-aggregates](window-aggregates.md)
