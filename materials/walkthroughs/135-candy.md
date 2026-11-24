# 135. Candy

**Hard** · [LeetCode](https://leetcode.com/problems/candy/) · [Solution file (no hints)](../../problems/0001-0499/135.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

`n` children stand in a line, each with a rating `ratings[i]`. Give every child **at least one candy**, and any child with a **higher rating than an immediate neighbour must get more candies than that neighbour**. Return the **minimum total** number of candies.

```
ratings = [1, 0, 2]   →  5     (2, 1, 2)
ratings = [1, 2, 2]   →  4     (1, 2, 1)   equal ratings don't force more candy
```

**Constraints:** `1 <= n <= 2 * 10⁴` · `0 <= ratings[i] <= 2 * 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "at least one candy" | Everyone starts at 1 |
| "higher rating than a neighbour → more candy" | A constraint with **both** neighbours: left and right |
| "minimum total" | Give each child **exactly what the constraints force**, nothing extra |
| equal ratings | No constraint between them |

Two separate constraints per child: **left** (`if ratings[i] > ratings[i-1]`, then `candy[i] > candy[i-1]`) and **right** (`if ratings[i] > ratings[i+1]`, then `candy[i] > candy[i+1]`). Handling both in one pass is the trap: fixing the left neighbour can break the right one.

**Split them.** Satisfy each direction in its own pass:

1. **Left to right:** make sure every child with a higher rating than the **left** neighbour has more than that neighbour.
2. **Right to left:** make sure every child with a higher rating than the **right** neighbour has more than that neighbour, **without lowering** what the first pass gave. Take the `max` of the two requirements.

Each pass is easy because it has just one direction to worry about. The `max` merges them: a child gets the larger of "what the left side demands" and "what the right side demands".

🤔 **Before you open the next section:** for `[1, 3, 2, 1]`, what does the first pass give, and what does the second pass raise?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Repeat "fix violations" until stable | O(n²) worst | O(n) | ❌ Slow on long slopes |
| **Two passes with a `candies` array** | **O(n)** | O(n) | ✅ |
| One pass tracking slope lengths (up / down / peak) | O(n) | O(1) | ✅ Clever, but easy to get wrong |
| Sort by rating, assign in order | O(n log n) | O(n) | ⚠️ Works, with extra cost |

**The decision: two [greedy](../learning/16-greedy.md) passes.** The first pass fixes left-neighbour constraints. The second pass fixes right-neighbour constraints and keeps `max` with the existing value, so earlier work is never undone. Greedy works because each child's minimum is determined by the **longest strictly increasing run** that ends at, or starts from, them: the left pass measures one, the right pass measures the other.

The O(1)-space slope version is worth naming as the follow-up.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(ratings)
candies = [1] * n
```

Everyone gets the mandatory minimum of one candy.
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(1, n):
    if ratings[i] > ratings[i - 1]:
        candies[i] = candies[i - 1] + 1
```

**Left to right.** A child rated above the **left** neighbour must have one more than them. Going in order means `candies[i-1]` is already final with respect to *its* left. An equal or lower rating needs nothing here and stays at 1.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
for i in range(n - 2, -1, -1):
    if ratings[i] > ratings[i + 1]:
        candies[i] = max(candies[i], candies[i + 1] + 1)
```

**Right to left.** A child rated above the **right** neighbour must have more than them. Going backwards means `candies[i+1]` is already final for its right side. Use `max` so a child who already needed *more* from the left pass keeps it: the two requirements combine as "whichever is larger".
→ [min-max-key](../syntax/min-max-key.md) · [range-function](../syntax/range-function.md)

```python
return sum(candies)
```

Every constraint is satisfied and nothing extra was given.
→ [for-loop](../syntax/for-loop.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        candies = [1] * n

        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)
```

</details>

**Trace it.** `ratings = [1, 3, 2, 1]`:

| Index | ratings | After left pass | After right pass |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | 3 | 2 (3 > 1) | `max(2, candies[2]+1 = 2+1)` = **3** (3 > 2) |
| 2 | 2 | 1 | `max(1, candies[3]+1 = 2)` = **2** (2 > 1) |
| 3 | 1 | 1 | 1 |

Total `1 + 3 + 2 + 1 = 7` ✅. The peak needed 3: one more than its **right** neighbour's 2, a fact only the second pass could see.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** two passes and a sum, `3n` steps in total.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the `candies` array. A one-pass slope-counting solution gets O(1).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each child has two constraints, one against the left neighbour and one against the right, and handling both at once is where people go wrong. So I split them. Start everyone at 1. A left-to-right pass makes any child rated above their left neighbour have one more candy than that neighbour. A right-to-left pass does the same against the right neighbour, taking the max with what's already there so I never undo the first pass. Summing gives the minimum, in O(n) time and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | Walk the array tracking the length of the current rising run and falling run. At each peak, the candies are `max(up, down)` for it, plus triangular sums for the slopes |
| "Why `max` in the second pass?" | A child at a peak needs one more than **both** neighbours. The first pass satisfied the left one, the second must not lower it |
| "Equal ratings?" | No constraint, so the child may drop back to 1 |
| "Circular line?" | Break the circle at a minimum-rated child, or run the passes twice around |
| "Why is greedy optimal?" | Each candy count is exactly the longest strictly increasing run into the child from either side: the minimum any valid assignment needs |

**Traps:**

- **A single left-to-right pass.** It misses cases like `[1, 2, 3, 1, 0]`'s descent.
- **Overwriting instead of `max` in the second pass.**
- **Treating equal ratings as needing more candy.** They don't.
- **Forgetting everyone starts at 1,** not 0.

**This same move shows up in:** [Product of Array Except Self](238-product-of-array-except-self.md) (left pass, right pass, combine) · [Trapping Rain Water](42-trapping-rain-water.md) (left max and right max) · [Daily Temperatures](739-daily-temperatures.md).

</details>

---
