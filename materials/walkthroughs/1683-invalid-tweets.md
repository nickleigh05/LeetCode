# 1683. Invalid Tweets

**Easy** · [LeetCode](https://leetcode.com/problems/invalid-tweets/) · [Solution file (no hints)](../../problems/1500-1999/1683.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A tweet is **invalid** if its content is longer than 15 characters. Return the ids of the invalid tweets, in any order.

```
Table: Tweets
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
tweet_id is the primary key (column with unique values) for this table.
content consists of alphanumeric characters, '!', or ' ' and no other special characters.
This table contains all the tweets in a social media app.
```

```
Input:
Tweets table:
+----------+-----------------------------------+
| tweet_id | content                           |
+----------+-----------------------------------+
| 1        | Let us Code                       |
| 2        | More than fifteen chars are here! |
+----------+-----------------------------------+
Output:
+----------+
| tweet_id |
+----------+
| 2        |
+----------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The filter isn't on a stored value this time — it's on something you **compute** from each row: the length of a string.

| The statement says | Which really means |
|---|---|
| "the number of **characters**" | Count characters, not bytes — the distinction matters in MySQL |
| "**strictly greater** than 15" | `> 15`. A 15-character tweet is valid |
| content is alphanumeric, `!`, or space | Spaces count as characters too — `'Let us Code'` is 11, not 9 |
| "find the IDs" | Return `tweet_id` only |

🤔 **Before you open the next section:** MySQL has both `LENGTH()` and `CHAR_LENGTH()`. One counts characters; what does the other count?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`CHAR_LENGTH`** | `WHERE CHAR_LENGTH(content) > 15` | ✅ Counts characters — exactly what's asked |
| `LENGTH` | `WHERE LENGTH(content) > 15` | ⚠️ Counts **bytes**. Passes here only because this content is plain ASCII |
| `LIKE` with 16 `_` | `WHERE content LIKE '________________%'` | ✅ Correct (`_` matches one character), but unreadable |
| `>= 15` | `WHERE CHAR_LENGTH(content) >= 15` | ❌ Flags valid 15-character tweets |

**The decision: `CHAR_LENGTH(content) > 15`.** The name says what it measures.

**Why `LENGTH` is a trap.** MySQL's default character set, `utf8mb4`, stores ASCII in 1 byte per character but other characters in 2–4 bytes. `LENGTH` returns bytes:

| `s` | `CHAR_LENGTH` | `LENGTH` |
|---|---|---|
| cafe | 4 | 4 |
| café | 4 | 5 |
| 😀 | 1 | 4 |

On this problem's ASCII-only data the two agree, which is why `LENGTH` gets accepted. On a real social network, an emoji-heavy tweet would be wrongly flagged.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT tweet_id
```

```sql
FROM Tweets
```

```sql
WHERE CHAR_LENGTH(content) > 15;
```

**Filter on a computed value.** `WHERE` can test any expression, not just a raw column. `CHAR_LENGTH` is evaluated for each row, then compared to 15.
→ [string-functions](../sql/string-functions.md) · [where](../sql/where.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT tweet_id
FROM Tweets
WHERE CHAR_LENGTH(content) > 15;
```

</details>

**Trace it** — the computed length for each tweet:

| `tweet_id` | `content` | `CHAR_LENGTH(content)` | `invalid?` |
|---|---|---|---|
| 1 | Let us Code | 11 | 0 |
| 2 | More than fifteen chars are here! | 33 | 1 |

Tweet 2 has 33 characters, so it's the only invalid one.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · L)</summary>

**O(n · L)** for n tweets of at most L characters — computing each length walks the string.

`content` is `varchar(50)` here, so L ≤ 50 and this is effectively **O(n)**: one scan of the table.

`LENGTH` is cheaper — the byte count is stored with each value — while `CHAR_LENGTH` has to walk variable-width `utf8mb4` text. It's the correct one regardless.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output — each length is computed, compared, and discarded.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Invalid means more than 15 characters, so I filter on `CHAR_LENGTH(content) > 15`. I use `CHAR_LENGTH` rather than `LENGTH` because `LENGTH` counts bytes, and in `utf8mb4` a single character can take up to four. It's one scan."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `LENGTH`?" | Bytes, not characters. `LENGTH('café')` is 5; an emoji is 4. |
| "Return the length too." | `SELECT tweet_id, CHAR_LENGTH(content) AS len …` — you can't use `len` in `WHERE`, though; repeat the expression there. |
| "Truncate long tweets to 15 characters." | `LEFT(content, 15)` in the `SELECT`. |
| "Would an index on `content` help?" | No — the filter wraps the column in a function, so an index on `content` can't be used. MySQL 8 can index the expression itself (a functional index on `CHAR_LENGTH(content)`). |
| "Do trailing spaces count?" | Yes. `VARCHAR` keeps them and `CHAR_LENGTH` counts them. |

**Traps:**

- **`LENGTH` instead of `CHAR_LENGTH`** — right answer on ASCII data, wrong on real text.
- **`>= 15`** — the boundary case "exactly 15" is valid.
- **Using a `SELECT` alias in `WHERE`** — `WHERE len > 15` fails; `WHERE` runs before `SELECT`.

**This same move shows up in:** [Fix Names in a Table](1667-fix-names-in-a-table.md) (more string functions, applied in `SELECT`) · [Patients With a Condition](1527-patients-with-a-condition.md) (pattern matching inside a string) · [Find Users With Valid E-Mails](1517-find-users-with-valid-e-mails.md) (a filter on a string's shape).

</details>

---
