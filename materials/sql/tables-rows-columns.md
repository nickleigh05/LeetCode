# Tables, Rows & Columns

```sql
-- Employee
-- id  name  salary  departmentId
-- 1   Ann   90000   1
-- 2   Bob   60000   2
-- 3   Cat   75000   1
-- 4   Dan   50000   NULL

SELECT name, salary
FROM Employee
WHERE departmentId = 1;
-- name  salary
-- Ann   90000
-- Cat   75000
```

A **table** is a set of **rows** that all share the same **columns**, and every column has a type (`INT`, `VARCHAR`, `DATE`…). The schema box at the top of each LeetCode SQL problem lists exactly that — column names and types — followed by a note on the keys:

- **Primary key** (`id` here): unique and never `NULL`, so "id is the primary key" guarantees one row per id.
- **Foreign key** (`departmentId`): holds another table's primary key, and it's what you join on. It can be `NULL` — Dan has no department.

Every query reads tables and **returns a table**, which is why a query can stand in anywhere a table can (subqueries, CTEs). Rows have **no inherent order**: "Return the result table in any order" means any row order is accepted, and when a problem does name an order, you need `ORDER BY`.

**Related:** [select-from](select-from.md) · [data-types](data-types.md) · [null-is-null](null-is-null.md) · [joins-overview](joins-overview.md) · [create-table-insert](create-table-insert.md)
