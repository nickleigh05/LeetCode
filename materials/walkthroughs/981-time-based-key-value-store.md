# 981. Time Based Key-Value Store

**Medium** · [LeetCode](https://leetcode.com/problems/time-based-key-value-store/)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Design a time-based key-value data structure that stores multiple values for the same key at different timestamps, and retrieves the value at a given point in time.

- **`set(key, value, timestamp)`** — store the key with the value at that timestamp.
- **`get(key, timestamp)`** — return the value set for `key` with the **largest `timestamp_prev <= timestamp`**. If there is none, return `""`.

```
set("foo", "bar", 1)
get("foo", 1)   →  "bar"
get("foo", 3)   →  "bar"    (nothing at 3, so the value from time 1)
set("foo", "bar2", 4)
get("foo", 4)   →  "bar2"
get("foo", 5)   →  "bar2"
```

**Constraints:** `1 <= timestamp <= 10⁷` · ⚠️ **all `set` calls for a given key have strictly increasing timestamps** · up to 2·10⁵ calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Design** a structure" | A class with persistent state — like [Min Stack](155-min-stack.md) |
| "multiple values for the same key" | Each key owns a *history*, not a single value |
| "largest `timestamp_prev` **<= timestamp**" | ⚠️ Not an exact match — a **predecessor search**. This is the whole problem |
| "**strictly increasing** timestamps per key" | ⚠️⚠️ **The gift.** Each key's history is **already sorted** — you never have to sort it |
| return `""` if none | A defined not-found result |
| up to 2·10⁵ calls | O(n) per `get` would be 4·10¹⁰ overall. Need **O(log n)** |

Two independent lookups are happening, and separating them is the key design move:

1. **Which key?** → a hash map, O(1).
2. **Which timestamp within that key's history?** → the interesting part.

The second is a **predecessor query**: not "find this exact value" but "find the largest value that doesn't exceed the target." Since the timestamps arrive sorted, this is binary search — with the same *record-and-continue* shape as [Koko Eating Bananas](875-koko-eating-bananas.md).

**Why the increasing-timestamps guarantee matters so much.** Without it, each `set` would need an O(n) insertion to keep the list sorted, or you'd sort on every `get`. With it, `set` is a plain O(1) append and the list is sorted for free. **Always look for a constraint like this — it's the difference between an easy solution and a hard one.**

🤔 **Before you open the next section:** if the target timestamp doesn't exist exactly, standard binary search returns "not found". How do you get it to return the *closest earlier* entry instead?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `set` | `get` | Verdict |
|---|---|---|---|
| List of all entries, filter on get | O(1) | O(n) | ❌ 2·10⁵ gets × 2·10⁵ entries |
| Dict of key → dict of timestamp → value | O(1) | O(n) to find the predecessor | ❌ Hash maps can't answer "largest ≤ x" |
| Dict of key → **sorted list**, binary search | **O(1)** | **O(log n)** | ✅ |
| Balanced BST / `SortedList` per key | O(log n) | O(log n) | ⚠️ Correct, but unnecessary machinery |

**The decision: a [hash map](../data-structures/hashmap.md) from key → list of `(timestamp, value)` pairs, with binary search on `get`.**

Note the third row's point carefully: **a hash map alone cannot solve this.** Hashing gives O(1) *exact* lookup but destroys ordering, so it can't answer "largest key ≤ x". You need an ordered structure for that dimension — and a sorted list is the cheapest one available, given the input already arrives in order.

**The binary search variant: predecessor search.** Unlike [704](704-binary-search.md), you don't return on a match. Instead:

- **`values[mid][0] <= timestamp`** → this entry is a **valid candidate** (at or before the query time). Record it, then search **right** for something even later but still valid.
- **`values[mid][0] > timestamp`** → too late to be valid. Discard it and everything right of it.

The last recorded candidate is the answer. It's [Koko](875-koko-eating-bananas.md)'s *record-and-continue* shape, mirrored: Koko minimized and searched left; here you maximize and search right.

**Initializing `result = ""`** handles "no valid entry" with no special case — if every timestamp is too late, nothing is ever recorded and the empty string falls through.

**Why not `bisect`?** [`bisect_right(timestamps, timestamp) - 1`](../syntax/bisect-module.md) gives the same index and is the right production code. Writing the loop is the point here, but mention the built-in.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.store = {}
```

`key → list of (timestamp, value)` pairs. One list per key, each kept in increasing timestamp order by the input guarantee.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [dict-basics](../syntax/dict-basics.md)

```python
def set(self, key: str, value: str, timestamp: int) -> None:
    if key not in self.store:
        self.store[key] = []
    self.store[key].append((timestamp, value))
```

Create the list on first use, then **append** — O(1) amortized.

The append keeps the list sorted **only because the problem guarantees increasing timestamps**. Without that promise you'd need an O(n) insertion at the right position. This one line is where the constraint pays off.

Storing a tuple keeps each timestamp bound to its value through the search.
→ [membership-operators](../syntax/membership-operators.md) · [list-methods](../syntax/list-methods.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
def get(self, key: str, timestamp: int) -> str:
    values = self.store.get(key, [])
    result = ""
```

`.get(key, [])` returns an empty list for an unknown key — so the loop simply doesn't run and `""` is returned. No `KeyError`, no explicit guard.

`result = ""` is both the default answer and the accumulator for the best candidate found.
→ [dict-methods](../syntax/dict-methods.md)

```python
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = (left + right) // 2
```

The standard inclusive-range skeleton from [704](704-binary-search.md).
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        if values[mid][0] <= timestamp:
            result = values[mid][1]
            left = mid + 1
```

**The predecessor logic.** `values[mid][0]` is the timestamp, `[1]` the value.

This entry is at or before the query time, so it's a **valid** answer — record it. But a *later* valid entry may exist, so **keep searching right** rather than returning.

`<=` because an exact timestamp match is valid.
→ [comparison-operators](../syntax/comparison-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
        else:
            right = mid - 1
```

This entry is **after** the query time — invalid, and so is everything to its right (timestamps only increase). Discard that whole half.
→ [elif-else](../syntax/elif-else.md)

```python
    return result
```

The last recorded candidate — the largest valid timestamp — or `""` if none was ever valid.

<details>
<summary>The whole thing together</summary>

```python
class TimeMap:

    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        values = self.store.get(key, [])
        result = ""

        left = 0
        right = len(values) - 1

        while left <= right:
            mid = (left + right) // 2

            if values[mid][0] <= timestamp:
                result = values[mid][1]
                left = mid + 1
            else:
                right = mid - 1

        return result
```

</details>

**Trace it** — after `set("foo","a",1)`, `set("foo","b",4)`, `set("foo","c",9)`, so `values = [(1,"a"), (4,"b"), (9,"c")]`.

**`get("foo", 6)`:**

| `left` | `right` | `mid` | timestamp there | ≤ 6? | Action | `result` |
|---|---|---|---|---|---|---|
| 0 | 2 | 1 | 4 | ✅ valid | record `"b"`, search right | **"b"** |
| 2 | 2 | 2 | 9 | ✗ too late | search left | "b" |
| 2 | 1 | — | | | exit | **"b"** ✅ |

Correct — at time 6 the most recent set was at time 4.

**`get("foo", 0)`:**

| `left` | `right` | `mid` | timestamp | ≤ 0? | Action |
|---|---|---|---|---|---|
| 0 | 2 | 1 | 4 | ✗ | `right = 0` |
| 0 | 0 | 0 | 1 | ✗ | `right = -1` |
| 0 | −1 | — | | | exit → `""` ✅ |

Nothing was ever recorded, so the initialized `""` is returned — the not-found case handled for free.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) set, O(log n) get</summary>

