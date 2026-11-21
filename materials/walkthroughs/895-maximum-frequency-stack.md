# 895. Maximum Frequency Stack

**Hard** · [LeetCode](https://leetcode.com/problems/maximum-frequency-stack/) · [Solution file (no hints)](../../problems/0500-0999/895.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Design a stack-like data structure that pushes values and pops the **most frequent** one.

- `push(val)`: push an integer onto the stack.
- `pop()`: remove and return the **most frequent** element. If there's a **tie**, remove the one **closest to the top**, meaning the one pushed most recently.

```
push(5), push(7), push(5), push(7), push(4), push(5)
stack (bottom → top): [5, 7, 5, 7, 4, 5]

pop() → 5     (5 appears 3 times)
pop() → 7     (5 and 7 both appear 2 times; 7 is closer to the top)
pop() → 5     (5 appears 2 times; 7 and 4 appear once)
pop() → 4
```

**Constraints:** `0 <= val <= 10⁹` · at most `2·10⁴` calls · `pop` is never called on an empty stack

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| pop the **most frequent** | You need fast access to the current maximum frequency |
| tie → **closest to the top** | Within a frequency, it's last in, first out. That's a stack |
| frequencies change on every push and pop | A value's count goes up and down, so the maximum can change too |
| up to 2·10⁴ calls | Aim for O(1) or O(log n) per call |

**The key insight: think of each push as joining a level.** When you push a value for the **k-th** time, put it in "level k." So with pushes `5, 7, 5, 7, 4, 5`:

```
level 3:  [5]                ← 5's third push
level 2:  [5, 7]             ← second pushes of 5, then 7
level 1:  [5, 7, 4]          ← first pushes of 5, 7, 4
```

Each level is its own **stack**, in push order. Now `pop` is simple:

1. Go to the **highest non-empty level**. Those values have the maximum frequency.
2. Pop from the **top** of that level. That's the most recent among the tied values.

This works because popping value `v` from level k leaves its copies in levels 1 to k − 1 untouched. They're its earlier pushes, and they're still correctly placed.

**Why the maximum level only drops by one.** When the top level empties, the next level down is guaranteed to be non-empty. Any value that reached level k also has an entry in level k − 1. So after emptying the top level, the maximum is always exactly one lower. You never have to search.

🤔 **Before you open the next section:** after the first `pop()` returns 5 from level 3, why is it safe to drop the maximum level to 2 straight away?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `push` | `pop` | Verdict |
|---|---|---|---|
| One list, scan on pop | O(1) | O(n) count + find | ❌ Too slow |
| Heap of `(-freq, -push_index, val)` | O(log n) | O(log n) | ✅ Works |
| **Frequency map + a stack per frequency** | **O(1)** | **O(1)** | ✅ |

**The decision: a [hash map](../data-structures/hashmap.md) of frequencies, plus a map from frequency to a [stack](../data-structures/stack.md) of values.**

- `freq[val]`: the current count of each value.
- `groups[f]`: a stack of the values pushed for the f-th time, in order.
- `max_freq`: the highest non-empty level.

Every operation is a few O(1) dictionary and list operations.

**The heap alternative.** Push `(-freq, -time, val)` into a [heap](../data-structures/heap.md), where `time` is a global push counter. The heap's top is then the most frequent and, among ties, the most recent. It's O(log n) per operation. It's a fine fallback if you can't see the level trick, but the level structure is the answer interviewers are looking for.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.freq = {}
    self.groups = {}
    self.max_freq = 0
```

The three pieces of state. `groups` maps a frequency to its stack of values. A `defaultdict(list)` would remove the "does this level exist" check below, but a plain dict keeps it explicit.
→ [init-method](../syntax/init-method.md) · [dict-basics](../syntax/dict-basics.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md)

```python
def push(self, val: int) -> None:
    f = self.freq.get(val, 0) + 1
    self.freq[val] = f
```

**Bump the value's frequency.** This is its f-th push, so it belongs in level f.
→ [dict-methods](../syntax/dict-methods.md)

```python
    if f > self.max_freq:
        self.max_freq = f
```

**A new highest level?** Frequencies only go up one at a time, so if `f` beats `max_freq`, it's exactly one higher.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    if f not in self.groups:
        self.groups[f] = []
    self.groups[f].append(val)
```

**Push the value onto level f's stack.** Create the level the first time it's needed. Earlier levels keep their copies of `val`.
→ [membership-operators](../syntax/membership-operators.md) · [list-methods](../syntax/list-methods.md)

```python
def pop(self) -> int:
    val = self.groups[self.max_freq].pop()
    self.freq[val] -= 1
```

**Take the most recent value from the top level.** Those values all have the maximum frequency, and the stack order breaks ties in favour of the most recent push. Then lower the value's count.
→ [list-methods](../syntax/list-methods.md)

```python
    if not self.groups[self.max_freq]:
        self.max_freq -= 1
    return val
```

**If the top level is now empty, step down one.** The next level down is guaranteed to have something in it, because every value that reached level k also has a copy in level k − 1.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

<details>
<summary>The whole thing together</summary>

```python
class FreqStack:

    def __init__(self):
        self.freq = {}
        self.groups = {}
        self.max_freq = 0

    def push(self, val: int) -> None:
        f = self.freq.get(val, 0) + 1
        self.freq[val] = f
        if f > self.max_freq:
            self.max_freq = f
        if f not in self.groups:
            self.groups[f] = []
        self.groups[f].append(val)

    def pop(self) -> int:
        val = self.groups[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.groups[self.max_freq]:
            self.max_freq -= 1
        return val
```

</details>

**Trace it.** The example's pushes give:

```
groups = {1: [5, 7, 4],  2: [5, 7],  3: [5]}      max_freq = 3
```

| Call | Level popped from | Returns | Levels after | `max_freq` |
|---|---|---|---|---|
| `pop()` | 3 | **5** | `{1:[5,7,4], 2:[5,7], 3:[]}` | 3 → **2** |
| `pop()` | 2 | **7** | `{1:[5,7,4], 2:[5]}` | 2 |
| `pop()` | 2 | **5** | `{1:[5,7,4], 2:[]}` | 2 → **1** |
| `pop()` | 1 | **4** | `{1:[5,7]}` | 1 |

The output `5, 7, 5, 4` matches ✅. In the second pop, 5 and 7 were tied at 2, and level 2's stack put 7 on top because it was pushed more recently.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) per operation</summary>

**O(1)** for both `push` and `pop`. Each one does a constant number of dict lookups and updates and a single list append or pop. There are no loops and no searching, since `max_freq` is always known and only changes by one.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, where n is the number of values currently in the structure. Each push stores exactly one entry, in one level, and each pop removes exactly one. `freq` has one key per distinct value.

Empty level lists may stay in `groups`, but there are at most `max_freq` of them, which is ≤ n.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I treat each push as joining a level: the k-th push of a value goes on stack k. I keep a frequency map, a map from frequency to a stack of values, and the current max frequency. Pop takes from the top of the max-frequency stack, which gives the most frequent value, with ties broken by recency because it's a stack. Then I decrement that value's count, and if the level is empty I lower the max by one. The level below is never empty, because every value at level k also has a copy at level k − 1. Both operations are O(1), and space is O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the next level down never empty?" | Any value at level k was pushed k times, so it also has a copy at level k − 1. |
| "Alternative if you don't see the trick?" | A heap of `(-freq, -push_time, val)`. O(log n) per operation. |
| "Ties broken by the *oldest* instead?" | The level trick depends on recency, so switch to the heap: `(-freq, +push_time, val)` puts the earliest push first among ties. |
| "Least frequent instead?" | Track `min_freq`. But it can jump around on pop. That's LFU Cache territory (LeetCode 460). |
| "Also support `peek`?" | Return `self.groups[self.max_freq][-1]` without popping. |

**Traps:**

- **Removing a value from *every* level on pop.** Only its top copy goes. Lower copies represent earlier pushes and stay.
- **Searching for the new maximum after a pop.** It's always `max_freq − 1` when the top level empties.
- **Ignoring recency among ties.** A frequency map alone can't break ties. The per-level stack is what does it.
- **Scanning a single list on every pop.** O(n) per pop.

**This same move shows up in:** [Min Stack](155-min-stack.md) (a stack carrying extra information so every query is O(1)) · [LRU Cache](146-lru-cache.md) (combining two structures for O(1) operations) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (bucketing values by frequency) · [Task Scheduler](621-task-scheduler.md) (choosing the most frequent item repeatedly).

</details>

---
