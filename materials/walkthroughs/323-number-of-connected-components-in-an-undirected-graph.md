# 323. Number of Connected Components in an Undirected Graph

**Medium** · [LeetCode](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) · [Solution file (no hints)](../../problems/0001-0499/323.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

You have a graph of `n` nodes labelled `0` to `n - 1`. Given `n` and a list of **undirected** edges, return **the number of connected components** in the graph.

```
n = 5, edges = [[0,1],[1,2],[3,4]]  →  2

   0 —— 1 —— 2        3 —— 4
   └── component 1 ──┘  └ comp 2 ┘

n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]  →  1
```

**Constraints:** `1 <= n <= 2000` · `0 <= edges.length <= 5000` · no self-loops, no repeated edges

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**connected components**" | Maximal groups where every node reaches every other — the same question as [Number of Islands](200-number-of-islands.md), on an explicit graph |
| "**undirected**" | Each edge works both ways, so it must be added to **both** nodes' adjacency lists |
| nodes labelled `0` to `n−1` | Convenient — you can index arrays directly by node id |
| edges may be **empty** | Then every node is its own component → answer is `n` |
| isolated nodes exist | ⚠️ A node with no edges is still a component. You must iterate over **all** n nodes, not just those appearing in edges |

**This is [Number of Islands](200-number-of-islands.md) with an explicit graph.** There, the graph was implicit — cells and their orthogonal neighbours. Here it's given as an edge list, but the counting logic is identical:

1. Scan every node.
2. When you find an **unvisited** one, you've discovered a **new component** — increment.
3. **Flood-fill** everything reachable from it, marking all as visited.
4. Continue scanning.

> **Each component is counted exactly once — at whichever of its nodes the scan reaches first.** Every other node in it gets marked during the flood-fill and skipped.

**The one setup step that's new.** An edge list isn't traversable — given node 3, you can't ask "who are my neighbours?" without scanning all edges. So you first build an **adjacency list**:

```
edges [[0,1],[1,2],[3,4]]   →   graph[0] = [1]
                                graph[1] = [0, 2]
                                graph[2] = [1]
                                graph[3] = [4]
                                graph[4] = [3]
```

⚠️ **Because the graph is undirected, each edge appears twice** — once in each endpoint's list. Adding it only one way silently makes the graph directed, and components split incorrectly.

🤔 **Before you open the next section:** if you only iterated over nodes mentioned in `edges`, what would you get wrong on `n = 5, edges = [[0,1]]`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| For each pair, test reachability | Check if every pair is connected | O(V²·(V+E)) | ❌ Hopeless |
| **DFS/BFS from each unvisited node** | Flood-fill, count starts | **O(V + E)** | ✅ |
| [Union-Find](../data-structures/union-find.md) | Union every edge; count distinct roots | O(V + E·α) | ✅ Equally good, and better for dynamic edges |

**The decision: build an adjacency list, then DFS from every unvisited node, counting how many times you start.**

**The counting mechanism is the whole idea.** You don't count nodes or edges — you count **how many times you had to start a fresh traversal**. Each start means you found a node unreachable from everything seen so far, which is exactly a new component.

**Union-find is an equally standard answer**, and worth naming:

```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

count = n                      # start with every node isolated
for a, b in edges:
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb
        count -= 1             # two components merged into one
return count
```

**A neat framing:** start at `n` components and decrement each time an edge merges two. It needs no adjacency list and processes edges as a stream — the same advantage noted in [Graph Valid Tree](261-graph-valid-tree.md).

| | DFS | Union-Find |
|---|---|---|
| Needs adjacency list | **yes** — O(V + E) | no |
| Handles streaming edges | no | **yes** |
| Recursion depth risk | **yes** at V = 2000 | no |

**Why marking happens on *entry* here.** Look closely: `dfs` marks each **neighbour** before recursing, and the outer loop marks the start node itself. That's slightly unusual — most flood-fills mark at the top of the function. Both work; this version simply never calls `dfs` on an already-visited node, so the check lives at the call sites.

**Why the marking is permanent**, as in every graph traversal: you're computing reachability, not exploring alternative paths. No backtracking.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
graph = [[] for _ in range(n)]
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)
```

**Build the adjacency list — both directions.** The graph is undirected, so each edge is recorded in both endpoints' lists.

⚠️ Adding only `graph[a].append(b)` would make it directed, and a component reachable only "backwards" would be miscounted.

⚠️ `[[] for _ in range(n)]` — the comprehension is required. `[[]] * n` creates n references to *one* list, so every node would share the same neighbours.
→ [list-comprehension](../syntax/list-comprehension.md) · [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [graph](../data-structures/graph.md)

```python
visited = set()

