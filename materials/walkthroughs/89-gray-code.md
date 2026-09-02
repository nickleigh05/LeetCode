# 89. Gray Code

**Medium** · [LeetCode](https://leetcode.com/problems/gray-code/) · [Solution file (no hints)](../../problems/0001-0499/89.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Return **any** `n`-bit Gray code sequence — a permutation of `0 .. 2^n − 1` in which **every adjacent pair differs by exactly one bit**, starting at `0`, and **cyclic** (the last and first also differ by one bit).

```
n = 2  →  [0,1,3,2]     00 → 01 → 11 → 10 → (00)
n = 1  →  [0,1]
```

**Constraints:** `1 <= n <= 16`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return **any** valid sequence" | ⚠️ **No uniqueness to worry about** — `[0,2,3,1]` is equally correct |
| "a permutation of `[0, 2^n − 1]`" | Every value exactly once — **length is always `2^n`** |
| "first integer is 0" | A fixed anchor |
| "adjacent differ by **exactly one** bit" | ⚠️ **`x ^ y` must be a power of two** |
| "**first and last** also differ by one bit" | ⚠️ **Cyclic.** The easy requirement to forget |
| `n <= 16` | Up to **65,536** values — the output *is* the cost |

**Five conditions, and they're a checklist worth writing down** before you start: right length, starts at 0, no repeats, all in range, and **every adjacent pair including the wrap-around** differs by one bit.

**The construction that makes it obvious — reflect and prefix.** Take a valid sequence for `n−1` bits. Then:

1. Write it out, each value prefixed with a `0`.
2. Write it **backwards**, each value prefixed with a `1`.

```
n = 1:      0    1

n = 2:      00  01     ← the n=1 list, prefixed 0
            11  10     ← the n=1 list REVERSED, prefixed 1
         →  [0, 1, 3, 2]  ✅

n = 3:      000 001 011 010        ← n=2 prefixed 0
            110 111 101 100        ← n=2 reversed, prefixed 1
         →  [0, 1, 3, 2, 6, 7, 5, 4]  ✅
```

**Why every adjacency holds:**

- **Inside each half** — the old sequence's adjacencies are preserved, and the prefix bit is constant.
- **At the seam** — ⚠️ **the last of the first half and the first of the second half are the *same* old value**, so they differ only in the new prefix bit. **One bit.**
- **At the wrap-around** — ⚠️ **the last of the second half and the very first are also the same old value** (the reversal put the old first element last), differing only in the prefix. **One bit.**

**That's a complete induction, and it's the answer to "prove your sequence is valid".**

**Now the closed form.** The same sequence has a one-line description:

```python
[i ^ (i >> 1) for i in range(1 << n)]
```

**Why it produces exactly one bit of change per step** is worth seeing rather than memorising:

```
g(i) = i ^ (i >> 1)
g(i) ^ g(i+1) = (i ^ (i>>1)) ^ ((i+1) ^ ((i+1)>>1))
```

**Going from `i` to `i + 1` in ordinary binary flips a suffix**: the lowest 0 becomes 1 and all the 1s below it become 0. **XOR-ing with the right-shift cancels all of that churn except a single bit** — the position of that lowest 0.

🤔 **Before you open the next section:** `i ^ (i >> 1)` looks arbitrary until you check the range. Why can the result never exceed `2^n − 1`, and what would `i ^ (i << 1)` do instead?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Backtracking over permutations | Search for a valid ordering | O(2^n · n) with pruning | O(2^n) | ⚠️ Works, wildly over-engineered |
| DFS on the hypercube | Hamiltonian cycle on `Q_n` | O(2^n · n) | O(2^n) | ⚠️ Same — the structure is known |
| **Mirror construction** | Reflect and prefix | **O(2^n)** | **O(2^n)** | ✅ **The constructive answer** |
| **`i ^ (i >> 1)`** | Closed form | **O(2^n)** | **O(2^n)** | ✅ **The answer** |

**The decision: `i ^ (i >> 1)`. Be able to derive the mirror construction, because that's the proof.**

**Why searching is the wrong instinct.** A Gray code is a **Hamiltonian cycle on the `n`-dimensional hypercube**, and finding Hamiltonian cycles is NP-hard *in general* — ⚠️ **but this graph's cycle is completely known and constructible.** **Reaching for backtracking here means you didn't recognise the structure.** *(It does work: with pruning, n ≤ 16 is reachable. It's just answering a much harder question than the one asked.)*

**Why `i ^ (i >> 1)` stays in range.** `i < 2^n`, so `i >> 1 < 2^(n-1)`, and XOR never sets a bit that isn't set in one of its operands — **so the result is below `2^n`.** ⚠️ **`i ^ (i << 1)` breaks exactly here**: shifting *left* introduces a bit at position `n`, so `n = 2` gives `[0, 3, 6, 5]` — **out of range and not even a permutation.** **Verified.**

**Why it's a bijection.** `g(i) = i ^ (i >> 1)` is invertible — the inverse accumulates a running XOR:

```python
def gray_to_binary(g):
    b = g
    shift = 1
    while g >> shift:
        b ^= g >> shift
        shift += 1
    return b
```

⚠️ **An invertible map on `[0, 2^n)` is a permutation**, so "every value exactly once" is automatic. **That's the cleanest argument for the no-duplicates condition.**

**Why the cyclic condition holds.** ⚠️ **The last element is always `g(2^n − 1) = (2^n − 1) ^ (2^(n-1) − 1) = 2^(n-1)`** — a single set bit. **So it differs from the first element, 0, in exactly one bit.** **Verified for every `n` from 1 to 16.**

| `n` | Last element | Single bit? |
|---|---|---|
| 1 | 1 | ✅ |
| 2 | 2 | ✅ |
| 3 | 4 | ✅ |
| 16 | 32768 | ✅ |

**The mirror construction is the one to *explain*; the formula is the one to *write*.** ⚠️ **They produce the identical sequence** — verified for `n = 1..16` against all five validity conditions.

**Why nothing beats O(2^n).** **The output has `2^n` elements**, so you cannot do better. At `n = 16` that's **65,536 integers** — the whole cost is producing them.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [list-comprehension](../syntax/list-comprehension.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
return [i ^ (i >> 1) for i in range(1 << n)]
```

**One line. Every piece is load-bearing.**

```python
1 << n
```

**`2^n` — the number of values.** ⚠️ **`1 << n`, not `2 ** n`** — equivalent, but the shift is the idiom in bit problems and is a single instruction. ⚠️ **At `n = 16` this is 65,536**, so `range` produces 0..65535.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [range-function](../syntax/range-function.md)

```python
i >> 1
```

**Shift right one position** — drop the lowest bit, everything moves down.

```python
i ^ (i >> 1)
```

⚠️ **The Gray code of `i`.** Each output bit is the XOR of two adjacent input bits, so **consecutive `i` values produce outputs differing in exactly one position.**

⚠️ **The parentheses are required.** `^` binds *looser* than `>>` in Python, so `i ^ i >> 1` actually parses as `i ^ (i >> 1)` — **the same thing** — but `>>` versus `^` precedence is not something to rely on from memory. **Write the parentheses.**

⚠️ **`>>` not `<<`.** Shifting left introduces a bit at position `n` and the result leaves the range: **`n = 2` gives `[0, 3, 6, 5]`** — three of the four values wrong, and `6` isn't even a 2-bit number. **Verified.**
→ [bitwise-operators](../syntax/bitwise-operators.md) · [list-comprehension](../syntax/list-comprehension.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def grayCode(self, n: int) -> List[int]:
        return [i ^ (i >> 1) for i in range(1 << n)]
```

</details>

<details>
<summary>The mirror construction — the version that explains itself</summary>

```python
class Solution:
    def grayCode(self, n: int) -> List[int]:

        result = [0]

        for k in range(n):
            high_bit = 1 << k
            result += [x | high_bit for x in reversed(result)]

        return result
```

**Each round doubles the list**: keep what you have, then append it **reversed** with bit `k` set.

- **`reversed(result)`** — ⚠️ **the reflection.** Without it the seam and the wrap-around both break.
- **`x | high_bit`** — prefix the new bit. ⚠️ **`|` not `+`**: the bit is guaranteed clear (every existing value is `< 2^k`), so they agree — **but `|` says what you mean and can't carry.**
- **`result += [...]`** — extends in place.

⚠️ **`reversed(result)` is evaluated into the comprehension before `result` is extended**, so there's no mutate-while-iterating hazard. **`result += [x | high_bit for x in reversed(result[:])]` is the paranoid version and unnecessary.**

**Verified to produce the identical sequence to the formula for every `n` from 1 to 16.**
→ [list-comprehension](../syntax/list-comprehension.md) · [iterators-iterables](../syntax/iterators-iterables.md) · [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary>The inverse — Gray code back to binary</summary>

```python
def gray_to_binary(g: int) -> int:
    b = g
    shift = 1
    while g >> shift:
        b ^= g >> shift
        shift += 1
    return b
```

⚠️ **The forward map XORs by one shift; the inverse XORs by *all* of them.** Since `g = i ^ (i>>1)`, unrolling gives `i = g ^ (g>>1) ^ (g>>2) ^ …`.

**Worth knowing because it proves `i ^ (i >> 1)` is a bijection** — which is what guarantees no value repeats.
→ [while-loop](../syntax/while-loop.md)

</details>

**Trace it** — `n = 3`:

| `i` | `i` binary | `i >> 1` | `i ^ (i>>1)` | Gray | Bit that changed |
|---|---|---|---|---|---|
| 0 | `000` | `000` | `000` | **0** | — |
| 1 | `001` | `000` | `001` | **1** | bit 0 |
| 2 | `010` | `001` | `011` | **3** | bit 1 |
| 3 | `011` | `001` | `010` | **2** | bit 0 |
| 4 | `100` | `010` | `110` | **6** | bit 2 |
| 5 | `101` | `010` | `111` | **7** | bit 0 |
| 6 | `110` | `011` | `101` | **5** | bit 1 |
| 7 | `111` | `011` | `100` | **4** | bit 0 |

**`[0, 1, 3, 2, 6, 7, 5, 4]`** ✅

**Check every condition:**

| Condition | Holds? |
|---|---|
| Length `2³ = 8` | ✅ |
| Starts at 0 | ✅ |
| All distinct | ✅ — `{0,1,2,3,4,5,6,7}` |
| All in `[0, 7]` | ✅ |
| Adjacent differ by one bit | ✅ — the last column is a single bit each time |
| ⚠️ **First and last differ by one bit** | ✅ — `0 ^ 4 = 4 = 2²`, one bit |

⚠️ **The wrap-around is the condition people forget to check.** Here it works because the last element is always `2^(n-1)` — a single set bit — which differs from `0` in exactly one position. **Verified for `n = 1..16`.**

**`n = 2`:** `[0, 1, 3, 2]` ✅ — matching the problem's first example exactly. *(The problem also accepts `[0, 2, 3, 1]`; the formula happens to produce the other one.)*

**`n = 1`:** `[0, 1]` ✅ — ⚠️ **`0 ^ 1 = 1`, one bit, both for the adjacency and the wrap-around.**

**The mirror construction on `n = 3`:**

```
start:            [0]
k=0, bit 1:       [0] + [0|1]        = [0, 1]
k=1, bit 2:       [0,1] + [1|2, 0|2] = [0, 1, 3, 2]
k=2, bit 4:       [0,1,3,2] + [2|4, 3|4, 1|4, 0|4]
                                     = [0, 1, 3, 2, 6, 7, 5, 4]  ✅
```

⚠️ **Identical to the formula's output**, and the seam is visible: `2` then `6` — **the same underlying value `2`, with bit 2 added.**

**What `i ^ (i << 1)` gives instead**, for `n = 2`:

```
i=0 → 0    i=1 → 1^2 = 3    i=2 → 2^4 = 6    i=3 → 3^6 = 5
[0, 3, 6, 5]   ❌  6 and 5 exceed 2² − 1, and it isn't a permutation
```

**Verified:** both implementations were checked against all five validity conditions — correct length, starts at 0, no duplicates, every value in `[0, 2^n − 1]`, and every adjacent pair **including the wrap-around** differing by exactly one bit — for **every `n` from 1 to 16**. **Both pass; their outputs are identical.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(2^n)</summary>

**O(2^n)** — one constant-time operation per output element.

| Version | Cost |
|---|---|
| **`i ^ (i >> 1)`** | **`2^n` iterations**, O(1) each ✅ |
| Mirror construction | `n` rounds, round `k` doing `2^k` work → **`2^n − 1` total** ✅ |
| Backtracking search | O(2^n · n) with pruning ⚠️ |

**The mirror construction's total is a geometric sum:**

```
1 + 2 + 4 + … + 2^(n-1)  =  2^n − 1
```

⚠️ **So both are Θ(2^n)** — the doubling loop is *not* more expensive, which is the thing people assume.

**At `n = 16`: 65,536 elements.** Instant either way.

| `n` | Output size |
|---|---|
| 4 | 16 |
| 10 | 1,024 |
| **16** | **65,536** |

⚠️ **The output size is the complexity.** There is no faster algorithm, because **producing `2^n` numbers takes `Ω(2^n)` time.** **Say that explicitly** — it's the correct answer to "can you do better?"

**The formula version has the better constant**: a shift and an XOR per element, with no list reallocation. ⚠️ **The mirror version does `n` list extensions**, each amortised O(1) per element but with more memory traffic.

**If you only need the `i`-th element**, the formula gives it in **O(1)** — `i ^ (i >> 1)` — while the mirror construction would have to build everything before it. **A real advantage worth naming.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(2^n)</summary>

**O(2^n)** — the output.

| Component | Size |
|---|---|
| Result list | **`2^n` integers** — the answer |
| `i` | O(1) |
| **Auxiliary beyond the output** | **O(1)** ✅ |

**At `n = 16` that's 65,536 Python integers** — a few megabytes with object overhead, well within limits.

⚠️ **The mirror version's `[x | high_bit for x in reversed(result)]` materialises a temporary list of `2^k` elements** before extending. **At the final round that's `2^(n-1)` extra** — momentarily about 1.5× the peak of the formula version. **Not a problem at n = 16; worth knowing.**

**Avoid it by extending in place:**

```python
for k in range(n):
    high_bit = 1 << k
    for idx in range(len(result) - 1, -1, -1):
        result.append(result[idx] | high_bit)
```

⚠️ **Iterating the index range downward is essential** — appending while walking forward would read the elements you're adding. **The snapshot `range(len(result) - 1, -1, -1)` is computed once, so it's safe.**

**The formula version is a single list comprehension** — CPython pre-sizes it, so there's no repeated reallocation.

⚠️ **A generator would make the auxiliary space O(1)** if the caller streams the values — but the problem asks for a list, so `2^n` is unavoidable:

```python
def gray_codes(n):
    for i in range(1 << n):
        yield i ^ (i >> 1)
```
→ [yield-generators](../syntax/yield-generators.md) · [list-comprehension](../syntax/list-comprehension.md)

**No recursion** in either version.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A Gray code is a Hamiltonian cycle on the n-dimensional hypercube, but I don't need to search for one — there's a standard construction. Build it by reflection: take the sequence for n minus one bits, write it out with a zero prefix, then write it *backwards* with a one prefix. Adjacencies inside each half are inherited; at the seam the two neighbours are the same old value differing only in the new prefix bit; and at the wrap-around the last element and the first are also the same old value, again differing only in the prefix. That's a complete induction covering the cyclic condition too. The closed form is `i XOR (i shifted right one)`, and it produces exactly that sequence. Incrementing i in ordinary binary flips a whole suffix, and XOR-ing with the right shift cancels all of it except one bit. It stays in range because shifting right can't introduce a bit at position n — shifting *left* would, and gives out-of-range garbage. And it's invertible, which is why every value appears exactly once. The cyclic property is easy to check directly: the last element is always two to the n minus one, a single set bit, so it differs from zero in one position. It's O(2^n) time and space, which is optimal because the output has that many elements — and the formula has the nice extra property that I can compute the i-th element in O(1) without building the rest."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why does `i ^ (i >> 1)` work?**" | Incrementing flips a suffix in binary; XOR-ing with the shift cancels all that churn except one bit — the position of the lowest 0 in `i`. |
| "**Prove your sequence is valid.**" | Use the mirror construction and induct: adjacencies inside each half are inherited, and both the seam and the wrap-around join two copies of the same old value differing only in the new bit. |
| "How do you know there are no duplicates?" | `i ^ (i>>1)` is invertible (`i = g ^ (g>>1) ^ (g>>2) ^ …`), so it's a bijection on `[0, 2^n)`. |
| "**Does the cyclic condition hold?**" | Yes — the last element is always `2^(n-1)`, a single set bit, so it differs from 0 in one position. **Verified for n = 1..16.** |
| "Why `>>` and not `<<`?" | `<<` introduces a bit at position `n`. `n = 2` gives `[0, 3, 6, 5]` — out of range and not a permutation. |
| "Can you do better than O(2^n)?" | **No** — the output has `2^n` elements. |
| "The `i`-th element only?" | `i ^ (i >> 1)` in **O(1)**. The mirror construction can't do that. |
| "**Convert Gray back to binary?**" | XOR by every shift: `b = g; while g >> s: b ^= g >> s; s += 1`. |
| "Start from a value other than 0?" | XOR every element of the sequence by that value — it's still a valid Gray code, just rotated in the hypercube. |
| "Is the answer unique?" | **No** — `[0,2,3,1]` is also valid for `n = 2`. The problem says any. |
| "Where is this used in practice?" | Rotary encoders and ADCs: one changing bit means no transient misreads while a value settles. Also Karnaugh maps. |
| "n = 0?" | Out of the stated range, but `[0]` would be the sensible answer — and the formula gives it. |

**Traps:**

- ⚠️ **`i ^ (i << 1)`** — produces values ≥ `2^n` and isn't a permutation. `n = 2` → `[0, 3, 6, 5]`.
- ⚠️ **Forgetting the cyclic condition** — the first-and-last check is a stated requirement, not a bonus.
- ⚠️ **Omitting `reversed()`** in the mirror construction — breaks both the seam and the wrap-around.
- **`2 ** n` vs `1 << n`** — equivalent; the shift is the idiom here.
- **Appending while iterating forward** in the in-place mirror version — reads the elements being added.
- **Backtracking for a Hamiltonian cycle** — correct, and it ignores a fully known construction.
- **Assuming the answer is unique** — any valid sequence is accepted.
- **Building `2^n` elements for `n = 32`** — out of range here, but the output size is the wall.

**This same move shows up in:** [Subsets](78-subsets.md) (the same doubling construction — each round appends a transformed copy) · [Counting Bits](338-counting-bits.md) (a closed form over all values `0..2^n`) · [Reverse Bits](190-reverse-bits.md) (bit rearrangement as the whole problem) · [Single Number III](260-single-number-iii.md) (XOR's structural properties) · [Bitwise AND of Numbers Range](201-bitwise-and-of-numbers-range.md) (reasoning about what changes as you count upward) · [bitwise-operators](../syntax/bitwise-operators.md).

</details>

---
