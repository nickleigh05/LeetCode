# Bit Manipulation

## Binary Representation

### Understanding Binary

```
Decimal to Binary conversion:
13 (decimal) = 1101 (binary)

Position:    3  2  1  0
Power of 2:  8  4  2  1
Binary:      1  1  0  1
Value:       8+ 4+ 0+ 1 = 13

Visual:
    1  1  0  1
    ↓  ↓  ↓  ↓
    8  4  0  1  = 13

Bit numbering (right to left, 0-indexed):
    Bit 3  Bit 2  Bit 1  Bit 0
      1      1      0      1

8-bit representation:
0000 1101 = 13

Signed integers (two's complement):
- Positive: same as unsigned
- Negative: flip bits and add 1

Example: -5 in 8-bit
5:  0000 0101
~5: 1111 1010 (flip)
+1: 1111 1011 (-5)

Visual:
    0000 0101  (5)
    ↓ flip all bits
    1111 1010
    ↓ add 1
    1111 1011  (-5)
```

## Bitwise Operators

### 1. AND (&)

```
Both bits must be 1:
    1 & 1 = 1
    1 & 0 = 0
    0 & 1 = 0
    0 & 0 = 0

Example: 13 & 7
    1101  (13)
  & 0111  (7)
    ----
    0101  (5)

Visual:
    Bit 3  Bit 2  Bit 1  Bit 0
13:   1      1      0      1
 7:   0      1      1      1
AND:  0      1      0      1  = 5

Common uses:
- Check if bit is set: num & (1 << i)
- Clear bit: num & ~(1 << i)
- Get last n bits: num & ((1 << n) - 1)
- Check even/odd: num & 1 (0=even, 1=odd)

Examples:
Is bit 2 of 13 set?
13 & (1 << 2) = 1101 & 0100 = 0100 ≠ 0 ✓ Yes

Is 13 even?
13 & 1 = 1 ✗ Odd

Get last 3 bits of 13:
13 & ((1 << 3) - 1) = 1101 & 0111 = 0101 = 5
```

### 2. OR (|)

```
Either bit is 1:
    1 | 1 = 1
    1 | 0 = 1
    0 | 1 = 1
    0 | 0 = 0

Example: 13 | 7
    1101  (13)
  | 0111  (7)
    ----
    1111  (15)

Visual:
    Bit 3  Bit 2  Bit 1  Bit 0
13:   1      1      0      1
 7:   0      1      1      1
OR:   1      1      1      1  = 15

Common uses:
- Set bit: num | (1 << i)
- Combine flags: flag1 | flag2

Examples:
Set bit 1 of 13:
13 | (1 << 1) = 1101 | 0010 = 1111 = 15

Combine flags:
READ = 4 (0100)
WRITE = 2 (0010)
READ | WRITE = 6 (0110)
```

### 3. XOR (^)

```
Bits are different:
    1 ^ 1 = 0
    1 ^ 0 = 1
    0 ^ 1 = 1
    0 ^ 0 = 0

Example: 13 ^ 7
    1101  (13)
  ^ 0111  (7)
    ----
    1010  (10)

Visual:
    Bit 3  Bit 2  Bit 1  Bit 0
13:   1      1      0      1
 7:   0      1      1      1
XOR:  1      0      1      0  = 10

Properties:
- a ^ 0 = a (identity)
- a ^ a = 0 (self-inverse)
- a ^ b ^ b = a (cancellation)
- Commutative: a ^ b = b ^ a
- Associative: (a ^ b) ^ c = a ^ (b ^ c)

Common uses:
- Toggle bit: num ^ (1 << i)
- Find unique element
- Swap without temp: a^=b, b^=a, a^=b

Examples:
Toggle bit 2 of 13:
13 ^ (1 << 2) = 1101 ^ 0100 = 1001 = 9

Find unique in [1,2,3,2,1]:
1 ^ 2 ^ 3 ^ 2 ^ 1
= (1 ^ 1) ^ (2 ^ 2) ^ 3
= 0 ^ 0 ^ 3
= 3 ✓

Swap a=5, b=3:
a = 5 (0101)
b = 3 (0011)

a ^= b: a = 0101 ^ 0011 = 0110 (6)
b ^= a: b = 0011 ^ 0110 = 0101 (5)
a ^= b: a = 0110 ^ 0101 = 0011 (3)

Result: a=3, b=5 ✓
```

### 4. NOT (~)

