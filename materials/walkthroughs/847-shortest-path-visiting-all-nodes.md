# 847. Shortest Path Visiting All Nodes

**Hard** · [LeetCode](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) · [Solution file (no hints)](../../problems/0500-0999/847.py)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Given a connected undirected graph, return the length of the **shortest walk visiting every node**. You may start and end anywhere, and revisit nodes and edges freely.

```
graph = [[1,2,3],[0],[0],[0]]        →  4      e.g. 1 → 0 → 2 → 0 → 3
graph = [[1],[0,2,4],[1,3,4],[2],[1,2]] →  4   e.g. 0 → 1 → 4 → 2 → 3
```

**Constraints:** `1 <= n <= 12` · connected · no self-loops

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**every** node" | A covering walk — related to Travelling Salesman, but with revisits allowed |
| "**start and stop at any node**" | ⚠️ No fixed source. BFS must be seeded from **all** nodes at once |
| "may **revisit** nodes, **reuse** edges" | It's a walk, not a path — so it always exists on a connected graph |
| "**shortest**" | Unweighted → BFS, not Dijkstra |
| `n <= 12` | ⚠️ **The giveaway.** 2¹² = 4096 → **bitmask over subsets** |

**Why plain BFS fails.** BFS on nodes alone answers "shortest path from A to B", where being at node `x` is the entire state. Here it isn't: arriving at node 0 having already seen `{0,1}` is a completely different situation from arriving at node 0 having seen `{0,1,2,3}` — one still has work to do, the other is finished.

> **The state isn't "where am I". It's "where am I, and what have I already visited".**

That's the central move, and once made, everything else is ordinary BFS:

```
state = (current node, set of visited nodes)

start states:  (0, {0}), (1, {1}), …, (n-1, {n-1})     ← any starting node
goal:          any state whose visited set is ALL nodes
```

**The visited set is a bitmask**, which is exactly what `n <= 12` is telling you:

```
n = 4

mask 0001 = {0}          mask 0101 = {0, 2}
mask 1111 = {0,1,2,3}  ← the goal, (1 << n) - 1
```

**How big is the state space?** `n` nodes × 2ⁿ masks = **12 × 4096 = 49,152** states. Tiny. **The constraint is naming the algorithm** — whenever you see n ≤ 20 on a graph problem, think "subset bitmask".

**Why BFS gives the right answer.** Every edge costs 1, so BFS explores states in non-decreasing distance order — the first time a full mask is reached, that distance is minimal. No weights, so no need for Dijkstra.

⚠️ **Revisiting nodes is allowed, and necessary.** In Example 1 (a star centred on node 0), any covering walk must pass through node 0 repeatedly — `1 → 0 → 2 → 0 → 3` visits node 0 three times. **The `(node, mask)` state handles this naturally**: revisiting node 0 with a *larger* mask is a genuinely new state, not a loop.

🤔 **Before you open the next section:** the answer allows starting anywhere. Rather than running BFS n times, one from each start, what could you put in the queue initially?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| BFS on nodes only | Ordinary shortest path | — | ❌ Wrong state; can't express "what's visited" |
| Try all n! orderings | Permutations + shortest paths between | O(n!·n) | ❌ 12! = 4.8·10⁸ |
| **BFS over `(node, mask)`** | Multi-source, bitmask state | **O(2ⁿ·n²)** | ✅ |
| Floyd–Warshall + Held–Karp DP | All-pairs, then TSP DP | O(2ⁿ·n²) | ✅ Same bound, more machinery |

**The decision: multi-source BFS over `(node, mask)` states.**

**The multi-source trick.** The walk may start anywhere, so rather than n separate BFS runs, **seed the queue with all n starting states at distance 0**:

```python
queue = deque((1 << i, i, 0) for i in range(n))
seen  = set((1 << i, i) for i in range(n))
```

**All n searches run simultaneously**, and because BFS explores by distance, the first full mask reached is the global minimum over all starting points. **One BFS instead of n** — and it isn't merely n times faster, it's *better*, because the searches share their `seen` set and stop duplicating work.

This is the same multi-source seeding as [Rotting Oranges](994-rotting-oranges.md) and [Walls and Gates](286-walls-and-gates.md), where every source is pushed at distance 0.

**Why `seen` must key on `(mask, node)`, not `node`:**

```
seen = {node}          ✗  node 0 is visited once and never revisited
                          → the star graph becomes unsolvable
seen = {(mask, node)}  ✅ revisiting node 0 with a bigger mask is a NEW state
```

