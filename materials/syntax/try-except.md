# `try` / `except`

```python
try:
    result = 10 / divisor
except ZeroDivisionError:
    result = 0

try:
    val = d["missing"]
except KeyError:
    val = None
```

Code in `try` runs normally; if it raises an exception matching the `except` type, control jumps there instead of crashing. Rare in day-to-day LeetCode solutions (most problems guarantee valid input), but essential for "design" problems that must handle bad input gracefully, or defensive real-world code.

**Related:** [raising-exceptions](raising-exceptions.md) · [finally-block](finally-block.md) · [custom-exceptions](custom-exceptions.md)
