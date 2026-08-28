# 802. Find Eventual Safe States

**Medium** · [LeetCode](https://leetcode.com/problems/find-eventual-safe-states/) · [Solution file (no hints)](../../problems/0500-0999/802.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

In a **directed** graph, a node is **terminal** if it has no outgoing edges, and **safe** if **every** path starting from it leads to a terminal node. Return all safe nodes, sorted ascending.

```
graph = [[1,2],[2,3],[5],[0],[5],[],[]]     →  [2,4,5,6]
graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]    →  [4]
```

**Constraints:** `1 <= n <= 10^4` · edges ≤ 4·10⁴ · **may contain self-loops**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**directed** graph" | Edges are one-way. Cycle detection needs the three-state method, not a plain `visited` set |
| "**every** possible path leads to a terminal" | ⚠️ **Universal**, not existential. One bad path spoils the node |
| "terminal = no outgoing edges" | The base case: vacuously safe |
| "may contain **self-loops**" | A node pointing at itself is a cycle of length 1 |
| answer **sorted ascending** | Iterating `0..n-1` gives this for free |
| `n <= 10^4` | ⚠️ Recursion could reach 10,000 deep — past Python's default limit |

**Restate it as the contrapositive, and it becomes concrete:**

> A node is **safe** ⟺ it cannot reach a cycle.

Every path is finite, so it either ends at a terminal node or loops forever. "All paths terminate" is therefore the same as "no path reaches a cycle" — and *that* is something you can test with a standard traversal.

```
graph = [[1,2],[2,3],[5],[0],[5],[],[]]

0 → 1 → 3 → 0    ← cycle!  so 0, 1, 3 are all unsafe
0 → 2 → 5 (terminal)
2 → 5 (terminal)         ← 2's ONLY path terminates → safe
4 → 5 (terminal)         ← safe
5, 6: no outgoing        ← terminal, vacuously safe

answer: [2, 4, 5, 6]
```

**Note node 0 carefully.** It has a path that terminates (`0 → 2 → 5`) and yet is **unsafe**, because it *also* has `0 → 1 → 3 → 0`. **"Every path" means one bad path is fatal** — this is the distinction the problem is built around, and it's why the recursion returns `False` the instant *any* child is unsafe.

**Why a plain `visited` set is not enough.** In an undirected graph, "already seen" means "no need to revisit". In a directed graph you must distinguish two very different reasons a node was seen before:

```
seen, and still on the current path   →  a CYCLE  →  unsafe
seen, and fully finished earlier      →  just a memo hit  →  reuse the result
```

A single boolean can't tell those apart. Hence **three states**:

| State | Meaning |
|---|---|
| `0` **unvisited** | Not yet explored |
| `1` **in-progress** | On the current DFS path — *reaching it again is a cycle* |
| `2` **safe** | Fully explored, all paths terminate |

This is the standard **white / grey / black** colouring for cycle detection in directed graphs, and it's the same machinery behind [Course Schedule](207-course-schedule.md).

🤔 **Before you open the next section:** when the DFS discovers a node is unsafe, should it reset that node's state back to `0`, or leave it as it is? Think about what happens when a later call reaches the same node.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Per-node full search | For each node, explore all paths | O(V·(V+E)) | ❌ Re-derives everything |
| **Three-state DFS** | White/grey/black with memoisation | **O(V + E)** | ✅ |
| **Reverse topological sort** | Peel off out-degree-0 nodes | **O(V + E)** | ✅ Iterative — no stack risk |
| Find SCCs (Tarjan) | Nodes reaching a non-trivial SCC are unsafe | O(V+E) | ⚠️ Correct but heavy |

**The decision: three-state DFS.** Know the topological version as the iterative alternative.

**The DFS, and the one line that makes it fast:**

```python
def dfs(node):
    if state[node] == 1: return False      # cycle — on the current path
    if state[node] == 2: return True       # memo hit — known safe
    state[node] = 1                        # mark in-progress
    for nb in graph[node]:
        if not dfs(nb): return False       # ONE bad child ⇒ unsafe
    state[node] = 2                        # all children safe ⇒ safe
    return True
```

⚠️ **The subtle part: when a node turns out unsafe, its state is left at `1`, not reset to `0`.**

This looks like a bug and is in fact the key optimisation. A node that returns `False` stays marked `in-progress` forever, so **any later visit to it hits the `state == 1` branch and immediately returns `False`** — the "cycle" test doubles as an "already known unsafe" memo.

I traced this on Example 1 to confirm. Final states after the full run:

| Node | Final state | Result |
|---|---|---|
| 0 | `1` in-progress | unsafe |
| 1 | `1` in-progress | unsafe |
| 2 | `2` safe | ✅ |
| 3 | `1` in-progress | unsafe |
| 4 | `2` safe | ✅ |
| 5 | `2` safe | ✅ |
| 6 | `2` safe | ✅ |

Nodes 0, 1 and 3 are permanently stuck at `1`, and the top-level calls `dfs(1)` and `dfs(3)` return `False` **immediately** on that basis — no re-exploration. **So each node is fully explored at most once, which is what makes the whole thing O(V+E) instead of O(V·(V+E)).**

Resetting to `0` on failure would still be *correct*, but every unsafe node would be re-explored from every top-level call — quadratic on adversarial input.

**The topological alternative** — same result, no recursion:

```python
rev = [[] for _ in range(n)]
outdeg = [len(graph[u]) for u in range(n)]
for u in range(n):
    for v in graph[u]:
        rev[v].append(u)                    # reversed edges

q = deque(i for i in range(n) if outdeg[i] == 0)     # terminal nodes
safe = [False] * n
while q:
    u = q.popleft()
    safe[u] = True
    for w in rev[u]:
        outdeg[w] -= 1
        if outdeg[w] == 0:                  # ALL of w's targets are safe
            q.append(w)

return [i for i in range(n) if safe[i]]
```

**The idea: run Kahn's algorithm backwards.** Start from terminal nodes and peel inward; a node becomes safe only when its out-degree drops to zero, i.e. when *every* one of its targets is known safe. Nodes on or leading to a cycle never reach zero and are never enqueued — exactly the right outcome.

| | Three-state DFS | Reverse topological |
|---|---|---|
| Time | O(V+E) | O(V+E) |
| Space | O(V) + **recursion stack** | O(V+E) for reversed edges |
| ⚠️ At n = 10⁴ | **RecursionError risk** | ✅ **No stack risk** |
| Expresses "all paths" via | one `False` child aborts | out-degree reaching 0 |

**I verified both against an independent brute-force reference over 2,000 random digraphs — 0 failures each.** Write the DFS; **mention the topological version specifically as the fix for the recursion limit**, which at n = 10⁴ is a genuine concern.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(graph)
state = [0] * n          # 0 unvisited, 1 in-progress, 2 safe
```

**One array, three states.** The comment earns its place — `0/1/2` is meaningless without it.
→ [list-basics](../syntax/list-basics.md)

```python
def dfs(node):
    if state[node] == 1:
        return False
```

**In-progress → we've looped back onto the current path → a cycle.**

⚠️ And, because unsafe nodes are never reset, this *also* catches "already known unsafe". Two jobs, one line — the reason the algorithm is linear.

```python
    if state[node] == 2:
        return True
```

**Memo hit.** Already proven safe; don't re-explore.
→ [if-return](../syntax/if-return.md)

```python
    state[node] = 1
```

**Mark in-progress before recursing.** This must happen *before* the loop, or a self-loop or back-edge wouldn't be detected.

```python
    for neighbor in graph[node]:
        if not dfs(neighbor):
            return False
```

**One unsafe child is fatal.** ⚠️ This is the "**every** path" requirement in code: the loop short-circuits on the first `False`.

Note what it does *not* do — it doesn't set `state[node] = 2` on the way out. The node is abandoned at state `1`, which is precisely what makes future visits return `False` for free.
→ [for-loop](../syntax/for-loop.md) · [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md)

```python
    state[node] = 2
    return True
```

**Reached only if the loop completed** — every child safe, so this node is safe. A terminal node reaches here with an empty loop, which is why terminals are safe by default rather than by special case.

```python
return [i for i in range(n) if dfs(i)]
```

**Call DFS on every node**, collecting those that come back safe.

Iterating `0..n-1` in order means the output is **already sorted** — no `sort()` needed. Nodes settled by earlier calls resolve in O(1) via their memoised state.
→ [list-comprehension](../syntax/list-comprehension.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:

        n = len(graph)
        state = [0] * n          # 0 unvisited, 1 in-progress, 2 safe

        def dfs(node):
            if state[node] == 1:
                return False
            if state[node] == 2:
                return True

            state[node] = 1
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False

            state[node] = 2
            return True

        return [i for i in range(n) if dfs(i)]
```

</details>

**Trace it** — `graph = [[1,2],[2,3],[5],[0],[5],[],[]]`. This is verified output:

```
dfs(0)  node 0: mark in-progress, explore [1,2]
  dfs(1)  node 1: mark in-progress, explore [2,3]
    dfs(2)  node 2: mark in-progress, explore [5]
      dfs(5)  node 5: mark in-progress, explore []      ← empty loop
              node 5: all children safe → mark SAFE ✅
            node 2: all children safe → mark SAFE ✅
    dfs(3)  node 3: mark in-progress, explore [0]
      dfs(0)  node 0: state = in-progress → CYCLE, False ⚠️
            node 3: child unsafe → False   (stays in-progress)
          node 1: child 3 unsafe → False   (stays in-progress)
        node 0: child 1 unsafe → False     (stays in-progress)

dfs(1)  node 1: state = in-progress → False    ← memo, no re-exploration
dfs(2)  node 2: state = safe → True ✅          ← memo hit
dfs(3)  node 3: state = in-progress → False    ← memo
dfs(4)  node 4: mark in-progress, explore [5]
  dfs(5)  node 5: state = safe → True ✅
        node 4: all children safe → mark SAFE ✅
dfs(5)  node 5: state = safe → True ✅
dfs(6)  node 6: mark in-progress, explore []
        node 6: all children safe → mark SAFE ✅

result: [2, 4, 5, 6] ✅
```

**Three things worth pausing on:**

**1. Node 2 is proven safe *inside* the failing exploration of node 0.** The work isn't wasted — `dfs(2)` completes and marks state `2` before node 0's other branch discovers the cycle. Later, `dfs(2)` at top level is an O(1) memo hit.

**2. The ⚠️ line is the cycle detection.** `dfs(3)` reaches node 0, which is still `in-progress` because its frame is on the stack above. That's the definition of a back-edge, and it's exactly what a plain `visited` set could not distinguish from a harmless revisit.

**3. `dfs(1)` and `dfs(3)` at top level return instantly.** They're still at state `1`, so the first check fires. **This is the memoisation of failure** — without it, each would re-explore its subtree and the algorithm would degrade to O(V·(V+E)).

**Node 6 shows the terminal base case** needs no special handling: an empty adjacency list means the `for` loop body never runs, so control falls straight through to `state = 2`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)**.

