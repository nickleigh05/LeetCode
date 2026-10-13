# 595. Big Countries

**Easy** · [LeetCode](https://leetcode.com/problems/big-countries/) · [Solution file (no hints)](../../problems/0500-0999/595.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A country is **big** if its area is at least 3,000,000 km² **or** its population is at least 25,000,000. Return the name, population, and area of every big country, in any order.

```
Table: World
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name is the primary key (column with unique values) for this table.
Each row of this table gives information about the name of a country, the continent to which it belongs, its area, the population, and its GDP value.
```

```
Input:
World table:
+-------------+-----------+---------+------------+--------------+
| name        | continent | area    | population | gdp          |
+-------------+-----------+---------+------------+--------------+
| Afghanistan | Asia      | 652230  | 25500100   | 20343000000  |
| Albania     | Europe    | 28748   | 2831741    | 12960000000  |
| Algeria     | Africa    | 2381741 | 37100000   | 188681000000 |
| Andorra     | Europe    | 468     | 78115      | 3712000000   |
| Angola      | Africa    | 1246700 | 20609294   | 100990000000 |
+-------------+-----------+---------+------------+--------------+
Output:
+-------------+------------+---------+
| name        | population | area    |
+-------------+------------+---------+
| Afghanistan | 25500100   | 652230  |
| Algeria     | 37100000   | 2381741 |
+-------------+------------+---------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Another single-table filter. The new ingredients are `OR`, an inclusive boundary, and a column list in a specific order.

| The statement says | Which really means |
|---|---|
| "big if … **or** …" | Either condition alone is enough → `OR`, not `AND` |
| "**at least** three million" | Inclusive: exactly 3,000,000 counts → `>=`, not `>` |
| "3000000 km2" / "25000000" | Write the literals with no commas or underscores — SQL has no digit separators |
| "name, population, and area" | Three columns, in that order — note the output puts `population` **before** `area` |
| `continent` and `gdp` | Present in the table, irrelevant to the answer. Leave them out |
| `name` is the primary key | Each country appears once — no duplicates to remove |

🤔 **Before you open the next section:** Afghanistan's area is small but its population is 25.5 million. Should it be in the answer?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **One `WHERE` with `OR`** | `WHERE area >= 3000000 OR population >= 25000000` | ✅ One pass, reads like the definition |
| `UNION` of two filters | `… WHERE area >= … UNION … WHERE population >= …` | ✅ Same answer. Can be faster *with an index on each column* — see section 6 |
| `AND` | `WHERE area >= 3000000 AND population >= 25000000` | ❌ Requires **both** — returns nothing on the example |
| `>` instead of `>=` | `WHERE area > 3000000 OR population > 25000000` | ❌ Drops a country sitting exactly on the line |

**The decision: one `WHERE` with `OR`.** It's the definition of "big," written as SQL.

`UNION` is the classic alternative, and it's worth understanding why it's correct: each half returns the countries meeting one condition, and `UNION` merges them **and removes duplicates** — so a country that's big both ways (none in the example, but possible) appears once, just like with `OR`. `UNION ALL` would list it twice.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT name, population, area
```

**Three columns, in the order the expected output lists them.** LeetCode compares the result column by column, so `name, area, population` is marked wrong even though every value in it is right.
→ [select-from](../sql/select-from.md)

```sql
FROM World
```

**One table** — `continent` and `gdp` are simply never mentioned.

```sql
WHERE area >= 3000000 OR population >= 25000000;
```

**The definition of "big."** Each comparison produces true or false per row; `OR` keeps the row if at least one is true. `>=` makes both boundaries inclusive, matching "at least."
→ [comparison-operators](../sql/comparison-operators.md) · [logical-operators](../sql/logical-operators.md) · [union](../sql/union.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000 OR population >= 25000000;
```

</details>

**Trace it** — each half of the `OR`, row by row (`1` = true, `0` = false):

| `name` | `area` | `population` | `big area` | `big pop` | `WHERE says` |
|---|---|---|---|---|---|
| Afghanistan | 652230 | 25500100 | 0 | 1 | kept |
| Albania | 28748 | 2831741 | 0 | 0 | dropped |
| Algeria | 2381741 | 37100000 | 0 | 1 | kept |
| Andorra | 468 | 78115 | 0 | 0 | dropped |
| Angola | 1246700 | 20609294 | 0 | 0 | dropped |

No country in the example is big by area — Afghanistan and Algeria both qualify on population alone. That's exactly the case `AND` would get wrong.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for n countries — one full scan, two comparisons per row.

The `UNION` version is two scans plus a duplicate-removal step, so without indexes it's strictly more work: O(n) for the scans plus the cost of deduplicating the combined result.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output for the `OR` version — rows are filtered as they stream past.

The `UNION` version needs a temporary table to remove duplicates: O(k) for the k rows the two halves return.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Big means either condition, so it's a single filter with `OR`, and 'at least' makes both comparisons `>=`. I return name, population, area in that order. One scan, O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do people write this with `UNION`?" | With an index on `area` **and** one on `population`, each half of a `UNION` can use its own index. A single `OR` across two columns can't use one ordinary index for both — MySQL may fall back to a full scan or try an index merge. On a table of 200 countries, it doesn't matter. |
| "`UNION` or `UNION ALL`?" | `UNION`, so a country that's big both ways isn't listed twice. `UNION ALL` skips the duplicate check — faster, and correct only when the halves can't overlap. |
| "Big by area **and** population?" | `AND` instead of `OR`. |
| "Count the big countries per continent." | Same `WHERE`, then `GROUP BY continent` with `COUNT(*)`. |
| "Sort by population, largest first." | `ORDER BY population DESC`. |

**Traps:**

- **`AND` for "or"** — the most common wrong answer on this problem.
- **`>` for "at least"** — boundary values are exactly what hidden test cases probe.
- **Wrong column order** — `SELECT name, area, population` is marked wrong even with exactly the right rows.
- **`UNION ALL`** — duplicates any country that meets both conditions.

**This same move shows up in:** [Recyclable and Low Fat Products](1757-recyclable-and-low-fat-products.md) (the same filter with `AND`) · [Not Boring Movies](620-not-boring-movies.md) (a filter combining two conditions, plus sorting) · [Count Salary Categories](1907-count-salary-categories.md) (range boundaries, and `UNION` used on purpose).

</details>

---
