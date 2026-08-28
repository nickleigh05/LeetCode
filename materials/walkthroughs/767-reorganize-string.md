# 767. Reorganize String

**Medium** · [LeetCode](https://leetcode.com/problems/reorganize-string/) · [Solution file (no hints)](../../problems/0500-0999/767.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

Rearrange the characters of `s` so that **no two adjacent characters are the same**. Return any valid rearrangement, or `""` if none exists.

```
s = "aab"   →  "aba"
s = "aaab"  →  ""      (impossible)
```

**Constraints:** `1 <= s.length <= 500` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "no two **adjacent** the same" | A spacing constraint — identical characters must be separated |
| "return **any** valid rearrangement" | No uniqueness requirement, which frees you to be greedy |
| `""` if impossible | ⚠️ You must **detect** impossibility, ideally before building |
| lowercase only | 26 distinct characters — a small, bounded alphabet |
| `n` up to 500 | Small; correctness and clarity matter more than constants |

**When is it impossible?** Think about the most frequent character. To keep copies apart you must place at least one different character between consecutive copies:

```
a _ a _ a       3 a's need 2 separators
```

With `n` total characters and the most frequent appearing `maxFreq` times, you need `maxFreq - 1` separators drawn from the other `n - maxFreq` characters. So it's possible exactly when:

> **`maxFreq <= (n + 1) // 2`**

- `"aab"`: `n = 3`, `maxFreq = 2`, `(3+1)//2 = 2` → `2 <= 2` ✅ possible
- `"aaab"`: `n = 4`, `maxFreq = 3`, `(4+1)//2 = 2` → `3 > 2` ❌ impossible

**The greedy that works.** Always place the character with the **highest remaining count**, subject to it differing from the one just placed.

Why greedy is safe: the most frequent character is the hardest to place later — if you defer it, its copies pile up and eventually have nowhere to go. Placing it as early as possible keeps the remaining problem balanced.

**Why that needs a heap.** After each placement, counts change and the "most frequent remaining" character shifts. You need repeated max-extraction from a changing multiset — exactly a max-heap.

**The mechanism that enforces the constraint.** Pop the most frequent, place it, then **hold it aside** for one step before pushing it back. Since it can't be chosen while held, the next character is necessarily different.

🤔 **Before you open the next section:** if you always place the currently most-frequent character, what must you do to guarantee it isn't chosen again immediately?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Backtracking | Try every arrangement | O(n!) | O(n) | ❌ Hopeless |
| **Max-heap, delay-by-one** | Pop most frequent, hold it one step | **O(n log 26)** | O(26) | ✅ |
| **Sort + fill even/odd slots** | Place the most frequent at even indices first | **O(n + 26 log 26)** | O(n) | ✅✅ No heap needed |

**The decision: a max-heap with a one-step delay** — the technique this unit is teaching. The slot-filling alternative is arguably better and worth knowing.

**The heap version:**

1. Count characters; push `(-count, char)` for a max-heap
2. Repeatedly: pop the most frequent, append it, decrement its count
3. **Hold the previous character aside**; push it back only *after* the next pop

That one-step delay is the entire constraint enforcement — a character just used is physically absent from the heap when the next choice is made, so it cannot repeat.

**Why the impossibility check can be implicit.** If the heap empties while characters remain unplaced (because the only available one is being held), no valid arrangement exists. Checking `maxFreq <= (n+1)//2` up front is clearer and fails fast, but the loop detects it too.

**The slot-filling alternative** — genuinely elegant and O(n) after counting:

```python
counts = Counter(s)
max_char, max_freq = counts.most_common(1)[0]
if max_freq > (len(s) + 1) // 2:
    return ""

result = [''] * len(s)
i = 0

# place the most frequent character in even slots first
for _ in range(max_freq):
    result[i] = max_char
    i += 2
del counts[max_char]

# then everything else, wrapping to odd slots
for ch, cnt in counts.items():
    for _ in range(cnt):
        if i >= len(s):
            i = 1                 # wrap to the first odd index
        result[i] = ch
        i += 2

return "".join(result)
```

The insight: filling **even indices `0, 2, 4, …` then odd indices `1, 3, 5, …`** guarantees that consecutive placements of the same character land at least two apart. Starting with the most frequent character ensures it fits before slots run out.

It's O(n) rather than O(n log 26), needs no heap, and the feasibility check makes correctness obvious. Mention both; the heap version is the pattern, the slot version is the sharper solution.

**Why a heap and not just sorting once.** Sorting gives a static order, but counts change as you place characters — the most frequent remaining shifts. A heap maintains that ordering dynamically. (The slot version sidesteps this by reasoning about *positions* rather than making a sequence of greedy choices.)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import Counter
import heapq

counts = Counter(s)

if max(counts.values()) > (len(s) + 1) // 2:
    return ""
```

**Feasibility check first.** The most frequent character needs `maxFreq - 1` separators from the remaining `n - maxFreq` characters; the inequality above is exactly that condition, rearranged.

Failing fast here means the main loop never has to handle the impossible case.
→ [counter](../syntax/counter.md) · [min-max-key](../syntax/min-max-key.md)

```python
heap = [(-cnt, ch) for ch, cnt in counts.items()]
heapq.heapify(heap)
```

**Negate for a max-heap** — `heapq` is a min-heap, so the most negative count (largest real count) sits at the root.

`heapify` is O(26) here; the alphabet bounds the heap's size regardless of `n`.
→ [heapq-module](../syntax/heapq-module.md)

```python
result = []
prev_count, prev_char = 0, ''
```

`prev_*` holds the character just placed, **kept out of the heap** for exactly one step.

Initializing `prev_count = 0` means nothing is pushed back on the first iteration — the `if prev_count < 0` guard below handles it.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while heap:
    count, ch = heapq.heappop(heap)
    result.append(ch)
```

**Take the most frequent available character and place it.**

Because the previously used character is being held aside, it cannot be popped here — the adjacency constraint is enforced structurally rather than by a check.
→ [while-loop](../syntax/while-loop.md)

```python
    if prev_count < 0:
        heapq.heappush(heap, (prev_count, prev_char))
```

**Return the held character to the heap — now that this step's choice is made.**

`prev_count < 0` means it still has remaining occurrences (counts are negated, so negative means non-zero). A count of 0 is exhausted and correctly never returns.

The **order matters**: push the previous character back *after* popping the current one, or it could be re-selected immediately.
→ [if-return](../syntax/if-return.md)

```python
    prev_count, prev_char = count + 1, ch
```

**Hold the character just placed.**

`count + 1` decrements the real count — since counts are stored negated, adding 1 moves toward zero (e.g. `-3 → -2` means three remaining became two).
→ [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
return "".join(result)
```

The feasibility check guarantees a complete arrangement, so no length verification is needed.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import Counter
import heapq

class Solution:
    def reorganizeString(self, s: str) -> str:

        counts = Counter(s)

        if max(counts.values()) > (len(s) + 1) // 2:
            return ""

        heap = [(-cnt, ch) for ch, cnt in counts.items()]
        heapq.heapify(heap)

        result = []
        prev_count, prev_char = 0, ''

        while heap:
            count, ch = heapq.heappop(heap)
            result.append(ch)

            if prev_count < 0:
                heapq.heappush(heap, (prev_count, prev_char))

            prev_count, prev_char = count + 1, ch

        return "".join(result)
```

</details>

<details>
<summary>The slot-filling version (O(n), no heap)</summary>

```python
from collections import Counter

class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        max_char, max_freq = counts.most_common(1)[0]

        if max_freq > (len(s) + 1) // 2:
            return ""

        result = [''] * len(s)
        i = 0

        for _ in range(max_freq):
            result[i] = max_char
            i += 2
        del counts[max_char]

        for ch, cnt in counts.items():
            for _ in range(cnt):
                if i >= len(s):
                    i = 1
                result[i] = ch
                i += 2

        return "".join(result)
```

Fills even indices then odd ones, so identical characters land ≥ 2 apart. Placing the most frequent first guarantees it fits.

</details>

**Trace it** — `s = "aab"`:

**Counts:** `a: 2, b: 1`. Check: `max = 2`, `(3+1)//2 = 2`, `2 <= 2` ✅ feasible.

**Heap:** `[(-2,'a'), (-1,'b')]`

| Step | Pop | `result` | Push back held? | New held |
|---|---|---|---|---|
| 1 | `(-2,'a')` | `"a"` | `prev_count = 0` → no | `(-1, 'a')` |
| 2 | `(-1,'b')` | `"ab"` | `-1 < 0` → push `(-1,'a')` | `(0, 'b')` |
| 3 | `(-1,'a')` | `"aba"` | `prev_count = 0` → no | `(0, 'a')` |
| 4 | heap empty | — | — | — |

Return **`"aba"`** ✅

Step 2 is the mechanism in action: `'a'` was held out of the heap, so `'b'` was the only option — guaranteeing they differ. Step 3 then returns `'a'` and it's chosen again, now safely non-adjacent to the previous `'a'`.

**The impossible case** — `s = "aaab"`: counts are `a: 3, b: 1`; `max = 3` and `(4+1)//2 = 2`, so `3 > 2` → return **`""`** ✅ immediately, without attempting construction.

**A longer trace** — `s = "vvvlo"`: counts `v: 3, l: 1, o: 1`; `n = 5`, `(5+1)//2 = 3`, `3 <= 3` ✅

| Step | Pop | `result` | Held after |
|---|---|---|---|
| 1 | `(-3,'v')` | `"v"` | `(-2,'v')` |
| 2 | `(-1,'l')` | `"vl"` | `(0,'l')`, and `(-2,'v')` pushed back |
| 3 | `(-2,'v')` | `"vlv"` | `(-1,'v')` |
| 4 | `(-1,'o')` | `"vlvo"` | `(0,'o')`, `(-1,'v')` pushed back |
| 5 | `(-1,'v')` | `"vlvov"` | — |

Return **`"vlvov"`** ✅ — no two adjacent characters match, and `'v'` appears at indices 0, 2, 4.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log 26) = O(n)</summary>

**O(n log 26)**, which is **O(n)** since the alphabet is fixed at 26.

| Phase | Cost |
|---|---|
| `Counter(s)` | O(n) |
| `heapify` | O(26) |
| Main loop | n iterations × O(log 26) push/pop |
| `join` | O(n) |

The heap never holds more than 26 entries — one per distinct character — so `log 26 ≈ 4.7` is a small constant. Effectively **O(n)**.

**The slot-filling version is O(n)** with no log factor at all: two linear passes after counting. Faster in practice, though the difference is immaterial at `n <= 500`.

**Compare to backtracking:** O(n!) — hopeless. The greedy works because the feasibility condition guarantees a solution exists whenever the check passes, so no search or backtracking is ever needed.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(26) = O(1)</summary>

**O(1) auxiliary** — the counter and heap each hold at most 26 entries, independent of `n`.

**O(n) for the output**, which is required.

| | Auxiliary space |
|---|---|
| **Heap version** | **O(26) = O(1)** |
| Slot-filling | O(26) counter + the O(n) result array |

**The bounded-alphabet observation is worth stating explicitly**, because it's what makes both the time and space claims clean:

> A frequency structure over a **fixed alphabet** is O(1), not O(n) — its size depends on the alphabet, not the input length.

The same reasoning appears in [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md) and [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md). It's also why this problem would be meaningfully different with an unbounded alphabet: the heap would be O(u) for `u` distinct characters, and `log u` would stop being a constant.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First, feasibility: to separate `maxFreq` copies of a character you need `maxFreq − 1` other characters between them, so it's possible exactly when `maxFreq <= (n+1)//2`. Checking that up front means the construction can't fail. Then the greedy: always place the character with the highest remaining count, because the most frequent one is the hardest to place later — deferring it lets copies pile up. That needs repeated max-extraction from a changing multiset, so a max-heap, which in Python means negating the counts. The constraint is enforced by **holding the character just placed out of the heap for one step** — it physically can't be chosen again, so the next character necessarily differs, and I push it back after the following pop. O(n) time since the heap is bounded by the 26-letter alphabet, O(1) auxiliary space. There's also a slot-filling version that places the most frequent character at even indices then fills the rest, which is O(n) with no heap at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "When is it impossible?" | **The key insight.** `maxFreq > (n+1)//2` — not enough other characters to separate the copies. |
| "Why is the greedy correct?" | The most frequent character is hardest to place later; deferring it strands copies. Placing it first keeps the remainder balanced. |
| "How is adjacency enforced?" | The previously placed character is held out of the heap for exactly one step, so it can't be re-selected. |
| "Solve it without a heap." | Slot filling — place the most frequent at even indices, then the rest, wrapping to odd. O(n). |
| "What if characters must be **k apart**?" | [Task Scheduler](621-task-scheduler.md) / [Rearrange String k Distance Apart](https://leetcode.com/problems/rearrange-string-k-distance-apart/) — hold a **queue** of the last `k−1` used characters instead of a single one. |
| "Why negate the counts?" | Python's `heapq` is a min-heap; negation simulates a max-heap. |
| "What if the alphabet were unbounded?" | The heap becomes O(u) and `log u` is no longer constant — O(n log u). |

**Traps:**

- **Pushing the previous character back before popping the current one.** It could be selected immediately, producing adjacent duplicates.
- **Pushing back a character whose count reached 0.** The `prev_count < 0` guard prevents phantom entries.
- **Getting the decrement backwards.** Counts are negated, so `count + 1` reduces the real count.
- **Skipping the feasibility check and not detecting failure.** The loop would produce a too-short string; you'd need to verify the length instead.
- **Using `(n // 2)` instead of `(n + 1) // 2`.** The `+1` matters for odd lengths — `"aab"` with `3 // 2 = 1` would wrongly report impossible.
- **Sorting once instead of using a heap.** Counts change as you place characters; a static order goes stale.

**This same move shows up in:** [Task Scheduler](621-task-scheduler.md) (the same greedy with a cooldown, generalized to `k` apart) · [Last Stone Weight](1046-last-stone-weight.md) (max-heap by negation, repeatedly taking extremes) · [Top K Frequent Words](692-top-k-frequent-words.md) (counting then heap-selecting) · [Remove Stones to Minimize the Total](1962-remove-stones-to-minimize-the-total.md) (greedy max-extraction from a changing multiset).

</details>

---
