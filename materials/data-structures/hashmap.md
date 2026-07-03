# Hash Map

```python
seen = {}
seen["a"] = 1        # O(1) average insert
seen["a"]              # O(1) average read
"a" in seen             # O(1) average membership check
```

Maps keys to values by running each key through a **hash function** to compute a bucket index, then storing/looking up directly at that bucket — trading memory for near-constant-time access instead of scanning. This is the single structure that turns "have I seen this before" or "what's paired with this" from an O(n) scan into O(1) average.

Collisions (two keys hashing to the same bucket) are handled internally (chaining/open addressing) and are why lookups are O(1) *average*, not worst-case guaranteed — but for interview purposes, treat it as O(1).

**Complexity:** insert/read/delete/membership O(1) average, O(n) worst case (pathological collisions, effectively never hit in practice).

**Used to solve:** [Two Sum](../practice/01-arrays-hashing/two-sum.md), [Group Anagrams](../practice/01-arrays-hashing/group-anagrams.md), [Top K Frequent Elements](../practice/01-arrays-hashing/top-k-frequent-elements.md), [Subarray Sum Equals K](../practice/01-arrays-hashing/subarray-sum-equals-k.md), and more.

**Related:** [dict-basics (syntax)](../syntax/dict-basics.md) · [hashset](hashset.md) · [complement pattern](../patterns/hashing/two-sum-complement-pattern.md) · [frequency counting](../patterns/hashing/frequency-counting.md)
