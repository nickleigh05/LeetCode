# 70. Climbing Stairs

**Easy** · [LeetCode](https://leetcode.com/problems/climbing-stairs/) · [Solution file (no hints)](../../problems/0001-0499/70.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Count the ways to climb n stairs taking 1 or 2 steps at a time. Why does the number of ways to reach step n equal the sum of ways to reach step n-1 and step n-2?

<details>
<summary>Hint</summary>

This is Fibonacci in disguise (see [Dynamic Programming](../algorithms/dynamic-programming.md)): the last move to reach step n was either a 1-step from n-1, or a 2-step from n-2, so `ways(n) = ways(n-1) + ways(n-2)`.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def climbStairs(self, n: int) -> int:

        if n == 1:
            return 1
        if n == 2:
            return 2

        two_back = 1
        one_back = 2

        for i in range(3, n + 1):
            current = one_back + two_back
            two_back = one_back
            one_back = current
        return one_back
```

Building blocks: [if-return](../syntax/if-return.md) · [for-loop](../syntax/for-loop.md) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass building up from the base cases.
**Space: O(1)** — only two running variables (space-optimized from an O(n) DP array).
</details>

---
