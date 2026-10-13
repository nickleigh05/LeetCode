# `UNION` & `UNION ALL`

```sql
-- Requests
-- sender  receiver
-- 1       2
-- 1       3
-- 4       3

SELECT sender AS user_id FROM Requests
UNION ALL
SELECT receiver FROM Requests;      -- every appearance: 6 rows
-- user_id
-- 1
-- 1
-- 4
-- 2
-- 3
-- 3

SELECT sender AS user_id FROM Requests
UNION
SELECT receiver FROM Requests;      -- duplicates removed
-- user_id
-- 1
-- 4
-- 2
-- 3

(SELECT sender AS user_id FROM Requests ORDER BY sender DESC LIMIT 1)
UNION ALL
(SELECT receiver FROM Requests ORDER BY receiver LIMIT 1);
-- user_id
-- 4
-- 2

SELECT 'senders' AS role, COUNT(DISTINCT sender) AS people FROM Requests
UNION ALL
SELECT 'receivers', COUNT(DISTINCT receiver) FROM Requests;
-- role       people
-- senders    2
-- receivers  2
```

`UNION` stacks the rows of two queries. Both need the same number of columns with compatible types, matched **by position**, and the output column names come from the first query. `UNION` removes duplicate rows (which costs a sort or hash), while `UNION ALL` keeps every row — use `UNION ALL` unless you specifically need the dedupe.

An `ORDER BY` or `LIMIT` at the end applies to the combined result; to sort or limit one branch, wrap that branch in parentheses. Selecting literal labels builds rows that no table contains — one row per category, say, even when a category's count is 0.

**Related:** [intersect-except](intersect-except.md) · [pivot-unpivot](pivot-unpivot.md) · [right-full-outer-join](right-full-outer-join.md) · [distinct](distinct.md)
