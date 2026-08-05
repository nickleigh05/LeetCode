# 347. Top K Frequent Elements

**Medium** · [LeetCode](https://leetcode.com/problems/top-k-frequent-elements/) · [Solution file (no hints)](../../problems/0001-0499/347.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

```
nums = [1,1,1,2,2,3], k = 2  →  [1,2]
nums = [1],           k = 1  →  [1]
```

**Constraints:** `1 <= nums.length <= 10⁵` · `k` is in the range `[1, number of distinct elements]` · the answer is **guaranteed unique** · **follow-up: better than O(n log n)?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**most frequent**" | Two distinct jobs: **count** the elements, then **rank** by those counts. Solve them separately |
| "return the **k** most" | A partial ordering. You need the top k, *not* a fully sorted list |
| "in **any order**" | No ordering work on the output. Pure selection |
| "answer is guaranteed unique" | No ties to break at the boundary — one less edge case to handle |
| "**better than O(n log n)**?" | The problem is pointing straight at the sort and telling you to beat it. That's the actual challenge |
| n up to 10⁵ | Counting is trivially fine; the question is entirely about the ranking step |

The part worth staring at: after counting, **what values can a frequency take?** With n elements, any frequency is an integer between 1 and n. That's a small, bounded, integer range — and whenever you're sorting *bounded integers*, the O(n log n) barrier doesn't apply, because that barrier only holds for comparison-based sorting.

🤔 **Before you open the next section:** if you must rank items by a value that's guaranteed to be an integer between 1 and n, how could you order them **without ever comparing two items**?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Counting is settled — a [hash map](../data-structures/hashmap.md), same as [Valid Anagram](242-valid-anagram.md). **The real decision is how to extract the top k from those counts.**

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Sort by count | `sorted(count, key=count.get)`, take the last k | O(n log n) | ⚠️ Correct, but it's exactly what the follow-up asks you to beat |
| Max-heap | Heapify all counts, pop k times | O(n + k log n) | ⚠️ Good, and the right answer if k is tiny |
| Min-heap of size k | Keep only the k best seen so far | O(n log k) | ⚠️ The streaming answer — best when n is huge and k is small |
| **Bucket sort** | Index an array **by frequency**, walk it downward | **O(n)** | ✅ Beats the follow-up outright |

**The decision: bucket sort by frequency.**

The unlock is that a frequency is an integer in `[1, n]`, so you can use the frequency itself **as an array index**. Build a list of n+1 buckets where `buckets[f]` holds every element that occurred exactly `f` times, then walk it from the high end and take the first k elements you meet. No comparisons, no sorting — **O(n)**.

That's the same principle behind [counting sort](../algorithms/counting-sort.md) and [bucket sort](../algorithms/bucket-sort.md): *comparison* sorting is bounded below by O(n log n), but if your keys are small bounded integers you can address them directly and skip comparing altogether.

**Why not the heap?** It's a genuinely good answer and worth naming out loud — and it's *the better answer* in the streaming variant, where you can't hold all n elements or don't know n in advance. Here you already have the whole array, and the bucket approach is strictly faster. Know both; volunteer the trade.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count = {}
for num in nums:
    count[num] = count.get(num, 0) + 1
```

Step one: the frequency map, `value → how many times it appeared`. Same counting idiom as [Valid Anagram](242-valid-anagram.md), and `.get(num, 0)` again handles the first sighting of a value without a `KeyError`.
→ [dict-basics](../syntax/dict-basics.md) · [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md)

```python
buckets = [[] for _ in range(len(nums) + 1)]
```

The trick, and it's all in the **indexing**: `buckets[f]` will hold every element whose frequency is exactly `f`. Length `n + 1` because a frequency can be as high as n (all elements identical) and index 0 goes unused — no element occurs zero times.

Each slot is its own list because several different values can share a frequency.

⚠️ Write `[[] for _ in range(...)]`, **not** `[[]] * (n+1)` — the second makes n+1 references to *one* list, so appending to any of them appends to all.
→ [list-comprehension](../syntax/list-comprehension.md) · [range-function](../syntax/range-function.md) · [nested-lists](../syntax/nested-lists.md)

```python
for num, freq in count.items():
    buckets[freq].append(num)
```

Scatter each distinct value into the bucket matching its frequency. `.items()` yields `(key, value)` pairs, unpacked straight into `num` and `freq`.

This is the step that replaces sorting: placing an item costs O(1), so placing all of them costs O(n) — and afterwards they're *already* grouped in frequency order, because array indices are ordered by construction.
→ [dict-methods](../syntax/dict-methods.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-methods](../syntax/list-methods.md)

```python
result = []
for freq in range(len(buckets) - 1, 0, -1):
```

Now walk the buckets **from the highest frequency downward** — that's the `-1` step. Stop at 1, not 0, since bucket 0 is always empty (`range` excludes its endpoint, so `0` is never visited).
→ [range-function](../syntax/range-function.md) · [list-basics](../syntax/list-basics.md)

```python
    for num in buckets[freq]:
        result.append(num)
        if len(result) == k:
            return result
```

Collect, and **return the moment you have k**. That early exit is what keeps this cheap: you never touch the remaining buckets. Most buckets are empty, and the inner loop simply skips them at no cost.
→ [list-methods](../syntax/list-methods.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        count = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1

        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)

        result = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result
```

</details>

**Trace it** — `nums = [1,1,1,2,2,3]`, `k = 2`:

```
count   = {1: 3, 2: 2, 3: 1}

buckets =  index:  0    1     2     3    4    5    6
                  [ ]  [3]   [2]   [1]  [ ]  [ ]  [ ]
                        ↑     ↑     ↑
                   freq 1  freq 2  freq 3

walk down from index 6 → 5, 4 empty · 3 holds [1] → result [1]
                      → 2 holds [2] → result [1,2] → len == k → return
```

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — which beats the O(n log n) the follow-up asks about.

| Step | Cost |
|---|---|
| Count frequencies | O(n) — one pass, O(1) per element |
| Allocate n+1 buckets | O(n) |
| Scatter into buckets | O(d), where d = distinct elements ≤ n |
| Walk buckets, collect k | O(n) — at most n+1 indices and n total elements across the lists |

Sequential steps **add**: O(n) + O(n) + O(d) + O(n) = **O(n)**.

**Why this dodges the O(n log n) sorting bound:** that lower bound applies only to *comparison-based* sorting. Bucket sort never compares two elements — it computes each item's position arithmetically from its key. That's legal precisely because frequencies are integers bounded by n, giving a small addressable index space.

**Where the cost hides:** the bucket walk is O(n) even when k = 1, because you may scan many empty buckets. That's fine, but it's why a size-k min-heap can win when n is enormous and k is tiny — O(n log k) with far less memory traffic.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

- The count map: one entry per **distinct** element → O(d), which is O(n) worst case (all elements different).
- The buckets: an n+1 slot array, plus the d values distributed across it → O(n).
- The result: O(k), and k ≤ d ≤ n.

Total **O(n)**. Unlike [Valid Anagram](242-valid-anagram.md), there's no bounded-alphabet escape here — the values can be any integers, so the count map genuinely scales with the input.

**The cost of the speedup:** the buckets array is allocated at full size n+1 even when almost all of it stays empty. `[1,1,1,...,1]` with one distinct value uses an n-slot array to hold a single number. **You traded memory for the ability to index by frequency** — the arrays & hashing bargain once again, just wearing a different hat.

If that waste matters, the heap approach uses O(d) or O(k) instead.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two steps: count, then rank. Counting is a hash map in O(n). For the ranking, sorting by count would be O(n log n), but a frequency has to be an integer between 1 and n — so I can bucket-sort instead: index an array *by frequency*, scatter each value into its bucket, then walk down from the highest bucket and take the first k. No comparisons, so O(n) overall, O(n) space. If k were tiny relative to n, or this were a stream, I'd use a size-k min-heap at O(n log k) instead."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `nums` is a stream you can't store?" | Size-k min-heap: push each count, pop when it exceeds k. O(n log k) time, O(k) space. See [heap](../data-structures/heap.md). |
| "What if k = 1?" | Just take the max of the count map — O(n), no buckets. See [min-max-key](../syntax/min-max-key.md). |
| "Return them sorted by frequency." | You already are — the bucket walk descends by frequency, so `result` comes out ordered. |
| "What if there are ties at the k boundary?" | Here the problem guarantees uniqueness. Without it you'd need a documented tie-break rule — ask the interviewer rather than assume. |
| "Reduce the memory." | Heap-based: O(d) or O(k) instead of an n+1 array that's mostly empty. |
| "The elements are strings, not ints." | Nothing changes — you bucket by *frequency*, and frequencies are integers regardless of the element type. |

**Traps:**

- **`[[]] * (n+1)`** — n+1 aliases of the same list. Appending to one appends to all, and the bug is maddening to spot. Use the comprehension.
- **Sizing the buckets as `len(nums)`** instead of `len(nums) + 1`. An element occurring all n times needs index n, so you'd get `IndexError` on the most uniform input possible.
- **Walking the buckets upward** and taking the first k — that returns the *least* frequent.
- **Forgetting the early return** and collecting everything, which quietly turns an O(n) selection into a full pass and returns too many elements.
- **Reaching for `Counter(nums).most_common(k)`.** It's the right production code and fine to mention, but writing it as your answer skips the entire point of the question.

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (the same counting pass) · [Group Anagrams](49-group-anagrams.md) (bucketing by a derived key) · [K Closest Points to Origin](973-k-closest-points-to-origin.md) (the same "top k" question, solved with a heap) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (selection without a full sort).

</details>

---
