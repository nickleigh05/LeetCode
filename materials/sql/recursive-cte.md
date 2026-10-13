# Recursive CTEs

```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n                          -- anchor: the starting row
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 5     -- recursive step: built from the previous round
)
SELECT n FROM nums;
-- n
-- 1
-- 2
-- 3
-- 4
-- 5

WITH RECURSIVE days AS (
    SELECT DATE('2024-01-30') AS d
    UNION ALL
    SELECT d + INTERVAL 1 DAY FROM days WHERE d < '2024-02-02'
)
SELECT d FROM days;
-- d
-- 2024-01-30
-- 2024-01-31
-- 2024-02-01
-- 2024-02-02

-- Employee
-- id  name  managerId
-- 1   Ann   NULL
-- 2   Bob   1
-- 3   Cat   2
-- 4   Dan   2

WITH RECURSIVE chain AS (
    SELECT id, name, 0 AS depth FROM Employee WHERE managerId IS NULL
    UNION ALL
    SELECT e.id, e.name, c.depth + 1 FROM Employee e JOIN chain c ON e.managerId = c.id
)
SELECT name, depth FROM chain ORDER BY depth, name;
-- name  depth
-- Ann   0
-- Bob   1
-- Cat   2
-- Dan   2

WITH RECURSIVE s AS (SELECT 'a' AS str UNION ALL SELECT CONCAT(str, 'b') FROM s WHERE CHAR_LENGTH(str) < 3)
SELECT str FROM s;    -- → ERROR 1406    ← the anchor made str a 1-character column; CAST it wider
```

`WITH RECURSIVE` builds a result in rounds. The **anchor** query produces the starting rows; then the **recursive** part, which reads the CTE itself, runs on the rows produced by the previous round, again and again, until a round produces nothing.

Use it to generate sequences — the numbers 1…n, or every date in a range to `LEFT JOIN` sparse data onto — and to walk hierarchies such as an org chart. The recursive part needs a stopping condition: MySQL aborts after 1000 rounds by default (`cte_max_recursion_depth`). The anchor fixes each column's type, so cast it wide enough (`CAST('a' AS CHAR(50))`) when the recursive part builds longer strings or bigger numbers.

**Related:** [cte-with](cte-with.md) · [union](union.md) · [cross-join](cross-join.md) · [date-arithmetic](date-arithmetic.md) · [self-join](self-join.md)
