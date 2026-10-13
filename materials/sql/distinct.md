# `DISTINCT`

```sql
-- Visits
-- id  user_id  page
-- 1   10       home
-- 2   10       home
-- 3   10       cart
-- 4   11       home
-- 5   12       NULL
-- 6   12       NULL

SELECT DISTINCT user_id FROM Visits;
-- user_id
-- 10
-- 11
-- 12

SELECT DISTINCT user_id, page FROM Visits;
-- user_id  page
-- 10       home
-- 10       cart
-- 11       home
-- 12       NULL      ← NULLs count as one value here

SELECT COUNT(DISTINCT page), COUNT(DISTINCT user_id, page) FROM Visits;   -- → 2  3
```

`DISTINCT` removes duplicate rows from the output. It applies to the **whole selected row**, not just the first column: `DISTINCT user_id, page` keeps each distinct pair. It runs after `SELECT`, so it also dedupes computed values, and it treats `NULL`s as equal to each other.

Inside an aggregate, `COUNT(DISTINCT x)` counts unique non-`NULL` values. `SELECT DISTINCT a, b` returns the same rows as `GROUP BY a, b` — switch to `GROUP BY` as soon as you need a count or a sum per group.

**Related:** [count](count.md) · [group-by](group-by.md) · [union](union.md) · [limit-offset](limit-offset.md)
