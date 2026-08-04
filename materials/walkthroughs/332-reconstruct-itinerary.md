# 332. Reconstruct Itinerary

**Hard** · [LeetCode](https://leetcode.com/problems/reconstruct-itinerary/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given a list of airline `tickets`, each `[from, to]`. Reconstruct the itinerary in order, starting from `"JFK"`. **All tickets must be used exactly once.** If several valid itineraries exist, return the one that is smallest in lexical order when read as a single list of airports.

```
tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
        → ["JFK","MUC","LHR","SFO","SJC"]

tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
        → ["JFK","ATL","JFK","SFO","ATL","SFO"]
           not ["JFK","SFO","ATL","JFK","ATL","SFO"] — "ATL" < "SFO" at the first choice
```

**Constraints:** `1 <= tickets.length <= 300` · airports are 3 uppercase letters · the input always has at least one valid itinerary.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| tickets are `[from, to]` pairs | This is a **directed graph**. Airports are nodes, tickets are edges. Say that out loud before anything else |
| "**all tickets must be used exactly once**" | The constraint is on **edges**, not nodes. You must traverse every edge once — that is the definition of an **Eulerian path** |
| a node can appear many times | Confirms it: this is *not* a visited-set traversal. `"JFK"` shows up twice in example 2. **Nodes get revisited; edges do not** |
| "starting from `JFK`" | The start of the Eulerian path is fixed for you — normally the hardest part of the problem |
| "lexically smallest itinerary" | A tie-break. Where an airport has several unused outbound tickets, take the alphabetically smallest first |
| "the input always has at least one valid itinerary" | Enormous gift. You never have to *detect* that no path exists — no validation, no backtracking-on-failure |

So the shape is: **walk a directed graph consuming edges, greedily choosing the smallest destination, until every edge is spent.**

The subtlety hiding in example 2 is worth staring at. From `JFK`, greedy says go to `ATL`. But greedy can also strand you: if from some airport you take the small option and it's a dead end with tickets still unused elsewhere, a naive "just walk greedily and print as you go" produces a broken answer.

🤔 **Before you open the next section:** if greedily walking forward can dead-end while tickets remain, what could you do with a dead end other than treat it as failure? Where in the *final answer* does a dead end have to sit?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every ordering | Permute all tickets, keep the first valid one | O(E!) | O(E) | ❌ 300 tickets. Not a chance |
| Backtracking DFS | Walk greedily; on a dead end with tickets left, undo and try the next destination | O(E!) worst | O(E) | ⚠️ Correct, and it passes — but it's exponential in theory and you're re-deriving a known algorithm badly |
| BFS | Explore level by level | — | — | ❌ There are no "levels" here. You need one specific path, not a shortest one |
| **Hierholzer's algorithm** | DFS that consumes edges and appends each node in **post-order**, then reverses | O(E log E) | O(E) | ✅ |

**The decision:** [Hierholzer's algorithm](../algorithms/hierholzer-eulerian-path.md) — the standard Eulerian-path construction — with the adjacency lists sorted so the greedy tie-break falls out for free.

**The insight that makes backtracking unnecessary.** Think about what a dead end *is*. You're standing at an airport with no unused outbound tickets. Since a valid itinerary is guaranteed to exist, that airport can only be the **final** airport of the whole trip. There is nowhere else it could go.

So instead of backtracking out of a dead end, you **record it as the last stop** and let the recursion unwind. Every time a node runs out of edges, it's appended — meaning nodes are appended in reverse order of the finished route. Reverse at the end and you have the itinerary.

That's the whole trick: **post-order append + final reverse turns "getting stuck" from a bug into the mechanism.**

**Why not just append in pre-order (as you visit)?** Because then a premature dead end lands in the middle of your list, with unused tickets orphaned after it. Pre-order records *the order you guessed*; post-order records *the order that survived*.

**Why does greedy + sorted lists give the lexically smallest result?** Because at each airport you consume outbound tickets smallest-first, and any of them can be completed into a valid finish. The earliest decision dominates lexical order, so taking the smallest available at every step is optimal.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import defaultdict
```
`graph[airport]` will be a list of destinations. A [`defaultdict(list)`](../syntax/defaultdict.md) means you never have to check whether an airport is already a key — including the dead-end airports that appear only as destinations, which is exactly where the recursion will touch a missing key.
→ [defaultdict](../syntax/defaultdict.md) · [graph](../data-structures/graph.md)

```python
        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):   # reverse-sorted so .pop() gives smallest
            graph[src].append(dst)
```
Build the adjacency list — but sorted **descending**. Reading it in that order and appending means each list ends up with the largest destination first and the **smallest last**. Since `list.pop()` takes from the end, `pop()` hands you the alphabetically smallest destination in O(1). Sorting ascending and using `pop(0)` would work too, but that's O(n) per removal.
→ [sorting-key](../syntax/sorting-key.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-methods](../syntax/list-methods.md)

```python
        route = []
```
The output, built **backwards**. Nothing enters it until an airport has exhausted every outbound ticket.
→ [list-basics](../syntax/list-basics.md)

```python
        def dfs(airport):
            while graph[airport]:
                dfs(graph[airport].pop())
```
The traversal. `while` rather than `for`, because the list is being mutated as you go — `pop()` **consumes** the ticket, which is how "each ticket exactly once" is enforced. There's no visited set anywhere: airports are free to be revisited, tickets are not.

Note the ordering inside the loop: `pop()` first, *then* recurse. The edge is removed before you follow it, so a cycle returning to this same airport can't take the same ticket again.
→ [recursion-basics](../syntax/recursion-basics.md) · [while-loop](../syntax/while-loop.md) · [dfs](../algorithms/dfs.md)

```python
            route.append(airport)
```
One line, and it's the whole algorithm. This runs **after** the `while` loop drains — meaning after this airport has no tickets left. Post-order. A dead end appends immediately and lands deep in `route`; `JFK` appends last and lands at the end.
→ [hierholzer-eulerian-path](../algorithms/hierholzer-eulerian-path.md)

```python
        dfs("JFK")
        return route[::-1]
```
Start where the problem tells you to, then flip. `route` was built from the last airport backwards, so reversing yields the itinerary in travel order.
→ [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:

        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):   # reverse-sorted so .pop() gives smallest
            graph[src].append(dst)

        route = []

        def dfs(airport):
            while graph[airport]:
                dfs(graph[airport].pop())
            route.append(airport)

        dfs("JFK")
        return route[::-1]
```
</details>

**Trace it** — `[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]`

After building: `JFK → [SFO, ATL]`, `ATL → [SFO, JFK]`, `SFO → [ATL]` (each list smallest-last).

| Call | Tickets left at this airport | Action | `route` after |
|---|---|---|---|
| `dfs(JFK)` | `[SFO, ATL]` | pop `ATL`, recurse | — |
| `dfs(ATL)` | `[SFO, JFK]` | pop `JFK`, recurse | — |
| `dfs(JFK)` | `[SFO]` | pop `SFO`, recurse | — |
| `dfs(SFO)` | `[ATL]` | pop `ATL`, recurse | — |
| `dfs(ATL)` | `[SFO]` | pop `SFO`, recurse | — |
| `dfs(SFO)` | `[]` | **dead end** → append | `[SFO]` |
| back in `dfs(ATL)` | `[]` | append | `[SFO, ATL]` |
| back in `dfs(SFO)` | `[]` | append | `[SFO, ATL, SFO]` |
| back in `dfs(JFK)` | `[]` | append | `[…, JFK]` |
| back in `dfs(ATL)` | `[]` | append | `[…, ATL]` |
| back in `dfs(JFK)` | `[]` | append | `[SFO,ATL,SFO,JFK,ATL,JFK]` |

Reversed: `["JFK","ATL","JFK","SFO","ATL","SFO"]` ✅

Watch the second row of the table: greedy took `ATL` over `SFO` — the lexical tie-break — and the dead-end `SFO` from row 6 landed at the *front* of `route`, which after reversing is the *end* of the itinerary. Exactly where a dead end belongs.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(E log E)</summary>

**O(E log E)**, where E is the number of tickets.

- `sorted(tickets)` — **O(E log E)**. This dominates.
- Building the adjacency list — O(E) appends.
- The DFS — every ticket is popped exactly once and never revisited, so the traversal is **O(E)** total. Not O(V·E), not exponential: the `pop()` is what bounds it.
- The final reverse — O(V) over the route, which has E + 1 entries.

E + E log E + E → **O(E log E)**.

**The thing to say out loud:** *the sorting is the bottleneck, not the graph traversal.* That's a nice inversion of what people expect from a "Hard" graph problem, and it signals you understand why edge-consumption makes the DFS linear.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(E)</summary>

**O(E).**

- The adjacency list holds every ticket exactly once → O(E).
- `route` ends up with E + 1 airports → O(E).
- The recursion stack: `dfs` can nest once per edge in the path, so **O(E)** frames in the worst case.

All three are O(E), so the total is O(E). With E ≤ 300 the recursion depth is trivially safe here — but on a bigger Eulerian graph you'd want to mention converting to an explicit stack, since Python's default [recursion limit](../syntax/recursion-limit.md) is 1000.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Tickets are directed edges and I have to use every one exactly once, so this is an Eulerian path with a fixed start at JFK. The naive greedy walk breaks, because taking the smallest destination can dead-end while tickets remain elsewhere. But a valid itinerary is guaranteed, so a dead end can only ever be the *final* airport — which means instead of backtracking I append nodes in post-order, after their edges are exhausted, and reverse at the end. That's Hierholzer's algorithm. I sort the adjacency lists descending so `pop()` gives me the lexically smallest destination in O(1). Sorting dominates at O(E log E); the traversal itself is O(E) because each edge is consumed once."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if no valid itinerary exists?" | Then you need the Eulerian precondition: at most one node with `outdeg − indeg == 1` (the start), at most one with `indeg − outdeg == 1` (the end), all others balanced, and the edges connected. Check that up front, or fall back to backtracking DFS and return `[]` on total failure. |
| "Why not a visited set?" | Because the constraint is on edges, not nodes. A visited set would forbid `JFK` appearing twice, which the expected output requires. Consuming the edge *is* the visited marker. |
| "Can you do it iteratively?" | Yes — keep an explicit stack: peek at the top airport, if it has tickets push `pop()`ed destination, else pop the airport into `route`. Same post-order, no recursion depth risk. |
| "What if you needed the largest itinerary?" | Sort ascending instead, so `pop()` returns the largest. One character of change. |
| "Undirected version?" | Hierholzer still works, but you must remove the edge from *both* adjacency lists — usually via an edge-id set rather than a plain list. |
| "Why is the DFS O(E) and not exponential?" | Because `pop()` deletes the edge before recursing. No edge is ever examined twice, so the total work across all calls is bounded by E. |

**Traps:**
- **Appending in pre-order** — the single most common wrong version. It looks right on the simple example and fails on any graph with a dead end.
- **Forgetting the final `[::-1]`** — you get a perfectly correct itinerary, backwards.
- Sorting ascending but still using `pop()` — silently returns the lexically *largest* itinerary.
- Using `graph[airport]` on a plain `dict` — a terminal airport that never appears as a source raises `KeyError`. `defaultdict` is doing real work here, not just tidiness.
- Recursing before popping — an airport with a self-loop or a 2-cycle will reuse the same ticket forever.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (edges as constraints, order emerges from the traversal) · [Course Schedule II](210-course-schedule-ii.md) (post-order DFS reversed to produce an ordering — the same reversal trick, applied to topological sort) · [Binary Tree Postorder](../algorithms/tree-traversal-orders.md) (the general "do the work after the children" shape).

</details>

---
