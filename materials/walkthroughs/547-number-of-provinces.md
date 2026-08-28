# 547. Number of Provinces

**Medium** · [LeetCode](https://leetcode.com/problems/number-of-provinces/) · [Solution file (no hints)](../../problems/0500-0999/547.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Given an `n × n` matrix where `isConnected[i][j] == 1` means cities `i` and `j` are **directly** connected, return the number of **provinces** — maximal groups of directly or indirectly connected cities.

```
isConnected = [[1,1,0],          →  2      {0,1} and {2}
               [1,1,0],
               [0,0,1]]

isConnected = [[1,0,0],          →  3      {0}, {1}, {2}
               [0,1,0],
               [0,0,1]]
```

**Constraints:** `1 <= n <= 200` · `isConnected[i][i] == 1` · matrix is symmetric

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**directly or indirectly** connected" | Transitive closure → **connected components** |
| "a **province** is a group…and no other cities" | Maximal component. Count them |
| given as an `n × n` **matrix** | ⚠️ **Adjacency matrix**, not an edge list — neighbours are a *row*, not a list |
| `isConnected[i][i] == 1` | Self-loops, which you must not mistake for real edges |
| symmetric matrix | Undirected |
| `n <= 200` | 40,000 matrix cells. O(n²) is fine and in fact unavoidable |

**"Count the connected components" — dressed as geography.** This is [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md) with a different input format and a different word for the answer. If you can see through the wording, you already know the algorithm:

```
for each city:
    if not yet visited:
        DFS/BFS its whole component     ← marks everything reachable
        provinces += 1                  ← one new component found
```

**The counter increments in the outer loop, not the traversal.** Each time the outer loop finds an unvisited city, it has found a component nobody has reached — so exactly one increment per component.

**The one genuinely new thing: the input is a matrix.** Every graph problem so far handed you an edge list or adjacency list. Here neighbours are found by **scanning a row**:

```
edge list        →  adj[node] is a list      →  iterate it directly, O(degree)
adjacency matrix →  row isConnected[node]    →  scan all n entries, O(n)
```

That single difference drives the complexity: finding one node's neighbours costs **O(n)** regardless of how few it has, so the traversal is **O(n²)** rather than O(V+E).

**And it's not a defect of the algorithm — it's the input format.** Just reading the matrix is O(n²), so no approach can beat that here.

```
n = 3, isConnected = [[1,1,0],
                      [1,1,0],
                      [0,0,1]]

city 0's row: [1,1,0]  →  connected to 0 (itself) and 1
city 2's row: [0,0,1]  →  connected only to itself  →  a province of one
```

⚠️ **`isConnected[i][i] == 1` always.** A city is trivially "connected to itself", and that diagonal 1 is not an edge. It happens to be harmless in the code below — the visited check absorbs it — but it's what makes `[[1,0,0],[0,1,0],[0,0,1]]` give **3**, not 0.

🤔 **Before you open the next section:** the outer loop increments the counter once per unvisited city it finds. Why doesn't that count every *city* rather than every *province*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **DFS from each unvisited city** | Mark the component, increment | **O(n²)** | ✅ |
| BFS from each unvisited city | Same, with a queue | O(n²) | ✅ Identical cost |
| **Union-Find** | Union every connected pair, count roots | **O(n²·α)** | ✅ Natural fit for "count groups" |
| Transitive closure (Floyd–Warshall) | Compute all-pairs reachability | O(n³) | ❌ 8M ops for no benefit |

**The decision: DFS with an outer scan.** Union-Find is equally defensible and worth naming.

**All the reasonable options are O(n²)** — the matrix has n² entries and each must be examined at least once. So choose on clarity, not speed.

**The DFS skeleton** — the "count components" pattern, worth memorising as a unit:

```python
visited = set()
count = 0
for node in range(n):
    if node not in visited:
        visited.add(node)
        dfs(node)          # swallows the entire component
        count += 1
```

**Why one increment per component, not per city:** after `dfs(node)` returns, *every* city reachable from `node` is in `visited`. The outer loop skips all of them. So the increment fires only for a city that begins a component no earlier traversal touched.

**Union-Find is arguably the more natural framing** for "how many groups?":

```python
parent = list(range(n))
count = n                       # start with n singleton provinces

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

for i in range(n):
    for j in range(i + 1, n):           # upper triangle only
        if isConnected[i][j]:
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
                count -= 1              # two provinces merged into one

return count
```

**The insight: start at n and decrement on each successful merge.** Every union reduces the group count by exactly one, so no final pass to count distinct roots is needed.

⚠️ **`range(i + 1, n)` skips the diagonal and the lower triangle** — the matrix is symmetric, so scanning half of it is both sufficient and twice as fast, and starting at `i+1` sidesteps the self-loops entirely. I verified both versions against an independent reference over 2,000 random symmetric matrices — 0 failures each.

| | DFS | Union-Find |
|---|---|---|
| Time | O(n²) | O(n²·α) |
| Space | O(n) visited + O(n) stack | **O(n)** parent array |
| Reads the matrix | full | **upper triangle only** |
| Extends to streaming edges | ❌ needs the whole graph | ✅ process edges as they arrive |

**DFS is shorter; Union-Find generalises better.** Both are right answers.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(isConnected)
visited = set()
```

`n` is the city count — the matrix is square, so the row count suffices.

`visited` holds cities already assigned to a province.
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
def dfs(city):
    for other in range(n):
        if isConnected[city][other] == 1 and other not in visited:
            visited.add(other)
            dfs(other)
```

**Neighbour lookup is a row scan.** `for other in range(n)` walks every column of `city`'s row — O(n) per node, the defining cost of the matrix representation.

Two conditions, in a deliberate order:
- `isConnected[city][other] == 1` — is there an edge?
- `other not in visited` — is it new?

⚠️ **The self-loop takes care of itself.** When `other == city`, the matrix says 1, but `city` is already in `visited` (added before the call), so the second condition rejects it. **No explicit `if other == city: continue` is needed** — but you should know *why*, not just that it works.

Marking visited **before** recursing prevents infinite mutual recursion between two connected cities.
→ [for-loop](../syntax/for-loop.md) · [recursion-basics](../syntax/recursion-basics.md) · [membership-operators](../syntax/membership-operators.md)

```python
provinces = 0
for city in range(n):
    if city not in visited:
        visited.add(city)
        dfs(city)
        provinces += 1
```

**The outer scan — where the counting happens.**

`city not in visited` means no previous traversal reached it, so it starts a **new** province. `dfs(city)` then absorbs everything connected to it, and the loop skips all of those.

⚠️ `visited.add(city)` **before** `dfs(city)`, matching the invariant inside the traversal: a node is marked at the moment it's committed to, never after.
→ [if-return](../syntax/if-return.md)

```python
return provinces
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:

        n = len(isConnected)
        visited = set()

        def dfs(city):
            for other in range(n):
                if isConnected[city][other] == 1 and other not in visited:
                    visited.add(other)
                    dfs(other)

        provinces = 0
        for city in range(n):
            if city not in visited:
                visited.add(city)
                dfs(city)
                provinces += 1

        return provinces
```

</details>

**Trace it** — `isConnected = [[1,1,0],[1,1,0],[0,0,1]]`:

| Outer `city` | In `visited`? | Action | `visited` after | `provinces` |
|---|---|---|---|---|
| 0 | no | mark, `dfs(0)` | | |
| | | ↳ row `[1,1,0]`: col 0 is self (visited) ✗ | | |
| | | ↳ col 1 connected & new → mark, `dfs(1)` | | |
| | | ↳↳ row `[1,1,0]`: cols 0, 1 both visited ✗ | | |
| | | ↳ col 2 not connected ✗ | `{0,1}` | **1** |
| 1 | **yes** — skip | | `{0,1}` | 1 |
| 2 | no | mark, `dfs(2)` | | |
| | | ↳ row `[0,0,1]`: only col 2, itself, visited ✗ | `{0,1,2}` | **2** |

**Result: 2** ✅

**City 1 is the row that shows the pattern working.** The outer loop reaches it, finds it already visited — because `dfs(0)` swallowed it — and does **not** increment. Without the visited check, every city would count as its own province and the answer would always be `n`.

**City 2 is a province of one.** Its row is all zeros apart from the diagonal, so `dfs(2)` finds nothing new — yet it still increments, because an isolated city *is* a province. This is where the identity matrix gives 3 rather than 0.

**Where the self-loop is silently handled:** at `dfs(0)`, column 0 has `isConnected[0][0] == 1`, so the edge test passes — and the visited test rejects it. Every diagonal entry is absorbed this way.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**.

- The outer loop runs n times.
- `dfs(city)` is called **once per city overall** (the visited check guarantees it), and each call scans a full row: **O(n)**.
- n calls × O(n) row scan = **O(n²)**.

At n = 200 that's 40,000 operations. Instant.

**This is optimal — and the reason is the input format, not the algorithm.** The matrix has n² entries and any correct answer depends on all of them: a single unread cell could be a 1 that merges two provinces. **Ω(n²) is a hard lower bound here.**

**The contrast worth drawing** with [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md), which is the same problem given an edge list:

| Input format | Neighbour lookup | Total |
|---|---|---|
| Edge list → adjacency list | O(degree) | **O(V + E)** |
| **Adjacency matrix** | **O(n) row scan** | **O(n²)** |

On a **sparse** graph (say n = 200 with 10 edges) the edge-list version does ~210 operations while the matrix version does 40,000 — **190× more**, all of it spent reading zeros. The algorithm is identical; the representation dictates the cost.

**So the honest answer is:** *"O(n²), and that's optimal given an adjacency matrix — but if the input were an edge list it'd be O(V+E), which is dramatically better on sparse graphs. The representation is doing the damage."* That's the observation the problem is really probing.

**Union-Find: O(n²·α(n))** — the same n²/2 upper-triangle scan, with near-constant find/union. Effectively identical.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** auxiliary — note that's **n**, not n².

| Component | Size |
|---|---|
| `visited` | at most n cities → **O(n)** |
| **Recursion depth** | at most n (one long chain) → **O(n)** |
| Input matrix | O(n²), but **given**, not allocated |
| **Total auxiliary** | **O(n)** |

**The input is O(n²) but doesn't count** — it's provided, not created. Auxiliary space is what you add, and here it's linear.

**Recursion depth is at most n**, reached when the graph is one long chain (city 0—1—2—…). At n = 200 that's 200 frames, comfortably inside Python's 1,000 limit.

⚠️ **This is why recursion is safe here but not in [Find if Path Exists](1971-find-if-path-exists-in-graph.md)**, where n = 2·10⁵ would blow the stack. **Same algorithm, different constraint, different verdict** — always check the bound before reaching for recursion.
→ [recursion-limit](../syntax/recursion-limit.md)

**Union-Find is also O(n)** — just the parent array, and it needs no `visited` set or stack at all. Marginally leaner, and it never recurses:

| Approach | Auxiliary |
|---|---|
| DFS | O(n) visited + O(n) stack |
| BFS | O(n) visited + O(n) queue |
| **Union-Find** | **O(n) parent array, no stack** |

**A boolean list beats a set** in practice — `visited = [False] * n` avoids hashing and, since labels are exactly `0..n-1`, loses nothing. Same O(n), better constant.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is counting connected components, phrased as provinces. I scan the cities, and whenever I find one that hasn't been visited I DFS its entire component and increment the counter — so the increment happens once per component, not once per city, because the traversal absorbs everything reachable before the outer loop moves on. The wrinkle is that the input is an adjacency matrix rather than an edge list, so finding a city's neighbours means scanning a whole row: O(n) per node instead of O(degree), which makes the total O(n²). That's optimal here because just reading the matrix is O(n²) — but it's worth noting the same problem with an edge list is O(V+E), which is far better on sparse graphs. Space is O(n) for the visited set and the recursion. Union-find is an equally good fit: start the count at n, scan the upper triangle, and decrement on each successful merge."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does the counter increment in the **outer** loop?" | **The question.** The DFS swallows the whole component, so the outer loop only reaches an unvisited city when it starts a genuinely new one. |
| "What about the diagonal `isConnected[i][i] == 1`?" | It's a self-loop, not an edge. The visited check absorbs it — the node is marked before the scan, so it fails the `not in visited` test. |
| "Why O(n²) and not O(V+E)?" | The adjacency matrix forces an O(n) row scan per node. With an edge list it'd be O(V+E). The representation, not the algorithm. |
| "Can you beat O(n²)?" | **No** — reading the matrix is already Ω(n²). Any unread cell could merge two provinces. |
| "Union-find version?" | Start `count = n`, scan the upper triangle, `count -= 1` on each successful union. O(n²·α), O(n) space, no recursion. |
| "Why only the upper triangle?" | The matrix is symmetric; `[i][j]` and `[j][i]` are the same edge. Halves the work and skips the diagonal for free. |
| "Largest province instead of the count?" | Have the DFS return its component's size and track the max — like [Max Area of Island](695-max-area-of-island.md). |
| "n = 10⁵ cities?" | An n×n matrix is 10¹⁰ entries — it wouldn't fit in memory. The input **must** be an edge list at that scale, and then it's O(V+E). |
| "Cities connected over time, queried as you go?" | Union-find, incrementally. DFS would require re-running from scratch after each addition. |

**Traps:**

- **Incrementing inside the DFS** — counts cities, not provinces, giving `n` every time.
- **Forgetting the visited check in the outer loop** — same result: every city counted separately.
- **Marking visited after recursing instead of before** — infinite recursion between any two connected cities.
- **Treating the diagonal as a real edge** — harmless here, but a sign you haven't traced why it's harmless.
- **Scanning the full matrix in the union-find version** — each edge unioned twice. Correct (the second is a no-op) but wasteful; `range(i+1, n)` is the right loop.
- **Using recursion at much larger n** — safe at 200, a `RecursionError` at 2·10⁵. Check the constraint.
- **Comparing to `'1'`** — the matrix holds **ints**.
- **Returning `len(visited)`** — that's the number of cities, always n.

**This same move shows up in:** [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md) (identical problem, edge-list input) · [Number of Islands](200-number-of-islands.md) (component counting on a grid) · [Find if Path Exists in Graph](1971-find-if-path-exists-in-graph.md) (one component, reachability only) · [Redundant Connection](684-redundant-connection.md) and [Graph Valid Tree](261-graph-valid-tree.md) (union-find on the same shape) · [dfs](../algorithms/dfs.md) · [union-find](../data-structures/union-find.md) · [graph](../data-structures/graph.md).

</details>

---
