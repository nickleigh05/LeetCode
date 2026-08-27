# 133. Clone Graph

**Medium** · [LeetCode](https://leetcode.com/problems/clone-graph/) · [Solution file (no hints)](../../problems/0001-0499/133.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Given a reference to a node in a **connected undirected graph**, return a **deep copy** of the graph.

Each node contains a value and a list of its neighbours:

```python
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

```
adjList = [[2,4],[1,3],[2,4],[1,3]]     a 4-node cycle: 1—2—3—4—1
  →  an identical graph made entirely of NEW nodes

adjList = [[]]   →  a single node with no neighbours
adjList = []     →  null
```

**Constraints:** `0 <= nodes <= 100` · `1 <= Node.val <= 100`, **unique** · no repeated edges, no self-loops · the graph is **connected**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**deep** copy" | Brand-new nodes; no pointer may lead back into the original |
| "**undirected**" | ⚠️ Every edge appears **twice** — if A lists B, then B lists A. So the graph has **cycles** everywhere |
| "**connected**" | One DFS from any node reaches everything — no outer scan needed |
| node values are **unique** | Handy, though the solution keys on node *identity* rather than value |
| graph can be **empty** | `None` in → `None` out |
| ≤ 100 nodes | Small; recursion depth is safe |

**The core difficulty: cycles.** In an undirected graph, `A —— B` means `A.neighbors` contains B *and* `B.neighbors` contains A. So a naive recursive copy does this:

```
clone(A) → clone its neighbour B → clone its neighbour A → clone its neighbour B → …
```

**Infinite recursion**, immediately, on the simplest possible edge.

**What you actually need.** Before cloning a neighbour, you must be able to ask:

> **"Have I already made a copy of this node? If so, give me that copy."**

Two requirements in one question — *detect* the repeat, and *retrieve* the existing clone so the new graph stays properly wired.

That's a **hash map from original node → its clone**. It serves as both the visited set and the lookup table.

**This is exactly [Copy List with Random Pointer](138-copy-list-with-random-pointer.md)'s technique**, applied to a general graph instead of a linked list. There the problem was *forward* pointers to uncopied nodes; here it's *cycles*. Both are solved by the same original→copy map — worth recognizing, because it means the technique generalizes to cloning any object graph.

🤔 **Before you open the next section:** when you create a clone, should you record it in the map *before* or *after* recursing into its neighbours? Try both against a two-node cycle.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Recursive copy, no memo | Clone each neighbour recursively | ❌ **Infinite recursion** on any edge |
| Separate `visited` set + node lookup | Track visited, find clones by value | ⚠️ Works, but two structures where one suffices |
| **Hash map `original → clone`, DFS** | The map is both the visited set and the lookup | ✅ |
| BFS with the same map | Queue instead of recursion | ✅ Equally valid |

**The decision: DFS with a [hash map](../data-structures/hashmap.md) from original node to its clone.**

The map does **two jobs at once**, which is why one structure is enough:

| Question | Answered by |
|---|---|
| "Have I seen this node?" | `current_node in old_to_new` |
| "Where's its clone?" | `old_to_new[current_node]` |

A separate `visited` set would answer the first but not the second — and you'd still need a way to find the existing clone, since the new graph's edges must point at *clones*, not originals.

**⚠️ The ordering that makes it work.** The clone must be recorded in the map **before** recursing into neighbours:

```python
copy_node = Node(current_node.val)
old_to_new[current_node] = copy_node      # ← BEFORE the recursion
for neighbor in current_node.neighbors:
    copy_node.neighbors.append(dfs(neighbor))
```

Trace a two-node cycle `A —— B` to see why:

1. `dfs(A)` — create A′, **record it**, then recurse into B.
2. `dfs(B)` — create B′, record it, then recurse into A.
3. `dfs(A)` — **A is already in the map** → return A′ immediately. ✅ Cycle broken.

Record *after* the recursion instead, and step 3 finds nothing in the map and recurses again — infinite loop. **The early registration is the entire cycle-breaking mechanism.**

**Why key on the node object, not `val`.** Python hashes objects by identity by default, so `old_to_new[node]` means "this specific node". Values happen to be unique here, but keying by identity is correct in general and needs no such guarantee — the same reasoning as [Copy List with Random Pointer](138-copy-list-with-random-pointer.md).

**Why no outer scan over all nodes.** The graph is **connected**, so one DFS from the given node reaches everything. In a disconnected graph you'd need to iterate over all nodes, like [Number of Islands](200-number-of-islands.md)'s scan.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if node is None:
    return None
```

**Empty graph guard.** Without it, `dfs(None)` would fail on `.val`.
→ [identity-operators](../syntax/identity-operators.md) · [none-type](../syntax/none-type.md) · [if-return](../syntax/if-return.md)

```python
old_to_new = {}
```

**The map doing double duty** — original node → its clone. It's simultaneously the visited set and the clone lookup.
→ [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dfs(current_node):
    if current_node in old_to_new:
        return old_to_new[current_node]
```

**The cycle breaker.** Already cloned ⇒ return the existing clone instead of recursing.

This single check is what turns infinite recursion into a terminating traversal — and returning the *clone* (not just `True`) is what keeps the new graph's edges pointing into the copy.
→ [membership-operators](../syntax/membership-operators.md) · [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
    copy_node = Node(current_node.val)
    old_to_new[current_node] = copy_node
```

**Create the clone and register it immediately** — *before* touching neighbours.

⚠️ **This ordering is the whole solution.** When the recursion inevitably comes back around a cycle to this node, the check above finds it and returns. Register *after* the loop instead and the cycle never breaks.

The clone starts with an empty neighbour list, filled in below.
→ [class-basics](../syntax/class-basics.md) · [graph](../data-structures/graph.md)

```python
    for neighbor in current_node.neighbors:
        copy_node.neighbors.append(dfs(neighbor))
```

**Wire the clone's edges.** For each *original* neighbour, `dfs` returns the corresponding *clone* — either freshly built or fetched from the map.

Appending `dfs(neighbor)` rather than `neighbor` is what makes it a **deep** copy: every pointer leads into the new graph, never the original.
→ [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    return copy_node

return dfs(node)
```

Return the clone of the entry node. The graph is connected, so this single call has cloned everything.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:

        if node is None:
            return None

        old_to_new = {}

        def dfs(current_node):
            if current_node in old_to_new:
                return old_to_new[current_node]

            copy_node = Node(current_node.val)
            old_to_new[current_node] = copy_node

            for neighbor in current_node.neighbors:
                copy_node.neighbors.append(dfs(neighbor))

            return copy_node

        return dfs(node)
```

</details>

**Trace it** — a triangle `1—2—3—1`:

| Step | Call | In map? | Action |
|---|---|---|---|
| 1 | `dfs(1)` | no | create **1′**, register, recurse into neighbours [2, 3] |
| 2 | `dfs(2)` | no | create **2′**, register, recurse into [1, 3] |
| 3 | `dfs(1)` | **yes** ✅ | **return 1′** — cycle broken |
| 4 | `dfs(3)` | no | create **3′**, register, recurse into [1, 2] |
| 5 | `dfs(1)` | **yes** ✅ | return 1′ |
| 6 | `dfs(2)` | **yes** ✅ | return 2′ |
| 7 | | | 3′.neighbors = [1′, 2′], return 3′ |
| 8 | | | 2′.neighbors = [1′, 3′], return 2′ |
| 9 | `dfs(3)` | **yes** ✅ | return 3′ |
| 10 | | | 1′.neighbors = [2′, 3′], return 1′ ✅ |

Result: a triangle of **new** nodes with identical structure — and every neighbour list points at clones.

**Steps 3, 5, 6 and 9 are the map earning its place.** Each is a moment where naive recursion would have looped forever. **Four cycles broken in a three-node graph** — which is why undirected graphs need this from the very first edge.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)**, where V is the number of nodes and E the number of edges.

- **Each node is cloned exactly once** — the map check ensures every subsequent encounter returns immediately → O(V) node creations.
- **Each edge is traversed** — from both endpoints, since the graph is undirected → O(2E) = O(E) map lookups and appends, each O(1).

**O(V + E)** total, which is optimal: you must examine every node and edge to reproduce them.

At ≤ 100 nodes this is instantly fast.

**This is the standard bound for graph traversal**, and it'll recur throughout Unit 11. Note it's *not* O(V²) — that would be the cost of an adjacency **matrix** traversal. With adjacency **lists**, you only touch edges that exist.

**Without the map it's infinite** — not merely slow. The memoization isn't an optimization here; it's what makes the algorithm terminate at all. Worth stating plainly, because it's a different kind of necessity from most memoization.

**BFS is identically O(V + E)**, visiting each node and edge once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V)</summary>

**O(V)**, plus the O(V + E) output.

| Component | Size |
|---|---|
| `old_to_new` map | one entry per node → **O(V)** |
| Recursion stack | up to V frames on a path-shaped graph → **O(V)** |
| The cloned graph | the required output → O(V + E) |

So: **"O(V) auxiliary, plus the cloned graph itself."**

**The recursion depth is bounded by V**, reached when the graph is a long chain. At ≤ 100 nodes that's safe; on a graph with 10⁵ nodes it would exceed Python's recursion limit, and BFS with an explicit queue would be required.
→ [recursion-limit](../syntax/recursion-limit.md)

**The map cannot be avoided.** Unlike some visited-tracking (where you might mark nodes in place), you genuinely need to *retrieve* each clone, not just know it exists. Marking the original nodes wouldn't help — you'd still have no way to find the corresponding copy.

**The BFS variant** uses the same map plus a queue bounded by the frontier — O(V) either way, but with no recursion-depth risk:

```python
from collections import deque
old_to_new = {node: Node(node.val)}
queue = deque([node])
while queue:
    curr = queue.popleft()
    for nei in curr.neighbors:
        if nei not in old_to_new:
            old_to_new[nei] = Node(nei.val)
            queue.append(nei)
        old_to_new[curr].neighbors.append(old_to_new[nei])
```

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The graph is undirected, so every edge appears in both nodes' neighbour lists — which means cycles everywhere, and a naive recursive copy loops forever on the very first edge. What I need is to ask 'have I already cloned this node, and if so where is its clone?' — that's a hash map from original node to clone, which serves as both the visited set and the lookup. The critical detail is *when* I register the clone: it has to go into the map immediately after creation, before recursing into neighbours. Then when the recursion comes back around the cycle, the lookup finds it and returns instead of recursing. I key on the node object rather than its value, so it works even without unique values. O(V + E) time, O(V) space, and no outer scan since the graph is connected."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why register the clone before recursing?" | **The question.** Otherwise a cycle returns to a node still absent from the map and recurses forever. Trace a two-node cycle. |
| "Why a map and not a `visited` set?" | A set answers "seen it?" but not "where's its clone?" — and the new edges must point at clones. |
| "What if the graph were **disconnected**?" | One DFS wouldn't reach everything. Iterate over all nodes, starting a DFS from each unvisited one — like [Number of Islands](200-number-of-islands.md)'s outer scan. |
| "Do it with BFS." | Same map; clone a node when first enqueued, and wire edges as you dequeue. Avoids the recursion-depth risk. |
| "What if node values weren't unique?" | Unchanged — the map keys on object identity, not value. That's why this is the robust choice. |
| "What about self-loops or repeated edges?" | The constraints exclude them, but the code handles both: a self-loop hits the map check, and a repeated edge just appends the same clone twice. |
| "How does this relate to [Copy List with Random Pointer](138-copy-list-with-random-pointer.md)?" | Identical technique. There the problem was forward pointers to uncopied nodes; here it's cycles. Both need original→copy. |

**Traps:**

- **Registering the clone after the neighbour loop** — the cycle is never broken and recursion is infinite. *The* bug of this problem.
- **Omitting the map entirely** — same infinite recursion.
- **Appending `neighbor` instead of `dfs(neighbor)`** — the clone's edges point into the *original* graph, making it a shallow copy.
- **Keying the map by `val`** — works here by luck, breaks whenever values repeat.
- **Forgetting the `None` guard** — `AttributeError` on empty input.
- **Adding an outer scan** over all nodes — harmless but unnecessary given connectivity, and it signals you missed the constraint.

**This same move shows up in:** [Copy List with Random Pointer](138-copy-list-with-random-pointer.md) (the identical original→copy map) · [Number of Islands](200-number-of-islands.md) (visited tracking during traversal) · [Course Schedule](207-course-schedule.md) (cycle detection, though for a different purpose) · [dfs](../algorithms/dfs.md) · [graph](../data-structures/graph.md).

</details>

---
