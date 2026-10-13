# Derived Tables (subquery in `FROM`)

```sql
-- Orders
-- id  customer  amount
-- 1   Ann       30
-- 2   Ann       20
-- 3   Bob       50
-- 4   Cat       10

SELECT AVG(total) AS avg_customer_total
FROM (SELECT customer, SUM(amount) AS total FROM Orders GROUP BY customer) AS t;
-- avg_customer_total
-- 36.6667

SELECT AVG(total) FROM (SELECT customer, SUM(amount) AS total FROM Orders GROUP BY customer);
-- ERROR 1248: Every derived table must have its own alias

SELECT customer, amount
FROM (SELECT customer, amount,
             ROW_NUMBER() OVER (PARTITION BY customer ORDER BY amount DESC) AS rn
      FROM Orders) AS ranked
WHERE rn = 1;
-- customer  amount
-- Ann       30
-- Bob       50
-- Cat       10
```

A query in the `FROM` clause acts as a temporary table for the outer query. Use one to aggregate an aggregate (the average of per-customer totals), to filter on a window function's result (window functions can't go in `WHERE`), or to join against a grouped result. MySQL requires an **alias** after the closing parenthesis.

A [CTE](cte-with.md) does the same job with the subquery pulled up to the top, which reads better once queries nest more than one level deep.

**Related:** [cte-with](cte-with.md) · [window-functions](window-functions.md) · [group-by](group-by.md) · [scalar-subquery](scalar-subquery.md) · [top-n-per-group](top-n-per-group.md)
