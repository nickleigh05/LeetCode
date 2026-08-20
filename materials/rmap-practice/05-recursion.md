# 05. Recursion — Practice

Unit 05 has no LeetCode problems. It's a **skills gate**: five drills you write from scratch, in your own editor, before Trees. Nothing downstream — trees, backtracking, DP — works until these are automatic.

[← Back to the lesson](../learning/05-recursion.md) · [🗺 Roadmap](../../roadmap.md)

---

## The five drills

**1 · Write these from scratch, no reference, no editor autocomplete.**

| Function | Base case | Recursive case |
|----------|-----------|----------------|
| `factorial(n)` | `n <= 1 → 1` | `n * factorial(n-1)` |
| `sum_of_list(xs)` | empty → `0` | `xs[0] + sum_of_list(xs[1:])` |
| `count_digits(n)` | `n < 10 → 1` | `1 + count_digits(n // 10)` |
| `power(base, n)` | `n == 0 → 1` | `base * power(base, n-1)` |
| `fibonacci(n)` (naïve) | `n < 2 → n` | `fib(n-1) + fib(n-2)` |

Do them again a day later with the table covered. The table is the answer key, not the exercise.

**2 · Trace a call stack by hand.** Take `count_digits(4071)`. On paper, write every frame as it's pushed, then every value as it's returned. *Predict the output before you run it.* If your prediction was wrong, that's the drill working — find out where.

**3 · Draw the recursion tree for `fibonacci(5)`.** Count the nodes. Derive the Big-O from the shape of the tree, not from memory. This is the single picture that makes [DP](../learning/14-dp-1d.md) make sense later.

**4 · Memoize it.** Add a `dict` cache to naïve `fibonacci`, then time `fib(35)` both ways. Watch seconds become microseconds. You have now written your first dynamic programming solution — that's all DP is.

**5 · State the space cost of each function you wrote.** Call-stack depth *is* extra memory. `sum_of_list` on a 10,000-element list is O(n) space and will hit Python's recursion limit — know why, and know [what the limit is](../syntax/recursion-limit.md).

---

## The gate

Don't start [Unit 08 · Trees](../learning/08-trees.md) until every box in the lesson's [Check Yourself](../learning/05-recursion.md#check-yourself) is ticked — honestly. Every tree problem is *base case → recurse → combine*, and most people who stall out in DP six units later are actually stalled on this page.

**Syntax reference:** [recursion basics](../syntax/recursion-basics.md) · [recursion limit](../syntax/recursion-limit.md) · [functools cache](../syntax/functools-cache.md)

---

Want to see recursion applied? It shows up next in [Binary Search](06-binary-search.md), then everywhere from [Trees](08-trees.md) onward.
