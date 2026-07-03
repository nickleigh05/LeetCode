# `while` Loop

```python
i = 0
while i < len(nums):
    print(nums[i])
    i += 1
```

Repeats the block as long as the condition stays truthy — you control the exit condition manually, unlike `for` which exhausts an iterable. Used whenever the number of iterations isn't known up front (two-pointer convergence, binary search, BFS/DFS with an explicit stack/queue).

**Related:** [for-loop](for-loop.md) · [break-continue](break-continue.md) · [walrus-operator](walrus-operator.md)
