# 178. Rank Scores

**Medium** · [LeetCode](https://leetcode.com/problems/rank-scores/) · [Solution file (no hints)](../../problems/0001-0499/178.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Rank scores from highest to lowest. Ties share a rank, and the next rank is the next integer — **no gaps**. Order by score, highest first.

```
Table: Scores
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| score       | decimal |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the score of a game. Score is a floating point value with two decimal places.
```

```
Input:
Scores table:
+----+-------+
| id | score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
Output:
+-------+------+
| score | rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The three rules describe one specific ranking function exactly.

| The statement says | Which really means |
|---|---|
| "ranked from the highest to the lowest" | `ORDER BY score DESC` inside the ranking |
| "If there is a tie … both should have the same ranking" | Equal scores, equal rank |
| "the next ranking number should be the next consecutive integer … no holes" | After two 1s comes 2, not 3 → `DENSE_RANK` |
| output column `rank` | `rank` is a reserved word in MySQL 8 — it needs backticks |
| "ordered by score in descending order" | Checked |

| `score` | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|
| 4.00 | 1 | 1 | 1 |
| 4.00 | 2 | 1 | 1 |
| 3.85 | 3 | 3 | 2 |
| 3.65 | 4 | 4 | 3 |
| 3.65 | 5 | 4 | 3 |
| 3.50 | 6 | 6 | 4 |

`ROW_NUMBER` never ties; `RANK` ties but skips (1, 1, 3); `DENSE_RANK` ties without skipping (1, 1, 2).

🤔 **Before you open the next section:** which column of that table matches the expected output?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`DENSE_RANK()`** | `DENSE_RANK() OVER (ORDER BY score DESC)` | ✅ Ties share a rank; no gaps |
| Correlated count | rank = number of distinct scores `>=` this one | ✅ The pre-window answer; O(n²) |
| `RANK()` | | ❌ Leaves gaps after ties |
| `ROW_NUMBER()` | | ❌ Gives tied scores different ranks |

**The decision: `DENSE_RANK`.** "No holes between ranks" is its definition.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS `rank`
```

**The score and its dense rank.** `OVER (ORDER BY score DESC)` ranks across the whole table, highest score first — there's no `PARTITION BY` because every score competes with every other. The backticks around `rank` are required: unquoted, `AS rank` is a syntax error in MySQL 8, because `RANK` is a function name.
→ [ranking-functions](../sql/ranking-functions.md) · [window-functions](../sql/window-functions.md) · [aliases](../sql/aliases.md)

```sql
FROM Scores
```

```sql
ORDER BY score DESC;
```

**The output order.** The window's `ORDER BY` decides the ranks; it doesn't sort the result. This final `ORDER BY` does.
→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS `rank`
FROM Scores
ORDER BY score DESC;
```

</details>

**Trace it** — distinct scores in descending order are 4.00, 3.85, 3.65, 3.50, so they get dense ranks 1, 2, 3, 4, and every row takes the rank of its score.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** — one sort by score, then a linear pass assigning ranks. The correlated-count version is **O(n²)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the sorted rows.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Ties share a rank and there are no gaps, which is exactly `DENSE_RANK() OVER (ORDER BY score DESC)`. I backtick the `rank` alias since it's reserved, and sort the output by score descending."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Ranks with gaps (Olympic style)?" | `RANK()`. |
| "Without window functions?" | `(SELECT COUNT(DISTINCT t.score) FROM Scores t WHERE t.score >= s.score)`. |
| "Rank within each category?" | Add `PARTITION BY category` inside `OVER`. |
| "The 3rd-ranked score?" | Wrap it: `… WHERE rnk = 3` in an outer query — see [Nth Highest Salary](177-nth-highest-salary.md). |

**Traps:**

- **`RANK` or `ROW_NUMBER`** — wrong tie behaviour.
- **Unquoted `rank`** — a syntax error.
- **Relying on the window's `ORDER BY` for output order** — it doesn't sort the result.

**This same move shows up in:** [Department Top Three Salaries](185-department-top-three-salaries.md) (`DENSE_RANK` per group) · [Nth Highest Salary](177-nth-highest-salary.md) (picking one dense rank) · [Second Highest Salary](176-second-highest-salary.md) (distinct ordering).

</details>

---
