# Stack

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that exercise monotonic stacks, auxiliary tracking stacks, and RPN evaluation. NeetCode 250 introduces design problems (stack-based queue, frequency stack) and nested decoding patterns. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, determine whether it needs a monotonic stack, a tracking stack, or a simulation stack, then find the matching pattern.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 20 | Easy | Valid Parentheses | [Link](https://leetcode.com/problems/valid-parentheses/) | ☑ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 155 | Medium | Min Stack | [Link](https://leetcode.com/problems/min-stack/) | ☑ |
| 150 | Medium | Evaluate Reverse Polish Notation | [Link](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | ☐ |
| 22 | Medium | Generate Parentheses | [Link](https://leetcode.com/problems/generate-parentheses/) | ☐ |
| 739 | Medium | Daily Temperatures | [Link](https://leetcode.com/problems/daily-temperatures/) | ☐ |
| 853 | Medium | Car Fleet | [Link](https://leetcode.com/problems/car-fleet/) | ☐ |
| 84 | Hard | Largest Rectangle in Histogram | [Link](https://leetcode.com/problems/largest-rectangle-in-histogram/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 682 | Easy | Baseball Game | [Link](https://leetcode.com/problems/baseball-game/) | ☐ | Simulation stack |
| 225 | Easy | Implement Stack using Queues | [Link](https://leetcode.com/problems/implement-stack-using-queues/) | ☐ | Queue-based stack |
| 232 | Easy | Implement Queue using Stacks | [Link](https://leetcode.com/problems/implement-queue-using-stacks/) | ☐ | Stack-based queue |
| 735 | Medium | Asteroid Collision | [Link](https://leetcode.com/problems/asteroid-collision/) | ☐ | Collision simulation |
| 901 | Medium | Online Stock Span | [Link](https://leetcode.com/problems/online-stock-span/) | ☐ | Monotonic stack |
| 71 | Medium | Simplify Path | [Link](https://leetcode.com/problems/simplify-path/) | ☐ | String processing stack |
| 394 | Medium | Decode String | [Link](https://leetcode.com/problems/decode-string/) | ☐ | Nested decoding stack |
| 895 | Hard | Maximum Frequency Stack | [Link](https://leetcode.com/problems/maximum-frequency-stack/) | ☐ | Design + frequency map |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Push (list.append) | O(1) amortized | — | Dynamic array resize is rare |
| Pop (list.pop()) | O(1) | — | Always from the end |
| Peek (list[-1]) | O(1) | — | No removal |
| Monotonic stack (full array) | O(n) | O(n) | Each element pushed and popped at most once |
| Auxiliary min/max stack | O(1) push/pop | O(n) | Parallel stack, always same size as main |
| RPN evaluation | O(n) | O(n) | One pass, stack holds at most n/2 operands |
| Generate Parentheses (backtrack) | O(4^n / √n) | O(n) | Catalan number of valid strings |
| Largest Rectangle in Histogram | O(n) | O(n) | Monotonic stack, one pass |

---

## Data Structures

### Stack (Python list)

A stack is a LIFO (last in, first out) structure. In Python, use a plain `list` — `append()` pushes to the top in O(1), `pop()` removes the top in O(1), and `[-1]` peeks without removing. There is no separate stack class; the list's end is the top.

```
Push 3, Push 7, Push 1:

Top →  [ 1 ]  ← pop() removes this
       [ 7 ]
       [ 3 ]
Bottom

list representation: [3, 7, 1]
                              ↑ top (index -1)
```

**When it matters:** Any time you need to process elements in reverse order of arrival, check the most recent thing, or undo the last action. Parenthesis matching, RPN evaluation, backtracking state.

### Monotonic Stack

A stack that enforces an ordering invariant — either strictly increasing or strictly decreasing from bottom to top. When a new element would violate the invariant, you pop (and process) everything that does violate it before pushing the new element. This means each element is pushed exactly once and popped at most once, giving O(n) for a full pass.

```
Decreasing monotonic stack — building while processing [2, 1, 5, 6, 2, 3]:

Process 2: stack = [2]
Process 1: 1 < 2, just push. stack = [2, 1]
Process 5: 5 > 1 → pop 1, 5 > 2 → pop 2, push 5. stack = [5]
Process 6: 6 > 5 → pop 5, push 6. stack = [6]
Process 2: 2 < 6, push. stack = [6, 2]
Process 3: 3 > 2 → pop 2, 3 < 6, push 3. stack = [6, 3]
```

**When it matters:** "Next greater element", Daily Temperatures (#739), Largest Rectangle in Histogram (#84), Car Fleet (#853), Online Stock Span (#901). Whenever you need to efficiently find the next element that is larger or smaller.

### Auxiliary (Min/Max) Stack

Two stacks in lockstep. The main stack holds actual values. The auxiliary stack holds the running minimum (or maximum) at each depth level — when you push onto the main stack, also push `min(new_val, aux[-1])` onto the auxiliary. When you pop from the main stack, pop from the auxiliary too. The current minimum is always `aux[-1]` in O(1).

```
Push 5, Push 3, Push 7, Push 2:

Main:  [5, 3, 7, 2]
Aux:   [5, 3, 3, 2]   ← running min at each level
        ↑              ↑
       min was 5      min is now 2
```

**When it matters:** Min Stack (#155), any design problem requiring O(1) min/max with push/pop.

---

## Core Patterns

### Matching Pairs
**When to use:** Validate or process nested structure — parentheses, brackets, tags. Push open symbols; on a close symbol, check that the top matches.
**Complexity:** O(n) time, O(n) space
**Problems:** Valid Parentheses (#20), Generate Parentheses (#22)
**Common mistake:** Not checking `if stack` before popping — popping an empty stack raises IndexError.

```python
stack = []
pairs = {')': '(', ']': '[', '}': '{'}
for c in s:
    if c in '([{':
        stack.append(c)
    elif c in ')]}':
        if not stack or stack[-1] != pairs[c]:
            return False
        stack.pop()
return not stack   # must be empty — unmatched opens would remain
```

### Monotonic Stack (Decreasing)
**When to use:** For each element, find the next element that is greater (or smaller). Maintain a stack of "candidates" waiting for their answer. When a new element beats the top of the stack, that element is the answer for the top.
**Complexity:** O(n) time, O(n) space
**Problems:** Daily Temperatures (#739), Largest Rectangle in Histogram (#84), Car Fleet (#853), Online Stock Span (#901), Asteroid Collision (#735)
**Common mistake:** Storing values instead of indices — you usually need the index to compute distances or widths.

```python
stack = []   # stores indices
res = [0] * len(temps)
for i, t in enumerate(temps):
    while stack and temps[stack[-1]] < t:  # current temp beats the top
        j = stack.pop()
        res[j] = i - j                     # days until warmer
    stack.append(i)
```

### Auxiliary Stack (Min/Max Tracking)
**When to use:** You need O(1) access to the running minimum or maximum at any stack depth, across arbitrary push/pop sequences.
**Complexity:** O(1) push, pop, and getMin; O(n) space
**Problems:** Min Stack (#155)
**Common mistake:** Only pushing to the aux stack when the new value is smaller — you must push on every push, not just on new minimums, so that pop stays in sync.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()   # always pop both together

    def getMin(self):
        return self.min_stack[-1]
```

### Backtracking State Stack
**When to use:** Nested or recursive structure where you need to resume from a saved state — decode a string with nested brackets, generate parentheses iteratively.
**Complexity:** Varies — O(n) for Decode String, O(4^n/√n) for Generate Parentheses
**Problems:** Decode String (#394), Generate Parentheses (#22)
**Common mistake:** Forgetting to save the current accumulated string before opening a new nested level — you need `(current_string, repeat_count)` not just the count.

```python
stack = []
cur_str = ""
cur_num = 0
for c in s:
    if c.isdigit():
        cur_num = cur_num * 10 + int(c)   # handles multi-digit numbers
    elif c == '[':
        stack.append((cur_str, cur_num))  # save state before going deeper
        cur_str, cur_num = "", 0
    elif c == ']':
        prev_str, num = stack.pop()
        cur_str = prev_str + cur_str * num
    else:
        cur_str += c
```

---

## Syntax Reference

### Stack basics

```python
stack = []
stack.append(x)   # push — O(1)
stack.pop()       # pop top, returns value — O(1); raises IndexError if empty
stack[-1]         # peek top without removing — O(1)
if stack:         # check non-empty before peeking or popping
if not stack:     # check empty
len(stack)        # number of elements
```

### Safe pop pattern

```python
# Always guard before popping in matching problems:
if stack and stack[-1] == expected:
    stack.pop()
else:
    return False
```

### RPN evaluation skeleton

```python
stack = []
ops = {'+', '-', '*', '/'}
for token in tokens:
    if token not in ops:
        stack.append(int(token))
    else:
        b, a = stack.pop(), stack.pop()   # order matters: a op b
        if token == '+': stack.append(a + b)
        elif token == '-': stack.append(a - b)
        elif token == '*': stack.append(a * b)
        elif token == '/': stack.append(int(a / b))  # truncate toward zero
return stack[0]
```

### deque (when you need O(1) popleft)

```python
from collections import deque

dq = deque()
dq.append(x)      # push right — O(1)
dq.appendleft(x)  # push left — O(1)
dq.pop()          # pop right — O(1)
dq.popleft()      # pop left — O(1)
# Use deque for queue simulation (Implement Queue using Stacks #232)
# For pure stack problems, list is fine — dq gives no benefit over list.append/pop()
```

### Histogram rectangle area (monotonic stack pattern)

```python
# Largest Rectangle in Histogram (#84):
# Stack stores (index, height) of bars still "open" (not yet bounded on the right)
stack = []  # (start_index, height)
max_area = 0
for i, h in enumerate(heights):
    start = i
    while stack and stack[-1][1] > h:
        idx, height = stack.pop()
        max_area = max(max_area, height * (i - idx))
        start = idx               # this bar extends back to where the popped bar started
    stack.append((start, h))
for idx, height in stack:         # bars still open — extend to end
    max_area = max(max_area, height * (len(heights) - idx))
```
