# 05b. Sorting — Why, How, and When

*Knowing which sort to reach for, and why n log n is the floor.*

[← Prev](05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](06-linked-list.md)

---

> **Builds on:** binary search from [Lesson 05](05-binary-search.md) — binary search is the payoff for having sorted data.

Lesson 05 showed you *how* merge sort and quicksort work algorithmically. This lesson answers the questions that come after: *why* is n log n the best comparison sort can do, *which sort* do you choose in practice, and *how* do you use Python's built-in sort safely and idiomatically? Intervals (17), Greedy (16), and almost every "sort first, then sweep" pattern depend on internalizing this.

## Concept

### The comparison lower bound — why O(n log n) is the floor

Any algorithm that sorts n elements by *comparing pairs* must make at least **Ω(n log n)** comparisons in the worst case. Here's the intuition:

n elements can be arranged in n! different orders. Each comparison halves the remaining possibilities (it's a binary question: "is A ≤ B?"). To distinguish all n! arrangements you need at least log₂(n!) comparisons. By Stirling's approximation, log₂(n!) ≈ n log₂ n. So no comparison-based sort can do better than O(n log n).

The practical takeaway: **merge sort and heapsort achieve this bound in the worst case; quicksort achieves it on average.** Any O(n²) sort (bubble, insertion, selection) is sub-optimal for large n.

### Merge sort — stable, predictable, O(n log n) always

**Idea:** split in half → sort each half → merge the two sorted halves.

```
[5, 2, 8, 1, 9, 3]
        ↓ split
[5, 2, 8]    [1, 9, 3]
    ↓ split       ↓ split
[5,2] [8]    [1,9] [3]
  ↓ split      ↓ split
[5][2] [8]   [1][9] [3]
  ↓ merge      ↓ merge
[2,5]  [8]   [1,9]  [3]
    ↓ merge        ↓ merge
  [2,5,8]       [1,3,9]
          ↓ merge
    [1,2,3,5,8,9]
```

- **Time:** O(n log n) always — log n levels, n total work per level.
- **Space:** O(n) extra — the merge step needs a temporary array.
- **Stable:** equal elements keep their original relative order.

**Reach for it when:** you need guaranteed worst-case O(n log n), or stability matters (sorting by secondary key after primary key, counting inversions).

### Quicksort — fast in practice, O(n²) worst case

**Idea:** pick a pivot → put elements smaller than pivot left, larger right → recurse on both halves. No merge step needed.

```
[5, 2, 8, 1, 9, 3]   pivot = 5 (last element, say)
                       partition:
  [2, 1, 3]  [5]  [8, 9]
      ↓ recurse          ↓ recurse
  [1, 2, 3]         [8, 9]
          combine:
  [1, 2, 3, 5, 8, 9]
```

- **Time:** O(n log n) *average*; O(n²) worst case (already-sorted input with bad pivot choice).
- **Space:** O(log n) extra on average for the call stack; O(n) worst case.
- **Not stable** in the standard implementation.
- **Fastest in practice** because the constant factor is small and it has great cache behavior.

**Reach for it when:** you need in-place sorting with excellent average performance and don't need stability. Python's built-in avoids its pathological cases (see Timsort below).

### Timsort — what Python actually uses

Python's `sorted()` and `.sort()` use **Timsort**, a hybrid of merge sort and insertion sort:

- Finds naturally occurring sorted runs in the data.
- Merges those runs using merge sort logic.
- Uses insertion sort (very fast for tiny arrays) on short runs.

In practice: **O(n log n) worst case, O(n) on already-sorted data.** Stable. Requires O(n) extra space.

You'll almost never implement Timsort in an interview — but knowing it's stable and has an O(n) best case is worth the fact.

### When sorting isn't the answer — O(n) alternatives

Comparison-based sorts can't beat O(n log n), but if your values come from a **bounded integer range**, you can do better:

| Algorithm | When to use | Time | Space |
|-----------|-------------|------|-------|
| Counting sort | Values in range [0, k], k small | O(n + k) | O(k) |
| Radix sort | Fixed-width integers/strings | O(d · n) | O(n) |
| Bucket sort | Uniformly distributed floats in [0,1] | O(n) avg | O(n) |

Counting sort is the most common interview variant: count occurrences, then reconstruct.

```python
def counting_sort(nums, max_val):
    counts = [0] * (max_val + 1)
    for x in nums:
        counts[x] += 1
    result = []
    for val, cnt in enumerate(counts):
        result.extend([val] * cnt)
    return result
```

## Python Sorting in Practice

### `sorted()` vs `.sort()`

```python
nums = [3, 1, 4, 1, 5]
new  = sorted(nums)       # returns new list; nums unchanged
nums.sort()               # sorts in-place; returns None — don't do sorted_nums = nums.sort()!
```

### The `key=` parameter — sort by anything

```python
words = ["banana", "fig", "apple", "kiwi"]
words.sort(key=len)                         # sort by length
# → ['fig', 'kiwi', 'apple', 'banana']

pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
pairs.sort(key=lambda x: x[1])             # sort by second element
# → [(3, 'a'), (1, 'b'), (2, 'c')]

# Sort descending: negate the key
nums.sort(key=lambda x: -x)
# or
nums.sort(reverse=True)
```

### Custom comparison with `functools.cmp_to_key`

For tricky orderings (e.g. "arrange numbers to form the largest integer"):

```python
from functools import cmp_to_key

def compare(a, b):
    if str(a)+str(b) > str(b)+str(a): return -1   # a should come first
    if str(a)+str(b) < str(b)+str(a): return  1
    return 0

nums = [3, 30, 34, 5, 9]
nums.sort(key=cmp_to_key(compare))
# → [9, 5, 34, 3, 30]  → "9534330"
```

### Stability in practice

Because Python's sort is stable, you can sort by a secondary key first, then by a primary key second, and the relative order within tied primary keys will respect the secondary sort:

```python
students = [("Alice",90), ("Bob",85), ("Carol",90)]
students.sort(key=lambda s: s[1], reverse=True)   # sort by grade desc, stable
# Ties (90): Alice before Carol, their original order
# → [('Alice',90), ('Carol',90), ('Bob',85)]
```

## In-Lesson Exercises

<details>
<summary><strong>Exercise 1 — sort then two-pointer</strong></summary>

Given an unsorted array `nums` and a target, find if any two numbers sum to target. What do you sort first, and what's the total complexity?

**Answer:** Sort `nums` in O(n log n), then use two pointers in O(n). Total: O(n log n). The sort unlocks the O(n) pointer scan.
</details>

<details>
<summary><strong>Exercise 2 — stability matters</strong></summary>

You have a list of `(name, score, date)` records. You want them sorted by score descending, and ties broken by date ascending. How do you do this with Python's sort?

**Answer:** Sort by date first (ascending), then by score (descending). Because `.sort()` is stable, ties in the second sort preserve the order from the first.

```python
records.sort(key=lambda r: r[2])              # date ascending
records.sort(key=lambda r: r[1], reverse=True) # score descending, stable
```

Or in one call with a tuple key (negate score for descending):
```python
records.sort(key=lambda r: (-r[1], r[2]))
```
</details>

<details>
<summary><strong>Exercise 3 — when to use counting sort</strong></summary>

You're given `n` numbers, each between 0 and 9. What sort should you use?

**Answer:** Counting sort — O(n + 10) = O(n) since k=10 is constant. Beats any comparison sort for this bounded range.
</details>

<details>
<summary><strong>Exercise 4 — trace merge sort</strong></summary>

Trace merge sort on `[4, 2, 7, 1]`. Draw the split tree and the merge steps.

**Answer:**
```
[4,2,7,1]
  [4,2]   [7,1]
  [4][2]  [7][1]
  [2,4]   [1,7]
  [1,2,4,7]
```
</details>

## Practice

Sorting unlocks many patterns. Drill these to cement the "sort first" instinct:

- [LeetCode 56 — Merge Intervals](https://leetcode.com/problems/merge-intervals/) (sort by start, then sweep)
- [LeetCode 75 — Sort Colors](https://leetcode.com/problems/sort-colors/) (3-way partition / Dutch flag)
- [LeetCode 179 — Largest Number](https://leetcode.com/problems/largest-number/) (custom comparator)
- [LeetCode 912 — Sort an Array](https://leetcode.com/problems/sort-an-array/) (implement merge sort or quicksort by hand)

## Check Yourself

- [ ] I can explain why no comparison sort can beat O(n log n) in the worst case.
- [ ] I know when to prefer merge sort (stability, guaranteed worst case) vs. quicksort (in-place, fast average).
- [ ] I can use `sorted()`, `.sort()`, `key=`, and `reverse=` confidently in Python.
- [ ] I know that Timsort is stable and that Python's sort is O(n) on already-sorted data.
- [ ] I can identify when counting sort applies and implement it.

---

**Up next:** [Linked Lists](06-linked-list.md) — pointer surgery: reverse, dummy head, fast/slow.

[← Prev](05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](06-linked-list.md)
