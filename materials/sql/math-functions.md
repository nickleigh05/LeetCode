# `ROUND` & Math Functions

```sql
SELECT ROUND(2.345, 2), ROUND(2.5), ROUND(-2.5), ROUND(1234, -2);   -- → 2.35  3  -3  1200
SELECT ROUND(2.5e0), ROUND(3.5e0);                                  -- → 2  4      ← DOUBLE rounds half to even
SELECT ROUND(10 / 3, 2);                                            -- → 3.33
SELECT TRUNCATE(2.349, 2), FLOOR(2.7), CEIL(2.1), FLOOR(-2.5);      -- → 2.34  2  3  -3
SELECT ABS(-4), POWER(2, 10), SQRT(16), SIGN(-3);                   -- → 4  1024  4  -1
SELECT GREATEST(3, 9, 5), LEAST(3, 9, 5);                           -- → 9  3      ← within one row

-- Matches
-- id  team_a  team_b
-- 1   Lions   Bears
-- 2   Bears   Lions
-- 3   Hawks   Bears

SELECT DISTINCT LEAST(team_a, team_b) AS t1, GREATEST(team_a, team_b) AS t2 FROM Matches;
-- t1     t2
-- Bears  Lions      ← (Lions, Bears) and (Bears, Lions) collapse into one pair
-- Bears  Hawks
```

`ROUND(x, d)` rounds to `d` decimal places; `d` defaults to 0, and a negative `d` rounds to the left of the point. Exact values (`INT`, `DECIMAL`, and literals like `2.5`) round half away from zero. Approximate ones (`FLOAT`/`DOUBLE` columns, and anything computed from them) round **half to even**, so `ROUND(2.5)` is 3 but `ROUND(2.5e0)` is 2. `TRUNCATE` cuts digits without rounding, and `FLOOR` / `CEIL` go to the integer below / above (`FLOOR(-2.5)` is −3).

"Round to 2 decimal places" means `ROUND(expr, 2)` as the very last step, because rounding intermediate values changes the answer. `GREATEST` and `LEAST` compare values within one row (`MAX` and `MIN` compare across rows), which makes them the tool for normalizing unordered pairs.

**Related:** [arithmetic-operators](arithmetic-operators.md) · [ratios-percentages](ratios-percentages.md) · [aggregate-functions](aggregate-functions.md) · [data-types](data-types.md)
