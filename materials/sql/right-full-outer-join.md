# `RIGHT JOIN` & `FULL OUTER JOIN`

```sql
-- A     B
-- id    id
-- 1     2
-- 2     3

SELECT a.id AS a_id, b.id AS b_id FROM A a RIGHT JOIN B b ON a.id = b.id;
-- a_id  b_id
-- 2     2
-- NULL  3

SELECT a.id AS a_id, b.id AS b_id FROM A a FULL OUTER JOIN B b ON a.id = b.id;   -- → ERROR 1064    ← not in MySQL

SELECT a.id AS a_id, b.id AS b_id FROM A a LEFT JOIN B b ON a.id = b.id
UNION
SELECT a.id, b.id FROM A a RIGHT JOIN B b ON a.id = b.id;
-- a_id  b_id
-- 1     NULL
-- 2     2
-- NULL  3
```

`RIGHT JOIN` is a `LEFT JOIN` with the tables swapped: it keeps every row of the right table. Most people write every outer join as a `LEFT JOIN`, reordering the tables, so that queries read top-down.

`FULL OUTER JOIN` keeps the unmatched rows from both sides. MySQL doesn't support it, so emulate it with a `LEFT JOIN` `UNION` a `RIGHT JOIN` — `UNION` removes the matched rows that both halves produce. If the tables can hold fully identical rows that must all survive, use `UNION ALL` and add `WHERE a.id IS NULL` to the second half instead. Postgres and SQL Server support `FULL OUTER JOIN` directly.

**Related:** [left-join](left-join.md) · [union](union.md) · [joins-overview](joins-overview.md)