def dfs(node):
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            dfs(neighbor)
```

**The flood-fill.** For each neighbour not yet seen, mark it and recurse.

Marking **before** recursing is what prevents infinite recursion — without it, two adjacent nodes would call each other forever, since every edge is bidirectional.

Note the check and the mark happen **at the call site** rather than at the top of `dfs`. That means `dfs` is only ever called on nodes already marked — a valid variant, just slightly different from the [Number of Islands](200-number-of-islands.md) style.
→ [set-basics](../syntax/set-basics.md) · [membership-operators](../syntax/membership-operators.md) · [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md)

```python
count = 0
for i in range(n):
    if i not in visited:
        visited.add(i)
        dfs(i)
        count += 1
```

**The counting scan — and the heart of the solution.**

Iterating `range(n)` covers **every** node, including isolated ones that never appear in `edges`. That's essential: a node with no edges is still a component.

Finding an unvisited node means it's unreachable from everything explored so far ⇒ **a new component**. Mark it, flood-fill its whole component, and increment.

`visited.add(i)` before the call keeps the invariant that `dfs` is only entered on marked nodes.
→ [range-function](../syntax/range-function.md) · [if-return](../syntax/if-return.md)

```python
return count
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:

        graph = [[] for _ in range(n)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        visited = set()

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor)

        count = 0
        for i in range(n):
            if i not in visited:
                visited.add(i)
                dfs(i)
                count += 1

        return count
```

</details>

**Trace it** — `n = 5`, `edges = [[0,1],[1,2],[3,4]]`:

```
adjacency:  0 → [1]
            1 → [0, 2]
            2 → [1]
            3 → [4]
            4 → [3]
