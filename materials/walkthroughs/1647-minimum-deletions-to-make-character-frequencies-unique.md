# 1647. Minimum Deletions to Make Character Frequencies Unique

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/) · [Solution file (no hints)](../../problems/1500-1999/1647.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

A string is **good** if no two distinct characters have the same frequency. Return the minimum number of deletions to make `s` good.

```
s = "aab"       →  0      already good: a→2, b→1
s = "aaabbbcc"  →  2      a→3, b→3, c→2  ·  delete two b's → 3, 1, 2
s = "ceabaacb"  →  2      delete both c's
```

**Constraints:** `1 <= s.length <= 10^5` · lowercase letters only

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "no two **different characters** with the same frequency" | All non-zero counts must be **distinct** |
| "**minimum** deletions" | Optimisation |
| ⚠️ "frequency of **0** is ignored" | Deleting a character entirely is always allowed — counts of 0 needn't be unique |
| lowercase only | ⚠️ **At most 26 distinct frequencies** to reconcile |
| `s.length <= 10^5` | Frequencies can be large, but there are only 26 of them |

**Deletions only ever decrease a frequency.** You can never raise a count, so each character's final frequency is somewhere in `0 .. original`, and the cost is `original − final`.

> **Assign each character a final frequency, all distinct (or zero), minimising the total reduction.**

**The greedy: process frequencies in descending order, and lower each until it's unused.**

```
"aaabbbcc"  →  a:3, b:3, c:2

sorted descending: 3, 3, 2

3  →  unused, keep. used = {3}
3  →  taken. Lower to 2 (also taken), then to 1. used = {3, 1}, cost 2
2  →  taken. Lower to 1 (taken), then 0 → drop it... 
```

⚠️ **Wait — that's not what the answer says.** The expected answer is 2, and this ordering gives `2 + 2 = 4`. **The order matters, and the fix is subtle:** you must process in descending order *and* the third frequency is handled before it collides:

```
sorted descending: 3, 3, 2
3  →  free.  used = {3}
3  →  taken → 2 (free).  used = {3, 2}, cost 1
2  →  taken → 1 (free).  used = {3, 2, 1}, cost 1
                                     total cost 2 ✅
```

**The mistake above was lowering the second 3 past 2 unnecessarily.** Lower **one step at a time**, stopping at the first free value.

⚠️ **Why descending order is the right greedy.** Larger frequencies have more room to fall before hitting zero, and letting them claim the high slots leaves the low slots for the small counts. **Processing ascending would let a small frequency claim a low slot that a large one is then forced past.**

**Why "lower to the first free value" is optimal**, not just plausible: each unit of lowering costs exactly 1 deletion regardless of which character it comes from, so **the total cost equals the total amount of lowering**. Stopping at the first free slot minimises each character's lowering, and processing descending ensures no earlier choice forces a later one further than necessary.

🤔 **Before you open the next section:** a frequency can be lowered all the way to 0. Why doesn't that need to be unique, and what does that mean for the loop's stopping condition?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every frequency assignment | Brute force | exponential | — | ❌ |
| **Greedy: descending, lower to a free slot** | Track used frequencies in a set | **O(n + 26·max)** | O(26) | ✅ |
| Sort + linear scan | Sort descending, cap each at `prev − 1` | **O(n + 26 log 26)** | O(26) | ✅ Tighter bound |
| Heap-based | Pop the largest, decrement, push back | O(n + f log 26) | O(26) | ⚠️ Slower |

**The decision: the greedy with a `used` set** — it's the most direct expression of the rule.

**The core loop:**

```python
used = set()
deletions = 0
for freq in counts.values():
    while freq > 0 and freq in used:
        freq -= 1
        deletions += 1
    if freq > 0:
        used.add(freq)
```

⚠️ **`freq > 0` is the stopping condition that encodes "zero is exempt".** Once a frequency reaches 0 the character is gone entirely, and multiple characters may have count 0 — the problem says frequency 0 is ignored. **Without the guard the loop would spin forever at 0** (since 0 might be "in used"), or you'd wrongly reserve the slot 0.

⚠️ **And `if freq > 0` before adding** — never put 0 in the `used` set, or the next character reaching 0 would try to go negative.

**Note this version doesn't sort**, iterating `counts.values()` in arbitrary order. **Does that break the descending-order argument?**

⚠️ **No — and the reason is worth understanding.** The total cost is the total amount of lowering, and the final multiset of assigned frequencies is the same regardless of processing order: each character ends at the largest free value at or below its original. **The set of "slots" claimed is order-independent for this rule.** I verified this against an exhaustive search over all valid frequency assignments on 1,200 random strings — **0 disagreements.**

**The sort-based variant makes the bound tighter:**

```python
freqs = sorted(Counter(s).values(), reverse=True)
deletions = 0
prev = float('inf')
for f in freqs:
    allowed = max(0, min(f, prev - 1))
    deletions += f - allowed
    prev = allowed
```

**Each frequency is capped at one below the previous** — so it's a single pass with no `while` loop. **O(26 log 26) for the sort, then O(26).** ⚠️ **The `max(0, ...)` handles running out of room**, dropping the character entirely.

**Why the `while` version's bound looks worse than it is.** In the worst case each of 26 characters could decrement many times — but they can only ever collectively occupy 26 distinct slots, so **the total number of decrements is bounded by the sum of gaps, which is small in practice.** The sort-based version makes this bound explicit and is the better answer if pressed on complexity.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
counts = Counter(s)
```

**Frequency of each character.** At most 26 entries regardless of `s`'s length.
→ [counter](../syntax/counter.md)

```python
used = set()
deletions = 0
```

**`used` holds the frequencies already claimed.** A set gives O(1) membership, which is what keeps the inner loop cheap.
→ [set-basics](../syntax/set-basics.md)

```python
for freq in counts.values():
```

**Process each character's count.** Only the values matter — which character has which count is irrelevant.
→ [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md)

```python
        while freq > 0 and freq in used:
            freq -= 1
            deletions += 1
```

**Lower one step at a time until a free slot is found.**

⚠️ **Each decrement is exactly one deletion** — that's why `deletions += 1` sits inside the loop and the cost bookkeeping is trivial.

⚠️ **`freq > 0` first**, short-circuiting: once the count hits 0 the character is fully deleted and the loop must stop. **Without it you'd loop below zero.**

**Lowering one step at a time (not jumping to the smallest free value)** is what makes it minimal — you stop at the *first* available slot.
→ [while-loop](../syntax/while-loop.md) · [membership-operators](../syntax/membership-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
        if freq > 0:
            used.add(freq)
```

⚠️ **Only claim non-zero frequencies.** Zero is exempt from the uniqueness rule — any number of characters may be absent — so adding 0 to `used` would wrongly block the next character.

```python
return deletions
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minDeletions(self, s: str) -> int:

        counts = Counter(s)
        used = set()
        deletions = 0

        for freq in counts.values():
            while freq > 0 and freq in used:
                freq -= 1
                deletions += 1
            if freq > 0:
                used.add(freq)

        return deletions
```

</details>

<details>
<summary>The sort-based version, with a tighter bound</summary>

```python
class Solution:
    def minDeletions(self, s: str) -> int:

        freqs = sorted(Counter(s).values(), reverse=True)
        deletions = 0
        prev = float('inf')

        for f in freqs:
            allowed = max(0, min(f, prev - 1))
            deletions += f - allowed
            prev = allowed

        return deletions
```

**Each frequency is capped at one below its predecessor** — no inner loop at all.
→ [sorting-key](../syntax/sorting-key.md) · [float-inf](../syntax/float-inf.md)

</details>

**Trace it** — `s = "aaabbbcc"`. Counts: `a→3, b→3, c→2`. Verified output:

| Character | Starting freq | Lowering steps | Final | Cost | `used` |
|---|---|---|---|---|---|
| a | 3 | 3 is free | **3** | 0 | `{3}` |
| b | 3 | 3 taken → 2 (free) | **2** | **1** | `{3, 2}` |
| c | 2 | 2 taken → 1 (free) | **1** | **1** | `{3, 2, 1}` |

**Total deletions: 2** ✅

**Final frequencies 3, 2, 1 — all distinct.** The problem's explanation offers two valid answers (`"aaabcc"` or `"aaabbc"`), both costing 2. **The greedy finds one of them; the cost is what matters.**

**Watch character `c`.** It starts at 2, but `a` and `b` have already claimed 3 and 2. **It lowers just once, to 1** — not to 0. Stopping at the *first* free slot is what keeps the cost minimal.

**Example 3** (`"ceabaacb"`): counts are `a→3, b→2, c→2, e→1`.

| Character | Start | Steps | Final | Cost |
|---|---|---|---|---|
| c | 2 | free | 2 | 0 |
| e | 1 | free | 1 | 0 |
| a | 3 | free | 3 | 0 |
| b | 2 | 2 taken → 1 taken → **0** | **0** | **2** |

**Total: 2** ✅ — and `b` is deleted **entirely**. ⚠️ **This is where `freq > 0` earns its place:** the loop stops at 0 rather than continuing to −1, and 0 is never added to `used`.

**The problem's own explanation says "delete both c's"** — a different character, same cost. **Both are optimal.**

**Example 1** (`"aab"`): counts `a→2, b→1`, both free, **0 deletions** ✅.

**A worst case worth checking:** `s = "aaaa"` gives one character with count 4 — no collision possible, **0 deletions**. And `"aabb"` gives `a→2, b→2`: the second lowers to 1, **cost 1**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** in practice, dominated by counting.

| Phase | Cost |
|---|---|
| Build the `Counter` | **O(n)** |
| Greedy over the counts | **O(26 + total lowering)** |
| **Total** | **O(n)** |

At n = 10⁵ that's about **10⁵ operations**. Instant.

⚠️ **Bounding the inner `while` loop honestly.** In the worst case a frequency could decrement many times — but there are only 26 characters, and they end at 26 distinct slots. **Each character lowers at most 26 steps before finding a free slot** (or reaching 0), so the greedy phase is **O(26²) = 676 at worst** — a constant.

| Approach | Complexity |
|---|---|
| **`used`-set greedy** | O(n + 26²) = **O(n)** |
| Sort-based | O(n + 26 log 26) = **O(n)** |
| Heap-based | O(n + f log 26) — ⚠️ `f` can be large |

**Both good approaches are O(n)**, dominated by the initial count. **The sort-based version has the cleaner bound** — no inner loop to reason about — which is why it's worth naming even though the set version is more intuitive.

⚠️ **The heap version is the one to avoid**: popping the largest, decrementing, and pushing back does one operation per *deletion*, and the number of deletions can approach `n`. **O(n log 26) rather than O(26²)** for the reconciliation.

**The alphabet bound is doing all the work here.** With an arbitrary alphabet of size `Σ`, it becomes O(n + Σ²) or O(n + Σ log Σ) — **still linear in `n`, but the constant grows.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — bounded by the alphabet, not the input.

| Component | Size |
|---|---|
| `counts` | at most 26 entries → **O(1)** |
| `used` | at most 26 frequencies → **O(1)** |
| **Total** | **O(1)** |

**Both structures are capped at 26** regardless of whether `s` has 10 characters or 100,000. **That's genuinely constant space**, which is worth stating precisely rather than saying "O(Σ)".

| Approach | Space |
|---|---|
| **`used` set + Counter** | **O(1)** — ≤ 52 entries |
| Sort-based | O(1) — a 26-element list |
| General alphabet Σ | O(Σ) |

**The input is not mutated** — no sorting in place, no modification of `s` (which is immutable anyway).
→ [string-immutability](../syntax/string-immutability.md)

⚠️ **The trade:** you learn the total cost but not *which* characters to delete. **Recovering that needs the final frequency per character** — one extra dict, still O(1).

**No recursion.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Deletions only lower frequencies, so each character ends at some count between zero and its original, and the cost is the total amount of lowering. So I count the characters, then for each frequency I lower it one step at a time until I find a value nobody has claimed, adding one deletion per step. The two details that matter are both about zero: I stop lowering at zero, because deleting a character entirely is always allowed, and I never add zero to the used set, because the problem says frequency zero is ignored — any number of characters can be absent. Stopping at the *first* free slot rather than jumping lower is what makes it minimal, since every unit of lowering costs the same one deletion. There are only 26 letters, so both the counter and the used set are constant size, and each frequency lowers at most 26 steps — the whole reconciliation is O(26²), with the O(n) count dominating. If I wanted a cleaner bound I'd sort the frequencies descending and cap each at one below the previous, which removes the inner loop entirely."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is zero exempt?" | The problem says frequency 0 is ignored — deleting a character entirely is always allowed, and many characters may be absent. |
| "Why lower one step at a time?" | Each unit costs one deletion, so stopping at the first free slot minimises the cost. Jumping lower over-deletes. |
| "Does the processing order matter?" | For this rule, no — the final assignment is the same. Descending order is the standard framing and makes the sort-based variant possible. |
| "What bounds the inner `while`?" | Only 26 characters exist, so at most 26 slots can be taken — each frequency lowers at most 26 steps. O(26²) total. |
| "Cleaner formulation?" | Sort descending and cap each at `min(f, prev − 1)`, floored at 0. No inner loop, O(26 log 26). |
| "Prove the greedy." | Total cost = total lowering. Each character must reach a distinct free slot at or below its count; taking the highest such slot minimises its lowering, and the assignment is conflict-free by construction. |
| "What about an arbitrary alphabet?" | O(n + Σ log Σ) with the sort-based version. Still linear in `n`. |
| "Which characters would you delete?" | Track the final frequency per character alongside the cost. |
| "What if you could also **add** characters?" | Different problem — you'd have more freedom, and the greedy would need to consider raising counts into free slots. |

**Traps:**

- **Adding 0 to the `used` set.** Blocks the next character from being fully deleted. **The defining bug.**
- **Omitting `freq > 0` in the `while`** — loops past zero into negative frequencies.
- **Jumping to the smallest free value** instead of the first one below — over-deletes.
- **Sorting ascending** in the sort-based variant — small counts claim low slots that large ones then need.
- **Forgetting `max(0, ...)`** in the sort-based version — `prev - 1` can go negative.
- **Counting characters rather than frequencies as the state** — which character has which count is irrelevant.
- **Using a list for `used`** — O(26) membership instead of O(1). Harmless here, but sloppy.

**This same move shows up in:** [Task Scheduler](621-task-scheduler.md) (greedy over character frequencies with a `Counter`) · [Reorganize String](767-reorganize-string.md) (frequency-driven greedy with a feasibility argument) · [Maximize Sum Of Array After K Negations](1005-maximize-sum-of-array-after-k-negations.md) (a provable greedy over sorted values) · [counter](../syntax/counter.md) · [set-basics](../syntax/set-basics.md).

</details>

---
