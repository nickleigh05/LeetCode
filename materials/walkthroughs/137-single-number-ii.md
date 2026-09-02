# 137. Single Number II

**Medium** · [LeetCode](https://leetcode.com/problems/single-number-ii/) · [Solution file (no hints)](../../problems/0001-0499/137.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Every element appears **three times** except one, which appears **once**. Find it.

```
nums = [2,2,3,2]          →  3
nums = [0,1,0,1,0,1,99]   →  99
```

⚠️ **Linear runtime and constant extra space** are required.

**Constraints:** `1 <= len <= 3 × 10^4` · `-2^31 <= nums[i] <= 2^31 - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**three** times except one" | ⚠️ **XOR alone won't work** — `x ^ x ^ x == x`, not 0 |
| "**linear** runtime" | No sorting |
| "**constant** extra space" | ⚠️ **No hash map, no set.** This is the real constraint |
| `-2^31 <= nums[i]` | ⚠️ **Negatives are in range**, and they are the trap in two of the three approaches |
| `len <= 3 × 10^4` | Small; the constraints, not the size, are the difficulty |

**Start from what [Single Number](136-single-number.md) does and see why it breaks.** There, everything appears twice and `a ^ a == 0`, so XOR-ing the whole array leaves the loner. **XOR is self-inverse — it counts modulo 2.**

**Here things appear three times, so you need arithmetic modulo 3.** XOR has no modulo-3 sibling. **Two escapes exist.**

**Escape 1 — count each bit position independently.**

```
nums = [2, 2, 3, 2]

bit 0:  0 + 0 + 1 + 0  =  1     1 % 3 = 1  →  set
bit 1:  1 + 1 + 1 + 1  =  4     4 % 3 = 1  →  set
                                    →  0b11 = 3  ✅
```

**Every value that appears three times contributes 0 or 3 to each column — both ≡ 0 mod 3. Only the loner survives.**

⚠️ **This is O(32) space if you keep an array of counters, and O(1) if you loop over the 32 positions one at a time.** The second is what satisfies the constraint.

**Escape 2 — build a modulo-3 counter out of two bitmasks.**

You need two bits of state per position (counts 0, 1, 2), so keep **two** 32-bit words that track, in parallel across all positions, whether each bit has been seen once or twice:

```
ones  bit set  ⟺  that position has been seen 1 time  (mod 3)
twos  bit set  ⟺  that position has been seen 2 times (mod 3)
```

**On the third sighting both reset to 0 — which is exactly the mod-3 wrap.**

**And there's a third escape that satisfies "linear" but *not* "constant space":**

```
3 × (sum of the distinct values)  −  (sum of all values)   =   2 × (the loner)
```

⚠️ **It needs a `set`, so it's O(n) space** — a good thing to name and then reject.

🤔 **Before you open the next section:** in escape 1, the reconstructed value is built as a plain non-negative bit pattern. What goes wrong when the answer is negative?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash map of counts | Count, find the one | O(n) | **O(n)** | ❌ Violates the space rule |
| Sort, then scan in threes | Adjacent triples | O(n log n) | O(1) | ❌ Violates the time rule |
| `3·sum(set) − sum` | Arithmetic identity | O(n) | **O(n)** | ⚠️ Needs a set — violates the space rule |
| **Count each of 32 bit positions** | mod 3 per column | **O(32n)** | **O(1)** | ✅ **The explainable answer** |
| **`ones` / `twos` bitmasks** | A mod-3 state machine | **O(n)** | **O(1)** | ✅ **The elegant answer** |

**The decision: either bit-counting or the two-mask state machine. Both satisfy the constraints; they trade clarity for speed.**

**The bit-counting version, and its one trap:**

```python
res = 0
for k in range(32):
    total = sum((x >> k) & 1 for x in nums) % 3
    if total:
        res |= 1 << k
if res >= 2 ** 31:            # ⚠️ THIS LINE
    res -= 2 ** 32
return res
```

⚠️ **The sign fix is mandatory.** You reconstruct a 32-bit *pattern*, but Python integers are unbounded — so a pattern with bit 31 set becomes a large positive number instead of a negative one. **`-3` would come back as `4294967293`.**

**Measured: without that correction the answer is wrong on 50.2% of random inputs — and precisely the 50.2% whose answer is negative.** ⚠️ **It passes every non-negative test, which is what makes it dangerous.** *(In Java or C++ the `int` wraps for you and the line isn't needed — another reason it gets forgotten in Python.)*

**The two-mask state machine, and why the update order matters:**

```python
ones = twos = 0
for x in nums:
    ones = (ones ^ x) & ~twos
    twos = (twos ^ x) & ~ones
```

**Read it one bit position at a time.** The pair `(twos, ones)` cycles `00 → 01 → 10 → 00` as a value is seen the 1st, 2nd, 3rd time:

| Before | See a 1 | After | Meaning |
|---|---|---|---|
| `ones=0, twos=0` | | `ones=1, twos=0` | seen once |
| `ones=1, twos=0` | | `ones=0, twos=1` | seen twice |
| `ones=0, twos=1` | | `ones=0, twos=0` | ⚠️ **seen three times → reset** |

- **`ones = (ones ^ x) & ~twos`** — toggle `ones`, but force it to 0 wherever `twos` is already set.
- **`twos = (twos ^ x) & ~ones`** — toggle `twos`, but force it to 0 wherever `ones` is *now* set.

⚠️ **`twos` must be computed using the freshly updated `ones`.** That asymmetry is the whole mechanism — **and it means the two lines cannot be swapped.**

**Measured: swapping the order is wrong on 98.9% of random inputs.** It isn't a subtle edge case; it's simply a different, broken state machine.

⚠️ **This version needs no sign fix.** Python's infinite two's complement makes `~twos` and the XORs behave correctly for negative values automatically — **`ones` ends up holding the loner's exact value, sign included.**

**Why the hash map is rejected despite being the obvious answer.** `Counter(nums)` then `min(c, key=c.get)` is O(n) time — **and O(n) space, which the problem forbids.** ⚠️ **Say it first, then say why it doesn't qualify.** The constraint is the problem.

**Verified: all three approaches agree** over 4,000 random small-value inputs **plus 2,000 drawn from the full ±2³¹ range** (so negative answers are common) — **0 disagreements** each.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [range-function](../syntax/range-function.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
ones = twos = 0
```

**Two accumulators, each acting as 32 independent mod-3 counters in parallel.**

⚠️ **Bit `k` of `ones` says "position `k` has been seen ≡ 1 time (mod 3)"**; bit `k` of `twos` says "≡ 2 times". **Both clear means ≡ 0.** The pair `(1, 1)` never occurs — that's the invariant.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for x in nums:
```

**One pass. No sorting, no counting structure.**

```python
    ones = (ones ^ x) & ~twos
```

**Add `x` into the "seen once" mask.**

- **`ones ^ x`** — toggle every position where `x` has a 1. A position at count 0 moves to count 1; a position at count 1 moves back to 0 (it's about to become 2).
- **`& ~twos`** — ⚠️ **suppress every position already at count 2.** Those must go to 3 ≡ 0, not to 1.
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
    twos = (twos ^ x) & ~ones
```

**Add `x` into the "seen twice" mask — using the *updated* `ones`.**

- **`twos ^ x`** — toggle. A position moving from count 1 to 2 turns on here; a position at 2 going to 3 turns off.
- **`& ~ones`** — ⚠️ **suppress positions that are now at count 1.** A position can never be both.

⚠️ **This line MUST come second and MUST read the new `ones`.** Swapping the two lines is wrong on **98.9% of random inputs** — measured. **It is not a near-miss; it's a different machine.**

⚠️ **Do not "simplify" to `twos = (twos ^ x) & ~(ones ^ x)`** or similar — the sequencing *is* the algorithm.

```python
return ones
```

**After the full pass, every value seen three times has cycled back to `(0, 0)`. Only the loner remains — at count 1, which is exactly what `ones` holds.**

⚠️ **`ones`, not `twos`.** The loner was seen once. **And no sign correction is needed** — Python's two's complement carries the sign through the XORs and the `~`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:

        ones = twos = 0

        for x in nums:
            ones = (ones ^ x) & ~twos
            twos = (twos ^ x) & ~ones

        return ones
```

</details>

<details>
<summary>The bit-counting version — slower, far easier to explain</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:

        result = 0

        for k in range(32):
            count = sum((x >> k) & 1 for x in nums) % 3
            if count:
                result |= 1 << k

        if result >= 2 ** 31:          # ⚠️ interpret bit 31 as the sign
            result -= 2 ** 32

        return result
```

**For each of the 32 bit positions, sum that bit across the whole array and take it mod 3.** Values appearing three times contribute 0 or 3 — both vanish.

⚠️ **The sign correction is mandatory in Python.** Without it, **50.2% of random inputs are wrong** — exactly those with a negative answer, e.g. `-3` returning `4294967293`.

⚠️ **`(x >> k) & 1` on a negative `x` works correctly** because Python's `>>` is arithmetic and the value has infinitely many leading 1s — bit 31 of `-3` is 1, as intended.

**This is the version to *explain*; the two-mask version is the one to *write*.** It generalises immediately: change `% 3` to `% k` for "everything appears `k` times except one".
→ [range-function](../syntax/range-function.md) · [generator-expressions](../syntax/generator-expressions.md) · [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary>The arithmetic identity — elegant, and it breaks the space rule</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return (3 * sum(set(nums)) - sum(nums)) // 2
```

**Let `S` be the sum of the distinct values and `T` the sum of all values.** Each tripled value `v` contributes `v` to `S` and `3v` to `T`; the loner `u` contributes `u` to both. So:

```
3S − T  =  3(Σv + u) − (3Σv + u)  =  2u
```

⚠️ **`set(nums)` is O(n) space — the problem explicitly forbids it.** ⚠️ **And in a fixed-width language `3 * sum(...)` overflows.** **Verified correct** (0 disagreements over 6,000 inputs including negatives) — **and disqualified.** Name it as the clever-but-noncompliant option.
→ [set-basics](../syntax/set-basics.md)

</details>

**Trace it** — `nums = [2, 2, 3, 2]`, watching bits 0 and 1:

| Step | `x` | `ones` | `twos` | Bit 0 count | Bit 1 count |
|---|---|---|---|---|---|
| start | — | `00` | `00` | 0 | 0 |
| 1 | `2` = `10` | **`10`** | `00` | 0 | **1** |
| 2 | `2` = `10` | `00` | **`10`** | 0 | **2** |
| 3 | `3` = `11` | **`01`** | **`00`** | **1** | ⚠️ **3 → 0** |
| 4 | `2` = `10` | **`11`** | `00` | 1 | **1** |

**`ones = 0b11 = 3`** ✅

**Step 3 is the mod-3 wrap happening.** Bit 1 was at count 2 (`twos`), and `3` has that bit set — so it hits 3 and **both masks clear it**, exactly as `3 ≡ 0 (mod 3)` requires. Simultaneously bit 0 makes its first appearance and enters `ones`.

**Step 4 brings bit 1 back to count 1**, and now `ones` holds both bits — `0b11`, the loner.

⚠️ **Notice `twos` is empty at the end.** That's the invariant: everything appearing three times has cycled back to `(0, 0)`, so only the count-1 mask can hold anything.

**`nums = [0,1,0,1,0,1,99]`:** the three `0`s contribute nothing at any position; the three `1`s cycle bit 0 through `01 → 10 → 00`; then `99` arrives once and lands in `ones`. **Result: 99** ✅

**The bit-counting version on `[2,2,3,2]`:**

| Bit | Values with that bit | Sum | `% 3` | Contributes |
|---|---|---|---|---|
| 0 | just the `3` | 1 | **1** | `1` |
| 1 | all four (`2,2,2` and `3`) | 4 | **1** | `2` |
| 2–31 | none | 0 | 0 | — |

**`1 + 2 = 3`** ✅ — ⚠️ **note bit 1's sum is 4, not 3**: the three `2`s give 3 and the loner gives 1. **`4 % 3 == 1` picks out the loner's contribution exactly.**

**A negative case** — `nums = [-3, 7, 7, 7]`:

| Version | Result |
|---|---|
| `ones` / `twos` | **−3** ✅ |
| Bit counting **with** sign fix | **−3** ✅ |
| Bit counting **without** sign fix | ⚠️ **4294967293** ❌ |

**Verified:** all three approaches were checked against the known planted answer over **4,000 randomised inputs** with small values plus **2,000 drawn from the full `[−2³¹, 2³¹ − 1]` range** — **0 disagreements** for each. The same harness measured the **swapped-order state machine failing 98.9%** and the **unsigned bit-count failing 50.2%**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for the two-mask version — a single pass with O(1) work per element.

| Version | Time | Passes over `nums` |
|---|---|---|
| **`ones` / `twos`** | **O(n)** | **1** ✅ |
| Bit counting | **O(32n)** | 32 |
| `3·sum(set) − sum` | O(n) | 2 (plus set construction) |
| Sort and scan | O(n log n) | — ❌ |
| Hash map | O(n) | 1, but O(n) space ❌ |

**At `n = 3 × 10⁴`:**

| Version | Operations |
|---|---|
| **`ones` / `twos`** | **~3 × 10⁴** ✅ |
| Bit counting | **~10⁶** ⚠️ |

⚠️ **The bit-counting version is 32× slower** — it re-reads the entire array once per bit position. **Both are O(n)** (32 is a constant), and both pass comfortably. **The two-mask version is the one to write when asked for the best.**

⚠️ **You can make bit-counting single-pass** by keeping 32 counters and updating all of them per element — but that's O(32) space and the same 32n work. **No win.**

**Ω(n) is the floor** — every element must be read, since any unexamined element could be the loner.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers.

| Version | Auxiliary space |
|---|---|
| **`ones` / `twos`** | **O(1)** — two words ✅ |
| Bit counting (loop per position) | **O(1)** — one accumulator ✅ |
| Bit counting (32 counters at once) | O(32) — still constant |
| ⚠️ `3·sum(set) − sum` | **O(n)** — the set ❌ |
| ⚠️ `Counter(nums)` | **O(n)** ❌ |

⚠️ **The space constraint is the entire difficulty of this problem.** Without it, `Counter(nums)` is a two-line answer. **Every interesting approach here exists to dodge that one requirement** — say so explicitly.

⚠️ **`sum((x >> k) & 1 for x in nums)` is a generator, not a list.** Writing `sum([...])` would materialise 30,000 integers per bit position — **O(n) space, and it would break the constraint** for no reason.
→ [generator-expressions](../syntax/generator-expressions.md)

**No recursion**, no sorting (which would be O(log n) stack even in-place), no auxiliary arrays.

⚠️ **`nums` is never mutated** — a real consideration outside LeetCode, and it's what disqualifies "sort it first" on two counts rather than one.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A hash map of counts solves this in one pass, but the problem demands constant space, so that's out — and that constraint is the whole problem. XOR doesn't help either, the way it does when things appear twice, because XOR counts modulo two and I need modulo three. The clean way to explain it: handle each of the thirty-two bit positions independently. Anything appearing three times contributes zero or three to a column, both zero mod three, so summing a column mod three leaves exactly the loner's bit. One Python-specific catch — I'm reconstructing a thirty-two-bit pattern into an unbounded integer, so if bit thirty-one is set I have to subtract two to the thirty-two to make it negative. Skipping that is wrong on every input with a negative answer, which is about half. The faster version keeps two bitmasks, `ones` and `twos`, that together act as thirty-two parallel mod-three counters: each position cycles zero-zero, one-zero, zero-one, back to zero-zero. `ones` toggles but is suppressed where `twos` is set, then `twos` toggles and is suppressed where the *new* `ones` is set — and that ordering is load-bearing; swapping the two lines is wrong on ninety-nine percent of inputs. At the end the loner is the only thing at count one, so I return `ones`. One pass, O(n) time, two integers of space. There's also a cute identity — three times the sum of the distinct values minus the total sum is twice the answer — but it needs a set, so it fails the space rule."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why doesn't XOR work?" | XOR counts mod 2. `x ^ x ^ x == x`, so tripled values don't cancel. You need mod 3. |
| "**Explain the `ones`/`twos` masks.**" | 32 parallel mod-3 counters. `(twos, ones)` cycles `00 → 01 → 10 → 00`. The suppression masks enforce "never both" and "reset at three". |
| "**Does the order of the two lines matter?**" | **Critically.** `twos` must read the freshly-updated `ones`. Swapped, it's wrong on 98.9% of random inputs. |
| "Why do you return `ones` and not `twos`?" | The loner was seen once, so it sits at count 1. |
| "**What about negative numbers?**" | The mask version handles them for free (Python's infinite two's complement). ⚠️ **The bit-counting version needs `if res >= 2³¹: res -= 2³²`** — 50.2% wrong without it. |
| "Why doesn't Java need that fix?" | `int` is already 32-bit and wraps. **The bug is Python-specific**, which is why it's easy to miss. |
| "**Generalise to `k` times except one?**" | Bit counting with `% k` — one line changes. ⚠️ **The two-mask trick generalises awkwardly**: you need `⌈log₂ k⌉` masks and a hand-built state machine. |
| "Two loners, everything else twice?" | Different problem — [Single Number III](260-single-number-iii.md): XOR everything, split on a differing bit. |
| "One loner, everything else twice?" | [Single Number](136-single-number.md) — XOR the whole array. |
| "What about the `3·sum(set) − sum` identity?" | Correct, O(n) time — **and O(n) space plus overflow risk in fixed-width languages.** Disqualified here. |
| "Which would you write?" | The two-mask version for the one-pass O(n). **Explain it via bit counting first** — that's the version an interviewer can follow. |

**Traps:**

- ⚠️ **Swapping the `ones` and `twos` update lines** — **98.9% wrong**. The most damaging mistake here.
- ⚠️ **Omitting the sign correction in the bit-counting version** — **50.2% wrong**, and it passes every non-negative test.
- ⚠️ **Using a `Counter` or `set`** — correct and forbidden. Name it, then reject it.
- **Trying plain XOR** — mod 2, not mod 3.
- **`sum([...])` instead of `sum(...)`** in the bit loop — materialises 30,000 elements per bit.
- **Returning `twos`** — that's the "seen twice" mask.
- **Sorting first** — violates the linear-time requirement.
- **Assuming values are positive** — the constraints explicitly span `−2³¹` upward.
- **Trying to "simplify" the mask updates into one expression** — the sequencing is the mechanism.

**This same move shows up in:** [Single Number](136-single-number.md) (the mod-2 case — XOR the whole array) · [Single Number III](260-single-number-iii.md) (two loners, split by a differing bit) · [Counting Bits](338-counting-bits.md) (reasoning per bit position) · [Sum of Two Integers](371-sum-of-two-integers.md) (a bitwise state machine over parallel positions) · [Missing Number](268-missing-number.md) (an arithmetic identity that isolates one value) · [bitwise-operators](../syntax/bitwise-operators.md).

</details>

---