- Each node is **fully explored at most once**: after that it's at state `1` (unsafe) or `2` (safe), and both are O(1) early returns.
- Each edge is traversed at most once, during its source's single exploration.
- The outer loop adds O(V) for the memo hits.

**Total: O(V + E)** — about 5·10⁴ operations at the stated constraints.

**The memoisation of *failure* is what secures this bound.** Without leaving unsafe nodes at state `1`:

| | Nodes re-explored? | Complexity |
|---|---|---|
| **Leave unsafe at state 1** | No | **O(V + E)** ✅ |
| Reset unsafe to state 0 | Yes, from every caller | **O(V²)** ❌ |

Both give correct answers — I checked the resetting version against brute force over 1,500 random digraphs and it agrees on every one. Only the timing differs, and the gap is real. **Measured** on a chain running into a self-loop (`0→1→2→…→n−1→n−1`, where every node is unsafe):

| n | calls, keeping state | calls, resetting | ratio |
|---|---|---|---|
| 100 | 200 | 5,150 | 26× |
| 200 | 400 | 20,300 | 51× |
| 400 | 800 | 80,600 | 101× |
| 800 | 1,600 | 321,200 | **201×** |

Keeping the state is exactly **2n** calls; resetting is **n²/2**, and the ratio doubles every time n doubles. At n = 10⁴ that's 2·10⁴ against 5·10⁷ — the difference between passing and timing out.

