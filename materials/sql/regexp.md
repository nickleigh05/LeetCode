# `REGEXP`

```sql
SELECT 'abc123' REGEXP '^[a-z]+[0-9]+$';                -- → 1
SELECT 'abc123' REGEXP '[0-9]';                         -- → 1      ← unanchored: matches anywhere
SELECT 'ABC' REGEXP '^[a-z]+$';                         -- → 1      ← case-insensitive, like LIKE
SELECT REGEXP_LIKE('ABC', '^[a-z]+$', 'c');             -- → 0      ← 'c' = case-sensitive
SELECT 'x.y' REGEXP '^x\\.y$', 'xzy' REGEXP '^x[.]y$';  -- → 1  0   ← a literal dot: \\. or [.]
SELECT 'item SKU100' REGEXP '\\bSKU1', 'a1' REGEXP '\\d';  -- → 1  1   ← \\b word boundary, \\d digit
SELECT REGEXP_REPLACE('a1b22', '[0-9]+', '#');          -- → a#b#
SELECT REGEXP_SUBSTR('order-4471-x', '[0-9]+');         -- → 4471

-- Users
-- id  email
-- 1   ann@example.com
-- 2   1bob@example.com
-- 3   cat.w@example.org

SELECT email FROM Users WHERE email REGEXP '^[a-z][a-z0-9._]*@example[.]com$';
-- email
-- ann@example.com
```

`REGEXP` (also spelled `RLIKE`, or `REGEXP_LIKE(str, pattern)`) tests a regular expression. Unlike `LIKE`, it matches **anywhere** in the string unless you anchor it with `^` (start) and `$` (end). It follows the collation, so it's case-insensitive by default; pass `'c'` as `REGEXP_LIKE`'s third argument for a case-sensitive match.

Inside a MySQL string a backslash has to be doubled (`'\\.'` for a literal dot), or you can sidestep escaping with a class like `[.]`. MySQL 8 also has `REGEXP_REPLACE`, `REGEXP_SUBSTR` and `REGEXP_INSTR`.

**Cheat sheet:** `.` any character · `[abc]` one of · `[^abc]` none of · `[a-z0-9]` ranges · `*` 0+ · `+` 1+ · `?` 0 or 1 · `{2,4}` 2 to 4 · `a|b` either · `( )` group · `^` `$` anchors · `\\b` word boundary · `\\d` digit

**Related:** [like-wildcards](like-wildcards.md) · [string-functions](string-functions.md) · [where](where.md)
