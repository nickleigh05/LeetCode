# 787. Cheapest Flights Within K Stops

**Medium** · [LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. Advanced Graphs problems](../rmap-practice/13-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There are `n` cities connected by `flights`, where `flights[i] = [from, to, price]`. Given `src`, `dst` and `k`, return the **cheapest price** from `src` to `dst` using **at most `k` stops**. If there's no such route, return `-1`.

```
n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src = 0, dst = 3, k = 1                       →  700
        0 → 1 → 3 costs 700 and uses 1 stop.
        0 → 1 → 2 → 3 costs 400 but uses 2 stops — not allowed.

n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 1                       →  200
src = 0, dst = 2, k = 0                       →  500
```

**Constraints:** `1 <= n <= 100` · `0 <= flights.length <= (n·(n−1)/2)` · `0 <= price <= 10⁴` · `0 <= k < n` · no duplicate flights, no self-loops.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `[from, to, price]` | A **weighted directed graph**. Prices are non-negative, so Dijkstra's is at least *eligible* |
| "**cheapest** price from `src` to `dst`" | Single-source, single-target shortest path. On its own this is a plain Dijkstra's problem |
| "**at most `k` stops**" | And here's the twist. A second, independent budget. You're now optimizing cost **subject to a constraint on path length** |
| "at most k **stops**", not edges | `k` stops means **`k + 1` flights**. Example 2 nails it down: `k = 0` allows the direct flight only. Get this off-by-one wrong and everything else is wasted |
| `n <= 100`, E ≤ ~4950 | Small. O(k · E) ≈ 100 × 5000 = 5 × 10⁵. Anything polynomial is fine |
| `-1` if unreachable | Standard unreachable sentinel |

The whole problem is the third row. Adding a hop limit to shortest-path **breaks the greedy assumption Dijkstra's is built on**, and understanding *why* is the entire point of this problem — it's the reason it sits in Advanced Graphs rather than next to [Network Delay Time](743-network-delay-time.md).

Here's the failure, concretely, using example 1 with `k = 1`. Dijkstra's from node 0 reaches node 2 most cheaply via `0 → 1 → 2` at price 200. It **finalizes** node 2 at 200 and never reconsiders it. From node 2, `dst` costs 200 more — total 400, but that route used 2 stops. It's illegal, and Dijkstra's has already thrown away the information needed to notice or recover.

The deeper issue: Dijkstra's records **one number per node** — the cheapest price. But the cheapest way to reach a node isn't necessarily the best way *given a remaining hop budget*. A costlier route with fewer hops can be strictly better. **One number per node is not enough state.**

🤔 **Before you open the next section:** if "cheapest at node X" isn't sufficient, what *is* the right thing to track? What extra dimension does the state need — and is there an algorithm that naturally proceeds one hop at a time?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Plain Dijkstra's | Min-heap on price, finalize each node once | O(E log V) | O(V+E) | ❌ **Wrong.** Finalizing a node by price alone discards routes that cost more but use fewer hops |
| Dijkstra's on `(price, node, stops)` | Don't finalize; allow revisits when the new route has fewer stops remaining | O(E·k log(E·k)) | O(V·k) | ⚠️ Correct once you track best-stops-per-node, but it's Dijkstra's with its defining feature switched off. Fiddly, and slower here |
| DFS/BFS over all routes | Enumerate every path of length ≤ k+1 | exponential | O(k) | ❌ |
| BFS level by level | Each level = one more flight; run k+1 levels, keeping the cheapest price per node | O(k·E) | O(V) | ✅ Same idea as below, expressed as BFS |
| **[Bellman-Ford](../algorithms/bellman-ford.md), k+1 rounds** | Relax every edge, k+1 times, from a per-round snapshot | O(k·E) | O(V) | ✅ |

**The decision:** [Bellman-Ford](../algorithms/bellman-ford.md), truncated to exactly `k + 1` relaxation rounds.

**Why Bellman-Ford is the natural fit.** Its central invariant is the thing this problem asks for: **after `i` rounds of relaxing every edge, `prices[v]` holds the cheapest route from `src` to `v` using at most `i` edges.** Full Bellman-Ford runs V−1 rounds because that's the longest a simple path can be. Here you just... stop early. Run `k + 1` rounds and the array holds exactly the answer you want.

Where Dijkstra's is greedy — commit to the cheapest node and never look back — Bellman-Ford is **iterative refinement**: it never commits, it just improves everything for one more hop each round. That refusal to commit is precisely what makes it survive the extra constraint.

**Why Dijkstra's fails, in one sentence for the interview:** *"Dijkstra's finalizes a node at its cheapest price, but under a hop limit a more expensive route with fewer hops can be strictly better — so the greedy choice isn't safe."*

**The subtle part — why you need a snapshot.** If you relax edges directly into `prices`, a value updated earlier in the round can be used again later in the *same* round. That's two flights taken in what's supposed to be one round, and you'd allow routes with more than `k+1` flights. So each round reads from the **previous** round's values and writes into a copy. This is the difference between "at most i edges" and "any number of edges," and it's the one line most people get wrong.

**Why not the BFS version?** It's equally correct and arguably more intuitive (a level *is* a flight). Bellman-Ford is more compact, needs no queue, and names a known algorithm — which is usually the better interview move.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
prices = [float("inf")] * n
prices[src] = 0
```
One slot per city, holding "cheapest known price to get here." [`float("inf")`](../syntax/float-inf.md) means *unreachable so far* — chosen because it compares greater than every real price, so the relaxation test needs no special case for "not yet reached."

The source costs 0 to reach. That single seeded value is what the rounds propagate outward.
→ [float-inf](../syntax/float-inf.md) · [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for _ in range(k + 1):
```
**`k + 1`, not `k`.** `k` stops means `k` intermediate cities, which is `k + 1` flights, and each round buys one more flight. `k = 0` → one round → direct flights only, matching example 2.

The loop variable is unused, so `_` — the round number never matters, only how many.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    tmp_prices = prices[:]   # snapshot so updates don't leak within a round
```
**The load-bearing line.** `prices[:]` is a shallow copy via [slicing](../syntax/list-slicing.md). This round *reads* from `prices` (frozen at the end of last round) and *writes* into `tmp_prices`.

Without it, a price improved early in the round could immediately feed a second improvement later in the same round — two flights for the price of one round — and the hop limit would silently stop being enforced. The result would still look like a shortest path, just not one obeying `k`.
→ [list-slicing](../syntax/list-slicing.md) · [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md)

```python
    for u, v, w in flights:
        if prices[u] != float("inf") and prices[u] + w < tmp_prices[v]:
            tmp_prices[v] = prices[u] + w
```
**Relaxation** — the heart of Bellman-Ford. For every flight `u → v` costing `w`: if `u` was reachable within the previous round's budget, then `v` is reachable this round for `prices[u] + w`. Keep it if it beats what `v` already has.

Two details. The `prices[u] != inf` guard prevents `inf + w` arithmetic from an unreached city (it wouldn't be *wrong* — `inf + w` is still `inf` — but it's explicit and avoids float weirdness). And note the asymmetry: it **reads `prices[u]`** (last round) but **compares against `tmp_prices[v]`** (this round), so several different flights into `v` within one round can each improve it. That's fine — they're all one hop from a previous-round value.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [comparison-operators](../syntax/comparison-operators.md) · [logical-operators](../syntax/logical-operators.md) · [bellman-ford](../algorithms/bellman-ford.md)

```python
    prices = tmp_prices
```
Commit the round. Now `prices` holds the best routes using at most (rounds-so-far) flights, and the next round builds on it.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
return prices[dst] if prices[dst] != float("inf") else -1
```
Still `inf` means no route within the hop budget existed → `-1`. Otherwise that's the cheapest legal price.
→ [ternary-expression](../syntax/ternary-expression.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:

        prices = [float("inf")] * n
        prices[src] = 0

        for _ in range(k + 1):
            tmp_prices = prices[:]   # snapshot so updates don't leak within a round

            for u, v, w in flights:
                if prices[u] != float("inf") and prices[u] + w < tmp_prices[v]:
                    tmp_prices[v] = prices[u] + w

            prices = tmp_prices

        return prices[dst] if prices[dst] != float("inf") else -1
```
</details>

**Trace it** — example 1: `flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`, `src = 0`, `dst = 3`, `k = 1` → 2 rounds.

Start: `prices = [0, inf, inf, inf]`

**Round 1** (reads `[0, inf, inf, inf]`):

| Flight | `prices[u]` | Candidate | Beats `tmp[v]`? | `tmp_prices` |
|---|---|---|---|---|
| `0→1` (100) | 0 | 100 | yes | `[0, 100, inf, inf]` |
| `1→2` (100) | **inf** | — | skipped | unchanged |
| `2→0` (100) | inf | — | skipped | unchanged |
| `1→3` (600) | **inf** | — | skipped | unchanged |
| `2→3` (200) | inf | — | skipped | unchanged |

End of round 1: `prices = [0, 100, inf, inf]` — exactly the cities reachable in **1 flight**.

The second row is the snapshot earning its keep. `tmp_prices[1]` is already 100, but the code reads **`prices[1]`**, which is still `inf`. Without the snapshot, `1→2` would have fired here and reached node 2 in what is supposed to be a one-flight round.

**Round 2** (reads `[0, 100, inf, inf]`):

| Flight | `prices[u]` | Candidate | Beats `tmp[v]`? | `tmp_prices` |
|---|---|---|---|---|
| `0→1` (100) | 0 | 100 | no (already 100) | unchanged |
| `1→2` (100) | 100 | 200 | yes | `[0, 100, 200, inf]` |
| `2→0` (100) | inf | — | skipped | unchanged |
| `1→3` (600) | 100 | **700** | yes | `[0, 100, 200, 700]` |
| `2→3` (200) | **inf** | — | skipped | unchanged |

Final: `prices = [0, 100, 200, 700]` → **700** ✅

The last row is the payoff. `tmp_prices[2]` is 200 by now, and 200 + 200 = 400 would be cheaper than 700 — but the code reads `prices[2]`, which is `inf`. That 400 route is `0 → 1 → 2 → 3`: three flights, two stops, **illegal at `k = 1`**. The snapshot is the only thing standing between you and that wrong answer of 400.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(k · E)</summary>

**O(k · E)**, where E = `len(flights)`.

- The outer loop runs **k + 1** times.
- Each round copies the array — O(V) — and relaxes **every edge exactly once** — O(E).
- Per round: O(V + E). Total: **O((k + 1)(V + E))** = **O(k · E)**, since E ≥ V − 1 on any connected graph.

With n = 100, k < 100, E ≤ 4950: about 100 × 5000 = **5 × 10⁵** operations. Comfortable.

**Compared to the alternatives:**
- Full Bellman-Ford would run V−1 rounds → O(V·E). Truncating at k+1 is strictly less work *and* it's what makes the answer correct, not just faster.
- The modified-Dijkstra's version is O(E·k log(E·k)) — the heap adds a log factor and the state space grows by a factor of k. **Bellman-Ford is genuinely the better algorithm here**, which is a satisfying inversion of the usual "Dijkstra's beats Bellman-Ford" instinct.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — two arrays of n floats, `prices` and `tmp_prices`.

- No adjacency list is built; the flat `flights` list is iterated directly. That's a real saving, and it's possible only because Bellman-Ford relaxes **all edges** each round and never asks "what are node u's neighbours?"
- No heap, no queue, no visited set.
- `tmp_prices = prices[:]` allocates a fresh O(n) list each round, but only two exist at a time, so the peak stays O(n).

That's notably leaner than the O(V + E) that Dijkstra's or a BFS variant would need. Not needing an adjacency list is one of Bellman-Ford's quiet advantages, and it's worth naming.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Without the stop limit this is plain Dijkstra's. The limit breaks it: Dijkstra's finalizes a node at its cheapest price and never revisits, but under a hop constraint a more expensive route using fewer hops can be strictly better, so the greedy choice isn't safe. Bellman-Ford fits naturally, because its invariant is exactly what I need — after i rounds of relaxing every edge, each entry holds the cheapest route using at most i edges. So I run k+1 rounds; k stops means k+1 flights. The critical detail is relaxing from a snapshot of the previous round's array, so an improvement made this round can't be chained into a second flight within the same round — otherwise the hop limit silently stops being enforced. O(k·E) time, O(n) space, and no adjacency list needed since I relax the flat edge list."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you make Dijkstra's work?" | Yes, but you have to disable its defining optimization: push `(price, node, stops_used)` and allow revisiting a node when the new route has *fewer stops*, tracking the best stop-count seen per node. It's Dijkstra's with finalization removed — correct, but O(E·k log(E·k)), slower than Bellman-Ford here. |
| "Why `k + 1` rounds?" | `k` **stops** = `k` intermediate cities = `k + 1` flights. `k = 0` must still allow a direct flight, which is one round. |
| "What breaks without the snapshot?" | Improvements chain within a round, so one round can represent many flights. You'd compute the unconstrained shortest path and ignore `k`. On example 1 you'd return 400 instead of 700. |
| "Negative prices?" | Bellman-Ford handles them, unlike Dijkstra's. And the k+1 truncation actually protects you — a negative cycle can't be exploited indefinitely with a bounded hop count. Full Bellman-Ford detects them with a V-th round that still improves something. |
| "Solve it as BFS." | Level-order from `src`, one level per flight, k+1 levels, keeping the cheapest price seen per node per level. Same O(k·E), and the "level = flight" framing is often easier to explain. |
| "Solve it as DP." | It already is one: `dp[i][v]` = cheapest price to `v` using at most `i` flights, with `dp[i][v] = min(dp[i-1][u] + w)` over all edges `u→v`. The two arrays are the rolled-up rows — the snapshot is the "previous row." |
| "Why iterate `flights` directly instead of building a graph?" | Bellman-Ford relaxes *every* edge each round in any order, so it never needs neighbour lookup. Skipping the adjacency list saves O(V + E) space. |

**Traps:**
- **Omitting the snapshot.** The defining bug of this problem. It produces a correct-looking shortest path that ignores `k`.
- **`range(k)` instead of `range(k + 1)`.** Off by one flight; `k = 0` returns `-1` on a valid direct route.
- Reaching for plain Dijkstra's because prices are non-negative. Non-negativity makes Dijkstra's *eligible*, not *correct* — the added constraint is what disqualifies it.
- Writing `tmp_prices[u] + w` instead of `prices[u] + w`. That reads this round's value and reintroduces chaining — the snapshot exists precisely to prevent it.
- Comparing against `prices[v]` instead of `tmp_prices[v]`, which can overwrite a better improvement already made this round.
- Forgetting the `inf` → `-1` conversion and returning `float("inf")`.

**This same move shows up in:** [Network Delay Time](743-network-delay-time.md) (the same graph, *without* the constraint — where Dijkstra's is correct) · [Swim in Rising Water](778-swim-in-rising-water.md) (adapting a shortest-path template by changing what's minimized) · [Rotting Oranges](994-rotting-oranges.md) (round-by-round propagation, where a level equals a time step) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (rolling arrays as compressed DP rows).

</details>

---
