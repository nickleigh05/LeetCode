# Stack

## What is a Stack?
A stack is a linear data structure that follows the **Last In, First Out (LIFO)** principle. The last element added is the first one to be removed.

Think of it like a stack of plates - you add plates on top and remove from the top.

## Visual Representation

```
Push operations:        Pop operations:

Push(1):               Pop():
┌─────┐                ┌─────┐
│  1  │ ← top          │  3  │ ← pop this
└─────┘                ├─────┤
                       │  2  │ ← new top
Push(2):               ├─────┤
┌─────┐                │  1  │
│  2  │ ← top          └─────┘
├─────┤
│  1  │                Result: 3
└─────┘

Push(3):
┌─────┐
│  3  │ ← top
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘
```

## Basic Operations

### 1. Push (Add element)
```
Initial:               After push(4):
┌─────┐                ┌─────┐
│  3  │                │  4  │ ← new top
├─────┤                ├─────┤
│  2  │                │  3  │
├─────┤                ├─────┤
│  1  │                │  2  │
└─────┘                ├─────┤
                       │  1  │
                       └─────┘

Time: O(1)
```

### 2. Pop (Remove top element)
```
Initial:               After pop():
┌─────┐                ┌─────┐
│  4  │ ← remove       │  3  │ ← new top
├─────┤                ├─────┤
│  3  │                │  2  │
├─────┤                ├─────┤
│  2  │                │  1  │
├─────┤                └─────┘
│  1  │
└─────┘                Return: 4

Time: O(1)
```

### 3. Peek/Top (View top element)
```
┌─────┐
│  4  │ ← peek returns 4 (doesn't remove)
├─────┤
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Time: O(1)
```

### 4. IsEmpty (Check if empty)
```
Empty stack:           Non-empty stack:
                       ┌─────┐
(empty)                │  1  │
                       └─────┘

isEmpty(): True        isEmpty(): False
```

## Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Push      | O(1)          |
| Pop       | O(1)          |
| Peek/Top  | O(1)          |
| Search    | O(n)          |
| IsEmpty   | O(1)          |

## Stack Implementation

### Using Array/List
```
Array-based stack:
                              ┌── top index
                              ↓
Index:  0     1     2     3   4
      ┌─────┬─────┬─────┬─────┬─────┐
Array:│  1  │  2  │  3  │  4  │  5  │
      └─────┴─────┴─────┴─────┴─────┘

Push: Increment top, add element
Pop:  Remove element, decrement top
```

### Using Linked List
```
Linked List Stack (top at head):

top → [5] → [4] → [3] → [2] → [1] → null

Push: Add new node at head
Pop:  Remove head node
```

## Common Stack Patterns

### 1. Balanced Parentheses
```
Input: "({[]})"

Process each character:

'(' → push
┌─────┐
│  (  │
└─────┘

'{' → push
┌─────┐
│  {  │
├─────┤
│  (  │
└─────┘

'[' → push
┌─────┐
│  [  │
├─────┤
│  {  │
├─────┤
│  (  │
└─────┘

']' → pop '[', matches ✓
┌─────┐
│  {  │
├─────┤
│  (  │
└─────┘

'}' → pop '{', matches ✓
┌─────┐
│  (  │
└─────┘

')' → pop '(', matches ✓
(empty) → Valid!
```

### 2. Next Greater Element
```
arr = [2, 1, 2, 4, 3]

Find next greater element for each:

Process from right to left:

Index 4: value = 3
Stack: empty
Result[4] = -1
┌─────┐
│  3  │
└─────┘

Index 3: value = 4
Pop 3 (smaller than 4)
Result[3] = -1
┌─────┐
│  4  │
└─────┘

Index 2: value = 2
4 > 2, so Result[2] = 4
┌─────┐
│  4  │
├─────┤
│  2  │
└─────┘

Index 1: value = 1
2 > 1, so Result[1] = 2
┌─────┐
│  4  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Index 0: value = 2
Pop 1, pop 2, 4 > 2
Result[0] = 4
┌─────┐
│  4  │
├─────┤
│  2  │
└─────┘

Result: [4, 2, 4, -1, -1]
```

