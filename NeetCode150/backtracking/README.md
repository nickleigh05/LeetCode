# Backtracking

## 10. Backtracking (9 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 78 | Medium | Subsets | [Link](https://leetcode.com/problems/subsets/) |
| 39 | Medium | Combination Sum | [Link](https://leetcode.com/problems/combination-sum/) |
| 46 | Medium | Permutations | [Link](https://leetcode.com/problems/permutations/) |
| 90 | Medium | Subsets II | [Link](https://leetcode.com/problems/subsets-ii/) |
| 40 | Medium | Combination Sum II | [Link](https://leetcode.com/problems/combination-sum-ii/) |
| 79 | Medium | Word Search | [Link](https://leetcode.com/problems/word-search/) |
| 131 | Medium | Palindrome Partitioning | [Link](https://leetcode.com/problems/palindrome-partitioning/) |
| 17 | Medium | Letter Combinations of a Phone Number | [Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) |
| 51 | Hard | N-Queens | [Link](https://leetcode.com/problems/n-queens/) |

---

## Data Structures

### Recursion Stack (implicit)
Backtracking uses the call stack to undo decisions. There's no explicit data structure — just recursive function calls where you add a choice, recurse deeper, and then remove that choice when you return (the "undo" step).

### Current Path (list)
A mutable list that represents the choices made so far. You append to it before recursing and pop from it after returning — this is the "backtrack" step.

---

## Core Patterns

### Choose → Explore → Unchoose
The universal backtracking template:
```python
def backtrack(start, path):
    if is_solution(path):
        result.append(path[:])  # make a copy
        return
    for choice in choices_from(start):
        path.append(choice)      # choose
        backtrack(next, path)    # explore
        path.pop()               # unchoose
```

### Subsets (Power Set)
At each index, you either include or exclude the current element. Use a `start` index to avoid going backwards. Used in Subsets.

### Combinations
Pick elements in order (always move `start` forward) to avoid duplicate combinations. You can reuse elements (Combination Sum) or not (Combination Sum II). For problems with duplicate input values, sort first and skip duplicates at the same recursion level.

### Permutations
Order matters, so you consider every unused element at each step. Track which elements are used with a boolean array or by swapping. Each call to the recursion picks from all remaining unused elements.

### Skip Duplicates (Subsets II, Combination Sum II)
Sort the input first. In the for loop, if `nums[i] == nums[i-1]` and `i > start`, skip — this avoids generating duplicate subsets/combinations at the same recursion depth.

### Grid DFS with Visited Marking
Mark a cell as visited before recursing into it (e.g. set it to `#`). Unmark it when backtracking. Explore all 4 directions. Used in Word Search.

### Constraint Pruning
Before recursing, check if the current state can possibly lead to a solution. If not, return early. In N-Queens, track which columns, diagonals, and anti-diagonals are under attack — O(1) check per placement.
