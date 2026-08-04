# 66. Plus One

**Easy** · [LeetCode](https://leetcode.com/problems/plus-one/) · [Solution file (no hints)](../../problems/0001-0499/66.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Increment a number represented as an array of digits. Why do you only need to keep carrying left while a digit rolls over from 9 to 0?

<details>
<summary>Hint</summary>

Walk from the last digit backward: if it's less than 9, just increment it and stop — no carry needed. If it's 9, it rolls over to 0 and the carry continues into the next digit to the left.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        n = len(digits)

        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            else:
                digits[i] = 0
        return [1] + digits
```

Building blocks: [range-function](../syntax/range-function.md) (reverse step) · [if-return](../syntax/if-return.md) · [list-basics](../syntax/list-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — worst case (all 9s) touches every digit.
**Space: O(1)** extra, or O(n) in the rare all-9s case that returns a new longer list.
</details>

---
