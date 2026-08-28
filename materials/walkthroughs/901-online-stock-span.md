# 901. Online Stock Span

**Medium** · [LeetCode](https://leetcode.com/problems/online-stock-span/) · [Solution file (no hints)](../../problems/0500-0999/901.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Design an algorithm that collects daily stock price quotes and returns the **span** of that stock's price for the current day. The span is the maximum number of consecutive days (ending today, going backwards) for which the price was **less than or equal to** today's price.

```
StockSpanner()
next(100) → 1
next(80)  → 1
next(60)  → 1
next(70)  → 2    (70 ≥ 60, 70 < 80 → spans [60, 70])
next(60)  → 1
next(75)  → 4    (75 ≥ 60, 70, 60 → spans [60,70,60,75])
next(85)  → 6
```

**Constraints:** `1 <= price <= 10⁵` · at most `10⁴` calls to `next`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**consecutive** days going backwards" | You're looking left until the streak breaks |
| "price **≤** today's price" | ⚠️ Note the **≤**, not `<`. Equal prices *continue* the span |
| "**online**" | Prices arrive one at a time; you can't see the future, and you can't re-read the past cheaply |
| span ends when a **greater** price is found | Restated: the span is the distance back to the **previous strictly greater** price |
| `10⁴` calls | O(n) per call is 10⁸ — too slow. Need O(1) amortized |

**The reframe that turns this into a known problem:**

> The span is the number of days since the **previous strictly greater price**.

If the last price greater than today's was `d` days ago, then everything in between was ≤ today, so the span is exactly `d`. That's "previous greater element" — the mirror image of [Next Greater Element I](496-next-greater-element-i.md), which looked forward. Same [monotonic stack](../data-structures/monotonic-stack.md), pointed the other way.

**The key observation that makes it O(1) amortized:**

When today's price is ≥ some earlier price, that earlier price **can never matter again**. Any future day that would have been blocked by it is now blocked by today instead — today is at least as large *and* more recent. So you can discard it permanently.

But you mustn't lose the days it accounted for. The trick is to **absorb its span into yours**:

```
prices:  60   70          75
spans:   1  → 2 (ate 60)  → 4 (ate 70, which had already eaten 60)
```

Each stack entry is a `(price, span)` pair, where `span` is "how many days this entry represents." Popping an entry means inheriting its days. That's what compresses a potentially long backward scan into a handful of pops.

🤔 **Before you open the next section:** if you throw away an old price because today's is bigger, how do you avoid forgetting the days it was covering?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time per call | Space | Verdict |
|---|---|---|---|---|
| Store all prices, scan back | Walk backwards counting ≤ today | O(n) | O(n) | ⚠️ Correct; O(n²) overall = 10⁸ |
| Store all prices + precompute | Nothing to precompute — it's online | — | — | ❌ Future prices unknown |
| **Monotonic stack of `(price, span)`** | Pop smaller entries, absorbing their spans | **O(1) amortized** | O(n) | ✅ |

**The decision: a monotonic stack of `(price, span)` pairs, decreasing in price from bottom to top.**

Each `next(price)` does:

1. Start `span = 1` — today always counts for itself.
2. While the stack top has `price <= today`, pop it and **add its span to yours**.
3. Push `(today, span)`.
4. Return `span`.

**Why absorbing spans is correct.** A popped entry represented some block of consecutive days, all with prices ≤ its own price — which is ≤ today's. So all of those days are also ≤ today and belong in today's span. Adding its span adds exactly that block, without ever re-walking it.

**Why the stack stays decreasing.** Anything ≤ today gets popped before today is pushed, so whatever remains beneath is strictly greater. That's the invariant, and it's what makes step 2 a simple `while`.

**Why `<=` and not `<`.** The problem says "less than **or equal to**." An earlier day with the *same* price is part of today's span, so it must be popped and absorbed. Using `<` would stop at equal prices and under-count — e.g. `next(50)` twice should give `1` then `2`.

**Why storing only prices isn't enough.** If entries were bare prices, popping would tell you *that* a day was absorbed but not *how many* days it stood for — you'd have to count them, which reintroduces the O(n) scan. The span field is what compresses the history.

**Why it's O(1) amortized despite the `while`:** each price is pushed exactly once and popped at most once across the object's entire lifetime. Over `n` calls that's ≤ `n` pushes and ≤ `n` pops — **O(n) total**, hence O(1) per call on average. A single call can be O(n) (a large price after a long decline), but the total is bounded.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class StockSpanner:
    def __init__(self):
        self.stack = []
```

The only state: a stack of `(price, span)` tuples, decreasing in price bottom-to-top.

Notice there's no list of all prices — the stack *is* the compressed history, and everything absorbed is gone for good.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
    def next(self, price: int) -> int:
        span = 1
```

**Today always counts for itself**, hence 1 rather than 0. This is also the correct answer when nothing gets absorbed (today's price is lower than yesterday's).
→ [variables-assignment](../syntax/variables-assignment.md)

```python
        while self.stack and self.stack[-1][0] <= price:
            top = self.stack.pop()
            top_span = top[1]
            span = span + top_span
```

**Absorb every entry today dominates.**

- `self.stack[-1][0]` — the price of the top entry (index 0 of the tuple)
- `top[1]` — its span (index 1)

`<=` because equal prices continue the span. `while` because today may dominate many stacked entries at once.

`self.stack and ...` short-circuits so the indexing is never attempted on an empty stack.

Tuple unpacking would read more clearly — `top_price, top_span = self.stack.pop()` — but the indexed form here is equivalent.
→ [while-loop](../syntax/while-loop.md) · [tuple-basics](../syntax/tuple-basics.md) · [list-methods](../syntax/list-methods.md)

```python
        self.stack.append((price, span))
        return span
```

Push today with its **accumulated** span, so a future day that pops this entry inherits the whole block in one step. Then return it.
→ [tuple-unpacking](../syntax/tuple-unpacking.md)

<details>
<summary>The whole thing together</summary>

```python
class StockSpanner:

    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:

        span = 1

        while self.stack and self.stack[-1][0] <= price:
            top = self.stack.pop()
            top_span = top[1]
            span = span + top_span

        self.stack.append((price, span))

        return span


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```

</details>

**Trace it** — the full example sequence:

| Call | `span` start | Pops (price, span) | Final `span` | Stack after |
|---|---|---|---|---|
| `next(100)` | 1 | none | **1** | `[(100,1)]` |
| `next(80)` | 1 | none (100 > 80) | **1** | `[(100,1), (80,1)]` |
| `next(60)` | 1 | none (80 > 60) | **1** | `[(100,1), (80,1), (60,1)]` |
| `next(70)` | 1 | `(60,1)` → span 2 | **2** | `[(100,1), (80,1), (70,2)]` |
| `next(60)` | 1 | none (70 > 60) | **1** | `[(100,1), (80,1), (70,2), (60,1)]` |
| `next(75)` | 1 | `(60,1)` → 2 · `(70,2)` → 4 | **4** | `[(100,1), (80,1), (75,4)]` |
| `next(85)` | 1 | `(75,4)` → 5 · `(80,1)` → 6 | **6** | `[(100,1), (85,6)]` |

Return sequence **`[1,1,1,2,1,4,6]`** ✅

Look at `next(85)`: it absorbed `(75,4)` in a **single pop** and inherited four days at once. Those four days were themselves compressed from earlier pops — the history collapses rather than being re-walked. That's the whole reason this is O(1) amortized.

Also note the stack is always strictly decreasing in price: `[(100,1), (85,6)]` at the end.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) amortized per call</summary>

