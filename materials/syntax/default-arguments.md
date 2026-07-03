# Default Arguments

```python
def greet(name, greeting="hello"):
    return f"{greeting}, {name}"

greet("Sam")              # "hello, Sam"
greet("Sam", "hi")        # "hi, Sam"
```

A parameter with `= value` becomes optional — callers can omit it and get the default. Defaults are evaluated **once**, at function definition time, not per call — see [mutable-default-arg-pitfall](mutable-default-arg-pitfall.md) for why that matters with lists/dicts.

**Related:** [function-basics](function-basics.md) · [mutable-default-arg-pitfall](mutable-default-arg-pitfall.md)
