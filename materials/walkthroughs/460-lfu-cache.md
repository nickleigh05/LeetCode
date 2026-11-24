# 460. LFU Cache

**Hard** · [LeetCode](https://leetcode.com/problems/lfu-cache/) · [Solution file (no hints)](../../problems/0001-0499/460.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Design a **Least Frequently Used** cache with a fixed `capacity`.

- `get(key)` returns the value, or `-1` if absent. It counts as a **use**.
- `put(key, value)` inserts or updates a key (also a use). When the cache is **full**, first evict the **least frequently used** key. If several keys tie on frequency, evict the **least recently used** among them.

Both operations must run in **O(1)** average time.

```
LFUCache(2)
put(1, 1)  put(2, 2)
get(1)      → 1          (key 1 now used twice)
put(3, 3)                (full: evict key 2, used once, least frequent)
get(2)      → -1
get(3)      → 3
put(4, 4)                (full: keys 1 and 3 each used twice. Evict 1, the older one)
get(1)      → -1
get(3)      → 3
get(4)      → 4
```

**Constraints:** `0 <= capacity <= 10⁴` · `0 <= key <= 10⁵` · `0 <= value <= 10⁹` · up to `2 * 10⁵` calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "least **frequently** used" | Each key carries a **use count**, and the lowest count loses |
| tie → "least **recently** used" | Within one count you need an **ordering by recency**. That's [LRU Cache](146-lru-cache.md) nested inside each count |
| `get` **and** `put` count as uses | Both must bump the frequency |
| O(1) for both | No heaps (O(log n)), no scanning for the minimum |
| `capacity = 0` possible | `put` must do nothing. Guard it, or you'll evict from an empty cache |
| a **new** key | Enters with frequency 1, and the "minimum frequency" resets to 1 |

The design question is: how do you get at "the oldest key among those with the lowest count" in O(1)?

**Group the keys by frequency.** Keep a bucket per count, and keep each bucket in recency order. Then:

- Evicting = take the **oldest** entry of the bucket for the **minimum** frequency.
- Using a key = lift it out of its bucket and drop it at the **newest** end of the next bucket up.

Track the minimum frequency in a single integer. It only changes in two ways: a new key resets it to 1, and when a use empties the minimum bucket it moves up by one.

🤔 **Before you open the next section:** which structure gives you "remove this key from the middle" **and** "pop the oldest" **and** "append the newest", all in O(1)?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `get` / `put` | Verdict |
|---|---|---|
| Scan for the minimum count on every eviction | O(n) | ❌ |
| Min-heap on `(freq, last_used)` | O(log n) | ⚠️ Fast enough in practice, but the stated requirement is O(1), and updates need lazy deletion |
| **Hash maps + one ordered bucket per frequency** | **O(1)** | ✅ |

**The decision: three pieces of state.**

1. `vals`: `key → value`
2. `freq`: `key → count`
3. `buckets`: `count → OrderedDict of keys` (an ordered set, oldest first)

plus one integer, `min_freq`.

Python's `OrderedDict` is the shortcut: it is a hash map that **remembers insertion order**, with O(1) `popitem(last=False)` (pop the oldest) and O(1) deletion by key. That replaces the hand-built doubly linked list from [LRU Cache](146-lru-cache.md). Interviewers also accept a doubly linked list per frequency. The idea is identical, the code is longer. See [hashmap](../data-structures/hashmap.md) and [doubly-linked-list](../data-structures/doubly-linked-list.md).

LFU is LRU with a **second dimension**. LRU needs one recency list. LFU needs one recency list **per frequency**.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import OrderedDict, defaultdict

class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.vals = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0
```

`vals` and `freq` answer "what's the value / count of this key?". `buckets[f]` holds every key whose count is `f`, oldest first. The `defaultdict` creates a bucket the first time one is needed. `min_freq` points at the bucket we evict from.
→ [defaultdict](../syntax/defaultdict.md) · [ordered-dict-notes](../syntax/ordered-dict-notes.md) · [init-method](../syntax/init-method.md) · [dict-basics](../syntax/dict-basics.md)

```python
    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f] and self.min_freq == f:
            self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None
```

**The heart of it: record one use.** Take the key out of its current bucket. If that was the *minimum* bucket and it's now empty, the new minimum is `f + 1` (this very key is about to live there). Then bump the count and append the key to the **end** (newest) of the next bucket. Every `get` and every update-`put` calls this.
→ [dict-basics](../syntax/dict-basics.md) · [if-return](../syntax/if-return.md) · [function-basics](../syntax/function-basics.md)

```python
    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]
