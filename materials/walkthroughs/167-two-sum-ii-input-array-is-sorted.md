# 167. Two Sum II (Input Array Is Sorted)

**Medium** · [LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [Solution file (no hints)](../../problems/0001-0499/167.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**, find two numbers that add up to `target`.

Return their indices `[index1, index2]` as 1-based positions, where `index1 < index2`. Exactly one solution exists, and you may not use the same element twice.

**Your solution must use only constant extra space.**

```
numbers = [2,7,11,15], target = 9   →  [1,2]
numbers = [2,3,4],     target = 6   →  [1,3]
numbers = [-1,0],      target = -1  →  [1,2]
```

**Constraints:** `2 <= numbers.length <= 3·10⁴` · `-1000 <= numbers[i] <= 1000` · sorted non-decreasing · exactly one solution

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted** in non-decreasing order" | ⚠️ The gift. Sortedness is *information* — moving right always increases (or holds) the value, moving left always decreases |
| "**constant extra space**" | ⚠️ The constraint that rules out [Two Sum](1-two-sum.md)'s hash map. This is the same problem with the easy tool taken away |
| "**1-indexed**" | The answer is positions **+1**. A pure bookkeeping detail that costs people the submission |
| "exactly one solution" | No tie-breaking, no collecting. Return the moment you find it |
| "not the same element twice" | The two pointers must never land on the same index |
| "non-**decreasing**" | Duplicates are allowed (`[3,3]`). Your logic must not assume strict increase |

The question to sit with: **what does sortedness let you do that you couldn't before?**

Look at the two extremes — the smallest element and the largest. Their sum tells you something *decisive*:

- If `smallest + largest > target`, the sum is too big. The largest element is too large to pair with **anything** (it's already paired with the smallest possible partner), so it can be discarded entirely.
- If `smallest + largest < target`, symmetrically, the smallest element can't reach the target with **any** partner. Discard it.

Either way you eliminate one element per comparison — and you never have to look at it again.

🤔 **Before you open the next section:** if the sum of the two ends is too large, which pointer should move, and why is it safe to throw that element away forever?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Extra space | Verdict |
|---|---|---|---|---|
| Brute force | Every pair | O(n²) | O(1) | ❌ 9·10⁸ ops |
| Hash map | [Two Sum](1-two-sum.md)'s complement lookup | O(n) | **O(n)** | ❌ Violates the constant-space requirement |
| Binary search | For each `x`, binary-search for `target - x` | O(n log n) | O(1) | ⚠️ Correct, uses sortedness — but slower and more code |
| **Two pointers** | Converge from both ends | **O(n)** | **O(1)** | ✅ |

**The decision: two pointers converging from the ends.**

`left` at the smallest element, `right` at the largest. Compare their sum to the target and move the pointer that can fix the discrepancy:

- **sum too small** → `left += 1` (the only way to get a bigger sum)
- **sum too big** → `right -= 1` (the only way to get a smaller sum)
- **equal** → done

**Why it's correct, not just plausible.** This is worth being able to argue. When `numbers[left] + numbers[right] < target`, consider `numbers[left]`: it's currently paired with the **largest** available element, and that's still not enough. Every other partner is smaller, so no pair involving `numbers[left]` can ever reach the target. Discarding it eliminates n−1 pairs in one step without ever examining them. The mirror argument holds for `right`. Since the true answer is never discarded, the pointers must eventually land on it.

**Why not the hash map?** It's the right answer to [Two Sum](1-two-sum.md) — where the array is unsorted and there's no structure to exploit. Here the problem explicitly bans it, and the ban is instructive: **structure in the input can substitute for memory.** Sortedness is doing the job the hash map did.

**Why not binary search?** It's a legitimate O(n log n) and worth naming. But two pointers gets O(n) with less code — the extra log factor buys nothing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(numbers) - 1
```

Pointers at the smallest and largest elements. Note these are **0-based** indices — the 1-based conversion happens only at the return.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while left < right:
```

Run while there are still two *distinct* elements. **`<` not `<=`** is what enforces "not the same element twice" — if they ever met, you'd be pairing an element with itself.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if numbers[left] + numbers[right] < target:
        left += 1
```

Sum too small. The only way to increase it is a larger element, and sortedness says that's to the **right**. `numbers[left]` is now permanently eliminated — it was already paired with the largest possible partner and fell short.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    elif numbers[left] + numbers[right] > target:
        right -= 1
```

Sum too big. Mirror image: shrink it by moving `right` left. `numbers[right]` is eliminated for the same reason in reverse.
→ [elif-else](../syntax/elif-else.md)

```python
    else:
        return [left + 1, right + 1]
```

Exact match. **The `+ 1` on each is the 1-indexing** the problem demands — forget it and every answer is off by one. `left < right` guarantees the required `index1 < index2` ordering automatically.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:

        left = 0
        right = len(numbers) - 1

        while left < right:
            if numbers[left] + numbers[right] < target:
                left += 1
            elif numbers[left] + numbers[right] > target:
                right -= 1
            else:
                return [left + 1, right + 1]
```

</details>

**Trace it** — `numbers = [2, 3, 4, 8, 11]`, `target = 11`:

| `left` | `right` | Sum | vs target | Move |
|---|---|---|---|---|
| 0 (2) | 4 (11) | 13 | too big | `right` → 3 |
| 0 (2) | 3 (8) | 10 | too small | `left` → 1 |
| 1 (3) | 3 (8) | 11 | **match** | `return [2, 4]` |

Watch what happened: the pair `(2, 8)` was too small, so **every** pair starting with 2 was eliminated at once — `(2,3)` and `(2,4)` were never examined, because both are smaller still.

There's no `return` after the loop since the problem guarantees a solution. Production code would return `[]`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every iteration does O(1) work and then moves exactly one pointer — `left` right or `right` left. The gap between them starts at n−1 and **strictly shrinks by 1 each iteration**, so the loop runs at most n−1 times.

**O(n)** total.

**The intuition worth carrying:** each comparison eliminates an entire *element*, and with it every pair that element could have formed. That's why n comparisons suffice to search what is nominally an O(n²) space of pairs. The brute force examines pairs; two pointers examines elements.

**Compared to the alternatives:**

| | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Hash map | O(n) | O(n) |
| Binary search | O(n log n) | O(1) |
| **Two pointers** | **O(n)** | **O(1)** |

Two pointers is best in both columns — but *only* because the array is sorted. Take that away and the hash map is back on top.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integer variables, and that's the whole requirement satisfied.

The instructive comparison is with [Two Sum](1-two-sum.md), which needed O(n) for its hash map. Same question, different space:

> **Sortedness replaced the memory.** The hash map existed to remember which values had been seen; the sorted order means you don't need to remember anything, because position already tells you how values compare.

That's a general and genuinely useful idea: **structure in the input can substitute for auxiliary storage.** Sorted order, monotonicity, and bounded ranges all buy you the same kind of leverage. When an interviewer imposes a constant-space constraint, the first question to ask is *what structure does the input have that I'm not exploiting yet?*

**The caveat:** if you had to sort an unsorted array yourself, you'd pay O(n log n) time and, depending on the sort, O(n) or O(log n) space — at which point the hash map is simply better. This solution is only free because the array **arrives** sorted.

</details>

<details>
<summary><b>6 · Talk it through</b> — thinking out loud & follow-ups</summary>

**Say this out loud:**

> "The array is sorted and I'm restricted to constant space, so the hash map from Two Sum is out — but sortedness gives me something better. I'll put a pointer at each end. If the sum is too small, the left element paired with the *largest* available partner still falls short, so no pair with it can ever work — I discard it and move left inward. If the sum is too big, the same argument discards the right element. Each comparison eliminates one element, so the pointers meet in at most n steps. O(n) time, O(1) space. And the indices are 1-based, so I add one to each on the way out."

That middle sentence is the whole interview. Don't just say *"move the pointer"* — say **why discarding is safe**.

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if it *weren't* sorted?" | Back to the hash map — O(n) time, O(n) space. Or sort first at O(n log n), but then you'd need to carry original indices. See [Two Sum](1-two-sum.md). |
| "Prove the two-pointer approach can't miss the answer." | The argument above: whenever you discard an element, it's because it fails against its best possible partner, so no pair containing it is viable. The true pair is never discarded, and the window always shrinks. |
| "Three numbers summing to a target?" | Sort, fix one element, two-pointer the rest — O(n²). That's [3Sum](15-3sum.md). |
| "Find *all* pairs, not just one?" | Don't return on a match — record it, then move **both** pointers and skip duplicate values on each side. |
| "What if no solution exists?" | The loop exits when the pointers meet; return `[]`. The guarantee is a convenience of this problem, not of the algorithm. |
| "Can you use binary search instead?" | Yes — for each element, binary-search its complement. O(n log n), still O(1) space. Slower, more code. |

**Traps:**

- **Returning 0-based indices.** The single most common wrong submission here. The problem says 1-indexed.
- **`while left <= right`** — allows the pointers to coincide, which pairs an element with itself.
- **Moving the wrong pointer.** Sum too big means shrink, i.e. move `right` *down*. Getting this backwards makes the sum diverge and the loop terminate empty.
- **Moving both pointers on a mismatch.** You can skip past the answer entirely.
- **Reusing [Two Sum](1-two-sum.md)'s hash map out of habit** — it works, it's O(n), and it fails the stated space requirement.

**This same move shows up in:** [Valid Palindrome](125-valid-palindrome.md) (converging pointers, symmetric comparison) · [3Sum](15-3sum.md) (this exact routine used as an inner loop) · [Container With Most Water](11-container-with-most-water.md) (converge and discard the limiting side) · [Trapping Rain Water](42-trapping-rain-water.md) (converge while tracking running maxima).

</details>

---
