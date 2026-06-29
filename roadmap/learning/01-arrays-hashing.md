# 01. Arrays & Hashing
*The foundation. Hash maps trade memory for O(1) lookups and quietly power half of all interview solutions.*

[← Prev](00-foundations.md) · [🗺 Roadmap](../roadmap.md) · [Next →](02-two-pointers.md)

---

Everything starts here. An **array** is a contiguous block of memory you index in O(1); a **hash map** lets you ask "have I seen this before?" in O(1) instead of rescanning. The instant you find yourself writing a nested loop to compare every pair, ask whether a hash map could remember what you've already seen and collapse it to a single pass. **Prefix sums** extend the same memory-for-speed trade to range queries. Master this lesson and you'll recognize the move in dozens of later problems.

## Concept

### Array

```
Index:  0    1    2    3    4    5
      ┌────┬────┬────┬────┬────┬────┐
Value:│ 3  │ 1  │ 4  │ 1  │ 5  │ 9  │
      └────┴────┴────┴────┴────┴────┘
         ↑                        ↑
       O(1) access             O(1) append
```

**What it is:** A contiguous sequence of elements stored in memory, accessible in O(1) time by index. Python's `list` is a dynamic array that resizes automatically.

**Key Properties:**
- Random access via index in O(1)
- Insertion/deletion in the middle shifts elements → O(n)
- Appending to the end is O(1) amortized (occasionally resizes)
- Elements are ordered — position matters

**Complexity:**

| Operation | Average | Notes |
|-----------|---------|-------|
| Access by index | O(1) | Direct memory offset |
| Search (unsorted) | O(n) | Must scan linearly |
| Search (sorted) | O(log n) | With Binary Search |
| Insert at end | O(1) amortized | Occasional resize |
| Insert at middle | O(n) | Shift elements right |
| Delete at end | O(1) | |
| Delete at middle | O(n) | Shift elements left |
| Space | O(n) | |

**Use when:**
- You need O(1) index-based access
- You are appending/reading from the end frequently
- Order of elements matters
- You need to apply binary search (must be sorted)

**Python:**
```python
arr = [1, 2, 3, 4, 5]
arr.append(6)          # O(1) amortized
arr.insert(2, 99)      # O(n) - insert at index 2
arr.pop()              # O(1) - remove last
arr.pop(2)             # O(n) - remove at index
arr[2]                 # O(1) - access by index
arr[1:4]               # O(k) - slice, k = length of slice
```

### String

```
  s = "h  e  l  l  o"
       0  1  2  3  4    ← indices
       ↑              ↑
     s[0]='h'       s[4]='o'
     s[-1]='o'  (negative indexing wraps around)

  Slicing:
  s[1:4]  →  "ell"   (start inclusive, end exclusive)
  s[::-1] →  "olleh" (reverse)
```

**What it is:** An immutable sequence of characters. In Python, strings cannot be modified in place — any "change" creates a new string.

**Key Properties:**
- Immutable: `s[0] = 'x'` raises `TypeError`
- Concatenation with `+` is O(n+m) — avoid in loops; use `''.join(list)` instead
- String comparison is O(n) (character by character)
- `ord(c)` converts char to integer; `chr(n)` converts back

**Complexity:**

| Operation | Time | Notes |
|-----------|------|-------|
| Access `s[i]` | O(1) | |
| Slice `s[i:j]` | O(j-i) | Creates new string |
| Concat `s + t` | O(n+m) | Avoid in loops |
| `''.join(lst)` | O(n) | Preferred for building strings |
| `in` / `find` | O(n·m) | Naive substring search |
| Split / Strip | O(n) | |

**Use when:**
- Working with character frequency (anagrams, permutations)
- Palindrome checks
- Substring matching or extraction
- Encoding/decoding problems

**Python:**
```python
s = "hello world"
s.lower()              # "hello world"
s.upper()              # "HELLO WORLD"
s.split(" ")           # ["hello", "world"]
s.replace("l", "r")   # "herro worrd"
s[::-1]                # "dlrow olleh"  (reverse)
"".join(["a","b","c"]) # "abc"
ord("a")               # 97
chr(97)                # "a"

from collections import Counter
Counter("banana")      # {'a': 3, 'n': 2, 'b': 1}
```

### Hash Map and Hash Set

