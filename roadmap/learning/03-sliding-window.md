# 03. Sliding Window
*A moving boundary over contiguous ranges — O(n) where brute force is O(n²).*

[← Prev](02-two-pointers.md) · [🗺 Roadmap](../roadmap.md) · [Next →](04-stack.md)

---

> **Builds on:** arrays and the two-pointer mindset from [Lessons 01–02](02-two-pointers.md). A sliding window *is* two pointers moving the same direction.

When a problem asks about a **contiguous subarray or substring** — longest, shortest, max sum, "at most k" — you almost never need to re-examine elements. Grow a window from the right, shrink it from the left when it breaks a constraint, and every element enters and leaves at most once. That's the whole O(n) magic.

## The Pattern

### Sliding Window

```
  Find longest substring without repeating chars: "abcabcbb"

  Fixed window of size 3? → use fixed template
  Variable window:

  "a b c a b c b b"
   0 1 2 3 4 5 6 7

  left=0, right=0, window={}
  Add 'a': {a:1}         window="a"    len=1
  Add 'b': {a:1,b:1}     window="ab"   len=2
  Add 'c': {a:1,b:1,c:1} window="abc"  len=3
  Add 'a': a already in window!
    → shrink: remove arr[left]='a', left=1
    → now window="bc", add 'a': {b:1,c:1,a:1}  len=3
  Add 'b': b in window!
    → shrink: remove 'b', left=2
    → window="ca", add 'b': {c:1,a:1,b:1}  len=3
  ...
  Max = 3 ("abc")

  Fixed window (size k):
  [1,3,-1,-3,5,3,6,7]  k=3
  ┌───────┐
  │1  3 -1│-3  5  3  6  7   → max = 3
     ┌───────┐
      1│ 3 -1 -3│ 5  3  6  7  → max = 3
```

**What it is:** Maintain a "window" (contiguous subarray or substring) that expands or contracts to satisfy a condition. Avoids O(n²) by never re-scanning elements — each element enters and exits the window at most once.

**Two flavors:**
- **Fixed size k**: window is always exactly k elements; slide by one each step
- **Variable size**: expand right pointer, shrink left when constraint violated

**Use this when:**
- [ ] "Longest/shortest subarray/substring with constraint X"
- [ ] "Maximum sum subarray of size k"
- [ ] "Minimum window containing all characters"
- [ ] Contiguous elements, no gaps
- [ ] Constraint is about the window contents (sum, count, unique chars)

**Python:**
```python
# Fixed-size window: max sum subarray of length k
def max_sum_k(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # slide: add right, remove left
        best = max(best, window_sum)
    return best

# Variable-size window: longest substring with at most k distinct chars
def longest_k_distinct(s, k):
    freq = {}
    left = best = 0
    for right, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1
        while len(freq) > k:              # violated → shrink
            left_ch = s[left]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            left += 1
        best = max(best, right - left + 1)
    return best

# Minimum window substring (hard variant)
from collections import Counter
def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = best_left = best_right = 0
    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:                  # valid window found
            while need[s[left]] < 0:     # shrink from left
                need[s[left]] += 1
                left += 1
            if not best_right or right - left < best_right - best_left:
                best_left, best_right = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[best_left:best_right]
```

**Complexity:** O(n) — each element is added and removed from the window at most once.

**Blind 75 examples:** Best Time to Buy and Sell Stock · Longest Substring Without Repeating Characters · Minimum Window Substring · Longest Repeating Character Replacement

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/sliding-window/`](../appendix/templates/sliding-window/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/sliding-window/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Sliding Window problems →**](../../lists/recommended.md#3-sliding-window-14-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Stacks, Queues & Monotonic Stacks](04-stack.md) — lIFO for "most recent unresolved"; a monotonic stack answers next-greater questions in one pass.

[← Prev](02-two-pointers.md) · [🗺 Roadmap](../roadmap.md) · [Next →](04-stack.md)

