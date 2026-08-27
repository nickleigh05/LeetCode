# 525. Contiguous Array

**Medium** · [LeetCode](https://leetcode.com/problems/contiguous-array/) · [Solution file (no hints)](../../problems/0500-0999/525.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given a binary array `nums`, return the **maximum length** of a contiguous subarray with an **equal number of 0s and 1s**.

```
nums = [0,1]          →  2      ([0,1] — one 0, one 1)
nums = [0,1,0]        →  2      ([0,1] at 0-1, or [1,0] at 1-2)
nums = [0,0,1,0,0,0,1,1]  →  6  (indices 2-7 → [1,0,0,0,1,1] — three 0s, three 1s)
```

**Constraints:** `1 <= nums.length <= 10⁵` · `nums[i]` is `0` or `1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**binary** array" | Only two values. That's a strong hint they can be *re-encoded* into something more useful |
| "**equal number** of 0s and 1s" | A **balance** condition — not a sum, not a target. Count(0) − Count(1) = 0 |
| "**contiguous** subarray" | Defined by two endpoints, so prefix-based reasoning applies |
| "**maximum length**" | You want the **widest** such range, so among candidates you keep the earliest start |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead. Must be O(n) or O(n log n) |
| values are only 0 and 1 | No negatives to worry about, but also no useful sum structure *as given* |

The obstacle: "equal counts of two things" isn't directly a prefix-sum question, because summing a binary array just counts the 1s. You'd need to track two counts and compare them.

**The re-encoding that unlocks everything:**

> Treat every `0` as **−1** and every `1` as **+1**.

Now "equal numbers of 0s and 1s" becomes "**the values sum to zero**" — because each 0 contributes −1 and each 1 contributes +1, and they cancel exactly when the counts match. A balance condition has become a sum condition, and sum conditions are what prefix sums are *for*.

Then apply the prefix identity from [Range Sum Query](303-range-sum-query-immutable.md):

```
sum(i..j) = prefix[j+1] - prefix[i] = 0    ⟺    prefix[j+1] == prefix[i]
```

So: **a balanced subarray is exactly a pair of positions where the running sum is the same.** To maximize its length, for each running-sum value you want the **earliest** index at which it occurred.

🤔 **Before you open the next section:** if the running sum returns to a value it held earlier, what must be true about everything in between?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(i, j)`, count 0s and 1s | O(n³) | O(1) | ❌ Hopeless |
| Brute force + running counts | Every start, extend tracking balance | O(n²) | O(1) | ⚠️ Correct; 10¹⁰ ops — too slow |
| Sliding window | Grow/shrink to stay balanced | — | — | ❌ **Wrong** — balance isn't monotonic, so there's no shrink rule |
| **±1 prefix sum + hash map** | Map running sum → **first** index | **O(n)** | O(n) | ✅ |
| ±1 prefix + array indexing | Same, but the map is a fixed array | **O(n)** | O(n) | ✅ Faster constants; sums are bounded by ±n |

**The decision: re-encode to ±1, then map each running sum to the *first* index where it appeared.**

Three ideas stacked, and it's worth naming them separately:

1. **Re-encode** 0 → −1, so "balanced" becomes "sums to 0."
2. **Prefix sums**, so any subarray's sum is a difference of two running sums — and a zero sum means the two running sums are *equal*.
3. **Store the first occurrence**, because for a fixed sum value, pairing the current index with the **earliest** matching index maximizes the width.

That third point is the key difference from [Subarray Sum Equals K](560-subarray-sum-equals-k.md). There you wanted to *count* subarrays, so the map stored **frequencies** and you updated it every time. Here you want the *longest*, so the map stores the **first index** and you must **never overwrite** it — a later occurrence would only give a shorter subarray.

| | Subarray Sum Equals K | This problem |
|---|---|---|
| Goal | count all | longest one |
| Map value | frequency | **first index** |
| On repeat | increment | **do nothing** |

**The `{0: -1}` seed.** Initialize with running sum 0 at index **−1**, representing "before the array started." Then a balanced subarray beginning at index 0 computes its length correctly as `i - (-1) = i + 1`. It's the same empty-prefix sentinel as the leading zero in [Range Sum Query](303-range-sum-query-immutable.md) — just expressed as an index rather than a value.

Without it, `[0,1]` returns 0 instead of 2.

**Why not a sliding window?** Same reason as [Subarray Sum Equals K](560-subarray-sum-equals-k.md): the balance can move either direction as you extend, so "unbalanced right now" tells you nothing about whether to shrink. Windows need monotonicity; this has none.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
sum_map = {0: -1}
max_len = 0
running_sum = 0
```

- `sum_map` — running sum → **first index** where it occurred. Seeded with `0 → -1` for the empty prefix, as above.
- `max_len` — best answer so far. Starting at 0 makes "no balanced subarray exists" correct with no special case.
- `running_sum` — the ±1 accumulation.

→ [dict-basics](../syntax/dict-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i, num in enumerate(nums):
    running_sum += 1 if num == 1 else -1
```

**The re-encoding, done inline.** No need to transform the array first — just add the right value as you go. A `1` pushes the balance up, a `0` pushes it down.
→ [enumerate](../syntax/enumerate.md) · [ternary-expression](../syntax/ternary-expression.md)

```python
    if running_sum in sum_map:
        max_len = max(max_len, i - sum_map[running_sum])
```

**We've seen this balance before**, which means everything between that earlier index and here nets to zero — a balanced subarray.

Its length is `i - first_index`. Not `i - first_index + 1`: the stored index is the position *before* the subarray starts (that's what the −1 seed encodes), so the subtraction already yields the correct count.
→ [min-max-key](../syntax/min-max-key.md)

```python
    else:
        sum_map[running_sum] = i
```

**Only record a sum the first time — and the `else` is doing the work.** If this sum is already in the map, its stored index is earlier, and earlier is better for maximizing length. Overwriting would shrink every future match.

This single `else` is the difference between this problem and [Subarray Sum Equals K](560-subarray-sum-equals-k.md), where you update unconditionally.
→ [elif-else](../syntax/elif-else.md)

```python
return max_len
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:

        sum_map = {0: -1}
        max_len = 0
        running_sum = 0

        for i, num in enumerate(nums):
            running_sum += 1 if num == 1 else -1

            if running_sum in sum_map:
                max_len = max(max_len, i - sum_map[running_sum])
            else:
                sum_map[running_sum] = i

        return max_len
```

</details>

<details>
<summary>The array-indexed variant (also in the solution file)</summary>

```python
### Array solution for speed ###
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:

        n = len(nums)
        first_indices = [-2] * (2 * n + 1)
        first_indices[0 + n] = -1
        max_len = 0
        running_sum = 0

        for i, num in enumerate(nums):
            running_sum += 1 if num == 1 else -1
            idx = running_sum + n
            if first_indices[idx] != -2:
                max_len = max(max_len, i - first_indices[idx])
            else:
                first_indices[idx] = i

        return max_len
```

Identical algorithm, but the map is a plain array. The running sum is bounded to `[-n, n]`, so **shifting by `n`** maps it onto valid indices `[0, 2n]`. `-2` is the "unseen" sentinel (distinct from the legitimate `-1`). Same O(n)/O(n), but no hashing — meaningfully faster in practice. A nice demonstration that a hash map is only needed when keys are *unbounded*.

</details>

**Trace it** — `nums = [0, 1, 1, 1, 0]`:

| `i` | `num` | `running_sum` | in map? | length | `max_len` | map after |
|---|---|---|---|---|---|---|
| — | — | 0 | — | — | 0 | `{0: -1}` |
| 0 | 0 | −1 | no | — | 0 | `{0:-1, -1:0}` |
| 1 | 1 | 0 | **yes** (−1) | `1-(-1)=2` | **2** | unchanged |
| 2 | 1 | 1 | no | — | 2 | `{0:-1, -1:0, 1:2}` |
| 3 | 1 | 2 | no | — | 2 | `{…, 2:3}` |
| 4 | 0 | 1 | **yes** (2) | `4-2=2` | 2 | unchanged |

Answer **2** — the subarray `[0,1]` at indices 0–1. (With three 1s and two 0s overall, no longer balanced range exists.)

**A trace showing why "first index only" matters** — `nums = [0, 1, 0]`:

| `i` | `num` | `running_sum` | in map? | length | `max_len` |
|---|---|---|---|---|---|
| — | — | 0 | — | — | 0 |
| 0 | 0 | −1 | no → store `-1:0` | — | 0 |
| 1 | 1 | 0 | **yes** (−1) | `1-(-1)=2` | **2** |
| 2 | 0 | −1 | **yes** (0) | `2-0=2` | 2 |

At `i = 2` the sum −1 was first seen at index 0. Had we overwritten it at any point, this match would have been shorter or lost.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

A single pass. Each iteration does one addition, one membership test, and at most one insert or one `max` — all O(1) average.

No nesting, no early exit, no re-scanning. Exactly n iterations regardless of the input.

**Compare to O(n²) brute force:** at n = 10⁵ that's 10¹⁰ operations — hopeless in any language. The hash map replaces "search all earlier positions for a matching balance" with a single lookup, which is the same conversion that makes [Two Sum](1-two-sum.md) and [Subarray Sum Equals K](560-subarray-sum-equals-k.md) linear.

**The array variant is also O(n)** but avoids hashing entirely — same asymptotics, better constants, because integer indexing beats hash computation and pointer chasing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The running sum ranges over `[-n, n]` — that's `2n + 1` possible values — and the map holds at most one entry per distinct sum encountered, so at most `min(n + 1, 2n + 1)` = **O(n)** entries.

The array variant makes this explicit: it allocates exactly `2n + 1` slots up front. Slightly more memory in the best case, but a tighter constant per entry and no hash overhead.

**Can you do better?** Not without giving up linear time. The O(n²) brute force is O(1) space — the usual trade:

| | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| **Prefix + map** | **O(n)** | O(n) |

**The insight worth carrying forward:** the memory is buying you *history*. You need to know where each balance value first appeared, and there's no way to reconstruct that on demand. Whenever a problem asks about a relationship between the current position and *some earlier position*, expect to pay O(n) space to remember the past — that's the shape shared by [Two Sum](1-two-sum.md), [Subarray Sum Equals K](560-subarray-sum-equals-k.md), and [Longest Consecutive Sequence](128-longest-consecutive-sequence.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The trick is re-encoding: treat 0 as −1 and 1 as +1, so 'equal counts' becomes 'sums to zero.' Then a subarray sums to zero exactly when the running prefix sum is the same at both ends. So I keep a running sum and a hash map from sum value to the **first** index where I saw it — first, because pairing with the earliest occurrence maximizes length. I seed it with sum 0 at index −1 to represent the empty prefix, so subarrays starting at index 0 work. Each step, if the current sum is already in the map, I've found a balanced subarray of length `i - firstIndex`. O(n) time, O(n) space. Since the sum is bounded by ±n I could use a shifted array instead of a hash map for better constants."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why store the **first** index, not the latest?" | **The key question.** Earliest start ⇒ longest subarray. Overwriting only ever shortens future matches. |
| "How does this differ from Subarray Sum Equals K?" | Same prefix machinery, different bookkeeping: counts + always update (for counting) vs. first index + never overwrite (for longest). |
| "Equal numbers of **three** symbols?" | Track a *pair* of differences, e.g. `(count_a − count_b, count_b − count_c)`, and key the map on that tuple. Generalizes to k symbols with a (k−1)-tuple. |
| "Count balanced subarrays instead of the longest." | Store frequencies and sum them — exactly [Subarray Sum Equals K](560-subarray-sum-equals-k.md) with `k = 0` on the ±1 encoding. |
| "Longest subarray with equal 0s and 1s **and** even length?" | Any balanced subarray already has even length — the counts are equal, so the total is 2× either count. Free. |
| "Can you avoid the hash map?" | Yes — the sum is bounded by ±n, so use an array of size `2n+1` shifted by `n`. Same complexity, faster in practice. |
| "Return the subarray, not the length." | Track the best `(start, end)` alongside `max_len`, then slice. |

**Traps:**

- **Overwriting the stored index.** The defining bug. Use `else`, or an explicit `if running_sum not in sum_map`. An unconditional update turns a correct algorithm into a wrong one that still passes small tests.
- **Omitting the `{0: -1}` seed.** Any balanced subarray starting at index 0 is missed. `[0,1]` returning 0 is the tell.
- **Using `i - first + 1`.** The stored index is *before* the subarray starts, so the `+1` double-counts. Off by one every time.
- **Forgetting to re-encode.** Summing the raw binary array just counts 1s and tells you nothing about balance.
- **Reaching for a sliding window.** Balance isn't monotonic under extension, so there's no valid shrink rule.
- **Using `-1` as the "unseen" sentinel in the array variant.** `-1` is a *legitimate* stored index (from the seed). Use `-2`, or a separate presence array.

**This same move shows up in:** [Subarray Sum Equals K](560-subarray-sum-equals-k.md) (the counting sibling — same prefix identity, different bookkeeping) · [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (the prefix-sum identity in isolation) · [Two Sum](1-two-sum.md) (hash map remembering earlier positions) · [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) (a binary-array problem where a window *does* work, because the constraint is monotonic — a useful contrast).

</details>

---
