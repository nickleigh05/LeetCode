# CTEs (`WITH`)

```sql
-- Orders
-- id  customer  amount
-- 1   Ann       30
-- 2   Ann       20
-- 3   Bob       50
-- 4   Cat       10

WITH totals AS (
    SELECT customer, SUM(amount) AS total
    FROM Orders
    GROUP BY customer
),
best AS (
    SELECT MAX(total) AS top FROM totals
)
SELECT t.customer, t.total
FROM totals t
JOIN best b ON t.total = b.top;
-- customer  total
-- Ann       50
-- Bob       50
```

`WITH name AS (query)` names a subquery up front, and the main query — plus every later CTE — can then use the name like a table. Several CTEs share one `WITH`, separated by commas, and each can read the ones defined before it. A CTE can be referenced more than once: `totals` is used twice above.

That makes CTEs the cleanest way to write a multi-step query: one named step per idea (aggregate, then rank, then filter) instead of derived tables nested inside each other. A CTE exists only for the statement it's attached to. Available in MySQL 8.0 and later.

**Related:** [derived-tables](derived-tables.md) · [recursive-cte](recursive-cte.md) · [window-functions](window-functions.md) · [top-n-per-group](top-n-per-group.md) · [execution-order](execution-order.md)
