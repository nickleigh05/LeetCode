# 584. Find Customer Referee

**Easy** · [LeetCode](https://leetcode.com/problems/find-customer-referee/) · [Solution file (no hints)](../../problems/0500-0999/584.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Return the names of customers who were **not** referred by customer 2 — that includes customers referred by someone else **and** customers nobody referred. Any order.

```
Table: Customer
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| referee_id  | int     |
+-------------+---------+
In SQL, id is the primary key column for this table.
Each row of this table indicates the id of a customer, their name, and the id of the customer who referred them.
```

```
Input:
Customer table:
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1  | Will | null       |
| 2  | Jane | null       |
| 3  | Alex | 2          |
| 4  | Bill | null       |
| 5  | Zack | 1          |
| 6  | Mark | 2          |
+----+------+------------+
Output:
+------+
| name |
+------+
| Will |
| Jane |
| Bill |
| Zack |
+------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

It looks like a one-condition filter, and that's the point of the problem: the obvious condition is wrong, and the reason is `NULL`.

| The statement says | Which really means |
|---|---|
| "referred by any customer with id != 2" | Rows where `referee_id` holds a number other than 2 |
| "not referred by any customer" | Rows where `referee_id` is **`NULL`** — there's no number at all |
| "either … or …" | Two kinds of rows qualify → two conditions joined by `OR` |
| `null` in the example table | Will, Jane, and Bill have no referee — and all three are in the output |
| "find the names" | Return just `name`. Names can repeat; ids are unique, but you're not asked for ids |

The statement spells out the second case on purpose. In SQL, "not equal to 2" does **not** include "has no value."

🤔 **Before you open the next section:** what does `NULL != 2` evaluate to — true, false, or something else?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Handle `NULL` explicitly** | `WHERE referee_id IS NULL OR referee_id != 2` | ✅ Says both cases out loud |
| Null-safe equality | `WHERE NOT (referee_id <=> 2)` | ✅ One comparison; `<=>` treats `NULL` as a comparable value. MySQL-only |
| Replace `NULL` first | `WHERE COALESCE(referee_id, 0) <> 2` | ✅ Works, but relies on 0 never being a real id |
| Just `!= 2` | `WHERE referee_id != 2` | ❌ Returns only Zack — drops every `NULL` row |
| `= NULL` | `WHERE referee_id != 2 OR referee_id = NULL` | ❌ `= NULL` is never true. Same wrong answer |

**The decision: `IS NULL OR != 2`.** It's portable, and it makes the `NULL` case impossible to miss when someone reads the query later.

**Why `!= 2` alone fails.** SQL uses three-valued logic: a comparison can be true, false, or **unknown** — and any comparison with `NULL` is unknown. `WHERE` keeps a row only when its condition is *true*, so unknown rows are dropped right alongside the false ones:

| `name` | `referee_id` | `referee_id != 2` | `WHERE referee_id != 2` |
|---|---|---|---|
| Will | `NULL` | `NULL` | dropped |
| Jane | `NULL` | `NULL` | dropped |
| Alex | 2 | 0 | dropped |
| Bill | `NULL` | `NULL` | dropped |
| Zack | 1 | 1 | kept |
| Mark | 2 | 0 | dropped |

`NULL` in the third column is the "unknown." Will, Jane, and Bill vanish, even though nobody referred them.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT name
```

**What to return.** Only the name, matching the expected output's single column.
→ [select-from](../sql/select-from.md)

```sql
FROM Customer
```

**Where to look.** Everything is in one table. `referee_id` points at another row's `id`, but you don't need to follow that pointer — you only compare it to the number 2.

```sql
WHERE referee_id IS NULL OR referee_id != 2;
```

**The whole problem, in one line.** Two ways to qualify:

- `referee_id IS NULL` — nobody referred this customer. `IS NULL` is the only test that's *true* for a missing value; `= NULL` is always unknown.
- `referee_id != 2` — someone referred them, and it wasn't customer 2.

`OR` keeps the row if either side is true. For a `NULL` row, the left side is true, so the unknown on the right doesn't matter.
→ [null-is-null](../sql/null-is-null.md) · [logical-operators](../sql/logical-operators.md) · [where](../sql/where.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL OR referee_id != 2;
```

</details>

**Trace it** — both halves of the condition, row by row (`1` = true, `0` = false, `NULL` = unknown):

| `name` | `referee_id` | `IS NULL` | `!= 2` | `WHERE says` |
|---|---|---|---|---|
| Will | `NULL` | 1 | `NULL` | kept |
| Jane | `NULL` | 1 | `NULL` | kept |
| Alex | 2 | 0 | 0 | dropped |
| Bill | `NULL` | 1 | `NULL` | kept |
| Zack | 1 | 0 | 1 | kept |
| Mark | 2 | 0 | 0 | dropped |

Will, Jane, and Bill pass the left side; Zack passes the right. Alex and Mark fail both.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n customers — one pass, testing the condition once per row.

An index on `referee_id` wouldn't help much: "everything except 2" matches most of the table, and a full scan beats thousands of index lookups.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output. Rows are filtered one at a time as they stream past.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A customer qualifies if nobody referred them or someone other than 2 did. The catch is that `referee_id != 2` is *unknown* when `referee_id` is `NULL`, and `WHERE` throws unknowns away. So I test `IS NULL` explicitly and `OR` it with the inequality. Single scan, O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it with one comparison?" | `WHERE NOT (referee_id <=> 2)`. `<=>` is MySQL's null-safe equals: `NULL <=> 2` is false, not unknown. The standard-SQL spelling is `IS DISTINCT FROM`, which MySQL doesn't support. |
| "Customers referred by 2 **or 3**?" | `WHERE referee_id IN (2, 3)`. `NULL` rows correctly drop out. |
| "Customers **not** referred by 2 or 3?" | `WHERE referee_id IS NULL OR referee_id NOT IN (2, 3)` — `NOT IN` has the same `NULL` blind spot as `!=`. |
| "How many customers have a referee?" | `COUNT(referee_id)` — `COUNT(column)` skips `NULL`s, while `COUNT(*)` counts rows. On the example: 3 vs 6. |
| "Show each customer with their referee's **name**." | Join the table to itself: `LEFT JOIN Customer r ON c.referee_id = r.id`. |

**Traps:**

- **`!= 2` alone** — silently loses every customer with no referee.
- **`= NULL` or `!= NULL`** — always unknown, so it matches nothing. Use `IS NULL` / `IS NOT NULL`.
- **`NOT IN (2)`** — the same trap in a different spelling.
- **`COALESCE(referee_id, 0)`** — fine here, but only because 0 isn't a real id. Pick a sentinel that can't collide, or avoid sentinels.

**This same move shows up in:** [Recyclable and Low Fat Products](1757-recyclable-and-low-fat-products.md) (the plain version of this filter) · [Employee Bonus](577-employee-bonus.md) (`NULL` from a `LEFT JOIN` that must be kept) · [Customer Who Visited but Did Not Make Any Transactions](1581-customer-who-visited-but-did-not-make-any-transactions.md) (`IS NULL` to find missing matches).

</details>

---
