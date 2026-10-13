# Window Functions

```sql
-- Employee
-- id  name  dept   salary
-- 1   Ann   eng    90000
-- 2   Bob   eng    70000
-- 3   Cat   sales  50000
-- 4   Dan   sales  60000

SELECT name, dept, salary,
       AVG(salary) OVER (PARTITION BY dept) AS dept_avg,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
FROM Employee;
-- name  dept   salary  dept_avg    rn
-- Ann   eng    90000   80000.0000  1
-- Bob   eng    70000   80000.0000  2
-- Dan   sales  60000   55000.0000  1
-- Cat   sales  50000   55000.0000  2

SELECT name FROM Employee WHERE ROW_NUMBER() OVER (ORDER BY salary DESC) = 1;
-- ERROR 3593: You cannot use the window function 'row_number' in this context.

WITH ranked AS (
    SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn FROM Employee
)
SELECT name FROM ranked WHERE rn = 1;
-- name
-- Ann
```

A window function computes a value for each row from a set of related rows — its **window** — without collapsing them the way `GROUP BY` does. Every input row stays and gains a column. `OVER (…)` defines the window:

- `PARTITION BY` splits the rows into independent groups, like `GROUP BY` but without merging them.
- `ORDER BY` orders the rows inside each partition. Ranking and `LAG`/`LEAD` need it, and it turns aggregates into running totals.
- An optional frame (`ROWS BETWEEN …`) narrows the window further — see [window-frames](window-frames.md).

Windows are computed after `WHERE`, `GROUP BY` and `HAVING`, so you **can't filter on them in `WHERE`**: compute them in a CTE or derived table, then filter outside. Available in MySQL 8.0+. Older solutions fake them with user variables (`@rank := @rank + 1`), which window functions replace.

**The families:** [ranking](ranking-functions.md) (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) · [offset](lag-lead.md) (`LAG`, `LEAD`) · [aggregates](window-aggregates.md) (`SUM`/`AVG`/`COUNT`/`MIN`/`MAX OVER`) · [value](first-last-value.md) (`FIRST_VALUE`, `LAST_VALUE`)

**Related:** [ranking-functions](ranking-functions.md) · [lag-lead](lag-lead.md) · [window-aggregates](window-aggregates.md) · [window-frames](window-frames.md) · [cte-with](cte-with.md) · [execution-order](execution-order.md)
