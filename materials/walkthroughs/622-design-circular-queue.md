# 622. Design Circular Queue

**Medium** · [LeetCode](https://leetcode.com/problems/design-circular-queue/) · [Solution file (no hints)](../../problems/0500-0999/622.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Design a **circular queue** of fixed capacity `k`: a FIFO structure where the last position connects back to the first, so freed space at the front is reused.

- `MyCircularQueue(k)` creates a queue of size `k`.
- `enQueue(value)` inserts at the rear. Returns `True` on success, `False` if full.
- `deQueue()` removes from the front. Returns `True` on success, `False` if empty.
- `Front()` / `Rear()` return the front or last item, or `-1` if empty.
- `isEmpty()` / `isFull()` do what they say.

```
k = 3
enQueue(1) → True    enQueue(2) → True    enQueue(3) → True
enQueue(4) → False   (full)
Rear()     → 3       isFull()   → True
deQueue()  → True    enQueue(4) → True    (reuses the freed slot)
Rear()     → 4
```

**Constraints:** `1 <= k <= 1000` · `0 <= value <= 1000` · at most `3000` calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "circular", fixed size `k` | A ring buffer. Positions wrap around with **modulo** instead of shifting elements |
| "reuse the space in front of the queue" | A plain list with `pop(0)` is the cheap way out and it's O(n) per dequeue. Wrapping avoids moving anything |
| `enQueue` / `deQueue` return a bool | Full and empty must be detected exactly |
| `Front` / `Rear` return `-1` when empty | Handle the empty case before touching the array |

The classic trap in a ring buffer: **how do you tell empty from full?** In both states the front index can equal the rear index, if you track only those two indices. There are three standard fixes: keep a **size counter**, leave one slot unused, or keep a flag. The size counter is the simplest to get right.

🤔 **Before you open the next section:** with a `head` index and a `size`, what's the array index of the rear element? And the slot where the next item goes?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Operations | Verdict |
|---|---|---|
| Python list, `append` / `pop(0)` | `pop(0)` shifts everything: O(k) | ❌ Not what "circular" means, and slow |
| Singly linked list with head and tail pointers | All O(1), O(k) memory | ✅ Valid, but more pointer code for a fixed-size queue |
| **Fixed array + `head` + `size`, wrapped with `%`** | **All O(1)** | ✅ The standard [circular buffer](../data-structures/circular-buffer.md) |
| Fixed array + `head` + `tail`, one slot wasted | All O(1) | ✅ Works, but off-by-one prone |

**The decision: an array of size `k`, a `head` index, and a `size` counter.**

- The rear element lives at `(head + size - 1) % k`.
- The next free slot is `(head + size) % k`.
- Dequeue just moves `head` forward by one (wrapping) and decrements `size`. No shifting.
- `size == 0` means empty, `size == k` means full. No ambiguity.

This is the structure behind a [queue](../data-structures/queue.md) with fixed memory, such as audio buffers and network packet rings.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self, k: int):
    self.queue = [0] * k
    self.head = 0
    self.size = 0
    self.capacity = k
```

`queue` is the ring: `k` slots, whose contents are meaningless until written. `head` is the index of the front element. `size` is how many elements are stored. `capacity` is saved so the other methods don't need `len`.
→ [init-method](../syntax/init-method.md) · [class-basics](../syntax/class-basics.md) · [list-basics](../syntax/list-basics.md)

```python
def enQueue(self, value: int) -> bool:
    if self.isFull():
        return False
    self.queue[(self.head + self.size) % self.capacity] = value
    self.size += 1
    return True
```

Refuse when full. Otherwise write at the first free slot, `(head + size) % capacity`. The `%` wraps the index back to 0 after the last slot. Then grow `size`.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [if-return](../syntax/if-return.md)

```python
def deQueue(self) -> bool:
    if self.isEmpty():
        return False
    self.head = (self.head + 1) % self.capacity
    self.size -= 1
    return True
