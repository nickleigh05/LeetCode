# 1405. Longest Happy String

**Medium** · [LeetCode](https://leetcode.com/problems/longest-happy-string/) · [Solution file (no hints)](../../problems/1000-1499/1405.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

A string is **happy** if it contains only `'a'`, `'b'`, `'c'`, **never has three equal letters in a row** (`"aaa"`, `"bbb"`, `"ccc"` are forbidden), and uses at most `a` letters `'a'`, at most `b` letters `'b'`, at most `c` letters `'c'`. Return the **longest** happy string. Any longest one is accepted.

```
a = 1, b = 1, c = 7   →  "ccaccbcc"   (or "ccbccacc")
a = 7, b = 1, c = 0   →  "aabaa"
```

**Constraints:** `0 <= a, b, c <= 100` · `a + b + c > 0`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "longest" | Use as many letters as possible. Never give up a letter unless forced |
| no `"aaa"`, `"bbb"`, `"ccc"` | You can place the same letter twice in a row, but the third must be different |
| counts `a`, `b`, `c` | A supply of each letter. Use the most plentiful one the most |
| any answer accepted | A greedy construction is fine. No search needed |

**Greedy idea.** At each step place the letter with the **most remaining**, because the most plentiful letter is the one most likely to get stranded at the end. But if the last two letters placed are already that letter, you can't use it, so you **fall back to the second most plentiful**. And if nothing else remains, you stop (the string is as long as it can be).

"Give me the letter with the largest remaining count, again and again, while the counts keep changing" is the shape of a **max-heap**.

🤔 **Before you open the next section:** if the heap's top is `'c'` but the string already ends in `"cc"`, what do you place, and what do you do with the `'c'` you didn't use?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Try every arrangement | exponential | | ❌ |
| Greedy with `max()` over three counts each step | O(n) | O(1) | ✅ With only 3 letters this is just as good |
| **Greedy with a max-heap** | **O(n log 3) = O(n)** | O(1) | ✅ Generalises cleanly to "k letters" |

**The decision: a [max-heap](../data-structures/heap.md) of `(−count, letter)`** (Python's `heapq` is a min-heap, so negate the counts). Same family as [Reorganize String](767-reorganize-string.md) and [Task Scheduler](621-task-scheduler.md).

Each step:

1. Pop the most plentiful letter `X`.
2. If the string already ends with `XX`: pop the next best letter `Y`, place **it** instead, then push **both** back. If the heap is empty at that point, stop.
3. Otherwise place `X` and push it back if any remain.

The "pop a second letter" move is the whole difficulty. The blocked letter goes back on the heap unchanged, so it will be used on the next round.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
heap = []
for count, letter in ((a, 'a'), (b, 'b'), (c, 'c')):
    if count > 0:
        heapq.heappush(heap, (-count, letter))
```

Push only letters with a positive supply. The count is negated so the *largest* count pops first.
→ [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
result = []

while heap:
    count1, letter1 = heapq.heappop(heap)
```

Take the most plentiful letter. `result` is a list (joined at the end) because string `+=` in a loop copies.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-methods](../syntax/list-methods.md)

```python
    if len(result) >= 2 and result[-1] == letter1 and result[-2] == letter1:
        if not heap:
            break
```

**Blocked:** the last two letters are the same as our pick. If there is nothing else to use, the string can't be extended: stop.
→ [logical-operators](../syntax/logical-operators.md) · [break-continue](../syntax/break-continue.md)

```python
        count2, letter2 = heapq.heappop(heap)
        result.append(letter2)
        count2 += 1
        if count2 < 0:
            heapq.heappush(heap, (count2, letter2))
        heapq.heappush(heap, (count1, letter1))
```

Use the **second best** instead. Counts are negative, so `+= 1` means "one used up". Push it back only if some remain, and put the blocked letter back untouched.

```python
    else:
        result.append(letter1)
        count1 += 1
        if count1 < 0:
            heapq.heappush(heap, (count1, letter1))

return "".join(result)
```

**Normal case:** place the most plentiful letter and put it back with one fewer if any are left.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq


class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        heap = []
        for count, letter in ((a, 'a'), (b, 'b'), (c, 'c')):
            if count > 0:
                heapq.heappush(heap, (-count, letter))

        result = []

        while heap:
            count1, letter1 = heapq.heappop(heap)

            if len(result) >= 2 and result[-1] == letter1 and result[-2] == letter1:
                if not heap:
                    break
                count2, letter2 = heapq.heappop(heap)
                result.append(letter2)
                count2 += 1
                if count2 < 0:
                    heapq.heappush(heap, (count2, letter2))
                heapq.heappush(heap, (count1, letter1))
            else:
                result.append(letter1)
                count1 += 1
                if count1 < 0:
                    heapq.heappush(heap, (count1, letter1))

        return "".join(result)
```

</details>

**Trace it.** `a = 1, b = 1, c = 7`:

| Heap top | Last two | Action | `result` |
|---|---|---|---|
| c (7) | | place c | `c` |
| c (6) | `c` | place c | `cc` |
| c (5) | `cc` blocked | use next best (a or b): a | `cca` |
| c (5) | `ca` | place c | `ccac` |
| c (4) | `ac` | place c | `ccacc` |
| c (3) | `cc` blocked | use b | `ccaccb` |
| c (3) | `cb` | place c | `ccaccbc` |
| c (2) | `bc` | place c | `ccaccbcc` |
| c (1) | `cc` blocked, heap empty | **stop** | `ccaccbcc` ✅ (length 8, as expected) |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

The result has at most `a + b + c` letters. Each step does a constant number of heap operations on a heap of **at most 3 elements**, so each is O(log 3) = O(1). Total **O(a + b + c)**.

For `k` letters it would be O(n log k).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) beyond the output</summary>

The heap never exceeds 3 entries. The output list is O(n) but is the answer itself.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "To make the string as long as possible I always spend the letter I have the most of, since that's the one that would otherwise get stranded. A max-heap of counts gives it to me each step. The only constraint is no three in a row, so if the last two letters equal the heap's top, I use the second most plentiful letter instead and push the top back. If there's no second letter, I stop. Each step is O(1) because the heap has at most 3 items, so it's O(n) overall."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is greedy correct?" | Using the biggest pile first minimises the chance it's left over. Switching away only when forced keeps the string valid. Randomised tests against exhaustive search confirm the lengths |
| "More letters?" | The heap generalises. O(n log k) |
| "Without a heap?" | With three letters, sort three `(count, letter)` pairs each step. Same logic |
| "Longer runs allowed (up to `m`)?" | Replace the "last two" check with "last `m`" |
| "Related?" | [Reorganize String](767-reorganize-string.md) (no two *adjacent* equal letters) · [Task Scheduler](621-task-scheduler.md) |

**Traps:**

- **Pushing back an exhausted letter** (count 0). It would be popped later and placed with a "negative" supply.
- **Forgetting to push the blocked letter back.** It vanishes and the string ends early.
- **Using the second letter without checking that the heap has one.** `heappop` on an empty heap crashes.
- **Python's min-heap:** forgetting to negate the counts places the *least* plentiful letter first.

**This same move shows up in:** [Reorganize String](767-reorganize-string.md) · [Task Scheduler](621-task-scheduler.md) · [Last Stone Weight](1046-last-stone-weight.md) (repeatedly take the largest).

</details>

---
