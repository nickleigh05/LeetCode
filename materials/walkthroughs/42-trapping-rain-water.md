# 42. Trapping Rain Water

**Hard** · [LeetCode](https://leetcode.com/problems/trapping-rain-water/) · [Solution file (no hints)](../../problems/0001-0499/42.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute **how much water it can trap after raining**.

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]  →  6

           █
   █░░░░░░███░█            ░ = trapped water (6 units)
 █░██░█████████
```

```
height = [4,2,0,3,2,5]  →  9
```

**Constraints:** `1 <= n <= 2·10⁴` · `0 <= height[i] <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

The reframe that makes this tractable: **stop thinking about pools, start thinking about columns.** Don't try to identify basins and measure them — instead ask, for each index independently, *how deep is the water directly above this bar?*

For a single position `i`:

```
water[i] = min(tallest bar to the left, tallest bar to the right) − height[i]
```

Water at `i` is held in by the tallest wall on each side, and it spills over whichever of those is **shorter**. Subtract the bar itself to get the water, and clamp at 0 (a bar taller than its walls holds nothing).

Sum that over every index and you're done. One hard geometry problem became n independent easy ones.

| The statement says | Which really means |
|---|---|
| "how much water is **trapped**" | Total volume — so per-column depths just **add up**. No merging of basins needed |
| bars have **width 1** | Volume = depth, arithmetically. No area calculation |
| n up to 2·10⁴ | O(n²) = 4·10⁸ is borderline-dead; aim for O(n) |
| heights can be **0** | Flat gaps are normal, and water sits above them fine |
| non-negative | No negative depths to reason about |

⚠️ Note how this differs from [Container With Most Water](11-container-with-most-water.md), which looks like the same picture: there, intermediate bars are ignored and you want *one* best pair. Here, **every** bar matters — they're both the walls and the floor.

🤔 **Before you open the next section:** the formula needs the max to the left *and* the max to the right of every index. The obvious way is to precompute two arrays. Can you get both without storing either?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Extra space | Verdict |
|---|---|---|---|---|
| Brute force | For each `i`, scan both directions for the maxima | O(n²) | O(1) | ❌ Rescans the same bars endlessly |
| **Prefix/suffix arrays** | Precompute `left_max[]` and `right_max[]`, then one pass | O(n) | **O(n)** | ⚠️ **Write this first** — it's the clearest expression of the formula |
| [Monotonic stack](../data-structures/monotonic-stack.md) | Pop bars to fill basins layer by layer | O(n) | O(n) | ⚠️ Works, computes water horizontally instead of vertically |
| **Two pointers** | Converge, carrying running maxima | **O(n)** | **O(1)** | ✅ |

**The decision: two pointers with running `left_max` and `right_max`.**

**How you get there.** Start from the prefix/suffix version — it's the honest first draft and directly encodes the formula. Then notice you never need the *whole* arrays, only the maxima at the current position. A running variable can carry each one, if you walk in the right direction.

**The subtlety that makes it work.** From the left you can maintain a true `left_max`, but you don't know the real `right_max` yet — you only know the max of what you've seen from the right so far, which is a **lower bound** on the true one. Symmetrically from the right.

The resolution: `water[i] = min(left_max, right_max) − height[i]` depends only on the **smaller** of the two. So:

> If `left_max < right_max`, then `left_max` is definitely the minimum — because the true right max is at least the `right_max` we've seen, which already exceeds `left_max`. **We can commit to the left side's water without knowing the true right max.**

So always advance the pointer on the side whose running max is smaller. That side's answer is fully determined right now.

**Why not the stack?** It's a good O(n) solution and worth naming — it fills basins horizontally, layer by layer. But it's O(n) space and harder to explain under pressure. Two pointers gets O(1).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(height) - 1
left_max = height[left]
right_max = height[right]
rain = 0
```

Pointers at both ends, each seeded with the wall it's standing on. Seeding with the actual heights (not 0) matters: the outermost bars are the first walls, and it guarantees `max_ − height[i] >= 0` so no negative water can ever be added.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while left < right:
```

Converge until they meet.
→ [while-loop](../syntax/while-loop.md)

```python
    if left_max < right_max:
```

**The decision line.** The smaller running max is the binding constraint, so that side's water is already determined — advance it. Whichever side is smaller, we can compute its answer without knowing anything more about the other.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
        left += 1
        left_max = max(left_max, height[left])
        rain += left_max - height[left]
```

Read the order carefully — **move first, then update, then collect**:

1. `left += 1` steps onto the new bar.
2. `left_max = max(...)` folds it into the running maximum.
3. `rain += left_max - height[left]` adds the water above it.

Updating the max **before** collecting is what makes this safe. If the new bar is the tallest so far, `left_max` becomes `height[left]` and the water added is exactly `0` — correct, since a bar taller than everything to its left holds no water. **That's why no explicit `max(0, ...)` clamp is needed.**
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    else:
        right -= 1
        right_max = max(right_max, height[right])
        rain += right_max - height[right]
```

The mirror image. Ties go here — fine, since when the maxima are equal either side's water is fully determined.
→ [elif-else](../syntax/elif-else.md)

```python
return rain
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def trap(self, height: List[int]) -> int:

        left = 0
        right = len(height) - 1
        left_max = height[left]
        right_max = height[right]
        rain = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                rain += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                rain += right_max - height[right]

        return rain
```

</details>

