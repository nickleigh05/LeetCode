# Algorithm Skeletons

The canonical code *shape* for each major DSA pattern — not solutions to specific
problems. Each pattern is the reusable skeleton you adapt to a problem, with the
problem-specific logic marked `# TODO`. When you recognize the pattern, you
already know 80% of the code; this directory is that 80%.

Think labuladong, but in English and tuned to how I write.

## How to use this

- **Stuck on a problem?** Identify the pattern from its "Recognize this pattern when..." section, then start from the matching `template.py`.
- **Drilling a category?** Read the `README.md`, type out the `template.py` from memory, then grind the representative problems listed.
- Each folder has exactly two files:
  - **`template.py`** — the generic, fully-typed skeleton with inline *why* comments and a docstring covering time / space / the invariant it maintains.
  - **`README.md`** — when to reach for it, 3–5 variations, representative LeetCode problems (easy → hard), and the off-by-one traps.

## Patterns, in suggested study order

Work top to bottom — each tier builds on the last. Don't jump to graphs before two pointers feels automatic.

### Foundations

| # | Pattern | The one-line idea |
|---|---------|-------------------|
| 1 | [Arrays & Hashing](arrays-hashing/README.md) | Trade memory for O(1) lookups; kills brute-force double loops. |
| 2 | [Two Pointers](two-pointers/README.md) | Two cursors on a sorted array converge or chase to drop the O(n²). |
| 3 | [Sliding Window](sliding-window/README.md) | A moving boundary over contiguous ranges; O(n) instead of O(n²). |
| 4 | [Stack](stack/README.md) | LIFO for "most recent unresolved" — matching, monotonic, evaluation. |
| 5 | [Binary Search](binary-search/README.md) | Halve any ordered search space — including the answer itself. |

### Linked structures & trees

| # | Pattern | The one-line idea |
|---|---------|-------------------|
| 6 | [Linked List](linked-list/README.md) | Pointer surgery: reverse, dummy head, fast/slow. |
| 7 | [Trees](trees/README.md) | DFS base→recurse→combine, or BFS level-by-level. |
| 8 | [Tries](tries/README.md) | Prefix trees: O(k) prefix queries, dictionary stored once. |
| 9 | [Heap / Priority Queue](heap-priority-queue/README.md) | Always-available extreme element for top-K and streaming. |

### Recursion & graphs

| # | Pattern | The one-line idea |
|---|---------|-------------------|
| 10 | [Backtracking](backtracking/README.md) | Choose → explore → un-choose over the tree of partial solutions. |
| 11 | [Graphs](graphs/README.md) | BFS for shortest unweighted paths, DFS for connectivity. |
| 12 | [Union-Find](union-find/README.md) | Near-O(1) connectivity and cycle detection under merges. |
| 13 | [Advanced Graphs](advanced-graphs/README.md) | Weighted shortest paths (Dijkstra), ordering (topo sort), MST. |

### Dynamic programming

| # | Pattern | The one-line idea |
|---|---------|-------------------|
| 14 | [1-D Dynamic Programming](dp-1d/README.md) | State + transition + base case over one axis. |
| 15 | [2-D Dynamic Programming](dp-2d/README.md) | Same engine, two indices: grids and sequence pairs. |

### Optimization & odds-and-ends

| # | Pattern | The one-line idea |
|---|---------|-------------------|
| 16 | [Greedy](greedy/README.md) | Take the locally best choice; the proof is the hard part. |
| 17 | [Intervals](intervals/README.md) | Sort first, then one linear pass to merge / count / sweep. |
| 18 | [Bit Manipulation](bit-manipulation/README.md) | Masks, shifts, and XOR cancellation in O(1). |
| 19 | [Math & Geometry](math-geometry/README.md) | GCD, fast power, in-place matrix transforms. |

---

*Categories follow the NeetCode 150/250 taxonomy. For the curated problem sets that pair with these skeletons, see [lists/](../../../lists/); to learn each pattern in depth, follow the [🗺 Roadmap](../../roadmap.md).*
