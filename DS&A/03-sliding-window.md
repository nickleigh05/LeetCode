# Sliding Window

## What is Sliding Window?
The sliding window technique is used to perform operations on a specific window size of an array or string. The window "slides" through the data structure, expanding and contracting as needed.

## Types of Sliding Windows

### 1. Fixed Size Window
The window maintains a constant size as it moves:

```
Window size = 3

Initial position:
┌─────────────┐
│             ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
└──────────────┘
   window

After slide right:
        ┌─────────────┐
        │             ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
      └──────────────┘
         window

After another slide:
              ┌─────────────┐
              │             ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
            └──────────────┘
               window
```

### 2. Variable Size Window
The window expands and contracts based on conditions:

```
Expanding window:
L     R
↓     ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
└──────────┘

Window expands:
L           R
↓           ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
└────────────────────┘

Window contracts:
      L     R
      ↓     ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
└─────┴─────┴─────┴─────┴─────┴─────┘
      └──────────┘
```

## Fixed Size Window Problems

### Example 1: Maximum Sum of Subarray (size k)
```
arr = [2, 1, 5, 1, 3, 2], k = 3
Find maximum sum of any subarray of size 3

Step 1: Initialize first window
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  2  │  1  │  5  │  1  │  3  │  2  │
└─────┴─────┴─────┴─────┴─────┴─────┘
└──────────────┘
Sum = 2 + 1 + 5 = 8

Step 2: Slide window right
        Remove 2, Add 1
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  2  │  1  │  5  │  1  │  3  │  2  │
└─────┴─────┴─────┴─────┴─────┴─────┘
  ✗   └──────────────┘
              ✓
Sum = 8 - 2 + 1 = 7

Step 3: Slide window right
        Remove 1, Add 3
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  2  │  1  │  5  │  1  │  3  │  2  │
└─────┴─────┴─────┴─────┴─────┴─────┘
        ✗   └──────────────┘
                      ✓
Sum = 7 - 1 + 3 = 9

Step 4: Slide window right
        Remove 5, Add 2
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  2  │  1  │  5  │  1  │  3  │  2  │
└─────┴─────┴─────┴─────┴─────┴─────┘
              ✗   └──────────────┘
                            ✓
Sum = 9 - 5 + 2 = 6

Maximum sum = 9
```

### Template for Fixed Size Window
```python
def fixed_window(arr, k):
    # Initialize first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        # Remove leftmost element of previous window
        # Add rightmost element of new window
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum
```

## Variable Size Window Problems

### Example 2: Longest Substring Without Repeating Characters
```
s = "abcabcbb"

Step 1: Expand window
L,R
 ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
└─┘
length = 1, chars = {a}

Step 2: Expand
L   R
↓   ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
└─────┘
length = 2, chars = {a, b}

Step 3: Expand
L       R
↓       ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
└───────────┘
length = 3, chars = {a, b, c}

Step 4: Expand - found duplicate 'a'!
L           R
↓           ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
└───────────────┘
  ✗           ✓ (duplicate)

Step 5: Contract - remove 'a'
    L       R
    ↓       ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
✗   └───────────┘
length = 3, chars = {b, c, a}

Step 6: Expand
    L           R
    ↓           ↓
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ a │ b │ c │ a │ b │ c │ b │ b │
└───┴───┴───┴───┴───┴───┴───┴───┘
    └───────────────┘
    chars = {b, c, a, b} - duplicate!

Continue... max length = 3 ("abc")
```

### Example 3: Minimum Window Substring
```
s = "ADOBECODEBANC", t = "ABC"
Find minimum window containing all characters of t

Step 1: Expand until we have all chars
L                 R
↓                 ↓
A D O B E C O D E B A N C
└───────────────┘
Window: "ADOBEC" - has A, B, C ✓

Step 2: Contract from left while valid
      L           R
      ↓           ↓
A D O B E C O D E B A N C
      └─────────┘
Window: "BECODEB" - missing A ✗

Step back:
    L             R
    ↓             ↓
A D O B E C O D E B A N C
    └───────────┘
Window: "OECODEB" - missing A ✗

Step 3: Expand right to find valid window
    L                   R
    ↓                   ↓
A D O B E C O D E B A N C
    └─────────────────┘
Window: "OECODEBA" - has A, B, C ✓

Continue until smallest window found: "BANC"
```

### Template for Variable Size Window
```python
def variable_window(arr):
    left = 0
    result = 0
    window_state = {}  # Track window state

    for right in range(len(arr)):
        # Add arr[right] to window
        # Update window state

        # Contract window while condition is met
        while window_invalid:
            # Remove arr[left] from window
            # Update window state
            left += 1

        # Update result
        result = max(result, right - left + 1)

    return result
```

## Common Sliding Window Patterns

### Pattern 1: Maximum/Minimum Sum (Fixed Window)
```
Window size k = 3

┌───┬───┬───┬───┬───┬───┐
│ 1 │ 4 │ 2 │ 10│ 2 │ 3 │
└───┴───┴───┴───┴───┴───┘
└─────────┘ sum = 7

    └─────────┘ sum = 16 (max)

        └─────────┘ sum = 14

            └─────────┘ sum = 15
```

