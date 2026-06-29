# 01. Arrays & Hashing
*The foundation. Hash maps trade memory for O(1) lookups and quietly power half of all interview solutions.*

[← Prev](00-foundations.md) · [🗺 Roadmap](../roadmap.md) · [Next →](01b-prefix-sums.md)

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

A string is an **immutable** array of characters — indexing and slicing work exactly like a list (`s[i]`, `s[1:4]`, `s[::-1]`), but you can't assign to `s[i]`. Two gotchas matter for interviews:

- **Building strings:** `+=` in a loop is O(n²) because each concat copies the whole string. Collect characters in a list and `"".join(list)` once — O(n).
- **Char ↔ int:** `ord('a') → 97` and `chr(97) → 'a'`, used constantly for frequency arrays and alphabet indexing.

For the full string method reference (split, strip, replace, f-strings, `Counter`), see [Python syntax → Strings](../appendix/python-syntax.md#04-strings). Everything else about strings *is* the array material above.

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

## The Pattern — Prefix Sums

The classic memory-for-speed pattern built on arrays — precompute cumulative sums so any range query is an O(1) subtraction, and pair it with a hash map to count subarrays summing to `k`— gets its own lesson next: [**01b · Prefix Sums**](01b-prefix-sums.md). It also covers difference arrays and 2-D prefix sums. Finish this lesson's hash-map practice first, then go there.

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/arrays-hashing/`](../appendix/templates/arrays-hashing/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/arrays-hashing/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Arrays & Hashing problems →**](../../lists/recommended.md#1-arrays--hashing-24-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain *why* a hash map turns an O(n²) double loop into O(n) — what it trades and what it remembers.
- [ ] I can write the Two Sum complement pattern from memory, plus frequency counting with `Counter`/`defaultdict`.
- [ ] I know when a set beats a list for membership (`x in s`) and why.
- [ ] I solved a 🔴 Hard array/hashing problem (e.g. Longest Consecutive Sequence).

---

**Up next:** [Prefix Sums](01b-prefix-sums.md) — precompute once, answer range queries in O(1). The hidden engine behind subarray problems.

[← Prev](00-foundations.md) · [🗺 Roadmap](../roadmap.md) · [Next →](01b-prefix-sums.md)