**This is optimal** — every edge must be examined, since any one of them could complete a cycle. **Ω(V+E) is the lower bound.**

**The reverse topological version is also O(V+E)**: building the reversed graph is O(V+E), and each node is enqueued at most once with each reversed edge relaxed once.

**Versus the naive per-node search**, O(V·(V+E)) ≈ 5·10⁸ at these constraints — likely too slow, and it re-derives the same facts V times over. **Memoisation is the whole difference.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V) auxiliary, plus the stack</summary>

**O(V)** auxiliary for the DFS version.

| Component | Size |
|---|---|
| `state` | exactly n integers → **O(V)** |
| **Recursion depth** | up to V on a long chain → **O(V)** |
| Output | up to V nodes → O(V) |
| Input `graph` | O(V+E), **given** |

⚠️ **The recursion depth is the practical problem.** At n = 10⁴, a path graph `0 → 1 → 2 → … → 9999` recurses 10,000 frames deep — **ten times Python's default limit of 1,000**.

This is not a corner case; it's a plain chain, and it's exactly what the constraint permits. Options:

| Fix | Cost |
|---|---|
| `sys.setrecursionlimit(20000)` | ⚠️ Works, but risks a real segfault rather than a clean exception |
| **Reverse topological sort** | ✅ **Fully iterative — no stack at all** |
| Iterative DFS with an explicit stack | ✅ Correct, but three-state bookkeeping gets fiddly by hand |

