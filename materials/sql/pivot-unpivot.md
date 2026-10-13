# Pivot & Unpivot

```sql
-- Revenue
-- dept  month  amount
-- eng   Jan    100
-- eng   Feb    150
-- ops   Jan    80

SELECT dept,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan_revenue,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb_revenue
FROM Revenue
GROUP BY dept;
-- dept  Jan_revenue  Feb_revenue
-- eng   100          150
-- ops   80           NULL          ← no Feb row; use ELSE 0 to get 0 instead

-- Stock
-- product  store1  store2
-- pen      10      NULL
-- ink      5       7

SELECT product, 'store1' AS store, store1 AS qty FROM Stock WHERE store1 IS NOT NULL
UNION ALL
SELECT product, 'store2', store2 FROM Stock WHERE store2 IS NOT NULL;
-- product  store   qty
-- pen      store1  10
-- ink      store1  5
-- ink      store2  7
```

**Pivot** turns row values into columns: `GROUP BY` the row key and write one conditional aggregate per output column (`SUM(CASE WHEN month = 'Jan' THEN amount END)`). MySQL has no `PIVOT` keyword, so every output column is listed by hand.

**Unpivot** turns columns into rows: one `SELECT` per column, each with a literal label, glued together with `UNION ALL`. The same trick builds a fixed list of category rows — each branch selects a label and its count — so a category with a count of 0 still appears.

**Related:** [conditional-aggregation](conditional-aggregation.md) · [case-when](case-when.md) · [union](union.md) · [group-by](group-by.md)
