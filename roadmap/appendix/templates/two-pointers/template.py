"""
Two Pointers — Converging Pointers Skeleton

Two indices walk the array instead of one. The classic shape places them at
opposite ends of a *sorted* array and moves them toward each other; each step
discards a whole branch of the search space, turning an O(n^2) pair scan into a
single O(n) sweep.

Invariant (converging form): every pair (i, j) with i < left or j > right has
already been ruled out. So the answer, if one exists, must involve an index in
the still-live window [left, right].
"""

from typing import List, Optional


def converging_pointers(nums: List[int], target: int) -> Optional[List[int]]:
    """Scan a sorted array from both ends toward the middle.

    Time:      O(n) for the scan; O(n log n) if you must sort first.
    Space:     O(1) — only two indices.
    Invariant: nums is sorted, so moving `left` rightward strictly increases the
               combined quantity and moving `right` leftward strictly decreases
               it. That monotonicity is what makes discarding an end *safe*.
    """

    left = 0
    right = len(nums) - 1

    # Strict `<` (not `<=`): left and right must stay on distinct elements so we
    # never pair an element with itself. The loop ends the instant they meet.
    while left < right:
        # TODO: problem-specific quantity built from the two ends.
        current = nums[left] + nums[right]

        if current == target:
            return [left, right]
        elif current < target:
            # Too small. The only way to grow the sum is to abandon the smallest
            # value still in play — that is nums[left]. Anything that could pair
            # with the old left is now provably <= target, so we lose nothing.
            left += 1
        else:
            # Symmetric: the sum is too big, so drop the largest remaining value.
            right -= 1

    return None


def same_direction_partition(nums: List[int]) -> int:
    """Overwrite in place with a slow writer and a fast reader.

    Time:      O(n)
    Space:     O(1) — done in place.
    Invariant: nums[0 .. slow-1] always holds the kept elements in order, and
               `fast` is the next element to examine. `slow` only advances when
               we commit a keeper, so it never overtakes `fast`.
    """

    slow = 0  # next write position == one past the last kept element

    for fast in range(len(nums)):
        # TODO: problem-specific "keep this element?" test, e.g. nums[fast] != 0
        # for Move Zeroes, or nums[fast] != val for Remove Element.
        keep_current = True

        if keep_current:
            nums[slow] = nums[fast]
            slow += 1

    # slow is now the length of the kept prefix.
    return slow
