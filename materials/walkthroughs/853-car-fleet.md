# 853. Car Fleet

**Medium** · [LeetCode](https://leetcode.com/problems/car-fleet/)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There are `n` cars heading to the same destination along a one-lane road at position `target`. Car `i` starts at `position[i]` and drives at `speed[i]`.

A car can **never pass** another. A faster car that catches up to a slower one slows down to match it, and the two travel as a single **car fleet** (a fleet may be a single car). A car that catches the fleet at the exact moment it reaches the target counts as part of that fleet.

Return the **number of car fleets** that arrive at the destination.

```
target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]  →  3
target = 10, position = [3],          speed = [3]          →  1
target = 100, position = [0,2,4],     speed = [4,2,1]      →  1
```

**Constraints:** `n <= 10⁵` · `0 < target <= 10⁶` · positions are **distinct** · `0 < speed[i] <= 10⁶`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "can **never pass**" | ⚠️ Position order is **permanent**. A car behind stays behind — which is why sorting by position is meaningful |
| "slows down to **match**" | A caught-up car adopts the slower car's arrival time. Fleets are defined by their **slowest, front-most** member |
| "arrives at the **exact moment**" counts | Use `<=` when testing catch-up, not `<` |
| "**number** of fleets" | Just a count — you never need to know which car is in which fleet |
| positions are **distinct** | No ties to break at the start |
| n up to 10⁵ | O(n²) simulation is dead. **O(n log n)** for the sort is the natural target |

Simulating the driving is a trap — it's O(n²) and full of floating-point misery.

The reframe: forget speeds and collisions, and compute the one number that matters for each car — **how long it would take to reach the target if nothing were in its way**:

```
time = (target − position) / speed
```

Now think about the car **closest to the target**. Nothing can block it, so it arrives in exactly its own time. Now consider the car just behind it:

- If its time is **≤** the front car's time, it would arrive at the same moment or sooner — meaning it catches up. It joins that fleet, and the fleet's arrival time stays the *front* car's (slower) time.
- If its time is **greater**, it's genuinely slower and can never catch up. It starts a **new fleet**.

Crucially, when a car merges, it becomes irrelevant — the fleet still arrives at the front car's time. So the merged car changes nothing about what happens behind it.

🤔 **Before you open the next section:** which end should you process from — the car nearest the target, or the one furthest away? Which direction lets you decide each car's fate using only what you've already computed?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Simulate the drive | Step time forward, detect collisions | O(n²) or worse | ❌ Slow and numerically fragile |
| Sort front-to-back, forward scan | Process the car furthest from the target first | O(n log n) | ❌ Wrong direction — a car's fate depends on what's *ahead*, which you haven't seen |
| **Sort back-to-front, stack of times** | Nearest the target first; compare each car to the fleet ahead | **O(n log n)** | ✅ |
| Same, with just a counter | Identical logic, tracking one `max` instead of a stack | O(n log n) | ✅ O(1) extra space |

**The decision: sort by position **descending** (closest to the target first), then scan, keeping a stack of fleet arrival times.**

**Why that direction is forced.** A car's fate depends entirely on what's **ahead** of it — it can be blocked, but it can't affect anything in front. So process front-to-back in *road* terms: start with the car nearest the target, whose time is unblockable, and work backwards. Each car is then compared against a fleet whose arrival time is already final.

The rule per car, using `stack[-1]` = the arrival time of the fleet immediately ahead:

- **`time > stack[-1]`** → slower than the fleet ahead, can never catch it → **push** (a new fleet).
- **`time <= stack[-1]`** → catches up → **don't push** (absorbed; the fleet's time is unchanged).

The answer is `len(stack)`.

**Why `<=` and not `<`.** The problem explicitly says a car arriving at the exact same moment counts as part of the fleet. With `<`, equal times would create a spurious extra fleet.

**The stack observation.** The times on the stack are strictly increasing from bottom to top — another **monotonic stack**, like [Daily Temperatures](739-daily-temperatures.md). But note the difference: here nothing is ever *popped*. Cars are either pushed or discarded on arrival. So you don't actually need the stack's structure — only its top and its size.

