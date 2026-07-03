# Array

```python
nums = [10, 20, 30]
nums[1]        # 20 — O(1), direct memory offset
nums.append(40) # O(1) amortized
nums.insert(0, 5) # O(n) — shifts every element right
```

A contiguous block of memory holding same-type elements back-to-back — that contiguity is *why* index access is O(1): the address of `nums[i]` is just `base + i * element_size`, no searching required. Insert/delete anywhere but the end costs O(n) because everything after has to shift.

**Complexity:** index read/write O(1) · append O(1) amortized · insert/delete at arbitrary index O(n) · search (unsorted) O(n).

**Used to solve:** [Plus One](../../problems/0001-0499/66.py) — direct index access is the whole trick.

**Related:** [list-basics (syntax)](../syntax/list-basics.md) · [list-slicing (syntax)](../syntax/list-slicing.md) · [hashmap](hashmap.md) · [two pointers (template)](../appendix/templates/two-pointers/README.md)
