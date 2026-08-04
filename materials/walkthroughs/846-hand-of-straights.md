# 846. Hand of Straights

**Medium** · [LeetCode](https://leetcode.com/problems/hand-of-straights/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

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

Building blocks: [counter](../syntax/counter.md) · [sorting-key](../syntax/sorting-key.md) (`sorted()` on a dict) · [for-loop](../syntax/for-loop.md) (nested)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by sorting the distinct card values.
**Space: O(n)** — the frequency counter.
</details>

---
