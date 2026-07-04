# How to Approach a Problem

*A repeatable procedure for going from problem statement to accepted solution — so a blank editor never means a blank mind.*

Strong solvers don't wing it; they run the same loop every time. Here it is, six steps.

## 1. Understand — restate and probe

Read the statement twice, then restate it in one sentence *without the story* ("given an array, find two indices whose values sum to target"). Interrogate the details people skip: Can the input be empty? Duplicates? Negatives? Is the array sorted? One valid answer or many? Return *indices* or *values*? In an interview, ask these out loud — see [interview-guide](interview-guide.md).

## 2. Read the constraints — they leak the intended solution

The line `1 <= nums.length <= 10^5` is not legal boilerplate; it's the strongest hint on the page. Rough budget: ~10⁷–10⁸ simple operations pass. So n = 10⁵ means O(n²) = 10¹⁰ is dead — you're looking for O(n log n) or O(n). And n ≤ 20 *invites* the exponential [backtracking](../learning/10-backtracking.md) solution. Full table: [constraints-cheatsheet](constraints-cheatsheet.md).

## 3. Work small examples by hand

Take the sample input (and one you invent) and solve it *on paper, as a human*. Watch what your own brain does — "I keep checking whether I've seen the complement before" *is* the [hash map](../learning/01-arrays-hashing.md) solution announcing itself. If you can't do it by hand, you have no business coding it yet.

## 4. Brute force first, then name the bottleneck

State the dumb solution and its complexity ("try all pairs, O(n²)"). Now you have something correct to optimize, and the optimization question becomes concrete: *what work is being repeated?* Match the smell to a pattern:

- Repeatedly *searching* for something → [hash map](../learning/01-arrays-hashing.md), or [binary search](../learning/05-binary-search.md) if sorted
- Re-scanning overlapping ranges → [sliding window](../learning/03-sliding-window.md) / [prefix sums](../learning/01b-prefix-sums.md)
- Pairs in a sorted array → [two pointers](../learning/02-two-pointers.md)
- Repeatedly needing the min/max so far → [heap](../learning/09-heap-priority-queue.md) / [monotonic stack](../data-structures/monotonic-stack.md)
- Same subproblem recomputed → [DP](../learning/14-dp-1d.md)
- "All combinations/paths" with tiny n → [backtracking](../learning/10-backtracking.md)

## 5. Code it — top-down, edge cases first

Write the skeleton before the cleverness: handle the empty/one-element cases, set up the data structure, then the main loop. Name variables for meaning (`left`, `best`, `seen` — not `a`, `b`, `x`). If you know the pattern's [template](../appendix/templates/README.md), start from it and adapt.

## 6. Verify before you submit

Trace your code line-by-line on one sample and one edge case — *by hand, playing computer*, not by re-reading it and nodding. Then check the classics: empty input, single element, all duplicates, negatives, min/max constraint sizes. One minute of tracing beats three Wrong Answer round-trips.

---

**Stuck?** Set a timer. At 30 minutes with no working idea, read a hint or the first paragraph of the editorial, then *close it* and implement from memory. At 45+, study the full solution, close it, re-implement from scratch, and schedule a re-solve in 3 days — see [study-plan](study-plan.md). Struggling productively builds skill; staring at a wall past 45 minutes just builds frustration.

**Related:** [constraints-cheatsheet](constraints-cheatsheet.md) · [how-to-use-leetcode](how-to-use-leetcode.md) · [interview-guide](interview-guide.md) · [study-plan](study-plan.md)
