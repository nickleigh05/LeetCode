# 18. Bit Manipulation
*Masks, shifts, and XOR cancellation in O(1).*

[← Prev](17-intervals.md) · [🗺 Roadmap](../roadmap.md) · [Next →](19-math-geometry.md)

---

> **Builds on:** nothing new structurally — just integers viewed as rows of bits.

Working directly with bits unlocks O(1) tricks that look like magic: **XOR** cancels duplicates, masks test and flip individual bits, and `n & (n-1)` clears the lowest set bit. Niche but high-leverage — a handful of problems become one-liners once you see the bit pattern.

## The Pattern

### Bit Manipulation and XOR

```
  Binary number cheat sheet:
  Dec  Bin
   0 = 0000
   1 = 0001
   2 = 0010
   4 = 0100
   8 = 1000
  15 = 1111

  XOR magic:
  a ^ a = 0000  (cancels itself)
  a ^ 0 = a     (identity)
  [1,1,2,2,3] XOR all: 1^1^2^2^3 = 0^0^3 = 3   ← finds single number!

  Missing number in [0..n]:
  [0,1,3]:  XOR indices 0,1,2,3 = 0^1^2^3 = 0
            XOR nums  0,1,3     = 0^1^3 = 2
            0 ^ 2 = 2  ← missing!

  Power of 2 check:
  8  = 1000
  7  = 0111
  8 & 7 = 0000 ← power of 2!

  n & (n-1) clears the lowest set bit:
  12 = 1100
  11 = 1011
  12 & 11 = 1000  ← cleared bit 2

  Counting set bits — Kernighan's:
  n=12=1100:
  12 & 11 = 1000 (count=1)
   8 &  7 = 0000 (count=2) → 2 set bits
```

**What it is:** Direct manipulation of binary representations of integers to achieve results that would otherwise require extra space or more time.

**Use this when:**
- [ ] Find the single number (others appear twice)
- [ ] Find the missing number in [0..n]
- [ ] Check if n is a power of 2
- [ ] Count number of set bits
- [ ] Reverse bits of a 32-bit integer
- [ ] Sum of two integers without using `+`
- [ ] Enumerate all subsets (bitmask DP)

**Core tricks reference:**

| Trick | Expression | What it does |
|-------|-----------|-------------|
| Check bit k | `(n >> k) & 1` | 1 if bit k is set |
| Set bit k | `n \| (1 << k)` | Force bit k to 1 |
| Clear bit k | `n & ~(1 << k)` | Force bit k to 0 |
| Toggle bit k | `n ^ (1 << k)` | Flip bit k |
| Power of 2? | `n & (n-1) == 0` | True if exactly 1 bit set |
| Clear lowest bit | `n & (n-1)` | Remove lowest set bit |
| Get lowest bit | `n & (-n)` | Isolate lowest set bit |

**Python:**
```python
# Single number — XOR all elements
from functools import reduce
import operator
def single_number(nums):
    return reduce(operator.xor, nums)

# Missing number
def missing_number(nums):
    return len(nums) ^ reduce(operator.xor, enumerate(nums), 0)
    # or cleaner:
    n = len(nums)
    return n*(n+1)//2 - sum(nums)  # math alternative

# Count set bits (Hamming weight)
def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1    # clear lowest set bit
        count += 1
    return count

# Reverse bits of 32-bit integer
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

# Sum without + (bit carry simulation)
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a if b == 0 else a & mask

# Subset enumeration with bitmask
def all_subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

**Complexity:** All individual operations are O(1). Problems over arrays are typically O(n) time, O(1) space.

**Blind 75 examples:** Number of 1 Bits · Counting Bits · Reverse Bits · Missing Number · Sum of Two Integers

## Algorithm Deep-Dive

### Bit Manipulation

```
  Binary representation:
  13 = 1101₂  →  bit3=1, bit2=1, bit1=0, bit0=1

  Core operations:
  ┌──────────────┬──────────┬─────────────────────────────┐
  │ Operation    │ Syntax   │ Example                      │
  ├──────────────┼──────────┼─────────────────────────────┤
  │ AND          │ a & b    │ 1101 & 1010 = 1000           │
  │ OR           │ a | b    │ 1101 | 1010 = 1111           │
  │ XOR          │ a ^ b    │ 1101 ^ 1010 = 0111           │
  │ NOT          │ ~a       │ ~1101 = ...0010 (2's comp)   │
  │ Left shift   │ a << n   │ 0001 << 2 = 0100 (× 2^n)    │
  │ Right shift  │ a >> n   │ 1100 >> 2 = 0011 (÷ 2^n)    │
  └──────────────┴──────────┴─────────────────────────────┘

  XOR truth table:
  0 ^ 0 = 0   (same → 0)
  0 ^ 1 = 1   (diff → 1)
  1 ^ 0 = 1
  1 ^ 1 = 0   (same → 0)

  Key XOR properties:
  a ^ a = 0        (self-cancels)
  a ^ 0 = a        (identity)
  a ^ b ^ a = b    (used in "find single number")
```

**What it does:** Operates directly on the binary representation of integers. Enables O(1) space solutions and often O(n) time for problems that would otherwise require sets or additional space.

**Recognition signals:**
- "Find the single number" (XOR pairs to cancel)
- "Missing number" (XOR with full range)
- Powers of 2 check: `n & (n-1) == 0`
- Count set bits (popcount)
- Subset generation using bitmask
- "Sum without +" (bit by bit carry simulation)

**Python:**
```python
# Check if bit k is set
(n >> k) & 1

# Set bit k
n | (1 << k)

# Clear bit k
n & ~(1 << k)

# Toggle bit k
n ^ (1 << k)

# Check power of 2 (exactly one bit set)
n > 0 and (n & (n - 1)) == 0

# Count set bits (Hamming weight)
bin(n).count('1')
# OR kernighan's method: O(number of set bits)
count = 0
while n:
    n &= n - 1   # clear lowest set bit
    count += 1

# XOR: find single number (all others appear twice)
from functools import reduce
import operator
single = reduce(operator.xor, nums)

# Missing number (0..n, one missing)
missing = len(nums)
for i, num in enumerate(nums):
    missing ^= i ^ num

# Subset enumeration using bitmask
n = 3
for mask in range(1 << n):   # 0 to 2^n - 1
    subset = [i for i in range(n) if mask & (1 << i)]
```

**Complexity:** All individual bit operations are O(1). Problems using bits over an array are typically O(n) time, O(1) space.

**Data structures it uses:**
Array (of integers)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/bit-manipulation/`](../appendix/templates/bit-manipulation/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/bit-manipulation/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Bit Manipulation problems →**](../../lists/recommended.md#18-bit-manipulation-13-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Math & Geometry](19-math-geometry.md) — gCD, fast power, and in-place matrix transforms.

[← Prev](17-intervals.md) · [🗺 Roadmap](../roadmap.md) · [Next →](19-math-geometry.md)

