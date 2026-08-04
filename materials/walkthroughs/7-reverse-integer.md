# 7. Reverse Integer

**Medium** · [LeetCode](https://leetcode.com/problems/reverse-integer/)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Solution: not yet solved in this repo.

Reverse the digits of a 32-bit signed integer, returning 0 if it overflows. Why does peeling off digits with `% 10` and `// 10` — the same digit-extraction trick used elsewhere — naturally build the reversed number?

<details>
<summary>Hint</summary>

Repeatedly take the last digit with `x % 10` and remove it with integer division `x // 10` (see [integer division & modulo](../syntax/integer-division-modulo.md)), building the reversed number as `res = res * 10 + digit`. Check the 32-bit signed range before returning.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def reverse(self, x: int) -> int:

        sign = -1 if x < 0 else 1
        x = abs(x)

        result = 0
        while x:
            digit = x % 10
            x //= 10
            result = result * 10 + digit

        result *= sign

        INT_MIN = -2**31
        INT_MAX = 2**31 - 1
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result
```

Building blocks: [integer-division-modulo](../syntax/integer-division-modulo.md) (`%`, `//`) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`abs()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log₁₀ x)** — proportional to the number of digits.
**Space: O(1)** — a few running variables.
</details>
