# 626. Exchange Seats

**Medium** · [LeetCode](https://leetcode.com/problems/exchange-seats/) · [Solution file (no hints)](../../problems/0500-0999/626.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Swap the seats of every two consecutive students: 1 ↔ 2, 3 ↔ 4, and so on. With an odd count, the last student stays put. Return the result ordered by `id`.

```
Table: Seat
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| student     | varchar |
+-------------+---------+
id is the primary key (unique value) column for this table.
Each row of this table indicates the name and the ID of a student.
The ID sequence always starts from 1 and increments continuously.
```

```
Input:
Seat table:
+----+---------+
| id | student |
+----+---------+
| 1  | Abbot   |
| 2  | Doris   |
| 3  | Emerson |
| 4  | Green   |
| 5  | Jeames  |
+----+---------+
Output:
+----+---------+
| id | student |
+----+---------+
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |
+----+---------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

You don't actually move students — you **relabel** each row's id, then sort. Every row's new id follows from its old id with simple arithmetic.

| The statement says | Which really means |
|---|---|
| "The ID sequence always starts from 1 and increments continuously" | No gaps — so pairs are (1,2), (3,4), … and id arithmetic is safe |
| "swap … every two consecutive students" | Odd id → next one up (`id + 1`); even id → next one down (`id - 1`) |
| "If the number of students is odd, the id of the last student is not swapped" | The last odd id has no partner — it keeps its id |
| "ordered by id" | Sort by the **new** id |

🤔 **Before you open the next section:** for an odd id, how can you tell whether it's the last row, with nobody to swap with?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`CASE` on the id** | odd and last → `id`; odd → `id + 1`; even → `id - 1` | ✅ Pure arithmetic, then sort |
| `LEAD`/`LAG` on the name | odd rows take the next student's name, even rows the previous one's | ✅ Moves names instead of ids; `COALESCE` handles the last odd row |
| Self-join on the partner id | join each row to `id ^ 1`'s row | ⚠️ Works, but the unpaired last row needs a `LEFT JOIN` and `COALESCE` |
| `CASE` without the last-row check | odd → `id + 1` always | ❌ An odd count leaves student 5 at id 6, which doesn't exist |

**The decision: the `CASE` on ids.** Three branches mirror the three situations in the statement.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT CASE
           WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM Seat) THEN id
           WHEN id % 2 = 1 THEN id + 1
           ELSE id - 1
       END AS id,
       student
```

**Compute each student's new seat.** `CASE` takes the first `WHEN` that's true, so the order matters: check "odd **and** last" before the general odd rule. `(SELECT MAX(id) FROM Seat)` is a scalar subquery giving the highest id. The result is aliased `id`, replacing the old value in the output.
→ [case-when](../sql/case-when.md) · [scalar-subquery](../sql/scalar-subquery.md) · [arithmetic-operators](../sql/arithmetic-operators.md)

```sql
FROM Seat
```

```sql
ORDER BY id;
```

**Sort by the new id.** In `ORDER BY`, MySQL resolves `id` to the `SELECT` alias first — the computed seat — which is what we want. To make that unmistakable, you could name the alias differently and order by it.
→ [order-by](../sql/order-by.md) · [aliases](../sql/aliases.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT CASE
           WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM Seat) THEN id
           WHEN id % 2 = 1 THEN id + 1
           ELSE id - 1
       END AS id,
       student
FROM Seat
ORDER BY id;
```

</details>

**Trace it** — each student's old and new seat:

| `old id` | `student` | `new id` |
|---|---|---|
| 1 | Abbot | 2 |
| 2 | Doris | 1 |
| 3 | Emerson | 4 |
| 4 | Green | 3 |
| 5 | Jeames | 5 |

Sorted by the new id, the students read Doris, Abbot, Green, Emerson, Jeames.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)** — a constant amount of work per row (the `MAX` subquery is computed once), then a sort by the new id.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the sort.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I relabel ids rather than moving names: odd ids go up by one, even ids go down by one, except an odd id that's also the maximum, which stays. Then I order by the new id. This relies on ids being continuous from 1, which the statement guarantees."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if ids had gaps?" | Pair by position instead: number the rows with `ROW_NUMBER() OVER (ORDER BY id)` and swap on that. |
| "Do it with window functions." | Keep ids, swap names: `CASE WHEN id % 2 = 1 THEN COALESCE(LEAD(student) OVER (ORDER BY id), student) ELSE LAG(student) OVER (ORDER BY id) END`. |
| "Actually update the table?" | Swapping primary-key values in place can collide mid-update; the safe route is to update names, not ids. |
| "Is there a one-liner for the new id?" | `(id + 1) ^ 1 - 1` maps 1↔2, 3↔4 — clever, but you'd still need the last-row check. |

**Traps:**

- **No last-row check** — an odd count produces a seat that doesn't exist.
- **`CASE` branches in the wrong order** — the general odd rule would catch the last row first.
- **Forgetting the final sort.**

**This same move shows up in:** [Triangle Judgement](610-triangle-judgement.md) (`CASE` computing a value per row) · [Consecutive Numbers](180-consecutive-numbers.md) (pairing rows by neighbouring ids) · [Rising Temperature](197-rising-temperature.md) (relating a row to its neighbour).

</details>

---
