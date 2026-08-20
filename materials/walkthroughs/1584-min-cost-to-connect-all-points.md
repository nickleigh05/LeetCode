# 1584. Min Cost to Connect All Points

**Medium** · [LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. Advanced Graphs problems](../rmap-practice/13-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given `points` on a 2-D plane. The cost of connecting two points is their **Manhattan distance**: `|x1 − x2| + |y1 − y2|`. Return the minimum total cost to connect all points such that there is **exactly one simple path** between any two points.

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]  →  20

points = [[3,12],[-2,5],[-4,1]]            →  18
```

**Constraints:** `1 <= points.length <= 1000` · `-10⁶ <= xi, yi <= 10⁶` · all points are distinct.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| points, and a cost between any two | This is a **complete weighted graph** — every pair of points is a candidate edge. You are not *given* the edges; you compute them on demand |
| "**minimum** total cost" | An optimization problem, so the candidates are greedy, DP, or a known graph algorithm |
| "connect **all** points" | Every node must end up in one connected component |
| "**exactly one** simple path between any two points" | This is the textbook definition of a **tree**: connected, and no cycles (two paths would mean a cycle). Combined with "minimum cost", the problem is literally asking for a **minimum spanning tree** |
| `n <= 1000` | n² = 10⁶ edges. Materializing all of them is *borderline* fine; anything worse than n² log n is not |
| Manhattan distance, all weights ≥ 0 | Weights are non-negative and symmetric — an undirected graph, which is what MST algorithms require |

That fourth row is the whole problem. The phrase "exactly one simple path between any two points" is a **disguised definition** — recognizing that it means *spanning tree* is the entire recognition step, and the rest is recall.

The other thing worth noticing: **you're not handed an edge list.** The graph is implicit, defined by a distance formula. That will shape which MST algorithm is convenient.

🤔 **Before you open the next section:** you know two MST algorithms. One sorts all the edges; one grows a tree outward from a starting node. Given that this graph has n² edges but only n nodes, which one wants less from you?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try all spanning trees | Enumerate them and take the cheapest | O(nⁿ⁻²) | — | ❌ Cayley's formula. Astronomically dead |
| Greedy "connect each point to its nearest" | For each point, add its cheapest edge | O(n²) | O(n) | ❌ Doesn't produce a tree — you get disconnected clusters and duplicated edges |
| [Kruskal's](../algorithms/kruskal-mst.md) | Build all n² edges, sort, add each if it joins two components ([union-find](../data-structures/union-find.md)) | O(n² log n) | **O(n²)** | ⚠️ Correct, same time bound — but it must *materialize and sort* all 500k edges |
| **[Prim's](../algorithms/prim-mst.md)** | Grow one tree from point 0; repeatedly add the cheapest edge to an unvisited point, via a min-[heap](../data-structures/heap.md) | O(n² log n) | O(n²) | ✅ |

**The decision:** [Prim's algorithm](../algorithms/prim-mst.md) with a min-heap.

**Why Prim's over Kruskal's here?** Both are O(n² log n) on paper, so this is a judgment call — and the reason is the *implicit graph*. Kruskal's needs the complete sorted edge list before it can start; on a dense graph that's a 500,000-element list you construct up front. Prim's never needs a global edge list: it only ever asks *"from the tree I have so far, what's the cheapest way out?"* — and it can compute those distances lazily as it expands. **Kruskal's is the tool when edges are given and sparse; Prim's is the tool when the graph is dense or implicit.** That sentence is the answer to "why did you pick this one."

**Why does the greedy work at all?** The *cut property*: for any way of splitting the nodes into two groups, the cheapest edge crossing that split is in some MST. Prim's split is always "visited vs. unvisited," and the heap always hands back the cheapest edge crossing it. So every edge it adds is safe.

**Why not Dijkstra?** They look nearly identical — both are heap-driven greedy expansions — and confusing them is the classic error. The difference is what the heap key measures: **Dijkstra pushes `distance_from_source + edge_weight` (a cumulative path cost); Prim's pushes just `edge_weight` (the cost of one hop into the tree).** Dijkstra minimizes distance *to each node*; Prim's minimizes the *total* of the edges chosen.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
```
Python's binary min-heap. It's a set of functions operating on a plain list, not a class — `heappush` / `heappop` maintain the heap invariant in place.
→ [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
n = len(points)
visited = set()
min_heap = [(0, 0)]   # (cost, point index)
total = 0
```
Four pieces of state. `visited` is the growing tree. The heap holds candidate edges as `(cost, point_index)` — cost first, because tuples compare element-wise and that's what makes the heap order by cost. Seeding it with `(0, 0)` means "point 0 joins the tree for free," which is how you pick an arbitrary start; **any** starting point yields a valid MST of the same total.
→ [set-basics](../syntax/set-basics.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
while len(visited) < n:
    cost, i = heapq.heappop(min_heap)
```
Loop until every point is in the tree — n additions, so the loop body's *successful* runs are exactly n. `heappop` returns the globally cheapest pending edge in O(log n).
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    if i in visited:
        continue
```
The **lazy-deletion** line, and the one worth understanding. The heap accumulates stale entries: a point can be pushed many times, once from each tree node that considered it. Rather than hunt down and remove the outdated ones (a heap can't do that efficiently), you leave them and discard them on the way out. The first time a point is popped it carries its *cheapest* edge, because the heap is ordered by cost — every later copy is by definition worse, and skipped.
→ [membership-operators](../syntax/membership-operators.md) · [break-continue](../syntax/break-continue.md)

```python
    visited.add(i)
    total += cost
```
The point joins the tree, and its connecting edge is bought. Because of the `continue` above, this runs exactly n times — so exactly n − 1 real edges get paid for (the seed contributes 0). That's the edge count of a spanning tree, which is a good self-check.
→ [set-operations](../syntax/set-operations.md)

```python
    for j in range(n):
        if j not in visited:
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            heapq.heappush(min_heap, (dist, j))
```
The implicit graph, materialized one row at a time. Having just added point `i`, every unvisited point now has a new way in — through `i` — so push all of those as candidates. The distance is computed on the spot from the formula; no edge list ever exists.

The `if j not in visited` guard isn't strictly needed (the pop-side check would catch them), but it keeps the heap meaningfully smaller.
→ [range-function](../syntax/range-function.md) · [nested-lists](../syntax/nested-lists.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return total
```
Every point is in the tree; `total` is the sum of the n − 1 edges that put them there.

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        visited = set()
        min_heap = [(0, 0)]   # (cost, point index)
        total = 0

        while len(visited) < n:
            cost, i = heapq.heappop(min_heap)
            if i in visited:
                continue
            visited.add(i)
            total += cost

            for j in range(n):
                if j not in visited:
                    dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    heapq.heappush(min_heap, (dist, j))

        return total
```
</details>

**Trace it** — `points = [[0,0],[2,2],[3,10],[5,2],[7,0]]` (indices 0–4)

| Pop | Skip? | `visited` | `total` | Pushed next |
|---|---|---|---|---|
| `(0, 0)` | no | `{0}` | 0 | `(4,1) (13,2) (7,3) (7,4)` |
| `(4, 1)` | no | `{0,1}` | 4 | `(9,2) (3,3) (7,4)` |
| `(3, 3)` | no | `{0,1,3}` | 7 | `(10,2) (4,4)` |
| `(4, 4)` | no | `{0,1,3,4}` | 11 | `(14,2)` |
| `(7, 4)` | **yes** — stale | — | — | — |
| `(7, 4)` | **yes** — stale | — | — | — |
| `(9, 2)` | no | all 5 | **20** | — |

Answer: **20** ✅

Two things the trace shows. Point 4 was pushed three separate times at costs 7, 7 and 4 — the cheapest surfaced first and the rest were discarded by the `continue`, which is lazy deletion doing its job. And point 2 (the far-off `[3,10]`) kept getting cheaper offers — 13, then 9 — as the tree grew closer to it, which is exactly the behaviour that makes the greedy correct.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n² log n)</summary>

**O(n² log n).**

- The `while` loop does useful work n times, but it also spins once per stale entry, so it runs once per heap element overall.
- Each successful iteration pushes up to n candidates → **O(n²) pushes total**.
- Every push and every pop is O(log(heap size)) = O(log n²) = **O(2 log n) = O(log n)**.
- n² operations × O(log n) = **O(n² log n)**.

With n = 1000 that's about 10⁶ × 10 = 10⁷ heap operations — comfortably fast enough.

**The optimization worth naming:** you can drop the heap entirely and keep a plain `dist[]` array of "cheapest known edge into the tree" per point, scanning it linearly to find the minimum each round. That's **O(n²)** with no log factor, and on a *dense* graph like this it's genuinely faster. Mentioning that you know dense-Prim's exists is a strong signal; the heap version is still the right thing to write first because it's the one that generalizes to sparse graphs.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²)</summary>

**O(n²)**, and the heap is entirely to blame.

- `visited` holds at most n indices → O(n).
- `total`, `n`, `dist` → O(1).
- `min_heap` — each of the n additions pushes up to n candidates, and stale entries are never removed early. In the worst case it holds **O(n²)** tuples.

That's ~10⁶ tuples at n = 1000. Fine, but it's the honest number, and it's the price of lazy deletion.

**The fix, if pressed:** the array-based dense Prim's above is **O(n)** space — one distance per point, updated in place. So the two variants trade cleanly: heap version is O(n² log n) time / O(n²) space; array version is O(n²) time / O(n) space. On this problem the array version wins on both.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "'Exactly one simple path between any two points' means the result has to be a tree, and we want the cheapest one — so this is a minimum spanning tree. The graph is complete and implicit: n² edges defined by a distance formula, not given to me. That pushes me toward Prim's over Kruskal's, because Kruskal's would need me to build and sort all 500,000 edges up front, while Prim's just grows a tree from any starting point and asks the heap for the cheapest way out. I use lazy deletion — a stale heap entry is discarded when popped rather than removed. O(n² log n) time, O(n²) space. If space mattered, the array-based dense version is O(n²) time and O(n) space, and on a graph this dense it's actually faster."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not Kruskal's?" | Same complexity, but it requires materializing and sorting all n² edges. Kruskal's shines when the edge list is given and sparse (E ≈ V); here the graph is dense and implicit, which is Prim's home turf. |
| "Prove the greedy is correct." | The cut property: for any partition of the nodes, the minimum-weight edge crossing it belongs to some MST. Prim's cut is always visited/unvisited, and the heap returns exactly that minimum edge — so every edge added is safe. |
| "How is this different from Dijkstra?" | The heap key. Dijkstra pushes `dist_so_far + weight` (cumulative from a source); Prim's pushes just `weight` (one hop into the tree). Dijkstra minimizes each node's distance from a source; Prim's minimizes the total edge weight. Structurally identical, semantically different. |
| "Can you get rid of the log factor?" | Yes — dense Prim's: keep `min_dist[j]` for every point, pick the minimum by linear scan, then relax all j against the newly added point. O(n²) time, O(n) space. |
| "What if some points are already connected for free?" | Seed union-find with those merges and run Kruskal's, or set those edge weights to 0. Kruskal's handles pre-existing components more naturally. |
| "Euclidean distance instead of Manhattan?" | Nothing changes — swap the formula. MST doesn't care which metric, only that weights are non-negative. (Though Euclidean MSTs admit an O(n log n) Delaunay-triangulation approach.) |
| "Why does `(0, 0)` as the seed not bias the answer?" | An MST's *total weight* is the same regardless of start point. Prim's is correct from any root. |

**Traps:**
- **Checking `visited` only on push, not on pop.** A point pushed twice before being visited would get counted twice. The pop-side `continue` is mandatory; the push-side check is only an optimization.
- Putting the index before the cost in the tuple — `(i, cost)` makes the heap order by index, silently returning nonsense.
- Building the tree by connecting each point to its own nearest neighbour. It's the tempting greedy and it produces disconnected clusters, not a spanning tree.
- Forgetting `abs()` and summing signed differences.
- Looping `while min_heap:` instead of `while len(visited) < n:` — it still terminates correctly, but it drains every stale entry after the tree is complete, doing pointless work.

**This same move shows up in:** [Network Delay Time](743-network-delay-time.md) (the same heap-driven expansion, but keyed on cumulative distance — Dijkstra rather than Prim's) · [Swim in Rising Water](778-swim-in-rising-water.md) (same skeleton again, keyed on path *maximum*) · [Redundant Connection](684-redundant-connection.md) (the union-find machinery Kruskal's would need) · [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (heap as a running "best so far").

</details>

---
