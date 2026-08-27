# Hash Set

```python
seen = set()
seen.add(5)        # O(1) average
5 in seen           # O(1) average membership check
```

A [hashmap](hashmap.md) that only stores keys — no values — used purely to answer "have I seen this value." Same underlying hash-table mechanics, same O(1) average membership check, half the bookkeeping when you don't need to pair a value with each key.

**Complexity:** add/remove/membership O(1) average.

**Used to solve:** [Contains Duplicate](../rmap-practice/01-arrays-hashing.md#217-contains-duplicate--easy), [Find All Numbers Disappeared in an Array](../../problems/0001-0499/448.py), [Longest Consecutive Sequence](../rmap-practice/01-arrays-hashing.md#128-longest-consecutive-sequence--medium), [Valid Sudoku](../rmap-practice/01-arrays-hashing.md#36-valid-sudoku--medium).

**Related:** [set-basics (syntax)](../syntax/set-basics.md) · [hashmap](hashmap.md)
