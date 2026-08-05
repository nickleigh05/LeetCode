# 207. Course Schedule

**Medium** · [LeetCode](https://leetcode.com/problems/course-schedule/) · [Solution file (no hints)](../../problems/0001-0499/207.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

There are `numCourses` courses labelled `0` to `numCourses - 1`. You're given `prerequisites` where `prerequisites[i] = [aᵢ, bᵢ]` means **you must take course `bᵢ` first** in order to take course `aᵢ`.

Return `true` if you can finish all courses.

```
numCourses = 2, prerequisites = [[1,0]]        →  true
   take 0, then 1

numCourses = 2, prerequisites = [[1,0],[0,1]]  →  false
   1 needs 0, and 0 needs 1 — a cycle, so neither can ever start
```

**Constraints:** `1 <= numCourses <= 2000` · `0 <= prerequisites.length <= 5000` · all prerequisite pairs are **distinct**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "you must take `b` **first**" | ⚠️ A **directed** edge `b → a` — order matters, unlike the undirected grids so far |
| "can you **finish all** courses?" | ⚠️ Possible **iff** the graph has **no cycle** |
| pairs are distinct | No duplicate edges to deduplicate |
| `prerequisites` can be **empty** | No constraints at all → trivially `true` |
| 2000 courses, 5000 edges | O(V + E) expected |

**Why a cycle makes it impossible.** If course A requires B and B requires A, neither can ever be the *first* one you take — each is blocked waiting for the other. Any cycle traps every course on it in the same deadlock.

Conversely, **if there's no cycle, a valid order always exists**: at every moment some course has all its prerequisites satisfied, so you take it and repeat.

So the question reduces exactly to: **does this directed graph contain a cycle?**

A directed graph with no cycles is a **DAG** (directed acyclic graph), and ordering its nodes so every edge points forward is a **[topological sort](../algorithms/topological-sort.md)**. So an equivalent phrasing: *does a topological ordering exist?*

**The edge direction is worth getting right.** `[a, b]` means "take b before a", so the dependency flows `b → a`. Reversing this is the single most common bug in the problem — and it often still produces a plausible-looking answer.

**The approach that follows naturally.** Repeatedly take any course with **no unmet prerequisites**, then remove it, which may free others:

```
[[1,0]]:   course 0 has no prereqs  →  take it  →  now 1 is free  →  take it
           2 of 2 taken  ✅

[[1,0],[0,1]]:  neither has zero prereqs  →  nothing can start
                0 of 2 taken  ❌
```

**Counting how many you managed to take is the cycle test** — if it's fewer than `numCourses`, the remainder are stuck in a cycle.

🤔 **Before you open the next section:** what should you track per course so that "no unmet prerequisites" is an O(1) check rather than a scan?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Repeatedly scan for a free course | Find one with no prereqs, remove, repeat | O(V²) | ⚠️ Correct but rescans constantly |
| **DFS with three states** | white/grey/black; a grey node reached again = cycle | **O(V + E)** | ✅ |
| **Kahn's algorithm (BFS topological sort)** | Peel off zero-indegree nodes | **O(V + E)** | ✅ |

**The decision: [Kahn's algorithm](../algorithms/topological-sort.md) — BFS-based topological sort using indegrees.**

Two structures:

| Structure | Holds |
|---|---|
| `graph[prereq]` | the courses **unlocked by** finishing `prereq` (adjacency list) |
| `indegree[course]` | how many prerequisites `course` is **still waiting on** |

The algorithm:

1. Queue every course with **indegree 0** — no prerequisites, so it can be taken now.
2. Take one, count it, and **decrement the indegree** of everything it unlocks.
3. Any course whose indegree drops to **0** is now free — enqueue it.
4. When the queue empties, compare the count to `numCourses`.

**Why the count detects cycles.** A course in a cycle always has at least one unmet prerequisite from within the cycle, so its indegree **never reaches 0** and it's never enqueued. If `visited_count < numCourses`, exactly the cycle-trapped courses are missing.

> **You don't detect the cycle directly — you detect that some nodes were never freed.** That's simpler and cheaper than tracking recursion state.

**Why the indegree array makes it linear.** Without it, "does this course have unmet prerequisites?" requires scanning — O(V) per check, O(V²) overall. The counter makes it O(1), and each edge is processed exactly once when its source is taken.

**The DFS alternative** uses three colours: unvisited, *currently in the recursion stack*, and fully explored. Reaching a node that's currently on the stack means a cycle. Equally O(V + E), and the natural choice if you want to *find* the cycle rather than just detect one. **Kahn's is usually easier to explain and has no recursion-depth risk** — worth saying you know both.

**Why BFS here doesn't need level tracking.** Unlike [Rotting Oranges](994-rotting-oranges.md), there's no distance question — the queue is just "courses currently available", in any order.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
graph = [[] for _ in range(numCourses)]
indegree = [0] * numCourses
```

**The adjacency list and the prerequisite counter.**

⚠️ `[[] for _ in range(n)]` — the comprehension is required. `[[]] * n` creates n references to *one* list, so every course would share the same neighbours. The same aliasing trap as [N-Queens](51-n-queens.md) and [Valid Sudoku](36-valid-sudoku.md).

`[0] * n` is safe, since integers are immutable.
→ [list-comprehension](../syntax/list-comprehension.md) · [list-basics](../syntax/list-basics.md) · [graph](../data-structures/graph.md)

```python
for course, prereq in prerequisites:
    graph[prereq].append(course)
    indegree[course] += 1
```

**Build the graph — and note the direction carefully.**

`[course, prereq]` means *"take `prereq` before `course`"*, so the dependency flows **`prereq → course`**. Finishing `prereq` unlocks `course`, hence `graph[prereq].append(course)`.

`indegree[course] += 1` records that `course` is waiting on one more prerequisite.

**Getting this backwards is the classic bug** — and it often still returns plausible answers on symmetric test cases.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
queue = deque()
for i in range(numCourses):
    if indegree[i] == 0:
        queue.append(i)
```

**Seed with every course that has no prerequisites** — these can be taken immediately.

If *no* course has indegree 0, the queue starts empty, the loop never runs, and the count stays 0 → correctly `False`.
→ [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [range-function](../syntax/range-function.md)

```python
visited_count = 0
while queue:
    node = queue.popleft()
    visited_count += 1
```

**Take a course and count it.** The count is what the final cycle test compares against.

`deque.popleft()` is O(1); a list's `pop(0)` would be O(n) and make this quadratic.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    for neighbor in graph[node]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)
```

**Unlock what this course enables.** Each dependent course has one fewer unmet prerequisite.

**`== 0`, not `<= 0`** — the check fires exactly once per course, at the moment its last prerequisite is satisfied. That's what guarantees each course is enqueued exactly once.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return visited_count == numCourses
```

**The cycle test.** Every course taken ⇒ no cycle ⇒ `True`. Any shortfall means those courses were trapped waiting on each other.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        visited_count = 0
        while queue:
            node = queue.popleft()
            visited_count += 1
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count == numCourses
```

</details>

**Trace it — the acyclic case** — `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`:

```
graph:     0 → [1, 2]        indegree:  0: 0
           1 → [3]                      1: 1
           2 → [3]                      2: 1
           3 → []                       3: 2
```

| Step | Queue | Take | Decrements | New zeros |
|---|---|---|---|---|
| seed | `[0]` | — | — | — |
| 1 | `[]` | **0** | 1→0, 2→0 | enqueue 1, 2 |
| 2 | `[1,2]` | **1** | 3→1 | — |
| 3 | `[2]` | **2** | 3→0 | enqueue 3 |
| 4 | `[3]` | **3** | — | — |

`visited_count = 4 == numCourses` → **`True`** ✅

**And the cyclic case** — `[[1,0],[0,1]]`:

```
graph:  0 → [1]       indegree:  0: 1
        1 → [0]                  1: 1
```

No course has indegree 0, so the queue starts **empty**. The loop never runs, `visited_count = 0`.

`0 != 2` → **`False`** ✅

Notice the algorithm never "finds" the cycle — it simply observes that two courses were never freed. **The absence is the detection.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)**, where V = `numCourses` and E = `len(prerequisites)`.

| Step | Cost |
|---|---|
| Build the graph and indegrees | O(E) |
| Seed the queue | O(V) |
| Process each node | each enqueued and dequeued **exactly once** → O(V) |
| Traverse each edge | each processed **exactly once**, when its source is taken → O(E) |

**O(V + E)** total — at 2000 courses and 5000 edges, ~7000 operations.

**Why each edge is touched once.** An edge `u → v` is examined only when `u` is dequeued, and `u` is dequeued exactly once (it's enqueued the moment its indegree hits 0, and never again). So the inner loop across all iterations totals E.

**This is the standard graph-traversal bound**, matching [Clone Graph](133-clone-graph.md).

**Versus the naive rescan:** repeatedly scanning all courses for one with no prerequisites is O(V) per course removed → **O(V²)** = 4·10⁶. The indegree array replaces that scan with an O(1) counter — **the same "maintain it incrementally instead of recomputing" instinct** as the running minimum in [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md).

**DFS cycle detection is also O(V + E)** — same bound, different mechanism.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E)**.

| Component | Size |
|---|---|
| `graph` adjacency list | one entry per edge → **O(V + E)** |
| `indegree` array | **O(V)** |
| `queue` | at most V nodes → O(V) |

**O(V + E)** total.

**Why an adjacency list rather than a matrix.** A `numCourses × numCourses` matrix would be O(V²) = 4·10⁶ entries for only 5000 edges — 99.9% empty. **Adjacency lists cost O(V + E), which is what makes sparse graphs cheap**, and it's why the traversal is O(V + E) rather than O(V²).

That choice is worth stating explicitly: *matrix for dense graphs and O(1) edge lookups; list for sparse graphs and fast neighbour iteration.* Course prerequisites are sparse.

**No recursion means no stack-depth risk** — a genuine advantage of Kahn's over DFS cycle detection at V = 2000, where a chain-shaped dependency graph would otherwise exceed Python's recursion limit.

**The DFS alternative** needs O(V) for the state array plus O(V) recursion depth — same order, but with that stack risk.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Finishing all courses is possible exactly when the prerequisite graph has no cycle — a cycle means every course on it waits on another, so none can ever start. So this is cycle detection on a directed graph, which I do with Kahn's algorithm. I build an adjacency list where an edge points from a prerequisite to the course it unlocks, and an indegree array counting how many prerequisites each course is still waiting on. I queue everything with indegree zero, and each time I take a course I decrement the indegree of everything it unlocks, enqueuing any that reach zero. At the end I compare how many I took to the total — anything trapped in a cycle never reaches indegree zero, so it's never enqueued. O(V + E) time and space. DFS with three colours works too, but Kahn's has no recursion-depth risk."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does a cycle make it impossible?" | **The question.** Every course on the cycle waits on another one on the cycle, so none is ever free to be first. |
| "How does the count detect the cycle?" | Cycle-trapped courses never reach indegree 0, so they're never enqueued. A shortfall in the count *is* the cycle. |
| "Solve it with DFS." | Three states: unvisited, on the current stack, fully explored. Reaching a node that's on the stack means a cycle. Same O(V + E). |
| "Return the actual **order**, not just a boolean." | Collect the dequeued nodes into a list — that's [Course Schedule II](210-course-schedule-ii.md). |
| "Which direction should the edges go?" | `[a, b]` means b before a, so `b → a`. Reversing it is the classic bug. |
| "Adjacency list or matrix?" | List — 2000 courses and 5000 edges is sparse; a matrix would be 4 million mostly-empty entries. |
| "Why not just rescan for a free course?" | O(V²). The indegree counter makes the check O(1). |

**Traps:**

- **Reversing the edge direction.** `graph[course].append(prereq)` inverts the dependency and silently gives wrong answers on asymmetric inputs.
- **`[[]] * numCourses`** — n aliases of one list; every course shares neighbours.
- **`indegree[neighbor] <= 0`** instead of `== 0` — a course could be enqueued more than once, inflating the count and reporting `True` on a cyclic graph.
- **Using a list as the queue** — `pop(0)` is O(n), making it quadratic.
- **Returning `len(queue) == 0`** or similar — the queue is always empty at the end. Compare the *count*.
- **Forgetting the empty-prerequisites case** — every indegree is 0, all courses are enqueued, and it correctly returns `True`.

**This same move shows up in:** [Course Schedule II](210-course-schedule-ii.md) (this algorithm, returning the order) · [Alien Dictionary](269-alien-dictionary.md) (topological sort to recover a character ordering) · [Clone Graph](133-clone-graph.md) (adjacency-list traversal) · [topological-sort](../algorithms/topological-sort.md) · [graph](../data-structures/graph.md).

</details>

---
