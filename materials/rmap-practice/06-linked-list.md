# 06. Linked List — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md)

---

### 206. Reverse Linked List — Easy
[LeetCode](https://leetcode.com/problems/reverse-linked-list/)  
[Solution file (no hints)](../../problems/0001-0499/206.py)

Reverse a singly [linked list](../data-structures/linked-list.md). At each node, what three pointers do you need in hand simultaneously so that flipping one link doesn't strand the rest of the list?

<details>
<summary>Hint</summary>

Track `prev` and `curr`. At each step, save `curr.next` before overwriting it (pointing it back to `prev`), then advance both `prev` and `curr` forward.
</details>

<details>
<summary>Solution</summary>

```python
prev = None
curr = head

while curr:                          # while loop until we run off the list
    next_node = curr.next               # save the next node before we lose it
    curr.next = prev                     # flip this node's pointer backward
    prev = curr                          # advance prev
    curr = next_node                     # advance curr

return prev                          # prev is the new head
```

Building blocks: [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited once.
**Space: O(1)** — only a few pointer variables.
</details>

---

### 21. Merge Two Sorted Lists — Easy
[LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/)  
[Solution file (no hints)](../../problems/0001-0499/21.py)

Merge two sorted [linked lists](../data-structures/linked-list.md) into one sorted list. Why does a throwaway "dummy" head node make the merging loop simpler than special-casing the very first node?

<details>
<summary>Hint</summary>

Use a dummy node so you always have a `tail.next` to attach to, even before the real result has a first node. Compare the heads of both lists and attach whichever is smaller, advancing that list.
</details>

<details>
<summary>Solution</summary>

```python
dummy = ListNode()                   # placeholder so tail.next always works
tail = dummy

while list1 and list2:                 # while loop, both lists still have nodes
    if list1.val <= list2.val:            # attach the smaller head
        tail.next = list1
        list1 = list1.next
    else:
        tail.next = list2
        list2 = list2.next
    tail = tail.next

tail.next = list1 if list1 else list2   # attach whichever list has leftovers
return dummy.next                       # skip the dummy node
```

Building blocks: [class-basics](../syntax/class-basics.md) · [while-loop](../syntax/while-loop.md) · [ternary-expression](../syntax/ternary-expression.md) · [none-type](../syntax/none-type.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n + m)** — one pass across both lists combined.
**Space: O(1)** — nodes are relinked in place, no new nodes allocated.
</details>

---

### 143. Reorder List — Medium
[LeetCode](https://leetcode.com/problems/reorder-list/)  
[Solution file (no hints)](../../problems/0001-0499/143.py)

Reorder a list so it goes first, last, second, second-last, ... Why does finding the middle, reversing the second half, then merging the two halves beat trying to do it in a single pass?

<details>
<summary>Hint</summary>

Three steps on a singly [linked list](../data-structures/linked-list.md): (1) find the middle with fast/slow pointers, (2) reverse the second half, (3) zipper-merge the two halves node by node.
</details>

<details>
<summary>Solution</summary>

```python
# 1. find the middle
slow, fast = head, head
while fast and fast.next:              # fast moves 2x speed of slow
    slow = slow.next
    fast = fast.next.next

# 2. reverse the second half
second = slow.next
slow.next = None                      # cut the list into two halves
prev = None
while second:
    nxt = second.next
    second.next = prev
    prev = second
    second = nxt
second = prev                         # head of the reversed second half

# 3. merge the two halves, alternating nodes
first = head
while second:
    tmp1, tmp2 = first.next, second.next
    first.next = second
    second.next = tmp1
    first, second = tmp1, tmp2
```

Building blocks: [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md) · [multiple-return-values](../syntax/multiple-return-values.md) (tuple assignment)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each of the three phases is a linear pass.
**Space: O(1)** — nodes are relinked in place.
</details>

---

### 19. Remove Nth Node From End of List — Medium
[LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)  
[Solution file (no hints)](../../problems/0001-0499/19.py)

Remove the nth node from the end of a list in one pass. Without knowing the list's length up front, how does a gap of `n` nodes between two pointers locate "n from the end"?

<details>
<summary>Hint</summary>

Move a `fast` pointer `n` steps ahead first, then advance `fast` and `slow` together on this [linked list](../data-structures/linked-list.md). When `fast` hits the end, `slow` sits right before the node to remove.
</details>

<details>
<summary>Solution</summary>

```python
dummy = ListNode(next=head)          # handles removing the head cleanly
slow = fast = dummy

for _ in range(n):                     # advance fast n steps ahead first
    fast = fast.next

while fast.next:                       # move both until fast reaches the last node
    slow = slow.next
    fast = fast.next

slow.next = slow.next.next            # skip over the node to remove
return dummy.next
```

Building blocks: [class-basics](../syntax/class-basics.md) · [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass through the list (length n).
**Space: O(1)** — a dummy node and two pointers.
</details>

---

### 138. Copy List with Random Pointer — Medium
[LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/)  
Solution: not yet solved in this repo.

Deep-copy a list where each node has a `next` pointer and a `random` pointer to any node (or None). Since `random` pointers can point *forward* to nodes you haven't copied yet, what lets you fill them in without a second pass?

<details>
<summary>Hint</summary>

Build a [hashmap](../data-structures/hashmap.md) from original node -> copied node in a first pass (creating every copy with empty `next`/`random`). In a second pass, use that map to wire up each copy's `next` and `random` using the *original* node's pointers as the lookup key.
</details>

<details>
<summary>Solution</summary>

```python
old_to_copy = {None: None}           # None maps to None, avoids edge-case checks

curr = head
while curr:                           # first pass: create every copy node
    old_to_copy[curr] = Node(curr.val)
    curr = curr.next

curr = head
while curr:                           # second pass: wire up next/random
    copy = old_to_copy[curr]
    copy.next = old_to_copy[curr.next]
    copy.random = old_to_copy[curr.random]
    curr = curr.next

return old_to_copy[head]
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes over the list.
**Space: O(n)** — the hashmap holds every node once.
</details>

---

### 2. Add Two Numbers — Medium
[LeetCode](https://leetcode.com/problems/add-two-numbers/)  
Solution: not yet solved in this repo.

Two numbers are given as linked lists of digits in reverse order. Add them and return the sum as a linked list. How does elementary-school column addition, digit by digit with a carry, map directly onto walking both lists together?

<details>
<summary>Hint</summary>

Walk both [linked lists](../data-structures/linked-list.md) simultaneously, summing corresponding digits plus a running carry, and build a new list one digit-node at a time — exactly like adding numbers by hand from the ones place up.
</details>

<details>
<summary>Solution</summary>

```python
dummy = ListNode()
tail = dummy
carry = 0

while l1 or l2 or carry:              # while loop: stop once both lists and carry are exhausted
    v1 = l1.val if l1 else 0
    v2 = l2.val if l2 else 0
    total = v1 + v2 + carry
    carry = total // 10                  # carry over to the next digit
    tail.next = ListNode(total % 10)     # this digit of the result
    tail = tail.next

    l1 = l1.next if l1 else None
    l2 = l2.next if l2 else None

return dummy.next
```

Building blocks: [class-basics](../syntax/class-basics.md) · [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`, `%`) · [ternary-expression](../syntax/ternary-expression.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(max(m, n))** — one pass across the longer of the two lists.
**Space: O(max(m, n))** — for the output list (not counting the returned result, O(1) extra).
</details>

---

### 141. Linked List Cycle — Easy
[LeetCode](https://leetcode.com/problems/linked-list-cycle/)  
[Solution file (no hints)](../../problems/0001-0499/141.py)

Determine if a linked list has a cycle, without extra memory. Why must a pointer moving twice as fast as another eventually land on the same node if a cycle exists?

<details>
<summary>Hint</summary>

Floyd's cycle detection ("tortoise and hare") on this [linked list](../data-structures/linked-list.md): if `fast` ever equals `slow`, there's a cycle. If `fast` reaches the end (`None`), there isn't.
</details>

<details>
<summary>Solution</summary>

```python
slow, fast = head, head
while fast and fast.next:              # while loop, fast can still move 2 steps
    slow = slow.next
    fast = fast.next.next
    if slow == fast:                     # they met: there's a cycle
        return True
return False
```

Building blocks: [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md) / [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — the fast pointer covers the list (and any cycle) in a bounded number of steps.
**Space: O(1)** — two pointers, no extra data structure.
</details>

---

### 287. Find the Duplicate Number — Medium
[LeetCode](https://leetcode.com/problems/find-the-duplicate-number/)  
Solution: not yet solved in this repo.

Given `n+1` integers in range `[1, n]`, find the one duplicate without modifying the array or using extra space. How does treating `nums[i] -> nums[nums[i]]` as a linked-list "next pointer" turn this into a cycle-detection problem?

<details>
<summary>Hint</summary>

Because a value repeats, following `i -> nums[i]` as a chain of pointers must eventually loop — that loop's entry point is the duplicate. Run Floyd's cycle detection (same idea as [141](#141-linked-list-cycle--easy)) on this implicit linked list.
</details>

<details>
<summary>Solution</summary>

```python
slow, fast = nums[0], nums[0]

while True:                            # phase 1: find a meeting point inside the cycle
    slow = nums[slow]
    fast = nums[nums[fast]]
    if slow == fast:
        break

slow2 = nums[0]                        # phase 2: find the cycle's entrance
while slow != slow2:
    slow = nums[slow]
    slow2 = nums[slow2]

return slow                          # the entrance is the duplicate value
```

Building blocks: [while-loop](../syntax/while-loop.md) · [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — Floyd's algorithm runs in linear time.
**Space: O(1)** — no extra data structure, and the input array isn't modified.
</details>

---

### 146. LRU Cache — Medium
[LeetCode](https://leetcode.com/problems/lru-cache/)  
[Solution file (no hints)](../../problems/0001-0499/146.py)

Design a cache with O(1) get/put that evicts the least-recently-used item when full. Why does pairing a [hashmap](../data-structures/hashmap.md) with a [doubly linked list](../data-structures/doubly-linked-list.md) give you O(1) for both "find this key" and "move it to most-recently-used"?

<details>
<summary>Hint</summary>

The hashmap gives O(1) lookup from key to its node; the doubly linked list keeps nodes ordered by recency so moving a node to the front (most-recent) or evicting from the back (least-recent) is an O(1) pointer operation.
</details>

<details>
<summary>Solution</summary>

```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}                    # key -> Node
        self.left = Node(0, 0)              # dummy head (least recent side)
        self.right = Node(0, 0)             # dummy tail (most recent side)
        self.left.next, self.right.prev = self.right, self.left

    def remove(self, node):                # unlink a node from the list
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def insert(self, node):                # insert node right before the tail (most recent)
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key):
        if key not in self.cache:
            return -1
        self.remove(self.cache[key])
        self.insert(self.cache[key])         # mark as most recently used
        return self.cache[key].val

    def put(self, key, value):
        if key in self.cache:
            self.remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        if len(self.cache) > self.cap:        # evict least recently used
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]
```

Building blocks: [class-basics](../syntax/class-basics.md) · [dict-basics](../syntax/dict-basics.md) · [membership-operators](../syntax/membership-operators.md) · [dunder-methods](../syntax/dunder-methods.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** for both `get` and `put`.
**Space: O(capacity)** — the hashmap and linked list both hold at most `capacity` entries.
</details>

---

### 23. Merge k Sorted Lists — Hard
[LeetCode](https://leetcode.com/problems/merge-k-sorted-lists/)  
[Solution file (no hints)](../../problems/0001-0499/23.py)

Merge k sorted linked lists into one. Why is merging the lists two-at-a-time in pairs (divide and conquer) faster than repeatedly merging one list into a growing result?

<details>
<summary>Hint</summary>

Reuse [Merge Two Sorted Lists (21)](#21-merge-two-sorted-lists--easy) but call it in pairs, halving the number of lists each round — like the merge step of [merge sort](../algorithms/merge-sort.md) — instead of merging sequentially one list at a time.
</details>

<details>
<summary>Solution</summary>

```python
def merge_two(l1, l2):                 # same routine as problem 21
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 if l1 else l2
    return dummy.next

if not lists:
    return None

while len(lists) > 1:                  # pair up and merge, halving each round
    merged = []
    for i in range(0, len(lists), 2):
        l1 = lists[i]
        l2 = lists[i + 1] if (i + 1) < len(lists) else None
        merged.append(merge_two(l1, l2))
    lists = merged

return lists[0]
```

Building blocks: [range-function](../syntax/range-function.md) (step argument) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(N log k)** — N total nodes across k lists, merged in O(log k) rounds of pairwise merges.
**Space: O(log k)** — recursion/iteration overhead for the pairing rounds (not counting the output).
</details>

---

### 25. Reverse Nodes in k-Group — Hard
[LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/)  
Solution: not yet solved in this repo.

Reverse the nodes of a linked list, k at a time. How does reusing "reverse a linked list" ([206](#206-reverse-linked-list--easy)) on each k-sized chunk, then relinking the chunks, solve this?

<details>
<summary>Hint</summary>

First check that at least k nodes remain (a partial final group is left alone). Then reverse exactly k nodes as in [206](#206-reverse-linked-list--easy), and connect the group before it to the new head, and the new tail to whatever comes after.
</details>

<details>
<summary>Solution</summary>

```python
def get_kth(node, k):                  # walk k nodes forward, or return None if too short
    while node and k > 0:
        node = node.next
        k -= 1
    return node

dummy = ListNode(next=head)
group_prev = dummy

while True:
    kth = get_kth(group_prev, k)
    if not kth:                           # fewer than k nodes left: stop, leave as-is
        break
    group_next = kth.next

    prev, curr = group_next, group_prev.next
    while curr != group_next:              # reverse this group of k nodes
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    tmp = group_prev.next                  # old head of the group is now its tail
    group_prev.next = kth                    # new head of the reversed group
    group_prev = tmp

return dummy.next
```

Building blocks: [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited a constant number of times across all groups.
**Space: O(1)** — nodes are relinked in place.
</details>
