"""
Greedy — Single-Pass Local-Choice Skeleton

A greedy algorithm builds the answer by always taking the choice that looks best
right now and never reconsidering. It is correct only when a local optimum
provably leads to a global one (an "exchange argument") — proving that is the
hard part, not the code.

Two shapes:
  1. RUNNING-STATE pass — sweep once, keep a running best/reach/total, update it
                          with a constant-time decision per element.
  2. SORT-THEN-GREEDY   — impose an order first (by end time, ratio, size), then
                          take greedily in that order.

Invariant: the running state summarizes the best result achievable using
everything seen so far under the greedy rule.
"""

from typing import List


def greedy_single_pass(nums: List[int]) -> int:
    """One sweep, one local decision per element (Kadane / jump-reach shape).

    Time:      O(n)
    Space:     O(1)
    Invariant: `best` is the optimal answer for the prefix processed so far, and
               `running` carries exactly the state the next decision needs.
    """

    best = nums[0]     # TODO: problem-specific initial answer
    running = nums[0]  # TODO: problem-specific carried state

    for value in nums[1:]:
        # GREEDY CHOICE: decide using only `running` and the current value — no
        # looking ahead, no undoing past choices.
        # TODO: problem-specific transition, e.g. Kadane's maximum subarray:
        #   running = max(value, running + value)
        running = max(value, running + value)

        # Fold the local choice into the global answer.
        best = max(best, running)

    return best


def greedy_after_sort(items: List[List[int]]) -> int:
    """Sort to expose the greedy order, then take non-conflicting items.

    This is interval scheduling: sort by END, keep an item iff it starts after
    the last kept one finished.

    Time:      O(n log n) for the sort.
    Space:     O(1)
    Invariant: among all valid selections from the items seen so far, `count` is
               the largest, and `last_end` is the earliest possible finish for
               such a selection — leaving maximum room for what comes next.
    """

    # TODO: problem-specific sort key. Scheduling sorts by finish time so every
    # accepted item frees the timeline as early as possible.
    items.sort(key=lambda item: item[1])

    count = 0
    last_end = float("-inf")

    for start, end in items:
        # GREEDY CHOICE: take this item iff it doesn't conflict with the last
        # one we committed to.
        if start >= last_end:
            count += 1
            last_end = end

    return count
