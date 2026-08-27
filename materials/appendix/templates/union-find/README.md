# Union-Find (Disjoint Set Union)

*Track who's connected to whom under a stream of merges, in near-constant time. The quiet workhorse behind components, cycle detection, and Kruskal's MST.*

## Recognize this pattern when...

- You're answering **"are these two connected?"** while edges are being **added over time**.
- The ask is **"number of connected components / provinces / groups"**.
- You must detect a **cycle in an undirected graph** (the edge that closes it).
- You're checking whether edges form a **valid tree** (connected + exactly n−1 edges).
- You need **Kruskal's MST**, or to **merge equivalence classes** (accounts, emails, similar strings).

## Variations

1. **Count components** — start `count = n`, decrement on each successful union. *(Number of Connected Components, Number of Provinces)*
2. **Cycle detection** — if `union(u, v)` returns False, that edge closes a cycle. *(Redundant Connection)*
3. **Valid tree** — exactly n−1 edges *and* every union succeeds (no cycle). *(Graph Valid Tree)*
4. **Kruskal's MST** — sort edges by weight, union endpoints, skip ones already joined. *(Min Cost to Connect All Points)*
5. **Equivalence grouping** — map arbitrary IDs to indices, union by shared attribute, bucket by root. *(Accounts Merge)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 323 | Medium | Number of Connected Components in an Undirected Graph |
| 547 | Medium | Number of Provinces |
| 684 | Medium | Redundant Connection |
| 261 | Medium | Graph Valid Tree |
| 721 | Medium | Accounts Merge |
| 1584 | Medium | Min Cost to Connect All Points (Kruskal) |

## Common bugs & traps

- **Skipping the optimizations.** Without path compression *and* union by rank, `find` degrades to O(n) and large inputs TLE.
- **Recursive `find` stack overflow.** A long chain blows Python's recursion limit — use the iterative two-pass form.
- **Union without finding roots.** Always union the *roots*, not the raw elements, or rank and count go wrong.
- **Decrementing count on a no-op union.** Only decrement when the two were in *different* sets.
- **Comparing `parent[x] == x` instead of calling `find`.** Parents can be stale; only `find` resolves the true root.
- **Non-integer elements.** Map labels (emails, coordinates) to indices via a dict before using the array-backed DSU.
---

*See also: [Lesson 12 →](../../../learning/12-union-find.md) · [🗺 Roadmap](../../../../roadmap.md) · [problem lists](../../../../lists/)*
