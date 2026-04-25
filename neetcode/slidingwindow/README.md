# Sliding Window

## 3. Sliding Window (6 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 121 | Easy | Best Time to Buy and Sell Stock | [Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) |
| 3 | Medium | Longest Substring Without Repeating Characters | [Link](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |
| 424 | Medium | Longest Repeating Character Replacement | [Link](https://leetcode.com/problems/longest-repeating-character-replacement/) |
| 567 | Medium | Permutation in String | [Link](https://leetcode.com/problems/permutation-in-string/) |
| 76 | Hard | Minimum Window Substring | [Link](https://leetcode.com/problems/minimum-window-substring/) |
| 239 | Hard | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) |

---

## Data Structures

### Array / String with Two Pointers
The window is defined by a `left` and `right` pointer on the same array or string. You expand the right side and shrink the left side to maintain a valid window.

### Hash Map (Frequency Map)
Used to track character counts inside the window. Lets you check in O(1) whether the current window satisfies a condition (e.g. contains all required characters).

### Monotonic Deque
A double-ended queue that maintains elements in sorted order (usually decreasing). Used when you need the max or min of the current window in O(1). Elements that can never be the answer are discarded from the back. Used in Sliding Window Maximum.

---

## Core Patterns

### Fixed-Size Window
The window size `k` is given. Slide it one step at a time: add the new right element, remove the old left element, update your answer. Used in Sliding Window Maximum.

### Dynamic Window (Expand and Shrink)
Expand `right` to include new elements. When the window becomes invalid (violates a constraint), advance `left` until it's valid again. Keep track of the best valid window seen. Used in Longest Substring Without Repeating Characters, Minimum Window Substring.

### Character Frequency + Have/Need Count
Maintain a freq map of what's in the window and compare against what's needed. Track a `have` counter that increments when a character's count in the window matches the required count — this avoids scanning the whole map each step. Used in Permutation in String, Minimum Window Substring.

### Longest Valid Window Trick
For "longest substring where at most K replacements are allowed": the window is valid when `window_size - max_freq_char <= k`. When invalid, slide `left` by 1 (don't shrink — you only care about growing). Used in Longest Repeating Character Replacement.

### Running Min/Max
Track a running minimum (or maximum) as you scan. The profit at each day is `price - running_min`. No actual sliding window needed — it's a single-pass scan. Used in Best Time to Buy and Sell Stock.
