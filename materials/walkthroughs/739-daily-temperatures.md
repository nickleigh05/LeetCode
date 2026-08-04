# 739. Daily Temperatures

**Medium** · [LeetCode](https://leetcode.com/problems/daily-temperatures/) · [Solution file (no hints)](../../problems/0500-0999/739.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given an array `temperatures` of daily temperatures, return an array `answer` where `answer[i]` is **the number of days you have to wait after day `i` to get a warmer temperature**. If no future day is warmer, put `0`.

```
temperatures = [73,74,75,71,69,72,76,73]  →  [1,1,4,2,1,1,0,0]
temperatures = [30,40,50,60]              →  [1,1,1,0]
temperatures = [30,60,90]                 →  [1,1,0]
```

**Constraints:** `1 <= temperatures.length <= 10⁵` · `30 <= temperatures[i] <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**how many days until** warmer" | This is the **next greater element** problem in disguise — the classic name for it |
| "**after** day `i`" | Strictly forward-looking. Each day's answer lives somewhere to its right |
| "`0` if none" | A sentinel for "never warmer" — and initializing the array to 0 handles it for free |
| n up to 10⁵ | O(n²) = 10¹⁰ → dead. Target **O(n)** |
| temperatures are 30–100 | A narrow range, which permits an alternative bucket solution — but it isn't the intended one |

The brute force is obvious: for each day, scan right until you find something warmer. O(n²), and on a decreasing array like `[100,99,98,…]` every scan runs to the end.

Where's the waste? Consider `[75, 71, 69, 72]`. Scanning from day 1 (71) you pass 69 and find 72. Then scanning from day 2 (69) you look at 72 **again**. Every day re-examines the same future days.

Now flip the direction of thought. Instead of *"for each day, search forward for its answer"*, ask *"as each new day arrives, whose question does it answer?"*

Day 3 (72°) arrives. It resolves day 2 (69°) and day 1 (71°) — both were waiting, and both are colder. It does **not** resolve day 0 (75°), which is still warmer than 72.

Notice which days are "waiting" at any moment: they're always in **decreasing** temperature order. Any day that was colder than a later day has already been resolved and removed. And the most recently added waiting day is always the first one a new warm day can resolve.

> "Most recent unresolved item, resolved first" — LIFO. A [stack](../data-structures/stack.md).

🤔 **Before you open the next section:** if day 5 is warmer than day 4, can day 4 ever be the answer for any day *before* it? What does that let you throw away?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | For each day, scan right | O(n²) | ❌ 10¹⁰ on decreasing input |
| Scan right-to-left with jumps | Use computed answers to skip ahead | O(n) amortized | ⚠️ Clever, harder to justify |
| Bucket by temperature | 71 buckets, track the next occurrence of each | O(71n) | ⚠️ Exploits the narrow value range; not the general solution |
| **Monotonic stack** | Stack of unresolved indices, decreasing | **O(n)** | ✅ |

**The decision: a [monotonic decreasing stack](../data-structures/monotonic-stack.md) of *indices* whose answers are still unknown.**

The invariant:

> **The stack holds indices of days awaiting a warmer day, and their temperatures decrease from bottom to top.**

Why decreasing? Because if a day on the stack were *colder* than a day above it, that later, warmer day would already have resolved it. Anything still waiting must be warmer than everything added after it.

The rule per new day `i`:

- **While** the top of the stack is colder than today → today is its answer. Pop it and record `i - prev_index`.
- Then push `i`, since today itself now awaits something warmer.

**Why store indices, not temperatures?** The answer is a *distance* — `i - prev_index` — so you need to know where each waiting day was. Same reason as [Sliding Window Maximum](239-sliding-window-maximum.md).

**The connection to 239.** That problem used a monotonic **deque** because it needed to expire elements from the front as the window moved. Here there's no window, so nothing ever expires from the bottom — one end suffices, and a **stack** is exactly a deque with one end. The family is the same:

> **Monotonic structures work by discarding elements that are provably useless.** Once a warmer day arrives, every colder day before it is answered and gone forever.

**Why not the bucket approach?** It leans on temperatures being 30–100. It works, but it's a special-case trick — the stack solution generalizes to any comparable values, which is why it's what interviewers want.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
answer = [0] * len(temperatures)
```

Pre-filled with **0**, which is the required output for "no warmer day ever comes". Days left on the stack at the end are simply never written to — the default is already correct, so no cleanup pass is needed.
→ [list-basics](../syntax/list-basics.md)

```python
stack = []
```

Holds **indices** of days still waiting for a warmer temperature, in decreasing order of temperature.
→ [stack](../data-structures/stack.md)

```python
for i in range(len(temperatures)):
```

One forward pass. Each day gets a turn both as a *resolver* of earlier days and as a new *waiter*.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    while stack and temperatures[i] > temperatures[stack[-1]]:
```

**The resolution step.** While today is warmer than the day on top of the stack, today answers that day's question.

- `stack and …` guards against indexing an empty stack — `and` short-circuits, so `stack[-1]` is never evaluated when empty.
- `temperatures[stack[-1]]` is a double lookup: `stack[-1]` gives the *index*, then we read its temperature.
- It's a **`while`**, not an `if`, because one warm day can resolve many waiting days at once — see the trace.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        prev_index = stack.pop()
        answer[prev_index] = i - prev_index
```

Pop the resolved day and record its wait: `i - prev_index` is the number of days from that day to today.

Once popped, it's gone for good — its answer is final. Nothing later can be a *closer* warmer day, because today already is.
→ [list-methods](../syntax/list-methods.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    stack.append(i)
```

Push today. It's now the newest unresolved day, sitting on top — and the invariant holds, because everything warmer than it remains below and everything colder was just popped.

```python
return answer
```

Indices still on the stack keep their initialized `0` — correct, since no warmer day ever arrived.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        answer = [0] * len(temperatures)
        stack = []

        for i in range(len(temperatures)):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index
            stack.append(i)

        return answer
```

</details>

**Trace it** — `temperatures = [73,74,75,71,69,72,76,73]` (stack shown as *index(temp)*):

| `i` | temp | Pops (resolved) | Stack after | `answer` so far |
|---|---|---|---|---|
| 0 | 73 | — | `0(73)` | `[0,0,0,0,0,0,0,0]` |
| 1 | 74 | pop `0(73)` → `1-0=1` | `1(74)` | `[**1**,0,…]` |
| 2 | 75 | pop `1(74)` → `2-1=1` | `2(75)` | `[1,**1**,…]` |
| 3 | 71 | — (71 < 75) | `2(75) 3(71)` | |
| 4 | 69 | — (69 < 71) | `2(75) 3(71) 4(69)` | |
| 5 | 72 | pop `4(69)` → `1`; pop `3(71)` → `2` | `2(75) 5(72)` | `[1,1,0,**2**,**1**,…]` |
| 6 | 76 | pop `5(72)` → `1`; pop `2(75)` → `4` | `6(76)` | `[1,1,**4**,2,1,**1**,…]` |
| 7 | 73 | — (73 < 76) | `6(76) 7(73)` | |

Days 6 and 7 remain on the stack ⇒ they keep `0`.

Final: `[1,1,4,2,1,1,0,0]` ✅

Row 5 is the point of the `while` — one 72° day resolved **two** waiting days in a single iteration. And notice the stack is always decreasing: `75, 72` then `76`, never increasing.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — and the nested `while` is again what needs defending.

The argument is about **total** work:

> **Every index is pushed exactly once and popped at most once.** With n indices, that's at most n pushes and n pops across the entire run — 2n stack operations total, regardless of how the loops nest.

Each operation is O(1). Plus n iterations of O(1) bookkeeping → **O(n)**.

A single iteration's `while` can pop many items (row 5 popped two, and on `[5,4,3,2,1,100]` the last day pops five). But those pops are *paid for* by the pushes that created them. **Amortized** analysis, the same as [Sliding Window Maximum](239-sliding-window-maximum.md) and [Longest Consecutive Sequence](128-longest-consecutive-sequence.md).

**The sentence to have ready:**

> *"Each index is pushed once and popped once, so the total work is linear even though there's a loop inside a loop."*

**Versus brute force:** O(n²) → O(n). At n = 10⁵ that's 10¹⁰ operations down to ~2·10⁵.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** auxiliary for the stack.

The stack holds unresolved days, which in the worst case is all of them:

- **Worst case O(n):** strictly decreasing temperatures, `[100,99,98,…]`. Nothing is ever warmer, so nothing is ever popped and the stack grows to n.
- **Best case O(1):** strictly increasing, `[30,40,50,…]`. Each day immediately resolves the one before it, so the stack holds a single index.

`answer` is O(n) but it's the required output — state it as **"O(n) auxiliary for the stack, plus O(n) output."**

**The bucket alternative gets O(1) auxiliary**: since temperatures are 30–100, keep 71 slots recording the next day each temperature occurs, and scan right-to-left. That's O(71) = O(1) space, O(71n) time. Better on space, worse on time, and it only works because the value range happens to be tiny — mention it as evidence you read the constraints, but the stack is the answer that generalizes.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is next-greater-element. Brute force scans forward from every day, O(n²), and the waste is that the same future days get re-examined. So I flip it: instead of each day searching for its answer, I ask which earlier days *this* day resolves. The days still waiting are always in decreasing temperature order — anything colder than a later day was already resolved — so I keep a monotonic decreasing stack of indices. Each new day pops every colder day off the top and records the distance, then pushes itself. Each index is pushed and popped at most once, so O(n) time and O(n) space for the stack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the nested loop still O(n)?" | **The question.** Each index is pushed once and popped once, so total pops ≤ n across the whole run — amortized, not per-iteration. |
| "Why indices instead of temperatures?" | The answer is a distance, so you need each waiting day's position. |
| "Next *smaller* element?" | Flip the comparison — keep an increasing stack. Same code. |
| "The *previous* warmer day?" | Same stack, but record the answer when pushing rather than popping: the element below you is your previous greater. |
| "Exploit the 30–100 range." | 71 buckets holding the next occurrence of each temperature, scanned right to left. O(1) space, O(71n) time. |
| "What about ties?" | `>` means an equal temperature doesn't resolve anything, matching "warmer". Use `>=` if the problem said "at least as warm" — **ask** which is meant. |
| "How does this relate to problem 239?" | Same monotonic family. 239 needs a deque because a window expires elements from the front; here nothing expires, so one end — a stack — is enough. |

**Traps:**

- **Pushing temperatures instead of indices.** You can then compute *that* it got warmer, but not *when*.
- **`if` instead of `while`.** One warm day can resolve several waiting days; an `if` resolves only the topmost and silently leaves the rest wrong.
- **Forgetting the `stack and` guard** — `stack[-1]` on an empty list raises `IndexError`.
- **Comparing `temperatures[i] > stack[-1]`** — that compares a temperature to an *index*. It runs without error and produces nonsense, which makes it nasty to debug.
- **A cleanup pass** setting leftover stack entries to 0. Unnecessary — the array was initialized to 0.
- **`i - prev_index - 1`** or similar. It's the plain difference; verify on day 0 → day 1, which must be 1.

**This same move shows up in:** [Sliding Window Maximum](239-sliding-window-maximum.md) (the deque version, when elements expire) · [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (a monotonic stack computing widths on pop) · [Car Fleet](853-car-fleet.md) (a stack resolving items against the one ahead) · [Trapping Rain Water](42-trapping-rain-water.md) (solvable with the same monotonic stack).

</details>
