# Consecutive Rows & Streaks

```sql
-- Logs
-- id  num
-- 1   5
-- 2   5
-- 3   5
-- 4   8
-- 5   8
-- 6   5

SELECT DISTINCT num FROM (
    SELECT num,
           LAG(num, 1) OVER (ORDER BY id) AS prev1,
           LAG(num, 2) OVER (ORDER BY id) AS prev2
    FROM Logs
) AS t
WHERE num = prev1 AND num = prev2;
-- num
-- 5

SELECT DISTINCT a.num
FROM Logs a
JOIN Logs b ON b.id = a.id + 1 AND b.num = a.num
JOIN Logs c ON c.id = a.id + 2 AND c.num = a.num;
-- num
-- 5

-- Activity
-- user_id  active_on
-- 1        2024-01-01
-- 1        2024-01-02
-- 1        2024-01-03
-- 1        2024-01-07
-- 1        2024-01-08

SELECT user_id, MIN(active_on) AS streak_start, MAX(active_on) AS streak_end, COUNT(*) AS days
FROM (
    SELECT user_id, active_on,
           DATE_SUB(active_on, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_on) DAY) AS grp
    FROM Activity
) AS t
GROUP BY user_id, grp
ORDER BY streak_start;
-- user_id  streak_start  streak_end  days
-- 1        2024-01-01    2024-01-03  3
-- 1        2024-01-07    2024-01-08  2
```

Three tools, from simplest to most general:

- **`LAG` / `LEAD`** compare each row with its neighbours in a chosen order. "The same value as the previous two rows" means three in a row.
- **A self-join on `id + 1`** (or `date + INTERVAL 1 DAY`) does the same without window functions, but only finds runs when the ids or dates have no gaps. `LAG` compares adjacent rows whatever the gap.
- **Gaps and islands** gives whole streaks (start, end, length). Inside a run of consecutive dates (or ids), `value − ROW_NUMBER()` stays constant, so it works as a group key.

`DISTINCT` matters in the first two: a run of four contains two runs of three, and each would report the value.

**Related:** [lag-lead](lag-lead.md) · [self-join](self-join.md) · [ranking-functions](ranking-functions.md) · [date-arithmetic](date-arithmetic.md) · [group-by](group-by.md)
