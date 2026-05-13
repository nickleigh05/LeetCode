# Sliding Window

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that push the same expand/shrink pattern into harder territory (permutation matching, window maximum). NeetCode 250 introduces binary-search-plus-window hybrids and fixed-window set tricks. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, identify whether the window is fixed or variable first, then find the matching pattern.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 121 | Easy | Best Time to Buy and Sell Stock | [Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | ☑ |
| 3 | Medium | Longest Substring Without Repeating Characters | [Link](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | ☑ |
| 424 | Medium | Longest Repeating Character Replacement | [Link](https://leetcode.com/problems/longest-repeating-character-replacement/) | ☑ |
| 76 | Hard | Minimum Window Substring | [Link](https://leetcode.com/problems/minimum-window-substring/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 567 | Medium | Permutation in String | [Link](https://leetcode.com/problems/permutation-in-string/) | ☐ |
| 239 | Hard | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 219 | Easy | Contains Duplicate II | [Link](https://leetcode.com/problems/contains-duplicate-ii/) | ☐ | Fixed-size window + set |
| 209 | Medium | Minimum Size Subarray Sum | [Link](https://leetcode.com/problems/minimum-size-subarray-sum/) | ☐ | Variable window shrink |
| 658 | Medium | Find K Closest Elements | [Link](https://leetcode.com/problems/find-k-closest-elements/) | ☐ | Binary search + window |

---

## Complexity Reference

| Pattern / Structure | Time | Space | Notes |
|---------------------|------|-------|-------|
| Fixed-size window (slide) | O(n) | O(1) or O(k) | Each element enters and exits exactly once |
| Variable window (expand/shrink) | O(n) | O(k) | Both l and r each move at most n steps total |
| Two-frequency-map (permutation) | O(n) | O(1) | Alphabet size is constant (26 chars) |
| Monotonic deque window max | O(n) | O(k) | Each index pushed/popped at most once |
| deque append / popleft | O(1) amortized | — | Both ends are O(1); random access is O(n) |
| Counter construction | O(n) | O(n) | One pass over the iterable |

---

## Data Structures

### Two-Index Window (left, right)

The window itself is just two integer indices into the array. No extra memory for the window boundaries — the real memory cost comes from whatever state you track inside the window (a hash map of counts, a deque of indices, etc.). The key invariant: at every point in the outer loop, the window `s[l:r+1]` satisfies the problem's constraint, or you shrink until it does.

```
Variable window — expand r, shrink l when violated:

s = [a, b, c, b, c, d]
      ↑           ↑
      l           r      window = s[l..r]

Step 1: r advances → window grows
Step 2: constraint violated → l advances until valid again
Step 3: record window size or update answer
```

**When it matters:** Any "subarray/substring satisfying X" problem. Fixed windows have k fixed; variable windows have a constraint that determines when to shrink.

### Hash Map (frequency tracking)

When the window's validity depends on character or element counts, a hash map tracks the count of each element currently inside the window. Adding an element increments its count; removing (sliding the left edge) decrements it. For permutation problems, you compare this "window map" to a "target map" — when they're equal, you have a valid window.

```
Target: "abc"   target_freq = {a:1, b:1, c:1}

Window sliding over "cbaebacd":
  window "cba" → freq = {c:1, b:1, a:1} → matches target ✓
  window "bae" → freq = {b:1, a:1, e:1} → no match ✗
```

**When it matters:** Permutation in String (#567), Minimum Window Substring (#76), Longest Repeating Character Replacement (#424).

### Monotonic Deque

A deque (double-ended queue) maintains a decreasing sequence of values (or their indices). When a new element comes in that is larger than the deque's back, pop the back — those smaller elements can never be the window maximum while the new larger element is in the window. The front of the deque always holds the index of the current window's maximum.

```
Array: [1, 3, -1, -3, 5, 3, 6, 7],  k=3

Window [1,3,-1]: deque indices → [1, 2]  (values 3, -1)  max = arr[1] = 3
Window [3,-1,-3]: deque indices → [1, 2, 3] (3,-1,-3)    max = arr[1] = 3
Window [-1,-3,5]: new 5 > all → deque → [4]              max = arr[4] = 5
```

**When it matters:** Sliding Window Maximum (#239). Any time you need O(1) running max/min inside a sliding window.

---

## Core Patterns

### Fixed-Size Window
**When to use:** The problem specifies a window of exactly k elements. Slide the window by removing the element leaving the left and adding the element entering the right.
**Complexity:** O(n) time, O(k) or O(1) space
**Problems:** Sliding Window Maximum (#239), Contains Duplicate II (#219), Permutation in String (#567)
**Common mistake:** Checking the answer before the window reaches size k. Start recording only when `r >= k - 1`.

```python
for r in range(len(nums)):
    # add nums[r] to window state
    if r >= k - 1:
        # window is full — record answer
        # remove nums[r - k + 1] from window state (element leaving)
        pass
```

### Variable Window (Expand/Shrink)
**When to use:** Find the longest or shortest subarray/substring where some constraint holds. Expand the right pointer freely; when the constraint breaks, shrink from the left until it's satisfied again.
**Complexity:** O(n) time (each pointer moves at most n steps), O(k) space for state
**Problems:** Longest Substring Without Repeating Characters (#3), Minimum Window Substring (#76), Minimum Size Subarray Sum (#209)
**Common mistake:** Shrinking with `if` instead of `while` — a single left-step may not restore the constraint; keep shrinking until it does.

```python
l = 0
state = {}  # or Counter, or set
for r in range(len(s)):
    # add s[r] to state
    while constraint_violated(state):
        # remove s[l] from state
        l += 1
    ans = max(ans, r - l + 1)  # or record minimum, etc.
```

### Two-Frequency-Map (Permutation / Anagram)
**When to use:** Check if a fixed-size window contains a permutation of a target string. Keep a target frequency map and a window frequency map; compare after every slide.
**Complexity:** O(n) time, O(1) space (26-char alphabet is constant)
**Problems:** Permutation in String (#567), Minimum Window Substring (#76)
**Common mistake:** Comparing the full Counter objects on every step — O(26) per step is fine, but forgetting to decrement the outgoing character before comparing causes off-by-one windows.

```python
from collections import Counter
need = Counter(s1)
window = Counter(s2[:len(s1)])
if window == need:
    return True
for i in range(len(s1), len(s2)):
    window[s2[i]] += 1                   # add incoming
    out = s2[i - len(s1)]
    window[out] -= 1
    if window[out] == 0:
        del window[out]                  # keep window clean — no zero-count keys
    if window == need:
        return True
```

### Deque Monotonic Window (Max/Min)
**When to use:** You need the maximum (or minimum) of every window of size k in O(n) total.
**Complexity:** O(n) time, O(k) space
**Problems:** Sliding Window Maximum (#239)
**Common mistake:** Forgetting to expire the front of the deque — check `dq[0] <= r - k` and pop it before reading the max.

```python
from collections import deque
dq = deque()   # stores indices, values in decreasing order
res = []
for r in range(len(nums)):
    while dq and nums[dq[-1]] < nums[r]:
        dq.pop()                         # back is smaller — useless while r is in window
    dq.append(r)
    if dq[0] <= r - k:                   # front is outside the window
        dq.popleft()
    if r >= k - 1:
        res.append(nums[dq[0]])          # front is always the window max
```

---

## Syntax Reference

### deque — double-ended queue

Use `deque` when you need O(1) append and popleft. Python `list.pop(0)` is O(n); `deque.popleft()` is O(1).

```python
from collections import deque

dq = deque()
dq.append(x)       # add to right — O(1)
dq.appendleft(x)   # add to left — O(1)
dq.pop()           # remove from right — O(1)
dq.popleft()       # remove from left — O(1)
dq[-1]             # peek right (newest) — O(1)
dq[0]              # peek left (oldest) — O(1)
```

### Counter for fixed-window frequency comparison

```python
from collections import Counter

need = Counter(s1)          # target frequency map — built once
window = Counter(s2[:k])    # initial window of size k

# slide: add incoming, remove outgoing
window[new_char] += 1
window[old_char] -= 1
if window[old_char] == 0:
    del window[old_char]    # delete zero-count keys so == comparison works cleanly

window == need              # True if same chars with same counts
```

### Variable window loop structure

```python
l = 0
for r in range(len(s)):
    # 1. expand: incorporate s[r] into state
    # 2. shrink: while constraint violated, remove s[l] and advance l
    # 3. record: update answer using current window [l, r]
```

### Tracking max frequency inside window (for #424)

```python
# Longest Repeating Character Replacement trick:
# window is valid if (window_size - max_freq) <= k
# You never need to decrease max_freq — only increase it.
# A smaller window will never be the answer, so just let it slide.

freq = {}
max_freq = 0
l = 0
for r in range(len(s)):
    freq[s[r]] = freq.get(s[r], 0) + 1
    max_freq = max(max_freq, freq[s[r]])    # max_freq only grows — intentional
    if (r - l + 1) - max_freq > k:
        freq[s[l]] -= 1
        l += 1
```

### Best time to buy and sell (single-variable sliding window)

```python
# Treat buy price as the "left" of the window — update it greedily.
min_price = float('inf')
max_profit = 0
for price in prices:
    min_price = min(min_price, price)        # best buy so far
    max_profit = max(max_profit, price - min_price)
```