```

| Scan | Visited? | Action | `visited` after | `count` |
|---|---|---|---|---|
| 0 | no | **new component** → DFS reaches 1, then 2 | `{0,1,2}` | **1** |
| 1 | **yes** | skip | | 1 |
| 2 | **yes** | skip | | 1 |
| 3 | no | **new component** → DFS reaches 4 | `{0,1,2,3,4}` | **2** |
| 4 | **yes** | skip | | 2 |

Answer: **2** ✅

**And an isolated node** — `n = 5`, `edges = [[0,1]]`:

| Scan | Action | `count` |
|---|---|---|
| 0 | new component → reaches 1 | **1** |
| 1 | skip (visited) | 1 |
| 2 | **new component** (no edges) | **2** |
| 3 | **new component** | **3** |
| 4 | **new component** | **4** |

Answer: **4** ✅

Nodes 2, 3 and 4 appear in no edge at all — which is exactly why the scan iterates `range(n)` rather than the nodes mentioned in `edges`. **Iterating only over edge endpoints would return 1.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)**, where V = n and E = `len(edges)`.

| Step | Cost |
|---|---|
| Build the adjacency list | O(V + E) — allocate V lists, append 2E entries |
| Outer scan | O(V) — one `in visited` check per node |
| All DFS calls combined | each node visited once, each edge traversed twice → **O(V + E)** |

**O(V + E)** total. At 2000 nodes and 5000 edges, ~12,000 operations.

**Every node enters `visited` exactly once**, so it can start at most one DFS. Every edge is examined from both endpoints — hence the factor of 2, absorbed into O(E).

**The nested loops aren't quadratic**, for the same reason as [Number of Islands](200-number-of-islands.md): the flood-fills are bounded in total by the graph size, not multiplied by the scan.

**Versus checking every pair for reachability:** O(V²) pairs × O(V + E) per check — completely impractical.

**Union-find is O(V + E·α(n))** — effectively the same, with a smaller constant on the traversal but the cost of the `find` operations. Neither dominates; pick based on whether edges arrive dynamically.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E)**.

| Component | Size |
|---|---|
| `graph` adjacency list | V lists + 2E entries → **O(V + E)** |
| `visited` set | up to V nodes → O(V) |
| Recursion stack | ⚠️ up to V frames on a chain → **O(V)** |

⚠️ **The recursion depth is a real risk at n = 2000.** A path-shaped graph `0—1—2—…—1999` makes the DFS 2000 frames deep, **exceeding Python's default limit of 1000** → `RecursionError`.

Two fixes worth naming:

**BFS** — swap the recursion for a queue:
```python
from collections import deque
queue = deque([i])
while queue:
    node = queue.popleft()
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei); queue.append(nei)
```

**Union-find** — no traversal at all, so **no adjacency list and no recursion**:

| Approach | Space |
|---|---|
| DFS | **O(V + E)** — adjacency list + visited + stack |
| BFS | O(V + E) — adjacency list + visited + queue |
| **Union-Find** | **O(V)** — just the `parent` array |

Union-find is the leanest here, since it never materializes the graph — the same observation as [Graph Valid Tree](261-graph-valid-tree.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is counting connected components, the same question as Number of Islands but on an explicit graph. First I convert the edge list into an adjacency list, adding each edge in *both* directions since the graph is undirected. Then I scan every node from 0 to n−1: whenever I find one that's unvisited, it must be unreachable from everything I've explored, so it starts a new component — I increment the count and flood-fill everything reachable from it. The counting mechanism is 'how many times did I have to start a fresh traversal'. Iterating over all n nodes rather than just the ones in the edge list matters, because isolated nodes are components too. O(V + E) time and space. At n = 2000 a chain-shaped graph would exceed the recursion limit, so I'd use BFS — or union-find, which needs no adjacency list at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it with union-find." | Start `count = n`, union each edge, and decrement whenever two distinct components merge. No adjacency list needed. |
| "Why iterate all n nodes?" | Isolated nodes appear in no edge but are still components. Iterating edge endpoints alone would miss them. |
| "Why add each edge twice?" | Undirected edges work both ways. Adding one direction silently makes the graph directed and splits components wrongly. |
| "What if n = 2000 in a chain?" | DFS recursion overflows. Use BFS or union-find. |
| "DFS or union-find — which?" | DFS if the graph is static and you already need an adjacency list; union-find if edges arrive dynamically or memory is tight. |
| "Return the components themselves?" | Collect nodes during each flood-fill into a list instead of just counting. |
| "How does this relate to [Number of Islands](200-number-of-islands.md)?" | Identical logic. There the graph was implicit in the grid; here it's an explicit edge list. |

**Traps:**

- **Adding edges in only one direction** — components split incorrectly.
- **`[[]] * n`** — n aliases of one list; every node shares neighbours.
- **Iterating only over nodes in `edges`** — isolated nodes are missed entirely.
- **Marking after recursing** rather than before — infinite recursion, since every edge is bidirectional.
- **Counting nodes or edges** instead of traversal starts.
- **Forgetting `visited.add(i)`** in the outer loop — the start node isn't marked, so `dfs` could re-enter it.

**This same move shows up in:** [Number of Islands](200-number-of-islands.md) (the same counting, on an implicit grid graph) · [Graph Valid Tree](261-graph-valid-tree.md) (union-find on an edge list) · [Redundant Connection](684-redundant-connection.md) (union-find detecting the cycle-forming edge) · [union-find](../data-structures/union-find.md) · [dfs](../algorithms/dfs.md).

</details>
