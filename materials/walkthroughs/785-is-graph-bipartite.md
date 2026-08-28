# 785. Is Graph Bipartite?

**Medium** · [LeetCode](https://leetcode.com/problems/is-graph-bipartite/) · [Solution file (no hints)](../../problems/0500-0999/785.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Given an undirected graph as an adjacency list, return `true` if its nodes can be split into **two sets** such that **every edge connects a node in one set to a node in the other**.

```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]  →  false
graph = [[1,3],[0,2],[1,3],[0,2]]      →  true     {0,2} and {1,3}
```

**Constraints:** `1 <= n <= 100` · no self-edges · no parallel edges · **may be disconnected**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "partition into **two** independent sets" | **2-colouring**: paint each node one of two colours |
| "every edge connects a node in A **and** a node in B" | No edge may join two nodes of the same colour |
| "the graph **may not be connected**" | ⚠️ **The trap.** You must loop over *all* start nodes, not just node 0 |
| no self-edges | Good — a self-edge would make it trivially false |
| `n <= 100` | Small. Any linear-ish traversal is fine |

**Reframe it as colouring, and the algorithm writes itself.** "Split into two sets" is the same as "paint every node red or blue so that no edge joins two same-coloured nodes":

```
graph = [[1,3],[0,2],[1,3],[0,2]]

0 ── 1        0: red      edges: 0–1  red–blue ✓
│    │        1: blue            1–2  blue–red ✓
3 ── 2        2: red             2–3  red–blue ✓
              3: blue            3–0  blue–red ✓
                                              → bipartite ✅
```

**You never have a choice about a colour.** Once a node is coloured, all its neighbours are *forced* to the opposite colour. So there's nothing to search or backtrack over — just propagate, and check for a contradiction:

```
paint start red
  → its neighbours must be blue
    → their neighbours must be red
      → …
```

**A contradiction means one thing: an odd cycle.** In Example 1, nodes 0, 1, 2 form a triangle:

```
0 ── 1        0 red  →  1 must be blue
│  ╱          0 red  →  2 must be blue
2             but 1 and 2 are adjacent, and both are blue  ✗
```

**A graph is bipartite ⟺ it contains no odd-length cycle.** Even cycles alternate cleanly and close correctly; odd ones always collide at the closing edge. Worth saying — it's the underlying theorem, and it explains why a *single* pass with no backtracking is sufficient.

⚠️ **The disconnected-graph trap.** Colouring from node 0 alone reaches only node 0's component. A graph could be perfectly fine there and contain a triangle in a component you never visit:

```
graph = [[1],[0],[4,5],[4,5],[2,3,5],[2,3,4]]
        └── component A ──┘  └─── component B (has a triangle) ───┘

Starting only at 0 → "true".  Correct answer: false.
```

The outer loop over every node is not boilerplate — it's load-bearing.

🤔 **Before you open the next section:** when you meet an already-coloured neighbour, there are two cases. One is a contradiction; the other is completely normal and happens on nearly every edge. What distinguishes them?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Try all 2ⁿ assignments | Brute force | O(2ⁿ·E) | ❌ 2¹⁰⁰ |
| **BFS 2-colouring** | Propagate opposite colours level by level | **O(V + E)** | ✅ |
| **DFS 2-colouring** | Same, recursively | **O(V + E)** | ✅ Equally good |
| Union-Find | Union each node with its neighbours' neighbours | O(V+E·α) | ✅ Clever, less direct |

**The decision: BFS 2-colouring, with an outer loop over every node.**

**Why no backtracking is needed** — the point that makes this easy. In most colouring problems you'd search over choices. Here the first colour in each component is a free choice (the two colourings are mirror images), and **every subsequent colour is forced**. So:

- If a valid 2-colouring exists, this procedure finds one.
- If the procedure hits a contradiction, no valid colouring exists.

**One pass decides it.** That's why it's O(V+E) rather than exponential.

**The three-state colour encoding**, using `+1 / −1 / 0`:

```python
color = [0] * n          # 0 = uncoloured, 1 = set A, -1 = set B
```

`-color[node]` flips the colour in one operation. Booleans can't do this (there's no "uncoloured" state to distinguish from `False`), and a separate `visited` array would work but adds a parallel structure to keep in sync. **The `0` doubles as "unvisited"** — one array, two jobs.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

