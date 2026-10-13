# `IFNULL`, `COALESCE` & `NULLIF`

```sql
-- Employee
-- id  name  bonus
-- 1   Ann   500
-- 2   Bob   NULL

SELECT name, IFNULL(bonus, 0) AS bonus FROM Employee;
-- name  bonus
-- Ann   500
-- Bob   0

SELECT COALESCE(NULL, NULL, 'third', 'fourth');   -- → third    ← the first non-NULL argument
SELECT NULLIF(5, 5), NULLIF(5, 3);                -- → NULL  5
SELECT 10 / NULLIF(0, 0);                         -- → NULL     ← guards a division by zero
```

`IFNULL(x, fallback)` returns `x`, or `fallback` when `x` is `NULL`. It's the standard way to turn "no data" into 0 after a `LEFT JOIN` or an aggregate over nothing: `IFNULL(SUM(amount), 0)`. `COALESCE(a, b, c, …)` returns its first non-`NULL` argument and is the portable spelling (`IFNULL` is MySQL-only).

`NULLIF(a, b)` works the other way round: it returns `NULL` when `a = b`, otherwise `a`. Wrap a denominator in it so that a zero becomes `NULL` instead of an error. MySQL already returns `NULL` for `x / 0`, but Postgres and SQL Server raise an error.

**Related:** [null-is-null](null-is-null.md) · [left-join](left-join.md) · [aggregate-functions](aggregate-functions.md) · [ratios-percentages](ratios-percentages.md)
