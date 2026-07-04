# frozenset

```python
fs = frozenset([1, 2, 3])
2 in fs                      # O(1) membership, like a normal set
fs | {4}, fs & {2, 3}        # all read-only set ops work
fs.add(4)                    # AttributeError — immutable, no mutation methods

seen = set()
seen.add(frozenset(group))   # ★ the use case: a SET as a set member / dict key
groups[frozenset(word)]      # e.g. key anagram-ish groups by their letter set
```

An immutable [set](set-basics.md) — same O(1) lookups and [set algebra](set-operations.md), no `add`/`remove`. Its entire reason to exist: regular sets aren't hashable, so they can't go inside other sets or be [dict](dict-basics.md) keys; `frozenset` can, because immutability makes it hashable. It's to `set` what [tuple](tuple-basics.md) is to list. Order-insensitive by nature — `frozenset("ab") == frozenset("ba")` — which is sometimes exactly the key you want, and sometimes a bug (use a sorted tuple when counts matter).

**Complexity:** membership O(1) average, like set.

**Related:** [set-basics](set-basics.md) · [set-operations](set-operations.md) · [tuple-basics](tuple-basics.md) · [hashset (data-structures)](../data-structures/hashset.md)