### 3. Evaluate Postfix Expression
```
Expression: "2 3 + 5 *"
(means: (2 + 3) * 5)

Step 1: Read '2'
┌─────┐
│  2  │
└─────┘

Step 2: Read '3'
┌─────┐
│  3  │
├─────┤
│  2  │
└─────┘

Step 3: Read '+'
Pop 3, 2
Calculate: 2 + 3 = 5
┌─────┐
│  5  │
└─────┘

Step 4: Read '5'
┌─────┐
│  5  │
├─────┤
│  5  │
└─────┘

Step 5: Read '*'
Pop 5, 5
Calculate: 5 * 5 = 25
┌─────┐
│ 25  │
└─────┘

Result: 25
```

### 4. Daily Temperatures
```
temps = [73, 74, 75, 71, 69, 72, 76, 73]
Find days until warmer temperature

Process from right to left:

Index 7: temp = 73
Stack: empty
Result[7] = 0
┌──────┐
│ (7,73)│
└──────┘

Index 6: temp = 76
Pop (7,73) - 76 > 73
Result[6] = 0
┌──────┐
│ (6,76)│
└──────┘

Index 5: temp = 72
76 > 72, Result[5] = 6 - 5 = 1
┌──────┐
│ (6,76)│
├──────┤
│ (5,72)│
└──────┘

Continue...

Visual result:
Days:  1   1   4   2   1   1   0   0
Temp: 73  74  75  71  69  72  76  73
       ↓→74
          ↓→75
             ↓──────→76
                ↓→72
                   ↓→72
```

## Monotonic Stack

A stack that maintains elements in increasing or decreasing order.

### Monotonic Increasing Stack
```
arr = [3, 1, 4, 1, 5]

Process each element:

3: Stack empty
┌─────┐
│  3  │
└─────┘

1: 1 < 3, pop 3
┌─────┐
│  1  │
└─────┘

4: 4 > 1, push
┌─────┐
│  4  │
├─────┤
│  1  │
└─────┘

1: 1 < 4, pop 4, 1 = 1, pop 1
┌─────┐
│  1  │
└─────┘

5: 5 > 1, push
┌─────┐
│  5  │
├─────┤
│  1  │
└─────┘

Bottom → Top: [1, 5] (increasing)
```

### Monotonic Decreasing Stack
```
arr = [3, 1, 4, 1, 5]

Process each element:

3: Stack empty
┌─────┐
│  3  │
└─────┘

1: 1 < 3, push
┌─────┐
│  1  │
├─────┤
│  3  │
└─────┘

4: 4 > 1, pop until empty or top > 4
┌─────┐
│  4  │
└─────┘

1: 1 < 4, push
┌─────┐
│  1  │
├─────┤
│  4  │
└─────┘

5: 5 > 1, pop all
┌─────┐
│  5  │
└─────┘

Bottom → Top: [5] (would be decreasing if more elements)
```

## Advanced Stack Problems

### 1. Largest Rectangle in Histogram
```
heights = [2, 1, 5, 6, 2, 3]

Visualization:
        ┌───┐
        │   │
    ┌───┤   │
    │   │   │       ┌───┐
┌───┤   │   ├───┬───┤   │
│   │   │   │   │   │   │
│ 2 │ 1 │ 5 │ 6 │ 2 │ 3 │
└───┴───┴───┴───┴───┴───┘
  0   1   2   3   4   5

Use stack to track increasing heights:

Index 0: height = 2
┌─────┐
│  0  │
└─────┘

Index 1: height = 1 (< 2)
Pop 0, calculate area with height 2
Area = 2 × 1 = 2
┌─────┐
│  1  │
└─────┘

Index 2: height = 5 (> 1)
┌─────┐
│  2  │
├─────┤
│  1  │
└─────┘

Index 3: height = 6 (> 5)
┌─────┐
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Index 4: height = 2 (< 6)
Pop 3: area = 6 × 1 = 6
Pop 2: area = 5 × 2 = 10 ✓ (maximum)

Maximum area = 10
```

