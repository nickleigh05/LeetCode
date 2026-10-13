# `INTERSECT` & `EXCEPT`

```sql
-- Jan        Feb
-- user_id    user_id
-- 1          2
-- 2          3
-- 3          4

SELECT user_id FROM Jan INTERSECT SELECT user_id FROM Feb;   -- in both months
-- user_id
-- 2
-- 3

SELECT user_id FROM Jan EXCEPT SELECT user_id FROM Feb;      -- in January only
-- user_id
-- 1

SELECT user_id FROM Jan WHERE user_id IN (SELECT user_id FROM Feb);
-- user_id
-- 2
-- 3

SELECT user_id FROM Jan j WHERE NOT EXISTS (SELECT 1 FROM Feb f WHERE f.user_id = j.user_id);
-- user_id
-- 1
```

`INTERSECT` keeps the rows that appear in both results, and `EXCEPT` keeps the rows of the first result that don't appear in the second. Like `UNION`, both remove duplicates and match columns by position.

MySQL added them in 8.0.31. `IN` / `EXISTS` (for `INTERSECT`) and `NOT EXISTS` (for `EXCEPT`) express the same thing on any version and in any dialect — and unlike `NOT IN`, neither `EXCEPT` nor `NOT EXISTS` is thrown off by `NULL`s.

**Related:** [union](union.md) · [in-subquery](in-subquery.md) · [anti-join](anti-join.md) · [exists](exists.md)
