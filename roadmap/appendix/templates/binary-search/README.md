# Binary Search

*If the search space is ordered, halve it. The real skill is spotting the hidden monotonic predicate — binary search works on answers, not just arrays.*

## Recognize this pattern when...

- The array is **sorted**, or you can phrase the problem as monotone (a `True/False` test that flips exactly once).
- The target runtime is **O(log n)** or the input is huge (10⁹+).
- The wording is **"minimize the maximum"**, **"maximize the minimum"**, or **"smallest/largest x such that ... is feasible"**.
- A linear scan over the *answer space* (speeds, capacities, lengths) is too slow but feasibility is cheap to check.
- The array is **sorted but rotated**, or you need the **first/last occurrence** of a value.

## Variations

1. **Find exact** — `left <= right`, return on equality. *(Binary Search)*
2. **Leftmost / first True** — lower_bound; `high = mid` on success. *(Search Insert Position, first position of target)*
3. **Rightmost / last True** — upper_bound minus one; bias `mid` upward or search the complement predicate. *(Find First and Last Position)*
4. **Rotated array** — at each step one half is sorted; decide which, then check if the target lies inside it. *(Search in Rotated Sorted Array)*
5. **Binary search on the answer** — the search space is a numeric range, the predicate is a feasibility check. *(Koko Eating Bananas, Capacity to Ship Packages)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 704 | Easy | [Binary Search](../../../../problems/0500-0999/704.py) |
| 35 | Easy | [Search Insert Position](../../../../problems/0001-0499/35.py) |
| 153 | Medium | Find Minimum in Rotated Sorted Array |
| 33 | Medium | Search in Rotated Sorted Array |
| 875 | Medium | Koko Eating Bananas |
| 4 | Hard | Median of Two Sorted Arrays |

## Common bugs & traps

- **Infinite loops.** In the boundary form, `low = mid` (without `+ 1`) can stall forever when `mid == low`. Always make progress: `low = mid + 1` on the failing side.
- **`<` vs `<=` mismatch.** `left <= right` pairs with `mid ± 1` updates; `left < right` pairs with `high = mid`. Mixing them off-by-ones the result.
- **Overflow mid.** Use `left + (right - left) // 2`. (Harmless in Python, a real bug in C/Java — and interviewers notice.)
- **Wrong return for "insert position".** When the target is absent, `left` (not `left - 1`) is where it would go.
- **Rotated array: picking the sorted half wrong.** Compare `nums[mid]` against `nums[left]` (or `nums[right]`) consistently to identify the sorted side before deciding where the target is.
- **Forgetting duplicates.** In a rotated array with duplicates, `nums[left] == nums[mid] == nums[right]` forces a linear shrink (`left += 1`) — the clean O(log n) guarantee is lost.
---

*See also: [Lesson 05 →](../../../learning/05-binary-search.md) · [🗺 Roadmap](../../../roadmap.md) · [problem lists](../../../../lists/)*
