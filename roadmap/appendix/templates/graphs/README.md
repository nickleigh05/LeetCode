# Graphs

*BFS for shortest unweighted paths, DFS for connectivity, and a `visited` set so cycles don't trap you. Know both engines cold.*

## Recognize this pattern when...

- The input is a **grid of cells**, an **adjacency list/matrix**, or **edges between nodes**.
- You're counting **islands / regions / connected components**.
- The ask is a **shortest path in an unweighted graph** (fewest steps / moves).
- There are **prerequisites or ordering** constraints → cycle detection / topological sort.
- You need to **clone, color, or reach** all nodes from a start.

## Variations

1. **Grid flood-fill (DFS)** — recurse into 4 neighbors, mark visited, count area. *(Number of Islands, Max Area of Island)*
2. **Multi-source BFS** — seed *all* sources into the queue at distance 0, then expand. *(Rotting Oranges, Walls and Gates)*
3. **Adjacency-list DFS** — connectivity, component counting, graph cloning. *(Clone Graph)*
4. **Unweighted shortest path (BFS)** — first arrival = fewest edges. *(Word Ladder)*
5. **Cycle detection / topological sort** — in-degree BFS or DFS coloring. *(Course Schedule — see [advanced-graphs](../advanced-graphs/README.md))*
6. **Bipartite coloring (BFS/DFS)** — 2-color neighbors; conflict ⇒ not bipartite. *(Is Graph Bipartite?)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 733 | Easy | Flood Fill |
| 200 | Medium | Number of Islands |
| 133 | Medium | Clone Graph |
| 994 | Medium | Rotting Oranges |
| 207 | Medium | Course Schedule |
| 127 | Hard | Word Ladder |

## Common bugs & traps

- **No `visited` set.** Any cycle loops forever; shared nodes get re-expanded exponentially.
- **Marking visited at dequeue, not enqueue.** The same node gets queued by multiple neighbors → duplicates and TLE. Mark when you *add* to the queue.
- **Bounds checked after access.** Test `0 <= row < rows` *before* reading `grid[row][col]`.
- **Mutating the grid vs. a separate set.** Either is fine, but pick one and be consistent — half-and-half causes double counting.
- **Single-source when you need multi-source.** "Rot all oranges simultaneously" requires seeding every source first.
- **Deep recursion on large grids.** A 10⁶-cell grid can blow the recursion stack — switch to an explicit stack or BFS.
---

*See also: [Lesson 11 →](../../../learning/11-graphs.md) · [🗺 Roadmap](../../../roadmap.md) · [problem lists](../../../../lists/)*