**O(1) amortized**, O(n) worst case for a single call, **O(n) total** across `n` calls.

The amortized argument, which is the whole point of the problem:

> Every price is pushed **exactly once** and popped **at most once** over the object's lifetime. Across `n` calls that's ≤ `n` pushes and ≤ `n` pops — O(n) total work, so O(1) per call on average.

**A single call can be expensive.** After `[100, 90, 80, 70, 60]`, a `next(200)` pops all five. That call is O(n). But those five entries can never be popped again, so the cost is *paid once*, not repeatedly.

**Say it out loud like this:** *"Individual calls can be O(n), but each element is pushed and popped at most once overall, so the total across n calls is O(n) — amortized O(1)."*

**Compare to the naive version:** storing all prices and scanning backwards is O(n) per call *every time* — O(n²) overall, 10⁸ at 10⁴ calls. The stack's compression is what avoids re-walking the same days.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, where `n` is the number of calls so far.

Worst case is a strictly **increasing** price sequence… no — think again. On strictly increasing prices, each new price pops everything, so the stack stays tiny. The worst case is strictly **decreasing** prices like `[100, 90, 80, …]`, where nothing is ever absorbed and every entry survives.

| Sequence | Stack size |
|---|---|
| `[100, 90, 80, 70]` (decreasing) | **4** — nothing pops |
| `[70, 80, 90, 100]` (increasing) | **1** — each pops everything |

