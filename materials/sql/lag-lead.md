# `LAG` & `LEAD`

```sql
-- Readings
-- id  day         value
-- 1   2024-01-01  10
-- 2   2024-01-02  15
-- 3   2024-01-03  15
-- 4   2024-01-05  12

SELECT day, value,
       LAG(value) OVER (ORDER BY day)          AS prev_value,
       LEAD(value) OVER (ORDER BY day)         AS next_value,
       LAG(value, 1, 0) OVER (ORDER BY day)    AS prev_or_0,
       value - LAG(value) OVER (ORDER BY day)  AS delta
FROM Readings;
-- day         value  prev_value  next_value  prev_or_0  delta
-- 2024-01-01  10     NULL        15          0          NULL
-- 2024-01-02  15     10          15          10         5
-- 2024-01-03  15     15          12          15         0
-- 2024-01-05  12     15          NULL        15         -3     ← "previous row" is Jan 3: Jan 4 is missing

SELECT day FROM (
    SELECT day, value, LAG(value) OVER (ORDER BY day) AS prev_value FROM Readings
) AS t
WHERE value > prev_value;
-- day
-- 2024-01-02
```

`LAG(col)` reads `col` from the **previous** row of the window, and `LEAD(col)` from the **next** one; the window's `ORDER BY` defines what "previous" means. `LAG(col, n, default)` looks n rows back and returns `default` instead of `NULL` when there's no such row (the first row has no previous one). With `PARTITION BY`, the lookback restarts in each group — the previous reading of the same sensor.

Use them for day-over-day changes, "went up since last time", and runs of equal values; to filter on the result, wrap the query in a CTE or derived table. **`LAG` looks at the previous row, not the previous date**: if days can be missing, check the gap too (`DATEDIFF(day, LAG(day) OVER …) = 1`) or self-join on the date.

**Related:** [window-functions](window-functions.md) · [consecutive-rows](consecutive-rows.md) · [self-join](self-join.md) · [date-arithmetic](date-arithmetic.md)
