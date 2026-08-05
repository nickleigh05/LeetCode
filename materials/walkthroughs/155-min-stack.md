# 155. Min Stack

**Medium** · [LeetCode](https://leetcode.com/problems/min-stack/) · [Solution file (no hints)](../../problems/0001-0499/155.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Design a stack that supports `push`, `pop`, `top`, and retrieving the **minimum element** — each in **constant time**.

- `push(val)` — push `val` onto the stack
- `pop()` — remove the element on top
- `top()` — get the top element
- `getMin()` — retrieve the minimum element in the stack

```
push(-2), push(0), push(-3)
getMin()  →  -3
pop()
top()     →  0
getMin()  →  -2
```

**Constraints:** `-2³¹ <= val <= 2³¹ - 1` · `pop`, `top` and `getMin` are always called on a **non-empty** stack · up to 3·10⁴ calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Design** a stack" | A **class**, not a function. You're building an API with state that persists across calls |
| "each in **constant time**" | ⚠️ `getMin()` in O(1). Scanning the stack would be O(n) — that's the entire challenge |
| `push`, `pop`, `top`, `getMin` | Four methods; the first three are trivial on a list |
| "always called on a non-empty stack" | No empty-stack edge cases to guard. A small mercy |
| values are arbitrary ints | Negative values allowed — don't initialize a minimum to 0 |

The trap is thinking a single variable suffices. Try it: keep `self.min` and update it on push.

```
push(5)  → min = 5
push(3)  → min = 3
push(7)  → min = 3
pop()    → removed 7, min still 3 ✅
pop()    → removed 3 … and now min should be 5. But we overwrote it. ✗
```

**Popping the minimum destroys the information needed to recover the previous one.** A single variable can't survive that, because it kept only the current answer, not the history.

So the question becomes: *what was the minimum when the stack looked like this?* And notice — that question has a different answer at every **depth** of the stack, and those answers behave in a perfectly LIFO way. The minimum at depth 3 is restored exactly when you pop back to depth 3.

🤔 **Before you open the next section:** the answer to "what's the minimum?" changes as the stack grows and shrinks, and it always reverts to a previous value when you pop. What structure has exactly that behaviour?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `getMin()` | `push`/`pop` | Verdict |
|---|---|---|---|
| Scan on demand | O(n) | O(1) | ❌ Violates the constant-time requirement |
| One `min` variable | O(1) | O(1) | ❌ **Wrong** — popping the min loses the previous one |
| Sorted structure alongside | O(1) | O(log n) | ⚠️ Correct but slower, and more machinery |
| **Parallel min-stack** | **O(1)** | **O(1)** | ✅ |

**The decision: a second stack that records the running minimum at every depth.**

`min_stack[i]` holds *the minimum of all elements from the bottom up to depth `i`*. The two stacks always have the same height, so they move in lockstep:

- **push(val)** → push `val` to the main stack, and push `min(val, current min)` to the min-stack.
- **pop()** → pop **both**.
- **getMin()** → read the top of the min-stack. O(1).

**Why this works where the single variable failed.** The min-stack *keeps the history*. Popping doesn't recompute the previous minimum — it simply reveals the entry that was already sitting underneath, recorded when the stack was last at that depth. The information was never thrown away.

**The key idea, stated generally:** the answer to `getMin()` depends only on the stack's current *depth*, and depths are restored in LIFO order. So the answers themselves can live on a stack, perfectly parallel to the data. **Whenever a derived value has a well-defined answer at each stack depth, you can store those answers on a parallel stack.**

**Why not one stack of `(value, min)` pairs?** Genuinely equivalent, and arguably cleaner — `self.stack.append((val, min(val, self.getMin())))`. Same complexity, one structure. Mention it as an alternative; both are correct.

**The space optimization worth knowing:** you only need to push to the min-stack when `val <= current min`, and pop from it only when the popped value equals its top. That saves memory on inputs with few new minima. Use `<=`, not `<` — with strict `<`, duplicate minima would be popped off too early. Mention it; implement the simple version unless asked.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.stack = []
    self.min_stack = []
```

The constructor, run once per instance. Two parallel lists: the actual data, and the running minimum at each depth. `self.` makes them instance attributes that persist across method calls.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md)

```python
def push(self, val: int) -> None:
    self.stack.append(val)
```

The ordinary stack push — O(1) at the end of a list.
→ [list-methods](../syntax/list-methods.md) · [function-basics](../syntax/function-basics.md)

```python
    if self.min_stack:
        self.min_stack.append(min(val, self.min_stack[-1]))
    else:
        self.min_stack.append(val)
```

**The heart of it.** The new minimum is the smaller of the incoming value and the minimum *before* this push — and `self.min_stack[-1]` is exactly that previous minimum.

The `if` handles the first push, when there's no previous minimum to compare against; then the value is trivially the minimum. (You could avoid the branch by seeding with `float("inf")`, but the explicit check reads more clearly.)

Crucially, **the previous minimum is not overwritten** — it stays one level down, ready to be revealed on pop.
→ [min-max-key](../syntax/min-max-key.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [elif-else](../syntax/elif-else.md)

```python
def pop(self) -> None:
    self.stack.pop()
    self.min_stack.pop()
```

**Pop both, always.** This lockstep is the invariant the whole design rests on: the two stacks must stay the same height, or `min_stack[-1]` would describe the wrong depth.

Popping the min-stack doesn't *compute* anything — it just exposes the minimum that applied at the previous depth, recorded back when we were last there.

```python
def top(self) -> int:
    return self.stack[-1]
```

`[-1]` is the last element, i.e. the top. O(1).
→ [list-basics](../syntax/list-basics.md)

```python
def getMin(self) -> int:
    return self.min_stack[-1]
```

The payoff. No scan, no computation — the answer was precomputed on the way in, so reading it is O(1).

<details>
<summary>The whole thing together</summary>

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

</details>

**Trace it** — `push(5), push(3), push(7), push(2)`, then pops:

| Operation | `stack` | `min_stack` | `getMin()` |
|---|---|---|---|
| push(5) | `[5]` | `[5]` | 5 |
| push(3) | `[5,3]` | `[5,3]` | 3 |
| push(7) | `[5,3,7]` | `[5,3,**3**]` | 3 |
| push(2) | `[5,3,7,2]` | `[5,3,3,2]` | **2** |
| pop() | `[5,3,7]` | `[5,3,3]` | 3 ← *restored* |
| pop() | `[5,3]` | `[5,3]` | 3 |
| pop() | `[5]` | `[5]` | **5** ← *restored* |

Look at row 3: pushing `7` still records `3` in the min-stack, because 7 didn't change the minimum. The min-stack tracks *the minimum at each depth*, not the values themselves — that redundancy is exactly what makes the restoration on pop free.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) per operation</summary>

**O(1) for all four operations.**

| Operation | Work | Cost |
|---|---|---|
| `push` | two list appends, one `min` of two values | O(1) amortized |
| `pop` | two list pops from the end | O(1) |
| `top` | one index lookup | O(1) |
| `getMin` | one index lookup | **O(1)** |

`.append()` is *amortized* O(1) — Python lists occasionally reallocate to grow, but the cost is spread across many appends. Worth naming if pressed on strict worst-case bounds.

**Where the O(1) came from.** The naive `getMin()` scans the stack: O(n) per call, but O(1) memory. The min-stack **precomputes the answer on the way in**, so the query is a lookup. That's the classic trade — do the work at write time so reads are cheap — and it's the same reasoning behind caching, database indexes, and [prefix sums](../learning/01b-prefix-sums.md).

Since `push` was already O(1) and gains only a `min` and an append, the cost of that precomputation is **free asymptotically**. You pay in memory, not time.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

Two stacks of equal height, each up to n entries → 2n, which is **O(n)**.

Compared to a plain stack you're paying **2× the memory** to make `getMin()` constant instead of linear. That's the deal, and it's usually a good one.

**The optimization that reduces the constant:** only push to the min-stack when `val <= self.min_stack[-1]`, and only pop it when the popped value equals `min_stack[-1]`.

```python
if not self.min_stack or val <= self.min_stack[-1]:
    self.min_stack.append(val)
```

On `[5,3,7,9,8]` the min-stack holds just `[5,3]` instead of five entries. Worst case is still O(n) — a strictly decreasing sequence like `[5,4,3,2,1]` records every element — but typical inputs use far less.

⚠️ **`<=` not `<`.** With strict `<`, pushing `3` twice records it once, and the first pop would remove it while a `3` is still in the main stack — `getMin()` would then report a value that's too large. Duplicate minima must each be recorded.

**Can you get O(1) extra space?** There's a known trick storing encoded differences from the minimum, but it risks overflow and is unreadable. Not worth it — mention it exists if asked, don't write it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The hard part is `getMin()` in O(1). A single `min` variable doesn't work, because popping the minimum destroys the information about what the previous minimum was. But notice the minimum is well-defined *at each depth* of the stack, and depths come back in LIFO order — so the minima can live on a parallel stack. On push I record `min(val, current min)`; on pop I pop both stacks in lockstep; `getMin()` just reads the top of the min-stack. Every operation is O(1), at 2× the memory. I could also store `(value, min)` pairs in a single stack, or only record new minima to save space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why doesn't one variable work?" | **The question.** Push 5, 3, then pop — the minimum must revert to 5, but a single variable overwrote it. Walk through the sequence. |
| "Reduce the memory." | Only push when `val <= current min`, pop when the popped value equals the min-stack top. `<=` is essential for duplicate minima. |
| "Use one stack instead of two." | Store `(value, running_min)` tuples. Equivalent complexity, arguably cleaner. |
| "Add `getMax()` too." | A third parallel stack with `max` instead of `min`. The pattern generalizes to any associative running aggregate. |
| "What about a queue with `getMin()`?" | Much harder — a queue removes from the *front*, so the parallel-stack trick fails. You'd use two stacks to simulate the queue, or a monotonic deque like [Sliding Window Maximum](239-sliding-window-maximum.md). |
| "What if `pop()` could be called on an empty stack?" | The constraints exclude it, but you'd guard both pops and decide whether to raise or return `None`. Worth *asking* rather than assuming. |
| "Get the **median** in O(1)?" | Not with this trick — the median isn't a running aggregate. You'd need two heaps: [Find Median from Data Stream](295-find-median-from-data-stream.md). |

**Traps:**

- **A single `min` variable.** The defining mistake here.
- **Only pushing to the min-stack when the minimum changes, but still popping it unconditionally.** The two stacks desynchronize and everything after is wrong. If you optimize the push, you *must* make the pop conditional too.
- **Using `<` instead of `<=`** in the optimized version — duplicate minima get under-recorded and `getMin()` returns too large a value.
- **Recomputing `min(self.stack)` in `getMin()`.** O(n), which is precisely what the problem forbids.
- **Forgetting the first-push case** — `min_stack[-1]` on an empty list raises `IndexError`.
- **Initializing the minimum to 0** instead of the first value or `float("inf")`. Values can be negative.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the plain stack this augments) · [Daily Temperatures](739-daily-temperatures.md) (a stack carrying extra per-element state) · [Sliding Window Maximum](239-sliding-window-maximum.md) (a running extreme maintained without rescanning) · [LRU Cache](146-lru-cache.md) (another design problem where the right auxiliary structure makes every operation O(1)).

</details>

---
