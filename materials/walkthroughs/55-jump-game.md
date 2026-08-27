# 55. Jump Game

**Medium** · [LeetCode](https://leetcode.com/problems/jump-game/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an integer array `nums`. You start at the **first index**, and each `nums[i]` is the **maximum** jump length from that position. Return `true` if you can reach the **last index**, otherwise `false`.

```
nums = [2,3,1,1,4]   →  true     jump 1 step to index 1, then 3 steps to the end
nums = [3,2,1,0,4]   →  false    every route lands on index 3, whose value is 0 — a dead stop
nums = [0]           →  true     already at the last index
```

**Constraints:** `1 <= nums.length <= 10⁴` · `0 <= nums[i] <= 10⁵`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return true/false" | **Feasibility**, not counting and not optimizing. You need to know *whether*, not *how* |
| "`nums[i]` is the **maximum** jump length" | You may jump **any** distance from 1 to `nums[i]` — not exactly `nums[i]`. That flexibility is what makes the greedy work |
| jumps always go **forward** | No backtracking, so progress is monotonic. There's no cycle to worry about |
| a `0` means you're stuck | Landing on a 0 ends the run — unless you're already at the last index |
| `n <= 10⁴` | n² = 10⁸ is borderline; **O(n) is clearly intended** |

Start with the honest brute force: from each index, try every jump length, recurse. That's exponential. Memoizing on the index gives O(n²) — for each of n positions, scan up to n destinations. Both work; both are more than this problem needs.

The reframing that collapses it: **you don't care about paths at all.**

Ask instead — *what is the farthest index I could possibly be at, given everything I've seen so far?* Call it `farthest`. Then:

- Standing at index `i` with `farthest >= i`, you can definitely **get** to `i`.
- From `i`, you can extend your reach to `i + nums[i]`.
- So `farthest = max(farthest, i + nums[i])`.

And here's the part that makes it a feasibility test rather than a search: **if you ever reach an index `i` with `i > farthest`, that index is unreachable** — and since jumps only go forward, so is everything after it. You're stuck; return false immediately.

The key realization is that **reachability is an interval, not a set.** If you can reach index 7, you can reach every index from 0 to 7 — because from any position you may jump *any* distance up to the maximum, including 1. So "where can I get to" is fully described by a **single number**, not a collection.

That's why one variable suffices and why no path bookkeeping is needed.

🤔 **Before you open the next section:** why is it safe to take `max(farthest, i + nums[i])` at *every* index, rather than deciding which index to actually jump from? What would you lose by committing to a specific jump?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion over every jump length | Branch on all 1..`nums[i]` choices | **O(2ⁿ)** | O(n) | ❌ Exponential |
| Recursion + memo on the index | Cache "can I reach the end from here?" | O(n²) | O(n) | ⚠️ Correct; n² inner steps because each index scans its whole range |
| Bottom-up DP | `dp[i]` = can reach the end from `i`, filled right to left | O(n²) | O(n) | ⚠️ Same bound, no recursion |
| Work backwards greedily | Track the leftmost index from which the end is reachable | O(n) | O(1) | ✅ Also correct, and a nice alternative framing |
| **Forward greedy frontier** | One pass, tracking the farthest reachable index | **O(n)** | **O(1)** | ✅ |

**The decision:** the **forward greedy frontier** — one pass, one variable.

**Why the greedy is safe** — the answer to section 1's question, and the thing to be able to argue. At index `i` you are *not* committing to a jump. You're recording a **fact**: the reach from `i` is `i + nums[i]`, and since reachability is an interval, the union of all reaches seen so far is just their maximum. **Taking the max at every index loses nothing, because you never had to choose.** There's no scenario where jumping from an earlier index gets you *farther* than the best `i + nums[i]` you've recorded — that's exactly what the max is over.

Contrast a greedy that *does* commit, like "always jump the maximum distance." That one is wrong: `[2,3,1,1,4]` — jumping 2 from index 0 lands on index 2 (value 1), then index 3 (value 1), then index 4. It happens to work here, but the strategy can skip over a high-value cell. **The frontier greedy avoids the trap by never committing to a landing spot at all.**

**Why the interval property matters so much.** Because `nums[i]` is a *maximum* rather than an exact distance, everything up to `i + nums[i]` is reachable — not just that one index. Had the problem said "jump exactly `nums[i]`," reachability would be a scattered set, one number wouldn't describe it, and you'd genuinely need DP or BFS. **One word in the statement is worth an entire complexity class here**, and noticing it is the mark of having read carefully.

**Why not the O(n²) DP?** It's correct and at n = 10⁴ it's 10⁸ operations — likely too slow, and certainly wasteful. The DP recomputes reachability per index when a single running number captures all of it.

**The backwards variant**, worth knowing as an alternative: start with `target = n - 1`, sweep right to left, and whenever `i + nums[i] >= target` set `target = i`. If `target` ends at 0, the end is reachable. Same O(n)/O(1), different intuition — *"pull the goalpost backwards."* Some people find it more obviously correct.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
farthest = 0
```
**The frontier** — the largest index reachable using everything examined so far.

Starting at 0 says "I can reach index 0," which is true by definition since that's where you begin. It's also what makes the single-element case `[0]` work: the loop's first check passes, nothing else happens, and the function returns `True`.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i, num in enumerate(nums):
```
One left-to-right pass. [`enumerate`](../syntax/enumerate.md) gives the index and value together — both are needed, since the reach from a position is `index + value`.

Sweeping forwards is essential: `farthest` must reflect every position **up to** `i` before `i` is tested for reachability.
→ [enumerate](../syntax/enumerate.md) · [for-loop](../syntax/for-loop.md)

```python
    if i > farthest:
        return False
```
**The failure test, and it comes first.** If the current index lies beyond the frontier, nothing seen so far can reach it — and since jumps only move forward, no *later* index can help either. You're stranded.

This ordering matters. Checking reachability **before** extending the frontier means you never use position `i`'s jump value to justify standing on `i`. Swap the two statements and `[0, 1]` would wrongly report `True`: the 0 at index 0 would extend `farthest` to 0, and index 1's check would then be skipped.

The early return is also what makes this efficient on hopeless inputs — no need to scan the rest.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    farthest = max(farthest, i + num)
```
**Extend the frontier.** From index `i` you can land anywhere up to `i + num`, so the reachable interval grows to the larger of what it was and what `i` offers.

`max` rather than plain assignment, because a later index doesn't necessarily reach farther — `[5, 1, 1, 1, 1, 1]` has index 0 dominating everything after it. **Overwriting instead of maximizing would shrink the frontier** and produce false negatives.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return True
```
The loop completed without ever finding an unreachable index — which means every index, including the last, was within the frontier when it was examined.

Note there's no explicit `farthest >= len(nums) - 1` check at the end. It's unnecessary: reaching the final iteration without returning `False` already proves the last index was reachable.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:

        farthest = 0

        for i, num in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + num)

        return True
