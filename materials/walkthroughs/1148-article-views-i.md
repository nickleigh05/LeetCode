# 1148. Article Views I

**Easy** · [LeetCode](https://leetcode.com/problems/article-views-i/) · [Solution file (no hints)](../../problems/1000-1499/1148.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find every author who viewed **at least one of their own articles**. Return their ids in a column named `id`, sorted ascending.

```
Table: Views
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| article_id    | int     |
| author_id     | int     |
| viewer_id     | int     |
| view_date     | date    |
+---------------+---------+
There is no primary key (column with unique values) for this table, the table may have duplicate rows.
Each row of this table indicates that some viewer viewed an article (written by some author) on some date. 
Note that equal author_id and viewer_id indicate the same person.
```

```
Input:
Views table:
+------------+-----------+-----------+------------+
| article_id | author_id | viewer_id | view_date  |
+------------+-----------+-----------+------------+
| 1          | 3         | 5         | 2019-08-01 |
| 1          | 3         | 6         | 2019-08-02 |
| 2          | 7         | 7         | 2019-08-01 |
| 2          | 7         | 6         | 2019-08-02 |
| 4          | 7         | 1         | 2019-07-22 |
| 3          | 4         | 4         | 2019-07-21 |
| 3          | 4         | 4         | 2019-07-21 |
+------------+-----------+-----------+------------+
Output:
+------+
| id   |
+------+
| 4    |
| 7    |
+------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Three new ideas in one Easy: comparing two columns **of the same row**, removing duplicates, and sorting.

| The statement says | Which really means |
|---|---|
| "equal `author_id` and `viewer_id` indicate the same person" | "Viewed their own article" is the condition `author_id = viewer_id`, checked within one row |
| "the table may have duplicate rows" | The same view can appear twice — the example's last two rows are identical |
| "**at least one**" of their own articles | An author counts once, however many self-views they have → remove duplicates |
| output column is `id` | Rename `author_id` with `AS id` |
| "sorted by id in ascending order" | `ORDER BY id` — and here the order *is* checked |

The duplicate rows are the trap. Author 4 viewed article 3 twice, so a plain filter returns 4 twice — but each author belongs in the answer exactly once.

🤔 **Before you open the next section:** after filtering to self-views, how do you collapse repeated ids down to one row each?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`DISTINCT`** | `SELECT DISTINCT author_id AS id … ORDER BY id` | ✅ States the intent: unique ids |
| `GROUP BY` | `SELECT author_id AS id … GROUP BY author_id ORDER BY author_id` | ✅ Same result. Natural if you'll add a `COUNT(*)` later |
| No dedupe | `SELECT author_id AS id … WHERE author_id = viewer_id` | ❌ Returns 4 twice |
| No `ORDER BY` | `SELECT DISTINCT author_id AS id … WHERE …` | ❌ Order isn't guaranteed — and this problem checks it |

**The decision: `DISTINCT`.** You want a set of ids, and `DISTINCT` says exactly that. Reach for `GROUP BY` when you need something *per* author — a count, a first date.

Without the dedupe, the filter alone gives:

| `id` |
|---|
| 4 |
| 4 |
| 7 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT DISTINCT author_id AS id
```

**Unique author ids, renamed.** `DISTINCT` applies to the whole selected row — here that's one column, so it means "each id once." `AS id` names the output column the way the expected result does.
→ [distinct](../sql/distinct.md) · [aliases](../sql/aliases.md)

```sql
FROM Views
```

```sql
WHERE author_id = viewer_id
```

**A self-view is a row where the two people are the same.** The comparison runs once per row, between two columns of that row.

Notice this says `author_id`, not `id`. `WHERE` runs **before** `SELECT`, so the alias doesn't exist yet — `WHERE id = …` fails with *Unknown column 'id' in 'where clause'*.
→ [where](../sql/where.md) · [comparison-operators](../sql/comparison-operators.md)

```sql
ORDER BY id ASC;
```

**Sorting comes last.** `ORDER BY` runs after `SELECT`, which is why it *can* use the alias `id`. `ASC` is the default, so `ORDER BY id` alone means the same thing — writing it out just makes the direction explicit.
→ [order-by](../sql/order-by.md) · [execution-order](../sql/execution-order.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id ASC;
```

</details>

**Trace it** — which rows are self-views:

| `article_id` | `author_id` | `viewer_id` | `own article?` |
|---|---|---|---|
| 1 | 3 | 5 | 0 |
| 1 | 3 | 6 | 0 |
| 2 | 7 | 7 | 1 |
| 2 | 7 | 6 | 0 |
| 4 | 7 | 1 | 0 |
| 3 | 4 | 4 | 1 |
| 3 | 4 | 4 | 1 |

Three rows pass the filter — one for author 7 and two identical ones for author 4. `DISTINCT` collapses them to `4, 7`, and `ORDER BY` returns them in that order.

**The evaluation order, again:** `FROM` → `WHERE` → `SELECT` (including `DISTINCT`) → `ORDER BY`. The alias rule falls straight out of it: anything that runs after `SELECT` can see aliases; anything before it can't. See [execution-order](../sql/execution-order.md).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + k log k)</summary>

**O(n + k log k)** — n views, k distinct qualifying authors.

- The scan and filter touch each row once: O(n).
- `DISTINCT` keeps a hash set (in practice, a temporary table with a unique key) of ids seen so far: O(1) per row on average.
- Sorting the k surviving ids: O(k log k).

k is at most the number of authors, usually far smaller than n.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** for the set of distinct ids that `DISTINCT` maintains, which is also the size of the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A self-view is a row where `author_id` equals `viewer_id`. Filter to those, keep each author once with `DISTINCT` — the table has duplicate rows — rename to `id`, and sort. The filter can't use the alias because `WHERE` runs before `SELECT`, but `ORDER BY` can."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How many times did each author view their own work?" | `SELECT author_id, COUNT(*) … WHERE author_id = viewer_id GROUP BY author_id`. Decide whether duplicate rows should count — `COUNT(DISTINCT article_id)` counts articles instead of views. |
| "Authors who **never** viewed their own articles?" | All authors minus these: `SELECT DISTINCT author_id FROM Views WHERE author_id NOT IN (…this query…)`, or `GROUP BY author_id HAVING SUM(author_id = viewer_id) = 0`. |
| "Why not `GROUP BY`?" | It works and gives the same rows. `DISTINCT` states intent better when there's no aggregate. |
| "Sort by the date of their first self-view?" | Now you need a value per author → `GROUP BY author_id ORDER BY MIN(view_date)`. |
| "Could you `ORDER BY view_date` with `DISTINCT`?" | No — MySQL rejects it (error 3065): after `DISTINCT` there's no single `view_date` per id to sort by. |

**Traps:**

- **Forgetting `DISTINCT`** — duplicate rows are in the example on purpose.
- **Missing `AS id`** — the expected column is `id`, not `author_id`.
- **Using the alias in `WHERE`** — `WHERE id = viewer_id` is an error. Aliases exist from `SELECT` onwards.
- **Leaving out `ORDER BY`** — rows can come back in any order unless you ask; "sorted by id" means you have to ask.

**This same move shows up in:** [Find Followers Count](1729-find-followers-count.md) (one row per id, with a count) · [Number of Unique Subjects Taught by Each Teacher](2356-number-of-unique-subjects-taught-by-each-teacher.md) (duplicates removed inside a count) · [Recyclable and Low Fat Products](1757-recyclable-and-low-fat-products.md) (the plain filter this builds on).

</details>

---
