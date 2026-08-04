# 1851. Minimum Interval to Include Each Query

**Hard** · [LeetCode](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Solution: not yet solved in this repo.

For each query point, find the size of the smallest interval that contains it. Why does processing queries in sorted order, adding newly-eligible intervals to a min-heap keyed by size, let stale (too-small) intervals be discarded lazily instead of tracked explicitly?

<details>
<summary>Hint</summary>

Sort intervals by start and queries by value. Sweep through sorted queries, pushing every interval whose start is `<=` the query onto a min-[heap](../data-structures/heap.md) keyed by `(size, end)`. Pop off intervals whose `end` is too small for the current query (lazy deletion) — the heap's root is then the smallest valid interval.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:

        intervals.sort()
        sorted_queries = sorted(range(len(queries)), key=lambda i: queries[i])

        heap = []   # (size, end)
        result = [0] * len(queries)
        i = 0

        for query_index in sorted_queries:
            query = queries[query_index]

            while i < len(intervals) and intervals[i][0] <= query:
                left, right = intervals[i]
                heapq.heappush(heap, (right - left + 1, right))
                i += 1

            while heap and heap[0][1] < query:
                heapq.heappop(heap)

            result[query_index] = heap[0][0] if heap else -1

        return result
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [heap](../data-structures/heap.md) · [while-loop](../syntax/while-loop.md) (nested) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O((n + q) log n)** — n intervals and q queries, each heap push/pop O(log n).
**Space: O(n)** — the heap holds up to all intervals at once.
</details>