**Which means a counter works too:**

```python
fleets = 0
max_time = 0
for pos, spd in sorted(zip(position, speed), reverse=True):
    time = (target - pos) / spd
    if time > max_time:
        fleets += 1
        max_time = time
```

Identical logic in O(1) space. Write whichever you can explain; the stack version makes the "fleet ahead" idea visible, which is often easier to narrate.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
pairs = sorted(zip(position, speed), reverse=True)
```

Three things at once:

- `zip(position, speed)` pairs each car's position with its speed, so they stay together through the sort. Sorting the two lists separately would scramble the correspondence — a classic bug.
- `sorted(...)` on tuples sorts by the **first** element, i.e. position.
- `reverse=True` gives **descending** position — the car closest to the target comes first, which is the direction the logic requires.
→ [zip-function](../syntax/zip-function.md) · [sorting-key](../syntax/sorting-key.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
stack = []
```

Holds the arrival times of established fleets. Its **length** is the answer.
→ [stack](../data-structures/stack.md) · [list-basics](../syntax/list-basics.md)

```python
for pos, spd in pairs:
    time = (target - pos) / spd
```

Each car's **unobstructed** arrival time: distance remaining divided by speed.

Note this is true division producing a float — deliberately. Integer division would round `11/3` down to 3 and merge fleets that shouldn't merge.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if not stack or time > stack[-1]:
        stack.append(time)
```

**The whole decision, in one condition.**

- `not stack` — the first car (nearest the target) has nothing ahead of it, so it always starts a fleet.
- `time > stack[-1]` — this car is **slower** than the fleet immediately ahead, so it can never catch up. New fleet.

And the implicit `else`: if `time <= stack[-1]`, the car catches the fleet ahead and is absorbed. **We simply don't push it** — no bookkeeping needed, because the fleet still arrives at the front car's (larger) time, which is already on the stack.

That "do nothing" branch is what makes this solution so short, and it's worth pointing out explicitly when explaining it.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return len(stack)
```

One entry per fleet.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:

        pairs = sorted(zip(position, speed), reverse=True)
        stack = []

        for pos, spd in pairs:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:
                stack.append(time)

        return len(stack)
```

</details>

**Trace it** — `target = 12`, `position = [10,8,0,5,3]`, `speed = [2,4,1,1,3]`:

Sorted descending by position: `(10,2), (8,4), (5,1), (3,3), (0,1)`

| Car | `time = (12−pos)/spd` | Fleet ahead (`stack[-1]`) | Decision | Stack |
|---|---|---|---|---|
| pos 10, spd 2 | (12−10)/2 = **1.0** | — (first) | new fleet | `[1.0]` |
| pos 8, spd 4 | (12−8)/4 = **1.0** | 1.0 | 1.0 ≤ 1.0 → **catches up** | `[1.0]` |
| pos 5, spd 1 | (12−5)/1 = **7.0** | 1.0 | 7.0 > 1.0 → new fleet | `[1.0, 7.0]` |
| pos 3, spd 3 | (12−3)/3 = **3.0** | 7.0 | 3.0 ≤ 7.0 → **catches up** | `[1.0, 7.0]` |
| pos 0, spd 1 | (12−0)/1 = **12.0** | 7.0 | 12.0 > 7.0 → new fleet | `[1.0, 7.0, 12.0]` |

Answer: **3** ✅

Row 2 is exactly the `<=` case the problem calls out — the car arrives at precisely the same moment and counts as part of the fleet. Row 4 shows a *faster* car (3.0 < 7.0) being absorbed: it catches the fleet ahead and is stuck behind it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated entirely by the sort.

| Step | Cost |
|---|---|
| `zip` + `sorted` | **O(n log n)** |
| The scan | O(n) — one iteration per car, O(1) each |
| `len(stack)` | O(1) |

O(n log n) + O(n) = **O(n log n)**.

**Can you avoid the sort?** No. The algorithm's correctness rests on processing cars in road order — a car's fate depends on the one immediately ahead, and you can't know which that is without ordering by position. Since positions are arbitrary integers up to 10⁶, comparison sorting is the general tool. (Counting sort over positions would be O(target) = O(10⁶) — technically linear in the position range, but worse here and not the expected answer.)

**Contrast with [Daily Temperatures](739-daily-temperatures.md):** that was O(n) because the array order was already the order it needed. Here the input arrives unordered, so you pay the sort. **The stack scan is O(n) in both**; the difference is entirely whether the input comes pre-ordered.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** as written; **O(1) auxiliary** if you use the counter version.

- `pairs` — the zipped, sorted list of n tuples → O(n).
- `stack` — one entry per fleet, up to n when no car ever catches another (e.g. speeds decreasing toward the back) → O(n).
- Python's `sorted` itself uses O(n) for Timsort.

**The O(1) version.** Since nothing is ever popped, the stack's only roles are *"what's the time of the fleet ahead"* (its top) and *"how many fleets"* (its length). Both collapse into two variables:

```python
fleets = 0
max_time = 0
for pos, spd in sorted(zip(position, speed), reverse=True):
    time = (target - pos) / spd
    if time > max_time:
        fleets += 1
        max_time = time
