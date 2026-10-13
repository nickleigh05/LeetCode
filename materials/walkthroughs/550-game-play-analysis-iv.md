# 550. Game Play Analysis IV

**Medium** · [LeetCode](https://leetcode.com/problems/game-play-analysis-iv/) · [Solution file (no hints)](../../problems/0500-0999/550.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

What fraction of players logged in again **on the day right after their first login**? Round to 2 decimals.

```
Table: Activity
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with unique values) of this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.
```

```
Input:
Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-03-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+
Output:
+-----------+
| fraction  |
+-----------+
| 0.33      |
+-----------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the day they first logged in" | Per player, `MIN(event_date)` |
| "logged in again on the day after" | A row for that player dated `first_login + 1 day` |
| "divide it by the number of total players" | Denominator: distinct players — every player, whether they came back or not |
| `(player_id, event_date)` is the key | At most one row per player per day — the "next day" row is either there or not |
| player 3 played on consecutive days … later | Only the day after the **first** login counts |

So for each player: did a row exist for their first login + 1? The answer is the share of players for whom it did.

🤔 **Before you open the next section:** if you left-join each player's first login to `Activity` on "same player, one day later," what does the joined column look like for a player who didn't come back?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **First-login subquery, `LEFT JOIN` the next day** | `COUNT(a.player_id) / COUNT(f.player_id)` | ✅ One row per player; the match either exists or it's `NULL` |
| Window `MIN`, then count | `MIN(event_date) OVER (PARTITION BY player_id)`, then `SUM(DATEDIFF(event_date, first) = 1) / COUNT(DISTINCT player_id)` | ✅ No join; clear once you know window functions |
| Tuple `IN` | `AVG((player_id, first + INTERVAL 1 DAY) IN (SELECT player_id, event_date FROM Activity))` | ✅ Compact: average of a 1/0 "came back?" flag |
| Any two consecutive days | self-join on `event_date + 1` with no first-login condition | ❌ Counts players who returned *later* in their history |

**The decision: the left join.** After it, each player is exactly one row — the next-day column is a date if they came back, `NULL` if not — and `COUNT(column)` counts only the non-`NULL`s.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT ROUND(COUNT(a.player_id) / COUNT(f.player_id), 2) AS fraction
```

**Players who came back ÷ all players.** `COUNT(a.player_id)` skips `NULL`s, so it counts only players whose next-day row was found. `COUNT(f.player_id)` counts every player. MySQL's `/` returns a decimal, so `1 / 3` is `0.3333`, and `ROUND` takes it to 0.33.
→ [count](../sql/count.md) · [ratios-percentages](../sql/ratios-percentages.md)

```sql
FROM (
    SELECT player_id, MIN(event_date) AS first_login
    FROM Activity
    GROUP BY player_id
) f
```

**Each player's first login, as a derived table.** A subquery in `FROM` acts like a temporary table — here, one row per player — and needs an alias (`f`).
→ [derived-tables](../sql/derived-tables.md) · [group-by](../sql/group-by.md)

```sql
LEFT JOIN Activity a
    ON  a.player_id = f.player_id
    AND a.event_date = f.first_login + INTERVAL 1 DAY;
```

**Look for a login exactly one day later.** `first_login + INTERVAL 1 DAY` is real date arithmetic — it handles month and year boundaries (`2016-02-28` + 1 day is `2016-02-29`). The left join keeps players with no such row.
→ [left-join](../sql/left-join.md) · [date-arithmetic](../sql/date-arithmetic.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT ROUND(COUNT(a.player_id) / COUNT(f.player_id), 2) AS fraction
FROM (
    SELECT player_id, MIN(event_date) AS first_login
    FROM Activity
    GROUP BY player_id
) f
LEFT JOIN Activity a
    ON  a.player_id = f.player_id
    AND a.event_date = f.first_login + INTERVAL 1 DAY;
```

</details>

**Trace it** — one row per player after the join:

| `player_id` | `first_login` | `next-day login` |
|---|---|---|
| 1 | 2016-03-01 | 2016-03-02 |
| 2 | 2017-06-25 | `NULL` |
| 3 | 2016-03-02 | `NULL` |

One of three players came back the next day → 1 / 3 = 0.33.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n activity rows: one grouping pass for first logins, then a hash join on `(player_id, event_date)` — an equality on both columns, since `first_login + INTERVAL 1 DAY` is computed on the derived table's side.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(p)** for p players' first logins, plus **O(n)** for the join's hash table.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I compute each player's first login in a derived table, then left-join `Activity` looking for the same player one day later. Each player is one row — a date if they returned, `NULL` if not — so returning players over all players is `COUNT(a.player_id) / COUNT(f.player_id)`, rounded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Retention within 7 days?" | Join on `a.event_date BETWEEN f.first_login + INTERVAL 1 DAY AND f.first_login + INTERVAL 7 DAY` and count `DISTINCT a.player_id` — now several rows can match. |
| "Why `COUNT(a.player_id)` and not `COUNT(*)`?" | `COUNT(*)` counts every row, including the `NULL` ones — it would always give 1.00. |
| "Do it with window functions." | `MIN(event_date) OVER (PARTITION BY player_id)` per row, then `SUM(DATEDIFF(event_date, first) = 1) / COUNT(DISTINCT player_id)`. |
| "Retention per signup date?" | Group the final query by `f.first_login`. |

**Traps:**

- **Consecutive days anywhere** — only the day after the *first* login counts.
- **Wrong denominator** — divide by all players, not by players with two or more logins.
- **`event_date - 1`** — numeric subtraction, not date arithmetic; see [Rising Temperature](197-rising-temperature.md).

**This same move shows up in:** [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (each customer's first order, then a percentage) · [Rising Temperature](197-rising-temperature.md) ("one day later" as a join condition) · [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md) (counting `NULL`s after a left join).

</details>

---
