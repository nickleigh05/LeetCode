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
class Solution:
    def isValid(self, s: str) -> bool:

        stack = []
        pairs = {")": "(", "]": "[", "}": "{"}

        for char in s:
            if char in pairs:
                if stack and stack[-1] == pairs[char]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(char)

        return not stack
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
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
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
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        stack = []
        operators = {"+", "-", "*", "/"}

        for token in tokens:
            if token in operators:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                else:
                    result = int(left / right)

                stack.append(result)
            else:
                stack.append(int(token))

        return stack.pop()
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
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        result = []

        def backtrack(current, open_count, close_count):
            if len(current) == 2 * n:
                result.append(current)
                return

            if open_count < n:
                backtrack(current + "(", open_count + 1, close_count)

            if close_count < open_count:
                backtrack(current + ")", open_count, close_count + 1)

        backtrack("", 0, 0)
        return result
```

Building blocks: [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md) (inner `def` capturing `n` and `result`) · [list-methods](../syntax/list-methods.md) (`.append()`) · [string-basics](../syntax/string-basics.md) (`+` concatenation)
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
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        answer = [0] * len(temperatures)
        stack = []

        for i in range(len(temperatures)):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index
            stack.append(i)

        return answer
```

Building blocks: [list-basics](../syntax/list-basics.md) · [range-function](../syntax/range-function.md) · [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`, `.pop()`)
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
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:

        pairs = sorted(zip(position, speed), reverse=True)
        stack = []

        for pos, spd in pairs:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:
                stack.append(time)

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
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:

        stack = []
        max_area = 0

        for i, height in enumerate(heights):
            start = i
            while stack and stack[-1][1] > height:
                index, prev_height = stack.pop()
                max_area = max(max_area, prev_height * (i - index))
                start = index
            stack.append((start, height))

        for index, height in stack:
            max_area = max(max_area, height * (len(heights) - index))

        return max_area
```

Building blocks: [tuple-basics](../syntax/tuple-basics.md) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each bar is pushed and popped from the stack at most once.
**Space: O(n)** — the stack holds up to n bars in the worst case (strictly increasing heights).
</details>
