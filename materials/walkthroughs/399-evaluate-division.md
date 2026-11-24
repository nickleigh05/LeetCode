# 399. Evaluate Division

**Medium** · [LeetCode](https://leetcode.com/problems/evaluate-division/) · [Solution file (no hints)](../../problems/0001-0499/399.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

You're given equations like `A / B = k` as `equations[i] = [A, B]` with `values[i] = k`. Each variable is a string. For every query `[C, D]`, return `C / D`, or `-1.0` if it can't be determined (including when a variable never appeared).

```
equations = [["a", "b"], ["b", "c"]],  values = [2.0, 3.0]
queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
→ [6.0, 0.5, -1.0, 1.0, -1.0]
      a/c = (a/b)·(b/c) = 2·3,   b/a = 1/2,   e is unknown,   a/a = 1,   x is unknown
```

**Constraints:** `1 <= equations.length <= 20` · `values[i] > 0` · `1 <= queries.length <= 20` · variables are short lowercase or digit strings

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `A / B = k` | A **weighted edge** `A → B` with weight `k`. And the reverse edge `B → A` has weight `1/k` |
| answer `C / D` from known equations | **Multiply the weights along a path** from `C` to `D`: `a/c = (a/b) · (b/c)` |
| `-1.0` when unknown | No path between them, or a variable that isn't in the graph at all |
| `a / a = 1` | A path of length 0, but only if `a` exists. `x / x = -1.0` when `x` was never seen |

So this is a **graph** problem: variables are nodes, each equation is a pair of directed edges with reciprocal weights, and a query is "find a path from C to D and multiply the weights".

Any path works, since the equations are consistent (the problem guarantees no contradictions). So a plain **DFS or BFS** is enough: no shortest-path logic.

🤔 **Before you open the next section:** for the equation `a / b = 2.0`, what weight goes on the edge `b → a`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time per query | Verdict |
|---|---|---|
| **Adjacency map + DFS/BFS per query** | O(V + E) | ✅ Simple, and queries and equations are small |
| Floyd-Warshall on the ratios | O(V³) once, O(1) per query | ✅ Works for tiny `V` |
| Weighted union-find | near O(1) | ✅ Elegant: store each node's ratio to its root |

**The decision: an adjacency map of `dict[str, dict[str, float]]` and a [DFS](../algorithms/dfs.md) per query.** With at most 20 equations and 20 queries it's well within limits, and it's the most direct translation of "multiply along a path".

Build the [graph](../data-structures/graph.md): for `A / B = k`, set `graph[A][B] = k` and `graph[B][A] = 1 / k`. A query `C / D` runs a DFS from `C`, tracking visited nodes so cycles terminate, returning the product of weights when it reaches `D`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
graph = defaultdict(dict)
for (a, b), value in zip(equations, values):
    graph[a][b] = value
    graph[b][a] = 1 / value
```

Each equation becomes two edges: `a → b` with weight `value`, and the reciprocal `b → a`. `defaultdict(dict)` creates a node's neighbour map the first time it appears.
→ [defaultdict](../syntax/defaultdict.md) · [zip-function](../syntax/zip-function.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [graph](../data-structures/graph.md)

```python
def dfs(current: str, target: str, visited: set) -> float:
    if current == target:
        return 1.0
    visited.add(current)
```

Find the product of weights from `current` to `target`, or `-1.0`. Reaching the target means "ratio of a thing to itself": `1.0`, the identity for multiplication. Mark `current` visited so cycles don't recurse forever.
→ [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md) · [set-basics](../syntax/set-basics.md)

```python
    for neighbour, weight in graph[current].items():
        if neighbour in visited:
            continue
        result = dfs(neighbour, target, visited)
        if result != -1.0:
            return weight * result
    return -1.0
```

Try each unvisited neighbour. If that branch finds the target, the answer is the edge weight times the rest of the path. If no branch finds it, report `-1.0`.
→ [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)

```python
answers = []
for c, d in queries:
    if c not in graph or d not in graph:
        answers.append(-1.0)
    else:
        answers.append(dfs(c, d, set()))
return answers
```

For each query, unknown variables answer `-1.0` straight away. That is also what makes `x / x` give `-1.0` when `x` never appeared, while `a / a` reaches the `current == target` case and gives `1.0`. Each DFS gets a fresh `visited` set.
→ [membership-operators](../syntax/membership-operators.md) · [list-methods](../syntax/list-methods.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import defaultdict


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)
        for (a, b), value in zip(equations, values):
            graph[a][b] = value
            graph[b][a] = 1 / value

        def dfs(current: str, target: str, visited: set) -> float:
            if current == target:
                return 1.0
            visited.add(current)
            for neighbour, weight in graph[current].items():
                if neighbour in visited:
                    continue
                result = dfs(neighbour, target, visited)
                if result != -1.0:
                    return weight * result
            return -1.0

        answers = []
        for c, d in queries:
            if c not in graph or d not in graph:
                answers.append(-1.0)
            else:
                answers.append(dfs(c, d, set()))
        return answers
```

</details>

**Trace it.** Graph: `a→b 2`, `b→a 0.5`, `b→c 3`, `c→b 1/3`. Query `a / c`:

| Step | Position | Action |
|---|---|---|
| `dfs(a, c)` | a | neighbour `b`, weight 2 |
| `dfs(b, c)` | b | neighbours: `a` visited, skip. `c`, weight 3 |
| `dfs(c, c)` | c | `current == target`, return `1.0` |
| back in `b` | | return `3 × 1.0 = 3.0` |
| back in `a` | | return `2 × 3.0 = ` **6.0** ✅ |

Query `b / a`: one edge, weight `0.5` ✅. Query `a / e`: `e` isn't in the graph, so `-1.0` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(Q · (V + E))</summary>

Building the graph is **O(E)**. Each query does one DFS over at most `V` nodes and `2E` edges: **O(V + E)**. With `Q` queries: **O(Q · (V + E))**. With `E, Q <= 20` that's trivial.

Weighted union-find reduces queries to near O(1) after an O(E α) build.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E)** for the adjacency map, plus O(V) for the `visited` set and the recursion stack during a query.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each equation `A/B = k` is a weighted edge A→B with weight k and a reverse edge B→A with weight 1/k. A query C/D is then the product of the weights along any path from C to D, since the equations are consistent. So I build an adjacency map and run a DFS per query with a visited set, multiplying as I return. Unknown variables return -1.0. Building is O(E) and each query is O(V + E), which is tiny here. If there were many queries I'd use weighted union-find."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Many queries?" | **Weighted union-find**: each node stores its ratio to its root, so `C/D = ratio[C] / ratio[D]` when they share a root. Near O(1) per query |
| "Precompute all answers?" | Floyd-Warshall on the ratio matrix, O(V³). Only good for small `V` |
| "BFS instead of DFS?" | Equivalent. Carry the running product in the queue |
| "Contradictory equations?" | The problem rules this out. In general, detect when a cycle's product isn't 1 |
| "Why `1 / value` and not `values`'s opposite?" | `B / A = 1 / (A / B)` |

**Traps:**

- **Only adding the forward edge.** `b / a` then returns `-1.0`.
- **Returning `1.0` for an unknown `x / x`.** Check membership in the graph first.
- **Sharing one `visited` set across queries.** Each query needs a fresh one.
- **Using `if result:`** to test success. `0` can't occur, but compare with `-1.0` explicitly so intent is clear.

**This same move shows up in:** [Clone Graph](133-clone-graph.md) (build an adjacency structure, then traverse) · [Number of Provinces](547-number-of-provinces.md) · [Accounts Merge](721-accounts-merge.md) (union-find on relationships).

</details>

---
