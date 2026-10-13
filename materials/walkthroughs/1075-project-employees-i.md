# 1075. Project Employees I

**Easy** · [LeetCode](https://leetcode.com/problems/project-employees-i/) · [Solution file (no hints)](../../problems/1000-1499/1075.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each project, report the average experience of the employees working on it, rounded to 2 decimals. Any order.

```
Table: Project
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| project_id  | int     |
| employee_id | int     |
+-------------+---------+
(project_id, employee_id) is the primary key of this table.
employee_id is a foreign key to Employee table.
Each row of this table indicates that the employee with employee_id is working on the project with project_id.

Table: Employee
+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| employee_id      | int     |
| name             | varchar |
| experience_years | int     |
+------------------+---------+
employee_id is the primary key of this table. It's guaranteed that experience_years is not NULL.
Each row of this table contains information about one employee.
```

```
Input:
Project table:
+-------------+-------------+
| project_id  | employee_id |
+-------------+-------------+
| 1           | 1           |
| 1           | 2           |
| 1           | 3           |
| 2           | 1           |
| 2           | 4           |
+-------------+-------------+
Employee table:
+-------------+--------+------------------+
| employee_id | name   | experience_years |
+-------------+--------+------------------+
| 1           | Khaled | 3                |
| 2           | Ali    | 2                |
| 3           | John   | 1                |
| 4           | Doe    | 2                |
+-------------+--------+------------------+
Output:
+-------------+---------------+
| project_id  | average_years |
+-------------+---------------+
| 1           | 2.00          |
| 2           | 2.50          |
+-------------+---------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The textbook join-then-aggregate: bring the number you need onto the rows you're grouping, then average it.

| The statement says | Which really means |
|---|---|
| `Project` links projects to employees | One row per (project, employee) — the thing you group |
| `experience_years` lives in `Employee` | Join to fetch it |
| "average experience years … for each project" | `GROUP BY project_id`, `AVG(experience_years)` |
| "rounded to 2 digits" | `ROUND(…, 2)` |
| "guaranteed that `experience_years` is not NULL" | `AVG` skips `NULL`s — no surprise here, but that guarantee is why |

🤔 **Before you open the next section:** after joining, how many rows does project 1 have, and what are their experience values?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Join, then `AVG`** | `JOIN Employee e … GROUP BY p.project_id`, `ROUND(AVG(e.experience_years), 2)` | ✅ The direct translation |
| `SUM` ÷ `COUNT(*)` | `ROUND(SUM(e.experience_years) / COUNT(*), 2)` | ✅ Same result here; `AVG` says it in one word |
| `AVG` without `ROUND` | `AVG(e.experience_years)` | ❌ `2.0000` instead of `2.00` |

**The decision: join, then `ROUND(AVG(…), 2)`.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT p.project_id,
       ROUND(AVG(e.experience_years), 2) AS average_years
```

**The average, rounded.** `AVG` adds the group's values and divides by how many there are. On integers, MySQL returns a decimal with 4 digits after the point, and `ROUND(…, 2)` brings it to two.
→ [aggregate-functions](../sql/aggregate-functions.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Project p
```

```sql
JOIN Employee e
    ON p.employee_id = e.employee_id
```

**Fetch each assignee's experience.** Every `Project` row finds exactly one employee, so the join keeps one row per assignment.
→ [inner-join](../sql/inner-join.md)

```sql
GROUP BY p.project_id;
```

**One output row per project.**
→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT p.project_id,
       ROUND(AVG(e.experience_years), 2) AS average_years
FROM Project p
JOIN Employee e
    ON p.employee_id = e.employee_id
GROUP BY p.project_id;
```

</details>

**Trace it** — the joined rows, grouped by project:

| `project_id` | `employee_id` | `name` | `experience_years` |
|---|---|---|---|
| 1 | 1 | Khaled | 3 |
| 1 | 2 | Ali | 2 |
| 1 | 3 | John | 1 |
| 2 | 1 | Khaled | 3 |
| 2 | 4 | Doe | 2 |

Project 1: (3 + 2 + 1) / 3 = 2.00. Project 2: (3 + 2) / 2 = 2.50.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(p + e)</summary>

**O(p + e)** for p assignments and e employees — a hash join on `employee_id`, then one grouping pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(e)</summary>

**O(e)** for the hash table over employees, plus one running sum and count per project.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Experience lives in `Employee`, so I join it onto the project assignments, group by project, and take `ROUND(AVG(experience_years), 2)`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `experience_years` could be `NULL`?" | `AVG` would skip those employees entirely. To count them as 0, use `AVG(IFNULL(experience_years, 0))`. |
| "The project(s) with the most employees?" | `GROUP BY project_id HAVING COUNT(*) = (SELECT MAX(cnt) FROM (SELECT COUNT(*) AS cnt …) t)` — or rank with a window function. |
| "The most experienced employee on each project?" | A per-group maximum that returns the whole row — see [Department Highest Salary](184-department-highest-salary.md). |
| "Projects with no employees?" | They'd need their own table to appear; `Project` only lists assignments. |

**Traps:**

- **Forgetting `ROUND`** — four decimals instead of two.
- **Grouping by employee** — gives one row per person, not per project.

**This same move shows up in:** [Average Time of Process per Machine](1661-average-time-of-process-per-machine.md) (join, then `AVG` per group) · [Queries Quality and Percentage](1211-queries-quality-and-percentage.md) (`AVG` of a computed value) · [Average Selling Price](1251-average-selling-price.md) (when a plain average is the wrong one).

</details>

---
