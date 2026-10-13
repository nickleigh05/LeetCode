# `SELECT … FROM`

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   60000

SELECT name FROM Employee;
-- name
-- Ann
-- Bob

SELECT * FROM Employee;
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   60000

SELECT name, salary / 12 AS monthly, 'USD' AS currency FROM Employee;
-- name  monthly    currency
-- Ann   7500.0000  USD
-- Bob   5000.0000  USD

SELECT 2 + 3;                -- → 5                ← FROM is optional for plain expressions
SELECT * FROM employee;      -- → ERROR 1146: Table 'employee' doesn't exist
```

`SELECT` lists the output columns and `FROM` names the table they come from. Each item in the `SELECT` list — a column, an expression, or a literal — becomes one output column, and `AS` names it. `SELECT *` returns every column, which is handy for exploring, but answers should list their columns explicitly, in the order the expected output shows.

Keywords are case-insensitive (`select` works; uppercase is convention), and so are column names. **Table names are case-sensitive on Linux servers** — the last query fails because the table is `Employee` — so copy them exactly as the schema spells them.

**Related:** [aliases](aliases.md) · [where](where.md) · [execution-order](execution-order.md) · [distinct](distinct.md) · [tables-rows-columns](tables-rows-columns.md)