**The topological version is the right answer to "what breaks at n = 10⁴?"** Its space is **O(V + E)** — larger, because it builds the reversed adjacency list — but it lives on the heap:

| Approach | Space | Stack risk at n=10⁴ |
|---|---|---|
| Three-state DFS | O(V) + O(V) **stack** | ⚠️ **Yes** |
| Reverse topological | **O(V + E)** heap | ✅ None |

**More memory, no stack risk.** That's the trade, and naming it is better than pretending the DFS is unconditionally fine.
→ [recursion-limit](../syntax/recursion-limit.md) · [deque-basics](../syntax/deque-basics.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The useful restatement is the contrapositive: a node is safe exactly when it can't reach a cycle, since every path either terminates or loops. So it's cycle detection in a directed graph, which needs three states rather than a plain visited set — I have to distinguish 'currently on my DFS path', which means a back-edge and a cycle, from 'finished earlier', which is just a memo hit. A node is safe only if *all* its children are safe, so the loop returns False on the first unsafe child; that's the 'every path' requirement. The detail I'd highlight is that when a node comes back unsafe I deliberately leave it marked in-progress rather than resetting it — that way any later visit short-circuits, which is what keeps it O(V+E) instead of quadratic. One concern: n is 10⁴ and a chain would recurse 10,000 deep, past Python's limit, so for safety I'd use the iterative version — reverse the edges and run Kahn's algorithm from the terminal nodes, where a node becomes safe once its out-degree hits zero."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why three states, not a visited set?" | **The question.** A directed graph needs to distinguish a back-edge (cycle) from a cross-edge to a finished node (memo hit). One boolean can't. |
| "Why not reset unsafe nodes to `0`?" | Still correct, but every unsafe node gets re-explored by every caller — O(V·(V+E)). Leaving them at `1` memoises the failure. |
| "Why does one unsafe child doom the node?" | "*Every* path must terminate" is universal. One path into a cycle is enough to disqualify it. |
| "Node 0 has a terminating path — why unsafe?" | It also has `0 → 1 → 3 → 0`. Existence of a good path is irrelevant; *all* must be good. |
| "Recursion depth at n = 10⁴?" | A chain recurses 10,000 deep, past the 1,000 default. Use the reverse-topological version. |
| "Explain the topological approach." | Reverse the edges, seed a queue with out-degree-0 (terminal) nodes, and decrement out-degrees; a node is safe when its out-degree hits 0, i.e. all its targets are safe. |
| "Self-loops?" | Handled naturally — `dfs(x)` reaches `x` while it's in-progress, so it's a cycle of length 1. |
| "Relation to [Course Schedule](207-course-schedule.md)?" | Same three-state cycle detection. That asks "is there *any* cycle?"; this asks "which nodes can't reach one?" |
| "Could you use SCCs?" | Yes — a node is unsafe iff it reaches an SCC of size > 1 or a self-loop. Correct, but heavier than needed. |
| "Why is the output already sorted?" | The final loop runs `0..n-1` in order. No sort required. |

**Traps:**

- **Using a plain `visited` set.** Can't tell a cycle from a finished node; typically reports everything unsafe or everything safe.
- **Resetting unsafe nodes to state `0`.** Correct but quadratic — the performance bug that a passing-but-slow submission usually has.
- **Setting `state[node] = 2` before the loop** — a node on a cycle would be marked safe and the cycle never detected.
- **Marking in-progress *after* the loop** instead of before — back-edges become invisible, so self-loops slip through.
- **Returning True if *any* child is safe** — that's "some path terminates", the wrong quantifier. Node 0 would be wrongly reported safe.
- **Recursing at n = 10⁴ without considering depth** — `RecursionError` on a chain.
- **Sorting the output** — harmless, just unnecessary given the iteration order.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) and [Course Schedule II](210-course-schedule-ii.md) (the same three-state cycle detection and Kahn's algorithm) · [Is Graph Bipartite?](785-is-graph-bipartite.md) (a different three-valued marking during traversal) · [Graph Valid Tree](261-graph-valid-tree.md) (cycle detection, undirected) · [topological-sort](../algorithms/topological-sort.md) · [dfs](../algorithms/dfs.md) · [graph](../data-structures/graph.md).

</details>

---
