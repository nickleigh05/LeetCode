# 04b. Recursion & the Call Stack

*A function that calls itself — and the stack that makes it possible.*

[← Prev](04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](05-binary-search.md)

---

> **Builds on:** stacks from [Lesson 04](04-stack.md). The call stack *is* a stack — every function call pushes a frame, every return pops one.

Three of the most important phases in this roadmap — Trees (07), Backtracking (10), and Dynamic Programming (14) — are all recursion wearing different clothes. Understanding recursion as its own topic here will make all three of those click faster. Don't skip this lesson.

## Concept

### What makes a function recursive

A **recursive function** calls itself on a smaller version of the problem. Every correct recursive function has exactly two parts:

1. **Base case** — the version of the problem so small you can answer it directly (no more calls). Without this, the function calls itself forever and crashes.
2. **Recursive case** — the general case: solve a smaller sub-problem by calling yourself, then use that result to build the current answer.

```python
def factorial(n):
    if n <= 1:       # 1. base case — factorial(0)=1, factorial(1)=1
        return 1
    return n * factorial(n - 1)   # 2. recursive case
```

Reading it top-down: "if n ≤ 1 I know the answer; otherwise I need factorial(n-1) first and I'll multiply by n when it comes back."

### The call stack

Every function call creates a **stack frame**: a small packet of memory holding local variables and the return address. Frames stack up as calls go deeper; when a function returns its frame is popped.

```
factorial(4)  ← lives on the stack while waiting for factorial(3)
  factorial(3)  ← lives while waiting for factorial(2)
    factorial(2)  ← lives while waiting for factorial(1)
      factorial(1)  ← base case: returns 1 immediately
    ← factorial(2) gets 1 back, computes 2*1=2, returns 2, frame popped
  ← factorial(3) gets 2 back, computes 3*2=6, returns 6, frame popped
← factorial(4) gets 6 back, computes 4*6=24, returns 24, frame popped

Answer: 24
```

The key insight: **each frame is frozen in place until the call it's waiting for returns.** This is the stack from Lesson 04 — pushed on the way down, popped on the way up.

### Space: call stack depth = O(depth)

At peak depth, all frames from the first call to the base case exist simultaneously. If you make `n` nested calls before hitting a base case, you consume **O(n) extra space** — even if each frame is tiny. Python's default limit is ~1000 frames (configurable but small); deep recursion on large inputs requires iteration instead.

```
factorial(n) → depth n → O(n) space on the call stack
binary_search (recursive) → depth log n → O(log n) space
```

### The recursion tree

For functions that make **more than one** recursive call, draw the **recursion tree** to count total work.

```python
def fib(n):                 # each call spawns 2 more
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

```
                 fib(4)
               /        \
          fib(3)        fib(2)
         /     \        /    \
      fib(2) fib(1) fib(1) fib(0)
      /   \
  fib(1) fib(0)
```

- **Depth:** n levels
- **Nodes at each level:** doubles each step → 2⁰ + 2¹ + 2² + … + 2ⁿ⁻¹ ≈ **2ⁿ total calls**
- **Time:** O(2ⁿ) — exponential, catastrophically slow for large n
- **Space:** O(n) — only one path from root to a leaf is alive at once

The fix is to never recompute sub-problems: memoize or use DP. That's [Lesson 14](14-dp-1d.md).

### Patterns — every recursion follows one of these shapes

```
Shape 1: Linear (one recursive call, shrinks by 1 or ½)
  factorial, sum-of-list, reverse-a-list → O(n) or O(log n)

Shape 2: Branching (two or more recursive calls)
  fib, tree traversal, backtracking → O(2ⁿ) without memoization
  merge sort (halves + merges) → O(n log n)

