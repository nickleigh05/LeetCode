# Anti-Join (rows with no match)

```sql
-- Customers        Orders
-- id  name         id  customer_id
-- 1   Ann          10  1
-- 2   Bob          11  3
-- 3   Cat          12  NULL

SELECT c.name
FROM Customers c
LEFT JOIN Orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
-- name
-- Bob

SELECT c.name
FROM Customers c
WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.id);
-- name
-- Bob

SELECT name FROM Customers WHERE id NOT IN (SELECT customer_id FROM Orders);
-- (no rows)      ← order 12's NULL customer_id makes NOT IN unknown for everyone

SELECT name FROM Customers
WHERE id NOT IN (SELECT customer_id FROM Orders WHERE customer_id IS NOT NULL);
-- name
-- Bob
```

"Which X never did Y?" is an **anti-join**: keep the left rows that have no partner. There are two safe ways to write it:

- `LEFT JOIN`, then keep the rows where the right table's primary key `IS NULL` — a key is never `NULL` in a real match, so `NULL` there means "no match".
- `NOT EXISTS` with a correlated subquery.

`NOT IN` looks simpler but breaks if the subquery returns even one `NULL`: `x NOT IN (…, NULL)` can never be `TRUE`, so nothing comes back. If you use it, filter the `NULL`s out of the subquery. The opposite question — rows with at least one match, each listed once — is a semi-join, written with `EXISTS` or `IN`.

**Related:** [left-join](left-join.md) · [exists](exists.md) · [in-subquery](in-subquery.md) · [null-is-null](null-is-null.md) · [intersect-except](intersect-except.md)
