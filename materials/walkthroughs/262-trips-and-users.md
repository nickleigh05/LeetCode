# 262. Trips and Users

**Hard** · [LeetCode](https://leetcode.com/problems/trips-and-users/) · [Solution file (no hints)](../../problems/0001-0499/262.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each day from **2013-10-01 to 2013-10-03** with at least one trip, compute the **cancellation rate** among trips where **both** the client and the driver are unbanned. Round to 2 decimals. Any order.

```
Table: Trips
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| id          | int      |
| client_id   | int      |
| driver_id   | int      |
| city_id     | int      |
| status      | enum     |
| request_at  | varchar  |     
+-------------+----------+
id is the primary key (column with unique values) for this table.
The table holds all taxi trips. Each trip has a unique id, while client_id and driver_id are foreign keys to the users_id at the Users table.
Status is an ENUM (category) type of ('completed', 'cancelled_by_driver', 'cancelled_by_client').

Table: Users
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| users_id    | int      |
| banned      | enum     |
| role        | enum     |
+-------------+----------+
users_id is the primary key (column with unique values) for this table.
The table holds all users. Each user has a unique users_id, and role is an ENUM type of ('client', 'driver', 'partner').
banned is an ENUM (category) type of ('Yes', 'No').
```

```
Input:
Trips table:
+----+-----------+-----------+---------+---------------------+------------+
| id | client_id | driver_id | city_id | status              | request_at |
+----+-----------+-----------+---------+---------------------+------------+
| 1  | 1         | 10        | 1       | completed           | 2013-10-01 |
| 2  | 2         | 11        | 1       | cancelled_by_driver | 2013-10-01 |
| 3  | 3         | 12        | 6       | completed           | 2013-10-01 |
| 4  | 4         | 13        | 6       | cancelled_by_client | 2013-10-01 |
| 5  | 1         | 10        | 1       | completed           | 2013-10-02 |
| 6  | 2         | 11        | 6       | completed           | 2013-10-02 |
| 7  | 3         | 12        | 6       | completed           | 2013-10-02 |
| 8  | 2         | 12        | 12      | completed           | 2013-10-03 |
| 9  | 3         | 10        | 12      | completed           | 2013-10-03 |
| 10 | 4         | 13        | 12      | cancelled_by_driver | 2013-10-03 |
+----+-----------+-----------+---------+---------------------+------------+
Users table:
+----------+--------+--------+
| users_id | banned | role   |
+----------+--------+--------+
| 1        | No     | client |
| 2        | Yes    | client |
| 3        | No     | client |
| 4        | No     | client |
| 10       | No     | driver |
| 11       | No     | driver |
| 12       | No     | driver |
| 13       | No     | driver |
+----------+--------+--------+
Output:
+------------+-------------------+
| Day        | Cancellation Rate |
+------------+-------------------+
| 2013-10-01 | 0.33              |
| 2013-10-02 | 0.00              |
| 2013-10-03 | 0.50              |
+------------+-------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The "Hard" label comes from stacking several ideas you already know: joining one table **twice** for two roles, filtering on both joins, then a percentage per group.

| The statement says | Which really means |
|---|---|
| `client_id` and `driver_id` both point at `Users` | Join `Users` twice — once as client, once as driver |
| "both client and driver must not be banned" | Each join requires `banned = 'No'` |
| "canceled (by client or driver)" | Any status other than `completed` |
| "cancellation rate … on that day" | Share of that day's eligible trips that were cancelled → average of a flag |
| "between 2013-10-01 and 2013-10-03" | Inclusive date range; `request_at` is a `varchar` in `YYYY-MM-DD`, so string comparison sorts correctly |
| output columns `Day`, `Cancellation Rate` | The second has a space — quote it with backticks |

🤔 **Before you open the next section:** trip 2 was cancelled — why doesn't it count on 2013-10-01?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Join `Users` twice, average a flag** | `JOIN Users c … AND c.banned = 'No' JOIN Users d … AND d.banned = 'No'`, `AVG(status != 'completed')` | ✅ Each role checked by its own join |
| `NOT IN` banned users | `client_id NOT IN (SELECT users_id … banned = 'Yes') AND driver_id NOT IN (…)` | ✅ Fine here — `users_id` is never `NULL` |
| One join on `client_id OR driver_id` | | ❌ A trip with one banned and one unbanned user still matches the unbanned one |
| Check only the client | | ❌ Banned drivers' trips would count |

**The decision: two joins to `Users`, one per role.** Each alias (`c`, `d`) is a separate copy of the table, so each role has its own `banned` check.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT t.request_at AS Day,
       ROUND(AVG(t.status != 'completed'), 2) AS `Cancellation Rate`
```

**The day, and the share of cancelled trips.** `t.status != 'completed'` is 1 for a cancellation, 0 otherwise; `AVG` of it is the cancellation rate. The alias needs backticks because it contains a space.
→ [conditional-aggregation](../sql/conditional-aggregation.md) · [ratios-percentages](../sql/ratios-percentages.md) · [aliases](../sql/aliases.md)

```sql
FROM Trips t
```

```sql
JOIN Users c ON c.users_id = t.client_id AND c.banned = 'No'
```

**The client must exist and be unbanned.** Putting `banned = 'No'` in the inner join's `ON` drops trips by banned clients.

```sql
JOIN Users d ON d.users_id = t.driver_id AND d.banned = 'No'
```

**Same check for the driver, on a second copy of `Users`.**
→ [inner-join](../sql/inner-join.md) · [self-join](../sql/self-join.md)

```sql
WHERE t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
```

**Only the three days.**
→ [between](../sql/between.md)

```sql
GROUP BY t.request_at;
```

→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT t.request_at AS Day,
       ROUND(AVG(t.status != 'completed'), 2) AS `Cancellation Rate`
FROM Trips t
JOIN Users c ON c.users_id = t.client_id AND c.banned = 'No'
JOIN Users d ON d.users_id = t.driver_id AND d.banned = 'No'
WHERE t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY t.request_at;
```

</details>

**Trace it** — the trips that survive both joins and the date filter:

| `id` | `request_at` | `client_id` | `driver_id` | `status` | `cancelled?` |
|---|---|---|---|---|---|
| 1 | 2013-10-01 | 1 | 10 | completed | 0 |
| 3 | 2013-10-01 | 3 | 12 | completed | 0 |
| 4 | 2013-10-01 | 4 | 13 | cancelled_by_client | 1 |
| 5 | 2013-10-02 | 1 | 10 | completed | 0 |
| 7 | 2013-10-02 | 3 | 12 | completed | 0 |
| 9 | 2013-10-03 | 3 | 10 | completed | 0 |
| 10 | 2013-10-03 | 4 | 13 | cancelled_by_driver | 1 |

Trips 2, 6, and 8 are gone (client 2 is banned). 10-01: 1 of 3 cancelled → 0.33. 10-02: 0 of 2 → 0.00. 10-03: 1 of 2 → 0.50.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(t + u)</summary>

**O(t + u)** — two hash joins on user ids (one build over `Users`, probed by each trip), the date filter, and one grouping pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u)</summary>

**O(u)** for the hash tables over `Users`, plus one accumulator per day.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A trip counts only if both its client and its driver are unbanned, so I join `Users` twice — once per role — each requiring `banned = 'No'`. I filter to the three days, group by day, and the cancellation rate is the average of `status != 'completed'`, rounded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Days with no eligible trips?" | They don't appear; the statement only wants days with at least one trip. To force them, start from a calendar of dates and `LEFT JOIN`. |
| "Cancellations split by who cancelled?" | `AVG(status = 'cancelled_by_driver')` and `AVG(status = 'cancelled_by_client')` as separate columns. |
| "Why `!= 'completed'` rather than listing both cancellations?" | Equivalent with these three statuses; `status LIKE 'cancelled%'` or `IN (…)` are more explicit if new statuses could appear. |
| "`request_at` is a varchar — is `BETWEEN` safe?" | Yes for zero-padded `YYYY-MM-DD` strings; they sort the same as dates. |

**Traps:**

- **One join for both roles** — misses banned drivers or banned clients.
- **Filtering cancellations in `WHERE`** — then you can't compute a rate; the flag goes inside the aggregate.
- **Unquoted `Cancellation Rate`** — the space breaks the alias.

**This same move shows up in:** [Confirmation Rate](1934-confirmation-rate.md) (rate as the average of a flag) · [Market Analysis I](1158-market-analysis-i.md) (one table referenced in two roles) · [Queries Quality and Percentage](1211-queries-quality-and-percentage.md) (percentages per group).

</details>

---
