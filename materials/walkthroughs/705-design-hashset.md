# 705. Design HashSet

**Easy** · [LeetCode](https://leetcode.com/problems/design-hashset/) · [Solution file (no hints)](../../problems/0500-0999/705.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Design a `MyHashSet` **without using any built-in hash table library**. It supports `add(key)`, `remove(key)` and `contains(key)`.

```
MyHashSet()
add(1)        →  set is {1}
add(2)        →  set is {1, 2}
contains(1)   →  True
contains(3)   →  False
add(2)        →  set is still {1, 2}   (no duplicates)
contains(2)   →  True
remove(2)     →  set is {1}
contains(2)   →  False
```

**Constraints:** `0 <= key <= 10⁶` · at most `10⁴` calls in total

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "without any built-in hash table library" | You may not use `set` or `dict`. You must **build the idea behind them** |
| `add`, `remove`, `contains` | The three operations a set needs. Each should be fast |
| a set | `add` of a key already present must change nothing. No duplicates |
| `0 <= key <= 10⁶` | Keys are small non-negative integers. That opens a shortcut (a giant array), but it won't generalise |
| `10⁴` calls | Not many. Even a slow structure would pass, but the point is to build the fast one |

The question this problem really asks: **how does a hash set find a key in O(1) without scanning everything?**

The answer is the hash function. Turn the key into a **bucket number** (`key % number_of_buckets`). Every key has exactly one home bucket, so a lookup only ever searches that one small bucket. Two different keys can land in the same bucket (a **collision**), so each bucket needs to hold more than one key.

🤔 **Before you open the next section:** if you used a plain list as the whole set, what would `contains` cost? What does splitting the list into 1000 smaller lists buy you?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time per op | Space | Verdict |
|---|---|---|---|---|
| One list | `add` appends if absent, `contains` scans | O(n) | O(n) | ❌ This is the brute force. Every operation scans everything |
| Boolean array of size 10⁶+1 | `present[key]` is `True` or `False` | O(1) | O(10⁶) | ⚠️ Works for this key range only. It wastes memory when the set is small and breaks for large keys |
| **Buckets with chaining** | `key % B` picks a bucket, each bucket is a linked list | O(n / B) average | O(n + B) | ✅ How real hash tables work |
| Open addressing | On a collision, probe the next free slot | O(1) average | O(capacity) | ⚠️ Correct, but removals need tombstones, which is more to explain |

**The decision: an array of buckets, each bucket a [linked list](../data-structures/linked-list.md) (separate chaining).** This is the textbook design of a [hash set](../data-structures/hashset.md), and it is the answer interviewers expect when they say "implement a hash set".

The array of buckets turns one big search into one tiny search. The linked list inside a bucket handles collisions. With 1000 buckets and at most 10⁴ keys, each chain stays short.

**A dummy head node per bucket** is the detail that makes it clean. Every chain starts with a node that holds no real key, so `add` and `remove` always work on `cur.next`. Removing the first real key is then the same code as removing any other. The same trick appears in [Merge Two Sorted Lists](21-merge-two-sorted-lists.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class ListNode:
    def __init__(self, key=-1, next=None):
        self.key = key
        self.next = next
```

One link in a bucket's chain: a key and a pointer to the next node.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [default-arguments](../syntax/default-arguments.md) · [linked-list](../data-structures/linked-list.md)

```python
class MyHashSet:

    def __init__(self):
        self.buckets = [ListNode() for _ in range(1000)]
```

1000 buckets, and each starts as a lone **dummy node**. A list comprehension builds 1000 separate nodes. `[ListNode()] * 1000` would put the *same* node in every slot, which is a classic bug.
→ [list-comprehension](../syntax/list-comprehension.md) · [mutable-default-arg-pitfall](../syntax/mutable-default-arg-pitfall.md) · [hashset](../data-structures/hashset.md)

```python
    def add(self, key: int) -> None:
        cur = self.buckets[key % len(self.buckets)]
        while cur.next:
            if cur.next.key == key:
                return
            cur = cur.next
        cur.next = ListNode(key)
```

The hash function is `key % len(self.buckets)`. Start at that bucket's dummy node and walk the chain. If the key is already there, return (a set never stores duplicates). If the walk reaches the tail, `cur` is the last node, so hang the new node on `cur.next`.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [while-loop](../syntax/while-loop.md) · [if-return](../syntax/if-return.md)

```python
    def remove(self, key: int) -> None:
        cur = self.buckets[key % len(self.buckets)]
        while cur.next:
            if cur.next.key == key:
                cur.next = cur.next.next
                return
            cur = cur.next
```

Same walk, but we look at `cur.next` so that `cur` is the node **before** the one to delete. To delete, skip over the target: `cur.next = cur.next.next`. Because of the dummy head, deleting the first real node needs no special case. If the key isn't there, the loop ends and nothing happens.
→ [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md)

```python
    def contains(self, key: int) -> bool:
        cur = self.buckets[key % len(self.buckets)].next
        while cur:
            if cur.key == key:
                return True
            cur = cur.next
        return False
```

Start at the first *real* node (skip the dummy with `.next`) and walk the chain. Finding the key means `True`. Reaching `None` means `False`.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [boolean-basics](../syntax/boolean-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class ListNode:
    def __init__(self, key=-1, next=None):
        self.key = key
        self.next = next


class MyHashSet:

    def __init__(self):
        self.buckets = [ListNode() for _ in range(1000)]

    def add(self, key: int) -> None:
        cur = self.buckets[key % len(self.buckets)]
        while cur.next:
            if cur.next.key == key:
                return
            cur = cur.next
        cur.next = ListNode(key)

    def remove(self, key: int) -> None:
        cur = self.buckets[key % len(self.buckets)]
        while cur.next:
            if cur.next.key == key:
                cur.next = cur.next.next
                return
            cur = cur.next

    def contains(self, key: int) -> bool:
        cur = self.buckets[key % len(self.buckets)].next
        while cur:
            if cur.key == key:
                return True
            cur = cur.next
        return False
```

</details>

**Trace it.** 1000 buckets. `add(1)`, `add(1001)`, `contains(1001)`, `remove(1)`, `contains(1)`:

| Call | Bucket | Chain before | Result |
|---|---|---|---|
| `add(1)` | `1 % 1000 = 1` | `D` | chain `D → 1` |
| `add(1001)` | `1001 % 1000 = 1` | `D → 1` | collision, same bucket: `D → 1 → 1001` |
| `contains(1001)` | 1 | `D → 1 → 1001` | walks two nodes, `True` |
| `remove(1)` | 1 | `D → 1 → 1001` | `D.next = 1001`: `D → 1001` |
| `contains(1)` | 1 | `D → 1001` | not found, `False` |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n / B) per operation</summary>

Each operation does one modulo, one array index, then walks **one** chain.

- With `n` keys spread over `B` buckets, a chain holds about `n / B` keys on average.
- Here `B = 1000` and `n <= 10⁴`, so a chain is about 10 nodes. Effectively **O(1)**.
- **Worst case O(n)** if every key lands in the same bucket (for example, all multiples of 1000). A good hash function avoids this. Real hash tables also **resize** when chains grow, keeping the average chain length constant.

Compared with the one-list brute force, which is O(n) on every call, the bucket array cuts the work by a factor of `B`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + B)</summary>

