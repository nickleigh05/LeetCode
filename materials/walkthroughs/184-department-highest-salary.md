# 184. Department Highest Salary

**Medium** · [LeetCode](https://leetcode.com/problems/department-highest-salary/) · [Solution file (no hints)](../../problems/0001-0499/184.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find the employees with the **highest salary in each department** — all of them, if several tie. Any order.

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
departmentId is a foreign key (reference columns) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.

Table: Department
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table. It is guaranteed that department name is not NULL.
Each row of this table indicates the ID of a department and its name.
```

```
Input:
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Jim   | 90000  | 1            |
| 3  | Henry | 80000  | 2            |
| 4  | Sam   | 60000  | 2            |
| 5  | Max   | 90000  | 1            |
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
| IT         | Jim      | 90000  |
| Sales      | Henry    | 80000  |
| IT         | Max      | 90000  |
+------------+----------+--------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The classic "row with the per-group maximum." The maximum is easy to compute; the work is getting back to the **rows** that hold it.

| The statement says | Which really means |
|---|---|
| "highest salary in each of the departments" | `MAX(salary)` per `departmentId` |
| Jim and Max both earn 90000 in IT | Ties all come back — one row each |
| output `Department`, `Employee`, `Salary` | Department name from `Department`, aliases as given |
| `Department` name is not `NULL` | Plain inner join is fine |

🤔 **Before you open the next section:** `SELECT departmentId, MAX(salary) … GROUP BY departmentId` gives one number per department. How do you find *who* earns it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Tuple `IN` a grouped subquery** | `WHERE (e.departmentId, e.salary) IN (SELECT departmentId, MAX(salary) … GROUP BY departmentId)` | ✅ Every row matching its department's maximum |
| `RANK()` per department | `RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) = 1` | ✅ Ties share rank 1 |
| Correlated `MAX` | `WHERE e.salary = (SELECT MAX(salary) FROM Employee e2 WHERE e2.departmentId = e.departmentId)` | ✅ Readable; one subquery per row |
| `GROUP BY` with `MAX` and a name | `SELECT d.name, e.name, MAX(e.salary) … GROUP BY d.id` | ❌ The name isn't tied to the max |

**The decision: the tuple `IN`.** Compute each department's maximum once, then keep every employee whose (department, salary) matches.

**Why the `GROUP BY` shortcut is wrong.** `MAX(e.salary)` and `e.name` are computed independently. MySQL rejects it under `ONLY_FULL_GROUP_BY`; forced through with `ANY_VALUE`, it returns any name from the group next to the maximum:

| `Department` | `Employee` | `Salary` |
|---|---|---|
| IT | Joe | 90000 |
| Sales | Henry | 80000 |

Joe earns 70000, not 90000 — and Max is missing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
```

→ [aliases](../sql/aliases.md)

```sql
FROM Employee e
```

```sql
JOIN Department d ON d.id = e.departmentId
```

→ [inner-join](../sql/inner-join.md)

```sql
WHERE (e.departmentId, e.salary) IN (
    SELECT departmentId, MAX(salary)
    FROM Employee
    GROUP BY departmentId
);
```

**Keep employees earning their department's maximum.** The subquery produces one (department, max salary) pair per department:

| `departmentId` | `MAX(salary)` |
|---|---|
| 1 | 90000 |
| 2 | 80000 |

`(e.departmentId, e.salary) IN (…)` keeps a row only if its pair is in that list — which includes both Jim and Max.
→ [in-subquery](../sql/in-subquery.md) · [first-row-per-group](../sql/first-row-per-group.md) · [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
FROM Employee e
JOIN Department d ON d.id = e.departmentId
WHERE (e.departmentId, e.salary) IN (
    SELECT departmentId, MAX(salary)
    FROM Employee
    GROUP BY departmentId
);
```

</details>

**Trace it** — IT's maximum is 90000 (Jim and Max); Sales's is 80000 (Henry). Three rows.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one grouping pass for the maxima, a hashed membership test per employee, and a hash join to `Department`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d)</summary>

**O(d)** for d (department, max) pairs.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I compute each department's max salary in a grouped subquery, then keep every employee whose (department, salary) pair is in it — so ties all come back — and join `Department` for the name. Grouping the outer query wouldn't work, because the name isn't tied to the max."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "With a window function?" | `RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)` and keep 1 — `RANK` or `DENSE_RANK`, so ties survive. |
| "Only one employee per department?" | `ROW_NUMBER()` with a tiebreaker, e.g. `ORDER BY salary DESC, id`. |
| "Top three salaries per department?" | [Department Top Three Salaries](185-department-top-three-salaries.md). |
| "Lowest earner?" | `MIN` instead of `MAX`. |

**Traps:**

- **`GROUP BY` with a non-aggregated name** — the wrong person, or an error.
- **Matching on salary alone** — `WHERE salary IN (SELECT MAX(salary) … GROUP BY departmentId)` would match a Sales employee who happens to earn IT's maximum.
- **`ROW_NUMBER() = 1`** — drops ties.

**This same move shows up in:** [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (rows matching a per-group minimum) · [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (each customer's first row) · [Department Top Three Salaries](185-department-top-three-salaries.md) (top N per group).

</details>

---
