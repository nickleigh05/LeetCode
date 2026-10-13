# Aggregates `OVER` (group totals, running totals)

```sql
-- Sales
-- id  region  amount
-- 1   east    10
-- 2   east    30
-- 3   west    20
-- 4   east    40

SELECT id, region, amount,
       SUM(amount) OVER () AS grand_total,
       SUM(amount) OVER (PARTITION BY region) AS region_total,
       SUM(amount) OVER (ORDER BY id) AS running_total,
       SUM(amount) OVER (PARTITION BY region ORDER BY id) AS region_running,
       ROUND(100 * amount / SUM(amount) OVER (PARTITION BY region), 1) AS pct_of_region
FROM Sales
ORDER BY id;
-- id  region  amount  grand_total  region_total  running_total  region_running  pct_of_region
-- 1   east    10      100          80            10             10              12.5
-- 2   east    30      100          80            40             40              37.5
-- 3   west    20      100          20            60             20              100.0
-- 4   east    40      100          80            100            80              50.0

SELECT id, region FROM (
    SELECT id, region, COUNT(*) OVER (PARTITION BY region) AS region_rows FROM Sales
) AS t
WHERE region_rows > 1;
-- id  region
-- 1   east
-- 2   east
-- 4   east
```

Any aggregate becomes a window function with `OVER`: the row keeps its own columns and gains the aggregate over its window.

- `OVER ()` — the whole result: a grand total on every row.
- `OVER (PARTITION BY x)` — a per-group total on every row. Ideal for "share of group", and for "groups with more than one row" (`COUNT(*) OVER (PARTITION BY x) > 1`) without a join.
- `OVER (ORDER BY y)` — cumulative: a **running total** up to the current row.

That cumulative default has a catch when the `ORDER BY` column has ties — see [window-frames](window-frames.md).

**Related:** [window-functions](window-functions.md) · [window-frames](window-frames.md) · [running-totals](running-totals.md) · [aggregate-functions](aggregate-functions.md) · [ratios-percentages](ratios-percentages.md)
