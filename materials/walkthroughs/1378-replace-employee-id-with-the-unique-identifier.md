# 1378. Replace Employee ID With The Unique Identifier

**Easy** · [LeetCode](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/) · [Solution file (no hints)](../../problems/1000-1499/1378.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Show each employee's `unique_id` next to their name. Employees with no unique id still appear, with `null`. Any order.

```
Table: Employees
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| name          | varchar |
+---------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the id and the name of an employee in a company.

Table: EmployeeUNI
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| unique_id     | int     |
+---------------+---------+
(id, unique_id) is the primary key (combination of columns with unique values) for this table.
Each row of this table contains the id and the corresponding unique id of an employee in the company.
```

```
Input:
Employees table:
+----+----------+
| id | name     |
+----+----------+
| 1  | Alice    |
| 7  | Bob      |
| 11 | Meir     |
| 90 | Winston  |
| 3  | Jonathan |
+----+----------+
EmployeeUNI table:
+----+-----------+
| id | unique_id |
+----+-----------+
| 3  | 1         |
| 11 | 2         |
| 90 | 3         |
+----+-----------+
Output:
+-----------+----------+
| unique_id | name     |
+-----------+----------+
| null      | Alice    |
| null      | Bob      |
| 2         | Meir     |
| 3         | Winston  |
| 1         | Jonathan |
+-----------+----------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The first problem with two tables. The facts you need are split: names live in `Employees`, unique ids in `EmployeeUNI`, and `id` is the column they share.

| The statement says | Which really means |
|---|---|
| two tables sharing `id` | Stitch rows together where `Employees.id = EmployeeUNI.id` → a **join** |
| "show the unique ID of **each** user" | Every employee appears — even ones with no match on the other side |
| "if a user does not have a unique ID … show null" | Missing matches must survive as `NULL`, not disappear |
| output is `unique_id, name` | The id column comes first |
| EmployeeUNI's primary key is `(id, unique_id)` | One row per id here, so the join won't multiply employees |

"Each employee, matched or not" is the definition of a **left join**: keep every row of the left table, fill in the right side where a match exists, `NULL` where it doesn't.

🤔 **Before you open the next section:** Alice has no row in `EmployeeUNI`. What happens to her with a plain `JOIN`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT JOIN`** | `FROM Employees e LEFT JOIN EmployeeUNI u ON e.id = u.id` | ✅ Keeps every employee; `NULL` where there's no match |
| `RIGHT JOIN`, tables swapped | `FROM EmployeeUNI u RIGHT JOIN Employees e ON …` | ✅ Identical result. Rarely used — `LEFT JOIN` with the "keep all" table first reads better |
| Scalar subquery | `SELECT (SELECT unique_id FROM EmployeeUNI u WHERE u.id = e.id), name …` | ✅ Works because each id has at most one unique id; errors otherwise |
| Plain `JOIN` | `FROM Employees e JOIN EmployeeUNI u ON e.id = u.id` | ❌ Drops Alice and Bob |

**The decision: `LEFT JOIN`.** The statement's "each user, `null` if missing" is precisely what it does.

An inner join keeps only rows that match on **both** sides:

| `unique_id` | `name` |
|---|---|
| 2 | Meir |
| 3 | Winston |
| 1 | Jonathan |

Alice and Bob are gone, because they have no partner row.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT u.unique_id, e.name
```

**Two columns, from two different tables.** The prefixes `u.` and `e.` say which table each column comes from. They're required when both tables have a column with the same name (`id` here) and good practice always.
→ [aliases](../sql/aliases.md) · [select-from](../sql/select-from.md)

```sql
FROM Employees e
```

**The table whose rows must all survive goes first.** In a left join, the left table is the one you're keeping. `e` is a table alias, so you can write `e.name` instead of `Employees.name`.

```sql
LEFT JOIN EmployeeUNI u
    ON e.id = u.id;
```

**Attach each employee's unique id, if there is one.** `ON` says which rows belong together: same `id`. For Alice there's no matching row, so every `u.` column comes back `NULL`.
→ [left-join](../sql/left-join.md) · [joins-overview](../sql/joins-overview.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT u.unique_id, e.name
FROM Employees e
LEFT JOIN EmployeeUNI u
    ON e.id = u.id;
```

</details>

**Trace it** — the joined rows before the final `SELECT` picks two columns:

| `e.id` | `name` | `u.id` | `unique_id` |
|---|---|---|---|
| 1 | Alice | `NULL` | `NULL` |
| 7 | Bob | `NULL` | `NULL` |
| 11 | Meir | 11 | 2 |
| 90 | Winston | 90 | 3 |
| 3 | Jonathan | 3 | 1 |

Every employee is here once. Where `u.id` is `NULL`, there was no match and `unique_id` is `NULL` too — exactly what the expected output shows.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)** for n employees and m unique-id rows.

LeetCode's tables have no indexes, so MySQL 8 runs this as a **hash join**: build a hash table on one side's `id` (O(m)), then probe it once per employee (O(n)). With an index on `EmployeeUNI.id`, it would instead look each employee up in the index: O(n log m).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** for the hash table built on the smaller side, plus the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Names and unique ids are in different tables, joined on `id`. Every employee has to appear even without a unique id, so it's a `LEFT JOIN` from `Employees` — unmatched rows get `NULL` on the right side. An inner join would silently drop them."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Only employees **without** a unique id?" | Add `WHERE u.id IS NULL` — the anti-join pattern. See [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md). |
| "Show `'none'` instead of `null`." | `COALESCE(u.unique_id, 'none')` — or `IFNULL`. |
| "What if an employee had two unique ids?" | The left join returns that employee twice, once per match. Joins multiply rows by the number of matches. |
| "Unique ids that belong to no employee?" | Flip it: `EmployeeUNI LEFT JOIN Employees … WHERE e.id IS NULL`. MySQL has no `FULL OUTER JOIN`; emulate it with a `UNION` of a left and a right join. |
| "Why `LEFT` and not `RIGHT`?" | Same power; `LEFT` puts the "keep every row" table first, which is how most people read queries. |

**Traps:**

- **Plain `JOIN`** — drops every unmatched employee.
- **Unqualified `id`** — both tables have one; MySQL rejects `SELECT id` as ambiguous.
- **Wrong column order** — the expected output is `unique_id, name`.

**This same move shows up in:** [Employee Bonus](577-employee-bonus.md) (left join, then filter) · [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md) (left join to find what's missing) · [Product Sales Analysis I](1068-product-sales-analysis-i.md) (when an inner join is the right call).

</details>

---
