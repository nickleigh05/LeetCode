# 1633. Percentage of Users Attended a Contest

**Easy** · [LeetCode](https://leetcode.com/problems/percentage-of-users-attended-a-contest/) · [Solution file (no hints)](../../problems/1500-1999/1633.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each contest, find the percentage of **all users** who registered for it, rounded to 2 decimals. Sort by percentage, highest first; break ties by `contest_id` ascending.

```
Table: Users
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| user_name   | varchar |
+-------------+---------+
user_id is the primary key (column with unique values) for this table.
Each row of this table contains the name and the id of a user.

Table: Register
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| contest_id  | int     |
| user_id     | int     |
+-------------+---------+
(contest_id, user_id) is the primary key (combination of columns with unique values) for this table.
Each row of this table contains the id of a user and the contest they registered into.
```

```
Input:
Users table:
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Alice     |
| 2       | Bob       |
| 7       | Alex      |
+---------+-----------+
Register table:
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
| 209        | 7       |
| 209        | 6       |
| 215        | 7       |
| 208        | 7       |
| 210        | 2       |
| 207        | 2       |
| 210        | 7       |
+------------+---------+
Output:
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 208        | 100.0      |
| 209        | 100.0      |
| 210        | 100.0      |
| 215        | 66.67      |
| 207        | 33.33      |
+------------+------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A percentage needs a numerator and a denominator, and here they come from **different places**: the numerator is per contest, the denominator is one number for the whole table.

| The statement says | Which really means |
|---|---|
| "percentage of the users registered in each contest" | Registrations for the contest ÷ **total users** × 100 |
| `(contest_id, user_id)` is the key | No duplicate registrations — counting rows counts users |
| the denominator | The size of `Users`, the same for every contest → a subquery |
| "ordered by percentage … descending … tie … contest_id ascending" | `ORDER BY percentage DESC, contest_id` |
| contests 208, 209, 210 all have 100% | The tiebreaker is exercised by the example |

🤔 **Before you open the next section:** inside `GROUP BY contest_id`, `COUNT(*)` counts one contest's registrations. Where does the total number of users come from?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Scalar subquery for the total** | `COUNT(user_id) * 100 / (SELECT COUNT(*) FROM Users)` | ✅ The denominator, computed once |
| Cross join a one-row total | `CROSS JOIN (SELECT COUNT(*) AS total FROM Users) u` | ✅ Same thing as a join; handy when the total is used several times |
| Count distinct users in `Register` | `… / (SELECT COUNT(DISTINCT user_id) FROM Register)` | ❌ Leaves out users who registered for nothing |
| Join `Users` and count | `Register JOIN Users …`, `COUNT(*)` per contest | ❌ Still no total — the join doesn't bring the denominator |

**The decision: a scalar subquery.** A query that returns exactly one value can stand anywhere a number can.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT contest_id,
       ROUND(COUNT(user_id) * 100 / (SELECT COUNT(*) FROM Users), 2) AS percentage
```

**Registrations × 100 ÷ total users, rounded.** `(SELECT COUNT(*) FROM Users)` is a **scalar subquery** — one row, one column — and MySQL computes it once, not once per contest. Multiplying by 100 *before* dividing keeps it a percentage; MySQL's `/` always returns a decimal, so there's no integer-division trap.
→ [scalar-subquery](../sql/scalar-subquery.md) · [ratios-percentages](../sql/ratios-percentages.md) · [count](../sql/count.md)

```sql
FROM Register
```

```sql
GROUP BY contest_id
```

→ [group-by](../sql/group-by.md)

```sql
ORDER BY percentage DESC, contest_id;
```

**Primary and secondary sort.** Rows are sorted by `percentage` descending; rows with the same percentage are then sorted by `contest_id` ascending (the default). The alias works here because `ORDER BY` runs after `SELECT`.
→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT contest_id,
       ROUND(COUNT(user_id) * 100 / (SELECT COUNT(*) FROM Users), 2) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id;
```

</details>

**Trace it** — the two numbers behind each percentage:

| `contest_id` | `registered` | `total_users` |
|---|---|---|
| 207 | 1 | 3 |
| 208 | 3 | 3 |
| 209 | 3 | 3 |
| 210 | 3 | 3 |
| 215 | 2 | 3 |

215: 2 × 100 / 3 = 66.67. 207: 33.33. The three contests at 100.00 are tied, so they appear in `contest_id` order: 208, 209, 210.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(u + r + c log c)</summary>

**O(u)** to count users once, **O(r)** to group r registrations, and **O(c log c)** to sort c contests.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(c)</summary>

**O(c)** — one counter per contest, which is also the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Per contest I count registrations, and divide by the total number of users from a scalar subquery, times 100, rounded to two places. Then sort by percentage descending with `contest_id` as the tiebreaker. The denominator has to come from `Users`, not `Register`, because some users never register."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Could registrations be duplicated?" | Not here — it's the key. If they could, use `COUNT(DISTINCT user_id)`. |
| "Is the subquery run once per group?" | No — it's not correlated, so MySQL evaluates it once. |
| "Contests nobody registered for?" | They'd need a `Contests` table to appear; `Register` only knows contests with registrations. |
| "Return a fraction instead of a percentage?" | Drop the `* 100`. |

**Traps:**

- **Wrong denominator** — counting users in `Register` skips users who never registered.
- **Missing tiebreaker** — tied percentages must be in `contest_id` order.
- **Rounding before multiplying** — `ROUND(x / n, 2) * 100` loses precision: 66.67 becomes 67.00.

**This same move shows up in:** [Immediate Food Delivery II](1174-immediate-food-delivery-ii.md) (a percentage over a filtered set) · [Queries Quality and Percentage](1211-queries-quality-and-percentage.md) (a percentage per group) · [Game Play Analysis IV](550-game-play-analysis-iv.md) (a fraction of all players).

</details>

---
