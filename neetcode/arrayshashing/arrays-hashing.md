# Arrays & Hashing

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints. NeetCode 250 introduces new patterns (Boyer-Moore voting, prefix sums, in-place hashing) and design problems. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, find the matching pattern first, then check the syntax.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 217 | Easy | Contains Duplicate | [Link](https://leetcode.com/problems/contains-duplicate/) | ☑ |
| 242 | Easy | Valid Anagram | [Link](https://leetcode.com/problems/valid-anagram/) | ☑ |
| 1 | Easy | Two Sum | [Link](https://leetcode.com/problems/two-sum/) | ☑ |
| 49 | Medium | Group Anagrams | [Link](https://leetcode.com/problems/group-anagrams/) | ☑ |
| 347 | Medium | Top K Frequent Elements | [Link](https://leetcode.com/problems/top-k-frequent-elements/) | ☑ |
| 271 | Medium | Encode and Decode Strings | [Link](https://leetcode.com/problems/encode-and-decode-strings/) | ☑ |
| 238 | Medium | Product of Array Except Self | [Link](https://leetcode.com/problems/product-of-array-except-self/) | ☑ |
| 128 | Medium | Longest Consecutive Sequence | [Link](https://leetcode.com/problems/longest-consecutive-sequence/) | ☑ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 36 | Medium | Valid Sudoku | [Link](https://leetcode.com/problems/valid-sudoku/) | ☑ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 1929 | Easy | Concatenation of Array | [Link](https://leetcode.com/problems/concatenation-of-array/) | ☑ | Array manipulation |
| 14 | Easy | Longest Common Prefix | [Link](https://leetcode.com/problems/longest-common-prefix/) | ☑ | Array (vertical scan) |
| 27 | Easy | Remove Element | [Link](https://leetcode.com/problems/remove-element/) | ☑ | Array (in-place) |
| 169 | Easy | Majority Element | [Link](https://leetcode.com/problems/majority-element/) | ☑ | Frequency Counting / Boyer-Moore |
| 705 | Easy | Design HashSet | [Link](https://leetcode.com/problems/design-hashset/) | ☐ | Hash Table design |
| 706 | Easy | Design HashMap | [Link](https://leetcode.com/problems/design-hashmap/) | ☐ | Hash Table design |
| 912 | Medium | Sort an Array | [Link](https://leetcode.com/problems/sort-an-array/) | ☐ | Bucket Sort |
| 75 | Medium | Sort Colors | [Link](https://leetcode.com/problems/sort-colors/) | ☐ | Bucket Sort |
| 304 | Medium | Range Sum Query 2D - Immutable | [Link](https://leetcode.com/problems/range-sum-query-2d-immutable/) | ☐ | Prefix Products (2D) |
| 122 | Medium | Best Time to Buy and Sell Stock II | [Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | ☐ | Greedy |
| 229 | Medium | Majority Element II | [Link](https://leetcode.com/problems/majority-element-ii/) | ☐ | Frequency Counting / Boyer-Moore |
| 560 | Medium | Subarray Sum Equals K | [Link](https://leetcode.com/problems/subarray-sum-equals-k/) | ☑ | Frequency Counting + Complement Lookup |
| 41 | Hard | First Missing Positive | [Link](https://leetcode.com/problems/first-missing-positive/) | ☐ | Index as value (in-place hashing) |

---

## Complexity Reference

| Pattern / Structure | Best | Average | Worst | Space |
|---------------------|------|---------|-------|-------|
| Array access (by index) | O(1) | O(1) | O(1) | O(n) |
| Array insert/delete (middle) | O(n) | O(n) | O(n) | O(1) |
| Hash Table lookup/insert/delete | O(1) | O(1) | O(n)* | O(n) |
| Frequency Counting | O(n) | O(n) | O(n) | O(n) |
| Seen-Before Check | O(n) | O(n) | O(n) | O(n) |
| Complement Lookup (Two Sum) | O(n) | O(n) | O(n) | O(n) |
| Prefix Products | O(n) | O(n) | O(n) | O(1)† |
| Grouping by Key | O(n·k log k) | O(n·k log k) | O(n·k log k) | O(n·k) |
| Bucket Sort / Counting Sort | O(n) | O(n) | O(n) | O(n) |

> \* Hash table worst case is O(n) due to hash collisions — rare in practice with a good hash function.  
> † O(1) extra space if the output array doesn't count.

---

## Data Structures

### Array

A fixed-size, contiguous block of memory. Elements sit at sequential addresses, so the CPU can jump directly to any index in O(1) — it's just `base_address + index * element_size`. The tradeoff is that inserting or deleting anywhere except the end requires shifting every element after that point, which is O(n). In Python, `list` is a dynamic array that occasionally resizes by doubling capacity, but amortized append is still O(1).

```
Index:  0    1    2    3    4
      +----+----+----+----+----+
      | 10 | 20 | 30 | 40 | 50 |
      +----+----+----+----+----+
         ↑              ↑
       O(1) access    O(n) insert (elements after index shift right)
```

**When it matters:** Random access by index is free. Searching without an index is O(n). Prefer arrays when you know the index; prefer hash tables when you're looking up by value.

### Hash Table (dict / set)

Converts a key into a bucket index via a hash function, then stores the value there. Lookup, insert, and delete are O(1) on average. Collisions happen when two keys hash to the same bucket — Python resolves them with open addressing (probing for the next empty slot). Worst case is O(n) if everything collides, but a good hash function makes this essentially impossible in practice.

```
key → hash("name") % 5 → bucket 3

Buckets:
[0] → empty
[1] → ("age", 25)
[2] → empty
[3] → ("name", "nick") → ("city", "QC")  ← collision chain
[4] → ("job", "dev")
```

**Keys must be hashable:** strings, ints, tuples — anything immutable. Lists and dicts cannot be keys. A `set` is just a hash table where each key is its own value — same O(1) membership, just no associated value to store.

---

## Core Patterns

### Frequency Counting
**When to use:** You need to know how many times each value appears.  
**Complexity:** O(n) time, O(n) space  
**Problems:** Valid Anagram (#242), Top K Frequent Elements (#347), Group Anagrams (#49), Majority Element (#169), Majority Element II (#229), Subarray Sum Equals K (#560)  
**Common mistake:** Forgetting that two dicts are equal only if both keys AND counts match.

Build a hash map of `value → count`. Lets you answer "how many times does X appear?" in O(1) after an O(n) setup pass.

```python
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
```

### Seen-Before Check
**When to use:** You need to detect if something has appeared before in one pass.  
**Complexity:** O(n) time, O(n) space  
**Problems:** Contains Duplicate (#217), Two Sum (#1), Valid Sudoku (#36), First Missing Positive (#41)  
**Common mistake:** Using a list instead of a set — membership check is O(n) on a list.

```python
seen = set()
for x in nums:
    if x in seen:
        return True   # duplicate found
    seen.add(x)
```

### Complement Lookup (Two Sum Pattern)
**When to use:** You're looking for a pair that satisfies some relationship (sum, difference).  
**Complexity:** O(n) time, O(n) space  
**Problems:** Two Sum (#1), Subarray Sum Equals K (#560)  
**Common mistake:** Storing the value instead of the index, then not being able to return positions.

```python
seen = {}
for i, x in enumerate(nums):
    complement = target - x
    if complement in seen:
        return [seen[complement], i]
    seen[x] = i
```

### Prefix Products
**When to use:** Product (or sum) of everything except the current index, no division allowed.  
**Complexity:** O(n) time, O(1) extra space (if output array doesn't count)  
**Problems:** Product of Array Except Self (#238), Range Sum Query 2D (#304)  
**Common mistake:** Trying to divide by zero instead of handling zeros explicitly via prefix/suffix pass.

```python
res = [1] * len(nums)
prefix = 1
for i in range(len(nums)):
    res[i] = prefix
    prefix *= nums[i]
# then do a suffix pass multiplying in from the right
```

### Grouping by Key
**When to use:** You need to cluster elements that are "equivalent" by some normalization.  
**Complexity:** O(n·k log k) where k is element length  
**Problems:** Group Anagrams (#49)  
**Common mistake:** Using a list as a dict key — lists aren't hashable. Use `tuple(sorted(s))`.

```python
groups = defaultdict(list)
for s in strs:
    key = tuple(sorted(s))   # "eat" and "tea" both → ('a','e','t')
    groups[key].append(s)
```

### Bucket Sort / Counting Sort
**When to use:** Values are bounded so you can use index-as-value instead of sorting.  
**Complexity:** O(n) time  
**Problems:** Top K Frequent Elements (#347), Sort an Array (#912), Sort Colors (#75)  
**Common mistake:** Off-by-one on bucket size — frequency can equal len(nums) so bucket needs n+1 slots.

```python
bucket = [[] for _ in range(len(nums) + 1)]  # index = frequency
for val, count in freq.items():
    bucket[count].append(val)
# iterate bucket in reverse to get highest-frequency first
```

---

## Syntax Reference

### dict (Hash Map)

A `dict` maps **keys** to **values**. Think of it as a lookup table — given a key, you get its associated value back in O(1). Keys must be hashable (strings, ints, tuples — not lists). Values can be anything.

**Structure:**
```python
d = {key: value, key: value}

d = {"name": "nick", "age": 21}
#     ↑ key   ↑ value
```

**Accessing values:**
```python
d["name"]           # returns "nick" — raises KeyError if key doesn't exist
d.get("name")       # returns "nick" — returns None if key doesn't exist (safe)
d.get("age", 0)     # returns value if found, otherwise returns the default (0)
```
> Use `.get()` any time you're not sure if a key exists. Bare bracket access will crash on missing keys.

**Adding / updating:**
```python
d["name"] = "nick"      # adds key if new, overwrites if already exists
d["score"] += 1         # only safe if "score" already exists, otherwise KeyError
d["score"] = d.get("score", 0) + 1   # safe increment — the pattern for counting
```

**Deleting:**
```python
del d["name"]           # removes key — raises KeyError if missing
d.pop("name")           # removes and returns the value — raises KeyError if missing
d.pop("name", None)     # removes and returns, or returns None if missing (safe)
```

**Iterating:**
```python
for key in d:                    # iterate over keys
for key in d.keys():             # same, explicit
for val in d.values():           # iterate over values
for key, val in d.items():       # iterate over (key, value) pairs — most common
```

**Checking membership:**
```python
"name" in d             # True if key exists — always check keys, not values
"name" not in d         # inverse
```

**Useful methods:**
```python
len(d)                  # number of key-value pairs
d.keys()                # all keys (view object, not a list)
d.values()              # all values
d.items()               # all (key, value) pairs
d.update({"x": 1})     # merge another dict in — overwrites on conflict
```

---

### defaultdict

A `defaultdict` is a `dict` that never raises a `KeyError`. When you access a missing key, it automatically creates it with a default value based on the type you pass in. Saves you from writing `.get(key, 0)` everywhere.

```python
from collections import defaultdict

freq = defaultdict(int)     # missing keys default to 0
freq["a"] += 1              # no KeyError — "a" is auto-initialized to 0

groups = defaultdict(list)  # missing keys default to []
groups["vowels"].append("a")  # no KeyError — auto-initialized to []

nested = defaultdict(set)   # missing keys default to set()
nested["seen"].add(1)
```

> Pick `defaultdict(int)` for counting, `defaultdict(list)` for grouping. If you need a normal dict back, call `dict(freq)`.

---

### Counter

`Counter` is a specialized dict for counting hashable objects. Pass it any iterable and it builds a frequency map automatically. More ergonomic than building one manually with a loop.

```python
from collections import Counter

c = Counter("anagram")              # {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
c = Counter([1, 1, 2, 3])          # {1: 2, 2: 1, 3: 1}
c = Counter({"a": 3, "b": 1})      # from an existing dict
```

**Accessing counts:**
```python
c["a"]              # 3 — returns 0 for missing keys (unlike regular dict)
c.get("z", 0)       # also safe, but c["z"] already returns 0 so this is redundant
```

**Useful methods:**
```python
c.most_common(k)            # list of (element, count) sorted by count descending
                            # c.most_common(2) → [('a', 3), ('n', 1)]
c.most_common()[:-k-1:-1]   # k least common elements

sum(c.values())             # total count of all elements
list(c.elements())          # expand back out: ['a','a','a','n','g','r','m']
```

**Anagram check:**
```python
Counter(s1) == Counter(s2)   # True if same characters with same frequencies
```

**Arithmetic:**
```python
c1 + c2     # combine counts
c1 - c2     # subtract counts (drops zero/negative)
c1 & c2     # intersection — minimum of each count
c1 | c2     # union — maximum of each count
```

---

### set

A `set` stores unique values with no duplicates and no order. Backed by a hash table, so membership check is O(1) — this is the main reason you use a set over a list for "have I seen this before" checks.

```python
s = {1, 2, 3}           # literal — note: {} alone makes a dict, not a set
s = set()               # empty set — you must use set(), not {}
s = set([1, 2, 2, 3])  # from iterable — duplicates dropped → {1, 2, 3}
```

**Adding / removing:**
```python
s.add(x)            # adds x — no error if already present
s.remove(x)         # removes x — raises KeyError if not present
s.discard(x)        # removes x — no error if not present (safe)
s.pop()             # removes and returns an arbitrary element
s.clear()           # empties the set
```

**Membership (the main use case):**
```python
x in s              # O(1) — True if x is in the set
x not in s          # O(1) — inverse
```
> This is why you use a set and not a list for seen-before checks. `x in list` is O(n); `x in set` is O(1).

**Set operations:**
```python
s1 | s2             # union — all elements from both
s1 & s2             # intersection — only elements in both
s1 - s2             # difference — in s1 but not s2
s1 ^ s2             # symmetric difference — in one but not both
s1.issubset(s2)     # True if all of s1 is in s2
```

---

### list (as used in these problems)

You already know lists. These are the tricks that come up constantly in array/hashing problems.

**Slicing:**
```python
nums[i:j]       # elements from index i up to but not including j
nums[:j]        # from start to j
nums[i:]        # from i to end
nums[::-1]      # reversed copy
```

**Common operations:**
```python
nums.append(x)          # add to end — O(1)
nums.insert(i, x)       # insert at index i — O(n) because elements shift
nums.pop()              # remove and return last element — O(1)
nums.pop(i)             # remove and return element at index i — O(n)
nums.index(x)           # first index of x — O(n), raises ValueError if missing
x in nums               # O(n) membership — use a set if you do this in a loop
```

**Sorting:**
```python
nums.sort()                             # in-place, ascending
nums.sort(reverse=True)                 # in-place, descending
nums.sort(key=lambda x: -freq[x])      # sort by custom key (e.g. frequency)
sorted(nums)                            # returns new sorted list, original unchanged
sorted(nums, key=lambda x: (x[1], x[0]))  # sort by second element, then first
```

**Building a frequency bucket (Bucket Sort pattern):**
```python
bucket = [[] for _ in range(len(nums) + 1)]   # index = frequency, need n+1 slots
# +1 because max frequency possible is len(nums) (all elements identical)
```

---

### Useful built-ins

```python
enumerate(nums)             # yields (index, value) pairs — use instead of range(len(nums))
zip(l1, l2)                 # pairs up elements from two lists — stops at shortest
zip(*matrix)                # transpose a 2D list
any(x > 0 for x in nums)   # True if at least one element satisfies condition
all(x > 0 for x in nums)   # True if every element satisfies condition
min(nums), max(nums)        # O(n) scan
sum(nums)                   # O(n) sum
```

---

### heapq (for Top-K problems)

Python's `heapq` is a **min-heap** — the smallest element is always at the top. For a max-heap, negate your values.

```python
import heapq

heapq.nlargest(k, iterable, key=fn)    # top k largest by key — O(n log k)
heapq.nsmallest(k, iterable, key=fn)   # top k smallest by key

# manual heap if you need to push/pop repeatedly:
h = []
heapq.heappush(h, val)      # push — O(log n)
heapq.heappop(h)            # pop smallest — O(log n)
h[0]                        # peek at smallest without removing — O(1)
heapq.heapify(list)         # convert existing list to heap in-place — O(n)
```

**Top K frequent elements pattern:**
```python
# option 1 — most concise
heapq.nlargest(k, freq.items(), key=lambda x: x[1])

# option 2 — bucket sort (O(n), no heap needed)
bucket = [[] for _ in range(len(nums) + 1)]
for val, count in freq.items():
    bucket[count].append(val)
result = []
for i in range(len(bucket) - 1, 0, -1):
    result.extend(bucket[i])
    if len(result) >= k:
        return result[:k]
```
