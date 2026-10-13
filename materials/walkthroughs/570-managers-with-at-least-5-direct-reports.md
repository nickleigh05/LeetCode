# 570. Managers with at Least 5 Direct Reports

**Medium** · [LeetCode](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/) · [Solution file (no hints)](../../problems/0500-0999/570.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find the names of managers with **at least five** direct reports. Any order.

```
Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the name of an employee, their department, and the id of their manager.
If managerId is null, then the employee does not have a manager.
No employee will be the manager of themself.
```

```
Input:
Employee table:
+-----+-------+------------+-----------+
| id  | name  | department | managerId |
+-----+-------+------------+-----------+
| 101 | John  | A          | null      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |
+-----+-------+------------+-----------+
Output:
+------+
| name |
+------+
| John |
+------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The table holds two roles at once: every row is an employee, and `managerId` points at another row in the **same** table. Counting reports means grouping by that pointer.

| The statement says | Which really means |
|---|---|
| `managerId` | A reference to another row's `id` in this same table |
| "direct reports" | Rows whose `managerId` is the manager's `id` — one level only |
| "at least five" | `COUNT(*) >= 5`, a condition on a **group**, not a row → `HAVING` |
| return the manager's **name** | The count is per `managerId`, but the answer is the manager's own row |
| names aren't unique | Two managers called John must stay two separate groups — group by `id` |

🤔 **Before you open the next section:** you can count reports with `GROUP BY managerId`. How do you then get the *manager's* name, which lives on a different row?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Self-join, group by manager** | `Employee m JOIN Employee e ON e.managerId = m.id … GROUP BY m.id, m.name HAVING COUNT(*) >= 5` | ✅ One query, manager and reports side by side |
| `IN` subquery | `WHERE id IN (SELECT managerId … GROUP BY managerId HAVING COUNT(*) >= 5)` | ✅ Clear two-step logic: find ids, then names |
| Join to a grouped derived table | `JOIN (SELECT managerId … HAVING …) r ON r.managerId = m.id` | ✅ Same idea, as a join |
| `GROUP BY managerId`, select `name` | `SELECT name … GROUP BY managerId` | ❌ That `name` is a report's, not the manager's — and MySQL rejects it |

**The decision: the self-join.** Each joined row is one (manager, report) pair, so counting rows per manager counts reports.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT m.name
```

```sql
FROM Employee m
```

```sql
JOIN Employee e
    ON e.managerId = m.id
```

**Pair every manager with each of their reports.** `m` plays the manager, `e` the employee. A manager with five reports produces five joined rows; an employee who manages nobody produces none.
→ [self-join](../sql/self-join.md)

```sql
GROUP BY m.id, m.name
```

**One group per manager.** Group by `m.id` so that two managers with the same name stay separate. `m.name` has to be listed too: LeetCode's table declares no primary key, so MySQL can't prove that `name` depends on `id`, and its default `ONLY_FULL_GROUP_BY` mode rejects `GROUP BY m.id` on its own.
→ [group-by](../sql/group-by.md)

```sql
HAVING COUNT(*) >= 5;
```

**Keep groups with five or more rows.** `WHERE` filters individual rows before grouping; `HAVING` filters whole groups after. A count only exists after grouping, so this has to be `HAVING`.
→ [having](../sql/having.md) · [execution-order](../sql/execution-order.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT m.name
FROM Employee m
JOIN Employee e
    ON e.managerId = m.id
GROUP BY m.id, m.name
HAVING COUNT(*) >= 5;
```

</details>

**Trace it** — the (manager, report) pairs the join produces:

| `m.id` | `manager` | `report` |
|---|---|---|
| 101 | John | Dan |
| 101 | John | James |
| 101 | John | Amy |
| 101 | John | Anne |
| 101 | John | Ron |

Grouped by manager:

| `id` | `name` | `reports` |
|---|---|---|
| 101 | John | 5 |

John has 5 reports, so he passes `HAVING COUNT(*) >= 5`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n employees: a hash join on `e.managerId = m.id`, where each employee matches at most one manager, then one grouping pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the join's hash table and the per-manager counters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Managers and reports are rows of the same table, so I self-join: manager on one side, reports on the other, matched on `managerId = id`. Each joined row is one report, so I group by the manager's id and keep groups with `HAVING COUNT(*) >= 5`. I group by id, not name, because names can repeat."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Include the number of reports." | `SELECT m.name, COUNT(*) AS reports …`. |
| "What if a `managerId` points at someone not in the table?" | The join finds no manager row, so that group never forms — no name to return. The `IN` version behaves the same. |
| "Count **all** reports, not just direct ones?" | That's a tree walk — a recursive CTE (`WITH RECURSIVE`). |
| "Why not `WHERE COUNT(*) >= 5`?" | `WHERE` runs before grouping, when no count exists yet. MySQL rejects aggregates in `WHERE`. |
| "Managers with **no** reports?" | `LEFT JOIN` the reports and keep `e.id IS NULL`. |

**Traps:**

- **Grouping by `name`** — merges different managers who share a name.
- **`SELECT name … GROUP BY managerId`** — selects a report's name, and fails under `ONLY_FULL_GROUP_BY`.
- **`WHERE` for the count** — aggregates belong in `HAVING`.
- **`> 5`** — "at least five" includes exactly five.

**This same move shows up in:** [The Number of Employees Which Report to Each Employee](1731-the-number-of-employees-which-report-to-each-employee.md) (the same self-join, with counts and averages) · [Employees Whose Manager Left the Company](1978-employees-whose-manager-left-the-company.md) (following `managerId` to a missing row) · [Classes With at Least 5 Students](596-classes-with-at-least-5-students.md) (`HAVING COUNT >= 5` without a join).

</details>

---