So O(n) is the bound, but real usage is typically far below it — the stack holds only the "record highs from the right," which is usually a small subset.

**The compression insight worth keeping:**

> The stack stores only prices that could still block a future span. Everything else has been absorbed into a span count and discarded.

That's a genuinely different kind of memory saving than "we allocated a hash map" — you're storing a *summary* of history, not the history itself. The same idea underpins [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md), where popped bars contribute their widths, and it's the general shape of monotonic-stack problems that accumulate a quantity while popping.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The span is the number of days back to the previous **strictly greater** price, so it's a previous-greater-element problem — a monotonic stack, looking backwards. The insight is that once today's price is ≥ some earlier price, that earlier price is irrelevant forever: today is bigger and more recent, so it blocks everything the old one would have. So I pop it — but I must not lose the days it stood for, so each stack entry is a `(price, span)` pair and popping means **absorbing** its span into mine. I start at 1 for today itself, pop while the top price is ≤ today's, and push today with the accumulated span. It's O(1) amortized because each price is pushed once and popped at most once, and O(n) space in the worst case of strictly decreasing prices."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is it O(1) if there's a `while` loop?" | **The key question.** Each price is pushed once and popped at most once — total work over n calls is O(n). |
| "Why `<=` rather than `<`?" | The problem says "less than **or equal to**." Equal prices continue the span, so they must be absorbed. |
| "Why store spans instead of just prices?" | Popping a bare price wouldn't tell you how many days it represented; you'd have to re-count, restoring O(n). |
| "Store indices instead?" | Also works — push `(price, index)` and compute `span = current_index - popped_index`. Equivalent; requires tracking a day counter. |
| "Span with **strictly** less than?" | Change to `<`. Equal prices then break the span. |
| "Support a `rollback()` of the last day?" | Much harder — you'd need to restore absorbed entries, so a persistent/immutable stack or an undo log. |
| "What if prices could repeat heavily?" | Fine — equal prices are absorbed, so a run of identical prices collapses into one entry with a large span. |

**Traps:**

- **Using `<` instead of `<=`.** Under-counts whenever prices repeat. `next(50)` twice should give 1 then 2.
- **Not absorbing spans.** Returning the pop *count* instead of the summed spans loses all the compressed history — badly wrong on the `next(85)` step above.
- **Starting `span = 0`.** Today counts for itself; the answer would be off by one everywhere.
- **Storing every price and scanning back.** O(n) per call, O(n²) overall.
- **Indexing the tuple wrongly.** `stack[-1][0]` is the price, `[1]` is the span. Unpack into named variables if it's at all unclear.
- **Checking `stack[-1]` before testing `stack`.** `IndexError` on the very first call.

**This same move shows up in:** [Next Greater Element I](496-next-greater-element-i.md) (the same monotonic stack, looking forward) · [Daily Temperatures](739-daily-temperatures.md) (monotonic stack of indices, computing distances) · [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (accumulating width while popping — the same absorption idea) · [Min Stack](155-min-stack.md) (another stack where each entry carries extra state).

</details>

---
