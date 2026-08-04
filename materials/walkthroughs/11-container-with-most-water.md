# 11. Container With Most Water

**Medium** · [LeetCode](https://leetcode.com/problems/container-with-most-water/) · [Solution file (no hints)](../../problems/0001-0499/11.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

You're given an integer array `height` of length `n`. There are `n` vertical lines, where line `i` runs from `(i, 0)` to `(i, height[i])`.

Find two lines that, together with the x-axis, form a container holding **the most water**. Return that maximum amount.

*(The container can't be tilted, and the lines have no thickness.)*

```
height = [1,8,6,2,5,4,8,3,7]  →  49     (lines at index 1 and 8: width 7 × height min(8,7)=7)
height = [1,1]                →  1
```

**Constraints:** `2 <= n <= 10⁵` · `0 <= height[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

First, get the formula exact — everything depends on it. For lines at indices `i` and `j`:

```
area = (j - i) × min(height[i], height[j])
        └ width ┘   └──── height ────┘
```

Water spills over the **shorter** wall, so the shorter line alone determines the depth. That single fact drives the entire solution.

| The statement says | Which really means |
|---|---|
| "**most** water" | An optimization over all pairs — n² of them, and you can't afford to enumerate |
| the area formula | Two competing factors: **width** shrinks as lines get closer, **height** is capped by the shorter line |
| "**can't be tilted**" | Intermediate lines are irrelevant. Water isn't blocked by shorter bars between the two walls — unlike [Trapping Rain Water](42-trapping-rain-water.md) |
| n up to 10⁵ | O(n²) = 10¹⁰ → dead. You need **O(n)** or O(n log n) |
| heights can be **0** | A zero-height line gives zero area. No crash, just useless |

Now think about where to start. **Width is maximized at the two extreme ends** — that's the widest container possible. Any other pair is narrower, so it can only win by being *taller*.

That reframes the search: begin at maximum width, then look for the height gains that justify giving width up.

🤔 **Before you open the next section:** starting at both ends, you must move one pointer inward — which loses width. If you move the **taller** line's pointer, can the area ever improve? Work through why not.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | Every pair `(i, j)`, compute area | O(n²) | ❌ 10¹⁰ operations |
| Sort by height | Sort, then… | — | ❌ Sorting **destroys the indices**, and width depends on index |
| **Two pointers, move the shorter** | Start at the ends, converge | **O(n)** | ✅ |

**The decision: two pointers at the ends, always moving the pointer at the shorter line.**

**Why moving the shorter line is the *only* safe choice** — this is the whole problem, and the thing you must be able to argue:

Say `left` and `right` are the current pointers, with `height[left] < height[right]`. The current area is `(right − left) × height[left]`.

Now consider **every** container that uses `left` as one wall. All of them are narrower than the current one (any partner is to the left of `right`), and all of them are capped at `height[left]` or lower — because the depth is `min(height[left], other)` and `height[left]` is already the smaller. So:

> **No pair involving `left` can beat the area we just computed.** `left` is exhausted — discard it.

Whereas if you moved `right` instead, you'd lose width while the height stays capped by that same short `left` wall — guaranteed strictly worse. Every move must discard the shorter side.

This is the same **discard argument** as [Two Sum II](167-two-sum-ii-input-array-is-sorted.md): each step eliminates one element along with every pair it could form, which is how n comparisons search an n² space.

**Why not sort?** The width term depends on the *positions*, and sorting scrambles them. This is a case where the input's structure is positional, so reordering destroys the problem.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(height) - 1
max_area = 0
```

Pointers at the extreme ends — **the widest possible container**, the natural starting point. `max_area` starts at 0 since areas are never negative.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while left < right:
```

Run until the pointers meet. At `left == right` the width is 0, so there's no container left to consider.
→ [while-loop](../syntax/while-loop.md)

```python
    area = (right - left) * min(height[left], height[right])
    max_area = max(max_area, area)
```

The formula, applied to the current pair. `right - left` is the width; `min(...)` is the depth, because **water spills over the shorter wall**.

Compute the area *before* moving anything — this pair is a genuine candidate and must be measured.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [min-max-key](../syntax/min-max-key.md)

```python
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
```

**The decision that makes it O(n).** Move the pointer at the shorter line — it's the limiting wall, and per the argument in section 2, no remaining pair involving it can beat what we just recorded.

The `else` handles the tie: when the heights are equal, moving either is fine. Both walls are equally limiting, and any narrower container using either one is capped at the same height with less width — so neither can improve. Moving one is enough.
→ [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return max_area
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:

        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

</details>

**Trace it** — `height = [1,8,6,2,5,4,8,3,7]`:

| `left` | `right` | Width | Depth `min` | Area | `max_area` | Move |
|---|---|---|---|---|---|---|
| 0 (1) | 8 (7) | 8 | 1 | 8 | 8 | `left` (1 < 7) |
| 1 (8) | 8 (7) | 7 | 7 | **49** | **49** | `right` (8 ≥ 7) |
| 1 (8) | 7 (3) | 6 | 3 | 18 | 49 | `right` |
| 1 (8) | 6 (8) | 5 | 8 | 40 | 49 | `right` (tie) |
| 1 (8) | 5 (4) | 4 | 4 | 16 | 49 | `right` |
| … | | | | | 49 | |

Answer: **49**.

Look at step 1: the very first move discarded index 0 (height 1) forever — and with it, all 8 pairs that used it. That's the discard argument doing its work.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each iteration does O(1) work and moves exactly one pointer inward. The gap starts at n−1 and shrinks by exactly 1 per iteration, so the loop runs at most n−1 times.

**O(n)** total — down from the brute force's O(n²). At n = 10⁵ that's 10¹⁰ operations reduced to 10⁵.

**Why one pass suffices to search n²/2 pairs:** every move eliminates a line *and every pair containing it*, justified by the argument in section 2. You never examine most pairs because you've **proven** they can't win, not because you're sampling or guessing. That proof is what makes it a correct algorithm rather than a heuristic — and it's exactly what an interviewer probes.

There's no early exit: the maximum could be anywhere, so all n steps always run.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Three integers — `left`, `right`, `max_area` — plus a transient `area`. Nothing scales with n; the input is only read.

This is the cleanest case in the unit: **O(n²) → O(n) time at zero memory cost.** Unit 01's hash-map solutions all bought their speed with O(n) space. Here the speedup comes from a *proof* about which candidates can be discarded, and proofs are free.

Worth naming the distinction out loud:

| Source of speedup | Cost |
|---|---|
| Remembering things (hash map) | O(n) space |
| **Eliminating things (two pointers)** | **O(1) space** |

When an interviewer asks for better time *and* constant space, the elimination family — two pointers, sliding window, monotonic stacks — is where to look.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Area is width times the shorter of the two lines. Brute force is O(n²) and too slow at 10⁵. I'll start with the widest possible container — pointers at both ends — and move inward. The key insight is which pointer to move: the shorter line is the limiting wall, and any other container using it is both narrower *and* still capped at that same height, so no pair involving it can beat what I've already measured. That means I can discard it entirely. Each step eliminates one line, so it's a single pass — O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Prove moving the shorter pointer is safe." | **The question.** Fix the shorter line: every remaining partner gives less width and a depth still capped by that line. So all its pairs are ≤ the current area, and discarding it loses nothing. |
| "What if the heights are equal?" | Move either — both are equally limiting, and every narrower container using either is capped at the same depth. |
| "What if the container *could* be tilted, or bars blocked the water?" | Then intermediate bars matter and it becomes [Trapping Rain Water](42-trapping-rain-water.md) — a genuinely different problem despite the similar picture. |
| "Return the indices, not just the area." | Store `best_left`/`best_right` whenever you update `max_area`. |
| "Could a divide-and-conquer approach work?" | Yes, but O(n log n) at best and far more code. Two pointers is optimal here — you can't do better than reading the input. |
| "What about three lines?" | Not well defined for a container, but it's a good sign the interviewer wants to see you ask clarifying questions rather than guess. |

**Traps:**

- **Using `max` instead of `min` for the depth.** Water spills over the *shorter* wall — this is the #1 conceptual slip.
- **Moving the taller pointer.** Loses width with no possible height gain; produces answers that are silently too small.
- **Moving both pointers** each iteration — skips over the optimal pair.
- **Computing the area after moving.** You'd never evaluate the widest container at all.
- **Confusing this with [Trapping Rain Water](42-trapping-rain-water.md).** Similar picture, different question: here intermediate bars are irrelevant, there they're the whole point.
- **Sorting by height.** Destroys the positions that the width depends on.

**This same move shows up in:** [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (the identical discard-and-converge argument) · [Trapping Rain Water](42-trapping-rain-water.md) (converge from both ends, driven by the smaller side) · [3Sum](15-3sum.md) (converging pointers as an inner loop) · [Valid Palindrome](125-valid-palindrome.md) (the simplest converging pair).

</details>
