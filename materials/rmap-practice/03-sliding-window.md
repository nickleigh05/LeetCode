# 03. Sliding Window — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md)

---

### 121. Best Time to Buy and Sell Stock — Easy
[LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)  
[Solution file (no hints)](../../problems/0001-0499/121.py)

Given daily prices, find the max profit from one buy and one sell. As you scan once left to right, what's the only thing you need to remember about the past to know today's best possible profit?

<details>
<summary>Hint</summary>

Keep a window anchored at the cheapest price seen so far (see [Sliding Window](../learning/03-sliding-window.md)). At each day, the best profit is today's price minus that running minimum.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        left, right = 0, 1
        max_profit = 0

        while right < len(prices):
            if prices[right] < prices[left]:
                left = right
            else:
                max_profit = max(max_profit, prices[right] - prices[left])
            right += 1

        return max_profit
```

Building blocks: [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) (`left, right = 0, 1`) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the prices.
**Space: O(1)** — two running variables.
</details>

---

### 3. Longest Substring Without Repeating Characters — Medium
[LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/)  
[Solution file (no hints)](../../problems/0001-0499/3.py)

Find the length of the longest substring with no repeated characters. When you hit a character you've already seen inside your current window, what's the minimal shrink that fixes it?

<details>
<summary>Hint</summary>

Use a growing/shrinking window with a [hashset](../data-structures/hashset.md) of characters currently inside it (see [Sliding Window](../learning/03-sliding-window.md)). When the new character is already in the set, shrink from the left until the duplicate is gone.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        window = set()
        left = 0
        longest = 0

        for right in range(len(s)):
            while s[right] in window:
                window.remove(s[left])
                left += 1
            window.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md) · [set-operations](../syntax/set-operations.md) (`.remove()`, `.add()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each character enters and leaves the window at most once.
**Space: O(min(n, m))** — the hashset holds at most the size of the character set m or the string length n.
</details>

---

### 424. Longest Repeating Character Replacement — Medium
[LeetCode](https://leetcode.com/problems/longest-repeating-character-replacement/)  
[Solution file (no hints)](../../problems/0001-0499/424.py)

Given a string and a number of allowed character replacements `k`, find the longest substring you can turn into all-one-character. How do you know, from just a window's length and its most frequent character's count, whether `k` replacements are enough?

<details>
<summary>Hint</summary>

Keep a [hashmap](../data-structures/hashmap.md) of character counts inside the window (see [Sliding Window](../learning/03-sliding-window.md)). A window of length `L` is achievable if `L - max(count) <= k` — that's how many characters you'd need to replace.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:

        count = {}
        left = 0
        max_count = 0
        longest = 0

        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            max_count = max(max_count, count[s[right]])

            while (right - left + 1) - max_count > k:
                count[s[left]] -= 1
                left += 1

            longest = max(longest, right - left + 1)

        return longest
```

Building blocks: [dict-methods](../syntax/dict-methods.md) (`.get()`) · [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each character enters and leaves the window at most once.
**Space: O(1)** — at most 26 uppercase letters in the hashmap.
</details>

---

### 567. Permutation in String — Medium
[LeetCode](https://leetcode.com/problems/permutation-in-string/)  
[Solution file (no hints)](../../problems/0500-0999/567.py)

Given strings `s1` and `s2`, determine if any permutation of `s1` appears as a contiguous substring of `s2`. How can a fixed-size window of letter counts, matched against `s1`'s own letter counts, spot an anagram as it slides?

<details>
<summary>Hint</summary>

Keep a 26-length count array for `s1` and for a same-size sliding window over `s2` (see [Sliding Window](../learning/03-sliding-window.md)). If the two count arrays ever match exactly, that window is a permutation of `s1`.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1_count = [0] * 26
        window = [0] * 26

        for ch in s1:
            s1_count[ord(ch) - ord("a")] += 1

        for ch in s2[:len(s1)]:
            window[ord(ch) - ord("a")] += 1

        if s1_count == window:
            return True

        for right in range(len(s1), len(s2)):
            window[ord(s2[right]) - ord("a")] += 1
            window[ord(s2[right - len(s1)]) - ord("a")] -= 1

            if s1_count == window:
                return True

        return False
```

Building blocks: [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) · [list-slicing](../syntax/list-slicing.md) (`s2[:len(s1)]`) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (list equality)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — the window slides once across `s2` of length n, each step O(1) (fixed 26-length arrays).
**Space: O(1)** — two fixed 26-length arrays.
</details>

---

### 76. Minimum Window Substring — Hard
[LeetCode](https://leetcode.com/problems/minimum-window-substring/)  
Solution: not yet solved in this repo.

Given strings `s` and `t`, find the smallest window in `s` that contains every character of `t` (with multiplicity). How do you know a window is "valid" without rescanning it every time?

<details>
<summary>Hint</summary>

Keep a [hashmap](../data-structures/hashmap.md) of required counts from `t`, and a running count of how many *distinct* required characters are currently satisfied in the window (see [Sliding Window](../learning/03-sliding-window.md)). Expand right until valid, then shrink left while it stays valid, recording the smallest valid window.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:

        if not t:
            return ""

        need = {}
        for ch in t:
            need[ch] = need.get(ch, 0) + 1

        window = {}
        have = 0
        need_count = len(need)
        res = [-1, -1]
        res_len = float("inf")
        left = 0

        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1

            if ch in need and window[ch] == need[ch]:
                have += 1

            while have == need_count:
                if (right - left + 1) < res_len:
                    res = [left, right]
                    res_len = right - left + 1

                window[s[left]] -= 1
                if s[left] in need and window[s[left]] < need[s[left]]:
                    have -= 1
                left += 1

        left, right = res
        return s[left:right + 1] if res_len != float("inf") else ""
```

Building blocks: [dict-methods](../syntax/dict-methods.md) (`.get()`) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [membership-operators](../syntax/membership-operators.md) · [string-join-slice](../syntax/string-join-slice.md) · [ternary-expression](../syntax/ternary-expression.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n + m)** — n = len(s), m = len(t); each character in `s` is added and removed from the window at most once.
**Space: O(m)** — the `need` hashmap is bounded by the distinct characters in `t`.
</details>

---

### 239. Sliding Window Maximum — Hard
[LeetCode](https://leetcode.com/problems/sliding-window-maximum/)  
Solution: not yet solved in this repo.

Given an array and a window size `k`, return the max of each window as it slides across the array. How could a deque that only ever keeps *candidates for the max* avoid rescanning the whole window each time?

<details>
<summary>Hint</summary>

Keep a monotonically decreasing [deque](../data-structures/deque.md) of indices (see [Sliding Window](../learning/03-sliding-window.md)). Before pushing a new index, pop off any indices whose values are smaller — they can never be the max while the new, larger value is still in range. Pop from the front once the front index falls outside the window.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        queue = deque()
        result = []

        for i, num in enumerate(nums):
            while queue and nums[queue[-1]] < num:
                queue.pop()
            queue.append(i)

            if queue[0] <= i - k:
                queue.popleft()

            if i >= k - 1:
                result.append(nums[queue[0]])

        return result
```

Building blocks: [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each index is pushed and popped from the deque at most once.
**Space: O(k)** — the deque holds at most k indices.
</details>
