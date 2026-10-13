# `IN (subquery)`

```sql
-- Employee                     Department
-- id  name  dept_id  salary    id  name
-- 1   Ann   1        90000     1   Eng
-- 2   Bob   1        70000     2   Sales
-- 3   Cat   2        60000
-- 4   Dan   2        60000

SELECT name FROM Employee
WHERE dept_id IN (SELECT id FROM Department WHERE name = 'Eng');
-- name
-- Ann
-- Bob

SELECT name, dept_id, salary FROM Employee
WHERE (dept_id, salary) IN (SELECT dept_id, MAX(salary) FROM Employee GROUP BY dept_id);
-- name  dept_id  salary
-- Ann   1        90000
-- Cat   2        60000      ← ties both come back
-- Dan   2        60000

SELECT name FROM Employee WHERE salary > ALL (SELECT salary FROM Employee WHERE dept_id = 2);
-- name
-- Ann
-- Bob
```

`IN (SELECT …)` keeps the rows whose value appears anywhere in the subquery's one-column result. It's a **semi-join**: an outer row appears at most once no matter how many times it matches, where a `JOIN` would repeat it.

With a row constructor, `(a, b) IN (SELECT a, b …)` matches pairs. It's the classic way to fetch each group's max (or min) row: compute `(group, MAX(x))` in the subquery and keep the rows that match, ties included. `x > ALL (…)` means greater than every value the subquery returns, and `x = ANY (…)` is the same as `IN`. `NOT IN` is the negation, with a trap: one `NULL` in the subquery makes it return nothing (see [anti-join](anti-join.md)).

**Related:** [exists](exists.md) · [in-list](in-list.md) · [first-row-per-group](first-row-per-group.md) · [anti-join](anti-join.md) · [scalar-subquery](scalar-subquery.md)
