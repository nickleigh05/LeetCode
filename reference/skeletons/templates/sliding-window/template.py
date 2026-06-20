"""
Sliding Window — Variable-Size (Shrink-to-Valid) Skeleton

A window [left, right] slides across the array/string. `right` always moves
forward to *grow* the window and pull in new data; `left` moves forward only to
*shrink* the window back to a valid (or optimal) state. Because each index is
added once and removed at most once, the whole thing is O(n) even though it
reads like a nested loop.

Invariant: at the bottom of each iteration the window [left, right] is in a
state the problem considers valid, so any answer read there is legitimate. The
inner while-loop is what restores that validity after the window grows.
"""

from typing import Dict, List


def variable_window(nums: List[int]) -> int:
    """Grow on the right, shrink on the left, track the best valid window.

    Time:      O(n) — `left` and `right` each advance at most n times total.
    Space:     O(k) for whatever window summary you keep (counts, sum, set...).
    Invariant: the inner while-loop always exits with the window valid, so
               `best` is only ever updated from a valid window.
    """

    window_state: Dict[int, int] = {}  # running summary of [left, right]
    left = 0
    best = 0

    for right in range(len(nums)):
        # 1. EXPAND: fold nums[right] into the window summary.
        right_value = nums[right]
        window_state[right_value] = window_state.get(right_value, 0) + 1

        # 2. SHRINK: while the window violates the constraint, evict from left.
        #    TODO: problem-specific "is the window invalid?" condition, e.g.
        #    len(window_state) > k, or a running sum exceeding a cap.
        while False:
            left_value = nums[left]
            window_state[left_value] -= 1
            if window_state[left_value] == 0:
                del window_state[left_value]  # keep map size == distinct count
            left += 1

        # 3. RECORD: the window is valid here — update the answer.
        #    NOTE: this placement is for "longest valid window" problems. For
        #    "shortest valid window", record *inside* the shrink loop and flip
        #    the while-condition to "while the window is STILL valid".
        best = max(best, right - left + 1)

    return best


def fixed_window(nums: List[int], k: int) -> int:
    """Slide a window of constant width k across the array.

    Time:      O(n)
    Space:     O(1) beyond the running aggregate.
    Invariant: once `right >= k - 1`, the window is exactly the k elements
               nums[right-k+1 .. right]; add the entering element and subtract
               the leaving one so the aggregate stays exact in O(1) per step.
    """

    window_sum = 0
    best = 0

    for right in range(len(nums)):
        window_sum += nums[right]  # element entering on the right edge

        # Only act once the window has reached full width.
        if right >= k - 1:
            # TODO: problem-specific read of the full-width window.
            best = max(best, window_sum)

            # Drop the element that is about to fall off the left edge, so the
            # next iteration's window is again exactly k wide.
            window_sum -= nums[right - k + 1]

    return best
