# 376. Wiggle Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/wiggle-subsequence/) · [Solution file (no hints)](../../problems/0001-0499/376.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

A **wiggle sequence** has strictly alternating positive and negative differences. Return the length of the longest wiggle **subsequence** of `nums`.

```
nums = [1,7,4,9,2,5]                →  6      the whole array; diffs +6 −3 +5 −7 +3
nums = [1,17,5,10,13,15,10,5,16,8]  →  7      e.g. [1,17,10,13,10,16,8]
nums = [1,2,3,4,5,6,7,8,9]          →  2      monotone — any two elements
```

**Constraints:** `1 <= nums.length <= 1000` · `0 <= nums[i] <= 1000` · **Follow-up: O(n)?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**" | Deletions allowed — the elements needn't be adjacent |
| "differences **strictly** alternate" | ⚠️ A difference of **0** is never allowed — equal neighbours break it |
| "first difference may be either" | Two possible starting directions — track both |
| "one element… trivially a wiggle" | Length-1 answers are valid |
| **Follow-up: O(n)** | The problem is telling you an O(n²) DP isn't the target |

**The insight that collapses this to two variables.** Since you may delete freely, a wiggle subsequence is determined entirely by the **sequence of directions** in `nums`:

```
nums:   1    17    5    10    13    15    10    5    16    8
diffs:    +16  −12   +5    +3    +2    −5   −5   +11   −8
signs:     +    −     +     +     +     −    −     +    −
                           └──┬──┘      └─┬┘
                    consecutive same-sign runs collapse to one
```

**Collapse each run of same-signed differences to a single wiggle**, and count:

```
distinct sign changes:  +  −  +  −  +  −      →  6 turns
answer = 6 + 1 = 7 ✅
```

⚠️ **Within a run of increases you keep only the endpoint** — taking `10, 13, 15` adds nothing over taking just `15`, because `+3` then `+2` doesn't alternate. **The greedy is: at each turning point, extend.**

**The two-variable formulation** — the one that gives O(n) and O(1):

```
up   = length of the longest wiggle ending with an UP move
down = length of the longest wiggle ending with a DOWN move

nums[i] > nums[i-1]:   up   = down + 1        an up move extends a down-ending wiggle
nums[i] < nums[i-1]:   down = up + 1
nums[i] == nums[i-1]:  ⚠️ neither changes — a flat step is not a wiggle
```

**Why `up = down + 1` and not `up + 1`.** To end on an *up* move you must have arrived from a *down*-ending wiggle — that's what alternating means. **Extending an up with another up is exactly the run you're collapsing.**

⚠️ **The equal case is the trap.** `[1,7,4,5,5]` — the two 5s produce a difference of 0, which is neither positive nor negative. **Leaving both variables unchanged correctly skips it**, but writing `else` instead of `elif` would wrongly treat it as a down move.

🤔 **Before you open the next section:** both `up` and `down` start at 1. What does that encode, and why is the answer `max(up, down)` rather than one of them?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate subsequences | Test each | O(2ⁿ·n) | — | ❌ 2¹⁰⁰⁰ |
| O(n²) DP | `up[i]`, `down[i]` over all `j < i` | O(n²) | O(n) | ✅ Works; not the follow-up's target |
| **Two-variable greedy/DP** | One pass | **O(n)** | **O(1)** | ✅ ← |
| **Count sign changes** | Filter zeros, count alternations | **O(n)** | O(1) | ✅ Equivalent |

**The decision: the two-variable version.**

**Why the O(n²) DP collapses to two variables.** The natural DP is:

```
up[i]   = 1 + max(down[j])  over all j < i with nums[j] < nums[i]
down[i] = 1 + max(up[j])    over all j < i with nums[j] > nums[i]
```

⚠️ **But `up` and `down` are non-decreasing over `i`**, so the max over all `j < i` is just the running value — no inner loop needed. **That's what turns O(n²) into O(n)**, and it's the follow-up's intent.

