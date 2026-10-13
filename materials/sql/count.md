# `COUNT`

```sql
-- Orders
-- id  customer  coupon
-- 1   Ann       SAVE10
-- 2   Ann       NULL
-- 3   Bob       SAVE10
-- 4   Bob       FREESHIP

SELECT COUNT(*), COUNT(coupon), COUNT(DISTINCT coupon), COUNT(DISTINCT customer, coupon) FROM Orders;
-- COUNT(*)  COUNT(coupon)  COUNT(DISTINCT coupon)  COUNT(DISTINCT customer, coupon)
-- 4         3              2                       3

-- Customers        Purchases
-- id  name         id  customer_id
-- 1   Ann          10  1
-- 2   Bob          11  1
-- 3   Cat          12  3

SELECT c.name, COUNT(p.id) AS purchases, COUNT(*) AS rows_after_join
FROM Customers c
LEFT JOIN Purchases p ON p.customer_id = c.id
GROUP BY c.id, c.name;
-- name  purchases  rows_after_join
-- Ann   2          2
-- Bob   0          1        ← Bob's NULL-filled row still counts as a row
-- Cat   1          1
```

| Form | Counts |
|---|---|
| `COUNT(*)` | rows |
| `COUNT(col)` | rows where `col` is not `NULL` |
| `COUNT(DISTINCT col)` | unique non-`NULL` values |
| `COUNT(DISTINCT a, b)` | unique non-`NULL` combinations (MySQL) |

After a `LEFT JOIN`, count a column from the right table — usually its key. Unmatched rows have `NULL` there, so they count as 0, while `COUNT(*)` counts them as 1. `COUNT` never returns `NULL`, even over zero rows. To count only the rows that meet a condition, see [conditional-aggregation](conditional-aggregation.md).

**Related:** [aggregate-functions](aggregate-functions.md) · [left-join](left-join.md) · [distinct](distinct.md) · [conditional-aggregation](conditional-aggregation.md) · [group-by](group-by.md)
