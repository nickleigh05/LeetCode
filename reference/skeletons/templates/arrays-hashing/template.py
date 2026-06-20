"""
Arrays & Hashing — One-Pass Hash Map Skeleton

The core idea: trade space for time. A hash map (dict) or hash set turns an
O(n) membership scan into an O(1) lookup, which collapses an O(n^2) brute-force
double loop down to a single O(n) pass.

There are two canonical shapes:

  1. Complement / "have I already seen what I need?"  -> dict or set, one pass.
  2. Frequency counting / grouping by a derived key    -> dict of counts/buckets.

Both share the same invariant: at the moment you process index i, the hash
structure holds a fully-correct summary of everything in nums[0 .. i-1]. You
answer the question for element i using only that summary, then fold element i
into the summary for whoever comes next.
"""

from typing import Dict, List, Optional


def one_pass_complement(nums: List[int], target: int) -> Optional[List[int]]:
    """Find two indices whose values combine to satisfy a target relation.

    Time:      O(n) — each element is visited once, every dict op is O(1).
    Space:     O(n) — the map can hold up to n - 1 earlier elements.
    Invariant: `seen` contains every value in nums[0 .. i-1] mapped to its
               index, so the complement check below only ever pairs i with an
               element that genuinely came before it (no element pairs itself).
    """

    # Maps a previously-seen value -> the index it appeared at. We look up the
    # complement *before* inserting the current value, which is what guarantees
    # i != j without an explicit equality check.
    seen: Dict[int, int] = {}

    for index in range(len(nums)):
        current_value = nums[index]

        # TODO: problem-specific complement. For two-sum this is the value that
        # would complete the target; other problems derive a different key from
        # current_value (e.g. current_value - k, or a canonical form).
        needed_value = target - current_value

        # If the thing we need was already recorded, we have our answer. This is
        # the whole point of the pattern: the "did I see it?" question is O(1).
        if needed_value in seen:
            return [seen[needed_value], index]

        # Record current_value only AFTER the check, so it is visible to
        # everyone who comes after index i but never matches itself.
        seen[current_value] = index

    return None


def frequency_map(nums: List[int]) -> Dict[int, int]:
    """Count how many times each distinct key occurs, in a single pass.

    Time:      O(n)
    Space:     O(k) where k is the number of distinct keys.
    Invariant: after processing nums[0 .. i], counts[x] equals exactly the
               number of times x appeared in that prefix.
    """

    counts: Dict[int, int] = {}

    for value in nums:
        # TODO: problem-specific key. Often `value` itself, but could be a
        # canonical form: sorted(word) for anagram grouping, value % k for
        # bucketing, or a tuple of features.
        key = value

        # dict.get keeps the "first time we see a key" case branch-free.
        counts[key] = counts.get(key, 0) + 1

    return counts
