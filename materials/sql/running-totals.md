# Running Totals & Moving Averages

```sql
-- Sales
-- sale_day    amount
-- 2024-01-01  100
-- 2024-01-02  250
-- 2024-01-03  200
-- 2024-01-04  50

SELECT sale_day, amount,
       SUM(amount) OVER (ORDER BY sale_day) AS running_total,
       AVG(amount) OVER (ORDER BY sale_day ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS avg_2day
FROM Sales;
-- sale_day    amount  running_total  avg_2day
-- 2024-01-01  100     100            100.0000
-- 2024-01-02  250     350            175.0000
-- 2024-01-03  200     550            225.0000
-- 2024-01-04  50      600            125.0000

SELECT sale_day FROM (
    SELECT sale_day, SUM(amount) OVER (ORDER BY sale_day) AS running_total FROM Sales
) AS t
WHERE running_total >= 500
ORDER BY sale_day
LIMIT 1;
-- sale_day
-- 2024-01-03         ← the first day the running total reached 500
```

`SUM(x) OVER (ORDER BY t)` is a **running total**: cumulative up to each row. Add `PARTITION BY` to restart it per group. A frame turns it into a **moving window**: `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` is a 7-row moving sum or average.

For a true N-day window, first aggregate to one row per day (in a CTE), then apply the frame — and drop the first N − 1 days if only complete windows count. Threshold questions ("the day the total passed 500", "the last row that still fits under a limit") are a running total plus a filter and `ORDER BY … LIMIT 1`. Without window functions, a self-join on `b.t <= a.t` with `GROUP BY` computes the same totals in O(n²) — see [non-equi-join](non-equi-join.md).

**Related:** [window-aggregates](window-aggregates.md) · [window-frames](window-frames.md) · [non-equi-join](non-equi-join.md) · [cte-with](cte-with.md) · [limit-offset](limit-offset.md)