**O(n + B).** `B` dummy nodes for the buckets, plus one node for every key currently stored. Removed keys are unlinked and become garbage.

The boolean-array alternative would be O(10⁶) no matter how few keys you store.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A single list would make every operation O(n). A real hash set avoids that by using a hash function to pick one bucket per key, so each operation only searches a short chain. I'll use an array of 1000 buckets and `key % 1000` as the hash. Collisions are handled by separate chaining: each bucket is a linked list with a dummy head, so add and remove are uniform. Add checks for the key and appends, remove unlinks, contains scans one chain. Average O(1) per operation, O(n) in the worst case if everything collides."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How would you handle a growing set?" | **Resize.** When `n / B` passes a load factor (about 0.75), double `B` and re-insert every key. Amortised cost stays O(1) |
| "Chaining vs open addressing?" | Chaining is simpler and removal is trivial. Open addressing is more cache-friendly but needs tombstones for removal and degrades fast at high load |
| "What if keys aren't integers?" | Use a real hash function (`hash(key)`) before the modulo. The rest is unchanged |
| "Why a dummy head?" | It removes the "is this the first node?" special case from `add` and `remove` |
| "Why 1000 buckets?" | Any size works. Larger means shorter chains but more memory. A **prime** size spreads keys more evenly when keys have patterns |
| "Now store values too?" | That is [Design HashMap](706-design-hashmap.md): same structure, each node also holds a value |

**Traps:**

- **`[ListNode()] * 1000`.** Every bucket is then the same object, so one `add` appears in all of them.
- **Forgetting the duplicate check in `add`.** A set must ignore a key that is already present.
- **Walking with `cur` instead of `cur.next` in `remove`.** You need the node *before* the target in order to unlink it.
- **Using the key itself as the index** (`buckets[key]`). It works for `10⁶` but misses the point of hashing.

**This same move shows up in:** [Design HashMap](706-design-hashmap.md) (add a value to each node) · [LRU Cache](146-lru-cache.md) (a hash map paired with a list) · [Contains Duplicate](217-contains-duplicate.md) (the built-in set you're now replacing).

</details>

---
