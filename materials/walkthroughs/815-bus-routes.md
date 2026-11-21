# 815. Bus Routes

**Hard** · [LeetCode](https://leetcode.com/problems/bus-routes/) · [Solution file (no hints)](../../problems/0500-0999/815.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

You're given an array `routes`, where `routes[i]` lists the stops bus `i` visits. Each bus **loops forever** along its route. You start at stop `source` (not on any bus) and want to reach stop `target`, travelling only by bus.

Return the **minimum number of buses** you must take, or `-1` if it's impossible.

```
routes = [[1,2,7],[3,6,7]], source = 1, target = 6
→ 2      (bus 0 from 1 to 7, then bus 1 from 7 to 6)

routes = [[7,12],[4,5,15],[6],[15,19],[9,12,13]], source = 15, target = 12
→ -1
```

**Constraints:** `1 <= routes.length <= 500` · `1 <= routes[i].length <= 10⁵` · all values in `routes[i]` are unique · `sum(routes[i].length) <= 10⁵` · `0 <= routes[i][j] < 10⁶` · `0 <= source, target < 10⁶`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| minimum number of **buses** | You're counting **boardings**, not stops. Riding through 50 stops on one bus costs 1 |
| bus **loops forever** | Once you're on a bus, you can get off at **any** of its stops |
| stop labels up to 10⁶, total stops 10⁵ | Use dicts keyed by stop, not arrays indexed by stop |
| `source == target` | Zero buses. An easy case to miss |

**The tempting graph is the wrong one.** If you make **stops** the nodes, with an edge between consecutive stops, BFS counts **stops travelled**, not buses. You'd also need edges between *every pair* of stops on a route (since you can get off anywhere), which is O(L²) edges for a route of length L. A 10⁵-stop route would produce 10¹⁰ edges.

**The right graph: buses are the nodes.** What costs 1 is **boarding a bus**. So BFS over **buses**:

- **Level 1:** every bus that serves `source`.
- **Level k + 1:** every new bus you can transfer to from a level-k bus, meaning any bus that shares a stop with it.
- The answer is the first level containing a bus that serves `target`.

**How to find transfers quickly: map each stop to its buses.** `stop_to_buses[stop]` lists every bus serving that stop. From a bus, go through its stops, and each stop's list gives the buses you can switch to there.

**Two visited sets keep it linear.** Mark **buses** as seen so none is boarded twice. Also mark **stops** as seen, so once you've expanded a stop's bus list, you never scan it again. That second set is what keeps a busy interchange from being scanned once per bus that passes through it.

🤔 **Before you open the next section:** in the first example, which buses are in level 1, and how do you discover bus 1 from there?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Nodes | Edges | Verdict |
|---|---|---|---|
| BFS over stops, consecutive edges | stops | route order | ❌ Counts stops, not buses |
| BFS over stops, all-pairs per route | stops | O(L²) per route | ❌ Can be 10¹⁰ edges |
| Bus graph with explicit edges | buses | buses sharing a stop: O(B²·L) to build | ⚠️ Correct, slow to build |
| **BFS over buses via `stop → buses`** | buses | discovered on the fly through shared stops | ✅ O(total stops) |

**The decision: [BFS](../algorithms/bfs.md) where each [queue](../data-structures/queue.md) entry is a bus, using a `stop → buses` [hash map](../data-structures/hashmap.md)** to find transfers.

BFS level = number of buses boarded, so the first time you reach a bus that stops at `target`, that level is the answer.

**Why not build the bus-to-bus graph first?** Comparing every pair of buses for a shared stop is O(B² · L). The `stop → buses` index gives the same neighbours lazily, at the moment you need them, and each stop is expanded once.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if source == target:
    return 0
```

You're already there, with no bus needed. Without this check, the BFS below would board a bus first and return 1.
→ [if-return](../syntax/if-return.md)

```python
stop_to_buses = defaultdict(list)
for bus, route in enumerate(routes):
    for stop in route:
        stop_to_buses[stop].append(bus)
```

**The interchange index.** For every stop, the list of buses that serve it. It's built in one pass over all routes, O(total stops).
→ [defaultdict](../syntax/defaultdict.md) · [enumerate](../syntax/enumerate.md) · [nested-lists](../syntax/nested-lists.md)

```python
queue = deque()
bus_seen = set()
for bus in stop_to_buses[source]:
    bus_seen.add(bus)
    queue.append((bus, 1))
stop_seen = {source}
```

**Level 1: every bus you can board at `source`.** Each entry is `(bus, buses_taken)`. `source` is marked seen because its bus list has just been used.
→ [deque-basics](../syntax/deque-basics.md) · [set-basics](../syntax/set-basics.md)

```python
while queue:
    bus, rides = queue.popleft()
    for stop in routes[bus]:
        if stop == target:
            return rides
```

**Ride the bus and check every stop.** The bus loops, so every stop on its route is reachable with this many rides. If one is `target`, BFS order guarantees `rides` is the minimum.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
        if stop in stop_seen:
            continue
        stop_seen.add(stop)
```

**Expand each stop only once.** If another bus already brought you here, its transfers have already been queued. Skipping it keeps the total work linear.
→ [break-continue](../syntax/break-continue.md) · [membership-operators](../syntax/membership-operators.md)

```python
        for nxt in stop_to_buses[stop]:
            if nxt not in bus_seen:
                bus_seen.add(nxt)
                queue.append((nxt, rides + 1))
```

**Transfer.** Every not-yet-boarded bus at this stop is one more ride away.

```python
return -1
```

Every reachable bus has been ridden without reaching `target`.

<details>
<summary>The whole thing together</summary>

```python
from collections import defaultdict, deque

class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        if source == target:
            return 0

        stop_to_buses = defaultdict(list)
        for bus, route in enumerate(routes):
            for stop in route:
                stop_to_buses[stop].append(bus)

        queue = deque()
        bus_seen = set()
        for bus in stop_to_buses[source]:
            bus_seen.add(bus)
            queue.append((bus, 1))
        stop_seen = {source}

        while queue:
            bus, rides = queue.popleft()
            for stop in routes[bus]:
                if stop == target:
                    return rides
                if stop in stop_seen:
                    continue
                stop_seen.add(stop)
                for nxt in stop_to_buses[stop]:
                    if nxt not in bus_seen:
                        bus_seen.add(nxt)
                        queue.append((nxt, rides + 1))

        return -1
```

</details>

**Trace it.** `routes = [[1,2,7],[3,6,7]]`, `source = 1`, `target = 6`:

`stop_to_buses = {1:[0], 2:[0], 7:[0,1], 3:[1], 6:[1]}`

| Pop | Stops ridden | Target? | New stops expanded | Buses queued |
|---|---|---|---|---|
| (bus 0, 1) | 1, 2, 7 | no | 2 → [0] (seen); 7 → [0, **1**] | (1, 2) |
| (bus 1, 2) | 3, **6** | **yes → 2** ✅ | | |

Bus 1 was discovered by **transferring at stop 7**, the stop the two routes share.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(S)</summary>

**O(S)**, where S = `sum(len(route))` is the total number of stops listed across all routes.

- Building `stop_to_buses`: O(S).
- Each **bus** is queued once (`bus_seen`), and riding it scans its route once. Across all buses, that's O(S).
- Each **stop** is expanded once (`stop_seen`). The total length of all `stop_to_buses` lists is S, so all transfer scans add up to O(S).

Without `stop_seen`, a busy interchange served by many buses would have its bus list scanned once per bus, which can grow quadratically.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(S)</summary>

**O(S)** for `stop_to_buses` (one entry per stop listed on a route) and `stop_seen`. `bus_seen` and the queue are O(B), where B ≤ 500 is the number of buses.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The cost is buses boarded, not stops, so I BFS over buses. I build a map from each stop to the buses that serve it. Level 1 is every bus at the source. Riding a bus, I check each of its stops for the target, and for any stop I haven't expanded yet, I queue every unboarded bus there at one more ride. I keep visited sets for both buses and stops so each is processed once, which makes it linear in the total number of route stops. Source equal to target returns 0, and an empty queue means -1."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not BFS over stops?" | It counts stops, not boardings. Connecting all stops on a route to each other is O(L²) edges. |
| "Why the `stop_seen` set?" | So each interchange's bus list is scanned once. Without it, a stop shared by many buses is rescanned for each one. |
| "Return the actual journey?" | Store each bus's parent bus and transfer stop when you queue it, then walk back from the bus that reached `target`. |
| "Fewest stops instead of fewest buses?" | That's BFS over stops with route-order edges, a different cost model. |
| "Weighted, like ticket prices per bus?" | [Dijkstra](../algorithms/dijkstra.md) over buses, with the same transfer index. |

**Traps:**

- **Missing `source == target`.** It returns 1 instead of 0.
- **Modelling stops as nodes.** It gives the wrong cost, or an edge explosion.
- **No `stop_seen`.** Correct, but it can time out on routes that share a huge hub.
- **Arrays indexed by stop.** Labels go up to 10⁶, but only 10⁵ appear, so use dicts.
- **Counting the first bus as 0 rides.** Boarding at `source` is already one bus, so level 1 starts at `rides = 1`.

**This same move shows up in:** [Word Ladder](127-word-ladder.md) (BFS where the "edges" are discovered through an index of shared patterns) · [Open the Lock](https://leetcode.com/problems/open-the-lock/) (LeetCode 752, BFS over states) · [Course Schedule](207-course-schedule.md) (building an adjacency map before traversing) · [Accounts Merge](721-accounts-merge.md) (connecting groups through shared members).

</details>

---
