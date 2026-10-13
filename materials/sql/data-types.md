# Data Types & Literals

```sql
SELECT 'it''s', "double quotes work too";            -- → it's  double quotes work too
SELECT TRUE, FALSE, TRUE + TRUE;                     -- → 1  0  2
SELECT '5' + 3, '5' = 5;                             -- → 8  1      ← strings convert in a numeric context
SELECT '10' < '9', 10 < 9;                           -- → 1  0      ← but two strings compare as text
SELECT CAST('2024-01-31' AS DATE) + INTERVAL 1 DAY;  -- → 2024-02-01
SELECT CAST(3.99 AS SIGNED), CAST(7 AS DECIMAL(5, 2));   -- → 4  7.00
SELECT 0.1 + 0.2 = 0.3, 0.1e0 + 0.2e0 = 0.3e0;       -- → 1  0      ← DECIMAL is exact, DOUBLE is not
```

| Type | Holds | Literal |
|---|---|---|
| `INT` | whole numbers | `42` |
| `DECIMAL(p, s)` | exact decimals: money, averages, rates | `19.99` |
| `FLOAT` / `DOUBLE` | approximate decimals | `1.5e0` |
| `VARCHAR(n)` | text up to n characters | `'Ann'` |
| `DATE` / `DATETIME` | a day / a day and a time | `'2024-01-31'` / `'2024-01-31 14:05:00'` |
| `ENUM('a', 'b')` | one value from a fixed list of strings | `'a'` |
| `BOOLEAN` | an alias for `TINYINT(1)`: 1 or 0 | `TRUE` |

Strings take **single quotes**, and you double a quote to put one inside (`'it''s'`). MySQL also accepts double quotes, but most other databases don't. Dates are written as `'YYYY-MM-DD'` strings, and that format compares correctly even as plain text. Booleans are just 1 and 0, so conditions can be added up — see [conditional-aggregation](conditional-aggregation.md).

MySQL converts types silently (`'5' = 5` is true), but compare like with like: two strings compare character by character, so `'10' < '9'`. Use `DECIMAL` for exact arithmetic, because `FLOAT`/`DOUBLE` accumulate binary rounding error. `ENUM` values compare as strings but **sort in declaration order**, not alphabetically.

**Related:** [arithmetic-operators](arithmetic-operators.md) · [comparison-operators](comparison-operators.md) · [date-arithmetic](date-arithmetic.md) · [null-is-null](null-is-null.md) · [math-functions](math-functions.md)
