# `BETWEEN`

```sql
-- Products
-- id  name    price
-- 1   Pen     1.50
-- 2   Mouse   25.00
-- 3   Desk    150.00
-- 4   Laptop  999.00

SELECT name, price FROM Products WHERE price BETWEEN 25 AND 150;
-- name   price
-- Mouse  25.00
-- Desk   150.00     ← both ends are included

SELECT name FROM Products WHERE price BETWEEN 150 AND 25;    -- → (no rows)    ← smaller value first

-- Logins
-- id  login_time
-- 1   2024-02-01 09:00:00
-- 2   2024-02-29 14:30:00
-- 3   2024-03-01 00:00:00

SELECT id FROM Logins WHERE login_time BETWEEN '2024-02-01' AND '2024-02-29';
-- id
-- 1                 ← the 14:30 login on the 29th is missed: '2024-02-29' means midnight

SELECT id FROM Logins WHERE login_time >= '2024-02-01' AND login_time < '2024-03-01';
-- id
-- 1
-- 2
```

`x BETWEEN a AND b` means `x >= a AND x <= b`: **inclusive at both ends**, with the smaller value first. It works on numbers, strings and dates, and `NOT BETWEEN` is the complement.

On a `DATE` column, `BETWEEN '2024-02-01' AND '2024-02-29'` covers all of February. On a `DATETIME` column, a bare date means midnight, so the same range stops at `2024-02-29 00:00:00`. Use a half-open range there instead: `>= first day AND < the day after`.

**Related:** [in-list](in-list.md) · [comparison-operators](comparison-operators.md) · [date-arithmetic](date-arithmetic.md) · [date-parts-format](date-parts-format.md)
