# 300. Longest Increasing Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Find the length of the longest strictly increasing subsequence. Why does maintaining a "tails" array — the smallest possible tail value for an increasing subsequence of each length — let binary search replace an O(n²) comparison?

<details>
<summary>Hint</summary>

Keep an array `tails` where `tails[k]` is the smallest tail value seen for a length-`k+1` increasing subsequence. For each number, [binary search](../algorithms/binary-search.md) `tails` for where it belongs, replacing that spot (or appending if it extends the longest sequence).
</details>

<details>
<summary>Solution</summary>

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:

        tails = []

        for num in nums:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num

        return len(tails)
```

Building blocks: [import-basics](../syntax/import-basics.md) (`import bisect`) · [for-loop](../syntax/for-loop.md) · [list-basics](../syntax/list-basics.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — n numbers, each doing a binary search over `tails`.
**Space: O(n)** — the `tails` array, up to length n.
</details>

---
