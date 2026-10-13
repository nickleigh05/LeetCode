# 197. Rising Temperature

**Easy** · [LeetCode](https://leetcode.com/problems/rising-temperature/) · [Solution file (no hints)](../../problems/0001-0499/197.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find the ids of days that were warmer than the **day before**. Any order.

```
Table: Weather
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+
id is the column with unique values for this table.
There are no different rows with the same recordDate.
This table contains information about the temperature on a certain day.
```

```
Input:
Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+
Output:
+----+
| id |
+----+
| 2  |
| 4  |
+----+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Each answer compares **two rows of the same table**: a day and the day before it. When one row needs to see another row of the same table, join the table to itself.

| The statement says | Which really means |
|---|---|
| "compared to its previous dates (yesterday)" | The row whose `recordDate` is exactly one day earlier — not just the previous row |
| "no different rows with the same `recordDate`" | At most one "yesterday" per day |
| `id` and `recordDate` both look sequential | Don't trust it. Ids can be out of date order, and days can be missing |
| "higher temperatures" | Strictly greater: `>` |
| the first day has no yesterday | It can't qualify — it should simply have no partner |

🤔 **Before you open the next section:** if 2015-01-02 were missing from the table, should 2015-01-03 be compared to 2015-01-01?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Self-join on date difference** | `JOIN Weather y ON DATEDIFF(t.recordDate, y.recordDate) = 1` | ✅ Pairs each day with the calendar day before — gaps handled |
| Self-join on `DATE_SUB` | `ON y.recordDate = DATE_SUB(t.recordDate, INTERVAL 1 DAY)` | ✅ Same thing; an equality, so an index on `recordDate` could serve it |
| `LAG` + a date check | `LAG(temperature) OVER (ORDER BY recordDate)`, then check the dates are one day apart | ✅ Works — **only** with the date check |
| `LAG` alone | `WHERE temperature > LAG(temperature) …` | ❌ Compares with the previous *row*, which may be days earlier |
| Join on `id = id + 1` | `ON t.id = y.id + 1` | ❌ Assumes ids follow the dates with no gaps |
| `recordDate - 1` | `ON y.recordDate = t.recordDate - 1` | ❌ Date minus a number isn't date arithmetic in MySQL — see below |

**The decision: a self-join on `DATEDIFF(…) = 1`.** It encodes "yesterday" exactly, whatever the ids or gaps look like.

**Why the shortcuts fail.** Take a week with a missing day — 2015-01-02 isn't recorded:

| `id` | `recordDate` | `temperature` | `LAG(temperature)` | `LAG says warmer?` |
|---|---|---|---|---|
| 1 | 2015-01-01 | 10 | `NULL` | `NULL` |
| 2 | 2015-01-03 | 25 | 10 | 1 |
| 3 | 2015-01-04 | 20 | 25 | 0 |
| 4 | 2015-01-05 | 30 | 20 | 1 |

`LAG` happily compares Jan 3 with Jan 1 and calls it warmer. Jan 3 has no yesterday, so it must not qualify. The date-based join gets this right — Jan 3 simply finds no partner:

| `today.id` | `today` | `yesterday` |
|---|---|---|
| 3 | 2015-01-04 | 2015-01-03 |
| 4 | 2015-01-05 | 2015-01-04 |

And never subtract a plain number from a date in MySQL. It converts the date to a number like `20150301` and subtracts from that:

| `DATE('2015-01-02') - 1` | `DATE('2015-03-01') - 1` | `DATE('2015-03-01') - INTERVAL 1 DAY` |
|---|---|---|
| 20150101 | 20150300 | 2015-02-28 |

The first one looks right by luck. The second isn't a date at all. Use `INTERVAL`, `DATE_SUB`, or `DATEDIFF`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT today.id
```

```sql
FROM Weather today
```

**Two copies of the same table, with names that say what they are.** `today` and `yesterday` are aliases for the same `Weather` table. A self-join needs aliases — otherwise there's no way to say which copy a column comes from.
→ [self-join](../sql/self-join.md) · [aliases](../sql/aliases.md)

```sql
JOIN Weather yesterday
    ON DATEDIFF(today.recordDate, yesterday.recordDate) = 1
```

**Pair each day with the calendar day before it.** `DATEDIFF(a, b)` returns the number of days from `b` to `a`, so `= 1` means "yesterday is exactly one day earlier." Days with no recorded yesterday find no partner and drop out of the inner join — which is what we want.
→ [date-arithmetic](../sql/date-arithmetic.md) · [inner-join](../sql/inner-join.md)

```sql
WHERE today.temperature > yesterday.temperature;
```

**Keep the pairs where today is warmer.** `>` because the statement says "higher."
→ [where](../sql/where.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT today.id
FROM Weather today
JOIN Weather yesterday
    ON DATEDIFF(today.recordDate, yesterday.recordDate) = 1
WHERE today.temperature > yesterday.temperature;
```

</details>

**Trace it** — every (today, yesterday) pair the join produces:

| `today.id` | `today` | `t_today` | `yesterday` | `t_yesterday` | `warmer?` |
|---|---|---|---|---|---|
| 2 | 2015-01-02 | 25 | 2015-01-01 | 10 | 1 |
| 3 | 2015-01-03 | 20 | 2015-01-02 | 25 | 0 |
| 4 | 2015-01-04 | 30 | 2015-01-03 | 20 | 1 |

Jan 1 has no yesterday, so it never appears as `today`. Of the three pairs, ids 2 and 4 were warmer.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²) as written, O(n) with an equality join</summary>

**O(n²)** for n days, as written. `DATEDIFF(today.recordDate, yesterday.recordDate) = 1` wraps both columns in a function, so it can't serve as a join key. `EXPLAIN` shows an *inner hash join (no condition)* followed by a filter: every pair of rows is formed, then tested.

The `DATE_SUB` form — `yesterday.recordDate = DATE_SUB(today.recordDate, INTERVAL 1 DAY)` — is an **equality** on `yesterday.recordDate`, and `EXPLAIN` shows a hash join keyed on it: O(n). An index on `recordDate` would serve it too. On LeetCode's data sizes both pass; in an interview, mentioning the difference is a strong signal.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) to O(n) extra</summary>

The nested-loop version needs **O(1)** beyond the output. The hash-join version builds a table over the dates: **O(n)**.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each answer compares a day with the calendar day before it, so I join `Weather` to itself, pairing rows whose dates differ by exactly one day, and keep pairs where today is warmer. I don't rely on ids or on `LAG` alone, because both break when a day is missing."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it with a window function." | `LAG(temperature)` and `LAG(recordDate)` in a subquery, then `WHERE temperature > prev_temp AND DATEDIFF(recordDate, prev_date) = 1`. |
| "Warmer than **two** days ago?" | `DATEDIFF(…) = 2`, or `LAG(…, 2)` with the same date check. |
| "Three warmer days in a row?" | Chain the comparison, or use the consecutive-rows technique from [Consecutive Numbers](180-consecutive-numbers.md). |
| "Make the join index-friendly." | Equality on the bare column: `y.recordDate = t.recordDate - INTERVAL 1 DAY`. |
| "Report the temperature change too." | `SELECT today.id, today.temperature - yesterday.temperature AS delta …`. |

**Traps:**

- **`id = id + 1`** — ids aren't promised to follow the dates.
- **`LAG` without a date check** — the previous row isn't necessarily yesterday.
- **`recordDate - 1`** — numeric subtraction, not date arithmetic.
- **`>=`** — "higher" means strictly.

**This same move shows up in:** [Consecutive Numbers](180-consecutive-numbers.md) (comparing neighbouring rows) · [Game Play Analysis IV](550-game-play-analysis-iv.md) (a "next day" check) · [Average Time of Process per Machine](1661-average-time-of-process-per-machine.md) (a self-join that pairs two kinds of rows).

</details>

---
