# 213. House Robber II

**Medium** · [LeetCode](https://leetcode.com/problems/house-robber-ii/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Same as [House Robber](198-house-robber.md), except the houses are arranged in a **circle** — the first house is the neighbour of the last one. Adjacent houses still can't both be robbed. Return the maximum amount you can rob without alerting the police.

```
nums = [2,3,2]      →  3      you cannot rob houses 0 and 2 — they're adjacent in a circle
nums = [1,2,3,1]    →  4      rob houses 0 and 2 → 1 + 3
nums = [1,2,3]      →  3
```

**Constraints:** `1 <= nums.length <= 100` · `0 <= nums[i] <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "same as House Robber, but…" | **Do not start from scratch.** The interviewer is testing whether you can adapt a known solution, not whether you can rederive it |
| houses in a **circle** | Exactly **one** new constraint gets added: house `0` and house `n-1` are now adjacent |
| everything else unchanged | The interior of the array behaves identically. Whatever you do, it must reduce to the linear problem |
| `nums = [2,3,2] → 3` | The example exists purely to catch you. Linearly the answer would be 4 (houses 0 and 2); the circle forbids it |
| `n <= 100`, `n >= 1` | Note `n == 1`: a single house is adjacent to *itself* under a naive wraparound reading. That'll need a guard |

The temptation is to write a new DP with extra state — "did I rob house 0?" carried through the whole pass. That works, but it's more machinery than the problem needs.

The better move is to **turn the new constraint into a case split.** The circle adds precisely one rule: *houses 0 and n-1 cannot both be robbed.* So consider the possibilities for house 0:

- **House 0 is not robbed** → the wraparound can't fire, so houses `1 .. n-1` are just a plain line.
- **House 0 is robbed** → then house `n-1` definitely isn't, so houses `0 .. n-2` are just a plain line.

Either way you're left with a **linear** House Robber problem. Solve both and take the better one.

There's a subtle point that makes this airtight, and it's the thing to be ready to defend. Case 1 says "0 is not robbed," but solving `nums[1:]` doesn't *force* anything about house 0 — it merely makes it unavailable. Likewise `nums[:-1]` doesn't force you to rob house 0, only permits it. So the two cases **overlap**: a solution robbing neither endpoint appears in both. That's harmless. Overlap can't produce a wrong answer for a `max` — it would only be a problem if you were *counting*. What matters is that every legal solution appears in **at least one** case, and every candidate considered is **legal**. Both hold.

🤔 **Before you open the next section:** if you just ran the linear solution on the whole array and then subtracted something when both endpoints were used — why would that be hard to get right? What's cleaner about splitting the problem before you start?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Run linear DP on the whole array | Ignore the wraparound | O(n) | O(1) | ❌ Returns 4 on `[2,3,2]`. It's the answer to the wrong problem |
| Linear DP, then patch the result | Detect that both endpoints were used and fix it up | — | — | ❌ There's no clean fix. Dropping an endpoint may cascade into a completely different optimal subset, not a local adjustment |
| DP with extra state | Carry a "robbed house 0?" flag through the pass, forbidding house n-1 when set | O(n) | O(1) | ⚠️ Correct, and a legitimate answer — but it's two interleaved DPs in one loop, easy to get wrong under pressure |
| **Two linear runs** | Solve `nums[:-1]` and `nums[1:]` with the [198](198-house-robber.md) DP, take the max | O(n) | O(n) for slices, O(1) with indices | ✅ |

**The decision:** run the **unchanged** [House Robber](198-house-robber.md) solution twice, on two overlapping subarrays, and take the max.

**Why the "patch it afterwards" idea is a trap.** It feels like the wraparound should be a small correction to the linear answer, but it isn't. If the linear optimum happens to use both endpoints, the fix isn't "drop the smaller one" — removing a house frees up its neighbours, which can make an entirely different subset optimal. On `[5,1,1,5]`, dropping either 5 changes which interior houses are worth taking. **You can't repair a DP result locally**, because the whole point of the DP was that decisions interact non-locally. Split *before* solving, not after.

**Why the case split is the right instinct in general.** When a problem adds a constraint that couples exactly two positions, enumerating the possibilities for one of them turns the hard problem into a small number of easy ones. Here two cases suffice, each costing O(n), so the total is still O(n). That pattern — *"a constrained problem = a few unconstrained subproblems"* — recurs throughout DP.

**Why reuse the function verbatim rather than adapt it?** Because the interior logic genuinely hasn't changed, and demonstrating that you *recognized* the reduction is worth more than writing clever new code. In an interview: name 198, say the circle splits into two linear cases, then write the helper once.

**The remaining wrinkle** is `n == 1`. Both `nums[:-1]` and `nums[1:]` are empty for a single house, so both runs return 0 and you'd answer 0 instead of `nums[0]`. That needs an explicit guard — which is why it's the first line of the solution.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(nums) == 1:
    return nums[0]
```
**The edge case, handled first.** With one house, both slices below are empty, both runs return 0, and you'd lose the only house on the street.

It's worth pausing on *why* this is the only special case needed. With `n == 2`, `nums[:-1]` is `[nums[0]]` and `nums[1:]` is `[nums[1]]`, so the max is `max(nums[0], nums[1])` — correct, since the two houses are adjacent both ways round and only one can be robbed. The split handles `n >= 2` on its own.
→ [if-return](../syntax/if-return.md) · [list-basics](../syntax/list-basics.md)

```python
def rob_linear(houses):
    prev, curr = 0, 0
    for num in houses:
        prev, curr = curr, max(curr, prev + num)
    return curr
```
**[House Robber](198-house-robber.md), copied without a single change.** `curr` is the best through the previous house, `prev` the best through the one before that; at each house you take the better of *skip* (`curr`) and *rob* (`prev + num`).

The [tuple assignment](../syntax/swap-tuple-assign.md) evaluates its entire right-hand side before assigning, so `curr` reads as the old value in both slots and the window slides in one step.

Defining it as a **nested function** rather than inlining it twice is the honest expression of the idea: *the same subproblem, solved on two different inputs.*
→ [function-basics](../syntax/function-basics.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [min-max-key](../syntax/min-max-key.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```
**The case split, in one line.**

- `nums[:-1]` — every house **except the last**. This is the "house 0 is available" world; the wraparound can't fire because house `n-1` isn't there.
- `nums[1:]` — every house **except the first**. This is the "house n-1 is available" world.

Every legal circular arrangement lives in at least one of these, and neither can produce an illegal one, so the larger of the two results is the answer.
→ [list-slicing](../syntax/list-slicing.md) · [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:

        if len(nums) == 1:
            return nums[0]

        def rob_linear(houses):
            prev, curr = 0, 0
            for num in houses:
                prev, curr = curr, max(curr, prev + num)
            return curr

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```
</details>

**Trace it** — `nums = [2, 3, 2]`

**Run A** — `nums[:-1]` = `[2, 3]`:

| `num` | rob (`prev + num`) | skip (`curr`) | new `curr` | new `prev` |
|---|---|---|---|---|
| 2 | 0 + 2 = **2** | 0 | **2** | 0 |
| 3 | 0 + 3 = **3** | 2 | **3** | 2 |

→ **3**

**Run B** — `nums[1:]` = `[3, 2]`:

| `num` | rob | skip | new `curr` | new `prev` |
|---|---|---|---|---|
| 3 | 0 + 3 = **3** | 0 | **3** | 0 |
| 2 | 0 + 2 = 2 | **3** | **3** | 3 |

→ **3**

`max(3, 3)` = **3** ✅

The plain linear DP on the full `[2,3,2]` would return **4** by robbing houses 0 and 2 — which the circle forbids. Neither run can reach that answer, because neither ever sees both endpoints at once. That's the split doing its job.

**And `nums = [1,2,3,1]`:** run A on `[1,2,3]` gives 4 (houses 0 and 2); run B on `[2,3,1]` gives 3. `max(4, 3)` = **4** ✅ — and here the winner *does* use house 0, which is exactly the case run A exists to cover.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The `n == 1` check is O(1).
- `nums[:-1]` and `nums[1:]` each copy up to n−1 elements → **O(n)** each.
- Each `rob_linear` call is a single pass over its input, doing O(1) work per house → **O(n)** each.
- Total: 2 × O(n) + 2 × O(n) = **O(n)**.

The constant factor is roughly 4 passes over the data — two for slicing, two for the DP. Constant factors don't change the class, and saying "two linear passes, so still O(n)" is the right level of detail.

**The thing worth stating explicitly:** solving *two* subproblems doesn't make this worse than [198](198-house-robber.md). A fixed number of O(n) passes is still O(n). That's what makes the case-split approach cheap enough to prefer over a cleverer single-pass version.

**Can it be faster?** No — every house's value can change the answer, so Ω(n) is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) as written, O(1) achievable</summary>

**O(n) as written**, because of the slices — `nums[:-1]` and `nums[1:]` each allocate a new list of up to n−1 elements. The DP itself is O(1) (two integers per call, and the calls don't overlap).

**The O(1) version** avoids the copies by passing index ranges instead:

```python
def rob_range(lo, hi):          # inclusive lo, exclusive hi
    prev = curr = 0
    for i in range(lo, hi):
        prev, curr = curr, max(curr, prev + nums[i])
    return curr

return max(rob_range(0, len(nums) - 1), rob_range(1, len(nums)))
```

Same logic, same complexity in time, but **O(1)** space.

Which to write? The slicing version is shorter and reads better, and at `n <= 100` the copies are free. Write it, then say *"the slices cost O(n); I could pass index bounds instead for O(1) if space mattered."* Naming the trade-off unprompted is the part that counts — reaching for index arithmetic first is optimizing something nobody asked about.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The circle adds exactly one constraint: houses 0 and n−1 can't both be robbed. So I'll split on house 0. If I don't rob it, the remaining houses 1 through n−1 form a plain line. If I do rob it, house n−1 is out, and houses 0 through n−2 form a plain line. Either way it's the linear House Robber problem, so I run that unchanged on both subarrays and take the max. The two cases overlap — a solution using neither endpoint appears in both — but that's fine for a max; what matters is that every legal solution appears in at least one, and no illegal one appears in either. The only edge case is a single house, where both slices are empty. Two linear passes, so O(n) time; the slices make it O(n) space, or O(1) if I pass index bounds instead."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not run the linear DP once and fix up the result?" | Because removing an endpoint frees its neighbours, which can change the entire optimal subset — it's not a local correction. `[5,1,1,5]` shows the fix isn't just "drop the smaller endpoint." |
| "Isn't double-counting the overlap a problem?" | Not for a `max`. Overlap only matters when counting. Both cases contain only legal solutions, and their union covers all of them, so the max is correct. |
| "Can you do it in one pass?" | Yes — carry two parallel DP states through a single loop, one that permits house 0 and one that forbids it. Same O(n), but two interleaved recurrences are much easier to botch. |
| "Why does `n == 2` not need a special case?" | Each slice becomes a single house, so the max is `max(nums[0], nums[1])` — correct, since in a 2-circle the houses are adjacent and only one is robbable. |
| "Make it O(1) space." | Pass `(lo, hi)` index bounds instead of slicing, and index `nums` directly inside the loop. |
| "What if it were a circle *and* you couldn't rob within k?" | Same idea, more cases: enumerate which of the first k houses (if any) is robbed, and solve a linear problem for each. Cases grow with k, but the reduction is identical. |
| "Which houses were robbed?" | Run both cases keeping their `dp` arrays, see which won, and reconstruct by walking that one backwards. O(n) space. |

**Traps:**
- **Forgetting `n == 1`.** Both slices are empty, both runs return 0, and you answer 0 for a street with money on it. The single most-failed case.
- Running the linear DP on the whole array and forgetting the wraparound entirely — `[2,3,2]` catches it immediately.
- Slicing as `nums[:-1]` and `nums[:1]` — a one-character typo that silently solves the wrong second case.
- Trying to repair the linear answer instead of splitting up front.
- Worrying about the overlap and adding logic to exclude it. It's harmless, and the extra logic is where bugs come from.
- Adding a special case for `n == 2` that returns `nums[0]` — wrong, and unnecessary.

**This same move shows up in:** [House Robber](198-house-robber.md) (the linear problem this reduces to, twice) · [Climbing Stairs](70-climbing-stairs.md) (the same two-cell recurrence, counting instead of maximizing) · [Best Time to Buy and Sell Stock with Cooldown](309-best-time-to-buy-and-sell-stock-with-cooldown.md) (carrying multiple parallel DP states, which is the one-pass alternative here) · [Palindrome Partitioning](131-palindrome-partitioning.md) (splitting a problem into independent subproblems at a chosen boundary).

</details>

---
