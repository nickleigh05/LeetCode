# 50. Pow(x, n)

**Medium** · [LeetCode](https://leetcode.com/problems/powx-n/) · [Solution file (no hints)](../../problems/0001-0499/50.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Compute `x^n` in better than O(n) time. Why does `x^n = (x^(n/2))^2` (adjusted for odd n) cut the work in half at every step?

<details>
<summary>Hint</summary>

This is [fast exponentiation](../algorithms/fast-exponentiation.md): recursively (or iteratively) square the base and halve the exponent, multiplying in an extra factor of `x` whenever the exponent is odd.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:

        if n == 0:
            return 1
        if n < 0:
            x, n = 1 / x, -n

        if n % 2 == 0:
            return self.myPow(x * x, n // 2)
        else:
            return x * self.myPow(x * x, n // 2)
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`%`, `//`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** — the exponent halves at each recursive step.
**Space: O(log n)** — recursion stack depth.
</details>

---
