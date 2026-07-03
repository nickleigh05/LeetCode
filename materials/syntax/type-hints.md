# Type Hints

```python
def add(a: int, b: int) -> int:
    return a + b

def find(nums: list[int], target: int) -> int | None:
    ...
```

Type hints (`: type` on parameters, `-> type` on the return) document expected types — Python does **not** enforce them at runtime, they're purely for readers and static-analysis tools (mypy). LeetCode function signatures are usually pre-typed this way; matching that style signals intentional, interview-ready code.

**Related:** [function-basics](function-basics.md) · [none-type](none-type.md)
