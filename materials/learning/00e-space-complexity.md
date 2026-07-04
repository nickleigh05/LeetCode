# 00e. Space Complexity

*Counting extra memory the same way — and the memory-for-speed trade at the heart of this course.*

[← Prev](00d-time-complexity.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00f-foundations-practice.md)

---

**Space complexity** is the Big O of *extra memory* your algorithm allocates. Same notation, same growth-as-n-grows question — just counting bytes instead of steps.

## Rule 1 — Count only what *you* allocate

The input doesn't count against you; it was already there. Count the structures your code creates:

```python
def has_duplicate(nums):
    seen = set()             # grows up to n items → O(n) space
    for x in nums:
        if x in seen: return True
        seen.add(x)
    return False
```

```python
def max_of(nums):
    best = nums[0]           # one variable, no matter how big nums is
    for x in nums:
        best = max(best, x)
    return best              # O(1) space
```

A fixed handful of variables is **O(1)**; a structure that scales with the input is **O(n)** (a copy of a 2-D grid would be O(n·m), and so on).

## Rule 2 — Recursion uses memory too

Every unfinished recursive call sits on the **call stack**, and that's real memory. The space cost is the *maximum depth* of the recursion:

```python
def countdown(n):
    if n == 0: return
    countdown(n - 1)     # n frames deep before anything returns → O(n) space
```

No visible list anywhere, but this uses O(n) memory. You'll see why in [Recursion (04b)](04b-recursion.md).

## The trade that powers everything

Time and space are currencies you exchange. The classic move — the one [Lesson 01](01-arrays-hashing.md) is built on — is spending **O(n) space** (a hash map that remembers what you've seen) to cut time from **O(n²) to O(n)**. Interviewers will ask for both costs, and "can you trade one for the other?" is often the follow-up.

## Check Yourself

- [ ] I know what counts toward space complexity (extra allocations, not the input).
- [ ] I can spot O(1) vs O(n) space in a short function at a glance.
- [ ] I know recursion depth costs memory even with no visible data structure.

---

**Up next:** [Foundations Practice](00f-foundations-practice.md) — drills that turn all of Phase 0 into reflex before the first real lesson.

[← Prev](00d-time-complexity.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00f-foundations-practice.md)
