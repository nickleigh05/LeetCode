# Bucket Sort

```python
# Top K Frequent Elements flavor: bucket index = frequency (bounded by n!)
def top_k_frequent(nums, k):
    from collections import Counter
    buckets = [[] for _ in range(len(nums) + 1)]
    for val, freq in Counter(nums).items():
        buckets[freq].append(val)              # drop each value in its bucket
    res = []
    for freq in range(len(buckets) - 1, 0, -1):  # walk buckets high → low
        for val in buckets[freq]:
            res.append(val)
            if len(res) == k:
                return res
```

Distribute items into an array of buckets indexed by some bounded key (frequency, digit, value range), then read the buckets off in order — sorting without comparisons, which is how it ducks under the O(n log n) comparison-sort floor. The LeetCode-famous uses: Top K Frequent in O(n) (frequency ≤ n, so frequencies *are* valid indices) and Maximum Gap. The classic uniform-floats version sorts each bucket individually with [insertion sort](insertion-sort.md). Only works when keys are integers in a reasonable range — the same precondition family as [counting sort](counting-sort.md), which is bucket sort with bucket = exact value.

**Complexity:** O(n + #buckets) for the index-by-bounded-key uses · degrades toward O(n²) if everything lands in one bucket.

**Related:** [counting-sort](counting-sort.md) · [radix-sort](radix-sort.md) · [counter (syntax)](../syntax/counter.md)