### 2. Min Stack
```
Design stack that supports getMin() in O(1)

Regular Stack:    Min Stack:
┌─────┐           ┌─────┐
│  3  │           │  1  │ ← current min
├─────┤           ├─────┤
│  5  │           │  1  │
├─────┤           ├─────┤
│  1  │           │  1  │
├─────┤           ├─────┤
│  2  │           │  2  │
└─────┘           └─────┘

Push 3:
Regular: [2, 1, 5, 3]
Min:     [2, 1, 1, 1]  getMin() = 1

Pop:
Regular: [2, 1, 5]
Min:     [2, 1, 1]     getMin() = 1
```

### 3. Valid Stack Sequences
```
pushed = [1, 2, 3, 4, 5]
popped = [4, 5, 3, 2, 1]

Simulate:

Push 1:
┌─────┐
│  1  │
└─────┘

Push 2:
┌─────┐
│  2  │
├─────┤
│  1  │
└─────┘

Push 3:
┌─────┐
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Push 4:
┌─────┐
│  4  │ ← matches popped[0], pop!
├─────┤
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

After pop 4:
┌─────┐
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Push 5:
┌─────┐
│  5  │ ← matches popped[1], pop!
├─────┤
│  3  │
├─────┤
│  2  │
├─────┤
│  1  │
└─────┘

Continue... Valid sequence ✓
```

## Stack vs Other Data Structures

### Stack vs Queue
```
Stack (LIFO):          Queue (FIFO):
┌─────┐                ┌─────┬─────┬─────┐
│  3  │ ← push/pop     │  1  │  2  │  3  │
├─────┤                └─────┴─────┴─────┘
│  2  │                  ↑           ↑
├─────┤                front        rear
│  1  │                dequeue      enqueue
└─────┘
```

## Python Implementation

```python
# Using list
stack = []
stack.append(1)      # Push
stack.append(2)
top = stack[-1]      # Peek: 2
val = stack.pop()    # Pop: 2
is_empty = len(stack) == 0

# Using collections.deque (more efficient)
from collections import deque
stack = deque()
stack.append(1)      # Push
top = stack[-1]      # Peek
val = stack.pop()    # Pop

# Custom Stack class
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
```

## Common Use Cases

1. **Function Call Stack**
```
main() calls foo() calls bar():

┌──────────┐
│  bar()   │ ← currently executing
├──────────┤
│  foo()   │ ← waiting
├──────────┤
│  main()  │ ← waiting
└──────────┘

When bar() returns, pop from stack
```

2. **Undo Mechanism**
```
Text editor actions:

┌──────────────┐
│ Delete "o"   │ ← most recent action
├──────────────┤
│ Type "llo"   │
├──────────────┤
│ Type "He"    │
└──────────────┘

Undo: Pop and reverse action
```

3. **Browser History (back button)**
```
┌──────────────────┐
│ page3.com        │ ← current page
├──────────────────┤
│ page2.com        │
├──────────────────┤
│ page1.com        │
└──────────────────┘

Back: Pop current, go to previous
```

4. **Expression Evaluation**
```
Infix: 3 + 4 * 2
Postfix: 3 4 2 * +

Operators stack for conversion/evaluation
```

## Key Takeaways

1. **LIFO Principle**: Last In, First Out
2. **O(1) Operations**: Push, pop, peek are constant time
3. **Use Cases**:
   - Reversing
   - Parentheses matching
   - Expression evaluation
   - DFS traversal
   - Backtracking
   - Undo/Redo

4. **Common Patterns**:
   - Monotonic stack for next greater/smaller
   - Two stacks for queue implementation
   - Stack for recursion simulation

5. **When to Use**:
   - Need to access most recent element
   - Nested structures (parentheses, HTML tags)
   - Reversing order
   - Backtracking algorithms
