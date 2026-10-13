# 1667. Fix Names in a Table

**Easy** · [LeetCode](https://leetcode.com/problems/fix-names-in-a-table/) · [Solution file (no hints)](../../problems/1500-1999/1667.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Fix every name so that only the first letter is uppercase and the rest are lowercase. Order by `user_id`.

```
Table: Users
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| name           | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains the ID and the name of the user. The name consists of only lowercase and uppercase characters.
```

```
Input:
Users table:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | aLice |
| 2       | bOB   |
+---------+-------+
Output:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | Alice |
| 2       | Bob   |
+---------+-------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

There's no "capitalise" function in MySQL. Split the name into its first character and the rest, change the case of each piece, and glue them back together.

| The statement says | Which really means |
|---|---|
| "only the first character is uppercase" | `UPPER` of the first character |
| "the rest are lowercase" | `LOWER` of everything from character 2 on |
| "only lowercase and uppercase characters" | No spaces or multi-word names to handle |
| output column is still `name` | Alias the expression `AS name` |
| "ordered by user_id" | Checked |

🤔 **Before you open the next section:** which string functions give you "the first character" and "everything after it"?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT` + `SUBSTRING`, then `CONCAT`** | `CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2)))` | ✅ Each piece is one function call |
| `SUBSTRING` for both pieces | `SUBSTRING(name, 1, 1)` and `SUBSTRING(name, 2, CHAR_LENGTH(name))` | ✅ Same thing, wordier |
| `UPPER(LEFT(name, 1))` alone | | ❌ Returns only the first letter |
| `INITCAP(name)` | | ❌ PostgreSQL/Oracle only — MySQL has no such function |

**The decision: `CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2)))`.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT user_id,
       CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2))) AS name
```

**Two pieces, recased, rejoined.** `LEFT(name, 1)` is the first character. `SUBSTRING(name, 2)` starts at character 2 and runs to the end — string positions in SQL start at **1**, not 0. `CONCAT` joins the results.
→ [string-functions](../sql/string-functions.md) · [aliases](../sql/aliases.md)

```sql
FROM Users
```

```sql
ORDER BY user_id;
```

→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT user_id,
       CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2))) AS name
FROM Users
ORDER BY user_id;
```

</details>

**Trace it** — each piece:

| `name` | `LEFT(name, 1)` | `SUBSTRING(name, 2)` | `fixed` |
|---|---|---|---|
| aLice | a | Lice | Alice |
| bOB | b | OB | Bob |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · L)</summary>

**O(n · L)** for n names of length up to L (≤ 40 here) — each name is copied and recased once — plus **O(n log n)** for the sort.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · L)</summary>

**O(n · L)** for the new strings in the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "MySQL has no capitalise function, so I split the name: `UPPER` of `LEFT(name, 1)` and `LOWER` of `SUBSTRING(name, 2)`, concatenated, aliased back to `name`, sorted by `user_id`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Names with several words, like 'mary ann'?" | Capitalise after each space — in MySQL 8, `REGEXP_REPLACE` can't change case, so split with `SUBSTRING_INDEX`, or handle it in application code. |
| "What if `name` is `NULL` or empty?" | `CONCAT` with a `NULL` argument returns `NULL`; an empty string stays empty. |
| "Actually update the table?" | `UPDATE Users SET name = CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2)))`. |
| "Why `SUBSTRING(name, 2)` and not `(name, 1)`?" | Positions are 1-based; position 1 is the first letter, which you've already taken. |

**Traps:**

- **0-based positions** — `SUBSTRING(name, 0)` returns an empty string in MySQL.
- **Forgetting `LOWER`** on the rest — `bOB` would become `BOB`.
- **Comparing to check your work** — string comparison is case-insensitive by default, so `'Bob' = 'bOB'` is true; it can't tell you the case is fixed.

**This same move shows up in:** [Invalid Tweets](1683-invalid-tweets.md) (character-counting functions) · [Patients With a Condition](1527-patients-with-a-condition.md) (matching inside strings) · [Group Sold Products By The Date](1484-group-sold-products-by-the-date.md) (building a string from many rows).

</details>

---
