# 232. Implement Queue using Stacks

**Easy** · [LeetCode](https://leetcode.com/problems/implement-queue-using-stacks/) · [Solution file (no hints)](../../problems/0001-0499/232.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Implement a FIFO queue using only **two stacks**. The queue must support `push`, `pop`, `peek`, and `empty`, and you may only use standard stack operations — push to top, pop from top, peek at top, size, and is-empty.

```
push(1); push(2)
peek()   → 1
pop()    → 1
empty()  → false
```

**Constraints:** `1 <= x <= 9` · at most `100` calls · all calls are valid

**Follow-up:** can you implement it with **amortized O(1)** per operation?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| queue from **stacks** | ⚠️ FIFO from LIFO — you must **reverse** the order somewhere |
| "only standard stack operations" | No peeking into the middle, no indexing, no `deque` |
| "**two** stacks" | The second one exists precisely to hold the reversal |
| follow-up: **amortized O(1)** | Rules out reversing on every operation; you need lazy transfer |
| all calls valid | No `pop` on an empty queue to defend against |

**The core tension:** a stack gives you the **most recent** item; a queue needs the **oldest**. Those are opposite ends.

**The insight:** pouring one stack into another reverses it.

```
stack_in (push order 1,2,3):     top → [3, 2, 1] ← bottom

pour into stack_out (pop from in, push to out):

stack_out:                        top → [1, 2, 3] ← bottom
                                         ↑
                                    oldest on top — exactly what a queue needs
```

One transfer flips the order, turning LIFO into FIFO. So keep two stacks with distinct jobs:

- **`stack_in`** — receives all new pushes
- **`stack_out`** — serves all pops and peeks, holding elements in *queue* order

**The critical refinement — when to transfer.** The naive version transfers on every operation, which is O(n) each time. The follow-up wants amortized O(1), and the rule that achieves it is:

> **Only transfer when `stack_out` is empty.**

If `stack_out` still has elements, they're already older than anything in `stack_in`, so they must be served first. Transferring early would interleave the two and break FIFO order entirely.

🤔 **Before you open the next section:** if `stack_out` already holds some elements and you pour `stack_in` on top of them, whose turn would come next — and is that right?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `push` | `pop` | Verdict |
|---|---|---|---|
| Transfer on every `push` | O(n) — pour out, push, pour back | O(1) | ⚠️ Correct; expensive pushes |
| Transfer on every `pop` | O(1) | O(n) **every time** | ⚠️ Correct; expensive pops |
| **Lazy transfer — only when `stack_out` is empty** | **O(1)** | **O(1) amortized** | ✅ |

**The decision: two stacks with a lazy, one-way transfer.**

The invariant that makes it work — state this out loud, it's the whole design:

> **`stack_out` holds the front of the queue (in correct order); `stack_in` holds the back (in reverse). Every element is in exactly one of them, and everything in `stack_out` is older than everything in `stack_in`.**

Given that:

- `push` → always onto `stack_in`. O(1), no exceptions.
- `pop` / `peek` → serve from `stack_out`. If it's empty, **first** pour all of `stack_in` into it, then serve.
- `empty` → true only when **both** are empty.

**Why "only when empty" is not just an optimization but a correctness requirement.** Suppose `stack_out = [1, 2]` (1 on top) and `stack_in` receives `3`. If you poured now, `3` would land *on top of* `1`, and the next `pop` would return `3` — wrong, since `1` arrived first. Waiting until `stack_out` drains guarantees the older batch is fully served before the newer one is reversed.

**Why it's amortized O(1).** Each element is moved exactly **twice** in its lifetime: once from `stack_in` to `stack_out`, and once when popped. A single `pop` that triggers a transfer is O(n) — but that transfer pays for the next `n` pops, which are all O(1). Total work over `n` operations is O(n).

**Why a single stack can't work.** With one stack, reversing means popping everything into… nowhere. You need a second container to hold the reversal, which is why the problem specifies two.

**The contrast with [Implement Stack using Queues](225-implement-stack-using-queues.md).** That problem is the mirror image, and it does *not* have a lazy trick available — its cost is O(n) on one operation, unavoidably. This one is genuinely amortized O(1), which is why it's the more elegant of the pair. Worth knowing which is which.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []
```

Two stacks with clearly separated roles — `stack_in` for arrivals, `stack_out` for departures. The names carry the design.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
    def push(self, x: int) -> None:
        self.stack_in.append(x)
```

**Always O(1).** New elements go to the back of the queue, which is the top of `stack_in`. No transfer, no bookkeeping.
→ [list-methods](../syntax/list-methods.md)

```python
    def transfer_if_needed(self) -> None:
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
```

**The heart of the design, factored into a helper.**

- `if not self.stack_out` — **only when empty.** This is the lazy condition, and it's what preserves FIFO order as well as the amortized bound.
- `while self.stack_in` — pour *everything* across, not just one element. A partial transfer would leave the two stacks interleaved and break the invariant.
- `append(pop())` — pop from one, push to the other. That single operation is what reverses the order.

Factoring this out means `pop` and `peek` share identical logic and can't drift apart.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    def pop(self) -> int:
        self.transfer_if_needed()
        return self.stack_out.pop()
```

Ensure `stack_out` is populated, then take from its top — which is the queue's front.

```python
    def peek(self) -> int:
        self.transfer_if_needed()
        return self.stack_out[-1]
```

Identical, but `[-1]` looks without removing.
→ [list-slicing](../syntax/list-slicing.md)

```python
    def empty(self) -> bool:
        return not self.stack_in and not self.stack_out
```

**Both** must be empty. Checking only one is a classic bug — elements sitting in `stack_in` still belong to the queue even though `stack_out` is empty.
→ [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class MyQueue:

    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x: int) -> None:
        self.stack_in.append(x)

    def pop(self) -> int:
        self.transfer_if_needed()
        return self.stack_out.pop()

    def peek(self) -> int:
        self.transfer_if_needed()
        return self.stack_out[-1]

    def empty(self) -> bool:
        return not self.stack_in and not self.stack_out

    def transfer_if_needed(self) -> None:
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

</details>

**Trace it** — showing the lazy transfer and why it must wait:

| Call | Action | `stack_in` (top→) | `stack_out` (top→) | Returns |
|---|---|---|---|---|
| `push(1)` | append to in | `[1]` | `[]` | — |
| `push(2)` | append to in | `[2, 1]`\* | `[]` | — |
| `peek()` | out empty → **transfer** | `[]` | `[1, 2]`\* | **1** ✅ |
| `pop()` | out non-empty, no transfer | `[]` | `[2]` | **1** ✅ |
| `push(3)` | append to in — **no transfer** | `[3]` | `[2]` | — |
| `pop()` | out non-empty → **no transfer** | `[3]` | `[]` | **2** ✅ |
| `pop()` | out empty → **transfer** | `[]` | `[3]` | **3** ✅ |
| `empty()` | both empty | `[]` | `[]` | **true** |

\* listed top-first: `stack_in` `[2, 1]` means 2 is on top.

**Step 5 is the one to study.** `push(3)` happens while `stack_out` still holds `2`. Because we don't transfer, the next `pop` correctly returns `2` (which arrived first), and `3` waits its turn. Had we transferred eagerly, `3` would have landed on top of `2` and been returned first — breaking FIFO.

Order out: **1, 2, 3** ✅ — exactly the push order.

</details>

<details>
<summary><b>4 · Time complexity</b> — amortized O(1)</summary>

| Operation | Worst case | Amortized |
|---|---|---|
| `push` | **O(1)** | O(1) |
| `pop` | O(n) | **O(1)** |
| `peek` | O(n) | **O(1)** |
| `empty` | **O(1)** | O(1) |

**The amortized argument** — this is what the follow-up is testing:

> Each element is moved **exactly twice** in its lifetime: once into `stack_out` during a transfer, and once when it's popped off. Over `n` operations the total work is bounded by `2n` moves, so the average cost per operation is **O(1)**.

An individual `pop` can be O(n) — the one that triggers a transfer of `n` elements. But that transfer is only possible because `n` pushes happened first, and it enables the next `n` pops to be O(1) each. **The expensive operation pays for the cheap ones that follow.**

**Say it out loud like this:** *"Worst case O(n) on a single pop, but each element transfers at most once, so it's amortized O(1) — the cost is paid once per element, not once per operation."*

**Compare to the eager alternatives:** transferring on every push or every pop makes that operation O(n) **every single time**, giving O(n²) over `n` operations. The lazy condition is the entire difference.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, where `n` is the number of elements currently in the queue.

Every element lives in **exactly one** of the two stacks — never both, never neither. So the combined size is precisely the queue's size; the second stack costs no extra asymptotic space.

That's a nice property worth noticing: two containers, but no duplication. Contrast with [Min Stack](155-min-stack.md), where an auxiliary stack genuinely does store extra copies.

| | Space |
|---|---|
| `stack_in` + `stack_out` | **O(n)** combined, no duplication |
| A native queue / `deque` | O(n) |

So this implementation is asymptotically free compared to a real queue — the only cost is the amortized transfer, and constant factors.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A stack gives me the newest element and a queue needs the oldest, so I need a reversal — and pouring one stack into another reverses it. I keep `stack_in` for pushes and `stack_out` for pops. Push is always O(1) onto `stack_in`. For pop or peek, if `stack_out` is empty I pour everything from `stack_in` into it, which flips the order so the oldest ends up on top; otherwise I serve directly. The crucial rule is transferring **only when `stack_out` is empty** — that's both a correctness requirement, since elements already in `stack_out` are older and must be served first, and what gives amortized O(1), since each element moves at most twice in its lifetime. `empty` checks both stacks."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Prove the amortized O(1)." | **The follow-up.** Each element is pushed to `in`, moved to `out` once, and popped once — ≤ 2 moves per element, so O(n) total over n operations. |
| "Why not transfer on every push?" | That's O(n) per push — O(n²) overall. Lazy transfer defers the cost and amortizes it. |
| "Why only transfer when `stack_out` is empty?" | Correctness: elements already in `stack_out` are older. Pouring on top of them would serve newer elements first. |
| "Implement a **stack using queues**." | [LeetCode 225](225-implement-stack-using-queues.md) — the mirror image, and notably it has *no* lazy trick: one operation is unavoidably O(n). |
| "Add a `size()` method." | `len(stack_in) + len(stack_out)` — O(1). |
| "Make it thread-safe." | The transfer is not atomic; a lock around pop/peek is needed, or the invariant breaks under concurrency. |
| "What if `pop` on empty were allowed?" | Guard with `if self.empty(): return None` or raise — the constraints exclude it here. |

**Traps:**

- **Transferring when `stack_out` is non-empty.** Breaks FIFO — the single most important rule. Test `push, push, pop, push, pop` to catch it.
- **Partial transfer.** Moving only one element leaves the stacks interleaved; the `while` must drain `stack_in` completely.
- **`empty()` checking only one stack.** Elements in `stack_in` still count.
- **Duplicating transfer logic in `pop` and `peek`.** They drift apart under edits — factor it into a helper.
- **`peek` using `stack_out.pop()` then re-pushing.** Works but is needlessly destructive; `[-1]` is O(1) and non-mutating.
- **Using `pop(0)` on a list to fake a queue.** O(n) per call, and it dodges the exercise entirely.

**This same move shows up in:** [Implement Stack using Queues](225-implement-stack-using-queues.md) (the mirror problem, where the cost can't be amortized away) · [Min Stack](155-min-stack.md) (another two-container design with a maintained invariant) · [Insert Delete GetRandom O(1)](380-insert-delete-getrandom-o1.md) (composing two structures and keeping them in sync) · [LRU Cache](146-lru-cache.md) (the canonical "two structures, one invariant" design).

</details>

---
