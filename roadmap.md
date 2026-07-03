# The Roadmap

## 🛤 The lessons

### Phase 0 — Foundations
| # | Lesson | Why it matters |
|---|--------|----------------|
| 00 | [Foundations](materials/learning/00-foundations.md) | What data structures & algorithms *are*, Big O, and how to use this repo. |
| 00b | [Foundations Practice](materials/learning/00b-foundations-practice.md) | Big-O & code-tracing drills, amortized analysis — make Phase 0 stick before Lesson 01. |

### Phase 1 — Linear Structures *(the building blocks)*
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 01 | [Arrays & Hashing](materials/learning/01-arrays-hashing.md) | Trade memory for O(1) lookups; kill brute-force double loops. | [→](materials/rmap-practice/01-arrays-hashing.md) |
| 01b | [Prefix Sums](materials/learning/01b-prefix-sums.md) | Precompute once, range queries in O(1); subarray sum = k in O(n). | woven into 03/15 |
| 02 | [Two Pointers](materials/learning/02-two-pointers.md) | Two cursors on a sorted array drop the O(n²). | [→](materials/rmap-practice/02-two-pointers.md) |
| 03 | [Sliding Window](materials/learning/03-sliding-window.md) | A moving boundary over contiguous ranges; O(n). | [→](materials/rmap-practice/03-sliding-window.md) |
| 04 | [Stacks & Queues](materials/learning/04-stack.md) | LIFO/FIFO for order-sensitive work; monotonic stack for next-greater. | [→](materials/rmap-practice/04-stack.md) |
| 04b | [Recursion & the Call Stack](materials/learning/04b-recursion.md) | Base case + recursive case; the call stack *is* a stack. The bridge to trees, backtracking & DP. | woven into 07/10/14 |

### Phase 2 — Searching & Lists
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 05 | [Binary Search](materials/learning/05-binary-search.md) | Halve any ordered search space — including the answer. | [→](materials/rmap-practice/05-binary-search.md) |
| 05b | [Sorting](materials/learning/05b-sorting.md) | How `sorted()` actually works: merge/quick sort, the n·log n floor, stability. | woven into 16/17 |
| 06 | [Linked Lists](materials/learning/06-linked-list.md) | Pointer surgery: reverse, dummy head, fast/slow. | [→](materials/rmap-practice/06-linked-list.md) |

### Phase 3 — Hierarchical Structures
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 07 | [Trees & BSTs](materials/learning/07-trees.md) | DFS base→recurse→combine, or BFS level-by-level. | [→](materials/rmap-practice/07-trees.md) |
| 08 | [Tries](materials/learning/08-tries.md) | Prefix trees: O(k) prefix queries. | [→](materials/rmap-practice/08-tries.md) |
| 09 | [Heaps / Priority Queues](materials/learning/09-heap-priority-queue.md) | The always-available extreme element; top-K & streaming. | [→](materials/rmap-practice/09-heap-priority-queue.md) |

### Phase 4 — Recursion & Graphs
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 10 | [Backtracking](materials/learning/10-backtracking.md) | Choose → explore → un-choose over partial solutions. | [→](materials/rmap-practice/10-backtracking.md) |
| — | [Grids Primer](materials/learning/10b-grids-primer.md) | The 2-D matrix toolkit — indexing, 4-neighbors, bounds, visited. Read before grid problems. | woven into 11/15/19 |
| 11 | [Graphs (BFS/DFS)](materials/learning/11-graphs.md) | BFS for shortest unweighted paths, DFS for connectivity. | [→](materials/rmap-practice/11-graphs.md) |
| 12 | [Union-Find](materials/learning/12-union-find.md) | Near-O(1) connectivity and cycle detection under merges. | [→](materials/rmap-practice/11-graphs.md) |
| 13 | [Advanced Graphs](materials/learning/13-advanced-graphs.md) | Weighted shortest paths (Dijkstra), ordering (topo sort). | [→](materials/rmap-practice/12-advanced-graphs.md) |

### Phase 5 — Optimization
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 14 | [1-D Dynamic Programming](materials/learning/14-dp-1d.md) | State + transition + base case over one axis. | [→](materials/rmap-practice/13-dp-1d.md) |
| 15 | [2-D Dynamic Programming](materials/learning/15-dp-2d.md) | Same engine, two indices: grids and sequence pairs. | [→](materials/rmap-practice/14-dp-2d.md) |
| 16 | [Greedy](materials/learning/16-greedy.md) | Take the locally best choice; the proof is the hard part. | [→](materials/rmap-practice/15-greedy.md) |
| 17 | [Intervals](materials/learning/17-intervals.md) | Sort first, then one linear sweep to merge / count. | [→](materials/rmap-practice/16-intervals.md) |

### Phase 6 — Specialized
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 18 | [Bit Manipulation](materials/learning/18-bit-manipulation.md) | Masks, shifts, and XOR cancellation in O(1). | [→](materials/rmap-practice/18-bit-manipulation.md) |
| 19 | [Math & Geometry](materials/learning/19-math-geometry.md) | GCD, fast power, in-place matrix transforms. | [→](materials/rmap-practice/17-math-geometry.md) |

### Phase 7 — Mastery Track *(optional — for hard-level & competitive programming)*
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 20 | [Segment Trees & Fenwick Trees](materials/learning/20-segment-trees.md) | Range queries + point updates in O(log n). The upgrade from prefix sums when the array changes. | LC 307, 315, 493 |

### Materials
