# `NULL` & `IS NULL`

```sql
-- Products
-- id  name    discount
-- 1   Pen     10
-- 2   Laptop  NULL
-- 3   Mouse   25
-- 4   Desk    NULL

SELECT name FROM Products WHERE discount != 10;
-- name
-- Mouse      ← Laptop and Desk vanish: NULL != 10 is NULL, not TRUE

SELECT name FROM Products WHERE discount != 10 OR discount IS NULL;
-- name
-- Laptop
-- Mouse
-- Desk

SELECT name FROM Products WHERE discount = NULL;            -- → (no rows)   ← never true: write IS NULL
SELECT NULL = NULL, NULL + 1, NULL IS NULL, NULL <=> NULL;  -- → NULL  NULL  1  1
```

`NULL` means "unknown", and it spreads. Arithmetic with `NULL` gives `NULL`, and any comparison with `NULL` — even `NULL = NULL` — gives `NULL` instead of true or false. `WHERE` keeps a row only when its condition is `TRUE`, so rows with `NULL` in the tested column silently drop out of `=`, `!=`, `<`, `LIKE` and `NOT IN` filters.

Test for missing values with `IS NULL` / `IS NOT NULL`, or with MySQL's NULL-safe equality `<=>`. Whenever a column can be `NULL` — the schema or the example data will show it — ask what your filter does to those rows.

**Trap:** on a nullable column, "not equal to X" almost always means `col != X OR col IS NULL`.

**Related:** [ifnull-coalesce](ifnull-coalesce.md) · [logical-operators](logical-operators.md) · [count](count.md) · [anti-join](anti-join.md) · [in-list](in-list.md)
