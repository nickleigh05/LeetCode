# 146. LRU Cache

**Medium** · [LeetCode](https://leetcode.com/problems/lru-cache/) · [Solution file (no hints)](../../problems/0001-0499/146.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Design a data structure that follows the **Least Recently Used (LRU)** cache eviction policy.

- **`LRUCache(capacity)`** — initialize with a positive capacity.
- **`get(key)`** — return the value if the key exists, otherwise `-1`.
- **`put(key, value)`** — insert or update. If this exceeds capacity, **evict the least recently used key**.

Both `get` and `put` must run in **O(1) average time complexity**.

```
LRUCache(2)
put(1,1); put(2,2)
get(1)      →  1        (1 is now most recent)
put(3,3)                 evicts key 2 (least recently used)
get(2)      →  -1
```

**Constraints:** `1 <= capacity <= 3000` · up to 2·10⁵ calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Design**" | A class with persistent state — like [Min Stack](155-min-stack.md) |
| "**O(1)** for both operations" | ⚠️ The entire challenge. Any scan to find the least-recently-used item is O(n) |
| "least **recently used**" | You must track an **ordering by access time**, and that ordering changes on every operation |
| `get` counts as a use | Reading an item makes it most-recent — so `get` mutates the ordering too |
| `put` on an existing key | Updates the value **and** refreshes recency |
| capacity ≤ 3000, 2·10⁵ calls | O(n) per call would be 6·10⁸ — too slow. O(1) is genuinely required |

Two requirements pull in opposite directions:

1. **Find a key instantly** → a [hash map](../data-structures/hashmap.md). But hash maps have no order.
2. **Know which item is least recently used, and reorder on every touch** → an ordered structure. But ordered structures don't have O(1) lookup by key.

**Neither one alone can do it.** A hash map can't tell you what's oldest; a list can't find a key without scanning.

So: **use both, and make them point at each other.**

What ordered structure supports O(1) *removal from the middle*? Not an array — deleting from the middle shifts everything, O(n). But a **doubly linked list** can splice a node out in O(1) — *provided you already have a reference to that node.*

And that's exactly what the hash map can store: not the value, but **the node itself**.

```
hash map:  key → node
list:      MRU ←→ … ←→ LRU     (order = recency)
```

🤔 **Before you open the next section:** why does the linked list need to be **doubly** linked? What breaks if each node only knows its `next`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `get` | `put` | Verdict |
|---|---|---|---|
| Hash map + timestamps | O(1) | **O(n)** to find the minimum timestamp | ❌ |
| Array ordered by recency | O(n) search | O(n) shifting | ❌ |
| Hash map + **singly** linked list | O(1) find | **O(n)** — no way to reach a node's predecessor | ❌ |
| **Hash map + doubly linked list** | **O(1)** | **O(1)** | ✅ |

**The decision: a [hash map](../data-structures/hashmap.md) from key → node, plus a [doubly linked list](../data-structures/doubly-linked-list.md) ordered by recency.**

The division of labour:

- **Hash map:** *"where is key k?"* → O(1), returning the node object.
- **Doubly linked list:** *"move this node to the front"* / *"what's at the back?"* → O(1), given the node.

**Why doubly linked is non-negotiable.** To unlink a node you must fix the pointer *aimed at it*, which means reaching its predecessor. In a singly linked list that's an O(n) walk from the head — destroying the whole point. A `prev` pointer makes it O(1):

```python
node.prev.next = node.next
node.next.prev = node.prev
```

**The two sentinel nodes.** `head` and `tail` are permanent dummies that never hold data:

```
head ←→ [MRU] ←→ … ←→ [LRU] ←→ tail
 ↑                                ↑
 sentinels — never removed, never read
```

They're the [dummy-head idiom](21-merge-two-sorted-lists.md) taken to both ends, and they eliminate **every** null check: inserting at the front, removing from the back, and handling an empty cache all become the same uniform pointer surgery. Without them, `remove` and `add_to_front` would each need branches for "is this the first/last node?"

**The convention:** front (just after `head`) = most recently used; back (just before `tail`) = least recently used, i.e. the eviction target.

**Why not `OrderedDict`?** Python's [`OrderedDict`](../syntax/ordered-dict-notes.md) has `move_to_end` and `popitem(last=False)`, giving a ~10-line solution. It's the right production answer and worth mentioning — but it *is* a hash map plus a doubly linked list internally, so writing it out is the actual exercise.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
```

A doubly linked node. **Storing the `key` as well as the value is essential** — on eviction you have the node but need its key to delete the map entry. Without it you'd have no way to clean up the map.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [doubly-linked-list](../data-structures/doubly-linked-list.md)

```python
def __init__(self, capacity: int):
    self.capacity = capacity
    self.cache = {}
    self.head = Node(0, 0)
    self.tail = Node(0, 0)
    self.head.next = self.tail
    self.tail.prev = self.head
```

The map (`key → node`) and the two sentinels, wired to each other to represent an empty list.

Those last two lines matter: with `head ←→ tail` already linked, the first real insertion needs no special case.
→ [dict-basics](../syntax/dict-basics.md)

```python
def remove(self, node):
    prev_node = node.prev
    next_node = node.next
    prev_node.next = next_node
    next_node.prev = prev_node
```

**Unlink a node in O(1).** Route its neighbours around it — both directions, since the list is doubly linked.

Thanks to the sentinels, `node.prev` and `node.next` are **never `None`** for a real node, so no guards are needed.
→ [linked-list](../data-structures/linked-list.md)

```python
def add_to_front(self, node):
    node.prev = self.head
    node.next = self.head.next
    self.head.next.prev = node
    self.head.next = node
```

**Insert just after `head`** — the most-recently-used position. Four assignments, in a safe order: set the new node's two pointers *first*, then redirect the old neighbours.

⚠️ Order matters. Doing `self.head.next = node` before reading `self.head.next` would lose the reference to the old first node.

```python
def get(self, key: int) -> int:
    if key not in self.cache:
        return -1

    node = self.cache[key]
    self.remove(node)
    self.add_to_front(node)
    return node.value
```

Miss → `-1`. Hit → **remove and re-add at the front**, which is how a read refreshes recency. That remove-then-add pair is the "move to front" operation, and it's O(1) because the map handed us the node directly.
→ [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
def put(self, key: int, value: int) -> None:
    if key in self.cache:
        node = self.cache[key]
        node.value = value
        self.remove(node)
        self.add_to_front(node)
        return
```

**Existing key:** update the value in place and refresh recency. Return early — no insertion, no eviction, since the size didn't change.

```python
    if len(self.cache) >= self.capacity:
        lru_node = self.tail.prev
        self.remove(lru_node)
        del self.cache[lru_node.key]
```

**Evict before inserting.** `self.tail.prev` is the least recently used node — O(1), no search.

Unlink it **and** delete its map entry. `lru_node.key` is why nodes store their key: the node alone can't tell you which map entry to remove.

Forgetting the `del` is the classic leak — the map grows unboundedly while the list stays capped.
→ [dict-basics](../syntax/dict-basics.md)

```python
    new_node = Node(key, value)
    self.cache[key] = new_node
    self.add_to_front(new_node)
```

Create, register in the map, and place at the front as most-recently-used. **Both structures must be updated together** — that mutual consistency is the invariant the whole design rests on.

<details>
<summary>The whole thing together</summary>

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.remove(node)
        self.add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.remove(node)
            self.add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            self.remove(lru_node)
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self.cache[key] = new_node
        self.add_to_front(new_node)
```

</details>

**Trace it** — `LRUCache(2)`:

| Operation | List (front → back) | Map keys | Returns |
|---|---|---|---|
| `put(1,1)` | `head ←→ 1 ←→ tail` | {1} | |
| `put(2,2)` | `head ←→ 2 ←→ 1 ←→ tail` | {1,2} | |
| `get(1)` | `head ←→ **1** ←→ 2 ←→ tail` | {1,2} | **1** |
| `put(3,3)` | evict `tail.prev` = **2**; then insert 3 | {1,3} | |
| | `head ←→ 3 ←→ 1 ←→ tail` | | |
| `get(2)` | unchanged | {1,3} | **-1** |
| `get(3)` | `head ←→ **3** ←→ 1 ←→ tail` | {1,3} | **3** |

Watch `get(1)`: it *moved* key 1 to the front, which is why the later `put(3,3)` evicted key 2 rather than key 1. **Reading changes the eviction order** — the detail people miss.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) for both</summary>

**O(1) average for `get` and `put`.**

| Step | Cost |
|---|---|
| Map lookup / insert / delete | O(1) average |
| `remove(node)` | O(1) — four pointer writes, no traversal |
| `add_to_front(node)` | O(1) — four pointer writes |
| Find the LRU node (`tail.prev`) | **O(1)** — no search |

Every operation is a fixed number of pointer assignments and dict operations.

**The two O(1)s that make it work:**
1. *"Where is key k?"* — the hash map, without scanning the list.
2. *"Splice this node out."* — the `prev` pointer, without scanning to find a predecessor.

Remove either and the whole thing collapses to O(n). **Each structure covers precisely the other's weakness** — the same pairing idea as [Time Based Key-Value Store](981-time-based-key-value-store.md) (hash map + sorted list), just with a different ordered structure because the required operation differs.

"Average" because hash operations degrade to O(n) under adversarial collisions — the standard asterisk.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(capacity)</summary>

**O(capacity).**

- The map: at most `capacity` entries.
- The list: at most `capacity` real nodes, plus 2 sentinels.

Both are capped by the eviction policy, so memory is **bounded regardless of how many operations run**. That's the entire point of a cache — 2·10⁵ calls against a capacity of 3000 still uses only 3000 entries' worth of memory.

**Each key is stored twice** — once as a map key, once inside its node. That redundancy is deliberate: the node needs its key so eviction can clean up the map. A ~2× constant factor buys O(1) eviction, which is a good trade.

**The two sentinels are O(1)** — two nodes total, regardless of capacity. Cheap price for removing every null check from `remove` and `add_to_front`.

**Real-world note:** this is genuinely how LRU caches are built — CPU caches, database buffer pools, and Python's own `functools.lru_cache` all use this structure or a close variant.
→ [lru-cache](../data-structures/lru-cache.md) · [functools-cache](../syntax/functools-cache.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two requirements conflict: O(1) lookup by key, and O(1) access to the least-recently-used item with reordering on every touch. A hash map gives the first but has no order; an ordered structure gives the second but no fast lookup. So I use both — a hash map from key to *node*, and a doubly linked list ordered by recency. The list must be doubly linked because unlinking a node requires its predecessor, which a singly linked list can't give you in O(1). I use head and tail sentinel nodes so insertion at the front, eviction from the back, and the empty case all need no null checks. `get` moves the node to the front; `put` either refreshes an existing node or, when full, evicts `tail.prev` — and the node stores its key so I can delete the corresponding map entry. O(1) both operations, O(capacity) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why **doubly** linked?" | **The question.** Unlinking needs the predecessor. Singly linked means an O(n) walk to find it, destroying the O(1) guarantee. |
| "Why do nodes store the key?" | On eviction you have the node but must delete its map entry — the node alone can't tell you which key that is. |
| "Why sentinel nodes?" | They eliminate every null check: first insertion, last removal, and empty cache all become uniform pointer surgery. |
| "Use the standard library." | `OrderedDict` with `move_to_end` and `popitem(last=False)`, or `functools.lru_cache` for function memoization. Both are this structure internally. |
| "Implement **LFU** instead." | Least *Frequently* Used — much harder: a map of frequency → list of nodes, plus a running minimum frequency. LeetCode 460, Hard. |
| "Make it thread-safe." | A lock around both structures, since they must stay consistent. Or a sharded cache with per-shard locks for concurrency. |
| "What if capacity were 0?" | Every `put` would immediately evict. The constraints say ≥ 1, but worth *asking*. |

**Traps:**

- **Forgetting `del self.cache[lru_node.key]`** on eviction. The list stays capped but the map grows forever — a memory leak that passes small tests.
- **A singly linked list.** Looks fine until you realize removal is O(n).
- **Not moving the node on `get`.** Reading counts as a use; skip it and evictions are wrong in exactly the way the example demonstrates.
- **Forgetting to update recency** when `put` overwrites an existing key.
- **Wrong pointer order in `add_to_front`** — set the new node's pointers before overwriting `head.next`, or you lose the old first node.
- **Evicting from the front** instead of the back. Front is most-recent; back is the victim.
- **Checking `len(self.cache) > self.capacity`** after inserting rather than `>=` before. Both can work, but mixing them off-by-ones the capacity.

**This same move shows up in:** [Time Based Key-Value Store](981-time-based-key-value-store.md) (hash map + ordered structure, each covering the other's weakness) · [Min Stack](155-min-stack.md) (auxiliary structure making every operation O(1)) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the dummy/sentinel idiom) · [lru-cache](../data-structures/lru-cache.md) (the reference page).

</details>

---
