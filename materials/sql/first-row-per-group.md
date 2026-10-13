# First / Latest Row per Group

```sql
-- Logins
-- user_id  login_date  device
-- 1        2024-01-03  phone
-- 1        2024-01-01  laptop
-- 2        2024-01-02  tablet
-- 2        2024-01-05  phone

SELECT user_id, login_date, device
FROM Logins
WHERE (user_id, login_date) IN (SELECT user_id, MIN(login_date) FROM Logins GROUP BY user_id);
-- user_id  login_date  device
-- 1        2024-01-01  laptop
-- 2        2024-01-02  tablet

SELECT user_id, login_date, device
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM Logins) AS t
WHERE rn = 1;
-- user_id  login_date  device
-- 1        2024-01-01  laptop
-- 2        2024-01-02  tablet

-- Prices
-- product  changed_on  price
-- pen      2024-01-01  2.00
-- pen      2024-03-01  2.50
-- ink      2024-04-01  5.00

SELECT product, price FROM Prices
WHERE (product, changed_on) IN (
    SELECT product, MAX(changed_on) FROM Prices
    WHERE changed_on <= '2024-03-15'
    GROUP BY product
);
-- product  price
-- pen      2.50       ← each product's price as of 2024-03-15; ink had none yet, so it's missing
```

To get the **whole row** behind each group's first, last, min or max — not just the value — there are two ways:

1. Compute `(group, MIN(x))` in a subquery and keep the rows that match that pair. Ties all come back.
2. Number the rows with `ROW_NUMBER() OVER (PARTITION BY group ORDER BY x)` and keep `rn = 1` — exactly one row per group (add a tie-breaker to the `ORDER BY`).

`GROUP BY` alone can't do it: `SELECT user_id, MIN(login_date), device` has no way to know which device goes with the minimum. "Value as of a date" is the same pattern restricted to rows on or before that date. Groups with no qualifying row disappear, so `LEFT JOIN` from the full list of keys (or `UNION` in a default) when they must appear.

**Related:** [in-subquery](in-subquery.md) · [ranking-functions](ranking-functions.md) · [top-n-per-group](top-n-per-group.md) · [group-by](group-by.md) · [first-last-value](first-last-value.md)
