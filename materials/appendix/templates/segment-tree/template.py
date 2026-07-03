"""
Segment Tree & Fenwick Tree — Range Query + Point Update Skeletons

Both structures answer range queries over an array that *changes*: point
updates and range queries each cost O(log n), where prefix sums would pay O(n)
per update. Reach for the Fenwick tree when the operation is invertible (sum);
reach for the segment tree when it isn't (min/max) or when you need lazy
range updates.

Invariants: a segment tree node covers a contiguous interval and stores the
combined value of its two children; a Fenwick tree cell `i` is responsible for
the `i & (-i)` elements ending at `i` (1-indexed).
"""

from typing import List


class FenwickTree:
    """Binary indexed tree for prefix sums with point updates. 1-indexed."""

    def __init__(self, size: int) -> None:
        self.n = size
        self.tree: List[int] = [0] * (size + 1)

    def add(self, i: int, delta: int) -> None:
        """Add delta at position i (1-indexed). Pass a *delta*, not the new value."""

        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # jump to the next cell responsible for i

    def prefix_sum(self, i: int) -> int:
        """Sum of positions 1..i."""

        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)  # strip the lowest set bit
        return s

    def range_sum(self, left: int, right: int) -> int:
        """Sum of positions left..right (1-indexed, inclusive)."""

        return self.prefix_sum(right) - self.prefix_sum(left - 1)


class SegmentTree:
    """Iterative segment tree for range sum. Swap `+` for min/max as needed.

    For min/max, also swap the 0 identity for float('inf') / float('-inf').
    """

    def __init__(self, nums: List[int]) -> None:
        self.n = len(nums)
        # Leaves live at tree[n..2n); internal node i combines 2i and 2i+1.
        self.tree: List[int] = [0] * (2 * self.n)
        for i, v in enumerate(nums):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        """Set nums[index] = value (0-indexed), then fix ancestors."""

        i = self.n + index
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def query(self, left: int, right: int) -> int:
        """Combine of nums[left..right] (0-indexed, inclusive)."""

        result = 0  # identity for sum
        lo, hi = self.n + left, self.n + right + 1  # [lo, hi)
        while lo < hi:
            if lo % 2 == 1:  # lo is a right child: take it, step past
                result += self.tree[lo]
                lo += 1
            if hi % 2 == 1:  # hi's left sibling is inside the range
                hi -= 1
                result += self.tree[hi]
            lo //= 2
            hi //= 2
        return result
