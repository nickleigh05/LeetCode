# 134. Gas Station

**Medium** · [LeetCode](https://leetcode.com/problems/gas-station/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There are `n` gas stations in a **circle**. Station `i` has `gas[i]` fuel, and it costs `cost[i]` fuel to travel from station `i` to station `i+1`. You begin with an **empty tank** at some station. Return the **starting station's index** that lets you complete the circuit once in the clockwise direction, or **`-1`** if it's impossible. The answer is **guaranteed unique** if it exists.

```
gas  = [1,2,3,4,5]
cost = [3,4,5,1,2]        →  3      start at station 3:
                                    tank 4 → 4-1=3 → +5=8, 8-2=6 → +1=7, 7-3=4 → +2=6, 6-4=2 → +3=5, 5-5=0 ✓

gas  = [2,3,4]
cost = [3,4,3]            →  -1     total gas 9 < total cost 10
```

**Constraints:** `n == gas.length == cost.length` · `1 <= n <= 10⁵` · `0 <= gas[i], cost[i] <= 10⁴` · the answer is unique when it exists.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| stations in a **circle** | Wraparound. The naive simulation has to handle indices modulo n, and trying every start is O(n²) |
| "start with an **empty tank**" | You can't borrow fuel. The running tank must stay **≥ 0** at every step |
| "return the starting index" or `-1` | A search *and* a feasibility test, bundled together |
| "the answer is **guaranteed unique**" | A strong hint. If a valid start exists, there's exactly one — so once you've proven a candidate can't be beaten, you're done |
| `n <= 10⁵` | n² = 10¹⁰ — the try-every-start simulation is dead. **O(n) required** |

Only `gas[i] - cost[i]` ever matters — the **net** fuel change at station `i`. Reframing in those terms:

> Find a starting point on a circular array of net values such that **every prefix sum from that point stays non-negative.**

Now two observations, and together they give the whole algorithm.

**First — the feasibility test is global.** If `sum(gas) < sum(cost)`, the total fuel available is less than the total needed, so **no** start can work: going all the way around costs more than the circuit provides. And the converse holds too — if `sum(gas) >= sum(cost)`, a valid start is **guaranteed to exist**. That's not obvious, and it's the fact the whole solution leans on. (Section 2 proves it.)

**Second — failure is informative.** Suppose you start at station `s` and run out of fuel arriving at station `f`. The naive response is to try `s+1` next. But something stronger is true:

> **No station between `s` and `f` can be a valid start either.**

Why? Because starting at `s`, your tank was non-negative at every station up to `f`. So arriving at any intermediate station `k`, you had **at least as much fuel** as someone who started fresh at `k` with an empty tank. If *you* couldn't make it to `f`, neither can they.

So a failure at `f` doesn't eliminate one candidate — **it eliminates the entire block from `s` through `f`**. Jump the candidate start to `f + 1` and keep going. That's what turns O(n²) into a single pass.

🤔 **Before you open the next section:** if the total gas is enough, and every failed prefix lets you skip forward, why does the *last* candidate you land on have to be correct — without ever wrapping around to verify it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Simulate from every start | For each `s`, drive the full circle | **O(n²)** | O(1) | ❌ 10¹⁰ at n = 10⁵ |
| Prefix sums + find the minimum | Build cumulative nets; the answer is just after the global minimum prefix | O(n) | O(n) | ✅ Correct, and a clean alternative derivation |
| Two pointers / deque over a doubled array | Sliding window on `2n` elements | O(n) | O(n) | ⚠️ Works, but heavier than needed |
| **Total check + single greedy pass** | Verify feasibility globally, then reset the candidate on every failure | **O(n)** | **O(1)** | ✅ |

**The decision:** the **global total check plus one greedy pass**.

**Why "total gas ≥ total cost" guarantees a solution exists.** This is the load-bearing claim, and it deserves a proper argument since the code's correctness depends on it entirely.

Think of the net values `d[i] = gas[i] - cost[i]`, and the running prefix sums `P[0], P[1], …, P[n-1]` starting from station 0. Let `m` be the index where the prefix sum is **smallest**. Now start the journey at station `m + 1`.

For any station `j` reached from there, your tank equals `P[j] - P[m]` (with wraparound adding the total, which is ≥ 0 by assumption). Since `P[m]` is the *global minimum*, `P[j] - P[m] >= 0` for every `j`. **The tank never goes negative.** So station `m + 1` always works when the total is non-negative.

That's the proof, and it also *is* the alternative solution: find the minimum prefix, answer with the index after it.

**Why the greedy pass finds that same station.** Every time the running tank dips below zero at station `i`, the algorithm resets the candidate to `i + 1`. The **last** such reset lands exactly on the station after the global minimum prefix — because that's the deepest dip, and no later dip occurs after it. So a single left-to-right pass converges on the right answer with no wraparound needed.

**And that's the answer to section 1's question.** You never verify the final candidate by driving the circle, because you don't need to: the total check already proved *some* start works, the skip argument proved every earlier candidate fails, and uniqueness means the survivor is it. **The verification is replaced by a proof.** That's the elegance of the solution, and it's what to articulate in an interview — the code looks almost too simple otherwise.

**Why not the prefix-sum version?** It's equally valid and arguably more obviously correct. It costs O(n) space if you materialize the prefixes (though a running minimum makes it O(1) too). The greedy version is shorter; mention both.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if sum(gas) < sum(cost):
    return -1
```
**The global feasibility test, and it does double duty.**

Going around the circle consumes `sum(cost)` and provides `sum(gas)`. If supply is short, no starting point can possibly work — the deficit is unavoidable regardless of where you begin.

But the more important role is what it establishes for the rest of the function: **once this check passes, a valid start is guaranteed to exist.** Everything below is a search for *which* one, never a test of *whether*. That's why no verification pass appears afterwards.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) · [list-basics](../syntax/list-basics.md)

```python
total = 0
start = 0
```
- **`total`** — the running tank level for the *current* candidate start. Not the global sum; it's reset whenever the candidate changes.
- **`start`** — the current best guess at the answer.

Both begin at 0: try station 0 first, with an empty tank.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(len(gas)):
```
A single left-to-right pass — **no wraparound, no modulo, no second lap.** That's surprising for a circular problem and is exactly what the proof in section 2 buys you.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    total += gas[i] - cost[i]
```
Collect the fuel at station `i`, then spend what it costs to leave. The **net** is all that matters, which is why the two arrays never need to be tracked separately.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [list-basics](../syntax/list-basics.md)

```python
    if total < 0:
        start = i + 1
        total = 0
```
**The greedy reset, and the whole algorithm lives here.**

A negative tank means the current candidate can't reach station `i + 1`. And by the skip argument from section 1, **no station from `start` through `i` can either** — anyone starting in that range arrives with less fuel than you had.

So jump the candidate all the way past the failure and start fresh with an empty tank. Note it's `i + 1`, not `start + 1`: you're discarding the entire failed block at once, which is what makes the pass linear instead of quadratic.

Resetting `total = 0` reflects starting over with an empty tank at the new candidate.
→ [comparison-operators](../syntax/comparison-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
return start
```
The last surviving candidate. **No verification** — the total check guaranteed some start works, every earlier candidate has been provably eliminated, and the answer is unique, so this must be it.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:

        if sum(gas) < sum(cost):
            return -1

        total = 0
        start = 0

        for i in range(len(gas)):
            total += gas[i] - cost[i]
            if total < 0:
                start = i + 1
                total = 0

        return start
```
</details>

**Trace it** — `gas = [1,2,3,4,5]`, `cost = [3,4,5,1,2]`

Total gas = 15, total cost = 15 → the check passes, so a solution exists.

Net values: `d = [-2, -2, -2, 3, 3]`

| `i` | net | `total` after | `total < 0`? | `start` after |
|---|---|---|---|---|
| 0 | −2 | −2 | **yes** | **1** (and `total` → 0) |
| 1 | −2 | −2 | **yes** | **2** (and `total` → 0) |
| 2 | −2 | −2 | **yes** | **3** (and `total` → 0) |
| 3 | +3 | 3 | no | 3 |
| 4 | +3 | 6 | no | 3 |

Return **3** ✅

Stations 0, 1, and 2 each fail immediately — every one has a negative net, so no journey can even leave them with fuel to spare. Station 3 begins the surplus, and from there the tank only grows. The final `total` of 6 is the surplus accumulated from index 3 onwards, which (since the grand total is 0) exactly offsets the deficit of −6 that will be incurred wrapping back around through stations 0–2.

**A case where the skip does real work** — `gas = [5,1,2,3,4]`, `cost = [4,4,1,5,1]`:

Totals: gas = 15, cost = 15 ✓. Nets: `d = [1, -3, 1, -2, 3]`

| `i` | net | `total` after | `total < 0`? | `start` after |
|---|---|---|---|---|
| 0 | +1 | 1 | no | 0 |
| 1 | −3 | −2 | **yes** | **2** |
| 2 | +1 | 1 | no | 2 |
| 3 | −2 | −1 | **yes** | **4** |
| 4 | +3 | 3 | no | 4 |

Return **4** ✅

Row 2 is the skip: the candidate was 0, the failure happened at index 1, and `start` jumps to **2** — not to 1. Station 1 is eliminated without ever being tried, because a traveller starting there would have had *less* fuel at index 1 than the one who started at 0 (who arrived carrying a surplus of 1). Row 4 does it again, discarding stations 2 and 3 together.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- `sum(gas)` and `sum(cost)` are two passes → **O(n)**.
- The main loop is a third pass → **O(n)**, with each iteration doing one subtraction, one addition, one comparison, and occasionally two assignments — all O(1).
- 3 × O(n) = **O(n)**.

At n = 10⁵ that's a few hundred thousand operations. Instant.

**Against the naive approach:** simulating from every start is **O(n²)** — 10¹⁰ at the limit, hopelessly slow. The saving comes entirely from the skip argument: **a failure at index `i` invalidates the whole block from `start` to `i` at once**, so across the entire run each index is "discarded" only once. That's an amortized argument, and it's why one pass suffices where n passes seemed necessary.

**Can it be one pass instead of three?** Yes — accumulate the grand total alongside the running tank in the same loop, then check it at the end:

```python
total_net = 0
tank = 0
start = 0
for i in range(len(gas)):
    net = gas[i] - cost[i]
    total_net += net
    tank += net
    if tank < 0:
        start = i + 1
        tank = 0
return start if total_net >= 0 else -1
```

Same O(n), one traversal instead of three. Worth mentioning; the three-pass version is clearer.

**Faster?** No. Any station's values can change the answer, so **Ω(n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers, `total` and `start`. `sum()` computes its result without allocating anything proportional to n, and neither input array is modified.

| Approach | Space | Why |
|---|---|---|
| Simulate every start | O(1) | But O(n²) time |
| Prefix-sum array | **O(n)** | If materialized — though a running minimum makes it O(1) |
| Doubled-array sliding window | **O(n)** | The 2n copy |
| **Greedy pass** | **O(1)** | Two running integers |

**Why nothing more is needed** is the interesting part. A circular problem normally suggests either duplicating the array (to linearize the wraparound) or doing modular index arithmetic. **This solution does neither** — it makes a single left-to-right pass and never wraps.

That's possible because the circularity was handled *analytically* rather than mechanically: the total check proves a solution exists, and the greedy proves where it must be. **The proof replaces the second lap.**

That's a genuinely transferable idea — **when a circular problem has a global invariant, you can often reason about the wraparound instead of simulating it.** Compare [House Robber II](213-house-robber-ii.md), which handles its circle differently, by splitting into two linear cases.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Only the net `gas[i] - cost[i]` matters, so I'm looking for a start where every prefix sum stays non-negative. Two facts make it linear. First, if total gas is less than total cost, no start works — and conversely, if total gas is enough, a valid start is *guaranteed* to exist. Second, if I start at `s` and run dry arriving at station `f`, then no station between `s` and `f` works either: starting at `s` I arrived at each of those with a non-negative tank, so anyone starting fresh there had *less* fuel and would fail no later than I did. So a failure lets me skip the whole block and jump the candidate to `f+1`. One pass, and I never need to wrap around or verify the final answer — the total check proved a solution exists, every earlier candidate is provably eliminated, and the answer is unique, so the survivor is it. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does total gas ≥ total cost guarantee a solution?" | Take the prefix sums of the nets and let `m` be the index of the global minimum. Starting at `m+1`, the tank at any station `j` is `P[j] − P[m]`, which is ≥ 0 since `P[m]` is the minimum. So `m+1` always works. |
| "Why can you skip the whole failed block?" | Starting at `s`, you reached every intermediate station with a non-negative tank — so you had at least as much fuel there as someone starting fresh. If you couldn't reach `f`, neither can they. |
| "Why don't you verify the final answer?" | You don't need to. The total check proved *some* start works; the skip argument eliminated everything before the survivor; uniqueness means it's the one. |
| "Solve it with prefix sums." | Compute cumulative nets, find the index of the global minimum, and return the index after it (mod n). Same O(n), and it's essentially the proof written as code. |
| "What if the answer weren't unique?" | The greedy still returns *a* valid start — the one just past the global minimum prefix. It just wouldn't be the only one. |
| "What if you could travel counter-clockwise?" | Run the same algorithm on the reversed arrays with costs shifted appropriately, and take whichever direction succeeds. |
| "Make it a single pass." | Accumulate the grand total inside the same loop and check it at the end, rather than calling `sum()` twice up front. |
| "What if you started with `k` fuel in the tank?" | Initialize `total = k` after each reset, and the feasibility condition becomes `sum(gas) + k >= sum(cost)`. |

**Traps:**
- **Resetting `start = start + 1` instead of `i + 1`.** Loses the skip entirely and makes the algorithm O(n²) — or worse, wrong, since the running total wouldn't correspond to the candidate.
- **Forgetting to reset `total = 0`.** The new candidate would inherit the old one's deficit.
- **Omitting the global total check.** Without it the loop still returns some index, and on an infeasible input that index is wrong rather than `-1`.
- Trying to verify the answer with a wraparound simulation. Harmless but unnecessary, and it suggests you haven't grasped why the proof suffices.
- Handling the circle by doubling the array or using modulo indices. Correct, but far more machinery than the problem needs.
- Assuming a station with negative net can never be the answer. It can — what matters is the *prefix sums* from the start, not any single station's value.

**This same move shows up in:** [Maximum Subarray](53-maximum-subarray.md) (discard a running total the moment it goes negative — the identical greedy reset, on a linear array) · [Jump Game](55-jump-game.md) (a single forward pass whose local decisions provably can't be improved) · [House Robber II](213-house-robber-ii.md) (a circular problem solved by reasoning about the wraparound rather than simulating it) · [Partition Labels](763-partition-labels.md) (a one-pass scan that commits to a boundary and never revisits it).

</details>

---
