# 2-D Dynamic Programming

*Same engine as 1-D, but the state is a grid. Usually string matching or path problems — two indices, one table.*

## Recognize this pattern when...

- You're comparing **two strings or sequences** (edit distance, common subsequence, matching).
- It's a **grid** and you count paths or optimize a route through it.
- There's a **capacity / budget** plus items → 0/1 or unbounded knapsack.
- The subproblem is naturally indexed by a **range `[i, j]`** of the input (interval DP).
- A 1-D state isn't enough — the answer depends on **two independent positions**.

## Variations

1. **Grid path count / cost** — come from above or left; first row/col are base cases. *(Unique Paths, Minimum Path Sum)*
2. **Two-sequence matching** — `dp[i][j]` over prefixes; branch on char match. *(Longest Common Subsequence, Edit Distance)*
3. **0/1 knapsack** — `dp[i][capacity]`; iterate capacity carefully to avoid reusing an item. *(Partition Equal Subset Sum, Target Sum)*
4. **Interval / range DP** — `dp[i][j]` over substrings; iterate by *increasing length*. *(Burst Balloons, Longest Palindromic Subsequence)*
5. **Wildcard / pattern matching** — extra branches for `.`, `*`, `?`. *(Regular Expression Matching)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 62 | Medium | Unique Paths |
| 1143 | Medium | Longest Common Subsequence |
| 518 | Medium | Coin Change II |
| 72 | Medium | Edit Distance |
| 312 | Hard | Burst Balloons |
| 10 | Hard | Regular Expression Matching |

## Common bugs & traps

- **Index shift confusion.** With a padded `(n+1) × (m+1)` table, the i-th character is `text[i - 1]`. Mixing 0-based and 1-based indexing is the dominant bug here.
- **Unset base row/column.** The empty-prefix row and column must be seeded (0, `i`, `j`, or `True`) before the main loop.
- **Wrong iteration order for interval DP.** Loop by *substring length* outward, not by raw `i` then `j` — inner intervals must be solved first.
- **Knapsack capacity direction.** 0/1 knapsack with a rolling array iterates capacity **high → low**; unbounded iterates **low → high**.
- **Out-of-bounds without padding.** `dp[i-1][j-1]` needs the extra row/column, or `i = 0` / `j = 0` crashes.
- **Space optimization clobbering the diagonal.** When collapsing to one row, cache `dp[i-1][j-1]` before you overwrite it.
---

*See also: [Lesson 15 →](../../../learning/15-dp-2d.md) · [🗺 Roadmap](../../../roadmap.md) · [problem lists](../../../../lists/)*