**This is the single most important line in the solution.** Marking only nodes makes revisits impossible, and revisits are mandatory.

**The Held–Karp alternative** — the classic TSP DP:

```
1. Floyd–Warshall for all-pairs shortest paths          O(n³)
2. dp[mask][i] = min cost to visit `mask`, ending at i   O(2ⁿ·n²)
```

Same asymptotic bound and the more standard framing for TSP. **BFS is preferable here** because the graph is unweighted — the BFS *is* the shortest-path computation, so step 1 disappears. Mention Held–Karp as the weighted generalisation.

**Why not brute-force permutations:** 12! = 479 million orderings, and it's also *wrong* in spirit — an optimal walk may revisit nodes, so it isn't described by a permutation at all.

**A subtlety worth pre-empting: `n = 1`.** One node, already visited, answer **0**. The code below returns it via an explicit guard — otherwise the goal test (which only fires on *moving* to a new state) would never trigger, since there are no edges to traverse.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(graph)
if n == 1:
    return 0
```

**The single-node case.** Already complete at distance 0, and the main loop's goal test only fires when *moving*, so it needs its own guard.
→ [if-return](../syntax/if-return.md)

```python
full = (1 << n) - 1
```

**The goal mask** — n ones. For n = 4, `1 << 4` = `10000₂` = 16, minus 1 = `1111₂` = 15.

Reaching this mask means every node has been visited.
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
queue = deque((1 << i, i, 0) for i in range(n))
seen = set((1 << i, i) for i in range(n))
```

**Multi-source seeding: every node is a valid start**, each with only itself visited, at distance 0.

`1 << i` is the mask containing just node `i`. Because BFS proceeds by distance, running all n searches together still yields the global optimum.
→ [deque-basics](../syntax/deque-basics.md) · [generator-expressions](../syntax/generator-expressions.md) · [set-basics](../syntax/set-basics.md)

```python
while queue:
    mask, node, dist = queue.popleft()

    for nb in graph[node]:
        nmask = mask | (1 << nb)
```

**Move to a neighbour and add it to the visited set.**

`mask | (1 << nb)` sets `nb`'s bit. ⚠️ If `nb` was already visited the mask is **unchanged** — which is correct and is precisely what permits revisits: the state `(same mask, different node)` is still new and still explorable.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md)

```python
        if nmask == full:
            return dist + 1
```

**Goal test on generation, not on dequeue.** Safe here because all edges cost 1 — the first state to complete the mask does so at minimal distance, so returning early is correct and saves a queue round-trip.

⚠️ This is the opposite of the rule in [Path With Minimum Effort](1631-path-with-minimum-effort.md), where you must test on *pop*. The difference is that Dijkstra's frontier holds mixed distances, while BFS's holds at most two adjacent levels. **Know which regime you're in.**

```python
        if (nmask, nb) not in seen:
            seen.add((nmask, nb))
            queue.append((nmask, nb, dist + 1))
```

⚠️ **`seen` is keyed on the pair.** Keying on `nb` alone forbids revisiting a node with a richer mask and makes Example 1 unsolvable.

Marking at enqueue time keeps each state in the queue exactly once.
→ [membership-operators](../syntax/membership-operators.md)

```python
return 0
```

Unreachable on a connected graph; present so every path returns.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:

        n = len(graph)
        if n == 1:
            return 0

        full = (1 << n) - 1
        queue = deque((1 << i, i, 0) for i in range(n))
        seen = set((1 << i, i) for i in range(n))

        while queue:
            mask, node, dist = queue.popleft()

            for nb in graph[node]:
                nmask = mask | (1 << nb)
                if nmask == full:
                    return dist + 1
                if (nmask, nb) not in seen:
                    seen.add((nmask, nb))
                    queue.append((nmask, nb, dist + 1))

        return 0
