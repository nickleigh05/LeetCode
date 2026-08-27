# Glossary

*The jargon of DSA and LeetCode, one line each. When a lesson or editorial drops a term without explaining it, look here.*

**Adjacency list / matrix** — the two ways to store a [graph](../data-structures/graph.md): per-node neighbor lists (usual) vs. an n×n grid of edge flags (dense graphs).

**Amortized** — average cost per operation over a long sequence, even if single operations occasionally spike (list `append` is amortized O(1) despite occasional resizes). See [00f](../learning/00f-foundations-practice.md).

**Ancestor / descendant** — any node above you on the path to the root / anything in your subtree.

**Anti-pattern** — a common approach that looks fine and is reliably wrong (e.g. string `+=` in a loop).

**Base case** — the input a [recursive](../syntax/recursion-basics.md) function answers without recursing; missing one = `RecursionError`.

**Brute force** — the direct try-everything solution; the correct starting point, not an insult.

**Cycle** — a path that revisits a node; in linked lists detected by [fast/slow pointers](../algorithms/floyd-cycle-detection.md), in graphs by DFS states or [topological sort](../algorithms/topological-sort.md).

**DAG** — directed acyclic graph; the shape that makes [topological order](../algorithms/topological-sort.md) and DAG-DP possible.

**Divide and conquer** — split, solve halves recursively, combine ([merge sort](../algorithms/merge-sort.md), [quicksort](../algorithms/quicksort.md)).

**Dry run / trace** — executing code by hand on paper; the highest-value debugging skill. See [debugging-python](debugging-python.md).

**Edge case** — input at the boundary of validity: empty, single element, all equal, min/max constraint values.

**Greedy** — always take the locally best choice; only correct when an exchange argument proves it ([lesson 16](../learning/16-greedy.md)).

**Hash collision** — two keys landing in the same bucket; why dict operations are O(1) *average*, O(n) pathological.

**Heapify** — turning an array into a [heap](../data-structures/heap.md) in O(n).

**In-place** — modifying the input using O(1) extra space instead of building a copy.

**Invariant** — a condition your loop keeps true every iteration ("everything left of `left` is < pivot"); the tool for *proving* two-pointer and binary-search code correct.

**Iterative vs. recursive** — loop-based vs. self-calling; any recursion can be rewritten with an explicit [stack](../data-structures/stack.md).

**k-th smallest/largest** — order-statistic problems; [heap](../learning/09-heap-priority-queue.md) or [quickselect](../algorithms/quickselect.md).

**Leaf** — tree node with no children.

**Lexicographic order** — dictionary order; how Python compares strings, lists, and [tuples](../syntax/tuple-basics.md) element by element.

**Memoization** — caching a function's results by argument so repeats are free; recursion + memoization = top-down [DP](../algorithms/dynamic-programming.md). See [functools-cache](../syntax/functools-cache.md).

**Monotonic** — only ever increasing (or only decreasing); the property behind [monotonic stacks](../data-structures/monotonic-stack.md) and binary-searchable predicates.

**Off-by-one** — the boundary bug family: `<` vs `<=`, `n` vs `n-1`. Half of all Wrong Answers.

**Online / offline algorithm** — must answer queries as they arrive vs. may read all queries first and reorder.

**Pivot** — the element you partition around in [quicksort](../algorithms/quicksort.md)/[quickselect](../algorithms/quickselect.md).

**Pruning** — cutting a [backtracking](../algorithms/backtracking.md) branch early once it provably can't lead to an answer.

**Sentinel / dummy node** — a fake node (or value like `float('inf')`) added to kill edge cases, e.g. the dummy head in [linked lists](../learning/06-linked-list.md).

**Stable sort** — equal elements keep their original relative order; Python's sort is stable, which makes multi-key sorting work ([sorting-key](../syntax/sorting-key.md)).

**State** — the tuple of information that fully describes "where you are" in a search or DP; choosing it *is* the hard part of [DP](../learning/14-dp-1d.md).

**Subarray vs. subsequence vs. subset** — contiguous slice vs. keep-order-drop-some vs. any selection, order irrelevant. Misreading which one the problem wants is a classic instant-fail.

**Tabulation** — bottom-up DP: fill a table from base cases upward (vs. top-down memoization).

**Time/space trade-off** — spending memory to buy speed; the hash-map move ([lesson 01](../learning/01-arrays-hashing.md)).

**TLE / WA / AC / RE / MLE** — judge verdicts; decoded in [how-to-use-leetcode](how-to-use-leetcode.md).

**Two-pass** — solving in two sweeps (often left-to-right then right-to-left) when one direction can't see the whole picture.

**Visited set** — the structure that stops graph traversal from looping forever; forgetting it is the #1 graph bug.

**Related:** [how-to-approach-a-problem](how-to-approach-a-problem.md) · [Foundations lessons](../learning/00a-data-structures.md) · [Data Structures hub](../data-structures/_index.md) · [Algorithms hub](../algorithms/_index.md)
