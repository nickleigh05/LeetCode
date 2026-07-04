# 00d. Time Complexity

*How to look at code and determine its Big O — four rules cover almost everything.*

[← Prev](00c-big-o-notation.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00e-space-complexity.md)

---

**Time complexity** is the Big O of *steps taken*. Determining it from code is mechanical once you know the rules:

## Rule 1 — Sequential steps *add* (then keep the biggest)

```python
for x in nums:      # O(n)
    total += x
for x in nums:      # O(n)
    print(x)
# O(n) + O(n) = O(2n) → O(n)
```

## Rule 2 — Nested loops *multiply*

```python
for i in range(n):        # n iterations
    for j in range(n):    # n iterations inside each
        check(i, j)
# n × n → O(n²)
```

This is the shape of most brute-force solutions — and the thing this course teaches you to kill.

## Rule 3 — Halving the input each step is O(log n)

```python
while lo <= hi:               # search space: n → n/2 → n/4 → …
    mid = (lo + hi) // 2
    ...                       # keep one half, discard the other
# O(log n) — you can only halve n about log₂(n) times
```

Anything that throws away a constant *fraction* of the problem each round is logarithmic. And a loop that does O(log n) work n times — like sorting's merge levels — is O(n log n).

## Rule 4 — Built-ins hide loops; count them too

```python
if target in my_list:    # O(n) — scans the whole list!
if target in my_set:     # O(1) — hash lookup
nums.sort()              # O(n log n)
```

A single innocent-looking line can carry the whole cost. The most common mistake at this stage: `in` on a **list** is O(n), so putting it inside a loop silently makes O(n²).

## Worked example

```python
def has_duplicate(nums):
    seen = set()
    for x in nums:          # n iterations
        if x in seen:       # O(1) set lookup
            return True
        seen.add(x)         # O(1)
    return False
```

n iterations × O(1) work each = **O(n)** time. (The early `return True` might fire sooner, but Big O assumes the worst case: no duplicate, full scan.)

## Check Yourself

- [ ] I can state the four rules: add sequential, multiply nested, halving = log, count hidden built-in costs.
- [ ] I can explain why `x in some_list` inside a loop is an O(n²) trap.
- [ ] I can walk any short snippet and produce its time complexity — [the practice drills](00f-foundations-practice.md) will prove it.

---

**Up next:** [Space Complexity](00e-space-complexity.md) — the same counting game, applied to memory.

[← Prev](00c-big-o-notation.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00e-space-complexity.md)
