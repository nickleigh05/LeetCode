# `INNER JOIN`

```sql
-- Employee                    Department
-- id  name  departmentId      id  name
-- 1   Ann   1                 1   Eng
-- 2   Bob   2                 2   Sales
-- 3   Cat   NULL              3   HR

SELECT e.name AS employee, d.name AS department
FROM Employee e
JOIN Department d ON e.departmentId = d.id;
-- employee  department
-- Ann       Eng
-- Bob       Sales           ← Cat (no department) and HR (no employees) drop out

-- Orders           Shipments
-- order_id  item   order_id  carrier
-- 1         pen    1         UPS
-- 2         ink    2         DHL

SELECT order_id, item, carrier FROM Orders JOIN Shipments USING (order_id);
-- order_id  item  carrier
-- 1         pen   UPS
-- 2         ink   DHL
```

`JOIN` — short for `INNER JOIN` — keeps only the pairs where the `ON` condition is true, and rows with no partner on either side vanish. That makes it the right default when every row must have a match, and the wrong one when the question says "all customers" or "including those with none" — that's a [`LEFT JOIN`](left-join.md).

Chain more joins one after another; each `ON` can reference any table joined before it. Qualify column names that exist in both tables (`name`, `id`), and alias duplicate output names. When the join columns share a name, `USING (col)` is shorthand for `ON a.col = b.col` and outputs the column once.

**Related:** [joins-overview](joins-overview.md) · [left-join](left-join.md) · [aliases](aliases.md) · [self-join](self-join.md) · [non-equi-join](non-equi-join.md)
