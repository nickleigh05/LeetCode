# 04. Stack — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md)

---

### 20. Valid Parentheses — Easy
[LeetCode](https://leetcode.com/problems/valid-parentheses/)  
[Solution file (no hints)](../../problems/0001-0499/20.py)

Given a string of brackets, determine if they're properly matched and nested. Why does a LIFO structure fit this problem better than counting opens and closes?

<details>
<summary>Hint</summary>

Push opening brackets onto a [stack](../data-structures/stack.md). On a closing bracket, it must match whatever is on top of the stack — nesting means the most recent open is always the next one that needs to close.
</details>

<details>
<summary>Solution</summary>

```python
pairs = {")": "(", "]": "[", "}": "{"}   # closing -> matching opening
stack = []                                # init the stack

for c in s:                                 # for loop over the string
    if c in pairs:                            # closing bracket
        if not stack or stack[-1] != pairs[c]:  # nothing to match, or wrong match
            return False
        stack.pop()
    else:                                      # opening bracket
        stack.append(c)

return not stack                            # valid only if everything got matched
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [list-basics](../syntax/list-basics.md) (list as stack) · [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass through the string.
**Space: O(n)** — worst case (all opening brackets) the stack holds every character.
</details>

---

### 155. Min Stack — Medium
[LeetCode](https://leetcode.com/problems/min-stack/)  
[Solution file (no hints)](../../problems/0001-0499/155.py)

Design a stack that supports push, pop, top, and getMin — all in O(1). Since the minimum can change on every pop, what could you track alongside each element to make "what was the min at this point" a lookup instead of a recompute?

<details>
<summary>Hint</summary>

Keep a second [stack](../data-structures/stack.md) that tracks the running minimum at each depth. Every push also pushes `min(new value, current min)` onto the min-stack, so popping never loses track of the previous minimum.
</details>

<details>
<summary>Solution</summary>

```python
class MinStack:
    def __init__(self):
        self.stack = []                    # regular values
        self.min_stack = []                # running min at each depth

    def push(self, val):
        self.stack.append(val)
        m = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(m)             # min including this new value

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()                 # keep both stacks in sync

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]            # O(1) lookup of current min
```

Building blocks: [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`) · [comparison-operators](../syntax/comparison-operators.md) (`min()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** for every operation (push, pop, top, getMin).
**Space: O(n)** — two parallel stacks, each up to n elements.
</details>

---

### 150. Evaluate Reverse Polish Notation — Medium
[LeetCode](https://leetcode.com/problems/evaluate-reverse-polish-notation/)  
[Solution file (no hints)](../../problems/0001-0499/150.py)

Given tokens in Reverse Polish (postfix) notation, evaluate the expression. Since operators always come *after* their operands in this notation, what structure naturally holds "the operands waiting to be combined"?

<details>
<summary>Hint</summary>

Push numbers onto a [stack](../data-structures/stack.md). When you hit an operator, pop the top two numbers, apply the operator, and push the result back.
</details>

<details>
<summary>Solution</summary>

```python
stack = []
ops = {"+", "-", "*", "/"}

for token in tokens:                     # for loop over the tokens
    if token in ops:                        # operator: pop two operands
        b = stack.pop()
        a = stack.pop()
        if token == "+":
            stack.append(a + b)
        elif token == "-":
            stack.append(a - b)
        elif token == "*":
            stack.append(a * b)
        else:                                 # division truncates toward zero
            stack.append(int(a / b))
    else:                                    # number: push it
        stack.append(int(token))

return stack[-1]
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [elif-else](../syntax/elif-else.md) · [type-conversion](../syntax/type-conversion.md) (`int()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each token is processed once.
**Space: O(n)** — the stack holds up to n operands in the worst case.
</details>

---

### 22. Generate Parentheses — Medium
[LeetCode](https://leetcode.com/problems/generate-parentheses/)  
[Solution file (no hints)](../../problems/0001-0499/22.py)

Given `n` pairs of parentheses, generate all combinations of well-formed parentheses strings. How do you know, at any partial string, whether it's still legal to add an open or a close?

<details>
<summary>Hint</summary>

Build the string with [backtracking](../algorithms/backtracking.md): you can add an open bracket whenever you've used fewer than `n`, and a close bracket whenever fewer closes than opens have been used so far.
</details>

<details>
<summary>Solution</summary>

```python
res = []

def backtrack(open_n, close_n, path):     # path = the string built so far
    if len(path) == 2 * n:                   # base case: full-length string
        res.append("".join(path))
        return
    if open_n < n:                            # choice 1: add an open bracket
        path.append("(")
        backtrack(open_n + 1, close_n, path)
        path.pop()                              # un-choose
    if close_n < open_n:                       # choice 2: add a close bracket
        path.append(")")
        backtrack(open_n, close_n + 1, path)
        path.pop()                              # un-choose

backtrack(0, 0, [])
return res
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`) · [string-join-slice](../syntax/string-join-slice.md) (`"".join()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(4ⁿ / √n)** — the nth Catalan number bounds the number of valid strings generated.
**Space: O(4ⁿ / √n)** — for the output, plus O(n) recursion depth.
</details>

---

### 739. Daily Temperatures — Medium
[LeetCode](https://leetcode.com/problems/daily-temperatures/)  
[Solution file (no hints)](../../problems/0500-0999/739.py)

For each day, find how many days until a warmer temperature. Instead of scanning forward from every day, what could a stack of "still waiting for something warmer" indices save you?

<details>
<summary>Hint</summary>

Keep a monotonically decreasing [stack](../data-structures/stack.md) of indices whose answer isn't known yet. When today's temperature beats the one at the top of the stack, that's the answer for that index — pop and record it.
</details>

<details>
<summary>Solution</summary>

```python
res = [0] * len(temperatures)
stack = []                              # indices with unresolved "warmer day"

for i, t in enumerate(temperatures):      # for loop over each day
    while stack and t > temperatures[stack[-1]]:  # today is warmer than the top
        prev_i = stack.pop()
        res[prev_i] = i - prev_i             # days until it got warmer
    stack.append(i)

return res
```

Building blocks: [list-basics](../syntax/list-basics.md) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each index is pushed and popped from the stack at most once.
**Space: O(n)** — the stack holds up to n indices in the worst case (strictly decreasing temperatures).
</details>

---

### 853. Car Fleet — Medium
[LeetCode](https://leetcode.com/problems/car-fleet/)  
Solution: not yet solved in this repo.

Given car positions, speeds, and a target, count how many "fleets" arrive together (a faster car behind a slower one is stuck behind it). Why does sorting by starting position and scanning from the car closest to the target work?

<details>
<summary>Hint</summary>

Sort cars by position descending, then use a [stack](../data-structures/stack.md) of arrival times. If the current car's arrival time is *less than or equal to* the time of the fleet ahead (top of stack), it catches up and merges — otherwise it starts a new fleet.
</details>

<details>
<summary>Solution</summary>

```python
pairs = sorted(zip(position, speed), reverse=True)   # closest to target first
stack = []                                             # arrival times of fleets

for pos, spd in pairs:                                   # for loop from closest to farthest
    time = (target - pos) / spd                            # time to reach target
    if not stack or time > stack[-1]:                        # slower than the fleet ahead: new fleet
        stack.append(time)
    # else: catches up to the fleet ahead, merges — no push

return len(stack)
```

Building blocks: [sorting-key](../syntax/sorting-key.md) (`sorted(..., reverse=True)`) · [zip-function](../syntax/zip-function.md) · [for-loop](../syntax/for-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by the sort; the scan afterward is O(n).
**Space: O(n)** — for the sorted pairs and the stack.
</details>

---

### 84. Largest Rectangle in Histogram — Hard
[LeetCode](https://leetcode.com/problems/largest-rectangle-in-histogram/)  
Solution: not yet solved in this repo.

Given bar heights, find the largest rectangle that fits under the histogram. For a rectangle anchored at a given bar's height, how far can it extend left and right before hitting a shorter bar — and how does a stack find that boundary in one pass?

<details>
<summary>Hint</summary>

Keep a monotonically increasing [stack](../data-structures/stack.md) of `(start_index, height)`. When a new bar is shorter than the top of the stack, that top bar's rectangle is finished — its width spans from its recorded start index to the current position.
</details>

<details>
<summary>Solution</summary>

```python
stack = []                            # (start_index, height), increasing heights
max_area = 0

for i, h in enumerate(heights):         # for loop over each bar
    start = i
    while stack and stack[-1][1] > h:     # current bar is shorter: close out taller bars
        idx, height = stack.pop()
        max_area = max(max_area, height * (i - idx))
        start = idx                          # this rectangle could have started earlier
    stack.append((start, h))

for idx, h in stack:                    # close out whatever remains on the stack
    max_area = max(max_area, h * (len(heights) - idx))

return max_area
```

Building blocks: [tuple-basics](../syntax/tuple-basics.md) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each bar is pushed and popped from the stack at most once.
**Space: O(n)** — the stack holds up to n bars in the worst case (strictly increasing heights).
</details>
