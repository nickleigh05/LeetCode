# Top N per Group

```sql
-- Employee
-- id  name  dept   salary
-- 1   Ann   eng    90000
-- 2   Bob   eng    85000
-- 3   Cat   eng    85000
-- 4   Dan   eng    70000
-- 5   Eve   eng    60000
-- 6   Fay   sales  50000

WITH ranked AS (
    SELECT name, dept, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM Employee
)
SELECT dept, name, salary
FROM ranked
WHERE rnk <= 2
ORDER BY dept, salary DESC, name;
-- dept   name  salary
-- eng    Ann   90000
-- eng    Bob   85000      ← the top 2 distinct salaries, so the tie brings 3 people
-- eng    Cat   85000
-- sales  Fay   50000

SELECT e.dept, e.name, e.salary
FROM Employee e
WHERE (SELECT COUNT(DISTINCT e2.salary) FROM Employee e2
       WHERE e2.dept = e.dept AND e2.salary > e.salary) < 2
ORDER BY e.dept, e.salary DESC, e.name;
-- dept   name  salary
-- eng    Ann   90000
-- eng    Bob   85000
-- eng    Cat   85000
-- sales  Fay   50000
```

"The top N per group" means: rank within each partition, then filter. Rank in a CTE (window functions can't go in `WHERE`), then keep `rnk <= N` outside. The ranking function decides what ties mean:

- `DENSE_RANK` — the top N **distinct values**, with every tied row included. This is what "top three salaries" usually means.
- `RANK` — competition ranking, with gaps after ties.
- `ROW_NUMBER` — exactly N rows per group, ties broken arbitrarily unless you add a tie-breaker.

Without window functions, keep the rows that have fewer than N distinct higher values in the same group (a correlated subquery, the second query). For N = 1 — the max per group — the `(group, MAX(x)) IN (…)` form from [in-subquery](in-subquery.md) works too.

**Related:** [ranking-functions](ranking-functions.md) · [cte-with](cte-with.md) · [correlated-subquery](correlated-subquery.md) · [first-row-per-group](first-row-per-group.md) · [in-subquery](in-subquery.md)
