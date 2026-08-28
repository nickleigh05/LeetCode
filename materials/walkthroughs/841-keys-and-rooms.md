# 841. Keys and Rooms

**Medium** · [LeetCode](https://leetcode.com/problems/keys-and-rooms/) · [Solution file (no hints)](../../problems/0500-0999/841.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

`n` rooms are locked except room `0`. Room `i` contains the keys in `rooms[i]`. Return `true` if you can visit **all** rooms.

```
rooms = [[1],[2],[3],[]]        →  true      0 → 1 → 2 → 3
rooms = [[1,3],[3,0,1],[2],[0]] →  false     room 2's only key is inside room 2
```

**Constraints:** `2 <= n <= 1000` · `sum(rooms[i].length) <= 3000` · keys within a room are distinct

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "rooms… keys that unlock other rooms" | ⚠️ **It's a graph.** Rooms are nodes, keys are **directed** edges |
| "all rooms locked **except room 0**" | Fixed start node — no outer loop over start nodes |
| "return true if you can visit **all**" | Reachability from a single source, then compare the count to `n` |
| "you can take all of them with you" | Keys accumulate — no state beyond "which rooms have I entered" |
| `sum(rooms[i].length) <= 3000` | ⚠️ That's the **edge** count. E ≤ 3000, V ≤ 1000 |

**The translation is the problem.** Once you see it as a graph, the code is eight lines:

```
room i          →  node i
key j in room i →  directed edge i → j

"can I visit all rooms?"  →  "is every node reachable from node 0?"
```

**Note the edges are directed.** Room 0 holding a key to room 3 says nothing about room 3 holding a key to room 0. Adding reverse edges — the reflex from [Find if Path Exists](1971-find-if-path-exists-in-graph.md) — makes this problem trivially `true` almost always, and wrong.

```
rooms = [[1,3],[3,0,1],[2],[0]]

0 → 1, 3
1 → 3, 0, 1
2 → 2                ← room 2's only key opens room 2 itself
3 → 0

Start at 0: reach 1, 3. From 1: 3, 0 (seen). From 3: 0 (seen).
Reached {0, 1, 3} — never 2.                       → false ✅
```

**Room 2 is unreachable because its only key is locked inside it.** Nothing points *into* room 2 from anywhere you can get to. That's an in-degree-zero node outside the reachable set — the shape of every "false" case here.

**Why no "keys collected" state is needed.** It sounds like an inventory problem, but keys are never consumed and never expire. So "I hold room j's key" and "I can enter room j" are the same statement, and once entered, a room offers nothing new. **`visited` is the entire state** — you don't track keys at all.

🤔 **Before you open the next section:** could a room be reachable, but only if you visited some *other* room first to pick up its key? What does that imply about whether a simple traversal is enough?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Simulate with a key inventory | Track held keys, repeat until stable | O(V·E) | ❌ Models state that doesn't matter |
| **DFS from room 0** | Traverse, count visited | **O(V + E)** | ✅ |
| BFS from room 0 | Same, with a queue | O(V + E) | ✅ Identical |
| Union-Find | ❌ | — | ❌ Edges are **directed**; union-find models undirected connectivity |

**The decision: DFS (or BFS) from room 0, then check `len(visited) == len(rooms)`.**

**Why the naive "inventory" simulation is the wrong model.** A tempting formulation: hold a set of keys, repeatedly open any room you have a key for, loop until nothing changes. It's *correct*, but it re-scans the key set on every round — O(V) rounds × O(E) work = **O(V·E)**.

The traversal is better because of the monotonicity noted above: **entering a room can only ever add keys, never remove them**, so there's no reason to reconsider a room. One pass suffices.

⚠️ **Union-Find does not apply here**, and it's worth knowing why, since it's the natural tool for [Number of Provinces](547-number-of-provinces.md) and [Find if Path Exists](1971-find-if-path-exists-in-graph.md). Union-Find models **undirected** connectivity — it can only answer "are these in the same blob?" But reachability here is **one-way**:

```
rooms = [[], [0]]

Room 1 holds a key to room 0. Room 0 holds nothing.
Union-find: {0, 1} are connected → would say true.
Reality: you start in room 0, hold no keys, can never enter room 1 → false ✅
```

**Directedness is the reason.** Recognising when a familiar tool *doesn't* apply is worth as much as knowing when it does.

**DFS vs BFS: interchangeable.** Both O(V+E), both correct — the order of exploration is irrelevant when you only need the reachable *set*. The iterative DFS below uses a list as a stack:

```python
stack = [0]
while stack:
    room = stack.pop()          # pop() from the end — O(1)
```

**Iterative over recursive**, even though n ≤ 1000 makes recursion technically safe (a chain would be 1,000 frames deep — right at Python's default limit, uncomfortably close). `stack.pop()` costs nothing and removes the question.
→ [recursion-limit](../syntax/recursion-limit.md)

**The final check is the only non-traversal step:**

```python
return len(visited) == len(rooms)
```

**Count, don't re-search.** Having explored everything reachable from room 0, the answer is simply whether that set covers every room.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
visited = set([0])
stack = [0]
```

**Both seeded with room 0** — the one room that starts unlocked.

Marking room 0 visited immediately, rather than when it's popped, keeps the invariant "anything in the stack is already in `visited`", which is what stops rooms being pushed twice.
→ [set-basics](../syntax/set-basics.md) · [list-basics](../syntax/list-basics.md)

```python
while stack:
    room = stack.pop()
```

**Iterative DFS.** `stack.pop()` removes from the **end** — O(1).

⚠️ `pop()` with no argument, not `pop(0)`. The latter removes from the front, is O(n), and would turn the traversal quadratic. (It would also make this a BFS — still correct, just slow. Use a `deque` if you want BFS.)
→ [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    for key in rooms[room]:
        if key not in visited:
            visited.add(key)
            stack.append(key)
```

**Each key is a directed edge.** `rooms[room]` is already an adjacency list — nothing to build, unlike [Find if Path Exists](1971-find-if-path-exists-in-graph.md).

⚠️ **Add to `visited` at push time, not pop time.** Otherwise a room reachable by several keys is pushed once per key: harmless for correctness, but the stack can bloat to O(E) and work is duplicated.

`not in visited` on a set is O(1) — the reason the traversal stays linear.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md)

```python
return len(visited) == len(rooms)
```

**Did we reach everything?** `visited` holds exactly the rooms reachable from 0; if that's all `n` of them, the answer is `true`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        visited = set([0])
        stack = [0]

        while stack:
            room = stack.pop()
            for key in rooms[room]:
                if key not in visited:
                    visited.add(key)
                    stack.append(key)

        return len(visited) == len(rooms)
```

</details>

**Trace it** — Example 2: `rooms = [[1,3],[3,0,1],[2],[0]]`:

| Step | Pop | Keys inside | New rooms opened | `stack` | `visited` |
|---|---|---|---|---|---|
| 1 | `0` | 1, 3 | both new | `[1,3]` | `{0,1,3}` |
| 2 | `3` | 0 | already visited | `[1]` | `{0,1,3}` |
| 3 | `1` | 3, 0, 1 | all visited | `[]` | `{0,1,3}` |
| 4 | — | stack empty | | | |

`len(visited) = 3`, `len(rooms) = 4` → **`false`** ✅

**Room 2 is never even considered.** No key to it exists in any reachable room — its only key sits inside itself. The traversal doesn't *fail* to open room 2; it never encounters a reference to it at all. **That's what unreachable means operationally.**

**Step 3 shows why `visited` is essential.** Room 1 holds a key to room 1 — itself. Without the check, room 1 would be pushed again, popped again, forever. Self-referential keys are explicitly allowed by the constraints.

**Example 1** (`[[1],[2],[3],[]]`) is a chain: 0 opens 1, 1 opens 2, 2 opens 3, 3 is empty. All four visited → **`true`**.

**A useful edge case not in the examples:** `rooms = [[], [0]]` → `visited = {0}`, so **`false`**. Room 1 holds the key to room 0, but that's backwards — you can never get *into* room 1. This is the case that rules out union-find.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(V + E)</summary>

**O(V + E)** — where V = `len(rooms)` and E = total keys, `sum(len(rooms[i]))`.

| Phase | Cost |
|---|---|
| Traversal | **O(V + E)** — each room popped once, each key examined once |
| Final count | **O(1)** — `len()` on a set |
| **Total** | **O(V + E)** |

At V ≤ 1000 and E ≤ 3000 that's about 4,000 operations.

**Each key is examined exactly once.** A room is pushed at most once (guaranteed by adding to `visited` at push time), so it's popped at most once, so its key list is scanned at most once. Summing over rooms gives E.

**⚠️ Note E is bounded separately from V** — `sum(rooms[i].length) <= 3000` is an explicit constraint. Don't assume E = O(V²); the problem tells you it's small.

**This is optimal.** Proving some room unreachable requires exhausting everything reachable from room 0. **Ω(V+E) is the lower bound.**

**Versus the inventory simulation**, O(V·E): each round scans all held keys and may open one more room, so up to V rounds × O(E) work ≈ 3·10⁶ here. Still passes, but it re-derives facts the traversal establishes once. **The saving comes from monotonicity — keys are never lost, so a room never needs revisiting.**

**Early exit is possible but pointless:** you could stop the moment `len(visited) == len(rooms)`, but the worst case (`false`) still requires the full traversal, so the asymptotic bound is unchanged.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V)</summary>

**O(V)** auxiliary.

| Component | Size |
|---|---|
| `visited` | at most V rooms → **O(V)** |
| `stack` | at most V rooms → **O(V)** |
| Input `rooms` | O(V+E), **given** not allocated |
| **Total auxiliary** | **O(V)** |

**Note it's O(V), not O(V+E)** — no adjacency list is built, because the input already is one. Compare [Find if Path Exists](1971-find-if-path-exists-in-graph.md), which spends O(V+E) converting an edge list first.

**The stack holds at most V rooms**, not E, precisely because of the push-time `visited` marking. Marking at pop time instead would let it grow to **O(E)** — 3,000 entries instead of 1,000 here:

| When you mark visited | Stack size | Correct? |
|---|---|---|
| **On push** | **O(V)** ✅ | ✅ |
| On pop | O(E) | ✅ but wasteful |

**A boolean list beats a set** in practice — `visited = [False] * len(rooms)` with a running counter avoids hashing, and room labels are already `0..n-1`. Same O(V), better constant, and it makes the final check a counter comparison rather than `len()`.

**Recursive DFS would also be O(V)**, on the call stack — and at V = 1000 a chain (`rooms = [[1],[2],[3],…]`, exactly Example 1's shape) recurses 1,000 deep, **right at Python's default limit**. Not guaranteed to fail, but close enough that the iterative version is the better habit.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is reachability in a directed graph wearing a costume — rooms are nodes and keys are directed edges, and the question is whether every node is reachable from node 0. The input is already an adjacency list, so I just DFS from room 0 with a visited set and compare its size to the room count at the end. What makes a plain traversal sufficient is that keys are never consumed or lost, so entering a room can only add options — there's no inventory state to track and no reason to revisit a room. I mark rooms visited when I push them rather than when I pop, so nothing enters the stack twice. O(V+E) time and O(V) space. One thing I'd flag: union-find doesn't work here even though it's the usual tool for connectivity, because these edges are directed — `rooms = [[], [0]]` is connected undirected but the answer is false."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why no key inventory?" | **The question.** Keys are never consumed, so "I hold room j's key" and "I can enter room j" coincide. `visited` is the whole state. |
| "Why not union-find?" | The edges are **directed**. `[[], [0]]` is undirected-connected but the answer is false — you can't enter room 1 from room 0. |
| "DFS or BFS?" | Either; both O(V+E). Only the reachable *set* matters, not the order. |
| "Why mark visited on push?" | Keeps the stack O(V) instead of O(E) and prevents duplicate work. |
| "What does `false` look like structurally?" | A room with no key to it in any reachable room — in-degree zero relative to the reachable set, like a room holding only its own key. |
| "Which rooms can't be reached?" | `set(range(n)) - visited`. Same traversal. |
| "Minimum keys to add for `true`?" | One per unreachable strongly-connected component with in-degree zero — condense to the SCC DAG and count sources. See [tarjan-scc](../algorithms/tarjan-scc.md). |
| "Millions of rooms?" | Same algorithm; use a boolean array over a set and stay iterative. It's already linear. |
| "What if keys were single-use?" | A genuinely different, much harder problem — state becomes (room, multiset of keys) and the search space explodes. |

**Traps:**

- **Treating the graph as undirected** — adding reverse edges makes almost everything `true`. Example 2 would wrongly return `true`.
- **Using union-find** — same failure, for the same reason.
- **Reaching for a key inventory** — correct but O(V·E), and it models state that can't change the answer.
- **`stack.pop(0)`** — O(n) per pop, quadratic overall. Use `pop()` or a `deque`.
- **Marking visited on pop** — stack grows to O(E), duplicated work.
- **Forgetting room 0 starts unlocked** — seed both `visited` and the stack with it.
- **Returning `len(visited) > 0`** or comparing against the wrong count — the check is `== len(rooms)`.
- **Not handling a room whose key list includes itself** — the constraints allow it; `visited` handles it, but only if you check before pushing.

**This same move shows up in:** [Find if Path Exists in Graph](1971-find-if-path-exists-in-graph.md) (the same traversal, undirected, with a target instead of a count) · [Number of Provinces](547-number-of-provinces.md) (counting components rather than checking one) · [Find Eventual Safe States](802-find-eventual-safe-states.md) (directed reachability with cycle handling) · [Course Schedule](207-course-schedule.md) (directed graph hidden in a word problem) · [dfs](../algorithms/dfs.md) · [graph](../data-structures/graph.md).

</details>

---
