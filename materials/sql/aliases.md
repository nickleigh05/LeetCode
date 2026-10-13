# Aliases (`AS`)

```sql
-- Employee
-- id  name  salary  managerId
-- 1   Ann   90000   NULL
-- 2   Bob   60000   1
-- 3   Cat   75000   1

SELECT name AS employee, salary / 12 AS monthly FROM Employee;
-- employee  monthly
-- Ann       7500.0000
-- Bob       5000.0000
-- Cat       6250.0000

SELECT e.name, m.name AS manager
FROM Employee AS e
JOIN Employee AS m ON e.managerId = m.id;
-- name  manager
-- Bob   Ann
-- Cat   Ann

SELECT COUNT(*) AS `rank`, COUNT(*) AS "Total Staff" FROM Employee;
-- rank  Total Staff
-- 3     3

SELECT COUNT(*) AS rank FROM Employee;    -- → ERROR 1064    ← rank is a reserved word in MySQL 8
SELECT Employee.name FROM Employee e;     -- → ERROR 1054    ← once a table has an alias, use the alias
```

`AS` renames a column or a table for the rest of the query. **Column aliases** name your output, and LeetCode's expected output fixes the column names, so match them exactly. **Table aliases** (`Employee AS e`, or just `Employee e`) shorten every column reference and are required when the same table appears twice. Once a table has an alias, its original name is no longer visible. The `AS` keyword itself is optional, but it makes the intent obvious.

Quote an alias with backticks (or double quotes) when it contains spaces or is a reserved word — `rank`, `order`, `group`, `key` and `change` are the usual collisions. Aliases are visible to `ORDER BY` (and, in MySQL, to `GROUP BY` and `HAVING`), but never to `WHERE` — see [execution-order](execution-order.md).

**Related:** [select-from](select-from.md) · [execution-order](execution-order.md) · [self-join](self-join.md)
