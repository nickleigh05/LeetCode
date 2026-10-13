# `CASE WHEN`

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   45000
-- 3   Cat   60000

SELECT name,
       CASE
           WHEN salary >= 80000 THEN 'high'
           WHEN salary >= 50000 THEN 'mid'
           ELSE 'low'
       END AS band
FROM Employee;
-- name  band
-- Ann   high
-- Bob   low
-- Cat   mid

SELECT name, CASE id WHEN 1 THEN 'first' WHEN 2 THEN 'second' END AS label FROM Employee;
-- name  label
-- Ann   first
-- Bob   second
-- Cat   NULL         ← no branch matched and there's no ELSE

SELECT name FROM Employee ORDER BY CASE WHEN salary < 50000 THEN 0 ELSE 1 END, name;
-- name
-- Bob
-- Ann
-- Cat
```

`CASE` is SQL's if / elif / else, and it's an **expression**: it produces a value, so it can go anywhere a value can — `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, inside `SUM()`, or in `UPDATE … SET`.

The searched form (`CASE WHEN condition THEN …`) checks the conditions top to bottom and returns the first match, so put the most specific branch first. The simple form (`CASE expr WHEN value THEN …`) compares one expression against a list of values. If nothing matches and there's no `ELSE`, the result is `NULL`. Keep every branch the same type, and finish with `END`.

**Related:** [if-function](if-function.md) · [conditional-aggregation](conditional-aggregation.md) · [update](update.md) · [pivot-unpivot](pivot-unpivot.md) · [order-by](order-by.md)
