"""
Math & Geometry — Number-Theory and Matrix-Transform Skeletons

This category is a grab-bag, but a handful of routines recur constantly:

  1. EUCLID'S GCD        — replace (a, b) with (b, a % b) until b is 0; the
                           remainder shrinks fast, giving O(log min(a, b)).
  2. FAST EXPONENTIATION — square the base and halve the exponent, turning O(n)
                           multiplications into O(log n).
  3. IN-PLACE MATRIX OPS — rotations / transposes done by swapping cells, no
                           second grid (O(1) extra space).

There's no single shared invariant; each routine documents its own.
"""

from typing import List


def gcd(a: int, b: int) -> int:
    """Greatest common divisor via the Euclidean algorithm.

    Time:      O(log min(a, b))
    Space:     O(1)
    Invariant: gcd(a, b) == gcd(b, a % b) at every step, and b strictly
               decreases — so when b reaches 0, a holds the answer.
    """

    while b != 0:
        # The remainder is always smaller than b, which guarantees progress.
        a, b = b, a % b
    return a


def fast_power(base: float, exponent: int) -> float:
    """Compute base ** exponent by binary (fast) exponentiation.

    Time:      O(log |exponent|)
    Space:     O(1)
    Invariant: result * (base ** exponent_remaining) stays constant across the
               loop, so when the exponent reaches 0 `result` is the full answer.
    """

    # Handle negative exponents up front: x ** -n == (1 / x) ** n.
    if exponent < 0:
        base = 1 / base
        exponent = -exponent

    result = 1.0
    # TODO: for modular problems, take `% mod` after every multiplication.
    while exponent > 0:
        # If the lowest exponent bit is set, fold one copy of the current base in.
        if exponent & 1:
            result *= base

        # Square the base and drop the bit we just consumed.
        base *= base
        exponent >>= 1

    return result


def rotate_matrix_clockwise(matrix: List[List[int]]) -> None:
    """Rotate a square matrix 90 degrees clockwise, in place.

    Trick: transpose (reflect over the main diagonal), then reverse each row.
    Those two reflections compose into a rotation.

    Time:      O(n^2)
    Space:     O(1) — every value is swapped within the existing grid.
    Invariant: after the transpose loop, matrix[i][j] holds the original
               matrix[j][i]; reversing each row then sends it to its rotated spot.
    """

    n = len(matrix)

    # Transpose: swap across the main diagonal. Start j at i + 1 so each pair is
    # swapped exactly once — swapping the whole grid would undo itself.
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row to finish the clockwise rotation.
    for row in matrix:
        row.reverse()
