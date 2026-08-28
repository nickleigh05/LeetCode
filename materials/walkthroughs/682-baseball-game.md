# 682. Baseball Game

**Easy** · [LeetCode](https://leetcode.com/problems/baseball-game/) · [Solution file (no hints)](../../problems/0500-0999/682.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

You are keeping score for a game with a list of strings `operations`. Apply each in order and return the **sum of all scores** on the record afterward:

- **integer `x`** — record a new score of `x`
- **`"+"`** — record a new score that is the **sum of the previous two**
- **`"D"`** — record a new score that is **double the previous one**
- **`"C"`** — **invalidate** the previous score, removing it from the record

```
ops = ["5","2","C","D","+"]        →  30    record: [5, 10, 15]
ops = ["5","-2","4","C","D","9","+","+"]  →  27
```

**Constraints:** `1 <= operations.length <= 1000` · operations are valid · `-3·10⁴ <= x <= 3·10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the **previous** score" / "previous two" | ⚠️ Everything references the **most recent** entries. That's the definition of LIFO |
| "`C` **invalidates** the previous" | Remove from the end — a `pop` |
| "record a **new** score" | Append to the end — a `push` |
| "sum of all scores **on the record**" | Order is irrelevant to the answer; you just need the surviving multiset |
| "operations are **valid**" | No need to defend against `C` on an empty record, or `+` with fewer than two entries |
| `x` can be **negative** | So `"-2"` must parse correctly — a naive `isdigit()` check fails on it |

This is the most direct possible statement of a [stack](../data-structures/stack.md). Every operation touches only the top:

| Operation | Stack primitive |
|---|---|
| integer | `push(x)` |
| `"+"` | `push(top + second)` |
| `"D"` | `push(top * 2)` |
| `"C"` | `pop()` |

No searching, no scanning, no indexing into the middle. The whole problem is recognizing that "previous" always means "top of stack," and that a Python `list` already *is* a stack via `append` and `pop`.

🤔 **Before you open the next section:** which of these four operations changes the record's size, and in which direction?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Stack (Python list)** | `append` / `pop` / peek via `[-1]` | **O(n)** | O(n) | ✅ |
| [`deque`](../data-structures/deque.md) | Same operations from the right end | O(n) | O(n) | ⚠️ Works, but you never need the left end |
| Linked list | Manual node manipulation | O(n) | O(n) | ⚠️ Correct, needlessly manual |
| Running sum, no storage | Track a total, adjust per op | — | O(1) | ❌ **Doesn't work** — see below |

**The decision: a plain Python list used as a stack.**

`list.append()` and `list.pop()` are both **amortized O(1)** at the end, and `stack[-1]` / `stack[-2]` peek without removing. That's every primitive this problem needs, with no imports.

**Why you can't just keep a running total.** It's tempting: add on push, subtract on `C`. But `"+"` and `"D"` need the *values* of the last one or two entries, and a single total can't tell you what those were. `[5, 10]` and `[3, 12]` both sum to 15 but behave differently under `D`. **You must retain the individual scores**, which is exactly why a stack (and O(n) space) is required.

**Why a list beats a `deque` here.** A `deque` gives O(1) at *both* ends, but this problem only ever touches one end. Reaching for the more powerful structure when the simpler one suffices is a small signal — take the list. (`deque` earns its place in [Implement Stack using Queues](225-implement-stack-using-queues.md), where the *other* end genuinely matters.)

**The parsing subtlety.** The natural instinct is `if op.isdigit()`, but `"-2".isdigit()` is **`False`** — the minus sign isn't a digit. That would silently misroute negative numbers into the `else` branch or crash. The clean approach is to check the three known *commands* first and treat everything else as a number:

```python
if op == '+': ...
elif op == 'D': ...
elif op == 'C': ...
else: stack.append(int(op))
```

Structuring the branches this way makes the negative-number case correct by construction rather than by an extra guard.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
```

The record. A Python list, used as a stack — `append` to push, `pop` to remove, `[-1]` to peek.
→ [list-basics](../syntax/list-basics.md) · [stack](../data-structures/stack.md)

```python
for i in operations:
```

Process operations in order. (`i` here is the operation string, not an index — `op` would be a clearer name.)
→ [for-loop](../syntax/for-loop.md)

```python
    if i == '+':
        stack.append(stack[-1] + stack[-2])
```

**Sum of the previous two.** `stack[-1]` is the last score, `stack[-2]` the one before it.

Note both are **peeks, not pops** — the previous two scores stay on the record, and a *new* third entry is added. Popping them would be wrong: `"+"` adds a score, it doesn't consume the ones it reads.

Negative indexing is Python's idiom for "from the end"; `stack[-2]` is the second-to-last.
→ [list-slicing](../syntax/list-slicing.md)

```python
    elif i == 'D':
        stack.append(stack[-1] * 2)
```

**Double the previous.** Again a peek-then-push — the original score remains.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    elif i == 'C':
        stack.pop()
```

**Invalidate the previous.** The only operation that shrinks the record. `pop()` with no argument removes and returns the last element in O(1).
→ [list-methods](../syntax/list-methods.md)

```python
    else:
        stack.append(int(i))
```

**Anything else is a number.** Reaching the `else` means the token wasn't one of the three commands, so it's an integer literal — and `int()` handles the leading `-` correctly, which `isdigit()` would not.
→ [type-conversion](../syntax/type-conversion.md) · [elif-else](../syntax/elif-else.md)

```python
return sum(stack)
```

Total everything still on the record. Order never mattered — only which entries survived.
→ [any-all](../syntax/any-all.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def calPoints(self, operations: List[str]) -> int:

        stack = []

        for i in operations:
            if i == '+':
                stack.append(stack[-1] + stack[-2])
            elif i == 'D':
                stack.append(stack[-1] * 2)
            elif i == 'C':
                stack.pop()
            else:
                stack.append(int(i))

        return sum(stack)
```

</details>

**Trace it** — `operations = ["5","2","C","D","+"]`:

| Op | Action | Stack after |
|---|---|---|
| `"5"` | push 5 | `[5]` |
| `"2"` | push 2 | `[5, 2]` |
| `"C"` | pop (removes 2) | `[5]` |
| `"D"` | push `5 × 2 = 10` | `[5, 10]` |
| `"+"` | push `10 + 5 = 15` | `[5, 10, 15]` |

`sum([5, 10, 15])` = **30** ✅

**And the negative-number case** — `["5","-2","4","C","D","9","+","+"]`:

| Op | Action | Stack after |
|---|---|---|
| `"5"` | push 5 | `[5]` |
| `"-2"` | push −2 (`int("-2")` ✅) | `[5, -2]` |
| `"4"` | push 4 | `[5, -2, 4]` |
| `"C"` | pop (removes 4) | `[5, -2]` |
| `"D"` | push `-2 × 2 = -4` | `[5, -2, -4]` |
| `"9"` | push 9 | `[5, -2, -4, 9]` |
| `"+"` | push `9 + (-4) = 5` | `[5, -2, -4, 9, 5]` |
| `"+"` | push `5 + 9 = 14` | `[5, -2, -4, 9, 5, 14]` |

`sum` = `5 - 2 - 4 + 9 + 5 + 14` = **27** ✅

The `"-2"` at step 2 is exactly where `isdigit()`-based routing would break.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass over `operations`, and every branch does O(1) work:

- `append` — amortized O(1) (CPython over-allocates, so occasional resizes average out)
- `pop()` from the end — O(1), no shifting
- `stack[-1]` / `stack[-2]` — O(1) indexing
- `int(i)` — O(len(token)), and tokens are at most ~6 characters, so effectively O(1)

The final `sum(stack)` is one more O(n) pass. Total **O(n)**.

**The contrast worth noting:** `pop()` from the *end* is O(1), but `pop(0)` from the front is **O(n)** because every remaining element shifts left. That asymmetry is why a list works as a stack but makes a poor queue — precisely the issue that motivates [Implement Queue using Stacks](232-implement-queue-using-stacks.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the stack holds up to one entry per operation.

Worst case is all pushes with no `C`, giving exactly `n` entries.

**Could you do better?** No. As covered in section 2, `"+"` and `"D"` need the *values* of the most recent entries, and a running total can't reconstruct them. Retaining the individual scores is inherent to the problem, so **O(n) is a floor**.

That's a useful thing to be able to state confidently: not every O(n)-space solution is a trade you chose — sometimes the problem's information requirements force it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every operation references the most recent entries — 'previous score', 'previous two' — which is LIFO, so a stack. A Python list gives me `append`, `pop`, and `[-1]` peeking, all O(1). `+` and `D` peek rather than pop, since they add a new score without consuming the ones they read; `C` is the only operation that removes. I check the three command strings explicitly and treat everything else as an integer, which handles negative numbers — `isdigit()` would return `False` on `\"-2\"`. Then sum whatever survives. O(n) time and O(n) space, and the space is unavoidable because `D` and `+` need the individual values, not a running total."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it in O(1) space?" | No. `D` and `+` need the actual previous values; a running total can't recover them. |
| "What if operations could be invalid?" | Guard each branch: `if len(stack) >= 2` before `+`, `>= 1` before `D` and `C`. Decide whether to skip or raise. |
| "Add an 'undo last operation' command." | Now you need a stack of *stack states*, or a log of inverse operations — meaningfully harder. |
| "Why not `isdigit()`?" | `\"-2\".isdigit()` is `False`. Check commands first and let `int()` handle the rest. |
| "Why peek instead of pop for `+`?" | The two previous scores stay on the record; `+` appends a third. |
| "Return the record, not the sum." | Return `stack` directly — insertion order is preserved. |
| "Use a `deque`?" | Works, but you only ever touch one end; a list is simpler and has less overhead. |

**Traps:**

- **Using `isdigit()` to detect numbers.** Fails on negatives — the single most common bug here.
- **Popping for `+` or `D`.** Those operations *read* the previous scores; only `C` removes.
- **`stack[-2] + stack[-1]` order confusion.** Addition is commutative so it happens not to matter here — but be deliberate, because in [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md) the order is critical for `-` and `/`.
- **Using `pop(0)`.** O(n) per call and removes from the *wrong* end entirely.
- **Forgetting `int()`.** Leaving tokens as strings makes `+` concatenate rather than add.
- **Summing as you go.** You'd have to subtract on `C`, which works — but you still need the stack for `D` and `+`, so it buys nothing.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the canonical LIFO matching problem) · [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md) (a stack of operands, where pop order *does* matter) · [Min Stack](155-min-stack.md) (a stack augmented with extra per-entry state) · [Decode String](394-decode-string.md) (nested structure handled with a stack).

</details>

---