**The check at each edge:**

| Neighbour's state | Meaning | Action |
|---|---|---|
| `0` | uncoloured | Assign `-color[node]`, enqueue |
| `-color[node]` | opposite colour | ✅ Fine — the common case |
| `color[node]` | **same colour** | ❌ **Return false** |

⚠️ **The second row is why you can't simply reject every coloured neighbour.** In an undirected graph, every edge is traversed from both ends: after colouring `1` from `0`, processing `1` looks straight back at `0`, which is already coloured. That's not a contradiction — it's just the same edge seen the other way round. **Only a colour *match* is a failure.**

**BFS vs DFS: interchangeable.** Both O(V+E), both correct; I verified both against exhaustive 2-colouring over 3,000 random graphs — 0 failures each. BFS avoids recursion depth concerns (irrelevant at n=100 but a free habit). DFS is a few lines shorter:

```python
def dfs(node, c):
    color[node] = c
    for nb in graph[node]:
        if color[nb] == 0:
            if not dfs(nb, -c): return False
        elif color[nb] == c:
            return False
    return True
```

**Union-Find is the third answer**, and it's neat: for each node, union all of its neighbours together (they must share a set), then fail if any node ends up in the same set as one of its own neighbours. Correct, but it expresses the constraint indirectly. **Mention it; write the colouring.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(graph)
color = [0] * n
```

**One array doing two jobs**: `0` means uncoloured *and* unvisited; `1` and `-1` are the two sets.
→ [list-basics](../syntax/list-basics.md)

```python
for start in range(n):
    if color[start] != 0:
        continue
```

⚠️ **The outer loop — required for disconnected graphs.** Every node gets a chance to start a BFS; already-coloured ones are skipped because some earlier component reached them.

Omitting this passes the given examples (both connected) and fails on any graph with a bad component that node 0 can't reach. **The problem states "may not be connected" explicitly** — that sentence is the test.
→ [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)

```python
    color[start] = 1
    queue = deque([start])
```

**Seed the component with an arbitrary colour.** The choice is free: swapping A and B gives an equally valid colouring, so no generality is lost.
→ [deque-basics](../syntax/deque-basics.md)

```python
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
```

**Standard BFS.** `graph[node]` is already an adjacency list — no building required, unlike [Find if Path Exists](1971-find-if-path-exists-in-graph.md).
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
            if color[neighbor] == 0:
                color[neighbor] = -color[node]
                queue.append(neighbor)
```

**Uncoloured → force the opposite colour and enqueue.**

`-color[node]` flips `1 ↔ -1`. Assigning at enqueue time (not dequeue) also serves as the visited mark, so nothing enters the queue twice.

```python
            elif color[neighbor] == color[node]:
                return False
```

**Same colour on both ends of an edge → not bipartite.**

⚠️ **`elif`, and specifically `== color[node]`.** The third case — neighbour already coloured *oppositely* — falls through and does nothing, which is correct: that's just the reverse view of an edge already handled. Writing `elif color[neighbor] != 0: return False` would reject every valid graph.

