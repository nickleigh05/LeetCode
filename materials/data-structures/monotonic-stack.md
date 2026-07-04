# Monotonic Stack

```python
# next greater element to the right, for every index — one pass
res = [-1] * len(nums)
stack = []                          # holds indices; values strictly decreasing
for i, n in enumerate(nums):
    while stack and nums[stack[-1]] < n:   # n is the "next greater" for these
        res[stack.pop()] = n
    stack.append(i)
```

A [stack](stack.md) kept sorted by construction: before pushing, pop everything that would break the ordering — and each pop is exactly the moment you've *found the answer* for that popped element. This turns "for each element, find the next greater/smaller one" from O(n²) rescanning into O(n) total, because every index is pushed once and popped at most once. Decreasing stack → next **greater** questions (Daily Temperatures, Next Greater Element); increasing stack → next **smaller** (Largest Rectangle in Histogram). The deque-based variant (popping from both ends) gives sliding-window maximum.

**Complexity:** O(n) total across the whole pass — amortized O(1) per element · O(n) space.

**Related:** [stack](stack.md) · [deque](deque.md) · [Stack lesson](../learning/04-stack.md) · [stack template](../appendix/templates/stack/README.md)
