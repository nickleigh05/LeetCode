# 577. Employee Bonus

**Easy** · [LeetCode](https://leetcode.com/problems/employee-bonus/) · [Solution file (no hints)](../../problems/0500-0999/577.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Report the name and bonus of every employee whose bonus is **less than 1000** — or who got **no bonus at all**. Any order.

```
Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |
+-------------+---------+
empId is the column with unique values for this table.
Each row of this table indicates the name and the ID of an employee in addition to their salary and the id of their manager.

Table: Bonus
+-------------+------+
| Column Name | Type |
+-------------+------+
| empId       | int  |
| bonus       | int  |
+-------------+------+
empId is the column of unique values for this table.
empId is a foreign key (reference column) to empId from the Employee table.
Each row of this table contains the id of an employee and their respective bonus.
```

```
Input:
Employee table:
+-------+--------+------------+--------+
| empId | name   | supervisor | salary |
+-------+--------+------------+--------+
| 3     | Brad   | null       | 4000   |
| 1     | John   | 3          | 1000   |
| 2     | Dan    | 3          | 2000   |
| 4     | Thomas | 3          | 4000   |
+-------+--------+------------+--------+
Bonus table:
+-------+-------+
| empId | bonus |
+-------+-------+
| 2     | 500   |
| 4     | 2000  |
+-------+-------+
Output:
+------+-------+
| name | bonus |
+------+-------+
| Brad | null  |
| John | null  |
| Dan  | 500   |
+------+-------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This combines the two `NULL` lessons so far: a `LEFT JOIN` produces `NULL`s for missing matches ([Replace Employee ID With The Unique Identifier](1378-replace-employee-id-with-the-unique-identifier.md)), and `< 1000` is unknown for a `NULL` ([Find Customer Referee](584-find-customer-referee.md)).

| The statement says | Which really means |
|---|---|
| names in `Employee`, bonuses in `Bonus` | Join on `empId` |
| "did not get any bonus" | No row in `Bonus` → must survive the join → `LEFT JOIN` from `Employee` |
| "bonus less than 1000" | `b.bonus < 1000` |
| "either of the following" | `OR` the two cases |
| Brad and John show `null` | Missing bonuses stay `NULL` in the output — don't replace them with 0 |
| `supervisor`, `salary` | Not needed |

🤔 **Before you open the next section:** for Brad, who has no row in `Bonus`, what does `b.bonus < 1000` evaluate to after the left join?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT JOIN`, then `WHERE … OR … IS NULL`** | `WHERE b.bonus < 1000 OR b.bonus IS NULL` | ✅ Both cases spelled out |
| `IFNULL` in the filter | `WHERE IFNULL(b.bonus, 0) < 1000` | ✅ Treats "no bonus" as 0 — correct here, and compact |
| `LEFT JOIN … WHERE b.bonus < 1000` | only the first case | ❌ Drops Brad and John — `NULL < 1000` is unknown |
| Filter in `ON` | `LEFT JOIN Bonus b ON … AND b.bonus < 1000` | ❌ Keeps **everyone** — see below |

**The decision: `WHERE b.bonus < 1000 OR b.bonus IS NULL`.** It reads like the two bullet points in the statement.

**Why the filter can't go in `ON`.** In a left join, `ON` decides which right-hand rows *match*; it never removes left-hand rows. So moving the condition there keeps Thomas, with his bonus blanked out:

| `name` | `bonus` |
|---|---|
| Brad | `NULL` |
| John | `NULL` |
| Dan | 500 |
| Thomas | `NULL` |

Thomas's 2000 bonus doesn't match `bonus < 1000`, so he's treated as having no bonus at all. Filters on the result belong in `WHERE`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT e.name, b.bonus
```

```sql
FROM Employee e
```

```sql
LEFT JOIN Bonus b
    ON e.empId = b.empId
```

**Keep every employee; attach a bonus where one exists.** Brad and John have no `Bonus` row, so their `b.bonus` is `NULL`.
→ [left-join](../sql/left-join.md) · [on-vs-where](../sql/on-vs-where.md)

```sql
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

**Both ways to qualify.** `b.bonus < 1000` catches Dan. `b.bonus IS NULL` catches the employees with no bonus row — for them the first comparison is unknown, so without this half they'd vanish.
→ [null-is-null](../sql/null-is-null.md) · [logical-operators](../sql/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b
    ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

</details>

**Trace it** — the joined rows and both halves of the condition (`NULL` = unknown):

| `empId` | `name` | `bonus` | `bonus < 1000` | `bonus IS NULL` |
|---|---|---|---|---|
| 1 | John | `NULL` | `NULL` | 1 |
| 2 | Dan | 500 | 1 | 0 |
| 3 | Brad | `NULL` | `NULL` | 1 |
| 4 | Thomas | 2000 | 0 | 0 |

John and Brad pass on `IS NULL`; Dan passes on `< 1000`; Thomas fails both.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)** for n employees and m bonus rows — a hash join on `empId`, then one filter pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** for the hash table over `Bonus`, plus the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Employees without a bonus still count, so I left-join `Bonus` onto `Employee`. Then I keep rows where the bonus is under 1000 or missing — I need the explicit `IS NULL` because `NULL < 1000` is unknown, and `WHERE` drops unknowns. The filter goes in `WHERE`, not `ON`, or no employee would ever be removed."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Show 0 instead of `null`." | `SELECT e.name, IFNULL(b.bonus, 0) AS bonus …` — but the expected output here wants `null`. |
| "Employees with a bonus of **at least** 1000?" | Now an inner join is enough: `JOIN Bonus b … WHERE b.bonus >= 1000`. Missing bonuses can't qualify. |
| "Why not put the condition in `ON`?" | For a left join, `ON` filters the right side only; every left row survives. |
| "Average bonus, counting employees with none as 0?" | `AVG(IFNULL(b.bonus, 0))`. Plain `AVG(b.bonus)` skips `NULL`s and averages only the employees who got one. |

**Traps:**

- **`WHERE b.bonus < 1000` alone** — loses everyone without a bonus.
- **The condition in `ON`** — keeps everyone.
- **An inner join** — drops employees with no bonus row before you ever filter.

**This same move shows up in:** [Find Customer Referee](584-find-customer-referee.md) (the same `IS NULL OR` fix, without a join) · [Replace Employee ID With The Unique Identifier](1378-replace-employee-id-with-the-unique-identifier.md) (the plain left join) · [Confirmation Rate](1934-confirmation-rate.md) (a left join whose `NULL`s must become zeros).

</details>

---
