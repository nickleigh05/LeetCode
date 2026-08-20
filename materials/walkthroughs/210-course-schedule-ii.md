# 210. Course Schedule II

**Medium** · [LeetCode](https://leetcode.com/problems/course-schedule-ii/)

[📖 12. Graphs lesson](../learning/12-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Graphs problems](../rmap-practice/12-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There are `numCourses` courses labelled `0` to `numCourses - 1`, with `prerequisites[i] = [aᵢ, bᵢ]` meaning **you must take `bᵢ` first** to take `aᵢ`.

Return **the ordering of courses** you should take to finish them all. If there are many valid answers, return **any** of them. If it's impossible, return an **empty array**.

```
numCourses = 2, prerequisites = [[1,0]]              →  [0,1]
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
   →  [0,1,2,3]  or  [0,2,1,3]     both valid
numCourses = 1, prerequisites = []                   →  [0]
```

**Constraints:** `1 <= numCourses <= 2000` · `0 <= prerequisites.length <= numCourses·(numCourses−1)` · all pairs **distinct**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return the **ordering**" | ⚠️ [Course Schedule](207-course-schedule.md) asked *whether* an order exists; this asks for the order itself |
| "**any** valid answer" | Multiple orderings are usually valid — no canonical one to find |
| "**empty array** if impossible" | The cycle case returns `[]`, not `false` |
| same graph model | Identical setup: directed edges from prerequisite to dependent |

**This is [Course Schedule](207-course-schedule.md) with the answer already computed.**

That problem ran Kahn's algorithm and counted how many courses it managed to take. But look at *what it was doing* while counting: it dequeued courses in an order where **every course came after all its prerequisites**.

> **That dequeue order *is* a valid schedule.** The algorithm was producing the answer all along — [207](207-course-schedule.md) just threw it away and kept the count.

So the only change is to **record the order instead of counting it**, and return it when complete.

**Why the dequeue order is guaranteed valid.** A course is enqueued exactly when its indegree hits 0 — meaning every prerequisite has already been dequeued. So by construction, no course ever appears before something it depends on. **That's the definition of a [topological ordering](../algorithms/topological-sort.md).**

**Why "any" answer is accepted.** When several courses have indegree 0 simultaneously, any of them can go next — they're mutually independent. Different queue orders give different valid schedules, which is why the problem permits any.

🤔 **Before you open the next section:** [207](207-course-schedule.md) compared a count against `numCourses`. What's the equivalent check when you're building a list?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Repeatedly scan for a free course | Find zero-prereq courses by scanning | O(V²) | ⚠️ Correct but rescans |
| **Kahn's algorithm, recording the order** | Dequeue order *is* the schedule | **O(V + E)** | ✅ |
| DFS post-order, reversed | Finish a node after its dependents; reverse at the end | O(V + E) | ✅ Also standard |

**The decision: [Kahn's algorithm](../algorithms/topological-sort.md), collecting the dequeue order.**

The diff from [Course Schedule](207-course-schedule.md) is three lines:

| | [207](207-course-schedule.md) | **210** |
|---|---|---|
| Accumulator | `visited_count = 0` | **`order = []`** |
| On dequeue | `visited_count += 1` | **`order.append(node)`** |
| Return | `visited_count == numCourses` | **`order if len(order) == numCourses else []`** |

Everything else — the adjacency list, the indegree array, the queue seeding, the decrement loop — is **identical**.

**Why the length check still detects cycles.** Courses trapped in a cycle never reach indegree 0, so they're never enqueued and never appended. A short `order` means exactly those courses are missing. **Same detection, just measuring the list instead of a counter.**

⚠️ **And returning a partial order would be wrong.** If a cycle exists, `order` holds a genuine partial schedule — but the problem demands `[]`, since the full set can't be completed. Returning the partial list is a plausible-looking bug.

**The DFS alternative** is worth knowing because it's the other standard topological sort: DFS from every unvisited node, append a node to a list **after** exploring all its dependents, then **reverse** the list. The reversal is needed because post-order finishes dependents first. It requires the three-colour cycle check to detect cycles, and carries a recursion-depth risk at V = 2000.

**Kahn's is usually the better interview answer here** — no recursion, and the cycle check falls out of the length comparison rather than needing separate state.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
graph = [[] for _ in range(numCourses)]
indegree = [0] * numCourses

for course, prereq in prerequisites:
    graph[prereq].append(course)
    indegree[course] += 1
```

**Identical setup to [Course Schedule](207-course-schedule.md).** The edge points from the prerequisite to the course it unlocks, and `indegree` counts how many prerequisites each course still awaits.

⚠️ The comprehension `[[] for _ in range(n)]` is required — `[[]] * n` would alias one list across all courses.
→ [list-comprehension](../syntax/list-comprehension.md) · [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [graph](../data-structures/graph.md)

```python
queue = deque()
for i in range(numCourses):
    if indegree[i] == 0:
        queue.append(i)
```

**Seed with courses that have no prerequisites** — the ones that can be taken first.

If none exist, the queue starts empty and `order` stays empty → correctly `[]`.
→ [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [range-function](../syntax/range-function.md)

```python
order = []
while queue:
    node = queue.popleft()
    order.append(node)
```

**The one substantive change from [207](207-course-schedule.md):** record the course instead of just counting it.

Because a course is only enqueued once all its prerequisites have been dequeued, **appending on dequeue produces a valid ordering by construction** — no sorting or post-processing needed.
→ [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md)

```python
    for neighbor in graph[node]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)
```

**Unlock the dependents.** Each course this one enables has one fewer unmet prerequisite; reaching 0 means it's now takeable.

`== 0` rather than `<= 0` fires exactly once per course, guaranteeing each is enqueued — and therefore appended — exactly once.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return order if len(order) == numCourses else []
```

**The cycle check, as a length comparison.**

Every course scheduled ⇒ valid ordering. A shortfall ⇒ some courses were trapped in a cycle ⇒ return `[]`, **not** the partial order.
→ [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == numCourses else []
```

</details>

**Trace it** — `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`:

```
graph:  0 → [1, 2]        indegree:  0: 0    ← can start
        1 → [3]                      1: 1
        2 → [3]                      2: 1
        3 → []                       3: 2
```

| Step | Queue | Dequeue | `order` | Decrements | Enqueued |
|---|---|---|---|---|---|
| seed | `[0]` | — | `[]` | — | — |
| 1 | `[]` | **0** | `[0]` | 1→0, 2→0 | 1, 2 |
| 2 | `[1,2]` | **1** | `[0,1]` | 3→1 | — |
| 3 | `[2]` | **2** | `[0,1,2]` | 3→0 | 3 |
| 4 | `[3]` | **3** | `[0,1,2,3]` | — | — |

`len(order) == 4` → return **`[0,1,2,3]`** ✅

Check it: 0 has no prerequisites ✓; 1 needs 0, which came first ✓; 2 needs 0 ✓; 3 needs both 1 and 2, both already taken ✓.

**Note `[0,2,1,3]` is equally valid** — at step 2 the queue held both 1 and 2, and either could have gone first. They're independent, which is why the problem accepts any answer.

**And the cyclic case** — `[[1,0],[0,1]]`: both courses have indegree 1, the queue starts empty, `order` stays `[]`, and `0 != 2` → return **`[]`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)**, where V = `numCourses` and E = `len(prerequisites)`.

| Step | Cost |
|---|---|
| Build graph and indegrees | O(E) |
| Seed the queue | O(V) |
| Dequeue each node once | O(V) |
| Traverse each edge once | O(E) |

**O(V + E)** — identical to [Course Schedule](207-course-schedule.md), since recording the order costs O(1) per node.

At V = 2000, the edge count can reach ~4·10⁶ under these constraints, so linear matters.

**Each edge is examined exactly once**, when its source course is dequeued — and each course is dequeued exactly once, because it's enqueued only at the moment its indegree hits 0.

**Versus repeatedly scanning for a free course:** O(V) per scan × V courses = **O(V²)** = 4·10⁶ even before edges. The indegree array turns that scan into an O(1) counter.

**The DFS alternative is also O(V + E)** — same bound, plus a reversal at the end and a recursion-depth risk.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E)</summary>

**O(V + E)**.

| Component | Size |
|---|---|
| `graph` adjacency list | **O(V + E)** |
| `indegree` array | O(V) |
| `queue` | up to V |
| `order` | the required output, O(V) |

**Adjacency list, not matrix.** At V = 2000, a matrix would be 4·10⁶ entries regardless of how few edges exist. The list costs O(V + E) — proportional to what's actually there, which is what keeps the traversal linear.

**No recursion**, so no stack-depth concern — a real advantage over the DFS topological sort at V = 2000, where a chain-shaped dependency graph would exceed Python's recursion limit.

**`order` is the output**, so it isn't auxiliary overhead — but note it's the *only* structural difference from [207](207-course-schedule.md), which used a single integer. **The extra O(V) is precisely the cost of returning the answer rather than a yes/no.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Course Schedule with the answer kept instead of discarded. That problem ran Kahn's algorithm and counted how many courses it could take — but the *order* it dequeued them in was already a valid schedule, because a course is only enqueued once all its prerequisites have been dequeued. So I record the dequeue order rather than counting, and the cycle check becomes a length comparison: if the order is shorter than `numCourses`, some courses were trapped in a cycle and never reached indegree zero, so I return an empty array rather than the partial order. O(V + E) time and space. Multiple orderings are valid whenever several courses have no unmet prerequisites at the same time, which is why the problem accepts any."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the dequeue order valid?" | **The question.** A course is enqueued exactly when its last prerequisite is dequeued, so it always appears after all of them. |
| "Why return `[]` and not the partial order?" | The problem demands a *complete* schedule. A partial one is a plausible-looking wrong answer. |
| "Why are multiple answers valid?" | Courses with indegree 0 at the same moment are mutually independent — any order among them works. |
| "Solve it with DFS." | Post-order DFS appending each node after its dependents, then reverse. Needs three-colour cycle detection, and risks stack depth at V = 2000. |
| "Return the **lexicographically smallest** order?" | Swap the queue for a **min-heap**, so the smallest available course is always taken next. O((V + E) log V). |
| "How is this different from [207](207-course-schedule.md)?" | Three lines: a list instead of a counter, append instead of increment, and the length check. |
| "What if there are no prerequisites?" | Every indegree is 0, all courses enqueue immediately, and the order is `[0, 1, …, n−1]`. |

**Traps:**

- **Returning the partial `order` on a cycle** instead of `[]`.
- **Reversing the edge direction** — `graph[course].append(prereq)` inverts the dependency and produces a backwards schedule.
- **`[[]] * numCourses`** — aliased lists; every course shares neighbours.
- **`indegree[neighbor] <= 0`** instead of `== 0` — a course could be appended twice, making the length check pass on a cyclic graph.
- **Appending on *enqueue* rather than dequeue.** It happens to work for Kahn's, but dequeue is the defensible choice — that's the moment the course is "taken".
- **Sorting the result.** The order is already valid; sorting destroys it.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (the same algorithm, returning a boolean) · [Alien Dictionary](269-alien-dictionary.md) (topological sort recovering a character ordering) · [topological-sort](../algorithms/topological-sort.md) · [graph](../data-structures/graph.md).

</details>

---
