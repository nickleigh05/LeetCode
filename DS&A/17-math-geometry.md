# Math & Geometry

## Mathematical Concepts

### 1. Prime Numbers

```
Definition: Number > 1 with no divisors except 1 and itself

First primes: 2, 3, 5, 7, 11, 13, 17, 19, 23...

Properties:
- 2 is the only even prime
- All primes > 3 are of form 6k ± 1

Check if prime:
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True

Only check up to √n:
If n = a × b and a ≤ b, then a ≤ √n

Example: Is 17 prime?
Check divisors up to √17 ≈ 4.1
Test: 2, 3
None divide 17 → Prime ✓

Sieve of Eratosthenes (find all primes ≤ n):
def sieve(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i*i, n + 1, i):
                primes[j] = False

    return [i for i in range(n + 1) if primes[i]]

Visual for n = 20:
2: Mark 4, 6, 8, 10, 12, 14, 16, 18, 20
3: Mark 9, 15
5: Mark 25 (> 20, stop)

Primes: [2, 3, 5, 7, 11, 13, 17, 19]

Time: O(n log log n)
```

### 2. GCD and LCM

```
GCD (Greatest Common Divisor):
Largest number that divides both

Example: GCD(48, 18)
48 = 2^4 × 3
18 = 2 × 3^2
GCD = 2 × 3 = 6

Euclidean Algorithm:
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

Execution for gcd(48, 18):
Step 1: gcd(48, 18)
    48 % 18 = 12
    → gcd(18, 12)

Step 2: gcd(18, 12)
    18 % 12 = 6
    → gcd(12, 6)

Step 3: gcd(12, 6)
    12 % 6 = 0
    → gcd(6, 0)

Result: 6

Visual:
48 = 18 × 2 + 12
18 = 12 × 1 + 6
12 = 6 × 2 + 0

LCM (Least Common Multiple):
Smallest number divisible by both

Formula: LCM(a, b) = (a × b) / GCD(a, b)

Example: LCM(48, 18)
LCM = (48 × 18) / 6 = 144

Time: O(log min(a, b))
```

### 3. Modular Arithmetic

```
Properties:
(a + b) % m = ((a % m) + (b % m)) % m
(a - b) % m = ((a % m) - (b % m) + m) % m
(a × b) % m = ((a % m) × (b % m)) % m

Power with mod:
def pow_mod(base, exp, mod):
    result = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod

    return result

Example: 2^10 % 1000
2^1 = 2
2^2 = 4
2^4 = 16
2^8 = 256

10 = 8 + 2 (binary: 1010)
2^10 = 2^8 × 2^2 = 256 × 4 = 1024
1024 % 1000 = 24

Visual:
exp = 10 (1010 in binary)
      ↓↓
     2^8 × 2^2

Time: O(log exp)
```

### 4. Factorial and Combinations

```
Factorial: n! = n × (n-1) × ... × 1

0! = 1
5! = 5 × 4 × 3 × 2 × 1 = 120

Combinations: C(n, k) = n! / (k! × (n-k)!)

Example: C(5, 2) = 5! / (2! × 3!)
       = 120 / (2 × 6)
       = 10

Visual: Choose 2 from {A,B,C,D,E}
AB, AC, AD, AE
BC, BD, BE
CD, CE
DE

Total: 10 combinations

Optimized calculation:
def combination(n, k):
    if k > n - k:
        k = n - k

    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)

    return result

Time: O(k)
```

### 5. Pascal's Triangle

```
Each number is sum of two above:

        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1
   1 5 10 10 5 1

Row n, position k: C(n, k)

Properties:
- Row n sums to 2^n
- Symmetric: C(n,k) = C(n, n-k)
- C(n,k) = C(n-1,k-1) + C(n-1,k)

Generate:
def generate(numRows):
    triangle = []

    for i in range(numRows):
        row = [1] * (i + 1)

        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]

        triangle.append(row)

    return triangle

Time: O(n²)
```

## Geometry Problems

### 1. Distance and Points

```
Euclidean Distance:
dist = √((x2-x1)² + (y2-y1)²)

Example: Distance from (1,2) to (4,6)
dist = √((4-1)² + (6-2)²)
     = √(9 + 16)
     = √25 = 5

Visual:
    6 •──┐
      │  │4
    2 •──┘
      1  4
        3

Right triangle: legs 3 and 4, hypotenuse 5

Manhattan Distance:
dist = |x2-x1| + |y2-y1|

Example: (1,2) to (4,6)
dist = |4-1| + |6-2| = 3 + 4 = 7

Visual (grid movement):
    • → → → •
    ↑       ↓
    ↑       ↓
    ↑       ↓
    •       ↓

Chebyshev Distance (max of abs differences):
dist = max(|x2-x1|, |y2-y1|)

Example: (1,2) to (4,6)
dist = max(3, 4) = 4
```

### 2. Lines and Slopes

