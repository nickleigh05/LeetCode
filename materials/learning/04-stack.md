# 04. Stacks, Queues & Monotonic Stacks
*LIFO for "most recent unresolved"; a monotonic stack answers next-greater questions in one pass.*

[← Prev](03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](04b-recursion.md)

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

## Algorithm Deep-Dive — Recognizing Monotonic Stack Problems

The pattern looks the same in code every time. The skill is *recognizing when you need it*. Every monotonic stack problem is one of four questions:

```
                      ┌─────────────────────────────────────────┐
                      │   For each element, find the nearest…    │
                      ├──────────────────┬──────────────────────┤
                      │   to the RIGHT   │   to the LEFT        │
  ┌───────────────────┼──────────────────┼──────────────────────┤
  │  element GREATER  │ Next Greater →   │ Previous Greater ←   │
  │                   │ (decreasing stk) │ (decreasing stk)     │
  ├───────────────────┼──────────────────┼──────────────────────┤
  │  element SMALLER  │ Next Smaller →   │ Previous Smaller ←   │
  │                   │ (increasing stk) │ (increasing stk)     │
  └───────────────────┴──────────────────┴──────────────────────┘

  → direction: scan left to right, push index, pop when condition met
  ← direction: scan right to left (or use the stack's remaining elements
    after a left-to-right pass — they're the "unanswered" questions)
```

**Four templates, one skeleton:**

```python
# Next Greater Element (right) — decreasing stack
result = [-1] * n
stack = []
for i in range(n):
    while stack and nums[i] > nums[stack[-1]]:
        result[stack.pop()] = nums[i]     # nums[i] is the answer for popped element
    stack.append(i)

# Previous Greater Element (left) — decreasing stack, scan right
result = [-1] * n
stack = []
for i in range(n):
    while stack and nums[i] >= nums[stack[-1]]:
        stack.pop()                        # pop smaller/equal elements, they can't be the answer
    if stack: result[i] = nums[stack[-1]] # stack top is nearest greater to the left
    stack.append(i)

# Next Smaller (right) — increasing stack (flip the comparison)
# Previous Smaller (left) — same shape, flip comparison
```

**Monotonic Deque — sliding window maximum:**

When the window slides, you also need to *evict old elements from the front*. A deque gives you O(1) pop from both ends:

```
  nums=[1,3,-1,-3,5,3,6,7], k=3
  Window max using a decreasing deque (stores indices):

  i=0 (1):  dq=[0]
  i=1 (3):  3>1 → pop 0,  dq=[1]
  i=2 (-1): dq=[1,2],  window=[0..2]: max = nums[dq[0]] = nums[1] = 3
  i=3 (-3): dq=[1,2,3], window=[1..3]: max = nums[1] = 3
  i=4 (5):  pop 3,2,1 (all < 5), dq=[4], window=[2..4]: max = 5
  i=5 (3):  dq=[4,5],  window=[3..5]: max = 5
  i=6 (6):  pop 5,4, dq=[6], window=[4..6]: max = 6
  i=7 (7):  pop 6, dq=[7], window=[5..7]: max = 7
```

```python
from collections import deque

def sliding_window_max(nums, k):
    dq = deque()   # indices, decreasing by value
    result = []
    for i, n in enumerate(nums):
        # evict indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # maintain decreasing order
        while dq and n > nums[dq[-1]]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])   # front is always the window max
    return result
```

**Complexity:** O(n) — each index enters and leaves the deque at most once.

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/stack/`](../appendix/templates/stack/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/stack/template.py) from memory before you drill problems.

## Practice

Work the guided set with hints & solutions: [**Stacks & Queues — Practice →**](../rmap-practice/04-stack.md). Easy → hard, top to bottom; when the pattern feels automatic, move on — don’t grind it forever. Want more volume? See the [recommended list](../../lists/recommended.md#4-stack-16-problems).

## Check Yourself

- [ ] I can explain when "most recent unresolved item" signals a stack, and why BFS needs a queue not a stack.
- [ ] I can write the monotonic-stack next-greater-element template from memory.
- [ ] I know to use `collections.deque` (not `list.pop(0)`) for a queue, and why.
- [ ] I solved a 🔴 Hard stack problem (e.g. Largest Rectangle in Histogram).

---

**Up next:** [Recursion & the Call Stack](04b-recursion.md) — the call stack *is* a stack; this is the bridge to trees, backtracking, and DP.

[← Prev](03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](04b-recursion.md)

