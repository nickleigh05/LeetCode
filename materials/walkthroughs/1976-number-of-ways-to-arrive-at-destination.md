# 1976. Number of Ways to Arrive at Destination

**Medium** · [LeetCode](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) · [Solution file (no hints)](../../problems/1500-1999/1976.py)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Given `n` intersections and bidirectional weighted `roads`, count the number of ways to travel from `0` to `n-1` **in the shortest possible time**. Return it modulo `10^9 + 7`.

```
n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],
                [3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]   →  4

Shortest time is 7 minutes, achieved by:  0→6 · 0→4→6 · 0→1→2→5→6 · 0→1→3→5→6
```

**Constraints:** `1 <= n <= 200` · `1 <= time_i <= 10^9` · graph is connected, at most one road per pair

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| weighted roads, "**shortest** amount of time" | Dijkstra — positive weights, so no Bellman–Ford needed |
| "in **how many ways**" | ⚠️ **Count paths**, not just find one. A second array rides alongside `dist` |
| "modulo 10⁹ + 7" | The count can be astronomically large; the distances are **not** reduced |
| `time_i <= 10^9`, `n <= 200` | ⚠️ Total distance can reach ~2·10¹¹ — **needs 64-bit**, fine in Python |
| bidirectional | Add both directions |
| "you can reach any intersection from any other" | Connected — no unreachable-destination case |

**Two things travel together.** Dijkstra normally answers "how far?"; here you also need "how many optimal routes get me there?" The insight is that **both can be computed in the same pass**, because the number of shortest paths to a node is determined entirely by its shortest-path predecessors:

```
ways[v] = sum of ways[u]  over every u that lies on a shortest path into v
```

So carry a parallel array and update it during relaxation. **No second traversal, no path enumeration.**

**The three cases at every edge `u → v`**, and this is the entire algorithm:

```
nd = dist[u] + time(u,v)

nd <  dist[v]   →  found a strictly better route.
                   dist[v] = nd,  ways[v] = ways[u]      ← OVERWRITE, don't add
nd == dist[v]   →  found another equally good route.
                   ways[v] += ways[u]                     ← ACCUMULATE
nd >  dist[v]   →  worse. Ignore entirely.
```

⚠️ **The first case must overwrite, not accumulate.** Every route counted so far reached `v` more slowly and is now obsolete — those paths are no longer shortest paths. Writing `ways[v] += ways[u]` there is the classic bug and produces inflated counts.

**Why the counts compose by addition.** If `v` sits at the same shortest distance via several predecessors, every shortest path to `v` is (a shortest path to some predecessor `u`) + (the edge `u→v`). Those sets are disjoint — they differ in their final edge — so the totals simply add:

```
node 5 is reached at time 6 via node 2 (1 way) and via node 3 (1 way)  →  ways[5] = 2
node 6 is reached at time 7 via node 0 (1), node 4 (1), node 5 (2)     →  ways[6] = 4 ✅
```

That's Example 1 exactly, and it shows the counts **propagating and compounding** — node 5's 2 flows into node 6.

🤔 **Before you open the next section:** Dijkstra finalises a node when it's popped. Why does that guarantee `ways[u]` is complete at the moment you use it to update a neighbour?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Enumerate all paths, keep the shortest | DFS every route | exponential | ❌ |
| Dijkstra, then count on the shortest-path DAG | Two passes | O(E log V + V + E) | ✅ Correct, more code |
| **Dijkstra carrying a `ways` array** | One pass, both answers | **O(E log V)** | ✅ |
| Bellman–Ford with counts | Relax V−1 times | O(V·E) | ⚠️ Works; unnecessary with positive weights |
| Floyd–Warshall with counts | All pairs | O(V³) | ⚠️ 8·10⁶ at n=200 — passes, but overkill |

**The decision: Dijkstra with a parallel `ways` array.**

**Why one pass is enough — the correctness argument.** Dijkstra's invariant is that **when a node is popped, its distance is final**. The extension needed here is that its *count* is final too, and it follows from the same ordering:

