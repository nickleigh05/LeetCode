# `yield` / Generator Functions

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i        # pauses here, resumes on next() call
        i += 1

for num in count_up_to(3):
    print(num)          # 1, 2, 3
```

A function containing `yield` becomes a **generator function** — calling it doesn't run the body immediately, it returns an iterator that runs the code up to the next `yield` each time you ask for a value. Useful for producing a (possibly infinite) sequence without holding it all in memory at once.

**Related:** [generator-expressions](generator-expressions.md) · [for-loop](for-loop.md) · [recursion-basics](recursion-basics.md)
