# 1899. Merge Triplets to Form Target Triplet

**Medium** · [LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given a list of `triplets` and a `target` triplet. You may repeatedly pick two triplets and **merge** them, replacing both with the **element-wise maximum**:

```
[a, b, c] merged with [d, e, f]  →  [max(a,d), max(b,e), max(c,f)]
```

Return `true` if it's possible to obtain `target` as one of the triplets after any number of merges.

```
triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]   →  true
        merge [2,5,3] and [1,7,5] → [2,7,5] ✓

triplets = [[3,4,5],[4,5,6]], target = [3,2,5]           →  false
        no merge can lower a value; 4 and 5 both exceed target's 2

triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]  →  true
```

**Constraints:** `1 <= triplets.length <= 10⁵` · `1 <= triplets[i][j], target[j] <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| merging takes the **element-wise max** | The operation is **monotone** — values only ever go **up**, never down. That single property drives everything |
| "any number of merges" | You're effectively choosing a **subset** of triplets and taking the element-wise max over all of them. Order doesn't matter, and merging is associative |
| "obtain `target`" — exactly | Every position must land **exactly** on the target. Not ≥, not close — exact |
| positions are independent | `max` applies per position with no interaction, so the three coordinates can be reasoned about **separately** |
| `n <= 10⁵` | O(n) or O(n log n). But subsets are 2ⁿ, so you can't enumerate them |

Two facts, and together they solve the problem.

**Fact one — merging can never decrease a value.** Since every merge takes a maximum, once a position holds some value it can only grow. So if a triplet has **any** component strictly greater than the target's, including it is fatal: that position overshoots and can never come back down.

> **Any triplet with `t[i] > target[i]` for some `i` is permanently unusable.** Discard it outright.

That's not a heuristic — it's a hard constraint. There's no scenario where such a triplet helps, because it damages a position irreparably.

**Fact two — among the survivors, merging is free.** Every remaining triplet has `t[i] <= target[i]` in all three positions. Merging any collection of them yields a result that is **still ≤ target everywhere**, so it can never overshoot. There's no downside to including a safe triplet.

**So merge them all.** The best achievable result is the element-wise max over *every* safe triplet, and the question becomes:

> Does that max equal `target`?

Which reduces further, since each position is independent:

> For each position `i`, is there **some** safe triplet with `t[i] == target[i]` exactly?

If yes for all three, merging those (up to three) triplets produces the target.

🤔 **Before you open the next section:** the answer never needs to find *which* subset to merge. Why does "merge every safe triplet" lose nothing — and why can the three positions be checked completely independently of one another?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every subset | Enumerate all 2ⁿ, merge each, compare | **O(2ⁿ · n)** | O(n) | ❌ 2^(10⁵) |
| Simulate merges pairwise | Repeatedly merge pairs and search | unbounded | — | ❌ No sensible strategy, and the search space explodes |
| **Filter unsafe, then check coverage** | Discard overshooting triplets; verify each position is hit exactly | **O(n)** | **O(1)** | ✅ |

**The decision:** **one pass — discard the unsafe, record which positions the survivors hit exactly.**

**Why "merge everything safe" is optimal** — the answer to section 1's first question. Merging a safe triplet can only raise values, and since a safe triplet is ≤ target in every position, the merged result stays ≤ target in every position. **So including it can never hurt, and it might help.** With no downside, the optimal strategy is to include all of them — which means the best reachable triplet is exactly the element-wise max over all safe triplets, and there's no subset selection to perform.

That's an unusually clean greedy: not "pick carefully" but **"take everything that isn't forbidden."** The difficulty was entirely in identifying what's forbidden.

**Why the positions are independent** — the second question. `max` operates coordinate-wise with no cross-talk: position 0's value never influences position 1's. So "the element-wise max over safe triplets equals target" decomposes into three separate questions, each answerable by scanning for a single exact hit. **A 3-dimensional problem becomes three 1-dimensional ones**, which is why the state is a set of at most three indices rather than anything larger.

**Why exact equality and not ≥.** Every safe triplet is ≤ target at position `i`, so the max over them is also ≤ target there. To reach target exactly, at least one triplet must *achieve* it. If none does, the max falls strictly short and no merging can close the gap. **Being ≤ everywhere isn't enough — you need a witness at each position.**

**Why this isn't DP or search.** There's no sequential decision-making, no overlapping subproblems, nothing to optimize over. The monotonicity of `max` collapses the entire combinatorial structure into a filter plus three membership checks. **Recognizing that a problem's operation is monotone is often what dissolves it** — the same reason [Jump Game](55-jump-game.md)'s reachability collapsed to a single number.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
good = set()
```
Which **positions** (0, 1, 2) have been matched exactly by some safe triplet. It holds indices, not triplets — at most three elements ever.

A [set](../data-structures/hashset.md) because you only care *whether* a position has been covered, not how many times or by which triplet.
→ [set-basics](../syntax/set-basics.md) · [hashset](../data-structures/hashset.md)

```python
for triplet in triplets:
```
A single pass. No sorting, no preprocessing — each triplet is judged in isolation, because whether it's usable depends only on itself and the target.
→ [for-loop](../syntax/for-loop.md)

```python
    if triplet[0] > target[0] or triplet[1] > target[1] or triplet[2] > target[2]:
        continue
```
**The filter, and it's the heart of the problem.** If *any* component exceeds the target's, this triplet is poison: merging it would push that position above the target permanently, since `max` never decreases.

Note it's `or`, not `and` — a **single** overshooting component disqualifies the whole triplet. And `>`, not `>=` — a component *equal* to the target is exactly what you want.

[`continue`](../syntax/break-continue.md) discards it entirely; it contributes nothing to `good`.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md) · [break-continue](../syntax/break-continue.md)

