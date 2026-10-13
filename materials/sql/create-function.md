# `CREATE FUNCTION`

```sql
-- Products
-- id  price
-- 1   30
-- 2   10
-- 3   20
-- 4   10

CREATE FUNCTION kthCheapestPrice(K INT) RETURNS INT
READS SQL DATA
BEGIN
  SET K = K - 1;
  RETURN (
      SELECT DISTINCT price FROM Products
      ORDER BY price
      LIMIT 1 OFFSET K
  );
END
SELECT kthCheapestPrice(1), kthCheapestPrice(2), kthCheapestPrice(9);   -- → 10  20  NULL
```

```sql
CREATE FUNCTION broken(K INT) RETURNS INT
READS SQL DATA
BEGIN
  RETURN (SELECT price FROM Products ORDER BY price LIMIT 1 OFFSET K - 1);
END
-- ERROR 1064: … near '- 1)'     ← LIMIT / OFFSET take a variable, not an expression
```

This is the shape of LeetCode's function problems. Parameters go in the parentheses, `RETURNS` declares the type, and the body sits between `BEGIN` and `END`. `RETURN (SELECT …)` hands back a single value — `NULL` if the query finds no rows. Inside the body, `DECLARE m INT DEFAULT K - 1;` creates a local variable and `SET K = K - 1;` assigns one; each statement ends with `;`. `LIMIT` and `OFFSET` accept a variable but not an expression, so compute `K − 1` first.

**Running it locally:** MySQL 8 rejects a function that doesn't declare `DETERMINISTIC`, `READS SQL DATA` or `NO SQL` (error 1418) while binary logging is on, which it is by default. LeetCode's template leaves the characteristic out and is accepted there; adding `READS SQL DATA` is valid either way. The `mysql` command-line client also needs `DELIMITER $$ … END$$ DELIMITER ;` around the function, so the `;` inside the body doesn't end the statement early.

**Related:** [limit-offset](limit-offset.md) · [scalar-subquery](scalar-subquery.md) · [nth-highest-value](nth-highest-value.md) · [distinct](distinct.md)
