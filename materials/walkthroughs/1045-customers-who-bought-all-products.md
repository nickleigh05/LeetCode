# 1045. Customers Who Bought All Products

**Medium** · [LeetCode](https://leetcode.com/problems/customers-who-bought-all-products/) · [Solution file (no hints)](../../problems/1000-1499/1045.sql)

[🗺 Roadmap](../../roadmap.md) · [📋 All SQL 50 problems](../../lists/sql.md)

---

Report the customers who bought **every** product in the `Product` table. Any order.

```
Table: Customer
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| customer_id | int     |
| product_key | int     |
+-------------+---------+
This table may contain duplicates rows. 
customer_id is not NULL.
product_key is a foreign key (reference column) to Product table.

Table: Product
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_key | int     |
+-------------+---------+
product_key is the primary key (column with unique values) for this table.
```

```
Input:
Customer table:
+-------------+-------------+
| customer_id | product_key |
+-------------+-------------+
| 1           | 5           |
| 2           | 6           |
| 3           | 5           |
| 3           | 6           |
| 1           | 6           |
+-------------+-------------+
Product table:
+-------------+
| product_key |
+-------------+
| 5           |
| 6           |
+-------------+
Output:
+-------------+
| customer_id |
+-------------+
| 1           |
| 3           |
+-------------+
```

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

"Bought all products" is a comparison between two counts: how many **different** products this customer bought, and how many products exist.

| The statement says | Which really means |
|---|---|
| "bought **all** the products" | The customer's set of products equals the full set |
| `product_key` is a foreign key to `Product` | A customer can only buy real products — so "same size" means "same set" |
| "may contain duplicate rows" | A customer can buy the same product twice — count **distinct** products |
| the full set | `(SELECT COUNT(*) FROM Product)` |

Because every `product_key` a customer bought is a real product, a customer with as many distinct products as the table has must have bought each one.

🤔 **Before you open the next section:** customer 1 bought product 5 twice and nothing else. With two products in the table, what goes wrong if you count rows?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Code | Verdict |
|---|---|---|
| **Compare distinct count to total** | `HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product)` | ✅ One grouping pass |
| Double `NOT EXISTS` | "no product exists that this customer didn't buy" | ✅ The classic relational-division form; correct even without the foreign key |
| `COUNT(product_key)` | counts rows | ❌ Duplicate purchases inflate it |

**The decision: the distinct count.** It relies on the foreign key, which the statement guarantees.

With a duplicate purchase:

| `customer_id` | `COUNT(product_key)` | `COUNT(DISTINCT …)` |
|---|---|---|
| 1 | 2 | 1 |
| 2 | 1 | 1 |

Counting rows says customer 1 bought 2 products; they bought one product twice.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```sql
SELECT customer_id
```

```sql
FROM Customer
```

```sql
GROUP BY customer_id
```

→ [group-by](../sql/group-by.md)

```sql
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);
```

**Keep customers whose distinct products equal the number of products.** The right side is a scalar subquery — computed once, compared with every group.
→ [having](../sql/having.md) · [count](../sql/count.md) · [scalar-subquery](../sql/scalar-subquery.md)

<details>
<summary>The whole thing together</summary>

```sql
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);
```

</details>

**Trace it** — per customer:

| `customer_id` | `COUNT(*)` | `COUNT(DISTINCT product_key)` | `products` |
|---|---|---|---|
| 1 | 2 | 2 | 2 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 2 |

Customers 1 and 3 have 2 distinct products, which matches the 2 products in the table.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + p)</summary>

**O(n)** to group n purchase rows with per-customer distinct sets, plus **O(p)** to count the products once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** worst case for the distinct (customer, product) pairs.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Bought everything means the number of distinct products a customer bought equals the number of products. I group by customer and compare `COUNT(DISTINCT product_key)` with a scalar subquery counting `Product`. Distinct because purchases can repeat; and it's safe because every key is a real product."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `Customer` could reference products not in `Product`?" | Count only real products: join to `Product` first, or use the double `NOT EXISTS`. |
| "Customers who bought **every product in a category**?" | Filter both sides to the category, then compare the counts. |
| "Customers missing exactly one product?" | `HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product) - 1`. |
| "What is this pattern called?" | Relational division — "find X related to *all* of Y." |

**Traps:**

- **`COUNT` without `DISTINCT`** — duplicates fake a full set.
- **Hard-coding the product count** — `= 2` breaks on any other data.

**This same move shows up in:** [Students and Examinations](1280-students-and-examinations.md) (comparing against the full set of subjects) · [Number of Unique Subjects Taught by Each Teacher](2356-number-of-unique-subjects-taught-by-each-teacher.md) (`COUNT(DISTINCT …)`) · [Percentage of Users Attended a Contest](1633-percentage-of-users-attended-a-contest.md) (a scalar-subquery total).

</details>

---
