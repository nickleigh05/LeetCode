# 585. Investments in 2016

**Medium** · [LeetCode](https://leetcode.com/problems/investments-in-2016/) · [Solution file (no hints)](../../problems/0500-0999/585.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Sum `tiv_2016` over policyholders who **share** their `tiv_2015` value with someone else **and** live in a city (`lat`, `lon`) **no one else** shares. Round to 2 decimals.

```
Table: Insurance
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| pid         | int   |
| tiv_2015    | float |
| tiv_2016    | float |
| lat         | float |
| lon         | float |
+-------------+-------+
pid is the primary key (column with unique values) for this table.
Each row of this table contains information about one policy where:
pid is the policyholder's policy ID.
tiv_2015 is the total investment value in 2015 and tiv_2016 is the total investment value in 2016.
lat is the latitude of the policy holder's city. It's guaranteed that lat is not NULL.
lon is the longitude of the policy holder's city. It's guaranteed that lon is not NULL.
```

```
Input:
Insurance table:
+-----+----------+----------+-----+-----+
| pid | tiv_2015 | tiv_2016 | lat | lon |
+-----+----------+----------+-----+-----+
| 1   | 10       | 5        | 10  | 10  |
| 2   | 20       | 20       | 20  | 20  |
| 3   | 10       | 30       | 20  | 20  |
| 4   | 10       | 40       | 40  | 40  |
+-----+----------+----------+-----+-----+
Output:
+----------+
| tiv_2016 |
+----------+
| 45.00    |
+----------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Both conditions are about **other rows**: "same as someone else" and "unlike anyone else". Each one is a group count — over `tiv_2015` and over `(lat, lon)`.

| The statement says | Which really means |
|---|---|
| "same `tiv_2015` value as one or more other policyholders" | Their `tiv_2015` group has `COUNT(*) > 1` |
| "not located in the same city as any other" | Their `(lat, lon)` group has `COUNT(*) = 1` |
| "the (lat, lon) attribute pairs must be unique" | A city is the **pair** — matching `lat` alone isn't the same city |
| "sum of all total investment values in 2016" | `SUM(tiv_2016)` over the rows passing both tests |
| "Round … to two decimal places" | `ROUND(…, 2)` |

🤔 **Before you open the next section:** policyholder 3 shares `tiv_2015 = 10` with others. Why isn't it counted?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Two `IN` subqueries with `HAVING`** | `tiv_2015 IN (… HAVING COUNT(*) > 1) AND (lat, lon) IN (… HAVING COUNT(*) = 1)` | ✅ Each condition is a small grouped query |
| Window counts | `COUNT(*) OVER (PARTITION BY tiv_2015)` and `… OVER (PARTITION BY lat, lon)`, then filter | ✅ Both counts on every row in one pass |
| Separate `lat IN` and `lon IN` tests | | ❌ Treats (10, 20) and (20, 10) as related; a city is the pair |
| Self-joins with `EXISTS` / `NOT EXISTS` | correlated subqueries per row | ✅ Works; harder to read |

**The decision: two grouped `IN` subqueries.** One finds `tiv_2015` values that repeat; the other finds cities that don't. A row must be in both lists.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
```

**The rounded total.** The output column is named `tiv_2016`, like the input column.
→ [aggregate-functions](../sql/aggregate-functions.md) · [math-functions](../sql/math-functions.md)

```sql
FROM Insurance
```

```sql
WHERE tiv_2015 IN (
          SELECT tiv_2015
          FROM Insurance
          GROUP BY tiv_2015
          HAVING COUNT(*) > 1
      )
```

**Condition 1: the 2015 value repeats.** Group by `tiv_2015`, keep values with more than one policyholder.
→ [in-subquery](../sql/in-subquery.md) · [having](../sql/having.md)

```sql
  AND (lat, lon) IN (
          SELECT lat, lon
          FROM Insurance
          GROUP BY lat, lon
          HAVING COUNT(*) = 1
      );
```

**Condition 2: the city is unique.** Group by the **pair** `(lat, lon)`, keep pairs that occur once. The row constructor `(lat, lon) IN (…)` compares both columns together.
→ [in-subquery](../sql/in-subquery.md) · [logical-operators](../sql/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance
WHERE tiv_2015 IN (
          SELECT tiv_2015
          FROM Insurance
          GROUP BY tiv_2015
          HAVING COUNT(*) > 1
      )
  AND (lat, lon) IN (
          SELECT lat, lon
          FROM Insurance
          GROUP BY lat, lon
          HAVING COUNT(*) = 1
      );
```

</details>

**Trace it** — both group counts for every policyholder:

| `pid` | `tiv_2015` | `tiv_2016` | `lat` | `lon` | `same tiv_2015` | `same city` |
|---|---|---|---|---|---|---|
| 1 | 10.0 | 5.0 | 10.0 | 10.0 | 3 | 1 |
| 2 | 20.0 | 20.0 | 20.0 | 20.0 | 1 | 2 |
| 3 | 10.0 | 30.0 | 20.0 | 20.0 | 3 | 2 |
| 4 | 10.0 | 40.0 | 40.0 | 40.0 | 3 | 1 |

Rows 1 and 4 pass: shared 2015 value (3 holders) and a unique city. Row 2 fails both; row 3 shares its city with row 2. Sum: 5 + 40 = 45.00.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — two grouping passes for the subqueries (materialised into hashed sets), then one filter pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the two sets.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Both conditions compare a row with the others, so each is a group count. I keep rows whose `tiv_2015` appears more than once and whose `(lat, lon)` pair appears exactly once — two `IN` subqueries with `HAVING` — and sum `tiv_2016`, rounded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "With window functions?" | `COUNT(*) OVER (PARTITION BY tiv_2015)` and `COUNT(*) OVER (PARTITION BY lat, lon)` in a subquery; filter `> 1` and `= 1`. |
| "These are floats — is `=` safe?" | Comparing floats for equality is fragile in general. Here the values are stored once and compared as-is, so it works; for computed values, compare with a tolerance or use `DECIMAL`. |
| "Return the policy ids instead?" | Same filter, `SELECT pid`. |
| "What if no one qualifies?" | `SUM` of no rows is `NULL`, so the result is `NULL`; wrap in `IFNULL(…, 0)` if 0 is wanted. |

**Traps:**

- **Testing `lat` and `lon` separately** — a city is the pair.
- **`>= 1` for "shared"** — every value appears at least once; "with others" means `> 1`.
- **Counting the city condition with `> 1`** — reversed.

**This same move shows up in:** [Primary Department for Each Employee](1789-primary-department-for-each-employee.md) (row filters based on group counts) · [Biggest Single Number](619-biggest-single-number.md) (`HAVING COUNT(*) = 1`) · [Product Sales Analysis III](1070-product-sales-analysis-iii.md) (row-constructor `IN`).

</details>

---
