# 881. Boats to Save People

**Medium** · [LeetCode](https://leetcode.com/problems/boats-to-save-people/) · [Solution file (no hints)](../../problems/0500-0999/881.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

`people[i]` is the weight of the `i`-th person. Each boat carries **at most two people** at once, and their combined weight must be at most `limit`. Return the **minimum number of boats** needed to carry everyone. Every person's weight is at most `limit`, so everyone can always travel alone.

```
people = [1, 2],        limit = 3   →  1     (1 + 2 = 3)
people = [3, 2, 2, 1],  limit = 3   →  3     ([1, 2], [2], [3])
people = [3, 5, 3, 4],  limit = 5   →  4     (no two fit together)
```

**Constraints:** `1 <= people.length <= 5 * 10⁴` · `1 <= people[i] <= limit <= 3 * 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "at most **two** people" | Each boat is either a solo trip or a **pair**. So the whole problem is choosing good pairs |
| "minimum number of boats" | Maximise the number of pairs. Each pair saves one boat |
| `people[i] <= limit` | Nobody is too heavy. Every person can at least travel alone, so the answer always exists |
| order of `people` is arbitrary | Order carries no meaning, so **sort** it |

**The greedy instinct.** Look at the **heaviest** person. They are the hardest to pair. Only the **lightest** person has the best chance of fitting with them:

- If the lightest person fits with the heaviest, pair them. You can't do better with that heavy person.
- If the lightest *doesn't* fit with the heaviest, **nobody does** (everyone else is heavier than the lightest). The heavy person goes alone.

Either way, the heaviest person leaves on this boat, and you've lost nothing.

🤔 **Before you open the next section:** after sorting, which two indices do you compare first, and which index definitely leaves in this boat regardless of the outcome?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every pairing | Search all ways to group people | exponential | — | ❌ |
| Greedy, heaviest first, scan for a partner | For each heavy person find any who fits | O(n²) | O(1) | ⚠️ Right idea, slow search |
| **Sort + two pointers** | `left` = lightest, `right` = heaviest | **O(n log n)** | O(1) or O(n) for the sort | ✅ |
| Counting sort + two pointers | Bucket weights | O(n + limit) | O(limit) | ✅ Faster, but more code |

**The decision: sort, then [two pointers](../learning/02-two-pointers.md) from both ends.** It's the same "converge from both sides of a sorted array" pattern as [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) and [Container With Most Water](11-container-with-most-water.md).

**Why the greedy is right (the exchange argument).** Take any optimal solution where `H + L` fits but `H` rides with someone else `X` (or alone) and `L` rides with `Y` (or alone). Swap `X` and `L`:

- The new boat `H + L` fits, because `L <= X` and `H + X` already fit.
- The other boat `X + Y` fits, because `Y <= H` (H is the heaviest) and `H + X` already fit.

The boat count didn't change, so some optimal solution pairs `H` with `L`. And if `H + L` doesn't fit, nobody is lighter than `L`, so `H` can't pair with anyone and must ride alone.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
people.sort()
left, right = 0, len(people) - 1
boats = 0
```

Sort ascending so the lightest is at `left` and the heaviest at `right`. `boats` counts trips.
→ [list-methods](../syntax/list-methods.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [sorting-key](../syntax/sorting-key.md)

```python
while left <= right:
```

Keep going while anyone is unassigned. The `<=` matters: when `left == right` exactly one person remains and they still need a boat.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if people[left] + people[right] <= limit:
        left += 1
```

If the lightest fits with the heaviest, the lightest hops on too. Moving `left` right marks that person as taken.

```python
    right -= 1
    boats += 1
```

**Unconditionally**, the heaviest person leaves, whether alone or with a partner, and one boat is used. This is the line people forget: `right` moves in *both* cases.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return boats
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        left, right = 0, len(people) - 1
        boats = 0

        while left <= right:
            if people[left] + people[right] <= limit:
                left += 1
            right -= 1
            boats += 1

        return boats
```

</details>

**Trace it.** `people = [3, 2, 2, 1]`, `limit = 3`. Sorted: `[1, 2, 2, 3]`:

| `left` | `right` | Pair | Fits? | Action | `boats` |
|---|---|---|---|---|---|
| 0 (1) | 3 (3) | 1 + 3 = 4 | no | 3 goes alone | 1 |
| 0 (1) | 2 (2) | 1 + 2 = 3 | yes | 1 and 2 go together | 2 |
| 1 (2) | 1 (2) | 2 + 2 = 4 | no | last 2 goes alone | 3 |
| 1 | 0 | `left > right` | | stop | **3** ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n).** The sort dominates. The two-pointer loop is **O(n)**: every iteration moves `right` left by one, so it runs at most `n` times.

If you want to beat the sort, weights are bounded by `limit`, so a counting sort makes the whole thing O(n + limit).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra (O(n) for Python's sort)</summary>

The pointers and counter are O(1). Sorting in place with `list.sort()` uses up to O(n) auxiliary space inside Timsort. If you're asked, say "O(1) beyond the sort".

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each boat holds at most two people, so I want as many pairs as possible. Sort the weights. The heaviest person is the hardest to pair, and the lightest is their best chance. If those two fit, put them together. If they don't, nobody fits with the heaviest, so they go alone. Either way the heaviest leaves, so I move the right pointer every time and move the left pointer only when the pair fit. One boat per iteration. O(n log n) for the sort, O(n) for the scan."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is greedy correct?" | The exchange argument: swapping any partner for the lightest person never breaks a pair and never costs a boat |
| "What if a boat held *three* people?" | The greedy stops being optimal. It becomes a bin-packing problem (NP-hard in general) |
| "Faster than sorting?" | Counting sort over weights `1..limit`, then the same two pointers: O(n + limit) |
| "Weights can exceed the limit?" | Then some person can't ride at all. Check `max(people) <= limit` first |
| "Related problems?" | [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (converging pointers on a sorted array) · [Container With Most Water](11-container-with-most-water.md) |

**Traps:**

- **`while left < right`.** The last remaining person (when `left == right`) never gets a boat.
- **Moving `right` only when they pair.** The heaviest person leaves on *every* trip.
- **Forgetting to sort.** The pointers mean nothing on unsorted data.
- **Pairing greedy-from-the-front** (lightest with second-lightest). That wastes light people on light people and can use more boats.

**This same move shows up in:** [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) · [3Sum](15-3sum.md) · [Valid Palindrome](125-valid-palindrome.md) · [Squares of a Sorted Array](977-squares-of-a-sorted-array.md).

</details>

---
