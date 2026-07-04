# global & nonlocal

```python
def count_nodes(root):
    count = 0
    def dfs(node):
        nonlocal count        # "count means the one in count_nodes, not a new local"
        if not node:
            return
        count += 1
        dfs(node.left); dfs(node.right)
    dfs(root)
    return count
```

Assigning to a name inside a function makes it **local by default** — so `count += 1` in a nested helper dies with `UnboundLocalError` unless you declare `nonlocal count` (use the enclosing function's variable) or `global count` (use the module-level one). You only need the declaration for **assignment**; *reading* an outer variable, or mutating a mutable one (`seen.add(x)`, `res.append(p)`), works without it — which is why many DFS helpers sidestep the keyword entirely by accumulating into a list. `global` is almost never wanted on LeetCode: module-level state leaks between the judge's test cases.

**Related:** [closures](closures.md) · [recursion-basics](recursion-basics.md) · [scope-legb](scope-legb.md) · [common-python-errors (guides)](../guides/common-python-errors.md)
