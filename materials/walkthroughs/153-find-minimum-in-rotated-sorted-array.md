# 153. Find Minimum in Rotated Sorted Array

**Medium** · [LeetCode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/153.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Suppose an array sorted in ascending order with **unique** elements is **rotated** between 1 and n times. For example, `[0,1,2,4,5,6,7]` might become `[4,5,6,7,0,1,2]`.

Given the rotated array, return the **minimum element**. You must write an algorithm that runs in **O(log n)**.

```
nums = [3,4,5,1,2]       →  1
nums = [4,5,6,7,0,1,2]   →  0
nums = [11,13,15,17]     →  11    (rotated n times = back to sorted)
```

**Constraints:** `1 <= n <= 5000` · `-5000 <= nums[i] <= 5000` · all values **unique**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**rotated**" | The array is two sorted runs stuck together, with one "cliff" where it drops |
| "find the **minimum**" | The minimum is exactly the element **at the cliff** — the start of the second run |
| "**O(log n)**" | ⚠️ Rules out scanning. You must halve, despite the array not being fully sorted |
| "**unique** elements" | No duplicates. This matters enormously — see the follow-ups; with duplicates O(log n) is impossible |
| "rotated **1 to n** times" | ⚠️ A full rotation returns it to sorted order, so **the un-rotated case is legal input** and must work |

Picture the shape:

```
nums = [4,5,6,7,0,1,2]

  7 ●
 6 ●│
5 ●  │
4●   │
     └──● 0 ● 1 ● 2       ← the minimum sits at the bottom of the cliff
      cliff
```

Two ascending runs. Everything in the left run is **greater** than everything in the right run — that's what rotation guarantees.

**Why plain [704](704-binary-search.md) doesn't apply:** there's no target to compare against, and the array isn't globally sorted so `nums[mid] < nums[mid+1]` tells you nothing about direction on its own.

**But there's still a monotonic property to exploit.** Compare `nums[mid]` against the **last** element, `nums[right]`:

- **`nums[mid] > nums[right]`** → `mid` is in the *left* (higher) run. The cliff must be to its **right**.
- **`nums[mid] <= nums[right]`** → `mid` is in the *right* (lower) run, or the array is already sorted. The minimum is at `mid` **or to its left**.

One comparison, half the array gone. That's binary search on a *rotated* array.

🤔 **Before you open the next section:** why compare against `nums[right]` rather than `nums[left]`? Try both on the already-sorted `[1,2,3]` and see which one misleads you.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | `min(nums)` | O(n) | ❌ Violates the stated O(log n) |
| Find where `nums[i] > nums[i+1]` by scanning | The cliff | O(n) | ❌ Same problem |
| Compare `nums[mid]` to **`nums[left]`** | Decide which run `mid` is in | O(log n) | ⚠️ Works, but needs an extra case for the already-sorted array |
| **Compare `nums[mid]` to `nums[right]`** | Same idea, no special case | **O(log n)** | ✅ |

**The decision: binary search comparing `nums[mid]` against `nums[right]`.**

**Why `nums[right]` and not `nums[left]` — the detail that makes this clean.**

Try `nums = [1,2,3]` (a legal, fully-rotated input) with `mid = 1`:

- **Against `nums[left]`:** `nums[1]=2 > nums[0]=1`. That *looks* like "mid is in the left run, so go right" — which is **wrong**; the minimum is at index 0. You'd need an extra check for "is this segment already sorted?"
- **Against `nums[right]`:** `nums[1]=2 <= nums[2]=3` → "minimum is at mid or left" → `right = mid`. **Correct**, no special case.

Comparing against the right end handles the un-rotated array as an ordinary case rather than an exception. **Fewer branches means fewer bugs** — worth stating out loud, because interviewers notice when you can justify a choice like this.

**The other structural change: `while left < right`, and `right = mid`.**

This is a **convergence** search, not a *find-this-value* search. You're not testing whether `mid` is the answer — you're narrowing until one candidate remains.

- **`left < right`** — stop when exactly one element remains; that element *is* the answer.
- **`right = mid`, not `mid - 1`** — when `nums[mid] <= nums[right]`, `mid` could itself *be* the minimum, so you must not discard it.
- **`left = mid + 1`** is still safe, because `nums[mid] > nums[right]` proves `mid` is in the higher run and definitively not the minimum.

**This asymmetry is the whole problem**, and it's where people get it wrong: one branch excludes the midpoint, the other keeps it. That's also why `while left <= right` would infinite-loop here — with `right = mid` and `left == right`, nothing would ever change.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

The full array. Both are valid indices, and `nums[right]` — the comparison anchor — is the last element.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while left < right:
```

**`<`, not `<=`** — the departure from [704](704-binary-search.md).

This is a convergence loop: it runs while **two or more** candidates remain, and stops when `left == right` — at which point that single surviving element is the answer. With `<=` and `right = mid`, a one-element range would loop forever.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    mid = left + (right - left) // 2
```

The overflow-safe midpoint form. Mathematically identical to `(left + right) // 2` in Python — where ints are arbitrary-precision — but it's the idiom that transfers to C/Java, where `left + right` can overflow. Costs nothing to write it this way.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if nums[mid] > nums[right]:
        left = mid + 1
```

**`mid` is in the higher (left) run.** Since it's greater than the last element, the cliff — and therefore the minimum — must be strictly to its right.

`mid + 1` safely excludes `mid`: it's provably *not* the minimum, because something smaller (`nums[right]`) exists.
→ [if-return](../syntax/if-return.md)

```python
    else:
        right = mid
```

**`nums[mid] <= nums[right]`** — `mid` is in the lower (right) run, or this segment is already sorted. Either way the minimum is at `mid` **or to its left**.

**`right = mid`, not `mid - 1`** — `mid` might *be* the minimum, so it stays in the range. Getting this wrong loses the answer whenever the minimum lands exactly on a midpoint.
→ [elif-else](../syntax/elif-else.md)

```python
return nums[left]
```

The loop ended with `left == right`, so both point at the single surviving candidate — the minimum. (`nums[right]` would be identical.)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:

        left = 0
        right = len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```

</details>

**Trace it** — `nums = [4,5,6,7,0,1,2]`:

| `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Compare | Action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | 2 | 7 > 2 → higher run | `left = 4` |
| 4 | 6 | 5 | 1 | 2 | 1 ≤ 2 → lower run | `right = 5` |
| 4 | 5 | 4 | **0** | 1 | 0 ≤ 1 → lower run | `right = 4` |
| 4 | 4 | — | | | `left == right`, exit | `return nums[4] = 0` ✅ |

**And the already-sorted case** — `nums = [11,13,15,17]`:

| `left` | `right` | `mid` | `nums[mid]` vs `nums[right]` | Action |
|---|---|---|---|---|
| 0 | 3 | 1 | 13 ≤ 17 | `right = 1` |
| 0 | 1 | 0 | 11 ≤ 13 | `right = 0` |
| 0 | 0 | — | exit | `return 11` ✅ |

No special-casing needed — comparing against the right end handles it naturally. Row 3 of the first trace is also worth noting: `right = mid` kept index 4, which *was* the answer.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each iteration eliminates roughly half the range:

- `left = mid + 1` discards the left half **plus** the midpoint.
- `right = mid` discards the right half, keeping the midpoint.

The second branch shrinks by *half minus one* rather than a clean half — but the range still strictly decreases every iteration (since `mid < right` whenever `left < right`), so termination is guaranteed and the bound is still log₂ n.

At n = 5000, that's about **13 iterations**.

**Why the array can be searched despite not being sorted.** Binary search needs a **monotonic decision rule**, not sortedness — the same lesson as [Koko Eating Bananas](875-koko-eating-bananas.md). Here the rule is *"is `mid` in the higher run or the lower run?"*, and comparing to `nums[right]` answers it in O(1). Sortedness was never the requirement; it was one way of getting a reliable comparison.

**There's no early exit** — you can't recognize the minimum by looking at it in isolation, so the loop always runs to convergence.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers, and the array is read-only.

**The space story is identical across all of Unit 05**, which is the point of the unit: binary search never needs auxiliary memory, because it stores *boundaries* rather than *data*. Two integers describe a range of any size.

Compare the two families you've now seen:

| Speedup source | Example | Space |
|---|---|---|
| Remember what you've seen | [Two Sum](1-two-sum.md) hash map | **O(n)** |
| Eliminate what can't win | Two pointers, **binary search** | **O(1)** |

Binary search is the most extreme version of elimination — a *single comparison* discards half the remaining candidates, and it costs two variables to track.

**Recursive alternative:** O(log n) stack space, no benefit. Iterative wins.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A rotated sorted array is two ascending runs, with the minimum at the cliff between them — and everything in the left run is bigger than everything in the right run. So I compare the midpoint against the *last* element: if `nums[mid] > nums[right]`, mid is in the higher run and the minimum must be strictly to its right; otherwise mid is in the lower run and the minimum is at mid or to its left. I compare against the right end rather than the left because it handles a fully-rotated, already-sorted array without a special case. It's a convergence search — `while left < right`, and crucially `right = mid` rather than `mid - 1`, because mid might itself be the minimum. When they meet, that element is the answer. O(log n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why compare to `nums[right]` and not `nums[left]`?" | **The question.** On an already-sorted array, `nums[mid] > nums[left]` misleads you rightward. Comparing to the right end has no such exception. |
| "Why `right = mid` instead of `mid - 1`?" | Mid might *be* the minimum. `mid - 1` would discard the answer. The other branch can use `mid + 1` because mid is provably not the minimum there. |
| "What if there are **duplicates**?" | ⚠️ `nums[mid] == nums[right]` becomes ambiguous — you can't tell which run you're in, so you shrink by one (`right -= 1`) and the **worst case degrades to O(n)** (e.g. `[1,1,1,0,1]`). That's LeetCode 154, and O(log n) is provably impossible. |
| "Find the **rotation count**?" | It's the *index* of the minimum — return `left` instead of `nums[left]`. |
| "Now search for a target in the rotated array." | Two ways: find the pivot first then binary search the right run, or handle it in one pass — that's [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md). |
| "Find the **maximum**?" | It's the element just before the minimum: `nums[left - 1]`, or `nums[-1]` if the array isn't rotated. |

**Traps:**

- **`while left <= right` with `right = mid`.** Infinite loop — when `left == right`, `mid == left` and nothing changes. The loop condition and the update must match.
- **`right = mid - 1`.** Skips over the minimum when it lands on a midpoint.
- **Comparing to `nums[left]`** without the extra sorted-segment check — wrong on already-sorted input.
- **`return nums[mid]`** after the loop. `mid` is stale; the answer is at `left`.
- **Assuming the array is genuinely rotated.** A full rotation is legal and looks sorted; the code must handle it.
- **Applying this to arrays with duplicates** and claiming O(log n).

**This same move shows up in:** [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md) (same structure, plus a target) · [Binary Search](704-binary-search.md) (the base template this modifies) · [Koko Eating Bananas](875-koko-eating-bananas.md) (monotonic decision rule without sortedness) · [Find Peak Element](../learning/05-binary-search.md) (halving on an unsorted array using a local comparison).

</details>

---
