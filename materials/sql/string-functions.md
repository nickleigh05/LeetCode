# String Functions

```sql
SELECT CONCAT('Ann', ' ', 'Lee'), CONCAT('a', NULL);          -- → Ann Lee  NULL     ← any NULL argument → NULL
SELECT CONCAT_WS('-', '2024', '01', NULL, '31');              -- → 2024-01-31        ← separator first; skips NULLs
SELECT UPPER('aBc'), LOWER('aBc');                            -- → ABC  abc
SELECT LEFT('hello', 2), RIGHT('hello', 3), SUBSTRING('hello', 2, 3);   -- → he  llo  ell    ← positions start at 1
SELECT SUBSTRING('hello', 2), SUBSTRING('hello', -3);         -- → ello  llo         ← to the end / from the end
SELECT LENGTH('héllo'), CHAR_LENGTH('héllo');                 -- → 6  5              ← bytes vs characters
SELECT TRIM('  hi  '), REPLACE('a-b-c', '-', '');             -- → hi  abc
SELECT LOCATE('l', 'hello'), LOCATE('z', 'hello');            -- → 3  0              ← 1-based position; 0 = not found
SELECT SUBSTRING_INDEX('ann@mail.com', '@', -1);              -- → mail.com          ← everything after the last '@'
SELECT LPAD('7', 3, '0'), REVERSE('abc'), REPEAT('ab', 3);    -- → 007  cba  ababab
SELECT CONCAT(UPPER(LEFT('aLICE', 1)), LOWER(SUBSTRING('aLICE', 2)));   -- → Alice
SELECT 'a' || 'b';                                            -- → 0                 ← || is OR in MySQL, not concatenation
```

Positions are **1-based**: `SUBSTRING(s, start, length)` starts counting at character 1, and a negative `start` counts from the end. `CONCAT` returns `NULL` if any argument is `NULL`, while `CONCAT_WS` (concat with separator) skips them.

`LENGTH` counts **bytes** and `CHAR_LENGTH` counts **characters**. They agree on plain ASCII and disagree on accented or non-Latin text, so `CHAR_LENGTH` is the safe choice for "longer than N characters". In MySQL `||` is a deprecated logical `OR`, not concatenation — use `CONCAT`. String comparisons and `LIKE` already ignore case under the default collation, so `UPPER`/`LOWER` are for formatting output, not for matching.

**Related:** [like-wildcards](like-wildcards.md) · [regexp](regexp.md) · [group-concat](group-concat.md) · [null-is-null](null-is-null.md)
