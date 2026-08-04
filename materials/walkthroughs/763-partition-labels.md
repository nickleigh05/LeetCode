# 763. Partition Labels

**Medium** · [LeetCode](https://leetcode.com/problems/partition-labels/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Partition a string into as many parts as possible so each letter appears in only one part. Why must a partition's boundary be pushed out to the *last* occurrence of every letter seen inside it so far?

<details>
<summary>Hint</summary>

Precompute the last index of each character. Scan left to right, extending the current partition's `end` to the last occurrence of every character encountered; when you reach `end`, that partition is complete.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def partitionLabels(self, s: str) -> List[int]:

        last_index = {char: i for i, char in enumerate(s)}

        result = []
        start = 0
        end = 0

        for i, char in enumerate(s):
            end = max(end, last_index[char])

            if i == end:
                result.append(end - start + 1)
                start = i + 1

        return result
```

Building blocks: [dict-comprehension](../syntax/dict-comprehension.md) · [enumerate](../syntax/enumerate.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes (building `last_index`, then scanning).
**Space: O(1)** — at most 26 lowercase letters in the hashmap.
</details>

---