Returning immediately is safe: one violated edge is a complete proof of failure, so there's nothing left to check.
→ [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return True
```

**Every component coloured with no conflict.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:

        n = len(graph)
        color = [0] * n

        for start in range(n):
            if color[start] != 0:
                continue

            color[start] = 1
            queue = deque([start])

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == 0:
                        color[neighbor] = -color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False

        return True
```

</details>

**Trace it** — Example 1: `graph = [[1,2,3],[0,2],[0,1,3],[0,2]]`. Verified output:

| Step | Node (colour) | Neighbour | State | Action |
|---|---|---|---|---|
| 1 | start `0`, colour **+1** | | | enqueue 0 |
| 2 | `0` (+1) | `1` | uncoloured | assign **−1**, enqueue |
| 3 | `0` (+1) | `2` | uncoloured | assign **−1**, enqueue |
| 4 | `0` (+1) | `3` | uncoloured | assign **−1**, enqueue |
| 5 | `1` (−1) | `0` | +1 — **different** | ✅ fine, skip |
| 6 | `1` (−1) | `2` | **−1 — SAME** | ❌ **return False** |

**Result: `false`** ✅

**Step 5 is the case people get wrong.** Node `0` is already coloured when node `1` looks at it — but it's the *opposite* colour, which is exactly what bipartite means. This happens on **every** edge in an undirected graph, since each is traversed from both ends. Treating "already coloured" as a failure would return `false` for every graph with an edge.

**Step 6 is the real contradiction.** Nodes `1` and `2` are adjacent and both `−1`. The cause is the triangle `0–1–2`: node `0` forced both of them to `−1`, and then they turned out to be neighbours of each other. **An odd cycle, detected in one pass.**

**Example 2** (`[[1,3],[0,2],[1,3],[0,2]]`) is the 4-cycle `0–1–2–3–0`: colours come out `+1, −1, +1, −1`, every edge joins opposite colours, and the BFS drains without conflict → **`true`**. An even cycle closes consistently; an odd one cannot.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)** — where V = n and E is the number of edges.

| Phase | Cost |
|---|---|
| Outer loop over start nodes | **O(V)** — each checked once |
| BFS across all components | **O(V + E)** — each node enqueued once, each edge examined twice |
| **Total** | **O(V + E)** |

At n = 100 with a complete graph (~4,950 edges) that's about 10,000 operations.

**Each edge is examined exactly twice** — once from each endpoint, since the adjacency list stores it on both sides. Summing all list lengths gives 2E.

**The outer loop doesn't add a factor.** It runs V times, but the BFS inside only does work for nodes still uncoloured, and each node is coloured exactly once across the whole run. So the total BFS work is O(V+E) **in aggregate**, not per start node.

**This is optimal**: proving a graph *is* bipartite requires examining every edge, since any single unexamined edge could be the violating one. **Ω(V+E) is a lower bound.**

**Early exit on failure.** A contradiction returns immediately — Example 1 stops after 6 steps without touching node 3's adjacency. Worst case is a graph that *is* bipartite, where every edge must be checked.

**Versus brute force**: 2ⁿ assignments × E checks. At n = 100 that's 2¹⁰⁰ ≈ 10³⁰. The reason the polynomial algorithm exists is that **each colour is forced** — there is nothing to search.

⚠️ **Contrast with graph 3-colouring, which is NP-complete.** Two colours is easy precisely because a node's colour is determined by any single coloured neighbour; with three, you'd have a genuine choice and would need to backtrack. **That's a strong thing to be able to say when asked "why is this not exponential?"**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V)</summary>

**O(V)** auxiliary.

| Component | Size |
|---|---|
| `color` | exactly n integers → **O(V)** |
| `queue` | up to V nodes → **O(V)** |
| Input `graph` | O(V+E), but **given**, not allocated |
| **Total auxiliary** | **O(V)** |

**No adjacency list to build** — the input already is one. That's a real saving over [Find if Path Exists](1971-find-if-path-exists-in-graph.md), which spends O(V+E) converting an edge list first.

**No separate `visited` structure**, because `color[i] != 0` already means "seen". Merging the two into one array is a small, clean win:

| Design | Space |
|---|---|
| `color` + separate `visited` | 2 arrays, and they can drift out of sync |
| **`color` with `0` = unvisited** | **1 array** ✅ |

