# Hash Set

```python
seen = set()
seen.add(5)        # O(1) average
5 in seen           # O(1) average membership check
```

A [hashmap](hashmap.md) that only stores keys — no values — used purely to answer "have I seen this value." Same underlying hash-table mechanics, same O(1) average membership check, half the bookkeeping when you don't need to pair a value with each key.

**Complexity:** add/remove/membership O(1) average.

**Used to solve:** [Contains Duplicate](../practice/01-arrays-hashing/contains-duplicate.md), [Find All Numbers Disappeared in an Array](../practice/01-arrays-hashing/find-all-numbers-disappeared-in-an-array.md), [Longest Consecutive Sequence](../practice/01-arrays-hashing/longest-consecutive-sequence.md), [Valid Sudoku](../practice/01-arrays-hashing/valid-sudoku.md).

**Related:** [set-basics (syntax)](../syntax/set-basics.md) · [hashmap](hashmap.md)
