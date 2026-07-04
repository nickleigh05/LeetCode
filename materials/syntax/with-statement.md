# with Statement (Context Managers)

```python
with open("input.txt") as f:        # file is guaranteed closed after the block,
    data = f.read()                  # even if an exception happens inside

with open("out.txt", "w") as f:
    f.write("results\n")

lines = open("input.txt").read().splitlines()   # you'll see this too — works,
                                                # but nothing guarantees the close
```

`with` acquires a resource, runs the block, and **always releases it on exit** — success, `return`, or crash. It's `try/finally` ([finally-block](finally-block.md)) with the cleanup pre-written by the object itself (anything implementing `__enter__`/`__exit__` — files, locks, database connections). Never needed for LeetCode's function-only format, but it *is* the correct way to read input files for Advent of Code and scripts, and interviewers notice bare `open()` calls.

**Related:** [finally-block](finally-block.md) · [try-except](try-except.md) · [competitive-programming-io (guides)](../guides/competitive-programming-io.md)