```

</details>

**Trace it** — Example 1: `graph = [[1,2,3],[0],[0],[0]]`, a star centred on node 0. `full = 1111₂`. Verified output:

**Seeded queue** (all four starts, distance 0):

```
(mask=0001, node=0)   (mask=0010, node=1)   (mask=0100, node=2)   (mask=1000, node=3)
```

| Distance | Expansion | New state |
|---|---|---|
| 0→1 | from `(0001, 0)` → node 1 | `(0011, 1)` |
| 0→1 | from `(0001, 0)` → node 2 | `(0101, 2)` |
| 0→1 | from `(0001, 0)` → node 3 | `(1001, 3)` |
| 0→1 | from `(0010, 1)` → node 0 | `(0011, 0)` |
| 0→1 | from `(0100, 2)` → node 0 | `(0101, 0)` |
| 0→1 | from `(1000, 3)` → node 0 | `(1001, 0)` |
| 1→2 | from `(0011, 0)` → node 2 | `(0111, 2)` |
| 1→2 | from `(0011, 0)` → node 3 | `(1011, 3)` |
| 1→2 | from `(0101, 0)` → node 1 | `(0111, 1)` |
| 1→2 | from `(0101, 0)` → node 3 | `(1101, 3)` |
| 1→2 | from `(1001, 0)` → node 1 | `(1011, 1)` |
| 1→2 | from `(1001, 0)` → node 2 | `(1101, 2)` |
| 2→3 | from `(0111, 2)` → node 0 | `(0111, 0)` ⚠️ **mask unchanged** |
| 2→3 | from `(1011, 3)` → node 0 | `(1011, 0)` ⚠️ |
| 2→3 | from `(1101, 3)` → node 0 | `(1101, 0)` ⚠️ |
| 3→4 | from `(0111, 0)` → node 3 | mask becomes **1111 = full** → **return 4** ✅ |

**The three ⚠️ rows are why `seen` must key on the pair.** Each moves *back* to node 0 without changing the mask — node 0 was already visited. If `seen` held only nodes, these states would be rejected and the search would dead-end. **They're not wasted moves; they're the pivot through the hub**, and the final answer routes through one of them.

**Reading off the walk:** the winning state came from `(0111, 0)` at distance 3, which traces back to starting at node 1: `1 → 0 → 2 → 0 → 3`. **Four edges, node 0 visited three times** — exactly the walk the problem describes.

**Note the mask grows monotonically** — `mask | (1 << nb)` can only add bits. The search is a BFS over a lattice of subsets, moving strictly upward toward `full`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(2ⁿ · n²)</summary>

**O(2ⁿ · n²)**.

| Component | Count |
|---|---|
| States `(mask, node)` | 2ⁿ masks × n nodes = **2ⁿ·n** |
| Edges explored per state | up to n−1 neighbours → **O(n)** |
| **Total** | **O(2ⁿ · n²)** |

At n = 12: 4096 × 12 = **49,152 states**, each with ≤ 11 neighbours → about **540,000 operations**. Instant.

**Each state is expanded at most once** thanks to the `seen` set — that's what bounds the work, exactly as a `visited` set does in ordinary BFS.

**The exponent is unavoidable.** This is a Travelling-Salesman-style problem, which is **NP-hard**; there's no known polynomial algorithm. `n <= 12` exists because 2¹² is small, and **the right answer to "can you do better?" is a confident no** — 2ⁿ·n² is essentially the best known bound for exact TSP (Held–Karp, 1962).

| n | 2ⁿ·n² | n! (permutations) |
|---|---|---|
| 8 | 16,384 | 40,320 |
| 10 | 102,400 | 3,628,800 |
| **12** | **589,824** | **479,001,600** |
| 20 | 4.2·10⁸ | 2.4·10¹⁸ |

**At n = 12 the bitmask DP is ~800× faster than permutations**, and the gap grows explosively. Note also that permutations are *incorrect* here — optimal walks revisit nodes, so no permutation describes them.

**Why BFS and not Dijkstra:** all edges cost 1. BFS's level order already gives shortest distances, and it avoids the log factor. **Weighted edges would need Dijkstra over the same `(mask, node)` state space** — the state design is unchanged.

**Early return on generation** saves a level of expansion — worthwhile, and valid only because the graph is unweighted.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(2ⁿ · n)</summary>

**O(2ⁿ · n)**.

| Component | Size |
|---|---|
| `seen` | up to 2ⁿ·n states → **O(2ⁿ·n)** |
| `queue` | up to 2ⁿ·n states → **O(2ⁿ·n)** |
| **Total** | **O(2ⁿ·n)** |

At n = 12 that's up to 49,152 `(mask, node)` pairs in each — a few megabytes in Python. Comfortable.

**The `seen` set dominates**, and it's the price of correctness: without it the BFS revisits states endlessly, since the graph has cycles and walks may repeat.

**A tighter representation:** since masks are integers and nodes are small, `seen` can be a list of bitmasks, `seen[node]` being a set of masks — or a single `2ⁿ × n` boolean array. Same class, far smaller constant:

| Representation | Storage at n=12 |
|---|---|
| `set` of `(mask, node)` tuples | ~49k Python tuples — **heavy** |
| `[[False] * n for _ in range(1 << n)]` | 49k booleans — lighter |
| `seen[node]` as one big int bitmask | **12 integers** ✅ |

⚠️ **Space is what actually limits this algorithm, not time.** At n = 20 it's 2²⁰ × 20 ≈ 2·10⁷ states — still feasible; at n = 30 it's 3·10¹⁰ and hopeless. **The exponential memory is the practical ceiling on Held–Karp-style TSP**, which is worth saying when asked about scaling.

**No recursion** — iterative BFS throughout.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Plain BFS doesn't work because the state isn't just 'which node am I at' — arriving at a node having seen two others is different from arriving having seen all of them. So the state is the pair (current node, set of visited nodes), and with n ≤ 12 that set is a 12-bit mask, giving 4096 × 12 ≈ 49,000 states. Since the walk can start anywhere, I seed the queue with all n starting states at distance 0 — one multi-source BFS instead of n separate ones. Then it's ordinary BFS: move to a neighbour, OR its bit into the mask, and the first time the mask is complete, that distance is the answer, because unweighted edges mean BFS explores in distance order. The critical detail is that `seen` is keyed on the *pair*, not the node — revisiting a node with a larger mask is a genuinely new state, and in a star graph you *must* pass through the hub repeatedly. O(2ⁿ·n²) time and O(2ⁿ·n) space; that's TSP-class, it's NP-hard, and the n ≤ 12 bound is what makes the exponential affordable."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't the node alone a sufficient state?" | **The question.** Progress depends on what's been visited, not just position. The mask carries that. |
| "Why key `seen` on `(mask, node)`?" | Revisiting a node with more bits set is a new, useful state. Keying on the node alone makes the star graph unsolvable. |
| "Why multi-source seeding?" | The walk may start anywhere. Seeding all n starts at distance 0 runs every search at once and shares the `seen` set. |
| "Why BFS rather than Dijkstra?" | All edges cost 1. Weighted edges would need Dijkstra over the same state space — the state design doesn't change. |
| "Can you do better than exponential?" | **No.** This is TSP-class and NP-hard. 2ⁿ·n² is the Held–Karp bound and remains the best known. |
| "What's the largest feasible n?" | Around 20–22 before memory dominates. 2ⁿ·n *space* is the binding constraint, not time. |
| "Return the actual walk?" | Store a parent per `(mask, node)` state and walk back from the completed state. |
| "Must return to the start?" | That's the TSP cycle version — track the start node in the state too, multiplying the space by n. |
| "Relation to Held–Karp?" | The same DP. On a weighted graph you'd run Floyd–Warshall first, then `dp[mask][i]`; unweighted, the BFS subsumes both steps. |
| "Why can you return on generation, not pop?" | Unweighted BFS explores in distance order, so the first completed mask is minimal. In Dijkstra you'd have to wait for the pop. |

**Traps:**

- **Using `visited` on nodes only.** Forbids the revisits the problem explicitly allows — Example 1 becomes unsolvable. **The defining bug.**
- **Running n separate BFS searches** — correct but n× the work, and it misses the multi-source idea.
- **Forgetting the `n == 1` guard** — the goal test only fires on a move, and a single node has no edges, so it would fall through to `return 0` by accident rather than by design.
- **`1 << n - 1` instead of `(1 << n) - 1`** — operator precedence makes that `1 << (n-1)`, a single bit rather than n ones.
- **Trying permutations** — 12! is far too slow *and* wrong, since optimal walks revisit nodes.
- **Reaching for Dijkstra** — unnecessary on an unweighted graph; adds a log factor for nothing.
- **Storing the mask as a `frozenset`** — correct but far slower and heavier than an integer.

**This same move shows up in:** [Rotting Oranges](994-rotting-oranges.md) and [Walls and Gates](286-walls-and-gates.md) (multi-source BFS seeded at distance 0) · [Word Ladder](127-word-ladder.md) (BFS where the state is richer than a plain node) · [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) (bitmask over subsets with n ≤ 16) · [Cheapest Flights Within K Stops](787-cheapest-flights-within-k-stops.md) (shortest path over an augmented state) · [bfs](../algorithms/bfs.md) · [bitwise-operators](../syntax/bitwise-operators.md) · [graph](../data-structures/graph.md).

</details>

---
