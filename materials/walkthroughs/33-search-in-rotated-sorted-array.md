# 33. Search in Rotated Sorted Array

**Medium** · [LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/33.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

There is an integer array `nums` sorted in ascending order with **distinct** values, which has been **rotated** at some unknown pivot.

Given the array after rotation and an integer `target`, return the **index** of `target`, or `-1` if it's not present. You must write an algorithm with **O(log n)** runtime.

```
nums = [4,5,6,7,0,1,2], target = 0   →  4
nums = [4,5,6,7,0,1,2], target = 3   →  -1
nums = [1],             target = 0   →  -1
```

**Constraints:** `1 <= n <= 5000` · `-10⁴ <= nums[i], target <= 10⁴` · all values **distinct**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**rotated**" | Two ascending runs joined at a cliff, as in [153](153-find-minimum-in-rotated-sorted-array.md) |
| "return the **index**" | Not a boolean — the position |
| "**O(log n)**" | Halving required, despite the array not being globally sorted |
| "**distinct** values" | ⚠️ Essential. With duplicates, `nums[left] == nums[mid]` becomes ambiguous and O(log n) is impossible |
| "some unknown pivot" | You don't know where the cliff is — **and you shouldn't need to find it** |

**The observation that cracks it.** Pick any midpoint of a rotated array. The cliff lies on exactly one side of it — which means **the other side is a completely ordinary sorted run**.

```
nums = [4,5,6,7,0,1,2],  mid = 3 (value 7)

  [4,5,6,7]  |  [0,1,2]
   ↑ sorted     ↑ sorted (cliff is between them)

nums = [6,7,0,1,2,4,5],  mid = 3 (value 1)

  [6,7,0,1]  |  [1,2,4,5]
   ↑ has the cliff   ↑ sorted
```

**At least one half is always properly sorted.** And within a sorted half you can answer *"is the target in this range?"* with a simple range check — because in a sorted run, being between the endpoints is exactly the same as possibly being present.

So each step is:

1. Identify which half is sorted.
2. Does the target fall inside that sorted half's range?
   - **Yes** → search there.
   - **No** → search the other half.

Either way, half the array is gone. O(log n).

🤔 **Before you open the next section:** given `left`, `mid`, and `right`, what single comparison tells you whether the **left** half is the sorted one? (Hint: what's true of `nums[left]` and `nums[mid]` if no cliff lies between them?)

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Check every element | O(n) | ❌ Violates the stated bound |
| Find the pivot, then binary search | [153](153-find-minimum-in-rotated-sorted-array.md) to locate the cliff, then search one run | O(log n) | ✅ Correct, two passes, more code |
| **One-pass modified binary search** | Detect the sorted half, range-check the target | **O(log n)** | ✅ |

**The decision: one binary search that, at each step, identifies the sorted half and decides using a range check.**

**Detecting the sorted half:**

```python
left_half_is_sorted = nums[left] <= nums[mid]
```

If no cliff sits between `left` and `mid`, that segment is ascending, so its first element can't exceed its last. If the cliff *is* in there, `nums[left]` would be from the higher run and `nums[mid]` from the lower — so `nums[left] > nums[mid]`.

The `<=` handles `left == mid` (a one-element segment, trivially sorted).

**The range check, and why it's the crux.** Once you know a half is sorted, `nums[left] <= target < nums[mid]` decides everything:

- **True** → the target lies inside that sorted range, so search it.
- **False** → the target is **definitely not** in the sorted half, so it must be in the other half — if it's anywhere.

That second inference is what makes this work: **in a sorted run, "not in range" is proof of absence**, not just a hint. So you can discard the entire half with confidence.

Note the **asymmetric bounds**, `<=` on one side and `<` on the other: `nums[mid]` was already tested for equality at the top of the loop, so it's excluded here.

**Why not find the pivot first?** That approach is perfectly good and arguably easier to explain — run [153](153-find-minimum-in-rotated-sorted-array.md), then binary search whichever run can hold the target. It's two O(log n) passes. The one-pass version is the same complexity with a single loop; the trade is conceptual density versus code volume. **If you're blanking in an interview, the two-pass version is easier to get right — say so and write it.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

Inclusive range over the whole array — the [704](704-binary-search.md) convention. Unlike [153](153-find-minimum-in-rotated-sorted-array.md)'s convergence loop, this one is a *find-the-value* search, so it returns from inside.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
    mid = (left + right) // 2
```

**`<=` here**, unlike [153](153-find-minimum-in-rotated-sorted-array.md) — because this search checks whether `mid` *is* the answer, so the final single element must be examined. The updates below all use `mid ± 1`, so there's no infinite-loop risk.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if nums[mid] == target:
        return mid
```

Check the midpoint first. Values are distinct, so this is the answer — and it also lets the range checks below exclude `mid` safely.
→ [if-return](../syntax/if-return.md)

```python
    left_half_is_sorted = nums[left] <= nums[mid]
```

**The key test.** If the segment `[left, mid]` contains no cliff it's ascending, so `nums[left] <= nums[mid]`. If it does contain the cliff, `nums[left]` is from the higher run and exceeds `nums[mid]`.

Naming it rather than inlining it is deliberate — the two nested branches below are hard to read otherwise, and in an interview a named boolean is something you can point at while explaining.
→ [comparison-operators](../syntax/comparison-operators.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
    if left_half_is_sorted:
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
```

**Left half is the sorted one.** The chained comparison asks whether the target lies within it — `>=` its first element and `<` the midpoint (which we already ruled out).

- **In range** → it can only be in the left half. Search left.
- **Out of range** → it is *definitely absent* from the sorted left half, so search right.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [elif-else](../syntax/elif-else.md)

```python
    else:
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
```

**Right half is the sorted one** (the cliff is on the left). Mirror logic: is the target in `(mid, right]`?

Note the bounds flip — `<` on the left (excluding the tested `mid`) and `<=` on the right (including the endpoint). Getting these backwards is the classic bug here.

```python
return -1
```

The range emptied — the target isn't present.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            left_half_is_sorted = nums[left] <= nums[mid]

            if left_half_is_sorted:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

</details>

**Trace it** — `nums = [4,5,6,7,0,1,2]`, `target = 0`:

| `l` | `r` | `mid` | `nums[mid]` | Sorted half | Range check | Action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left `[4..7]` (4 ≤ 7) | is 0 in `[4, 7)`? **no** | `left = 4` |
| 4 | 6 | 5 | 1 | left `[0..1]` (0 ≤ 1) | is 0 in `[0, 1)`? **yes** | `right = 4` |
| 4 | 4 | 4 | **0** | — | match | `return 4` ✅ |

**And a miss** — `target = 3`:

| `l` | `r` | `mid` | `nums[mid]` | Sorted half | Range check | Action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left `[4..7]` | is 3 in `[4,7)`? no | `left = 4` |
| 4 | 6 | 5 | 1 | left `[0..1]` | is 3 in `[0,1)`? no | `left = 6` |
| 6 | 6 | 6 | 2 | left `[2..2]` | is 3 in `[2,2)`? no | `left = 7` |
| 7 | 6 | — | | | `left > right` | `return -1` ✅ |

Row 1 of the first trace shows the inference doing its work: 0 isn't in the sorted `[4..7]`, and because that half is sorted, that's **proof** it's not there — so the whole left half goes.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Every iteration does O(1) work — a handful of comparisons — and then discards half the range via `mid + 1` or `mid - 1`. Starting from n candidates, that's log₂ n iterations.

At n = 5000: about **13 iterations**.

**Why the rotation doesn't cost anything.** You might expect to pay something for the array not being sorted — but you don't. The trick is that a rotated array's midpoint always has one properly sorted side, and one comparison identifies which. Both branches still eliminate exactly half.

**Compared to the two-pass approach:** finding the pivot is O(log n), then searching one run is O(log n) → O(2 log n) = O(log n). **Identical complexity.** The one-pass version saves a constant factor and a second loop, nothing asymptotic. Choose based on which you can write correctly under pressure.

**Best case O(1):** the target is at the first midpoint.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers plus a boolean; the array is only read.

Same as every problem in this unit — binary search stores *boundaries*, never data.

**What's worth noticing here is what replaced the memory.** A hash map from value to index would answer this in O(1) per query, but costs O(n) space and O(n) to build. Binary search gets O(log n) queries at O(1) space by exploiting structure — and *rotation doesn't destroy enough structure to break it*.

That's the interesting part of this problem: rotation looks like it should ruin sortedness, but it leaves behind exactly enough — **one guaranteed-sorted half at every midpoint** — for the elimination argument to survive. Recognizing that partially-broken structure is still exploitable is the transferable skill.

**Recursive version:** O(log n) stack space, no benefit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array isn't fully sorted, but here's the key: wherever I put the midpoint, the cliff is on one side, so the *other* side is a properly sorted run. I check `nums[left] <= nums[mid]` to see whether the left half is the sorted one. Then, since the sorted half's range is trustworthy, I check whether the target falls inside it — if yes I search there, and if no, that's *proof* it isn't in the sorted half, so I search the other one. Either way I halve the space, so O(log n) time and O(1) space. The alternative is finding the pivot with a first binary search and then searching the appropriate run — same complexity, two loops."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is one half always sorted?" | **The question.** There's exactly one cliff. It falls on one side of the midpoint, so the other side has no cliff and is therefore ascending. |
| "What if the target isn't in the sorted half?" | Then it's provably absent from it — a sorted range's endpoints fully determine membership. So it's in the other half or nowhere. |
| "What about **duplicates**?" | ⚠️ `nums[left] == nums[mid]` no longer tells you which half is sorted (e.g. `[1,1,1,0,1]`). You shrink by one and degrade to **O(n)** worst case. That's LeetCode 81. |
| "Two-pass version?" | Find the minimum's index with [153](153-find-minimum-in-rotated-sorted-array.md), then binary search whichever run can contain the target. Easier to explain, same O(log n). |
| "Why `<=` in the loop here but `<` in 153?" | This search tests whether `mid` is the answer, so the last element must be checked, and updates use `mid ± 1`. 153 converges on a survivor with `right = mid`, which needs `<`. |
| "Rotated **descending** array?" | Same idea, all comparisons flipped. |

**Traps:**

- **Wrong range-check bounds.** `nums[left] <= target < nums[mid]` for the left half, `nums[mid] < target <= nums[right]` for the right. Mixing up which end is inclusive is the most common failure — remember `mid` is already excluded by the equality test.
- **Comparing `nums[mid]` to `nums[right]` to detect the sorted half.** That works for finding the *minimum* ([153](153-find-minimum-in-rotated-sorted-array.md)) but here you need to know which half is sorted; use `nums[left] <= nums[mid]`.
- **`nums[left] < nums[mid]`** with strict `<` — fails when `left == mid` (a one-element segment), which happens on small ranges.
- **Using `<` in the loop condition.** With `mid ± 1` updates you'd skip the final element.
- **Assuming the array is actually rotated.** A zero/full rotation is legal; the code handles it since the whole array is then the sorted left half.
- **Applying this with duplicates** and claiming O(log n).

**This same move shows up in:** [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (same structure, finding the cliff instead) · [Binary Search](704-binary-search.md) (the template) · [Koko Eating Bananas](875-koko-eating-bananas.md) (halving without sortedness) · [Median of Two Sorted Arrays](4-median-of-two-sorted-arrays.md) (binary search where the decision rule is the hard part).

</details>