### Pattern 2: Longest Subarray with Condition
```
Find longest subarray with sum ≤ k

k = 8
┌───┬───┬───┬───┬───┬───┐
│ 3 │ 1 │ 2 │ 1 │ 1 │ 1 │
└───┴───┴───┴───┴───┴───┘

Expand:
L               R
↓               ↓
└───────────────┘ sum = 8 ✓
length = 4

Continue expanding:
L                   R
↓                   ↓
└───────────────────┘ sum = 9 > k ✗

Contract:
    L               R
    ↓               ↓
    └───────────────┘ sum = 6 ✓
```

### Pattern 3: Count Subarrays
```
Count subarrays with exactly k distinct elements

arr = [1, 2, 1, 2, 3], k = 2

Window with ≤ 2 distinct:
L           R
↓           ↓
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 1 │ 2 │ 3 │
└───┴───┴───┴───┴───┘
└───────────┘
Subarrays: [1], [1,2], [1,2,1], [1,2,1,2]
           [2], [2,1], [2,1,2]
           [1], [1,2]
           [2]
```

## Visualization: Maximum of All Subarrays of Size k

```
arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Step 1:
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ 1  │ 3  │ -1 │ -3 │ 5  │ 3  │ 6  │ 7  │
└────┴────┴────┴────┴────┴────┴────┴────┘
└──────────────┘
max = 3

Step 2:
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ 1  │ 3  │ -1 │ -3 │ 5  │ 3  │ 6  │ 7  │
└────┴────┴────┴────┴────┴────┴────┴────┘
      └──────────────┘
      max = 3

Step 3:
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ 1  │ 3  │ -1 │ -3 │ 5  │ 3  │ 6  │ 7  │
└────┴────┴────┴────┴────┴────┴────┴────┘
            └──────────────┘
            max = 5

Result: [3, 3, 5, 5, 6, 7]
```

## Optimization: Deque for Window Maximum

```
Use deque to maintain maximum in current window:

arr = [1, 3, -1, -3, 5], k = 3

Window: [1, 3, -1]
Deque: [3, -1] (decreasing order, store indices)
       Front is maximum

Window: [3, -1, -3]
Deque: [3, -1, -3]
       Front: 3 (max)

Window: [-1, -3, 5]
Deque: [5] (removed all smaller elements)
       Front: 5 (max)

Deque visualization:
┌──────────────────┐
│  Front  →  Back  │
│  (Max)     (Min) │
└──────────────────┘
│   3   │  -1  │    │
└──────────────────┘
```

## Time and Space Complexity

### Fixed Size Window
- **Time**: O(n) - single pass through array
- **Space**: O(1) - constant extra space

### Variable Size Window
- **Time**: O(n) - each element visited at most twice (by left and right)
- **Space**: O(k) - for storing window state, where k is window size or alphabet size

### With Deque (for max/min)
- **Time**: O(n) - each element added and removed at most once
- **Space**: O(k) - deque stores at most k elements

## Common Problems

### 1. Maximum Average Subarray
```
Find subarray of size k with maximum average

arr = [1, 12, -5, -6, 50, 3], k = 4

Window 1: [1, 12, -5, -6]
┌────┬────┬────┬────┬────┬────┐
│ 1  │ 12 │ -5 │ -6 │ 50 │ 3  │
└────┴────┴────┴────┴────┴────┘
└──────────────────┘
sum = 2, avg = 0.5

Window 2: [12, -5, -6, 50]
┌────┬────┬────┬────┬────┬────┐
│ 1  │ 12 │ -5 │ -6 │ 50 │ 3  │
└────┴────┴────┴────┴────┴────┘
      └──────────────────┘
sum = 51, avg = 12.75 (max)
```

### 2. Longest Repeating Character Replacement
```
s = "AABABBA", k = 1
(can replace k characters)

Window: "AAB"
L     R
↓     ↓
A A B A B B A
└─────┘
Most frequent: A (2)
Need to replace: 3 - 2 = 1 ✓

Window: "AABA"
L       R
↓       ↓
A A B A B B A
└─────────┘
Most frequent: A (3)
Need to replace: 4 - 3 = 1 ✓
```

### 3. Minimum Size Subarray Sum
```
arr = [2, 3, 1, 2, 4, 3], target = 7

Window expands:
L           R
↓           ↓
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 3 │ 1 │ 2 │ 4 │ 3 │
└───┴───┴───┴───┴───┴───┘
└───────────┘
sum = 6 < 7

Expand more:
L               R
↓               ↓
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 3 │ 1 │ 2 │ 4 │ 3 │
└───┴───┴───┴───┴───┴───┘
└───────────────┘
sum = 8 ≥ 7 ✓ length = 4

Contract:
    L           R
    ↓           ↓
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 3 │ 1 │ 2 │ 4 │ 3 │
└───┴───┴───┴───┴───┴───┘
    └───────────┘
sum = 6 < 7 (too small)

Continue... min length = 2 ([4, 3])
```

## Key Takeaways

1. **Fixed Window**:
   - Window size is constant
   - Add new element, remove old element
   - Single pass, O(n) time

2. **Variable Window**:
   - Window size changes dynamically
   - Expand until condition met
   - Contract to optimize
   - Two pointers (left and right)

3. **When to Use**:
   - Contiguous subarrays/substrings
   - Optimization problems (min/max)
   - Counting problems
   - Pattern matching

4. **Common Patterns**:
   - HashMap/Set for character tracking
   - Deque for max/min in window
   - Two pointers for window boundaries
   - Running sum/count for window state

5. **Optimization**:
   - O(n) instead of O(n²)
   - Avoid recalculating entire window
   - Incremental updates (add/remove one element)
