# Correlated Subqueries

```sql
-- Employee
-- id  name  dept   salary
-- 1   Ann   eng    90000
-- 2   Bob   eng    70000
-- 3   Cat   sales  50000
-- 4   Dan   sales  60000

SELECT name, dept, salary
FROM Employee e
WHERE salary > (SELECT AVG(salary) FROM Employee WHERE dept = e.dept);
-- name  dept   salary
-- Ann   eng    90000
-- Dan   sales  60000

SELECT name, salary,
       (SELECT COUNT(DISTINCT e2.salary) FROM Employee e2 WHERE e2.salary > e.salary) + 1 AS salary_rank
FROM Employee e
ORDER BY salary_rank;
-- name  salary  salary_rank
-- Ann   90000   1
-- Bob   70000   2
-- Dan   60000   3
-- Cat   50000   4
```

A correlated subquery refers to a column of the outer query (`e.dept`), so it is logically re-run for every outer row: "compare each employee with the average of **their own** department". Unqualified names resolve to the innermost table that has them, so qualify the outer reference, and alias both copies when the same table appears inside and out.

Correlated subqueries can express per-group comparisons and rankings without window functions, but they cost up to one inner query per outer row. A window function, or a join against a grouped derived table, is usually faster and clearer.

**Related:** [scalar-subquery](scalar-subquery.md) · [exists](exists.md) · [window-aggregates](window-aggregates.md) · [ranking-functions](ranking-functions.md) · [derived-tables](derived-tables.md)
