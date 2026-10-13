# 176. Second Highest Salary

**Medium** · [LeetCode](https://leetcode.com/problems/second-highest-salary/) · [Solution file (no hints)](../../problems/0001-0499/176.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find the second highest **distinct** salary, as `SecondHighestSalary`. If there isn't one, return `null`.

```
Table: Employee
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
```

```
Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

```
Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| null                |
+---------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The query itself is short. What makes it Medium is two edge cases: duplicate salaries, and **no second salary at all**.

| The statement says | Which really means |
|---|---|
| "second highest **distinct** salary" | Collapse duplicates first — 300, 300, 200 has second highest 200 |
| "If there is no second highest salary, return null" | One row containing `NULL` — not zero rows |
| Example 2: a single employee | Exercises the `null` case |
| output column `SecondHighestSalary` | Alias it exactly |

🤔 **Before you open the next section:** `ORDER BY salary DESC LIMIT 1 OFFSET 1` skips the top salary and takes the next. What does it return when there's only one salary?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LIMIT … OFFSET`, wrapped in a scalar subquery** | `SELECT (SELECT DISTINCT salary … ORDER BY salary DESC LIMIT 1 OFFSET 1) AS …` | ✅ An empty scalar subquery becomes `NULL` |
| `MAX` below the `MAX` | `SELECT MAX(salary) … WHERE salary < (SELECT MAX(salary) FROM Employee)` | ✅ `MAX` of nothing is `NULL`; elegant for "second" specifically |
| `DENSE_RANK` = 2 | rank distinct salaries, keep rank 2, wrap in `MAX` | ✅ Generalises to any N |
| Bare `LIMIT … OFFSET` | `SELECT DISTINCT salary … LIMIT 1 OFFSET 1` | ❌ Returns **no rows** in Example 2 |
| Without `DISTINCT` | `SELECT salary … LIMIT 1 OFFSET 1` | ❌ With salaries 300, 300, 200, returns 300 |

**The decision: `DISTINCT … LIMIT 1 OFFSET 1`, wrapped as a scalar subquery.** It reads as "the second distinct salary," and the wrapper handles the missing case.

In Example 2, the bare query returns nothing at all:

| `salary` |
|---|

Wrapped in `SELECT ( … ) AS SecondHighestSalary`, the same query produces the required `null` row:

| `SecondHighestSalary` |
|---|
| `NULL` |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT (
```

```sql
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
```

**The second distinct salary.** `DISTINCT` collapses equal salaries; `ORDER BY salary DESC` puts the highest first; `OFFSET 1` skips one row and `LIMIT 1` takes the next.

Without `DISTINCT`, a tie at the top is mistaken for second place:

| `salary` |
|---|
| 300 |

→ [distinct](../sql/distinct.md) · [limit-offset](../sql/limit-offset.md) · [nth-highest-value](../sql/nth-highest-value.md)

```sql
) AS SecondHighestSalary;
```

**Turn "no row" into `NULL`.** A subquery used as a value — a **scalar subquery** — evaluates to `NULL` when it returns no rows. The outer `SELECT` has no `FROM`, so it always produces exactly one row.
→ [scalar-subquery](../sql/scalar-subquery.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

</details>

**Trace it** — Example 1's distinct salaries in descending order are 300, 200, 100. Skip one, take one: 200.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** to deduplicate and sort the salaries. The `MAX`-below-`MAX` version is **O(n)** — two scans.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the distinct salaries being sorted; **O(1)** for the `MAX` version.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Distinct salaries in descending order, skip one, take one. I wrap it in a scalar subquery, because when there's no second salary the inner query returns no rows, and the problem wants a `null` row instead. `DISTINCT` matters because a tie at the top isn't a second salary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "The Nth highest?" | `OFFSET N - 1` — see [Nth Highest Salary](177-nth-highest-salary.md), where N comes in as a parameter. |
| "Without `LIMIT`?" | `SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee)`. |
| "Second highest per department?" | `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) = 2` — and decide what to return for departments without one. |
| "Return the employees who earn it?" | `WHERE salary = (this query)`. |

**Traps:**

- **The bare `LIMIT … OFFSET`** — empty result instead of `null`.
- **No `DISTINCT`** — duplicates at the top.
- **`OFFSET 2`** — that's the third highest; the offset counts rows skipped.

**This same move shows up in:** [Nth Highest Salary](177-nth-highest-salary.md) (the same idea, parameterised) · [Biggest Single Number](619-biggest-single-number.md) (returning `null` instead of nothing) · [Department Top Three Salaries](185-department-top-three-salaries.md) (distinct ranking per group).

</details>

---
