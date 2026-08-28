# 225. Implement Stack using Queues

**Easy** · [LeetCode](https://leetcode.com/problems/implement-stack-using-queues/) · [Solution file (no hints)](../../problems/0001-0499/225.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Implement a LIFO stack using only **queue** operations. Support `push`, `pop`, `top`, and `empty`, using only push-to-back, peek/pop-from-front, size, and is-empty.

```
push(1); push(2)
top()    → 2
pop()    → 2
empty()  → false
```

**Constraints:** `1 <= x <= 9` · at most `100` calls · all calls are valid

**Follow-up:** can you implement it using **one** queue?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| stack from **queues** | ⚠️ LIFO from FIFO — the reverse of [Implement Queue using Stacks](232-implement-queue-using-stacks.md) |
| only queue operations | Add at the back, remove from the front. No indexing, no reaching into the middle |
| follow-up: **one** queue | Achievable — and the one-queue version is arguably *simpler* than two |
| all calls valid | No empty-stack defence needed |
| ≤ 100 calls | Tiny, so an O(n) operation is perfectly acceptable |

**The tension:** a queue serves the **oldest** element; a stack needs the **newest**. Opposite ends again.

**The key asymmetry with problem 232.** There, two stacks let you pour one into the other and *reverse* the order lazily, achieving amortized O(1). Here that trick isn't available: pouring a queue into another queue **preserves** order rather than reversing it, because both remove from the front and add to the back. FIFO into FIFO is still FIFO.

So you can't get an amortized win. **One operation must be O(n)**, and the design choice is *which one*.

**The rotation trick** — the neat solution, and the one that makes the follow-up work:

After adding a new element to the back, **rotate the queue** so that new element sits at the front. Move every *other* element from front to back, one at a time:

```
queue [1, 2]   (1 at front)
push(3) → append:      [1, 2, 3]
rotate 2 times:        [2, 3, 1] → [3, 1, 2]
                        ↑
                    3 is now at the front — pop() returns it. LIFO ✅
```

Now the queue's front always holds the most recently pushed element, so `pop` and `top` are trivially O(1). All the cost is concentrated in `push`.

🤔 **Before you open the next section:** if you just appended an element to the back of a queue of size `k`, how many front-to-back rotations bring it to the front?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `push` | `pop` | Queues | Verdict |
|---|---|---|---|---|
| Two queues, shuffle on pop | O(1) | O(n) | 2 | ✅ Correct; costly pops |
| Two queues, shuffle on push | O(n) | O(1) | 2 | ✅ Correct; needs a swap step |
| **One queue, rotate on push** | **O(n)** | **O(1)** | **1** | ✅✅ Answers the follow-up, simplest code |

**The decision: a single queue, rotated on every push.**

The invariant — say this out loud, it's the whole design:

> **The queue is always stored in reverse push order: the most recently pushed element is at the front.**

Maintaining it is one step in `push`:

1. `append(x)` — x is now at the back
2. Rotate `len(queue) - 1` times — move each older element from front to back

After the rotation, `x` has bubbled to the front and every other element trails behind in the correct (reversed) order.

**Why `len(queue) - 1` rotations exactly.** After appending, the queue holds `k` elements with `x` last. Moving the `k - 1` elements ahead of it to the back brings `x` to the front, and — crucially — leaves those `k - 1` in their original relative order behind it. Rotating `k` times would return to the starting arrangement; rotating fewer would leave `x` buried.

**Why this beats the two-queue versions.** Both two-queue designs work, but they need a second container and a swap or a careful "leave one behind" loop. The one-queue rotation is fewer moving parts, uses less memory, and answers the follow-up directly. **Fewer things to get wrong is a real advantage** in an interview.

**Why there's no amortized trick here.** Worth being explicit, because interviewers ask: in problem 232, transferring between two *stacks* reverses order, so you can defer the work and each element moves at most twice. Here, moving between queues preserves order — there's no reversal to bank. Every push must do its own O(n) rotation, and no lazy scheme avoids it. The two problems look symmetric but are genuinely different in this respect.

**Why `deque`?** `collections.deque` gives O(1) `append` and `popleft`, which is exactly the queue interface. A plain list's `pop(0)` is O(n) because everything shifts, which would make the rotation O(n²).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class MyStack:
    def __init__(self):
        self.queue = deque()
```

A single [`deque`](../data-structures/deque.md), used strictly as a queue: `append` to the back, `popleft` from the front.
→ [deque-basics](../syntax/deque-basics.md) · [class-basics](../syntax/class-basics.md)

```python
    def push(self, x: int) -> None:
        self.queue.append(x)
```

Add to the back — the only place a queue lets you insert.

```python
        rotations_needed = len(self.queue) - 1
        for _ in range(rotations_needed):
            front_element = self.queue.popleft()
            self.queue.append(front_element)
```

**The rotation — where all the work happens.**

`len(self.queue) - 1` is computed **after** the append, so it counts the elements sitting ahead of `x`. Moving each of them from front to back lifts `x` to the front while preserving the relative order of the rest.

The `_` name signals the loop variable is unused — it's a pure repetition count.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    def pop(self) -> int:
        return self.queue.popleft()
```

**O(1).** The invariant guarantees the front is the most recently pushed element — exactly what a stack's `pop` must return.

```python
    def top(self) -> int:
        return self.queue[0]
```

Same element, without removing it. Indexing a `deque` at position 0 is O(1) (arbitrary middle indexing is not, but the ends are).

```python
    def empty(self) -> bool:
        return len(self.queue) == 0
```

One container, so one check. (`return not self.queue` is the more idiomatic form.)
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

<details>
<summary>The whole thing together</summary>

```python
class MyStack:

    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)

        rotations_needed = len(self.queue) - 1
        for _ in range(rotations_needed):
            front_element = self.queue.popleft()
            self.queue.append(front_element)

    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return len(self.queue) == 0


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
```

</details>

**Trace it** — `push(1)`, `push(2)`, `push(3)`, then pops. Queue shown **front → back**:

| Call | After append | Rotations | Queue after | Front |
|---|---|---|---|---|
| `push(1)` | `[1]` | `1-1 = 0` | `[1]` | 1 |
| `push(2)` | `[1, 2]` | `2-1 = 1`: move 1 → `[2, 1]` | `[2, 1]` | **2** |
| `push(3)` | `[2, 1, 3]` | `3-1 = 2`: move 2 → `[1, 3, 2]`; move 1 → `[3, 2, 1]` | `[3, 2, 1]` | **3** |

The queue now reads `[3, 2, 1]` — exactly **reverse push order**, which is the invariant.

| Call | Returns | Queue after |
|---|---|---|
| `top()` | **3** | `[3, 2, 1]` |
| `pop()` | **3** | `[2, 1]` |
| `pop()` | **2** | `[1]` |
| `pop()` | **1** | `[]` |
| `empty()` | **true** | `[]` |

Pop order **3, 2, 1** — LIFO ✅, the reverse of the push order.

Note `push(3)` performed 2 rotations, and after them the older elements `2, 1` kept their relative order behind the new front. That preservation is what makes a single rotation pass sufficient.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n) push, O(1) everything else</summary>

