# assert

```python
assert condition                       # AssertionError if condition is falsy
assert s.twoSum([2, 7], 9) == [0, 1]   # the one-line unit test
assert node is not None, "hit a null node"   # optional message, shown on failure

def solve(nums):
    assert len(nums) > 0, "empty input reached solve()"   # sanity-check assumption
```

`assert` crashes loudly the moment an assumption is false — which is exactly what you want while practicing: a stack of asserts under `if __name__ == "__main__":` is a free test suite ([testing-locally](../guides/testing-locally.md)). Use it for *checking your own logic*, not for handling user input (that's [raising exceptions](raising-exceptions.md)) — asserts are stripped when Python runs with `-O`, so real programs shouldn't rely on them for control flow. Classic typo alert: `assert (cond, "msg")` — a two-element [tuple](tuple-basics.md) — is always truthy and never fails.

**Related:** [testing-locally (guides)](../guides/testing-locally.md) · [raising-exceptions](raising-exceptions.md) · [truthy-falsy-values](truthy-falsy-values.md)