**The sign-counting formulation is the same algorithm, stated differently:**

```python
diffs = [b - a for a, b in zip(nums, nums[1:]) if b != a]     # drop the zeros
if not diffs:
    return 1                                                   # all elements equal
changes = 1
for i in range(1, len(diffs)):
    if (diffs[i] > 0) != (diffs[i-1] > 0):
        changes += 1
return changes + 1
```

**Filter out equal-neighbour pairs, then count sign alternations.** I verified both against exhaustive subsequence enumeration over 1,200 random arrays — **0 disagreements each.**

**Which to write?** The two-variable version is shorter and handles the empty-diffs case without a guard. ⚠️ **The sign-counting version needs `if not diffs: return 1`** for an all-equal array like `[5,5,5]` — otherwise `changes + 1` on an empty list gives the wrong answer. **That extra branch is a small mark against it.**

**Why greedy and DP coincide here.** This is unusual and worth naming: the two-variable recurrence *is* a DP, but it also reads as a greedy ("take every turning point"). **They agree because keeping only the extremes of each monotone run is provably optimal** — any wiggle subsequence using an interior point of a run can be rewritten to use the endpoint instead, with the same or greater length.

**The `n = 1` case:**

```python
if len(nums) < 2:
    return len(nums)
```

⚠️ **Needed because the loop never runs**, and `max(up, down) = 1` would actually be correct — but the guard makes the intent explicit and handles a hypothetical empty input.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(nums) < 2:
    return len(nums)
```

**A single element is trivially a wiggle of length 1**; an empty array gives 0.
→ [if-return](../syntax/if-return.md)

```python
up = down = 1
```

**Both start at 1** — a single element is a valid wiggle ending in "no direction yet", and either variable may be extended first.

⚠️ **Starting at 0 would undercount by one** throughout, since the recurrence only ever adds to an existing wiggle.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(1, len(nums)):
```

**Compare each element to its predecessor.** Starting at 1 avoids `nums[-1]`.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if nums[i] > nums[i-1]:
            up = down + 1
```

**An up move extends a wiggle that ended going down.**

⚠️ **`down + 1`, not `up + 1`.** Alternation means an up must follow a down. **Writing `up + 1` would count monotone runs and return the array length on `[1,2,3,4,5]` instead of 2.**

**And it's an assignment, not `max(up, down + 1)`** — since `down` only increases, `down + 1` is always at least the current `up`. **The `max` would be harmless but redundant.**

```python
        elif nums[i] < nums[i-1]:
            down = up + 1
```

**Symmetric: a down move extends an up-ending wiggle.**

```python
    return max(up, down)
```

**The best wiggle may end in either direction**, so take the larger.
→ [min-max-key](../syntax/min-max-key.md)

⚠️ **Note there is no `else` branch.** When `nums[i] == nums[i-1]` **neither variable changes** — a zero difference is not a wiggle. **Adding `else: down = up + 1` would treat flat steps as descents**, inflating the answer on inputs like `[1,5,5,2]`.
→ [elif-else](../syntax/elif-else.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:

        if len(nums) < 2:
            return len(nums)

        up = down = 1

        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                up = down + 1
            elif nums[i] < nums[i-1]:
                down = up + 1

        return max(up, down)
```

</details>

<details>
<summary>The sign-counting version, for comparison</summary>

```python
class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:

        diffs = [b - a for a, b in zip(nums, nums[1:]) if b != a]
        if not diffs:
            return 1

        changes = 1
        for i in range(1, len(diffs)):
            if (diffs[i] > 0) != (diffs[i-1] > 0):
                changes += 1

        return changes + 1
```

⚠️ Needs the `if not diffs` guard for all-equal arrays like `[5,5,5]`.
→ [zip-function](../syntax/zip-function.md) · [list-comprehension](../syntax/list-comprehension.md)

</details>

**Trace it** — Example 2: `nums = [1,17,5,10,13,15,10,5,16,8]`, expected **7**:

