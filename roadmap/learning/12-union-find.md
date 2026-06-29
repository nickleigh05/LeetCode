# 12. Union-Find (Disjoint Set Union)
*Near-O(1) connectivity and cycle detection under merges.*

[← Prev](11-graphs.md) · [🗺 Roadmap](../roadmap.md) · [Next →](13-advanced-graphs.md)

---

When you keep merging groups and asking "are these two in the same group?", **union-find** answers both in near-constant time with path compression and union by rank. It's the go-to for connected components and cycle detection in an undirected graph.

## Concept

### Disjoint Set Union

```
  Initial: 5 separate components
  {0} {1} {2} {3} {4}
   0   1   2   3   4   ← parent[i] = i (each is own root)

  union(0, 1):       union(1, 2):       union(3, 4):
  {0,1} {2} {3} {4}  {0,1,2} {3} {4}  {0,1,2} {3,4}

  Tree after union(0,1) and union(1,2):
       0                       With path compression:
      /                        find(2) → 2→1→0, then set parent[2]=0
     1
     |
     2

  find(x): return root of x's component (with path compression)
  union(x, y): merge the two components (by rank)
```

**What it is:** A data structure that tracks which elements are in the same connected component. Supports two operations: `find` (which component?) and `union` (merge two components). With path compression and union by rank, both are nearly O(1).

**Key Properties:**
- `find(x)` returns the representative (root) of x's component
- `union(x, y)` connects x's and y's components
- Path compression: on `find`, directly connect nodes to root → amortized O(α(n)) ≈ O(1)
- Union by rank: always attach smaller tree under larger → keeps trees flat

**Complexity:**

| Operation | Time |
|-----------|------|
| find | O(α(n)) ≈ O(1) |
| union | O(α(n)) ≈ O(1) |
| Build for n elements | O(n) |
| Space | O(n) |

α(n) = inverse Ackermann function, effectively constant for all practical n.

**Use when:**
- Counting connected components
- Detecting a cycle in an undirected graph
- Kruskal's Minimum Spanning Tree
- Dynamic connectivity: checking if two nodes are in the same group

**Python:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px          # union by rank
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

## The Pattern

### Union Find

```
  6 nodes, edges: (0,1),(1,2),(3,4),(4,5)

  Initial:  parent=[0,1,2,3,4,5]
  union(0,1): root(0)=0, root(1)=1 → parent[1]=0
              parent=[0,0,2,3,4,5]
  union(1,2): root(1)=0, root(2)=2 → parent[2]=0
              parent=[0,0,0,3,4,5]
  union(3,4): parent[4]=3
              parent=[0,0,0,3,3,5]
  union(4,5): root(4)=3, root(5)=5 → parent[5]=3
              parent=[0,0,0,3,3,3]

  Components: {0,1,2} and {3,4,5}  → count=2

  Cycle detection (undirected graph):
  For each edge (u,v): if find(u)==find(v) → CYCLE!
  Otherwise: union(u,v)
```

**What it is:** Tracks connected components. Two operations: `find(x)` returns the root of x's group, `union(x,y)` merges two groups. Path compression + union by rank makes both nearly O(1).

**Use this when:**
- [ ] Count connected components (and you process edges one at a time)
- [ ] Detect cycle in an undirected graph
- [ ] Kruskal's Minimum Spanning Tree
- [ ] Dynamic connectivity queries ("are A and B connected?")
- [ ] Redundant connection / extra edge in graph

**Python:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False   # already connected
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        self.components -= 1
        return True

# Number of connected components
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components

# Detect cycle in undirected graph
def has_cycle(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):   # already connected → adding this edge = cycle
            return True
    return False
```

**Complexity:** Nearly O(1) per operation with path compression + union by rank.

**Blind 75 examples:** Graph Valid Tree · Number of Connected Components · (Redundant Connection)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/union-find/`](../appendix/templates/union-find/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/union-find/template.py) from memory before you drill problems.

## Practice

The union-find problems live in the [**Graphs section →**](../../lists/recommended.md#11-graphs-23-problems) — focus on the connectivity ones: Number of Connected Components (323), Number of Provinces (547), Graph Valid Tree (261), Redundant Connection (684), Find if Path Exists (1971). Then carry the structure into the [Advanced Graphs set](../../lists/recommended.md#12-advanced-graphs-11-problems) (e.g. Min Cost to Connect All Points / Kruskal's MST).

## Check Yourself

- [ ] I can write find (with path compression) and union (by rank/size) from memory.
- [ ] I can explain why Union-Find beats DFS for incremental connectivity / cycle detection.
- [ ] I know roughly why the amortized cost is near-O(1) (inverse Ackermann).
- [ ] I solved a 🔴 Hard Union-Find problem (e.g. Redundant Connection II or Accounts Merge).

---

**Up next:** [Advanced Graphs (Dijkstra & Topological Sort)](13-advanced-graphs.md) — weighted shortest paths and dependency ordering.

[← Prev](11-graphs.md) · [🗺 Roadmap](../roadmap.md) · [Next →](13-advanced-graphs.md)

