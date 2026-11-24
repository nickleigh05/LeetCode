# 2392. Build a Matrix With Conditions

**Hard** · [LeetCode](https://leetcode.com/problems/build-a-matrix-with-conditions/) · [Solution file (no hints)](../../problems/2000-2499/2392.py)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Given a positive integer `k`, build a `k × k` matrix that contains each number `1..k` **exactly once** (the other cells are `0`), such that:

- `rowConditions[i] = [above, below]`: `above` appears in a **strictly higher row** than `below`.
- `colConditions[i] = [left, right]`: `left` appears in a **strictly earlier column** than `right`.

Return any valid matrix, or `[]` if none exists.

```
k = 3,  rowConditions = [[1, 2], [3, 2]],  colConditions = [[2, 1], [3, 2]]
→ [[0, 0, 1],
   [3, 0, 0],
   [0, 2, 0]]
```

**Constraints:** `2 <= k <= 400` · `1 <= rowConditions.length, colConditions.length <= 10⁴` · conditions are pairs of numbers in `1..k` that differ

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "`a` must be above `b`" | A **precedence constraint**: `a → b` in a directed graph |
| rows and columns have **independent** constraints | Two separate problems: order the numbers by row, and order them by column |
| each number exactly once | Every number gets one row and one column, so each number sits at `(row_position, col_position)` |
| "or return `[]`" | A **cycle** in either constraint set makes it impossible |
| any valid matrix | Any topological order works |

**The key insight is the independence.** Row conditions say nothing about columns, and vice versa. So:

1. [Topologically sort](../algorithms/topological-sort.md) the numbers using `rowConditions` → `row_order` (position in this list = row).
2. Topologically sort them again using `colConditions` → `col_order` (position = column).
3. Place number `v` at `(row_order.index(v), col_order.index(v))`.

Every number has a distinct row (its position in `row_order`) and a distinct column, so no two collide, and all constraints hold by construction.

🤔 **Before you open the next section:** if the row conditions contain `[1, 2]` and `[2, 1]`, what does a topological sort do, and how do you notice?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Try all placements | exponential | ❌ |
| **Two topological sorts (Kahn's algorithm, BFS with in-degrees)** | **O(k + R + C)** | ✅ |
| Two DFS-based topological sorts | O(k + R + C) | ✅ Needs three-colour cycle detection |

**The decision: [Kahn's algorithm](../algorithms/topological-sort.md) twice.** Count each node's in-degree, start with in-degree-0 nodes, and repeatedly remove them while lowering their neighbours' in-degrees. If you finish with fewer than `k` nodes ordered, a cycle blocked the rest, so return `[]`. The same technique solves [Course Schedule II](210-course-schedule-ii.md).

I'll write the sort as a helper that takes a list of conditions and returns an order, or an empty list on a cycle.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def topo_sort(conditions: List[List[int]]) -> List[int]:
    graph = [[] for _ in range(k + 1)]
    indegree = [0] * (k + 1)
    for before, after in conditions:
        graph[before].append(after)
        indegree[after] += 1
```

Build the directed graph for one dimension. `graph[u]` holds everything that must come after `u`, and `indegree[v]` counts how many things must come before `v`. Index `0` is unused since numbers start at 1.
→ [list-comprehension](../syntax/list-comprehension.md) · [graph](../data-structures/graph.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    queue = deque(node for node in range(1, k + 1) if indegree[node] == 0)
    order = []
```

Start with numbers that have no prerequisites. A number with no conditions at all also starts here, so unconstrained numbers still get placed.
→ [deque-basics](../syntax/deque-basics.md) · [generator-expressions](../syntax/generator-expressions.md)

```python
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
```

Take a ready node, append it to the order, and "remove" its outgoing edges. Any neighbour whose in-degree falls to 0 has no remaining prerequisites, so it joins the queue.
→ [while-loop](../syntax/while-loop.md) · [bfs](../algorithms/bfs.md)

```python
    return order if len(order) == k else []
```

If a cycle exists, its nodes never reach in-degree 0, so `order` is short. An empty list signals "impossible".
→ [ternary-expression](../syntax/ternary-expression.md)

```python
row_order = topo_sort(rowConditions)
col_order = topo_sort(colConditions)
if not row_order or not col_order:
    return []
```

Sort each dimension independently. A cycle in either one means no matrix exists.

```python
col_position = {value: index for index, value in enumerate(col_order)}
matrix = [[0] * k for _ in range(k)]
for row, value in enumerate(row_order):
    matrix[row][col_position[value]] = value
return matrix
```

Number `value` goes in row `row` (its place in `row_order`) and column `col_position[value]`. A dictionary avoids an O(k) `.index` call per number.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [nested-lists](../syntax/nested-lists.md) · [enumerate](../syntax/enumerate.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque


class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]],
                    colConditions: List[List[int]]) -> List[List[int]]:

        def topo_sort(conditions: List[List[int]]) -> List[int]:
            graph = [[] for _ in range(k + 1)]
            indegree = [0] * (k + 1)
            for before, after in conditions:
                graph[before].append(after)
                indegree[after] += 1

            queue = deque(node for node in range(1, k + 1) if indegree[node] == 0)
            order = []
            while queue:
                node = queue.popleft()
                order.append(node)
                for nxt in graph[node]:
                    indegree[nxt] -= 1
                    if indegree[nxt] == 0:
                        queue.append(nxt)

            return order if len(order) == k else []

        row_order = topo_sort(rowConditions)
        col_order = topo_sort(colConditions)
        if not row_order or not col_order:
            return []

        col_position = {value: index for index, value in enumerate(col_order)}
        matrix = [[0] * k for _ in range(k)]
        for row, value in enumerate(row_order):
            matrix[row][col_position[value]] = value

        return matrix
```

</details>

**Trace it.** `k = 3`, rows `[[1,2],[3,2]]`, columns `[[2,1],[3,2]]`:

| Dimension | Edges | Order |
|---|---|---|
| rows | `1→2`, `3→2` | `[1, 3, 2]` |
| columns | `2→1`, `3→2` | `[3, 2, 1]` |

| Number | Row (`row_order` index) | Column (`col_order` index) |
|---|---|---|
| 1 | 0 | 2 |
| 3 | 1 | 0 |
| 2 | 2 | 1 |

The matrix is `[[0,0,1],[3,0,0],[0,2,0]]` ✅ (matches the example).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(k² + R + C)</summary>

Each topological sort is **O(k + conditions)**. Building the `k × k` matrix of zeros is **O(k²)**, which dominates for dense inputs: `400² = 160,000`. Total **O(k² + R + C)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k² + R + C)</summary>

The output matrix is `k²`. The graphs hold `R` and `C` edges. Everything else is O(k).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Row conditions and column conditions are independent, so I solve them separately. Each is a precedence graph over the numbers 1..k, and a valid arrangement is a topological order. I run Kahn's algorithm for rows and again for columns, and if either one can't order all k numbers, there's a cycle and I return empty. Otherwise a number's row is its index in the row order and its column is its index in the column order. Each number gets a unique row and column, so the placements can't collide. O(k² + conditions)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do the two dimensions not interfere?" | A number's row only matters to row conditions and its column only to column conditions, and unique indices in both orders prevent collisions |
| "DFS instead of Kahn?" | Reverse post-order with a three-state visited array (unvisited, in-progress, done). An in-progress node being reached again means a cycle |
| "Multiple valid answers?" | Any topological order is fine, so the matrix isn't unique |
| "Duplicate conditions?" | They add duplicate edges, but in-degree counts match the edge counts, so Kahn's algorithm still works |
| "Related?" | [Course Schedule II](210-course-schedule-ii.md) · [Alien Dictionary](269-alien-dictionary.md) |

**Traps:**

- **Treating rows and columns as one graph.** They're independent.
- **Skipping the cycle check.** `len(order) < k` is how you detect it.
- **Looking numbers up with `.index`** inside the loop: O(k²) for no reason.
- **Not including unconstrained numbers.** They have in-degree 0 and must be in the initial queue.

**This same move shows up in:** [Course Schedule II](210-course-schedule-ii.md) · [Course Schedule](207-course-schedule.md) · [Alien Dictionary](269-alien-dictionary.md).

</details>

---
