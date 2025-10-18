# Linked List

## What is a Linked List?
A linked list is a linear data structure where elements (nodes) are stored in non-contiguous memory locations. Each node contains data and a reference (pointer) to the next node.

Unlike arrays, linked lists don't require contiguous memory and can grow/shrink dynamically.

## Types of Linked Lists

### 1. Singly Linked List
Each node points to the next node:

```
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
data  next    data  next   data  next   data  null

Node structure:
┌──────────┐
│  data    │
│  next────┼──→ (points to next node)
└──────────┘
```

### 2. Doubly Linked List
Each node points to both next and previous nodes:

```
head
 ↓
┌───┬───┬───┐    ┌───┬───┬───┐    ┌───┬───┬───┐
│ ∅ │ 1 │ ●─┼───→│ ●─┼ 2 │ ●─┼───→│ ●─┼ 3 │ ∅ │
└───┴───┴─┬─┘    └─┬─┴───┴─┬─┘    └─┬─┴───┴───┘
          │        │       │        │
          └────────┘       └────────┘
         prev ←          prev ←

Node structure:
┌──────────┐
│  prev────┼──→ (points to previous node)
│  data    │
│  next────┼──→ (points to next node)
└──────────┘
```

### 3. Circular Linked List
Last node points back to the first node:

```
     head
      ↓
    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
    │ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼──┐
    └─┬─┴───┘    └───┴───┘    └───┴───┘  │
      ↑                                   │
      └───────────────────────────────────┘
```

## Basic Operations

### 1. Insertion at Head
```
Initial List:
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘

Insert 1 at head:
Step 1: Create new node
┌───┬───┐
│ 1 │ ? │
└───┴───┘

Step 2: Point new node to current head
new_node.next = head

┌───┬───┐
│ 1 │ ●─┼──┐
└───┴───┘  │
           ↓
head      ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
 ↓        │ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
          └───┴───┘    └───┴───┘    └───┴───┘

Step 3: Update head
head = new_node

head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Time: O(1)
```

### 2. Insertion at Tail
```
Initial List:
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘

Insert 4 at tail:
Step 1: Traverse to last node
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘
                            ↑
                          last

Step 2: Create new node and link
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Time: O(n) - need to traverse to end
With tail pointer: O(1)
```

### 3. Insertion at Middle
```
Insert 2.5 after node with value 2:

head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘
              ↑
            curr

Step 1: Create new node
┌─────┬───┐
│ 2.5 │ ? │
└─────┴───┘

Step 2: new_node.next = curr.next
┌─────┬───┐
│ 2.5 │ ●─┼──┐
└─────┴───┘  │
             ↓
        ┌───┬───┐
        │ 3 │ ∅ │
        └───┴───┘

Step 3: curr.next = new_node
┌───┬───┐    ┌─────┬───┐    ┌───┬───┐
│ 2 │ ●─┼───→│ 2.5 │ ●─┼───→│ 3 │ ∅ │
└───┴───┘    └─────┴───┘    └───┴───┘

Time: O(1) if we have the node
      O(n) to find the node
```

### 4. Deletion
```
Delete node with value 2:

Initial:
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
  ↑            ↑
 prev        curr (to delete)

Step 1: prev.next = curr.next (bypass the node)
head
 ↓
┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘

┌───┬───┐
│ 2 │ X │ (orphaned, will be garbage collected)
└───┴───┘

Time: O(n) - need to find the node
```

## Common Linked List Problems

### 1. Reverse Linked List
```
Initial:
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Step 1: Reverse first link
prev=∅  curr=1  next=2

┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ∅ │    │ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Step 2: Reverse second link
prev=1  curr=2  next=3

┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ∅ │ ←──┼ 2 │ ? │    │ 3 │ ●─┼───→│ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Step 3: Continue until end

Final:
                                        head
                                         ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ∅ │ ←──┼ 2 │ ? │ ←──┼ 3 │ ? │ ←──┼ 4 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Result: 4 → 3 → 2 → 1 → null
```

### 2. Find Middle (Fast & Slow Pointers)
```
head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
S,F

After 1 iteration:
              S             F
              ↓             ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

After 2 iterations:
                            S                         F
                            ↓                         ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Fast reached end, Slow is at middle! ✓
```

### 3. Detect Cycle (Floyd's Algorithm)
```
Linked list with cycle:

head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼──┐
└───┴───┘    └───┴───┘    └───┴─┬─┘    └───┴───┘  │
                                 ↑                  │
                                 └──────────────────┘

Initially:
S,F at head

After iterations:
S = 1, F = 2
S = 2, F = 4
S = 3, F = 3  → S == F, cycle detected! ✓

No cycle:
S and F will never meet, F reaches null
```

### 4. Remove Nth Node from End
```
Remove 2nd node from end:

head
 ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
                                         ↑ (to remove)

Step 1: Move fast n steps ahead
S             F (n=2 steps ahead)
↓             ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘

Step 2: Move both until fast reaches end
              S                         F
              ↓                         ↓
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 3 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
                           (to remove)

Step 3: Remove node
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬───┐
│ 1 │ ●─┼───→│ 2 │ ●─┼───→│ 4 │ ●─┼───→│ 5 │ ∅ │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴───┘
```

