# The Roadmap

### Foundations
| # | Lesson | Why it matters |
|---|--------|----------------|
| 00a | [Data Structures](materials/learning/00a-data-structures.md) | What a data structure *is*, matching structure to operation, contiguous vs. linked memory. |
| 00b | [Algorithms](materials/learning/00b-algorithms.md) | What an algorithm *is*, and why two correct recipes can differ wildly in speed. |
| 00c | [Big O Notation](materials/learning/00c-big-o-notation.md) | The growth classes (O(1) → O(2ⁿ)) and the rules for writing them. |
| 00d | [Time Complexity](materials/learning/00d-time-complexity.md) | How to determine a snippet's Big O: add sequential, multiply nested, halving = log, count built-ins. |
| 00e | [Space Complexity](materials/learning/00e-space-complexity.md) | How to count extra memory (including recursion depth) and the memory-for-speed trade. |
| 00f | [Foundations Practice](materials/learning/00f-foundations-practice.md) | Big-O & code-tracing drills, amortized analysis — make Phase 0 stick before Lesson 01. |

### Linear Structures
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 01 | [Arrays & Hashing](materials/learning/01-arrays-hashing.md) | Trade memory for O(1) lookups; kill brute-force double loops. | [Practice](materials/rmap-practice/01-arrays-hashing.md) |
| 01b | [Prefix Sums](materials/learning/01b-prefix-sums.md) | Precompute once, range queries in O(1); subarray sum = k in O(n). | [Practice](materials/rmap-practice/03-sliding-window.md) · [Practice](materials/rmap-practice/14-dp-2d.md) |
| 02 | [Two Pointers](materials/learning/02-two-pointers.md) | Two cursors on a sorted array drop the O(n²). | [Practice](materials/rmap-practice/02-two-pointers.md) |
| 03 | [Sliding Window](materials/learning/03-sliding-window.md) | A moving boundary over contiguous ranges; O(n). | [Practice](materials/rmap-practice/03-sliding-window.md) |
| 04 | [Stacks & Queues](materials/learning/04-stack.md) | LIFO/FIFO for order-sensitive work; monotonic stack for next-greater. | [Practice](materials/rmap-practice/04-stack.md) |
| 04b | [Recursion & the Call Stack](materials/learning/04b-recursion.md) | Base case + recursive case; the call stack *is* a stack. The bridge to trees, backtracking & DP. | [Practice](materials/rmap-practice/07-trees.md) · [Practice](materials/rmap-practice/10-backtracking.md) · [Practice](materials/rmap-practice/13-dp-1d.md) |

### Searching & Lists
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 05 | [Binary Search](materials/learning/05-binary-search.md) | Halve any ordered search space — including the answer. | [Practice](materials/rmap-practice/05-binary-search.md) |
| 05b | [Sorting](materials/learning/05b-sorting.md) | How `sorted()` actually works: merge/quick sort, the n·log n floor, stability. | [Practice](materials/rmap-practice/15-greedy.md) · [Practice](materials/rmap-practice/16-intervals.md) |
| 06 | [Linked Lists](materials/learning/06-linked-list.md) | Pointer surgery: reverse, dummy head, fast/slow. | [Practice](materials/rmap-practice/06-linked-list.md) |

### Hierarchical Structures
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 07 | [Trees & BSTs](materials/learning/07-trees.md) | DFS base→recurse→combine, or BFS level-by-level. | [Practice](materials/rmap-practice/07-trees.md) |
| 08 | [Tries](materials/learning/08-tries.md) | Prefix trees: O(k) prefix queries. | [Practice](materials/rmap-practice/08-tries.md) |
| 09 | [Heaps / Priority Queues](materials/learning/09-heap-priority-queue.md) | The always-available extreme element; top-K & streaming. | [Practice](materials/rmap-practice/09-heap-priority-queue.md) |

### Recursion & Graphs
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 10 | [Backtracking](materials/learning/10-backtracking.md) | Choose → explore → un-choose over partial solutions. | [Practice](materials/rmap-practice/10-backtracking.md) |
| — | [Grids Primer](materials/learning/10b-grids-primer.md) | The 2-D matrix toolkit — indexing, 4-neighbors, bounds, visited. Read before grid problems. | [Practice](materials/rmap-practice/11-graphs.md) · [Practice](materials/rmap-practice/14-dp-2d.md) · [Practice](materials/rmap-practice/17-math-geometry.md) |
| 11 | [Graphs (BFS/DFS)](materials/learning/11-graphs.md) | BFS for shortest unweighted paths, DFS for connectivity. | [Practice](materials/rmap-practice/11-graphs.md) |
| 12 | [Union-Find](materials/learning/12-union-find.md) | Near-O(1) connectivity and cycle detection under merges. | [Practice](materials/rmap-practice/11-graphs.md) |
| 13 | [Advanced Graphs](materials/learning/13-advanced-graphs.md) | Weighted shortest paths (Dijkstra), ordering (topo sort). | [Practice](materials/rmap-practice/12-advanced-graphs.md) |

### Optimization
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 14 | [1-D Dynamic Programming](materials/learning/14-dp-1d.md) | State + transition + base case over one axis. | [Practice](materials/rmap-practice/13-dp-1d.md) |
| 15 | [2-D Dynamic Programming](materials/learning/15-dp-2d.md) | Same engine, two indices: grids and sequence pairs. | [Practice](materials/rmap-practice/14-dp-2d.md) |
| 16 | [Greedy](materials/learning/16-greedy.md) | Take the locally best choice; the proof is the hard part. | [Practice](materials/rmap-practice/15-greedy.md) |
| 17 | [Intervals](materials/learning/17-intervals.md) | Sort first, then one linear sweep to merge / count. | [Practice](materials/rmap-practice/16-intervals.md) |

### Specialized
| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 18 | [Bit Manipulation](materials/learning/18-bit-manipulation.md) | Masks, shifts, and XOR cancellation in O(1). | [Practice](materials/rmap-practice/18-bit-manipulation.md) |
| 19 | [Math & Geometry](materials/learning/19-math-geometry.md) | GCD, fast power, in-place matrix transforms. | [Practice](materials/rmap-practice/17-math-geometry.md) |

### Materials

| Hub | What's inside |
|-----|---------------|
| [🎯 Interview Roadmap](interview.md) | Behavioral, the interview loop, and system design — paced against these lessons |
| [Guides](materials/guides/_index.md) | Practical know-how: installing Python, editor/terminal/git setup, using LeetCode, debugging, study strategy, interviews |
| [Data Structures](materials/data-structures/_index.md) | Atomic, one-structure-per-file reference pages (array → segment tree) |
| [Algorithms](materials/algorithms/_index.md) | Atomic, one-algorithm-per-file reference pages (binary search → Dijkstra) |
| [Python Syntax Cookbook](materials/syntax/_index.md) | Atomic Python syntax pages — every construct the solutions lean on |
| [Code Templates](materials/appendix/templates/README.md) | Per-pattern `template.py` + README skeletons to memorize |
| [Problem Lists](lists/) | Curated sets: [recommended](lists/recommended.md) · [Blind 75](lists/neetcodeblind75.md) · [NeetCode 150](lists/neetcode150.md) · [NeetCode 250](lists/neetcode250.md) · [Rushed 40](lists/rushed40.md) |
