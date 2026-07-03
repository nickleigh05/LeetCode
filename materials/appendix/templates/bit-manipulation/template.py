"""
Bit Manipulation — Masking, XOR, and Bit-Iteration Skeleton

Bits are a fixed set of boolean flags you can test, set, and combine in O(1).
Three ideas cover most problems:

  1. MASKING       — isolate / set / clear / toggle the k-th bit with shifts.
  2. XOR tricks    — a ^ a == 0 and a ^ 0 == a, so XOR cancels pairs; perfect for
                     "find the unique element".
  3. BIT ITERATION — process one bit at a time; `n & (n - 1)` clears the lowest
                     set bit, so the loop runs once per set bit (Kernighan).

Invariant (Kernighan loop): each iteration removes exactly one set bit, so the
loop count equals the popcount — never more.
"""

from typing import List


def common_bit_operations(n: int, k: int) -> None:
    """Reference for the four single-bit operations at bit position k.

    Time:  O(1) each.
    Space: O(1).
    """

    mask = 1 << k  # a single 1 in position k, 0 everywhere else

    is_set = (n & mask) != 0   # TEST  : is bit k a 1?  (parenthesize — & binds loosely)
    set_k = n | mask           # SET   : force bit k to 1
    clear_k = n & ~mask        # CLEAR : force bit k to 0
    toggle_k = n ^ mask        # TOGGLE: flip bit k

    # Shown for reference; a real problem uses whichever it needs.
    _ = (is_set, set_k, clear_k, toggle_k)


def xor_unique(nums: List[int]) -> int:
    """Find the single element that appears an odd number of times.

    Every value appearing twice cancels itself (x ^ x == 0), leaving only the
    unpaired one.

    Time:      O(n)
    Space:     O(1) — no hash set required.
    Invariant: after folding in nums[0..i], `accumulator` is the XOR of those
               elements, i.e. every fully-paired value has already cancelled.
    """

    accumulator = 0
    for value in nums:
        # TODO: plain XOR handles "all pairs but one". Variants (an element
        # appears 3x, or there are two singles) need bit-counting or a mask split.
        accumulator ^= value
    return accumulator


def count_set_bits(n: int) -> int:
    """Count the 1-bits with Brian Kernighan's trick.

    Time:      O(number of set bits) — beats scanning all 32/64 positions.
    Space:     O(1)
    Invariant: `n & (n - 1)` clears the lowest set bit, so each turn drops
               exactly one bit and the count comes out exact.
    """

    count = 0
    while n:
        n &= n - 1  # erase the lowest set bit
        count += 1
    return count
