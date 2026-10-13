# 620. Not Boring Movies

**Easy** · [LeetCode](https://leetcode.com/problems/not-boring-movies/) · [Solution file (no hints)](../../problems/0500-0999/620.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Report the movies with an **odd** id whose description isn't `"boring"`, sorted by rating, highest first.

```
Table: Cinema
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| id             | int      |
| movie          | varchar  |
| description    | varchar  |
| rating         | float    |
+----------------+----------+
id is the primary key (column with unique values) for this table.
Each row contains information about the name of a movie, its genre, and its rating.
rating is a 2 decimal places float in the range [0, 10]
```

```
Input:
Cinema table:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantacy     | 8.6    |
| 5  | House card | Interesting | 9.1    |
+----+------------+-------------+--------+
Output:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |
+----+------------+-------------+--------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "odd-numbered ID" | `id % 2 = 1` — the remainder after dividing by 2 |
| "description that is not `boring`" | `description != 'boring'` |
| both conditions | Joined with `AND` |
| output columns are the whole row | `SELECT *` is fine here — the expected output is every column, in table order |
| "ordered by rating in descending order" | `ORDER BY rating DESC` — and the order is checked |

The schema says `Table: Cinema`, but LeetCode's own `CREATE TABLE` names it lowercase `cinema`. MySQL on Linux treats table names as case-sensitive by default, so the walkthrough uses `cinema`, which matches the real table on any server.

🤔 **Before you open the next section:** which arithmetic operator tells you whether a number is odd?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Modulo** | `WHERE id % 2 = 1 AND description != 'boring'` | ✅ The standard odd test |
| `MOD()` | `WHERE MOD(id, 2) = 1 …` | ✅ Same operator, function form |
| Bitwise AND | `WHERE id & 1 …` | ✅ The lowest bit of an odd number is 1. Clever, less readable |
| `NOT LIKE 'boring'` | `description NOT LIKE 'boring'` | ✅ Works — with no wildcards, `LIKE` is plain equality |
| Sort ascending | `ORDER BY rating` | ❌ Lowest rating first |

**The decision: `id % 2 = 1` with `!=`.** Both read exactly like the statement.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT *
```

**Every column.** The expected output is the whole row, in the table's column order, so `*` is correct. On most problems, list columns explicitly instead.
→ [select-from](../sql/select-from.md)

```sql
FROM cinema
```

```sql
WHERE id % 2 = 1
  AND description != 'boring'
```

**Odd, and not boring.** `%` is the remainder operator: `5 % 2` is 1, `4 % 2` is 0.
→ [arithmetic-operators](../sql/arithmetic-operators.md) · [comparison-operators](../sql/comparison-operators.md) · [where](../sql/where.md)

```sql
ORDER BY rating DESC;
```

**Highest rating first.** `DESC` reverses the default ascending order.
→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT *
FROM cinema
WHERE id % 2 = 1
  AND description != 'boring'
ORDER BY rating DESC;
```

</details>

**Trace it** — both conditions per row:

| `id` | `description` | `id % 2` | `not boring?` | `WHERE says` |
|---|---|---|---|---|
| 1 | great 3D | 1 | 1 | kept |
| 2 | fiction | 0 | 1 | dropped |
| 3 | boring | 1 | 0 | dropped |
| 4 | Fantacy | 0 | 1 | dropped |
| 5 | Interesting | 1 | 1 | kept |

Movies 1 and 5 survive; sorted by rating, 5 (9.1) comes before 1 (8.9).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + k log k)</summary>

**O(n + k log k)** — one scan over n movies, then sorting the k that survive.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** — the surviving rows are buffered so they can be sorted.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two row filters joined with `AND` — `id % 2 = 1` for odd ids, and description not equal to 'boring' — then sort by rating descending."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Even ids instead?" | `id % 2 = 0`. |
| "What about negative ids?" | In MySQL, `-7 % 2` is `-1`, so `= 1` would miss negative odd ids. `id % 2 <> 0` is the safe odd test. |
| "Exclude any description *containing* 'boring'." | `description NOT LIKE '%boring%'`. |
| "Ties in rating?" | Add a tiebreaker: `ORDER BY rating DESC, id`. |
| "Only the top 3?" | Add `LIMIT 3`. |

**Traps:**

- **Ascending sort** — `ORDER BY rating` alone puts the worst first.
- **Table-name case** — `Cinema` vs `cinema` matters on a case-sensitive server.
- **`id % 2 = 1` with negative ids** — not an issue here, worth knowing.

**This same move shows up in:** [Big Countries](595-big-countries.md) (two conditions in one filter) · [Article Views I](1148-article-views-i.md) (filter, then sort) · [Triangle Judgement](610-triangle-judgement.md) (arithmetic in a condition).

</details>

---
