# 1581. Customer Who Visited but Did Not Make Any Transactions

**Easy** · [LeetCode](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/) · [Solution file (no hints)](../../problems/1500-1999/1581.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Find customers who visited **without** making a transaction, and how many such visits each one had. Any order.

```
Table: Visits
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| visit_id    | int     |
| customer_id | int     |
+-------------+---------+
visit_id is the column with unique values for this table.
This table contains information about the customers who visited the mall.

Table: Transactions
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| transaction_id | int     |
| visit_id       | int     |
| amount         | int     |
+----------------+---------+
transaction_id is column with unique values for this table.
This table contains information about the transactions made during the visit_id.
```

```
Input:
Visits
+----------+-------------+
| visit_id | customer_id |
+----------+-------------+
| 1        | 23          |
| 2        | 9           |
| 4        | 30          |
| 5        | 54          |
| 6        | 96          |
| 7        | 54          |
| 8        | 54          |
+----------+-------------+
Transactions
+----------------+----------+--------+
| transaction_id | visit_id | amount |
+----------------+----------+--------+
| 2              | 5        | 310    |
| 3              | 5        | 300    |
| 9              | 5        | 200    |
| 12             | 1        | 910    |
| 13             | 2        | 970    |
+----------------+----------+--------+
Output:
+-------------+----------------+
| customer_id | count_no_trans |
+-------------+----------------+
| 54          | 2              |
| 30          | 1              |
| 96          | 1              |
+-------------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

You're looking for something that **isn't there**: a visit with no matching transaction. That's the anti-join pattern, followed by a count.

| The statement says | Which really means |
|---|---|
| "visited **without** making any transactions" | A visit whose `visit_id` appears nowhere in `Transactions` |
| "the number of times they made these types of visits" | Count those empty visits **per customer** → `GROUP BY customer_id` |
| visit 5 has three transactions | Joining visits to transactions can **multiply** rows — one per transaction |
| customer 54 has visits 5, 7, 8 | Visit 5 had purchases; 7 and 8 didn't → 54 counts 2 |
| output column `count_no_trans` | Name the count exactly that |

🤔 **Before you open the next section:** after a `LEFT JOIN` from `Visits` to `Transactions`, what does `t.transaction_id` look like for a visit with no transactions?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`LEFT JOIN … WHERE t.… IS NULL`** | join, keep the rows with no match, then group | ✅ The classic anti-join; easy to extend |
| `NOT IN` subquery | `WHERE visit_id NOT IN (SELECT visit_id FROM Transactions)` | ✅ Reads naturally — but breaks if that subquery can return `NULL` |
| `NOT EXISTS` | `WHERE NOT EXISTS (SELECT 1 FROM Transactions t WHERE t.visit_id = v.visit_id)` | ✅ The safest anti-join; `NULL`-proof |
| Inner join, then count | `FROM Visits v JOIN Transactions t …` | ❌ Inner joins can only see visits that **do** have transactions |

**The decision: `LEFT JOIN … IS NULL`.** It's the pattern you'll reuse most, and it makes the "no match" rows visible. `NOT EXISTS` is equally good, and the one to choose when `NULL`s are possible.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
```

**The customer, and how many qualifying visits they had.** `COUNT(*)` counts rows in each group — and by the time we count, every row left is one empty visit.
→ [count](../sql/count.md) · [aliases](../sql/aliases.md)

```sql
FROM Visits v
```

```sql
LEFT JOIN Transactions t
    ON v.visit_id = t.visit_id
```

**Attach each visit's transactions — if any.** A visit with three transactions becomes three rows. A visit with none becomes one row with every `t.` column `NULL`.
→ [left-join](../sql/left-join.md)

```sql
WHERE t.transaction_id IS NULL
```

**Keep only the visits that found no transaction.** `transaction_id` is never `NULL` in a real transaction row, so `NULL` here can only mean "no match."
→ [anti-join](../sql/anti-join.md) · [null-is-null](../sql/null-is-null.md)

```sql
GROUP BY v.customer_id;
```

**One row per customer.** Each group holds that customer's empty visits; `COUNT(*)` counts them.
→ [group-by](../sql/group-by.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t
    ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

</details>

**Trace it** — the left join, before any filtering:

| `visit_id` | `customer_id` | `transaction_id` | `amount` |
|---|---|---|---|
| 1 | 23 | 12 | 910 |
| 2 | 9 | 13 | 970 |
| 4 | 30 | `NULL` | `NULL` |
| 5 | 54 | 2 | 310 |
| 5 | 54 | 3 | 300 |
| 5 | 54 | 9 | 200 |
| 6 | 96 | `NULL` | `NULL` |
| 7 | 54 | `NULL` | `NULL` |
| 8 | 54 | `NULL` | `NULL` |

Visit 5 fanned out into three rows. Visits 4, 6, 7, and 8 found nothing. After `WHERE t.transaction_id IS NULL`:

| `visit_id` | `customer_id` | `transaction_id` |
|---|---|---|
| 4 | 30 | `NULL` |
| 6 | 96 | `NULL` |
| 7 | 54 | `NULL` |
| 8 | 54 | `NULL` |

Grouped by customer: 30 → 1, 96 → 1, 54 → 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(v + t)</summary>

**O(v + t)** for v visits and t transactions: a hash join builds on one side and probes with the other, then the grouping is one pass with a hash table keyed by customer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(t + c)</summary>

**O(t)** for the join's hash table and **O(c)** for one counter per customer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I need visits with no transaction. A left join from `Visits` keeps every visit, and the ones with no match have `NULL` transaction columns, so I filter on `transaction_id IS NULL`. Then I group by customer and count. `NOT EXISTS` would work too, and is safer when `NULL`s are possible."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not `COUNT(t.transaction_id)`?" | After the filter, that column is always `NULL`, and `COUNT(column)` skips `NULL`s — it returns 0 for everyone. See the trap below. |
| "Why is `NOT IN` risky?" | If the subquery returns even one `NULL`, `x NOT IN (…)` is never true, and the query returns nothing. `NOT EXISTS` doesn't have this problem. |
| "Count visits **with** transactions instead?" | Inner join, then `COUNT(DISTINCT v.visit_id)` — `DISTINCT` because the join repeats a visit once per transaction. |
| "Total amount spent per customer?" | `LEFT JOIN`, `GROUP BY customer_id`, `SUM(t.amount)` — `NULL` for customers who never bought; wrap it in `IFNULL(…, 0)`. |

**Traps:**

- **`COUNT(t.transaction_id)`** — counts only non-`NULL` values, and after this filter there aren't any:

| `customer_id` | `COUNT(t.transaction_id)` | `COUNT(*)` |
|---|---|---|
| 30 | 0 | 1 |
| 96 | 0 | 1 |
| 54 | 0 | 2 |

- **Putting `t.transaction_id IS NULL` in the `ON` clause** — it changes which rows match, not which rows survive. The filter belongs in `WHERE`.
- **An inner join** — can never see a visit with no transactions.

**This same move shows up in:** [Employees Whose Manager Left the Company](1978-employees-whose-manager-left-the-company.md) (anti-join on a self-reference) · [Replace Employee ID With The Unique Identifier](1378-replace-employee-id-with-the-unique-identifier.md) (the left join on its own) · [Students and Examinations](1280-students-and-examinations.md) (counting matches that might be zero).

</details>

---
