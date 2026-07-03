# Closures

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
counter()   # 1
counter()   # 2
```

A closure is an inner function that "remembers" variables from its enclosing function even after that function has returned. `nonlocal` is required to *modify* (not just read) an enclosing variable from inside the inner function. Shows up in memoized recursive helpers and generator-like state machines.

**Related:** [function-basics](function-basics.md) · [recursion-basics](recursion-basics.md) · [decorators-basics](decorators-basics.md)
