# Window Frames (`ROWS BETWEEN`)

```sql
-- Daily
-- day_no  amount
-- 1       10
-- 2       20
-- 3       30
-- 4       40

SELECT day_no, amount,
       SUM(amount) OVER (ORDER BY day_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3_sum,
       AVG(amount) OVER (ORDER BY day_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3_avg,
       SUM(amount) OVER (ORDER BY day_no ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS total
FROM Daily;
-- day_no  amount  last3_sum  last3_avg  total
-- 1       10      10         10.0000    100
-- 2       20      30         15.0000    100
-- 3       30      60         20.0000    100
-- 4       40      90         30.0000    100

-- Txn
-- id  day_no  amount
-- 1   1       10
-- 2   2       20
-- 3   2       5
-- 4   3       1

SELECT id, day_no, amount,
       SUM(amount) OVER (ORDER BY day_no) AS default_frame,
       SUM(amount) OVER (ORDER BY day_no, id ROWS UNBOUNDED PRECEDING) AS rows_frame
FROM Txn
ORDER BY id;
-- id  day_no  amount  default_frame  rows_frame
-- 1   1       10      10             10
-- 2   2       20      35             30         ← the default frame takes every row tied on day_no = 2 at once
-- 3   2       5       35             35
-- 4   3       1       36             36
```

A frame limits which rows of the partition the function sees, relative to the current row. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` is a sliding 3-row window (moving sum or average), and `UNBOUNDED PRECEDING` / `UNBOUNDED FOLLOWING` reach the partition's edges. Frames apply to aggregates and to `FIRST_VALUE` / `LAST_VALUE` / `NTH_VALUE`; ranking functions and `LAG`/`LEAD` ignore them.

With an `ORDER BY` and no frame, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, and `RANGE` treats rows tied on the `ORDER BY` value as one step — so tied rows all get the same running total. Use `ROWS` with a unique tie-breaker when you want one step per row.

**Trap:** `ROWS` counts rows, not days. A "7-day" `ROWS 6 PRECEDING` window is only 7 days if every day has exactly one row, so aggregate to one row per day first. MySQL can also frame by value: `RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW` over a date column.

**Related:** [window-aggregates](window-aggregates.md) · [running-totals](running-totals.md) · [first-last-value](first-last-value.md) · [window-functions](window-functions.md)
