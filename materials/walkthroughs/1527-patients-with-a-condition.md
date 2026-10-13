# 1527. Patients With a Condition

**Easy** · [LeetCode](https://leetcode.com/problems/patients-with-a-condition/) · [Solution file (no hints)](../../problems/1500-1999/1527.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

`conditions` holds zero or more space-separated codes. Find patients with Type I Diabetes — any code that **starts with** `DIAB1`. Any order.

```
Table: Patients
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| patient_id   | int     |
| patient_name | varchar |
| conditions   | varchar |
+--------------+---------+
patient_id is the primary key (column with unique values) for this table.
'conditions' contains 0 or more code separated by spaces. 
This table contains information of the patients in the hospital.
```

```
Input:
Patients table:
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 1          | Daniel       | YFEV COUGH   |
| 2          | Alice        |              |
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
| 5          | Alain        | DIAB201      |
+------------+--------------+--------------+
Output:
+------------+--------------+--------------+
| patient_id | patient_name | conditions   |
+------------+--------------+--------------+
| 3          | Bob          | DIAB100 MYOP |
| 4          | George       | ACNE DIAB100 |
+------------+--------------+--------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The trap is the word **starts**. A code can be anywhere in the list, but `DIAB1` must be at the start of a *code*, not just somewhere in the string.

| The statement says | Which really means |
|---|---|
| "0 or more code separated by spaces" | The column is a list: codes joined by single spaces |
| "Type I Diabetes always starts with DIAB1 prefix" | Some code begins with `DIAB1` — like `DIAB100` |
| George: `ACNE DIAB100` | The code can come after others — so not just "the string starts with" |
| a code like `SADIAB100` | Contains `DIAB1` but doesn't **start** with it — must not match |

A code starts with `DIAB1` exactly when either the whole string starts with it, or it appears right after a space.

🤔 **Before you open the next section:** `conditions LIKE '%DIAB1%'` finds both Bob and George. What else does it find?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Two `LIKE` patterns** | `LIKE 'DIAB1%' OR LIKE '% DIAB1%'` | ✅ First code, or any code after a space |
| `REGEXP` | `conditions REGEXP '(^\| )DIAB1'` | ✅ The same two cases in one pattern |
| Pad with a leading space | `CONCAT(' ', conditions) LIKE '% DIAB1%'` | ✅ Turns the first-code case into the after-a-space case |
| `LIKE '%DIAB1%'` | | ❌ Matches `DIAB1` in the middle of a code |

**The decision: two `LIKE` patterns.** `%` matches any run of characters (including none), and the space before `DIAB1` in the second pattern pins it to the start of a code.

The one-pattern shortcut gets this wrong:

| `patient_id` | `conditions` | `LIKE '%DIAB1%'` | `correct` |
|---|---|---|---|
| 1 | SADIAB100 | 1 | 0 |
| 2 | DIAB100 MYOP | 1 | 1 |
| 3 | ACNE DIAB100 | 1 | 1 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT patient_id, patient_name, conditions
```

```sql
FROM Patients
```

```sql
WHERE conditions LIKE 'DIAB1%'
   OR conditions LIKE '% DIAB1%';
```

**The first code starts with `DIAB1`, or a later one does.** `'DIAB1%'` — the string begins with `DIAB1`. `'% DIAB1%'` — somewhere there's a space followed by `DIAB1`, i.e. a later code begins with it.
→ [like-wildcards](../sql/like-wildcards.md) · [logical-operators](../sql/logical-operators.md) · [regexp](../sql/regexp.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT patient_id, patient_name, conditions
FROM Patients
WHERE conditions LIKE 'DIAB1%'
   OR conditions LIKE '% DIAB1%';
```

</details>

**Trace it** — both patterns per patient:

| `patient_id` | `conditions` | `starts with DIAB1` | `a later code starts with DIAB1` |
|---|---|---|---|
| 1 | YFEV COUGH | 0 | 0 |
| 2 |  | 0 | 0 |
| 3 | DIAB100 MYOP | 1 | 0 |
| 4 | ACNE DIAB100 | 0 | 1 |
| 5 | DIAB201 | 0 | 0 |

Bob matches the first pattern, George the second. `DIAB201` starts with `DIAB2`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · L)</summary>

**O(n · L)** — each pattern scans a string of length L ≤ 100. A leading `%` prevents any index from helping.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Conditions are space-separated codes, and I need any code that *starts* with `DIAB1`. That's either the first code — `LIKE 'DIAB1%'` — or a code after a space — `LIKE '% DIAB1%'`. A bare `'%DIAB1%'` would also match codes that merely contain it."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "In one pattern?" | `REGEXP '(^\| )DIAB1'` — or `\\bDIAB1` (a word boundary). |
| "Is `LIKE` case-sensitive?" | Not under MySQL's default collation — `'diab100'` would match too. For exact case, use `LIKE BINARY 'DIAB1%'` or a `_bin` collation. |
| "Better schema?" | One row per (patient, condition) in a separate table. Then it's `WHERE code LIKE 'DIAB1%'`, and indexable. |
| "Count patients per condition prefix?" | Much easier with that normalised table. |

**Traps:**

- **`'%DIAB1%'`** — matches `SADIAB100`.
- **Only `'DIAB1%'`** — misses George, whose diabetes code isn't first.
- **Forgetting the space in `'% DIAB1%'`** — you're back to "anywhere".

**This same move shows up in:** [Find Users With Valid E-Mails](1517-find-users-with-valid-e-mails.md) (a pattern that must match exactly) · [Invalid Tweets](1683-invalid-tweets.md) (filtering on a string property) · [Fix Names in a Table](1667-fix-names-in-a-table.md) (string functions).

</details>

---
