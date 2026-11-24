# 1489. Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

**Hard** · [LeetCode](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) · [Solution file (no hints)](../../problems/1000-1499/1489.py)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Given a weighted, undirected, connected graph with `n` vertices and `edges[i] = [a, b, weight]`, find the **MST** edges that matter:

- A **critical** edge is in **every** MST: deleting it makes the best spanning tree heavier (or disconnects the graph).
- A **pseudo-critical** edge is in **some** MSTs but not all.

Return `[critical_indices, pseudo_critical_indices]`, in any order.

```
n = 5
edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
→ [[0, 1], [2, 3, 4, 5]]
   edges 0 and 1 (weight 1) must be used; 2-5 are interchangeable pairs

n = 4,  edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]   →  [[], [0, 1, 2, 3]]
```

**Constraints:** `2 <= n <= 100` · `1 <= edges.length <= min(200, n(n-1)/2)` · distinct edges · weights `1..1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| MST | Run [Kruskal](../algorithms/kruskal-mst.md): sort edges, add each one that joins two components (union-find) |
| **critical**: in every MST | Removing it **raises the MST weight** (or disconnects). Test: rebuild the MST **without** this edge |
| **pseudo-critical**: in some MST | Not critical, but **forcing it in** still yields the minimum weight. Test: rebuild the MST starting with this edge included |
| return **indices** | Edges get sorted by weight, so remember each edge's original index |
| `n <= 100`, `E <= 200` | Rebuilding the MST once per edge is fine: about 200 × 200 operations |

The whole problem is two tests per edge, each a Kruskal run:

1. **Exclude** edge `e`: if the MST weight is greater than the baseline (or the graph breaks), `e` is **critical**.
2. Otherwise **force-include** `e`: if the MST weight equals the baseline, `e` is **pseudo-critical**.
3. Otherwise `e` is in no MST at all, and appears in neither list.

🤔 **Before you open the next section:** why must the exclusion test run before the inclusion test? What would an edge that's both "not critical" and "force-includable at the same cost" mean?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Enumerate every spanning tree | exponential | ❌ |
| **Kruskal + [union-find](../data-structures/union-find.md), re-run per edge** | **O(E² · α(n))** | ✅ Simple and fast enough for `E <= 200` |
| Group equal-weight edges and analyse cycles/bridges | O(E log E) | ✅ Faster but far more complex. Mention only |

**The decision: a Kruskal function with two optional parameters:** `skip` (an edge index to leave out) and `force` (an edge index to add first). Each call returns the MST weight, or infinity if the graph isn't connected.

- **Baseline** = `kruskal()` with neither option.
- For each edge: `kruskal(skip=e) > baseline` → critical. Else `kruskal(force=e) == baseline` → pseudo-critical.

The union-find has `find` with path compression and `union` that reports whether a merge happened.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        self.components -= 1
        return True
```

A standard [union-find](../data-structures/union-find.md). `union` returns `True` only when it actually joins two components, which is exactly Kruskal's "does this edge add something?" test. `components` lets us check connectivity at the end.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [while-loop](../syntax/while-loop.md)

```python
indexed = sorted((w, a, b, i) for i, (a, b, w) in enumerate(edges))
```