```
Flip all bits:
    ~1 = 0
    ~0 = 1

Example: ~13 (in 8-bit)
    ~0000 1101
    = 1111 0010 (two's complement: -14)

In unsigned: 242
In signed: -14

Common uses:
- Invert bits
- Create masks: ~(1 << i)

Example:
Clear bit 2 of 13:
13 & ~(1 << 2)
= 1101 & ~0100
= 1101 & 1011
= 1001 = 9
```

### 5. Left Shift (<<)

```
Shift bits left, fill with 0:
a << b = a × 2^b

Example: 5 << 2
    0000 0101  (5)
    <<  2
    0001 0100  (20)

Visual:
Before: 0 0 0 0 0 1 0 1  (5)
After:  0 0 0 1 0 1 0 0  (20)
        ← ← shift left, add 0s

5 << 2 = 5 × 2² = 5 × 4 = 20 ✓

Common uses:
- Multiply by power of 2: n << k = n × 2^k
- Create bit mask: 1 << i
- Set bit: num | (1 << i)

Examples:
Multiply 7 by 4:
7 << 2 = 28 ✓

Create mask for bit 3:
1 << 3 = 0000 1000
```

### 6. Right Shift (>>)

```
Shift bits right:
a >> b = a / 2^b (integer division)

Example: 20 >> 2
    0001 0100  (20)
    >>  2
    0000 0101  (5)

Visual:
Before: 0 0 0 1 0 1 0 0  (20)
After:  0 0 0 0 0 1 0 1  (5)
        → → shift right, discard

20 >> 2 = 20 / 2² = 20 / 4 = 5 ✓

Logical vs Arithmetic shift:
- Logical: Fill with 0
- Arithmetic: Fill with sign bit

Negative example: -8 >> 1
    1111 1000  (-8)
    >> 1
    1111 1100  (-4) [arithmetic]
    0111 1100  (124) [logical]

Common uses:
- Divide by power of 2: n >> k = n / 2^k
- Extract bits
- Check bit: (num >> i) & 1

Example:
Divide 100 by 8:
100 >> 3 = 12 ✓ (100/8 = 12.5, truncated)
```

## Common Bit Manipulation Tricks

### 1. Check if Power of 2

```
Power of 2 has exactly one bit set:
1:  0001
2:  0010
4:  0100
8:  1000
16: 0001 0000

Trick: n & (n-1) == 0

Example: Is 8 power of 2?
    8:  1000
    7:  0111
8 & 7:  0000  ✓ Power of 2

Example: Is 6 power of 2?
    6:  0110
    5:  0101
6 & 5:  0100  ✗ Not power of 2

Visual:
Power of 2:    Non-power of 2:
    1000           0110
  & 0111         & 0101
    ----           ----
    0000           0100
    ↑              ↑
   Zero          Non-zero
```

### 2. Count Set Bits

```
Count 1s in binary representation:

Example: Count bits in 13 (1101)
Answer: 3

Brian Kernighan's Algorithm:
n & (n-1) removes rightmost set bit

13: 1101
  & 1100 (12)
    1100  count=1

12: 1100
  & 1011 (11)
    1000  count=2

8:  1000
  & 0111 (7)
    0000  count=3

Result: 3 bits ✓

Visual:
    1101
  & 1100
    ----
    1100  ← Removed rightmost 1

    1100
  & 1011
    ----
    1000  ← Removed rightmost 1

    1000
  & 0111
    ----
    0000  ← Removed rightmost 1

Time: O(number of set bits)
```

### 3. Get/Set/Clear/Toggle Bit

```
Get bit i:
(num >> i) & 1

Example: Get bit 2 of 13 (1101)
(13 >> 2) & 1 = 0011 & 1 = 1 ✓

Set bit i:
num | (1 << i)

Example: Set bit 1 of 13
13 | (1 << 1) = 1101 | 0010 = 1111 = 15

Clear bit i:
num & ~(1 << i)

Example: Clear bit 2 of 13
13 & ~(1 << 2) = 1101 & 1011 = 1001 = 9

Toggle bit i:
num ^ (1 << i)

Example: Toggle bit 0 of 13
13 ^ (1 << 0) = 1101 ^ 0001 = 1100 = 12

Visual summary for bit 2:
Original: 1101

Get:    (1101 >> 2) & 1 = 0011 & 0001 = 1
Set:     1101 | 0100 = 1101 (already set)
Clear:   1101 & 1011 = 1001
Toggle:  1101 ^ 0100 = 1001
```

### 4. Get Lowest Set Bit

