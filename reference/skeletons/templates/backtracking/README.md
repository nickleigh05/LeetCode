# Backtracking

*Explore every possibility, prune early. Build → recurse → undo. That three-beat loop is the whole template — the art is in the pruning.*

## Recognize this pattern when...

- The problem says **"find all / generate all / return every"** combination, permutation, subset, or partition.
- The output is itself **exponential** (all 2ⁿ subsets, all n! permutations).
- You must place items under **constraints** (N-Queens, Sudoku, valid IP addresses).
- A **grid search** must try paths and reverse course on dead ends (Word Search).
- Greedy/DP won't work because you genuinely need to *enumerate*, not just count or optimize.

## Variations

1. **Subsets** — record at *every* node; recurse with `index + 1`. *(Subsets)*
2. **Combinations / Combination Sum** — fixed length or a target; `index + 1` forbids reuse, `index` allows it. *(Combination Sum)*
3. **Permutations** — start each level from 0, track a `used` set so each element appears once. *(Permutations)*
4. **Duplicate handling** — sort first, then skip equal siblings (`nums[i] == nums[i-1]`). *(Subsets II, Permutations II)*
5. **Grid backtracking** — mark a cell visited, explore 4 directions, then unmark. *(Word Search)*
6. **Constraint placement** — track column / diagonal occupancy sets, place and remove. *(N-Queens)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 78 | Medium | Subsets |
| 39 | Medium | Combination Sum |
| 46 | Medium | Permutations |
| 79 | Medium | Word Search |
| 131 | Medium | Palindrome Partitioning |
| 51 | Hard | N-Queens |

## Common bugs & traps

- **Storing the path by reference.** `results.append(path)` saves a pointer that keeps mutating — append `list(path)` (a copy).
- **Forgetting to un-choose.** Every `append` / mark needs a matching `pop` / unmark, or state leaks into sibling branches.
- **Wrong recursion index.** `index + 1` (no reuse) vs `index` (reuse) vs `0 + used[]` (permutations) — picking wrong silently changes the problem.
- **Duplicate skipping without sorting.** The `nums[i] == nums[i-1]` skip only works on a *sorted* input.
- **Permutations reusing elements.** Without a `used` set you'll emit `[1,1]` from `[1,2]`.
- **Grid: not restoring the visited mark.** Unmark the cell after exploring, or later paths can't legally cross it.
