# 84. Largest Rectangle in Histogram

**Hard** · [LeetCode](https://leetcode.com/problems/largest-rectangle-in-histogram/)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array `heights` representing the heights of histogram bars, each of **width 1**, return the **area of the largest rectangle** in the histogram.

```
heights = [2,1,5,6,2,3]  →  10

      █                    the 5 and 6 bars, both ≥ 5 tall,
   █  █                    give a 5 × 2 = 10 rectangle
   █  █     █
█  █  █  █  █
█  █  █  █  █  █
2  1  5  6  2  3
```

```
heights = [2,4]  →  4
```

**Constraints:** `1 <= heights.length <= 10⁵` · `0 <= heights[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**largest** rectangle" | An optimization over every possible rectangle |
| bars have **width 1** | Area = height × (number of bars spanned). Pure integer arithmetic |
| the rectangle must **fit under** the bars | ⚠️ A rectangle spanning bars `i..j` is limited to the **minimum** height in that range |
| n up to 10⁵ | O(n²) = 10¹⁰ → dead. Target **O(n)** |
| heights can be **0** | A zero bar splits the histogram — nothing spans it |

**The reframe that makes it tractable.** Instead of enumerating rectangles by their left and right edges (n² of them), enumerate by **height**. Every maximal rectangle has some bar whose full height it uses — so ask, for each bar `i`:

> *"If my rectangle is exactly `heights[i]` tall, how far left and right can it extend?"*

It extends until it meets a bar **shorter** than `heights[i]` in either direction. So:

```
area(i) = heights[i] × (right_boundary − left_boundary)
```

where the boundaries are the nearest strictly-shorter bars on each side. Take the max over all `i`.

That's now n subproblems of the form *"find the nearest shorter bar to the left/right"* — which is **next smaller element**, the mirror of [Daily Temperatures](739-daily-temperatures.md). And you already know that's a monotonic stack.

**The key realization for the one-pass version:** when a new shorter bar arrives, it *is* the right boundary for every taller bar still waiting. So you can compute each bar's rectangle at the moment it gets popped.

🤔 **Before you open the next section:** a bar is popped because a shorter bar arrived. At that instant, do you know both of its boundaries? Where did the left one come from?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| All pairs `(i, j)` | Try every range, find its min | O(n³) or O(n²) | ❌ 10¹⁰ |
| For each bar, expand outward | Walk left and right until shorter | O(n²) | ❌ Degenerate on uniform heights |
| Divide and conquer | Split at the minimum bar, recurse | O(n log n) avg, **O(n²)** worst | ⚠️ Degrades on sorted input |
| **Monotonic increasing stack** | Compute each bar's rectangle when it's popped | **O(n)** | ✅ |

**The decision: a monotonic **increasing** stack of `(start_index, height)` pairs.**

Increasing, not decreasing — the mirror of [Daily Temperatures](739-daily-temperatures.md), because here you're hunting the nearest **shorter** bar rather than the nearest taller one.

The invariant:

> **The stack holds bars whose rectangles are still open — their right boundary hasn't been found — and their heights increase from bottom to top.**

When bar `i` arrives:

- **While the top of the stack is taller than `heights[i]`**, that bar can't extend past `i`. Its right boundary is `i`. Pop it, compute `height × (i − start_index)`, and record.
- Then push `(start, heights[i])`.

**The `start` trick — the piece that makes this elegant.** When you pop a taller bar, the new bar can extend **backwards** over the popped bar's territory: everything the taller bar covered is at least as tall as the new bar. So the new bar inherits the popped bar's start index.

```
heights = [5, 6, 2]
                ↑ when 2 arrives, it pops 6 (start 1) and 5 (start 0)
                  so 2's rectangle starts at index 0, not index 2
```

Without carrying `start`, you'd compute widths from the wrong left edge and undercount.

**Why the stack is increasing.** After popping everything taller, the new bar is taller than whatever remains — so the stack stays sorted. And a bar's left boundary is exactly the bar below it on the stack, which is why the boundaries never need a separate search.

**Why not divide and conquer?** O(n log n) on average, but O(n²) on already-sorted input — the recursion degenerates. The stack is O(n) unconditionally.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
max_area = 0
```

`stack` holds `(start_index, height)` tuples for bars whose rectangles are still open. `max_area` starts at 0 since areas are never negative.
→ [list-basics](../syntax/list-basics.md) · [tuple-basics](../syntax/tuple-basics.md) · [stack](../data-structures/stack.md)

```python
for i, height in enumerate(heights):
    start = i
```

`start` is where the current bar's rectangle *begins*. It's initialized to `i` — but it will be pushed **backwards** as taller bars get popped.
→ [enumerate](../syntax/enumerate.md) · [for-loop](../syntax/for-loop.md)

```python
    while stack and stack[-1][1] > height:
```

**The resolution step.** While the bar on top is **taller** than the current one, it can't extend past here — this bar is its right boundary, so its rectangle is finished.

`stack[-1][1]` is the height component of the top tuple (`[-1]` = top of stack, `[1]` = the height field).

`while`, not `if` — one short bar can close out many taller ones.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
        index, prev_height = stack.pop()
        max_area = max(max_area, prev_height * (i - index))
```

Pop and compute. The width is `i - index`: from where that bar's rectangle started, up to (not including) the current position — which is exactly the span over which it was the limiting height.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        start = index
```

**The subtle line.** The current bar inherits the popped bar's start, because everything that bar spanned is at least as tall as the current bar — so the current bar's rectangle can extend back that far too.

Miss this and every width after a pop is too small.

```python
    stack.append((start, height))
```

Push the current bar with its (possibly extended) start. The stack is increasing again: everything taller was just popped.

```python
for index, height in stack:
    max_area = max(max_area, height * (len(heights) - index))
```

**The cleanup pass.** Bars still on the stack never met a shorter bar, so they extend all the way to the **right end** of the histogram. Their width is `len(heights) - index`.

Forgetting this pass is the classic bug — on `[1,2,3,4,5]` nothing is ever popped during the loop, and you'd return 0.
→ [for-loop](../syntax/for-loop.md)

```python
return max_area
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:

        stack = []
        max_area = 0

        for i, height in enumerate(heights):
            start = i
            while stack and stack[-1][1] > height:
                index, prev_height = stack.pop()
                max_area = max(max_area, prev_height * (i - index))
                start = index
            stack.append((start, height))

        for index, height in stack:
            max_area = max(max_area, height * (len(heights) - index))

        return max_area
```

</details>

**Trace it** — `heights = [2,1,5,6,2,3]`:

| `i` | h | Pops → area | `start` | Stack after `(start,h)` | `max_area` |
|---|---|---|---|---|---|
| 0 | 2 | — | 0 | `(0,2)` | 0 |
| 1 | 1 | pop `(0,2)` → 2×(1−0)=**2** | **0** | `(0,1)` | 2 |
| 2 | 5 | — | 2 | `(0,1) (2,5)` | 2 |
| 3 | 6 | — | 3 | `(0,1) (2,5) (3,6)` | 2 |
| 4 | 2 | pop `(3,6)` → 6×(4−3)=6; pop `(2,5)` → 5×(4−2)=**10** | **2** | `(0,1) (2,2)` | **10** |
| 5 | 3 | — | 5 | `(0,1) (2,2) (5,3)` | 10 |

**Cleanup:**
- `(0,1)` → 1 × (6−0) = 6
- `(2,2)` → 2 × (6−2) = 8
- `(5,3)` → 3 × (6−5) = 3

Answer: **10** ✅

Row 4 shows both mechanisms: the `while` popping two bars, and `start` being dragged back to 2 so the bar of height 2 spans indices 2–5 in the cleanup (width 4, area 8) rather than just itself.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

| Step | Cost |
|---|---|
| Main loop | n iterations, O(1) each excluding pops |
| All pops, total | **≤ n**, since each bar is pushed exactly once |
| Cleanup pass | ≤ n entries remaining |

The familiar amortized argument, one more time:

> **Every bar is pushed exactly once and popped at most once**, so total stack operations are bounded by 2n regardless of how the `while` nests.

A single iteration can pop many bars (row 4 popped two; on `[1,2,3,4,5,1]` the final bar pops five). Those pops are paid for by the pushes that created them → **O(n)** overall.

**Versus the alternatives:** brute force O(n²) → 10¹⁰; divide and conquer O(n log n) average but O(n²) on sorted input; the stack is O(n) unconditionally, which is why it's the expected answer on a Hard.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the stack.

- **Worst case O(n):** strictly increasing heights, `[1,2,3,4,5]`. Nothing is ever popped in the main loop, so all n bars sit on the stack until the cleanup pass.
- **Best case O(1):** strictly decreasing, `[5,4,3,2,1]`. Each bar pops the previous one immediately, so the stack holds one entry.

Each entry is a 2-tuple, so it's 2n integers — still O(n).

**The `start`-tracking version vs. the index-only version.** Many published solutions push only indices and derive the width as `i - stack[-1] - 1` after popping, using the *new* stack top as the left boundary. That's equivalent and uses slightly less memory.

Storing `(start, height)` explicitly is more verbose but makes the width calculation direct — `i - index` needs no reasoning about what's underneath. **On a Hard problem, the version you can explain without hesitating is the right one to write.**

**A common simplification** is appending a sentinel `0` to the input, which forces every remaining bar to be popped and eliminates the cleanup pass entirely. Tidy, and worth mentioning — but the explicit pass makes the "these bars reach the end" logic visible.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rather than enumerate rectangles by their edges, I enumerate by height: for each bar, the biggest rectangle using its full height extends until it hits a shorter bar on either side. So each bar needs its nearest smaller element left and right — that's a monotonic stack. I keep an increasing stack of `(start, height)`. When a shorter bar arrives, every taller bar on the stack has found its right boundary, so I pop it and compute `height × (i − start)`. The subtle part is that the incoming bar inherits the popped bar's start index, because it can extend back over that territory. At the end, anything left on the stack reaches the right edge, so I do a final pass with width `n − start`. Each bar is pushed and popped once, so O(n) time and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does the new bar inherit `start`?" | **The question.** Everything the popped (taller) bar spanned is ≥ the new bar's height, so the new bar's rectangle extends back over it too. Demo with `[5,6,2]`. |
| "Why is the nested loop O(n)?" | Each bar is pushed once and popped once — total pops ≤ n across the whole run. |
| "Why does the cleanup pass exist?" | Bars never popped never found a shorter bar to their right, so they extend to the end. Without it, `[1,2,3]` returns 0. |
| "Avoid the cleanup pass." | Append a sentinel `0` to `heights` — it's shorter than everything, so it flushes the stack. |
| "**Maximal Rectangle** in a binary matrix?" | Build a histogram per row (heights of consecutive 1s above) and run this algorithm on each row. O(rows × cols). LeetCode 85, and the reason this problem matters. |
| "Solve [Trapping Rain Water](42-trapping-rain-water.md) with a stack?" | Same family — but there you compute water *horizontally* on each pop rather than a rectangle. |
| "Divide and conquer?" | Split at the minimum bar, recurse both sides. O(n log n) average, O(n²) on sorted input. |

**Traps:**

- **Forgetting `start = index`.** Every width after a pop is too small. The single most common bug here.
- **Skipping the cleanup pass.** Increasing input returns 0.
- **Width as `i - index + 1`** or `i - index - 1`. It's the plain difference — verify on `[5,1]`: popping the 5 at `i=1` gives width 1, area 5. ✅
- **A decreasing stack** instead of increasing. You'd be finding the nearest *taller* bar, which is the wrong boundary.
- **`>=` instead of `>`** when popping. Equal heights are fine to keep — popping them still yields the right maximum, but `>` avoids redundant work and keeps starts cleaner.
- **Comparing `stack[-1]` to `height`** without indexing into the tuple — you'd compare a tuple to an int, which raises `TypeError`.

**This same move shows up in:** [Daily Temperatures](739-daily-temperatures.md) (the mirror — nearest *greater*, on a decreasing stack) · [Sliding Window Maximum](239-sliding-window-maximum.md) (the monotonic deque) · [Trapping Rain Water](42-trapping-rain-water.md) (same stack, computing water instead of rectangles) · [Car Fleet](853-car-fleet.md) (resolving each item against the one ahead).

</details>

---
