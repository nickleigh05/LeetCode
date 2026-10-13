# `GROUP BY`

```sql
-- Employee
-- id  name  dept   salary
-- 1   Ann   eng    90000
-- 2   Bob   eng    70000
-- 3   Cat   sales  50000
-- 4   Dan   sales  60000
-- 5   Eve   hr     55000

SELECT dept, COUNT(*) AS headcount, MAX(salary) AS top_salary
FROM Employee
GROUP BY dept;
-- dept   headcount  top_salary
-- eng    2          90000
-- sales  2          60000
-- hr     1          55000

SELECT dept, salary >= 60000 AS well_paid, COUNT(*) AS n
FROM Employee
GROUP BY dept, well_paid
ORDER BY dept, well_paid;
-- dept   well_paid  n
-- eng    1          2
-- hr     0          1
-- sales  0          1
-- sales  1          1

SELECT dept, name, MAX(salary) FROM Employee GROUP BY dept;
-- ERROR 1055: Expression #2 of SELECT list is not in GROUP BY clause    ← which name? the group has several
```

`GROUP BY` splits rows into groups that share the same values in the listed columns, then `SELECT` produces **one row per group**. Group by several columns (or expressions) for one row per combination; `NULL`s form a group of their own.

Every `SELECT` item must be a grouping column or an aggregate. MySQL 8's `ONLY_FULL_GROUP_BY` mode rejects anything else — the last query asks for "the name" of a group that has two. Columns that the grouping columns fully determine are allowed, like any column of a table you grouped by its primary key. Getting the whole row behind each group's maximum (the name of each department's top earner) is a different problem — see [first-row-per-group](first-row-per-group.md) and [top-n-per-group](top-n-per-group.md).

**Related:** [aggregate-functions](aggregate-functions.md) · [having](having.md) · [count](count.md) · [first-row-per-group](first-row-per-group.md) · [window-aggregates](window-aggregates.md)
