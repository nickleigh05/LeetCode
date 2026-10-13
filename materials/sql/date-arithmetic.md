# Date Arithmetic

```sql
SELECT DATEDIFF('2024-03-01', '2024-02-27');                 -- → 3      ← first minus second, in days
SELECT DATEDIFF('2024-02-27', '2024-03-01');                 -- → -3
SELECT DATEDIFF('2024-01-02 00:01', '2024-01-01 23:59');     -- → 1      ← the time of day is ignored
SELECT TIMESTAMPDIFF(HOUR, '2024-01-01 08:00', '2024-01-01 17:30');   -- → 9    ← second minus first, in the unit named
SELECT DATE_ADD('2024-01-31', INTERVAL 1 DAY);               -- → 2024-02-01
SELECT DATE_SUB('2024-03-31', INTERVAL 1 MONTH);             -- → 2024-02-29    ← clamped to the month's last day
SELECT '2024-01-31' + INTERVAL 1 YEAR;                       -- → 2025-01-31

-- Visits
-- user_id  visit_date
-- 1        2024-01-01
-- 1        2024-01-02
-- 2        2024-01-01
-- 2        2024-01-05

SELECT DISTINCT a.user_id
FROM Visits a
JOIN Visits b ON b.user_id = a.user_id AND b.visit_date = a.visit_date + INTERVAL 1 DAY;
-- user_id
-- 1                ← visited on two consecutive days

SELECT user_id, visit_date FROM Visits
WHERE DATEDIFF('2024-01-05', visit_date) BETWEEN 0 AND 2;    -- the 3 days ending on 2024-01-05
-- user_id  visit_date
-- 2        2024-01-05
```

`DATEDIFF(a, b)` returns `a − b` in whole days and ignores any time of day. `TIMESTAMPDIFF(unit, a, b)` returns `b − a` — note the **flipped order** — in `SECOND`, `MINUTE`, `HOUR`, `DAY`, `MONTH` or `YEAR`. `DATE_ADD` / `DATE_SUB`, or simply `date ± INTERVAL n UNIT`, shift a date, and month or year steps clamp to the last valid day. `'YYYY-MM-DD'` strings convert to dates automatically, and `CURDATE()` / `NOW()` give today's date and the current timestamp.

Typical uses: "the next day" is a self-join on `d + INTERVAL 1 DAY`, and "within n days" is `DATEDIFF(…) <= n`. An n-day window ending on day X is `DATEDIFF(X, d) BETWEEN 0 AND n − 1` — the `− 1` is the classic off-by-one.

**Related:** [date-parts-format](date-parts-format.md) · [between](between.md) · [self-join](self-join.md) · [lag-lead](lag-lead.md) · [consecutive-rows](consecutive-rows.md)
