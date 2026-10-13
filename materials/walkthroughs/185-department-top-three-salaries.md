# 185. Department Top Three Salaries

**Hard** · [LeetCode](https://leetcode.com/problems/department-top-three-salaries/) · [Solution file (no hints)](../../problems/0001-0499/185.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A **high earner** has a salary among the **top three distinct salaries** in their department. List every high earner with their department name and salary. Any order.

```
Table: Employee
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id is the primary key (column with unique values) for this table.
departmentId is a foreign key (reference column) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.

Table: Department
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID of a department and its name.
```

```
Input:
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+
Department table:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
Output:
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

"Top N **per group**" is the most common window-function question in online assessments. The word that decides which window function you need is **unique**.

| The statement says | Which really means |
|---|---|
| "in each of the company's departments" | Rank separately per department → `PARTITION BY departmentId` |
| "top three **unique** salaries" | Ties share a position, and the next salary takes the next position — no gaps |
| Joe and Randy both earn 85000 | Both are "second"; Will at 70000 is "third" and still qualifies |
| department names in the output | Join `Department` for `name` |
| columns `Department`, `Employee`, `Salary` | Alias each — capitalised |

Three ranking functions differ exactly on ties:

| `name` | `salary` | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|---|
| Max | 90000 | 1 | 1 | 1 |
| Joe | 85000 | 2 | 2 | 2 |
| Randy | 85000 | 3 | 2 | 2 |
| Will | 70000 | 4 | 4 | 3 |
| Janet | 69000 | 5 | 5 | 4 |

`DENSE_RANK` counts distinct salaries — 90000 is 1, 85000 is 2, 70000 is 3 — which is what "top three unique salaries" means.

🤔 **Before you open the next section:** with `RANK`, what number does Will get — and would `rank <= 3` keep him?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`DENSE_RANK()` per department** | `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)`, keep `<= 3` | ✅ Ties share a rank, no gaps — "top three unique salaries" exactly |
| Correlated count | keep a row if fewer than 3 distinct higher salaries exist in its department | ✅ The classic pre-window answer; O(n²) |
| `RANK()` | | ❌ Gaps after ties — Will gets 4 and is dropped |
| `ROW_NUMBER()` | | ❌ Breaks ties arbitrarily — Joe or Randy is dropped |
| `ORDER BY salary DESC LIMIT 3` | | ❌ Three rows for the whole company, not per department |

**The decision: `DENSE_RANK`.** It's the window function whose ranks count *distinct values*.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
```

**The output columns, aliased to match.** `d.name` and `e.name` would both be called `name` without aliases.
→ [aliases](../sql/aliases.md)

```sql
FROM (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS rnk
    FROM Employee
) e
```

**Rank salaries within each department.** `PARTITION BY departmentId` restarts the ranking for every department; `ORDER BY salary DESC` puts the highest salary at rank 1. The ranking has to live in a subquery: window functions are computed after `WHERE`, so you can't filter on `rnk` in the same query.
→ [ranking-functions](../sql/ranking-functions.md) · [top-n-per-group](../sql/top-n-per-group.md) · [derived-tables](../sql/derived-tables.md)

```sql
JOIN Department d ON d.id = e.departmentId
```

**Fetch the department name.**
→ [inner-join](../sql/inner-join.md)

```sql
WHERE e.rnk <= 3;
```

**Keep the top three distinct salaries.** With `DENSE_RANK`, `rnk <= 3` keeps every employee earning one of the three highest distinct salaries — any number of people.
→ [where](../sql/where.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
FROM (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS rnk
    FROM Employee
) e
JOIN Department d ON d.id = e.departmentId
WHERE e.rnk <= 3;
```

</details>

**Trace it** — IT: Max (rank 1), Joe and Randy (2), Will (3) are kept; Janet (4) isn't. Sales has only two salaries, so both employees are kept.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** — sorting employees by (department, salary) for the window, then a linear pass to assign ranks and a hash join to `Department`. The correlated-count version is **O(n²)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the sorted rows and their ranks.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Top three *distinct* salaries per department is a dense rank: `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)` in a subquery, keep ranks up to 3, and join `Department` for the name. `RANK` would leave gaps after ties and `ROW_NUMBER` would break ties arbitrarily — both drop people who should be included."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Top three *employees* per department, ties broken by name?" | `ROW_NUMBER() OVER (PARTITION BY departmentId ORDER BY salary DESC, name)`, keep `<= 3`. |
| "Without window functions?" | `WHERE (SELECT COUNT(DISTINCT e2.salary) FROM Employee e2 WHERE e2.departmentId = e.departmentId AND e2.salary > e.salary) < 3`. |
| "Only the single highest earner(s)?" | `rnk = 1` — see [Department Highest Salary](184-department-highest-salary.md). |
| "Departments with no employees?" | They can't appear in a list of employees; a `LEFT JOIN` from `Department` would give them a `NULL` row. |

**Traps:**

- **`RANK`** — drops the third distinct salary when the second is tied.
- **`ROW_NUMBER`** — drops tied employees.
- **Filtering the rank in the same `SELECT`** — window results aren't available in `WHERE`.
- **Missing `PARTITION BY`** — ranks the whole company at once.

**This same move shows up in:** [Department Highest Salary](184-department-highest-salary.md) (the top-1 version) · [Rank Scores](178-rank-scores.md) (`DENSE_RANK` without partitions) · [Nth Highest Salary](177-nth-highest-salary.md) (the nth distinct value).

</details>

---
