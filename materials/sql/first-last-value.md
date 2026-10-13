# `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`

```sql
-- Prices
-- product  changed_on  price
-- pen      2024-01-01  2.00
-- pen      2024-03-01  2.50
-- pen      2024-06-01  3.00
-- ink      2024-02-01  5.00

SELECT product, changed_on, price,
       FIRST_VALUE(price) OVER w AS first_price,
       LAST_VALUE(price)  OVER w AS last_price_wrong,
       LAST_VALUE(price)  OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_price,
       NTH_VALUE(price, 2) OVER w AS second_price
FROM Prices
WINDOW w AS (PARTITION BY product ORDER BY changed_on)
ORDER BY product, changed_on;
-- product  changed_on  price  first_price  last_price_wrong  last_price  second_price
-- ink      2024-02-01  5.00   5.00         5.00              5.00        NULL
-- pen      2024-01-01  2.00   2.00         2.00              3.00        NULL
-- pen      2024-03-01  2.50   2.00         2.50              3.00        2.50
-- pen      2024-06-01  3.00   2.00         3.00              3.00        2.50
```

`FIRST_VALUE(x)`, `LAST_VALUE(x)` and `NTH_VALUE(x, n)` return `x` from the first, last, or nth row of the **frame**. The trap: with an `ORDER BY`, the default frame ends at the current row, so `LAST_VALUE` just returns the current row's value, and `NTH_VALUE` is `NULL` until the frame reaches row n. Add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or flip the sort and use `FIRST_VALUE`.

The `WINDOW` clause names a window once so several functions can share it, and `OVER (w ROWS …)` extends a named window with a frame.

**Related:** [window-frames](window-frames.md) · [window-functions](window-functions.md) · [first-row-per-group](first-row-per-group.md) · [lag-lead](lag-lead.md)