| Operation | Cost |
|---|---|
| **`set`** | **O(1)** — a dict lookup and a list append (amortized) |
| **`get`** | **O(log n)** — a dict lookup plus binary search over that key's n entries |

where n is the number of values stored **for that particular key** — not the total across all keys, since each key has its own list. Worth stating precisely; it's a better bound than "O(log total)".

**Where the guarantee earns its keep.** Without increasing timestamps, `set` would need to insert in sorted position — O(n) per call, or O(log n) with a balanced structure. The problem hands you sortedness, so `set` stays a plain append.

**Total for 2·10⁵ operations:** ~2·10⁵ × log₂(2·10⁵) ≈ 2·10⁵ × 18 = 3.6·10⁶. Instant. The linear-scan version would be ~4·10¹⁰.

**The design lesson:** the hash map and the sorted list each handle the dimension they're good at — O(1) exact lookup for keys, O(log n) ordered lookup for timestamps. **Combining structures so each covers the other's weakness** is what "design" problems are really testing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, where n is the total number of `set` calls.

Every call stores one `(timestamp, value)` tuple, and nothing is ever removed. Across all keys the lists hold exactly n entries, plus O(k) for the k distinct keys in the dict.

**No compression is possible** here, because `get` can query *any* past timestamp — the full history is genuinely needed. Contrast with [Min Stack](155-min-stack.md), where the min-stack could skip non-minima; there, only depths reachable by popping mattered.

