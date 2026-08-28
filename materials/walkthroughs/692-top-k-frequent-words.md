# 692. Top K Frequent Words

**Medium** · [LeetCode](https://leetcode.com/problems/top-k-frequent-words/) · [Solution file (no hints)](../../problems/0500-0999/692.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

Given an array of strings `words` and an integer `k`, return the `k` most frequent strings, sorted by **frequency descending**. Words with the **same frequency** are ordered **lexicographically ascending**.

```
words = ["i","love","leetcode","i","love","coding"], k = 2  →  ["i","love"]
words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
  →  ["the","is","sunny","day"]
```

**Constraints:** `1 <= words.length <= 500` · `1 <= words[i].length <= 10` · lowercase · `1 <= k <= number of unique words`

**Follow-up:** can you solve it in **O(n log k)** time and **O(n)** space?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "k most **frequent**" | Count first — this is [Top K Frequent Elements](347-top-k-frequent-elements.md) with a twist |
| "frequency **highest to lowest**" | Descending on the primary key |
| ties broken **lexicographically ascending** | ⚠️ **The twist.** The two sort keys point in **opposite directions** |
| `k <= unique words` | No "not enough words" case |
| follow-up: **O(n log k)** | Rules out sorting everything — a size-`k` heap is wanted |

**The whole difficulty is the mixed-direction ordering.**

```
frequency:      DESCENDING   (higher is better)
word (on tie):  ASCENDING    (lexicographically smaller is better)
```

With a plain sort that's easy — Python's `sort` is stable and accepts a tuple key:

```python
sorted(count, key=lambda w: (-count[w], w))[:k]
```

Negating the frequency flips it to descending while leaving the word ascending. Clean, correct, **O(n log n)**.

But the follow-up wants **O(n log k)** via a size-`k` heap — and that's where the mixed directions bite.

**Why the heap version is subtle.** The size-`k` heap pattern from [Kth Largest](215-kth-largest-element-in-an-array.md) says: *keep a min-heap of the `k` best, evict the root.* The root must be the **worst** of your current top-`k` — the one to discard.

Here "worst" means: **lowest frequency**, and among equal frequencies, **lexicographically largest**. So the heap ordering must be:

| Key component | Heap order | Achieved by |
|---|---|---|
| frequency | ascending (min at root) | `count[w]` as-is |
| word | **descending** (largest at root) | ⚠️ needs inverting |

Python can't negate a string, so the standard trick is a small wrapper class defining `__lt__` — or, more simply, **push `(count, word)` into a max-heap of size `n`** and pop `k` times, which is O(n + k log n) rather than O(n log k).

🤔 **Before you open the next section:** if your heap holds the `k` best words so far, which word should sit at the root ready to be evicted — and how does that differ for frequency versus alphabetical order?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n` = number of words, `u` = unique words.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Count + sort by `(-freq, word)`** | One tuple key handles both directions | O(n + u log u) | O(u) | ✅ Clearest; fine at these limits |
| **Count + max-heap, pop `k`** | Heapify all, extract `k` | **O(n + u + k log u)** | O(u) | ✅ Avoids full sort |
| **Count + size-`k` min-heap** | Keep only the `k` best | **O(n + u log k)** | O(k) | ✅✅ Meets the follow-up; needs a custom comparator |
| Bucket by frequency | Index buckets by count, sort each | O(n + u log u) worst | O(n) | ⚠️ Buckets still need sorting for ties |

**The decision depends on whether you're answering the follow-up.**

**Start with the sort.** It's one line, obviously correct, and the tuple key `(-count[w], w)` expresses the mixed ordering perfectly. At `n <= 500` this is genuinely the right answer.

**For O(n log k), use a size-`k` min-heap** — but you must invert the *word* comparison only. Two ways:

**Option A — a wrapper class:**

```python
class Word:
    def __init__(self, word, freq):
        self.word, self.freq = word, freq
    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq      # lower freq = "worse" = closer to root
        return self.word > other.word          # lexicographically LARGER = "worse"
```

The `__lt__` defines "worse than," so the root is always the least desirable entry — exactly the eviction candidate.

**Option B — the max-heap over all unique words:**

```python
heap = [(-freq, word) for word, freq in count.items()]
heapq.heapify(heap)                                  # O(u)
return [heapq.heappop(heap)[1] for _ in range(k)]    # O(k log u)
```

Negating the frequency makes higher counts sort first; the word stays ascending, which is exactly the tie-break. **No custom class needed** — and it's the version to reach for under time pressure.

It's O(n + u + k log u) rather than O(n log k). Technically that misses the follow-up's letter when `k ≪ u`, but it's simpler and often faster in practice since `heapify` is O(u).

**Why negating the frequency works but negating the word doesn't.** `-freq` flips a number's order trivially. Strings have no negation, so a tuple like `(-freq, -word)` is impossible. That asymmetry is the entire reason this problem is harder than [Top K Frequent Elements](347-top-k-frequent-elements.md), where both keys point the same way.

**Why bucket sort doesn't fully solve it.** Bucketing by frequency gives O(n) grouping, but each bucket still needs lexicographic sorting for ties — so the worst case (all words equally frequent) is back to O(u log u).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**The primary version — count, then max-heap**

```python
from collections import Counter
import heapq

count = Counter(words)
```

Frequency map in one pass — **O(n)**.
→ [counter](../syntax/counter.md)

```python
heap = [(-freq, word) for word, freq in count.items()]
heapq.heapify(heap)
```

**The tuple `(-freq, word)` encodes both orderings at once.**

Python compares tuples element-wise:

1. `-freq` ascending in the min-heap ⇒ **higher frequency first** ✅
2. On a tie, `word` ascending ⇒ **lexicographically smallest first** ✅

Exactly the required ordering, with no custom comparator.

`heapify` builds in **O(u)**, versus O(u log u) for repeated pushes.
→ [heapq-module](../syntax/heapq-module.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
return [heapq.heappop(heap)[1] for _ in range(k)]
```

**Pop `k` times**, taking `[1]` to extract the word from each `(-freq, word)` tuple.

Each pop is O(log u), so this is O(k log u).
→ [list-comprehension](../syntax/list-comprehension.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import Counter
import heapq

class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:

        count = Counter(words)

        heap = [(-freq, word) for word, freq in count.items()]
        heapq.heapify(heap)

        return [heapq.heappop(heap)[1] for _ in range(k)]
```

</details>

<details>
<summary>The one-line sort (simplest)</summary>

```python
from collections import Counter

class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        count = Counter(words)
        return sorted(count, key=lambda w: (-count[w], w))[:k]
```

The same tuple key, applied as a sort key. O(n + u log u). At `n <= 500` this is the answer to write first.

</details>

<details>
<summary>The size-k heap (meets the O(n log k) follow-up)</summary>

```python
from collections import Counter
import heapq

class Word:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq     # lower frequency is "worse"
        return self.word > other.word         # larger word is "worse"


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        count = Counter(words)

        heap = []
        for word, freq in count.items():
            heapq.heappush(heap, Word(word, freq))
            if len(heap) > k:
                heapq.heappop(heap)           # evict the worst

        return [heapq.heappop(heap).word for _ in range(len(heap))][::-1]
```

`__lt__` defines "worse," so the root is always the eviction candidate. The heap holds only `k` entries → **O(n + u log k)** time, **O(k)** space. The final reversal is needed because popping a min-heap yields worst-to-best.

</details>

**Trace it** — `words = ["the","day","is","sunny","the","the","the","sunny","is","is"]`, `k = 4`:

**Counts:** `the: 4, is: 3, sunny: 2, day: 1`

**Heap entries** as `(-freq, word)`:

```
(-4, "the"), (-3, "is"), (-2, "sunny"), (-1, "day")
```

| Pop | Tuple | Word |
|---|---|---|
| 1 | `(-4, "the")` | **the** |
| 2 | `(-3, "is")` | **is** |
| 3 | `(-2, "sunny")` | **sunny** |
| 4 | `(-1, "day")` | **day** |

Return **`["the","is","sunny","day"]`** ✅

**The tie-break case** — `words = ["i","love","leetcode","i","love","coding"]`, `k = 2`:

**Counts:** `i: 2, love: 2, leetcode: 1, coding: 1`

Heap entries: `(-2,"i"), (-2,"love"), (-1,"coding"), (-1,"leetcode")`

| Pop | Tuple | Why it came first |
|---|---|---|
| 1 | `(-2, "i")` | frequency ties with `"love"`, but `"i" < "love"` ✅ |
| 2 | `(-2, "love")` | same frequency, next alphabetically |

Return **`["i","love"]`** ✅

The starred behaviour: `"i"` and `"love"` both have frequency 2, so the tuple's **second** element decides — and since it isn't negated, ascending string order wins, exactly as specified.

Contrast what would happen with a naive `(-freq, -something)` attempt: you can't negate `"love"`, which is precisely why the tuple approach only works when the *string* key already points the right way.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + u + k log u)</summary>

For the primary (heapify + pop) version:

| Phase | Cost |
|---|---|
| `Counter(words)` | **O(n)** |
| Build tuple list | O(u) |
| `heapify` | **O(u)** |
| `k` pops | **O(k log u)** |

Total **O(n + u + k log u)**.

**Compare the three approaches:**

| | Time | Space | Meets O(n log k)? |
|---|---|---|---|
| Sort | O(n + u log u) | O(u) | ❌ |
| **Heapify + pop k** | **O(n + u + k log u)** | O(u) | ⚠️ close, not literally |
| **Size-k heap** | **O(n + u log k)** | **O(k)** | ✅ |

At `n <= 500` all three are instantaneous — the follow-up is about demonstrating you know the size-`k` pattern, not about measurable speed.

**Why `heapify` matters.** Building from a list is O(u); pushing `u` items individually is O(u log u). One function call, meaningful difference.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(u) or O(k)</summary>

| Approach | Space |
|---|---|
| Counter | O(u) — unavoidable, you must count |
| Sort | O(u) for the sorted list |
| Heapify all | O(u) for the heap |
| **Size-k heap** | **O(k)** for the heap (plus O(u) for the counts) |

The counter is O(u) regardless, so the size-`k` heap's advantage is bounded here — it saves on the *heap*, not the counting. That differs from [Kth Largest Integer](1985-find-the-kth-largest-integer-in-the-array.md), where no counting step is needed and O(k) is the true total.

**The transferable lesson is about comparator direction:**

> **In a size-`k` heap, the root must be the element you'd most like to evict.** So the heap's ordering is the *inverse* of "best" — and when the sort keys point in opposite directions, only the numeric one can be negated. The other needs a custom `__lt__`.

That asymmetry — numbers negate, strings don't — is the specific thing this problem teaches, and it's why it's rated harder than [Top K Frequent Elements](347-top-k-frequent-elements.md) despite nearly identical structure.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Count with a `Counter`, then select the top `k`. The interesting part is that the two sort keys point in **opposite** directions — frequency descending, but words ascending on ties. With a sort that's a one-liner: key on `(-count[w], w)`, since negating the frequency flips it while leaving the word ascending. For a heap I use the same tuple: `(-freq, word)` in a min-heap puts the highest frequency at the root, and ties resolve by ascending word — exactly right. I `heapify` in O(u) and pop `k` times. To hit the follow-up's O(n log k) I'd keep a size-`k` heap instead, but that needs a custom `__lt__` class, because the root must be the *worst* entry — lowest frequency, and among ties the lexicographically **largest** — and you can't express 'descending string' by negation the way you can with a number."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(n log k)?" | **The stated follow-up** — a size-`k` min-heap with a custom `__lt__` defining "worse": lower frequency, or larger word on a tie. |
| "Why can't you just use `(-freq, -word)`?" | **The key point.** Strings can't be negated. Only the numeric key flips by negation. |
| "How does this differ from [Top K Frequent Elements](347-top-k-frequent-elements.md)?" | There the tie-break is unspecified, so both keys align and `(-freq, value)` suffices. Here the opposing directions force a custom comparator for the size-`k` version. |
| "Bucket sort by frequency?" | O(n) to bucket, but each bucket still needs lexicographic sorting — worst case O(u log u). |
| "What if ties should be **descending** alphabetically?" | Then both keys align: `(-freq, word)` reversed, or negate frequency and reverse the word comparison — the size-`k` version gets simpler. |
| "Why `heapify` over pushes?" | O(u) versus O(u log u). |
| "Return the counts too?" | Pop the full tuple and negate the frequency back. |

**Traps:**

- **Sorting by frequency alone.** Ties come out in arbitrary (dict-insertion) order, silently failing on the first example.
- **Trying to negate the word.** Impossible; this is why the size-`k` version needs a class.
- **Getting `__lt__` backwards in the size-`k` heap.** It defines "worse," not "better" — the root must be the eviction candidate.
- **Forgetting to reverse the size-`k` heap's output.** Popping a min-heap yields worst-to-best.
- **Building the heap with repeated `heappush`.** O(u log u) instead of O(u).
- **Forgetting `[1]` when popping tuples.** Returns `(-4, "the")` instead of `"the"`.

**This same move shows up in:** [Top K Frequent Elements](347-top-k-frequent-elements.md) (the same count-then-select structure, without the opposing tie-break) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (the size-`k` heap pattern in its simplest form) · [Find the Kth Largest Integer in the Array](1985-find-the-kth-largest-integer-in-the-array.md) (another problem where the *comparison rule* is the difficulty) · [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) (counting plus ordering by count).

</details>

---
