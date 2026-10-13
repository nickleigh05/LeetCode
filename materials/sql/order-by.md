# `ORDER BY`

```sql
-- Scores
-- id  player  score
-- 1   Ann     80
-- 2   Bob     95
-- 3   Cat     80
-- 4   Dan     NULL

SELECT player, score FROM Scores ORDER BY score DESC, player;
-- player  score
-- Bob     95
-- Ann     80         ← tied on score, so player (ASC) breaks the tie
-- Cat     80
-- Dan     NULL       ← NULL sorts last in DESC, first in ASC

SELECT player, score FROM Scores ORDER BY score IS NULL, score, player;
-- player  score
-- Ann     80
-- Cat     80
-- Bob     95
-- Dan     NULL       ← "score IS NULL" is 0 or 1, so NULLs go to the end

SELECT player FROM Scores ORDER BY CASE player WHEN 'Dan' THEN 0 ELSE 1 END, id;
-- player
-- Dan                ← a custom order: Dan first, then everyone else by id
-- Ann
-- Bob
-- Cat
```

`ORDER BY` sorts the final result, `ASC` (the default) or `DESC` per column, and each later column breaks the ties left by the ones before it. Without `ORDER BY`, row order is unspecified, even when the output happens to look sorted. MySQL puts `NULL`s first in ascending order and last in descending order; `ORDER BY col IS NULL, col` moves them to the end.

`ORDER BY` runs after `SELECT`, so it can use aliases, expressions (a `CASE` for a custom order), and columns that aren't in the output. It only orders the outermost result. Inside a subquery or CTE, an `ORDER BY` doesn't order the outer query; there it only matters alongside `LIMIT`, to choose which rows are kept.

**Related:** [limit-offset](limit-offset.md) · [execution-order](execution-order.md) · [case-when](case-when.md) · [ranking-functions](ranking-functions.md)
