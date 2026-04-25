# Math & Geometry

## 17. Math & Geometry (8 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 48 | Medium | Rotate Image | [Link](https://leetcode.com/problems/rotate-image/) |
| 54 | Medium | Spiral Matrix | [Link](https://leetcode.com/problems/spiral-matrix/) |
| 73 | Medium | Set Matrix Zeroes | [Link](https://leetcode.com/problems/set-matrix-zeroes/) |
| 202 | Easy | Happy Number | [Link](https://leetcode.com/problems/happy-number/) |
| 66 | Easy | Plus One | [Link](https://leetcode.com/problems/plus-one/) |
| 50 | Medium | Pow(x, n) | [Link](https://leetcode.com/problems/powx-n/) |
| 43 | Medium | Multiply Strings | [Link](https://leetcode.com/problems/multiply-strings/) |
| 2013 | Medium | Detect Squares | [Link](https://leetcode.com/problems/detect-squares/) |

---

## Data Structures

### 2D Matrix (List of Lists)
The grid itself is the main structure. Most operations are done in-place by careful index manipulation. Understanding how indices transform under rotation, spiral traversal, or zeroing is the key skill.

### Hash Map / Hash Set
Used to detect cycles (Happy Number), count point frequencies (Detect Squares), or track which rows/cols need to be zeroed without a second pass (Set Matrix Zeroes).

---

## Core Patterns

### In-Place Matrix Rotation (90 degrees clockwise)
Two steps: (1) Transpose the matrix — swap `matrix[i][j]` with `matrix[j][i]`. (2) Reverse each row. No extra space needed. Used in Rotate Image.

### Spiral Traversal
Maintain four boundaries: `top`, `bottom`, `left`, `right`. Traverse right along top, down along right, left along bottom, up along left. Shrink the boundaries after each pass. Stop when `top > bottom` or `left > right`. Used in Spiral Matrix.

### Mark Using Existing Structure (Set Matrix Zeroes)
To avoid using extra space, use the first row and first column of the matrix as markers — record which rows/cols should be zeroed there. Process in the right order (fill matrix last so markers aren't overwritten).

### Cycle Detection (Happy Number)
Repeatedly apply the digit-square-sum operation. If you reach 1, it's happy. If you reach a number you've seen before, it cycles and is not happy. Use a seen set or fast/slow pointers (Floyd's cycle detection).

### Fast Exponentiation (Pow)
`x^n` = `(x^(n/2))^2`. Recursively halve the exponent — O(log n) multiplications instead of O(n). Handle negative exponents with `1 / pow(x, -n)`. Handle even/odd exponent separately.

### Grade-School Multiplication (Multiply Strings)
Use an array of length `m + n` to accumulate partial products. For each digit pair `(i, j)`, the product contributes to positions `i + j` and `i + j + 1`. Process carries at the end.

### Point Counting + Geometry (Detect Squares)
Store point frequencies in a hash map. To form a square with a query point as one corner, find all points sharing the same x-coordinate (vertical edge candidates), then check if the two completing points exist using the frequency map.
