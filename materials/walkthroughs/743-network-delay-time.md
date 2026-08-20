# 743. Network Delay Time

**Medium** · [LeetCode](https://leetcode.com/problems/network-delay-time/)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. Advanced Graphs problems](../rmap-practice/13-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There are `n` network nodes labelled `1..n`. You're given `times`, where `times[i] = [u, v, w]` means a signal travels from `u` to `v` in `w` time. Send a signal from node `k`. Return the time it takes for **all** n nodes to receive it, or `-1` if some node never does.

```
times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2  →  2
        node 1 at t=1, node 3 at t=1, node 4 at t=2 — the slowest is 2

times = [[1,2,1]], n = 2, k = 2                  →  -1
        node 1 is unreachable from node 2 (edges are directed)
```

**Constraints:** `1 <= k <= n <= 100` · `1 <= times.length <= 6000` · `0 <= w <= 100` · all `(u, v)` pairs unique.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `[u, v, w]` triples | A **weighted, directed graph**. The weight is the thing that rules out plain BFS — BFS counts hops, and here hops have different costs |
| "a signal from `k`" | **Single source.** One starting node, and you care about every other node's distance from it |
| "the time for **all** nodes to receive it" | The signal spreads in parallel along every path at once, so each node receives at the earliest possible moment — its **shortest path** from `k`. The answer is the **maximum** of those shortest paths |
| `w >= 0` | No negative weights. That's the precondition for **Dijkstra's** — and worth saying out loud, because it's the one thing that would disqualify it |
| "`-1` if impossible" | Reachability check. If any node has no path from `k`, fail |
| `n <= 100`, `E <= 6000` | Small. Even O(V·E) Bellman-Ford would pass. Complexity isn't the constraint — correctness is |

The one sentence to arrive at: **compute the shortest path from `k` to every node, then return the largest one.** "How long until everyone has it" = "how long until the *last* person has it" = max over all shortest paths.

That reframing — a max over a set of minima — is the only conceptual step. Once you have it, the problem is a straight application.

🤔 **Before you open the next section:** why does BFS give the wrong answer here, when it's the correct shortest-path algorithm on an unweighted graph? What exactly does BFS assume that this problem breaks?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| BFS | Expand level by level from `k` | O(V + E) | O(V) | ❌ Minimizes **hop count**, not weight. A 1-hop edge of weight 50 beats a 3-hop path of weight 3 in BFS's eyes, and that's wrong |
| DFS over all paths | Enumerate every path, keep the min per node | O(V!) | O(V) | ❌ Exponential |
| [Bellman-Ford](../algorithms/bellman-ford.md) | Relax all E edges, V−1 times | O(V·E) | O(V) | ⚠️ Correct, and fast enough at this size — but it's the tool for *negative* weights, and using it here is bringing a heavier hammer than needed |
| [Floyd-Warshall](../algorithms/floyd-warshall.md) | All-pairs shortest paths | O(V³) | O(V²) | ⚠️ 10⁶ ops, passes — but computes n² answers when you asked for n |
| **[Dijkstra's](../algorithms/dijkstra.md)** | Repeatedly finalize the closest unfinalized node, relaxing its neighbours | O(E log V) | O(V + E) | ✅ |

**The decision:** [Dijkstra's algorithm](../algorithms/dijkstra.md) with a min-[heap](../data-structures/heap.md).

**Why BFS fails, precisely.** BFS is correct because of an assumption: *the first time you reach a node is via the fewest edges, and with uniform weights fewest-edges = cheapest.* Weights break the second half. Dijkstra's is the repair — it replaces "the queue naturally orders by hop count" with "**a priority queue explicitly orders by accumulated cost.**" Everything else about the traversal is identical. If every weight were 1, Dijkstra's would degenerate into exactly BFS.

**Why Dijkstra's is safe here:** non-negative weights. That's what guarantees the greedy step — once you pop a node, no cheaper route to it can appear later, because every remaining path costs at least what's already in the heap and extending it can only *add*. With a negative edge that guarantee dies, and you'd need Bellman-Ford.

**Why the answer is a max.** The signal doesn't travel one route at a time; it floods. Every node is lit at its own shortest-path time, and "all nodes have it" happens when the last one lights up.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
from collections import defaultdict
```
The heap gives you "cheapest pending node" in O(log V); the [defaultdict](../syntax/defaultdict.md) lets you append to `graph[u]` without pre-creating keys — which matters because sink nodes never appear as a source.
→ [heapq-module](../syntax/heapq-module.md) · [defaultdict](../syntax/defaultdict.md) · [from-import](../syntax/from-import.md)

```python
graph = defaultdict(list)
for u, v, w in times:
    graph[u].append((v, w))
```
The edge list becomes an **adjacency list**: `graph[u]` is every `(destination, weight)` reachable in one hop from `u`. Appending only `u → v` and not the reverse is what keeps the graph **directed**, which example 2 depends on.
→ [graph](../data-structures/graph.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-methods](../syntax/list-methods.md)

```python
dist = {}
min_heap = [(0, k)]   # (time so far, node)
```
`dist` is both the answer *and* the visited set — a node is in it exactly when its shortest time is **finalized**. Using one structure for both is the idiom worth internalizing.

The heap holds `(time, node)`, time first so tuple comparison orders by time. Seed it with `(0, k)`: the source is reachable at cost 0.
→ [dict-basics](../syntax/dict-basics.md) · [heap](../data-structures/heap.md)

```python
while min_heap:
    time, node = heapq.heappop(min_heap)
    if node in dist:
        continue
    dist[node] = time
```
The core. Pop the globally cheapest pending node — and **that popped value is final**. Nothing cheaper can arrive later, because everything still in the heap costs at least this much and all weights are ≥ 0. That's the greedy guarantee, and it's the sentence to say in an interview.

The `continue` is **lazy deletion**: a node can be pushed several times, once per inbound edge relaxed. You can't cheaply remove the stale entries from a heap, so you keep them and discard them on pop. The *first* pop of a node carries its smallest time, so every later copy is redundant.
→ [while-loop](../syntax/while-loop.md) · [membership-operators](../syntax/membership-operators.md) · [break-continue](../syntax/break-continue.md)

```python
    for neighbor, weight in graph[node]:
        if neighbor not in dist:
            heapq.heappush(min_heap, (time + weight, neighbor))
```
**Relaxation.** Having finalized `node` at `time`, every neighbour now has a candidate route costing `time + weight`. Push them all and let the heap sort out which is best.

`time + weight` is the line that separates this from Prim's MST, where you'd push just `weight`. **Dijkstra accumulates; Prim's does not** — same skeleton, different key, completely different meaning.
→ [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [dijkstra](../algorithms/dijkstra.md)

```python
if len(dist) != n:
    return -1
return max(dist.values())
```
Two questions, in order. Did everyone get it? `dist` only contains reachable nodes, so a short dict means someone was stranded → `-1`. Otherwise the answer is the slowest of the finalized times.
→ [dict-methods](../syntax/dict-methods.md) · [min-max-key](../syntax/min-max-key.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:

        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}
        min_heap = [(0, k)]   # (time so far, node)

        while min_heap:
            time, node = heapq.heappop(min_heap)
            if node in dist:
                continue
            dist[node] = time

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(min_heap, (time + weight, neighbor))

        if len(dist) != n:
            return -1
        return max(dist.values())
```
</details>

**Trace it** — `times = [[2,1,1],[2,3,1],[3,4,1]]`, `n = 4`, `k = 2`

Adjacency: `2 → [(1,1), (3,1)]`, `3 → [(4,1)]`

| Heap before pop | Popped | Stale? | `dist` after | Pushed |
|---|---|---|---|---|
| `[(0,2)]` | `(0, 2)` | no | `{2:0}` | `(1,1) (1,3)` |
| `[(1,1),(1,3)]` | `(1, 1)` | no | `{2:0, 1:1}` | — (node 1 has no outbound) |
| `[(1,3)]` | `(1, 3)` | no | `{2:0, 1:1, 3:1}` | `(2,4)` |
| `[(2,4)]` | `(2, 4)` | no | `{2:0, 1:1, 3:1, 4:2}` | — |

`len(dist) == 4 == n` ✅ → `max(0, 1, 1, 2)` = **2** ✅

Now example 2: `times = [[1,2,1]]`, `k = 2`. `graph[2]` is empty, so the first pop finalizes `dist = {2: 0}` and the heap empties. `len(dist) == 1 != 2` → **-1** ✅. Node 1 can reach node 2, but not the other way — the directed edge list is doing exactly what it should.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(E log V)</summary>

**O(E log V)**, where V = n and E = `len(times)`.

- Building the adjacency list: one pass over the edges → O(E).
- The `while` loop runs once per heap entry. Each relaxation pushes at most one entry, so the heap sees **at most E + 1 entries** overall.
- Each push and pop is O(log(heap size)). The heap holds at most E entries, and log E ≤ log V² = 2 log V, so each operation is **O(log V)**.
- Total: **O(E log V)**.

At n = 100 and E = 6000, that's roughly 6000 × 7 ≈ 4 × 10⁴ operations. Instant.

**The variant worth naming:** this is *lazy* Dijkstra's. The *eager* version uses a decrease-key operation to keep exactly one entry per node — with a Fibonacci heap that's **O(E + V log V)**, which is asymptotically better. Nobody writes it in an interview (Python has no decrease-key) but knowing the bound exists is a good signal.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E).**

- `graph` stores every edge exactly once → **O(V + E)**.
- `dist` holds at most one entry per node → O(V).
- `min_heap` holds up to one entry per relaxation → **O(E)**, because lazy deletion never removes stale entries early.

Sum: O(V + E), dominated by the adjacency list and the heap.

The eager variant would cut the heap to O(V), giving O(V + E) overall anyway — the adjacency list is the floor you can't get under.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The signal floods outward, so each node receives it at its shortest-path time from k, and 'all nodes have it' is the maximum of those. That makes this single-source shortest path on a weighted directed graph. BFS won't work because it minimizes hop count, not weight. All weights are non-negative, so Dijkstra's applies: a min-heap keyed on accumulated time, pop the cheapest pending node and finalize it — non-negative weights guarantee nothing cheaper can arrive later — then relax its neighbours. I use lazy deletion, skipping a node that's already finalized. At the end, if the distance map is smaller than n someone was unreachable, so -1; otherwise return the max. O(E log V) time, O(V + E) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if a weight could be negative?" | Dijkstra's breaks — the finalize-on-pop guarantee depends on weights never decreasing a path. Switch to [Bellman-Ford](../algorithms/bellman-ford.md): relax all edges V−1 times, O(V·E). It also detects negative cycles with one extra round. |
| "What if all weights were equal?" | Dijkstra's collapses into BFS. Use a plain [deque](../data-structures/deque.md) and drop the heap — O(V + E). |
| "Weights of only 0 and 1?" | **0-1 BFS**: a deque, appendleft for weight-0 edges and append for weight-1. O(V + E), no log factor. |
| "Shortest path between *all* pairs?" | [Floyd-Warshall](../algorithms/floyd-warshall.md), O(V³) — or run Dijkstra's from every node, O(V·E log V), which is better on sparse graphs. |
| "Return the actual path, not just the time?" | Keep a `parent[node]` map, set when you finalize a node, then walk back from the target and reverse. |
| "Why is this not Prim's? It looks identical." | The heap key. Prim's pushes `weight` (cost of one hop into the tree); Dijkstra's pushes `time + weight` (cumulative from the source). Same code shape, different quantity minimized. |
| "Can you exit early?" | For a single target, yes — return the moment you pop it. Here you need *every* node, so you must drain. |

**Traps:**
- **Skipping the `if node in dist: continue`.** Without it, a stale entry overwrites a node's finalized (smaller) time with a larger one. Silently wrong on graphs with multiple routes.
- Pushing `weight` instead of `time + weight` — you've written Prim's and computed a spanning tree cost.
- Forgetting the `len(dist) != n` check and returning `max()` over a partial map — you'd report success while a node never got the signal.
- Treating edges as undirected by also appending `graph[v].append((u, w))`. Example 2 exists specifically to catch this.
- Nodes are labelled `1..n`, not `0..n-1`. Off-by-one on any array-indexed variant.
- Calling `max()` on an empty `dist` raises `ValueError` — the `len` check happens to guard this too.

**This same move shows up in:** [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md) (identical heap skeleton, key is `weight` not `time + weight`) · [Swim in Rising Water](778-swim-in-rising-water.md) (same skeleton, key is `max(so_far, cell)` instead of a sum) · [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md) (where Dijkstra's *fails* and Bellman-Ford is required) · [Rotting Oranges](994-rotting-oranges.md) (the unweighted version — BFS levels are enough).

</details>

---
