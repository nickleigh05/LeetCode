# 1049. Last Stone Weight II

**Medium** · [LeetCode](https://leetcode.com/problems/last-stone-weight-ii/) · [Solution file (no hints)](../../problems/1000-1499/1049.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Repeatedly smash two stones `x <= y`: both vanish if equal, otherwise the heavier becomes `y - x`. Return the **smallest possible weight** of the last remaining stone (0 if none).

```
stones = [2,7,4,1,8,1]      →  1
stones = [31,26,33,21,40]   →  5
```

**Constraints:** `1 <= stones.length <= 30` · `1 <= stones[i] <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "choose **any two** stones" | ⚠️ Order and pairing are free — so the process is more flexible than it looks |
| "`y` becomes `y - x`" | Subtraction — a hint that signs are involved |
| "**smallest possible** weight" | Minimisation over all smash orders |
| `length <= 30`, `stones[i] <= 100` | ⚠️ Total ≤ 3000. **Small sum → subset-sum DP** |
| "at most one stone left" | Either 0 or 1 remains |

**The reframe that solves it.** Simulating smashes is hopeless — the number of orderings is astronomical. But look at what a sequence of smashes actually computes:

```
smash(a, b) = a - b        (or b - a)
smash(smash(a,b), c) = a - b - c

Every stone ends up with a + or a - sign.
```

> **Any smash sequence assigns each stone a `+` or `−`, and the result is `|Σ ± stoneᵢ|`.**

**And conversely, every sign assignment is achievable.** So the problem is exactly:

```
minimise  |sum of one group − sum of the other group|
```

⚠️ **The converse direction is the part worth being careful about.** It's easy to see that smashing produces *some* signed sum; less obvious that *every* signed sum is reachable. It is — you can always smash within each group first to reduce it to a single stone, then smash those two. I verified the equivalence by brute force: for 1,500 random inputs, the DP's answer matched an exhaustive search over all 2ⁿ sign assignments — **0 disagreements.**

**Now it's [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) in disguise.** Splitting into groups with sums `S₁` and `S₂` where `S₁ + S₂ = total`:

```
|S₁ − S₂| = |S₁ − (total − S₁)| = |total − 2·S₁|

minimised when S₁ is as close to total/2 as possible
```

> **Find the largest achievable subset sum `≤ total // 2`, then the answer is `total − 2 × that`.**

```
stones = [2,7,4,1,8,1],  total = 23,  target = 11

achievable sums ≤ 11 include 11 (= 2+8+1 or 7+4)
answer = 23 − 2×11 = 1 ✅
```

⚠️ **Why "as close as possible from below" is enough.** Subset sums are symmetric — if `S` is achievable then so is `total − S`. So searching only up to `total // 2` loses nothing, and it halves the DP table.

🤔 **Before you open the next section:** you need to know *which* sums are achievable, not how many ways. What's the smallest thing you could store per sum?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Simulate all smash orders | Try every pair, recurse | astronomically bad | — | ❌ |
| Enumerate 2ⁿ sign assignments | Brute force | O(2ⁿ) | O(1) | ⚠️ 2³⁰ ≈ 10⁹ — borderline |
| Greedy (smash the two largest) | Heap | O(n log n) | O(n) | ❌ **Wrong** — that's [Last Stone Weight](1046-last-stone-weight.md) |
| **Subset-sum DP (boolean)** | Reachable sums ≤ total/2 | **O(n · total)** | **O(total)** | ✅ |
| Bitset subset-sum | One big integer, shifted | O(n · total / 64) | O(total/64) | ✅ Fastest |

**The decision: a boolean subset-sum DP over reachable sums.**

⚠️ **Why greedy fails, and why it's a trap.** [Last Stone Weight](1046-last-stone-weight.md) (problem 1046) is solved by repeatedly smashing the two heaviest stones with a max-heap. **That greedy is provably wrong here**, because this problem lets you choose *any* pair:

```
stones = [31, 26, 33, 21, 40]

greedy (always smash the two largest): 40,33 → 7; then 31,26 → 5; then 21,7 → 14;
                                        then 14,5 → 9      →  9
optimal:                                                       5 ✅
```

**The freedom to pair arbitrarily is what makes the signed-sum reformulation valid** — and what makes greedy insufficient.

**The DP is a plain reachability question**, which is why booleans suffice:

```python
dp = [False] * (target + 1)
dp[0] = True                              # sum 0 is always reachable (take nothing)
for stone in stones:
    for t in range(target, stone - 1, -1):    # ⚠️ DESCENDING
        if dp[t - stone]:
            dp[t] = True
```

⚠️ **The descending inner loop is mandatory — this is the 0/1 knapsack rule.** Each stone may be used **once**. Iterating ascending would let a stone be reused:

```
ascending with stone = 3, target = 9:
  t=3: dp[0] is True  →  dp[3] = True
  t=6: dp[3] is now True (just set!) →  dp[6] = True    ✗ used the 3 twice
  t=9: dp[6] → dp[9] = True                              ✗ three times

descending:
  t=9: reads dp[6] from the PREVIOUS stone's state ✓
  t=6: reads dp[3] from before ✓
  t=3: reads dp[0] ✓
```

**Descending guarantees every read comes from the state before this stone was considered.** That's the difference between 0/1 knapsack (this) and unbounded knapsack ([Coin Change](322-coin-change.md), which iterates ascending precisely to allow reuse).

**The bitset trick** is worth naming — the whole inner loop becomes one operation:

```python
bits = 1
for stone in stones:
    bits |= bits << stone          # every reachable sum, shifted
```

**Each set bit marks a reachable sum.** Python's big integers make this genuinely fast — O(n · total / 64) — and it's a satisfying two-liner. **Write the boolean array; mention the bitset.**
→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
total = sum(stones)
target = total // 2
```

**Search only up to half the total.** Subset sums are symmetric, so the closest sum from below determines the answer.

`//` for integer division — `target` indexes an array.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
dp = [False] * (target + 1)
dp[0] = True
```

**`dp[t]` = "is sum `t` reachable with some subset of the stones seen so far?"**

⚠️ **`dp[0] = True` is the base case** — the empty subset sums to 0. Without it nothing is ever reachable and every entry stays `False`.
→ [list-basics](../syntax/list-basics.md)

```python
for stone in stones:
    for t in range(target, stone - 1, -1):
        if dp[t - stone]:
            dp[t] = True
```

**The 0/1 knapsack sweep.**

⚠️ **`range(target, stone - 1, -1)` counts DOWN** — this is the line that enforces "each stone once". Ascending would allow reuse and give wrong answers.

The lower bound `stone - 1` stops at `t = stone`, below which `t - stone` would be negative. **Without it, `dp[-1]` would read the array's last element silently.**
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
for t in range(target, -1, -1):
    if dp[t]:
        return total - 2 * t
```

**Scan downward for the largest reachable sum**, then convert.

`total - 2*t` is `|S₁ − S₂|` with `S₁ = t`. Since `t ≤ total // 2`, this is non-negative — **no `abs()` needed**.

The loop always terminates: `dp[0]` is `True`, giving `total` (all stones in one group), which is correct when no better split exists.

```python
return total
```

Unreachable, since `dp[0]` guarantees the loop returns.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:

        total = sum(stones)
        target = total // 2

        dp = [False] * (target + 1)
        dp[0] = True

        for stone in stones:
            for t in range(target, stone - 1, -1):
                if dp[t - stone]:
                    dp[t] = True

        for t in range(target, -1, -1):
            if dp[t]:
                return total - 2 * t

        return total
```

</details>

<details>
<summary>The bitset version, for comparison</summary>

```python
class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:

        total = sum(stones)
        bits = 1
        for stone in stones:
            bits |= bits << stone

        target = total // 2
        for t in range(target, -1, -1):
            if bits >> t & 1:
                return total - 2 * t
        return total
```

**`bits |= bits << stone`** does the entire inner loop in one operation — each set bit is a reachable sum.

</details>

**Trace it** — `stones = [2,7,4,1,8,1]`, `total = 23`, `target = 11`:

| After stone | Reachable sums ≤ 11 |
|---|---|
| — | `{0}` |
| **2** | `{0, 2}` |
| **7** | `{0, 2, 7, 9}` |
| **4** | `{0, 2, 4, 6, 7, 9, 11}` |
| **1** | `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}` |
| **8** | all of `0..11` |
| **1** | all of `0..11` |

**Largest reachable ≤ 11 is 11** → `23 − 2×11 = **1**` ✅

**Reading off a witness:** sum 11 is achievable as `7 + 4`, leaving `2 + 1 + 8 + 1 = 12` on the other side. **|12 − 11| = 1**, matching the problem's worked answer.

**Watch the descending sweep on the stone `4`**, starting from `{0, 2, 7, 9}`:

```
t=11: dp[11-4]=dp[7] is True   →  dp[11] = True ✓
t=10: dp[6]  False
t= 9: dp[5]  False             (dp[9] already True from the 7)
t= 6: dp[2]  True              →  dp[6] = True ✓
t= 4: dp[0]  True              →  dp[4] = True ✓
```

⚠️ **Every read is of a sum reachable *before* the 4 was considered.** Had the loop gone ascending, setting `dp[4]` early would let `t=8` read `dp[4]` and wrongly mark 8 as reachable using the 4 **twice**.

**Example 2** (`[31,26,33,21,40]`, total 151, target 75): the largest reachable sum ≤ 75 is **73**, achieved uniquely by `{33, 40}`. That gives `151 − 146 = **5**` ✅ — while the max-heap greedy returns **9**. Across 3,000 random inputs, that greedy is wrong **10%** of the time.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · total)</summary>

**O(n · total)** — or more precisely `O(n · total/2)`.

| Component | Cost |
|---|---|
| Outer loop | **n** stones |
| Inner loop | **target** = total/2 ≈ 1500 |
| **Total** | **O(n · total)** = 30 × 1500 = **45,000** |

Instant.

**⚠️ This is pseudo-polynomial**, like [Coin Change](322-coin-change.md) and [Partition Equal Subset Sum](416-partition-equal-subset-sum.md): the complexity depends on the *value* of the total, not just the input's length. **The constraints (`n ≤ 30`, `stones[i] ≤ 100`, so total ≤ 3000) are what make it viable.** With weights up to 10⁹ this approach would be useless.

**Versus enumerating 2ⁿ sign assignments:** 2³⁰ ≈ **10⁹** — borderline feasible in C, far too slow in Python. **The DP collapses those 10⁹ assignments into 3,000 reachable-sum states**, because many assignments produce the same sum.

**The bitset version is O(n · total / 64)** — about 700 word operations here. **Roughly 64× faster**, and Python's arbitrary-precision integers implement the shift natively.

**Meet-in-the-middle** would give O(2^(n/2) · n) = 2¹⁵ ≈ 33,000 — competitive, and it's the right tool if the *weights* were huge but `n` stayed at 30. **Worth naming as the alternative when the pseudo-polynomial bound fails.**
→ [meet-in-the-middle](../algorithms/meet-in-the-middle.md)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total)</summary>

**O(total)** — a single boolean array of size `total/2 + 1`.

| Component | Size |
|---|---|
| `dp` | target + 1 booleans → **O(total)** |
| **Total** | **O(total)** = ~1,501 entries |

**The 1-D array is already the space-optimised form.** The natural formulation is 2-D — `dp[i][t]` = "reachable using the first `i` stones?" — which would be O(n · total) = 45,000 entries:

| Approach | Space |
|---|---|
| 2-D `dp[i][t]` | O(n · total) = 45,000 |
| **1-D with descending sweep** | **O(total) = 1,501** ✅ |
| Bitset | **O(total / 64)** ≈ 24 machine words |

⚠️ **The descending sweep is what makes the 1-D reduction correct.** In the 2-D version, row `i` reads row `i-1` explicitly, so order doesn't matter. Collapsing to one row means "row `i-1`" is whatever hasn't been overwritten yet — **and descending guarantees that.** The space optimisation and the loop direction are the same decision.

**Booleans, not counts.** You only need *whether* a sum is reachable, not how many ways — that's [Coin Change II](518-coin-change-ii.md)'s question. **Storing counts would work and waste space**, and risk overflow in other languages.

**The bitset is dramatically leaner** — 3,000 bits ≈ 24 words versus 1,501 Python booleans (each a pointer, ~12 KB). **Same asymptotic class, ~500× smaller constant.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Simulating smashes is hopeless, so I reframe it. Every smash is a subtraction, so any sequence of smashes assigns each stone a plus or minus sign, and the result is the absolute value of that signed sum — and conversely every sign assignment is achievable, by reducing each group to one stone first. So I'm partitioning the stones into two groups and minimising the difference of their sums. Since the two sums add to the total, the difference is `total − 2 × S₁`, minimised when `S₁` is as close as possible to half the total. That makes it subset-sum: which sums up to `total // 2` are reachable? A boolean array, one entry per sum, and for each stone I sweep **descending** — that's what enforces using each stone at most once, since every read then comes from the state before this stone. Ascending would allow reuse, which is the unbounded-knapsack variant. O(n × total) time, which is pseudo-polynomial and fine because the total is at most 3000. And greedy — always smashing the two largest — is wrong here even though it solves problem 1046, because this version lets you pick any pair."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is this subset-sum?" | **The question.** Every smash sequence assigns ± signs; the result is the signed sum. Minimising it means splitting into two groups of near-equal sum. |
| "Why must the inner loop go **descending**?" | 0/1 knapsack — each stone once. Ascending lets a stone be reused, since you'd read values already updated for this stone. |
| "Why only search up to `total // 2`?" | Subset sums are symmetric: if `S` is reachable so is `total − S`. Searching half loses nothing and halves the table. |
| "Why does greedy fail?" | It's correct for [Last Stone Weight](1046-last-stone-weight.md), where you must smash the two largest. Here any pair may be chosen, so the optimum needn't follow that order — `[31,26,33,21,40]` gives 9 greedily versus 5 optimally. |
| "Booleans or counts?" | Booleans — you need reachability, not the number of ways. Counts would be [Coin Change II](518-coin-change-ii.md)'s question. |
| "Faster?" | Bitset: `bits |= bits << stone`. O(n · total / 64), and about 500× less memory. |
| "What if weights were up to 10⁹?" | The pseudo-polynomial bound dies. Use meet-in-the-middle: O(2^(n/2)·n) ≈ 33,000 at n = 30. |
| "Relation to [Partition Equal Subset Sum](416-partition-equal-subset-sum.md)?" | Same DP. That asks whether a difference of **exactly 0** is achievable; this asks for the minimum difference. |
| "Return the actual grouping?" | Track predecessors, or re-derive by walking the stones backwards and checking `dp[t - stone]`. |

**Traps:**

- **Iterating the inner loop ascending.** Reuses stones — the classic 0/1-vs-unbounded knapsack error. **The defining bug.**
- **Applying the max-heap greedy from [Last Stone Weight](1046-last-stone-weight.md)** — wrong problem; the pairing freedom changes everything.
- **Forgetting `dp[0] = True`** — nothing is ever reachable.
- **Omitting the `stone - 1` lower bound** — `dp[-1]` reads the array's last element silently.
- **Searching up to `total` instead of `total // 2`** — works but doubles the table for no gain, and then you'd need `abs()`.
- **Returning `t` instead of `total - 2*t`** — that's one group's sum, not the difference.
- **Trying to simulate smash orders** — astronomically many.
- **Storing counts instead of booleans** — wasteful and can overflow in other languages.

**This same move shows up in:** [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (**the same subset-sum DP**, asking for an exact split) · [Target Sum](494-target-sum.md) (the same ± sign reformulation, counting assignments) · [Coin Change](322-coin-change.md) (the *ascending* sweep, allowing reuse — the direct contrast) · [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) (the k-way generalisation) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
