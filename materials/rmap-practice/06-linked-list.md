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
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        prev = None
        curr = head

        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        return prev
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
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode(0)
        current = dummy

        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        if list1 is not None:
            current.next = list1
        else:
            current.next = list2

        return dummy.next
```

Building blocks: [class-basics](../syntax/class-basics.md) · [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md) (`is not None`) · [elif-else](../syntax/elif-else.md) · [none-type](../syntax/none-type.md)
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
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:

        if head is None or head.next is None:
            return

        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        second_half_head = slow.next
        slow.next = None

        previous_node = None
        current_node = second_half_head
        while current_node is not None:
            next_node = current_node.next
            current_node.next = previous_node
            previous_node = current_node
            current_node = next_node
        second_half_head = previous_node

        first_pointer = head
        second_pointer = second_half_head

        while second_pointer is not None:
            first_next = first_pointer.next
            second_next = second_pointer.next

            first_pointer.next = second_pointer
            second_pointer.next = first_next

            first_pointer = first_next
            second_pointer = second_next
```

Building blocks: [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md) (`is None` / `is not None`) · [logical-operators](../syntax/logical-operators.md) (`and`, `or`) · [none-type](../syntax/none-type.md)
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

Start `slow` and `fast` at a dummy node and move `fast` ahead `n + 1` steps, then advance both together on this [linked list](../data-structures/linked-list.md). When `fast` runs off the end, `slow` sits right before the node to remove.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        slow = dummy
        fast = dummy

        for _ in range(n + 1):
            fast = fast.next

        while fast is not None:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next

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
class Solution:
    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:

        old_to_copy = {None: None}

        curr = head
        while curr:
            old_to_copy[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
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
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode()
        tail = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            total = v1 + v2 + carry
            carry = total // 10
            tail.next = ListNode(total % 10)
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
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        slow = head
        fast = head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
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
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:

        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        slow2 = nums[0]
        while slow != slow2:
            slow = nums[slow]
            slow2 = nums[slow2]

        return slow
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
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.remove(node)
        self.add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.remove(node)
            self.add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            self.remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self.cache[key] = new_node
        self.add_to_front(new_node)
```

Building blocks: [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [dict-basics](../syntax/dict-basics.md) (`del cache[key]`) · [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)
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

Merge k sorted linked lists into one. If you could always grab the smallest current head among all k lists in O(log k), how would that build the merged list — and what structure gives you that?

<details>
<summary>Hint</summary>

Push each list's head node into a [min-heap](../data-structures/heap.md) keyed by node value (include the list index as a tie-breaker so nodes are never compared directly). Repeatedly pop the smallest node, append it to the result, and push that node's `next` in its place.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        min_heap = []

        for list_index in range(len(lists)):
            head_node = lists[list_index]
            if head_node is not None:
                heapq.heappush(min_heap, (head_node.val, list_index, head_node))

        dummy_head = ListNode()
        current_node = dummy_head

        while min_heap:
            smallest_val, list_index, smallest_node = heapq.heappop(min_heap)

            current_node.next = smallest_node
            current_node = current_node.next

            next_node = smallest_node.next
            if next_node is not None:
                heapq.heappush(min_heap, (next_node.val, list_index, next_node))

        current_node.next = None

        return dummy_head.next
```

Building blocks: [import-basics](../syntax/import-basics.md) (`import heapq`) · [tuple-basics](../syntax/tuple-basics.md) (heap entries) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(N log k)** — N total nodes across k lists, each pushed and popped once from a heap of at most k entries.
**Space: O(k)** — the heap holds at most one node per list (not counting the relinked output).
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
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        def get_kth(node, steps):
            while node and steps > 0:
                node = node.next
                steps -= 1
            return node

        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = get_kth(group_prev, k)
            if not kth:
                break
            group_next = kth.next

            prev = group_next
            curr = group_prev.next

            while curr != group_next:
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node

            group_tail = group_prev.next
            group_prev.next = kth
            group_prev = group_tail

        return dummy.next
```

Building blocks: [while-loop](../syntax/while-loop.md) · [function-basics](../syntax/function-basics.md) (inner `def`) · [break-continue](../syntax/break-continue.md) (`break`) · [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — every node is visited a constant number of times across all groups.
**Space: O(1)** — nodes are relinked in place.
</details>