```
Slope: m = (y2 - y1) / (x2 - x1)

Example: Points (1,2) and (4,8)
m = (8-2) / (4-1) = 6/3 = 2

Visual:
    8 •
      │ ╱
      │╱
    2 •
      1   4

Rise over run: 6/3 = 2

Collinear points (on same line):
Points A, B, C are collinear if:
slope(A,B) = slope(B,C)

Or using cross product:
(B.y - A.y) × (C.x - B.x) = (C.y - B.y) × (B.x - A.x)

Line equation: y = mx + b
where b = y - mx (y-intercept)

Perpendicular lines:
m1 × m2 = -1

Parallel lines:
m1 = m2
```

### 3. Rectangles and Areas

```
Rectangle overlap:
rect1 = [x1, y1, x2, y2]
rect2 = [x3, y3, x4, y4]

Overlap if:
x1 < x4 AND x3 < x2 AND
y1 < y4 AND y3 < y2

Visual:
    ┌─────┐
    │  ┌──┼──┐
    │  │  │  │
    └──┼──┘  │
       └─────┘
       overlap

No overlap examples:
    ┌───┐  ┌───┐
    │   │  │   │
    └───┘  └───┘
    separated

    ┌───┐
    └───┘
       ┌───┐
       └───┘
       separated vertically

Area of overlap:
x_overlap = min(x2, x4) - max(x1, x3)
y_overlap = min(y2, y4) - max(y1, y3)
area = max(0, x_overlap) × max(0, y_overlap)
```

### 4. Circles

```
Circle equation: (x-h)² + (y-k)² = r²
Center: (h, k)
Radius: r

Point inside circle:
dist(point, center) ≤ radius

Example:
Circle: center (0,0), radius 5
Point (3,4):
dist = √(3² + 4²) = 5
On circle ✓

Point (2,2):
dist = √(2² + 2²) = √8 ≈ 2.83
Inside circle ✓

Point (4,4):
dist = √(4² + 4²) = √32 ≈ 5.66
Outside circle ✗

Visual:
      •(4,4)
    ○─────○
   ○   •   ○
  ○  (3,4)  ○
  ○         ○
   ○  •(2,2)○
    ○─────○
     (0,0)
```

### 5. Polygons

```
Triangle area:
Given vertices (x1,y1), (x2,y2), (x3,y3)

Area = |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| / 2

Example: (0,0), (4,0), (0,3)
Area = |0(0-3) + 4(3-0) + 0(0-0)| / 2
     = |0 + 12 + 0| / 2
     = 6

Visual:
    3 •
      │╲
      │ ╲
      │  ╲
    0 •───•
      0   4

Base = 4, Height = 3
Area = 4 × 3 / 2 = 6 ✓

Convex Hull:
Smallest convex polygon containing all points

Example points:
    •   •
  •   •   •
    •   •

Convex hull:
    •───•
   ╱     ╲
  •       •
   ╲     ╱
    •───•

Graham Scan:
1. Find lowest point
2. Sort by polar angle
3. Use stack to build hull

Time: O(n log n)
```

### 6. Rotation and Transformation

```
Rotate point (x,y) by angle θ around origin:
x' = x × cos(θ) - y × sin(θ)
y' = x × sin(θ) + y × cos(θ)

90° clockwise: (x,y) → (y,-x)
90° counter-clockwise: (x,y) → (-y,x)
180°: (x,y) → (-x,-y)

Example: Rotate (3,4) by 90° clockwise
(3,4) → (4,-3)

Visual:
    4 •
      │
      │
      │
    0 └───•3
         -3•

Matrix rotation:
Rotate matrix 90° clockwise:
1. Transpose
2. Reverse each row

Original:
1 2 3
4 5 6
7 8 9

Transpose:
1 4 7
2 5 8
3 6 9

Reverse rows:
7 4 1
8 5 2
9 6 3
```

## Common Problem Patterns

### 1. Missing Number

```
nums = [3,0,1]  (missing 2)

Approach 1: Sum formula
Expected sum = n(n+1)/2
Actual sum = sum(nums)
Missing = Expected - Actual

Example:
n = 3, Expected = 3×4/2 = 6
Actual = 3+0+1 = 4
Missing = 6-4 = 2 ✓

Approach 2: XOR
XOR all indices and values
Missing = 0 XOR 1 XOR 2 XOR 3 XOR 3 XOR 0 XOR 1
        = 2

Time: O(n)
Space: O(1)
```

### 2. Pow(x, n)

```
Calculate x^n efficiently

Example: 2^10

Binary: 10 = 1010₂
2^10 = 2^8 × 2^2

Steps:
n=10: even, square base: 2² = 4, n=5
n=5:  odd, result×base: result=4, n=4
n=4:  even, square base: 4² = 16, n=2
n=2:  even, square base: 16² = 256, n=1
n=1:  odd, result×base: result=1024

Visual:
    2^10
     ↓
    (2²)^5
     ↓
    4 × 4^4
        ↓
       (4²)^2
        ↓
       16^2
        ↓
       256 × 256
        = 1024 (wrong, let me recalculate)

Correct:
2^10 = (2^5)² = (32)² = 1024
2^5 = 2 × 2^4 = 2 × 16 = 32
2^4 = (2^2)² = 4² = 16

Time: O(log n)
```

