# 1978. Employees Whose Manager Left the Company

**Easy** · [LeetCode](https://leetcode.com/problems/employees-whose-manager-left-the-company/) · [Solution file (no hints)](../../problems/1500-1999/1978.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find employees earning **less than $30000** whose manager **left the company** — the manager's row was deleted, but the employee's `manager_id` still points at them. Order by `employee_id`.

```
Table: Employees
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| employee_id | int      |
| name        | varchar  |
| manager_id  | int      |
| salary      | int      |
+-------------+----------+
In SQL, employee_id is the primary key for this table.
This table contains information about the employees, their salary, and the ID of their manager. Some employees do not have a manager (manager_id is null). 
```

```
Input:
Employees table:
+-------------+-----------+------------+--------+
| employee_id | name      | manager_id | salary |
+-------------+-----------+------------+--------+
| 3           | Mila      | 9          | 60301  |
| 12          | Antonella | null       | 31000  |
| 13          | Emery     | null       | 67084  |
| 1           | Kalel     | 11         | 21241  |
| 9           | Mikaela   | null       | 50937  |
| 11          | Joziah    | 6          | 28485  |
+-------------+-----------+------------+--------+
Output:
+-------------+
| employee_id |
+-------------+
| 11          |
+-------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

"Manager left" means the pointer leads **nowhere**: there's a `manager_id`, but no row with that id. That's an anti-join on the table itself.

| The statement says | Which really means |
|---|---|
| "salary is strictly less than $30000" | `salary < 30000` |
| "manager left … their information is deleted" | `manager_id` is set, but no row has `employee_id = manager_id` |
| "Some employees do not have a manager (manager_id is null)" | No manager ≠ a manager who left — these must **not** be reported |
| "ordered by employee_id" | Checked |

Joziah (11) points at manager 6, and there's no employee 6 — he's the answer. Kalel's manager, 11, still exists.

🤔 **Before you open the next section:** an employee with `manager_id = NULL` — does their manager "not exist"? Should they count?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`NOT IN` a subquery** | `manager_id NOT IN (SELECT employee_id FROM Employees)` | ✅ Reads like the statement; `NULL` managers drop out on their own |
| `NOT EXISTS` | `manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 … WHERE m.employee_id = e.manager_id)` | ✅ The safest anti-join — needs the explicit `IS NOT NULL` |
| `LEFT JOIN … IS NULL` | `LEFT JOIN Employees m ON m.employee_id = e.manager_id WHERE m.employee_id IS NULL` | ⚠️ Correct only with `AND e.manager_id IS NOT NULL` added |

**The decision: `NOT IN`.** It's safe here for two reasons: `employee_id` is never `NULL` (so the subquery can't poison `NOT IN`), and for an employee with no manager, `NULL NOT IN (…)` is unknown — so `WHERE` drops them, which is exactly right.

The left-join form needs care. Without the extra `IS NOT NULL`, an employee with **no** manager also finds no match:

| `employee_id` | `manager_id` | `m.employee_id` |
|---|---|---|
| 11 | 6 | `NULL` |
| 14 | `NULL` | `NULL` |

Ann has no manager at all — she shouldn't be reported.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT employee_id
```

```sql
FROM Employees
```

```sql
WHERE salary < 30000
  AND manager_id NOT IN (SELECT employee_id FROM Employees)
```

**Underpaid, and the manager is gone.** The subquery lists every id still in the table. `NOT IN` is true only when the manager's id isn't on that list.

For a `NULL` `manager_id`, `NOT IN` is unknown (`NULL` compared with anything is unknown), so those rows are dropped without extra code.
→ [in-subquery](../sql/in-subquery.md) · [anti-join](../sql/anti-join.md) · [null-is-null](../sql/null-is-null.md)

```sql
ORDER BY employee_id;
```

→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT employee_id
FROM Employees
WHERE salary < 30000
  AND manager_id NOT IN (SELECT employee_id FROM Employees)
ORDER BY employee_id;
```

</details>

**Trace it** — both conditions per row (`NULL` = unknown):

| `employee_id` | `manager_id` | `salary` | `salary < 30000` | `manager gone?` |
|---|---|---|---|---|
| 3 | 9 | 60301 | 0 | 0 |
| 12 | `NULL` | 31000 | 0 | `NULL` |
| 13 | `NULL` | 67084 | 0 | `NULL` |
| 1 | 11 | 21241 | 1 | 0 |
| 9 | `NULL` | 50937 | 0 | `NULL` |
| 11 | 6 | 28485 | 1 | 1 |

Only Joziah (11) passes both.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — MySQL materialises the subquery into a hashed set of ids once, then tests each row against it.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the set of existing ids.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A manager who left has no row, so I need employees whose `manager_id` isn't among the existing `employee_id`s — `NOT IN` a subquery — combined with `salary < 30000`. Employees with no manager have a `NULL` `manager_id`; `NOT IN` evaluates to unknown for them, so they're correctly excluded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "When is `NOT IN` dangerous?" | When the **subquery** can return `NULL`: `x NOT IN (1, NULL)` is never true, and the query returns nothing. `employee_id` can't be `NULL` here; `NOT EXISTS` is safe either way. |
| "Write it as a left join." | `LEFT JOIN Employees m ON m.employee_id = e.manager_id WHERE m.employee_id IS NULL AND e.manager_id IS NOT NULL AND e.salary < 30000`. |
| "Count reports per departed manager?" | Same filter without the salary condition, then `GROUP BY manager_id`. |
| "Re-assign them to the CEO?" | An `UPDATE … WHERE manager_id NOT IN (…)` — MySQL needs the subquery wrapped in a derived table to read the table it's updating. |

**Traps:**

- **Left join without `manager_id IS NOT NULL`** — reports employees who never had a manager.
- **`NOT IN` against a nullable column** — fine here, a classic bug elsewhere.
- **`<=` 30000** — "strictly less".

**This same move shows up in:** [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md) (the anti-join, across two tables) · [Managers with at Least 5 Direct Reports](570-managers-with-at-least-5-direct-reports.md) (following `managerId` within one table) · [Find Customer Referee](584-find-customer-referee.md) (`NULL` in a comparison).

</details>

---
