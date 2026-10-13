# Comments & Formatting

```sql
-- Employee
-- id  name  salary
-- 1   Ann   90000
-- 2   Bob   60000

-- a line comment: two dashes, then a space
# also a line comment (MySQL only)
/* a block comment,
   which can span lines */
SELECT name          -- comments can trail code
FROM Employee
WHERE salary > 70000;
-- name
-- Ann

SELECT 5 --1;        -- → 6    ← no space after --, so this is arithmetic: 5 - (-1)
```

`-- ` comments out the rest of the line, and MySQL **requires the space** (or a tab) after the dashes — without it, `--1` is read as minus minus one. `#` also works, but only in MySQL. `/* … */` spans lines; the problem statement at the top of each `.sql` solution file in this repo is one.

SQL ignores whitespace and line breaks, so formatting is purely for the reader. The common conventions: keywords in uppercase, one clause per line, each `JOIN … ON` on its own line under `FROM`, and one `SELECT` column per line once there are more than a few.

**Related:** [select-from](select-from.md) · [execution-order](execution-order.md)
