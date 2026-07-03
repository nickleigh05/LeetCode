# 10. Backtracking — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

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
res = []
path = []

def backtrack(i):
    if i == len(nums):                  # base case: considered every element
        res.append(path[:])              # copy, since path keeps mutating
        return

    path.append(nums[i])                  # choice 1: include nums[i]
    backtrack(i + 1)
    path.pop()                              # un-choose

    backtrack(i + 1)                       # choice 2: exclude nums[i]

backtrack(0)
return res
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

[Backtrack](../algorithms/backtracking.md) with a running remaining target: at index `i`, either take `candidates[i]` again (recurse without advancing `i`, since reuse is allowed) or move on to `i + 1`. Stop a branch once the remaining target goes negative or hits zero.
</details>

<details>
<summary>Solution</summary>

```python
res = []
path = []

def backtrack(i, remaining):
    if remaining == 0:                   # base case: exact sum reached
        res.append(path[:])
        return
    if i >= len(candidates) or remaining < 0:  # out of candidates or overshot
        return

    path.append(candidates[i])             # choice 1: reuse candidates[i]
    backtrack(i, remaining - candidates[i])
    path.pop()                               # un-choose

    backtrack(i + 1, remaining)             # choice 2: move past candidates[i]

backtrack(0, target)
return res
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`)
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
res = []
path = []
used = [False] * len(nums)

def backtrack():
    if len(path) == len(nums):           # base case: a full permutation
        res.append(path[:])
        return

    for i in range(len(nums)):             # for loop trying every candidate
        if used[i]:                          # already placed in this permutation
            continue
        used[i] = True
        path.append(nums[i])
        backtrack()
        path.pop()                             # un-choose
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
nums.sort()                             # group duplicates together
res = []
path = []

def backtrack(start):
    res.append(path[:])                    # every path so far is a valid subset

    for i in range(start, len(nums)):        # for loop over remaining candidates
        if i > start and nums[i] == nums[i - 1]:  # skip duplicates at this depth
            continue
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()                             # un-choose

backtrack(0)
return res
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
candidates.sort()
res = []
path = []

def backtrack(start, remaining):
    if remaining == 0:                    # base case: exact sum reached
        res.append(path[:])
        return
    if remaining < 0:
        return

    for i in range(start, len(candidates)):  # for loop over remaining candidates
        if i > start and candidates[i] == candidates[i - 1]:  # skip duplicates at this depth
            continue
        if candidates[i] > remaining:          # sorted: no point trying larger values
            break
        path.append(candidates[i])
        backtrack(i + 1, remaining - candidates[i])   # advance past i: no reuse
        path.pop()

backtrack(0, target)
return res
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
rows, cols = len(board), len(board[0])

def dfs(r, c, i):                       # i = index into word we're trying to match
    if i == len(word):                    # base case: matched the whole word
        return True
    if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[i]):        # out of bounds or letter mismatch
        return False

    tmp = board[r][c]
    board[r][c] = "#"                       # mark visited so this path can't reuse it

    found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
             dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))

    board[r][c] = tmp                        # un-mark (backtrack)
    return found

for r in range(rows):
    for c in range(cols):
        if dfs(r, c, 0):
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
res = []
path = []

def is_palindrome(sub):
    return sub == sub[::-1]

def backtrack(start):
    if start == len(s):                  # base case: reached the end of the string
        res.append(path[:])
        return

    for end in range(start + 1, len(s) + 1):  # for loop over every possible next piece
        piece = s[start:end]
        if is_palindrome(piece):              # only recurse on valid palindrome pieces
            path.append(piece)
            backtrack(end)
            path.pop()

backtrack(0)
return res
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
if not digits:
    return []

digit_to_letters = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}
res = []
path = []

def backtrack(i):
    if i == len(digits):                 # base case: one letter chosen per digit
        res.append("".join(path))
        return

    for letter in digit_to_letters[digits[i]]:  # for loop over this digit's letters
        path.append(letter)
        backtrack(i + 1)
        path.pop()

backtrack(0)
return res
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
res = []
cols = set()
pos_diag = set()                        # r + c is constant along this diagonal
neg_diag = set()                        # r - c is constant along this diagonal
board = [["."] * n for _ in range(n)]

def backtrack(r):
    if r == n:                            # base case: placed a queen in every row
        res.append(["".join(row) for row in board])
        return

    for c in range(n):                      # for loop trying every column in this row
        if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
            continue                          # under attack, skip

        cols.add(c); pos_diag.add(r + c); neg_diag.add(r - c)
        board[r][c] = "Q"

        backtrack(r + 1)

        cols.remove(c); pos_diag.remove(r + c); neg_diag.remove(r - c)  # un-choose
        board[r][c] = "."

backtrack(0)
return res
```

Building blocks: [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n!)** — roughly n choices in the first row, n-2 in the next valid row, and so on.
**Space: O(n²)** for the board, plus O(n) recursion depth.
</details>
