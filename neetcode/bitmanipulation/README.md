# Bit Manipulation

## 18. Bit Manipulation (7 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 136 | Easy | Single Number | [Link](https://leetcode.com/problems/single-number/) |
| 191 | Easy | Number of 1 Bits | [Link](https://leetcode.com/problems/number-of-1-bits/) |
| 338 | Easy | Counting Bits | [Link](https://leetcode.com/problems/counting-bits/) |
| 190 | Easy | Reverse Bits | [Link](https://leetcode.com/problems/reverse-bits/) |
| 268 | Easy | Missing Number | [Link](https://leetcode.com/problems/missing-number/) |
| 371 | Medium | Sum of Two Integers | [Link](https://leetcode.com/problems/sum-of-two-integers/) |
| 7 | Medium | Reverse Integer | [Link](https://leetcode.com/problems/reverse-integer/) |

---

## Data Structures

### Integer (Binary Representation)
An integer is a sequence of bits. You manipulate individual bits using bitwise operators. No extra data structure needed — the operations work directly on the number's binary form.

---

## Bitwise Operators

| Operator | Symbol | Effect |
|----------|--------|--------|
| AND | `a & b` | 1 only if both bits are 1 |
| OR | `a \| b` | 1 if either bit is 1 |
| XOR | `a ^ b` | 1 if bits differ (0 if same) |
| NOT | `~a` | flip all bits |
| Left shift | `a << n` | multiply by 2^n |
| Right shift | `a >> n` | integer divide by 2^n |

---

## Core Patterns

### XOR to Find Unique Element
XOR is commutative and associative, and `x ^ x = 0`, `x ^ 0 = x`. XOR all numbers together — duplicates cancel out, leaving only the unique element. O(n) time, O(1) space. Used in Single Number.

### XOR to Find Missing Number
XOR all indices `0..n` with all values in the array. Every number that appears cancels itself out, leaving only the missing one. Alternatively: `missing = n*(n+1)//2 - sum(nums)`. Used in Missing Number.

### Count Set Bits (Popcount)
**Loop method**: `while n: count += n & 1; n >>= 1` — checks the lowest bit and shifts right.
**Brian Kernighan's trick**: `n &= n - 1` removes the lowest set bit in one operation. Loop until `n == 0`. O(number of set bits). Used in Number of 1 Bits.

### Counting Bits DP
For each number `i`, `bits[i] = bits[i >> 1] + (i & 1)`. Shifting right by 1 removes the last bit (same count as `i//2`), then add 1 if the last bit was set. O(n) total. Used in Counting Bits.

### Reverse Bits
Process bit by bit: read the lowest bit of `n` with `n & 1`, write it into the result by shifting result left, then shift `n` right. Repeat 32 times. Used in Reverse Bits.

### Add Without Arithmetic Operators (XOR + AND)
`a ^ b` gives the sum without carries. `(a & b) << 1` gives just the carries shifted left. Repeat until no carry remains. Used in Sum of Two Integers. In Python, mask to 32 bits to handle two's complement correctly.
