# 1907. Count Salary Categories

**Medium** · [LeetCode](https://leetcode.com/problems/count-salary-categories/) · [Solution file (no hints)](../../problems/1500-1999/1907.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Count accounts in three salary categories — **Low** (< 20000), **Average** (20000–50000 inclusive), **High** (> 50000). All three categories must appear, with 0 if empty. Any order.

```
Table: Accounts
+-------------+------+
| Column Name | Type |
+-------------+------+
| account_id  | int  |
| income      | int  |
+-------------+------+
account_id is the primary key (column with unique values) for this table.
Each row contains information about the monthly income for one bank account.
```

```
Input:
Accounts table:
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 |
| 2          | 12747  |
| 8          | 87709  |
| 6          | 91796  |
+------------+--------+
Output:
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Low Salary     | 1              |
| Average Salary | 0              |
| High Salary    | 3              |
+----------------+----------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The category names aren't stored anywhere, and one of them has **no** accounts in the example — yet it must appear with a 0. Grouping can only produce groups that have rows, so the three output rows have to be built explicitly.

| The statement says | Which really means |
|---|---|
| "Low Salary": strictly less than 20000 | `income < 20000` |
| "Average Salary": inclusive [20000, 50000] | `income BETWEEN 20000 AND 50000` |
| "High Salary": strictly greater than 50000 | `income > 50000` |
| "must contain all three categories … return 0" | Exactly three rows, always — even for an empty category |
| output columns `category`, `accounts_count` | A constant label and a count |

🤔 **Before you open the next section:** if you label each account with `CASE` and `GROUP BY` the label, where does the "Average Salary" row come from when no account is average?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **One `SELECT` per category, `UNION ALL`** | `SELECT 'Low Salary', COUNT(*) FROM Accounts WHERE income < 20000 UNION ALL …` | ✅ Each branch always returns one row — `COUNT(*)` is 0 when nothing matches |
| Conditional sums | `SUM(income < 20000)` per branch | ⚠️ Correct on non-empty tables — but `SUM` of no rows is `NULL`, so wrap it in `IFNULL(…, 0)` |
| Categories table + `LEFT JOIN` | three labels in a derived table, left-join the labelled accounts, `COUNT` | ✅ The general fix for "show zero groups" |
| `CASE` + `GROUP BY` | label each account, group by the label | ❌ Empty categories never appear |

**The decision: three `COUNT(*)` queries joined by `UNION ALL`.** An aggregate without `GROUP BY` returns exactly one row, so each category is guaranteed its row.

The grouping version silently loses the empty category:

| `category` | `accounts_count` |
|---|---|
| High Salary | 3 |
| Low Salary | 1 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count
FROM Accounts
WHERE income < 20000
```

**Low salaries.** `'Low Salary'` is a constant — the same string on the one row this query returns. `COUNT(*)` counts the rows that survive the `WHERE`, and is 0 if none do. The column names are set here, in the first branch.
→ [count](../sql/count.md) · [aliases](../sql/aliases.md)

```sql
UNION ALL
```

**Stack the rows.** `UNION ALL` keeps every row; plain `UNION` would also work here (the labels differ), but it does unnecessary duplicate checking.
→ [union](../sql/union.md)

```sql
SELECT 'Average Salary', COUNT(*)
FROM Accounts
WHERE income BETWEEN 20000 AND 50000
```

**Average salaries.** `BETWEEN` is inclusive at both ends, matching "[20000, 50000]". Later branches don't need aliases — the first branch names the columns.
→ [between](../sql/between.md)

```sql
UNION ALL
```

```sql
SELECT 'High Salary', COUNT(*)
FROM Accounts
WHERE income > 50000;
```

<details>
<summary>The whole thing together</summary>

```sql
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count
FROM Accounts
WHERE income < 20000
UNION ALL
SELECT 'Average Salary', COUNT(*)
FROM Accounts
WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'High Salary', COUNT(*)
FROM Accounts
WHERE income > 50000;
```

</details>

**Trace it** — on the example: one income under 20000 (12747), none between 20000 and 50000, three over 50000.

**Why not `SUM(condition)`?** On an empty table — or any time no rows reach the aggregate — `SUM` returns `NULL`, while `COUNT(*)` returns 0:

| `SUM(income < 20000)` | `COUNT(*)` |
|---|---|
| `NULL` | 0 |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — three scans of the table, one per branch (3n). A single-pass version would use conditional sums with `IFNULL`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** — each branch keeps one counter.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "All three categories must appear even when empty, and `GROUP BY` can't create a group with no rows. So I write one aggregate query per category — each returns exactly one row, and `COUNT(*)` is 0 when nothing matches — and stack them with `UNION ALL`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it in one scan." | `SELECT IFNULL(SUM(income < 20000), 0) …` per category in one `SELECT`, then unpivot — or keep the `UNION ALL` of three conditional sums. |
| "Ten categories?" | Put the category names and bounds in a derived table (or a real table) and `LEFT JOIN` the accounts on the range. |
| "Why `UNION ALL` and not `UNION`?" | The rows can't be duplicates, so the dedupe in `UNION` is wasted work. |
| "Sort by the category's salary order?" | Add a sort column to each branch (1, 2, 3) and `ORDER BY` it in an outer query. |

**Traps:**

- **`CASE` + `GROUP BY`** — empty categories vanish.
- **`SUM` without `IFNULL`** — `NULL` instead of 0 when nothing matches.
- **Boundary mistakes** — 20000 and 50000 are "Average".

**This same move shows up in:** [Students and Examinations](1280-students-and-examinations.md) (building rows the data doesn't contain) · [Product Price at a Given Date](1164-product-price-at-a-given-date.md) (a `UNION` adding default rows) · [Big Countries](595-big-countries.md) (`UNION` of filters).

</details>

---
