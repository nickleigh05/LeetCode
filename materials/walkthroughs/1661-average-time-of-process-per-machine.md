# 1661. Average Time of Process per Machine

**Easy** · [LeetCode](https://leetcode.com/problems/average-time-of-process-per-machine/) · [Solution file (no hints)](../../problems/1500-1999/1661.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Each process on a machine has a `start` row and an `end` row. Find every machine's average process duration (`end − start`), rounded to 3 decimals, as `processing_time`. Any order.

```
Table: Activity
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| machine_id     | int     |
| process_id     | int     |
| activity_type  | enum    |
| timestamp      | float   |
+----------------+---------+
The table shows the user activities for a factory website.
(machine_id, process_id, activity_type) is the primary key (combination of columns with unique values) of this table.
machine_id is the ID of a machine.
process_id is the ID of a process running on the machine with ID machine_id.
activity_type is an ENUM (category) of type ('start', 'end').
timestamp is a float representing the current time in seconds.
'start' means the machine starts the process at the given timestamp and 'end' means the machine ends the process at the given timestamp.
The `start` timestamp will always be less than or equal to the `end` timestamp for every `(machine_id, process_id)` pair.
It is guaranteed that each (machine_id, process_id) pair has a 'start' and 'end' timestamp.
```

```
Input:
Activity table:
+------------+------------+---------------+-----------+
| machine_id | process_id | activity_type | timestamp |
+------------+------------+---------------+-----------+
| 0          | 0          | start         | 0.712     |
| 0          | 0          | end           | 1.520     |
| 0          | 1          | start         | 3.140     |
| 0          | 1          | end           | 4.120     |
| 1          | 0          | start         | 0.550     |
| 1          | 0          | end           | 1.550     |
| 1          | 1          | start         | 0.430     |
| 1          | 1          | end           | 1.420     |
| 2          | 0          | start         | 4.100     |
| 2          | 0          | end           | 4.512     |
| 2          | 1          | start         | 2.500     |
| 2          | 1          | end           | 5.000     |
+------------+------------+---------------+-----------+
Output:
+------------+-----------------+
| machine_id | processing_time |
+------------+-----------------+
| 0          | 0.894           |
| 1          | 0.995           |
| 2          | 1.456           |
+------------+-----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The two numbers you need to subtract are on **different rows**. Before you can average durations, you have to get each process's start and end onto one row.

| The statement says | Which really means |
|---|---|
| `start` and `end` are separate rows | A row only knows one timestamp — pair the two rows up first |
| `(machine_id, process_id, activity_type)` is the key | Each process has exactly one start row and one end row |
| "time to complete a process is end − start" | One duration per (machine, process) pair |
| "average … per machine" | `GROUP BY machine_id`, then `AVG` |
| "rounded to 3 decimal places" | `ROUND(…, 3)` on the final average |
| `timestamp` is a **float** | Floating-point values are approximate — rounding isn't cosmetic here |

🤔 **Before you open the next section:** how do you put a process's `start` row and its `end` row side by side, using only the `Activity` table?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Self-join start rows to end rows** | `Activity s JOIN Activity e ON` same machine, same process, `s` = start, `e` = end | ✅ Builds one row per process with both timestamps |
| Signed sum | `SUM(IF(activity_type = 'end', timestamp, -timestamp)) / COUNT(DISTINCT process_id)` | ✅ Clever and join-free: each process contributes `end − start` |
| Conditional aggregation per process | `MAX(IF(type = 'end', …)) - MAX(IF(type = 'start', …))` in a subquery, then `AVG` | ✅ Works; two levels of grouping |
| `AVG(timestamp)` by machine | `GROUP BY machine_id` on the raw table | ❌ Averages timestamps, not durations |

**The decision: the self-join.** It makes the shape of the data explicit — one row per process, start and end side by side — and every later step is ordinary grouping.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT s.machine_id,
       ROUND(AVG(e.timestamp - s.timestamp), 3) AS processing_time
```

**Average the durations, then round.** `e.timestamp - s.timestamp` is one process's duration; `AVG` averages it over the machine's group; `ROUND(…, 3)` rounds the result. Round **after** averaging — rounding each duration first can shift the final digit.
→ [aggregate-functions](../sql/aggregate-functions.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Activity s
```

```sql
JOIN Activity e
    ON  s.machine_id = e.machine_id
    AND s.process_id = e.process_id
    AND s.activity_type = 'start'
    AND e.activity_type = 'end'
```

**Pair each start with its end.** Two copies of `Activity`: `s` for start rows, `e` for end rows. The four conditions say "same machine, same process, one is the start, the other is the end." Because each process has exactly one of each, every process produces exactly one joined row.

Putting the `activity_type` tests in `ON` (instead of `WHERE`) is a style choice for an inner join — the result is the same.
→ [self-join](../sql/self-join.md) · [on-vs-where](../sql/on-vs-where.md)

```sql
GROUP BY s.machine_id;
```

**One output row per machine.**
→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT s.machine_id,
       ROUND(AVG(e.timestamp - s.timestamp), 3) AS processing_time
FROM Activity s
JOIN Activity e
    ON  s.machine_id = e.machine_id
    AND s.process_id = e.process_id
    AND s.activity_type = 'start'
    AND e.activity_type = 'end'
GROUP BY s.machine_id;
```

</details>

**Trace it** — the joined rows, one per process:

| `machine_id` | `process_id` | `start` | `end` | `duration` |
|---|---|---|---|---|
| 0 | 0 | 0.712 | 1.52 | 0.808 |
| 0 | 1 | 3.14 | 4.12 | 0.98 |
| 1 | 0 | 0.55 | 1.55 | 1.0 |
| 1 | 1 | 0.43 | 1.42 | 0.99 |
| 2 | 0 | 4.1 | 4.512 | 0.412 |
| 2 | 1 | 2.5 | 5.0 | 2.5 |

Machine 0 averages (0.808 + 0.98) / 2 = 0.894. Machine 1: (1.0 + 0.99) / 2 = 0.995. Machine 2: (0.412 + 2.5) / 2 = 1.456.

**Why rounding matters on floats.** Without `ROUND`, MySQL shows the raw floating-point averages:

| `machine_id` | `AVG(e.timestamp - s.timestamp)` |
|---|---|
| 0 | 0.8939998745918274 |
| 1 | 0.9949999451637268 |
| 2 | 1.4560000896453857 |

`FLOAT` stores binary approximations of decimal numbers, so `0.894` comes back as `0.89399987…`. `ROUND(…, 3)` gives the answer the problem expects.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n activity rows. The join has equality conditions on `machine_id` and `process_id`, so MySQL hash-joins: one pass to build, one to probe. Each start meets only its own end. Grouping is another linear pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the join's hash table, plus one accumulator per machine for the grouping.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Start and end are on separate rows, so I self-join `Activity`: start rows on one side, end rows on the other, matched on machine and process. That gives one row per process with both timestamps. Then it's `AVG(end − start)` per machine, rounded to three places at the end."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it without a join." | `SUM(IF(activity_type = 'end', timestamp, -timestamp)) / COUNT(DISTINCT process_id)` — each process adds `end − start` to the sum. |
| "What if a process is missing its end row?" | The inner join drops it, which is reasonable: an unfinished process has no duration. The signed-sum trick would get it wrong. |
| "The longest process per machine?" | `MAX(e.timestamp - s.timestamp)` instead of `AVG`. |
| "Why round after averaging?" | Rounding each duration first loses precision before the division. Round once, at the end. |
| "Should `timestamp` be a FLOAT?" | Not in a real schema — `DECIMAL` stores exact decimals, and real timestamps would be `DATETIME`/`TIMESTAMP`. |

**Traps:**

- **Averaging raw timestamps** — `AVG(timestamp)` has nothing to do with durations.
- **Forgetting `ROUND`** — float noise in the 7th decimal makes the answer wrong.
- **Joining on `machine_id` only** — pairs every start with every end on the machine.

**This same move shows up in:** [Rising Temperature](197-rising-temperature.md) (a self-join pairing a row with a related row) · [Confirmation Rate](1934-confirmation-rate.md) (`AVG` over a computed value, rounded) · [Monthly Transactions I](1193-monthly-transactions-i.md) (conditional sums).

</details>

---