### 5. Merge Two Sorted Lists
```
List 1:  1 → 3 → 5 → null
List 2:  2 → 4 → 6 → null

Step 1: Compare 1 and 2
dummy → 1
        ↓
List1: 3 → 5 → null
List2: 2 → 4 → 6 → null

Step 2: Compare 3 and 2
dummy → 1 → 2
            ↓
List1: 3 → 5 → null
List2: 4 → 6 → null

Step 3: Compare 3 and 4
dummy → 1 → 2 → 3
                ↓
List1: 5 → null
List2: 4 → 6 → null

Continue...

Result: 1 → 2 → 3 → 4 → 5 → 6 → null
```

### 6. Reorder List
```
L0 → L1 → L2 → L3 → L4 → L5

Reorder to:
L0 → L5 → L1 → L4 → L2 → L3

Steps:
1. Find middle
2. Reverse second half
3. Merge two halves

Initial:
1 → 2 → 3 → 4 → 5 → 6

After finding middle:
First half:  1 → 2 → 3
Second half: 4 → 5 → 6

After reversing second half:
First half:  1 → 2 → 3
Second half: 6 → 5 → 4

Merge alternately:
1 → 6 → 2 → 5 → 3 → 4
```

## Doubly Linked List Operations

```
Insert after node:

Initial:
┌───┬───┬───┐    ┌───┬───┬───┐    ┌───┬───┬───┐
│ ∅ │ 1 │ ●─┼───→│ ●─┼ 2 │ ●─┼───→│ ●─┼ 3 │ ∅ │
└───┴───┴─┬─┘    └─┬─┴───┴─┬─┘    └─┬─┴───┴───┘
          │        │       │        │
          └────────┘       └────────┘

Insert 1.5 after node 1:

Step 1: Create new node
┌───┬─────┬───┐
│ ? │ 1.5 │ ? │
└───┴─────┴───┘

Step 2: Set pointers
new.next = curr.next
new.prev = curr
curr.next.prev = new
curr.next = new

Result:
┌───┬───┬───┐  ┌───┬─────┬───┐  ┌───┬───┬───┐  ┌───┬───┬───┐
│ ∅ │ 1 │ ●─┼─→│ ●─┼ 1.5 │ ●─┼─→│ ●─┼ 2 │ ●─┼─→│ ●─┼ 3 │ ∅ │
└───┴───┴─┬─┘  └─┬─┴─────┴─┬─┘  └─┬─┴───┴─┬─┘  └─┬─┴───┴───┘
          │      │         │      │       │      │
          └──────┘         └──────┘       └──────┘
```

## Time Complexity Comparison

| Operation         | Array | Linked List |
|------------------|-------|-------------|
| Access by index  | O(1)  | O(n)        |
| Search           | O(n)  | O(n)        |
| Insert at head   | O(n)  | O(1)        |
| Insert at tail   | O(1)  | O(n) or O(1)* |
| Insert at middle | O(n)  | O(n)        |
| Delete at head   | O(n)  | O(1)        |
| Delete at tail   | O(1)  | O(n)        |
| Delete at middle | O(n)  | O(n)        |

*O(1) with tail pointer

## Advantages vs Disadvantages

### Advantages
```
✓ Dynamic size
✓ Easy insertion/deletion at head: O(1)
✓ No wasted memory (grows as needed)
✓ No need for contiguous memory

Memory:
Array:     ┌─┬─┬─┬─┬─┬─┬─┬─┐ (contiguous)
           └─┴─┴─┴─┴─┴─┴─┴─┘

Linked:    ┌─┐   ┌─┐     ┌─┐    ┌─┐
           └─┘   └─┘     └─┘    └─┘
          (scattered in memory)
```

### Disadvantages
```
✗ No random access: O(n) to access element
✗ Extra memory for pointers
✗ Not cache-friendly (scattered memory)
✗ Reverse traversal difficult (in singly linked list)

Array access:    O(1)
arr[5] directly

Linked access:   O(n)
Must traverse from head
```

## Python Implementation

```python
# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Singly Linked List
class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_tail(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def delete(self, data):
        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        curr = self.head
        while curr.next:
            if curr.next.data == data:
                curr.next = curr.next.next
                return
            curr = curr.next

    def reverse(self):
        prev = None
        curr = self.head

        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        self.head = prev

    def find_middle(self):
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data if slow else None
```

## Key Takeaways

1. **Structure**: Nodes connected by pointers, not contiguous
2. **Types**: Singly, doubly, circular
3. **Best For**:
   - Frequent insertions/deletions at head
   - Unknown or changing size
   - Don't need random access

4. **Common Patterns**:
   - Fast & slow pointers
   - Dummy node for easier operations
   - Reversing pointers
   - Two-pointer techniques

5. **Interview Tips**:
   - Draw pictures!
   - Handle edge cases (empty list, single node)
   - Use dummy node to simplify code
   - Consider space constraints (in-place vs extra space)
