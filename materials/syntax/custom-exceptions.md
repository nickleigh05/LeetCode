# Custom Exceptions

```python
class InvalidInputError(Exception):
    pass

def process(x):
    if x < 0:
        raise InvalidInputError("x must be non-negative")
```

A custom exception is just a class inheriting from `Exception` (usually with an empty body — `pass`) — giving you a specific, descriptive type to `raise` and `except` instead of a generic `Exception` or built-in type. Lets calling code distinguish "your specific error" from unrelated failures.

**Related:** [raising-exceptions](raising-exceptions.md) · [class-basics](class-basics.md) · [inheritance-basics](inheritance-basics.md)
