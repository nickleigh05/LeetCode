"""
Advanced Graphs — Dijkstra and Topological Sort Skeletons

Once edges carry weights or ordering constraints, plain BFS/DFS is not enough:

  1. DIJKSTRA          — shortest paths from a source on a graph with
                         NON-NEGATIVE weights. A min-heap always expands the
                         closest unsettled node, which locks in its distance.
  2. TOPOLOGICAL SORT  — a linear ordering of a DAG so every edge points
     (Kahn's)            "forward". Repeatedly emit a node with no remaining
                         prerequisites; if you can't emit all, there's a cycle.

Invariant (Dijkstra): once a node is popped from the heap its distance is final
— no later path can beat it, because every edge weight is >= 0.
Invariant (Kahn's): a node is emitted only when its in-degree hits 0, i.e. all
its prerequisites are already in the order.
"""

import heapq
from collections import deque
from typing import Dict, List, Tuple


def dijkstra(graph: Dict[int, List[Tuple[int, int]]], source: int) -> Dict[int, int]:
    """Single-source shortest paths with non-negative edge weights.

    `graph[u]` is a list of (neighbor, weight) pairs.

    Time:      O(E log V) — each edge can push once; heap ops are log V.
    Space:     O(V + E)
    Invariant: `distance[node]` is final the moment `node` is popped; stale heap
               entries (a worse distance pushed earlier) are skipped on pop.
    """

    distance: Dict[int, int] = {source: 0}
    min_heap: List[Tuple[int, int]] = [(0, source)]  # (distance_so_far, node)

    while min_heap:
        current_distance, node = heapq.heappop(min_heap)

        # Skip stale entries: this node was already settled via a shorter route.
        if current_distance > distance.get(node, float("inf")):
            continue

        for neighbor, weight in graph[node]:
            candidate = current_distance + weight

            # RELAX: only act if this path improves the best known distance.
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                heapq.heappush(min_heap, (candidate, neighbor))

    return distance


def topological_sort(num_nodes: int, edges: List[Tuple[int, int]]) -> List[int]:
    """Kahn's algorithm: order a DAG, or detect that it has a cycle.

    `edges` are directed (prerequisite -> dependent) pairs.

    Time:      O(V + E)
    Space:     O(V + E)
    Invariant: the queue holds exactly the nodes whose prerequisites are all
               already placed (in-degree 0). If fewer than num_nodes are
               emitted, a cycle blocked the rest.
    """

    adjacency: Dict[int, List[int]] = {node: [] for node in range(num_nodes)}
    in_degree = [0] * num_nodes

    for prerequisite, dependent in edges:
        adjacency[prerequisite].append(dependent)
        in_degree[dependent] += 1

    # Seed the queue with every node that has no prerequisites.
    queue: "deque[int]" = deque(
        node for node in range(num_nodes) if in_degree[node] == 0
    )
    order: List[int] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        # Removing `node` frees its dependents; any that reach in-degree 0 are
        # now ready to be placed next.
        for dependent in adjacency[node]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # A complete ordering proves the graph was acyclic.
    if len(order) != num_nodes:
        return []  # TODO: signal a cycle however the problem expects
    return order
