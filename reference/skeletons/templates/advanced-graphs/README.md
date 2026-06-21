# Advanced Graphs

*Weighted shortest paths, MST, ordering constraints. High effort, high signal — these separate "can traverse a graph" from "can model a problem as one".*

## Recognize this pattern when...

- Edges carry **weights / costs / times** and you want the **cheapest / shortest** route → Dijkstra.
- You must **connect all nodes at minimum total cost** → Minimum Spanning Tree.
- There are **prerequisites, dependencies, or a build order** → topological sort.
- The path is constrained (**"within K stops"**, **"minimum effort"**, **"swim in rising water"**).
- A plain BFS gives wrong answers because not all edges are equal.

## Variations

1. **Dijkstra (shortest path)** — min-heap of `(dist, node)`, relax non-negative edges. *(Network Delay Time, Path With Minimum Effort)*
2. **State-augmented shortest path** — carry extra state like stops-remaining; Bellman-Ford bounds the hops. *(Cheapest Flights Within K Stops)*
3. **Topological sort (Kahn's BFS)** — in-degree queue; cycle iff not all nodes emitted. *(Course Schedule II)*
4. **Topological sort (DFS post-order)** — push on the way out, reverse at the end. *(Alien Dictionary)*
5. **MST — Prim's (heap) / Kruskal's (union-find)** — grow the cheapest tree spanning all nodes. *(Min Cost to Connect All Points)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 743 | Medium | Network Delay Time |
| 1584 | Medium | Min Cost to Connect All Points |
| 787 | Medium | Cheapest Flights Within K Stops |
| 210 | Medium | Course Schedule II |
| 332 | Hard | Reconstruct Itinerary |
| 778 | Hard | Swim in Rising Water |

## Common bugs & traps

- **Dijkstra with negative weights.** It silently returns wrong answers — use Bellman-Ford / SPFA instead.
- **Not skipping stale heap entries.** A node can sit in the heap with several distances; ignore any pop worse than the settled distance.
- **Settling a node twice.** Once popped (and not stale), its distance is final — don't relax *into* it again.
- **Topological sort cycle check.** If the emitted order is shorter than `num_nodes`, a cycle exists — return `[]` / `False` as required.
- **In-degree direction.** Edge `(prereq → dependent)` increments the *dependent's* in-degree. Reversing it inverts the whole order.
- **MST: re-adding settled nodes.** In Prim's, skip heap entries for nodes already in the tree, or you double-count edges.
---

*See also: [patterns.md](../../patterns.md) · [datastructures.md](../../../ds&a/datastructures.md) · [algorithms.md](../../../ds&a/algorithms.md) · [lists/](../../../../lists/)*
