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

**Used to solve:** [Two Sum](../rmap-practice/01-arrays-hashing.md#1-two-sum--easy), [Group Anagrams](../rmap-practice/01-arrays-hashing.md#49-group-anagrams--medium), [Top K Frequent Elements](../rmap-practice/01-arrays-hashing.md#347-top-k-frequent-elements--medium), [Subarray Sum Equals K](../../problems/0500-0999/560.py), and more.

**Related:** [dict-basics (syntax)](../syntax/dict-basics.md) · [hashset](hashset.md) · [Counter for frequency counting (syntax)](../syntax/counter.md)
