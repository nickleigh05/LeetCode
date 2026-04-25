# Stack

## 4. Stack (7 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 20 | Easy | Valid Parentheses | [Link](https://leetcode.com/problems/valid-parentheses/) |
| 155 | Medium | Min Stack | [Link](https://leetcode.com/problems/min-stack/) |
| 150 | Medium | Evaluate Reverse Polish Notation | [Link](https://leetcode.com/problems/evaluate-reverse-polish-notation/) |
| 22 | Medium | Generate Parentheses | [Link](https://leetcode.com/problems/generate-parentheses/) |
| 739 | Medium | Daily Temperatures | [Link](https://leetcode.com/problems/daily-temperatures/) |
| 853 | Medium | Car Fleet | [Link](https://leetcode.com/problems/car-fleet/) |
| 84 | Hard | Largest Rectangle in Histogram | [Link](https://leetcode.com/problems/largest-rectangle-in-histogram/) |

---

## Data Structures

### Stack
A Last-In-First-Out (LIFO) structure. You can only push to the top or pop from the top. In Python, a regular list works as a stack (`append` = push, `pop` = pop). O(1) for both operations. The key insight: a stack lets you "remember" the most recent unresolved thing while you process what comes after it.

---

## Core Patterns

### Matching Brackets
Push opening brackets onto the stack. When you see a closing bracket, check if the top of the stack is the matching opener — if not, it's invalid. At the end the stack must be empty. Used in Valid Parentheses.

### Monotonic Stack (Next Greater / Next Smaller)
Maintain a stack that is always in increasing or decreasing order. When a new element breaks the order, pop elements off the stack — each popped element has found its "next greater" or "next smaller" neighbor. O(n) total because each element is pushed and popped at most once. Used in Daily Temperatures, Largest Rectangle in Histogram, Car Fleet.

### Stack for Expression Evaluation
Push numbers onto the stack. When you see an operator, pop the top two numbers, apply the operator, and push the result back. Used in Evaluate Reverse Polish Notation.

### Auxiliary Min Stack
Use two stacks: one for the actual values and one to track the current minimum. The min stack stores the minimum at each state — when you pop from the main stack, also pop from the min stack. Used in Min Stack.

### Backtracking with Stack
Build a solution incrementally by pushing choices onto a stack (or using recursion which implicitly uses the call stack). When a constraint is violated, backtrack by popping. Used in Generate Parentheses — track `open` and `close` counts and only add a bracket when valid.

### Histogram Rectangle Area
For each bar, find how far left and right it can extend at its height (i.e. how far the rectangle can stretch before hitting a shorter bar). A monotonic stack of increasing heights tracks the left boundary. When a shorter bar is found, pop and compute areas. Used in Largest Rectangle in Histogram.
