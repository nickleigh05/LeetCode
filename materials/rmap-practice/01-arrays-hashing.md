# 01. Arrays & Hashing — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md)

---

### 217. Contains Duplicate — Easy
[LeetCode](https://leetcode.com/problems/contains-duplicate/)  
[Solution file (no hints)](../../problems/0001-0499/217.py)

Given an array of integers, determine if any value appears at least twice. What data structure gives you O(1) membership checks so you can spot a repeat while scanning once?

<details>
<summary>Hint</summary>

You want a [hashset](../data-structures/hashset.md) — O(1) average insert and lookup. Walk the array once, and check each number against the set before adding it.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:

        hashset = set()

        for num in nums:
            if num in hashset:
                return True
            hashset.add(num)
        return False
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) (the `in` check) · [if-return](../syntax/if-return.md) · [set-operations](../syntax/set-operations.md) (`.add()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every element is visited once, and each hashset lookup/insert is O(1) average.
**Space: O(n)** — worst case (no duplicates) the hashset ends up holding every element.
</details>

---

### 242. Valid Anagram — Easy
[LeetCode](https://leetcode.com/problems/valid-anagram/)  
[Solution file (no hints)](../../problems/0001-0499/242.py)

Given two strings, determine if one is an anagram of the other. How could you compare the letter counts of both strings without sorting?

<details>
<summary>Hint</summary>

Count each character's frequency with a [hashmap](../data-structures/hashmap.md) (or `Counter`) for both strings and compare the two counts.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:

        if len(s) != len(t):
            return False

        count_s = {}
        count_t = {}

        for char in s:
            count_s[char] = count_s.get(char, 0) + 1

        for char in t:
            count_t[char] = count_t.get(char, 0) + 1

        return count_s == count_t
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [dict-methods](../syntax/dict-methods.md) (`.get()`) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes over strings of length n.
**Space: O(1)** — at most 26 lowercase letters in the hashmap (bounded alphabet), so it doesn't grow with input size.
</details>

---

### 1. Two Sum — Easy
[LeetCode](https://leetcode.com/problems/two-sum/)  
[Solution file (no hints)](../../problems/0001-0499/1.py)

Given an array of integers and a target, return the indices of the two numbers that add up to the target. Instead of checking every pair, what could you remember as you scan so the complement is a single lookup away?

<details>
<summary>Hint</summary>

Use a [hashmap](../data-structures/hashmap.md) to store each number's index as you go. For each new number, check whether `target - num` has already been seen.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        hashmap = {}

        for i, num in enumerate(nums):
            diff = target - num
            if diff in hashmap:
                return [hashmap[diff], i]
            hashmap[num] = i
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [enumerate](../syntax/enumerate.md) · [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — single pass, O(1) hashmap lookups.
**Space: O(n)** — the hashmap can hold up to n entries.
</details>

---

### 49. Group Anagrams — Medium
[LeetCode](https://leetcode.com/problems/group-anagrams/)  
[Solution file (no hints)](../../problems/0001-0499/49.py)

Given an array of strings, group the anagrams together. What key could two anagram strings share so you can bucket them in a hashmap?

<details>
<summary>Hint</summary>

Anagrams share the same sorted-character signature (or the same 26-letter count). Use a [hashmap](../data-structures/hashmap.md) keyed by that signature, mapping to a list of the original strings.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        hashmap = {}

        for word in strs:
            key = "".join(sorted(word))

            if key not in hashmap:
                hashmap[key] = []

            hashmap[key].append(word)

        return list(hashmap.values())
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [for-loop](../syntax/for-loop.md) · [sorting-key](../syntax/sorting-key.md) (`sorted()`) · [string-join-slice](../syntax/string-join-slice.md) (`"".join()`) · [list-methods](../syntax/list-methods.md) (`.append()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · k log k)** — n words, each sorted in O(k log k) where k is the word's length.
**Space: O(n · k)** — storing every string once, grouped in the hashmap.
</details>

---

### 347. Top K Frequent Elements — Medium
[LeetCode](https://leetcode.com/problems/top-k-frequent-elements/)  
[Solution file (no hints)](../../problems/0001-0499/347.py)

Given an array, return the k most frequent elements. Once you know each element's frequency, what's an O(n) way to pick the top k without a full sort?

<details>
<summary>Hint</summary>

Count frequencies with a [hashmap](../data-structures/hashmap.md), then bucket elements by frequency in an array indexed 0..n (bucket sort) — no need for a full O(n log n) sort or even a heap.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        count = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1

        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)

        result = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result
