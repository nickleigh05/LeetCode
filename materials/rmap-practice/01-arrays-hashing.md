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
hashset = set()               # init the hashset
for num in nums:               # for loop to iterate over data
    if num in hashset:          # if to check the number against the hashset
        return True
    hashset.add(num)            # add num if never seen
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
if len(s) != len(t):          # different lengths can't be anagrams
    return False

count = {}                     # init the hashmap
for c in s:                     # for loop over the first string
    count[c] = count.get(c, 0) + 1   # increment count for each char
for c in t:                     # for loop over the second string
    count[c] = count.get(c, 0) - 1   # decrement count for each char

return all(v == 0 for v in count.values())   # every count balanced back to 0
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
seen = {}                       # init hashmap: value -> index
for i, num in enumerate(nums):   # for loop with index and value
    complement = target - num     # what we need to complete the pair
    if complement in seen:         # if the complement was already seen
        return [seen[complement], i]
    seen[num] = i                  # remember this number's index
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
groups = defaultdict(list)      # init hashmap: signature -> list of words
for word in strs:                 # for loop over every string
    key = tuple(sorted(word))       # sorted letters as a hashable key
    groups[key].append(word)         # bucket the word under its signature
return list(groups.values())      # return the grouped lists
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [for-loop](../syntax/for-loop.md) · [sorting-key](../syntax/sorting-key.md) · [tuple-basics](../syntax/tuple-basics.md) · [list-methods](../syntax/list-methods.md) (`.append()`)
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
count = {}                       # init hashmap: value -> frequency
for num in nums:                   # for loop to count frequencies
    count[num] = count.get(num, 0) + 1

buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
for num, freq in count.items():     # for loop over counted values
    buckets[freq].append(num)         # drop num into its frequency bucket

result = []                       # collect answer highest-frequency first
for freq in range(len(buckets) - 1, 0, -1):   # walk buckets from high to low
    for num in buckets[freq]:
        result.append(num)
        if len(result) == k:            # stop once we have k elements
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
n = len(nums)
res = [1] * n                    # init result array, prefix product so far

prefix = 1
for i in range(n):                 # for loop left to right
    res[i] = prefix                  # everything to the left of i
    prefix *= nums[i]                 # extend the prefix product

postfix = 1
for i in range(n - 1, -1, -1):      # for loop right to left
    res[i] *= postfix                # fold in everything to the right of i
    postfix *= nums[i]                # extend the postfix product

return res
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

Keep a [hashset](../data-structures/hashset.md) of seen digits for each row, each column, and each 3x3 box (indexed by `(r // 3, c // 3)`). While scanning cell by cell, if a digit is already in the relevant set, the board is invalid.
</details>

<details>
<summary>Solution</summary>

```python
rows = defaultdict(set)          # row index -> seen digits
cols = defaultdict(set)          # col index -> seen digits
boxes = defaultdict(set)         # (r//3, c//3) -> seen digits

for r in range(9):                 # for loop over rows
    for c in range(9):               # nested for loop over columns
        val = board[r][c]
        if val == ".":                 # skip empty cells
            continue
        box_id = (r // 3, c // 3)       # which 3x3 box this cell belongs to
        if (val in rows[r] or             # if digit already seen in row/col/box
            val in cols[c] or
            val in boxes[box_id]):
            return False
        rows[r].add(val)                # mark digit as seen in all three
        cols[c].add(val)
        boxes[box_id].add(val)

return True
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [nested-lists](../syntax/nested-lists.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`) · [break-continue](../syntax/break-continue.md) · [membership-operators](../syntax/membership-operators.md)
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
def encode(strs):
    res = ""
    for s in strs:                   # for loop over each string
        res += str(len(s)) + "#" + s   # "<length>#<string>"
    return res

def decode(s):
    res = []
    i = 0
    while i < len(s):                 # while loop scanning the encoded string
        j = i
        while s[j] != "#":               # find the delimiter
            j += 1
        length = int(s[i:j])              # read the length before "#"
        start = j + 1
        res.append(s[start:start + length])  # slice out exactly that many chars
        i = start + length                 # jump past this string
    return res
```

Building blocks: [string-formatting](../syntax/string-formatting.md) · [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md) · [string-join-slice](../syntax/string-join-slice.md) · [type-conversion](../syntax/type-conversion.md) (`int()` / `str()`)
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
num_set = set(nums)              # init hashset for O(1) lookups
longest = 0

for num in num_set:                # for loop over unique values
    if num - 1 not in num_set:        # only start counting at sequence starts
        length = 1
        while num + length in num_set:  # while loop extending the run
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
