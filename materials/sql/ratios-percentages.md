# Ratios & Percentages

```sql
-- Users    Emails
-- id       user_id  opened
-- 1        1        1
-- 2        1        0
-- 3        2        0

SELECT u.id,
       ROUND(IFNULL(AVG(e.opened), 0), 2) AS open_rate,
       ROUND(100 * IFNULL(SUM(e.opened), 0) / (SELECT COUNT(*) FROM Emails), 2) AS pct_of_all_opens
FROM Users u
LEFT JOIN Emails e ON e.user_id = u.id
GROUP BY u.id;
-- id  open_rate  pct_of_all_opens
-- 1   0.50       33.33
-- 2   0.00       0.00
-- 3   0.00       0.00            ← no emails: AVG is NULL, so IFNULL supplies the 0

SELECT ROUND(100 * 1 / 3, 2), ROUND(1 / 3, 2) * 100;    -- → 33.33  33.00    ← scale first, round last
```

A rate is part ÷ whole. In MySQL, **`AVG(condition)` is the share of rows where the condition holds**; `SUM(condition) / COUNT(*)` is the same thing written out. When the denominator comes from somewhere else (all rows, another table), get it from a [scalar subquery](scalar-subquery.md).

Scale first and round last: `ROUND(100 * part / whole, 2)`, because rounding before multiplying throws digits away. Groups with no rows after a `LEFT JOIN` produce `NULL`, so wrap them in `IFNULL(…, 0)` when the expected answer is 0. Division by zero gives `NULL` in MySQL. In Postgres and SQL Server, integer ÷ integer truncates (`1 / 3 = 0`), so multiply by `100.0` or `CAST` first there.

**Related:** [conditional-aggregation](conditional-aggregation.md) · [math-functions](math-functions.md) · [scalar-subquery](scalar-subquery.md) · [ifnull-coalesce](ifnull-coalesce.md) · [arithmetic-operators](arithmetic-operators.md)
