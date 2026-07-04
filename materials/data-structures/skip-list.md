# Skip List

```
level 2:  1 ----------------> 9
level 1:  1 ------> 5 ------> 9
level 0:  1 -> 3 -> 5 -> 7 -> 9 -> 12     ← the real sorted linked list

search(7): ride the top level as far as possible, drop down when you'd overshoot
→ O(log n) expected, like binary search on a linked list
```

A sorted [linked list](linked-list.md) with express lanes: each node is randomly promoted (coin flips) into higher, sparser levels, so a search skims the top lane and drops down, skipping most nodes — binary-search behavior on a pointer structure. Insert/delete are just linked-list splices at each level, no rotations, which is why skip lists match [balanced-BST](balanced-bst.md) guarantees with far simpler code (the reason Redis sorted sets use one).

LeetCode has exactly one problem asking you to build it (LC 1206, hard); otherwise this is a "know it exists" structure — and a neat interview answer to "can you get O(log n) ordered operations *without* a tree?"

**Complexity:** search/insert/delete O(log n) *expected* (randomized) · space O(n).

**Related:** [linked-list](linked-list.md) · [balanced-bst](balanced-bst.md) · [sorted-list](sorted-list.md)
