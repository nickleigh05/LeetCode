# `IN`

```sql
-- Products
-- id  name    category
-- 1   Pen     office
-- 2   Laptop  tech
-- 3   Mouse   tech
-- 4   Shovel  garden

SELECT name FROM Products WHERE category IN ('tech', 'garden');
-- name
-- Laptop
-- Mouse
-- Shovel

SELECT name FROM Products WHERE id NOT IN (1, 2);
-- name
-- Mouse
-- Shovel

SELECT 3 IN (1, 2, 3), 3 NOT IN (1, 2), 3 NOT IN (1, 2, NULL);   -- → 1  1  NULL    ← one NULL poisons NOT IN
```

`x IN (a, b, c)` is shorthand for `x = a OR x = b OR x = c`, and `NOT IN` is its negation. The list can also be a subquery — `WHERE id IN (SELECT …)` — see [in-subquery](in-subquery.md).

The trap is `NOT IN` with a `NULL` in the list. `x NOT IN (1, 2, NULL)` means `x != 1 AND x != 2 AND x != NULL`, and that last part is `NULL`, so the test can never be `TRUE` and no rows come back. With a literal list it's easy to spot; with a subquery over a nullable column it's a silent wrong answer.

**Related:** [in-subquery](in-subquery.md) · [between](between.md) · [null-is-null](null-is-null.md) · [anti-join](anti-join.md)
