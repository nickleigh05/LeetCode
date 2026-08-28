# 1985. Find the Kth Largest Integer in the Array

**Medium** · [LeetCode](https://leetcode.com/problems/find-the-kth-largest-integer-in-the-array/) · [Solution file (no hints)](../../problems/1500-1999/1985.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

`nums` is an array of **strings**, each representing an integer without leading zeros. Return the string representing the **k-th largest** integer. Duplicates count distinctly — in `["1","2","2"]`, the values are 1st = `"2"`, 2nd = `"2"`, 3rd = `"1"`.

```
nums = ["3","6","7","10"], k = 4  →  "3"
nums = ["2","21","12","1"],  k = 3  →  "2"
nums = ["0","0"],            k = 2  →  "0"
```

**Constraints:** `1 <= k <= nums.length <= 10⁴` · `1 <= nums[i].length <= 100` · digits only · **no leading zeros**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| values are **strings** | ⚠️ **The trap.** Lexicographic order is *not* numeric order: `"21" < "3"` as strings, but 21 > 3 |
| length up to **100 digits** | ⚠️ Far beyond a 64-bit integer — matters enormously outside Python |
| "**k-th largest**", duplicates distinct | Positional selection, not "k-th distinct value" |
| **no leading zeros** | ⚠️ The gift that makes a manual comparison rule work cleanly |
| `n` up to 10⁴ | Sorting is fine; a heap is better if `k` is small |

**The core difficulty is the comparison, not the selection.** Selecting the k-th largest is routine — sort, or use a heap. The question is *how do you order 100-digit numbers given as strings?*

Naive string comparison fails immediately:

```
"21" vs "3"     lexicographic: "2" < "3", so "21" < "3"   ❌
                numeric:        21 > 3                     ✅
```

**Two correct approaches:**

1. **Convert to `int`.** In Python, integers are arbitrary-precision, so `int("9"*100)` is exact. This is the pragmatic answer — but it's *language-specific*, and worth flagging as such.
2. **Compare by (length, then lexicographic).** Because there are no leading zeros, a longer digit string is always the larger number; if lengths tie, lexicographic comparison *is* numeric comparison.

That second rule is the language-independent one:

```
compare(a, b):
    if len(a) != len(b):  longer wins
    else:                 plain string comparison
```

**Why "no leading zeros" is load-bearing.** With leading zeros allowed, `"007"` would have length 3 and beat `"99"` under the length rule — wrong. The constraint is what makes length a valid first-order comparison.

🤔 **Before you open the next section:** given two digit strings with no leading zeros, when can you decide which is larger just by looking at their lengths?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n` = number of strings, `L` = max digits.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Sort by `int` value, index | `sorted(nums, key=int)[-k]` | O(n·L log n) | O(n) | ✅ One line, Python-specific |
| Sort by `(len, string)` | Same, comparison without conversion | O(n·L log n) | O(n) | ✅ Language-independent |
| **Min-heap of size `k`** | Keep only the `k` largest seen | **O(n log k)** | **O(k)** | ✅✅ Best when `k ≪ n` |
| Quickselect | Partition around a pivot | O(n) average | O(1) | ✅ Optimal average, O(n²) worst |

**The decision: a min-heap of size `k`.**

The idea, which is the reusable pattern for every "k-th largest" problem:

> Maintain a **min-heap holding the `k` largest elements seen so far.** The root is the smallest of those `k` — which, once you've processed everything, is exactly the k-th largest overall.

For each element: push it, and if the heap exceeds `k`, pop the smallest. The heap can only ever contain the top `k`.

**Why a *min*-heap for the *largest* elements** — this inversion trips people up:

You need to evict the **weakest** member of your top-`k` collection. A min-heap surfaces the smallest in O(1), which is exactly the eviction candidate. A max-heap would surface the largest, which is the one you most want to keep.

| Want | Heap type | Root is |
|---|---|---|
| k-th **largest** | **min-heap** of size k | the smallest of the top k ✅ |
| k-th **smallest** | max-heap of size k | the largest of the bottom k |

**Why this beats sorting when `k` is small.** Sorting is O(n log n); the heap is **O(n log k)**. With `n = 10⁴` and `k = 5`, that's `10⁴ × 2.3` versus `10⁴ × 13` — and the heap uses O(k) memory instead of O(n). When `k` is close to `n` the advantage disappears, and sorting's simpler.

**The comparison key.** Pushing raw strings would order them lexicographically — wrong. Two fixes:

- Push `int(s)` and remember the original string, or
- Push a tuple `(len(s), s)`, which Python compares element-wise: length first, then lexicographic — exactly the correct numeric order

The tuple version avoids conversion entirely and is the one to prefer if asked about huge numbers in a language without bignums.

**Why quickselect is worth naming.** It finds the k-th largest in **O(n) average** with O(1) space by partitioning — strictly better asymptotically than the heap. But its worst case is O(n²), it needs a custom comparator here, and it destroys the input's order. Mention it as the theoretically optimal option; the heap is the practical one.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

min_heap = []
```

Will hold at most `k` elements — the largest seen so far.
→ [heapq-module](../syntax/heapq-module.md)

```python
for s in nums:
    heapq.heappush(min_heap, (len(s), s))
```

**Push a `(length, string)` tuple.**

Python compares tuples element by element: first by `len(s)`, and only on a tie by the string itself. With no leading zeros, that ordering **is** numeric ordering:

- Different lengths → the longer digit string is the larger number
- Same length → lexicographic comparison equals numeric comparison

No `int` conversion needed, so this works identically in a language without arbitrary-precision integers.
→ [tuple-basics](../syntax/tuple-basics.md) · [heapq-module](../syntax/heapq-module.md)

```python
    if len(min_heap) > k:
        heapq.heappop(min_heap)
```

**Evict the smallest whenever the heap grows past `k`.**

`heappop` removes the root — the smallest of the current collection — so what remains is always the `k` largest seen so far.

Push-then-pop (rather than checking before pushing) keeps the logic to two lines and is correct even on the first `k` elements, when no eviction occurs.
→ [if-return](../syntax/if-return.md)

```python
return min_heap[0][1]
```

**The root is the answer.**

After processing everything, the heap holds the `k` largest values and its root is the **smallest of those `k`** — which is the k-th largest overall.

`[0]` is the root; `[1]` extracts the original string from the `(length, string)` tuple.
→ [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def kthLargestNumber(self, nums: List[str], k: int) -> str:

        min_heap = []

        for s in nums:
            heapq.heappush(min_heap, (len(s), s))
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0][1]
```

</details>

<details>
<summary>The one-line sort (Python-specific)</summary>

```python
class Solution:
    def kthLargestNumber(self, nums: List[str], k: int) -> str:
        return sorted(nums, key=int)[-k]
```

Relies on Python's arbitrary-precision integers, so 100-digit values convert exactly. O(n·L log n) time, O(n) space. Perfectly acceptable — but say that it's leaning on a language feature, and offer the `(len, s)` key as the portable equivalent:

```python
return sorted(nums, key=lambda s: (len(s), s))[-k]
```

</details>

**Trace it** — `nums = ["2","21","12","1"]`, `k = 3`:

| Element | Pushed as | Heap after push (as tuples) | Size > 3? | Heap after |
|---|---|---|---|---|
| `"2"` | `(1,"2")` | `[(1,"2")]` | no | `[(1,"2")]` |
| `"21"` | `(2,"21")` | `[(1,"2"),(2,"21")]` | no | same |
| `"12"` | `(2,"12")` | `[(1,"2"),(2,"21"),(2,"12")]` | no | same |
| `"1"` | `(1,"1")` | 4 elements | **yes** → pop `(1,"1")` | `[(1,"2"),(2,"21"),(2,"12")]` |

Root = `(1,"2")` → return **`"2"`** ✅

Check by hand: sorted descending the values are `21, 12, 2, 1`, so the 3rd largest is **2** ✅

**Why the tuple key matters** — compare `"21"` and `"3"`:

| Comparison | Result |
|---|---|
| Plain strings | `"21" < "3"` (since `'2' < '3'`) ❌ wrong |
| Tuples `(2,"21")` vs `(1,"3")` | `2 > 1`, so `"21"` is larger ✅ correct |

The length component fixes exactly the case raw lexicographic ordering gets wrong.

**The duplicate case** — `["0","0"]`, `k = 2`: both push as `(1,"0")`, the heap holds two entries, and the root is `(1,"0")` → **`"0"`** ✅. Duplicates are counted distinctly, as specified.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log k)</summary>

**O(n log k)** heap operations, with each comparison costing up to O(L) to compare strings — so strictly **O(n · L · log k)**.

| Phase | Cost |
|---|---|
| Per element | one push O(log k) + at most one pop O(log k) |
| Across `n` elements | **O(n log k)** |

At `n = 10⁴` and `k = 10⁴` (worst case), `log k ≈ 13` → ~1.3 × 10⁵ heap operations. Instant.

**Compare:**

| | Time | Space |
|---|---|---|
| Sort | O(n·L log n) | O(n) |
| **Min-heap of size k** | **O(n·L log k)** | **O(k)** |
| Quickselect | **O(n·L)** average | O(1) |

The heap's advantage is real when `k ≪ n` — both in the log factor and, more importantly, in **memory**: O(k) instead of O(n). For a streaming input where `n` doesn't fit in memory, the heap is the only one of the three that works at all.

**Why the `L` factor is often ignored.** Comparing two 100-digit strings is O(L), but with the `(len, s)` key most comparisons resolve on the integer length alone — a single O(1) comparison. Only same-length values fall through to the string comparison.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** — the heap never exceeds `k` entries.

That's the headline advantage over sorting, which needs **O(n)** to hold the whole array.

| | Space |
|---|---|
| Sort | O(n) |
| **Min-heap** | **O(k)** ✅ |
| Quickselect | O(1) (in place, but mutates the input) |

**Why O(k) matters beyond the constraints.** This is the canonical **streaming** pattern: if `nums` arrived as an unbounded stream, you couldn't sort it — but you could keep a size-`k` heap and always know the k-th largest so far. That's exactly what [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) formalizes.

**The pattern in one line:**

> **To track the k largest of a changing collection, keep a min-heap of size k and evict the root whenever it overflows.**

Mirror it for the k smallest: a max-heap of size k. The heap type is always the *opposite* of what you're selecting, because the root must be the element you'd discard.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The selection is standard; the trap is the comparison. These are strings up to 100 digits, so lexicographic order isn't numeric order — `\"21\"` sorts before `\"3\"` but 21 is bigger. Since there are no leading zeros, I can compare by `(length, string)`: a longer digit string is always the larger number, and on a tie, lexicographic comparison *is* numeric comparison. That avoids converting to `int`, which only works because Python has arbitrary-precision integers. For the selection I keep a **min**-heap of size `k` holding the largest elements seen — min-heap because I need to evict the *weakest* member, and the root is exactly that. At the end the root is the smallest of the top `k`, which is the k-th largest. O(n log k) time and O(k) space, which beats sorting's O(n) memory and works on a stream. Quickselect would be O(n) average but O(n²) worst case."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not compare the strings directly?" | **The trap.** `"21" < "3"` lexicographically but 21 > 3. Compare by length first, then lexicographically. |
| "Why does the length rule work?" | No leading zeros, so a longer digit string is always the larger number. With leading zeros it would break — `"007"` vs `"99"`. |
| "Why a *min*-heap for the largest?" | The root must be the element you'd evict — the smallest of your top-k collection. |
| "What if you can't use `int`?" | The `(len, s)` key needs no conversion, so it works in languages without bignums. |
| "Can you do better than O(n log k)?" | Quickselect — O(n) average, O(1) space — but O(n²) worst case, and it needs a custom comparator here. |
| "What if the data were a **stream**?" | The heap is the only viable approach: O(k) memory, and the answer is available at any moment. |
| "k-th **smallest** instead?" | Mirror it — a max-heap of size k, evicting the largest. |

**Traps:**

- **Comparing strings lexicographically.** The defining bug — and small test cases with equal-length numbers won't reveal it.
- **Using a max-heap.** You'd evict the largest, which is precisely what you want to keep.
- **Pushing raw strings without a key.** Same as lexicographic comparison.
- **Forgetting to extract `[1]` from the tuple.** Returns `(1, "2")` instead of `"2"`.
- **Assuming `int()` is safe everywhere.** 100 digits overflows 64-bit types; the conversion works in Python only.
- **Popping before pushing.** The heap could drop below `k` and lose a candidate.
- **Off-by-one on `k`.** With sorting it's `[-k]`, not `[k]` or `[-k-1]`.

**This same move shows up in:** [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (the same size-k min-heap, on plain integers) · [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (the streaming formulation this generalizes) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (size-k selection by a derived key) · [Top K Frequent Words](692-top-k-frequent-words.md) (selection where the comparison rule is the subtle part).

</details>

---
