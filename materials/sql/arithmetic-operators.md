# Arithmetic Operators

```sql
SELECT 7 + 2, 7 - 2, 7 * 2;          -- → 9  5  14
SELECT 7 / 2, 1 / 3, 1.5 / 2;        -- → 3.5000  0.3333  0.75000    ← / is true division
SELECT 7 DIV 2, 7 % 2, MOD(7, 2);    -- → 3  1  1                    ← integer division and remainder
SELECT -7 DIV 2, -7 % 2;             -- → -3  -1                     ← both truncate toward zero
SELECT 1 / 0, 5 % 0;                 -- → NULL  NULL                 ← no error in a SELECT, just NULL
SELECT 2 + 3 * 4, (2 + 3) * 4;       -- → 14  20

-- Lockers
-- id  owner
-- 1   Ann
-- 2   Bob
-- 3   Cat

SELECT id, owner FROM Lockers WHERE id % 2 = 1;
-- id  owner
-- 1   Ann
-- 3   Cat
```

`+ - *` work as expected, and `* / DIV %` bind before `+ -`. **`/` is always true division**: `7 / 2` is `3.5000`. MySQL returns a `DECIMAL` with 4 more decimal places than the dividend has, and it never truncates the way Python's `//`, Java's integer division, or Postgres/SQL Server's integer `/` do.

For whole-number division use `DIV`, and for the remainder `%` or `MOD()`. `id % 2 = 1` picks the odd ids, the usual way to split rows into alternating halves. Division or modulo by zero returns `NULL` (with a warning) instead of failing the query.

**Related:** [math-functions](math-functions.md) · [ratios-percentages](ratios-percentages.md) · [data-types](data-types.md) · [case-when](case-when.md)
