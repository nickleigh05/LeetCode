# 1934. Confirmation Rate

**Medium** · [LeetCode](https://leetcode.com/problems/confirmation-rate/) · [Solution file (no hints)](../../problems/1500-1999/1934.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A user's confirmation rate is confirmed messages ÷ all requested messages, rounded to 2 decimals — and **0** for users who requested none. Report it for every user. Any order.

```
Table: Signups
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
+----------------+----------+
user_id is the column of unique values for this table.
Each row contains information about the signup time for the user with ID user_id.

Table: Confirmations
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
| action         | ENUM     |
+----------------+----------+
(user_id, time_stamp) is the primary key (combination of columns with unique values) for this table.
user_id is a foreign key (reference column) to the Signups table.
action is an ENUM (category) of the type ('confirmed', 'timeout')
Each row of this table indicates that the user with ID user_id requested a confirmation message at time_stamp and that confirmation message was either confirmed ('confirmed') or expired without confirming ('timeout').
```

```
Input:
Signups table:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 3       | 2020-03-21 10:16:13 |
| 7       | 2020-01-04 13:57:59 |
| 2       | 2020-07-29 23:09:44 |
| 6       | 2020-12-09 10:39:37 |
+---------+---------------------+
Confirmations table:
+---------+---------------------+-----------+
| user_id | time_stamp          | action    |
+---------+---------------------+-----------+
| 3       | 2021-01-06 03:30:46 | timeout   |
| 3       | 2021-07-14 14:00:00 | timeout   |
| 7       | 2021-06-12 11:57:29 | confirmed |
| 7       | 2021-06-13 12:58:28 | confirmed |
| 7       | 2021-06-14 13:59:27 | confirmed |
| 2       | 2021-01-22 00:00:00 | confirmed |
| 2       | 2021-02-28 23:59:59 | timeout   |
+---------+---------------------+-----------+
Output:
+---------+-------------------+
| user_id | confirmation_rate |
+---------+-------------------+
| 6       | 0.00              |
| 3       | 0.00              |
| 7       | 1.00              |
| 2       | 0.50              |
+---------+-------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A ratio per user, where some users have no rows to take a ratio of. Two lessons meet here: keep the users with no matches, and make sure they come out as `0.00`, not `NULL`.

| The statement says | Which really means |
|---|---|
| "the confirmation rate **of each user**" | Every user in `Signups` appears — user 6 has no confirmations at all |
| "confirmed ÷ total requested" | A fraction of rows → the **average of a 1/0 flag** |
| "a user that did not request any … is 0" | Not `NULL`. Users with no rows need special care |
| "round … to two decimal places" | `ROUND(…, 2)` |
| `action` is an ENUM | Compare to the string `'confirmed'` |

**The key trick:** the share of rows that satisfy a condition is `AVG` of a value that's 1 when the condition holds and 0 when it doesn't. User 2 has one confirmed, one timeout → AVG(1, 0) = 0.5.

🤔 **Before you open the next section:** after a `LEFT JOIN`, user 6 has one row with `action = NULL`. What should that row contribute to the average so the result is 0?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT JOIN` + `AVG(IF(…, 1, 0))`** | `ROUND(AVG(IF(c.action = 'confirmed', 1, 0)), 2)` | ✅ `NULL` actions become 0, so user 6 averages to 0 |
| Sum ÷ count, wrapped in `IFNULL` | `ROUND(IFNULL(SUM(c.action = 'confirmed') / COUNT(c.action), 0), 2)` | ✅ Explicit; `0/0` is `NULL` in MySQL, hence the `IFNULL` |
| `AVG(c.action = 'confirmed')` | the comparison directly | ❌ For user 6 that's `AVG(NULL)` → `NULL`, not 0 |
| Inner join | `Signups s JOIN Confirmations c …` | ❌ User 6 disappears |

**The decision: `LEFT JOIN` with `AVG(IF(…, 1, 0))`.** `IF` turns "confirmed" into 1 and *everything else — including `NULL`* — into 0, so users with no messages average exactly 0.

Here's what goes wrong with the plain comparison:

| `user_id` | `AVG(c.action = 'confirmed')` |
|---|---|
| 3 | 0.0000 |
| 7 | 1.0000 |
| 2 | 0.5000 |
| 6 | `NULL` |

`NULL = 'confirmed'` is `NULL`, and `AVG` of nothing but `NULL`s is `NULL`. And with an inner join, user 6 isn't even there:

| `user_id` | `confirmation_rate` |
|---|---|
| 3 | 0.00 |
| 7 | 1.00 |
| 2 | 0.50 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT s.user_id,
       ROUND(AVG(IF(c.action = 'confirmed', 1, 0)), 2) AS confirmation_rate
```

**The rate, as an average of 1s and 0s.** `IF(cond, 1, 0)` returns 1 when the condition is true and 0 when it's false **or unknown** — that's what rescues user 6. `AVG` divides the 1s by the number of rows; `ROUND(…, 2)` formats the result.
→ [if-function](../sql/if-function.md) · [conditional-aggregation](../sql/conditional-aggregation.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Signups s
```

```sql
LEFT JOIN Confirmations c
    ON s.user_id = c.user_id
```

**Keep every user, attach their messages.** A user with three messages becomes three rows; user 6 becomes one row of `NULL`s.
→ [left-join](../sql/left-join.md)

```sql
GROUP BY s.user_id;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT s.user_id,
       ROUND(AVG(IF(c.action = 'confirmed', 1, 0)), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c
    ON s.user_id = c.user_id
GROUP BY s.user_id;
```

</details>

**Trace it** — each joined row and the flag it contributes:

| `user_id` | `action` | `IF(confirmed, 1, 0)` |
|---|---|---|
| 2 | confirmed | 1 |
| 2 | timeout | 0 |
| 3 | timeout | 0 |
| 3 | timeout | 0 |
| 6 | `NULL` | 0 |
| 7 | confirmed | 1 |
| 7 | confirmed | 1 |
| 7 | confirmed | 1 |

User 2: (1 + 0) / 2 = 0.50. User 3: 0.00. User 6: one row, flag 0 → 0.00. User 7: 1.00.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(u + c)</summary>

**O(u + c)** for u users and c confirmation rows: a hash join on `user_id`, then one grouping pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u + c)</summary>

