# 45. Jump Game II

**Medium** · [LeetCode](https://leetcode.com/problems/jump-game-ii/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Same setup as [Jump Game](55-jump-game.md): you start at index 0, and `nums[i]` is the **maximum** jump length from that position. This time, return the **minimum number of jumps** to reach the last index. The test cases guarantee the end **is** reachable.

```
nums = [2,3,1,1,4]   →  2      index 0 → 1 (one step), then 1 → 4 (three steps)
nums = [2,3,0,1,4]   →  2
nums = [0]           →  0      already at the last index
```

**Constraints:** `1 <= nums.length <= 10⁴` · `0 <= nums[i] <= 1000` · the last index is always reachable.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** number of jumps" | Optimization, not feasibility. [55](55-jump-game.md) asked *whether*; this asks *how few* |
| "`nums[i]` is the **maximum** jump length" | Same as 55 — every index up to `i + nums[i]` is reachable, so reach is an **interval** |
| "the end is always reachable" | No failure case to detect. That's a real simplification: no `-1`, no early bail |
| jumps go forward only | Progress is monotonic, so there are no cycles |
| `n <= 10⁴` | n² = 10⁸ is too slow. **O(n) intended** |

The reframing that unlocks this: **think of it as BFS on an unweighted graph.**

Each index is a node, and there's an edge from `i` to every index in `i+1 .. i+nums[i]`. All edges cost 1 jump. So "minimum jumps" is exactly **shortest path in an unweighted graph**, which BFS solves — and BFS's *level number* is the answer.

Now, what does a BFS level look like here?

- **Level 0:** just index 0.
- **Level 1:** everything reachable in one jump — indices `1 .. nums[0]`.
- **Level 2:** everything reachable in two jumps — from any index in level 1.

And here's the key structural fact, inherited from [55](55-jump-game.md): because jump lengths are *maximums*, **each level is a contiguous interval of indices**. Level 1 is a range, level 2 is the range just after it, and so on.

That means you don't need a queue. **A level is fully described by its right endpoint**, so BFS collapses into a single scan with two numbers:

- `current_end` — the last index of the level you're currently walking through.
- `farthest` — the farthest index reachable from anything seen so far, which will become the *next* level's right endpoint.

Walk left to right. Every time you step past `current_end`, you've exhausted the current level, so you've taken **one more jump** — increment the counter and set the new boundary to `farthest`.

**That's BFS without a queue**, and the whole thing is O(1) space.

🤔 **Before you open the next section:** the loop below stops at `len(nums) - 1` rather than `len(nums)`. What would go wrong if it ran all the way to the end? Think about what happens when `i` lands exactly on the last index.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion over every jump | Try all lengths, take the min | **O(2ⁿ)** | O(n) | ❌ Exponential |
| DP array | `dp[i]` = min jumps to reach `i`, filled left to right | O(n²) | O(n) | ⚠️ Correct; each index scans its whole range. 10⁸ at the limit |
| Actual BFS with a queue | Level-order over the index graph | O(n) | O(n) | ✅ Correct, and the right *mental model* — but the queue is unnecessary |
| Greedy "always jump farthest" | From each landing spot, jump the maximum distance | O(n) | O(1) | ❌ **Wrong.** Jumping maximally can overshoot a high-value cell. `[3,1,1,1,1,1,1,1]`-style inputs break it |
| **Implicit BFS levels** | Track the current level's boundary and the next level's reach | **O(n)** | **O(1)** | ✅ |

**The decision:** **implicit BFS by levels** — one pass, three integers.

**Why "always jump the farthest" is wrong**, since it's the greedy people reach for first. The strategy commits to a *landing spot*, and the best landing spot isn't the farthest one — it's the one with the best onward reach. Consider `nums = [2, 3, 1, 1, 4]`: jumping maximally from index 0 lands on index 2 (value 1), then index 3 (value 1), then index 4 — **three jumps**. Jumping just one step to index 1 (value 3) reaches the end in **two**. **The greedy that commits fails; the greedy that tracks a frontier succeeds.**

That's the same distinction as in [55](55-jump-game.md), and it's the lesson of this pair: **a correct greedy here records what's reachable, it doesn't choose where to land.**

**Why the levels are contiguous** — this is what licenses the O(1) collapse. Since `nums[i]` is a *maximum*, everything from `i+1` to `i+nums[i]` is reachable in one more jump. Union those ranges across a whole level and you get another contiguous range, because they all start adjacent to or inside the current level. **A contiguous range is described by its endpoint alone**, so the queue's contents are redundant.

Had jumps been *exact* distances, levels would be scattered sets and you'd need a real queue — O(n) space, and a genuine BFS.

**Why not the O(n²) DP?** It's correct, and at n = 10⁴ it's 10⁸ operations — likely a timeout, and it recomputes per-index what a running frontier already knows.

**Why is this in the Greedy unit and not Graphs?** Because the queue disappears. What's left is a linear scan making irrevocable local decisions — the *shape* of a greedy algorithm, even though the *justification* is a BFS argument. Being able to say "this is BFS whose queue collapsed to two integers" is the strongest one-line description of the solution.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
jumps = 0
current_end = 0   # farthest index reachable within the current jump
farthest = 0      # farthest index reachable seen so far
```
Three integers, and the comments carry the meaning:

- **`jumps`** — the level number, i.e. how many jumps have been taken to reach the level currently being walked.
- **`current_end`** — the right boundary of the current level. Crossing it means another jump was needed.
- **`farthest`** — the best reach discovered while scanning the current level. It becomes the *next* level's boundary.

All start at 0: you begin at index 0, having taken no jumps, with level 0 being the single index `[0, 0]`.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(len(nums) - 1):
```
**Stop one short of the end** — this is the detail from section 1's question, and it's what makes the count correct.

If the loop ran to `len(nums) - 1` inclusive and the last index happened to equal `current_end`, the `if` would fire and increment `jumps` **after** you'd already arrived. You'd return one too many.

Stopping early is safe because arriving at the last index is the goal, not a place you jump *from*. It also handles `[0]` correctly: the loop body never runs and the answer is **0**.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    farthest = max(farthest, i + nums[i])
```
**Extend the next level's reach.** From index `i` you can land anywhere up to `i + nums[i]`, so the next boundary is at least that far.

`max` rather than assignment, because a later index in the level doesn't necessarily reach farther — index 0's jump can dominate several that follow.

This is the identical line from [55](55-jump-game.md); the difference is entirely in what happens next.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if i == current_end:
        jumps += 1
        current_end = farthest
```
**The level transition, and it's the whole algorithm.**

Reaching `current_end` means you've walked the entire current level and examined every index in it. Everything beyond requires **one more jump** — so increment the counter and set the new boundary to `farthest`, which by now holds the union of every reach in the level just finished.

Two things worth being precise about:

- **`==`, not `>=`.** You want to fire exactly once per level, at its final index. `>=` would be equivalent here (since `i` increments by 1 and `current_end` only ever grows), but `==` states the intent.
- **`farthest` is complete at this moment.** Because it was updated on the line above *before* the check, index `i`'s own reach is already folded in. Reversing the two lines would exclude the level's last index from its own level's reach — an off-by-one that's easy to introduce and hard to spot.
→ [comparison-operators](../syntax/comparison-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [bfs](../algorithms/bfs.md)

```python
return jumps
```
The number of level transitions crossed, which is the minimum number of jumps.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def jump(self, nums: List[int]) -> int:

        jumps = 0
        current_end = 0   # farthest index reachable within the current jump
        farthest = 0      # farthest index reachable seen so far

        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])

            if i == current_end:
                jumps += 1
                current_end = farthest

        return jumps
