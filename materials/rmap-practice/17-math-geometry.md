# 17. Math & Geometry — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

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
n = len(matrix)

for i in range(n):                        # transpose: swap across the diagonal
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

for row in matrix:                        # reverse each row left-right
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
res = []
top, bottom = 0, len(matrix) - 1
left, right = 0, len(matrix[0]) - 1

while top <= bottom and left <= right:      # while loop, boundaries haven't crossed
    for c in range(left, right + 1):           # across the top row
        res.append(matrix[top][c])
    top += 1

    for r in range(top, bottom + 1):           # down the right column
        res.append(matrix[r][right])
    right -= 1

    if top <= bottom:                           # across the bottom row (if it still exists)
        for c in range(right, left - 1, -1):
            res.append(matrix[bottom][c])
        bottom -= 1

    if left <= right:                           # up the left column (if it still exists)
        for r in range(bottom, top - 1, -1):
            res.append(matrix[r][left])
        left += 1

return res
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
rows, cols = len(matrix), len(matrix[0])
first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
first_col_zero = any(matrix[r][0] == 0 for r in range(rows))

for r in range(1, rows):                   # mark using the first row/col as flags
    for c in range(1, cols):
        if matrix[r][c] == 0:
            matrix[r][0] = 0
            matrix[0][c] = 0

for r in range(1, rows):                   # apply the marks (skip the first row/col for now)
    for c in range(1, cols):
        if matrix[r][0] == 0 or matrix[0][c] == 0:
            matrix[r][c] = 0

if first_row_zero:                          # handle the first row/col last
    for c in range(cols):
        matrix[0][c] = 0
if first_col_zero:
    for r in range(rows):
        matrix[r][0] = 0
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
def next_number(n):
    total = 0
    while n:                              # sum of squares of the digits
        digit = n % 10
        total += digit * digit
        n //= 10
    return total

seen = set()
while n != 1 and n not in seen:            # while loop until we hit 1 or repeat
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
for i in range(len(digits) - 1, -1, -1):    # for loop right to left
    if digits[i] < 9:                          # no carry needed, done
        digits[i] += 1
        return digits
    digits[i] = 0                              # rolls over, carry continues left

return [1] + digits                        # every digit was 9: e.g. 999 -> 1000
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
def helper(x, n):
    if n == 0:                            # base case: anything^0 = 1
        return 1
    if n % 2 == 1:                          # odd exponent: peel off one factor of x
        return x * helper(x, n - 1)
    half = helper(x, n // 2)                 # even exponent: square the half-power
    return half * half

if n < 0:                                # negative exponent: invert x and use positive n
    x = 1 / x
    n = -n

return helper(x, n)
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
if num1 == "0" or num2 == "0":
    return "0"

m, n = len(num1), len(num2)
result = [0] * (m + n)

for i in range(m - 1, -1, -1):              # for loop over digits of num1, right to left
    for j in range(n - 1, -1, -1):             # for loop over digits of num2, right to left
        digit_product = int(num1[i]) * int(num2[j])
        pos_low, pos_high = i + j + 1, i + j     # this product lands across two positions

        total = digit_product + result[pos_low]
        result[pos_low] = total % 10
        result[pos_high] += total // 10           # carry into the higher position

res_str = "".join(map(str, result)).lstrip("0")
return res_str
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
        self.point_count = defaultdict(int)    # (x, y) -> occurrences

    def add(self, point):
        self.point_count[tuple(point)] += 1

    def count(self, point):
        x, y = point
        total = 0

        for (px, py), cnt in list(self.point_count.items()):   # for loop over existing points
            if px != x or py == y:                          # need same x, different y
                continue
            side = py - y

            for x2 in (x + side, x - side):                  # try both square directions
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
