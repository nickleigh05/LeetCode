# 70. Climbing Stairs

**Easy** · [LeetCode](https://leetcode.com/problems/climbing-stairs/) · [Solution file (no hints)](../../problems/0001-0499/70.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

You're climbing a staircase with `n` steps. Each time you can climb **1 or 2 steps**. In how many **distinct ways** can you reach the top?

```
n = 2  →  2      (1+1, 2)
n = 3  →  3      (1+1+1, 1+2, 2+1)
n = 5  →  8
```

**Constraints:** `1 <= n <= 45`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "in how many **distinct ways**" | A **counting** problem, not an optimization. You're summing possibilities, not taking a max or min |
| "1 or 2 steps" | At every point there are exactly **two choices**. That's a branching structure — and branching you have to *count* rather than *explore* is the classic DP signal |
| `1+2` and `2+1` are different | **Order matters.** This is a sequence-counting problem, not a combination-counting one |
| `n <= 45` | Small enough that O(n) is obviously fine — but big enough that **2ⁿ is not**. 2⁴⁵ is ~3.5 × 10¹³ |

Now the actual insight, and it's the move worth practising because every DP problem needs it: **think backwards from the goal, not forwards from the start.**

You're standing on step `n`. How did you get here? There are only two possibilities — your last move was a 1-step (so you were on `n-1`) or a 2-step (so you were on `n-2`). There is no third option, and the two cases don't overlap, because they differ in your final move.

So every route to `n` is *some route to `n-1`, plus a 1-step*, **or** *some route to `n-2`, plus a 2-step*:

```
ways(n) = ways(n − 1) + ways(n − 2)
```

That's Fibonacci. You just derived it from a staircase.

🤔 **Before you open the next section:** if you write that recurrence as a plain recursive function, `ways(5)` calls `ways(4)` and `ways(3)`, and `ways(4)` calls `ways(3)` and `ways(2)`… how many times does `ways(3)` get computed? What does that do to the running time?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Plain recursion | `ways(n) = ways(n-1) + ways(n-2)`, no memory | **O(2ⁿ)** | O(n) | ❌ Recomputes the same subproblems exponentially often. At n = 45 that's billions of calls |
| Recursion + memo (top-down) | Same, but cache each result | O(n) | O(n) + O(n) stack | ⚠️ Correct and easy — but it carries a dict *and* n stack frames |
| DP array (bottom-up) | `dp[i] = dp[i-1] + dp[i-2]`, filled left to right | O(n) | O(n) | ⚠️ Correct, no recursion — but stores n values when you only ever read 2 |
| **Two rolling variables** | Same recurrence, keeping only the last two values | O(n) | **O(1)** | ✅ |
| Closed form (Binet's) | `φⁿ/√5`, rounded | O(1) | O(1) | ⚠️ Cute, but floating-point precision fails for large n. Mention, don't submit |
| Matrix exponentiation | `[[1,1],[1,0]]ⁿ` by fast power | O(log n) | O(1) | ⚠️ Real, and the right answer if n were 10¹⁸. Overkill at n ≤ 45 |

**The decision:** the recurrence, computed bottom-up with **two rolling variables**.

**The reasoning path an interviewer wants to hear** is the top three rows, in order. Start with the recursion, because it's the honest expression of the idea. Notice it's exponential *because subproblems repeat* — `ways(3)` is recomputed in every branch. That's **overlapping subproblems**, one of the two conditions that define a DP problem. (The other, **optimal substructure**, is here too: the answer for `n` is built from exact answers for smaller `n`.)

Then fix it, and there are two directions. **Memoize** the recursion — same shape, cache added. Or **flip it bottom-up** — compute `ways(1)`, `ways(2)`, `ways(3)`… upward, so every value you need already exists. Bottom-up wins here because it removes the call stack entirely.

**Then the space optimization, which is the real point of this problem.** Look at `dp[i] = dp[i-1] + dp[i-2]`. You only ever read **two** cells back. Everything older is dead weight. So don't keep an array — keep two variables and slide them forward. O(n) → O(1).

That last move is a **template you'll reuse all unit long**: [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md), [House Robber](198-house-robber.md), and [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) all end in exactly this rolling-variable form. 70 is where you learn it on the simplest possible recurrence.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if n == 1:
    return 1
if n == 2:
    return 2
```
**Base cases**, and every DP needs them — they're the values the recurrence can't produce, because it would have to reach below the start of the problem.

One way up 1 stair. Two ways up 2 (`1+1` or `2`). Handling them up front also protects the loop below, which assumes two prior values already exist.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
two_back = 1
one_back = 2
```
The rolling window, seeded with the base cases. Read the names literally at the moment the loop is about to compute step 3: `one_back` is `ways(2)`, `two_back` is `ways(1)`.

Naming them `one_back` / `two_back` rather than `a` / `b` is worth the keystrokes — it keeps the recurrence readable and it's what stops you sliding them in the wrong order.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(3, n + 1):
```
Walk upward from the first step the recurrence can actually handle. `n + 1` because [`range`](../syntax/range-function.md) excludes its endpoint and step `n` is the one you want.

Notice `i` is never used in the body — it's a **counter, not an index**. That's the giveaway that no array exists here.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    current = one_back + two_back
```
The recurrence, verbatim: routes ending in a 1-step, plus routes ending in a 2-step. Every line above exists to make this one line valid.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
    two_back = one_back
    one_back = current
```
**Slide the window forward.** What was one back is now two back; the value just computed becomes one back.

Order matters: `two_back` must be updated **before** `one_back` is overwritten, or you'd copy the new value into both and compute `2 × ways(n-1)` from then on. Python's [tuple assignment](../syntax/swap-tuple-assign.md) — `two_back, one_back = one_back, current` — does both at once and sidesteps the ordering question entirely; that's the form used in [House Robber](198-house-robber.md).
→ [variables-assignment](../syntax/variables-assignment.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
return one_back
```
After the final slide, `one_back` holds the most recently computed value — `ways(n)`. Returning `current` would also work, but breaks if the loop never runs; `one_back` is always meaningful.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def climbStairs(self, n: int) -> int:

        if n == 1:
            return 1
        if n == 2:
            return 2

        two_back = 1
        one_back = 2

        for i in range(3, n + 1):
            current = one_back + two_back
            two_back = one_back
            one_back = current
        return one_back
```
</details>

**Trace it** — `n = 5`

Start: `two_back = 1` (ways to step 1), `one_back = 2` (ways to step 2).

| `i` | `current = one_back + two_back` | `two_back` after | `one_back` after |
|---|---|---|---|
| 3 | 2 + 1 = **3** | 2 | 3 |
| 4 | 3 + 2 = **5** | 3 | 5 |
| 5 | 5 + 3 = **8** | 5 | 8 |

Return **8** ✅

The sequence 1, 2, 3, 5, 8 is Fibonacci offset by one position — which is the sanity check to reach for whenever you suspect an off-by-one in the base cases.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The loop runs from 3 to n → **n − 2 iterations**.
- Each iteration does one addition and two assignments — all **O(1)**.
- n × O(1) = **O(n)**.

**The comparison that matters.** Naive recursion on the same recurrence is **O(2ⁿ)**, because the call tree branches twice at every level and nothing is cached. Memoization collapses it to O(n) — each of the n subproblems is solved once, and every later request is a cache hit. Bottom-up gets the same O(n) with no cache and no stack.

Being able to say *"exponential → linear, and the reason is that there are only n distinct subproblems"* is the whole DP pitch, and it lands better than announcing "it's DP."

**If they push:** matrix exponentiation on `[[1,1],[1,0]]` gives **O(log n)**, which genuinely matters if n were 10¹⁸. At n ≤ 45 it's decoration, but knowing it exists is a real signal.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — genuinely constant. Four integers (`two_back`, `one_back`, `current`, `i`), regardless of n.

This is the payoff of the rolling-variable form, and it's worth naming what it replaced:

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(n)** | A cache with n entries *plus* n stack frames — two separate O(n) costs |
| Bottom-up DP array | **O(n)** | The `dp` array. No stack, but every value is retained |
| **Rolling variables** | **O(1)** | The recurrence reads exactly two cells back, so nothing older is ever needed |

The general rule to carry forward: **if `dp[i]` depends only on a fixed window of recent entries, the array can be replaced by that many variables.** Two cells back → two variables. It applies unchanged to [746](746-min-cost-climbing-stairs.md), [198](198-house-robber.md), and most of this unit.

The one thing you lose is the array itself. If a follow-up asked *"which sequence of steps?"* rather than *"how many?"*, you'd need the history back.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'll think backwards from step n. The last move was either a 1-step from n−1 or a 2-step from n−2 — those are the only options and they don't overlap — so `ways(n) = ways(n-1) + ways(n-2)`. That's Fibonacci. Written as plain recursion it's O(2ⁿ) because subproblems repeat, which is the signal for DP. I could memoize, but bottom-up is cleaner: build up from the base cases so every value I need already exists. And since the recurrence only ever looks two cells back, I don't need an array at all — two rolling variables give me O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if you can take 1, 2, or 3 steps?" | `ways(n) = ways(n-1) + ways(n-2) + ways(n-3)` — the Tribonacci sequence. Three rolling variables, three base cases. Same shape. |
| "What about an arbitrary set of step sizes?" | `ways(n) = Σ ways(n − s)` over each allowed `s`. Now you need a real `dp` array of size n+1, because the window isn't fixed — back to O(n) space. |
| "What if some steps are broken and can't be landed on?" | Set `dp[i] = 0` for those. With rolling variables, zero the current value when `i` is broken. |
| "Can you do better than O(n)?" | Matrix exponentiation: raise `[[1,1],[1,0]]` to the n-th power by fast doubling → O(log n). Or Binet's closed form, though floating-point error breaks it for large n. |
| "Write the top-down version." | `@cache` on a recursive `ways(i)` with `if i <= 2: return i`. Same complexity, and worth knowing — some problems are far easier expressed top-down. |
| "Why isn't this just combinatorics?" | You *can* count it directly: for each number `k` of two-steps, there are `C(n-k, k)` arrangements, summed over k. That's a valid closed form, and it produces Fibonacci — but it's more work than the recurrence. |
| "Does order really matter?" | Yes — `1+2` and `2+1` are distinct routes. That's exactly why the answer is Fibonacci rather than `⌊n/2⌋ + 1`. |

**Traps:**
- **Base cases off by one.** `ways(2) = 2`, not 1. Check that the sequence starts 1, 2, 3, 5 — if you get 1, 1, 2, 3 you've seeded standard Fibonacci instead of this problem's offset.
- **Sliding the variables in the wrong order** — assigning `one_back` before `two_back` clobbers the value you still need.
- Submitting the naive recursion. It's correct, and it times out; at n = 45 it's roughly 10¹³ calls.
- `range(3, n)` instead of `range(3, n + 1)` — computes `ways(n-1)` and returns it confidently.
- Reaching for a `dp` array by reflex and never noticing the O(1) improvement. The array version is *accepted*; the rolling version is what gets remarked on.

**This same move shows up in:** [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) (identical structure, `min` instead of `+` — the counting-to-optimizing switch) · [House Robber](198-house-robber.md) (same two-cell window, with a choice at each step) · [Decode Ways](91-decode-ways.md) (Fibonacci-shaped counting, but each step is conditional on the digits) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (rolling variables again, with more state per step).

</details>

---
