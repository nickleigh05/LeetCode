# 2356. Number of Unique Subjects Taught by Each Teacher

**Easy** · [LeetCode](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/) · [Solution file (no hints)](../../problems/2000-2499/2356.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each teacher, count the number of **unique** subjects they teach. Any order.

```
Table: Teacher
+-------------+------+
| Column Name | Type |
+-------------+------+
| teacher_id  | int  |
| subject_id  | int  |
| dept_id     | int  |
+-------------+------+
(subject_id, dept_id) is the primary key (combinations of columns with unique values) of this table.
Each row in this table indicates that the teacher with teacher_id teaches the subject subject_id in the department dept_id.
```

```
Input:
Teacher table:
+------------+------------+---------+
| teacher_id | subject_id | dept_id |
+------------+------------+---------+
| 1          | 2          | 3       |
| 1          | 2          | 4       |
| 1          | 3          | 3       |
| 2          | 1          | 1       |
| 2          | 2          | 1       |
| 2          | 3          | 1       |
| 2          | 4          | 1       |
+------------+------------+---------+
Output:
+------------+-----+
| teacher_id | cnt |
+------------+-----+
| 1          | 2   |
| 2          | 4   |
+------------+-----+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `(subject_id, dept_id)` is the key | The same subject can appear more than once for a teacher — once per department |
| "number of **unique** subjects" | Count distinct `subject_id`s, not rows |
| "each teacher" | `GROUP BY teacher_id` |
| teacher 1 teaches subject 2 in depts 3 and 4 | Two rows, one subject — teacher 1's answer is 2, not 3 |
| output column `cnt` | Alias the count |

🤔 **Before you open the next section:** teacher 1 has three rows. Which of them should count as the same subject?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`COUNT(DISTINCT …)`** | `COUNT(DISTINCT subject_id)` per teacher | ✅ Removes duplicates inside each group |
| Deduplicate first, then count | `FROM (SELECT DISTINCT teacher_id, subject_id …) t` then `COUNT(*)` | ✅ Same result, two steps |
| `COUNT(*)` | counts rows | ❌ Counts teacher 1's subject 2 twice |

**The decision: `COUNT(DISTINCT subject_id)`.** It says "how many different subjects" directly.

| `teacher_id` | `COUNT(*)` | `COUNT(DISTINCT subject_id)` |
|---|---|---|
| 1 | 3 | 2 |
| 2 | 4 | 4 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT teacher_id, COUNT(DISTINCT subject_id) AS cnt
```

**The teacher, and how many different subjects appear in their rows.** `COUNT(DISTINCT x)` counts each value of `x` once per group (and ignores `NULL`s).
→ [count](../sql/count.md) · [distinct](../sql/distinct.md) · [aliases](../sql/aliases.md)

```sql
FROM Teacher
```

```sql
GROUP BY teacher_id;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT teacher_id, COUNT(DISTINCT subject_id) AS cnt
FROM Teacher
GROUP BY teacher_id;
```

</details>

**Trace it** — teacher 1's rows are (2, 3), (2, 4), (3, 3). The distinct subjects are {2, 3} → 2. Teacher 2 teaches 1, 2, 3, 4 → 4.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** expected — one pass, inserting each (teacher, subject) into a per-group set. (MySQL may sort instead, O(n log n).)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** in the worst case — the distinct (teacher, subject) pairs being tracked.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A subject can appear once per department, so I count distinct subjects, not rows: `COUNT(DISTINCT subject_id)` grouped by teacher."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Count departments per teacher too?" | Another column: `COUNT(DISTINCT dept_id)`. |
| "Teachers with more than 3 subjects?" | `HAVING COUNT(DISTINCT subject_id) > 3`. |
| "Count distinct (subject, dept) pairs?" | `COUNT(DISTINCT subject_id, dept_id)` — MySQL accepts several columns. |
| "Which teachers share a subject?" | Self-join on `subject_id` with `a.teacher_id < b.teacher_id`. |

**Traps:**

- **`COUNT(*)`** — counts department rows, not subjects.
- **`DISTINCT` in the wrong place** — `SELECT DISTINCT teacher_id, COUNT(subject_id)` deduplicates the *output rows*, not the values being counted.

**This same move shows up in:** [Article Views I](1148-article-views-i.md) (`DISTINCT` to remove duplicates) · [User Activity for the Past 30 Days I](1141-user-activity-for-the-past-30-days-i.md) (`COUNT(DISTINCT user_id)` per day) · [Customers Who Bought All Products](1045-customers-who-bought-all-products.md) (distinct count compared to a total).

</details>

---
