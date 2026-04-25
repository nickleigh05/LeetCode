# Linked List

## 6. Linked List (11 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 206 | Easy | Reverse Linked List | [Link](https://leetcode.com/problems/reverse-linked-list/) |
| 21 | Easy | Merge Two Sorted Lists | [Link](https://leetcode.com/problems/merge-two-sorted-lists/) |
| 143 | Medium | Reorder List | [Link](https://leetcode.com/problems/reorder-list/) |
| 19 | Medium | Remove Nth Node From End of List | [Link](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) |
| 138 | Medium | Copy List with Random Pointer | [Link](https://leetcode.com/problems/copy-list-with-random-pointer/) |
| 2 | Medium | Add Two Numbers | [Link](https://leetcode.com/problems/add-two-numbers/) |
| 141 | Easy | Linked List Cycle | [Link](https://leetcode.com/problems/linked-list-cycle/) |
| 287 | Medium | Find the Duplicate Number | [Link](https://leetcode.com/problems/find-the-duplicate-number/) |
| 146 | Medium | LRU Cache | [Link](https://leetcode.com/problems/lru-cache/) |
| 23 | Hard | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) |
| 25 | Hard | Reverse Nodes in k-Group | [Link](https://leetcode.com/problems/reverse-nodes-in-k-group/) |

---

## Data Structures

### Singly Linked List
Each node holds a value and a `next` pointer. You can only traverse forward. No O(1) index access — you must walk from the head. Inserting or deleting a node is O(1) if you already have a pointer to the previous node.

### Doubly Linked List
Each node has both `next` and `prev` pointers. Allows O(1) removal of any node (as long as you have a pointer to it). Used in LRU Cache to support O(1) move-to-front and remove-from-back.

### Hash Map + Doubly Linked List (LRU Cache)
Combine a hash map (O(1) lookup by key) with a doubly linked list (O(1) insertion/deletion) to build a cache that supports O(1) get and O(1) put with LRU eviction.

---

## Core Patterns

### In-Place Reversal
Track `prev = None` and `curr = head`. On each step: save `curr.next`, point `curr.next` to `prev`, advance both pointers. No extra space needed. Used in Reverse Linked List, Reverse Nodes in k-Group.

### Dummy Head
Create a fake node before the real head. Lets you treat the head the same as any other node — no special-casing for insertions or deletions at the front. Used in Merge Two Sorted Lists, Remove Nth Node.

### Fast / Slow Pointers (Floyd's Algorithm)
`slow` moves one step, `fast` moves two steps. If there's a cycle, fast will eventually lap slow — they'll meet inside the cycle. If no cycle, fast reaches null first. Used in Linked List Cycle, Find the Duplicate Number.

### Find Nth From End
Advance `fast` pointer n steps ahead of `slow`. Then move both at the same speed. When `fast` hits the end, `slow` is at the nth node from the end. Used in Remove Nth Node From End.

### Find Middle
Use fast/slow pointers. When `fast` reaches the end, `slow` is at the middle. Useful for splitting a list before reversing the second half. Used in Reorder List.

### Deep Copy with Hash Map
Map each original node to its copy in a hash map. First pass: create all copies. Second pass: wire up `next` and `random` pointers using the map. Used in Copy List with Random Pointer.

### Merge with Two Pointers
Compare the heads of two sorted lists and always take the smaller one. Advance that pointer and repeat. Used in Merge Two Sorted Lists, Merge k Sorted Lists (with a min-heap for k lists).
