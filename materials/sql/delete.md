# `DELETE`

```sql
-- Tags
-- id  tag
-- 1   sql
-- 2   python
-- 3   sql
-- 4   sql

DELETE FROM Tags WHERE tag = 'python';
SELECT id, tag FROM Tags;
-- id  tag
-- 1   sql
-- 3   sql
-- 4   sql
```

```sql
DELETE t1 FROM Tags t1
JOIN Tags t2 ON t1.tag = t2.tag AND t1.id > t2.id;    -- every row that has a same-tag row with a smaller id
SELECT id, tag FROM Tags;
-- id  tag
-- 1   sql
-- 2   python
```

```sql
DELETE FROM Tags WHERE id NOT IN (SELECT MIN(id) FROM Tags GROUP BY tag);
-- ERROR 1093: You can't specify target table 'Tags' for update in FROM clause

DELETE FROM Tags
WHERE id NOT IN (SELECT keep_id FROM (SELECT MIN(id) AS keep_id FROM Tags GROUP BY tag) AS k);
SELECT id, tag FROM Tags;
-- id  tag
-- 1   sql
-- 2   python
```

`DELETE FROM t WHERE cond` removes the matching rows; without a `WHERE` it empties the table. MySQL's multi-table form `DELETE t1 FROM t1 JOIN t2 …` deletes rows of `t1` based on a join — for example, every row that has a duplicate with a smaller id, which keeps the first row of each group.

MySQL refuses a subquery that reads the table being deleted from (error 1093). Wrapping that subquery in a derived table works, because MySQL builds the derived table first. LeetCode's `DELETE` problems check the table's final contents, not a result set.

**Related:** [update](update.md) · [self-join](self-join.md) · [non-equi-join](non-equi-join.md) · [derived-tables](derived-tables.md)
