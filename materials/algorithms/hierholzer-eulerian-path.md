# Hierholzer's Algorithm (Eulerian Path)

```python
def find_itinerary(tickets):               # LC 332, Reconstruct Itinerary
    from collections import defaultdict
    adj = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        adj[a].append(b)                    # reverse-sorted → pop() gives smallest

    route, stack = [], ["JFK"]
    while stack:
        while adj[stack[-1]]:               # walk until stuck…
            stack.append(adj[stack[-1]].pop())   # each edge consumed exactly once
        route.append(stack.pop())           # …then peel off the finished node
    return route[::-1]
```

Finds a path/circuit using **every edge exactly once** (Eulerian — versus Hamiltonian's every *node*, which is NP-hard; this one is linear!). The trick: greedily walk, consuming edges, until you strand yourself; the stranded node is the *end* of the route, so record it and backtrack — any unused edges at earlier nodes form side-loops that get spliced in automatically as the stack unwinds. Existence check first: a directed Eulerian *path* needs at most one node with out−in = 1 (start) and one with in−out = 1 (end), all others balanced; undirected needs 0 or 2 odd-degree nodes. On LeetCode this *is* Reconstruct Itinerary (plus Valid Arrangement of Pairs, LC 2097); off LeetCode it's DNA fragment assembly and the classic Seven Bridges of Königsberg puzzle.

**Complexity:** O(E log E) here for the sorting; O(V + E) for the walk itself.

**Related:** [dfs](dfs.md) · [graph (data-structures)](../data-structures/graph.md) · [defaultdict (syntax)](../syntax/defaultdict.md) · [Advanced Graphs lesson](../learning/13-advanced-graphs.md)
