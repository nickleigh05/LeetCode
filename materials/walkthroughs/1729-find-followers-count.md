# 1729. Find Followers Count

**Easy** · [LeetCode](https://leetcode.com/problems/find-followers-count/) · [Solution file (no hints)](../../problems/1500-1999/1729.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

For each user, return the number of followers, ordered by `user_id`.

```
Table: Followers
+-------------+------+
| Column Name | Type |
+-------------+------+
| user_id     | int  |
| follower_id | int  |
+-------------+------+
(user_id, follower_id) is the primary key (combination of columns with unique values) for this table.
This table contains the IDs of a user and a follower in a social media app where the follower follows the user.
```

```
Input:
Followers table:
+---------+-------------+
| user_id | follower_id |
+---------+-------------+
| 0       | 1           |
| 1       | 0           |
| 2       | 0           |
| 2       | 1           |
+---------+-------------+
Output:
+---------+----------------+
| user_id | followers_count|
+---------+----------------+
| 0       | 1              |
| 1       | 1              |
| 2       | 2              |
+---------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| each row: `follower_id` follows `user_id` | One row = one follower of that user |
| "for each user, return the number of followers" | `GROUP BY user_id`, count the rows |
| `(user_id, follower_id)` is the key | No duplicate follows — counting rows counts followers |
| "ordered by `user_id` in ascending order" | `ORDER BY user_id` |
| output column `followers_count` | Alias the count |

Users who follow people but have no followers themselves never appear as `user_id`, so they aren't in the output — which matches the expected result.

🤔 **Before you open the next section:** which column do you group by — the one being followed, or the one doing the following?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`GROUP BY` + `COUNT`** | `COUNT(follower_id) … GROUP BY user_id ORDER BY user_id` | ✅ The textbook aggregation |
| Window count + `DISTINCT` | `SELECT DISTINCT user_id, COUNT(*) OVER (PARTITION BY user_id) …` | ✅ Works; a window is overkill here |
| `GROUP BY follower_id` | groups by the follower | ❌ Counts how many people each user *follows* |

**The decision: `GROUP BY user_id` with `COUNT`.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT user_id, COUNT(follower_id) AS followers_count
```

**The user and their follower count.** Each row in a user's group is one follower.
→ [count](../sql/count.md) · [aliases](../sql/aliases.md)

```sql
FROM Followers
```

```sql
GROUP BY user_id
```

→ [group-by](../sql/group-by.md)

```sql
ORDER BY user_id;
```

**The output order is checked.** Without `ORDER BY`, MySQL returns groups in whatever order is convenient.
→ [order-by](../sql/order-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT user_id, COUNT(follower_id) AS followers_count
FROM Followers
GROUP BY user_id
ORDER BY user_id;
```

</details>

**Trace it** — user 0's rows: one (follower 1) → 1. User 1: one (follower 0) → 1. User 2: two (followers 0 and 1) → 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + u log u)</summary>

**O(n)** to count n rows into groups, plus **O(u log u)** to sort u users — often free if MySQL groups by sorting.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u)</summary>

**O(u)** — one counter per user.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each row is one follower of `user_id`, so I group by `user_id`, count, and sort by `user_id`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Include users with zero followers?" | You'd need the full user list — `Users LEFT JOIN Followers`, with `COUNT(f.follower_id)`. |
| "How many people does each user follow?" | Group by `follower_id` instead. |
| "Mutual follows?" | Self-join: `a.user_id = b.follower_id AND a.follower_id = b.user_id`. |
| "The most-followed user?" | `ORDER BY followers_count DESC LIMIT 1` — mind ties. |

**Traps:**

- **Grouping by the wrong column.**
- **Missing `ORDER BY`** — this problem checks the order.

**This same move shows up in:** [Classes With at Least 5 Students](596-classes-with-at-least-5-students.md) (count per group, then filter) · [Number of Unique Subjects Taught by Each Teacher](2356-number-of-unique-subjects-taught-by-each-teacher.md) (count distinct per group) · [Friend Requests II: Who Has the Most Friends](602-friend-requests-ii-who-has-the-most-friends.md) (counting both sides of a relationship).

</details>

---
