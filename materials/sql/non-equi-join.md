# Non-Equi Joins (ranges & inequalities)

```sql
-- Members        Tiers
-- name  points   tier    min_pts  max_pts
-- Ann   120      Bronze  0        99
-- Bob   40       Silver  100      499
-- Cat   900      Gold    500      9999

SELECT m.name, t.tier
FROM Members m
JOIN Tiers t ON m.points BETWEEN t.min_pts AND t.max_pts;
-- name  tier
-- Ann   Silver
-- Bob   Bronze
-- Cat   Gold

-- Deposits
-- id  amount
-- 1   10
-- 2   20
-- 3   5

SELECT a.id, SUM(b.amount) AS running_total
FROM Deposits a
JOIN Deposits b ON b.id <= a.id
GROUP BY a.id
ORDER BY a.id;
-- id  running_total
-- 1   10
-- 2   30
-- 3   35
```

`ON` can hold any condition, not just equality. **Range joins** match each value to the bucket that contains it — `BETWEEN start AND end` for tiers, price periods or shifts. Make sure the buckets don't overlap, or rows will match twice.

**Inequality joins** pair each row with every earlier or later row (`b.id <= a.id`). That gives running totals and "within N days" windows without window functions, but at O(n²) cost, so prefer `SUM() OVER` when it's available. Deleting duplicates uses one too: `t1.id > t2.id` keeps the smallest id of each group (see [delete](delete.md)).

**Related:** [self-join](self-join.md) · [between](between.md) · [window-aggregates](window-aggregates.md) · [running-totals](running-totals.md) · [delete](delete.md) · [joins-overview](joins-overview.md)
