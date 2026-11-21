# 528. Random Pick with Weight

**Medium** · [LeetCode](https://leetcode.com/problems/random-pick-with-weight/) · [Solution file (no hints)](../../problems/0500-0999/528.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

You're given a 0-indexed array of positive integers `w`, where `w[i]` is the **weight** of index `i`. Implement `pickIndex()`, which randomly returns an index in `[0, w.length - 1]` with probability **`w[i] / sum(w)`**.

```
w = [1, 3]
pickIndex() → 0 with probability 1/4
              1 with probability 3/4

Solution([1, 3])
pickIndex() → 1
pickIndex() → 1
pickIndex() → 0      (any sequence consistent with those odds is accepted)
```

**Constraints:** `1 <= w.length <= 10⁴` · `1 <= w[i] <= 10⁵` · `pickIndex` is called at most 10⁴ times

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| probability `w[i] / sum(w)` | Heavier indices come up proportionally more often |
| a **class** with `pickIndex` called many times | Do the preparation **once** in `__init__`, then make each pick fast |
| weights up to 10⁵, length up to 10⁴ | The total can reach 10⁹, so you can't build a list with one entry per unit of weight |
| up to 10⁴ picks | O(n) per pick is 10⁸ total. Borderline. O(log n) is comfortable |

**The picture: lay the weights end to end on a number line.** With `w = [1, 3, 2]`:

```
index:     0 |     1     |  2
         [ 1 | 2   3   4 | 5   6 ]
prefix:    1         4       6
```

Each index owns a stretch of the line as long as its weight. Pick a random point between 1 and the total. The stretch it lands in is your answer, and longer stretches get hit more often in exact proportion.

**The stretches are given by the prefix sums.** `prefix = [1, 4, 6]` says index 0 owns `1..1`, index 1 owns `2..4` and index 2 owns `5..6`. A random target `t` belongs to the **first** index whose prefix sum is `>= t`.

**"Find the first value ≥ t in a sorted list" is binary search.** The prefix sums are sorted, because every weight is positive. So each pick is O(log n).

🤔 **Before you open the next section:** with `prefix = [1, 4, 6]` and a random target `t = 4`, which index should be returned, and which bisect function finds it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Setup | Per pick | Space | Verdict |
|---|---|---|---|---|
| Expand: repeat each index `w[i]` times | O(sum w) | O(1) | O(sum w) | ❌ Up to 10⁹ entries |
| Prefix sums + linear scan | O(n) | O(n) | O(n) | ⚠️ 10⁸ over all calls |
| **Prefix sums + binary search** | O(n) | **O(log n)** | O(n) | ✅ |
| Alias method | O(n) | O(1) | O(n) | ✅ Optimal, overkill here |

**The decision: [prefix sums](../learning/01b-prefix-sums.md) built once, then [binary search](../algorithms/binary-search.md) per pick**, using Python's [`bisect`](../syntax/bisect-module.md).

**Integer targets avoid the off-by-one.** Choose `target = random.randint(1, total)`. Both ends are included, so every unit of weight is equally likely. Then `bisect_left(prefix, target)` returns the first index whose prefix sum is `>= target`.

Why `bisect_left`? A target **equal** to a prefix sum is the last unit of that index's stretch. `prefix[1] = 4` means index 1 owns 2, 3 and 4. `bisect_left` returns the position of that equal value, index 1, which is right. `bisect_right` would skip past it to index 2, which is wrong.

**The alias method** (Vose's) gives O(1) per pick after O(n) setup. It's worth naming as the optimal answer, but it's rarely expected in an interview.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self, w: List[int]):
    self.prefix = []
    total = 0
    for weight in w:
        total += weight
        self.prefix.append(total)
    self.total = total
```

**Build the number line, once.** `self.prefix[i]` is the sum of weights `0..i`, which is where index `i`'s stretch ends. Storing it on `self` keeps it for every later pick. `self.total` is the length of the whole line.

`itertools.accumulate(w)` would build the same list in one call.
→ [init-method](../syntax/init-method.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) · [for-loop](../syntax/for-loop.md) · [itertools-basics](../syntax/itertools-basics.md)

```python
def pickIndex(self) -> int:
    target = random.randint(1, self.total)
```

**Throw a dart at the line.** `randint(a, b)` includes **both** ends, so each of the `total` units is equally likely. The units run from 1 to total, to match prefix sums that start at `w[0]`, not 0.
→ [random-module](../syntax/random-module.md)

```python
    return bisect.bisect_left(self.prefix, target)
```

**Find whose stretch the dart landed in.** `bisect_left` returns the first position where `prefix[pos] >= target`. That's the index that owns that unit. Since `target <= total = prefix[-1]`, the result is always a valid index.
→ [bisect-module](../syntax/bisect-module.md)

<details>
<summary>The whole thing together</summary>

```python
import bisect
import random

class Solution:

    def __init__(self, w: List[int]):
        self.prefix = []
        total = 0
        for weight in w:
            total += weight
            self.prefix.append(total)
        self.total = total

    def pickIndex(self) -> int:
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix, target)
```

</details>

**Trace it.** `w = [1, 3, 2]`, `prefix = [1, 4, 6]`, `total = 6`. Every possible target:

| `target` | `bisect_left` | Index | Owner's stretch |
|---|---|---|---|
| 1 | 0 | **0** | 1 |
| 2 | 1 | **1** | 2–4 |
| 3 | 1 | **1** | 2–4 |
| 4 | 1 | **1** | 2–4 (equal → stays left) |
| 5 | 2 | **2** | 5–6 |
| 6 | 2 | **2** | 5–6 |

Index 0 wins 1 of the 6 targets, index 1 wins 3 and index 2 wins 2. That matches `1/6`, `3/6`, `2/6` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n) setup, O(log n) per pick</summary>

- **`__init__`:** O(n), one pass to build the prefix sums.
- **`pickIndex`:** O(log n). One random number, then one binary search.

Over 10⁴ picks on 10⁴ weights, that's about 10⁴ × 14 ≈ 1.4·10⁵ steps, against 10⁸ for a linear scan per pick.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the prefix array, one entry per weight. Each pick uses O(1) extra.

Compare the expanded-list approach, which needs O(sum w), up to 10⁹ entries. The prefix sums store the same information as one boundary per index.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I picture the weights laid end to end on a number line, so each index owns a stretch as long as its weight. In the constructor I build prefix sums, which mark where each stretch ends. They're sorted because the weights are positive. To pick, I draw a random integer from 1 to the total and binary search for the first prefix sum at least that big, using bisect_left, so a target equal to a boundary stays with the index that owns it. O(n) setup, O(log n) per pick, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) per pick?" | The alias method (Vose's): O(n) setup into a table of (probability, alias) pairs, then each pick is one random column and one coin flip. |
| "Weights change between picks?" | Prefix sums would need O(n) per update. A [Fenwick tree](../data-structures/fenwick-tree.md) gives O(log n) updates and O(log n) searches. |
| "Why `randint(1, total)` and not `(0, total)`?" | Units run 1..total to match prefix sums that start at `w[0]`. Including 0 adds an extra unit that index 0 would always win. |
| "With floats?" | `random.random() * total` with `bisect_right` works, since the probability of landing exactly on a boundary is effectively zero. |
| "Pick uniformly from a stream of unknown length?" | [Reservoir sampling](../algorithms/reservoir-sampling.md). |

**Traps:**

- **`bisect_right` with integer targets.** A target equal to a boundary goes to the next index, which skews the odds and can return `n`, out of range.
- **`randint(0, total)`.** It has `total + 1` outcomes, which gives index 0 an extra share.
- **Building the prefix sums inside `pickIndex`.** O(n) per call, which wastes the class design.
- **Expanding to a list of size `sum(w)`.** Up to 10⁹ entries.

**This same move shows up in:** [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (prefix sums built once and queried many times) · [Search Insert Position](35-search-insert-position.md) (the `bisect_left` "first position ≥ target" search) · [Insert Delete GetRandom O(1)](380-insert-delete-getrandom-o1.md) (another randomised design problem) · [Time Based Key-Value Store](981-time-based-key-value-store.md) (binary search over sorted boundaries in a class).

</details>

---
