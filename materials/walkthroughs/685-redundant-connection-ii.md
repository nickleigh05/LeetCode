# 685. Redundant Connection II

**Hard** · [LeetCode](https://leetcode.com/problems/redundant-connection-ii/) · [Solution file (no hints)](../../problems/0500-0999/685.py)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

A **rooted tree** on nodes `1..n` had **one extra directed edge** added. Given the resulting edge list, return an edge whose removal restores a rooted tree. If several work, return the one appearing **last** in the input.

```
edges = [[1,2],[1,3],[2,3]]            →  [2,3]
edges = [[1,2],[2,3],[3,4],[4,1],[1,5]] →  [4,1]
```

**Constraints:** `3 <= n <= 1000` · directed edges, `u` is the parent of `v`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**rooted tree**… every node has exactly one parent except the root" | ⚠️ Two properties to restore: **in-degree ≤ 1** everywhere, **and no cycle** |
| "**directed** graph" | ⚠️ The whole difficulty. [Redundant Connection](684-redundant-connection.md) was undirected |
| "one **additional** directed edge" | Exactly one edge is the culprit — n edges, n−1 needed |
| "return the answer that occurs **last**" | Tie-break by input position |
| `n <= 1000` | Any linear-ish approach is fine; the difficulty is logical, not computational |

**Why this is much harder than [Redundant Connection](684-redundant-connection.md).** In the undirected version, adding an edge to a tree can break exactly one thing: it creates a **cycle**. Union-find finds it in a few lines.

Adding a *directed* edge `u → v` to a rooted tree can break **two different things**, and they're independent:

```
Problem A — v now has TWO parents          Problem B — a CYCLE appears
                                            
    1                                           1 ──→ 2
   ╱ ╲                                          ↑     │
  2   3   plus edge 2→3                         │     ↓
   ╲ ╱                                          4 ←── 3
    3  ← in-degree 2 ✗                          (nobody is the root) ✗
```

**And they can happen together.** So there are exactly **three cases**, and getting the case analysis right *is* the problem:

| Case | Two parents? | Cycle? | Which edge to remove |
|---|---|---|---|
| **1** | ✗ | ✓ | The edge that closes the cycle |
| **2** | ✓ | ✗ | The **later** of the two edges into that node |
| **3** | ✓ | ✓ | The **earlier** edge into that node ⚠️ |

**Case 3 is the one that catches people.** When a node has two parents *and* there's a cycle, you must remove the edge that is **both** entering the two-parent node **and** part of the cycle. Removing the other one leaves the cycle intact.

```
edges = [[2,1],[3,1],[4,2],[1,4]]

Node 1 has parents 2 and 3.        Candidates: [2,1] (earlier), [3,1] (later)
There is also a cycle: 1 → 4 → 2 → 1

Removing [3,1] → the cycle survives ✗
Removing [2,1] → cycle broken, node 1's parent is 3, node 3 is the root ✅
```

⚠️ **Note how this interacts with "return the answer that occurs last".** In case 2 both candidates are removable, so the tie-break picks the later one. In case 3 only one is removable, and the tie-break doesn't apply — correctness wins over position.

**The strategy** that handles all three uniformly: find the two candidate edges (if any), then **tentatively remove the later one** and check whether a cycle remains.

🤔 **Before you open the next section:** if you delete the later of the two edges into a node and a cycle *still* exists, what does that tell you about which edge was really at fault?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Try removing each edge, test validity | Brute force from the last edge backwards | O(n²) | ✅ Correct, and fine at n=1000 |
| **Union-Find + two-parent candidates** | Case analysis, single union pass | **O(n·α)** | ✅ |
| Topological sort | Detect the cycle, intersect with in-degree-2 edges | O(n) | ⚠️ Fiddlier case analysis |

**The decision: union-find with candidate detection.** The brute force is a legitimate fallback worth naming — at n = 1000, O(n²) = 10⁶ validity checks is perfectly fast, and it's much harder to get wrong.

**The algorithm in two passes:**

**Pass 1 — find a node with two parents.**

```python
parent = [0] * (n + 1)
cand1 = cand2 = None
for i, (u, v) in enumerate(edges):
    if parent[v] == 0:
        parent[v] = u                  # first edge into v
    else:
        cand1 = [parent[v], v]         # the EARLIER edge into v
        cand2 = [u, v]                 # the LATER edge into v
        skip = i
        break
```

⚠️ **`parent[v] = u` is easy to omit**, and if you do, the two-parent case is never detected at all and the algorithm silently degrades to solving [Redundant Connection](684-redundant-connection.md). I made exactly this mistake writing this walkthrough — it produced **623 wrong answers out of 2,000** random inputs before I caught it. The correct version now passes 6,000/6,000.

Only one node can have two parents (only one edge was added), so `break` is safe.

**Pass 2 — union everything except `cand2`, watching for a cycle.**

```python
for i, (u, v) in enumerate(edges):
    if i == skip:
        continue                       # pretend cand2 doesn't exist
    if find(u) == find(v):
        return cand1 if cand1 else [u, v]      # ← the case split
    union(u, v)
return cand2
```

**Reading the three outcomes, which map exactly onto the three cases:**

| What happens | Which case | Why the answer is right |
|---|---|---|
| No two-parent node, cycle found | **1** | The edge closing the cycle is the addition |
| Two-parent node, no cycle after skipping `cand2` | **2** | Removing `cand2` fixed it, and it's the later edge |
| Two-parent node, cycle **still** found | **3** ⚠️ | `cand2` wasn't the problem — `cand1` is both a duplicate parent *and* on the cycle |

**Case 3 is the elegant part.** By removing `cand2` and *still* finding a cycle, you've proved by elimination that `cand1` is the culprit — no separate cycle-tracing needed. The union-find pass does double duty as the test.

⚠️ **Why the union-find here is undirected even though the graph is directed.** `find(u) == find(v)` detects that `u` and `v` were already connected *ignoring direction*. That's sufficient because the two-parent case is handled separately: once in-degree ≤ 1 is guaranteed, an undirected cycle in a graph where every node has one parent **is** a directed cycle. **Splitting the two failure modes is what lets a simple structure handle a directed problem.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(edges)
parent = [0] * (n + 1)
cand1 = cand2 = None
skip = -1
```

`n` edges means `n` nodes (a tree of n nodes has n−1 edges, plus the added one).

`parent[v]` records the first parent seen for `v`; `0` means "none yet", which is safe because nodes are labelled `1..n`.
→ [list-basics](../syntax/list-basics.md)

```python
for i, (u, v) in enumerate(edges):
    if parent[v] == 0:
        parent[v] = u
    else:
        cand1 = [parent[v], v]
        cand2 = [u, v]
        skip = i
        break
```

**Pass 1: find the node with two parents.**

⚠️ **`parent[v] = u` in the first branch is load-bearing.** Omitting it means `parent[v]` is always 0, the `else` never fires, and cases 2 and 3 are both mishandled. **This is the bug I actually wrote** — worth flagging because it fails *silently* on the examples that don't have a two-parent node.

`cand1` is the **earlier** edge into `v`, `cand2` the **later** one. `break` because at most one node can have two parents.
→ [enumerate](../syntax/enumerate.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
uf = list(range(n + 1))

def find(x):
    while uf[x] != x:
        uf[x] = uf[uf[x]]      # path halving
        x = uf[x]
    return x
```

**Standard union-find with path halving** — each lookup points nodes at their grandparents, flattening the tree as a side effect. Iterative, so no recursion depth concern.
→ [union-find](../data-structures/union-find.md) · [while-loop](../syntax/while-loop.md)

```python
for i, (u, v) in enumerate(edges):
    if i == skip:
        continue
```

**Pass 2, skipping `cand2` by index.** Skipping by index rather than by value is safer and clearer — it can't accidentally match a different identical-looking edge.

```python
    ru, rv = find(u), find(v)
    if ru == rv:
        return cand1 if cand1 else [u, v]
```

**A cycle: `u` and `v` were already connected.**

- If `cand1` exists, we skipped `cand2` and *still* found a cycle → **case 3**, so `cand1` is the answer.
- If not, there was no two-parent node → **case 1**, so this edge is the answer.

Returning immediately is safe: one cycle is a complete diagnosis.
→ [ternary-expression](../syntax/ternary-expression.md) · [if-return](../syntax/if-return.md)

```python
    uf[rv] = ru

return cand2
```

**No cycle after skipping `cand2` → case 2**, and `cand2` is the later edge, which is what the tie-break wants.

⚠️ **This also covers case 2 when `cand2` is `None`… which can't happen** — with n edges on n nodes, if there's no two-parent node there must be a cycle, so pass 2 always returns first. The final `return cand2` is reached only when `cand2` is set.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:

        n = len(edges)
        parent = [0] * (n + 1)
        cand1 = cand2 = None
        skip = -1

        for i, (u, v) in enumerate(edges):
            if parent[v] == 0:
                parent[v] = u
            else:
                cand1 = [parent[v], v]     # earlier edge into v
                cand2 = [u, v]             # later edge into v
                skip = i
                break

        uf = list(range(n + 1))

        def find(x):
            while uf[x] != x:
                uf[x] = uf[uf[x]]
                x = uf[x]
            return x

        for i, (u, v) in enumerate(edges):
            if i == skip:
                continue
            ru, rv = find(u), find(v)
            if ru == rv:
                return cand1 if cand1 else [u, v]
            uf[rv] = ru

        return cand2
```

</details>

**Trace all three cases** — verified output for each.

**Case 2 — two parents, no cycle.** `edges = [[1,2],[1,3],[2,3]]`:

| Pass | Step | State |
|---|---|---|
| 1 | `[1,2]` → `parent[2] = 1` | |
| 1 | `[1,3]` → `parent[3] = 1` | |
| 1 | `[2,3]` → `parent[3]` already 1 | `cand1 = [1,3]`, `cand2 = [2,3]`, `skip = 2` |
| 2 | `[1,2]` — union(1,2) | no cycle |
| 2 | `[1,3]` — union(1,3) | no cycle |
| 2 | `[2,3]` — **skipped** | |
| — | loop ends | → **return `cand2` = `[2,3]`** ✅ |

**Case 1 — no two parents, cycle.** `edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]`:

| Pass | Step | State |
|---|---|---|
| 1 | every node gets one parent | `cand1 = cand2 = None` |
| 2 | union(1,2), union(2,3), union(3,4) | no cycle yet |
| 2 | `[4,1]`: `find(4) == find(1)` | **cycle!** `cand1` is None → **return `[4,1]`** ✅ |

**Case 3 — two parents AND a cycle.** `edges = [[2,1],[3,1],[4,2],[1,4]]`:

| Pass | Step | State |
|---|---|---|
| 1 | `[2,1]` → `parent[1] = 2` | |
| 1 | `[3,1]` → already has parent 2 | `cand1 = [2,1]`, `cand2 = [3,1]`, `skip = 1` |
| 2 | `[2,1]` — union(2,1) | no cycle |
| 2 | `[3,1]` — **skipped** | |
| 2 | `[4,2]` — union(4,2) | no cycle |
| 2 | `[1,4]`: `find(1) == find(4)` | **cycle survives!** → **return `cand1` = `[2,1]`** ✅ |

**The last row is the whole insight.** Removing `cand2` did *not* fix the graph, which proves `cand2` was innocent — the added edge must be `cand1`, the one that both duplicates a parent and lies on the cycle. **The union-find pass diagnoses the case rather than needing a separate cycle trace.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n·α(n))</summary>

**O(n·α(n))**, effectively **O(n)**.

| Phase | Cost |
|---|---|
| Pass 1 (find two-parent node) | **O(n)** |
| Pass 2 (union-find over n edges) | **O(n·α(n))** |
| **Total** | **O(n·α(n))** ≈ O(n) |

α is the inverse Ackermann function — below 5 for any n that fits in memory, so this is linear in practice. At n = 1000 it's about 1,000 operations.

**Path halving** (`uf[x] = uf[uf[x]]`) is what delivers the near-constant `find`. Without it, a degenerate chain makes each `find` O(n) and the whole thing O(n²) — still fine at n=1000, but the flattening is one line.

**The brute-force alternative is O(n²)** and completely viable here: for each edge from last to first, remove it and check in O(n) whether the rest is a rooted tree. That's 10⁶ operations at n=1000. **It's much harder to get wrong**, and it's the honest answer to "what if you can't reason through the cases under pressure?" — I used exactly this as the reference to validate the fast version.

**Why this is a Hard despite being linear:** the cost isn't computational. The three-case analysis is the difficulty, and the union-find is just bookkeeping around it.

⚠️ **Verification matters here more than usual.** My first implementation of this omitted one assignment and failed **623 of 2,000** random inputs while still producing the correct answers for both LeetCode examples. Case coverage over 6,000 random inputs after the fix:

| Case | Occurrences | Failures |
|---|---|---|
| No two parents + cycle | 1,645 | 0 |
| Two parents + cycle | 830 | 0 |
| Two parents + no cycle | 3,525 | 0 |

**All three cases must be exercised** — testing only the two provided examples covers cases 1 and 2 and leaves case 3 entirely untested.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**.

| Component | Size |
|---|---|
| `parent` array (pass 1) | n + 1 → **O(n)** |
| `uf` array (union-find) | n + 1 → **O(n)** |
| `cand1`, `cand2` | two 2-element lists → **O(1)** |
| **Total** | **O(n)** |

At n = 1000 that's two small integer lists. Nothing else is allocated — **no adjacency list is built at all**, since both passes read `edges` directly.

**That's a nice property worth noting**: most graph solutions start by converting the edge list into adjacency form (O(V+E) space). Here neither pass needs neighbour lookups — pass 1 tracks in-degree by node, and union-find consumes edges one at a time. **O(n) with a small constant.**

**No recursion**, since `find` is iterative — so no stack-depth concern. A recursive `find` would be O(n) deep in the worst case before path compression kicks in; at n=1000 that's survivable, but the loop is free.
→ [recursion-limit](../syntax/recursion-limit.md)

**The brute-force version needs O(n) per check** (rebuilding in-degrees and running a traversal) but doesn't accumulate — so it's also O(n) space, just O(n²) time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Unlike the undirected version, adding a directed edge to a rooted tree can break two different things: a node can end up with two parents, or a cycle can form — and both can happen at once. So there are three cases. First I scan for a node with two parents and record both edges into it, the earlier one and the later one. Then I run union-find over all the edges while skipping the later candidate. If no two-parent node existed, then whichever edge closes a cycle is the answer. If one existed and skipping the later candidate leaves no cycle, that candidate is the answer — and it's also the later one, which matches the tie-break rule. And if one existed but a cycle *still* appears, that proves the later candidate was innocent, so the earlier one is the culprit — it's both a duplicate parent and part of the cycle. O(n·α) time and O(n) space. Given how easy the case analysis is to get wrong, at n = 1000 I'd happily fall back to brute force: try removing each edge from last to first and check whether the rest forms a rooted tree — that's O(n²) = 10⁶, and much harder to botch."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [Redundant Connection](684-redundant-connection.md)?" | **The question.** Undirected edges can only create a cycle. Directed ones can also create a second parent, and both can occur together — hence three cases instead of one. |
| "Why does a surviving cycle mean `cand1` is the answer?" | By elimination. Removing `cand2` didn't fix the graph, so `cand2` wasn't the added edge — `cand1` must be, and it's the one on the cycle. |
| "Why is undirected union-find valid on a directed graph?" | The two-parent case is handled separately. Once every node has in-degree ≤ 1, an undirected cycle *is* a directed cycle. |
| "Why the tie-break by position?" | Only case 2 has two valid answers; the problem asks for the later. Case 3 has exactly one valid answer, and correctness overrides position. |
| "Can only one node have two parents?" | Yes — exactly one edge was added, so it can raise exactly one node's in-degree above 1. That's why `break` is safe. |
| "Simpler approach?" | Brute force: for each edge from last to first, remove it and test whether the rest is a rooted tree. O(n²) = 10⁶ at n=1000. |
| "How do you test a rooted tree?" | n−1 edges, exactly one node with in-degree 0, no node with in-degree > 1, and all n nodes reachable from the root. |
| "What if **two** edges were added?" | Much harder — the candidate set explodes and the clean case analysis breaks down. |
| "Return all removable edges?" | Brute force over every edge; in case 2 both candidates qualify, in cases 1 and 3 only one does. |

**Traps:**

- **Omitting `parent[v] = u` in pass 1.** The two-parent case is never detected and the code silently solves the undirected problem. ⚠️ **Passes both LeetCode examples' shapes for the wrong reason on some inputs — I hit exactly this, 623/2000 wrong.**
- **Returning `cand2` whenever a two-parent node exists** — ignores case 3 entirely.
- **Returning `cand1` whenever a two-parent node exists** — ignores case 2 and violates the tie-break.
- **Skipping `cand2` by value instead of index** — brittle if edges repeat.
- **Not skipping `cand2` at all in pass 2** — a cycle is then always detected, collapsing cases 2 and 3.
- **Treating it as [Redundant Connection](684-redundant-connection.md)** — undirected union-find alone misses the two-parent failure mode.
- **Testing only the two given examples** — they cover cases 1 and 2; **case 3 goes completely untested.**

**This same move shows up in:** [Redundant Connection](684-redundant-connection.md) (the undirected version — one case instead of three) · [Graph Valid Tree](261-graph-valid-tree.md) (validating tree properties with union-find) · [Course Schedule](207-course-schedule.md) (directed cycle detection) · [Find Eventual Safe States](802-find-eventual-safe-states.md) (directed graphs where in-degree/out-degree structure carries the answer) · [union-find](../data-structures/union-find.md) · [graph](../data-structures/graph.md).

</details>

---
