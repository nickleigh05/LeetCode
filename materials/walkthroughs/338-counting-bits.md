# 338. Counting Bits

**Easy** · [LeetCode](https://leetcode.com/problems/counting-bits/) · [Solution file (no hints)](../../problems/0001-0499/338.py)

[📖 19. Bit Manipulation lesson](../learning/19-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Bit Manipulation problems](../rmap-practice/19-bit-manipulation.md)

---

Given an integer `n`, return an array `ans` of length `n + 1` where, for each `i` from 0 to `n`, `ans[i]` is the **number of 1 bits** in the binary representation of `i`.

The follow-up asks for **O(n)** time using a single pass, **without** using any built-in popcount function.

```
n = 2   →  [0,1,1]
        0 → 0     1 → 1     10 → 1

n = 5   →  [0,1,1,2,1,2]
        0 → 0   1 → 1   10 → 1   11 → 2   100 → 1   101 → 2
```

**Constraints:** `0 <= n <= 10⁵`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| for **every** `i` from 0 to n | You're not answering one query — you're building a table. **Earlier answers can feed later ones** |
| count of 1 bits | Same quantity as [Number of 1 Bits](191-number-of-1-bits.md), but computed n + 1 times |
| follow-up wants **O(n)** | Calling a per-number counter is O(n log n). The follow-up is the actual problem |
| "without built-in popcount" | Rules out `bin(i).count('1')` and `int.bit_count()` |
| `n <= 10⁵` | Even O(n log n) would pass. So this is graded on **finding the recurrence**, not on speed |

The baseline is to call [Kernighan's trick](191-number-of-1-bits.md) once per number: **O(n log n)** total, since each call costs up to log n. That works and it's the answer if you stop thinking.

But the phrase "for every `i` from 0 to n" is a strong hint. **When you're computing an answer for every value in a range, look for a way to build each answer from a smaller one** — that's the DP instinct, and it applies here even though the problem is tagged bit manipulation.

So: **how does the bit count of `i` relate to the bit count of some smaller number?**

Look at what `i >> 1` (integer division by 2) does to a binary number — it drops the **lowest bit**:

```
i  = 13 = 1101
i >> 1 =  110  = 6
```

The bits of `13` are exactly the bits of `6` **plus** whatever the dropped bit was. So:

```
bits(i) = bits(i >> 1) + (lowest bit of i)
```

The lowest bit is `i & 1`, or equivalently `i % 2`. Which gives:

```
bits(i) = bits(i // 2) + (i % 2)
```

Check it: `bits(13) = bits(6) + 1`. And `bits(6) = bits(3) + 0`, `bits(3) = bits(1) + 1`, `bits(1) = bits(0) + 1 = 1`. So `bits(3) = 2`, `bits(6) = 2`, `bits(13) = 3` — and `1101` does have three 1s ✓

**Every answer depends on a strictly smaller index**, so filling the array left to right means the value you need is always already computed. **O(1) per number, O(n) overall.**

🤔 **Before you open the next section:** `i // 2` is always strictly less than `i` for `i >= 1`. Why does that guarantee the left-to-right fill is safe — and what's the one index that can't use the recurrence?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `bin(i).count("1")` per number | String conversion for each | O(n log n) | O(n) | ❌ Explicitly excluded by the follow-up |
| [Kernighan's](191-number-of-1-bits.md) per number | Clear the lowest set bit repeatedly | **O(n log n)** | O(n) | ⚠️ Correct and passes — but it's the baseline the follow-up wants beaten |
| **DP on `i >> 1`** | `bits(i) = bits(i // 2) + (i & 1)` | **O(n)** | O(n) | ✅ |
| DP on `i & (i - 1)` | `bits(i) = bits(i & (i-1)) + 1` | **O(n)** | O(n) | ✅ Equally good — a different recurrence, same bound |
| DP on the highest power of two | `bits(i) = bits(i - 2^k) + 1` where `2^k <= i` | O(n) | O(n) | ✅ Correct, but needs tracking of the current power |

**The decision:** **the `i >> 1` recurrence** — `ans[i] = ans[i // 2] + (i % 2)`.

**Why the DP beats calling a counter per number.** Kernighan's per number is O(log n) each, so O(n log n) total. The recurrence makes each answer **O(1)** by reusing work already done. **That's the classic DP trade: don't recompute what a smaller subproblem already established.**

And the reuse is genuine, not incidental. The bits of `13` literally *contain* the bits of `6` — dropping the last bit is a lossless-except-one-bit operation, so `bits(6)` is exactly the part of the answer you don't need to recompute.

**Two equally valid recurrences**, worth knowing both:

| Recurrence | Reasoning |
|---|---|
| `ans[i] = ans[i >> 1] + (i & 1)` | Drop the **lowest bit**; add it back if it was 1 |
| `ans[i] = ans[i & (i - 1)] + 1` | Clear the **lowest set bit** ([Kernighan's](191-number-of-1-bits.md)); that's always exactly one bit, so add 1 |

The second is arguably more elegant — the `+ 1` is unconditional, no parity test needed — and it reuses the identity from problem 191. The first is more intuitive if you think in terms of halving. **Both are O(n); pick either and mention the other.**

**Why the base case is index 0** — the answer to section 1's second question. `bits(0) = 0`, and it's the one value the recurrence can't produce: `0 // 2` is `0`, so it would depend on itself. The zero-initialized array supplies it for free, which is why the loop starts at 1.

**Why the left-to-right fill is safe.** For any `i >= 1`, `i // 2 < i` strictly. So when the loop reaches index `i`, index `i // 2` was filled on an earlier iteration. **No forward references, no ordering hazard** — the same guarantee that makes bottom-up DP work in [Climbing Stairs](70-climbing-stairs.md).

**Is this really DP or bit manipulation?** Both, and that's the interesting part. The *recurrence* is DP; the *insight that produces it* is bitwise. **Recognizing that a bit-manipulation problem has overlapping subproblems is the whole move here.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
ans = [0] * (n + 1)
```
The output array, **`n + 1`** long because indices run from 0 to `n` **inclusive**.

Initializing to zeros does double duty: it allocates the array *and* supplies the base case, since `ans[0] = 0` is exactly correct — zero has no set bits. **No separate base-case assignment is needed.**
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(1, n + 1):
```
Fill from **1** upward. Index 0 is already correct, and it's the only index the recurrence can't handle — `0 // 2` is `0`, so applying it there would be circular.

Ascending order is what makes the recurrence valid: `i // 2 < i` for every `i >= 1`, so the value being read has always already been written.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    ans[i] = ans[i // 2] + (i % 2)
```
**The recurrence, and the whole algorithm.**

Two pieces:

- **`ans[i // 2]`** — the bit count of `i` with its lowest bit removed. [Floor division](../syntax/integer-division-modulo.md) by 2 is a right shift, which discards the last binary digit. This value is already computed.
- **`i % 2`** — the bit that was discarded: **1** if `i` is odd, **0** if even. Adds it back.

So the line reads: *"the bits of `i` are the bits of `i` without its last digit, plus that digit."*

**Equivalent bitwise phrasing:** `ans[i >> 1] + (i & 1)`. `>>` and `&` express the intent more directly in bit terms, while `//` and `%` may read more clearly. **Identical behaviour for non-negative integers** — pick whichever you find more legible and be able to explain the other.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [bitwise-operators](../syntax/bitwise-operators.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return ans
```
Every index from 0 to `n` holds its bit count.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def countBits(self, n: int) -> List[int]:

        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            ans[i] = ans[i // 2] + (i % 2)
        return ans
```
</details>

**Trace it** — `n = 8`

| `i` | binary | `i // 2` | `ans[i // 2]` | `i % 2` | `ans[i]` |
|---|---|---|---|---|---|
| 0 | `0` | — | — | — | **0** (base case) |
| 1 | `1` | 0 | 0 | **1** | **1** |
| 2 | `10` | 1 | **1** | 0 | **1** |
| 3 | `11` | 1 | **1** | **1** | **2** |
| 4 | `100` | 2 | **1** | 0 | **1** |
| 5 | `101` | 2 | **1** | **1** | **2** |
| 6 | `110` | 3 | **2** | 0 | **2** |
| 7 | `111` | 3 | **2** | **1** | **3** |
| 8 | `1000` | 4 | **1** | 0 | **1** |

Return **[0,1,1,2,1,2,2,3,1]** ✅

Two patterns are worth seeing in that table.

**Even numbers inherit exactly.** `ans[4] = ans[2] = 1`, and `ans[8] = ans[4] = 1`. Doubling a number **shifts its bits left and appends a 0**, which doesn't change the count — so every power of two has exactly one set bit, inherited unchanged all the way down to `ans[1]`.

**Odd numbers are their predecessor plus one.** `ans[7] = ans[3] + 1 = 3`, because `111` is `11` with a 1 appended. Note that `i // 2` is the same for `2k` and `2k+1` — rows 6 and 7 both read `ans[3]` — so consecutive pairs differ only by the parity term.

**And the given example** — `n = 5` gives `[0,1,1,2,1,2]` ✅, the first six entries of the table above.

**Comparing the work:** computing `ans[7] = 3` took **one addition**. Kernighan's would have taken **three** iterations for that same number, and the savings compound across all n numbers — which is exactly the O(n log n) → O(n) improvement.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The loop runs **n** times, once per index from 1 to n.
- Each iteration does one division, one modulo, one array read, one addition, and one array write — all **O(1)**.
- **O(n)** total.

At n = 10⁵ that's a hundred thousand constant-time steps. Instant.

**Against the baseline:** calling [Kernighan's](191-number-of-1-bits.md) per number costs O(log i) for each `i`, so the total is **O(n log n)** — around 1.7 × 10⁶ operations at n = 10⁵. Both pass comfortably here, but the follow-up asks specifically for the linear version, and the gap is real: **17× fewer operations**.

**Where the saving comes from:** the per-number approach recomputes shared structure. Counting the bits of 13 walks its bits, then counting 26 (`11010`) walks *almost the same bits again*. The recurrence recognizes that `bits(26) = bits(13) + 0` and does one addition instead. **Overlapping subproblems, which is exactly the DP condition** — and it's what makes an ostensibly bit-manipulation problem yield to a DP technique.

**Faster?** No. The output has n + 1 entries, so **Ω(n)** is a floor — you can't produce n values in less than n time. O(n) is optimal.

**One pass, as the follow-up requires** — there's no preprocessing, no second sweep, and each entry is written exactly once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) output, O(1) auxiliary</summary>

**O(n)** for the output array; **O(1)** extra.

| Component | Space | Why |
|---|---|---|
| `ans` | **O(n)** *output* | n + 1 entries — required by the problem, not auxiliary |
| Loop index | O(1) | One integer |

So the honest statement is **O(n) including the output, O(1) auxiliary** — and there's no way around the output size, since the problem asks for n + 1 values.

**What makes this unusual among DP problems:** normally the DP table is *extra* space you'd like to eliminate — [Climbing Stairs](70-climbing-stairs.md) collapses its array to two variables, [Unique Paths](62-unique-paths.md) to one row. **Here the table *is* the answer**, so there's nothing to collapse. The array you'd want to optimize away is the thing being returned.

**And note the recurrence couldn't collapse anyway.** `ans[i]` reads `ans[i // 2]`, which can be arbitrarily far back — `ans[100000]` reads `ans[50000]`. **The lookback distance isn't bounded by a constant**, so the rolling-variable trick from Unit 13 doesn't apply, exactly as in [Coin Change](322-coin-change.md).

**No auxiliary structures at all** — no set, no stack, no recursion. The array is written in a single forward pass with each entry touched once.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The baseline is calling a bit-counter on each number — Kernighan's trick, say — which is O(n log n). But since I need the answer for *every* number in a range, I should look for a way to build each from a smaller one. Right-shifting `i` by one drops its lowest bit, so the bits of `i` are the bits of `i >> 1` plus that dropped bit: `ans[i] = ans[i // 2] + (i % 2)`. Every index depends on a strictly smaller one, so filling left to right means the value I need is always already there. Index 0 is the base case — it's the one the recurrence can't produce, since `0 // 2` is 0 — and the zero-initialized array supplies it for free. That's O(1) per number, O(n) overall, which is what the follow-up asks for. An equivalent recurrence is `ans[i] = ans[i & (i-1)] + 1`, using the fact that clearing the lowest set bit always removes exactly one."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `ans[i // 2]` help?" | Halving is a right shift, which drops the lowest bit. So `i` has all of `i//2`'s bits plus possibly one more — and that one is `i % 2`. |
| "Is there another recurrence?" | Yes: `ans[i] = ans[i & (i - 1)] + 1`. Clearing the lowest set bit always removes exactly one bit, so the `+1` is unconditional — no parity test. |
| "Why start the loop at 1?" | `ans[0] = 0` is the base case, and it's the only index the recurrence can't handle — `0 // 2` is 0, so it would depend on itself. |
| "Why is the left-to-right fill safe?" | `i // 2 < i` strictly for every `i >= 1`, so the dependency is always at a smaller, already-filled index. |
| "Can you use less space?" | Not below O(n) — the output is n + 1 values. And the recurrence couldn't collapse to variables anyway, since `ans[i]` may read an index far behind it. |
| "Why is a bit problem solved with DP?" | Because the answers overlap: the bits of 26 contain the bits of 13. Overlapping subproblems is the DP condition, whatever the problem is tagged. |
| "What if you only needed one number's count?" | Then there's nothing to reuse — use [Kernighan's](191-number-of-1-bits.md), O(log n) with O(1) space. |
| "What patterns show up in the output?" | Powers of two are always 1; `ans[2k] == ans[k]` since doubling appends a zero; `ans[2k+1] == ans[k] + 1`. The sequence is sometimes drawn as a fractal doubling pattern. |

**Traps:**
- **Sizing the array `n` instead of `n + 1`** — indices run 0 through n inclusive, so the last entry would be missing.
- **Starting the loop at 0** — `ans[0] = ans[0] + 0` is harmless here but circular in principle, and it signals not knowing where the base case comes from.
- Using `bin(i).count('1')` — explicitly ruled out by the follow-up, and O(n log n).
- Mixing up `i >> 1` with `i << 1` — the latter doubles rather than halves and would index out of range.
- Writing `ans[i] = ans[i // 2] + 1` unconditionally — that would count a bit for even numbers too. The parity term is essential.
- Trying to collapse the array to rolling variables. The dependency reaches back arbitrarily far.

**This same move shows up in:** [Number of 1 Bits](191-number-of-1-bits.md) (counting bits for a single number, where there's nothing to reuse) · [Climbing Stairs](70-climbing-stairs.md) (a bottom-up fill where each answer builds on smaller ones) · [Coin Change](322-coin-change.md) (a DP array that can't collapse because the lookback isn't bounded) · [Single Number](136-single-number.md) (a bitwise identity doing the work of explicit bookkeeping).

</details>

---
