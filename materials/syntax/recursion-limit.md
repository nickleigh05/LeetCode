# sys.setrecursionlimit

```python
import sys
sys.setrecursionlimit(200_000)     # first line of the solution, before recursing

def dfs(node):                     # now safe on a 10^5-node degenerate tree
    ...
```

Python caps the call stack at ~1000 frames by default, so a legitimately deep recursion — DFS over a 10⁵-node linked-list-shaped tree or path-shaped graph — dies with `RecursionError` even though the *logic* is fine. Raising the limit to comfortably above the max input (constraints + slack, e.g. `2 * 10**5`) fixes it. Two honesty checks first: if the recursion is infinite (missing [base case](recursion-basics.md)), raising the limit just delays the crash; and each frame costs real memory, so for extreme depths the robust fix is rewriting with an explicit [stack](../data-structures/stack.md). LeetCode sometimes pre-raises the limit for you — other judges don't, so keep this line in your [competitive-programming](../guides/competitive-programming-io.md) template.

**Related:** [recursion-basics](recursion-basics.md) · [Recursion lesson](../learning/04b-recursion.md) · [common-python-errors (guides)](../guides/common-python-errors.md) · [import-basics](import-basics.md)