```

Removing the front is just moving `head` one step on (wrapping). The old value stays in the array but is outside the live window, so it's invisible. This is why the structure is O(1): nothing moves.

```python
def Front(self) -> int:
    return -1 if self.isEmpty() else self.queue[self.head]

def Rear(self) -> int:
    return -1 if self.isEmpty() else self.queue[(self.head + self.size - 1) % self.capacity]
```

`Front` is at `head`. `Rear` is the last stored element, `size - 1` steps after `head`, wrapped. Guard both with the empty check, otherwise you would return stale data.
→ [ternary-expression](../syntax/ternary-expression.md)

```python
def isEmpty(self) -> bool:
    return self.size == 0

def isFull(self) -> bool:
    return self.size == self.capacity
```

The size counter makes both checks trivial and unambiguous.
→ [boolean-basics](../syntax/boolean-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class MyCircularQueue:

    def __init__(self, k: int):
        self.queue = [0] * k
        self.head = 0
        self.size = 0
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.queue[(self.head + self.size) % self.capacity] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.queue[(self.head + self.size - 1) % self.capacity]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
```

</details>

**Trace it.** `k = 3`:

| Call | `head` | `size` | Array | Result |
|---|---|---|---|---|
| `enQueue(1)` | 0 | 1 | `[1, _, _]` | True |
| `enQueue(2)` | 0 | 2 | `[1, 2, _]` | True |
| `enQueue(3)` | 0 | 3 | `[1, 2, 3]` | True |
| `enQueue(4)` | 0 | 3 | unchanged | **False**, full |
| `deQueue()` | 1 | 2 | `[1, 2, 3]`, window is `2, 3` | True |
| `enQueue(4)` | 1 | 3 | writes slot `(1+2) % 3 = 0`: `[4, 2, 3]` | True |
| `Rear()` | | | slot `(1+3-1) % 3 = 0` | **4** ✅ |

The write at slot 0 is the circular part: the freed space came back.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) per operation</summary>

Every method is a few arithmetic operations and one array access: **O(1)**. No loops, no shifting. A list-based queue using `pop(0)` would be O(k) per dequeue.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** for the fixed array, allocated once and never resized.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A circular queue is a ring buffer, so I'll use a fixed array of size k plus a head index and a size counter. The next free slot is `(head + size) % k`, the rear is `(head + size - 1) % k`, and dequeue just advances head with wrap-around. Tracking size removes the empty-versus-full ambiguity you get when you track only head and tail. Every operation is O(1) with no shifting, and the memory is O(k)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just track `head` and `tail`?" | `head == tail` happens when empty *and* when full. You'd need a wasted slot or a flag. A size counter is simpler |
| "Linked-list version?" | Keep `head` and `tail` nodes and a `size`. Enqueue appends at the tail, dequeue unlinks the head. Also O(1) |
| "Make it resizable?" | When full, allocate double, copy the elements in logical order, reset `head = 0`. Amortised O(1) |
| "Where are ring buffers used?" | I/O buffers, producer-consumer queues, logging, audio. Fixed memory, no allocation per item |
| "Circular **deque**?" | [Design Circular Deque](../data-structures/deque.md) adds insertion at the front: `head = (head - 1) % k` |
| "Thread safety?" | One producer and one consumer can use a lock-free ring with careful memory ordering. In general, lock it |

**Traps:**

- **Using `%` on a negative number.** Python handles `-1 % 3 == 2` fine, but other languages don't.
- **Computing the rear as `head + size`.** That is the *next free* slot, not the last element.
- **Returning `queue[head]` from `Front` when empty.** It is stale data. Check emptiness first.
- **Resetting `size` or the array on `deQueue`.** Just move `head`.

**This same move shows up in:** [Implement Queue using Stacks](232-implement-queue-using-stacks.md) · [Design Hit Counter](362-design-hit-counter.md) (a queue of recent events) · [LRU Cache](146-lru-cache.md) (another O(1) design problem).

</details>

---
