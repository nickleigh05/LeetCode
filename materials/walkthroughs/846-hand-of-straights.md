# 846. Hand of Straights

**Medium** · [LeetCode](https://leetcode.com/problems/hand-of-straights/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Alice has a `hand` of cards, each with an integer value. She wants to rearrange them into **groups of exactly `groupSize`**, where each group consists of `groupSize` **consecutive** cards. Return `true` if that's possible.

```
hand = [1,2,3,6,2,3,4,7,8], groupSize = 3   →  true    [1,2,3], [2,3,4], [6,7,8]
hand = [1,2,3,4,5],         groupSize = 4   →  false   5 cards don't divide into groups of 4
hand = [8,10,12],           groupSize = 3   →  false   not consecutive
```

**Constraints:** `1 <= hand.length <= 10⁴` · `0 <= hand[i] <= 10⁹` · `1 <= groupSize <= hand.length`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return true/false" | Feasibility. You don't have to *report* the groups, only prove they exist |
| "groups of **exactly** `groupSize`" | Every card is used, and no group is partial. So `len(hand) % groupSize` must be 0 — a free early rejection |
| "**consecutive** cards" | A group starting at `v` is exactly `v, v+1, …, v+groupSize-1`. **Knowing the smallest card in a group determines the entire group** |
| duplicates are allowed | `[1,2,3,2,3,4]` is fine. So you need **counts**, not a set |
| values up to 10⁹ | Sparse. Don't index an array by card value; use a hash map |
| `n <= 10⁴` | O(n log n) or O(n · groupSize) is comfortable |

The observation in row 3 is the one that matters, so state it precisely:

> **A group is fully determined by its smallest card.**

That's what makes a greedy possible. Normally "partition into groups" is a combinatorial nightmare, but here you never choose a *group* — you only choose a **starting value**, and everything else follows.

Now, which starting value? Look at the **smallest card remaining in the whole hand**. It has to be in *some* group. And within that group it must be the smallest member — nothing smaller exists to sit below it. So the group containing it is forced: it runs from that card upward.

**There is no choice to make.** The smallest remaining card's group is completely determined, so you form it, remove those cards, and repeat. If the required consecutive cards aren't available, the answer is `false` — not because you picked wrong, but because **there was nothing else to pick.**

That's the strongest kind of greedy: not "this choice looks best" but **"this is the only legal choice."**

🤔 **Before you open the next section:** if the smallest remaining card is a 5 and there are **three** copies of it, how many groups must start at 5? Could you handle them one at a time, or is there a shortcut?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every partition | Enumerate all ways to split the hand | **exponential** | O(n) | ❌ |
| Sort, then repeatedly scan for a group | Take the smallest, linear-search for each next card | O(n²) | O(n) | ⚠️ Correct but wasteful |
| Min-heap of card values | Pop the smallest, remove the consecutive run | O(n log n) | O(n) | ✅ Works, but a heap makes "remove a specific value" awkward |
| **Counter + iterate sorted keys** | Count frequencies, process distinct values in ascending order | **O(n log n)** | O(n) | ✅ |
| Counter + [TreeMap](../data-structures/sorted-list.md)-style ordered map | Same, with an ordered structure instead of sorting | O(n log n) | O(n) | ✅ Equivalent; Python has no built-in TreeMap |

**The decision:** a **[Counter](../syntax/counter.md) of card frequencies, iterated in ascending order of distinct value.**

**Why the greedy is not merely "good" but forced.** Every greedy needs a justification, and this one has the cleanest available: **the smallest remaining card cannot be anywhere except at the bottom of its own group.** Nothing smaller exists to precede it. So the group is determined, and forming it can't cost you a better option — there *is* no other option. An exchange argument isn't even needed.

Contrast [Coin Change](322-coin-change.md), where the greedy fails precisely because the largest coin *isn't* forced. Here the constraint structure removes the choice entirely.

**The batching insight** — the answer to section 1's question. If the smallest remaining value has **three** copies, then three separate groups must start there, and each needs the same consecutive run. Rather than looping three times, you handle all three at once: require `count[next] >= 3` for each subsequent value and subtract 3.

That's what `needed` does below, and it's a real optimization. Without it, a hand like 5000 copies of `1` plus 5000 of `2` and `3` would loop 5000 times; with it, one pass over three distinct values.

**Why counts rather than a set?** Duplicates are legal and essential — `[1,2,3,2,3,4]` is a valid hand. A set would lose the multiplicities that decide feasibility.

**Why not index an array by card value?** Values reach 10⁹, so an array would be absurd. A hash map handles the sparsity, and sorting its **distinct keys** (at most n of them, often far fewer) gives the ascending order the greedy requires.

**Why not a heap?** A min-heap gives you the smallest card cheaply, but the algorithm also needs to *remove specific values* — `card+1`, `card+2`, … — which a heap can't do efficiently. Sorted keys plus a count map supports both operations naturally.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import Counter
```
[`Counter`](../syntax/counter.md) is a dict subclass that tallies occurrences. Its key convenience here: **querying a missing key returns 0 instead of raising `KeyError`**, so the "is the next card available?" test needs no membership check.
→ [counter](../syntax/counter.md) · [from-import](../syntax/from-import.md) · [hashmap](../data-structures/hashmap.md)

```python
if len(hand) % groupSize != 0:
    return False
```
**The free rejection.** Every card must land in a group of exactly `groupSize`, so the total has to divide evenly. `[1,2,3,4,5]` with `groupSize = 4` fails here before any real work.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [if-return](../syntax/if-return.md)

```python
count = Counter(hand)
```
One pass, producing `{card_value: how_many}`. From here the original list is irrelevant — only the multiset matters.
→ [counter](../syntax/counter.md)

```python
for card in sorted(count):
```
**Iterate the distinct values in ascending order.** `sorted(count)` sorts the *keys*, not the full hand — so if there are many duplicates this is much shorter than `sorted(hand)`.

Ascending order is what makes the greedy valid: each `card` you reach is the smallest value that still has cards left, which (by section 1) is forced to start a group.
→ [sorting-key](../syntax/sorting-key.md) · [for-loop](../syntax/for-loop.md) · [dict-basics](../syntax/dict-basics.md)

```python
    if count[card] == 0:
        continue
```
This value was fully consumed by earlier groups — every copy of it was absorbed as the 2nd, 3rd, … member of a group starting lower down. Nothing to do.

Note the loop iterates over a **snapshot** of the sorted keys, so values whose counts have since dropped to zero still appear. This skip handles them.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    needed = count[card]   # every remaining copy must start a group here
```
**The batching step.** Every remaining copy of `card` must begin its own group, because no smaller value survives to absorb it. If there are 3 copies, exactly 3 groups start here.

Capturing this *before* the inner loop matters — `count[card]` is about to be decremented, so reading it later would give the wrong multiplier.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    for next_card in range(card, card + groupSize):
        if count[next_card] < needed:
            return False
        count[next_card] -= needed
```
**Form all `needed` groups at once.** Each group runs `card, card+1, …, card+groupSize-1`, so every value in that range must supply `needed` copies.

- **`count[next_card] < needed` → `False`.** Not enough cards to complete the groups, and since the groups were *forced*, no rearrangement could help. This is where infeasibility is detected.
- **`count[next_card] -= needed`** consumes them.

The [`range`](../syntax/range-function.md) starts at `card` itself, which is deliberate — the first iteration zeroes out `count[card]`, which is why the `continue` above works on later passes.

And thanks to `Counter`'s default, a missing `next_card` reads as 0, correctly failing the check without a `KeyError`.
→ [range-function](../syntax/range-function.md) · [counter](../syntax/counter.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [if-return](../syntax/if-return.md)

```python
return True
```
Every card was consumed by a valid group. Since the divisibility check passed and nothing failed, the partition exists.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import Counter

class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:

        if len(hand) % groupSize != 0:
            return False

        count = Counter(hand)

        for card in sorted(count):
            if count[card] == 0:
                continue

            needed = count[card]   # every remaining copy must start a group here
            for next_card in range(card, card + groupSize):
                if count[next_card] < needed:
                    return False
                count[next_card] -= needed

        return True
```
</details>

**Trace it** — `hand = [1,2,3,6,2,3,4,7,8]`, `groupSize = 3`

9 cards ÷ 3 = 3 groups ✓. Counts: `{1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}`

| `card` | `count[card]` | `needed` | requires | after |
|---|---|---|---|---|
| 1 | 1 | **1** | one each of 1, 2, 3 — all available ✓ | `{1:0, 2:1, 3:1, 4:1, 6:1, 7:1, 8:1}` |
| 2 | 1 | **1** | one each of 2, 3, 4 — all available ✓ | `{2:0, 3:0, 4:0, 6:1, 7:1, 8:1}` |
| 3 | **0** | — | skipped | — |
| 4 | **0** | — | skipped | — |
| 6 | 1 | **1** | one each of 6, 7, 8 — all available ✓ | all zero |
| 7 | **0** | — | skipped | — |
| 8 | **0** | — | skipped | — |

Return **true** ✅ — the groups `[1,2,3]`, `[2,3,4]`, `[6,7,8]`.

Rows 3 and 4 show the `continue` earning its place: 3 and 4 were consumed as the *middle and top* of the group starting at 2, so by the time the loop reaches them there's nothing left.

**And a batching case** — `hand = [1,1,2,2,3,3]`, `groupSize = 3`:

Counts: `{1:2, 2:2, 3:2}`

| `card` | `needed` | requires | after |
|---|---|---|---|
| 1 | **2** | **two** each of 1, 2, 3 — all available ✓ | all zero |
| 2 | 0 | skipped | — |
| 3 | 0 | skipped | — |

Return **true** ✅ — two groups of `[1,2,3]` formed in a **single** pass rather than two, because `needed = 2` handled both at once.

**And the two failure modes** — `hand = [8,10,12]`, `groupSize = 3`:

3 cards ÷ 3 = 1 group ✓, so the divisibility check passes. Counts: `{8:1, 10:1, 12:1}`

| `card` | `needed` | requires | result |
|---|---|---|---|
| 8 | 1 | one 8 ✓, then one **9** — `count[9]` is **0 < 1** | **return false** |

Return **false** ✅ — and note `Counter` returned 0 for the absent key 9 rather than raising, which is exactly why no membership check is needed.

The other failure mode is cheaper still: `hand = [1,2,3,4,5]` with `groupSize = 4` returns **false** from the divisibility check, before a Counter is ever built.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, where n = `len(hand)`.

- Building the `Counter` — one pass → **O(n)**.
- `sorted(count)` — sorting **k distinct values**, where k ≤ n → **O(k log k)**, which is O(n log n) in the worst case. **This dominates.**
- The nested loops: the outer runs k times, the inner `groupSize` times → O(k · groupSize) iterations. But notice the total work is bounded differently — **each of the n cards is consumed exactly once** across all the decrements, so the loops do **O(n)** work overall, not O(k · groupSize).
- Total: **O(n log n)**, dominated by the sort.

At n = 10⁴ that's trivial.

**The amortized argument is worth stating**, because the nested loops look worse than they are: every `count[next_card] -= needed` permanently removes `needed` cards from circulation, and there are only n cards. So the inner loop can't run more than n times in total across the whole algorithm, regardless of how the outer loop behaves.

**Can the sort be avoided?** In a language with a TreeMap (Java, C++'s `std::map`) you'd keep the counts in an ordered structure and get the minimum in O(log k) without a separate sort — still O(n log n) overall. Python has no built-in ordered map, so sorting the keys is the idiomatic choice.

**Faster?** Not meaningfully. You need the values in sorted order to know which is smallest, and comparison sorting is Ω(k log k). With bounded values you could counting-sort, but values reach 10⁹, so that's out.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the `Counter` holds one entry per **distinct** card value, up to n of them if all cards differ. `sorted(count)` allocates a list of those keys, also O(n).

| Component | Space |
|---|---|
| `Counter` | **O(k)** distinct values, ≤ n |
| `sorted(count)` list | **O(k)** |
| `needed`, loop variables | O(1) |

**Why a hash map rather than an array indexed by value:** card values reach 10⁹, so an array would need a billion slots for what might be ten distinct cards. **The hash map's cost scales with what's present, not with the value range** — the standard reason to prefer it whenever the key space is sparse.

**Can it be O(1)?** No. You genuinely need the multiset of cards; there's no running summary that captures feasibility. Contrast [Maximum Subarray](53-maximum-subarray.md) and [Jump Game](55-jump-game.md), where the state compressed to a couple of integers — here the state *is* the remaining cards.

**A small saving:** you could sort the hand in place and work with indices rather than a Counter, but that's O(n log n) time either way and makes the "consume `needed` copies" step much fiddlier. The Counter version is clearer for the same asymptotic cost.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key structural fact is that a group of consecutive cards is completely determined by its smallest member — so I never choose a *group*, only a starting value. And the smallest card remaining in the hand has no choice at all: it can't sit anywhere but at the bottom of its own group, because nothing smaller exists to precede it. So the greedy isn't 'this looks best', it's 'this is the only legal move.' I count frequencies, walk the distinct values in ascending order, and for each one that still has cards left, I form groups starting there. If there are three copies I form all three groups at once — they all need the same consecutive run, so I just require three of each subsequent value and subtract three. If any required card is missing, it's impossible, because the groups were forced. O(n log n) from sorting the distinct keys; the nested loops are only O(n) total, since each card is consumed exactly once."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why must you start at the smallest card?" | It can't be anywhere but the bottom of its group — no smaller card exists to precede it. So its group is forced, and forming it can't cost you a better option because there isn't one. |
| "Why batch all copies of a value at once?" | Every remaining copy must start its own group, and they all need identical consecutive runs. Handling them together turns a potentially 10⁴-iteration loop into one. |
| "Why not a heap?" | A heap gives the minimum cheaply but can't efficiently remove *specific* values like `card+1`. You need both operations, so a count map plus sorted keys fits better. |
| "Why not an array indexed by card value?" | Values go up to 10⁹. The hash map's cost scales with the number of distinct cards, not the value range. |
| "What if you had to output the groups?" | Same algorithm — append each formed group instead of just decrementing. Space becomes O(n) for the output. |
| "How does this relate to [Divide Array in Sets of K Consecutive Numbers](https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/)?" | It's the identical problem with different wording. Same solution verbatim. |
| "Could you use a TreeMap?" | In Java or C++, yes — keep counts in an ordered map and repeatedly take the smallest key. Same O(n log n), no separate sort. Python lacks a built-in equivalent. |
| "What if groups had to be consecutive *and* the same suit?" | Group by suit first, then run this per suit. The greedy is unaffected. |

**Traps:**
- **Reading `count[card]` after the inner loop starts decrementing it.** `needed` must be captured first, or the multiplier is wrong from the second iteration onward.
- **Forgetting the divisibility check.** Not just an optimization — without it, a hand like `[1,2,3,4]` with `groupSize = 3` could consume `[1,2,3]` and return `True` with a card stranded.
- Iterating `sorted(hand)` instead of `sorted(count)` — correct but slower, and it re-visits duplicates that the `continue` would have skipped.
- Using a `set` instead of a `Counter`. Duplicates are legal and decide feasibility.
- Starting the inner range at `card + 1` — then `count[card]` is never zeroed and the `continue` never fires, so the same value forms groups repeatedly.
- Processing values in unsorted order. The greedy's entire justification depends on always taking the smallest remaining.

**This same move shows up in:** [Task Scheduler](621-task-scheduler.md) (frequency counting driving a greedy scheduling decision) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (a Counter as the foundation of the algorithm) · [Merge Triplets to Form Target Triplet](1899-merge-triplets-to-form-target-triplet.md) (a greedy whose validity comes from certain options being *forbidden* rather than merely worse) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (processing in sorted order so each decision is forced).

</details>

---
