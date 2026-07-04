# 17. Math & Geometry — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md)

---

### 48. Rotate Image — Medium
[LeetCode](https://leetcode.com/problems/rotate-image/)  
[Solution file (no hints)](../../problems/0001-0499/48.py)

Rotate an n×n matrix 90° clockwise in place. Why does "transpose, then reverse each row" produce exactly a 90° clockwise rotation?

<details>
<summary>Hint</summary>

Transposing (swap `matrix[i][j]` with `matrix[j][i]`) flips the matrix across its main diagonal; reversing each row afterward flips it left-right — combined, that's precisely a 90° clockwise turn.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:

        n = len(matrix)

        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for row in matrix:
            row.reverse()
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [list-methods](../syntax/list-methods.md) (`.reverse()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — every cell is touched a constant number of times.
**Space: O(1)** — rotated in place, no extra matrix.
</details>

---

### 54. Spiral Matrix — Medium
[LeetCode](https://leetcode.com/problems/spiral-matrix/)  
Solution: not yet solved in this repo.

Return all elements of a matrix in spiral order. Why do four shrinking boundaries (top, bottom, left, right) naturally trace a spiral without needing to track visited cells?

<details>
<summary>Hint</summary>

Maintain `top`, `bottom`, `left`, `right` boundaries. Walk right across the top row, down the right column, left across the bottom row, up the left column — shrinking each boundary after its pass — until they cross.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:

        result = []
        top = 0
        bottom = len(matrix) - 1
        left = 0
        right = len(matrix[0]) - 1

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```

Building blocks: [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) (reverse range) · [list-methods](../syntax/list-methods.md) (`.append()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — every cell is visited exactly once.
**Space: O(1)** extra beyond the output list.
</details>

---

### 73. Set Matrix Zeroes — Medium
[LeetCode](https://leetcode.com/problems/set-matrix-zeroes/)  
Solution: not yet solved in this repo.

If a cell is 0, set its entire row and column to 0 — in O(1) extra space. Why can the matrix's own first row and first column be reused as the "which rows/cols need zeroing" markers?

<details>
<summary>Hint</summary>

Use the first row and first column of the matrix itself as marker flags. Track separately whether the first row/column originally contained a 0 (since they double as markers and would otherwise be overwritten). Two passes: mark, then apply.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:

        rows = len(matrix)
        cols = len(matrix[0])
        first_row_zero = any(matrix[0][col] == 0 for col in range(cols))
        first_col_zero = any(matrix[row][0] == 0 for row in range(rows))

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][col] == 0:
                    matrix[row][0] = 0
                    matrix[0][col] = 0

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][0] == 0 or matrix[0][col] == 0:
                    matrix[row][col] = 0

        if first_row_zero:
            for col in range(cols):
                matrix[0][col] = 0
        if first_col_zero:
            for row in range(rows):
                matrix[row][0] = 0
```

Building blocks: [generator-expressions](../syntax/generator-expressions.md) (`any(... for ...)`) · [for-loop](../syntax/for-loop.md) (nested) · [nested-lists](../syntax/nested-lists.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — a constant number of passes over the matrix.
**Space: O(1)** — the matrix's own first row/column are reused as markers.
</details>

---

### 202. Happy Number — Easy
[LeetCode](https://leetcode.com/problems/happy-number/)  
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

### 66. Plus One — Easy
[LeetCode](https://leetcode.com/problems/plus-one/)  
[Solution file (no hints)](../../problems/0001-0499/66.py)

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

### 50. Pow(x, n) — Medium
[LeetCode](https://leetcode.com/problems/powx-n/)  
[Solution file (no hints)](../../problems/0001-0499/50.py)

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

### 43. Multiply Strings — Medium
[LeetCode](https://leetcode.com/problems/multiply-strings/)  
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

### 2013. Detect Squares — Medium
[LeetCode](https://leetcode.com/problems/detect-squares/)  
Solution: not yet solved in this repo.

Support adding points and counting axis-aligned squares formed with existing points. Why does fixing one diagonal corner and checking for the other diagonal corner (plus the two remaining corners) cover every possible square through a query point?

<details>
<summary>Hint</summary>

Keep a [hashmap](../data-structures/hashmap.md) of point counts. For a query `(x, y)`, look for every existing point `(x, y2)` sharing the same x-coordinate — that gives a candidate side length `y2 - y`. Then check whether the other two corners, `(x + side, y)` and `(x + side, y2)` (and the mirrored `x - side` case), exist too.
</details>

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

class DetectSquares:

    def __init__(self):
        self.point_count = defaultdict(int)

    def add(self, point: List[int]) -> None:
        self.point_count[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0

        for (px, py), cnt in list(self.point_count.items()):
            if px != x or py == y:
                continue

            side = py - y
            for x2 in (x + side, x - side):
                total += cnt * self.point_count[(x2, y)] * self.point_count[(x2, py)]

        return total
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [dict-methods](../syntax/dict-methods.md) (`.items()`) · [tuple-basics](../syntax/tuple-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** per `count` call, where n is the number of distinct points added.
**Space: O(n)** — the hashmap of point counts.
</details>
