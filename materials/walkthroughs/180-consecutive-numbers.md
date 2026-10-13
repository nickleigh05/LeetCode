# 180. Consecutive Numbers

**Medium** · [LeetCode](https://leetcode.com/problems/consecutive-numbers/) · [Solution file (no hints)](../../problems/0001-0499/180.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find every number that appears **at least three times in a row** (by `id`). Return each such number once, in a column named `ConsecutiveNums`.

```
Table: Logs
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column starting from 1.
```

```
Input:
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

"Three in a row" compares a row with the **next two** rows. In SQL, a row only sees itself — so bring the neighbours onto the same row, either by joining the table to itself or with window functions.

| The statement says | Which really means |
|---|---|
| "id is an autoincrement column starting from 1" | Consecutive rows have consecutive ids: `id`, `id + 1`, `id + 2` |
| "appear at least three times consecutively" | Some position where three neighbouring rows share a number |
| "at least" three | A run of four or five also contains a run of three — and would match more than once |
| output column `ConsecutiveNums` | Alias it — capital letters and all |
| each number once | `DISTINCT` |

🤔 **Before you open the next section:** for the row with `id = 1`, which rows are its two neighbours, and how would you find them with a join condition?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Triple self-join on ids** | `JOIN Logs b ON b.id = a.id + 1 … JOIN Logs c ON c.id = a.id + 2`, all with the same `num` | ✅ Direct: three rows side by side |
| `LAG`/`LEAD` | `LAG(num) OVER (ORDER BY id)` and `LAG(num, 2) …`, then compare | ✅ One scan; uses row order rather than id arithmetic |
| Gaps-and-islands | `id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id)` groups runs | ✅ Generalises to "at least k in a row" for any k |
| `GROUP BY num HAVING COUNT(*) >= 3` | counts occurrences anywhere | ❌ Not consecutive — 2 appears three times here, but not in a row |

**The decision: the triple self-join.** For a fixed run length of three, it's the clearest. `LAG`/`LEAD` is the window-function equivalent, and gaps-and-islands is what you reach for when k is large or variable.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT DISTINCT a.num AS ConsecutiveNums
```

**Each qualifying number once.** A run of four 1s contains two windows of three (starting at ids 1 and 2), so without `DISTINCT` the 1 would be reported twice.
→ [distinct](../sql/distinct.md) · [aliases](../sql/aliases.md)

```sql
FROM Logs a
```

```sql
JOIN Logs b ON b.id = a.id + 1 AND b.num = a.num
```

```sql
JOIN Logs c ON c.id = a.id + 2 AND c.num = a.num;
```

**Line up each row with the next two, and require all three to match.** `b` is the row right after `a`, `c` the one after that. Putting `num` equality in the join conditions means only matching triples are ever formed.
→ [self-join](../sql/self-join.md) · [consecutive-rows](../sql/consecutive-rows.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT DISTINCT a.num AS ConsecutiveNums
FROM Logs a
JOIN Logs b ON b.id = a.id + 1 AND b.num = a.num
JOIN Logs c ON c.id = a.id + 2 AND c.num = a.num;
```

</details>

**Trace it** — every (a, a+1, a+2) window, before the `num` equalities are applied:

| `a.id` | `a.num` | `b.num` | `c.num` |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 2 | 1 |
| 4 | 2 | 1 | 2 |
| 5 | 1 | 2 | 2 |

Only the window starting at id 1 has the same number three times. So the answer is 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — each join is an equality on `id`, so MySQL hash-joins; every row finds at most one neighbour at each offset.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the hash tables, plus the distinct set of results.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I need three neighbouring rows with the same number, so I join `Logs` to itself twice — the row at `id + 1` and the row at `id + 2` — requiring the same `num` each time. A longer run produces several matching windows, so I return `DISTINCT` numbers."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if ids have gaps?" | The id join treats a gap as a break in the run; `LAG`/`LEAD` ordered by id would treat the rows around the gap as neighbours. On ids 1, 2, 4 all holding 1, the join finds nothing and `LAG` finds 1. Clarify which the question means. |
| "At least **k** in a row?" | Gaps-and-islands: group by `num` and `id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id)`, then `HAVING COUNT(*) >= k`. |
| "Return the length of the longest run?" | Same grouping, then `MAX(COUNT(*))` per number. |
| "Why not `HAVING COUNT(*) >= 3`?" | Counts occurrences anywhere, not consecutive ones. |

**Traps:**

- **Missing `DISTINCT`** — long runs repeat the number.
- **Counting instead of comparing neighbours** — `COUNT(*) >= 3` ignores order.
- **Forgetting the column alias** — the expected header is `ConsecutiveNums`.

**This same move shows up in:** [Rising Temperature](197-rising-temperature.md) (comparing with the previous row) · [Exchange Seats](626-exchange-seats.md) (pairing neighbouring ids) · [Last Person to Fit in the Bus](1204-last-person-to-fit-in-the-bus.md) (an order-dependent computation with a window function).

</details>

---