Attach each edge's original index, then sort by weight (the tuple's first element). Kruskal needs ascending weight, and the answer needs original indices.
→ [enumerate](../syntax/enumerate.md) · [sorting-key](../syntax/sorting-key.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
def mst(skip=-1, force=-1):
    dsu = DSU(n)
    weight = 0
    if force != -1:
        w, a, b, _ = indexed[force]
        dsu.union(a, b)
        weight += w
    for k, (w, a, b, _) in enumerate(indexed):
        if k == skip:
            continue
        if dsu.union(a, b):
            weight += w
    return weight if dsu.components == 1 else float('inf')
```

One Kruskal run. If `force` is given, that edge is added **before** the loop. Then every other edge (except `skip`) is added if it joins two components. If the result isn't a single component, the "MST" doesn't exist: infinite weight, so exclusion of a bridge always counts as critical.
→ [function-basics](../syntax/function-basics.md) · [default-arguments](../syntax/default-arguments.md) · [float-inf](../syntax/float-inf.md) · [kruskal-mst](../algorithms/kruskal-mst.md)

```python
base = mst()
critical, pseudo = [], []
for k, (_, _, _, original) in enumerate(indexed):
    if mst(skip=k) > base:
        critical.append(original)
    elif mst(force=k) == base:
        pseudo.append(original)
return [critical, pseudo]
```

For each edge: excluding it making things worse proves it's critical. If not, forcing it in and still matching the optimum proves it's in *some* MST. The `elif` matters: a critical edge must not also be reported as pseudo-critical. An edge failing both tests (heavier than needed, in no MST) is simply dropped.
→ [list-methods](../syntax/list-methods.md) · [elif-else](../syntax/elif-else.md)

<details>
<summary>The whole thing together</summary>

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        self.components -= 1
        return True


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        indexed = sorted((w, a, b, i) for i, (a, b, w) in enumerate(edges))

        def mst(skip=-1, force=-1):
            dsu = DSU(n)
            weight = 0
            if force != -1:
                w, a, b, _ = indexed[force]
                dsu.union(a, b)
                weight += w
            for k, (w, a, b, _) in enumerate(indexed):
                if k == skip:
                    continue
                if dsu.union(a, b):
                    weight += w
            return weight if dsu.components == 1 else float('inf')

        base = mst()
        critical, pseudo = [], []
        for k, (_, _, _, original) in enumerate(indexed):
            if mst(skip=k) > base:
                critical.append(original)
            elif mst(force=k) == base:
                pseudo.append(original)

        return [critical, pseudo]
```

</details>

**Trace it.** The 4-cycle `n = 4`, all weights 1: `0-1, 1-2, 2-3, 0-3`. Baseline MST weight = 3.

| Edge | `mst(skip)` | Critical? | `mst(force)` | Pseudo? |
|---|---|---|---|---|
| 0-1 | still connected via the other three, weight 3 | no | 3 == 3 | **yes** |
| 1-2 | 3 | no | 3 | **yes** |
| 2-3 | 3 | no | 3 | **yes** |
| 0-3 | 3 | no | 3 | **yes** |

Result `[[], [0, 1, 2, 3]]` ✅: any 3 of the 4 edges form an MST.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(E² · α(n))</summary>

Each Kruskal run is **O(E · α(n))** (the sort is done once, up front, for **O(E log E)**). We run it up to `2E + 1` times: **O(E² · α(n))**. With `E <= 200` that's about 80,000 union-find steps.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(E + n)</summary>

**O(E + n)**: the sorted edge list and one fresh union-find per run (freed between runs).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'll compute the baseline MST weight with Kruskal. For each edge, I test two things. First, rebuild the MST **without** it: if the weight goes up, or the graph disconnects, the edge is in every MST, so it's critical. If not, rebuild the MST **forcing** the edge in first: if I still get the baseline weight, the edge belongs to some MST but not all, so it's pseudo-critical. Anything else is in no MST. Kruskal costs E·α per run, and I do about 2E runs, so O(E²·α), fine for E ≤ 200."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Faster?" | Process edges in groups of equal weight. Within a group, edges that are **bridges** in the "component graph" are critical, and non-bridge edges that connect different components are pseudo-critical. O(E log E) with a bridge-finding pass |
| "Why must the force-test come second?" | A critical edge also passes the force test (it's in every MST). The `elif` stops it being listed twice |
| "Can a graph have several MSTs?" | Yes, whenever equal-weight edges form a cycle. This problem is about exactly those ties |
| "Disconnected graph?" | `float('inf')` for a failed build makes exclusion of a bridge count as critical |
| "Related?" | [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md) (Kruskal or Prim) · [Redundant Connection](684-redundant-connection.md) (union-find cycle detection) |

**Traps:**

- **Forgetting original indices** after sorting. The answer is in input order.
- **Reporting critical edges as pseudo-critical** too (no `elif`).
- **A disconnected result treated as weight 0.** Return infinity so a bridge's exclusion registers as worse.
- **Mutating one shared union-find** between runs. Build a fresh one every time.

**This same move shows up in:** [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md) · [Redundant Connection](684-redundant-connection.md) · [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md).

</details>

---
