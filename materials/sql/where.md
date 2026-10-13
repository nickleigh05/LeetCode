# `WHERE`

```sql
-- Products
-- id  name    price   category
-- 1   Pen     1.50    office
-- 2   Laptop  999.00  tech
-- 3   Mouse   25.00   tech
-- 4   Desk    150.00  office

SELECT name FROM Products WHERE category = 'tech';
-- name
-- Laptop
-- Mouse

SELECT name, price FROM Products WHERE category = 'tech' AND price < 100;
-- name   price
-- Mouse  25.00

SELECT name FROM Products WHERE price * 2 > 250;
-- name
-- Laptop
-- Desk
```

`WHERE` filters rows before anything else happens to them. It's evaluated once per row, and the row survives only when the condition is `TRUE` — `FALSE` and `NULL` both discard it. Any column of the `FROM` tables, and any expression over them, can be tested.

What `WHERE` can't use: aggregates like `COUNT(*)`, because rows aren't grouped yet (use [having](having.md)), and `SELECT` aliases, because they aren't computed yet (see [execution-order](execution-order.md)). Combine tests with `AND` / `OR` / `NOT`, and reach for `IN`, `BETWEEN`, `LIKE` and `IS NULL` for the common shapes.

**Related:** [comparison-operators](comparison-operators.md) · [logical-operators](logical-operators.md) · [in-list](in-list.md) · [between](between.md) · [like-wildcards](like-wildcards.md) · [null-is-null](null-is-null.md) · [having](having.md)
