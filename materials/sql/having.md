# `HAVING`

```sql
-- Employee
-- id  name  dept   salary
-- 1   Ann   eng    90000
-- 2   Bob   eng    70000
-- 3   Cat   sales  50000
-- 4   Dan   sales  60000
-- 5   Eve   hr     55000

SELECT dept, COUNT(*) AS headcount
FROM Employee
GROUP BY dept
HAVING COUNT(*) >= 2;
-- dept   headcount
-- eng    2
-- sales  2

SELECT dept, AVG(salary) AS avg_salary
FROM Employee
WHERE salary > 55000          -- rows first…
GROUP BY dept
HAVING AVG(salary) > 60000;   -- …then groups
-- dept  avg_salary
-- eng   80000.0000

SELECT dept FROM Employee WHERE COUNT(*) >= 2 GROUP BY dept;   -- → ERROR 1111    ← aggregates can't go in WHERE
```

`HAVING` filters **groups after aggregation**, the way `WHERE` filters rows before it, so conditions on aggregates go in `HAVING` and never in `WHERE`. Filter rows in `WHERE` whenever you can, since it shrinks the data before grouping, and keep `HAVING` for conditions that need the group.

`HAVING` can test aggregates that aren't in the `SELECT` list, and in MySQL it can use `SELECT` aliases (`HAVING headcount >= 2`). One idiom worth knowing: `HAVING COUNT(DISTINCT x) = (SELECT COUNT(*) FROM …)` keeps the groups that contain every one of something.

**Related:** [group-by](group-by.md) · [where](where.md) · [execution-order](execution-order.md) · [scalar-subquery](scalar-subquery.md) · [aggregate-functions](aggregate-functions.md)
