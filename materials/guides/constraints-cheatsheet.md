# Constraints → Complexity Cheatsheet

*The input size tells you which Big-O the judge expects. Read this table before designing anything.*

Rule of thumb: an online judge runs roughly **10⁷–10⁸ simple operations per second** of time limit (Python gets extra headroom on LeetCode). Plug the max n into a candidate complexity; if the result blows past ~10⁸, that approach will TLE.

| Max n | Target complexity | Typical intended approach |
|-------|-------------------|---------------------------|
| n ≤ 12 | O(n!) | Permutation [backtracking](../learning/10-backtracking.md) |
| n ≤ 20–25 | O(2ⁿ) | Subset backtracking, bitmask enumeration, [meet-in-the-middle](../algorithms/meet-in-the-middle.md) |
| n ≤ 100 | O(n³) | Triple loop, Floyd-Warshall, interval DP |
| n ≤ 1,000 | O(n²) | Double loop, 2-D [DP](../learning/15-dp-2d.md) over pairs |
| n ≤ 100,000 | O(n log n) | [Sort](../learning/05b-sorting.md), [heap](../learning/09-heap-priority-queue.md), [binary search](../learning/05-binary-search.md), [segment tree](../learning/20-segment-trees.md) |
| n ≤ 1,000,000 | O(n) | One pass — [hash map](../learning/01-arrays-hashing.md), [sliding window](../learning/03-sliding-window.md), [prefix sums](../learning/01b-prefix-sums.md), [Kadane](../algorithms/kadane-algorithm.md) |
| n ≤ 10⁹ or 10¹⁸ | O(log n) or O(1) | You never iterate n — [binary search on the answer](../learning/05-binary-search.md), math/[digit tricks](../learning/18-bit-manipulation.md), [fast exponentiation](../algorithms/fast-exponentiation.md) |

## How to actually use it

1. Find the max n in the constraints block.
2. Read off the target complexity row.
3. Reject designs above the row *before* coding them; the table is also permission — n ≤ 20 means "the exponential solution is the intended one, stop hunting for a polynomial trick."

## Second-order reads

- **Two sizes** (n and m): the target usually multiplies — n, m ≤ 1000 suggests O(n·m) 2-D DP; n ≤ 10⁵, m ≤ 10⁵ suggests O((n + m) log …).
- **Values bounded small** (`nums[i] ≤ 100`) while n is huge → iterate over *values*, not elements: [counting sort](../algorithms/counting-sort.md), frequency arrays, bucket tricks.
- **"answer modulo 10⁹ + 7"** → the count is astronomically large → it's a [DP](../learning/14-dp-1d.md)/combinatorics counting problem; see [modular-arithmetic](../algorithms/modular-arithmetic.md).
- **Grid up to 300 × 300** → n is really 9·10⁴ cells → O(cells) or O(cells · log) [BFS/DFS](../learning/11-graphs.md); O(cells²) is dead.
- **"follow-up: O(1) space"** → the interviewer wants pointer tricks or in-place mutation, not a hash map.

Numbers here are heuristics, not law — a heavy constant (nested Python loops with function calls) can sink a "passing" complexity, and simple array math can save a borderline one.

**Related:** [how-to-approach-a-problem](how-to-approach-a-problem.md) · [python-operation-costs](python-operation-costs.md) · [Big O lesson](../learning/00c-big-o-notation.md) · [Time complexity lesson](../learning/00d-time-complexity.md)
