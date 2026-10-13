# 619. Biggest Single Number

**Easy** · [LeetCode](https://leetcode.com/problems/biggest-single-number/) · [Solution file (no hints)](../../problems/0500-0999/619.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A **single number** appears exactly once in the table. Return the largest single number — or `null` if there isn't one.

```
Table: MyNumbers
+-------------+------+
| Column Name | Type |
+-------------+------+
| num         | int  |
+-------------+------+
This table may contain duplicates (In other words, there is no primary key for this table in SQL).
Each row of this table contains an integer.
```

```
Input:
MyNumbers table:
+-----+
| num |
+-----+
| 8   |
| 8   |
| 3   |
| 3   |
| 1   |
| 4   |
| 5   |
| 6   |
+-----+
Output:
+-----+
| num |
+-----+
| 6   |
+-----+
```

```
Input:
MyNumbers table:
+-----+
| num |
+-----+
| 8   |
| 8   |
| 7   |
| 7   |
| 3   |
| 3   |
| 3   |
+-----+
Output:
+------+
| num  |
+------+
| null |
+------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Two steps — find the numbers that appear once, then take the biggest — plus one requirement that decides the shape of the query: **always return one row**, even when there's no answer.

| The statement says | Which really means |
|---|---|
| "appeared only once" | Group by `num`, keep groups where `COUNT(*) = 1` |
| "the largest single number" | `MAX` over those |
| "if there is no single number, report null" | The output is one row containing `NULL` — **not** zero rows |
| Example 2 | Every number repeats; the expected output is a `null` row |

🤔 **Before you open the next section:** `MAX` over an empty set returns `NULL`. What does `ORDER BY num DESC LIMIT 1` over an empty set return?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`MAX` over a derived table** | `SELECT MAX(num) FROM (… HAVING COUNT(*) = 1) singles` | ✅ An aggregate with no `GROUP BY` always returns exactly one row |
| `LIMIT 1` wrapped in a scalar subquery | `SELECT (SELECT num … ORDER BY num DESC LIMIT 1) AS num` | ✅ An empty scalar subquery evaluates to `NULL` |
| Bare `ORDER BY … LIMIT 1` | `SELECT num … HAVING COUNT(*) = 1 ORDER BY num DESC LIMIT 1` | ❌ Returns **no rows** for Example 2 |

**The decision: `MAX` over the singles.** On Example 2 there are no singles. The bare `LIMIT` version returns nothing at all:

| `num` |
|---|

`MAX` over the same empty set returns a row with `NULL`, which is what's expected:

| `num` |
|---|
| `NULL` |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT MAX(num) AS num
```

**The biggest of the singles.** An aggregate function in a `SELECT` without `GROUP BY` treats all the rows as one group — so it returns exactly one row, and `MAX` of no values is `NULL`. The alias `num` matches the expected column name.
→ [aggregate-functions](../sql/aggregate-functions.md)

```sql
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) singles;
```

**The single numbers.** Group equal numbers together; `HAVING COUNT(*) = 1` keeps the ones that occur once. A subquery in `FROM` must have an alias — `singles`.
→ [having](../sql/having.md) · [derived-tables](../sql/derived-tables.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT MAX(num) AS num
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) singles;
```

</details>

**Trace it** — Example 1's counts:

| `num` | `COUNT(*)` |
|---|---|
| 8 | 2 |
| 6 | 1 |
| 5 | 1 |
| 4 | 1 |
| 3 | 2 |
| 1 | 1 |

The singles are 6, 5, 4, 1; the maximum is 6.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one grouping pass, then a scan of the distinct values for the maximum.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d)</summary>

**O(d)** for d distinct numbers.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Group by number and keep counts of exactly one — those are the singles. Then take `MAX` over them in an outer query. I use `MAX` rather than `ORDER BY … LIMIT 1` because an aggregate always returns a row, so when there are no singles I get the required `null` instead of an empty result."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `LIMIT 1`?" | No singles → zero rows, but the problem wants a `null` row. Wrapping it as a scalar subquery fixes that. |
| "The smallest single number?" | `MIN` instead of `MAX`. |
| "Numbers that appear exactly twice?" | `HAVING COUNT(*) = 2`. |
| "The most frequent number?" | `GROUP BY num ORDER BY COUNT(*) DESC LIMIT 1` — mind ties. |

**Traps:**

- **Empty result instead of `null`** — the `LIMIT 1` version fails Example 2.
- **`SELECT DISTINCT num`** — removes duplicates but keeps the repeated numbers as candidates.
- **`MAX` and `HAVING` in one query** — `SELECT MAX(num) … GROUP BY num HAVING COUNT(*) = 1` returns one row *per single number*, each its own maximum.

**This same move shows up in:** [Second Highest Salary](176-second-highest-salary.md) (return `null` when there's no answer) · [Nth Highest Salary](177-nth-highest-salary.md) (the same issue inside a function) · [Classes With at Least 5 Students](596-classes-with-at-least-5-students.md) (`HAVING` on a count).

</details>

---
