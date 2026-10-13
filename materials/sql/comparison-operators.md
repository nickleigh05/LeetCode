# Comparison Operators

```sql
SELECT 3 = 3, 3 <> 4, 3 != 4, 3 < 4, 3 >= 4;              -- → 1  1  1  1  0
SELECT 'apple' < 'banana', 'Zoo' < 'apple';               -- → 1  0      ← alphabetical, ignoring case
SELECT 'abc' = 'ABC', 'abc' = 'ABC' COLLATE utf8mb4_bin;  -- → 1  0      ← case-insensitive unless you ask
SELECT '2024-03-01' > '2024-02-15';                       -- → 1         ← ISO dates sort correctly as text
SELECT 1 = NULL, NULL <=> NULL, 1 <=> NULL;               -- → NULL  1  0
```

`=` is the equality test — SQL has no `==` — and `<>` and `!=` both mean "not equal". Every comparison returns 1 (true), 0 (false), or `NULL` when either side is `NULL`. That's why `= NULL` never matches anything; `<=>` is MySQL's NULL-safe equality.

Strings compare alphabetically under the column's collation. MySQL's default (`utf8mb4_0900_ai_ci`) ignores case and accents, so `'abc' = 'ABC'`; add `COLLATE utf8mb4_bin` for an exact, case-sensitive comparison. Dates in `'YYYY-MM-DD'` form compare correctly whether they're `DATE` values or plain strings.

**Related:** [where](where.md) · [null-is-null](null-is-null.md) · [logical-operators](logical-operators.md) · [data-types](data-types.md)
