# Bit Manipulation

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds simulation problems (reverse integer) and the XOR-for-single-element trick. NeetCode 250 extends into bitwise AND of ranges and bit construction. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table. For each new problem, ask yourself: which bit property applies here? (XOR cancellation, lowest-set-bit isolation, bit counting, or carry simulation.)

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 191 | Easy | Number of 1 Bits | [Link](https://leetcode.com/problems/number-of-1-bits/) | ☐ |
| 338 | Easy | Counting Bits | [Link](https://leetcode.com/problems/counting-bits/) | ☐ |
| 190 | Easy | Reverse Bits | [Link](https://leetcode.com/problems/reverse-bits/) | ☐ |
| 268 | Easy | Missing Number | [Link](https://leetcode.com/problems/missing-number/) | ☐ |
| 371 | Medium | Sum of Two Integers | [Link](https://leetcode.com/problems/sum-of-two-integers/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 136 | Easy | Single Number | [Link](https://leetcode.com/problems/single-number/) | ☐ |
| 7 | Medium | Reverse Integer | [Link](https://leetcode.com/problems/reverse-integer/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 67 | Easy | Add Binary | [Link](https://leetcode.com/problems/add-binary/) | ☐ | Binary string addition |
| 201 | Medium | Bitwise AND of Numbers Range | [Link](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | ☐ | Bit prefix |
| 3133 | Medium | Minimum Array End | [Link](https://leetcode.com/problems/minimum-array-end/) | ☐ | Bit construction |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| XOR all elements (single/missing) | O(n) | O(1) | Duplicates cancel to 0 |
| Count set bits (Brian Kernighan) | O(k) | O(1) | k = number of set bits |
| Count set bits (bin().count) | O(log n) | O(log n) | String conversion |
| Counting Bits (DP) | O(n) | O(n) | dp[i] = dp[i>>1] + (i&1) |
| Reverse Bits (bit by bit) | O(32) | O(1) | Fixed 32 iterations |
| Sum of Two Integers (carry sim) | O(32) | O(1) | At most 32 carry propagations |
| Bitwise AND of range | O(log n) | O(1) | Shift right until left==right |
| Add Binary strings | O(n) | O(n) | Process from LSB to MSB |

---

## Data Structures

### Integer as a Bit Array

In bit manipulation, you treat an integer as a fixed-length array of bits. Each bit position i holds a 0 or 1. You access, set, clear, and toggle individual bits using masks built from `1 << i`.

```
Number: 42  =  0b00101010

Bit positions (0-indexed from right):
  Position:   7  6  5  4  3  2  1  0
  Bit value:  0  0  1  0  1  0  1  0
                     ↑        ↑     ↑
                   bit 5    bit 3  bit 1

Check bit 3:  42 & (1 << 3) → 42 & 8 → 8  (non-zero → bit is set)
Clear bit 3:  42 & ~(1 << 3) → 42 & ...11110111 → 34
Set bit 0:    42 | (1 << 0) → 43
Toggle bit 1: 42 ^ (1 << 1) → 40
```

**When it matters:** Number of 1 Bits (#191), Sum of Two Integers (#371), Reverse Bits (#190). Think of `&`, `|`, `^`, `~` as bitwise AND, OR, XOR, NOT applied to every bit simultaneously.

### XOR Truth Table

XOR is the fundamental tool for cancellation and parity. The key properties: `x ^ x = 0`, `x ^ 0 = x`, and XOR is commutative and associative.

```
XOR truth table:
  0 ^ 0 = 0
  0 ^ 1 = 1
  1 ^ 0 = 1
  1 ^ 1 = 0   ← same inputs cancel to 0

Cancellation property:  a ^ b ^ a = b
  (because a ^ a = 0, and 0 ^ b = b)

Single Number: [4, 1, 2, 1, 2]
  4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1^1) ^ (2^2)
= 4 ^ 0 ^ 0
= 4  ← the one without a pair

Missing Number: [0,1,3]  expected [0,1,2,3]
  XOR all indices:  0^1^2^3
  XOR all values:   0^1^3
  XOR together:     (0^0) ^ (1^1) ^ (2) ^ (3^3) = 2
```

**When it matters:** Single Number (#136), Missing Number (#268). If every element appears an even number of times except one, XOR all elements — pairs cancel, leaving the odd one out.

---

## Core Patterns

### XOR for Duplicates / Missing
**When to use:** Every element appears exactly twice except one, or you need to find a missing number in a range. XOR all elements (and all expected values) — duplicates cancel, leaving only the unpaired value.
**Complexity:** O(n) time, O(1) space
**Problems:** Single Number (#136), Missing Number (#268)
**Common mistake:** Forgetting to XOR with the expected values (indices 0..n) for the missing number problem — you must XOR both the array values and the range values.

```python
# Single Number: every element appears twice except one
result = 0
for num in nums:
    result ^= num
return result

# Missing Number: range is [0..n], one is missing
result = len(nums)          # start with n
for i, num in enumerate(nums):
    result ^= i ^ num       # XOR with both index and value
return result
```

### Bit Masking
**When to use:** Check, set, clear, or toggle a specific bit at position i.
**Complexity:** O(1) per operation
**Problems:** Number of 1 Bits (#191), Sum of Two Integers (#371), any problem needing bit-level access
**Common mistake:** Using `>>` on a negative number in Python — Python integers are arbitrary precision and `>>` on negatives sign-extends infinitely. Mask with `& 0xFFFFFFFF` to simulate 32-bit behavior.

```python
n & 1            # lowest bit (0 or 1) — is n odd?
n & (1 << i)     # check bit i (non-zero if set)
n | (1 << i)     # set bit i
n & ~(1 << i)    # clear bit i
n ^ (1 << i)     # toggle bit i
n & (n - 1)      # clear the lowest set bit
n & (-n)         # isolate the lowest set bit (only that bit remains)
```

### Count Set Bits (Brian Kernighan)
**When to use:** Count the number of 1-bits in an integer. `n & (n-1)` always clears the lowest set bit — so count how many times you can do this until n reaches 0.
**Complexity:** O(k) time where k = number of set bits, O(1) space
**Problems:** Number of 1 Bits (#191)
**Common mistake:** Using a loop over all 32 bit positions instead — Brian Kernighan's method is faster when the number is sparse (few set bits).

```python
count = 0
while n:
    n &= n - 1    # clear the lowest set bit
    count += 1
return count
```

### Bit DP (Counting Bits)
**When to use:** Compute the number of set bits for every number from 0 to n in O(n) total — rather than calling popcount on each number individually.
**Complexity:** O(n) time, O(n) space
**Problems:** Counting Bits (#338)
**Common mistake:** Not recognizing the recurrence: every number's bit count equals its right-shifted version's count plus its lowest bit. `i >> 1` is just `i // 2` and is always already computed.

```python
dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i >> 1] + (i & 1)
    # dp[i>>1] = popcount of i with LSB removed
    # (i & 1)  = the LSB itself (0 or 1)
return dp
```

### Two's Complement Addition (Sum of Two Integers)
**When to use:** Add two integers without using `+` or `-`. Simulate carry propagation with XOR (sum without carry) and AND shifted left (the carry itself).
**Complexity:** O(32) time, O(1) space (at most 32 carry propagations for 32-bit integers)
**Problems:** Sum of Two Integers (#371)
**Common mistake:** Python integers are arbitrary precision — a carry can propagate infinitely. Mask both `a` and `b` with `0xFFFFFFFF` after each step to stay within 32 bits.

```python
mask = 0xFFFFFFFF
while b & mask:
    carry = (a & b) << 1    # carry: bits that overflow into next position
    a = a ^ b               # sum without carry
    b = carry
# Handle Python's arbitrary-precision negative numbers
return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

---

## Syntax Reference

### Key Bit Manipulation Operators

```python
n & 1            # lowest bit — is n odd?
n >> 1           # right shift: floor(n / 2)
n << 1           # left shift: n * 2
n & (n - 1)      # clear lowest set bit (Brian Kernighan)
n & (-n)         # isolate lowest set bit
~n               # bitwise NOT — in Python this equals -(n+1)
```

### 32-bit Simulation in Python

```python
# Python ints are unbounded — mask to 32 bits when simulating hardware:
MASK = 0xFFFFFFFF
MAX  = 0x7FFFFFFF   # 2^31 - 1 (largest positive 32-bit signed int)

n = n & MASK        # keep only lowest 32 bits
# Convert back to signed if the 32nd bit is set:
if n > MAX:
    n = ~(n ^ MASK)   # two's complement to negative
```

### Binary String Conversion

```python
bin(n)              # '0b1010' — note the '0b' prefix
bin(n)[2:]          # '1010'  — strip the prefix
int('1010', 2)      # 10      — parse binary string to int
f'{n:08b}'          # '00001010' — zero-padded to 8 bits

# Add Binary (#67) — process from right to left:
i, j, carry = len(a)-1, len(b)-1, 0
result = []
while i >= 0 or j >= 0 or carry:
    total = carry
    if i >= 0: total += int(a[i]); i -= 1
    if j >= 0: total += int(b[j]); j -= 1
    result.append(str(total % 2))
    carry = total // 2
return ''.join(reversed(result))
```

### Reverse Bits

```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)   # shift result left, OR in n's LSB
        n >>= 1                             # advance to next bit of n
    return result
```

### Bitwise AND of Numbers Range

```python
# AND of all numbers in [left, right]
# Key insight: common prefix of left and right in binary
def rangeBitwiseAnd(left, right):
    shift = 0
    while left != right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift
# The AND result is the common bit prefix — all bits below the common prefix are 0
```

### Counting Set Bits (three ways)

```python
# Method 1: bin + count (simplest)
bin(n).count('1')

# Method 2: Brian Kernighan (fewest iterations)
count = 0
while n:
    n &= n - 1
    count += 1

# Method 3: loop over all 32 bits (most explicit)
count = 0
for _ in range(32):
    count += n & 1
    n >>= 1
```
