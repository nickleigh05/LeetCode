# 912. Sort an Array

**Medium** · [LeetCode](https://leetcode.com/problems/sort-an-array/) · [Solution file (no hints)](../../problems/0500-0999/912.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums`, sort it in ascending order and return it. **Solve it without built-in sort functions**, in `O(n log n)` time and with the smallest space you can.

```
nums = [5, 2, 3, 1]          →  [1, 2, 3, 5]
nums = [5, 1, 1, 2, 0, 0]    →  [0, 0, 1, 1, 2, 5]
```

**Constraints:** `1 <= nums.length <= 5 * 10⁴` · `-5 * 10⁴ <= nums[i] <= 5 * 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "without built-in sort" | You must write the sort yourself. `sorted()` and `.sort()` are off the table |
| "`O(n log n)`" | The O(n²) sorts (bubble, insertion, selection) are out: at `n = 5 * 10⁴` that's 2.5 billion steps |
| "smallest space" | Prefer an in-place sort (heap sort, quicksort) over merge sort's O(n) buffer, *if* you can get one |
| values in `[-5*10⁴, 5*10⁴]` | A small range, which makes **counting sort** possible (O(n + range)) |
| duplicates present | Equal elements must all survive. Check your comparison for `<=` vs `<` |

This is the "implement a sort" interview question. The interviewer doesn't want a clever trick. They want to see you pick a standard O(n log n) algorithm and write it **correctly**.

**The reframe:** sorting a big array is hard; sorting an array of length 1 is free. Split the array in half, sort each half, and **merge** two sorted halves, which is a single linear pass.

🤔 **Before you open the next section:** given two sorted lists `[1, 4, 7]` and `[2, 3, 9]`, how would you build one sorted list using a pointer into each?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Stable? | Verdict |
|---|---|---|---|---|
| Bubble / insertion / selection sort | O(n²) | O(1) | varies | ❌ Too slow at `n = 5 * 10⁴` |
| Quicksort (random pivot) | O(n log n) avg, O(n²) worst | O(log n) | no | ⚠️ Fast in practice, but a bad pivot choice is a trap (and duplicates break naive versions) |
| Heap sort | O(n log n) always | O(1) | no | ✅ In-place and guaranteed, but the code is fiddlier |
| **Merge sort** | **O(n log n) always** | O(n) | **yes** | ✅ Simplest to get right, with no bad cases |
| Counting sort | O(n + range) | O(range) | yes | ✅ Fastest here (range ≈ 10⁵), but only valid because values are small |

**The decision: [merge sort](../algorithms/merge-sort.md).** It's guaranteed O(n log n) on every input, the logic is the cleanest of the three real contenders, and it's stable. Its O(n) buffer is the price.

If the interviewer pushes on space, offer [heap sort](../algorithms/heapsort.md) (O(1) space) or [counting sort](../algorithms/counting-sort.md) (when the value range is small). Quicksort needs care: see [quicksort](../algorithms/quicksort.md) for the pivot pitfalls.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def sortArray(self, nums: List[int]) -> List[int]:
    if len(nums) <= 1:
        return nums
```

**Base case.** An array of 0 or 1 elements is already sorted. Without this the recursion never stops.
→ [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md)

```python
    mid = len(nums) // 2
    left = self.sortArray(nums[:mid])
    right = self.sortArray(nums[mid:])
```

**Divide.** Cut at the middle and sort each half by calling ourselves. Each recursive call gets a half-sized problem, so the recursion is `log₂ n` levels deep. Trust that `left` and `right` come back sorted.
→ [list-slicing](../syntax/list-slicing.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    result = []
    i = j = 0
```

**Conquer, setup.** `result` collects the merged output. `i` points at the next unused element of `left`, `j` at the next unused element of `right`.
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
```

**The merge.** Compare the two front elements and take the smaller. Both halves are sorted, so the smaller front element is the smallest *remaining* element overall. Using `<=` (not `<`) takes the left one on ties, which keeps the sort **stable**.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

One half ran out. The other half's leftovers are already sorted and all at least as big as everything taken, so copy them over. Only one of these two lines will add anything.
→ [list-methods](../syntax/list-methods.md) · [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums

        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])

        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
```

</details>

**Trace it.** `nums = [5, 2, 3, 1]`:

| Step | Work |
|---|---|
| split | `[5, 2]` and `[3, 1]` |
| sort `[5, 2]` | split to `[5]`, `[2]`, then merge: `2 < 5`, take 2, then leftover 5 → `[2, 5]` |
| sort `[3, 1]` | merge `[3]`, `[1]` → `[1, 3]` |
| merge `[2, 5]` and `[1, 3]` | 1 vs 2 → take 1. 3 vs 2 → take 2. 3 vs 5 → take 3. Leftover 5 → `[1, 2, 3, 5]` ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n), on every input.**

- The array is halved until the pieces have size 1: **log₂ n levels**.
- At each level, the merges together touch every element once: **O(n) work per level**.
- log n levels × O(n) = **O(n log n)**.

For `n = 5 * 10⁴` that's roughly 800,000 steps, against 2.5 billion for an O(n²) sort.

Best, average and worst cases are all the same, which is merge sort's selling point over quicksort.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).** Each merge builds a new list, and the slices copy too. At any moment about `n` extra elements are alive, plus O(log n) recursion stack.

That is the cost of merge sort. Heap sort sorts in place in O(1) extra space, and counting sort trades space for speed (O(range)).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I need O(n log n), so no quadratic sorts. I'll use merge sort: split the array in half, sort each half recursively, then merge the two sorted halves with two pointers, always taking the smaller front element. Every level of recursion does O(n) merging across log n levels, so O(n log n) in every case, with O(n) extra space. If space matters I'd use heap sort for O(1) extra, and since the values are bounded I could also use counting sort in O(n + range)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it in place?" | [Heap sort](../algorithms/heapsort.md): build a max-heap, repeatedly swap the max to the end. O(n log n), O(1) space |
| "What about quicksort?" | Average O(n log n), in place, but O(n²) with a bad pivot. Pick a **random pivot** and use a 3-way partition so heavy duplicates don't hurt |
| "Faster than O(n log n)?" | Comparison sorts can't beat `n log n`. But with bounded values, [counting sort](../algorithms/counting-sort.md) is O(n + range), and [radix sort](../algorithms/radix-sort.md) works for larger ranges |
| "Is it stable?" | Yes, because of `<=` in the merge. Equal elements keep their original order |
| "Why is merge sort used for linked lists?" | Merging needs no random access and no extra buffer on a list. See [Sort List](148-sort-list.md) |

**Traps:**

- **`<` instead of `<=`** in the merge: still correct for sorting but not stable.
- **Missing base case**, or a base case of `len == 0` only, which recurses forever on a length-1 array.
- **Forgetting the leftover `extend` lines.** Elements silently disappear.
- **Quicksort with a first-element pivot** on an already sorted input: O(n²), and it can hit the recursion limit.

**This same move shows up in:** [Sort List](148-sort-list.md) (merge sort on a linked list) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the merge step on its own) · [Count of Smaller Numbers After Self](315-count-of-smaller-numbers-after-self.md) (counting during the merge) · [Reverse Pairs](493-reverse-pairs.md).

</details>

---
