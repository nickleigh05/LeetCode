# 177. Nth Highest Salary

**Medium** · [LeetCode](https://leetcode.com/problems/nth-highest-salary/) · [Solution file (no hints)](../../problems/0001-0499/177.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Write a **function** `getNthHighestSalary(N)` that returns the Nth highest **distinct** salary, or `null` if there are fewer than N distinct salaries.

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
n = 2
Output:
+------------------------+
| getNthHighestSalary(2) |
+------------------------+
| 200                    |
+------------------------+
```

```
Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
n = 2
Output:
+------------------------+
| getNthHighestSalary(2) |
+------------------------+
| null                   |
+------------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The same question as [Second Highest Salary](176-second-highest-salary.md), with N as a parameter — and that changes the syntax: the answer lives inside a stored function.

| The statement says | Which really means |
|---|---|
| a function taking `N` | LeetCode's template: `CREATE FUNCTION … RETURNS INT BEGIN RETURN ( … ); END` |
| "nth highest **distinct** salary" | Dedupe, sort descending, skip N − 1, take one |
| "less than n distinct salaries, return null" | The subquery may find no row — `RETURN (subquery)` gives `NULL` then |
| N is a variable | `LIMIT` and `OFFSET` won't accept an expression like `N - 1` |

🤔 **Before you open the next section:** for N = 2, how many rows should `OFFSET` skip?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`SET N = N - 1`, then `LIMIT 1 OFFSET N`** | adjust the variable first, then use it plainly | ✅ The standard answer |
| `DENSE_RANK() = N` | `… FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rk …) t WHERE rk = N` | ✅ No offset arithmetic; still needs `DISTINCT` |
| `OFFSET N - 1` | | ❌ Syntax error — `LIMIT`/`OFFSET` take a literal or a plain variable, not an expression |
| No `DISTINCT` | | ❌ Duplicate salaries shift the positions |

**The decision: decrement N, then `LIMIT 1 OFFSET N`.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
```

**LeetCode's wrapper.** A stored function takes `N`, returns an `INT`, and its body sits between `BEGIN` and `END`.
→ [create-function](../sql/create-function.md)

```sql
  SET N = N - 1;
```

**Turn "Nth" into "skip N − 1".** Inside a stored program you can reassign a parameter with `SET`. This has to happen before the query, because `OFFSET N - 1` isn't valid syntax.

```sql
  RETURN (
      SELECT DISTINCT salary
      FROM Employee
      ORDER BY salary DESC
      LIMIT 1 OFFSET N
  );
```

**The Nth distinct salary — or `NULL`.** Distinct salaries, highest first, skip N − 1 of them, take one. `RETURN (subquery)` returns `NULL` when the subquery has no row, which covers "fewer than N distinct salaries" without extra code.

| `salary` |
|---|
| 300 |
| 200 |
| 100 |

For N = 2: skip one (300), take 200.
→ [limit-offset](../sql/limit-offset.md) · [distinct](../sql/distinct.md) · [nth-highest-value](../sql/nth-highest-value.md)

```sql
END
```

<details>
<summary>The whole thing together</summary>

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  SET N = N - 1;
  RETURN (
      SELECT DISTINCT salary
      FROM Employee
      ORDER BY salary DESC
      LIMIT 1 OFFSET N
  );
END
```

</details>

**Trace it** — Example 2 has a single salary; skipping one leaves nothing, so the function returns `null`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** to deduplicate and sort the salaries, per call.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the distinct salaries.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's second-highest-salary with N as a parameter. `OFFSET` can't take `N - 1`, so I decrement N with `SET` first, then return distinct salaries in descending order with `LIMIT 1 OFFSET N`. If there are fewer than N distinct salaries the subquery is empty and the function returns `NULL`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Without `SET`?" | `DENSE_RANK() OVER (ORDER BY salary DESC)` in a subquery and `WHERE rk = N`, with `DISTINCT` on the outer select. |
| "What if N is 0 or negative?" | Either version returns `NULL` in MySQL — but check explicitly (`IF N < 1 THEN RETURN NULL; END IF;`) rather than rely on it. |
| "Per department?" | A function returning one value doesn't fit; use `DENSE_RANK() OVER (PARTITION BY departmentId …)` in a query. |
| "Why a function at all?" | It's LeetCode's way to pass a parameter. In an application you'd use a prepared statement with a placeholder. |

**Traps:**

- **`OFFSET N - 1`** — a syntax error.
- **Forgetting `DISTINCT`** — ties shift every position.
- **`OFFSET N`** without decrementing — returns the (N+1)th.

**This same move shows up in:** [Second Highest Salary](176-second-highest-salary.md) (N = 2, written as a query) · [Rank Scores](178-rank-scores.md) (dense ranking) · [Department Top Three Salaries](185-department-top-three-salaries.md) (top N per group).

</details>

---
