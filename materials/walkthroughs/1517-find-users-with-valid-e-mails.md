# 1517. Find Users With Valid E-Mails

**Easy** · [LeetCode](https://leetcode.com/problems/find-users-with-valid-e-mails/) · [Solution file (no hints)](../../problems/1500-1999/1517.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

A valid email is a **prefix** starting with a letter, followed by letters, digits, `_`, `.`, or `-`, then exactly **`@leetcode.com`** in lowercase. Return the users with valid emails. Any order.

```
Table: Users
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
| mail          | varchar |
+---------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains information of the users signed up in a website. Some e-mails are invalid.
```

```
Input:
Users table:
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 2       | Jonathan  | jonathanisgreat         |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
| 5       | Marwan    | quarz#2020@leetcode.com |
| 6       | David     | david69@gmail.com       |
| 7       | Shapiro   | .shapo@leetcode.com     |
+---------+-----------+-------------------------+
Output:
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
+---------+-----------+-------------------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

A rule about the **shape of the whole string** — that's a regular expression, anchored at both ends.

| The statement says | Which really means |
|---|---|
| "must start with a letter" | First character: `[a-zA-Z]` |
| "may contain letters, digits, underscore, period, and/or dash" | Then zero or more of `[a-zA-Z0-9_.-]` |
| "domain must be exactly '@leetcode.com'" | Then the literal text — and nothing after it |
| "in lowercase" | `@LEETCODE.COM` is invalid — the match must be **case-sensitive** |
| `.shapo@…` invalid, `bella-@…` valid | The first-character rule is strict; the rest is permissive |

The whole pattern: `^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode[.]com$`. `^` and `$` pin it to the start and end of the string.

🤔 **Before you open the next section:** in a regular expression, what does an unescaped `.` match?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **`REGEXP_LIKE(…, 'c')`** | `REGEXP_LIKE(mail, '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode[.]com$', 'c')` | ✅ Anchored, literal dot, case-sensitive |
| Binary collation | `mail COLLATE utf8mb4_bin REGEXP '…'` | ✅ Also case-sensitive |
| `REGEXP` with the default collation | `mail REGEXP '…'` | ⚠️ Case-insensitive — accepts `ann@LEETCODE.COM` |
| `LIKE '%@leetcode.com'` | | ❌ Can't check the prefix's characters |
| Unescaped dot | `…@leetcode.com$` | ❌ `.` matches any character — accepts `a@leetcodeXcom` |

**The decision: `REGEXP_LIKE` with the `'c'` flag.** MySQL's default collation compares case-insensitively, and `REGEXP` follows the collation — so `'c'` is what enforces "in lowercase".

Three tricky addresses against each version:

| `mail` | `REGEXP (default)` | `unescaped dot` | `REGEXP_LIKE … 'c'` |
|---|---|---|---|
| ann@LEETCODE.COM | 1 | 1 | 0 |
| a@leetcodeXcom | 0 | 1 | 0 |
| Ann@leetcode.com | 1 | 1 | 1 |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT user_id, name, mail
```

```sql
FROM Users
```

```sql
WHERE REGEXP_LIKE(mail, '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode[.]com$', 'c');
```

**The whole address must match the pattern, case-sensitively.**

- `^` — start of the string; `$` — end. Without them, the pattern could match a fragment in the middle.
- `[a-zA-Z]` — exactly one letter first.
- `[a-zA-Z0-9_.-]*` — any number of allowed characters. Inside brackets, `.` is a literal dot, and `-` at the end is a literal dash.
- `[.]` — a literal dot outside brackets. (`\\.` also works, but needs double escaping inside a SQL string.)
- `'c'` — case-sensitive matching.

→ [regexp](../sql/regexp.md) · [where](../sql/where.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT user_id, name, mail
FROM Users
WHERE REGEXP_LIKE(mail, '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode[.]com$', 'c');
```

</details>

**Trace it** — the example's addresses:

| `user_id` | `mail` | `valid?` |
|---|---|---|
| 1 | winston@leetcode.com | 1 |
| 2 | jonathanisgreat | 0 |
| 3 | bella-@leetcode.com | 1 |
| 4 | sally.come@leetcode.com | 1 |
| 5 | quarz#2020@leetcode.com | 0 |
| 6 | david69@gmail.com | 0 |
| 7 | .shapo@leetcode.com | 0 |

User 2 has no domain, 5 has `#`, 6 has the wrong domain, 7 starts with a period.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · L)</summary>

**O(n · L)** — the regex engine scans each address of length L ≤ 50 once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output (the compiled pattern is constant size).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The rule is about the whole string's shape, so it's an anchored regex: a letter, then letters, digits, underscore, dot or dash, then the literal `@leetcode.com` and the end of the string. I escape the dot, and I use `REGEXP_LIKE` with `'c'` because MySQL's default collation would otherwise accept an uppercase domain."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `[.]` instead of `.`?" | An unescaped dot matches any character. |
| "Why the `'c'` flag?" | Under the default `utf8mb4_0900_ai_ci` collation, `REGEXP` ignores case. |
| "Allow any domain?" | Replace the literal with something like `@[a-zA-Z0-9-]+([.][a-zA-Z0-9-]+)+$` — real email validation is much harder than any one regex. |
| "Extract the domain?" | `SUBSTRING_INDEX(mail, '@', -1)`. |
| "`LIKE` or `REGEXP`?" | `LIKE` has only `%` and `_` — no character classes. Use `REGEXP` when the rule is about *which* characters appear. |

**Traps:**

- **Unescaped `.`** — `leetcodeXcom` passes.
- **Missing `^` or `$`** — `xx.shapo@leetcode.com.org` style strings slip through.
- **Case-insensitive matching** — uppercase domains pass under the default collation.
- **`\.` in a SQL string** — MySQL's string parser eats the backslash; it has to be `\\.`. `[.]` avoids the question.

**This same move shows up in:** [Patients With a Condition](1527-patients-with-a-condition.md) (pattern matching inside a string) · [Invalid Tweets](1683-invalid-tweets.md) (filtering on a string property) · [Fix Names in a Table](1667-fix-names-in-a-table.md) (case functions).

</details>

---
