# 303. Range Sum Query - Immutable

**Easy** · [LeetCode](https://leetcode.com/problems/range-sum-query-immutable/) · [Solution file (no hints)](../../problems/0001-0499/303.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums`, handle multiple queries of the form: calculate the sum of elements between indices `left` and `right` **inclusive**.

Implement the `NumArray` class:
- `NumArray(int[] nums)` — initializes the object with the array
- `int sumRange(int left, int right)` — returns `nums[left] + nums[left+1] + … + nums[right]`

```
NumArray([-2, 0, 3, -5, 2, -1])
sumRange(0, 2)  →   1      (-2 + 0 + 3)
sumRange(2, 5)  →  -1      (3 + -5 + 2 + -1)
sumRange(0, 5)  →  -3
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁵ <= nums[i] <= 10⁵` · `0 <= left <= right < nums.length` · **at most 10⁴ calls** to `sumRange`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Immutable**" (in the title!) | ⚠️ The array **never changes**. So any work you do up front stays valid forever — precomputation is free money |
| "handle **multiple queries**" | You're being graded on the *total* cost across all calls, not one call. That shifts the whole optimization target |
| "at most **10⁴ calls**" with `n` up to 10⁴ | Naive per-query summing is 10⁴ × 10⁴ = **10⁸** operations. Too slow — and this number is in the constraints precisely to rule it out |
| it's a **class**, not a function | The split between `__init__` and `sumRange` is a hint: the constructor is where you're *invited* to precompute |
| `left <= right` guaranteed | No empty or backwards ranges to defend against |
| inclusive on **both** ends | The classic off-by-one hazard — `right` is part of the sum |

This is a **design** problem disguised as an array problem. The question isn't "how do I sum a range" — it's obvious how. The question is **how do I amortize repeated work across many queries**.

The reframe: you have two budgets, and they trade against each other.

| | Build cost (once) | Query cost (× 10⁴) |
|---|---|---|
| Do nothing up front | O(1) | O(n) each → **O(n·q) total** |
| Precompute | O(n) | **O(1)** each → **O(n + q) total** |

When queries vastly outnumber the build, you *always* want to shift work into the constructor.

🤔 **Before you open the next section:** if you knew the sum of everything from index 0 up to any point, could you get the sum of a middle chunk without adding it up?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let n = array length, q = number of queries.

| Approach | Build | Per query | Total | Verdict |
|---|---|---|---|---|
| Sum on demand | O(1) | O(n) | O(n·q) = 10⁸ | ❌ Too slow, and wastes the immutability |
| Cache seen ranges | O(1) | O(n) first, O(1) repeat | unbounded | ⚠️ Only helps if queries repeat; O(n²) worst-case memory |
| Precompute **all** ranges | O(n²) | O(1) | O(n²) build = 10⁸ | ❌ Fixes the wrong end |
| **Prefix sums** | **O(n)** | **O(1)** | **O(n + q)** | ✅ |
| [Segment tree](../data-structures/segment-tree.md) / [Fenwick](../data-structures/fenwick-tree.md) | O(n) | O(log n) | O(n + q log n) | ⚠️ Correct but strictly worse *here* — their power is updates, which don't exist |

**The decision: a [prefix sum](../learning/01b-prefix-sums.md) array.**

Define `prefix[i]` = sum of the first `i` elements = `nums[0] + … + nums[i-1]`. Then any range sum is a **single subtraction**:

```
sumRange(left, right) = prefix[right + 1] - prefix[left]
```

**Why that works** — and this is the mental picture to keep:

```
nums:      [-2,  0,  3, -5,  2, -1]
prefix:  [0, -2, -2,  1, -4, -2, -3]
             ↑            ↑
          prefix[0]    prefix[3]

sumRange(0, 2) = prefix[3] - prefix[0] = 1 - 0 = 1
```

`prefix[right+1]` is "everything up to and including `right`." `prefix[left]` is "everything strictly before `left`." Subtract, and the shared front section cancels exactly, leaving the middle chunk you asked for. It's the discrete analogue of the fundamental theorem of calculus — the difference of an accumulation gives you the piece between.

**Why the extra leading zero matters so much.** Making `prefix` length `n+1` with `prefix[0] = 0` means "the sum of nothing is zero" is *represented in the array*. That single sentinel is what makes `left = 0` work with no special case — otherwise you'd need `if left == 0` branching in every query, which is exactly the kind of thing that breeds bugs.

**Why not a segment tree?** Segment trees exist to support **updates** in O(log n). The word "Immutable" in the title is telling you there are no updates, so you'd be paying log n per query for flexibility you'll never use. Name it as the answer to the *mutable* follow-up ([LeetCode 307](https://leetcode.com/problems/range-sum-query-mutable/)) and move on.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class NumArray:
    def __init__(self, nums: List[int]):
```

The constructor — where all the real work happens. Everything expensive goes here, **once**, because the array is immutable and the result stays valid forever.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
        self.prefix = [0] * (len(nums) + 1)
```

**Length `n + 1`, not `n`** — the single most important line to get right.

The extra slot at the front holds `0`, meaning "sum of the empty prefix." It buys you a uniform formula with no edge case at `left = 0`. Sizing this `n` instead is the number-one bug on this problem.
→ [list-basics](../syntax/list-basics.md)

```python
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]
```

The running accumulation, in one pass. Each entry is the previous total plus the current element — so `prefix[i+1]` ends up holding the sum of `nums[0..i]`.

Note the **shift**: we read `nums[i]` but write `prefix[i+1]`. That offset *is* the leading-zero convention, and keeping it straight is most of the work.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

**The payoff — one subtraction, no loop.**

- `prefix[right + 1]` — everything up to and *including* `right` (the `+1` is the inclusive upper bound)
- `prefix[left]` — everything strictly *before* `left`
- the difference — exactly `nums[left..right]`

Trace the indices once by hand and this stops feeling arbitrary. Ask yourself "what does `prefix[k]` mean?" (answer: the sum of the first `k` elements) and both `+1`s fall out of that definition rather than needing to be memorized.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class NumArray:
    def __init__(self, nums: List[int]):

        self.prefix = [0] * (len(nums) + 1)

        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)
```

</details>

<details>
<summary>The naive alternative (also in the solution file)</summary>

```python
### Additional solutions ###

class NumArray:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def sumRange(self, left: int, right: int) -> int:
        return sum(self.nums[left : right + 1])
```

Correct, and worth saying as your baseline — but O(n) per query, so O(n·q) = 10⁸ overall. It also builds a throwaway slice on every call. This is what the constraints are designed to reject.

</details>

**Build the prefix** — `nums = [-2, 0, 3, -5, 2, -1]`:

| `i` | `nums[i]` | `prefix[i]` | `prefix[i+1]` = `prefix[i] + nums[i]` |
|---|---|---|---|
| — | — | — | `prefix[0] = 0` (sentinel) |
| 0 | −2 | 0 | −2 |
| 1 | 0 | −2 | −2 |
| 2 | 3 | −2 | 1 |
| 3 | −5 | 1 | −4 |
| 4 | 2 | −4 | −2 |
| 5 | −1 | −2 | −3 |

`prefix = [0, -2, -2, 1, -4, -2, -3]`

**Answer the queries** — each is one subtraction:

| Query | Formula | Arithmetic | Result |
|---|---|---|---|
| `sumRange(0, 2)` | `prefix[3] - prefix[0]` | `1 - 0` | **1** ✅ |
| `sumRange(2, 5)` | `prefix[6] - prefix[2]` | `-3 - (-2)` | **−1** ✅ |
| `sumRange(0, 5)` | `prefix[6] - prefix[0]` | `-3 - 0` | **−3** ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n) build, O(1) per query</summary>

Complexity here has **two numbers**, and quoting only one misses the point of the problem.

- **`__init__`: O(n)** — one pass, one addition per element.
- **`sumRange`: O(1)** — two array reads and a subtraction. Independent of range width: summing 1 element and summing 10⁴ elements cost exactly the same.

**Total for q queries: O(n + q).** At n = q = 10⁴ that's ~2·10⁴ operations, versus **10⁸** for the naive version — a ~5000× improvement, and precisely why the constraints are set where they are.

**How to talk about amortized design:** the one-time O(n) build is only worth it if queries are frequent enough to repay it. The break-even is a single query — after that you're strictly ahead. With 10⁴ queries promised, it's not close.

The general principle, which shows up constantly in system design as well as algorithms:

> **Move work from the hot path (queries) to the cold path (setup), whenever the setup's result stays valid.** "Immutable" is the guarantee that makes it valid.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the prefix array holds `n + 1` integers.

The naive version is O(1) auxiliary (it just keeps a reference to `nums`), so this is a deliberate **space-for-time trade** — the same bargain as [Contains Duplicate](217-contains-duplicate.md) and [Two Sum](1-two-sum.md), just applied to sums instead of lookups.

| | Space | Build | Query |
|---|---|---|---|
| Store `nums` only | O(1) extra | O(1) | O(n) |
| **Prefix sums** | **O(n)** | O(n) | **O(1)** |
| All-pairs table | O(n²) | O(n²) | O(1) |

Note the third row: precomputing *every* `(left, right)` pair also gives O(1) queries, but at 10⁸ cells it's hopeless. Prefix sums get the same query speed with **linear** space, because they exploit the fact that ranges *decompose* — every range is the difference of two prefixes, so you only need n of them, not n².

That decomposition is the real idea. You don't store answers; you store something answers can be *derived* from in O(1).

**Micro-optimization:** you could overwrite `nums` in place to get O(1) extra space — but it's called `Immutable` and mutating the caller's array would be rude. Keep the separate array.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array never changes and there are up to 10⁴ queries, so summing on demand would be 10⁸ operations. Instead I precompute prefix sums in the constructor: `prefix[i]` is the sum of the first `i` elements, with `prefix[0] = 0` so there's no edge case at the left boundary. Then any range is `prefix[right+1] - prefix[left]` — the shared front cancels and leaves the middle. O(n) build, O(1) per query, O(n) space. If updates were allowed I'd switch to a Fenwick tree or segment tree for O(log n) on both."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `nums` can be **updated**?" | **The standard follow-up** — [LeetCode 307](https://leetcode.com/problems/range-sum-query-mutable/). Prefix sums need O(n) to rebuild after any write. Use a [Fenwick tree](../data-structures/fenwick-tree.md) or [segment tree](../data-structures/segment-tree.md): O(log n) update *and* query. |
| "2-D version?" | [LeetCode 304](https://leetcode.com/problems/range-sum-query-2d-immutable/) — a 2-D prefix grid, with queries via inclusion–exclusion: `D - B - C + A`. |
| "Range **minimum** instead of sum?" | Prefix sums fail — min isn't invertible, so you can't subtract it away. Use a [sparse table](../data-structures/sparse-table.md) (O(1) query, immutable) or a segment tree. |
| "Why the leading zero?" | It represents "sum of nothing," which makes `left = 0` work in the same formula as everything else. Without it you need a branch in every query. |
| "Could you avoid the extra array?" | Overwrite `nums` in place — O(1) extra space. But the class is *Immutable*; mutating the caller's input is a bad trade for a constant factor. |
| "What if queries are sparse — say only 3?" | Then the O(n) build may not pay for itself. Compute on demand, or build lazily on first query. Complexity analysis has to include how often you're called. |
| "Overflow?" | Not in Python (arbitrary-precision ints). In C++/Java, 10⁴ × 10⁵ = 10⁹ fits in `int32` but is uncomfortably close — use `long`. |

**Traps:**

- **Sizing `prefix` as `n` instead of `n + 1`.** Then `prefix[right+1]` overruns on the last element, and `left = 0` needs a special case. *The* bug on this problem.
- **Forgetting `+ 1` on `right`.** The range is inclusive; `prefix[right] - prefix[left]` silently drops the last element and returns a plausible-looking wrong number.
- **Doing the work in `sumRange` instead of `__init__`.** The class structure exists to signal where precomputation belongs.
- **`sum(nums[left:right+1])`** — correct but O(n) per call, plus it allocates a slice every time. Fine as a stated baseline, not as your answer.
- **Reaching for a segment tree.** Over-engineering for an explicitly immutable array; it's a slower query for flexibility you don't need.
- **Assuming all values are positive.** They're not (−10⁵ to 10⁵), so sliding-window or two-pointer tricks that rely on monotonic sums don't apply here. Prefix sums don't care about sign.

**This same move shows up in:** [Product of Array Except Self](238-product-of-array-except-self.md) (prefix *products* from both directions) · [Subarray Sum Equals K](560-subarray-sum-equals-k.md) (prefix sums plus a hash map — the same subtraction identity, run in reverse) · [Contiguous Array](525-contiguous-array.md) (prefix sums over ±1 to find balanced ranges) · [Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/) (the two-dimensional generalization).

</details>

---
