# `CREATE TABLE` & `INSERT`

```sql
CREATE TABLE Employee (
    id     INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    salary INT,
    hired  DATE
);
INSERT INTO Employee (id, name, salary, hired) VALUES
    (1, 'Ann', 90000, '2021-03-01'),
    (2, 'Bob', NULL, '2023-07-15');
INSERT INTO Employee (id, name) VALUES (3, 'Cat');
SELECT * FROM Employee;
-- id  name  salary  hired
-- 1   Ann   90000   2021-03-01
-- 2   Bob   NULL    2023-07-15
-- 3   Cat   NULL    NULL          ← omitted columns get NULL (or their DEFAULT)

INSERT INTO Employee (id, name) VALUES (1, 'Dup');     -- → ERROR 1062    ← duplicate primary key
INSERT INTO Employee (id, name) VALUES (4, NULL);      -- → ERROR 1048    ← name is NOT NULL
```

You never write DDL in a LeetCode answer, but every problem's **SQL Schema** tab is exactly this: `CREATE TABLE` statements plus `INSERT`s for the example. Paste it into a local MySQL 8 server to experiment — for instance the official image, `docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=yes mysql:8.0`.

`PRIMARY KEY` means unique and never `NULL`; `NOT NULL` forbids `NULL`s; columns left out of an `INSERT` get `NULL` or their `DEFAULT`. `DROP TABLE IF EXISTS t` resets a table between runs, and `INSERT INTO t SELECT …` copies query results in.

**Related:** [data-types](data-types.md) · [tables-rows-columns](tables-rows-columns.md) · [delete](delete.md) · [update](update.md) · [indexes](indexes.md)
