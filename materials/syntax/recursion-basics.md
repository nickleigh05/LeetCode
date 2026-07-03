# Recursion Basics

```python
def factorial(n):
    if n <= 1:          # base case — stops the recursion
        return 1
    return n * factorial(n - 1)   # recursive case — calls itself on a smaller input
```

Every recursive function needs a **base case** (the condition that stops it) and a **recursive case** (where it calls itself on a smaller/simpler input, making progress toward the base case). Python's default recursion limit is ~1000 calls deep — deep recursion on large inputs can hit `RecursionError`.

**Related:** [function-basics](function-basics.md) · [closures](closures.md)
