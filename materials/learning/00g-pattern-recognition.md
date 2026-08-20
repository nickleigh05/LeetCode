# 00g. Pattern Recognition — Choosing the Right Tool

*You know what a hash map is and what O(n log n) means. This lesson is about the step nobody teaches: staring at a fresh problem and knowing where to even start.*

[← Prev](00f-foundations-practice.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](01-arrays-hashing.md)

---

Lessons 00a–00f gave you the vocabulary. This lesson is the missing translation layer: reading a problem statement and mapping its *shape* to a short list of candidate techniques, before you write a single line of code. That mapping is a skill you build by doing it deliberately, on purpose, every time — not something that appears automatically once you've memorized enough patterns.

## The real problem

Clicking "random problem," reading it once, and drawing a blank isn't a knowledge gap — it's a missing **process**. You have the tools (arrays, hash maps, two pointers, DP…); what's missing is a repeatable way to interrogate the problem statement so it tells you which tool it wants. Below is that process.

## Step 1 — Extract the signal, ignore the flavor text

Every problem is a costume over a small set of underlying shapes. Strip the story and answer three questions:

1. **What's the input shape?** Array, string, linked list, tree, graph, matrix, stream?
2. **What's being asked?** Find one thing, find all things, count, optimize (min/max), or decide yes/no?
3. **What's the constraint that would break a brute force?** Look at the input size bound — it's often a direct hint at the required complexity (see Step 3).

Example: *"Given a string, find the length of the longest substring without repeating characters."* Strip it: input = string, ask = optimize (longest), constraint = "substring" means *contiguous*. Contiguous + optimize over a linear structure is the signature of [sliding window](03-sliding-window.md).

## Step 2 — Match keywords to techniques

This isn't a substitute for understanding — it's a first-pass filter to narrow ten possibilities down to two or three you then reason about properly.

| Keywords / phrasing in the problem | Likely technique |
|---|---|
| "subarray", "substring", "contiguous", window with a size or condition | [Sliding window](03-sliding-window.md) |
| "sorted array", "pair that sums to", input already sorted | [Two pointers](02-two-pointers.md) |
| "have I seen this before", "count occurrences", "group by", fast lookup | [Arrays & hashing](01-arrays-hashing.md) |
| "sorted" or "rotated sorted" + "find X" | [Binary search](06-binary-search.md) |
| "valid parentheses", "next greater element", nested/matching structure | [Stack](04-stack.md) |
| "reverse", "cycle", "middle of", pointer surgery on a chain | [Linked list](07-linked-list.md) — fast/slow pointers |
| "top K", "kth largest/smallest", "K closest" | [Heap / priority queue](10-heap-priority-queue.md) |
| "all combinations", "all permutations", "all valid ways to place" | [Backtracking](11-backtracking.md) |
| "connected components", "shortest path", "islands", grid traversal | [Graphs](12-graphs.md) / [grids](11b-grids-primer.md) |
| "minimum/maximum number of ways", overlapping subproblems, "can you reach" | [Dynamic programming](14-dp-1d.md) / [2D DP](15-dp-2d.md) |
| "minimum number of intervals/meetings/resources", greedy-sounding optimum | [Greedy](16-greedy.md) or [intervals](17-intervals.md) |
| "merge intervals", "overlapping ranges", scheduling | [Intervals](17-intervals.md) |
| tree traversal, "ancestor", "depth", "balanced" | [Trees](08-trees.md) |
| "range sum", "range update", many queries over a fixed array | [Prefix sums](01b-prefix-sums.md) or [segment trees](20-segment-trees.md) |
| "union", "connected", "same group", merge sets | [Union-Find](12b-union-find.md) |

Keywords aren't proof — they're a hypothesis to test against Step 3.

## Step 3 — Let the constraints do the talking

Competitive programmers use this trick constantly: **the input size bound tells you the required time complexity**, which eliminates most of your options immediately.

| n (input size) | Required complexity | Rules out | Rules in |
|---|---|---|---|
| n ≤ ~10–12 | O(2ⁿ) or O(n!) fine | nothing | brute force, backtracking, bitmask DP |
| n ≤ ~500 | O(n³) fine | — | triple-nested loops, simple 2D DP |
| n ≤ ~5,000 | O(n²) fine | O(n³) | nested loops, simple DP |
| n ≤ ~10⁵–10⁶ | O(n log n) needed | any O(n²) | sorting, binary search, heap, two pointers, sliding window |
| n ≤ ~10⁸ | O(n) needed | O(n log n) sometimes too slow | single pass, hashing, prefix sums |
| huge / streaming | O(1) or O(log n) per op | almost everything | hashing, binary search, heaps, math |

