# 16. Greedy
*Take the locally best choice; the proof is the hard part.*

[← Prev](15-dp-2d.md) · [🗺 Roadmap](../roadmap.md) · [Next →](17-intervals.md)

---

> **Builds on:** sorting from [Lesson 05](05-binary-search.md) and intervals intuition — greedy almost always sorts first.

A **greedy** algorithm commits to the best-looking choice at each step and never reconsiders. When it works it's beautifully simple and fast; the real challenge is *justifying* that local optimum leads to a global one. We cover the classic greedy proofs-by-exchange and the problems where greed actually wins.

## Algorithm Deep-Dive

### Greedy

```
  Merge Intervals — Greedy approach:
  Input: [[1,3],[2,6],[8,10],[15,18]]
  Sort by start: [1,3],[2,6],[8,10],[15,18]

  current = [1,3]
  [2,6]:  2 ≤ 3 → overlap → merge → [1,6]
  [8,10]: 8 > 6 → no overlap → save [1,6], current=[8,10]
  [15,18]:15 > 10 → no overlap → save [8,10], current=[15,18]
  Save [15,18]
  Result: [[1,6],[8,10],[15,18]]

  Why greedy works here: sorting by start guarantees we only
  need to check the last merged interval — no need to look back.

  Jump Game — Greedy:
  nums = [2, 3, 1, 1, 4]
  max_reach = 0
  i=0: max_reach = max(0, 0+2) = 2
  i=1: max_reach = max(2, 1+3) = 4
  i=2: max_reach = max(4, 2+1) = 4
  i=3: max_reach = max(4, 3+1) = 4  ← i never exceeds max_reach
  i=4: reached end → True
```

**What it does:** Makes the locally optimal choice at each step with the hope that it leads to a globally optimal solution. Works only when the **greedy choice property** holds — you must prove (or recognize) that local optimality → global optimality.

**Recognition signals:**
- Interval scheduling / merging
- Minimum number of something (jumps, coins — but check if DP not needed)
- "Always pick the smallest/largest/earliest"
- Activity selection problems
- Huffman encoding, Kruskal's MST

**Python:**
```python
# Merge Intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Jump Game (can we reach end?)
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False    # can't reach this position
        max_reach = max(max_reach, i + jump)
    return True

# Activity selection (maximize non-overlapping intervals)
def max_activities(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by END time
    count, last_end = 0, float('-inf')
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

**Complexity:** Usually O(n log n) due to sorting, then O(n) for the greedy pass.

**Data structures it uses:**
Array · Heap and Priority Queue (for some greedy problems)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/greedy/`](../appendix/templates/greedy/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/greedy/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Greedy problems →**](../../lists/recommended.md#15-greedy-14-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Intervals](17-intervals.md) — sort first, then one linear pass to merge, count, or sweep.

[← Prev](15-dp-2d.md) · [🗺 Roadmap](../roadmap.md) · [Next →](17-intervals.md)

