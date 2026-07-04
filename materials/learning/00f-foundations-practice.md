# 00f. Big-O Practice — Drills & Tracing

*Reading about Big-O is not the same as computing it. This lesson makes you do it.*

[← Prev](00e-space-complexity.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](01-arrays-hashing.md)

---

Lessons 00c–00e explained what Big-O means. This one makes you compute it — on loops, on recursion, on Python's built-ins — until estimating complexity becomes a reflex.

> **How much to do now:** Work the **Analyzing Loops** and **built-in costs** drills before Phase 1 — that's the part you need immediately. The **recursion** and **amortized analysis** sections are here for completeness; if they feel abstract before you've written recursive code, skim them now and come back after [Recursion (04b)](04b-recursion.md). Don't let this page become a wall that blocks you from starting Lesson 01.

## Analyzing Loops

**The rule:** every nested loop multiplies. Find the number of iterations at each level.

```python
# --- Example 1 ---
for i in range(n):       # n iterations
    print(i)
# O(n) — single loop, one operation per step
```

```python
# --- Example 2 ---
for i in range(n):       # n iterations
    for j in range(n):   # n iterations inside each
        print(i, j)
# O(n²) — two nested loops
```

```python
# --- Example 3 ---
for i in range(n):       # n iterations
    for j in range(i):   # 0 + 1 + 2 + … + (n-1) = n(n-1)/2 iterations total
        print(i, j)
# O(n²) — triangular sum, same asymptotic class
```

```python
# --- Example 4 ---
i = n
while i > 1:
    i //= 2   # halves each time: n, n/2, n/4, … → log₂(n) steps
# O(log n)
```

```python
# --- Example 5 ---
for i in range(n):       # n iterations
    j = n
    while j > 1:
        j //= 2          # log n steps inside each
# O(n log n) — outer O(n), inner O(log n), multiply
```

### Exercises

Work these out *before* revealing the answer.

<details>
<summary><strong>Exercise 1 — what is the Big-O?</strong></summary>

```python
for i in range(n):
    for j in range(10):
        print(i, j)
```

**Answer: O(n).** The inner loop runs a *constant* 10 times regardless of `n`. Constants vanish in Big-O.
</details>

<details>
<summary><strong>Exercise 2 — what is the Big-O?</strong></summary>

```python
for i in range(n):
    for j in range(m):
        print(i, j)
```

**Answer: O(n · m).** Two independent sizes — don't collapse them to n² unless you know n ≈ m.
</details>

<details>
<summary><strong>Exercise 3 — what is the Big-O?</strong></summary>

```python
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**Answer: O(n) time, O(n) space.** One pass through `nums`; the set grows at most to size n.
</details>

<details>
<summary><strong>Exercise 4 — what is the Big-O?</strong></summary>

```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Answer: O(n²) time, O(1) space.** Every pair is tried; no extra data structure grows with n.
</details>

<details>
<summary><strong>Exercise 5 — what is the Big-O?</strong></summary>

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Answer: O(log n) time, O(1) space.** Each iteration halves the search range.
</details>

<details>
<summary><strong>Exercise 6 — what is the Big-O?</strong></summary>

```python
def prefix_sums(nums):
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i+1] = prefix[i] + x
    return prefix
```

**Answer: O(n) time, O(n) space.** One pass to build; the array grows with n.
</details>

## Space Complexity

Time isn't the only cost. **Space complexity** measures how much *extra* memory your algorithm uses — separate from the input itself.

| Pattern | Extra space | Why |
|---------|-------------|-----|
| Constant variables | O(1) | A handful of pointers/counters |
| Output array of size n | O(n) | Grows with input |
| Hash map storing all elements | O(n) | Worst case every element unique |
| 2D DP table for n×m problem | O(n·m) | Grid of subproblem answers |
| Recursive call stack depth d | O(d) | Each frame lives until it returns |

<details>
<summary><strong>Exercise 7 — time AND space Big-O</strong></summary>

```python
def reverse_list(nums):
    result = []
    for x in reversed(nums):
        result.append(x)
    return result
```

**Answer: O(n) time, O(n) space.** One pass, plus a new list of the same size.
</details>

<details>
<summary><strong>Exercise 8 — time AND space Big-O</strong></summary>

```python
def reverse_in_place(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1
```

**Answer: O(n) time, O(1) space.** Same number of swaps, but only two pointer variables — no extra array.
</details>

## Amortized Analysis — "O(1) on average"

Python's `list.append()` is described as O(1) **amortized** — but occasionally it triggers a resize. How can it be O(1)?

