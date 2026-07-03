# Dunder Methods

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"    # what print(p) / repr(p) shows

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y   # what == uses

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)       # what < / sorted() uses

    def __hash__(self):
        return hash((self.x, self.y))                        # required to use in a set/dict key
```

"Dunder" = double underscore. These are hooks Python calls automatically for built-in operations — `__repr__` for printing, `__eq__` for `==`, `__lt__` for `<`/`sorted()`, `__hash__` to be usable as a set element or dict key. Define them when you need custom objects to behave correctly in comparisons or hash-based collections.

**Related:** [class-basics](class-basics.md) · [comparison-operators](comparison-operators.md) · [sorting-key](sorting-key.md)
