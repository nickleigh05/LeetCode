# 202. Happy Number

**Easy** · [LeetCode](https://leetcode.com/problems/happy-number/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Solution: not yet solved in this repo.

Repeatedly replace a number with the sum of the squares of its digits; determine if it reaches 1. Why does this process either reach 1 or fall into a cycle — never grow unboundedly — and how does that make it a cycle-detection problem?

<details>
<summary>Hint</summary>

Track seen values in a [hashset](../data-structures/hashset.md); if you see a repeat before hitting 1, it's a cycle (not happy). Equivalently, use Floyd's cycle detection (fast/slow pointers) like [141](../rmap-practice/06-linked-list.md#141-linked-list-cycle--easy) with no extra space.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isHappy(self, n: int) -> bool:

        def next_number(num):
            total = 0
            while num:
                digit = num % 10
                total += digit * digit
                num //= 10
            return total

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = next_number(n)

        return n == 1
```

Building blocks: [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`%`, `//`) · [set-basics](../syntax/set-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** per iteration to sum digits; the number of iterations before repeating is bounded by a small constant in practice.
**Space: O(k)** — k is the number of distinct values seen before a cycle or reaching 1.
</details>

---
