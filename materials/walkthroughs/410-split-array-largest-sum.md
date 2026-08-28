# 410. Split Array Largest Sum

**Hard** · [LeetCode](https://leetcode.com/problems/split-array-largest-sum/) · [Solution file (no hints)](../../problems/0001-0499/410.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given an integer array `nums` and an integer `k`, split `nums` into `k` **non-empty contiguous** subarrays such that the **largest sum** among them is **minimized**. Return that minimized largest sum.

```
nums = [7,2,5,10,8], k = 2  →  18    ([7,2,5] and [10,8] — max sum 18)
nums = [1,2,3,4,5],  k = 2  →  9     ([1,2,3] and [4,5])
nums = [1,4,4],      k = 3  →  4
```

**Constraints:** `1 <= nums.length <= 1000` · `0 <= nums[i] <= 10⁶` · `1 <= k <= min(50, nums.length)`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimize** the **largest** sum" | ⚠️ A minimax objective — the classic signature of *binary search on the answer* |
| "**contiguous** subarrays" | No reordering. Splits are cut points, which keeps the feasibility check greedy |
| "exactly `k`" non-empty parts | But note: if you can do it in **fewer** than `k` parts, you can always split further to reach exactly `k` — see below |
| `nums.length` up to 1000 | An O(n) check inside an O(log range) search is trivially fast |
| `nums[i]` up to 10⁶ | Total ≤ 10⁹ — that's the search range's width |
| `nums[i]` can be **0** | Zero-weight elements are fine and don't break anything |

**Why "minimize the maximum" screams binary search.** You can't compute the optimal split directly, but you can easily answer the inverse question:

> **"Given a limit `L`, can I split the array into at most `k` parts where every part sums to ≤ `L`?"**

Simulate greedily: accumulate until adding the next element would exceed `L`, then cut. Count the parts. That's O(n).

And feasibility is **monotonic**: if limit `L` works, so does `L + 1` (a looser cap never needs more parts). If `L` fails, everything smaller fails.

```
limit:      15   16   17   18   19   20
feasible?   no   no   no  YES  YES  YES
                          ↑
                 the boundary — the answer
```

False-then-true, flipping once — exactly the boundary search from [First Bad Version](278-first-bad-version.md), with candidate *answers* as the domain.

**The subtle point about "at most `k`" vs "exactly `k`".** The greedy check counts the *minimum* parts needed for limit `L`. If that's fewer than `k`, you can always split some part further — every element is non-negative, so splitting never increases any part's sum. So "can be done in ≤ `k` parts" is equivalent to "can be done in exactly `k` parts," and the check can safely use `<=`.

**The search bounds:**

- **`left = max(nums)`** — some part must contain the largest element, so no limit below it can work.
- **`right = sum(nums)`** — one part holding everything always satisfies any `k >= 1`.

🤔 **Before you open the next section:** if a limit lets you finish in fewer than `k` parts, why is that still a success rather than a failure?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n = len(nums)`, `S = sum(nums)`, `M = max(nums)`.

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute-force splits | Try every combination of cut points | O(C(n−1, k−1)) | ❌ Exponential |
| **Dynamic programming** | `dp[i][j]` = best split of first `i` into `j` parts | O(n² · k) = 5·10⁷ | ⚠️ Correct, passes here, much slower |
| **Binary search on the answer** | Halve the limit range; O(n) greedy check | **O(n log S)** | ✅ |

**The decision: binary search the answer, with a greedy O(n) feasibility check.**

Same three ingredients as [Capacity To Ship Packages](1011-capacity-to-ship-packages-within-d-days.md) — and in fact **this is the identical problem with different wording**:

| | Ship Packages | Split Array |
|---|---|---|
| Domain | ship capacity | subarray sum limit |
| Predicate | days needed ≤ `days` | parts needed ≤ `k` |
| Greedy check | load until overflow, new day | accumulate until overflow, new part |
| Bounds | `[max, sum]` | `[max, sum]` |

Recognizing that two differently-dressed problems are the same algorithm is exactly the skill this pairing tests.

**Why greedy is optimal for the check.** Since subarrays must be contiguous and all values are non-negative, cutting as late as possible is never worse: extending a part can only delay the next cut, never force an extra one. So the greedy simulation returns the **exact minimum** number of parts for limit `L`, not an estimate.

If elements could be **negative**, this breaks — a negative value could make a longer part *cheaper*, and the greedy cut point would no longer be optimal. Worth flagging, since the constraint `nums[i] >= 0` is doing real work.

**Why binary search beats the DP.** The DP formulation is `dp[i][j] = min over m of max(dp[m][j-1], sum(m..i))`, which is O(n²·k) — about 5·10⁷ here, and it needs O(n·k) space. Binary search is O(n log S) ≈ 3·10⁴ operations with O(1) space. Both pass at these constraints, but the gap widens fast, and the binary search is far simpler to write correctly.

**The boundary convention:** minimizing means feasible candidates must be **kept**:

- feasible at `mid` → `right = mid` (keep it)
- infeasible → `left = mid + 1`
- loop while `left < right`, return `left`

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def splitArray(self, nums: List[int], k: int) -> int:
    left = max(nums)
    right = sum(nums)
```

**The answer range.**

- `left = max(nums)` — some subarray must contain the largest element, so the answer is at least that.
- `right = sum(nums)` — a single part containing everything is always valid.

Both O(n), dominated by the search.
→ [min-max-key](../syntax/min-max-key.md)

```python
    while left < right:
        mid = (left + right) // 2
```

Boundary-search convention: `<` pairs with `right = mid`.
→ [while-loop](../syntax/while-loop.md)

```python
        if self.partsNeeded(nums, mid) <= k:
            right = mid
        else:
            left = mid + 1
```

**The decision.**

- Achievable within `k` parts → `mid` is a valid limit, possibly not the smallest. **Keep it.**
- Needs more than `k` parts → `mid` is too tight; the answer is larger.

`<=` rather than `==` because finishing in *fewer* parts is still a success — you can always split further, as argued in section 1.
→ [comparison-operators](../syntax/comparison-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    return left
```

The smallest feasible limit — which is the minimized largest sum.

---

**The feasibility check**

```python
def partsNeeded(self, nums, limit):
    parts = 1
    current = 0
```

Start with **one** part open. Any non-empty array needs at least one.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    for num in nums:
        if current + num > limit:
            parts += 1
            current = 0
```

**The greedy cut.** If adding this element would exceed the limit, close the current part and open a new one.

Because `limit >= max(nums)` throughout the search, every individual element fits into a fresh part — so this can never loop or fail to place an element.
→ [for-loop](../syntax/for-loop.md)

```python
        current += num
    return parts
```

Add the element to the (possibly new) current part.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:

        left = max(nums)
        right = sum(nums)

        while left < right:
            mid = (left + right) // 2

            if self.partsNeeded(nums, mid) <= k:
                right = mid
            else:
                left = mid + 1

        return left

    def partsNeeded(self, nums: List[int], limit: int) -> int:

        parts = 1
        current = 0

        for num in nums:
            if current + num > limit:
                parts += 1
                current = 0
            current += num

        return parts
```

</details>

**Trace it** — `nums = [7,2,5,10,8]`, `k = 2`. Range: `left = 10`, `right = 32`.

| `left` | `right` | `mid` | Parts needed at `mid` | ≤ 2? | Action |
|---|---|---|---|---|---|
| 10 | 32 | 21 | 2 (`[7,2,5]`=14, `[10,8]`=18) | ✅ | `right = 21` |
| 10 | 21 | 15 | 3 (`[7,2,5]`=14, `[10]`, `[8]`) | ❌ | `left = 16` |
| 16 | 21 | 18 | **2** (`[7,2,5]`=14, `[10,8]`=18) | ✅ | `right = 18` ⭐ |
| 16 | 18 | 17 | 3 (`[7,2,5]`, `[10]`, `[8]`) | ❌ | `left = 18` |
| 18 | 18 | — | — | — | exit |

`return 18` ✅

The starred row is decisive: limit 18 is exactly achievable, and `right = mid` **kept it**. With `right = mid - 1` the range would have become `[16,17]` and returned 17 — a limit that provably needs 3 parts.

**Checking `partsNeeded([7,2,5,10,8], 18)`:**

| Element | `current` before | Would exceed 18? | Action | `parts` |
|---|---|---|---|---|
| 7 | 0 | no | `current = 7` | 1 |
| 2 | 7 | no | `current = 9` | 1 |
| 5 | 9 | no | `current = 14` | 1 |
| 10 | 14 | **yes** (24) | cut → `current = 10` | **2** |
| 8 | 10 | no | `current = 18` | 2 |

2 parts ✅ — exactly `k`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log S)</summary>

**O(n · log S)** where `S = sum(nums)`.

- Binary search over `[max(nums), sum(nums)]` — a range of width ≤ `S`, so **O(log S)** iterations.
- Each iteration runs the **O(n)** greedy check.

At the constraints: `n = 1000`, `S ≤ 1000 × 10⁶ = 10⁹`, so `log₂ S ≈ 30`. Total ≈ **3·10⁴ operations** — instant.

**Compare to the DP:** `dp[i][j] = min over m of max(dp[m][j-1], sum(m..i))` is **O(n² · k)** = `1000² × 50` = 5·10⁷, with O(n·k) space. It passes here, but binary search is three orders of magnitude faster and dramatically shorter.

**The reusable formula:**

> **Binary search on the answer costs O(log(range) × cost of one feasibility check).**

Once you spot the pattern, estimating the cost is mechanical.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a few integers. The greedy check allocates nothing, and `max`/`sum` are single passes.

**Versus the DP's O(n·k)** table — 50,000 entries here. Another concrete advantage of the search formulation.

**The structural point, one more time:** the sequence of candidate limits `[M, M+1, …, S]` — up to 10⁹ values — is **never materialized**. It's an implicit ordered domain, probed on demand.

This closes the arc of the unit:

| Problem | The implicit domain |
|---|---|
| [Guess Number](374-guess-number-higher-or-lower.md) | numbers `1…n` |
| [First Bad Version](278-first-bad-version.md) | version numbers |
| [Sqrt(x)](69-sqrtx.md) | candidate roots |
| [Ship Packages](1011-capacity-to-ship-packages-within-d-days.md) | candidate capacities |
| **Split Array** | **candidate sum limits** |

None of them build an array. All of them binary search.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "'Minimize the maximum' is the signature of binary search on the answer. I can't compute the optimal split directly, but I can check a candidate limit `L` in O(n): walk the array accumulating, and cut whenever adding the next element would exceed `L`. That greedy count is exact, because the subarrays are contiguous and the values are non-negative, so cutting as late as possible is never worse. Feasibility is monotonic — a looser limit never needs more parts — so I binary search `L` over `[max(nums), sum(nums)]`. The lower bound is forced because some part must contain the largest element; the upper bound is one part holding everything. If a limit needs at most `k` parts I keep it with `right = mid`; otherwise `left = mid + 1`. Note I use 'at most `k`', not 'exactly' — finishing in fewer parts is fine since I can always split further. O(n log S) time and O(1) space, versus O(n²k) for the DP."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why 'at most `k`' rather than exactly?" | **The subtle point.** Values are non-negative, so any part can be split further without increasing any sum. Fewer parts always upgrades to exactly `k`. |
| "Why is the greedy check exact?" | Contiguous parts and non-negative values mean cutting later never forces an extra cut. |
| "What if values could be **negative**?" | Greedy breaks — a negative element can make a longer part cheaper. You'd need the DP. |
| "Solve it with DP." | `dp[i][j] = min over m of max(dp[m][j-1], sum(m..i))`, with prefix sums. O(n²k) time, O(nk) space. |
| "This resembles [Ship Packages](1011-capacity-to-ship-packages-within-d-days.md)." | **It's the same algorithm** — capacity ↔ sum limit, days ↔ parts. |
| "**Maximize the minimum** instead?" | Same technique, mirrored: keep candidates on the *other* side of the predicate. |
| "Return the actual split?" | Re-run the greedy check at the final limit, recording cut positions. |

**Traps:**

- **`right = mid - 1`.** Discards a feasible limit that might be the answer. The `[7,2,5,10,8]` trace shows it returning 17 instead of 18.
- **Requiring *exactly* `k` parts in the check.** Using `== k` makes the predicate non-monotonic and breaks the search.
- **`left = 0` or `left = 1`.** Limits below `max(nums)` can't hold the largest element; the greedy check would misbehave.
- **`parts = 0`.** Off by one — any non-empty array needs at least one part.
- **`left <= right` with `right = mid`.** Infinite loop at a one-element range.
- **Assuming greedy works with negatives.** It doesn't; the non-negativity constraint is load-bearing.
- **Jumping straight to DP.** Correct but slower, longer, and harder to get right under time pressure.

**This same move shows up in:** [Capacity To Ship Packages Within D Days](1011-capacity-to-ship-packages-within-d-days.md) (literally the same algorithm, differently worded) · [Koko Eating Bananas](875-koko-eating-bananas.md) (answer-space search over eating speed) · [First Bad Version](278-first-bad-version.md) (the boundary convention underpinning all of these) · [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) (a related contiguous-partition question solved by sliding window instead).

</details>

---
