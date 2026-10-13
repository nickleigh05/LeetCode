# 596. Classes With at Least 5 Students

**Easy** · [LeetCode](https://leetcode.com/problems/classes-with-at-least-5-students/) · [Solution file (no hints)](../../problems/0500-0999/596.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find every class with **at least five** students. Any order.

```
Table: Courses
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| student     | varchar |
| class       | varchar |
+-------------+---------+
(student, class) is the primary key (combination of columns with unique values) for this table.
Each row of this table indicates the name of a student and the class in which they are enrolled.
```

```
Input:
Courses table:
+---------+----------+
| student | class    |
+---------+----------+
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |
+---------+----------+
Output:
+---------+
| class   |
+---------+
| Math    |
+---------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "classes that have at least five students" | A condition on a **count per class** → group, then filter groups |
| `(student, class)` is the key | A student is in a class at most once, so counting rows counts students |
| "at least five" | `>= 5` |
| output is just `class` | The count is used for filtering, not shown |

The filter can't go in `WHERE`: `WHERE` looks at one row at a time, and no single row knows how many students its class has.

🤔 **Before you open the next section:** which clause filters *groups* after `GROUP BY` has formed them?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`GROUP BY` + `HAVING`** | `GROUP BY class HAVING COUNT(student) >= 5` | ✅ Filter groups by their count |
| Count in a derived table, filter outside | `SELECT class FROM (SELECT class, COUNT(*) AS n … GROUP BY class) t WHERE n >= 5` | ✅ Same thing in two steps |
| `WHERE COUNT(*) >= 5` | an aggregate in `WHERE` | ❌ MySQL rejects it: *Invalid use of group function* |

**The decision: `HAVING`.** It exists for exactly this: conditions on aggregates.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT class
```

```sql
FROM Courses
```

```sql
GROUP BY class
```

**One group per class.**
→ [group-by](../sql/group-by.md)

```sql
HAVING COUNT(student) >= 5;
```

**Keep classes with five or more students.** `HAVING` runs after grouping, so it can use `COUNT`. With `(student, class)` as the key, `COUNT(student)` and `COUNT(*)` agree; if a student could be listed twice, you'd want `COUNT(DISTINCT student)`.
→ [having](../sql/having.md) · [count](../sql/count.md) · [execution-order](../sql/execution-order.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(student) >= 5;
```

</details>

**Trace it** — the count per class:

| `class` | `students` |
|---|---|
| Math | 6 |
| English | 1 |
| Biology | 1 |
| Computer | 1 |

Only Math has five or more.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one grouping pass with a counter per class.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(c)</summary>

**O(c)** — one counter per class.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Group by class and keep the groups whose count is at least five. That condition is on an aggregate, so it goes in `HAVING`, not `WHERE`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if enrolments could be duplicated?" | `HAVING COUNT(DISTINCT student) >= 5`. |
| "Show the count too." | `SELECT class, COUNT(*) AS students …`. |
| "Classes with the most students?" | `HAVING COUNT(*) = (SELECT MAX(n) FROM (SELECT COUNT(*) AS n … GROUP BY class) t)`. |
| "`WHERE` vs `HAVING`?" | `WHERE` filters rows before grouping; `HAVING` filters groups after. Push row filters into `WHERE` — fewer rows to group. |

**Traps:**

- **An aggregate in `WHERE`** — an error.
- **`> 5`** — "at least five" includes five.

**This same move shows up in:** [Managers with at Least 5 Direct Reports](570-managers-with-at-least-5-direct-reports.md) (the same `HAVING`, after a self-join) · [Biggest Single Number](619-biggest-single-number.md) (`HAVING COUNT(*) = 1`) · [Customers Who Bought All Products](1045-customers-who-bought-all-products.md) (`HAVING` against a subquery).

</details>

---
