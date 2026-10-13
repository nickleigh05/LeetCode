# Nth Highest Value

```sql
-- Scores
-- id  points
-- 1   300
-- 2   200
-- 3   300
-- 4   100

SELECT (SELECT DISTINCT points FROM Scores ORDER BY points DESC LIMIT 1 OFFSET 1) AS second_highest;
-- second_highest
-- 200

SELECT (SELECT DISTINCT points FROM Scores ORDER BY points DESC LIMIT 1 OFFSET 5) AS sixth_highest;
-- sixth_highest
-- NULL               ← the wrapper turns "no row" into NULL

SELECT MAX(points) AS second_highest FROM Scores WHERE points < (SELECT MAX(points) FROM Scores);
-- second_highest
-- 200

WITH r AS (SELECT points, DENSE_RANK() OVER (ORDER BY points DESC) AS rnk FROM Scores)
SELECT (SELECT DISTINCT points FROM r WHERE rnk = 2) AS second_highest;
-- second_highest
-- 200
```

"Second / Nth highest" has three standard answers:

1. `DISTINCT` + `ORDER BY … DESC` + `LIMIT 1 OFFSET N − 1`. The `DISTINCT` stops duplicates of the top value from taking up slots — without it, the second row here would be 300 again.
2. The `MAX` of everything below the `MAX` — second highest only.
3. `DENSE_RANK() = N`, which also generalizes to "per group" (see [top-n-per-group](top-n-per-group.md)).

When the value might not exist, problems usually want `NULL`, not an empty table. Wrap the query in `SELECT (…) AS name` (a scalar subquery with no rows is `NULL`), or use an aggregate (`MAX` over zero rows is `NULL`).

**Related:** [limit-offset](limit-offset.md) · [scalar-subquery](scalar-subquery.md) · [ranking-functions](ranking-functions.md) · [create-function](create-function.md) · [distinct](distinct.md)