```
Extract rightmost set bit:
n & -n

Example: 12 (1100)
    12:  0000 1100
   -12:  1111 0100 (two's complement)
12&-12:  0000 0100  = 4 ✓

Visual:
    0000 1100
  & 1111 0100
    ---------
    0000 0100
         ↑
    Lowest set bit

How it works:
-n flips all bits up to and including
rightmost 1, then AND keeps only that bit

Examples:
6:  0110, 6 & -6 = 0010 = 2
8:  1000, 8 & -8 = 1000 = 8
7:  0111, 7 & -7 = 0001 = 1
```

### 5. Remove Lowest Set Bit

```
n & (n-1)

Example: 12 (1100)
    12:  1100
    11:  1011
12 & 11: 1000 = 8 ✓

Visual:
    1100
  & 1011
    ----
    1000
    ↑↑
  Removed rightmost 1

Successive removals of 13 (1101):
1101 & 1100 = 1100 (removed bit 0)
1100 & 1011 = 1000 (removed bit 2)
1000 & 0111 = 0000 (removed bit 3)
```

## Classic Problems

### 1. Single Number

```
Find unique element when all others appear twice:
nums = [4,1,2,1,2]

XOR all elements:
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)
= 4 ^ 0 ^ 0
= 4 ✓

Visual:
    0100  (4)
  ^ 0001  (1)
    ----
    0101

  ^ 0010  (2)
    ----
    0111

  ^ 0001  (1)
    ----
    0110

  ^ 0010  (2)
    ----
    0100  (4) ✓

Time: O(n), Space: O(1)
```

### 2. Missing Number

```
Find missing number in [0, n]:
nums = [3,0,1] (missing 2)

XOR all indices and values:
0 ^ 1 ^ 2 ^ 3 ^ 3 ^ 0 ^ 1
= (0 ^ 0) ^ (1 ^ 1) ^ (3 ^ 3) ^ 2
= 0 ^ 0 ^ 0 ^ 2
= 2 ✓

Visual:
Index:  0  1  2  3
Value:  3  0  1

XOR chain:
0 ^ 1 ^ 2 ^ 3 (indices)
3 ^ 0 ^ 1 (values)

Paired cancellations:
(0 ^ 0) ^ (1 ^ 1) ^ (3 ^ 3) ^ 2
   0    ^    0    ^    0    ^ 2 = 2

Time: O(n), Space: O(1)
```

### 3. Reverse Bits

```
Reverse 32-bit unsigned integer:
Input:  00000010100101000001111010011100
Output: 00111001011110000010100101000000

Process bit by bit from right to left:

result = 0
for 32 times:
    result = result << 1
    result |= (n & 1)
    n >>= 1

Example: Reverse 13 (4-bit for simplicity)
n = 1101

Step 1: result = 0
    0000 << 1 = 0000
    0000 | 1 = 0001
    n >>= 1: 0110

Step 2: result = 1
    0001 << 1 = 0010
    0010 | 0 = 0010
    n >>= 1: 0011

Step 3: result = 2
    0010 << 1 = 0100
    0100 | 1 = 0101
    n >>= 1: 0001

Step 4: result = 5
    0101 << 1 = 1010
    1010 | 1 = 1011
    n >>= 1: 0000

Result: 1011 ✓

Visual:
Input:  1 1 0 1
Output: 1 0 1 1
        ← ← ← ← reversed

Time: O(1) - fixed 32 iterations
```

### 4. Hamming Distance

```
Count bits that differ:
x = 1 (0001)
y = 4 (0100)

XOR to find differing bits:
    0001
  ^ 0100
    ----
    0101

Count set bits in 0101 = 2 ✓

Visual:
Bit 3  Bit 2  Bit 1  Bit 0
  0      0      0      1    (1)
  0      1      0      0    (4)
  ^      ^      ^      ^
  0      1      0      1  (different bits)
         ↑             ↑
    Hamming distance = 2

Time: O(1)
```

### 5. Sum of Two Integers

```
Add without using + operator:
a = 5 (0101)
b = 3 (0011)

Use XOR for sum, AND for carry:

Step 1:
sum = 5 ^ 3 = 0110 (6)
carry = (5 & 3) << 1 = 0001 << 1 = 0010 (2)

Step 2:
sum = 6 ^ 2 = 0100 (4)
carry = (6 & 2) << 1 = 0010 << 1 = 0100 (4)

Step 3:
sum = 4 ^ 4 = 0000 (0)
carry = (4 & 4) << 1 = 0100 << 1 = 1000 (8)

Step 4:
sum = 0 ^ 8 = 1000 (8)
carry = (0 & 8) << 1 = 0000 (0)

Result: 8 ✓

Visual:
    0101  (5)
  + 0011  (3)
    ----

XOR (no carry):
    0101
  ^ 0011
    0110

AND (carry):
    0101
  & 0011
    0001
  << 1
    0010

Continue until no carry...

Time: O(1) - max 32 iterations
```

