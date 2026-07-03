# 15. Greedy — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

---

### 53. Maximum Subarray — Medium
[LeetCode](https://leetcode.com/problems/maximum-subarray/)  
[Solution file (no hints)](../../problems/0001-0499/53.py)

Find the contiguous subarray with the largest sum. Why does a running sum reset to 0 the moment it goes negative — what would carrying a negative sum forward ever gain you?

<details>
<summary>Hint</summary>

This is [Kadane's algorithm](../algorithms/kadane-algorithm.md): keep a running sum; if it ever drops below 0, reset it to 0, since a negative prefix can only hurt any subarray that follows it.
</details>

<details>
<summary>Solution</summary>

```python
best = nums[0]
current = 0

for num in nums:                         # for loop, one pass
    if current < 0:                         # a negative running sum only hurts what follows
        current = 0
    current += num
    best = max(best, current)

return best
```

Building blocks: [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — two running variables.
</details>

---

### 55. Jump Game — Medium
[LeetCode](https://leetcode.com/problems/jump-game/)  
Solution: not yet solved in this repo.

Given max-jump distances at each index, determine if you can reach the last index. Why does tracking only the farthest reachable index — rather than every possible path — settle this in one pass?

<details>
<summary>Hint</summary>

Greedily track `farthest` reachable so far. Walking left to right, if the current index ever exceeds `farthest`, you're stuck; otherwise extend `farthest` to `max(farthest, i + nums[i])`.
</details>

<details>
<summary>Solution</summary>

```python
farthest = 0

for i, num in enumerate(nums):            # for loop, one pass
    if i > farthest:                         # this index is unreachable
        return False
    farthest = max(farthest, i + num)

return True
```

Building blocks: [enumerate](../syntax/enumerate.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---

### 45. Jump Game II — Medium
[LeetCode](https://leetcode.com/problems/jump-game-ii/)  
Solution: not yet solved in this repo.

Same setup as [55](#55-jump-game--medium), but find the minimum number of jumps to reach the end. Why does tracking "the farthest reachable within the current jump" versus "the farthest reachable within the next jump" let you count jumps without simulating every path?

<details>
<summary>Hint</summary>

This is a greedy BFS-by-levels idea: track the boundary of the current jump's reach, and a running "farthest reachable" seen while scanning it. Once you scan past the current boundary, that's a new jump, and the boundary advances to the farthest seen.
</details>

<details>
<summary>Solution</summary>

```python
jumps = 0
current_end = 0                          # farthest reachable within the current jump
farthest = 0                              # farthest reachable seen so far

for i in range(len(nums) - 1):             # for loop, don't need to jump from the last index
    farthest = max(farthest, i + nums[i])

    if i == current_end:                     # exhausted this jump's range: take another jump
        jumps += 1
        current_end = farthest

return jumps
```

Building blocks: [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — a few running variables.
</details>

---

### 134. Gas Station — Medium
[LeetCode](https://leetcode.com/problems/gas-station/)  
Solution: not yet solved in this repo.

Find the starting gas station that lets you complete a full circuit (or -1 if none). Why does the first station where your running tank never goes negative, after any earlier attempt already failed, have to be the answer?

<details>
<summary>Hint</summary>

If the total gas is less than total cost, no solution exists. Otherwise greedily track a running tank total; whenever it goes negative, the current start is invalid, so reset the candidate start to the *next* station and reset the running tank — the total-gas check guarantees some start works.
</details>

<details>
<summary>Solution</summary>

```python
if sum(gas) < sum(cost):                 # not enough total gas: impossible
    return -1

total = 0
start = 0

for i in range(len(gas)):                  # for loop, one pass
    total += gas[i] - cost[i]
    if total < 0:                            # this start (and everything before i) can't work
        start = i + 1
        total = 0

return start
```

Building blocks: [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`sum()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the stations.
**Space: O(1)** — a couple of running variables.
</details>

---

### 846. Hand of Straights — Medium
[LeetCode](https://leetcode.com/problems/hand-of-straights/)  
Solution: not yet solved in this repo.

Determine if cards can be rearranged into groups of `groupSize` consecutive cards. Why must you always start a new group at the *smallest remaining* card?

<details>
<summary>Hint</summary>

Count card frequencies in a [hashmap](../data-structures/hashmap.md). Repeatedly take the smallest available card, and greedily consume one of each of the next `groupSize - 1` consecutive values to complete a group with it — if any is missing, it's impossible.
</details>

<details>
<summary>Solution</summary>

```python
from collections import Counter

if len(hand) % groupSize != 0:            # can't split evenly
    return False

count = Counter(hand)

for card in sorted(count):                 # always start a group at the smallest remaining card
    if count[card] == 0:                      # already fully consumed by an earlier group
        continue
    needed = count[card]                       # this many groups must start here
    for next_card in range(card, card + groupSize):   # consume groupSize consecutive values
        if count[next_card] < needed:              # can't complete the run
            return False
        count[next_card] -= needed

return True
```

Building blocks: [counter](../syntax/counter.md) · [sorting-key](../syntax/sorting-key.md) (`sorted()` on a dict) · [for-loop](../syntax/for-loop.md) (nested)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by sorting the distinct card values.
**Space: O(n)** — the frequency counter.
</details>

---

### 1899. Merge Triplets to Form Target Triplet — Medium
[LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)  
Solution: not yet solved in this repo.

Given triplets, determine if some subset can be merged (taking the max of each position) to form a target triplet. Why must you discard any triplet with a value exceeding the target in *any* position, no exceptions?

<details>
<summary>Hint</summary>

Any triplet with a component greater than the target's matching component can never be used — merging only takes maxes, so it would overshoot. Filter to only "safe" triplets, then check whether each target position is matched by at least one of them.
</details>

<details>
<summary>Solution</summary>

```python
good = set()

for t in triplets:                        # for loop over every triplet
    if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
        continue                             # this triplet would overshoot the target
    for i in range(3):
        if t[i] == target[i]:                  # this triplet nails one of the target's positions
            good.add(i)

return len(good) == 3                    # every target position was matched by some safe triplet
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass over the triplets.
**Space: O(1)** — the `good` set is capped at 3 elements.
</details>

---

### 763. Partition Labels — Medium
[LeetCode](https://leetcode.com/problems/partition-labels/)  
Solution: not yet solved in this repo.

Partition a string into as many parts as possible so each letter appears in only one part. Why must a partition's boundary be pushed out to the *last* occurrence of every letter seen inside it so far?

<details>
<summary>Hint</summary>

Precompute the last index of each character. Scan left to right, extending the current partition's `end` to the last occurrence of every character encountered; when you reach `end`, that partition is complete.
</details>

<details>
<summary>Solution</summary>

```python
last_index = {c: i for i, c in enumerate(s)}   # last occurrence of each character

res = []
start = end = 0

for i, c in enumerate(s):                 # for loop, one pass
    end = max(end, last_index[c])            # extend the partition to cover this char fully
    if i == end:                              # reached the boundary: partition is complete
        res.append(end - start + 1)
        start = i + 1

return res
```

Building blocks: [dict-comprehension](../syntax/dict-comprehension.md) · [enumerate](../syntax/enumerate.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes (building `last_index`, then scanning).
**Space: O(1)** — at most 26 lowercase letters in the hashmap.
</details>

---

### 678. Valid Parenthesis String — Medium
[LeetCode](https://leetcode.com/problems/valid-parenthesis-string/)  
Solution: not yet solved in this repo.

Determine if a string with `(`, `)`, and `*` (wildcard for `(`, `)`, or empty) can be valid parentheses. Why does tracking a *range* of possible open-parens counts, instead of one exact count, handle the wildcard's ambiguity?

<details>
<summary>Hint</summary>

Track `lo` (fewest possible open parens, treating `*` as `)` or empty when helpful) and `hi` (most possible open parens, treating `*` as `(`). If `hi` ever drops below 0, it's invalid; at the end, it's valid if `lo` can reach 0.
</details>

<details>
<summary>Solution</summary>

```python
lo, hi = 0, 0                            # range of possible "open paren" counts

for c in s:                                # for loop, one pass
    if c == "(":
        lo += 1
        hi += 1
    elif c == ")":
        lo -= 1
        hi -= 1
    else:                                    # '*' could be '(', ')', or empty
        lo -= 1
        hi += 1

    if hi < 0:                               # too many closes even in the best case
        return False
    lo = max(lo, 0)                          # can't have a negative "guaranteed open" count

return lo == 0
```

Building blocks: [for-loop](../syntax/for-loop.md) · [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the string.
**Space: O(1)** — two running variables.
</details>
