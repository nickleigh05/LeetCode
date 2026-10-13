# 1731. The Number of Employees Which Report to Each Employee

**Easy** · [LeetCode](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/) · [Solution file (no hints)](../../problems/1500-1999/1731.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A **manager** is anyone with at least one direct report. For each manager, report their id and name, how many people report to them, and the average age of those reports rounded to the nearest integer. Order by `employee_id`.

```
Table: Employees
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| employee_id | int      |
| name        | varchar  |
| reports_to  | int      |
| age         | int      |
+-------------+----------+
employee_id is the column with unique values for this table.
This table contains information about the employees and the id of the manager they report to. Some employees do not report to anyone (reports_to is null). 
```

```
Input:
Employees table:
+-------------+---------+------------+-----+
| employee_id | name    | reports_to | age |
|-------------|---------|------------|-----|
| 1           | Michael | null       | 45  |
| 2           | Alice   | 1          | 38  |
| 3           | Bob     | 1          | 42  |
| 4           | Charlie | 2          | 34  |
| 5           | David   | 2          | 40  |
| 6           | Eve     | 3          | 37  |
| 7           | Frank   | null       | 50  |
| 8           | Grace   | null       | 48  |
+-------------+---------+------------+-----+
Output:
+-------------+---------+---------------+-------------+
| employee_id | name    | reports_count | average_age |
| ----------- | ------- | ------------- | ----------- |
| 1           | Michael | 2             | 40          |
| 2           | Alice   | 2             | 37          |
| 3           | Bob     | 1             | 37          |
+-------------+---------+---------------+-------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The manager's details (id, name) and the facts you aggregate (count, age) live on **different rows** of the same table. Self-join, then group by the manager.

| The statement says | Which really means |
|---|---|
| `reports_to` is another employee's id | A pointer into the same table → self-join |
| "a manager … has at least 1 other employee reporting" | Only people who appear as someone's `reports_to` — an inner join drops the rest |
| "number of employees who report directly" | `COUNT(*)` of the report rows |
| "average age of the reports rounded to the nearest integer" | `ROUND(AVG(e.age))` — the **reports'** ages, not the manager's |
| "ordered by employee_id" | Checked |

🤔 **Before you open the next section:** after joining `Employees m` (manager) to `Employees e` (report), which alias's `age` do you average?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Self-join, group by manager** | `Employees m JOIN Employees e ON e.reports_to = m.employee_id` | ✅ Manager columns and report columns on one row |
| Aggregate first, then join | group `Employees` by `reports_to`, join the result to the manager rows | ✅ Same answer; the aggregation happens before the join |
| `AVG(m.age)` | the manager's own age | ❌ Averages the wrong person |
| `LEFT JOIN` | keeps non-managers | ❌ Adds rows with a count of 1 and a `NULL` age — not managers at all |

**The decision: the self-join.** Each joined row is one (manager, report) pair, so per-manager aggregates are aggregates over that manager's reports.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT m.employee_id, m.name,
       COUNT(*) AS reports_count,
       ROUND(AVG(e.age)) AS average_age
```

**The manager's identity, plus two aggregates over their reports.** `ROUND(x)` with no second argument rounds to a whole number; for exact decimals, MySQL rounds halves away from zero (38.5 → 39).
→ [aggregate-functions](../sql/aggregate-functions.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Employees m
```

```sql
JOIN Employees e
    ON e.reports_to = m.employee_id
```

**Pair each manager with each of their reports.** `m` is the manager, `e` the employee who reports to them. Employees nobody reports to never appear on the `m` side.
→ [self-join](../sql/self-join.md)

```sql
GROUP BY m.employee_id, m.name
```

**One group per manager.** `m.name` is listed because it's selected; LeetCode's table declares no primary key, so MySQL won't infer that the name depends on the id.
→ [group-by](../sql/group-by.md)

```sql
ORDER BY m.employee_id;
```

→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT m.employee_id, m.name,
       COUNT(*) AS reports_count,
       ROUND(AVG(e.age)) AS average_age
FROM Employees m
JOIN Employees e
    ON e.reports_to = m.employee_id
GROUP BY m.employee_id, m.name
ORDER BY m.employee_id;
```

</details>

**Trace it** — Example 2's (manager, report) pairs:

| `manager` | `name` | `report` | `age` |
|---|---|---|---|
| 1 | Michael | Alice | 38 |
| 1 | Michael | Bob | 42 |
| 2 | Alice | Charlie | 34 |
| 2 | Alice | David | 40 |
| 3 | Bob | Eve | 37 |

Grouped:

| `employee_id` | `AVG(e.age)` | `ROUND(AVG(e.age))` |
|---|---|---|
| 1 | 40.0000 | 40 |
| 2 | 37.0000 | 37 |
| 3 | 37.0000 | 37 |

Michael: (38 + 42) / 2 = 40. Alice: (34 + 40) / 2 = 37. Bob: 37. Frank and Grace have no reports, so they aren't managers.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — a hash join on `reports_to = employee_id`, where each employee matches at most one manager, then one grouping pass and a sort of the managers.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the join's hash table, plus one accumulator per manager.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Managers and reports are rows of the same table, so I self-join — manager on one side, reports on the other — group by the manager, and take `COUNT(*)` and `ROUND(AVG(e.age))` over the reports. The inner join leaves out anyone without reports, which is exactly the definition of a manager."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Include employees with zero reports?" | `LEFT JOIN`, `COUNT(e.employee_id)` (0 for them), and `AVG` will be `NULL`. |
| "Average age **including** the manager?" | Different groups — `UNION ALL` the manager's own row into the set before averaging. |
| "Indirect reports too?" | A recursive CTE walking down the tree. |
| "How does MySQL round 38.5?" | Up, to 39 — exact decimals round halves away from zero. (Floats can differ; this column is an integer, so `AVG` is exact.) |

**Traps:**

- **`AVG(m.age)`** — the manager's age.
- **`LEFT JOIN`** — makes everyone a "manager".
- **Missing `ORDER BY`.**

**This same move shows up in:** [Managers with at Least 5 Direct Reports](570-managers-with-at-least-5-direct-reports.md) (the same self-join with `HAVING`) · [Employees Whose Manager Left the Company](1978-employees-whose-manager-left-the-company.md) (following the pointer to a missing row) · [Project Employees I](1075-project-employees-i.md) (`AVG` over joined rows).

</details>

---