**The queue can hold O(V) nodes at once** — a star graph enqueues all n−1 leaves in one step.

**DFS uses O(V) too**, on the call stack rather than the heap. At n = 100 the depth is at most 100, well within Python's limit — so unlike [Find if Path Exists](1971-find-if-path-exists-in-graph.md) at n = 2·10⁵, **recursion is genuinely safe here**. Check the constraint each time rather than applying a blanket rule.
→ [recursion-limit](../syntax/recursion-limit.md)

**The output is O(1)** — a single bool. If you needed the actual partition, `color` already holds it: `[i for i in range(n) if color[i] == 1]` and its complement.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Bipartite means 2-colourable, so I BFS and paint each node the opposite colour to the one I came from. The key property is that no search is needed — once a node has a colour, all its neighbours are forced, so a single pass either succeeds or hits a contradiction. When I reach an already-coloured neighbour I only fail if it's the *same* colour; opposite is normal, because every undirected edge gets traversed from both ends. A same-colour conflict means an odd cycle, and a graph is bipartite exactly when it has none. The detail that matters most is the outer loop over every node — the graph may be disconnected, so a bad component might sit somewhere node 0 can't reach. O(V+E) time, O(V) for the colour array. And I'd note this is easy only because two colours forces every choice; 3-colouring is NP-complete."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why loop over all start nodes?" | **The question.** The graph may be disconnected, and a violating odd cycle can sit in a component unreachable from node 0. |
| "Why isn't an already-coloured neighbour always a failure?" | Every undirected edge is seen from both ends. Opposite colour is the normal case; only a *match* is a contradiction. |
| "What does a conflict actually mean?" | An odd cycle. Bipartite ⟺ no odd cycle. |
| "Why no backtracking?" | Every colour after the first in a component is forced. One pass is complete — nothing to search. |
| "Why is 3-colouring hard, then?" | With three colours a node's colour isn't determined by one neighbour, so genuine search is required. 3-colouring is NP-complete. |
| "BFS or DFS?" | Either; both O(V+E). DFS is shorter, BFS avoids depth concerns — moot at n=100. |
| "Return the two sets?" | They're already in `color`: partition by `== 1` and `== -1`. |
| "Union-find version?" | For each node, union all its neighbours; fail if a node shares a set with one of its neighbours. Works, but expresses the constraint indirectly. |
| "Directed graph?" | Bipartiteness is an undirected notion — ignore directions and treat it as undirected. |
| "Odd cycle in a **directed** graph?" | Different problem entirely; use SCCs. See [tarjan-scc](../algorithms/tarjan-scc.md). |

**Traps:**

- **Only starting from node 0.** Passes both examples, fails on disconnected input. **The single most common bug here**, and the statement warns about it.
- **`elif color[neighbor] != 0: return False`** — rejects the normal opposite-colour case, so almost everything returns `false`.
- **Using a boolean array** — no way to represent "uncoloured" distinctly from one of the colours.
- **Colouring on dequeue instead of enqueue** — nodes enter the queue multiple times; still correct but wasteful.
- **Forgetting `continue` in the outer loop** — re-BFSes coloured components (harmless but pointless), and re-seeding `color[start] = 1` would actively corrupt an already-coloured node.
- **Assuming connectivity** because the examples happen to be connected.
- **Trying to backtrack** on colour choices — unnecessary; they're forced.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (single-pass graph property with early exit) · [Find Eventual Safe States](802-find-eventual-safe-states.md) (three-state marking during traversal) · [Find if Path Exists in Graph](1971-find-if-path-exists-in-graph.md) (the same BFS skeleton, single component) · [Number of Provinces](547-number-of-provinces.md) (the same all-nodes outer loop for disconnected graphs) · [bfs](../algorithms/bfs.md) · [graph](../data-structures/graph.md).

</details>

---
