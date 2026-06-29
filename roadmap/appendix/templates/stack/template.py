"""
Stack — Monotonic Stack and Matching Skeletons

A stack gives you LIFO access, which is exactly what you want when the answer
for an element depends on the most recent *earlier* element that is still
unresolved. Two shapes dominate:

  1. MONOTONIC stack — keep the stack sorted (increasing or decreasing). The
                       moment a new element breaks the order you pop, and each
                       pop is an element finding its answer.
  2. MATCHING stack  — push openers / operands, pop to pair them with closers /
                       operators (parentheses, expression evaluation).

Invariant (monotonic): the stack holds, bottom to top, the indices whose answer
is still pending, in monotonic order of value. An element stays on the stack
only until something that resolves it arrives.
"""

from typing import Dict, List


def monotonic_stack(nums: List[int]) -> List[int]:
    """For each element, find the next element that breaks the monotonic order.

    This version finds the Next Greater Element to the right (a decreasing stack
    of indices). Flip the comparison for next-smaller; iterate in reverse for
    "to the left".

    Time:      O(n) — each index is pushed once and popped at most once.
    Space:     O(n) — worst case (already sorted) the whole array sits on it.
    Invariant: values at the indices on the stack strictly decrease from bottom
               to top, so the first element that exceeds the top resolves a
               contiguous run of pending elements in one sweep.
    """

    result = [-1] * len(nums)  # default: "no qualifying element found"
    stack: List[int] = []      # indices with no answer yet, decreasing by value

    for index in range(len(nums)):
        # TODO: problem-specific comparison. `>` means "current is greater than
        # the pending element", i.e. current IS that element's next-greater.
        while stack and nums[index] > nums[stack[-1]]:
            resolved_index = stack.pop()
            # TODO: store the value, the index, or the distance (index - resolved_index).
            result[resolved_index] = nums[index]

        # current is now pending; it waits for whatever breaks the order next.
        stack.append(index)

    # Anything still on the stack never found an answer; it keeps the default.
    return result


def matching_stack(tokens: str) -> bool:
    """Pair nested openers with closers using LIFO order.

    Time:      O(n)
    Space:     O(n) — the depth of nesting in the worst case.
    Invariant: the stack holds every opener seen so far that has not yet been
               closed, in the exact order it must be closed (most recent first).
    """

    stack: List[str] = []
    # TODO: problem-specific pairing rule (closer -> required opener).
    pairs: Dict[str, str] = {")": "(", "]": "[", "}": "{"}

    for token in tokens:
        if token not in pairs:
            # An opener (or, in evaluation problems, an operand to push).
            stack.append(token)
        else:
            # A closer must match the most recent unclosed opener exactly.
            if not stack or stack.pop() != pairs[token]:
                return False

    # Valid only if every opener was eventually closed.
    return not stack
