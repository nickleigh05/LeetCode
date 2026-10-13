# Date Parts & `DATE_FORMAT`

```sql
SELECT YEAR('2024-07-09'), MONTH('2024-07-09'), DAY('2024-07-09');   -- → 2024  7  9
SELECT DATE_FORMAT('2024-07-09', '%Y-%m');               -- → 2024-07     ← a month bucket
SELECT DATE_FORMAT('2024-07-09', '%b %e, %Y');           -- → Jul 9, 2024
SELECT LEFT('2024-07-09', 7);                            -- → 2024-07     ← the same bucket, by slicing the string
SELECT DAYNAME('2024-07-09'), WEEKDAY('2024-07-09'), DAYOFWEEK('2024-07-09');   -- → Tuesday  1  3   ← WEEKDAY: Mon = 0; DAYOFWEEK: Sun = 1
SELECT LAST_DAY('2024-02-10'), DATE('2024-07-09 18:30:00');   -- → 2024-02-29  2024-07-09

-- Orders
-- id  order_date  amount
-- 1   2024-01-05  20
-- 2   2024-01-20  30
-- 3   2024-02-02  50

SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS orders, SUM(amount) AS total
FROM Orders
GROUP BY month;
-- month    orders  total
-- 2024-01  2       50
-- 2024-02  1       50

SELECT id FROM Orders WHERE YEAR(order_date) = 2024 AND MONTH(order_date) = 1;
-- id
-- 1
-- 2
```

`YEAR()`, `MONTH()` and `DAY()` pull numbers out of a date, and `DATE()` drops the time from a `DATETIME`. `DATE_FORMAT(d, pattern)` renders a date as text. `'%Y-%m'` is the standard month bucket for "per month" reports (`LEFT(d, 7)` gives the same string), and grouping by the formatted value aggregates per month or year.

To filter a single month, `YEAR(d) = … AND MONTH(d) = …` reads clearly. A range (`d >= '2024-01-01' AND d < '2024-02-01'`) does the same job and can use an index — see [indexes](indexes.md).

**Specifiers:** `%Y` 2024 · `%y` 24 · `%m` 01–12 · `%c` 1–12 · `%d` 01–31 · `%e` 1–31 · `%M` January · `%b` Jan · `%W` Monday · `%a` Mon · `%H` 00–23 · `%i` minutes · `%s` seconds

**Related:** [date-arithmetic](date-arithmetic.md) · [group-by](group-by.md) · [between](between.md) · [string-functions](string-functions.md) · [indexes](indexes.md)
