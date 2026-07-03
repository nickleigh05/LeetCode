# Instance vs. Class Attributes

```python
class Counter:
    total_created = 0        # class attribute — shared by every instance

    def __init__(self):
        Counter.total_created += 1
        self.count = 0        # instance attribute — unique per object

a = Counter()
b = Counter()
a.count = 5
b.count            # 0 — a's change didn't affect b
Counter.total_created   # 2 — shared across both
```

Attributes set with `self.x = ...` inside methods belong to that one instance. Attributes defined directly in the class body are shared by all instances unless a specific instance overrides them.

**Related:** [class-basics](class-basics.md) · [init-method](init-method.md)
