# Radix Sort

```python
def radix_sort(nums):                      # non-negative ints
    exp = 1
    while max(nums) // exp > 0:            # one stable pass per digit
        buckets = [[] for _ in range(10)]
        for x in nums:
            buckets[(x // exp) % 10].append(x)
        nums = [x for b in buckets for x in b]   # least-significant digit first
        exp *= 10
    return nums
```

Sort by the last digit, then the second-to-last, and so on — each pass done with a **stable** [counting/bucket sort](counting-sort.md). Stability is the entire trick: when pass k sorts by digit k, ties keep the order established by earlier digits, so after the final pass every prefix of digits is respected. d passes over d-digit numbers gives O(d·n) — genuinely linear when numbers have bounded digits, beating the comparison-sort floor by never comparing. Rare on LeetCode (Maximum Gap is the canonical appearance) but a standard "how would you sort a billion 32-bit ints?" systems answer, and the engine inside serious [suffix-array](../data-structures/suffix-array.md) builders.

**Complexity:** O(d · (n + base)) time · O(n + base) space · stable.

**Related:** [counting-sort](counting-sort.md) · [bucket-sort](bucket-sort.md) · [Sorting lesson](../learning/05b-sorting.md)