```
</details>

**Trace it** — `nums = [2, 3, 1, 1, 4]`

| `i` | `num` | `i > farthest`? | reach `i + num` | `farthest` after |
|---|---|---|---|---|
| 0 | 2 | 0 > 0? no | 0 + 2 = 2 | **2** |
| 1 | 3 | 1 > 2? no | 1 + 3 = **4** | **4** |
| 2 | 1 | 2 > 4? no | 2 + 1 = 3 | 4 |
| 3 | 1 | 3 > 4? no | 3 + 1 = 4 | 4 |
| 4 | 4 | 4 > 4? no | 4 + 4 = 8 | 8 |

Loop finishes → **true** ✅

Row 3 shows why `max` is needed: index 2's reach is only 3, but `farthest` stays at 4 because index 1 already got there. Overwriting would have lost that.

**And the failing case**, `nums = [3, 2, 1, 0, 4]`:

| `i` | `num` | `i > farthest`? | reach | `farthest` after |
|---|---|---|---|---|
| 0 | 3 | no | 3 | **3** |
| 1 | 2 | 1 > 3? no | 3 | 3 |
| 2 | 1 | 2 > 3? no | 3 | 3 |
| 3 | **0** | 3 > 3? no | 3 + 0 = 3 | **3** |
| 4 | 4 | **4 > 3? yes** | — | — |

Return **false** ✅

The frontier stalls at 3 for three consecutive indices — none of 1, 2, or 3 can push past what index 0 already achieved, and index 3's value of 0 contributes nothing. When the loop reaches index 4, it's outside the frontier and the answer is settled.

That's the whole shape of a failure: **a `0` that no earlier jump can leap over.** Note it's not enough for a 0 to exist — `[3,2,1,0,4]` fails, but `[4,2,1,0,4]` would succeed, because index 0 reaches index 4 directly.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the array → at most **n iterations**.
- Each iteration does one comparison, one addition, and one `max` — all **O(1)**.
- **O(n)** total.

At n = 10⁴ that's ten thousand operations. Instant.

**Best case is better:** the function returns `False` the moment it hits an unreachable index, so `[0, 0, 0, …, 0]` exits on the second iteration — **O(1)**. The O(n) bound is the worst case (a reachable end), not the only case.

**Against the alternatives:** the memoized DP is **O(n²)**, because each index scans every destination in its jump range. At n = 10⁴ that's 10⁸ operations — probably too slow, and definitely unnecessary. Unmemoized recursion is **O(2ⁿ)**.

**Faster?** No. A single value anywhere in the array can flip the answer — turning one entry into a 0 can strand everything after it — so all n entries may need to be read. **Ω(n) is a lower bound** in the worst case, and O(n) meets it.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — one integer, `farthest`, regardless of input size. The array isn't modified and nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| Recursion (memoized or not) | **O(n)** | The call stack, up to n deep, plus the cache |
| Bottom-up DP array | **O(n)** | One boolean per index |
| **Greedy frontier** | **O(1)** | Reachability is an *interval*, so one number describes it entirely |

**The reason this collapses so far is structural, not clever.** In [Maximum Subarray](53-maximum-subarray.md) the state shrank to O(1) because the recurrence looked back one cell. Here it shrinks because **the set being tracked happens to be an interval** — and an interval anchored at 0 needs only its right endpoint.

That's worth stating as a general lesson: **before reaching for a DP table, ask whether the thing you're tracking has structure that compresses it.** Sets of reachable positions usually need a table; *contiguous ranges* of them need a number.

**What would break it:** if jumps had to be *exactly* `nums[i]`, reachable positions would form a scattered set rather than an interval, one number couldn't represent it, and you'd need the O(n) DP array or a BFS.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The important detail is that `nums[i]` is a *maximum* jump length, not an exact one — so from index i, every position up to `i + nums[i]` is reachable. That means the set of reachable indices is always a contiguous interval starting at 0, and I can describe it with a single number: the farthest index I can reach. I sweep left to right; at each index I first check whether it's beyond the frontier, in which case it's unreachable and so is everything after it, so I return false. Otherwise I extend the frontier to `max(farthest, i + nums[i])`. I'm not choosing a jump — I'm recording a fact — so the greedy can't cost me anything. O(n) time, O(1) space. The DP version is O(n²), which at n = 10⁴ is 10⁸ operations and unnecessary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the greedy safe?" | Because you never commit to a jump. Reachability is an interval, so the union of all reaches is just their maximum — taking the max at every index discards nothing. |
| "What if jumps had to be *exactly* `nums[i]`?" | Reachable positions would be a scattered set, not an interval, so one number couldn't represent it. You'd need an O(n) boolean DP array or BFS. |
| "Find the **minimum** number of jumps." | That's [Jump Game II](45-jump-game-ii.md) — same frontier idea, but you also track the current jump's boundary and increment a counter when you cross it. |
| "Solve it backwards." | Set `target = n - 1`; sweep right to left, and whenever `i + nums[i] >= target`, set `target = i`. Return `target == 0`. Same O(n)/O(1), different intuition. |
| "Why check reachability before extending the frontier?" | Otherwise index `i`'s own jump value would justify standing on `i`. On `[0, 1]` that ordering error returns `True` instead of `False`. |
| "Does a 0 always mean failure?" | No — only a 0 that nothing can jump *over*. `[4,2,1,0,4]` succeeds because index 0 reaches index 4 directly. A 0 at the last index is always fine. |
| "Why no final `farthest >= n-1` check?" | Completing the loop already proves it — the last index passed the `i > farthest` test, which is exactly that condition. |
| "What if you could also jump backwards?" | Then it's a graph reachability problem — BFS or union-find — and the interval property is gone. |

**Traps:**
- **Extending the frontier before checking reachability.** The ordering bug; `[0, 1]` catches it.
- **Assigning instead of maximizing** — `farthest = i + num` shrinks the frontier whenever a later index reaches less far.
- Assuming any 0 in the array means failure. Only an unjumpable one does.
- Reaching for the O(n²) DP by reflex. Correct, but it misses the interval insight and may time out.
- Treating `nums[i]` as an exact jump distance. The word "maximum" is doing the heavy lifting.
- Forgetting the single-element case. `[0]` is `true` — you're already at the last index.

**This same move shows up in:** [Jump Game II](45-jump-game-ii.md) (the same frontier, extended to count jumps by tracking level boundaries) · [Maximum Subarray](53-maximum-subarray.md) (a greedy one-pass scan whose local choice provably can't hurt) · [Gas Station](134-gas-station.md) (a single forward pass where failing early lets you discard a whole prefix) · [Merge Intervals](56-merge-intervals.md) (tracking a running interval endpoint rather than a set of positions).

</details>

---