## Time and Space Complexity

```
Operation               Time    Space
Check bit               O(1)    O(1)
Set/Clear/Toggle bit    O(1)    O(1)
Count bits              O(k)    O(1)  k=set bits
Reverse bits            O(1)    O(1)  32 iterations
Power of 2 check        O(1)    O(1)
Get lowest bit          O(1)    O(1)
XOR single number       O(n)    O(1)
```

## Python Implementation

```python
# Check if bit i is set
def is_bit_set(num, i):
    """Time: O(1)"""
    return (num >> i) & 1 == 1


# Set bit i
def set_bit(num, i):
    """Time: O(1)"""
    return num | (1 << i)


# Clear bit i
def clear_bit(num, i):
    """Time: O(1)"""
    return num & ~(1 << i)


# Toggle bit i
def toggle_bit(num, i):
    """Time: O(1)"""
    return num ^ (1 << i)


# Count set bits
def count_bits(n):
    """
    Brian Kernighan's algorithm.
    Time: O(k) where k = number of set bits
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


# Is power of 2
def is_power_of_two(n):
    """Time: O(1)"""
    return n > 0 and (n & (n - 1)) == 0


# Get lowest set bit
def get_lowest_bit(n):
    """Time: O(1)"""
    return n & -n


# Single number
def single_number(nums):
    """
    Find unique when all others appear twice.
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# Single number II (appears once, others thrice)
def single_number_ii(nums):
    """
    Time: O(n), Space: O(1)
    """
    ones = twos = 0

    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones


# Missing number
def missing_number(nums):
    """
    Time: O(n), Space: O(1)
    """
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result


# Reverse bits
def reverse_bits(n):
    """
    32-bit unsigned integer.
    Time: O(1), Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# Hamming distance
def hamming_distance(x, y):
    """
    Time: O(1), Space: O(1)
    """
    return count_bits(x ^ y)


# Sum of two integers
def get_sum(a, b):
    """
    Add without + operator.
    Time: O(1), Space: O(1)
    """
    mask = 0xFFFFFFFF

    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & mask
        b = carry & mask

    return a if a <= 0x7FFFFFFF else ~(a ^ mask)


# Number of 1 bits
def hamming_weight(n):
    """
    Time: O(1), Space: O(1)
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


# Bitwise AND of range
def range_bitwise_and(left, right):
    """
    Time: O(log n), Space: O(1)
    """
    shift = 0
    while left != right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift


# Maximum XOR of two numbers
def find_maximum_xor(nums):
    """
    Time: O(n), Space: O(n)
    """
    max_xor = 0
    mask = 0

    for i in range(31, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}

        temp = max_xor | (1 << i)
        for prefix in prefixes:
            if temp ^ prefix in prefixes:
                max_xor = temp
                break

    return max_xor


# UTF-8 Validation
def valid_utf8(data):
    """
    Time: O(n), Space: O(1)
    """
    n_bytes = 0

    for num in data:
        if n_bytes == 0:
            if (num >> 5) == 0b110:
                n_bytes = 1
            elif (num >> 4) == 0b1110:
                n_bytes = 2
            elif (num >> 3) == 0b11110:
                n_bytes = 3
            elif (num >> 7):
                return False
        else:
            if (num >> 6) != 0b10:
                return False
            n_bytes -= 1

    return n_bytes == 0
```

## Key Takeaways

1. **Basic Operations**:
   - AND: Check/clear bits
   - OR: Set bits
   - XOR: Toggle/find unique
   - NOT: Invert
   - Shift: Multiply/divide by 2

2. **Common Tricks**:
   - n & (n-1): Remove rightmost 1
   - n & -n: Get rightmost 1
   - n & 1: Check odd/even
   - n ^ n: Always 0

3. **XOR Properties**:
   - a ^ 0 = a
   - a ^ a = 0
   - Associative, commutative
   - Use for finding unique

4. **Optimization**:
   - Replace * and / by 2^k with shifts
   - Use bit operations for flags
   - Space-efficient storage

5. **When to Use**:
   - Flags and permissions
   - Set operations
   - Space optimization
   - Low-level optimization
   - Finding unique elements

6. **Edge Cases**:
   - Sign bit in negative numbers
   - Overflow in operations
   - 32-bit vs 64-bit integers
   - Logical vs arithmetic shift
