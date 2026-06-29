# 04. Stacks, Queues & Monotonic Stacks
*LIFO for "most recent unresolved"; a monotonic stack answers next-greater questions in one pass.*

[← Prev](03-sliding-window.md) · [🗺 Roadmap](../roadmap.md) · [Next →](05-binary-search.md)

---

A **stack** (LIFO) is the right tool whenever the most *recent* thing matters most: matching brackets, evaluating expressions, undo. A **queue/deque** (FIFO) handles the opposite order and powers BFS. The **monotonic stack** is the clever variant — by keeping the stack sorted as you push, you answer "what's the next greater element?" for every position in a single O(n) sweep.

## Concept

### Stack

```
  Push 3 → Push 1 → Push 4 → Pop

  After pushing 3, 1, 4:       After pop:
        ┌───┐                        ┌───┐
  top → │ 4 │                  top → │ 1 │
        ├───┤                        ├───┤
        │ 1 │                        │ 1 │  ← wait no:
        ├───┤                        ├───┤
        │ 3 │                        │ 3 │
        └───┘                        └───┘
       LIFO: Last In, First Out
```

**What it is:** A Last-In-First-Out (LIFO) collection. The last element pushed is the first one popped. Implemented with a Python list using `append`/`pop`.

**Key Properties:**
- O(1) push and pop (from the top)
- O(n) search (must scan)
- No random access
- The call stack in recursion is itself a stack — recursive DFS uses the implicit call stack

**Complexity:**

| Operation | Time |
|-----------|------|
| Push (append) | O(1) |
| Pop | O(1) |
| Peek (top) | O(1) |
| Search | O(n) |
| Space | O(n) |

**Use when:**
- Matching/balancing: parentheses, brackets, tags
- Tracking state as you go deeper (DFS iteratively)
- "Undo" operations — most recent action is most relevant
- Evaluating expressions (postfix notation)
- Keeping a history of previous states

**Python:**
```python
stack = []
stack.append(1)   # push
stack.append(2)
stack.append(3)
stack.pop()       # 3 — O(1)
stack[-1]         # peek top without removing → 2
if stack:         # check not empty
    ...
```

### Queue and Deque

```
  Queue (FIFO):
  Enqueue →  [ 1 | 2 | 3 | 4 ]  → Dequeue
             front             back
             (popleft)         (append)

  Deque (Double-Ended Queue):
  appendleft ←  [ 1 | 2 | 3 | 4 ]  → append
  popleft    →                      ← pop
               O(1) on both ends!
```

