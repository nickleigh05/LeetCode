# 1929. Concatenation of Array

**Easy** · [LeetCode](https://leetcode.com/problems/concatenation-of-array/) · [Solution file (no hints)](../../problems/1500-1999/1929.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums` of length `n`, build an array `ans` of length `2n` where `ans[i] == nums[i]` and `ans[i + n] == nums[i]` for `0 <= i < n`. Return `ans`.

```
nums = [1,2,1]    →  [1,2,1,1,2,1]
nums = [1,3,2,1]  →  [1,3,2,1,1,3,2,1]
```

**Constraints:** `n == nums.length` · `1 <= n <= 1000` · `1 <= nums[i] <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This one is deliberately gentle — it's a warm-up for array construction, not a puzzle. The value is in noticing how the *index algebra* in the statement translates directly into code.

| The statement says | Which really means |
|---|---|
| `ans` has length `2n` | The output is exactly twice the input. You know the final size up front |
| `ans[i] == nums[i]` | The **first half** is a verbatim copy |
| `ans[i + n] == nums[i]` | The **second half** is the same copy, shifted right by `n` — i.e. appended |
| both conditions for all `i` | Together they say: `ans` is `nums` followed by `nums` |
| return `ans` | Build a **new** array. Nothing in-place here |
| `n <= 1000` | Tiny. Any correct approach passes — so write the clearest one |

The whole problem is learning to read `ans[i + n] == nums[i]` and recognize it as *"the second copy starts at offset n."* Formal index notation describing something you'd say in plain English as "the array, twice."

🤔 **Before you open the next section:** if you appended every element of `nums` to a result list, and then did it a second time, what would you have?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Every approach here is O(n) time and O(n) space. There's no algorithmic trade-off to make — the only question is which reads best.

| Approach | Code | Verdict |
|---|---|---|
| **Explicit double loop** | `for _ in range(2): for num in nums: append` | ✅ Most explicit about the structure |
| List concatenation | `return nums + nums` | ✅ Clearest Python; `+` builds a new list |
| List repetition | `return nums * 2` | ✅ Same thing, even shorter |
| Preallocate + index | `ans = [0]*2*n`, then assign `ans[i]` and `ans[i+n]` | ⚠️ Mirrors the spec literally; more room for off-by-one |
| `itertools.chain` | `list(chain(nums, nums))` | ⚠️ Fine, but an import for nothing |

**The decision: any of them — but understand why `nums + nums` is safe.**

In Python, `+` on two lists **creates a new list**; it does not mutate either operand. Same for `*`. So `nums + nums` and `nums * 2` both return a fresh object, which is exactly what the problem wants. Compare with `nums += nums`, which mutates `nums` in place — a different operation with different consequences for the caller.

**One genuine subtlety worth knowing** (and the reason this problem is a decent teaching moment): `*` on a list of **mutable** objects copies *references*, not objects.

```python
grid = [[0, 0]] * 2      # ⚠️ both rows are the SAME list
grid[0][0] = 9           # → [[9, 0], [9, 0]]
```

Here `nums` holds integers, which are immutable, so there's nothing to alias and no danger. But the habit of asking *"am I copying objects or references?"* is what saves you later on [Rotate Image](48-rotate-image.md), [Spiral Matrix](54-spiral-matrix.md), and every grid-initialization bug you'll ever write. See [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md).

**Why the explicit loop is still worth writing once:** it makes the "two passes over the same data" structure visible, which is the shape the problem statement is describing. In an interview you'd say the one-liner and move on — but if asked to write it without built-ins, this is the version.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
array = []
```

The result accumulator, starting empty.
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(2):
```

**Two passes over the same data.** The loop variable `i` is never used — it's a pure repetition counter. (Python convention is to name a deliberately unused variable `_`; `for _ in range(2)` says "twice" more clearly than `for i in range(2)`.)
→ [range-function](../syntax/range-function.md)

```python
    for num in nums:
        array.append(num)
```

Copy every element, in order. Running this twice produces `nums` followed by `nums` — which satisfies both conditions in the spec at once: the first pass fills indices `0..n-1` (giving `ans[i] == nums[i]`), the second fills `n..2n-1` (giving `ans[i+n] == nums[i]`).
→ [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md)

```python
return array
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:

        array = []

        for i in range(2):
            for num in nums:
                array.append(num)

        return array

    # simpler nums + nums
    # or nums * 2
```

</details>

**Trace it** — `nums = [1,2,1]`:

| Pass | Appends | `array` |
|---|---|---|
| 1 | 1, 2, 1 | `[1,2,1]` |
| 2 | 1, 2, 1 | `[1,2,1,1,2,1]` |

Check the spec against the result: `ans[0]=1=nums[0]` ✅ and `ans[0+3]=1=nums[0]` ✅. Both conditions hold for every `i`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

The outer loop runs a **constant** 2 times, and the inner loop runs n times — so 2n appends total. Constants drop, leaving O(n).

Worth being precise about, because nested loops trigger a reflex to say O(n²): the bound is `outer × inner` only when *both* scale with the input. Here the outer bound is the literal number 2, so this is O(2n) = **O(n)**.

`list.append` is **amortized O(1)** — CPython over-allocates so most appends are a pointer write, with occasional O(n) reallocations that average out. See [list-methods](../syntax/list-methods.md).

This is optimal: producing 2n output values requires at least 2n writes.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the result holds 2n integers, and 2n is O(n).

There's **no O(1) version**, and that's not a failure of imagination: the problem asks you to *return* a 2n-element array, so the output alone is O(n). When the output is inherently that large, O(n) space is the floor.

Some analyses report O(1) *auxiliary* space here — meaning "beyond the required output, nothing extra is allocated," which is also true. Both are defensible as long as you say which you mean.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The two conditions together just say `ans` is `nums` followed by `nums`. In Python that's `nums + nums`, which builds a new list rather than mutating the input. If they want it explicit, it's two passes appending every element. O(n) time and O(n) space, and the space is unavoidable since the output itself is 2n."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it without `+` or `*`." | The explicit double loop above, or preallocate `[0] * (2*n)` and assign `ans[i]` and `ans[i+n]`. |
| "Concatenate `k` copies." | `nums * k`, or wrap the loop in `for _ in range(k)`. O(k·n). |
| "In-place, modifying `nums`?" | `nums.extend(nums)` — CPython snapshots the iterable's length first, so it terminates correctly. `nums += nums` does the same. Both mutate the caller's list. |
| "What's the difference between `nums + nums` and `nums += nums`?" | `+` builds a new list and rebinds; `+=` calls `__iadd__` and mutates in place. Visible to anyone else holding a reference to that list. |
| "Why is `[[0]*n]*m` dangerous?" | `*` copies **references**. All m rows become the same list object, so writing one row writes all of them. Use `[[0]*n for _ in range(m)]`. |
| "Return the concatenation reversed?" | `(nums + nums)[::-1]`, or `nums[::-1] * 2` — note those differ; reason about which the spec wants. |

**Traps:**

- **`nums.append(nums)`** appends the list *itself* as a nested element, creating a self-referential structure. You want `extend`, `+`, or a loop over elements.
- **Iterating `nums` while appending to it.** `for num in nums: nums.append(num)` is an infinite loop. Build a separate result, or use `extend`, which reads the length once.
- **Mutating the input when a new array was requested.** `nums += nums` changes the caller's list. Here the judge doesn't care, but the distinction matters in real code.
- **Assuming `*` deep-copies.** Safe for integers, catastrophic for nested lists. The instinct to check is worth building now, on the easy problem, rather than during a grid bug.
- **Calling it O(n²)** because of the nested loops. The outer bound is a constant.

**This same move shows up in:** [Next Greater Element II](503-next-greater-element-ii.md) (circular arrays are often handled by conceptually doubling them) · [Rotate Image](48-rotate-image.md) (where reference-vs-copy semantics genuinely bite) · [Product of Array Except Self](238-product-of-array-except-self.md) (building a result array with index-offset reasoning).

</details>

---