```

Building blocks: [dict-methods](../syntax/dict-methods.md) (`.get()`, `.items()`) · [list-comprehension](../syntax/list-comprehension.md) · [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — counting is O(n), bucket sort is O(n) since frequencies are bounded by n.
**Space: O(n)** — the hashmap and the buckets array both scale with n.
</details>

---

### 238. Product of Array Except Self — Medium
[LeetCode](https://leetcode.com/problems/product-of-array-except-self/)  
[Solution file (no hints)](../../problems/0001-0499/238.py)

Return an array where each element is the product of all other elements, without using division. What two passes over the array — one from the left, one from the right — give you everything you need?

<details>
<summary>Hint</summary>

For each index, the answer is `(product of everything to its left) × (product of everything to its right)`. Compute prefix products in one pass, then fold in suffix products in a second pass — see [prefix sums](../learning/01b-prefix-sums.md) for the same idea applied to sums.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        answer = [1] * len(nums)

        prefix = 1
        for i in range(len(nums)):
            answer[i] = prefix
            prefix *= nums[i]

        suffix = 1
        for i in range(len(nums) - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer
```

Building blocks: [list-basics](../syntax/list-basics.md) · [range-function](../syntax/range-function.md) (reverse step) · [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`*=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes over the array.
**Space: O(1)** extra — excluding the output array, only a couple of running products are kept.
</details>

---

### 36. Valid Sudoku — Medium
[LeetCode](https://leetcode.com/problems/valid-sudoku/)  
[Solution file (no hints)](../../problems/0001-0499/36.py)

Given a 9x9 board, determine if the filled cells satisfy Sudoku rules. How could a hashset per row, per column, and per 3x3 box let you check all three constraints in a single scan?

<details>
<summary>Hint</summary>

Keep a [hashset](../data-structures/hashset.md) of seen digits for each row, each column, and each 3x3 box (indexed by `(row // 3) * 3 + (col // 3)`). While scanning cell by cell, if a digit is already in the relevant set, the board is invalid.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        row_sets = [set() for _ in range(9)]
        col_sets = [set() for _ in range(9)]
        box_sets = [set() for _ in range(9)]

        for row in range(9):
            for col in range(9):
                cell = board[row][col]

                if cell == ".":
                    continue

                box = (row // 3) * 3 + (col // 3)

                if cell in row_sets[row]:
                    return False
                row_sets[row].add(cell)

                if cell in col_sets[col]:
                    return False
                col_sets[col].add(cell)

                if cell in box_sets[box]:
                    return False
                box_sets[box].add(cell)

        return True
```

Building blocks: [list-comprehension](../syntax/list-comprehension.md) · [nested-lists](../syntax/nested-lists.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`) · [break-continue](../syntax/break-continue.md) (`continue`) · [membership-operators](../syntax/membership-operators.md) · [set-operations](../syntax/set-operations.md) (`.add()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** — the board is a fixed 9x9, so 81 cells is a constant amount of work regardless of "n".
**Space: O(1)** — at most 9 rows × 9 cols × 9 boxes of hashsets, each bounded by 9 digits.
</details>

---

### 271. Encode and Decode Strings — Medium
[LeetCode](https://leetcode.com/problems/encode-and-decode-strings/)  
[Solution file (no hints)](../../problems/0001-0499/271.py)

Design an algorithm to encode a list of strings into one string, and decode it back — the strings may contain any character, including your delimiter. How do you record each string's length so decoding is unambiguous?

<details>
<summary>Hint</summary>

Prefix each string with its length and a delimiter the decoder can rely on structurally, e.g. `"5#hello"`. Since the length is read before the delimiter, the delimiter itself never needs to be escaped.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:

    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.index("#", i)
            length = int(s[i:j])
            result.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return result
```

Building blocks: [f-strings](../syntax/f-strings.md) · [generator-expressions](../syntax/generator-expressions.md) · [while-loop](../syntax/while-loop.md) · [string-methods](../syntax/string-methods.md) (`.index()`) · [string-join-slice](../syntax/string-join-slice.md) · [type-conversion](../syntax/type-conversion.md) (`int()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — encoding and decoding each touch every character once, where n is the total length of all strings.
**Space: O(n)** — the encoded string and decoded list both scale with the total input size.
</details>

---

### 128. Longest Consecutive Sequence — Medium
[LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/)  
[Solution file (no hints)](../../problems/0001-0499/128.py)

Given an unsorted array of integers, find the length of the longest run of consecutive integers, in O(n) time. Without sorting, how do you know where a consecutive run *starts*?

<details>
<summary>Hint</summary>

Put every number in a [hashset](../data-structures/hashset.md). A number is the *start* of a sequence only if `num - 1` isn't in the set. From each start, count upward (`num + 1`, `num + 2`, ...) while those values exist in the set.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        num_set = set(nums)
        longest = 0

        for num in num_set:
            if (num - 1) not in num_set:
                length = 1
                while (num + length) in num_set:
                    length += 1
                longest = max(longest, length)
        return longest
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) (`not in`) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each number is only ever the start of its run once, so the inner while loop across all iterations totals O(n) amortized.
**Space: O(n)** — the hashset holds every number.
</details>
