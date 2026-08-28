# 496. Next Greater Element I

**Easy** · [LeetCode](https://leetcode.com/problems/next-greater-element-i/) · [Solution file (no hints)](../../problems/0001-0499/496.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

`nums1` is a subset of `nums2`, and both have **distinct** elements. For each `nums1[i]`, find its **next greater element** in `nums2` — the first element to its right that is larger. Return an array of those values, using `-1` where none exists.

```
nums1 = [4,1,2], nums2 = [1,3,4,2]  →  [-1, 3, -1]
nums1 = [2,4],   nums2 = [1,2,3,4]  →  [3, -1]
```

**Constraints:** `1 <= nums1.length <= nums2.length <= 1000` · `0 <= nums[i] <= 10⁴` · all integers **unique** · every `nums1[i]` appears in `nums2`

**Follow-up:** can you do it in O(n + m)?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**next greater** to its right" | ⚠️ The signature phrase for a **monotonic stack** — learn to hear it |
| "all elements are **distinct**" | No tie-handling; `<` vs `<=` in the comparison won't bite you here |
| "`nums1` is a **subset** of `nums2`" | Solve the problem for **all** of `nums2` once, then look up the answers |
| "`-1` if none exists" | Elements with nothing larger to their right need an explicit default |
| follow-up: **O(n + m)** | Rules out the O(n·m) nested scan |
| `n, m <= 1000` | Brute force (10⁶) would pass — but the follow-up is the actual question |

**The first structural insight:** `nums1` is just a *query list*. The real work is computing the next greater element for every position in `nums2`, storing those in a map, and then answering each query with an O(1) lookup. Don't search `nums2` once per element of `nums1` — that's the O(n·m) trap.

**The second, and the heart of it:** how do you find every next-greater in one pass?

Walk `nums2` left to right, keeping a **stack of elements still waiting for their answer**. When a new element arrives, it is the next greater element for *every* pending element smaller than it — so pop them all and record the answer.

```
nums2 = [1, 3, 4, 2]

see 1  → stack [1]              (1 is waiting)
see 3  → 3 > 1, so 1's answer is 3. pop.  stack [3]
see 4  → 4 > 3, so 3's answer is 4. pop.  stack [4]
see 2  → 2 < 4, nothing resolved.         stack [4, 2]
end    → 4 and 2 never resolved → -1
```

The stack stays **decreasing** from bottom to top — that's the invariant, and it's what makes the algorithm work. Anything that would break it gets popped, and the act of popping is exactly the act of answering.

🤔 **Before you open the next section:** if the stack holds elements still waiting for a bigger number, why must those elements always be in decreasing order?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n = |nums1|`, `m = |nums2|`.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each `nums1[i]`, find it in `nums2`, then scan right | O(n · m) | O(1) | ⚠️ Passes at 10⁶, fails the follow-up |
| Index map + scan right | Map values to indices, then scan | O(n · m) | O(m) | ⚠️ Same bound |
| **Monotonic stack + map** | One pass over `nums2` resolving answers | **O(n + m)** | O(m) | ✅ |

**The decision: a [monotonic stack](../data-structures/monotonic-stack.md) over `nums2`, feeding a value → answer map.**

The stack is **monotonically decreasing** from bottom to top. Two rules maintain it, and both carry meaning:

1. **Before pushing `x`, pop everything smaller than `x`.** Each popped element has just found its next greater element — it's `x`. Record it.
2. **Push `x`.** It now waits for something bigger.

**Why decreasing is the correct invariant.** Suppose the stack held `[3, 5]` with 5 on top. Then 3 sits *below* 5 and appeared *earlier* — but 5 is to 3's right and is larger, so 3's answer would already be 5 and it should have been popped. The presence of a smaller element beneath a larger one is impossible by construction. So the stack is always decreasing, and that's precisely why a single `while` pop-loop resolves everything correctly.

**Why anything left at the end gets `-1`.** Elements still on the stack were never exceeded by anything to their right — that's the definition of having no next greater element.

**Why the map, not indices?** Because values are **distinct**, a value uniquely identifies a position, so you can key the map by value directly and skip index bookkeeping entirely. If duplicates were allowed you'd have to store *indices* on the stack and key results by index — which is exactly what [Daily Temperatures](739-daily-temperatures.md) does.

**Why is it O(m) and not O(m²) despite the nested `while`?** The amortized argument: **each element is pushed exactly once and popped at most once**, so total stack operations across the whole run are bounded by `2m`. The inner loop's total work is O(m), not O(m) per iteration. This is the same accounting as in [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) and every sliding-window problem — a nested loop with a global budget.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
next_greater_map = {}
stack = []
```

- `next_greater_map` — value → its next greater element in `nums2`
- `stack` — values still **waiting** for an answer, kept decreasing bottom-to-top

→ [dict-basics](../syntax/dict-basics.md) · [list-basics](../syntax/list-basics.md)

```python
for current_num in nums2:
    while stack and stack[-1] < current_num:
        smaller_num = stack.pop()
        next_greater_map[smaller_num] = current_num
```

**The engine.** `current_num` resolves every pending element smaller than itself.

`while`, not `if` — one large value can resolve **many** waiting elements at once. On `[5,4,3,10]`, the `10` pops 3, 4, and 5 in a single burst.

`stack and ...` short-circuits so `stack[-1]` is never evaluated on an empty stack.

Because elements are distinct, `<` and `<=` behave identically here. (With duplicates the choice matters: `<` gives "next *strictly* greater," `<=` gives "next greater *or equal*" — worth knowing which you want.)
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [list-methods](../syntax/list-methods.md)

```python
    stack.append(current_num)
```

Push the current value; it now waits for something larger.

```python
while stack:
    remaining_num = stack.pop()
    next_greater_map[remaining_num] = -1
```

**Cleanup.** Anything still waiting when `nums2` is exhausted has no next greater element.

(An alternative is to skip this loop and use `next_greater_map.get(num, -1)` at lookup time — same result, one less pass. Both are fine; the explicit drain makes the "no answer" case visible.)

```python
result = []
for num in nums1:
    result.append(next_greater_map[num])
return result
```

**Answer the queries.** Each is an O(1) map lookup — this is where the "solve for all of `nums2` once" decision pays off.

Equivalent one-liner: `return [next_greater_map[num] for num in nums1]`.
→ [list-comprehension](../syntax/list-comprehension.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:

        next_greater_map = {}
        stack = []

        for current_num in nums2:
            while stack and stack[-1] < current_num:
                smaller_num = stack.pop()
                next_greater_map[smaller_num] = current_num
            stack.append(current_num)

        while stack:
            remaining_num = stack.pop()
            next_greater_map[remaining_num] = -1

        result = []
        for num in nums1:
            result.append(next_greater_map[num])

        return result
```

</details>

**Trace it** — `nums2 = [1, 3, 4, 2]`:

| `current_num` | Stack before | Pops (answer recorded) | Stack after |
|---|---|---|---|
| 1 | `[]` | — | `[1]` |
| 3 | `[1]` | pop 1 → `map[1] = 3` | `[3]` |
| 4 | `[3]` | pop 3 → `map[3] = 4` | `[4]` |
| 2 | `[4]` | none (2 < 4) | `[4, 2]` |
| *drain* | `[4, 2]` | pop 2 → `map[2] = -1`; pop 4 → `map[4] = -1` | `[]` |

Final map: `{1: 3, 3: 4, 2: -1, 4: -1}`

Queries for `nums1 = [4, 1, 2]`:

| Query | Lookup | Result |
|---|---|---|
| 4 | `map[4]` | **−1** |
| 1 | `map[1]` | **3** |
| 2 | `map[2]` | **−1** |

Return **`[-1, 3, -1]`** ✅

Notice the stack was decreasing at every step (`[4, 2]` at the end), and the total pops across the run were 4 — one per element, exactly as the amortized argument predicts.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, meeting the follow-up.

- Main loop over `nums2`: `m` iterations. The inner `while` is amortized — **each element is pushed once and popped at most once**, so total pops ≤ `m` across the entire run.
- Drain loop: at most `m` pops.
- Query loop over `nums1`: `n` O(1) lookups.

Total: O(m) + O(m) + O(n) = **O(n + m)**.

**Say it out loud like this:** *"The nested `while` doesn't make it quadratic — every element enters the stack once and leaves once, so total inner work is bounded by m."*

**Compare to brute force:** O(n · m) = 10⁶ at the limits. It would pass, but the follow-up explicitly asks you to beat it, and the monotonic stack is the intended answer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m).**

- The map holds one entry per element of `nums2` — up to `m`.
- The stack holds at most `m` elements (all of `nums2`, if strictly decreasing, e.g. `[5,4,3,2,1]`).

The output is `O(n)`, but that's required by the problem.

**The trade:** brute force is O(1) space and O(n·m) time; this is O(m) space and O(n+m) time. Standard, and clearly worth it.

**Where the memory goes conceptually:** the stack is holding *unanswered questions*. Each element sits there until something larger arrives to answer it — so the stack's depth is "how many elements are currently waiting," which peaks when the input is strictly decreasing and nothing ever gets resolved until the end.

That framing — **a monotonic stack stores pending obligations** — is the intuition that makes [Daily Temperatures](739-daily-temperatures.md), [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md), and [Online Stock Span](901-online-stock-span.md) all feel like the same problem.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "'Next greater element to the right' is the signature of a monotonic stack. Rather than searching per query, I solve it for all of `nums2` in one pass and store the answers in a map, since `nums1` is a subset and the values are distinct. I keep a stack of elements still waiting for a bigger number, which stays decreasing bottom-to-top. When a new element arrives, it's the answer for every pending element smaller than it, so I pop those and record it. Whatever's left at the end gets −1. Then each `nums1` query is an O(1) lookup. It's O(n + m) because every element is pushed once and popped once, and O(m) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the array is **circular**?" | [Next Greater Element II](503-next-greater-element-ii.md) — iterate `2n` times using `i % n`, and don't push on the second pass. |
| "What if there are **duplicates**?" | Keys can't be values any more — push **indices** on the stack and index the result array. That's [Daily Temperatures](739-daily-temperatures.md). |
| "Next **smaller** element?" | Flip the comparison to `>`; the stack becomes monotonically increasing. |
| "Next greater to the **left**?" | Iterate right-to-left with the same machinery. |
| "Why is the stack decreasing?" | If a smaller element sat below a larger one, it would already have been resolved by that larger one. Impossible by construction. |
| "Why isn't the nested loop O(m²)?" | Amortized: each element is pushed once, popped once — total pops ≤ m. |
| "Can you skip the drain loop?" | Yes — use `map.get(num, -1)` when answering queries. |

**Traps:**

- **Searching `nums2` once per `nums1` element.** The O(n·m) trap. Solve for all of `nums2` once, then look up.
- **Using `if` instead of `while`.** One element can resolve many pending ones; `if` resolves only the top and leaves the rest permanently wrong.
- **Forgetting the `-1` default.** Elements never resolved must still appear in the map (or use `.get`).
- **Checking `stack[-1]` before testing `stack`.** `IndexError` on the first element. Order the `and` correctly.
- **Storing values when duplicates are possible.** Fine here because elements are distinct — but don't carry the habit to problems where they aren't.
- **Pushing before popping.** The new element would immediately compare against itself.

**This same move shows up in:** [Daily Temperatures](739-daily-temperatures.md) (the same monotonic stack, storing indices to compute distances) · [Next Greater Element II](503-next-greater-element-ii.md) (the circular version) · [Online Stock Span](901-online-stock-span.md) (a monotonic stack that accumulates spans as it pops) · [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (the Hard application of the same structure).

</details>

---