- Every predecessor `u` on a shortest path to `v` satisfies `dist[u] < dist[v]` (weights are strictly positive).
- Dijkstra pops in non-decreasing distance order.
- So **every** such `u` is popped, and has contributed to `ways[v]`, before `v` itself is popped.

**This is where the `time_i >= 1` constraint earns its keep.** With zero-weight edges, `dist[u] == dist[v]` becomes possible and a predecessor might be popped *after* `v` — leaving the count incomplete. Positive weights rule that out. **Worth saying explicitly**; it's the kind of detail that separates recital from understanding.

**The two-pass alternative** — run plain Dijkstra, then build the shortest-path DAG (keep edge `u→v` iff `dist[u] + w == dist[v]`) and count paths through it with a topological DP. Equally correct, and a good answer to "what if weights could be zero?", since the DAG construction doesn't depend on pop order. It's just more code for the same result.

**The modulus, and where it does and doesn't go:**

```python
MOD = 10 ** 9 + 7
ways[v] = (ways[v] + ways[u]) % MOD      # ✅ counts are reduced
dist[v] = dist[u] + time                  # ❌ NEVER reduce distances
```

⚠️ **Reducing distances mod anything destroys the comparisons** — a huge distance could wrap to a small residue and be wrongly preferred. Only the *counts* are modular. The distances stay exact (Python integers are arbitrary-precision; in C++ you'd need `long long`, since 200 edges × 10⁹ ≈ 2·10¹¹ overflows 32 bits).

**A subtle consequence of the modulus:** `ways[v]` can be reduced to a small number or even 0 while the true count is enormous. That's fine — you never *compare* counts, only sum them. If you were tempted to write `if ways[v] == 0`, that would be a bug.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
MOD = 10 ** 9 + 7

adj = defaultdict(list)
for u, v, t in roads:
    adj[u].append((v, t))
    adj[v].append((u, t))
```

**Undirected — both directions.** Roads are bidirectional; adding one direction silently makes half the graph unreachable.
→ [defaultdict](../syntax/defaultdict.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
dist = [float('inf')] * n
ways = [0] * n
dist[0] = 0
ways[0] = 1
```

**The two parallel arrays.**

⚠️ **`ways[0] = 1` is the base case that makes everything work**: there is exactly one way to be at the start — do nothing. Leaving it at 0 makes every count zero, since all sums trace back to this seed.
→ [float-inf](../syntax/float-inf.md) · [list-basics](../syntax/list-basics.md)

```python
heap = [(0, 0)]

while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]:
        continue
```

**Standard Dijkstra with the stale-entry check.** `(distance, node)` — distance first so the heap orders by it.

The `continue` discards outdated entries left behind by improvements, since `heapq` has no decrease-key.
→ [heapq-module](../syntax/heapq-module.md) · [while-loop](../syntax/while-loop.md)

```python
    for nb, t in adj[node]:
        nd = d + t
```

**Candidate distance to the neighbour.** ⚠️ Note `d + t` with **no modulus** — distances must stay exact and comparable.

```python
        if nd < dist[nb]:
            dist[nb] = nd
            ways[nb] = ways[node]
            heapq.heappush(heap, (nd, nb))
```

**Strictly better route → overwrite both.**

⚠️ `ways[nb] = ways[node]` — an **assignment**, not `+=`. Everything previously counted for `nb` took longer and is no longer a shortest path. This is the single most important line in the problem.

```python
        elif nd == dist[nb]:
            ways[nb] = (ways[nb] + ways[node]) % MOD
```

**Equally good route → accumulate**, under the modulus.

**No push here** — `nb` is already in the heap (or already finalised) at this exact distance, so re-pushing would only duplicate work. Only a *strict* improvement warrants a push.
→ [elif-else](../syntax/elif-else.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
return ways[n - 1] % MOD
```

The final `% MOD` is belt-and-braces — the accumulation already reduces.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:

        MOD = 10 ** 9 + 7

        adj = defaultdict(list)
        for u, v, t in roads:
            adj[u].append((v, t))
            adj[v].append((u, t))

        dist = [float('inf')] * n
        ways = [0] * n
        dist[0] = 0
        ways[0] = 1

        heap = [(0, 0)]

        while heap:
            d, node = heapq.heappop(heap)
            if d > dist[node]:
                continue

            for nb, t in adj[node]:
                nd = d + t
                if nd < dist[nb]:
                    dist[nb] = nd
                    ways[nb] = ways[node]
                    heapq.heappush(heap, (nd, nb))
                elif nd == dist[nb]:
                    ways[nb] = (ways[nb] + ways[node]) % MOD

        return ways[n - 1] % MOD
```

</details>

**Trace it** — Example 1, `n = 7`. Verified output:

| Pop | `d` | Relaxations |
|---|---|---|
| `0` | 0 | `6`: **new** best 7, ways=1 · `1`: **new** best 2, ways=1 · `4`: **new** best 5, ways=1 |
| `1` | 2 | `2`: **new** best 5, ways=1 · `3`: **new** best 5, ways=1 |
| `2` | 5 | `5`: **new** best 6, ways=1 |
| `3` | 5 | `5`: **TIE** at 6 → ways += 1 → **2** ⚠️ |
| `4` | 5 | `6`: **TIE** at 7 → ways += 1 → **2** ⚠️ |
| `5` | 6 | `6`: **TIE** at 7 → ways += 2 → **4** ⚠️ |
| `6` | 7 | — |

```
dist = [0, 2, 5, 5, 5, 6, 7]
ways = [1, 1, 1, 1, 1, 2, 4]        →  answer ways[6] = 4 ✅
```

**The three ⚠️ rows are the entire mechanism** — every one is the `elif` branch firing.

**The compounding is the part to internalise.** At the row popping node `5`, its own `ways` is already **2** (accumulated from nodes 2 and 3), and all of that flows into node 6 in a single `+= 2`. **The count multiplies through the graph without ever enumerating a path.** Node 6 ends at 1 + 1 + 2 = 4, matching the four routes the problem lists.

**Why node 5 is popped before node 6** matters: `dist[5] = 6 < dist[6] = 7`, so by the time node 6 is finalised, every contribution to it has landed. That's the pop-order argument, visible in miniature.

**Note node 6 was first assigned ways=1 on the very first row** (via the direct road `0→6`, time 7), then received two more contributions. Had that first assignment been `+=` on an `inf` distance, nothing would break — but if a *shorter* route to 6 had later appeared, `=` is what correctly discards those 3 obsolete ways.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(E log V)</summary>

**O(E log V)** — plain Dijkstra; the counting adds nothing asymptotically.

| Component | Cost |
|---|---|
| Build adjacency list | **O(E)** |
| Each edge relaxed | **O(E)** total |
| Each heap push/pop | **O(log V)** |
| **Total** | **O(E log V)** |

At n = 200, E can be `n(n−1)/2` = 19,900, so ≈ 19,900 × log₂(200) ≈ **1.5·10⁵ operations**. Trivial.

**The `ways` array costs O(1) per relaxation** — one comparison and either an assignment or an addition. **Counting shortest paths is asymptotically free** given that you're running Dijkstra anyway, which is the appealing part of this problem.

**Why not Floyd–Warshall**, which also handles it: O(V³) = 8·10⁶ at n=200. It would pass, but it computes all 40,000 pairs when one is wanted.

**Why not Bellman–Ford:** O(V·E) = 200 × 19,900 ≈ 4·10⁶. Also passes, but it's the tool for *negative* weights, and here all weights are ≥ 1.

**Why not enumerate paths:** the count itself can exceed 10⁹ (hence the modulus), so listing them is hopeless by definition. **The modulus is the problem telling you not to enumerate.**

⚠️ **The `>` in the stale check must not be `>=`.** With `>=`, the first (valid) pop of a node whose `d` equals `dist[node]` would be skipped and its neighbours never relaxed.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E)**.

| Component | Size |
|---|---|
| Adjacency list | 2E entries → **O(E)** |
| `dist` | n values → **O(V)** |
| `ways` | n values → **O(V)** |
| Heap | up to O(E) entries (stale included) → **O(E)** |
| **Total** | **O(V + E)** |

At n = 200 with a complete graph: ~40,000 adjacency entries, two 200-element arrays, and a heap bounded by the push count.

**The `ways` array is only O(V)** — one integer per node, kept small by the modulus. **Counting paths costs a single extra array**, not storage proportional to the number of paths (which can exceed 10⁹). That contrast is the space story:

| What you store | Size |
|---|---|
| The paths themselves | ⚠️ up to 10⁹⁺ — impossible |
| **A count per node** | **O(V)** ✅ |

**The heap holds pushes, not nodes** — each improvement adds an entry without removing the old one, so it's bounded by O(E) rather than O(V). Standard for `heapq`-based Dijkstra.

**Note the `elif` branch never pushes**, which meaningfully limits heap growth: equal-distance discoveries update the count in place. Pushing there would be correct but would add an entry per tie.

**No recursion** — iterative throughout, so no stack-depth concern.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's Dijkstra with a second array riding alongside `dist` that counts shortest paths. At each edge relaxation there are three cases: if I find a strictly shorter route I overwrite both the distance and the count — the previously counted paths are no longer shortest, so it's an assignment, not an addition. If I find an equally short route I add the predecessor's count to the node's. Anything longer I ignore. The base case is `ways[0] = 1`, one way to be at the start. This works in a single pass because Dijkstra pops in non-decreasing distance order and all weights are at least 1, so every predecessor on a shortest path to a node is strictly closer and therefore already finalised when the node is popped. Counts are taken mod 1e9+7, but distances never are — reducing those would break the comparisons. O(E log V), and the counting is asymptotically free."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why overwrite instead of `+=` on a shorter route?" | **The question.** The old paths are no longer shortest paths, so their count is obsolete. `+=` inflates the answer. |
| "Why is one pass enough?" | Dijkstra pops in non-decreasing distance order, and weights are ≥ 1, so every shortest-path predecessor is strictly closer and already final. |
| "What if a weight could be **0**?" | The pop-order argument breaks — a predecessor could be popped after the node. Do two passes: Dijkstra, then count over the shortest-path DAG. |
| "Why not reduce `dist` mod 1e9+7?" | It destroys ordering: a large distance could wrap small and be wrongly preferred. Only counts are modular. |
| "Overflow?" | Fine in Python. In C++/Java, 200 edges × 10⁹ ≈ 2·10¹¹ needs `long long`. |
| "Negative weights?" | Dijkstra is invalid. Bellman–Ford with the same three-case counting, provided there's no negative cycle. |
| "Count paths within `k` of the shortest?" | Much harder — Eppstein's k-shortest-paths, or a state-expanded Dijkstra over (node, slack). |
| "Return one actual shortest path?" | Track a parent per node on each strict improvement and walk back. |
| "Why can't you just enumerate paths?" | The count can exceed 10⁹ — the modulus is the problem saying so. |

**Traps:**

- **`ways[nb] += ways[node]` in the strict-improvement branch.** Counts obsolete paths. **The defining bug.**
- **Forgetting `ways[0] = 1`** — everything sums from zero and the answer is 0.
- **Reducing distances mod 1e9+7** — breaks all comparisons.
- **Adding only one direction** to the adjacency list — roads are bidirectional.
- **Pushing in the `elif` branch** — correct but adds a heap entry per tie for no benefit.
- **Using `>=` in the stale check** — skips the first legitimate pop of each node.
- **Forgetting the modulus in the accumulation** — the number grows unboundedly (correct in Python, but not what's asked, and it overflows elsewhere).
- **Comparing counts against 0** — a valid count can be ≡ 0 under the modulus.

**This same move shows up in:** [Network Delay Time](743-network-delay-time.md) (plain Dijkstra, the base this extends) · [Path With Minimum Effort](1631-path-with-minimum-effort.md) (Dijkstra with a different relaxation rule) · [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md) (shortest paths under an extra constraint) · [Unique Paths](62-unique-paths.md) (counting paths by summing predecessors, on a grid DAG) · [dijkstra](../algorithms/dijkstra.md) · [modular-arithmetic](../algorithms/modular-arithmetic.md) · [graph](../data-structures/graph.md).

</details>

---
