# 03. Sliding Window — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

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
min_price = float("inf")             # cheapest price seen so far
best = 0
for price in prices:                   # for loop, one pass
    min_price = min(min_price, price)    # update cheapest buy point
    best = max(best, price - min_price)  # profit if we sold today
return best
```

Building blocks: [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`min()`, `max()`) · [int-float-basics](../syntax/int-float-basics.md) (`float("inf")`)
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
window = set()                        # chars currently inside the window
l = 0
best = 0

for r in range(len(s)):                 # for loop expanding the right edge
    while s[r] in window:                  # shrink until the duplicate is removed
        window.remove(s[l])
        l += 1
    window.add(s[r])
    best = max(best, r - l + 1)             # current window size

return best
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
count = {}                            # char -> count inside window
l = 0
max_count = 0
best = 0

for r in range(len(s)):                 # for loop expanding the right edge
    count[s[r]] = count.get(s[r], 0) + 1
    max_count = max(max_count, count[s[r]])

    while (r - l + 1) - max_count > k:    # too many chars would need replacing
        count[s[l]] -= 1                    # shrink from the left
        l += 1

    best = max(best, r - l + 1)

return best
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
if len(s1) > len(s2):
    return False

s1_count = [0] * 26                  # letter counts for s1
window_count = [0] * 26              # letter counts for the current window

for i in range(len(s1)):               # for loop building initial counts
    s1_count[ord(s1[i]) - ord("a")] += 1
    window_count[ord(s2[i]) - ord("a")] += 1

if s1_count == window_count:           # check the first window
    return True

for i in range(len(s1), len(s2)):      # for loop sliding the window forward
    window_count[ord(s2[i]) - ord("a")] += 1              # add the new right char
    window_count[ord(s2[i - len(s1)]) - ord("a")] -= 1     # drop the old left char
    if s1_count == window_count:
        return True

return False
```

Building blocks: [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (list equality)
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
if not t:
    return ""

need = {}                             # required counts from t
for c in t:
    need[c] = need.get(c, 0) + 1

have = {}                              # counts currently in the window
have_count, need_count = 0, len(need)    # distinct chars satisfied vs required
res, res_len = [-1, -1], float("inf")
l = 0

for r, c in enumerate(s):               # for loop expanding the right edge
    have[c] = have.get(c, 0) + 1

    if c in need and have[c] == need[c]:   # this character just became satisfied
        have_count += 1

    while have_count == need_count:          # window is valid, try to shrink it
        if (r - l + 1) < res_len:              # record smallest valid window
            res = [l, r]
            res_len = r - l + 1
        have[s[l]] -= 1
        if s[l] in need and have[s[l]] < need[s[l]]:  # shrinking broke validity
            have_count -= 1
        l += 1

l, r = res
return s[l:r + 1] if res_len != float("inf") else ""
```

Building blocks: [dict-methods](../syntax/dict-methods.md) (`.get()`) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [membership-operators](../syntax/membership-operators.md) · [string-join-slice](../syntax/string-join-slice.md)
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

dq = deque()                          # stores indices, values decreasing
res = []

for i, num in enumerate(nums):          # for loop over the array
    while dq and nums[dq[-1]] < num:      # drop smaller values from the back
        dq.pop()
    dq.append(i)

    if dq[0] <= i - k:                    # front index fell out of the window
        dq.popleft()

    if i >= k - 1:                        # window is fully formed
        res.append(nums[dq[0]])             # front of deque is the current max

return res
```

Building blocks: [deque](../data-structures/deque.md) · [enumerate](../syntax/enumerate.md) · [while-loop](../syntax/while-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each index is pushed and popped from the deque at most once.
**Space: O(k)** — the deque holds at most k indices.
</details>
