"""
Binary Search — Exact and Boundary Skeletons

If the search space is ordered (or monotonic in some predicate), you can throw
away half of it every step. Two shapes cover almost everything:

  1. EXACT match  — `left <= right`, shrink past mid each time. Returns the
                    index of a target, or -1 if absent.
  2. BOUNDARY     — find the first index where a monotone predicate flips from
                    False to True (a.k.a. lower_bound / "leftmost"). This is the
                    shape that generalizes to "binary search on the answer".

Invariant: the target / boundary, if it exists, is always inside the current
search range. Every branch preserves that by discarding only a half that
provably cannot contain it.
"""

from typing import Callable, List


def binary_search_exact(nums: List[int], target: int) -> int:
    """Return the index of target in a sorted array, or -1 if absent.

    Time:      O(log n)
    Space:     O(1)
    Invariant: if target exists it lies within nums[left .. right]. The range
               strictly shrinks every iteration, so the loop always terminates.
    """

    left = 0
    right = len(nums) - 1  # inclusive upper bound

    # `<=` because both ends are valid candidates; the range is empty only once
    # left passes right.
    while left <= right:
        # Written as left + (right - left) // 2 (not (left + right) // 2) to
        # avoid integer overflow in fixed-width languages — idiomatic anyway.
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1   # target is strictly right of mid; discard mid too
        else:
            right = mid - 1  # target is strictly left of mid; discard mid too

    return -1


def find_left_boundary(predicate: Callable[[int], bool], low: int, high: int) -> int:
    """Find the smallest x in [low, high] where predicate(x) is True.

    `predicate` must be monotone: once True, it stays True. Pass index bounds
    for array search, or value bounds for "binary search on the answer" (the
    smallest eating speed, the smallest feasible capacity, etc.).

    Time:      O(log(high - low)) predicate evaluations.
    Space:     O(1)
    Invariant: predicate is False everywhere left of `low` and True at `high`,
               so the boundary always sits in [low, high]. When low == high the
               range is a single point — the answer.
    """

    # Half-open search: `high` is the known-True backstop, `low` may be the
    # answer, so the loop runs while there is still a gap to close.
    while low < high:
        mid = low + (high - low) // 2

        # TODO: problem-specific monotone predicate, e.g. nums[mid] >= target,
        # or can_finish_in_time(mid).
        if predicate(mid):
            # mid works, so the boundary is mid or to its left. Keep mid in play.
            high = mid
        else:
            # mid fails, so the boundary must be strictly to the right of mid.
            low = mid + 1

    # low == high: the first index where the predicate is True.
    return low
