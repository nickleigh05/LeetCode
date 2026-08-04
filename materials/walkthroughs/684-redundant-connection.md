# 684. Redundant Connection

**Medium** · [LeetCode](https://leetcode.com/problems/redundant-connection/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

In this problem, a tree is an **undirected graph that is connected and has no cycles**.

You're given a graph that started as a tree with `n` nodes labelled `1` to `n`, with **one additional edge** added. Return that edge. If there are multiple answers, return the one that occurs **last** in the input.

```
edges = [[1,2],[1,3],[2,3]]  →  [2,3]

    1                the edge [2,3] closes the cycle 1—2—3—1
   / \
  2 — 3

edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]  →  [1,4]
```

**Constraints:** `3 <= n <= 1000` · `edges.length == n` · no self-loops, no repeated edges · the graph is **connected**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "a tree with **one additional edge**" | ⚠️ Exactly **one** cycle exists. `n` nodes and `n` edges — one more than a tree's n−1 |
| "return **that** edge" | The one whose removal restores a tree |
| "the one that occurs **last**" | ⚠️ If several edges lie on the cycle, prefer the latest in the input |
| "**undirected**" | Union-find applies cleanly (unlike the directed variant, LeetCode 685) |
| n ≤ 1000 | Near-linear expected |

**Which edge is "redundant"?** Any edge on the cycle could be removed to restore a tree — the cycle `1—2—3—1` breaks if you delete any of its three edges. So the problem needs a tie-break, and it picks **the last one in the input order**.

**The observation that makes this simple.** Process the edges **in order**, building the graph incrementally:

> **An edge closes a cycle exactly when its two endpoints are already connected.**

If a path between `a` and `b` already exists, adding a direct edge creates a loop.

And because you're processing in input order, **the first edge that closes a cycle is automatically the last edge of the cycle to appear** — which is precisely the tie-break the problem wants. **The ordering requirement is satisfied for free**, with no extra logic.

```
[[1,2],[1,3],[2,3]]

  [1,2]  →  1 and 2 not connected  →  add
  [1,3]  →  1 and 3 not connected  →  add
  [2,3]  →  2 and 3 ALREADY connected (via 1)  →  ⛔ this is the answer
```

**So you need one operation:** *"are these two nodes already connected?"* — answered incrementally as edges arrive. That's **[union-find](../data-structures/union-find.md)**.

🤔 **Before you open the next section:** why does answering this incrementally, rather than building the whole graph and then hunting for the cycle, make the "last edge" requirement disappear?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Build the graph, find the cycle with DFS | Locate the cycle, then pick its last edge | O(V + E) | ⚠️ Correct; extracting *which* edges are on the cycle is fiddly |
| For each edge, remove it and test connectivity | n removals × O(V+E) each | O(V·(V+E)) | ⚠️ Correct but wasteful |
| **Union-Find, processing edges in order** | First edge joining an already-connected pair | **O(n·α(n))** | ✅ |

**The decision: [union-find](../data-structures/union-find.md), returning the first edge whose endpoints already share a root.**

**Why union-find is the natural fit.** The question is *dynamic connectivity* — "as I add edges one at a time, when do two nodes first become connected?" That's exactly what union-find is built for, and it's why this problem is the canonical introduction to it.

DFS could find the cycle, but you'd then have to determine which edges belong to it and pick the last — noticeably more code, and easy to get wrong.

**Why the input order handles the tie-break automatically.** Edges are processed left to right, so the first cycle-closing edge encountered is the last edge of that cycle to appear in the input. **No sorting, no comparison, no bookkeeping** — a genuinely elegant consequence of processing incrementally.

**The two operations:**

| Operation | Meaning |
|---|---|
| **`find(x)`** | which component is x in? (its root) |
| **`union(x, y)`** | merge two components; return `False` if they were already the same |

Having `union` **report** whether it did anything is what turns it into a cycle detector.

**Why `parent` is sized `len(edges) + 1`.** Nodes are labelled **1 to n** (not 0 to n−1), and `edges.length == n`, so node ids run up to `n`. Sizing the array `n + 1` lets you index by node id directly, wasting only index 0. **A one-off but classic off-by-one.**

**Path compression** — `parent[x] = parent[parent[x]]` — re-points each node at its grandparent during traversal, flattening the tree so later `find` calls are nearly O(1).

**This is [Graph Valid Tree](261-graph-valid-tree.md)'s machinery, asked differently:** that problem returned `False` on the first cycle; this one returns **the edge that caused it**.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
parent = list(range(len(edges) + 1))
```

**Every node starts as its own parent** — each in its own component.

⚠️ **`len(edges) + 1`** because nodes are labelled **1 to n** and `edges.length == n`. Sizing it `n + 1` allows direct indexing by node id; index 0 is unused.
→ [union-find](../data-structures/union-find.md) · [range-function](../syntax/range-function.md) · [list-basics](../syntax/list-basics.md)

```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
```

**Walk up to the component root**, compressing the path along the way.

`parent[x] = parent[parent[x]]` points `x` at its grandparent, halving the remaining path. Over repeated calls the tree flattens to nearly depth 1, making `find` effectively O(1).

Without it, a degenerate chain would make each `find` O(n).
→ [while-loop](../syntax/while-loop.md) · [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
def union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x == root_y:
        return False
```

**The cycle test.** Same root ⇒ already connected ⇒ this edge closes a cycle ⇒ report failure.

Returning a boolean rather than merging silently is what makes `union` usable as a detector.

```python
    parent[root_x] = root_y
    return True
```

**Merge** by pointing one root at the other, and report that a real merge happened.

*(A fuller implementation would add union-by-rank, attaching the smaller tree under the larger. Path compression alone is sufficient at n ≤ 1000.)*

```python
for a, b in edges:
    if not union(a, b):
        return [a, b]
```

**Process edges in input order, returning the first that closes a cycle.**

Because of that ordering, this is automatically the **last** edge of the cycle to appear — exactly what the problem asks for, with no extra logic.

The constraints guarantee exactly one extra edge, so this loop always returns.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [if-return](../syntax/if-return.md) · [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        parent = list(range(len(edges) + 1))

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
                return [a, b]
```

</details>

**Trace it** — `edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]`:

`parent` starts as `[0,1,2,3,4,5]` (index 0 unused).

| Edge | `find(a)` | `find(b)` | Same? | Action | `parent` after |
|---|---|---|---|---|---|
| `[1,2]` | 1 | 2 | no | merge | `[0,2,2,3,4,5]` |
| `[2,3]` | 2 | 3 | no | merge | `[0,2,3,3,4,5]` |
| `[3,4]` | 3 | 4 | no | merge | `[0,2,3,4,4,5]` |
| **`[1,4]`** | **4** | **4** | **YES** ⛔ | **cycle!** | → **return `[1,4]`** ✅ |

At the fourth edge, `find(1)` walks 1 → 2 → 3 → 4 and `find(4)` gives 4 — the same root, so 1 and 4 were already connected via the chain 1—2—3—4. Adding a direct edge closes the cycle.

**Note `[1,5]` is never examined** — the loop returned first. And that's correct: `[1,5]` isn't on the cycle at all.

**The first example** — `[[1,2],[1,3],[2,3]]`:

| Edge | Roots | Same? | Result |
|---|---|---|---|
| `[1,2]` | 1, 2 | no | merge |
| `[1,3]` | 2, 3 | no | merge |
| **`[2,3]`** | **3, 3** | **yes** | **return `[2,3]`** ✅ |

All three edges lie on the cycle, and the answer is the **last** one — which is exactly the one that first closed it. **The ordering requirement satisfied itself.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · α(n)) ≈ O(n)</summary>

**O(n · α(n))**, where α is the **inverse Ackermann function** — below 5 for any realistic input, so effectively **O(n)**.

| Step | Cost |
|---|---|
| Initialize `parent` | O(n) |
| Process each edge | one `union` = two `find`s |
| Each `find` | **O(α(n))** amortized with path compression |

There are `n` edges, giving **O(n·α(n))**.

At n = 1000, that's ~1000 operations with a tiny constant.

**Why `find` is near-constant.** Path compression flattens the tree during every traversal — after a few operations most nodes point directly at their root. The amortized bound over m operations is O(m·α(n)).

Without path compression, a chain-shaped structure makes each `find` O(n) and the total **O(n²)**.

**Early exit.** The loop returns at the first cycle-closing edge, so edges after it are never processed — as in the trace, where `[1,5]` was skipped.

**Versus the alternatives:** DFS cycle-finding is O(V + E) but needs extra work to identify which edges lie on the cycle; removing each edge and testing connectivity is O(V·(V+E)) = ~10⁶.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — just the `parent` array of n+1 integers.

**No adjacency list is built.** Union-find operates **directly on the edge list**, processing each edge as it arrives — so the graph is never materialized:

| Approach | Space |
|---|---|
| DFS cycle detection | **O(V + E)** — adjacency list + visited + recursion |
| **Union-Find** | **O(n)** — just `parent` |

**No recursion**, so no stack-depth risk — unlike a DFS approach, where a chain of 1000 nodes would need 1000 frames.

**The streaming property is the deeper point.** Union-find never needs the whole graph in memory: edges can arrive one at a time and connectivity questions are answered as you go. **That's what makes it the right tool for *dynamic* connectivity** — the same observation as [Graph Valid Tree](261-graph-valid-tree.md) and [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md).

**Union-by-rank** would add a second O(n) array to keep trees shallow. Skipping it keeps the code short, and path compression alone gives good behaviour at these sizes — worth naming as the standard companion optimization.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The graph is a tree plus one edge, so there's exactly one cycle, and any edge on it could be removed — the problem breaks the tie by asking for the last one in the input. The key observation is that an edge closes a cycle exactly when its two endpoints are already connected. So I process edges in input order with union-find, and the first edge whose endpoints already share a root is the answer. And because I'm going in order, that's automatically the *last* edge of the cycle to appear — the tie-break comes for free. Path compression makes `find` near-constant, so it's O(n·α(n)), effectively linear, with O(n) space and no adjacency list at all. DFS could find the cycle too, but working out which edges belong to it and picking the last is much more code."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the first cycle-closing edge the *last* one of the cycle?" | **The question.** Processing in input order means every earlier cycle edge was already added; the one that finally closes it is the latest to appear. |
| "Why union-find rather than DFS?" | Dynamic connectivity is exactly what it answers. DFS would find the cycle but then needs extra work to identify and order its edges. |
| "What if the graph were **directed**?" | Much harder — a node can have two parents, or a cycle can exist, or both. LeetCode 685 handles three cases. |
| "What does path compression do?" | Re-points nodes closer to the root during `find`, flattening the structure so later lookups are nearly O(1). |
| "Why is `parent` sized `n + 1`?" | Nodes are labelled 1 to n, so direct indexing needs one extra slot. Index 0 is unused. |
| "What if there were multiple extra edges?" | The loop would return the first cycle-closer. To find all, don't return — collect every failed union. |
| "Count components instead?" | Union everything, then count distinct roots — [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md). |

**Traps:**

- **Sizing `parent` as `n`** instead of `n + 1` — nodes are 1-indexed, so node `n` would be out of range.
- **Comparing `parent[a] == parent[b]`** instead of `find(a) == find(b)` — that compares immediate parents, not roots.
- **Omitting path compression** — correct but O(n²) on adversarial input.
- **Processing edges in a different order** (sorting them, say) — the last-edge tie-break breaks.
- **Returning the *first* edge of the cycle** rather than the one that closed it.
- **Building an adjacency list** — unnecessary; union-find works straight off the edge list.

**This same move shows up in:** [Graph Valid Tree](261-graph-valid-tree.md) (the same union-find cycle detection, returning a boolean) · [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md) (union-find counting components) · [union-find](../data-structures/union-find.md) · [12. Union-Find lesson](../learning/12-union-find.md).

</details>