```

That's **O(1) auxiliary** beyond the sort. It also reveals what the algorithm really is: *count how many times a new running maximum appears in the time sequence* — the same running-extreme idea as [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md).

Worth volunteering: *"the stack is never popped, so it can be reduced to a counter and a running max."* It shows you understand the algorithm rather than pattern-matching it to the unit's title.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Simulating collisions is O(n²). Instead, for each car I compute the time it would take to reach the target unobstructed — `(target − position) / speed`. Since cars can't pass, a car's fate depends only on what's ahead, so I sort by position descending and process from the car nearest the target. Each car compares its time to the fleet immediately ahead: if its time is greater it's genuinely slower and can never catch up, so it starts a new fleet; if it's less than or equal, it catches up and gets absorbed — and I do nothing, because the fleet still arrives at the front car's time. The answer is the number of fleets started. O(n log n) for the sort, O(n) for the scan. Since I never pop, the stack reduces to a counter and a running maximum, giving O(1) extra space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort descending?" | **The question.** A car can be blocked by what's ahead but never affects it, so you must resolve the front car first — its time is final and unblockable. |
| "Why `<=` rather than `<`?" | The problem states a car arriving at the exact same moment joins the fleet. `<` would create a phantom extra fleet on ties. |
| "Do you need the stack at all?" | No — nothing is ever popped, so a counter plus a running max is equivalent and O(1) space. |
| "Floating point worries you?" | Compare cross-multiplied integers instead: `(target−p₁)·s₂ <= (target−p₂)·s₁`. Exact, no division. Good answer if pressed on precision. |
| "Cars moving in both directions, or able to pass?" | The whole model breaks — position order is no longer permanent, so the front-to-back argument fails. |
| "Return the fleet **sizes**, not just the count." | Count absorbed cars against the current fleet instead of discarding them. |
| "What if positions could tie?" | The constraints forbid it; you'd need a stated rule for which car is "ahead". Worth asking rather than assuming. |

**Traps:**

- **Sorting ascending.** Processes cars in the wrong order — you'd be deciding a car's fate before knowing what blocks it.
- **Sorting `position` and `speed` separately.** They desynchronize and every time is wrong. `zip` them first.
- **Using `<` instead of `<=`** — over-counts fleets when arrival times tie.
- **Integer division `//`** — truncates times and merges fleets that shouldn't merge.
- **Simulating the motion.** O(n²) and floating-point-fragile.
- **Updating the stack top when a car merges.** Nothing to update — the fleet keeps the front car's slower time, which is already correct.

**This same move shows up in:** [Daily Temperatures](739-daily-temperatures.md) (a stack resolving each item against the one ahead) · [Best Time to Buy and Sell Stock](121-best-time-to-buy-and-sell-stock.md) (counting running maxima in one pass) · [Merge Intervals](56-merge-intervals.md) (sort first so the property you need becomes adjacent) · [3Sum](15-3sum.md) (sorting to unlock a linear scan).

</details>

---
