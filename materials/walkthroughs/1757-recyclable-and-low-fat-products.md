# 1757. Recyclable and Low Fat Products

**Easy** · [LeetCode](https://leetcode.com/problems/recyclable-and-low-fat-products/) · [Solution file (no hints)](../../problems/1500-1999/1757.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find the ids of products that are **both** low fat **and** recyclable. Return them in any order.

```
Table: Products
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| low_fats    | enum    |
| recyclable  | enum    |
+-------------+---------+
product_id is the primary key (column with unique values) for this table.
low_fats is an ENUM (category) of type ('Y', 'N') where 'Y' means this product is low fat and 'N' means it is not.
recyclable is an ENUM (category) of types ('Y', 'N') where 'Y' means this product is recyclable and 'N' means it is not.
```

```
Input:
Products table:
+-------------+----------+------------+
| product_id  | low_fats | recyclable |
+-------------+----------+------------+
| 0           | Y        | N          |
| 1           | Y        | Y          |
| 2           | N        | Y          |
| 3           | Y        | Y          |
| 4           | N        | N          |
+-------------+----------+------------+
Output:
+-------------+
| product_id  |
+-------------+
| 1           |
| 3           |
+-------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the "hello world" of SQL: one table, one condition, no joins, no grouping. The value is in learning the three questions every query answers — *which table*, *which rows*, *which columns*.

| The statement says | Which really means |
|---|---|
| one table, `Products` | Everything lives in one place — no `JOIN` |
| "find the ids" | The output is a single column, `product_id`. Not `SELECT *` |
| "both low fat **and** recyclable" | Two conditions that must hold **on the same row** → `AND` |
| `low_fats` is an ENUM of `('Y', 'N')` | Compare against the **string** `'Y'` — not `TRUE`, not `1` |
| `product_id` is the primary key | Ids are already unique — no `DISTINCT` needed |
| "any order" | No `ORDER BY` required |

Every query you'll write in this unit decomposes the same way: **`FROM`** picks the table, **`WHERE`** picks the rows, **`SELECT`** picks the columns. Here each one is a single line.

🤔 **Before you open the next section:** a row should survive only if *both* flags are `'Y'`. Which logical operator says "both"?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`WHERE` with `AND`** | `WHERE low_fats = 'Y' AND recyclable = 'Y'` | ✅ The sentence, translated word for word |
| Row comparison | `WHERE (low_fats, recyclable) = ('Y', 'Y')` | ✅ Same result, more compact, less common |
| `INTERSECT` two filters | `… WHERE low_fats = 'Y' INTERSECT … WHERE recyclable = 'Y'` | ⚠️ Correct (MySQL 8.0.31+), but two passes for a one-pass problem |
| Bare columns as booleans | `WHERE low_fats AND recyclable` | ❌ Returns **every** row — see the trap below |

**The decision: `WHERE … AND …`.** It reads exactly like the requirement, and anyone reviewing it can check it against the statement in one glance.

**Why the "bare booleans" version fails** — and this is MySQL-specific, so it's worth seeing once. An `ENUM` used where a number is expected evaluates to its **position in the list**, starting at 1: `'Y'` is 1 and `'N'` is 2. Both are non-zero, so both count as true:

| `product_id` | `low_fats` | `position in ENUM list` | `WHERE low_fats AND recyclable` |
|---|---|---|---|
| 0 | Y | 1 | kept |
| 1 | Y | 1 | kept |
| 2 | N | 2 | kept |
| 3 | Y | 1 | kept |
| 4 | N | 2 | kept |

Every row survives, including product 4, which is neither. Always compare an `ENUM` against its string value.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT product_id
```

**What to return.** Exactly one column, named exactly like the expected output. Listing the columns you want — instead of `SELECT *` — is the habit that keeps extra columns out of your result.
→ [select-from](../sql/select-from.md) · [tables-rows-columns](../sql/tables-rows-columns.md)

```sql
FROM Products
```

**Where to look.** One table holds every fact the problem mentions.
→ [select-from](../sql/select-from.md)

```sql
WHERE low_fats = 'Y' AND recyclable = 'Y';
```

**Which rows survive.** `WHERE` is tested once per row; a row is kept only when the whole condition is true. `AND` is true only when both sides are — which is precisely "both low fat and recyclable."

The values are quoted because they're strings. MySQL also accepts `"Y"`, but single quotes are standard SQL — in most other databases, double quotes name a *column*, not a string.
→ [where](../sql/where.md) · [logical-operators](../sql/logical-operators.md) · [data-types](../sql/data-types.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT product_id
FROM Products
WHERE low_fats = 'Y' AND recyclable = 'Y';
```

</details>

**Trace it** — the example, row by row:

| `product_id` | `low_fats` | `recyclable` | `WHERE says` |
|---|---|---|---|
| 0 | Y | N | dropped |
| 1 | Y | Y | kept |
| 2 | N | Y | dropped |
| 3 | Y | Y | kept |
| 4 | N | N | dropped |

Products 1 and 3 are the only rows where both flags are `'Y'`.

**One idea worth taking from this problem:** SQL is *written* `SELECT → FROM → WHERE`, but *evaluated* `FROM → WHERE → SELECT`. The engine finds the table, filters the rows, and only then picks the columns. Reading queries in evaluation order makes every later problem in this unit easier. See [execution-order](../sql/execution-order.md).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n is the number of rows in `Products`.

The engine checks the condition once per row — a full table scan. LeetCode's table definitions declare no indexes, so there's nothing faster available, and that's fine: you have to look at every row to know which ones qualify.

In a real database you'd ask whether an index helps. Here, probably not much — each flag has only two values, so an index on it would still point at roughly half the table.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output. Rows stream through the filter one at a time; nothing is sorted, grouped, or buffered. The result itself holds k ids, for k matching products.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Everything's in one table, so it's a single filter. I keep rows where both flags equal `'Y'` and return just the id. I'm comparing to the string because these are ENUMs — in MySQL a bare ENUM in a boolean context is its list position, which is always non-zero. It's one full scan, O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Low fat **or** recyclable?" | Swap `AND` for `OR`. With both in one condition, use parentheses when mixing them: `AND` binds tighter than `OR`. |
| "Low fat but **not** recyclable?" | `WHERE low_fats = 'Y' AND recyclable = 'N'`. |
| "How many are there?" | `SELECT COUNT(*) FROM Products WHERE …` — same filter, different `SELECT`. |
| "Sort them by id." | Add `ORDER BY product_id`. |
| "What if a flag could be `NULL`?" | `NULL = 'Y'` is *unknown*, and `WHERE` drops unknown rows — correct here. The opposite question is where `NULL` bites: see [Find Customer Referee](584-find-customer-referee.md). |
| "Would an index help?" | Barely — two-valued columns aren't selective. A covering index on `(low_fats, recyclable, product_id)` could answer from the index alone, but it's rarely worth it. |

**Traps:**

- **`WHERE low_fats AND recyclable`** — returns every row, because ENUM positions are non-zero. Compare against `'Y'`.
- **`SELECT *`** — extra columns don't match the expected output.
- **Comparing to `1` or `TRUE`** — `low_fats = 1` matches the ENUM's first *position*, which happens to be `'Y'` here. Correct by accident; it breaks the moment the list order changes.
- **Double quotes for strings** — fine in MySQL's default mode, an error or a column reference elsewhere.

**This same move shows up in:** [Find Customer Referee](584-find-customer-referee.md) (a filter where `NULL` changes the answer) · [Big Countries](595-big-countries.md) (a filter with `OR`) · [Invalid Tweets](1683-invalid-tweets.md) (a filter on a computed value).

</details>

---
