# 632. Smallest Range Covering Elements from K Lists

**Hard** · [LeetCode](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) · [Solution file (no hints)](../../problems/0500-0999/632.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

You have `k` lists of integers, each **sorted in non-decreasing order**. Find the **smallest range** `[a, b]` that includes **at least one number from each list**.

Range `[a, b]` is smaller than `[c, d]` if `b − a < d − c`, or if `b − a == d − c` and `a < c`.

```
nums = [[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]
→ [20, 24]      (24 from list 1, 20 from list 2, 22 from list 3)

nums = [[1,2,3], [1,2,3], [1,2,3]]
→ [1, 1]
```

**Constraints:** `1 <= k <= 3500` · `1 <= nums[i].length <= 50` · `-10⁵ <= nums[i][j] <= 10⁵` · each list is sorted

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| at least one number **from each list** | A valid range must cover one representative per list |
| **smallest** range | Minimise `max − min` across the chosen representatives |
| ties → smaller start | Only replace the best range on a **strictly** smaller width, since you meet starts in increasing order |
| each list **sorted** | You can walk each list forward with a pointer, like in a merge |
| k up to 3500, total up to 1.75·10⁵ | Trying every combination is impossible. You need about O(N log k) |

**The idea: pick one number from each list, then improve.** Start with the **first** element of every list. That's a valid choice (one per list), and its range runs from the smallest of them to the largest.

**How to improve it.** The range is `[min, max]`. To make it narrower, you must either raise the min or lower the max. You can't lower the max: every list's pointer starts at its smallest element, and lists only increase. So the only move is to **raise the min**: drop the smallest chosen number and replace it with the **next number from the same list**. That keeps one representative per list.

Repeat. Each step, record the range if it's the best so far. Stop when the list that holds the minimum runs out, because then there's no way to raise the min without losing that list entirely.

**What you need quickly at each step:** the current **minimum** (and which list it's from). That's a min-heap. The **maximum** only ever goes up, because you only add larger numbers, so a single variable tracks it.

🤔 **Before you open the next section:** in the first example, the starting picks are `4, 0, 5`. Which one gets replaced first, and by what?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every pair `(a, b)` | Check each candidate range covers all lists | O(N² · k) | O(1) | ❌ |
| Merge everything + sliding window | Sort all `(value, list)` pairs, then a window covering all k lists | O(N log N) | O(N) | ✅ Works, more memory |
| **Min-heap of one pointer per list** | Pop the min, push the next from its list, track the max | **O(N log k)** | **O(k)** | ✅ |

Here N is the total number of elements.

**The decision: a [heap](../data-structures/heap.md) holding exactly one element from each list.**

It's the same mechanism as [Merge k Sorted Lists](23-merge-k-sorted-lists.md): the heap always holds the current front of each list, and you repeatedly take the smallest. The difference is that you're not building merged output. You're watching the spread between the heap's smallest and the largest value seen.

**The sliding-window alternative.** Flatten everything into `(value, list_id)` pairs and sort. Then find the narrowest window that includes at least one pair from every list, the same technique as [Minimum Window Substring](76-minimum-window-substring.md). It's valid, but it uses O(N) memory against the heap's O(k).

**Heap entries are tuples.** Push `(value, list_index, element_index)`. Python compares tuples element by element, so the smallest value comes out first. The other two fields say where to find the next element.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
heap = []
current_max = float('-inf')
for i, lst in enumerate(nums):
    heapq.heappush(heap, (lst[0], i, 0))
    current_max = max(current_max, lst[0])
```

**The starting picks: the first element of every list.** Each heap entry says "value, from list `i`, at position 0." `current_max` tracks the largest pick. Starting at `-inf` means any real number replaces it.
→ [heapq-module](../syntax/heapq-module.md) · [float-inf](../syntax/float-inf.md) · [enumerate](../syntax/enumerate.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
best = [heap[0][0], current_max]
```

**The first valid range.** `heap[0]` is always the heap's smallest entry, without popping it.
→ [list-basics](../syntax/list-basics.md)

```python
while True:
    val, i, j = heapq.heappop(heap)
    if current_max - val < best[1] - best[0]:
        best = [val, current_max]
```

**Check the current range, then drop the minimum.** Before removing it, `[val, current_max]` is the range covering all current picks. Replace `best` only if it's **strictly** narrower. On a tie, the earlier range has the smaller start, because `val` only increases, so it wins.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if j + 1 == len(nums[i]):
        return best
```

**That list has run out.** Without a replacement from list `i`, any further range would leave that list uncovered. Every remaining option is worse, so return the best seen.
→ [if-return](../syntax/if-return.md)

```python
    nxt = nums[i][j + 1]
    heapq.heappush(heap, (nxt, i, j + 1))
    current_max = max(current_max, nxt)
```

**Replace the minimum with the next number from the same list.** There's still one pick per list. The new number might be the new maximum. The maximum never goes down, so updating it on each push is enough.
→ [heapq-module](../syntax/heapq-module.md) · [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = []
        current_max = float('-inf')
        for i, lst in enumerate(nums):
            heapq.heappush(heap, (lst[0], i, 0))
            current_max = max(current_max, lst[0])

        best = [heap[0][0], current_max]

        while True:
            val, i, j = heapq.heappop(heap)
            if current_max - val < best[1] - best[0]:
                best = [val, current_max]

            if j + 1 == len(nums[i]):
                return best

            nxt = nums[i][j + 1]
            heapq.heappush(heap, (nxt, i, j + 1))
            current_max = max(current_max, nxt)
```

</details>

**Trace it.** `nums = [[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]`:

| Picks (list 0, 1, 2) | Min (popped) | Max | Range | Best | Replace with |
|---|---|---|---|---|---|
| 4, **0**, 5 | 0 (L1) | 5 | [0, 5] = 5 | [0, 5] | 9 from L1 |
| **4**, 9, 5 | 4 (L0) | 9 | [4, 9] = 5 | — (tie) | 10 from L0 |
| 10, 9, **5** | 5 (L2) | 10 | [5, 10] = 5 | — | 18 from L2 |
| 10, **9**, 18 | 9 (L1) | 18 | [9, 18] = 9 | — | 12 from L1 |
| **10**, 12, 18 | 10 (L0) | 18 | 8 | — | 15 from L0 |
| 15, **12**, 18 | 12 (L1) | 18 | 6 | — | 20 from L1 |
| **15**, 20, 18 | 15 (L0) | 20 | 5 | — | 24 from L0 |
| 24, 20, **18** | 18 (L2) | 24 | 6 | — | 22 from L2 |
| 24, **20**, 22 | 20 (L1) | 24 | [20, 24] = **4** | **[20, 24]** | L1 is out → **stop** |

Answer **[20, 24]** ✅. The earlier width-5 ranges never replaced `[0, 5]` because a tie isn't strictly smaller, which matches the rule "on a tie, the smaller start wins."

</details>

<details>
<summary><b>4 · Time complexity</b> — O(N log k)</summary>

**O(N log k)**, where N is the total number of elements and k the number of lists.

- Building the heap: k pushes, O(k log k).
- Each loop iteration pops one entry and pushes one, both O(log k), because the heap holds exactly k entries.
- Each element is pushed at most once, so there are at most N iterations.

That's O(N log k) in total. With N ≤ 1.75·10⁵ and k ≤ 3500, it's about 2·10⁶ operations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k).** The heap holds exactly one entry per list at all times. Everything else is a few variables.

The sliding-window alternative needs O(N) to hold the merged list.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I keep one pick from each list, starting with every list's first element. The range is from the smallest pick to the largest. The only way to narrow it is to raise the smallest pick, so I pop the minimum from a min-heap and push the next element from the same list, tracking the maximum in a variable since it only grows. Each step I record the range if it's strictly narrower than the best. When the minimum's list runs out, I stop, because any later range would miss that list. The heap always holds k entries, so it's O(N log k) time and O(k) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why stop when one list runs out?" | Every remaining range would need to drop that list's last pick without a replacement, so it couldn't cover every list. |
| "Why is tracking the max in one variable enough?" | You only ever push numbers that are at least as large as the one popped, so the max never decreases. |
| "Why strict `<` when updating the best?" | The popped value only increases, so an earlier range of equal width already has the smaller start. |
| "Sliding-window version?" | Merge all `(value, list)` pairs, sort, and find the narrowest window covering all k lists, like [Minimum Window Substring](76-minimum-window-substring.md). |
| "Lists not sorted?" | Sort each list first, O(N log N) in total. Then run the same algorithm. |

**Traps:**

- **Moving forward in the list with the max.** That only widens the range. Always raise the **min**.
- **Using `<=` when updating the best.** On ties, that keeps the range with the **larger** start.
- **Continuing after a list runs out.** Ranges beyond that point don't cover every list.
- **Recomputing the max from the heap each step.** O(k) per step. A single variable is enough.
- **Pushing values without their list and position.** You can't find "the next element from the same list."

**This same move shows up in:** [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (a heap holding one front element per list) · [Minimum Window Substring](76-minimum-window-substring.md) (the narrowest window covering every required item) · [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) (LeetCode 373, a heap advancing pointers through sorted lists) · [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) (LeetCode 378, the same heap-of-row-fronts pattern).

</details>

---
