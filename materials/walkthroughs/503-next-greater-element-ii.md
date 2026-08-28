# 503. Next Greater Element II

**Medium** · [LeetCode](https://leetcode.com/problems/next-greater-element-ii/) · [Solution file (no hints)](../../problems/0500-0999/503.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a **circular** integer array `nums` (the element after `nums[n-1]` is `nums[0]`), return the next greater number for every element. The next greater number of `x` is the first greater number to its traversing-order next, searching **circularly**. Return `-1` where none exists.

```
nums = [1,2,1]      →  [2,-1,2]     (the last 1 wraps around to find 2)
nums = [1,2,3,4,3]  →  [2,3,4,-1,4]
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**next greater**" | [Monotonic stack](../data-structures/monotonic-stack.md) — same engine as [Next Greater Element I](496-next-greater-element-i.md) |
| "**circular**" | ⚠️ The only new thing. Searching can wrap past the end back to the start |
| return for **every** element | The output is length `n`, indexed positionally |
| duplicates **allowed** | ⚠️ Values are no longer unique, so you must track **indices**, not values |
| `n` up to 10⁴ | O(n²) is 10⁸ — borderline in Python. O(n) is the intended answer |
| values can be negative | So `-1` as "no answer" is a sentinel in the *output*, never confused with data, since it's written positionally |

This is [Next Greater Element I](496-next-greater-element-i.md) with two changes, and each demands a specific adjustment:

| | NGE I | NGE II |
|---|---|---|
| Elements | distinct | **duplicates allowed** ⇒ stack holds **indices** |
| Search range | to the right only | **circular** ⇒ wrap around |
| Output | answers for a query subset | answers for **every position** |

**Handling circularity — the standard trick:**

> **Iterate `2n` times, using `i % n` to index.** That simulates walking the array twice, giving every element a full lap's worth of candidates to its right.

Why two passes suffice: the farthest an element's answer can be is `n - 1` positions ahead (a full lap). One extra pass covers exactly that, and a third would add nothing.

**The critical refinement:** on the *second* pass, **resolve but don't push**. Second-pass elements are duplicates of ones already in flight — pushing them would create phantom entries that never get resolved and could produce wrong answers. Their only job is to answer questions left over from the first pass.

🤔 **Before you open the next section:** if you walk the array twice, what would go wrong if you pushed elements onto the stack during the second lap as well?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each `i`, scan up to `n-1` positions forward with `% n` | O(n²) | O(1) | ⚠️ 10⁸ — likely too slow in Python |
| Duplicate the array | Build `nums + nums`, run standard NGE, take the first `n` | O(n) | **O(n)** extra | ✅ Works; wastes memory on a copy |
| **Monotonic stack, `2n` loop with `% n`** | Simulate two laps without copying | **O(n)** | O(n) | ✅ |

**The decision: a monotonic stack of *indices*, iterating `2n` times with modular indexing.**

Three pieces, each fixing one of the problem's wrinkles:

1. **Stack holds indices, not values.** With duplicates, a value no longer identifies a position — `[2,2]` would collide in a value-keyed map. Indices are unique by construction, and they're also what you need to write into the result array.
2. **Loop `2n` times, index with `i % n`.** Simulates the wrap without allocating `nums + nums`. `i = n` maps back to index 0, and so on.
3. **Only push when `i < n`.** Second-lap elements resolve pending questions but must not become pending themselves.

**Why "resolve but don't push" is essential.** Suppose you pushed on the second lap. At the end, the stack would hold second-lap indices that were never resolved — and if you then wrote `-1` for them (or reused `i % n`), you'd overwrite legitimate first-pass answers with `-1`. The guard keeps the set of "pending" entries exactly equal to the `n` real positions.

**Why preinitializing the result to `-1` is the clean approach.** Rather than draining the stack at the end and writing `-1`, fill `result` with `-1` up front. Anything the stack resolves overwrites it; anything left unresolved keeps the default. One less loop, and no risk of the drain writing to the wrong indices.

**Why not duplicate the array?** `nums + nums` then a standard NGE pass is genuinely correct and arguably easier to read. It costs an extra O(n) array — trivial at n = 10⁴. Mention it as the simpler-to-explain variant; the `% n` version is the one that shows you understand the mechanism.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(nums)
result = [-1] * n
stack = []
```

- `result` — **preinitialized to `-1`**, so unresolved positions need no special handling
- `stack` — **indices** of elements still waiting for a next greater element, values decreasing bottom-to-top

→ [list-basics](../syntax/list-basics.md)

```python
for i in range(2 * n):
    current = nums[i % n]
```

**Two laps in one loop.** `i % n` wraps `i = n … 2n-1` back onto `0 … n-1`, so the second half revisits the array from the start — exactly the circular behaviour.
→ [range-function](../syntax/range-function.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    while stack and nums[stack[-1]] < current:
        result[stack.pop()] = current
```

**Resolve.** `current` is the next greater element for every pending index whose value is smaller.

Note the double indirection: `stack[-1]` is an *index*, so `nums[stack[-1]]` is the value it refers to. That's the cost of storing indices — and the benefit is that `stack.pop()` gives you exactly the slot to write into.

`while`, not `if` — one large value can resolve many pending indices at once.

`<` gives "next **strictly** greater," which is what the problem asks. With `<=` you'd get "next greater or equal," and equal elements would resolve each other — wrong here.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if i < n:
        stack.append(i)
```

**Push only on the first lap — the line that makes circularity correct.**

First-lap indices become pending questions. Second-lap elements are the same values seen again; they exist solely to answer leftovers. Pushing them would leave phantom entries and risk corrupting real answers.
→ [if-return](../syntax/if-return.md)

```python
return result
```

Anything the stack never resolved still holds its initial `-1` — no drain loop needed.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:

        n = len(nums)
        result = [-1] * n
        stack = []

        for i in range(2 * n):
            current = nums[i % n]

            while stack and nums[stack[-1]] < current:
                result[stack.pop()] = current

            if i < n:
                stack.append(i)

        return result
```

</details>

<details>
<summary>The array-duplication variant (simpler to explain)</summary>

```python
class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        doubled = nums + nums
        result = [-1] * n
        stack = []

        for i, current in enumerate(doubled):
            while stack and doubled[stack[-1]] < current:
                idx = stack.pop()
                if idx < n:
                    result[idx] = current
            stack.append(i)

        return result
```

Same idea, but the wrap is materialized rather than computed. The `if idx < n` guard replaces the push-guard. Costs O(n) extra memory; often easier to reason about on a whiteboard.

</details>

**Trace it** — `nums = [1, 2, 1]`, `n = 3`. Start: `result = [-1,-1,-1]`, `stack = []`.

| `i` | `i%n` | `current` | Stack before (indices) | Resolve | Push? | Stack after | `result` |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | `[]` | — | ✅ push 0 | `[0]` | `[-1,-1,-1]` |
| 1 | 1 | 2 | `[0]` | `nums[0]=1 < 2` → `result[0]=2`, pop | ✅ push 1 | `[1]` | `[2,-1,-1]` |
| 2 | 2 | 1 | `[1]` | `nums[1]=2 < 1`? no | ✅ push 2 | `[1,2]` | `[2,-1,-1]` |
| 3 | 0 | 1 | `[1,2]` | `nums[2]=1 < 1`? no | ❌ (`i >= n`) | `[1,2]` | `[2,-1,-1]` |
| 4 | 1 | 2 | `[1,2]` | `nums[2]=1 < 2` → `result[2]=2`, pop · then `nums[1]=2 < 2`? no | ❌ | `[1]` | `[2,-1,**2**]` |
| 5 | 2 | 1 | `[1]` | `nums[1]=2 < 1`? no | ❌ | `[1]` | `[2,-1,2]` |

Index 1 (value 2) is never resolved — nothing in the array exceeds it — so it keeps its `-1`.

Return **`[2, -1, 2]`** ✅

Row 4 is the payoff: the element at index 2 found its answer only by wrapping around, which is exactly what the second lap exists for. And rows 3–6 pushed nothing, keeping the stack clean.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The loop runs `2n` times — a constant factor, so O(n).
- The inner `while` is amortized: **at most `n` indices are ever pushed** (only first-lap iterations push), and each is popped at most once. Total pops ≤ `n`.

Total: O(2n) + O(n) = **O(n)**.

**Say it out loud like this:** *"It's two passes with an inner loop, but only n items are ever pushed and each pops once — so the total work is linear."*

**Compare to brute force:** O(n²) = 10⁸ at n = 10⁴, which in Python is seconds rather than milliseconds. The stack version is the intended solution.

Note the push-guard also *helps* the complexity argument: without it, up to `2n` items could be pushed, which is still O(n) — but the guard is about **correctness**, not speed. Don't conflate the two.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

- `result` — `n` entries (required output)
- `stack` — at most `n` indices, peaking on a strictly decreasing array like `[5,4,3,2,1]` where nothing resolves until the wrap

**O(n) auxiliary** for the stack, which is unavoidable — you must remember every pending element.

**The `% n` version versus duplication:**

| | Extra space |
|---|---|
| `% n` with `2n` loop | stack only — **O(n)** |
| `nums + nums` | stack + a copy — O(n), but ~2× the constant |

Same asymptotic class; the modular version simply avoids materializing the copy. At n = 10⁴ it's immaterial, but the technique — *simulate a circular array with modular indexing rather than duplicating it* — generalizes to cases where the array is huge or where copying isn't possible.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Same monotonic stack as Next Greater Element I, with two adjustments. First, duplicates are allowed, so the stack holds **indices** rather than values — a value no longer identifies a position, and indices are what I need to write into the result anyway. Second, the array is circular, so I loop `2n` times and index with `i % n`, which simulates a second lap without copying the array. The key detail is that I only **push** during the first lap — second-lap elements resolve pending questions but must not become pending themselves, or I'd leave phantom entries that could overwrite real answers. I preinitialize the result to −1 so unresolved positions need no cleanup. O(n) time, since at most n indices are pushed and each pops once, and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why loop exactly `2n`?" | The farthest an answer can be is a full lap, `n-1` positions. One extra pass covers it; a third adds nothing. |
| "Why not push on the second pass?" | Those indices would never be resolved and could overwrite correct answers with `-1` or wrong values. |
| "Why indices instead of values?" | Duplicates are allowed, so a value doesn't identify a position — and indices are what the result array needs. |
| "Circular **next smaller**?" | Flip the comparison to `>`; the stack becomes increasing. |
| "What if you wanted the next greater *or equal*?" | Use `<=` in the pop condition. |
| "Simpler version?" | Build `nums + nums`, run standard NGE, guard writes with `if idx < n`. O(n) extra memory, easier to explain. |
| "Circular maximum subarray?" | Different technique — [LeetCode 918](https://leetcode.com/problems/maximum-sum-circular-subarray/) uses Kadane twice (max, and total minus min). |

**Traps:**

- **Pushing on the second lap.** *The* bug for this problem. Produces phantom pending entries and corrupted answers.
- **Storing values instead of indices.** Breaks on duplicates like `[2,2]`, and gives you nowhere to write the result.
- **Forgetting `i % n`.** `IndexError` the moment `i` reaches `n`.
- **Draining the stack at the end and writing `-1` using `i % n`.** Easy to write to the wrong slots. Preinitialize instead.
- **Using `if` instead of `while`.** One element can resolve several pending indices.
- **Looping `3n` or more.** Harmless but pointless — and it signals you haven't reasoned about *why* two laps suffice.
- **Using `<=`** when the problem says strictly greater. Equal elements would wrongly resolve each other.

**This same move shows up in:** [Next Greater Element I](496-next-greater-element-i.md) (the non-circular original) · [Daily Temperatures](739-daily-temperatures.md) (monotonic stack of indices, computing distances) · [Online Stock Span](901-online-stock-span.md) (monotonic stack accumulating counts while popping) · [Concatenation of Array](1929-concatenation-of-array.md) (the "conceptually double the array" idea in its simplest form).

</details>

---