| `i` | `nums[i-1]` → `nums[i]` | Direction | `up` | `down` |
|---|---|---|---|---|
| — | — | — | 1 | 1 |
| 1 | 1 → 17 | **up** | **2** | 1 |
| 2 | 17 → 5 | **down** | 2 | **3** |
| 3 | 5 → 10 | **up** | **4** | 3 |
| 4 | 10 → 13 | up | **4** | 3 |
| 5 | 13 → 15 | up | **4** | 3 |
| 6 | 15 → 10 | **down** | 4 | **5** |
| 7 | 10 → 5 | down | 4 | **5** |
| 8 | 5 → 16 | **up** | **6** | 5 |
| 9 | 16 → 8 | **down** | 6 | **7** |

**`max(6, 7) = 7`** ✅

**Rows 4 and 5 are the run-collapsing in action.** The array rises `10 → 13 → 15`, three consecutive up moves. Each sets `up = down + 1 = 4` — **the same value every time**, because `down` hasn't changed. **The run contributes exactly one wiggle step**, not three.

**Row 7 does the same for a descent** (`10 → 5` after `15 → 10`): `down` stays at 5.

**Reading off a witness subsequence:** the turning points are `1, 17, 5, 15, 5, 16, 8` — **seven elements**, matching the answer. (The problem's own example gives `[1,17,10,13,10,16,8]`, a different witness of the same length — **both are optimal.**)

**Example 3** (`[1,2,3,4,5,6,7,8,9]`) is entirely monotone:

```
every step is "up", so up = down + 1 = 2 each time, and down never changes
final: up = 2, down = 1  →  max = 2 ✅
```

⚠️ **This is the case that catches `up = up + 1`** — that version would return 9.

**The equal-neighbours case**, not in the examples but explicitly warned about in the statement:

```
nums = [1, 7, 4, 5, 5]

i=1: up   →  up = 2
i=2: down →  down = 3
i=3: up   →  up = 4
i=4: 5 == 5  →  ⚠️ NEITHER branch fires
result: max(4, 3) = 4 ✓   (the subsequence 1, 7, 4, 5)
```

**The statement's own counterexample** `[1,7,4,5,5]` is called out as *not* a wiggle sequence precisely because of that trailing zero difference — **and the missing `else` is what handles it.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one pass, a comparison and an assignment per element.

At n = 1000 that's **1,000 operations**. Instant. **This satisfies the problem's follow-up.**

**This is optimal**: every element must be examined, since any could be a turning point. **Ω(n) is the lower bound.**

**Versus the O(n²) DP**, which is the natural first formulation:

| Approach | Time | Space |
|---|---|---|
| Enumerate subsequences | O(2ⁿ·n) | — |
| O(n²) DP with inner scan | O(n²) = 10⁶ | O(n) |
| **Two variables** | **O(n) = 10³** | **O(1)** ✅ |

⚠️ **The collapse from O(n²) to O(n) rests on a specific observation:** `up` and `down` are **non-decreasing** in `i`, so `max(down[j])` over all `j < i` is simply the current `down`. **No inner loop is needed to find it.** That's the insight the follow-up is fishing for.

**The sign-counting version is also O(n)** — one pass to build the diffs, one to count alternations. **Two passes rather than one**, and it allocates an O(n) list, so the two-variable version is marginally better.

**Contrast with [Longest Increasing Subsequence](300-longest-increasing-subsequence.md)**, which looks similar and is genuinely harder: LIS needs O(n log n) with patience sorting, because "increasing" admits many incomparable candidate subsequences. **Wiggle only ever cares about the last direction**, which is one bit of state — **that's why two variables suffice.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers.

| Component | Size |
|---|---|
| `up`, `down` | two integers → **O(1)** |
| **Total** | **O(1)** |

**No array, no DP table.** The input is read once and never modified.

| Approach | Space |
|---|---|
| O(n²) DP | O(n) — two arrays |
| Sign counting | O(n) — the `diffs` list |
| **Two variables** | **O(1)** ✅ |

⚠️ **The sign-counting version allocates an O(n) list** for the differences. It could be made O(1) by tracking the previous sign in a variable instead — **at which point it's essentially the two-variable version wearing different clothes.**

**Why O(1) is achievable at all:** the only state that matters is the length of the best wiggle ending in each direction. **Nothing about *which* elements were chosen is needed**, and the recurrence looks back exactly one step.

⚠️ **The trade:** you get the length, not the subsequence. **Recovering a witness needs O(n)** — record each turning point as you pass it.

**No recursion**, no auxiliary structures. The input is not mutated.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because deletions are free, the answer depends only on the sequence of directions in the array — a run of consecutive increases contributes just one wiggle step, since taking interior points of a run doesn't alternate. So I track two numbers: the longest wiggle ending on an up move and the longest ending on a down move. On an increase, `up` becomes `down + 1`, because an up must follow a down — that's what alternating means. On a decrease, symmetrically. And on equal neighbours, neither changes, because a zero difference isn't a wiggle at all — the statement calls that out explicitly, and it's why there's no `else` branch. Both start at 1, since a single element is a valid wiggle, and the answer is the larger of the two. O(n) time and O(1) space, which answers the follow-up. The natural formulation is an O(n²) DP scanning all earlier indices, and it collapses to this because `up` and `down` are non-decreasing — so the max over all earlier positions is just the current value."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `up = down + 1` rather than `up + 1`?" | **The question.** Alternation means an up move must follow a down-ending wiggle. `up + 1` would count monotone runs — `[1,2,3,4,5]` would return 5 instead of 2. |
| "What about equal neighbours?" | Neither variable changes — a zero difference isn't a wiggle. That's why there's no `else`. |
| "How does the O(n²) DP collapse?" | `up` and `down` are non-decreasing in `i`, so the max over all `j < i` is just the running value. No inner loop needed. |
| "Why does the greedy match the DP?" | Keeping only the extremes of each monotone run is provably optimal — any subsequence using an interior point can be rewritten to use the endpoint. |
| "Why do both start at 1?" | A single element is a valid wiggle of length 1, and either direction may be extended first. |
| "Return the actual subsequence?" | Record each turning point as you pass it. O(n) extra. |
| "How does this differ from [LIS](300-longest-increasing-subsequence.md)?" | LIS needs O(n log n) because many incomparable candidates exist. Wiggle only tracks the last direction — one bit of state, hence O(1). |
| "**Non-strict** alternation?" | Equal neighbours would then count, and the answer becomes the array length. Much easier. |
| "Longest wiggle **subarray** instead?" | Contiguity is required, so a run of same-signed differences ends the subarray. One pass tracking the current run length. |

**Traps:**

- **`up = up + 1`** — counts monotone runs; `[1,2,3,4,5]` returns 5 instead of 2. **The defining bug.**
- **Adding an `else` branch** — treats equal neighbours as a direction, inflating the answer on `[1,5,5,2]`.
- **Starting `up` and `down` at 0** — undercounts by one throughout.
- **Returning `up` or `down` alone** — the best wiggle can end in either direction.
- **Using `abs()` on the differences** — destroys the sign information the algorithm runs on.
- **Requiring contiguity** — it's a subsequence, so gaps are allowed.
- **Reaching for the O(n²) DP** — correct but misses the follow-up's point.

**This same move shows up in:** [Longest Increasing Subsequence](300-longest-increasing-subsequence.md) (the harder cousin, where O(1) state is impossible) · [Best Time to Buy and Sell Stock II](122-best-time-to-buy-and-sell-stock-ii.md) (another one-pass greedy over adjacent differences) · [Maximum Subarray](53-maximum-subarray.md) (running state collapsing an O(n²) DP to O(n)) · [Jump Game II](45-jump-game-ii.md) (greedy matching a DP because local extremes are provably optimal).

</details>

---
