# 1-D Dynamic Programming

*Break the problem into overlapping subproblems. Define the state, write the recurrence, nail the base case — in that order. The rest is bookkeeping.*

## Recognize this pattern when...

- The ask is **"number of ways"**, **"min / max cost or length"**, or **"can you reach / make X?"**
- You make a **decision at each step** (take it or skip it) and want the optimal sequence of decisions.
- A naive recursion **recomputes the same subproblem** over and over (Fibonacci-shaped).
- The answer for position `i` depends only on a **constant number of earlier positions**.
- Brute-force enumeration is exponential but the number of distinct *states* is linear.

## Variations

1. **Fibonacci-style rolling** — `dp[i]` from the last one or two; collapse to O(1) variables. *(Climbing Stairs, N-th Tribonacci)*
2. **Take / skip decision** — `dp[i] = max(skip, take + dp[i-2])`. *(House Robber, Delete and Earn)*
3. **Unbounded "make a target"** — coin/word reuse; iterate amounts outward. *(Coin Change, Word Break)*
4. **Longest subsequence** — `dp[i]` = best ending at `i`; O(n²), or O(n log n) with patience sorting. *(Longest Increasing Subsequence)*
5. **Running optimum (Kadane)** — extend or restart at each element. *(Maximum Subarray, Maximum Product Subarray)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 70 | Easy | [Climbing Stairs](../../../../problems/0001-0499/70.py) |
| 746 | Easy | Min Cost Climbing Stairs |
| 198 | Medium | House Robber |
| 322 | Medium | Coin Change |
| 300 | Medium | Longest Increasing Subsequence |
| 139 | Medium | Word Break |

## Common bugs & traps

- **Fuzzy state definition.** If you can't say what `dp[i]` *means* in one sentence, the recurrence will be wrong. This is the root cause of most DP bugs.
- **Missing or off-by-one base case.** `dp[0]` (and sometimes `dp[1]`) must be set before the loop, and the loop must start past them.
- **Wrong iteration order.** Every state a transition reads must already be filled — for 1-D that's almost always left-to-right.
- **Reachability vs. value.** For Coin Change, initialize with `inf` and treat "still `inf`" as "impossible", returning `-1`.
- **Over-eager space optimization.** When collapsing to rolling variables, update them in an order that doesn't clobber a value you still need.
- **Reading the wrong cell as the answer.** `dp[-1]`, `max(dp)`, and `dp[0]` are all common finals — match it to your state definition.
---

*See also: [Lesson 14 →](../../../learning/14-dp-1d.md) · [🗺 Roadmap](../../../../roadmap.md) · [problem lists](../../../../lists/)*