Shape 3: Divide-and-conquer (branching but sub-problems don't overlap)
  merge sort, binary-search → efficient; recursion tree has ~log n levels
```

## Worked Traces

Trace these **by hand** — cover the answer and work through each step.

### Reverse a list recursively

```python
def reverse(lst):
    if len(lst) <= 1:       # base case: empty or single element
        return lst
    return reverse(lst[1:]) + [lst[0]]   # reverse tail, append head at end
```

Trace `reverse([1, 2, 3])`:
```
reverse([1,2,3])
  → reverse([2,3]) + [1]
       → reverse([3]) + [2]
            → [3]           ← base case
       ← [3] + [2] = [3,2]
  ← [3,2] + [1] = [3,2,1]
```

Time: O(n²) — creating a new list at each level. A two-pointer in-place approach is O(n).

### Sum a list recursively

```python
def sum_list(nums):
    if not nums:          # base case: empty list sums to 0
        return 0
    return nums[0] + sum_list(nums[1:])
```

Trace `sum_list([3,1,4])`:
```
sum_list([3,1,4])
  → 3 + sum_list([1,4])
         → 1 + sum_list([4])
                → 4 + sum_list([])
                       → 0    ← base case
                ← 4+0 = 4
         ← 1+4 = 5
  ← 3+5 = 8
```

### Exercises

<details>
<summary><strong>Exercise 1 — write a recursive function</strong></summary>

Write `power(base, exp)` that computes `base ** exp` recursively (exp ≥ 0).

```python
def power(base, exp):
    if exp == 0:                     # base case: anything to the power 0 is 1
        return 1
    return base * power(base, exp - 1)   # recursive case
```

Time: O(exp), Space: O(exp) call stack depth.
</details>

<details>
<summary><strong>Exercise 2 — trace by hand</strong></summary>

What does `mystery(3)` return?

```python
def mystery(n):
    if n == 0:
        return 0
    return n + mystery(n - 1)
```

**Trace:**
```
mystery(3)
  → 3 + mystery(2)
         → 2 + mystery(1)
                → 1 + mystery(0)
                       → 0
                ← 1
         ← 3
  ← 6
```

Returns **6** — it's 0+1+2+3, i.e., the sum 0..n. Same as `n*(n+1)//2`.
</details>

<details>
<summary><strong>Exercise 3 — identify the Big-O</strong></summary>

```python
def count_down(n):
    if n <= 0:
        return
    print(n)
    count_down(n - 1)
    count_down(n - 1)    # two recursive calls!
```

**Answer:** O(2ⁿ) time. At depth k there are 2ᵏ calls; total = 2⁰+2¹+…+2ⁿ ≈ 2ⁿ⁺¹. O(n) space (call stack depth = n).
</details>

## The Recursion Template

Every recursive function looks like one of these two skeletons:

```python
# Linear recursion (one call, shrinks problem)
def solve(problem):
    if is_base_case(problem):
        return base_answer
    smaller = shrink(problem)           # remove one element, halve, etc.
    sub_answer = solve(smaller)
    return combine(problem, sub_answer)

# Branching recursion (multiple calls — for trees, search, DP)
def solve(node_or_state):
    if is_base_case(node_or_state):
        return base_answer
    results = [solve(child) for child in children(node_or_state)]
    return combine(node_or_state, results)
```

You'll see the branching form in Trees (07), Backtracking (10), and DP (14). They're all variations on that exact skeleton.

The full code template for the advanced application of recursion (backtracking) lives in [`appendix/templates/backtracking/`](../appendix/templates/backtracking/) — study it *after* you finish this lesson and Lesson 07.

## Practice

There's no dedicated recursion section in the curated list (it's woven into trees, DP, and backtracking). Instead, solidify the skill here:

1. **Implement from scratch:** `factorial`, `fibonacci` (naïve), `sum_of_list`, `power(base, n)`, `count_digits(n)`.
2. **Trace by hand** before running: predict the output, then verify.
3. **Add memoization** to your naïve Fibonacci and measure the speed difference.

When recursion is automatic — when you can write the base case and recursive case without thinking — move on.

## Check Yourself

- [ ] I can write a recursive function from scratch for any simple problem (factorial, sum, reverse).
- [ ] I can draw the call stack for a recursive call and see exactly when each frame is created and destroyed.
- [ ] I can draw the recursion tree for a branching function and derive its Big-O from the tree shape.
- [ ] I know why naïve Fibonacci is O(2ⁿ) and how memoization fixes it.
- [ ] I know that call stack depth = extra space, and I can state the space cost of my recursive functions.

---

**Up next:** [Binary Search & Sorting](05-binary-search.md) — halve any ordered search space, including the answer itself.

[← Prev](04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](05-binary-search.md)
