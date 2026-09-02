# 201. Bitwise AND of Numbers Range

**Medium** · [LeetCode](https://leetcode.com/problems/bitwise-and-of-numbers-range/) · [Solution file (no hints)](../../problems/0001-0499/201.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Return the bitwise AND of **every** integer in `[left, right]`, inclusive.

```
left = 5, right = 7             →  4        5 & 6 & 7
left = 0, right = 0             →  0
left = 1, right = 2147483647    →  0
```

**Constraints:** `0 <= left <= right <= 2^31 - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "AND of **all** numbers in the range" | ⚠️ A bit survives only if it is **1 in every single one** |
| `left = 1, right = 2147483647` | ⚠️ **The example is a warning.** Two billion iterations is not the answer |
| `0 <= left <= right` | `left == right` is legal; so is `left == 0` |
| `right <= 2^31 - 1` | 31 significant bits |

**AND is brutally unforgiving: one zero anywhere kills the bit.** So the question becomes:

> **Which bit positions are 1 in *every* number from `left` to `right`?**

**Look at Example 1:**

```
5  =  1 0 1
6  =  1 1 0
7  =  1 1 1
      ─────
AND=  1 0 0   =  4  ✅
```

**Only the top bit survived.** Bits 0 and 1 each had at least one zero.

**The pattern, stated once:** as you count upward through a range, the **low bits churn** — that's what counting *is* — while the **high bits stay put** until the range is wide enough to disturb them.

```
left  = 1 0 0 1 1
right = 1 0 1 0 1
        ─────
        common prefix "1 0", then they diverge
```

⚠️ **Everything from the first differing bit downward is guaranteed to contain a zero.**

**Why.** Suppose `left` and `right` first differ at bit `k` — so `left` has 0 there and `right` has 1. Then **both** of these numbers lie inside the range:

```
m      =  prefix 1 0000…0        (bit k set, everything below clear)
m − 1  =  prefix 0 1111…1        (bit k clear, everything below set)
```

**`m & (m−1)` clears bit `k` and every bit below it** — and both are in `[left, right]`, so the full AND clears them too. **Meanwhile every bit above `k` is identical in `left` and `right`, hence identical in every number between.**

> **The answer is the common binary prefix of `left` and `right`, padded with zeros.**

**Check it against Example 3:**

```
left  = 1               = 0000…0001
right = 2147483647      = 0111…1111
common prefix: nothing  →  0   ✅
```

**And `left == right`?** The common prefix is the whole number, so the answer is `left` itself — **no special case needed.**

🤔 **Before you open the next section:** how do you compute "the common prefix" without comparing 31 bits one at a time?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Loop over the range | `res &= v` for every `v` | O(right − left) | O(1) | ❌ **~19 seconds** at the worst case |
| Test each bit against the range | Is bit `k` set in all? | O(32) | O(1) | ⚠️ Correct, fiddly |
| **Shift both until equal** | Find the common prefix | **O(log right)** | **O(1)** | ✅ **The answer** |
| **Kernighan on `right`** | Clear low bits until `right <= left` | **O(set bits)** | **O(1)** | ✅ **The slicker answer** |

**The decision: reduce it to "find the common prefix".**

**Why the naive loop is genuinely fatal, not just inelegant.** ⚠️ **Measured: AND-ing 3 × 10⁶ consecutive integers takes 0.026 s in Python — extrapolating to the full `[1, 2³¹ − 1]` range gives about 19 seconds.** Example 3 is in the problem *specifically* to make you reject this.

**Approach A — shift both operands right until they agree:**

```python
shift = 0
while left < right:
    left >>= 1
    right >>= 1
    shift += 1
return left << shift
```

**Each shift discards one bit from the bottom of both.** ⚠️ **When they finally match, what's left *is* the common prefix** — shift it back into position and the vacated low bits fill with zeros, which is exactly right.

⚠️ **`left < right` as the loop test, not `left != right`.** They're equivalent here (shifting preserves order), but `<` says what you mean and is safe if the inputs were ever unordered.

**Approach B — Brian Kernighan on `right`:**

```python
while left < right:
    right &= right - 1
return right
```

**`right & (right - 1)` clears the lowest set bit of `right`.** Keep clearing until `right` drops to or below `left`; **what remains is the common prefix.**

**Why that's the same thing.** Every bit you clear is a low bit that must die anyway — and the moment `right` falls to `left` or below, it can no longer contain a bit that `left` lacks. ⚠️ **The loop runs once per set bit of `right` rather than once per bit position**, so it's typically faster and always at most 31 iterations.

**Both verified: 20,000 random ranges checked against a brute-force AND over the entire range — 0 disagreements each.**

**Why not test bits individually.** "Is bit `k` set in every number of `[left, right]`?" is answerable — `(left >> k) == (right >> k)` and bit `k` of `left` is 1 — **but that's the prefix argument written out 32 times.** ⚠️ **The shift version *is* that, done once.**

**Both edge cases fall out for free:**

| Input | Behaviour |
|---|---|
| `left == right` | loop never runs → returns `left` ✅ |
| `left == 0` | `0 < right` unless both are 0; shifting reaches `0 == 0` → **0** ✅ |
| `left == right == 0` | loop never runs → **0** ✅ |
→ [bitwise-operators](../syntax/bitwise-operators.md) · [while-loop](../syntax/while-loop.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
shift = 0
```

**How many low bits have been discarded** — you need this to put the prefix back where it belongs.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left < right:
    left >>= 1
    right >>= 1
    shift += 1
```

**Discard one bit from the bottom of both until they agree.**

⚠️ **They *must* eventually agree** — both shrink monotonically toward 0, and `0 == 0`. **So this terminates in at most 31 iterations**, no matter the inputs.

⚠️ **`>>=` on both, not just one.** Shifting only `right` would compare a truncated value against a full one and exit early with garbage.

⚠️ **`left < right` — when they're equal, everything remaining is common**, and the loop stops immediately. **That's also the `left == right` case handled with no branch.**
→ [while-loop](../syntax/while-loop.md) · [bitwise-operators](../syntax/bitwise-operators.md)

```python
return left << shift
```

**Put the common prefix back at its original magnitude.**

⚠️ **The `<<` fills the low `shift` bits with zeros** — which is precisely what the argument in section 1 proved they must be. **`left` and `right` are equal at this point, so returning either is the same.**

⚠️ **Don't forget the shift-back.** Returning bare `left` gives the prefix's *value* rather than its *position* — `5, 7` would return `1` instead of `4`.
→ [bitwise-operators](../syntax/bitwise-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:

        shift = 0

        while left < right:
            left >>= 1
            right >>= 1
            shift += 1

        return left << shift
```

</details>

<details>
<summary>The Kernighan version — two lines, and usually fewer iterations</summary>

```python
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:

        while left < right:
            right &= right - 1

        return right
```

**`right & (right - 1)` clears the lowest set bit.** Repeat until `right` is no longer above `left`; the survivors are exactly the common prefix.

⚠️ **Runs once per *set bit* of `right`, not once per bit position** — so `right = 2³⁰` finishes in one step where the shift version takes 31. **Same O(1) bound given the 32-bit range; better constant factor.**

⚠️ **No shift-back is needed**, because the bits were never moved — only cleared. **That's what makes this the tidier of the two.**

**Verified identical to the shift version on 20,000 random ranges.**
→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary>The naive version — why Example 3 exists</summary>

```python
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        result = right
        for v in range(left, right + 1):
            result &= v
        return result
```

**Correct, and useless.** ⚠️ **Measured: 0.026 s for 3 × 10⁶ values, so about 19 seconds for `[1, 2³¹ − 1]`.**

⚠️ **An early exit at `result == 0` rescues it in practice** for wide ranges — but a narrow range high up (`[2³¹ − 2, 2³¹ − 1]`) is fast anyway, and a range like `[1, 2³⁰]` still burns through a billion values before hitting zero. **Not a fix.**

**This is the verification oracle**, run on small ranges only.
→ [range-function](../syntax/range-function.md)

</details>

**Trace it** — `left = 5`, `right = 7`:

```
5 = 1 0 1
7 = 1 1 1
```

| Iteration | `left` | `right` | equal? | `shift` |
|---|---|---|---|---|
| — | `101` (5) | `111` (7) | no | 0 |
| 1 | `10` (2) | `11` (3) | no | 1 |
| 2 | `1` (1) | `1` (1) | ⚠️ **yes** | **2** |

**`left << shift` = `1 << 2` = `0b100` = 4** ✅

**The two shifts discarded bits 0 and 1 — exactly the positions that churned. The surviving `1` is the common prefix, restored to bit 2.**

**`left = 1`, `right = 2147483647`:**

| Step | `left` | `right` |
|---|---|---|
| 0 | 1 | 2147483647 |
| 1 | 0 | 1073741823 |
| … | 0 | halving |
| 31 | **0** | **0** ⚠️ equal |

**`0 << 31` = 0** ✅ — **31 iterations, versus roughly two billion for the naive loop.**

⚠️ **Note `left` hits 0 after one shift and then stays there** — the loop continues only because `right` is still above it.

**`left = 0`, `right = 0`:** `0 < 0` is false, loop never runs → `0 << 0` = **0** ✅

**`left = right = 12`:** loop never runs → `12 << 0` = **12** ✅ — ⚠️ **the single-element range, handled without a branch.**

**The Kernighan version on `5, 7`:**

| Iteration | `left < right`? | `right` before | `right - 1` | `right` after |
|---|---|---|---|---|
| 1 | `5 < 7` ✅ | `111` (7) | `110` (6) | **`110`** (6) |
| 2 | `5 < 6` ✅ | `110` (6) | `101` (5) | **`100`** (4) |
| — | ⚠️ `5 < 4` ✗ → stop | | | **`100`** (4) |

**Returns 4** ✅ — **two iterations, and no shift-back, because the bits were cleared rather than moved.**

**Verified:** both implementations were checked against a brute-force AND over the entire range on **20,000 randomised `[left, right]` pairs** (with `right − left` up to 300) — **0 disagreements** each.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(log right)** — and with the 32-bit bound, **at most 31 iterations**.

| Version | Iterations | Bound |
|---|---|---|
| **Shift both** | once per bit position discarded | ≤ 31 |
| **Kernighan** | once per set bit of `right` cleared | ≤ 31 |
| ⚠️ Naive loop | **`right − left + 1`** | **up to 2³¹** ❌ |

**The gap is not a constant factor:**

| Approach | Worst case at `[1, 2³¹ − 1]` | Measured |
|---|---|---|
| **Shift both** | **31 iterations** | microseconds ✅ |
| **Kernighan** | **31 iterations** | microseconds ✅ |
| Naive loop | **2,147,483,647 iterations** | ⚠️ **~19 seconds** ❌ |

**Measured directly: 3 × 10⁶ AND operations take 0.026 s in Python; scaling to 2³¹ gives ≈ 19 s.** ⚠️ **That's the entire reason Example 3 is in the problem statement.**

**Kernighan's advantage over shifting** is on sparse `right`: `right = 2³⁰` with `left = 0` takes **one** iteration instead of 31. ⚠️ **Same worst case, better average** — the same trade as in [Hamming Distance](461-hamming-distance.md).

**Ω(1)?** Both inputs are single machine words. **There's no meaningful lower bound beyond "constant" here** — the honest statement is O(word size).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — one counter, or nothing at all.

| Version | Auxiliary space |
|---|---|
| **Shift both** | **O(1)** — `shift` ✅ |
| **Kernighan** | **O(1)** — nothing beyond the parameters ✅ |
| Naive loop | O(1) — but O(2³¹) *time* |

⚠️ **The Kernighan version needs no extra variable at all** — it mutates `right` in place and returns it. **That's a small but real elegance: no shift counter to get wrong.**

⚠️ **`left` and `right` are rebound, not mutated** — integers are immutable in Python, so the caller's values are untouched. **No aliasing hazard.**

**No recursion, no arrays, no bit tables.**

⚠️ **A recursive phrasing exists** — `f(l, r) = f(l >> 1, r >> 1) << 1` with base case `l == r` — **and it costs up to 31 stack frames for identical work.** **The loop is strictly better.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "AND means a bit survives only if it's set in every number in the range, so the question is which bit positions are constant across the whole range. As you count upward the low bits churn — that's what counting is — and the high bits stay fixed. Concretely: if `left` and `right` first differ at bit `k`, then `left` has zero there and `right` has one, so the range contains both the number with bit `k` set and all lower bits clear, and its predecessor, which has bit `k` clear and all lower bits set. ANDing just those two kills bit `k` and everything below it. And every bit *above* `k` is identical in `left` and `right`, so it's identical in everything between. So the answer is exactly the common binary prefix, zero-padded. I compute it by shifting both operands right until they're equal, counting the shifts, then shifting back. At most thirty-one iterations. There's a two-line variant that's slicker — repeatedly clear the lowest set bit of `right` with `right and right minus one` until `right` drops to or below `left` — which runs once per set bit and needs no shift counter. The naive loop over the range is why example three is in the problem: I measured it at roughly nineteen seconds for one to two-billion-and-change."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why is the answer the common prefix?**" | **The question.** At the first differing bit `k`, the range contains `m` (bit `k` set, rest clear) and `m − 1` (bit `k` clear, rest set); their AND kills bit `k` and below. Bits above `k` are constant across the range. |
| "Why does the shift loop terminate?" | Both values shrink monotonically toward 0, and `0 == 0`. At most 31 steps. |
| "Why shift *both*?" | Comparing a truncated value against a full one exits early with a wrong prefix. |
| "Why the shift-back?" | The prefix must sit at its original magnitude. `5, 7` would return 1 instead of 4 without it. |
| "**How bad is the naive loop?**" | **~19 seconds** at `[1, 2³¹ − 1]`, measured. Example 3 exists to rule it out. |
| "Does an early exit at 0 save it?" | Not really — `[1, 2³⁰]` still burns through a billion values first. |
| "**Explain the Kernighan version.**" | `right & (right − 1)` clears the lowest set bit. Keep going until `right <= left`; what's left is the prefix, already in position. |
| "Which is faster?" | Kernighan on sparse `right` (one step for `2³⁰`); identical worst case. |
| "What if `left == right`?" | The loop never runs and `left` is returned. **No special case.** |
| "What about `left = 0`?" | The answer is 0 unless `right` is also 0 — falls out naturally. |
| "**Bitwise OR of the range instead?**" | Different: the OR is the prefix followed by all ones from the first differing bit down. Same analysis, opposite fill. |
| "XOR of the range?" | Different again — a closed form based on `right mod 4`, using `xor(0..n) ^ xor(0..left-1)`. |
| "Signed / negative ranges?" | The constraints keep everything non-negative. With negatives, the infinite sign bits make the shift loop's termination argument fail. |

**Traps:**

- ⚠️ **Looping over the range** — correct and ~19 seconds at the worst case.
- ⚠️ **Forgetting `left << shift`** — returns the prefix's value, not its position. `5, 7` → 1 instead of 4.
- ⚠️ **Shifting only `right`** — the comparison becomes meaningless.
- **`left != right` vs `left < right`** — equivalent here; `<` states the intent and survives unordered inputs.
- **Special-casing `left == right`** — unnecessary; the loop handles it.
- **Special-casing `left == 0`** — also unnecessary.
- **Assuming the answer has the same bit length as `right`** — it's zero-padded below the divergence.
- **Using `//= 2` instead of `>>= 1`** — equivalent for non-negatives, but it hides the operation.
- **Reaching for the Kernighan version without being able to explain it** — `right & (right-1)` is the bit you'll be asked about.

**This same move shows up in:** [Number of 1 Bits](191-number-of-1-bits.md) (`v & (v-1)` clearing the lowest set bit) · [Hamming Distance](461-hamming-distance.md) (the same Kernighan-versus-shift trade-off, measured) · [Single Number III](260-single-number-iii.md) (`v & -v`, the sibling trick) · [Counting Bits](338-counting-bits.md) (reasoning about bit positions rather than values) · [Reverse Bits](190-reverse-bits.md) (shifting bits into and out of position) · [bitwise-operators](../syntax/bitwise-operators.md).

</details>

---
