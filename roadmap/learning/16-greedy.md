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

## Proof Frameworks — Why Does Greedy Work?

An interviewer asking "why does greedy work here?" is asking for one of two arguments. Learn the template; the specific problem just fills in the blanks.

### Framework 1 — Exchange Argument

*Show that any solution can be converted to the greedy solution without getting worse.*

**Worked example: Activity Selection (maximize non-overlapping meetings)**

Greedy choice: always pick the activity with the **earliest finish time**.

**Claim:** the greedy solution is optimal.

**Proof:**
1. Let `G` be the greedy solution (activities sorted by finish time, greedily selected).
2. Let `O` be any optimal solution, ordered by finish time.
3. Suppose `G` and `O` first differ at activity `k`: greedy picked `g_k` (earliest finish), optimal picked `o_k`.
4. Since greedy sorts by finish time, `finish(g_k) ≤ finish(o_k)`.
5. **Swap** `o_k` for `g_k` in `O`: because `g_k` finishes no later than `o_k`, it cannot conflict with any activity `O` accepted after `o_k`. The swap is valid.
6. After the swap, `O` agrees with `G` on one more activity and is still feasible.
7. Repeat the swap until `O = G`. Since `O` was optimal and we never removed activities, `G` is optimal. ∎

**Template:**
```
1. Take any optimal solution O.
2. Find the first place it differs from the greedy solution G.
3. Show you can swap the optimal choice for the greedy choice without making O worse.
4. Conclude: repeat swaps → O becomes G → G is optimal.
```

This template applies to: interval scheduling, job scheduling by deadline, fractional knapsack, and most "sort by X and pick greedily" problems.

### Framework 2 — Greedy Stays Ahead

*Show that after every step, the greedy solution is at least as good as any other solution.*

**Worked example: Jump Game II (minimum jumps to reach end)**

Greedy: at each position, jump to the index that maximizes your next reach.

**Claim:** after `k` jumps, the greedy solution has reached at least as far as any other `k`-jump sequence.

**Proof by induction:**
- Base: after 0 jumps both are at index 0.
- Step: assume greedy is at position `g_k` after `k` jumps, any other strategy is at `p_k ≤ g_k`. From `g_k` we can reach anything from `g_k` onward; from `p_k ≤ g_k` you can reach at most the same indices (and possibly fewer). So after jump `k+1`, greedy is still ahead or tied.
- Since greedy stays ahead at each step and there is a finite end, greedy uses no more jumps. ∎

**Template:**
```
1. Define what "ahead" means (farthest position, most value collected, etc.).
2. Show the greedy solution is ahead after step 1 (base case).
3. Show: if greedy is ahead after step k, it's still ahead after step k+1.
4. Conclude: greedy never falls behind → it's optimal.
```

This template applies to: Jump Game variants, coin change with certain coin sets (all powers of a base), some scheduling problems.

### How to use this in an interview

When asked "why does greedy work?":
1. Identify which framework fits (exchange or stays-ahead).
2. State your greedy choice precisely ("always pick the activity that finishes earliest").
3. Sketch the argument in one sentence: "Any solution that doesn't do this can swap in our greedy choice without getting worse" (exchange) or "after each step, we've reached at least as far as anyone else" (stays-ahead).

You don't need a full formal proof — a clear sentence showing you understand *why* local decisions don't destroy global optimality is enough.

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/greedy/`](../appendix/templates/greedy/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/greedy/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Greedy problems →**](../../lists/recommended.md#15-greedy-14-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can state *why* the greedy choice is safe for a given problem (exchange argument), not just that it works.
- [ ] I can recognize when greedy fails and DP is required instead.
- [ ] I can write the interval-scheduling / Kadane-style greedy from memory.
- [ ] I solved a 🔴 Hard greedy problem (e.g. Candy or Jump Game II).

---

**Up next:** [Intervals](17-intervals.md) — sort first, then one linear pass to merge, count, or sweep.

[← Prev](15-dp-2d.md) · [🗺 Roadmap](../roadmap.md) · [Next →](17-intervals.md)

