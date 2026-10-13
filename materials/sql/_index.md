# SQL Syntax Cookbook

One topic per file, basics to advanced, in MySQL 8 — LeetCode's default dialect. Click into whatever you don't recognize; SQL walkthroughs hyperlink back here instead of re-explaining syntax inline.

Each page shows its example tables as comments above the query, and the result directly underneath it. Every query has been run against MySQL 8.0.

## Absolute Basics
[tables-rows-columns](tables-rows-columns.md) · [select-from](select-from.md) · [execution-order](execution-order.md) · [comments-formatting](comments-formatting.md)

## Columns & Values
[aliases](aliases.md) · [data-types](data-types.md) · [null-is-null](null-is-null.md) · [ifnull-coalesce](ifnull-coalesce.md)

## Filtering Rows
[where](where.md) · [comparison-operators](comparison-operators.md) · [logical-operators](logical-operators.md) · [in-list](in-list.md) · [between](between.md) · [like-wildcards](like-wildcards.md) · [regexp](regexp.md)

## Sorting & Limiting
[order-by](order-by.md) · [limit-offset](limit-offset.md) · [distinct](distinct.md)

## Expressions & Functions
[arithmetic-operators](arithmetic-operators.md) · [math-functions](math-functions.md) · [case-when](case-when.md) · [if-function](if-function.md) · [string-functions](string-functions.md) · [date-arithmetic](date-arithmetic.md) · [date-parts-format](date-parts-format.md)

## Aggregation
[aggregate-functions](aggregate-functions.md) · [count](count.md) · [group-by](group-by.md) · [having](having.md) · [conditional-aggregation](conditional-aggregation.md) · [group-concat](group-concat.md)

## Joins
[joins-overview](joins-overview.md) · [inner-join](inner-join.md) · [left-join](left-join.md) · [on-vs-where](on-vs-where.md) · [anti-join](anti-join.md) · [self-join](self-join.md) · [cross-join](cross-join.md) · [right-full-outer-join](right-full-outer-join.md) · [non-equi-join](non-equi-join.md)

## Subqueries & CTEs
[scalar-subquery](scalar-subquery.md) · [in-subquery](in-subquery.md) · [exists](exists.md) · [correlated-subquery](correlated-subquery.md) · [derived-tables](derived-tables.md) · [cte-with](cte-with.md) · [recursive-cte](recursive-cte.md)

## Set Operations
[union](union.md) · [intersect-except](intersect-except.md)

## Window Functions
[window-functions](window-functions.md) · [ranking-functions](ranking-functions.md) · [lag-lead](lag-lead.md) · [window-aggregates](window-aggregates.md) · [window-frames](window-frames.md) · [first-last-value](first-last-value.md)

## Writing Data
[delete](delete.md) · [update](update.md) · [create-table-insert](create-table-insert.md)

## Functions & Performance
[create-function](create-function.md) · [indexes](indexes.md)

## Common Interview Patterns
[top-n-per-group](top-n-per-group.md) · [nth-highest-value](nth-highest-value.md) · [first-row-per-group](first-row-per-group.md) · [consecutive-rows](consecutive-rows.md) · [running-totals](running-totals.md) · [ratios-percentages](ratios-percentages.md) · [pivot-unpivot](pivot-unpivot.md) · [anti-join](anti-join.md)