**O(c)** for the hash table and **O(u)** for one running average per user.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every user must appear, so I left-join confirmations onto signups. The rate is the share of confirmed rows, which is the average of a 1/0 flag. I use `IF(action = 'confirmed', 1, 0)` so the `NULL` row from users with no messages counts as 0 instead of making the average `NULL`. Round to two places at the end."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `AVG` of a flag give a ratio?" | AVG = sum ÷ count. The sum of 1/0 flags is the number of matches; the count is the number of rows. |
| "Write it as SUM ÷ COUNT." | `SUM(c.action = 'confirmed') / COUNT(c.action)` — and wrap it in `IFNULL(…, 0)`, because `0/0` gives `NULL` in MySQL. |
| "As a percentage?" | `ROUND(100 * AVG(…), 2)`. |
| "Only users with a rate below 0.5?" | `HAVING confirmation_rate < 0.5` — MySQL allows the alias in `HAVING`. |
| "Count each user's timeouts too." | `SUM(c.action = 'timeout')` in the same `SELECT`. |

**Traps:**

- **Inner join** — users with no confirmations vanish.
- **`AVG(c.action = 'confirmed')`** — `NULL` instead of 0 for those users.
- **`COUNT(*)` in a hand-written ratio** — counts user 6's `NULL` row as a message.
- **Rounding too early** — round the final ratio, not the parts.

**This same move shows up in:** [Queries Quality and Percentage](1211-queries-quality-and-percentage.md) (the average-of-a-flag trick) · [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (a percentage of rows) · [Employee Bonus](577-employee-bonus.md) (left join with `NULL`s that need handling).

</details>

---