**Trace it** — `height = [4,2,0,3,2,5]`, answer 9:

| `left` | `right` | `left_max` | `right_max` | Side | New bar | Water added | `rain` |
|---|---|---|---|---|---|---|---|
| 0 | 5 | 4 | 5 | left (4<5) | `h[1]=2` | 4−2 = **2** | 2 |
| 1 | 5 | 4 | 5 | left | `h[2]=0` | 4−0 = **4** | 6 |
| 2 | 5 | 4 | 5 | left | `h[3]=3` | 4−3 = **1** | 7 |
| 3 | 5 | 4 | 5 | left | `h[4]=2` | 4−2 = **2** | 9 |
| 4 | 5 | 4 | 5 | — | `left == right`, stop | | **9** ✅ |

Notice we computed all the water using `left_max = 4` while never learning that the true right max was 5 — we only ever needed to know it was **at least** 5, which was enough to prove the left side was binding.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pointer moves per iteration, the gap shrinks by exactly 1, so the loop runs at most n−1 times with O(1) work each — a `max`, a subtraction, an addition.

**O(n)** total, and every bar is visited exactly once by exactly one pointer.

**Versus the brute force:** O(n²) → O(n). The brute force rescans the entire array from every index to find the maxima; the running variables carry that information forward instead, so nothing is recomputed. Same "don't repeat work you've already done" principle as [prefix sums](../learning/01b-prefix-sums.md) and [Product of Array Except Self](238-product-of-array-except-self.md).

**All three efficient solutions are O(n)** — prefix/suffix arrays, monotonic stack, and two pointers. They differ only in space, which is why this problem is really a *space* exercise once you've found any linear approach.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — and this is what elevates the solution from "correct" to "the answer they're looking for."

Five integers: `left`, `right`, `left_max`, `right_max`, `rain`. Nothing scales with n.

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Prefix/suffix arrays | O(n) | **O(n)** |
| Monotonic stack | O(n) | O(n) |
| **Two pointers** | **O(n)** | **O(1)** |

**Where the O(n) went.** The prefix/suffix version stores a max for every index. The two-pointer version notices that at any moment you only need the max *behind each pointer* — a single number per side — provided you always advance the side whose max is smaller. **The O(1) is bought by the ordering of the traversal, not by storing less information.**

That's the transferable idea: *"do I need this whole array, or just its running value?"* is worth asking every time you precompute one. It's the same collapse that took [Product of Array Except Self](238-product-of-array-except-self.md) from two arrays down to two variables.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rather than finding pools, I'll compute the water above each bar independently: it's `min(max to the left, max to the right) − height[i]`. The direct version precomputes both max arrays — O(n) time, O(n) space. To get O(1) space I use two pointers with running maxima. The insight is that the water at a position depends only on the *smaller* of the two maxima, so if `left_max < right_max`, the left side is definitely binding — the true right max is at least the one I've seen, which already exceeds it. So I can commit to that side's water and advance it, without ever knowing the true right max. O(n) time, O(1) space."

**Start with the prefix/suffix version if you're stuck** — it demonstrates you have the formula, and the interviewer will often push you toward the optimization from there. Getting a correct O(n)/O(n) on the board beats stalling on O(1).

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is it safe to advance the smaller side?" | **The question.** The true opposite max is ≥ the running one, which already exceeds the smaller side — so the smaller side is the minimum regardless of what's still unseen. Its water is fully determined. |
| "Solve it with a stack." | Monotonic decreasing stack of indices: when a taller bar arrives, pop and fill the basin it closes, width × bounded height. O(n)/O(n), computes water *horizontally*. See [monotonic-stack](../data-structures/monotonic-stack.md). |
| "What if bars had width > 1?" | Multiply each column's depth by the width. The structure is unchanged. |
| "2-D version — water on a heightmap?" | Genuinely harder: a min-heap processing cells from the border inward, since water escapes via the lowest boundary. That's LeetCode 407. See [heap](../data-structures/heap.md). |
| "How is this different from Container With Most Water?" | There you pick **two** lines and ignore everything between; here **every** bar is both wall and floor, and you sum all of them. |
| "What if the input is a stream?" | You can't — the answer at the left depends on bars arbitrarily far right. You need the full array (or two passes). |

**Traps:**

- **Collecting water before updating the running max.** You'd add a negative amount at any new peak. Update, *then* collect.
- **Seeding `left_max = 0`** instead of `height[0]`. It usually still works because of the update-first ordering, but seeding with the real wall is what makes the non-negativity obvious.
- **Advancing the *larger* side.** Its water isn't determined yet — you'd be committing to a max that could still be beaten.
- **Trying to identify basins directly.** Vastly harder. The per-column reframe is the whole trick.
- **Confusing it with [Container With Most Water](11-container-with-most-water.md)** and using `min(height[left], height[right])` on the *bars* rather than on the running *maxima*.
- **Adding an unnecessary `max(0, ...)` clamp** — harmless, but it signals you haven't seen why the ordering already guarantees non-negativity.

**This same move shows up in:** [Container With Most Water](11-container-with-most-water.md) (converging pointers, similar picture, different question) · [Product of Array Except Self](238-product-of-array-except-self.md) (left-running and right-running values combined per index) · [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (the stack solution to this problem's sibling) · [Sliding Window Maximum](239-sliding-window-maximum.md) (running maxima maintained incrementally).

</details>

---
