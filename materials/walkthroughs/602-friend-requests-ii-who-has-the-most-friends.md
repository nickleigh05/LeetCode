# 602. Friend Requests II: Who Has the Most Friends

**Medium** · [LeetCode](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/) · [Solution file (no hints)](../../problems/0500-0999/602.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Each row is an accepted friend request — so both people gain a friend. Find the person with the most friends and how many they have. (Exactly one person has the most.)

```
Table: RequestAccepted
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| requester_id   | int     |
| accepter_id    | int     |
| accept_date    | date    |
+----------------+---------+
(requester_id, accepter_id) is the primary key (combination of columns with unique values) for this table.
This table contains the ID of the user who sent the request, the ID of the user who received the request, and the date when the request was accepted.
```

```
Input:
RequestAccepted table:
+--------------+-------------+-------------+
| requester_id | accepter_id | accept_date |
+--------------+-------------+-------------+
| 1            | 2           | 2016/06/03  |
| 1            | 3           | 2016/06/08  |
| 2            | 3           | 2016/06/08  |
| 3            | 4           | 2016/06/09  |
+--------------+-------------+-------------+
Output:
+----+-----+
| id | num |
+----+-----+
| 3  | 3   |
+----+-----+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A friendship is **symmetric**, but each one is stored once, with one person in `requester_id` and the other in `accepter_id`. To count everyone's friends, every friendship must count for **both** columns.

| The statement says | Which really means |
|---|---|
| a row = an accepted request between two people | One friendship → one friend for each person |
| a person can be requester in one row, accepter in another | Their friends are spread across both columns |
| "people who have the most friends and the most friends number" | Count per person, return the top one with the count |
| "only one person has the most friends" | `ORDER BY … LIMIT 1` is enough (the follow-up asks about ties) |
| output columns `id`, `num` | Alias both |

Person 3 sent one request and accepted two: 3 friends in total.

🤔 **Before you open the next section:** how do you turn two id columns into one column that you can group by?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Stack both columns with `UNION ALL`, then count** | `SELECT requester_id AS id … UNION ALL SELECT accepter_id …`, group by `id` | ✅ Every friendship counted from both sides |
| Group each column separately, then add | two grouped subqueries, joined or unioned and summed | ✅ Works; more steps |
| Stack with `UNION` | | ❌ Removes duplicate ids — every count becomes 1 |
| Count only `accepter_id` | | ❌ Ignores the requests a person sent |

**The decision: `UNION ALL` the two columns into one list of ids, then count.** Each id appears once per friendship it's part of.

Here's what `UNION` does instead — it deduplicates the stacked ids, so every person appears once:

| `id` | `num` |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT id, COUNT(*) AS num
```

```sql
FROM (
    SELECT requester_id AS id FROM RequestAccepted
    UNION ALL
    SELECT accepter_id FROM RequestAccepted
) ids
```

**Every friendship, seen from both sides.** The first half lists each requester, the second each accepter; `UNION ALL` keeps every row, duplicates included. The derived table needs an alias (`ids`).

| `id` | `came from` |
|---|---|
| 1 | requester |
| 1 | requester |
| 2 | requester |
| 2 | accepter |
| 3 | requester |
| 3 | accepter |
| 3 | accepter |
| 4 | accepter |

→ [union](../sql/union.md) · [derived-tables](../sql/derived-tables.md)

```sql
GROUP BY id
```

**Count each person's appearances.**

| `id` | `num` |
|---|---|
| 3 | 3 |
| 1 | 2 |
| 2 | 2 |
| 4 | 1 |

→ [group-by](../sql/group-by.md) · [count](../sql/count.md)

```sql
ORDER BY num DESC
```

```sql
LIMIT 1;
```

**The top one.** The statement guarantees a unique winner, so one row is the whole answer.
→ [order-by](../sql/order-by.md) · [limit-offset](../sql/limit-offset.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT id, COUNT(*) AS num
FROM (
    SELECT requester_id AS id FROM RequestAccepted
    UNION ALL
    SELECT accepter_id FROM RequestAccepted
) ids
GROUP BY id
ORDER BY num DESC
LIMIT 1;
```

</details>

**Trace it** — person 3 appears three times in the stacked list (one request sent, two accepted), more than anyone else.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + p log p)</summary>

**O(n)** to stack and group 2n ids, plus sorting p people — or O(p) if MySQL only tracks the top row.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the stacked list and the per-person counters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Friendship is symmetric, but each one is stored once across two columns. I stack both columns into one list of ids with `UNION ALL` — not `UNION`, which would deduplicate — then count per id and take the top row."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if several people tie for most?" | Keep every id whose count equals the max: `HAVING COUNT(*) = (SELECT MAX(c) FROM (…counts…) t)`, or `RANK() OVER (ORDER BY COUNT(*) DESC)` and keep rank 1. |
| "What if the same pair could appear twice, or in both directions?" | Normalise each pair (`LEAST(a, b), GREATEST(a, b)`) and deduplicate before stacking. |
| "List each person's friends?" | The stacked rows with the *other* person attached, then `GROUP_CONCAT`. |
| "Mutual friends of two people?" | Join each person's friend list to the other's. |

**Traps:**

- **`UNION`** — every count collapses to 1.
- **One column only** — misses half the friendships.
- **`LIMIT 1` with ties** — fine here only because the statement rules ties out.

**This same move shows up in:** [Find Followers Count](1729-find-followers-count.md) (counting relationships per user) · [Movie Rating](1341-movie-rating.md) (top-1 by a count, and `UNION ALL` vs `UNION`) · [Count Salary Categories](1907-count-salary-categories.md) (`UNION ALL` to build rows).

</details>

---
