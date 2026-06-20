# Two Pointers

*One scan, two cursors. The whole trick is knowing which condition moves which pointer — get that right and the search space halves itself.*

## Recognize this pattern when...

- The array or string is **sorted** (or sorting it first doesn't break the problem).
- You're hunting for a **pair, triplet, or sub-range** that meets a sum/difference constraint.
- The problem demands **O(1) extra space** or "in place" — no room for a hash map.
- It's a **palindrome** check, or comparing two sequences from both directions.
- Classic geometry-on-an-array: **container / most water / trapping rain**, where two boundaries close in.

## Variations

1. **Converging sum** — `left`/`right` from the ends of a sorted array; move the pointer that nudges the sum toward target. *(Two Sum II)*
2. **Palindrome check** — ends move inward comparing characters; skip non-alphanumerics as you go. *(Valid Palindrome)*
3. **Slow/fast in-place write** — a write pointer trails a read pointer to compact or partition. *(Move Zeroes, Sort Colors)*
4. **Fix one, two-pointer the rest** — outer loop pins index `i`, inner converging scan finds the pair; skip duplicates to dedupe. *(3Sum)*
5. **Greedy boundary shrink** — move whichever end is the bottleneck (the shorter wall). *(Container With Most Water)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 125 | Easy | Valid Palindrome |
| 283 | Easy | Move Zeroes |
| 167 | Medium | Two Sum II — Input Array Is Sorted |
| 15 | Medium | 3Sum |
| 11 | Medium | Container With Most Water |
| 42 | Hard | Trapping Rain Water |

## Common bugs & traps

- **`while left <= right` vs `< right`.** Use `<` when the two pointers must land on distinct elements (pair sums); `<=` only when a single element is itself a valid candidate.
- **Forgetting to sort.** Converging pointers rely on monotonicity — an unsorted array silently gives wrong answers, not crashes.
- **Moving the wrong pointer.** Sum too small ⇒ advance `left`; too big ⇒ retreat `right`. Swap these and you walk away from the answer.
- **Duplicate triplets in 3Sum.** After recording a hit, skip over equal neighbors on *both* pointers, and skip duplicate values for the pinned index too.
- **Off-by-one on `right`.** It starts at `len(nums) - 1`, not `len(nums)`.
- **In-place writes clobbering data.** The slow/fast form is safe because `slow <= fast` always; don't reorder the read and write.
