# 1141. User Activity for the Past 30 Days I

**Easy** · [LeetCode](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/) · [Solution file (no hints)](../../problems/1000-1499/1141.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each day in the 30 days ending **2019-07-27** (inclusive), count the users who did at least one activity. Skip days with no activity. Any order.

```
Table: Activity
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| session_id    | int     |
| activity_date | date    |
| activity_type | enum    |
+---------------+---------+
This table may have duplicate rows.
The activity_type column is an ENUM (category) of type ('open_session', 'end_session', 'scroll_down', 'send_message').
The table shows the user activities for a social media website. 
Note that each session belongs to exactly one user.
```

```
Input:
Activity table:
+---------+------------+---------------+---------------+
| user_id | session_id | activity_date | activity_type |
+---------+------------+---------------+---------------+
| 1       | 1          | 2019-07-20    | open_session  |
| 1       | 1          | 2019-07-20    | scroll_down   |
| 1       | 1          | 2019-07-20    | end_session   |
| 2       | 4          | 2019-07-20    | open_session  |
| 2       | 4          | 2019-07-21    | send_message  |
| 2       | 4          | 2019-07-21    | end_session   |
| 3       | 2          | 2019-07-21    | open_session  |
| 3       | 2          | 2019-07-21    | send_message  |
| 3       | 2          | 2019-07-21    | end_session   |
| 4       | 3          | 2019-06-25    | open_session  |
| 4       | 3          | 2019-06-25    | end_session   |
+---------+------------+---------------+---------------+
Output:
+------------+--------------+
| day        | active_users |
+------------+--------------+
| 2019-07-20 | 2            |
| 2019-07-21 | 2            |
+------------+--------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "30 days ending 2019-07-27 inclusively" | 2019-06-28 through 2019-07-27 — count them: 3 days in June, 27 in July |
| "active … if they made at least one activity" | A user counts once per day, however many rows they have → `COUNT(DISTINCT user_id)` |
| "may have duplicate rows" | Another reason to count distinct users, not rows |
| "we do not care about days with zero active users" | Only days that appear in the data — plain `GROUP BY`, no calendar table |
| output columns `day`, `active_users` | Alias both |

User 4's activity on 2019-06-25 is outside the window — 32 days before the end date.

🤔 **Before you open the next section:** what's the first day of a 30-day window that ends on 2019-07-27 and includes it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`BETWEEN` two dates** | `WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'` | ✅ Both ends explicit and inclusive |
| Interval arithmetic | `activity_date > DATE '2019-07-27' - INTERVAL 30 DAY AND activity_date <= '2019-07-27'` | ✅ Same window, no hand-computed start date |
| `DATEDIFF(…) < 30` alone | `WHERE DATEDIFF('2019-07-27', activity_date) < 30` | ❌ Lets **future** dates in — their difference is negative |
| `COUNT(user_id)` | rows instead of users | ❌ User 1 has three rows on 07-20 |

**The decision: `BETWEEN` with both dates written out.** The window is fixed, so state it.

**Why `DATEDIFF < 30` is a trap.** It only bounds the window from one side. An activity *after* the end date has a negative difference, which is also less than 30:

| `activity_date` | `DATEDIFF('2019-07-27', d)` | `< 30?` | `BETWEEN?` |
|---|---|---|---|
| 2019-07-20 | 7 | 1 | 1 |
| 2019-08-15 | -19 | 1 | 0 |

Adding `AND activity_date <= '2019-07-27'` fixes it — at which point `BETWEEN` is simpler.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
```

**One row per day: the date, and how many different users were active.** `COUNT(DISTINCT user_id)` counts each user once per day.
→ [count](../sql/count.md) · [aliases](../sql/aliases.md)

```sql
FROM Activity
```

```sql
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
```

**The 30-day window.** `BETWEEN a AND b` means `>= a AND <= b` — inclusive at both ends. Date strings in `'YYYY-MM-DD'` form compare correctly against a `DATE` column.
→ [between](../sql/between.md) · [date-arithmetic](../sql/date-arithmetic.md)

```sql
GROUP BY activity_date;
```

**Group by the real column.** `GROUP BY day` would also work in MySQL, but grouping by `activity_date` is portable.
→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date;
```

</details>

**Trace it** — activity rows per (day, user):

| `activity_date` | `user_id` | `activity rows` |
|---|---|---|
| 2019-06-25 | 4 | 2 |
| 2019-07-20 | 1 | 3 |
| 2019-07-20 | 2 | 1 |
| 2019-07-21 | 2 | 2 |
| 2019-07-21 | 3 | 3 |

2019-06-25 is outside the window. 2019-07-20 has users 1 and 2 → 2; 2019-07-21 has users 2 and 3 → 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** expected — one scan with the date filter, then per-day sets of user ids. An index on `activity_date` would turn the filter into a range scan.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d · u)</summary>

**O(d · u)** worst case — up to u distinct users tracked for each of d ≤ 30 days.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Filter to the inclusive window 2019-06-28 to 2019-07-27, group by day, and count distinct users, since one user can have many rows on one day. I avoid `DATEDIFF < 30` alone because it would let future dates through."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Include days with zero active users?" | Generate the 30 dates (a recursive CTE or a calendar table) and `LEFT JOIN` the activity onto them. |
| "Average sessions per user in the window?" | `COUNT(DISTINCT session_id) / COUNT(DISTINCT user_id)` over the filtered rows. |
| "Make the window relative to today?" | `activity_date > CURDATE() - INTERVAL 30 DAY AND activity_date <= CURDATE()`. |
| "Distinct active users over the whole window?" | Drop the `GROUP BY`: one `COUNT(DISTINCT user_id)`. |

**Traps:**

- **Off-by-one start date** — `'2019-06-27'` makes it 31 days.
- **One-sided `DATEDIFF`** — includes future activity.
- **`COUNT(*)`** — counts rows, not users.

**This same move shows up in:** [Number of Unique Subjects Taught by Each Teacher](2356-number-of-unique-subjects-taught-by-each-teacher.md) (`COUNT(DISTINCT …)` per group) · [Rising Temperature](197-rising-temperature.md) (date arithmetic) · [List the Products Ordered in a Period](1327-list-the-products-ordered-in-a-period.md) (filtering to a date range).

</details>

---
