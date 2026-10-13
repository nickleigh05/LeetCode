# `GROUP_CONCAT`

```sql
-- Purchases
-- id  buyer  item
-- 1   Ann    pen
-- 2   Ann    ink
-- 3   Ann    pen
-- 4   Bob    desk

SELECT buyer,
       COUNT(DISTINCT item) AS n,
       GROUP_CONCAT(DISTINCT item ORDER BY item) AS items,
       GROUP_CONCAT(item ORDER BY id SEPARATOR ' | ') AS history
FROM Purchases
GROUP BY buyer;
-- buyer  n  items    history
-- Ann    2  ink,pen  pen | ink | pen
-- Bob    1  desk     desk

SELECT @@group_concat_max_len;    -- → 1024    ← longer results are silently truncated
```

`GROUP_CONCAT` joins a group's values into one string, comma-separated by default. `DISTINCT`, `ORDER BY` and `SEPARATOR` all go **inside** the parentheses. Without `ORDER BY` the values come out in an unspecified order, so always give one when the expected output lists them sorted.

The result is cut off at `group_concat_max_len` bytes (1024 by default) with only a warning; raise the limit with `SET SESSION group_concat_max_len = 100000` when the strings can get long. Other databases call it `STRING_AGG` (Postgres, SQL Server) or `LISTAGG` (Oracle).

**Related:** [group-by](group-by.md) · [string-functions](string-functions.md) · [distinct](distinct.md) · [order-by](order-by.md)
