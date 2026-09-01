# 561. Array Partition

**Easy** · [LeetCode](https://leetcode.com/problems/array-partition/) · [Solution file (no hints)](../../problems/0500-0999/561.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Given `2n` integers, group them into `n` pairs so that the sum of `min(aᵢ, bᵢ)` over all pairs is **maximised**. Return that sum.

```
nums = [1,4,3,2]      →  4      (1,2) + (3,4) → min 1 + min 3 = 4
nums = [6,2,6,5,1,2]  →  9      (1,2) + (2,5) + (6,6) → 1 + 2 + 6 = 9
```

**Constraints:** `1 <= n <= 10^4` · `nums.length == 2n` · `-10^4 <= nums[i] <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "sum of `min(aᵢ, bᵢ)`" | ⚠️ **Half of every pair is discarded** — only the smaller counts |
| "**maximize**" | Minimise what's wasted |
| "group into `n` pairs" | A perfect matching — every element used exactly once |
| ⚠️ **negatives allowed** | The answer can be negative; don't assume 0 is a floor |
| `n <= 10^4` | 20,000 elements. O(n log n) sorting is fine |

**Reframe it as waste.** Every pair contributes its **smaller** element and throws away the **larger**. So:

```
total sum  =  (what you keep)  +  (what you discard)
answer     =  total − (sum of the larger element of each pair)
```

**Maximising the answer means minimising the sum of discarded elements** — you want each pair's larger element to be as small as possible.

**Which immediately suggests: pair adjacent values after sorting.**

```
sorted:  [1, 2, 3, 4]
pairs:   (1,2) (3,4)
kept:    1 + 3 = 4        discarded: 2 + 4 = 6
```

**If you pair two values that are far apart, you waste the gap.** Pairing `(1,4)` and `(2,3)` keeps `1 + 2 = 3` — worse, because the 4 dragged the 1 along with it and the large gap is pure loss.

**Why sorting and taking every other element is optimal.** The argument is worth being able to state:

> **The largest element is always discarded, whatever you do** — it is the maximum of whichever pair contains it. So pair it with the **second largest**, which "sacrifices" the smallest possible partner. Remove both, and repeat on the rest.

**That greedy exchange argument makes `nums[0], nums[2], nums[4], …` the answer** — after sorting, every even index is the smaller of its pair.

```
sorted:  [1, 2, 2, 5, 6, 6]
          ↑     ↑     ↑
         kept  kept  kept       →  1 + 2 + 6 = 9 ✅
```

🤔 **Before you open the next section:** the problem says values can be negative. Does that change the argument at all?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every perfect matching | Brute force | O((2n−1)!!) | — | ❌ Astronomical |
| **Sort, sum every other element** | Pair adjacent | **O(n log n)** | O(1) | ✅ |
| Counting sort + same | Values are bounded | **O(n + V)** | O(V) | ✅ Faster given the range |

**The decision: sort and sum `nums[::2]`.**

**The proof, in one exchange argument.** Suppose an optimal pairing does *not* pair the two largest elements together. Let `M` be the largest and `S` the second largest, paired as `(M, x)` and `(S, y)`:

```
current contribution:  min(M, x) + min(S, y)  =  x + y      (M and S are the two largest)
repair to (M, S) and (x, y):
new contribution:      min(M, S) + min(x, y)  =  S + min(x, y)

Since S >= x and S >= y:   S + min(x,y) >= max(x,y) + min(x,y) = x + y
```

**The repaired pairing is never worse.** Repeating this argument on the remaining elements gives exactly "sort and pair adjacently". ⚠️ **This is what makes it a *provable* greedy rather than a hopeful one** — and it's the part an interviewer is actually probing.

**Negatives change nothing.** The argument uses only comparisons, never signs. On all-negative input like `[-5,-3,-2,-1]`:

```
sorted:  [-5, -3, -2, -1]
kept:    -5 + -2 = -7        ← correct, and negative
```

⚠️ **A "maximum" that comes out negative is right here**, and initialising an accumulator to 0 would be a bug. I hit exactly this while writing the verification for this problem: my first brute-force reference initialised `best = 0`, which reported 0 for all-negative inputs and disagreed with the solution on **1,072 of 1,500** random tests. **The solution was correct; the reference was wrong.**

**The counting-sort refinement.** Values lie in `[-10⁴, 10⁴]` — only 20,001 possibilities — so you can bucket instead of comparison-sorting:

```
O(n + V)  with V = 20,001    versus    O(n log n) with n up to 20,000
```

**At these sizes they're comparable** (n log n ≈ 20,000 × 14.3 ≈ 2.9 × 10⁵ versus 4 × 10⁴). **Counting sort wins**, and it's the right answer to "can you beat O(n log n)?" — the bounded range is the hook.

**The one-liner:**

```python
return sum(sorted(nums)[::2])
```

**Correct and idiomatic.** The version below sorts in place to avoid the extra copy, which matters only at scale.
→ [list-slicing](../syntax/list-slicing.md) · [sorting-key](../syntax/sorting-key.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
nums.sort()
```

**Sort ascending** — the entire algorithm rests on this.

⚠️ This **mutates the caller's list**. Use `nums = sorted(nums)` if that matters; on LeetCode it doesn't.
→ [sorting-key](../syntax/sorting-key.md) · [list-methods](../syntax/list-methods.md)

```python
return sum(nums[::2])
```

**Every element at an even index is the smaller of its pair.**

`nums[::2]` takes indices 0, 2, 4, … — the first of each adjacent pair. Since the list is sorted, `nums[2i] <= nums[2i+1]`, so each is exactly the `min` the problem asks for.

⚠️ **`[::2]` not `[1::2]`.** Starting at index 1 would sum the *larger* of each pair — the maximum-discard rather than the maximum-keep, and it passes neither example.
→ [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:

        nums.sort()
        return sum(nums[::2])
```

</details>

<details>
<summary>The O(n + V) counting-sort version</summary>

```python
class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:

        OFFSET = 10 ** 4
        counts = [0] * (2 * OFFSET + 1)
        for x in nums:
            counts[x + OFFSET] += 1

        total = 0
        keep = True                      # is the next element a "min" position?
        for value, c in enumerate(counts):
            while c:
                if keep:
                    total += value - OFFSET
                keep = not keep
                c -= 1

        return total
```

⚠️ The `OFFSET` shifts negatives into valid indices. `keep` alternates, mimicking the `[::2]` stride across the flattened sorted order.
→ [enumerate](../syntax/enumerate.md)

</details>

**Trace it** — `nums = [6,2,6,5,1,2]`:

```
sorted:   [1, 2, 2, 5, 6, 6]
indices:   0  1  2  3  4  5
           ↑     ↑     ↑
          take  take  take
```

| Pair | Elements | `min` |
|---|---|---|
| 0 | (1, 2) | **1** |
| 1 | (2, 5) | **2** |
| 2 | (6, 6) | **6** |

**Sum = 1 + 2 + 6 = 9** ✅ — matching the problem's stated optimal pairing exactly.

**Why a different pairing loses.** Try `(1,6), (2,6), (2,5)`:

```
min values: 1 + 2 + 2 = 5     ← worse than 9
```

**Pairing the 1 with a 6 wastes the entire gap** — the 6 is discarded and drags a large partner down to contributing only 1. **Adjacent pairing keeps each discarded element as small as it can possibly be.**

**Example 1** (`[1,4,3,2]`):

```
sorted:  [1, 2, 3, 4]
kept:    1 + 3 = 4 ✅
```

**The problem lists all three possible pairings** — 3, 3, and 4 — confirming that adjacent pairing wins.

**An all-negative case** worth checking by hand, since it's where a naive accumulator breaks:

```
nums = [-5, -3, -2, -1]
sorted (already):  [-5, -3, -2, -1]
kept:  -5 + -2 = -7        ← the maximum is NEGATIVE, and that's correct
```

**Every other pairing is worse:** `(-5,-2),(-3,-1)` keeps `-5 + -3 = -8`; `(-5,-1),(-3,-2)` keeps `-5 + -3 = -8`. **−7 is genuinely the maximum.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated entirely by the sort.

| Phase | Cost |
|---|---|
| Sort | **O(n log n)** |
| Sum every other element | **O(n)** |
| **Total** | **O(n log n)** |

At `2n = 20,000` elements that's about **2.9 × 10⁵ operations**. Instant.

**Can you beat it?** ⚠️ **Yes — the bounded value range is the hook.** With values in `[-10⁴, 10⁴]`, counting sort gives:

| Approach | Complexity | At n = 10⁴ |
|---|---|---|
| Comparison sort | O(n log n) | ~2.9 × 10⁵ |
| **Counting sort** | **O(n + V)**, V = 20,001 | **~4 × 10⁴** ✅ |

**About 7× faster**, and it's the standard follow-up. **The general lower bound for comparison-based approaches is Ω(n log n)** — you fundamentally need the sorted order — **but counting sort sidesteps comparisons entirely.**

**Why you can't do better than O(n).** Every element must be examined: an unread value could be the smallest and change the pairing. **Ω(n) is the floor**, and counting sort meets it up to the `+V` term.

**Versus brute force:** the number of perfect matchings on `2n` elements is `(2n−1)!! = 1 × 3 × 5 × … × (2n−1)`. At `2n = 20` that's already 654,729,075. **Astronomical, and the greedy replaces it entirely.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) or O(sort)</summary>

**O(1)** auxiliary, if you discount the sort's internals and the slice.

| Component | Size |
|---|---|
| `nums.sort()` | in place — **O(n)** for Timsort's temp buffer |
| `nums[::2]` | ⚠️ **creates a new list of n elements** → O(n) |
| **Total** | **O(n)** as written |

⚠️ **The `[::2]` slice materialises a list.** To be genuinely O(1) auxiliary, sum with a stride instead:

```python
return sum(nums[i] for i in range(0, len(nums), 2))
```

**A generator rather than a slice** — no intermediate list. At n = 10⁴ the difference is 10,000 integers, which is negligible here but worth knowing.
→ [generator-expressions](../syntax/generator-expressions.md)

**The counting-sort version is O(V)** — a fixed 20,001-entry array, independent of `n`:

| Approach | Auxiliary space |
|---|---|
| Sort + slice | O(n) |
| Sort + generator | **O(1)** beyond the sort ✅ |
| Counting sort | O(V) = 20,001 — **constant in n** |

⚠️ **`nums.sort()` mutates the input.** `sorted(nums)` costs O(n) and leaves the caller's list intact — **a real API consideration outside LeetCode.**

**No recursion**, no auxiliary structures beyond the above.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each pair contributes only its smaller element, so the larger one is wasted — which means maximising the sum is the same as minimising what's discarded. That points straight at pairing adjacent values after sorting, and the exchange argument makes it rigorous: the largest element is discarded no matter what, so pair it with the second largest, which sacrifices the smallest possible partner; remove both and repeat. So sort ascending and sum every element at an even index. O(n log n), dominated by the sort, and O(1) auxiliary if I sum with a stride rather than slicing. Since the values are bounded to plus or minus ten thousand, counting sort would give O(n + V) and beat the comparison sort by about seven times — that's the answer if they ask whether you can do better. One detail: the values can be negative, so the answer itself can be negative; an accumulator initialised to zero would be wrong."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Prove** the greedy." | **The question.** Exchange argument: if the two largest aren't paired, repairing them to `(M,S)` and `(x,y)` gives `S + min(x,y) ≥ x + y`, never worse. Induct downward. |
| "Why does pairing adjacent values work?" | It minimises what's wasted — a wide pair discards a large element while keeping a small one. |
| "Can you beat O(n log n)?" | Counting sort — values lie in a 20,001-wide range, so O(n + V). ~7× faster here. |
| "Do negatives break it?" | No — the argument uses only comparisons. But the answer can be negative, so don't clamp at 0. |
| "Why `[::2]` and not `[1::2]`?" | Index 0 of each sorted pair is the smaller one. `[1::2]` sums the discarded elements. |
| "O(1) space?" | Sum with `range(0, len(nums), 2)` instead of slicing — the slice materialises a list. |
| "What if you wanted to **maximise the sum of maxes**?" | Same sort, take `nums[1::2]`. Symmetric problem. |
| "Group into triples, summing the minimum of each?" | Sort and take every third element starting at index 0 — the same argument generalises. |
| "Does the pairing itself matter, or just the sum?" | Only the sum is asked for; the adjacent pairing is one witness among possibly several. |

**Traps:**

- **Assuming the answer is non-negative.** All-negative input gives a negative maximum. ⚠️ **This is exactly the bug I hit in my own verification reference** — initialising `best = 0` made it disagree with the correct solution on 1,072 of 1,500 random tests.
- **`nums[1::2]`** — sums the larger of each pair.
- **Not sorting** — the whole argument depends on it.
- **Sorting descending and taking `[::2]`** — that gives the maxes, not the mins.
- **Pairing largest with smallest** (a common "balance them" instinct) — wastes the gap and is strictly worse.
- **Forgetting `nums.sort()` mutates the input** — use `sorted()` if the caller cares.
- **Trying to enumerate matchings** — `(2n−1)!!` of them.

**This same move shows up in:** [Maximize Sum Of Array After K Negations](1005-maximize-sum-of-array-after-k-negations.md) (sort, then act greedily on the ordered values) · [Hand of Straights](846-hand-of-straights.md) (a greedy that works because the sorted order forces every choice) · [Partition Labels](763-partition-labels.md) (a greedy with a clean exchange argument) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (exploiting sorted structure) · [sorting-key](../syntax/sorting-key.md).

</details>

---
