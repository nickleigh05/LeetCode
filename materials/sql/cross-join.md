# `CROSS JOIN`

```sql
-- Stores     Products    Sales
-- store      product     store  product  units
-- North      pen         North  pen      5
-- South      ink         North  pen      2
--                        South  ink      4

SELECT s.store, p.product FROM Stores s CROSS JOIN Products p;
-- store  product
-- North  ink
-- North  pen
-- South  ink
-- South  pen

SELECT s.store, p.product, IFNULL(SUM(sa.units), 0) AS units
FROM Stores s
CROSS JOIN Products p
LEFT JOIN Sales sa ON sa.store = s.store AND sa.product = p.product
GROUP BY s.store, p.product
ORDER BY s.store, p.product;
-- store  product  units
-- North  ink      0
-- North  pen      7
-- South  ink      4
-- South  pen      0
```

`CROSS JOIN` pairs every left row with every right row: no `ON`, n × m rows. Its main use is building the **full grid of combinations** the answer must contain (every store × every product, every user × every day), then `LEFT JOIN`ing the real data onto that grid so the missing combinations show up with 0.

A comma between tables (`FROM a, b`) is an old-style cross join; with a `WHERE` condition linking the two, it's an inner join in disguise. Watch the size: 10,000 × 10,000 rows is a hundred million.

**Related:** [left-join](left-join.md) · [joins-overview](joins-overview.md) · [count](count.md) · [ifnull-coalesce](ifnull-coalesce.md) · [recursive-cte](recursive-cte.md)
