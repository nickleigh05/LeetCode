# `IF()`

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   45000
-- 3   Cat   60000

SELECT IF(5 > 3, 'yes', 'no');    -- → yes
SELECT name, IF(salary >= 60000, 'senior', 'junior') AS level FROM Employee;
-- name  level
-- Ann   senior
-- Bob   junior
-- Cat   senior

SELECT SUM(IF(salary >= 60000, 1, 0)) AS seniors,
       SUM(IF(salary >= 60000, salary, 0)) AS senior_payroll
FROM Employee;
-- seniors  senior_payroll
-- 2        150000
```

`IF(condition, then, else)` is MySQL shorthand for `CASE WHEN condition THEN … ELSE … END`. It's compact for two-way choices, especially inside aggregates. It's MySQL-only (SQL Server's equivalent is `IIF`, and Postgres has neither), so write the `CASE` when portability matters.

Don't confuse it with `IFNULL(x, fallback)`, which only replaces `NULL`s, or with the `IF … THEN … END IF` statement used inside stored functions.

**Related:** [case-when](case-when.md) · [conditional-aggregation](conditional-aggregation.md) · [ifnull-coalesce](ifnull-coalesce.md)
