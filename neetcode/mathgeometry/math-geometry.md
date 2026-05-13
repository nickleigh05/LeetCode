# Math & Geometry

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds number theory (GCD, fast exponentiation), big-number arithmetic, and design problems. NeetCode 250 fills in base-conversion, index manipulation, and string-to-integer mapping. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table. For each new problem, identify the mathematical property being exploited (modular arithmetic, base conversion, cycle detection) before writing any code.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 48 | Medium | Rotate Image | [Link](https://leetcode.com/problems/rotate-image/) | ☐ |
| 54 | Medium | Spiral Matrix | [Link](https://leetcode.com/problems/spiral-matrix/) | ☐ |
| 73 | Medium | Set Matrix Zeroes | [Link](https://leetcode.com/problems/set-matrix-zeroes/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 202 | Easy | Happy Number | [Link](https://leetcode.com/problems/happy-number/) | ☐ |
| 66 | Easy | Plus One | [Link](https://leetcode.com/problems/plus-one/) | ☐ |
| 50 | Medium | Pow(x, n) | [Link](https://leetcode.com/problems/powx-n/) | ☐ |
| 43 | Medium | Multiply Strings | [Link](https://leetcode.com/problems/multiply-strings/) | ☐ |
| 2013 | Medium | Detect Squares | [Link](https://leetcode.com/problems/detect-squares/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 168 | Easy | Excel Sheet Column Title | [Link](https://leetcode.com/problems/excel-sheet-column-title/) | ☐ | Base-26 encoding |
| 1071 | Easy | Greatest Common Divisor of Strings | [Link](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | ☐ | GCD on lengths |
| 2807 | Medium | Insert GCDs in Linked List | [Link](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/) | ☐ | Math + linked list |
| 867 | Easy | Transpose Matrix | [Link](https://leetcode.com/problems/transpose-matrix/) | ☐ | Index swap |
| 13 | Easy | Roman to Integer | [Link](https://leetcode.com/problems/roman-to-integer/) | ☐ | String/map lookup |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| Matrix transpose (in-place) | O(n²) | O(1) | Swap (i,j) ↔ (j,i) for i < j |
| Matrix 90° rotation (in-place) | O(n²) | O(1) | Transpose then reverse each row |
| Spiral traversal | O(m·n) | O(1) | Shrink 4 boundaries per layer |
| Set Matrix Zeroes (in-place) | O(m·n) | O(1) | Use first row/col as markers |
| Fast exponentiation (Pow) | O(log n) | O(log n) | Recursive; O(1) iterative version |
| GCD (Euclidean) | O(log min(a,b)) | O(1) | math.gcd in Python |
| Happy Number (cycle detect) | O(log n) | O(log n) | Set or Floyd's tortoise/hare |
| Multiply Strings | O(m·n) | O(m+n) | Grade-school multiplication |
| Base-26 conversion | O(log n) | O(log n) | Repeated mod + subtract 1 |

---

## Data Structures

### 2-D Matrix (In-place Manipulation)

A matrix is stored as a list of rows in Python. In-place manipulation means modifying the matrix using only the values already in it — no extra copy allowed. The key insight for rotations: a 90° clockwise rotation = transpose + reverse each row.

```
Original 3×3:        After Transpose:      After Reverse Rows:
  1  2  3              1  4  7               7  4  1
  4  5  6    →→→       2  5  8     →→→       8  5  2
  7  8  9              3  6  9               9  6  3

Transpose: swap matrix[i][j] with matrix[j][i] for all i < j
           i.e., (row, col) becomes (col, row)

Reverse each row: matrix[i] = matrix[i][::-1]
```

**When it matters:** Rotate Image (#48), Transpose Matrix (#867). For Set Matrix Zeroes, use the first row and first column as a "marker" array to avoid O(m+n) extra space.

### Spiral Traversal Boundaries

Track four boundary variables: `top`, `bottom`, `left`, `right`. Each full "layer" of the spiral consumes all four sides and shrinks all four boundaries by one step inward.

```
Matrix:                     Traversal order:
  1   2   3   4             → right along top    (1,2,3,4)
  5   6   7   8             ↓ down along right   (8,12)
  9  10  11  12             ← left along bottom  (11,10,9)
 13  14  15  16             ↑ up along left      (5)
                            then repeat for inner layer:
top=1, bot=2, l=1, r=2     → (6,7), ↓ (11), ← (10), ↑ — ends

Boundaries shrink:
  top +=1  after going right
  right-=1 after going down
  bottom-=1 after going left
  left +=1  after going up
```

**When it matters:** Spiral Matrix (#54). Always check `top <= bottom` and `left <= right` before each of the four sweeps — the inner layers may be a single row or column.

---

## Core Patterns

### In-place Matrix Transformation (Rotate / Transpose)
**When to use:** Rotate a square matrix 90° in-place with O(1) extra space. Transpose swaps rows and columns; reversing rows (or columns) completes the rotation.
**Complexity:** O(n²) time, O(1) space
**Problems:** Rotate Image (#48), Transpose Matrix (#867)
**Common mistake:** Transposing the full matrix (including the diagonal) — only swap pairs where `i < j` to avoid double-swapping back to the original.

```python
n = len(matrix)
# Step 1: transpose (swap across the main diagonal)
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
# Step 2: reverse each row (completes 90° clockwise rotation)
for row in matrix:
    row.reverse()
```

### Spiral Traversal
**When to use:** Visit every element of a matrix in spiral order (clockwise from the outside in).
**Complexity:** O(m·n) time, O(1) extra space (output list doesn't count)
**Problems:** Spiral Matrix (#54)
**Common mistake:** Not checking boundaries between the four sweeps of each layer — when the matrix has an odd dimension, the middle row or column is a degenerate case.

```python
top, bottom, left, right = 0, len(matrix)-1, 0, len(matrix[0])-1
result = []
while top <= bottom and left <= right:
    for col in range(left, right + 1):   result.append(matrix[top][col])
    top += 1
    for row in range(top, bottom + 1):   result.append(matrix[row][right])
    right -= 1
    if top <= bottom:
        for col in range(right, left-1, -1): result.append(matrix[bottom][col])
        bottom -= 1
    if left <= right:
        for row in range(bottom, top-1, -1): result.append(matrix[row][left])
        left += 1
return result
```

### Fast Exponentiation (Pow)
**When to use:** Compute x^n in O(log n) by squaring: x^n = (x²)^(n//2) when n is even, x · x^(n-1) when n is odd.
**Complexity:** O(log n) time, O(log n) space (recursive); O(log n) time, O(1) space (iterative)
**Problems:** Pow(x, n) (#50)
**Common mistake:** Not handling negative exponents — `x^(-n) = 1 / x^n`. Also watch for n = INT_MIN when negating.

```python
def myPow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1
    while n:
        if n % 2 == 1:
            result *= x
        x *= x
        n //= 2
    return result
```

### Cycle Detection for Math (Happy Number)
**When to use:** A mathematical process either terminates at a target value or enters a cycle. Use a seen set or Floyd's algorithm to detect the cycle.
**Complexity:** O(log n) per step, O(log n) space (seen set)
**Problems:** Happy Number (#202)
**Common mistake:** Not knowing when to stop — without a cycle check, the loop runs forever on non-happy numbers.

```python
def is_happy(n):
    def digit_square_sum(x):
        total = 0
        while x:
            total += (x % 10) ** 2
            x //= 10
        return total
    seen = set()
    while n != 1:
        n = digit_square_sum(n)
        if n in seen:
            return False
        seen.add(n)
    return True
```

### GCD (Euclidean Algorithm)
**When to use:** Find the greatest common divisor of two numbers. Basis for fraction problems, string repetition checks, and LCM computation.
**Complexity:** O(log min(a, b)) time, O(1) space
**Problems:** Greatest Common Divisor of Strings (#1071), Insert GCDs in Linked List (#2807)
**Common mistake:** Implementing it manually when `math.gcd` is available in Python. Also, `gcd(a, 0) = a` — don't forget the base case.

```python
import math
math.gcd(a, b)          # built-in — handles 0 correctly

# Manual (for reference):
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
# gcd of strings: if s+t == t+s, gcd is s[:gcd(len(s), len(t))]
```

---

## Syntax Reference

### Matrix Initialization and Access

```python
m, n = len(matrix), len(matrix[0])
matrix[i][j]             # row i, column j
matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]  # swap (transpose)

# Transpose a non-square matrix (creates new matrix):
transposed = list(zip(*matrix))            # returns list of tuples
transposed = [list(row) for row in zip(*matrix)]  # list of lists

# Reverse each row in-place:
for row in matrix:
    row.reverse()         # in-place
# or: matrix[i] = matrix[i][::-1]  (creates new row)
```

### Set Matrix Zeroes (In-place Markers)

```python
# Use first row and first column as flag arrays — O(1) extra space
first_row_zero = any(matrix[0][j] == 0 for j in range(n))
first_col_zero = any(matrix[i][0] == 0 for i in range(m))

for i in range(1, m):      # mark zeros using first row/col
    for j in range(1, n):
        if matrix[i][j] == 0:
            matrix[i][0] = 0
            matrix[0][j] = 0

for i in range(1, m):      # zero out cells based on markers
    for j in range(1, n):
        if matrix[i][0] == 0 or matrix[0][j] == 0:
            matrix[i][j] = 0

if first_row_zero:
    for j in range(n): matrix[0][j] = 0
if first_col_zero:
    for i in range(m): matrix[i][0] = 0
```

### Base-26 Conversion (Excel Column Title)

```python
result = ""
while n > 0:
    n -= 1              # shift to 0-indexed (A=0, B=1, ..., Z=25)
    result = chr(ord('A') + n % 26) + result
    n //= 26
return result
# Key insight: subtract 1 before each mod because there's no "0" digit in base-26
```

### Multiply Strings (Big Integer Multiplication)

```python
m, n = len(num1), len(num2)
pos = [0] * (m + n)
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
        p1, p2 = i + j, i + j + 1
        total = mul + pos[p2]
        pos[p2] = total % 10
        pos[p1] += total // 10
result = ''.join(str(d) for d in pos).lstrip('0')
return result or '0'
```

### Roman to Integer

```python
roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
result = 0
for i in range(len(s)):
    if i + 1 < len(s) and roman[s[i]] < roman[s[i+1]]:
        result -= roman[s[i]]   # subtractive notation (IV, IX, etc.)
    else:
        result += roman[s[i]]
return result
```

### math Module Essentials

```python
import math
math.gcd(a, b)          # greatest common divisor
math.lcm(a, b)          # least common multiple (Python 3.9+)
math.isqrt(n)           # integer square root, floor(sqrt(n))
math.sqrt(n)            # float square root
math.log(n, base)       # log base
math.inf                # positive infinity
math.ceil(x)            # ceiling
math.floor(x)           # floor
```
