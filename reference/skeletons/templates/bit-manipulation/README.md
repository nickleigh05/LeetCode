# Bit Manipulation

*XOR, shifts, and masks. Weird-looking but O(1) and fast — and interviewers love asking them. Each bit is just a boolean flag you can flip.*

## Recognize this pattern when...

- The constraint is **"O(1) extra space"** for a counting/dedup problem.
- The phrase is **"single number"**, **"appears once / twice / three times"**, or **"missing number"**.
- You need to **count, reverse, or compare bits** of integers.
- A small set (≤ ~20 elements) can be encoded as a **bitmask** for subset enumeration.
- You must do arithmetic **without `+` / `-`**, or detect a **power of two**.

## Variations

1. **XOR cancellation** — pair elements cancel, the loner survives. *(Single Number)*
2. **Kernighan popcount** — `n &= n - 1` once per set bit. *(Number of 1 Bits, Counting Bits)*
3. **Single-bit masking** — test / set / clear / toggle bit `k` with `1 << k`. *(Reverse Bits)*
4. **Bitmask subset enumeration** — encode presence in an int, iterate `0 .. 2ⁿ−1`. *(Maximum Product of Word Lengths)*
5. **Arithmetic via bits** — sum with XOR (no carry) + AND-shift (carry). *(Sum of Two Integers)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 136 | Easy | Single Number |
| 191 | Easy | Number of 1 Bits |
| 338 | Easy | Counting Bits |
| 190 | Easy | Reverse Bits |
| 371 | Medium | Sum of Two Integers |
| 137 | Medium | Single Number II |

## Common bugs & traps

- **Operator precedence.** `&`, `|`, `^` bind *looser* than `==`. Always write `(n & mask) != 0`, never `n & mask != 0`.
- **Python ints are unbounded.** There's no natural 32-bit overflow — mask with `& 0xFFFFFFFF` and re-interpret the sign manually for two's-complement problems (Sum of Two Integers, Reverse Bits).
- **Shift off-by-one.** Bit `k` is `1 << k`; a 32-bit number's top bit is `1 << 31`, not `1 << 32`.
- **XOR variants.** Plain XOR only solves "everything paired but one." Three-of-a-kind or two-singles need bit-by-bit counts or splitting on a distinguishing bit.
- **`n & (n - 1)` on negatives.** In Python negatives have infinite leading 1s — mask to a fixed width first.
- **Signed reverse/rotate.** Watch the sign bit when reversing 32-bit integers; pad and mask explicitly.
