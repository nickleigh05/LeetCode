# `LIMIT` & `OFFSET`

```sql
-- Scores
-- id  player  score
-- 1   Ann     80
-- 2   Bob     95
-- 3   Cat     80
-- 4   Dan     70

SELECT player, score FROM Scores ORDER BY score DESC, player LIMIT 2;
-- player  score
-- Bob     95
-- Ann     80         ← Cat is tied with Ann but cut off: LIMIT ignores ties

SELECT player FROM Scores ORDER BY score DESC, player LIMIT 1 OFFSET 2;   -- → Cat    ← skip 2, take 1
SELECT player FROM Scores ORDER BY score DESC, player LIMIT 2, 1;         -- → Cat    ← MySQL shorthand: LIMIT offset, count
SELECT DISTINCT score FROM Scores ORDER BY score DESC LIMIT 1 OFFSET 1;   -- → 80     ← 2nd-highest distinct score
SELECT DISTINCT score FROM Scores ORDER BY score DESC LIMIT 1 OFFSET 5;   -- → (no rows)    ← empty, not NULL
SELECT player FROM Scores LIMIT 3 - 1;                                    -- → ERROR 1064    ← no expressions in LIMIT
```

`LIMIT n` keeps the first `n` rows, and `OFFSET m` skips `m` rows before that. MySQL also accepts `LIMIT m, n` — offset first, which is easy to misread. `LIMIT` without `ORDER BY` returns an arbitrary `n` rows.

`LIMIT` ignores ties. "The highest score" written as `ORDER BY … LIMIT 1` silently drops anyone tied for first; if ties should all come back, compare against `MAX()` in a subquery or use `RANK()`. Running past the end gives an **empty result rather than `NULL`** — wrap the query in a [scalar subquery](scalar-subquery.md) when `NULL` is the expected answer. `LIMIT` and `OFFSET` take literal numbers (or variables inside a stored function), never expressions like `N - 1`.

**Related:** [order-by](order-by.md) · [distinct](distinct.md) · [scalar-subquery](scalar-subquery.md) · [nth-highest-value](nth-highest-value.md) · [create-function](create-function.md) · [ranking-functions](ranking-functions.md)