**What it is:** A Queue is a First-In-First-Out (FIFO) structure. A Deque (double-ended queue) allows O(1) insertions and deletions from both ends. Always use `collections.deque`, not a plain list (list's `pop(0)` is O(n)).

**Key Properties:**
- Queue: enqueue at back, dequeue from front — both O(1)
- Deque: O(1) at both ends
- BFS requires a queue (not a stack) to guarantee shortest-path exploration
- A deque with a size limit is the sliding window max trick

**Complexity:**

| Operation | Queue | Deque |
|-----------|-------|-------|
| Enqueue / append | O(1) | O(1) |
| Dequeue / popleft | O(1) | O(1) |
| Append left | — | O(1) |
| Pop right | — | O(1) |
| Peek | O(1) | O(1) |
| Space | O(n) | O(n) |

**Use when:**
- BFS traversal (tree level-order, shortest path in grid)
- Processing items in the order they arrived
- Sliding window maximum/minimum (deque stores indices in monotonic order)
- Multi-source BFS (start with multiple nodes in the queue)

**Python:**
```python
from collections import deque

q = deque()
q.append(1)        # enqueue right
q.append(2)
q.popleft()        # dequeue left → 1  (O(1)!)
q.appendleft(0)    # O(1)
q.pop()            # O(1) from right
q[0]               # peek front
q[-1]              # peek back

# BFS template
q = deque([start])
visited = {start}
while q:
    node = q.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            q.append(neighbor)
```

### Monotonic Stack

```
  Array:  [2, 1, 5, 6, 2, 3]
  Goal: find "next greater element" for each index

  Process left to right, maintain a DECREASING stack:

  i=0, val=2:  stack=[]         push 2  → stack=[2]
  i=1, val=1:  1 < 2, push     → stack=[2,1]
  i=2, val=5:  5 > 1, pop 1 (next greater of 1 = 5)
               5 > 2, pop 2 (next greater of 2 = 5)
               push 5          → stack=[5]
  i=3, val=6:  6 > 5, pop 5 (next greater of 5 = 6)
               push 6          → stack=[6]
  i=4, val=2:  2 < 6, push     → stack=[6,2]
  i=5, val=3:  3 > 2, pop 2 (next greater of 2 = 3)
               3 < 6, push     → stack=[6,3]

  Result: [5, 5, 6, -1, 3, -1]
            ↑                ↑
           next greater   no next greater → -1
```

**What it is:** A stack that maintains a monotonically increasing or decreasing order. When a new element violates the order, you pop elements (and that's usually when you record the answer).

**Key Properties:**
- Each element is pushed and popped at most once → O(n) total
- Decreasing stack: useful for "next greater element"
- Increasing stack: useful for "next smaller element"
- Store indices, not values — you'll often need the position too

**Complexity:**

| Operation | Time |
|-----------|------|
| Process entire array | O(n) total |
| Space | O(n) |

**Use when:**
- Next Greater Element / Next Smaller Element
- Largest Rectangle in Histogram
- Daily Temperatures
- Trapping Rain Water
- Maximum width ramp

**Python:**
```python
# Next Greater Element template
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, maintains decreasing values

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]   # nums[i] is next greater for idx
        stack.append(i)

    return result

# Increasing monotonic stack (next smaller element)
def next_smaller(nums):
    result = [-1] * len(nums)
    stack = []
    for i, val in enumerate(nums):
        while stack and val < nums[stack[-1]]:
            result[stack.pop()] = val
        stack.append(i)
    return result
```

## The Pattern

### Monotonic Stack

```
  Daily Temperatures — find days until warmer:
  temps = [73, 74, 75, 71, 69, 72, 76, 73]

  Maintain a DECREASING stack of indices:

  i=0 (73):  stack=[]         → push 0      stack=[0]
  i=1 (74):  74>73 → pop 0,  result[0]=1-0=1  → push 1  stack=[1]
  i=2 (75):  75>74 → pop 1,  result[1]=2-1=1  → push 2  stack=[2]
  i=3 (71):  71<75 → push 3                   stack=[2,3]
  i=4 (69):  69<71 → push 4                   stack=[2,3,4]
  i=5 (72):  72>69 → pop 4,  result[4]=5-4=1
             72>71 → pop 3,  result[3]=5-3=2
             72<75 → push 5                   stack=[2,5]
  i=6 (76):  76>72 → pop 5,  result[5]=6-5=1
             76>75 → pop 2,  result[2]=6-2=4
             push 6                           stack=[6]
  i=7 (73):  73<76 → push 7                   stack=[6,7]
  End: remaining stack → result[6]=result[7]=0

  Result: [1, 1, 4, 2, 1, 1, 0, 0]
```

**What it is:** A stack that is kept in monotonically increasing or decreasing order. When a new element breaks the order, we pop elements and record the answer for each popped element (the new element is the "answer" for those elements).

**Use this when:**
- [ ] "Next Greater Element" / "Next Smaller Element"
- [ ] "Previous Greater/Smaller Element"
- [ ] Largest Rectangle in Histogram
- [ ] Trapping Rain Water
- [ ] Daily Temperatures
- [ ] Maximum width ramp / Stock span problem

**Decreasing vs Increasing:**
- **Decreasing stack** → finds next GREATER element (new larger element pops)
- **Increasing stack** → finds next SMALLER element (new smaller element pops)

**Python:**
```python
# Next Greater Element — decreasing stack
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []   # stores indices
    for i, val in enumerate(nums):
        while stack and val > nums[stack[-1]]:
            result[stack.pop()] = val
        stack.append(i)
    return result

# Daily Temperatures
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and t > temps[stack[-1]]:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result

# Largest Rectangle in Histogram
def largest_rectangle(heights):
    stack = []   # increasing stack of indices
    max_area = 0
    heights.append(0)   # sentinel to flush stack
    for i, h in enumerate(heights):
        while stack and h < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# Trapping Rain Water
def trap(height):
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack: break
            width = i - stack[-1] - 1
            bounded_height = min(h, height[stack[-1]]) - height[bottom]
            water += width * bounded_height
        stack.append(i)
    return water
```

**Complexity:** O(n) — each element is pushed and popped at most once.

**Blind 75 examples:** (Directly used in Largest Rectangle in Histogram, Daily Temperatures)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/stack/`](../appendix/templates/stack/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/stack/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Stacks, Queues & Monotonic Stacks problems →**](../../lists/recommended.md#4-stack-16-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Binary Search & Sorting](05-binary-search.md) — halve any ordered search space — including the answer itself.

[← Prev](03-sliding-window.md) · [🗺 Roadmap](../roadmap.md) · [Next →](05-binary-search.md)

