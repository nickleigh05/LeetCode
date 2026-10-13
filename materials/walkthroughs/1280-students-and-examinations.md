# 1280. Students and Examinations

**Easy** · [LeetCode](https://leetcode.com/problems/students-and-examinations/) · [Solution file (no hints)](../../problems/1000-1499/1280.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For **every** student and **every** subject, count how many times that student attended that exam — including 0. Order by `student_id`, then `subject_name`.

```
Table: Students
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| student_name  | varchar |
+---------------+---------+
student_id is the primary key (column with unique values) for this table.
Each row of this table contains the ID and the name of one student in the school.

Table: Subjects
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| subject_name | varchar |
+--------------+---------+
subject_name is the primary key (column with unique values) for this table.
Each row of this table contains the name of one subject in the school.

Table: Examinations
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| subject_name | varchar |
+--------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each student from the Students table takes every course from the Subjects table.
Each row of this table indicates that a student with ID student_id attended the exam of subject_name.
```

```
Input:
Students table:
+------------+--------------+
| student_id | student_name |
+------------+--------------+
| 1          | Alice        |
| 2          | Bob          |
| 13         | John         |
| 6          | Alex         |
+------------+--------------+
Subjects table:
+--------------+
| subject_name |
+--------------+
| Math         |
| Physics      |
| Programming  |
+--------------+
Examinations table:
+------------+--------------+
| student_id | subject_name |
+------------+--------------+
| 1          | Math         |
| 1          | Physics      |
| 1          | Programming  |
| 2          | Programming  |
| 1          | Physics      |
| 1          | Math         |
| 13         | Math         |
| 13         | Programming  |
| 13         | Physics      |
| 2          | Math         |
| 1          | Math         |
+------------+--------------+
Output:
+------------+--------------+--------------+----------------+
| student_id | student_name | subject_name | attended_exams |
+------------+--------------+--------------+----------------+
| 1          | Alice        | Math         | 3              |
| 1          | Alice        | Physics      | 2              |
| 1          | Alice        | Programming  | 1              |
| 2          | Bob          | Math         | 1              |
| 2          | Bob          | Physics      | 0              |
| 2          | Bob          | Programming  | 1              |
| 6          | Alex         | Math         | 0              |
| 6          | Alex         | Physics      | 0              |
| 6          | Alex         | Programming  | 0              |
| 13         | John         | Math         | 1              |
| 13         | John         | Physics      | 1              |
| 13         | John         | Programming  | 1              |
+------------+--------------+--------------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The output has rows that **don't come from any exam record** — Bob's Physics, all of Alex's subjects. You have to manufacture every (student, subject) pair first, then count exams into it.

| The statement says | Which really means |
|---|---|
| "each student … each exam" | One row per (student, subject) — 4 students × 3 subjects = 12 rows |
| Alex attended nothing | Rows with count 0 must still appear |
| `Examinations` "may contain duplicates" | Alice's three Math rows are three attendances — count rows, don't dedupe |
| `student_name` in the output | Comes from `Students` |
| "ordered by student_id and subject_name" | `ORDER BY` both — and this problem checks order |

Every pairing of two sets is a **cross join**. Then a left join attaches the matching exam rows, and the count can be zero.

🤔 **Before you open the next section:** which kind of join produces all 12 (student, subject) pairs, whether or not anyone sat the exam?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`CROSS JOIN`, then `LEFT JOIN` + count** | Students × Subjects, left-join `Examinations` on both keys, `COUNT(e.subject_name)` | ✅ Builds the full grid, counts into it |
| Correlated count per pair | `(SELECT COUNT(*) FROM Examinations e WHERE e.student_id = … AND e.subject_name = …)` | ✅ Clear; one subquery per grid cell |
| Join `Students` to `Examinations` directly | `Students s JOIN Examinations e …` | ❌ Only pairs that have exams — no zero rows |
| Cross join, then `COUNT(*)` | `COUNT(*)` instead of `COUNT(e.subject_name)` | ❌ Counts 1 for exams nobody took |

**The decision: cross join, left join, `COUNT(column)`.** Each piece does one job: the grid, the matches, the count.

Without the cross join, missing combinations never exist, so they can't be counted as 0. For Bob and Alex:

| `student_id` | `subject_name` | `attended_exams` |
|---|---|---|
| 2 | Math | 1 |
| 2 | Programming | 1 |

Bob's Physics and all of Alex's rows are missing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT s.student_id, s.student_name, sub.subject_name,
       COUNT(e.subject_name) AS attended_exams
```

**The grid columns, plus the count.** `COUNT(e.subject_name)` counts only rows where an exam actually matched — for an empty cell, the left join leaves `e.subject_name` as `NULL`, and `COUNT(column)` skips `NULL`s, giving 0.
→ [count](../sql/count.md)

```sql
FROM Students s
```

```sql
CROSS JOIN Subjects sub
```

**Every student paired with every subject.** A cross join has no `ON` — it returns all combinations. 4 × 3 = 12 rows. For Bob and Alex:

| `student_id` | `student_name` | `subject_name` |
|---|---|---|
| 2 | Bob | Math |
| 2 | Bob | Physics |
| 2 | Bob | Programming |
| 6 | Alex | Math |
| 6 | Alex | Physics |
| 6 | Alex | Programming |

→ [cross-join](../sql/cross-join.md)

```sql
LEFT JOIN Examinations e
    ON  e.student_id = s.student_id
    AND e.subject_name = sub.subject_name
```

**Attach the exam records for each cell.** The match needs **both** columns — same student *and* same subject. A cell with three exam rows becomes three rows; a cell with none stays as one row with `NULL`s.
→ [left-join](../sql/left-join.md)

```sql
GROUP BY s.student_id, s.student_name, sub.subject_name
```

**One output row per grid cell.** `student_name` is in the `GROUP BY` because it's selected and isn't aggregated. LeetCode's tables declare no primary key, so MySQL can't tell that the name depends on the id, and rejects the query under its default `ONLY_FULL_GROUP_BY` mode.
→ [group-by](../sql/group-by.md)

```sql
ORDER BY s.student_id, sub.subject_name;
```

→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT s.student_id, s.student_name, sub.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM Students s
CROSS JOIN Subjects sub
LEFT JOIN Examinations e
    ON  e.student_id = s.student_id
    AND e.subject_name = sub.subject_name
GROUP BY s.student_id, s.student_name, sub.subject_name
ORDER BY s.student_id, sub.subject_name;
```

</details>

**Trace it** — why the count must name a column. For Bob and Alex:

| `student_id` | `subject_name` | `COUNT(*)` | `COUNT(e.subject_name)` |
|---|---|---|---|
| 2 | Math | 1 | 1 |
| 2 | Physics | 1 | 0 |
| 2 | Programming | 1 | 1 |
| 6 | Math | 1 | 0 |
| 6 | Physics | 1 | 0 |
| 6 | Programming | 1 | 0 |

Every grid cell has at least one row after the left join — the cell itself — so `COUNT(*)` never drops below 1. `COUNT(e.subject_name)` counts only real exam rows.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(s · k + e)</summary>

**O(s · k + e)** for s students, k subjects, e exam rows. The grid has s · k cells; the left join hashes the exam rows on `(student_id, subject_name)` and probes once per cell; grouping is linear in the joined rows.

The output itself has s · k rows, so you can't do better than O(s · k).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(s · k + e)</summary>

**O(e)** for the hash table over exam rows, and **O(s · k)** for the groups — which is also the size of the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The result needs every student–subject pair, including ones with no exams, so I cross join `Students` with `Subjects` to build the grid. Then I left-join `Examinations` on both keys and count `e.subject_name`, which is `NULL` for empty cells, so they count as 0. Group by the grid columns and sort."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `COUNT(e.subject_name)` and not `COUNT(*)`?" | `COUNT(*)` counts the grid cell's own row, giving 1 for exams never taken. |
| "Only the pairs with zero attendances?" | Add `HAVING COUNT(e.subject_name) = 0`. |
| "What if `Examinations` mentions a subject not in `Subjects`?" | It's never counted — the grid comes from `Subjects`, and the left join only attaches matching rows. |
| "How big can the grid get?" | s × k rows. Cross joins are cheap to write and expensive to run on big tables — make sure you really want every pair. |
| "Each student's total exams?" | Drop `subject_name` from the grid: `Students LEFT JOIN Examinations`, group by student. |

**Traps:**

- **No cross join** — combinations with zero attendances are never created.
- **`COUNT(*)`** — turns zeros into ones.
- **Joining exams on `student_id` only** — every exam lands in every subject's cell.
- **Missing `student_name` in `GROUP BY`** — rejected by `ONLY_FULL_GROUP_BY`.

**This same move shows up in:** [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md) (counting after a left join) · [Count Salary Categories](1907-count-salary-categories.md) (making zero-count categories appear) · [Customers Who Bought All Products](1045-customers-who-bought-all-products.md) (comparing against the full set of products).

</details>

---