**The binary search itself is O(1) space** — three integers, as always in this unit. All the memory is the stored data, which is inherent to the problem rather than a cost of the algorithm.

**If memory were a concern:** you could deduplicate consecutive identical values (if `set("foo","a",5)` follows `set("foo","a",3)`, the second is redundant for `get` purposes). A reasonable optimization to mention, not to implement unprompted.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two lookups: the key, and the timestamp within that key's history. A hash map handles the key in O(1), but it can't answer 'largest timestamp ≤ x' — hashing destroys ordering. So per key I keep a list of `(timestamp, value)` pairs. The crucial constraint is that timestamps arrive strictly increasing, so `set` is just an append and the list is sorted for free. For `get` I binary search, but it's a predecessor search rather than an exact match: when a midpoint's timestamp is at or before the query I record it as a candidate and keep searching right for a later valid one; otherwise I discard that half. The last recorded candidate is the answer, and initializing it to the empty string handles the not-found case. O(1) set, O(log n) get, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if timestamps *weren't* increasing?" | **The question.** `set` becomes O(n) to insert in order, or use a balanced BST / `SortedList` for O(log n) both ways. |
| "Why not a dict of timestamp → value?" | Hash maps only do exact lookups. "Largest key ≤ x" needs order, which hashing destroys. |
| "Use the standard library." | `bisect_right(timestamps, timestamp) - 1` gives the same index. See [bisect-module](../syntax/bisect-module.md). Store timestamps in a parallel list, since `bisect` needs a comparable sequence. |
| "Support deletion / range queries?" | Now you want a real ordered structure per key — a balanced BST or skip list. See [balanced-bst](../data-structures/balanced-bst.md). |
| "Memory is a problem — millions of sets." | Deduplicate consecutive identical values, or evict history older than a retention window. |
| "Make it thread-safe?" | Per-key locks, or a copy-on-write list per key. A systems answer, and a good sign if you raise it. |
| "How is this different from a plain cache?" | A cache stores *current* values; this is a versioned store answering historical queries — closer to MVCC in a database. |

**Traps:**

- **Returning on an exact match only.** The query timestamp usually *doesn't* exist — you need the predecessor, not equality.
- **`values[mid][0] < timestamp`** with strict `<` — an exact match is valid and would be missed.
- **Searching left after finding a valid candidate.** You want the *largest* valid timestamp, so continue right.
- **Not initializing `result`** — you'd need an explicit not-found branch, and it's easy to return `None` instead of `""`.
- **`self.store[key]` without a default** in `get` — `KeyError` on an unseen key. Use `.get(key, [])`.
- **One shared list for all keys.** You'd have to filter by key first, losing the binary search.

**This same move shows up in:** [Koko Eating Bananas](875-koko-eating-bananas.md) (the record-and-continue shape, mirrored) · [Binary Search](704-binary-search.md) (the skeleton) · [Min Stack](155-min-stack.md) (a design problem solved by pairing structures) · [LRU Cache](146-lru-cache.md) (hash map + a second structure, each covering the other's weakness).

</details>
