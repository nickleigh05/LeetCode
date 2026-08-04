# 746. Min Cost Climbing Stairs

**Easy** · [LeetCode](https://leetcode.com/problems/min-cost-climbing-stairs/) · [Solution file (no hints)](../../problems/0500-0999/746.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

You're given an array `cost` where `cost[i]` is the cost of stepping **on** the i-th stair. Once you pay it, you may climb **1 or 2 stairs**. You may start from index `0` or index `1`. Return the **minimum cost** to reach the top of the floor — which is *past* the last stair.

```
cost = [10,15,20]                     →  15
        start at index 1, pay 15, take 2 steps to the top

cost = [1,100,1,1,1,100,1,1,100,1]    →  6
        indices 0 → 2 → 4 → 6 → 7 → 9 → top, paying 1 six times
```

**Constraints:** `2 <= cost.length <= 1000` · `0 <= cost[i] <= 999`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| climb **1 or 2 stairs** | Identical movement rules to [Climbing Stairs](70-climbing-stairs.md). The *structure* is already solved — only the question has changed |
| "**minimum** cost" | Not counting — **optimizing**. Where 70 summed the branches, here you take the cheaper one |
| `cost[i]` is paid to step **on** stair `i` | The cost lives on the **node**, not the edge. You pay for where you land, not for how far you jumped |
| "you may start from index 0 **or** 1" | Two entry points, both free to arrive at. That's why the base cases are both **0** rather than `cost[0]` and `cost[1]` |
| "reach the **top of the floor**" | The destination is index `n` — **one past the end** of the array, and it costs nothing. Miss this and you'll return the cost of reaching the last *stair* instead |
| `n <= 1000` | O(n) is trivially enough |

The recurrence comes from the same backwards question as 70. You're at position `i`. Where did you come from? Either `i-1` via a 1-step, or `i-2` via a 2-step. But now, instead of *adding* the possibilities, you take the **cheaper** — and you pay for the stair you left:

```
minCost(i) = min( minCost(i−1) + cost[i−1],
                  minCost(i−2) + cost[i−2] )
```

Read `minCost(i)` as "cheapest way to *arrive at* position i." Arriving is free; the payment happens for the stair you stood on to make the jump.

Two rows above deserve a second look together: the destination is `n`, not `n-1`, and starting is free. Those two facts are the entire difference between this problem and the version most people submit first.

🤔 **Before you open the next section:** in `[10,15,20]` the answer is 15, not 25. Which stairs did you actually pay for, and which did you skip entirely? What does that tell you about whether you must land on the last stair?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy — always take the cheaper next stair | Look one step ahead, pick the smaller cost | O(n) | O(1) | ❌ **Wrong.** A cheap stair now can force an expensive one later. Example 2 defeats it |
| Try every route | Recurse both branches, take the min | O(2ⁿ) | O(n) | ❌ Exponential, and the subproblems repeat |
| Recursion + memo | Same, cached | O(n) | O(n) + stack | ⚠️ Correct; carries a cache and n frames |
| DP array | `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])` | O(n) | O(n) | ⚠️ Correct, and the clearest to write first |
| **Two rolling variables** | Same recurrence, keeping only the last two | O(n) | **O(1)** | ✅ |

**The decision:** the recurrence bottom-up with **two rolling variables** — the same final form as [Climbing Stairs](70-climbing-stairs.md).

**Why greedy fails, and why it's worth saying so.** The tempting move is "at each stair, jump to whichever of the next two is cheaper." Run it on `[1,100,1,1,1,100,1,1,100,1]`: the local choices keep looking fine, and you drift into a position where paying a 100 is unavoidable. **A locally cheap step can commit you to a globally expensive path** — precisely the condition that rules out greedy and calls for DP. Naming a failing input is far stronger than asserting "greedy doesn't work."

**Why this is 70 with one operator changed.** Same movement rules, same two-cell dependency, same rolling-variable ending. The differences:
- `+` becomes `min` — **counting becomes optimizing**.
- Each branch carries a weight, `cost[i-1]` or `cost[i-2]`, because stepping isn't free.
- The target is `n`, one past the array.

That mapping is the most useful thing here. Once you see that *"count the ways"* and *"minimize the cost"* are the **same recurrence under a different combining operator**, a whole class of DP problems collapses into one template: `dp[i] = combine(dp[i-1] ⊕ w₁, dp[i-2] ⊕ w₂)`, where `combine` is `sum` for counting and `min`/`max` for optimizing.

**Why bottom-up over memoized recursion?** Same complexity, but no stack frames and no cache — and the array version then reduces to O(1) space in an obvious way, which the top-down version doesn't.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(cost)
one_back = 0
two_back = 0
```
`one_back` is the cheapest cost to **arrive at** the previous position; `two_back` the same for two positions back.

Both start at **0**, and that's the encoding of "you may start at index 0 or index 1" — arriving at either costs nothing, because you only pay when you *leave* a stair. Seeding these with `cost[0]` and `cost[1]` is the single most common wrong start.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
for i in range(2, n + 1):
```
Positions 0 and 1 are the free base cases, so the recurrence starts at 2. It ends at **`n`** — hence `n + 1` as the [range](../syntax/range-function.md) bound — because the top of the floor is one past the last stair.

That `n + 1` is the line that makes `[10,15,20]` return 15 instead of 30. The final iteration computes the cost of arriving *past* index 2, which is allowed to skip stair 2 entirely.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    current = min(one_back + cost[i - 1], two_back + cost[i - 2])
```
The recurrence. Two ways to reach position `i`:
- **One step**, from `i-1`: it cost `one_back` to get there, plus `cost[i-1]` to step off it.
- **Two steps**, from `i-2`: it cost `two_back` to get there, plus `cost[i-2]` to step off it.

Take the cheaper. Note the offsets: the *cost paid* is indexed by where you **were**, not where you're arriving — which is why it's `cost[i-1]` and not `cost[i]`. Getting this backwards is the other classic bug, and it also indexes out of bounds on the final iteration.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
    two_back = one_back
    one_back = current
```
Slide the window. Same as [70](70-climbing-stairs.md): update `two_back` **first**, or you overwrite the value you still need.
→ [variables-assignment](../syntax/variables-assignment.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
return one_back
```
The last iteration computed the cost of arriving at position `n` — the top — and the slide left it in `one_back`.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:

        n = len(cost)
        one_back = 0
        two_back = 0

        for i in range(2, n + 1):
            current = min(one_back + cost[i - 1], two_back + cost[i - 2])
            two_back = one_back
            one_back = current
        return one_back
```
</details>

**Trace it** — `cost = [10, 15, 20]`, so `n = 3` and the loop runs for `i = 2, 3`.

| `i` | from `i-1` | from `i-2` | `current` | `two_back` after | `one_back` after |
|---|---|---|---|---|---|
| 2 | `0 + cost[1]` = 0 + 15 = 15 | `0 + cost[0]` = 0 + 10 = **10** | **10** | 0 | 10 |
| 3 | `10 + cost[2]` = 10 + 20 = 30 | `0 + cost[1]` = 0 + 15 = **15** | **15** | 10 | 15 |

Return **15** ✅

The last row is the whole problem in miniature. Reaching position 3 — the top — from index 1 costs 15, which means **stair 2 is never stepped on at all**; its cost of 20 is simply skipped. That's why the destination has to be `n` rather than `n-1`: you are not required to land on the final stair.

**And the greedy counterexample**, `[1,100,1,1,1,100,1,1,100,1]`: one-step-lookahead greedy keeps taking the locally cheap option and ends up somewhere a 100 can't be avoided. The DP evaluates both branches at every position and finds the route paying 1 exactly six times → **6**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The loop runs from 2 to n → **n − 1 iterations**.
- Each iteration does two additions, one `min`, and two assignments — all **O(1)**. Both array reads are O(1) index lookups.
- n × O(1) = **O(n)**.

At n = 1000 that's a thousand operations. The constraint isn't remotely binding, which is a hint that the difficulty here is *index correctness*, not performance.

**Against the alternatives:** naive recursion over both branches is **O(2ⁿ)** — the same exponential blow-up as 70, for the same reason (the call tree branches twice, nothing is cached). Memoization or bottom-up bring it to O(n), because there are only n + 1 distinct positions to solve.

**Can it be faster?** No. Every stair's cost can affect the answer, so any correct algorithm must read all n values → **Ω(n)** is a hard floor. Unlike [Climbing Stairs](70-climbing-stairs.md), there's no matrix-exponentiation trick, because the weights differ at every step rather than following a fixed linear recurrence.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers (`n`, `one_back`, `two_back`, `current`), whatever the input size.

The `cost` array is input, not extra allocation, so it doesn't count.

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(n)** | Cache of n entries, plus up to n stack frames |
| Bottom-up DP array | **O(n)** | A `dp` array of size n + 1 |
| **Rolling variables** | **O(1)** | The recurrence reads exactly two positions back |

Same reduction as [70](70-climbing-stairs.md), for the same structural reason: **a fixed-width dependency window means a fixed number of variables suffices.** Writing the `dp` array version first is fine if it helps you think — collapsing it out loud is a good thing to demonstrate.

**What you give up:** the array. A follow-up asking *which stairs* were used would need it (or a parallel `choice[]` array) to reconstruct the path backwards.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Movement is identical to Climbing Stairs, so the structure carries over — but I want a minimum cost rather than a count, so the recurrence uses `min` instead of `+`, and each branch carries the cost of the stair I'm stepping off: `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`. Two details decide correctness. I compute up to index n, one past the last stair, because the top of the floor isn't a stair and I'm not required to land on the last one. And both base cases are 0, because starting at index 0 or 1 is free. Greedy fails — a cheap step now can force an expensive one later, which the second example demonstrates. Since the recurrence only looks two back, two rolling variables give O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the answer 15 and not 25 on `[10,15,20]`?" | Because stair 2 is never stepped on. From index 1, a 2-step lands past the array, at the top. The last stair is skippable — which is why the target is index n. |
| "Why are both base cases 0?" | The problem lets you start at index 0 *or* 1, so arriving at either is free. You pay `cost[i]` when you step off a stair, not when you begin on one. |
| "What if you could only start at index 0?" | Then arriving at 1 must come through 0, so it costs `cost[0]`. Seed `one_back = cost[0]`, `two_back = 0`, or handle position 1 explicitly. |
| "What if steps of size 1, 2, or 3 were allowed?" | Three terms in the `min`, three rolling variables. The template extends directly. |
| "Which stairs did you step on?" | Record the winning branch per position, or re-derive it by comparing the two candidates while walking backwards from n. That needs the O(n) array back. |
| "Prove greedy is wrong." | `[1,100,1,1,1,100,1,1,100,1]` → the answer is 6; one-step-lookahead greedy overpays. One concrete counterexample settles it. |
| "Can you beat O(n)?" | No — every cost can change the answer, so you must read them all. Ω(n) is a lower bound. |
| "How does this relate to Climbing Stairs?" | Same recurrence skeleton, different combining operator: `sum` counts routes, `min` optimizes them. That one substitution generalizes across most of 1-D DP. |

**Traps:**
- **Looping to `n-1` instead of `n`.** You compute the cost of reaching the *last stair* rather than the *top*, and return a too-large answer. The most-failed detail on this problem.
- **`cost[i]` instead of `cost[i-1]`/`cost[i-2]`.** Pays for the wrong stair, and indexes out of bounds when `i == n`.
- **Seeding the base cases with `cost[0]` and `cost[1]`.** Charges you for starting, which the statement explicitly makes free.
- Reaching for greedy because it's tagged Easy. The label describes the code length, not the reasoning.
- Sliding the rolling variables in the wrong order.
- Assuming you must land on the last stair. You don't — example 1 exists to prove it.

**This same move shows up in:** [Climbing Stairs](70-climbing-stairs.md) (the same recurrence with `+`, counting instead of minimizing) · [House Robber](198-house-robber.md) (a two-cell window with a take-or-skip choice at each index) · [Jump Game II](45-jump-game-ii.md) (minimizing steps along a line — where greedy *does* work, a useful contrast) · [Coin Change](322-coin-change.md) (minimize over several branches, the same `min`-of-subproblems shape).

</details>

---
