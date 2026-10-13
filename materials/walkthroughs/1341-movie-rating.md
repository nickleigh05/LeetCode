# 1341. Movie Rating

**Medium** · [LeetCode](https://leetcode.com/problems/movie-rating/) · [Solution file (no hints)](../../problems/1000-1499/1341.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Return two rows in one column, `results`:

1. the **user** who rated the most movies (ties → alphabetically first name);
2. the **movie** with the highest average rating in **February 2020** (ties → alphabetically first title).

```
Table: Movies
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| movie_id      | int     |
| title         | varchar |
+---------------+---------+
movie_id is the primary key (column with unique values) for this table.
title is the name of the movie.
Each movie has a unique title.

Table: Users
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
+---------------+---------+
user_id is the primary key (column with unique values) for this table.
The column 'name' has unique values.

Table: MovieRating
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| movie_id      | int     |
| user_id       | int     |
| rating        | int     |
| created_at    | date    |
+---------------+---------+
(movie_id, user_id) is the primary key (column with unique values) for this table.
This table contains the rating of a movie by a user in their review.
created_at is the user's review date. 
```

```
Input:
Movies table:
+-------------+--------------+
| movie_id    |  title       |
+-------------+--------------+
| 1           | Avengers     |
| 2           | Frozen 2     |
| 3           | Joker        |
+-------------+--------------+
Users table:
+-------------+--------------+
| user_id     |  name        |
+-------------+--------------+
| 1           | Daniel       |
| 2           | Monica       |
| 3           | Maria        |
| 4           | James        |
+-------------+--------------+
MovieRating table:
+-------------+--------------+--------------+-------------+
| movie_id    | user_id      | rating       | created_at  |
+-------------+--------------+--------------+-------------+
| 1           | 1            | 3            | 2020-01-12  |
| 1           | 2            | 4            | 2020-02-11  |
| 1           | 3            | 2            | 2020-02-12  |
| 1           | 4            | 1            | 2020-01-01  |
| 2           | 1            | 5            | 2020-02-17  |
| 2           | 2            | 2            | 2020-02-01  |
| 2           | 3            | 2            | 2020-03-01  |
| 3           | 1            | 3            | 2020-02-22  |
| 3           | 2            | 4            | 2020-02-25  |
+-------------+--------------+--------------+-------------+
Output:
+--------------+
| results      |
+--------------+
| Daniel       |
| Frozen 2     |
+--------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Two unrelated questions, each a "top-1 with a tiebreaker", stacked into one column. Solve each on its own, then combine.

| The statement says | Which really means |
|---|---|
| "the user who has rated the greatest number of movies" | Count ratings per user, take the largest |
| "In case of a tie, return the lexicographically smaller user name" | Sort by count descending, then name ascending, take one row |
| "highest average rating in February 2020" | Only ratings with `created_at` in Feb 2020, then `AVG` per movie |
| one output column, two rows | Stack two single-row queries: `UNION ALL` |
| Daniel and Monica both rated 3 | The tie is in the example — Daniel wins alphabetically |

🤔 **Before you open the next section:** what happens if a user's name happens to be identical to the winning movie's title — with `UNION`, and with `UNION ALL`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Two `ORDER BY … LIMIT 1` queries, `UNION ALL`** | each in parentheses, stacked | ✅ Each half is a small top-1 query |
| `RANK()` in each half | rank by the same keys, keep rank 1 | ✅ Works; more machinery for a single winner |
| `UNION` instead of `UNION ALL` | | ❌ If the user's name equals the movie's title, the two rows collapse into one |
| `MAX(COUNT(*))` | nested aggregates | ❌ Not allowed in MySQL, and it loses the name |

**The decision: two top-1 queries with `UNION ALL`.** Each half sorts by its metric and then by name, so the first row is the winner *including* the tiebreak.

**Why `UNION ALL`.** `UNION` removes duplicate rows, and here two different answers can be the same string. With a user and a movie both named "Joker":

| `results` |
|---|
| Joker |

One answer is gone. `UNION ALL` keeps both rows.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
(
    SELECT u.name AS results
    FROM MovieRating r
    JOIN Users u ON u.user_id = r.user_id
    GROUP BY u.user_id, u.name
    ORDER BY COUNT(*) DESC, u.name
    LIMIT 1
)
```

**The most active rater.** Count each user's ratings; sort by count descending, then name ascending for the tie; keep the first. The parentheses are required: they let each half have its own `ORDER BY` and `LIMIT`. The alias `results` names the output column.

| `name` | `ratings` |
|---|---|
| Daniel | 3 |
| Monica | 3 |
| Maria | 2 |
| James | 1 |

→ [order-by](../sql/order-by.md) · [limit-offset](../sql/limit-offset.md) · [group-by](../sql/group-by.md)

```sql
UNION ALL
```

**Stack the two answers, keeping duplicates.**
→ [union](../sql/union.md)

```sql
(
    SELECT m.title
    FROM MovieRating r
    JOIN Movies m ON m.movie_id = r.movie_id
    WHERE r.created_at >= '2020-02-01' AND r.created_at < '2020-03-01'
    GROUP BY m.movie_id, m.title
    ORDER BY AVG(r.rating) DESC, m.title
    LIMIT 1
);
```

**February's best-rated movie.** The half-open range `>= '2020-02-01' AND < '2020-03-01'` covers the whole month — including the 29th in a leap year — without listing a last day. Then average per movie, sort by average descending and title ascending, keep one.

| `title` | `Feb average` |
|---|---|
| Frozen 2 | 3.5000 |
| Joker | 3.5000 |
| Avengers | 3.0000 |

→ [date-arithmetic](../sql/date-arithmetic.md) · [aggregate-functions](../sql/aggregate-functions.md)

<details>
<summary>The whole thing together</summary>

```sql
(
    SELECT u.name AS results
    FROM MovieRating r
    JOIN Users u ON u.user_id = r.user_id
    GROUP BY u.user_id, u.name
    ORDER BY COUNT(*) DESC, u.name
    LIMIT 1
)
UNION ALL
(
    SELECT m.title
    FROM MovieRating r
    JOIN Movies m ON m.movie_id = r.movie_id
    WHERE r.created_at >= '2020-02-01' AND r.created_at < '2020-03-01'
    GROUP BY m.movie_id, m.title
    ORDER BY AVG(r.rating) DESC, m.title
    LIMIT 1
);
```

</details>

**Trace it** — Daniel and Monica tie at 3 ratings; Daniel is first alphabetically. Frozen 2 and Joker tie at 3.5 in February; Frozen 2 is first. Result: `Daniel`, `Frozen 2`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(r + u log u + m log m)</summary>

**O(r)** to group r ratings in each half, plus sorting u users and m movies. Each half needs only its top row, so MySQL can avoid a full sort — but O(n log n) is the honest bound to quote.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u + m)</summary>

