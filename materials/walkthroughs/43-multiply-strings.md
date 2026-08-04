# 43. Multiply Strings

**Medium** · [LeetCode](https://leetcode.com/problems/multiply-strings/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Solution: not yet solved in this repo.

Multiply two numbers given as strings, without converting the whole thing to native ints. Why does multiplying digit `i` of one number by digit `j` of the other always land in result positions `i+j` and `i+j+1`?

<details>
<summary>Hint</summary>

Do grade-school long multiplication: for every pair of digits `(i, j)`, their product contributes to result index `i + j + 1` (with any carry going to `i + j`). Accumulate into a result array sized `len(num1) + len(num2)`, then strip leading zeros.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:

        if num1 == "0" or num2 == "0":
            return "0"

        m = len(num1)
        n = len(num2)
        result = [0] * (m + n)

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                digit_product = int(num1[i]) * int(num2[j])
                pos_low = i + j + 1
                pos_high = i + j

                total = digit_product + result[pos_low]
                result[pos_low] = total % 10
                result[pos_high] += total // 10

        return "".join(map(str, result)).lstrip("0")
```

Building blocks: [for-loop](../syntax/for-loop.md) (nested, reverse range) · [type-conversion](../syntax/type-conversion.md) (`int()`, `str()`) · [string-methods](../syntax/string-methods.md) (`.lstrip()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every pair of digits is multiplied once.
**Space: O(m + n)** — the result array.
</details>

---