```
  Hash Map (dict):                Hash Set (set):
  ┌─────────────────────────┐    ┌───────────────┐
  │ Key      │ Value         │    │   Elements     │
  ├──────────┼───────────────┤    ├───────────────┤
  │ "apple"  │  5            │    │   "apple"      │
  │ "banana" │  3            │    │   "banana"     │
  │ "cherry" │  1            │    │   "cherry"     │
  └─────────────────────────┘    └───────────────┘
       O(1) avg lookup                O(1) avg lookup
                                      (no duplicates)

  Hashing:
  key ──→ hash(key) ──→ bucket index ──→ value
```

**What it is:** A data structure that maps keys to values (HashMap) or just stores unique keys (HashSet) using a hash function for O(1) average-case access.

**Key Properties:**
- Average O(1) for insert, delete, lookup
- Worst case O(n) due to hash collisions (rare with good hash functions)
- Unordered (Python 3.7+ dicts preserve insertion order, but don't rely on sorted order)
- Keys must be hashable (immutable types: int, str, tuple)

**Complexity:**

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Iterate | O(n) | O(n) |
| Space | O(n) | O(n) |

**Use when:**
- You need O(1) lookup by a key (not by position)
- Counting frequencies of elements
- Caching/memoizing previously computed results
- Checking membership quickly (`x in s` is O(1) for sets, O(n) for lists)
- Finding complements (Two Sum pattern: store `target - num`)

**Python:**
```python
# HashMap (dict)
freq = {}
freq["a"] = freq.get("a", 0) + 1

from collections import defaultdict
freq = defaultdict(int)
freq["a"] += 1

from collections import Counter
freq = Counter("banana")  # auto-counts

# HashSet (set)
seen = set()
seen.add(5)
seen.discard(5)    # remove if present (no error if missing)
5 in seen          # O(1) lookup

# Common patterns
# Two Sum: store complement
nums = [2, 7, 11, 15]
target = 9
lookup = {}
for i, n in enumerate(nums):
    if target - n in lookup:
        print(lookup[target - n], i)
    lookup[n] = i
```

## The Pattern

### Prefix Sum

```
  Array: [1, 2, 3, 4, 5]
  Prefix: [0, 1, 3, 6, 10, 15]
           ↑  ↑  ↑  ↑   ↑   ↑
           0  1  2  3   4   5  ← index in prefix array

  Range sum query [l, r] (0-indexed, inclusive):
  sum(2..4) = prefix[5] - prefix[2] = 15 - 3 = 12 ✓
  (3 + 4 + 5 = 12)

  General formula:
  prefix[i] = arr[0] + arr[1] + ... + arr[i-1]
  sum(l, r) = prefix[r+1] - prefix[l]    ← O(1)!

  Subarray sum equals k (use HashMap):
  arr = [1, 2, 3], k = 3
  prefix sums seen: {0: 1}
  i=0: prefix=1,  need=1-3=-2,  count += seen[-2] = 0
  i=1: prefix=3,  need=3-3=0,   count += seen[0] = 1   ← [1,2]
  i=2: prefix=6,  need=6-3=3,   count += seen[3] = 1   ← [3]
  Total = 2
```

**What it is:** Precompute cumulative sums so that any range sum query answers in O(1) instead of O(n). When combined with a hash map, it finds subarrays with a target sum in O(n).

**Use this when:**
- [ ] "Sum of subarray from index l to r" (multiple queries)
- [ ] "Number of subarrays with sum equal to k"
- [ ] "Product of array except self" (prefix + suffix products)
- [ ] 2D matrix range queries (2D prefix sum)
- [ ] Balance point / pivot index problems

**Python:**
```python
# Build prefix sum
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i, val in enumerate(arr):
        prefix[i+1] = prefix[i] + val
    return prefix

# Range sum query — O(1)
def range_sum(prefix, l, r):
    return prefix[r+1] - prefix[l]

# Subarray sum equals k — O(n)
from collections import defaultdict
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1
    for num in nums:
        prefix += num
        count += seen[prefix - k]   # how many times (prefix - k) appeared before
        seen[prefix] += 1
    return count

# Product of array except self (prefix × suffix)
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result
```

**Complexity:** O(n) build, O(1) query. Subarray sum k: O(n) time, O(n) space.

**Blind 75 examples:** Product of Array Except Self · (Subarray Sum Equals K is a common extension)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/arrays-hashing/`](../appendix/templates/arrays-hashing/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/arrays-hashing/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Arrays & Hashing problems →**](../../lists/recommended.md#1-arrays--hashing-24-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Two Pointers](02-two-pointers.md) — one scan, two cursors closing in. The trick is knowing which condition moves which pointer.

[← Prev](00-foundations.md) · [🗺 Roadmap](../roadmap.md) · [Next →](02-two-pointers.md)