| Operation | Complexity |
|---|---|
| `push` | **O(n)** — one append plus `n-1` rotations |
| `pop` | **O(1)** — one `popleft` |
| `top` | **O(1)** — one index read |
| `empty` | **O(1)** |

**This is genuinely O(n) per push, not amortized O(1)** — and being clear about that distinction matters:

> In [Implement Queue using Stacks](232-implement-queue-using-stacks.md), pouring stack→stack **reverses** order, so work can be deferred and each element moves at most twice — amortized O(1). Here, moving queue→queue **preserves** order, so there's no reversal to bank. Every push must rotate, and no lazy scheme avoids it.

Someone who says "it's amortized O(1) like the other one" has pattern-matched rather than reasoned. Say the opposite, and say why.

**The design trade-off:** you *choose* which operation absorbs the O(n). Rotating on push makes pops cheap; the alternative (two queues, shuffle on pop) makes pushes cheap. Pick based on the expected workload — if pushes vastly outnumber pops, the other design is better.

At `n ≤ 100` calls, total work is at most ~10⁴ operations either way.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — a single queue holding all `n` elements.

The one-queue solution is strictly better on space than the two-queue variants, which allocate a second container even though the combined element count is the same. Fewer objects, less overhead, one thing to keep consistent.

`deque` is implemented as a doubly-linked list of fixed-size blocks, giving O(1) at both ends with modest per-element overhead — the right structure here. A plain list would make `pop(0)` O(n), turning each rotation into O(n²).

**The general lesson from this pair of problems:**

> **Reversal is cheap between stacks and impossible between queues.** Which structure you're building *from* determines whether laziness can buy you an amortized bound.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A queue serves the oldest element and a stack needs the newest, so I keep the queue in reverse push order — newest at the front. On every push I append the element to the back, then rotate the `n-1` older elements from front to back, which lifts the new one to the front while preserving the others' relative order. Then `pop` and `top` are just `popleft` and index 0, both O(1). This works with a **single** queue, which answers the follow-up. Push is O(n), and unlike Implement Queue using Stacks there's no amortized trick available — pouring a queue into a queue preserves order rather than reversing it, so there's no deferred work to bank."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you use **one** queue?" | **The stated follow-up** — that's this solution. Rotate on push. |
| "Why isn't this amortized O(1) like problem 232?" | **The best question here.** Stack→stack transfer reverses order, enabling lazy deferral. Queue→queue preserves order, so every push must rotate. |
| "Make `push` O(1) instead." | Two queues, shuffle on `pop`: move all but the last element to the other queue, pop the straggler, swap the queues. O(1) push, O(n) pop. |
| "Which design is better?" | Depends on the workload. Push-heavy → shuffle on pop. Pop-heavy → rotate on push. |
| "Add `size()`." | `len(self.queue)` — O(1). |
| "Why `deque` over `list`?" | `list.pop(0)` is O(n) from shifting; `deque.popleft()` is O(1). Using a list would make each rotation O(n²). |
| "Is it thread-safe?" | No — the rotation isn't atomic, so a concurrent `pop` mid-rotation would see a broken invariant. |

**Traps:**

- **Rotating `len(queue)` times instead of `len(queue) - 1`.** A full cycle returns to the starting order, leaving the new element at the back — pops then return the *oldest* element, i.e. a queue, not a stack.
- **Computing the rotation count before the append.** Off by one; the new element stays buried.
- **Using a list with `pop(0)`.** Correct but O(n) per removal, making rotation quadratic.
- **Claiming amortized O(1).** It isn't, and the reason why is the most interesting part of the problem.
- **`top()` implemented as `pop()` then `push()`.** The re-push triggers another full rotation — O(n) for a read that should be O(1).
- **Forgetting `deque` needs importing.** `from collections import deque`.

**This same move shows up in:** [Implement Queue using Stacks](232-implement-queue-using-stacks.md) (the mirror problem, where reversal *is* possible and buys amortized O(1)) · [Rotting Oranges](994-rotting-oranges.md) (a `deque` used as a genuine BFS queue) · [Sliding Window Maximum](239-sliding-window-maximum.md) (a `deque` exploited at both ends) · [Min Stack](155-min-stack.md) (another container-design problem with a maintained invariant).

</details>

---
