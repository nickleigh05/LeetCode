# Conditional Aggregation

```sql
-- Orders
-- id  customer  status    amount
-- 1   Ann       paid      30
-- 2   Ann       refunded  20
-- 3   Bob       paid      50
-- 4   Bob       paid      10
-- 5   Cat       refunded  40

SELECT customer,
       COUNT(*)                                               AS orders,
       SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)       AS paid_orders,
       SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END)  AS paid_amount,
       COUNT(CASE WHEN status = 'refunded' THEN 1 END)        AS refunds,
       SUM(status = 'paid')                                   AS paid_orders_short,
       ROUND(AVG(status = 'paid'), 2)                         AS paid_rate
FROM Orders
GROUP BY customer;
-- customer  orders  paid_orders  paid_amount  refunds  paid_orders_short  paid_rate
-- Ann       2       1            30           1        1                  0.50
-- Bob       2       2            60           0        2                  1.00
-- Cat       1       0            0            1        0                  0.00
```

Put a condition inside an aggregate to compute several filtered totals **in one pass** — one row per group, one column per condition. `SUM(CASE WHEN cond THEN 1 ELSE 0 END)` counts the matching rows, and `THEN amount` sums them instead. `COUNT(CASE WHEN cond THEN 1 END)` also counts, because the missing `ELSE` yields `NULL` and `COUNT` skips `NULL`s.

In MySQL a comparison is already 1 or 0, so **`SUM(cond)` counts and `AVG(cond)` is the fraction of rows where it holds** — the shortest way to write a rate (portable SQL needs the `CASE` form). The same move pivots rows into columns — see [pivot-unpivot](pivot-unpivot.md).

**Related:** [case-when](case-when.md) · [if-function](if-function.md) · [aggregate-functions](aggregate-functions.md) · [ratios-percentages](ratios-percentages.md) · [pivot-unpivot](pivot-unpivot.md) · [count](count.md)