### 3. Happy Number

```
Number is happy if sum of squares of digits
eventually reaches 1

Example: 19
1² + 9² = 82
8² + 2² = 68
6² + 8² = 100
1² + 0² + 0² = 1 ✓ Happy!

Example: 2
2² = 4
4² = 16
1² + 6² = 37
3² + 7² = 58
5² + 8² = 89
8² + 9² = 145
1² + 4² + 5² = 42
4² + 2² = 20
2² + 0² = 4 ← Cycle!

Not happy ✗

Detect cycle with Floyd's algorithm
(slow and fast pointers)

Time: O(log n)
```

## Python Implementation

```python
import math

# Prime check
def is_prime(n):
    """Time: O(√n)"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


# Sieve of Eratosthenes
def sieve_of_eratosthenes(n):
    """Time: O(n log log n)"""
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i*i, n + 1, i):
                primes[j] = False

    return [i for i in range(n + 1) if primes[i]]


# GCD
def gcd(a, b):
    """Time: O(log min(a,b))"""
    while b:
        a, b = b, a % b
    return a


# LCM
def lcm(a, b):
    """Time: O(log min(a,b))"""
    return (a * b) // gcd(a, b)


# Power with modulo
def pow_mod(base, exp, mod):
    """Time: O(log exp)"""
    result = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod

    return result


# Combinations
def combination(n, k):
    """Time: O(k)"""
    if k > n - k:
        k = n - k

    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)

    return result


# Pascal's Triangle
def generate_pascals_triangle(numRows):
    """Time: O(n²)"""
    triangle = []

    for i in range(numRows):
        row = [1] * (i + 1)

        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]

        triangle.append(row)

    return triangle


# Euclidean distance
def euclidean_distance(p1, p2):
    """Time: O(1)"""
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


# Manhattan distance
def manhattan_distance(p1, p2):
    """Time: O(1)"""
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])


# Check if rectangles overlap
def is_rectangle_overlap(rec1, rec2):
    """Time: O(1)"""
    return not (rec1[2] <= rec2[0] or
                rec2[2] <= rec1[0] or
                rec1[3] <= rec2[1] or
                rec2[3] <= rec1[1])


# Rectangle area
def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    """Time: O(1)"""
    area1 = (ax2 - ax1) * (ay2 - ay1)
    area2 = (bx2 - bx1) * (by2 - by1)

    # Overlap
    x_overlap = max(0, min(ax2, bx2) - max(ax1, bx1))
    y_overlap = max(0, min(ay2, by2) - max(ay1, by1))
    overlap = x_overlap * y_overlap

    return area1 + area2 - overlap


# Rotate matrix 90° clockwise
def rotate(matrix):
    """Time: O(n²), in-place"""
    n = len(matrix)

    # Transpose
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i].reverse()


# Missing number
def missing_number(nums):
    """Time: O(n), Space: O(1)"""
    n = len(nums)
    expected = n * (n + 1) // 2
    actual = sum(nums)
    return expected - actual


# Power(x, n)
def my_pow(x, n):
    """Time: O(log n)"""
    if n < 0:
        x = 1 / x
        n = -n

    result = 1
    while n:
        if n % 2:
            result *= x
        x *= x
        n //= 2

    return result


# Happy number
def is_happy(n):
    """Time: O(log n)"""
    def get_next(num):
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1


# Sqrt(x)
def my_sqrt(x):
    """
    Binary search.
    Time: O(log x)
    """
    if x < 2:
        return x

    left, right = 1, x // 2

    while left <= right:
        mid = (left + right) // 2
        square = mid * mid

        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1

    return right


# Angle between clock hands
def angle_clock(hour, minutes):
    """Time: O(1)"""
    # Hour hand: 30° per hour + 0.5° per minute
    hour_angle = (hour % 12) * 30 + minutes * 0.5

    # Minute hand: 6° per minute
    minute_angle = minutes * 6

    # Difference
    diff = abs(hour_angle - minute_angle)

    # Smaller angle
    return min(diff, 360 - diff)
```

## Key Takeaways

1. **Math Fundamentals**:
   - Primes: Check up to √n
   - GCD: Euclidean algorithm
   - Combinations: Optimize calculations
   - Modular arithmetic: Handle large numbers

2. **Geometry Basics**:
   - Distance formulas
   - Line slopes and equations
   - Rectangle overlap
   - Circle containment

3. **Optimization**:
   - Binary exponentiation: O(log n)
   - Sieve for multiple primes
   - Use formulas over iteration

4. **Common Patterns**:
   - XOR for finding unique
   - Sum formulas for missing numbers
   - Fast power with squaring
   - Cycle detection with Floyd's

5. **Edge Cases**:
   - Zero and negative numbers
   - Overflow in multiplication
   - Division by zero
   - Precision in floating point