```python
    for i in range(3):
        if triplet[i] == target[i]:
            good.add(i)
```
**Record the exact hits.** Reaching here means the triplet is safe in all three positions. For each position where it matches the target *exactly*, mark that position as covered.

A safe triplet can cover zero, one, two, or all three positions — all are useful (or harmless). And covering the same position again is a no-op, which is precisely what a set gives you for free.

The check is `==`, not `>=`: since safe triplets are already ≤ target everywhere, `>=` would be equivalent, but `==` states the intent — **you need a witness that reaches the target exactly.**
→ [range-function](../syntax/range-function.md) · [set-operations](../syntax/set-operations.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return len(good) == 3
```
All three positions have a witness among the safe triplets, so merging those witnesses produces exactly the target.

The merge is never actually performed — you've proven it would work, which is all a feasibility question requires.
→ [if-return](../syntax/if-return.md) · [set-basics](../syntax/set-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:

        good = set()

        for triplet in triplets:
            if triplet[0] > target[0] or triplet[1] > target[1] or triplet[2] > target[2]:
                continue

            for i in range(3):
                if triplet[i] == target[i]:
                    good.add(i)

        return len(good) == 3
```
</details>

**Trace it** — `triplets = [[2,5,3],[1,8,4],[1,7,5]]`, `target = [2,7,5]`

| triplet | safe? | exact matches | `good` after |
|---|---|---|---|
| `[2,5,3]` | 2≤2 ✓, 5≤7 ✓, 3≤5 ✓ — **safe** | position 0: `2 == 2` ✓ | `{0}` |
| `[1,8,4]` | 1≤2 ✓, **8 > 7** ✗ — **discarded** | — | `{0}` |
| `[1,7,5]` | 1≤2 ✓, 7≤7 ✓, 5≤5 ✓ — **safe** | position 1: `7 == 7` ✓<br>position 2: `5 == 5` ✓ | `{0, 1, 2}` |

`len(good) == 3` → **true** ✅

Merging the two survivors confirms it: `max([2,5,3], [1,7,5])` = `[2, 7, 5]` = target ✓

Row 2 is the whole lesson. `[1,8,4]` looks helpful — its third component 4 is fine, and its first is fine — but the 8 in position 1 exceeds the target's 7. Merging it would lock position 1 at 8 forever. **One bad component poisons the entire triplet**, no matter how useful its other values are.

**And a failure** — `triplets = [[3,4,5],[4,5,6]]`, `target = [3,2,5]`:

| triplet | safe? | `good` after |
|---|---|---|
| `[3,4,5]` | 3≤3 ✓, **4 > 2** ✗ — **discarded** | `{}` |
| `[4,5,6]` | **4 > 3** ✗ — **discarded** | `{}` |

`len(good) == 0` → **false** ✅ — every triplet overshoots somewhere, so nothing is usable at all.

**And a case needing three separate witnesses** — `triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]]`, `target = [5,5,5]`:

| triplet | safe? | exact matches | `good` after |
|---|---|---|---|
| `[2,5,3]` | all ≤ 5 ✓ | position 1: `5 == 5` | `{1}` |
| `[2,3,4]` | all ≤ 5 ✓ | none | `{1}` |
| `[1,2,5]` | all ≤ 5 ✓ | position 2: `5 == 5` | `{1, 2}` |
| `[5,2,3]` | all ≤ 5 ✓ | position 0: `5 == 5` | `{0, 1, 2}` |

**true** ✅ — three *different* triplets supply the three positions, and merging all four (or just those three) gives `[5,5,5]`. Row 2 contributes nothing but costs nothing — which is exactly why "merge everything safe" is the right strategy.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n = `len(triplets)`.

- One pass over the triplets → **n iterations**.
- Each iteration does at most **3 comparisons** for the safety filter and **3 more** for the exact-match check, plus up to 3 set insertions — all **O(1)**, since the triplet size is fixed at 3.
- **O(n)** total.

At n = 10⁵ that's a few hundred thousand comparisons. Instant.

**Against the alternative:** enumerating subsets is **O(2ⁿ · n)** — completely impossible at this size. The collapse to O(n) comes entirely from the monotonicity argument: because merging never decreases a value, there's no subset *selection* problem at all. **Take everything safe, and check coverage.**

That's worth naming as the general lesson: **when an operation is monotone, "which subset?" often degenerates into "which elements are legal?"** — and the combinatorics vanish.

**Faster?** No. Any single triplet could be the sole witness for a position, so all n must be examined. **Ω(n)** is a lower bound.

**Best case:** no early exit exists in this implementation — the loop always runs fully. You *could* return early once `len(good) == 3`, which helps in practice but doesn't change the worst case.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — genuinely constant.

The `good` set holds **at most 3 elements** (the position indices 0, 1, 2), no matter how many triplets there are. No other allocation happens: the loop reads triplets in place, and the comparisons use no scratch space.

| Approach | Space | Why |
|---|---|---|
| Enumerate subsets | **O(n)** | Recursion or explicit subset storage — plus O(2ⁿ) time |
| Materialize the merged max | **O(1)** | Three running maxima over safe triplets — an equally valid formulation |
| **Coverage set** | **O(1)** | Bounded by the triplet size, which is fixed at 3 |

**The alternative formulation** is worth knowing because some find it more intuitive: instead of tracking which positions are covered, keep three running maxima over the safe triplets and compare the result to the target at the end.

```python
best = [0, 0, 0]
for t in triplets:
    if all(t[i] <= target[i] for i in range(3)):
        best = [max(best[i], t[i]) for i in range(3)]
return best == target
```

Same O(n)/O(1), and it makes the "merge everything safe" reasoning explicit rather than implicit. The `good`-set version is a slight refinement of the same idea — since safe triplets are ≤ target everywhere, the running max equals the target at position `i` exactly when *some* safe triplet hit it exactly, which is what the set records.

**Can it be less than O(1)?** No — but note the input itself is O(n) and can't be avoided. The point is that the *working* memory doesn't grow at all.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The operation is element-wise max, which means values only ever go up. So any triplet with a component strictly greater than the target's is permanently unusable — including it would push that position above the target with no way back down. Discard those outright. Among the survivors, every component is ≤ target, so merging any of them can never overshoot — which means there's no downside to including all of them. So the best reachable triplet is the element-wise max over every safe triplet, and since max works coordinate-wise with no interaction, I can check each position independently: does some safe triplet hit the target exactly there? If all three positions have a witness, merging those witnesses gives the target. One pass, O(n) time and O(1) space — the whole combinatorial subset problem dissolves because the operation is monotone."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why discard a triplet for one bad component?" | Because merging takes maxima, so that position would be locked above the target forever. One bad component poisons the whole triplet, regardless of how good the others are. |
| "Why merge *all* safe triplets rather than choosing?" | A safe triplet is ≤ target everywhere, so merging it can't overshoot. No downside means include everything — the subset-selection problem disappears. |
| "Why check for exact equality?" | Safe triplets are ≤ target at every position, so the max over them is too. To land *on* the target you need at least one triplet that achieves it; otherwise the max falls short. |
| "Why can the positions be checked independently?" | `max` operates coordinate-wise with no cross-talk between positions, so a 3-D condition decomposes into three 1-D ones. |
| "What if triplets had `k` components?" | Identical algorithm — the filter and the coverage check both loop to `k`. O(n·k) time, O(k) space. |
| "What if merging took the *minimum* instead?" | Symmetric: discard anything *below* the target in any position, then check each position has an exact hit from above. |
| "Could you return early?" | Yes — bail out as soon as `len(good) == 3`. Helps in practice, same worst case. |
| "Is there a subset-selection problem hiding here?" | No, and that's the point. Monotonicity means "which subset" reduces to "which elements are legal," and you take all of them. |

**Traps:**
- **Using `and` instead of `or` in the filter.** That would only discard triplets exceeding the target in *all three* positions — far too permissive, and it lets poison through.
- **Using `>=` instead of `>` in the filter.** Would discard triplets that hit the target exactly, which are precisely the witnesses you need.
- **Checking coverage before filtering**, or forgetting to filter at all — an overshooting triplet might match one position exactly while ruining another.
- Trying to choose *which* safe triplets to merge. There's nothing to choose; take them all.
- Storing triplets in `good` rather than position indices — works, but wastes O(n) space for a bounded question.
- Concluding `true` merely because every position is ≤ target somewhere. You need an exact hit at each position, not just non-exceedance.

**This same move shows up in:** [Hand of Straights](846-hand-of-straights.md) (a greedy whose validity comes from certain moves being *forced* or *forbidden*, not merely preferable) · [Jump Game](55-jump-game.md) (monotone structure collapsing a search into a single scan) · [Valid Parenthesis String](678-valid-parenthesis-string.md) (reasoning about what's *reachable* rather than simulating every choice) · [Partition Labels](763-partition-labels.md) (a one-pass scan where a precomputed fact per element decides everything).

</details>

---
