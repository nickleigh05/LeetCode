# Decorators Basics

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)   # prints "calling add", returns 5
```

`@decorator` above a function definition is shorthand for `add = log_calls(add)` — it wraps the function in another function that runs extra logic before/after the original call. `functools.lru_cache` (a built-in decorator) is the one most relevant here — it auto-memoizes recursive functions.

**Related:** [closures](closures.md) · [args-kwargs](args-kwargs.md) · [recursion-basics](recursion-basics.md)
