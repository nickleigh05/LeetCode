# 10. Backtracking — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md)

---

### 78. Subsets — Medium
[LeetCode](https://leetcode.com/problems/subsets/)  
[Solution file (no hints)](../../problems/0001-0499/78.py)

Return all possible subsets of a set of distinct integers. At each element, what are the two choices you make, and how does undoing one before trying the other build every combination?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md) index by index: for each element, either include it or don't, recursing both ways and popping it back off before trying the other branch.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:

        result = []
        subset = []

        def backtrack(i):
            if i == len(nums):
                result.append(subset[:])
                return

            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()

            backtrack(i + 1)

        backtrack(0)
        return result
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) (`path[:]`) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · 2ⁿ)** — 2ⁿ subsets, each up to O(n) to copy.
**Space: O(n)** recursion depth, plus O(n · 2ⁿ) for the output.
</details>

---

### 39. Combination Sum — Medium
[LeetCode](https://leetcode.com/problems/combination-sum/)  
[Solution file (no hints)](../../problems/0001-0499/39.py)

Given distinct candidates and a target, find all combinations that sum to target (each candidate reusable unlimited times). Since candidates can repeat, why does the recursive call stay at the same index instead of advancing?

<details>
<summary>Hint</summary>

Sort first, then [backtrack](../algorithms/backtracking.md) with a running remaining target: from index `i`, try each candidate at or after `i`, recursing *without* advancing the index (reuse is allowed). Because the list is sorted, you can stop the loop as soon as a candidate exceeds what remains.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        result = []
        candidates.sort()

        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i], path)
                path.pop()

        backtrack(0, target, [])
        return result
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [list-methods](../syntax/list-methods.md) (`.sort()`, `.append()`, `.pop()`) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) (`break`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(2^(target/min_candidate))** in the worst case — bounded by how many ways sums can be composed.
**Space: O(target/min_candidate)** recursion depth.
</details>

---

### 46. Permutations — Medium
[LeetCode](https://leetcode.com/problems/permutations/)  
[Solution file (no hints)](../../problems/0001-0499/46.py)

Return all permutations of a list of distinct integers. Why do you need a "used" tracker here, unlike Subsets, where each element is only ever considered once per branch?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md) by trying every not-yet-used number at each position; mark it used, recurse to fill the next position, then un-mark it before trying the next candidate.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        res = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            if len(path) == len(nums):
                res.append(path[:])
                return

            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return res
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [list-basics](../syntax/list-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · n!)** — n! permutations, each O(n) to build.
**Space: O(n)** recursion depth, plus O(n · n!) for the output.
</details>

---

### 90. Subsets II — Medium
[LeetCode](https://leetcode.com/problems/subsets-ii/)  
Solution: not yet solved in this repo.

Return all unique subsets of a list that may contain duplicates. After sorting, why does skipping a duplicate value *at the same recursion depth* (but not across depths) avoid duplicate subsets?

<details>
<summary>Hint</summary>

Sort first so duplicates are adjacent. [Backtrack](../algorithms/backtracking.md) as in [78](#78-subsets--medium), but within a single for-loop level, skip any candidate equal to the previous one you just returned from — that prevents generating the same subset twice.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:

        nums.sort()
        result = []
        path = []

        def backtrack(start):
            result.append(path[:])

            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
```

Building blocks: [list-methods](../syntax/list-methods.md) (`.sort()`) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · 2ⁿ)** — same shape as Subsets, with duplicate-skipping pruning some branches.
**Space: O(n)** recursion depth, plus output size.
</details>

---

### 40. Combination Sum II — Medium
[LeetCode](https://leetcode.com/problems/combination-sum-ii/)  
Solution: not yet solved in this repo.

Each candidate may only be used once, and the list may contain duplicates — find all unique combinations summing to target. How do this problem's "no reuse" and "skip duplicates at the same depth" rules combine [39](#39-combination-sum--medium) and [90](#90-subsets-ii--medium)?

<details>
<summary>Hint</summary>

Sort first. [Backtrack](../algorithms/backtracking.md) advancing the index every time (no reuse, unlike 39), and within one for-loop level skip a candidate equal to the previous one already tried (no duplicate combinations, like 90).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        candidates.sort()
        result = []
        path = []

        def backtrack(start, remaining):
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remaining:
                    break
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return result
```

Building blocks: [list-methods](../syntax/list-methods.md) (`.sort()`) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [recursion-basics](../syntax/recursion-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(2ⁿ)** worst case across all subsets of candidates.
**Space: O(n)** recursion depth, plus output size.
</details>

---

### 79. Word Search — Medium
[LeetCode](https://leetcode.com/problems/word-search/)  
Solution: not yet solved in this repo.

Given a grid and a word, determine if the word can be traced through adjacent cells without reusing a cell. Why must a visited cell be un-marked after exploring its neighbors, before trying a *different* path through it?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md)/DFS from every starting cell: mark a cell visited, try all 4 neighbors for the next letter, then un-mark it (that's the "backtrack" — a cell can be reused by a different path).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:

        rows = len(board)
        cols = len(board[0])

        def dfs(row, col, i):
            if i == len(word):
                return True
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            if board[row][col] != word[i]:
                return False

            letter = board[row][col]
            board[row][col] = "#"

            found = (dfs(row + 1, col, i + 1) or
                     dfs(row - 1, col, i + 1) or
                     dfs(row, col + 1, i + 1) or
                     dfs(row, col - 1, i + 1))

            board[row][col] = letter
            return found

        for row in range(rows):
            for col in range(cols):
                if dfs(row, col, 0):
                    return True
        return False
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md) (`or`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols · 4^L)** — L is the word's length; each cell can branch 4 ways at each step.
**Space: O(L)** recursion depth.
</details>

---

### 131. Palindrome Partitioning — Medium
[LeetCode](https://leetcode.com/problems/palindrome-partitioning/)  
Solution: not yet solved in this repo.

Partition a string so every substring is a palindrome; return all such partitions. At each position, what choice are you making about where to make the *next* cut?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md) over cut positions: at index `i`, try every possible end of the next piece; only recurse further if that piece is itself a palindrome.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:

        result = []
        path = []

        def is_palindrome(piece):
            return piece == piece[::-1]

        def backtrack(start):
            if start == len(s):
                result.append(path[:])
                return

            for end in range(start + 1, len(s) + 1):
                piece = s[start:end]
                if is_palindrome(piece):
                    path.append(piece)
                    backtrack(end)
                    path.pop()

        backtrack(0)
        return result
```

Building blocks: [list-slicing](../syntax/list-slicing.md) (`sub[::-1]`) · [for-loop](../syntax/for-loop.md) · [recursion-basics](../syntax/recursion-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · 2ⁿ)** — up to 2ⁿ partitions, each palindrome check up to O(n).
**Space: O(n)** recursion depth, plus output size.
</details>

---

### 17. Letter Combinations of a Phone Number — Medium
[LeetCode](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)  
Solution: not yet solved in this repo.

Given digits 2-9, return all letter combinations the number could represent. How does mapping each digit to its letters, then backtracking one digit at a time, build every combination?

<details>
<summary>Hint</summary>

Use a [hashmap](../data-structures/hashmap.md) of digit -> letters. [Backtrack](../algorithms/backtracking.md) one digit at a time: for each letter that digit could be, append it and recurse into the next digit.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:

        if not digits:
            return []

        digit_to_letters = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }

        result = []
        path = []

        def backtrack(i):
            if i == len(digits):
                result.append("".join(path))
                return

            for letter in digit_to_letters[digits[i]]:
                path.append(letter)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [string-join-slice](../syntax/string-join-slice.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(3ⁿ to 4ⁿ)** — n digits, each contributing 3 or 4 letters.
**Space: O(n)** recursion depth, plus output size.
</details>

---

### 51. N-Queens — Hard
[LeetCode](https://leetcode.com/problems/n-queens/)  
Solution: not yet solved in this repo.

Place n queens on an n×n board so none attack each other; return all solutions. Since exactly one queen goes in each row, what three hashsets let you check "is this column/diagonal already attacked" in O(1)?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md) row by row, placing one queen per row. Track attacked columns and both diagonals (`row - col` and `row + col` are constant along a diagonal) in [hashsets](../data-structures/hashset.md) to check placements in O(1).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:

        result = []
        cols = set()
        pos_diag = set()   # row + col is constant along this diagonal
        neg_diag = set()   # row - col is constant along this diagonal
        board = [["."] * n for _ in range(n)]

        def backtrack(row):
            if row == n:
                result.append(["".join(r) for r in board])
                return

            for col in range(n):
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)
                board[row][col] = "Q"

                backtrack(row + 1)

                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)
                board[row][col] = "."

        backtrack(0)
        return result
```

Building blocks: [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n!)** — roughly n choices in the first row, n-2 in the next valid row, and so on.
**Space: O(n²)** for the board, plus O(n) recursion depth.
</details>
