# 196. Delete Duplicate Emails

**Easy** · [LeetCode](https://leetcode.com/problems/delete-duplicate-emails/) · [Solution file (no hints)](../../problems/0001-0499/196.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

**Delete** duplicate emails, keeping only the row with the smallest `id` for each email. This is a `DELETE` statement, not a `SELECT` — the judge looks at the `Person` table afterwards.

```
Table: Person
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains an email. The emails will not contain uppercase letters.
```

```
Input:
Person table:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Output:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "write a `DELETE` statement and not a `SELECT`" | You change the table; there's no result set |
| "keeping only one unique email with the smallest id" | For each email, delete every row that has a **smaller** id with the same email |
| "The final order … does not matter" | No sorting |
| john appears as ids 1 and 3 | Delete 3, keep 1 |

Phrase the rule as a condition on a single row: **delete a row if another row has the same email and a smaller id.** That "another row" is a self-join.

🤔 **Before you open the next section:** for id 3, which other row proves it's a duplicate?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Multi-table `DELETE` with a self-join** | `DELETE p1 FROM Person p1 JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id` | ✅ Deletes exactly the rows that have a smaller twin |
| `NOT IN` the keepers, wrapped in a derived table | `DELETE FROM Person WHERE id NOT IN (SELECT keep_id FROM (SELECT MIN(id) AS keep_id … GROUP BY email) keepers)` | ✅ Works — the extra wrapping is required in MySQL |
| `NOT IN` the keepers, unwrapped | `… WHERE id NOT IN (SELECT MIN(id) FROM Person GROUP BY email)` | ❌ MySQL error 1093: *You can't specify target table 'Person' for update in FROM clause* |
| `SELECT DISTINCT email …` | | ❌ A query, not a deletion — the table is unchanged |

**The decision: the self-join `DELETE`.** MySQL lets `DELETE` name which alias's rows to remove, and the join decides which rows those are.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
DELETE p1
```

**Delete rows of `p1` — only `p1`.** In a multi-table `DELETE`, the names right after `DELETE` say which tables lose rows; the others are only read.
→ [delete](../sql/delete.md)

```sql
FROM Person p1
```

```sql
JOIN Person p2
    ON  p1.email = p2.email
    AND p1.id > p2.id;
```

**`p1` is a duplicate if some `p2` has the same email and a smaller id.** For the smallest-id row of each email there's no such `p2`, so it never joins and survives. Every larger-id row joins at least once and is deleted.
→ [self-join](../sql/self-join.md) · [non-equi-join](../sql/non-equi-join.md)

<details>
<summary>The whole thing together</summary>

```sql
DELETE p1
FROM Person p1
JOIN Person p2
    ON  p1.email = p2.email
    AND p1.id > p2.id;
```

</details>

**Trace it** — the rows the join produces, which are the rows to delete:

| `p1.id (deleted)` | `email` | `p2.id (smaller)` |
|---|---|---|
| 3 | john@example.com | 1 |

Only id 3 has a smaller twin (id 1). After the delete, `Person` holds ids 1 and 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + d)</summary>

**O(n)** to hash-join on `email` (the `id` comparison is checked per matching pair), plus the cost of deleting d rows. An email shared by k rows creates up to k²/2 pairs, so heavy duplication grows the join.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the join's hash table and the list of rows to delete.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A row is a duplicate if another row has the same email and a smaller id. I self-join `Person` on that condition and delete the `p1` side. The smallest id for each email has no smaller twin, so it's never matched and survives."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `DELETE … WHERE id NOT IN (SELECT MIN(id) …)`?" | MySQL won't let a `DELETE`'s subquery read the table being deleted from (error 1093). Wrapping the subquery in a derived table makes MySQL materialise it first. |
| "Keep the **largest** id instead?" | Flip the comparison: `p1.id < p2.id`. |
| "With a window function?" | `DELETE FROM Person WHERE id IN (SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM Person) t WHERE rn > 1)`. |
| "Prevent duplicates in the first place?" | A `UNIQUE` index on `email`. |
| "Is this safe to run twice?" | Yes — the second run finds nothing to delete. |

**Traps:**

- **Writing a `SELECT`** — the judge checks the table, not your output.
- **`p1.id != p2.id`** — deletes **every** row of a duplicated email, including the one to keep.
- **The unwrapped subquery** — error 1093.

**This same move shows up in:** [Rising Temperature](197-rising-temperature.md) (a self-join comparing two rows) · [Managers with at Least 5 Direct Reports](570-managers-with-at-least-5-direct-reports.md) (self-join within one table) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (keeping rows tied to a per-group minimum).

</details>

---
