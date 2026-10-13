# 1204. Last Person to Fit in the Bus

**Medium** · [LeetCode](https://leetcode.com/problems/last-person-to-fit-in-the-bus/) · [Solution file (no hints)](../../problems/1000-1499/1204.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

People board a bus in `turn` order. The bus holds **1000 kg**. Find the name of the last person who can board without the total going over the limit.

```
Table: Queue
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| person_id   | int     |
| person_name | varchar |
| weight      | int     |
| turn        | int     |
+-------------+---------+
person_id column contains unique values.
This table has the information about all people waiting for a bus.
The person_id and turn columns will contain all numbers from 1 to n, where n is the number of rows in the table.
turn determines the order of which the people will board the bus, where turn=1 denotes the first person to board and turn=n denotes the last person to board.
weight is the weight of the person in kilograms.
```

```
Input:
Queue table:
+-----------+-------------+--------+------+
| person_id | person_name | weight | turn |
+-----------+-------------+--------+------+
| 5         | Alice       | 250    | 1    |
| 4         | Bob         | 175    | 5    |
| 3         | Alex        | 350    | 2    |
| 6         | John Cena   | 400    | 3    |
| 1         | Winston     | 500    | 6    |
| 2         | Marie       | 200    | 4    |
+-----------+-------------+--------+------+
Output:
+-------------+
| person_name |
+-------------+
| John Cena   |
+-------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Whether someone fits depends on **everyone before them** in the queue: you need a running total in boarding order.

| The statement says | Which really means |
|---|---|
| `turn` decides the boarding order | Sort by `turn`, not by `person_id` — they differ in the example |
| "weight limit of 1000 kilograms" | The running total must stay `<= 1000` |
| "the last person that can fit" | The latest turn whose running total is still within the limit |
| "the first person does not exceed the weight limit" | There's always an answer |
| John Cena's total is exactly 1000 | `<=`, not `<` — exactly at the limit still fits |

Once the total passes 1000 it can only grow, so everyone with a running total `<= 1000` boards, and the answer is the last of them.

🤔 **Before you open the next section:** what's the running total at each turn in the example, and which is the last one that's at most 1000?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Window running total** | `SUM(weight) OVER (ORDER BY turn)`, keep `<= 1000`, take the highest turn | ✅ One pass, says "running total" directly |
| Self-join running total | join each person to everyone with `q2.turn <= q1.turn`, `HAVING SUM(q2.weight) <= 1000` | ✅ Works without window functions — O(n²) |
| Order by `person_id` | `SUM(weight) OVER (ORDER BY person_id)` | ❌ Wrong boarding order |
| `< 1000` | | ❌ Excludes John Cena, who brings the total to exactly 1000 |

**The decision: a window `SUM`.** `SUM(...) OVER (ORDER BY turn)` gives, on each row, the total weight of that person and everyone ahead of them.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT person_name
```

```sql
FROM (
    SELECT person_name, turn,
           SUM(weight) OVER (ORDER BY turn) AS total_weight
    FROM Queue
) boarding
```

**Running total per boarding turn.** A window function computes a value for each row from a set of related rows — here, every row up to the current turn. With `ORDER BY` and no explicit frame, `SUM` adds from the first row through the current one. The window result can't be filtered in the same query's `WHERE` (`WHERE` runs first), so the calculation goes in a derived table.
→ [running-totals](../sql/running-totals.md) · [window-functions](../sql/window-functions.md) · [derived-tables](../sql/derived-tables.md)

```sql
WHERE total_weight <= 1000
```

**Everyone who fits.**

```sql
ORDER BY turn DESC
```

```sql
LIMIT 1;
```

**The last of them.** Sort by turn, latest first, and keep one row.
→ [order-by](../sql/order-by.md) · [limit-offset](../sql/limit-offset.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT person_name
FROM (
    SELECT person_name, turn,
           SUM(weight) OVER (ORDER BY turn) AS total_weight
    FROM Queue
) boarding
WHERE total_weight <= 1000
ORDER BY turn DESC
LIMIT 1;
```

</details>

**Trace it** — the running total in boarding order:

| `turn` | `person_name` | `weight` | `total_weight` |
|---|---|---|---|
| 1 | Alice | 250 | 250 |
| 2 | Alex | 350 | 600 |
| 3 | John Cena | 400 | 1000 |
| 4 | Marie | 200 | 1200 |
| 5 | Bob | 175 | 1375 |
| 6 | Winston | 500 | 1875 |

Turns 1–3 stay within 1000; turn 4 pushes it to 1200. The last person who fits is John Cena.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** — sorting by `turn` for the window, then a linear pass to accumulate the total. The self-join version is **O(n²)**: every person is paired with everyone ahead of them.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the sorted rows with their running totals.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Whether someone fits depends on everyone ahead, so I compute a running total with `SUM(weight) OVER (ORDER BY turn)` in a subquery. Everyone whose total is at most 1000 boards; the answer is the one with the highest turn among them."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Without window functions?" | Self-join `q2.turn <= q1.turn`, group by `q1`, `HAVING SUM(q2.weight) <= 1000`, take the max turn. O(n²). |
| "What if someone heavy is skipped and lighter people behind them still board?" | Then it's a different rule — not a prefix — and a running total no longer works; you'd need a recursive CTE simulating each turn. |
| "Everyone who boards?" | Drop the `ORDER BY … LIMIT 1`. |
| "How much spare capacity is left?" | `1000 - MAX(total_weight)` over the rows that fit. |

**Traps:**

- **Ordering by `person_id`** — `turn` is the boarding order.
- **`<` instead of `<=`.**
- **Filtering the window result in the same `WHERE`** — window functions are computed after `WHERE`; use a subquery.

**This same move shows up in:** [Restaurant Growth](1321-restaurant-growth.md) (a window sum over a moving range) · [Consecutive Numbers](180-consecutive-numbers.md) (order-dependent logic) · [Department Top Three Salaries](185-department-top-three-salaries.md) (window functions per group).

</details>

---
