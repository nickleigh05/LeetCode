# 610. Triangle Judgement

**Easy** · [LeetCode](https://leetcode.com/problems/triangle-judgement/) · [Solution file (no hints)](../../problems/0500-0999/610.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each row of three lengths, report whether they can form a triangle: `Yes` or `No`. Any order.

```
Table: Triangle
+-------------+------+
| Column Name | Type |
+-------------+------+
| x           | int  |
| y           | int  |
| z           | int  |
+-------------+------+
In SQL, (x, y, z) is the primary key column for this table.
Each row of this table contains the lengths of three line segments.
```

```
Input:
Triangle table:
+----+----+----+
| x  | y  | z  |
+----+----+----+
| 13 | 15 | 30 |
| 10 | 20 | 15 |
+----+----+----+
Output:
+----+----+----+----------+
| x  | y  | z  | triangle |
+----+----+----+----------+
| 13 | 15 | 30 | No       |
| 10 | 20 | 15 | Yes      |
+----+----+----+----------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Every row stays; you're adding a computed **label** column. That's `CASE` (or `IF`) in the `SELECT`, not a filter.

| The statement says | Which really means |
|---|---|
| "for every three line segments" | Every row appears in the output — no `WHERE` |
| "whether they can form a triangle" | The triangle inequality: each pair of sides sums to **more than** the third |
| output adds a `triangle` column of `Yes`/`No` | A conditional expression producing a string |
| 13 + 15 = 28, not more than 30 | `No` |

The math: three lengths form a (non-degenerate) triangle exactly when `x + y > z`, `x + z > y`, and `y + z > x`. Equality means the "triangle" is flat — a straight line — and doesn't count.

🤔 **Before you open the next section:** how do you add a column whose value depends on a condition, without dropping any rows?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`CASE WHEN`** | `CASE WHEN x + y > z AND … THEN 'Yes' ELSE 'No' END` | ✅ Standard SQL; extends to more branches |
| `IF()` | `IF(x + y > z AND …, 'Yes', 'No')` | ✅ MySQL shorthand for a two-way choice |
| Largest side vs the rest | `IF(GREATEST(x, y, z) * 2 < x + y + z, 'Yes', 'No')` | ✅ One comparison: the longest side must be shorter than the other two combined |
| `>=` | `x + y >= z` | ❌ Calls a flat line a triangle |

**The decision: `CASE WHEN` with all three inequalities.** It's the definition, and `CASE` is the conditional you'll use most.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT x, y, z,
       CASE
           WHEN x + y > z AND x + z > y AND y + z > x THEN 'Yes'
           ELSE 'No'
       END AS triangle
```

**Keep the three sides and add the label.** `CASE` checks its `WHEN` conditions in order and returns the first matching `THEN`; `ELSE` covers everything else. `AND` requires all three inequalities.
→ [case-when](../sql/case-when.md) · [if-function](../sql/if-function.md) · [arithmetic-operators](../sql/arithmetic-operators.md)

```sql
FROM Triangle;
```

<details>
<summary>The whole thing together</summary>

```sql
SELECT x, y, z,
       CASE
           WHEN x + y > z AND x + z > y AND y + z > x THEN 'Yes'
           ELSE 'No'
       END AS triangle
FROM Triangle;
```

</details>

**Trace it** — each inequality per row:

| `x` | `y` | `z` | `x+y > z` | `x+z > y` | `y+z > x` |
|---|---|---|---|---|---|
| 13 | 15 | 30 | 0 | 1 | 1 |
| 10 | 20 | 15 | 1 | 1 | 1 |

The first row fails `x + y > z` (28 is not more than 30), so it's `No`. The second passes all three.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — a few additions and comparisons per row.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every row stays, so this is a computed column, not a filter. Three lengths make a triangle when each pair sums to more than the third, so I put all three inequalities in a `CASE WHEN` that returns 'Yes' or 'No'."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Only the rows that form triangles?" | Move the condition into `WHERE`. |
| "Classify as equilateral / isosceles / scalene?" | More `WHEN` branches, ordered from most specific: `WHEN x = y AND y = z THEN 'Equilateral' WHEN x = y OR y = z OR x = z THEN 'Isosceles' …`. |
| "What if a side is `NULL`?" | The comparison is unknown, `CASE` falls through to `ELSE`, and you'd get `No`. Decide whether that's right. |
| "Can it be done with one comparison?" | `GREATEST(x, y, z) * 2 < x + y + z`. |

**Traps:**

- **Checking only one inequality** — `x + y > z` alone misses cases where `x` or `y` is the longest side.
- **`>=`** — degenerate triangles.
- **Filtering with `WHERE`** — the output needs every row.

**This same move shows up in:** [Count Salary Categories](1907-count-salary-categories.md) (labelling rows by condition) · [Exchange Seats](626-exchange-seats.md) (a `CASE` that computes a new value) · [Not Boring Movies](620-not-boring-movies.md) (arithmetic in a condition).

</details>

---