**How to use this:** if you see n ≤ 20, stop looking for a clever O(n) trick — the problem *wants* you to try all subsets or permutations. If you see n ≤ 10⁵, an O(n²) double loop will time out, so a brute force that "obviously works" is actually a signal to look for the hash map / two-pointer / sorting alternative that collapses it to O(n) or O(n log n).

## Step 4 — A decision tree you can actually run in your head

```
Is the input already sorted, or can I sort it cheaply?
├─ Yes → binary search? two pointers? greedy after sorting?
└─ No
   │
   Am I looking for a contiguous run (subarray/substring)?
   ├─ Yes → sliding window
   └─ No
      │
      Do I need to remember "have I seen this" or count things fast?
      ├─ Yes → hash map / hash set
      └─ No
         │
         Is the input a tree or graph (explicit or implicit, e.g. a grid)?
         ├─ Yes → BFS (shortest path / levels) or DFS (explore all / components)
         └─ No
            │
            Do I need the K largest/smallest, or a running "best so far"?
            ├─ Yes → heap
            └─ No
               │
               Am I asked for ALL ways / combinations / arrangements?
               ├─ Yes → backtracking
               └─ No
                  │
                  Does the answer at position i depend on answers at earlier
                  positions (overlapping subproblems), or am I optimizing
                  a min/max/count over choices?
                  ├─ Yes → dynamic programming
                  └─ No → greedy, math, or a direct simulation
```

This tree won't nail every problem on the first pass — some problems are genuine hybrids (DP-on-graphs, sliding window + hash map). But it turns a blank stare into a ranked list of two or three things to *try*, which is the entire point.

## Step 5 — Verify before you commit

Before writing code, sanity-check your hypothesis out loud (or in your head, in an interview):

- **State the technique and why**: "This looks like sliding window because I need a contiguous substring and I'm optimizing its length."
- **Check it against Step 3**: does the complexity this technique gives match what the constraint demands?
- **Look for the one detail that breaks it**: negative numbers can break a sliding window that assumed monotonic growth; duplicates can break a two-pointer dedup; an unsorted input can quietly rule out binary search until you sort it (and sorting itself costs O(n log n) — worth it, but count it).

If your hypothesis survives this, start coding. If it doesn't, you've only spent a minute, and you have a second candidate from Step 4 ready to try.

## Worked example — cold read

*"You are given an array of integers `nums` and an integer `k`. Return the length of the shortest subarray whose sum is at least `k`. Array can contain negative numbers. `1 ≤ nums.length ≤ 10⁵`."*

1. **Shape**: array, ask = optimize (shortest), constraint word = "subarray" → contiguous.
2. **Keyword match**: "subarray" + "shortest/optimize" screams sliding window.
3. **Constraint check**: n ≤ 10⁵ demands O(n log n) or better — consistent with sliding window (O(n)).
4. **The trap**: sliding window relies on the window sum changing *monotonically* as you move pointers — that only holds when all numbers are non-negative. This problem explicitly allows negatives, so a plain sliding window is **wrong** here. That single sentence should send you to the fallback: monotonic deque + prefix sums, an O(n) technique built for exactly this trap.

This is what Step 5 is for — the "verify before you commit" check is what catches this before you burn ten minutes coding a solution that fails on `[-1, 1, ...]`.

## Practice: run the process, don't skip it

For your next five random problems, before looking at any hint or solution, write down (even just mentally):

1. Input shape + what's being asked (Step 1)
2. Top 2 keyword-matched candidate techniques (Step 2)
3. What the constraint bound requires (Step 3)
4. Which candidate survives Step 5's sanity check

Then check your answer against the problem's actual tag/topic. Being wrong is fine and expected early on — the point is building the habit of asking these questions *before* touching brute force, not being right immediately.

## Check Yourself

- [ ] Given a fresh problem statement, I can name its input shape and what's being asked in one sentence, before thinking about a solution.
- [ ] I can read an input-size bound and say what time complexity it demands.
- [ ] I can list at least two candidate techniques for a problem from its keywords, not just one guess.
- [ ] I know at least one "trap" detail (negative numbers, duplicates, unsorted input) that can invalidate an otherwise-correct-looking pattern match.

---

**Up next:** [Arrays & Hashing](01-arrays-hashing.md) — the first pattern from the table above, in depth.

[← Prev](00f-foundations-practice.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](01-arrays-hashing.md)
