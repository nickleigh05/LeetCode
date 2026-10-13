# `LIKE`

```sql
-- Users
-- id  name     email
-- 1   Ann Lee  ann@mail.com
-- 2   Bob_Ray  bob@site.org
-- 3   annabel  ann.b@mail.com
-- 4   Joanna   jo@site.org

SELECT name FROM Users WHERE name LIKE 'ann%';
-- name
-- Ann Lee      ← case-insensitive
-- annabel

SELECT name FROM Users WHERE name LIKE '%ann%';
-- name
-- Ann Lee
-- annabel
-- Joanna

SELECT email FROM Users WHERE email LIKE '___@%';
-- email
-- ann@mail.com
-- bob@site.org     ← each _ is exactly one character

SELECT name FROM Users WHERE name LIKE '%\_%';
-- name
-- Bob_Ray          ← \_ is a literal underscore

-- Posts
-- id  tags
-- 1   mysql python
-- 2   python sqlite
-- 3   sql
-- 4   nosql sqlserver

SELECT id FROM Posts WHERE tags LIKE 'sql%' OR tags LIKE '% sql%';
-- id
-- 2
-- 3
-- 4                ← any tag that starts with "sql"; mysql and nosql don't count
```

`LIKE` matches a whole string against a pattern: `%` stands for any run of characters (including none) and `_` for exactly one; everything else is literal. A pattern with no wildcards is an exact match. MySQL's default collation makes `LIKE` case-insensitive. Escape a literal `%` or `_` with a backslash.

To find a word that starts any token of a space-separated list, test the start of the string **and** the start of every word after a space: `'x%' OR '% x%'`. Anything more structured — "starts with a letter", "digits only" — needs [regexp](regexp.md).

**Related:** [regexp](regexp.md) · [string-functions](string-functions.md) · [where](where.md) · [comparison-operators](comparison-operators.md)
