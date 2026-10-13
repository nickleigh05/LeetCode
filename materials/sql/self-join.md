# Self-Join

```sql
-- Employee
-- id  name  salary  managerId
-- 1   Ann   90000   NULL
-- 2   Bob   95000   1
-- 3   Cat   60000   1
-- 4   Dan   70000   3

SELECT e.name AS employee, m.name AS manager
FROM Employee e
JOIN Employee m ON e.managerId = m.id;
-- employee  manager
-- Bob       Ann
-- Cat       Ann
-- Dan       Cat

SELECT e.name
FROM Employee e
JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;
-- name
-- Bob
-- Dan

SELECT a.name AS first, b.name AS second
FROM Employee a
JOIN Employee b ON a.managerId = b.managerId AND a.id < b.id;
-- first  second
-- Bob    Cat        ← colleagues, each pair once: a.id < b.id skips (Cat, Bob) and (Bob, Bob)
```

A self-join treats one table as two. Give it two aliases and join them on the relationship between rows: an employee and their manager (`e.managerId = m.id`), a day and the day before (`b.day = a.day + INTERVAL 1 DAY`), a row and the next id (`b.id = a.id + 1`). The aliases are mandatory — they're the only way to say which copy a column comes from.

To list unordered pairs once, add `a.id < b.id`. Use `LEFT JOIN` instead when rows without a partner must stay, like Ann, who has no manager. A self-join on "the next id" assumes the ids have no gaps; [lag-lead](lag-lead.md) compares neighbouring rows whatever the gap.

**Related:** [inner-join](inner-join.md) · [aliases](aliases.md) · [non-equi-join](non-equi-join.md) · [consecutive-rows](consecutive-rows.md) · [date-arithmetic](date-arithmetic.md) · [lag-lead](lag-lead.md)
