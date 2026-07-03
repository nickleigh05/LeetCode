# Raising Exceptions

```python
def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b
```

`raise` manually triggers an exception, immediately halting normal execution and propagating up to the nearest matching `except` (or crashing the program if none exists). Use it to fail loudly on invalid input rather than silently returning a wrong value.

**Related:** [try-except](try-except.md) · [custom-exceptions](custom-exceptions.md)
