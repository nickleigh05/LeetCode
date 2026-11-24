# 706. Design HashMap

**Easy** · [LeetCode](https://leetcode.com/problems/design-hashmap/) · [Solution file (no hints)](../../problems/0500-0999/706.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Design a `MyHashMap` **without using any built-in hash table library**.

- `put(key, value)` inserts the pair, or **updates** the value if the key exists.
- `get(key)` returns the value, or `-1` if the key is absent.
- `remove(key)` deletes the key and its value, if present.

```
put(1, 1)    put(2, 2)
get(1)   →  1
get(3)   →  -1       (never stored)
put(2, 1)            (update)
get(2)   →  1
remove(2)
get(2)   →  -1
```

**Constraints:** `0 <= key, value <= 10⁶` · at most `10⁴` calls in total

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "without any built-in hash table library" | No `dict`. Rebuild the mechanism |
| `put` inserts **or updates** | `put` must first look for the key. Found: overwrite. Not found: add |
| `get` returns `-1` if absent | Absent keys need a clean "not found" answer. `-1` is safe because values are `>= 0` |
| `remove` | Must delete the **pair**, not just the key |
| keys up to `10⁶` | A giant array indexed by key would work here, but it is the shortcut, not the design |

This is [Design HashSet](705-design-hashset.md) with one extra column. The set stored keys. The map stores **key + value**, and `put` now has to handle "already there, so update it".

🤔 **Before you open the next section:** in a chain of nodes, which two fields does each node need now? Which operation is the only one that changes an existing node instead of adding or removing one?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time per op | Space | Verdict |
|---|---|---|---|---|
| List of pairs | Scan for the key on every call | O(n) | O(n) | ❌ Brute force |
| Array of size 10⁶+1 | `arr[key] = value`, `-1` means empty | O(1) | O(10⁶) | ⚠️ Fast, but a memory hog and only valid because keys are small |
| **Buckets with chaining** | `key % B` picks a bucket; each bucket is a linked list of `(key, value)` nodes | O(n / B) average | O(n + B) | ✅ How real hash maps work |

**The decision: an array of buckets, each a [linked list](../data-structures/linked-list.md) with a dummy head**, exactly as in [Design HashSet](705-design-hashset.md). Each node now carries a `val` as well as a `key`.

The giant-array shortcut earns a mention in an interview (it's valid for these constraints), but then expect "what if keys were up to 10⁹?" Chaining answers that.

See [hashmap](../data-structures/hashmap.md) for how the real thing is built.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class ListNode:
    def __init__(self, key=-1, val=-1, next=None):
        self.key = key
        self.val = val
        self.next = next
```

A chain node now stores the key (so you can recognise it), the value (what `get` returns), and `next`.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [default-arguments](../syntax/default-arguments.md)

```python
class MyHashMap:

    def __init__(self):
        self.map = [ListNode() for _ in range(1000)]
```

1000 buckets, each starting with a **dummy head** so no operation needs a "first node" special case. A comprehension makes 1000 distinct nodes.
→ [list-comprehension](../syntax/list-comprehension.md) · [mutable-default-arg-pitfall](../syntax/mutable-default-arg-pitfall.md)

```python
    def hash(self, key: int) -> int:
        return key % len(self.map)
```

The hash function: map any key to a bucket index. Pulling it into a method keeps the other three short and gives you one place to change it.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [function-basics](../syntax/function-basics.md)

```python
    def put(self, key: int, value: int) -> None:
        cur = self.map[self.hash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next.val = value
                return
            cur = cur.next
        cur.next = ListNode(key, value)
```

Walk the chain. **If the key is found, overwrite its value** and stop (that's the "update" half of `put`). If the walk reaches the end, `cur` is the tail, so attach a new node. Each key appears at most once.
→ [while-loop](../syntax/while-loop.md) · [if-return](../syntax/if-return.md)

```python
    def get(self, key: int) -> int:
        cur = self.map[self.hash(key)].next
        while cur:
            if cur.key == key:
                return cur.val
            cur = cur.next
        return -1
```

Start past the dummy and walk. A matching key returns its value. Falling off the end means the key was never stored: `-1`.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    def remove(self, key: int) -> None:
        cur = self.map[self.hash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next = cur.next.next
                return
            cur = cur.next
```

Stand on the node **before** the target and skip it. Since the head is a dummy, the first real node is removed the same way as any other.
→ [none-type](../syntax/none-type.md)

<details>
<summary>The whole thing together</summary>

```python
class ListNode:
    def __init__(self, key=-1, val=-1, next=None):
        self.key = key
        self.val = val
        self.next = next


class MyHashMap:

    def __init__(self):
        self.map = [ListNode() for _ in range(1000)]

    def hash(self, key: int) -> int:
        return key % len(self.map)

    def put(self, key: int, value: int) -> None:
        cur = self.map[self.hash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next.val = value
                return
            cur = cur.next
        cur.next = ListNode(key, value)

    def get(self, key: int) -> int:
        cur = self.map[self.hash(key)].next
        while cur:
            if cur.key == key:
                return cur.val
            cur = cur.next
        return -1

    def remove(self, key: int) -> None:
        cur = self.map[self.hash(key)]
        while cur.next:
            if cur.next.key == key:
                cur.next = cur.next.next
                return
            cur = cur.next
```

</details>

**Trace it.** `put(1, 10)`, `put(1001, 20)`, `put(1, 30)`, `get(1)`, `remove(1)`, `get(1)`:

| Call | Bucket 1 chain after | Result |
|---|---|---|
| `put(1, 10)` | `D → (1,10)` | |
| `put(1001, 20)` | `D → (1,10) → (1001,20)` | collision, appended |
| `put(1, 30)` | `D → (1,30) → (1001,20)` | key 1 found, value overwritten |
| `get(1)` | unchanged | `30` |
| `remove(1)` | `D → (1001,20)` | |
| `get(1)` | unchanged | `-1` |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n / B) per operation</summary>

One modulo plus one chain walk. A chain holds about `n / B` nodes on average, so with 1000 buckets and at most 10⁴ calls it is around 10 nodes: effectively **O(1)**.

**Worst case O(n)** when all keys collide into one bucket. Real implementations keep chains short by resizing as the load grows.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + B)</summary>

**O(n + B):** `B` dummy heads plus one node per stored key. The giant-array version is O(10⁶) regardless of how many keys exist.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I can't use a dict, so I'll build one. Hash each key to one of 1000 buckets with `key % 1000`, and resolve collisions with separate chaining: each bucket is a linked list with a dummy head. `put` walks the chain, updates the value if the key exists and appends otherwise. `get` walks and returns the value or -1. `remove` unlinks the node. Average O(1) each, since chains are short; O(n) worst case if everything collides."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Simpler approach?" | A 10⁶+1 array initialised to `-1`. O(1) and trivial, but it costs O(10⁶) memory and only works for small integer keys |
| "What if the map grows?" | Track the count. When `n / B` exceeds about 0.75, double the buckets and re-insert every pair |
| "Non-integer keys?" | Apply `hash(key)` first, then modulo |
| "Iteration order?" | Not defined for this design. A real ordered map keeps a separate linked list or sorts |
| "Thread safety?" | Lock per bucket (striping) rather than one global lock |

**Traps:**

- **`put` that only appends.** Putting the same key twice must update, not duplicate.
- **`get` returning `None`** instead of `-1`.
- **Sharing one node across buckets** with `[ListNode()] * 1000`.
- **Unlinking from `cur` instead of `cur.next`.** You'd lose the pointer to the previous node.

**This same move shows up in:** [Design HashSet](705-design-hashset.md) (no value column) · [LRU Cache](146-lru-cache.md) (hash map plus ordering) · [Time Based Key-Value Store](981-time-based-key-value-store.md) (a map whose values are lists).

</details>

---
