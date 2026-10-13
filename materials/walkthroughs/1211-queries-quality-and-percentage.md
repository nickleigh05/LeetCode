# 1211. Queries Quality and Percentage

**Easy** · [LeetCode](https://leetcode.com/problems/queries-quality-and-percentage/) · [Solution file (no hints)](../../problems/1000-1499/1211.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each query name, report its **quality** — the average of `rating / position` — and its **poor query percentage** — the share of rows with `rating < 3`, as a percentage. Round both to 2 decimals. Any order.

```
Table: Queries
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| query_name  | varchar |
| result      | varchar |
| position    | int     |
| rating      | int     |
+-------------+---------+
This table may have duplicate rows.
This table contains information collected from some queries on a database.
The position column has a value from 1 to 500.
The rating column has a value from 1 to 5. Query with rating less than 3 is a poor query.
```

```
Input:
Queries table:
+------------+-------------------+----------+--------+
| query_name | result            | position | rating |
+------------+-------------------+----------+--------+
| Dog        | Golden Retriever  | 1        | 5      |
| Dog        | German Shepherd   | 2        | 5      |
| Dog        | Mule              | 200      | 1      |
| Cat        | Shirazi           | 5        | 2      |
| Cat        | Siamese           | 3        | 3      |
| Cat        | Sphynx            | 7        | 4      |
+------------+-------------------+----------+--------+
Output:
+------------+---------+-----------------------+
| query_name | quality | poor_query_percentage |
+------------+---------+-----------------------+
| Dog        | 2.50    | 33.33                 |
| Cat        | 0.66    | 33.33                 |
+------------+---------+-----------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Two aggregates over the same groups. The first is an average of a computed value; the second is the "share of rows that match a condition" pattern.

| The statement says | Which really means |
|---|---|
| "the average of the ratio between query rating and its position" | Compute `rating / position` **per row**, then average — `AVG(rating / position)` |
| "percentage of all queries with rating less than 3" | Share of the group's rows where `rating < 3`, × 100 |
| "for each `query_name`" | `GROUP BY query_name` |
| "may have duplicate rows" | Each row counts — don't dedupe |
| both "rounded to 2 decimal places" | `ROUND(…, 2)` on each |

The share of rows matching a condition is the **average of a 1/0 flag**: in MySQL, `rating < 3` already *is* 1 or 0.

🤔 **Before you open the next section:** what's `AVG` of the values 1, 0, 0?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`AVG` of a ratio and of a flag** | `AVG(rating / position)`, `AVG(rating < 3) * 100` | ✅ Both aggregates in one pass |
| `SUM(CASE …) / COUNT(*)` | `SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END) * 100 / COUNT(*)` | ✅ Portable to databases where comparisons aren't numbers |
| Ratio of averages | `AVG(rating) / AVG(position)` | ❌ Not the same thing — the average of ratios ≠ the ratio of averages |

**The decision: `AVG` of each per-row value.** In MySQL a comparison returns 1, 0, or `NULL`, so `AVG(rating < 3)` is directly the fraction of poor queries.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT query_name,
       ROUND(AVG(rating / position), 2) AS quality,
       ROUND(AVG(rating < 3) * 100, 2) AS poor_query_percentage
```

**Two aggregates, each rounded.**

- `rating / position` is computed per row, then `AVG` averages those ratios across the group.
- `rating < 3` is 1 for a poor query and 0 otherwise; averaging gives the fraction, and `* 100` makes it a percentage.

→ [aggregate-functions](../sql/aggregate-functions.md) · [conditional-aggregation](../sql/conditional-aggregation.md) · [ratios-percentages](../sql/ratios-percentages.md)

```sql
FROM Queries
```

```sql
GROUP BY query_name;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT query_name,
       ROUND(AVG(rating / position), 2) AS quality,
       ROUND(AVG(rating < 3) * 100, 2) AS poor_query_percentage
FROM Queries
GROUP BY query_name;
```

</details>

**Trace it** — the two per-row values:

| `query_name` | `position` | `rating` | `rating / position` | `rating < 3` |
|---|---|---|---|---|
| Dog | 1 | 5 | 5.0000 | 0 |
| Dog | 2 | 5 | 2.5000 | 0 |
| Dog | 200 | 1 | 0.0050 | 1 |
| Cat | 5 | 2 | 0.4000 | 1 |
| Cat | 3 | 3 | 1.0000 | 0 |
| Cat | 7 | 4 | 0.5714 | 0 |

Dog: quality = (5 + 2.5 + 0.005) / 3 = 2.50; poor = 1 of 3 → 33.33. Cat: quality = (0.4 + 1 + 0.5714) / 3 = 0.66; poor = 1 of 3 → 33.33.

MySQL returns `/` as a decimal with 4 digits after the point here (`0.5714`), which is plenty of precision before the final round to 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass, updating two running sums and a count for the row's group.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(g)</summary>

**O(g)** for g distinct query names — a few accumulators each.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Group by query name. Quality is the average of the per-row ratio `rating / position`. The poor percentage is the average of the flag `rating < 3` times 100 — in MySQL the comparison is already 1 or 0. Round both to two places."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `AVG(rating < 3)` work?" | The comparison is 1 or 0; the average of 1s and 0s is the share of 1s. |
| "Why not `AVG(rating) / AVG(position)`?" | Different number. For Dog: 11/3 ÷ 203/3 ≈ 0.05, nowhere near 2.50. |
| "In PostgreSQL?" | Comparisons are booleans there; write `AVG(CASE WHEN rating < 3 THEN 1 ELSE 0 END)`. |
| "What if `query_name` could be `NULL`?" | `NULL`s form their own group. Add `WHERE query_name IS NOT NULL` if they shouldn't be reported. |

**Traps:**

- **Ratio of averages** instead of average of ratios.
- **Forgetting `* 100`** — the percentage comes out as 0.33.
- **Deduplicating rows** — duplicates are separate queries.

**This same move shows up in:** [Confirmation Rate](1934-confirmation-rate.md) (average of a flag) · [Monthly Transactions I](1193-monthly-transactions-i.md) (several conditional aggregates at once) · [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (a percentage from a flag).

</details>

---
