# 261. Graph Valid Tree

**Medium** · [LeetCode](https://leetcode.com/problems/graph-valid-tree/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You have a graph of `n` nodes labelled `0` to `n - 1`. Given `n` and a list of **undirected** edges, return `true` if these edges make up a **valid tree**.

```
n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]  →  true

      0 —— 1 —— 4
     / \
    2   3           connected, no cycles ✅

n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]  →  false
                              ↑ 1—2—3—1 is a cycle
```

**Constraints:** `1 <= n <= 2000` · `0 <= edges.length <= 5000` · no self-loops, no repeated edges

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

**What is a tree, precisely?** A connected, acyclic, undirected graph. Two conditions:

1. **Connected** — every node is reachable from every other.
2. **Acyclic** — no cycles.

| The statement says | Which really means |
|---|---|
| "**undirected** edges" | Each edge connects both ways — unlike [Course Schedule](207-course-schedule.md)'s directed graph |
| "valid **tree**" | Both conditions must hold |
| no self-loops or repeats | Simplifies the cycle detection |
| n up to 2000, edges up to 5000 | O(V + E) or near-linear expected |

**The counting fact that shortcuts everything.** A tree on `n` nodes has **exactly `n − 1` edges**. Why:

- **Fewer than n−1** → not enough edges to connect everything. Some component is isolated.
- **More than n−1** → too many; by the pigeonhole principle some edge closes a cycle.

So `len(edges) == n - 1` is a **necessary** condition — a free O(1) early exit.

⚠️ **But it isn't sufficient**, and that's the trap the problem is testing:

```
n = 4, edges = [[0,1],[1,0]... ]  — no, repeats are excluded. Better:

n = 4, edges = [[0,1],[1,2],[0,2]]     3 edges = n − 1 ✓
      0 —— 1
       \  /                    but node 3 is ISOLATED,
        2        3             and 0—1—2—0 is a CYCLE
```

Exactly n−1 edges, yet neither connected nor acyclic. **The count alone proves nothing** — you still need one of the two real checks.

**The key insight that makes one check enough.** Given exactly n−1 edges:

> **acyclic ⟺ connected**

If it's acyclic with n−1 edges it must be connected (a forest with k components has n−k edges, so k=1). And if it's connected with n−1 edges it must be acyclic. **So after the edge-count check, verifying *either* property confirms the other** — you only have to test one.

🤔 **Before you open the next section:** you need to detect whether adding an edge creates a cycle. What does it mean, in terms of connectivity, if an edge's two endpoints are *already* connected?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| DFS/BFS, count visited from node 0 | Check connectivity after the edge-count test | O(V + E) | ✅ Perfectly good |
| DFS tracking parents | Detect a cycle by revisiting a non-parent node | O(V + E) | ✅ Also standard |
| **Union-Find** | Reject any edge joining two already-connected nodes | **O(n·α(n))** | ✅ |

**The decision: edge-count check, then [union-find](../data-structures/union-find.md) to reject cycle-forming edges.**

The idea in one line:

> **An edge creates a cycle exactly when its two endpoints are already in the same component.**

If `a` and `b` are already connected, there's an existing path between them — so adding a direct edge closes a loop. Union-find answers "same component?" in near-constant time.

The algorithm:
1. `len(edges) != n - 1` → **`False`** immediately.
2. For each edge, try to `union` its endpoints. If they already share a root, that edge forms a cycle → **`False`**.
3. All unions succeeded → acyclic, and with n−1 edges that means connected → **`True`**.

**Union-find in two operations:**

| Operation | Meaning |
|---|---|
| **`find(x)`** | which component does x belong to? (its root) |
| **`union(x, y)`** | merge two components; return `False` if they were already the same |

**Path compression** is what makes `find` near-constant: while walking up to the root, each node is re-pointed closer to it, so later lookups are shorter. The line `parent[x] = parent[parent[x]]` points each node at its grandparent, flattening the tree as it goes.

**Why union-find fits so well here.** Cycle detection in an *undirected* graph is awkward with DFS — you must track the parent to avoid mistaking the edge you just came along for a cycle. Union-find has no such subtlety: **"already connected" is exactly the cycle condition**, with no bookkeeping.

**The DFS alternative** is equally valid: after the edge-count check, DFS from node 0 and confirm you visited all n nodes. Simpler if union-find isn't fresh in your mind — **say which you'd write and why.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(edges) != n - 1:
    return False
```

**The counting shortcut.** A tree has exactly n−1 edges — fewer can't connect everything, more must create a cycle.

O(1), and it's what lets the rest of the function check only *one* of the two tree properties.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
parent = list(range(n))
```

**Union-find initialization: every node is its own parent**, so each starts in its own component. `list(range(n))` gives `[0, 1, 2, …, n−1]`.
→ [union-find](../data-structures/union-find.md) · [range-function](../syntax/range-function.md) · [list-basics](../syntax/list-basics.md)

```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
```

**Find the component root** — walk up until a node is its own parent.

**The path-compression line is the optimization.** `parent[x] = parent[parent[x]]` re-points `x` at its grandparent, halving the path on every traversal. Over many calls the tree flattens to nearly depth 1, making `find` effectively O(1).

Without it, a degenerate chain would make each `find` O(n).
→ [while-loop](../syntax/while-loop.md) · [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
def union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x == root_y:
        return False
```

**The cycle test.** Same root ⇒ already connected ⇒ this edge closes a loop ⇒ report failure.

Returning a boolean rather than just merging is what lets the caller detect the cycle — the union *reports* whether it did anything.

```python
    parent[root_x] = root_y
    return True
```

**Merge the components** by pointing one root at the other, and report success.

*(A production implementation would also use union-by-rank — attaching the smaller tree under the larger — to keep trees shallow. Path compression alone is enough here.)*

```python
for a, b in edges:
    if not union(a, b):
        return False

return True
```

**Process every edge.** Any failed union means a cycle → not a tree.

**Reaching the end means acyclic** — and combined with the n−1 edge count, that guarantees connectivity too. So `True` without a separate connectivity check.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:

        if len(edges) != n - 1:
            return False

        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]   # path compression
                x = parent[x]
            return x

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return False
            parent[root_x] = root_y
            return True

        for a, b in edges:
            if not union(a, b):
                return False

        return True
```

</details>

**Trace it — the valid tree** — `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`:

`len(edges) = 4 == 5 − 1` ✓ — continue.

| Edge | `find(a)` | `find(b)` | Same? | Action | `parent` |
|---|---|---|---|---|---|
| start | | | | | `[0,1,2,3,4]` |
| `[0,1]` | 0 | 1 | no | merge | `[1,1,2,3,4]` |
| `[0,2]` | 1 | 2 | no | merge | `[1,2,2,3,4]` |
| `[0,3]` | 2 | 3 | no | merge | `[1,2,3,3,4]` |
| `[1,4]` | 3 | 4 | no | merge | `[1,2,3,4,4]` |

All unions succeeded → **`True`** ✅

**And the invalid case** — `n = 5`, `edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]`:

`len(edges) = 5`, but `n − 1 = 4` → **`False`** immediately, no union-find needed ✅

**The case where the count passes but the graph fails** — `n = 4`, `edges = [[0,1],[1,2],[0,2]]`:

`len(edges) = 3 == 4 − 1` ✓ — the count check passes.

| Edge | Roots | Same? | Result |
|---|---|---|---|
| `[0,1]` | 0, 1 | no | merge |
| `[1,2]` | 1, 2 | no | merge |
| `[0,2]` | **2, 2** | **yes** ⛔ | **cycle → `False`** ✅ |

This is exactly why the edge count alone isn't sufficient — three edges on four nodes, but they form a triangle and leave node 3 isolated.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · α(n)) ≈ O(n)</summary>

**O(n · α(n))**, where α is the **inverse Ackermann function** — effectively a constant below 5 for any conceivable input. So in practice **O(n)**.

| Step | Cost |
|---|---|
| Edge-count check | **O(1)** |
| Initialize `parent` | O(n) |
| n−1 unions, each two `find`s | **O(α(n))** amortized each |

**Why `find` is near-constant.** Path compression flattens the tree during every traversal — after a few operations, most nodes point directly at their root. The amortized cost over m operations is O(m·α(n)), and α(n) < 5 for n below the number of atoms in the universe. **Treat it as constant, but know the name.**

Without path compression, a degenerate chain makes each `find` O(n) and the total O(n²).

**The edge-count check is a genuine short-circuit.** Any input with the wrong number of edges — the majority of invalid cases — is rejected in O(1) without touching union-find.

**The DFS alternative is O(V + E)** — the same order. Union-find's advantage is elsewhere: it processes edges **incrementally**, so it handles edges arriving one at a time, which DFS cannot without re-running.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — just the `parent` array, one entry per node.

**Notably, no adjacency list is built.** DFS or BFS would need one, at O(V + E). Union-find works **directly on the edge list**, processing each edge as it comes and never materializing the graph structure.

| Approach | Space |
|---|---|
| DFS/BFS | **O(V + E)** — adjacency list + visited + recursion |
| **Union-Find** | **O(n)** — just `parent` |

That's a real advantage on edge-heavy graphs, and it's part of why union-find is the natural tool for **dynamic connectivity**: edges can be processed as a stream, with no graph to rebuild.

**No recursion**, so no stack-depth risk at n = 2000 — unlike the DFS approach, where a chain-shaped graph would need 2000 frames and exceed Python's default limit.
→ [recursion-limit](../syntax/recursion-limit.md)

**Union-by-rank** would add a second O(n) array to keep trees shallow. Path compression alone gives good enough behaviour here, and skipping it keeps the code shorter — worth mentioning as the standard companion optimization.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A tree is connected and acyclic. The useful counting fact is that a tree on n nodes has exactly n−1 edges — fewer can't connect everything, more must create a cycle — so that's a free O(1) early exit. But the count alone isn't sufficient: three edges on four nodes could be a triangle plus an isolated vertex. The key insight is that *given* exactly n−1 edges, acyclic and connected imply each other — so I only need to check one. I use union-find: an edge creates a cycle exactly when its endpoints are already in the same component, so I union each edge and fail if a union finds them already joined. Path compression makes find near-constant. O(n·α(n)) time, O(n) space — and notably no adjacency list, since union-find works straight off the edge list."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't the edge count sufficient?" | **The question.** `n=4, edges=[[0,1],[1,2],[0,2]]` has n−1 edges but is a triangle with an isolated node. |
| "Why does checking one property suffice?" | With exactly n−1 edges, acyclic ⟺ connected. A forest with k components has n−k edges, so acyclic + n−1 edges forces k = 1. |
| "Solve it with DFS." | After the edge-count check, DFS from node 0 and confirm all n nodes were visited. O(V + E), needs an adjacency list. |
| "Why is union-find good for undirected cycles?" | "Already connected" *is* the cycle condition. DFS needs parent-tracking to avoid mistaking the incoming edge for a cycle. |
| "What is path compression doing?" | Re-pointing nodes closer to the root during `find`, flattening the tree so later lookups are nearly O(1). |
| "What if edges arrived one at a time?" | Union-find shines — it's incremental. DFS would have to re-run from scratch each time. |
| "Count the components instead?" | Union everything, then count distinct roots — that's [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md). |

**Traps:**

- **Checking only the edge count** — the triangle-plus-isolated-node case passes it.
- **Checking only connectivity** without the edge count — a connected graph with extra edges has cycles and isn't a tree.
- **Omitting path compression** — correct but O(n²) on adversarial input.
- **Forgetting to `find` before comparing** — comparing `parent[x] == parent[y]` tests immediate parents, not roots.
- **Treating the graph as directed** and using [Course Schedule](207-course-schedule.md)'s indegree approach — undirected edges have no direction to count.
- **Off-by-one on `n - 1`** — a single node with zero edges is a valid tree.

**This same move shows up in:** [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md) (union-find counting components) · [Redundant Connection](684-redundant-connection.md) (finding the edge that *creates* the cycle) · [Number of Islands](200-number-of-islands.md) (connectivity, solved by flood-fill instead) · [union-find](../data-structures/union-find.md) · [12. Union-Find lesson](../learning/12-union-find.md).

</details>