**O(u + m)** for the per-user and per-movie groups.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two independent top-1 queries. For users, count ratings per user and order by count descending, then name. For movies, filter to February 2020 with a half-open date range, average per movie, order by average descending, then title. Each takes `LIMIT 1`, and I combine them with `UNION ALL` — not `UNION`, since a user and a movie could share a name."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why the parentheses?" | Without them, an `ORDER BY … LIMIT` in the first half is a syntax error, and one at the end applies to the whole `UNION` — returning a single row overall. Parentheses scope each to its own half. |
| "Return all tied winners?" | Use `RANK() OVER (ORDER BY COUNT(*) DESC)` and keep rank 1 — without the name tiebreaker. |
| "Why `< '2020-03-01'` rather than `<= '2020-02-29'`?" | It's correct for any month length, and for `DATETIME` columns it includes the whole last day. |
| "Guarantee the user row comes first?" | Add a constant sort column to each half (1, 2) and order by it in an outer query. |

**Traps:**

- **`UNION`** — merges a user and a movie with the same name.
- **Forgetting the tiebreaker** — "lexicographically smaller" is checked.
- **Averaging all ratings** — the movie question is February 2020 only.

**This same move shows up in:** [Friend Requests II: Who Has the Most Friends](602-friend-requests-ii-who-has-the-most-friends.md) (top-1 by a count) · [Count Salary Categories](1907-count-salary-categories.md) (stacking rows with `UNION ALL`) · [Monthly Transactions I](1193-monthly-transactions-i.md) (month-based filtering).

</details>

---
