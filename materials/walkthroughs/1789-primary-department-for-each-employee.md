# 1789. Primary Department for Each Employee

**Easy** · [LeetCode](https://leetcode.com/problems/primary-department-for-each-employee/) · [Solution file (no hints)](../../problems/1500-1999/1789.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Report each employee's primary department. An employee in several departments marks one with `primary_flag = 'Y'`; an employee in **only one** department has `'N'` there — report that one. Any order.

```
Table: Employee
+---------------+---------+
| Column Name   |  Type   |
+---------------+---------+
| employee_id   | int     |
| department_id | int     |
| primary_flag  | varchar |
+---------------+---------+
(employee_id, department_id) is the primary key (combination of columns with unique values) for this table.
employee_id is the id of the employee.
department_id is the id of the department to which the employee belongs.
primary_flag is an ENUM (category) of type ('Y', 'N'). If the flag is 'Y', the department is the primary department for the employee. If the flag is 'N', the department is not the primary.
```

```
Input:
Employee table:
+-------------+---------------+--------------+
| employee_id | department_id | primary_flag |
+-------------+---------------+--------------+
| 1           | 1             | N            |
| 2           | 1             | Y            |
| 2           | 2             | N            |
| 3           | 3             | N            |
| 4           | 2             | N            |
| 4           | 3             | Y            |
| 4           | 4             | N            |
+-------------+---------------+--------------+
Output:
+-------------+---------------+
| employee_id | department_id |
+-------------+---------------+
| 1           | 1             |
| 2           | 1             |
| 3           | 3             |
| 4           | 3             |
+-------------+---------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Two kinds of rows qualify, and you can only recognise the second kind by looking at **other rows**.

| The statement says | Which really means |
|---|---|
| "If the flag is 'Y', the department is the primary" | Case 1: any row with `primary_flag = 'Y'` |
| "when an employee belongs to only one department, their primary column is 'N'" | Case 2: rows of employees who have exactly one row — whatever the flag |
| "employees who belong to one department" | Needs a **count per employee** — a property of the group, not the row |
| employee 1 and employee 3 | Only `'N'` rows, but both appear in the output |

Case 1 is a plain row filter. Case 2 needs `GROUP BY employee_id HAVING COUNT(*) = 1`. Combine the two.

🤔 **Before you open the next section:** looking only at employee 3's single row (`3, 3, N`), can you tell it's their only department?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Flag `OR` single-department subquery** | `WHERE primary_flag = 'Y' OR employee_id IN (… HAVING COUNT(*) = 1)` | ✅ Both cases in one filter |
| `UNION` of the two cases | `… WHERE primary_flag = 'Y' UNION … GROUP BY employee_id HAVING COUNT(*) = 1` | ✅ Each case on its own — very readable |
| Window count | `COUNT(*) OVER (PARTITION BY employee_id) AS n`, then `WHERE primary_flag = 'Y' OR n = 1` | ✅ The count lands on every row |
| `WHERE primary_flag = 'Y'` alone | case 1 only | ❌ Misses employees 1 and 3 |

**The decision: the `OR` with a subquery.** It's one pass over the table that reads like the statement.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT employee_id, department_id
```

```sql
FROM Employee
```

```sql
WHERE primary_flag = 'Y'
   OR employee_id IN (
        SELECT employee_id
        FROM Employee
        GROUP BY employee_id
        HAVING COUNT(*) = 1
   );
```

**Either flagged primary, or the employee's only department.** The subquery returns the ids of employees with exactly one row:

| `employee_id` | `departments` |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 3 |

Employees 1 and 3 have one department each. `IN` checks whether the current row's employee is in that list.
→ [in-subquery](../sql/in-subquery.md) · [having](../sql/having.md) · [logical-operators](../sql/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
   OR employee_id IN (
        SELECT employee_id
        FROM Employee
        GROUP BY employee_id
        HAVING COUNT(*) = 1
   );
```

</details>

**Trace it** — both conditions for every row:

| `employee_id` | `department_id` | `primary_flag` | `flag Y?` | `only dept?` |
|---|---|---|---|---|
| 1 | 1 | N | 0 | 1 |
| 2 | 1 | Y | 1 | 0 |
| 2 | 2 | N | 0 | 0 |
| 3 | 3 | N | 0 | 1 |
| 4 | 2 | N | 0 | 0 |
| 4 | 3 | Y | 1 | 0 |
| 4 | 4 | N | 0 | 0 |

Employees 2 and 4 pass on the flag; 1 and 3 pass because they have only one department.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one grouping pass to find single-department employees (materialised into a hashed set), then one pass over the rows testing both conditions.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(e)</summary>

**O(e)** for e employees in the grouping and the materialised id set.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A row is a primary department if it's flagged `'Y'`, or if it's the employee's only department. The second case needs a count per employee, so I find employees with `COUNT(*) = 1` in a subquery and `OR` that with the flag."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "With a window function?" | `COUNT(*) OVER (PARTITION BY employee_id)` in a subquery, then `WHERE primary_flag = 'Y' OR n = 1`. |
| "What if a multi-department employee forgot to flag one?" | They'd disappear. A fallback like "lowest department id" needs ranking: `ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY primary_flag = 'Y' DESC, department_id)`. |
| "Count employees per primary department." | Wrap this query and `GROUP BY department_id`. |
| "Why not `HAVING` on the outer query?" | The outer rows aren't grouped — you need individual rows (the department), so the count lives in a subquery. |

**Traps:**

- **Only the `'Y'` filter** — single-department employees vanish.
- **`GROUP BY employee_id` in the outer query** — you'd need an aggregate to choose the department, and `ONLY_FULL_GROUP_BY` won't let you just select it.

**This same move shows up in:** [Biggest Single Number](619-biggest-single-number.md) (`HAVING COUNT(*) = 1`) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (a grouped subquery choosing rows) · [Find Customer Referee](584-find-customer-referee.md) (two ways to qualify, joined with `OR`).

</details>

---
