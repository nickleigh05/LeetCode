# Balanced BSTs (AVL & Red-Black Trees)

```
Plain BST, sorted inserts 1,2,3,4:      Self-balancing tree, same inserts:
    1                                          2
     \                                        / \
      2        height = n                    1   3        height = log n
       \       search = O(n) 😱                    \
        3                                            4
         \
          4
```

A [binary search tree](binary-search-tree.md) is only O(log n) if it stays *bushy* — adversarial (e.g. sorted) inserts degrade it into a linked list. **Self-balancing BSTs** fix this by doing O(1) local *rotations* after each insert/delete to restore a height guarantee: **AVL trees** enforce subtree heights within ±1 (strictest balance, fastest lookups), **red-black trees** enforce looser color rules (fewer rotations, faster updates — what C++ `std::map` and Java `TreeMap` use). Both guarantee O(log n) search/insert/delete *and* sorted iteration — the combination hash maps can't offer.

You will likely never implement one (nor be asked to — rotations are memorization, not insight). What you need: (1) know *why* they exist — the degenerate-BST failure; (2) know they're the machinery behind "ordered map/set" in other languages; (3) know Python's substitute, since its stdlib has none — [sortedcontainers' SortedList](sorted-list.md), or [heaps](heap.md)/[bisect](../syntax/bisect-module.md) when you only need part of the power.

**Complexity:** search/insert/delete O(log n) guaranteed · in-order iteration O(n) sorted.

**Related:** [binary-search-tree](binary-search-tree.md) · [sorted-list](sorted-list.md) · [skip-list](skip-list.md) · [Trees lesson](../learning/07-trees.md)