```

A miss changes nothing. A hit is a use, then return the value.
→ [membership-operators](../syntax/membership-operators.md)

```python
    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
```

Zero capacity can store nothing. An existing key just gets its value overwritten and counts as a use. It never evicts, so we're done.

```python
        if len(self.vals) == self.capacity:
            oldest, _ = self.buckets[self.min_freq].popitem(last=False)
            del self.vals[oldest]
            del self.freq[oldest]
```

A new key and a full cache: evict. `buckets[min_freq]` holds the least-frequently-used keys, and `popitem(last=False)` pops the **oldest** of them, which is the LRU tie-break, for free.

```python
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
```

Insert the new key at frequency 1, newest in bucket 1. The minimum frequency is now exactly 1, because nothing can be used fewer times than a brand-new key.

<details>
<summary>The whole thing together</summary>

```python
from collections import OrderedDict, defaultdict


class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.vals = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f] and self.min_freq == f:
            self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return

        if len(self.vals) == self.capacity:
            oldest, _ = self.buckets[self.min_freq].popitem(last=False)
            del self.vals[oldest]
            del self.freq[oldest]

        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
```

</details>

**Trace it.** `capacity = 2`:

| Call | `buckets` after | `min_freq` | Result |
|---|---|---|---|
| `put(1,1)` | `{1: [1]}` | 1 | |
| `put(2,2)` | `{1: [1, 2]}` | 1 | |
| `get(1)` | `{1: [2], 2: [1]}` | 1 | 1 |
| `put(3,3)` | full, evict oldest of bucket 1 = **key 2**. `{1: [3], 2: [1]}` | 1 | |
| `get(2)` | | | **-1** |
| `get(3)` | `{2: [1, 3]}` (bucket 1 emptied) | **2** | 3 |
| `put(4,4)` | full, bucket 2 is `[1, 3]`, evict oldest = **key 1**. `{1: [4], 2: [3]}` | 1 | |
| `get(1)` | | | **-1** |

Key 1 and key 3 tied on frequency; the older one lost.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) per operation</summary>

**O(1) average** for `get` and `put`. Every step is a hash lookup, a delete by key, a pop from the front, or an append: all O(1) on `dict` and `OrderedDict`. `min_freq` is maintained with simple increments, never searched for.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(capacity)</summary>

**O(capacity).** Each cached key appears once in `vals`, once in `freq`, and once in exactly one bucket. Empty buckets stay as empty dictionaries, so deleting them is a small optimisation, not a requirement.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "LFU needs the least-frequently-used key, with ties broken by least-recent use, in O(1). I'll keep a value map and a frequency map, plus one ordered bucket per frequency, oldest first. A use moves a key from bucket f to the newest slot of bucket f+1. Eviction pops the oldest key of the minimum-frequency bucket. I track `min_freq` in one variable: a new key sets it to 1, and moving the last key out of the minimum bucket bumps it by one. That makes both operations O(1) with O(capacity) space. It's LRU with a second dimension."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Without `OrderedDict`?" | A doubly linked list per frequency, with a `key → node` map. Same moves, more pointer code. See [doubly-linked-list](../data-structures/doubly-linked-list.md) |
| "Why not a heap?" | Updating a key's priority in a heap is O(log n) or needs lazy deletion. The O(1) requirement rules it out |
| "How does LFU differ from LRU?" | LRU evicts by recency alone. LFU evicts by count first, so a once-hot key that is now cold can linger. Real systems often age the counts |
| "How does `min_freq` stay correct?" | It only goes up when its bucket empties through a use, and it resets to 1 on any insert. Eviction removes from the minimum bucket, and the insert that follows resets it anyway |
| "Capacity 0?" | `put` returns immediately |
| "Concurrency?" | Needs a lock around `_touch` and eviction because both mutate several structures |

**Traps:**

- **Forgetting `min_freq = 1` after inserting a new key.** The next eviction looks in the wrong bucket.
- **Forgetting to bump `min_freq`** when the minimum bucket empties after a `get`.
- **Treating `put` on an existing key as a fresh insert.** It must be a *use*, not a reset to 1.
- **Evicting before checking whether the key already exists.** Updating an existing key never evicts.
- **Skipping `capacity == 0`.** `popitem` on an empty bucket raises an error.

**This same move shows up in:** [LRU Cache](146-lru-cache.md) (one recency list) · [Min Stack](155-min-stack.md) (an O(1) minimum) · [Maximum Frequency Stack](895-maximum-frequency-stack.md) (buckets by frequency again).

</details>

---
