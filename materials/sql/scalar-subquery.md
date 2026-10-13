# Scalar Subqueries

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   60000
-- 3   Cat   75000

SELECT name FROM Employee WHERE salary > (SELECT AVG(salary) FROM Employee);
-- name
-- Ann

SELECT name, ROUND(100 * salary / (SELECT SUM(salary) FROM Employee), 1) AS pct_of_payroll
FROM Employee;
-- name  pct_of_payroll
-- Ann   40.0
-- Bob   26.7
-- Cat   33.3

SELECT (SELECT name FROM Employee WHERE salary > 100000) AS top_earner;
-- top_earner
-- NULL           ← no row → NULL, instead of an empty result

SELECT name FROM Employee WHERE salary = (SELECT salary FROM Employee);   -- → ERROR 1242    ← more than one row
```

A subquery in parentheses that returns one column and at most one row is a **single value**, and it can go anywhere a value can: compared against in `WHERE`, computed with in `SELECT` (the denominator of a percentage), or returned as the whole answer.

When it returns no rows, its value is `NULL`. That's the standard answer to "return `NULL` if there is no such value": wrap the query as `SELECT (…) AS name`. When it can return more than one row, that's an error — use `IN` for a list, or force a single row with an aggregate or `LIMIT 1`.

**Related:** [in-subquery](in-subquery.md) · [correlated-subquery](correlated-subquery.md) · [nth-highest-value](nth-highest-value.md) · [ratios-percentages](ratios-percentages.md) · [derived-tables](derived-tables.md)