```
Start with capacity 4:
[_, _, _, _]          ← append x1: O(1), fills slot 1
[x1, _, _, _]         ← append x2: O(1)
[x1, x2, _, _]        ← append x3: O(1)
[x1, x2, x3, _]       ← append x4: O(1)
[x1, x2, x3, x4]      ← append x5: capacity full!
                             copy 4 elements to new array of capacity 8 → O(4)
[x1,..,x4, x5, _, _, _, _]  ← then append x5 in O(1)
```

The key is that the next resize only happens after *another* 4 appends. If you spread the O(4) copy cost over the 4 cheap appends that paid for it, each append costs O(4/4) = O(1) *on average* — that's amortized O(1). Formal proof: over n appends, total work is O(n) (roughly 2n operations — n appends + n copy steps), so cost per append = O(n)/n = O(1).

**Bottom line:** when you see "O(1) amortized" it means "occasionally expensive but cheap on average over many operations."

<details>
<summary><strong>Exercise 9 — amortized reasoning</strong></summary>

A stack uses a Python list internally. `push()` calls `list.append()`; `pop()` calls `list.pop()`. What are the amortized time complexities?

**Answer:** Both are **O(1) amortized**. `append` and `pop` from the *end* of a list are amortized O(1) in Python (same resizing argument). This is why stacks and queues (when implemented as `collections.deque`) are efficient.
</details>

## Recursive Complexity

When a function calls itself, count how many times it runs and how deep the call stack gets.

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

```
factorial(4)
  └─ factorial(3)
       └─ factorial(2)
            └─ factorial(1)   ← base case, returns 1
```

- **Time:** n recursive calls, each O(1) work → **O(n)**
- **Space:** n frames on the call stack simultaneously → **O(n)**

```python
def fib(n):          # naïve recursive Fibonacci
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

```
fib(4)
├─ fib(3)
│    ├─ fib(2)
│    │    ├─ fib(1)  ✓
│    │    └─ fib(0)  ✓
│    └─ fib(1)       ✓
└─ fib(2)
     ├─ fib(1)       ✓    ← computed AGAIN
     └─ fib(0)       ✓    ← computed AGAIN
```

- **Time:** each call spawns 2 sub-calls, depth n → ~2ⁿ nodes in the tree → **O(2ⁿ)** — exponential and terrible.
- **Space:** maximum depth of call stack is n → **O(n)** (only one branch live at a time).
- **Fix:** memoize or use DP — [Lesson 14](14-dp-1d.md) is the cure.

<details>
<summary><strong>Exercise 10 — recursive Big-O</strong></summary>

```python
def sum_list(nums, i=0):
    if i == len(nums):
        return 0
    return nums[i] + sum_list(nums, i + 1)
```

**Answer: O(n) time, O(n) space.** One call per element; n frames on the stack simultaneously.
</details>

<details>
<summary><strong>Exercise 11 — recursive Big-O</strong></summary>

```python
def merge_sort_count(n):      # how many calls does merge sort make?
    if n <= 1:
        return
    merge_sort_count(n // 2)
    merge_sort_count(n // 2)
```

**Answer:** This spawns 2 sub-calls each time, but the sub-problem is *half* the size. The recursion tree has log₂(n) levels and at each level there are at most n total elements to process (merge step). Total: **O(n log n) time, O(log n) space** (call stack depth = tree height).
</details>

## Trace Exercise — Follow the Code

Trace this function by hand for `nums = [3, 1, 4, 1, 5]`. What does it return?

```python
def mystery(nums):
    best = nums[0]
    for x in nums[1:]:
        best = max(best, x)
    return best
```

<details>
<summary><strong>Answer</strong></summary>

```
best = 3
x=1: best = max(3,1) = 3
x=4: best = max(3,4) = 4
x=1: best = max(4,1) = 4
x=5: best = max(4,5) = 5
returns 5
```

It finds the maximum element. O(n) time, O(1) space.
</details>

## Check Yourself

- [ ] I can compute the Big-O of any single loop, nested loop, or while-halving loop without looking.
- [ ] I can state *both* time and space complexity, and I remember to count the call stack.
- [ ] I understand why `list.append` is O(1) amortized — I can explain the doubling argument.
- [ ] I can draw the recursion tree for a simple function and count its nodes.

---

**Up next:** [Arrays & Hashing](01-arrays-hashing.md) — the foundation. Hash maps trade memory for O(1) lookups and quietly power half of all interview solutions.

[← Prev](00e-space-complexity.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](01-arrays-hashing.md)
