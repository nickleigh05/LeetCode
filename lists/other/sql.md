# SQL 50 — Interview Roadmap
The LeetCode SQL 50 study plan in order, plus a handful of bonus problems that show up constantly in online assessments. Each phase builds on the one before it, so work straight down the list. Do a quick syntax pass first (SQLBolt lessons 1–12, about 2 hours) so the language itself isn't new.

**56 problems · 32 Easy · 22 Medium · 2 Hard**

---

## How to work through it
- Pace: about 2 problems a night clears the 50 in under a month.
- Stay stuck 20–25 minutes before reading a solution. Then close it and rewrite it from memory the next day.
- Write the query in stages: raw rows, then the join, then the filter, then the aggregation.
- Keep one line per problem naming its pattern (top-N per group, anti-join, running total, self-join). Reviewing that before an OA beats re-solving.
- Before Phase 6, spend an hour on window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `SUM() OVER`). Most OAs lean on them.
- Use MySQL, the LeetCode default, and stay with one dialect.

---

## 1. Basic SELECT (5 problems)
*`SELECT`, `WHERE`, `DISTINCT`, `LIKE`, `IS NULL`. Get comfortable reading a table and filtering rows.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 1757 | Easy | Recyclable and Low Fat Products | [Link](https://leetcode.com/problems/recyclable-and-low-fat-products/) | [Solution](../../problems/1500-1999/1757.sql) | [Walkthrough](../../materials/walkthroughs/1757-recyclable-and-low-fat-products.md) |
| 584 | Easy | Find Customer Referee | [Link](https://leetcode.com/problems/find-customer-referee/) | [Solution](../../problems/0500-0999/584.sql) | [Walkthrough](../../materials/walkthroughs/584-find-customer-referee.md) |
| 595 | Easy | Big Countries | [Link](https://leetcode.com/problems/big-countries/) | [Solution](../../problems/0500-0999/595.sql) | [Walkthrough](../../materials/walkthroughs/595-big-countries.md) |
| 1148 | Easy | Article Views I | [Link](https://leetcode.com/problems/article-views-i/) | [Solution](../../problems/1000-1499/1148.sql) | [Walkthrough](../../materials/walkthroughs/1148-article-views-i.md) |
| 1683 | Easy | Invalid Tweets | [Link](https://leetcode.com/problems/invalid-tweets/) | [Solution](../../problems/1500-1999/1683.sql) | [Walkthrough](../../materials/walkthroughs/1683-invalid-tweets.md) |

## 2. Joins (9 problems)
*`INNER JOIN`, `LEFT JOIN`, self-joins, and the anti-join (`LEFT JOIN ... WHERE x IS NULL`).*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 1378 | Easy | Replace Employee ID With The Unique Identifier | [Link](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/) | [Solution](../../problems/1000-1499/1378.sql) | [Walkthrough](../../materials/walkthroughs/1378-replace-employee-id-with-the-unique-identifier.md) |
| 1068 | Easy | Product Sales Analysis I | [Link](https://leetcode.com/problems/product-sales-analysis-i/) | [Solution](../../problems/1000-1499/1068.sql) | [Walkthrough](../../materials/walkthroughs/1068-product-sales-analysis-i.md) |
| 1581 | Easy | Customer Who Visited but Did Not Make Any Transactions | [Link](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/) | [Solution](../../problems/1500-1999/1581.sql) | [Walkthrough](../../materials/walkthroughs/1581-customer-who-visited-but-did-not-make-any-transactions.md) |
| 197 | Easy | Rising Temperature | [Link](https://leetcode.com/problems/rising-temperature/) | [Solution](../../problems/0001-0499/197.sql) | [Walkthrough](../../materials/walkthroughs/197-rising-temperature.md) |
| 1661 | Easy | Average Time of Process per Machine | [Link](https://leetcode.com/problems/average-time-of-process-per-machine/) | [Solution](../../problems/1500-1999/1661.sql) | [Walkthrough](../../materials/walkthroughs/1661-average-time-of-process-per-machine.md) |
| 577 | Easy | Employee Bonus | [Link](https://leetcode.com/problems/employee-bonus/) | [Solution](../../problems/0500-0999/577.sql) | [Walkthrough](../../materials/walkthroughs/577-employee-bonus.md) |
| 1280 | Easy | Students and Examinations | [Link](https://leetcode.com/problems/students-and-examinations/) | [Solution](../../problems/1000-1499/1280.sql) | [Walkthrough](../../materials/walkthroughs/1280-students-and-examinations.md) |
| 570 | Medium | Managers with at Least 5 Direct Reports | [Link](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/) | [Solution](../../problems/0500-0999/570.sql) | [Walkthrough](../../materials/walkthroughs/570-managers-with-at-least-5-direct-reports.md) |
| 1934 | Medium | Confirmation Rate | [Link](https://leetcode.com/problems/confirmation-rate/) | [Solution](../../problems/1500-1999/1934.sql) | [Walkthrough](../../materials/walkthroughs/1934-confirmation-rate.md) |

## 3. Aggregate Functions (8 problems)
*`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`. `WHERE` filters rows before grouping; `HAVING` filters groups after.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 620 | Easy | Not Boring Movies | [Link](https://leetcode.com/problems/not-boring-movies/) | [Solution](../../problems/0500-0999/620.sql) | [Walkthrough](../../materials/walkthroughs/620-not-boring-movies.md) |
| 1251 | Easy | Average Selling Price | [Link](https://leetcode.com/problems/average-selling-price/) | [Solution](../../problems/1000-1499/1251.sql) | [Walkthrough](../../materials/walkthroughs/1251-average-selling-price.md) |
| 1075 | Easy | Project Employees I | [Link](https://leetcode.com/problems/project-employees-i/) | [Solution](../../problems/1000-1499/1075.sql) | [Walkthrough](../../materials/walkthroughs/1075-project-employees-i.md) |
| 1633 | Easy | Percentage of Users Attended a Contest | [Link](https://leetcode.com/problems/percentage-of-users-attended-a-contest/) | [Solution](../../problems/1500-1999/1633.sql) | [Walkthrough](../../materials/walkthroughs/1633-percentage-of-users-attended-a-contest.md) |
| 1211 | Easy | Queries Quality and Percentage | [Link](https://leetcode.com/problems/queries-quality-and-percentage/) | [Solution](../../problems/1000-1499/1211.sql) | [Walkthrough](../../materials/walkthroughs/1211-queries-quality-and-percentage.md) |
| 1193 | Medium | Monthly Transactions I | [Link](https://leetcode.com/problems/monthly-transactions-i/) | [Solution](../../problems/1000-1499/1193.sql) | [Walkthrough](../../materials/walkthroughs/1193-monthly-transactions-i.md) |
| 1174 | Medium | Immediate Food Delivery II | [Link](https://leetcode.com/problems/immediate-food-delivery-ii/) | [Solution](../../problems/1000-1499/1174.sql) | [Walkthrough](../../materials/walkthroughs/1174-immediate-food-delivery-ii.md) |
| 550 | Medium | Game Play Analysis IV | [Link](https://leetcode.com/problems/game-play-analysis-iv/) | [Solution](../../problems/0500-0999/550.sql) | [Walkthrough](../../materials/walkthroughs/550-game-play-analysis-iv.md) |

## 4. Sorting and Grouping (7 problems)
*`ORDER BY`, `GROUP BY` with `DISTINCT` counts, and grouping conditions.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 2356 | Easy | Number of Unique Subjects Taught by Each Teacher | [Link](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/) | [Solution](../../problems/2000-2499/2356.sql) | [Walkthrough](../../materials/walkthroughs/2356-number-of-unique-subjects-taught-by-each-teacher.md) |
| 1141 | Easy | User Activity for the Past 30 Days I | [Link](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/) | [Solution](../../problems/1000-1499/1141.sql) | [Walkthrough](../../materials/walkthroughs/1141-user-activity-for-the-past-30-days-i.md) |
| 1070 | Medium | Product Sales Analysis III | [Link](https://leetcode.com/problems/product-sales-analysis-iii/) | [Solution](../../problems/1000-1499/1070.sql) | [Walkthrough](../../materials/walkthroughs/1070-product-sales-analysis-iii.md) |
| 596 | Easy | Classes With at Least 5 Students | [Link](https://leetcode.com/problems/classes-with-at-least-5-students/) | [Solution](../../problems/0500-0999/596.sql) | [Walkthrough](../../materials/walkthroughs/596-classes-with-at-least-5-students.md) |
| 1729 | Easy | Find Followers Count | [Link](https://leetcode.com/problems/find-followers-count/) | [Solution](../../problems/1500-1999/1729.sql) | [Walkthrough](../../materials/walkthroughs/1729-find-followers-count.md) |
| 619 | Easy | Biggest Single Number | [Link](https://leetcode.com/problems/biggest-single-number/) | [Solution](../../problems/0500-0999/619.sql) | [Walkthrough](../../materials/walkthroughs/619-biggest-single-number.md) |
| 1045 | Medium | Customers Who Bought All Products | [Link](https://leetcode.com/problems/customers-who-bought-all-products/) | [Solution](../../problems/1000-1499/1045.sql) | [Walkthrough](../../materials/walkthroughs/1045-customers-who-bought-all-products.md) |

## 5. Advanced Select and Joins (7 problems)
*Self-joins, `CASE WHEN`, `UNION`, gap and consecutive detection, and last-value-as-of-date lookups.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 1731 | Easy | The Number of Employees Which Report to Each Employee | [Link](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/) | [Solution](../../problems/1500-1999/1731.sql) | [Walkthrough](../../materials/walkthroughs/1731-the-number-of-employees-which-report-to-each-employee.md) |
| 1789 | Easy | Primary Department for Each Employee | [Link](https://leetcode.com/problems/primary-department-for-each-employee/) | [Solution](../../problems/1500-1999/1789.sql) | [Walkthrough](../../materials/walkthroughs/1789-primary-department-for-each-employee.md) |
| 610 | Easy | Triangle Judgement | [Link](https://leetcode.com/problems/triangle-judgement/) | [Solution](../../problems/0500-0999/610.sql) | [Walkthrough](../../materials/walkthroughs/610-triangle-judgement.md) |
| 180 | Medium | Consecutive Numbers | [Link](https://leetcode.com/problems/consecutive-numbers/) | [Solution](../../problems/0001-0499/180.sql) | [Walkthrough](../../materials/walkthroughs/180-consecutive-numbers.md) |
| 1164 | Medium | Product Price at a Given Date | [Link](https://leetcode.com/problems/product-price-at-a-given-date/) | [Solution](../../problems/1000-1499/1164.sql) | [Walkthrough](../../materials/walkthroughs/1164-product-price-at-a-given-date.md) |
| 1204 | Medium | Last Person to Fit in the Bus | [Link](https://leetcode.com/problems/last-person-to-fit-in-the-bus/) | [Solution](../../problems/1000-1499/1204.sql) | [Walkthrough](../../materials/walkthroughs/1204-last-person-to-fit-in-the-bus.md) |
| 1907 | Medium | Count Salary Categories | [Link](https://leetcode.com/problems/count-salary-categories/) | [Solution](../../problems/1500-1999/1907.sql) | [Walkthrough](../../materials/walkthroughs/1907-count-salary-categories.md) |

## 6. Subqueries and Window Functions (7 problems)
*Subqueries in `WHERE` and `FROM`, CTEs, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, running totals with `SUM() OVER`.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 1978 | Easy | Employees Whose Manager Left the Company | [Link](https://leetcode.com/problems/employees-whose-manager-left-the-company/) | [Solution](../../problems/1500-1999/1978.sql) | [Walkthrough](../../materials/walkthroughs/1978-employees-whose-manager-left-the-company.md) |
| 626 | Medium | Exchange Seats | [Link](https://leetcode.com/problems/exchange-seats/) | [Solution](../../problems/0500-0999/626.sql) | [Walkthrough](../../materials/walkthroughs/626-exchange-seats.md) |
| 1341 | Medium | Movie Rating | [Link](https://leetcode.com/problems/movie-rating/) | [Solution](../../problems/1000-1499/1341.sql) | [Walkthrough](../../materials/walkthroughs/1341-movie-rating.md) |
| 1321 | Medium | Restaurant Growth | [Link](https://leetcode.com/problems/restaurant-growth/) | [Solution](../../problems/1000-1499/1321.sql) | [Walkthrough](../../materials/walkthroughs/1321-restaurant-growth.md) |
| 602 | Medium | Friend Requests II: Who Has the Most Friends | [Link](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/) | [Solution](../../problems/0500-0999/602.sql) | [Walkthrough](../../materials/walkthroughs/602-friend-requests-ii-who-has-the-most-friends.md) |
| 585 | Medium | Investments in 2016 | [Link](https://leetcode.com/problems/investments-in-2016/) | [Solution](../../problems/0500-0999/585.sql) | [Walkthrough](../../materials/walkthroughs/585-investments-in-2016.md) |
| 185 | Hard | Department Top Three Salaries | [Link](https://leetcode.com/problems/department-top-three-salaries/) | [Solution](../../problems/0001-0499/185.sql) | [Walkthrough](../../materials/walkthroughs/185-department-top-three-salaries.md) |

## 7. Strings and Cleanup (7 problems)
*String functions, `LIKE`/`REGEXP`, `DELETE`, `GROUP_CONCAT`, and `LIMIT`/`OFFSET` tricks.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 1667 | Easy | Fix Names in a Table | [Link](https://leetcode.com/problems/fix-names-in-a-table/) | [Solution](../../problems/1500-1999/1667.sql) | [Walkthrough](../../materials/walkthroughs/1667-fix-names-in-a-table.md) |
| 1527 | Easy | Patients With a Condition | [Link](https://leetcode.com/problems/patients-with-a-condition/) | [Solution](../../problems/1500-1999/1527.sql) | [Walkthrough](../../materials/walkthroughs/1527-patients-with-a-condition.md) |
| 196 | Easy | Delete Duplicate Emails | [Link](https://leetcode.com/problems/delete-duplicate-emails/) | [Solution](../../problems/0001-0499/196.sql) | [Walkthrough](../../materials/walkthroughs/196-delete-duplicate-emails.md) |
| 176 | Medium | Second Highest Salary | [Link](https://leetcode.com/problems/second-highest-salary/) | [Solution](../../problems/0001-0499/176.sql) | [Walkthrough](../../materials/walkthroughs/176-second-highest-salary.md) |
| 1484 | Easy | Group Sold Products By The Date | [Link](https://leetcode.com/problems/group-sold-products-by-the-date/) | [Solution](../../problems/1000-1499/1484.sql) | [Walkthrough](../../materials/walkthroughs/1484-group-sold-products-by-the-date.md) |
| 1327 | Easy | List the Products Ordered in a Period | [Link](https://leetcode.com/problems/list-the-products-ordered-in-a-period/) | [Solution](../../problems/1000-1499/1327.sql) | [Walkthrough](../../materials/walkthroughs/1327-list-the-products-ordered-in-a-period.md) |
| 1517 | Easy | Find Users With Valid E-Mails | [Link](https://leetcode.com/problems/find-users-with-valid-e-mails/) | [Solution](../../problems/1500-1999/1517.sql) | [Walkthrough](../../materials/walkthroughs/1517-find-users-with-valid-e-mails.md) |

## 8. Bonus: Common OA Problems (6 problems)
*Not in the SQL 50, but they show up again and again in online assessments. Do these after the 50.*

| # | Difficulty | Problem | LeetCode | Solution | Walkthrough |
|---|------------|---------|----------|----------|-------------|
| 178 | Medium | Rank Scores | [Link](https://leetcode.com/problems/rank-scores/) | [Solution](../../problems/0001-0499/178.sql) | [Walkthrough](../../materials/walkthroughs/178-rank-scores.md) |
| 184 | Medium | Department Highest Salary | [Link](https://leetcode.com/problems/department-highest-salary/) | [Solution](../../problems/0001-0499/184.sql) | [Walkthrough](../../materials/walkthroughs/184-department-highest-salary.md) |
| 177 | Medium | Nth Highest Salary | [Link](https://leetcode.com/problems/nth-highest-salary/) | [Solution](../../problems/0001-0499/177.sql) | [Walkthrough](../../materials/walkthroughs/177-nth-highest-salary.md) |
| 262 | Hard | Trips and Users | [Link](https://leetcode.com/problems/trips-and-users/) | [Solution](../../problems/0001-0499/262.sql) | [Walkthrough](../../materials/walkthroughs/262-trips-and-users.md) |
| 1393 | Medium | Capital Gain/Loss | [Link](https://leetcode.com/problems/capital-gainloss/) | [Solution](../../problems/1000-1499/1393.sql) | [Walkthrough](../../materials/walkthroughs/1393-capital-gainloss.md) |
| 1158 | Medium | Market Analysis I | [Link](https://leetcode.com/problems/market-analysis-i/) | [Solution](../../problems/1000-1499/1158.sql) | [Walkthrough](../../materials/walkthroughs/1158-market-analysis-i.md) |

---

## Patterns to know cold
- **Top-N per group:** `DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)`
- **"Customers who never...":** `LEFT JOIN ... WHERE x IS NULL`
- **Running total:** `SUM(...) OVER (ORDER BY ...)`
- **Consecutive / gap detection:** `LAG`/`LEAD`, or a self-join on `id + 1`
- **Compare to a neighbor row or manager:** self-join
- **Conditional counts:** `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`
