# `AND`, `OR`, `NOT`

```sql
-- Products
-- id  name    price   category
-- 1   Pen     1.50    office
-- 2   Laptop  999.00  tech
-- 3   Mouse   25.00   tech
-- 4   Desk    150.00  office

SELECT name FROM Products
WHERE category = 'tech' OR category = 'office' AND price > 100;
-- name
-- Laptop
-- Mouse
-- Desk      ← AND binds first: tech OR (office AND price > 100)

SELECT name FROM Products
WHERE (category = 'tech' OR category = 'office') AND price > 100;
-- name
-- Laptop
-- Desk

SELECT name FROM Products WHERE NOT category = 'tech';
-- name
-- Pen
-- Desk

SELECT NULL AND FALSE, NULL AND TRUE, NULL OR TRUE, NULL OR FALSE, NOT NULL;   -- → 0  NULL  1  NULL  NULL
```

`AND` binds tighter than `OR`, the same way `*` binds tighter than `+`. The first query reads as `tech OR (office AND price > 100)`, which is almost never what was meant. Put parentheses around every `OR` group that's mixed with `AND`.

With `NULL` in play, SQL uses **three-valued logic**: `FALSE AND` anything is `FALSE`, `TRUE OR` anything is `TRUE`, and every other combination involving `NULL` is `NULL` — which `WHERE` treats as "drop the row". MySQL also accepts `&&`, `||` and `!`, but `||` is string concatenation in most other databases (and deprecated as `OR` in MySQL), so stick to the words.

**Related:** [where](where.md) · [null-is-null](null-is-null.md) · [comparison-operators](comparison-operators.md) · [case-when](case-when.md)
