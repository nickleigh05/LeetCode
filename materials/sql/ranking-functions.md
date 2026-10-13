# `ROW_NUMBER`, `RANK`, `DENSE_RANK`

```sql
-- Scores
-- player  score
-- Ann     95
-- Bob     90
-- Cat     90
-- Dan     85

SELECT player, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, player) AS row_num,
       RANK()       OVER (ORDER BY score DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rnk
FROM Scores
ORDER BY score DESC, player;
-- player  score  row_num  rnk  dense_rnk
-- Ann     95     1        1    1
-- Bob     90     2        2    2
-- Cat     90     3        2    2
-- Dan     85     4        4    3          ← RANK skips 3 after the tie; DENSE_RANK doesn't
```

All three number the rows in the window's `ORDER BY` order, restarting in each `PARTITION BY` group. They differ only on **ties**:

| Function | Ties | Example |
|---|---|---|
| `ROW_NUMBER()` | different numbers, arbitrary unless you add a tie-breaker | 1, 2, 3, 4 |
| `RANK()` | same number, then a gap | 1, 2, 2, 4 |
| `DENSE_RANK()` | same number, no gap | 1, 2, 2, 3 |

Pick by what the question means: "the top 3 salaries" (distinct values, ties share) → `DENSE_RANK`; ranking like a competition → `RANK`; exactly one row per group → `ROW_NUMBER`. `rank` is a reserved word in MySQL 8, so alias as `rnk` or `` `rank` ``. Also available: `NTILE(n)` splits rows into n buckets, and `PERCENT_RANK()` gives a relative rank from 0 to 1.

**Related:** [window-functions](window-functions.md) · [top-n-per-group](top-n-per-group.md) · [first-row-per-group](first-row-per-group.md) · [nth-highest-value](nth-highest-value.md) · [order-by](order-by.md)
