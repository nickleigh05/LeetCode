# 560. Subarray Sum Equals K

**Medium** · [LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/) · [Solution file (no hints)](../../problems/0500-0999/560.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array of integers `nums` and an integer `k`, return the **total number** of contiguous subarrays whose sum equals `k`.

```
nums = [1,1,1],  k = 2   →  2      ([1,1] at 0..1 and at 1..2)
nums = [1,2,3],  k = 3   →  2      ([1,2] and [3])
nums = [1,-1,0], k = 0   →  3      ([1,-1], [0], [1,-1,0])
```

**Constraints:** `1 <= nums.length <= 2·10⁴` · `-1000 <= nums[i] <= 1000` · `-10⁷ <= k <= 10⁷`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the total **number** of subarrays" | A count, not the subarrays themselves. You never have to build or store them |
| "**contiguous**" | A window `nums[i..j]`, not a subsequence. Order and adjacency are fixed |
| `-1000 <= nums[i]` | **Negatives are allowed.** Circle this. It is the single most important constraint on the page |
| `k` can be negative or zero | The target is unconstrained too — no assuming positive sums |
| `nums.length <= 2·10⁴` | n² = 4·10⁸ — too slow. The intended answer is O(n) or O(n log n) |
| no mention of sortedness | Unsorted, and you can't sort it: sorting destroys contiguity |

**Why the negatives matter so much.** [Sliding window](../learning/03-sliding-window.md) is the reflex for "contiguous subarray", and it does not work here. A window only works if extending it moves the sum *monotonically* — grow when too small, shrink when too big. With negatives, growing the window can make the sum go **down**, so "too big, shrink" is no longer valid reasoning and the window can skip valid answers. On `[1, -1, 1]` with `k = 1` the two-pointer approach falls apart immediately.

🤔 **Before you open the next section:** the sum of `nums[i..j]` equals `total(0..j) - total(0..i-1)`. If you're standing at `j` and you want that difference to be `k`, what exact number are you hoping to have seen earlier?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Triple loop | Every `(i, j)`, sum the slice | O(n³) | O(1) | ❌ |
| Double loop | Every `i`, extend `j` keeping a running sum | O(n²) | O(1) | ❌ 4·10⁸ at the limit |
| Sliding window | Two pointers, grow/shrink on the sum | O(n) | O(1) | ❌ **Wrong**, not just slow — negatives break the monotonicity it depends on |
| Prefix sums, pairwise | Build all prefixes, then check every pair | O(n²) | O(n) | ❌ Right idea, still quadratic |
| **Prefix sums + hash map** | One pass; count how often `curr_sum - k` has been seen | **O(n)** | O(n) | ✅ |

**The decision: a running [prefix sum](../learning/01b-prefix-sums.md) plus a [hash map](../data-structures/hashmap.md) of counts.**

The rearrangement is the whole solution. Let `P(j)` be the sum of everything up to index `j`. Then

```
sum(nums[i..j]) = P(j) - P(i-1)
```

so asking *"does some subarray ending at `j` sum to `k`?"* is asking

```
P(j) - P(i-1) = k        →        P(i-1) = P(j) - k
```

The left-hand endpoint is no longer unknown. At each `j` there is exactly one prefix value that would complete the subarray — `curr_sum - k` — and the question collapses to **"how many times have I already seen that value?"** That is a hash map lookup.

**This is [Two Sum](1-two-sum.md) wearing different clothes.** Same move: instead of hunting for a pair, walk once and ask a question with a definite answer about what you've already seen. The difference is that Two Sum stores *value → index* and returns on the first hit, while here you store *prefix sum → how many times it occurred* and **count** every hit, because several earlier prefixes can produce the same sum.

**The general move:** "count contiguous subarrays with property X" almost always becomes "prefix aggregate + hash map of how many times each aggregate was seen". It generalises past sums — see the follow-ups.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count = 0
curr_sum = 0
prefix_sums = {0: 1}
```

`curr_sum` is the running prefix. `prefix_sums` maps *a prefix sum* → *how many times it has occurred*.

**The `{0: 1}` seed is the line that decides whether this is correct.** It records the empty prefix — the sum before any element. Without it, a subarray starting at index 0 is never counted: on `nums = [3]`, `k = 3`, after the first element `curr_sum = 3` and you look up `3 - 3 = 0`. That 0 has to already be in the map, or you return 0 instead of 1.

Read it as: *"one way to have a sum of zero — take nothing."*
→ [dict-basics](../syntax/dict-basics.md)

```python
for num in nums:
    curr_sum += num
```

One pass. No index needed — you're counting, not locating.
→ [for-loop](../syntax/for-loop.md)

```python
    if (curr_sum - k) in prefix_sums:
        count += prefix_sums[curr_sum - k]
```

The lookup, and the reason it's `+=` rather than `+= 1`. If the prefix `curr_sum - k` occurred **three** times before now, then three different starting points each produce a subarray ending here that sums to `k`. Every one of them counts.

This is precisely where a set would fail: a set answers "did this prefix occur?", and the problem needs "how many times?"
→ [membership-operators](../syntax/membership-operators.md)

```python
    prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
```

Record the current prefix **after** the lookup. The ordering matters for the same reason it does in [Two Sum](1-two-sum.md): at check time the map must hold only *strictly earlier* prefixes. Increment first and a `k = 0` query would match the current prefix against itself and count a zero-length subarray.

`.get(curr_sum, 0)` handles the first occurrence without a branch; a [`defaultdict(int)`](../syntax/defaultdict.md) or [`Counter`](../syntax/counter.md) reads even cleaner.
→ [dict-methods](../syntax/dict-methods.md) · [defaultdict](../syntax/defaultdict.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:

        count = 0
        curr_sum = 0

        prefix_sums = {0: 1}

        for num in nums:
            curr_sum += num

            if (curr_sum - k) in prefix_sums:
                count += prefix_sums[curr_sum - k]

            prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1

        return count
```

</details>

**Trace it** — `nums = [1, 1, 1]`, `k = 2`:

| `num` | `curr_sum` | Looking for `curr_sum - k` | Map before | Found | `count` | Map after |
|---|---|---|---|---|---|---|
| 1 | 1 | −1 | `{0: 1}` | no | 0 | `{0:1, 1:1}` |
| 1 | 2 | 0 | `{0:1, 1:1}` | **×1** | 1 | `{0:1, 1:1, 2:1}` |
| 1 | 3 | 1 | `{0:1, 1:1, 2:1}` | **×1** | **2** | `{0:1, 1:1, 2:1, 3:1}` |

Answer **2** — the subarrays `[1,1]` at indices 0–1 and 1–2. ✅

**Now one with negatives** — `nums = [1, -1, 0]`, `k = 0`, where sliding window would fail:

| `num` | `curr_sum` | Looking for | Map before | Found | `count` |
|---|---|---|---|---|---|
| 1 | 1 | 1 | `{0:1}` | no | 0 |
| −1 | 0 | 0 | `{0:1, 1:1}` | **×1** | 1 |
| 0 | 0 | 0 | `{0:1, 1:1, 0:1}` → `{0:2, 1:1}` | **×2** | **3** |

Answer **3** — `[1,-1]`, `[0]`, and `[1,-1,0]`. The final step is the one that shows why the map stores *counts*: the prefix 0 had occurred twice, and both occurrences are legitimate starting points. ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over `nums` → n iterations.
- Per iteration: one addition, one subtraction, one hash lookup, one hash insert — all **O(1) average**.
- n × O(1) = **O(n)**.

**Compare to the double loop:** O(n²) → O(n). At n = 2·10⁴ that's 4·10⁸ operations down to 2·10⁴ — comfortably the difference between TLE and instant.

**No early exit.** Unlike [Two Sum](1-two-sum.md), you can't return the moment you find a hit — the answer is a total, so every element must be visited. It is always exactly n iterations.

**The honest asterisk:** hash operations are O(1) *average*. Adversarial collisions degrade each to O(n) and the whole thing to O(n²) — the standard caveat on every hash-based solution.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The map holds one entry per *distinct* prefix sum. Worst case — all prefixes distinct, as with any strictly positive array — that's n + 1 entries including the `{0: 1}` seed.

**Best case O(1)-ish:** on something like `[0,0,0,…,0]` every prefix is the same value, so the map holds a single key with a large count. The counts collapse the storage; the answer is still exact.

This is the [arrays & hashing](../learning/01-arrays-hashing.md) trade in its purest form: **O(n) memory buys a factor of n in time.** And unlike [Two Sum](1-two-sum.md), there's no sorted variant that escapes it — sorting would destroy contiguity, so the memory is not optional here.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "'Contiguous subarray' makes me reach for a sliding window, but the values can be negative, so extending a window doesn't move the sum monotonically and the two-pointer logic is invalid. Instead I'll use prefix sums: the sum of `nums[i..j]` is `P(j) - P(i-1)`, so a subarray ending at `j` sums to `k` exactly when some earlier prefix equals `curr_sum - k`. That turns it into a lookup — same shape as Two Sum. I keep a running sum and a hash map from prefix sum to *how many times* it occurred, seeded with `{0: 1}` for the empty prefix so subarrays starting at index 0 are counted. At each element I add however many times `curr_sum - k` has been seen, then record the current prefix. One pass, O(n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why the `{0: 1}`?" | It's the empty prefix — the sum before any element. It's what lets a subarray that starts at index 0 be counted. Drop it and `nums = [3], k = 3` returns 0. |
| "Why counts, not a set?" | Several earlier prefixes can share a value, and each is a distinct valid start. A set answers *whether*; this needs *how many*. |
| "What if all values were positive?" | Then sliding window **does** work — O(n) time and **O(1) space**, strictly better. Worth saying: the negatives are what force the hash map. |
| "Return the subarrays, not the count?" | Store prefix → list of indices instead of a count. Output can be O(n²) in size, so the complexity is output-bound. |
| "Longest such subarray?" | Store prefix → *earliest* index only, and never overwrite. Then `j - first_index[curr_sum - k]` is a candidate length. That's [Maximum Size Subarray Sum Equals k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/). |
| "Subarrays divisible by `k`?" | Same skeleton, key on `curr_sum % k` instead of `curr_sum` (mind Python's sign handling on negatives). |
| "2-D version?" | Fix a pair of rows, collapse the columns between them into a 1-D array, and run this exact algorithm on it. |

**Traps:**

- **Reaching for sliding window.** The defining mistake here. It passes the positive-only tests and fails the moment a negative appears.
- **Forgetting the `{0: 1}` seed.** Silently undercounts every subarray that starts at index 0.
- **Using `count += 1` instead of `count += prefix_sums[...]`.** Correct whenever prefixes are unique, wrong the instant one repeats — and the repeats are the interesting cases.
- **Recording the prefix before the lookup.** Lets the current prefix match itself; `k = 0` starts counting phantom empty subarrays.
- **Using a set.** Loses the multiplicity the whole answer depends on.
- **Trying to sort.** Sorting destroys contiguity — the property the problem is about.

**This same move shows up in:** [Two Sum](1-two-sum.md) (the same complement lookup, on values rather than prefixes) · [Prefix Sums](../learning/01b-prefix-sums.md) (the lesson this problem is the exam for) · [Product of Array Except Self](238-product-of-array-except-self.md) (prefix aggregates, multiplied instead of added) · [Contiguous Array](https://leetcode.com/problems/contiguous-array/) (map 0 → −1 and it becomes this problem with `k = 0`).

</details>

---