```
</details>

**Trace it** — `nums = [2, 3, 1, 1, 4]`, so the loop runs for `i = 0 .. 3`

| `i` | `nums[i]` | reach `i + nums[i]` | `farthest` after | `i == current_end`? | `jumps` | `current_end` after |
|---|---|---|---|---|---|---|
| 0 | 2 | 2 | **2** | 0 == 0 ✓ | **1** | **2** |
| 1 | 3 | **4** | **4** | 1 == 2 ✗ | 1 | 2 |
| 2 | 1 | 3 | 4 | 2 == 2 ✓ | **2** | **4** |
| 3 | 1 | 4 | 4 | 3 == 4 ✗ | 2 | 4 |

Return **2** ✅

Reading it as BFS levels makes the structure obvious:

- **Level 0** = index `[0, 0]`. Its reach is 2, so level 1 will be indices 1–2. The transition at `i = 0` sets `jumps = 1`.
- **Level 1** = indices `[1, 2]`. Walking it, index 1 reaches **4** and index 2 reaches 3, so the level's combined reach is 4. The transition at `i = 2` sets `jumps = 2` and `current_end = 4`.
- **Level 2** = indices `[3, 4]`, which contains the last index. Done — 2 jumps.

Row 2 is the payoff. Index 1 has the high value of 3, and even though the algorithm "walks past" it without committing, its reach is folded into `farthest` and becomes the next boundary. **That's how the frontier avoids the trap** that sinks "always jump the farthest": the greedy-maximal strategy would land on index 2 and never benefit from index 1's value at all.

And row 4 shows why the loop stops early: at `i = 3`, `current_end` is already 4 — the last index. If the loop continued to `i = 4`, the check `4 == 4` would fire and return **3** instead of 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the array, stopping one short → **n − 1 iterations**.
- Each iteration does one addition, one `max`, one comparison, and occasionally two assignments — all **O(1)**.
- **O(n)** total.

At n = 10⁴ that's ten thousand operations. Instant.

**Against the alternatives:** the DP array is **O(n²)** — each index scans up to `nums[i]` destinations, so with values up to 1000 that's ~10⁷–10⁸ operations at the limit. A real BFS with a queue is also O(n) (each index enqueued once), but it costs O(n) space for no benefit.

**The thing worth stating:** this is BFS, and BFS on a graph with V nodes and E edges is O(V + E). Here E could be up to 10⁷ (each index connecting to up to 1000 others), yet the scan is O(n) — because **the interval structure lets you process a whole level's worth of edges with a single `max`**, never enumerating them individually.

**Faster?** No. Any index's value can change the answer, so **Ω(n)** is a lower bound.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers, regardless of input size. Nothing allocated, input unmodified.

| Approach | Space | Why |
|---|---|---|
| Recursion + memo | **O(n)** | Cache plus call stack |
| DP array | **O(n)** | One entry per index |
| BFS with a queue | **O(n)** | The queue holds a level's worth of indices |
| **Implicit BFS levels** | **O(1)** | Each level is a contiguous interval, described by its endpoint |

**The collapse is the same one as [55](55-jump-game.md), applied to levels rather than to overall reach.** A BFS queue exists to remember *which* nodes are in the current frontier. When the frontier is guaranteed contiguous, remembering its endpoint is equivalent to remembering its contents — so the queue is pure redundancy.

That's a genuinely reusable observation: **whenever a BFS frontier has structure (an interval, a range, a monotone set), the queue can often be replaced by a couple of bounds.**

**What would break it:** exact-distance jumps. Levels would become scattered sets, an endpoint wouldn't describe them, and you'd need the real queue and O(n) space.

**What you'd need extra state for:** returning the actual sequence of jump positions. Record which index supplied `farthest` at each level transition, then reconstruct — O(number of jumps) extra.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is shortest path on an unweighted graph — each index connects to everything within its jump range, every edge costs one jump — so it's BFS, and the answer is the level number. The key structural fact is that because `nums[i]` is a maximum, each BFS level is a *contiguous interval* of indices. So I don't need a queue: a level is fully described by its right endpoint. I sweep left to right tracking two bounds — the current level's end, and the farthest reach discovered while scanning it. When I step past the current end, that's one more jump, and the new boundary becomes the farthest reach. I stop one index short of the end, because arriving is the goal, not a place I jump from — otherwise I'd count one jump too many. O(n) time, O(1) space. And note the naive greedy of always jumping the maximum distance is wrong: on `[2,3,1,1,4]` it takes three jumps because it overshoots the high-value index 1."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not always jump as far as possible?" | Because the best landing spot isn't the farthest — it's the one with the best onward reach. `[2,3,1,1,4]`: jumping maximally gives 3 jumps; stepping to index 1 gives 2. The frontier approach never commits to a landing spot. |
| "Why does the loop stop at `n-1`?" | Arriving at the last index ends the process. If the loop ran to `n-1` inclusive and that index equalled `current_end`, the counter would increment after arrival — one jump too many. |
| "Why is this BFS?" | Indices are nodes, jump ranges are edges, all edges cost 1. Minimum jumps is shortest path, and BFS's level number is the answer. The queue vanishes because levels are contiguous. |
| "What if the end weren't guaranteed reachable?" | Add [55](55-jump-game.md)'s check — if `i > farthest`, return −1. The two problems compose directly. |
| "What if jumps were exact distances?" | Levels would be scattered sets, so the endpoint wouldn't describe them. You'd need a real BFS queue, O(n) space. |
| "Return the actual jump positions." | Record which index provided `farthest` at each transition, then reconstruct. O(jumps) extra space. |
| "What if jump costs varied per index?" | Then edges are weighted and BFS no longer applies — you'd need [Dijkstra's](743-network-delay-time.md) or a DP. |
| "Can you do it backwards?" | Yes — repeatedly find the *earliest* index that can reach the current target, counting steps. It's O(n²) unless you're careful, so the forward scan is preferred. |

**Traps:**
- **Running the loop to the last index.** Off by one jump whenever the last index coincides with a level boundary. The defining bug here.
- **Updating `farthest` after the boundary check** instead of before — excludes the level's final index from its own level's reach.
- **Committing to the maximal jump.** The wrong greedy; `[2,3,1,1,4]` catches it.
- Assigning instead of maximizing `farthest`.
- Initializing `jumps = 1`. It must start at 0 — `[0]` needs zero jumps.
- Reaching for the O(n²) DP by reflex. Correct but likely too slow, and it misses the interval structure.

**This same move shows up in:** [Jump Game](55-jump-game.md) (the same frontier, answering feasibility instead of counting) · [Rotting Oranges](994-rotting-oranges.md) (BFS where the level number *is* the answer, with an explicit queue since the frontier isn't contiguous) · [Word Ladder](127-word-ladder.md) (BFS levels counting steps) · [Maximum Subarray](53-maximum-subarray.md) (a greedy one-pass scan with O(1) state).

</details>

---
