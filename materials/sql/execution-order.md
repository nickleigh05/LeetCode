# Execution Order

```text
1. FROM / JOIN … ON    build the row set
2. WHERE               keep rows where the condition is TRUE
3. GROUP BY            collapse rows into groups
4. HAVING              keep groups where the condition is TRUE
5. SELECT              compute the output columns — window functions run here
6. DISTINCT            drop duplicate output rows
7. ORDER BY            sort
8. LIMIT / OFFSET      cut
```

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   60000
-- 3   Cat   75000

SELECT name, salary * 12 AS yearly FROM Employee WHERE yearly > 800000;
-- ERROR 1054: Unknown column 'yearly' in 'where clause'    ← WHERE (step 2) runs before the alias exists (step 5)

SELECT name, salary * 12 AS yearly
FROM Employee
WHERE salary * 12 > 800000
ORDER BY yearly DESC;                                       -- ORDER BY (step 7) can see the alias
-- name  yearly
-- Ann   1080000
-- Cat   900000
```

SQL is written `SELECT`-first but runs `FROM`-first, and that order explains most "why doesn't this work?" moments. `WHERE` can't see `SELECT` aliases (they don't exist yet) or aggregates (groups don't exist yet — that's what `HAVING` is for). `ORDER BY` runs near the end, so it can use aliases and anything else. Window functions are computed at step 5, so filtering on one needs a CTE or derived table around the query.

MySQL relaxes one rule: `GROUP BY` and `HAVING` may reference `SELECT` aliases. `WHERE` never can. Building a query in the same order helps, too: get the `FROM`/`JOIN` rows right, then filter, then group, then shape the output.

**Related:** [where](where.md) · [having](having.md) · [aliases](aliases.md) · [group-by](group-by.md) · [window-functions](window-functions.md) · [cte-with](cte-with.md)
