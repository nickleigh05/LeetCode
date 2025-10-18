# Binary Search

## What is Binary Search?
Binary search is an efficient algorithm for finding a target value in a **sorted array** by repeatedly dividing the search interval in half.

Think of it like finding a word in a dictionary - you don't start from page 1, you open somewhere in the middle and decide which half to search next.

## Visual Representation

```
Search for 7 in: [1, 3, 5, 7, 9, 11, 13, 15]

Step 1: Check middle
L                 M                  R
↓                 ↓                  ↓
┌───┬───┬───┬───┬───┬────┬────┬────┐
│ 1 │ 3 │ 5 │ 7 │ 9 │ 11 │ 13 │ 15 │
└───┴───┴───┴───┴───┴────┴────┴────┘
                  9 > 7
                  Search left half ←

Step 2: Check middle of left half
L       M         R
↓       ↓         ↓
┌───┬───┬───┬───┐
│ 1 │ 3 │ 5 │ 7 │
└───┴───┴───┴───┘
        5 < 7
        Search right half →

Step 3: Check middle of right half
        L   M   R
        ↓   ↓   ↓
        ┌───┬───┐
        │ 7 │ 7 │
        └───┴───┘
        Found! ✓
```

## How Binary Search Works

### The Process
```
Array: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
Target: 23

Iteration 1:
L                       M                       R
↓                       ↓                       ↓
┌───┬───┬───┬───┬────┬────┬────┬────┬────┬────┐
│ 2 │ 5 │ 8 │12 │ 16 │ 23 │ 38 │ 56 │ 72 │ 91 │
└───┴───┴───┴───┴────┴────┴────┴────┴────┴────┘
                      mid = 16
                      16 < 23, search right →

Iteration 2:
                        L    M         R
                        ↓    ↓         ↓
                      ┌────┬────┬────┬────┬────┐
                      │ 23 │ 38 │ 56 │ 72 │ 91 │
                      └────┴────┴────┴────┴────┘
                            mid = 56
                            56 > 23, search left ←

Iteration 3:
                        L,M,R
                          ↓
                        ┌────┐
                        │ 23 │
                        └────┘
                        Found! ✓
```

## Binary Search Template

### Basic Template
```python
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if arr[mid] == target:
            return mid  # Found
        elif arr[mid] < target:
            left = mid + 1  # Search right
        else:
            right = mid - 1  # Search left

    return -1  # Not found
```

### Visualization of Mid Calculation
```
Why use: mid = left + (right - left) // 2
Instead of: mid = (left + right) // 2

Example: left = 1000000000, right = 1000000000
(left + right) might overflow in some languages

Safe calculation:
left = 5, right = 10
mid = 5 + (10 - 5) // 2
    = 5 + 5 // 2
    = 5 + 2
    = 7

Visual:
L           M           R
↓           ↓           ↓
5     6     7     8     9     10
```

## Variants of Binary Search

### 1. Find First Occurrence
```
arr = [1, 2, 2, 2, 3, 4, 5], target = 2

Standard binary search might return any 2:
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┴───┴───┘
      ↑   ↑   ↑
    Could return any of these

Find FIRST occurrence:
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┴───┴───┘
      ↑
    Return index 1

Algorithm: When found, continue searching left
L       M       R
↓       ↓       ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┴───┴───┘
        Found 2, but continue left
        right = mid - 1
```

### 2. Find Last Occurrence
```
arr = [1, 2, 2, 2, 3, 4, 5], target = 2

Find LAST occurrence:
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┴───┴───┘
              ↑
        Return index 3

Algorithm: When found, continue searching right
L       M       R
↓       ↓       ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┴───┴───┘
        Found 2, but continue right
        left = mid + 1
```

### 3. Find Insert Position
```
arr = [1, 3, 5, 6], target = 4

Find position where 4 should be inserted:

Step 1:
L       M       R
↓       ↓       ↓
┌───┬───┬───┬───┐
│ 1 │ 3 │ 5 │ 6 │
└───┴───┴───┴───┘
        5 > 4, search left

Step 2:
L   M   R
↓   ↓   ↓
┌───┬───┐
│ 1 │ 3 │
└───┴───┘
    3 < 4, search right

Step 3:
        L,R
        ↓
┌───┬───┬───┬───┐
│ 1 │ 3 │ 5 │ 6 │
└───┴───┴───┴───┘
        ↑
    Insert at index 2

Result: [1, 3, 4, 5, 6]
```

## Binary Search on Answer

Sometimes we binary search on the **answer space** rather than array indices.

### Example: Square Root
```
Find sqrt(8) (integer part)

Answer space: [0, 1, 2, 3, 4, 5, 6, 7, 8]

Step 1: Check mid = 4
        L           M           R
        ↓           ↓           ↓
Answer: 0  1  2  3  4  5  6  7  8
                    4² = 16 > 8
                    Search left ←

Step 2: Check mid = 2
        L   M   R
        ↓   ↓   ↓
Answer: 0  1  2  3  4
            2² = 4 < 8
            Search right →

Step 3: Check mid = 3
               L,M,R
                ↓
Answer: 0  1  2  3  4
                3² = 9 > 8
                Search left ←

Step 4: L > R, return right = 2
        2² = 4 ≤ 8 ✓
```

### Example: Koko Eating Bananas
```
piles = [3, 6, 7, 11], h = 8
Find minimum eating speed k

Answer space: k can be 1 to max(piles) = 11

Eating speed k = 6:
Hour 1: Eat 3 (pile 1 done)      ┌───┐
Hour 2: Eat 6 (pile 2 done)      │ 3 │ Done in 1 hr
Hour 3: Eat 6 (pile 3 done)      ├───┤
Hour 4: Eat 1 (pile 3 done)      │ 6 │ Done in 1 hr
Hour 5: Eat 6 (pile 4)           ├───┤
Hour 6: Eat 5 (pile 4 done)      │ 7 │ Done in 2 hrs (6+1)
                                 ├───┤
Total: 6 hours ≤ 8 ✓             │11 │ Done in 2 hrs (6+5)
                                 └───┘

Try smaller k:
        L       M       R
        ↓       ↓       ↓
Speed:  1  2  3  4  5  6  7  8  9  10  11
                    Check k=6
                    Works! Try smaller →
```

## Rotated Array Search

### Search in Rotated Sorted Array
```
arr = [4, 5, 6, 7, 0, 1, 2], target = 0

Original: [0, 1, 2, 4, 5, 6, 7]
Rotated at index 4

Step 1: Find which half is sorted
L           M           R
↓           ↓           ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 4 │ 5 │ 6 │ 7 │ 0 │ 1 │ 2 │
└───┴───┴───┴───┴───┴───┴───┘
Left half [4,5,6,7] is sorted
Right half [0,1,2] is also sorted

7 > 4 → left half is sorted
target = 0 not in [4,7]
Search right half →

Step 2:
                L   M   R
                ↓   ↓   ↓
                ┌───┬───┬───┐
                │ 0 │ 1 │ 2 │
                └───┴───┴───┘
                Found 0! ✓
```

### Find Minimum in Rotated Array
```
arr = [4, 5, 6, 7, 0, 1, 2]

Visual:
        7
      6
    5
  4
                2
              1
            0

Minimum is at the "break point"

Step 1:
L           M           R
↓           ↓           ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 4 │ 5 │ 6 │ 7 │ 0 │ 1 │ 2 │
└───┴───┴───┴───┴───┴───┴───┘
arr[M]=7 > arr[R]=2
Minimum is in right half →

Step 2:
                L   M   R
                ↓   ↓   ↓
                ┌───┬───┬───┐
                │ 0 │ 1 │ 2 │
                └───┴───┴───┘
                arr[M]=1 < arr[R]=2
                Minimum is in left half ←

Step 3:
                L,M,R
                  ↓
                ┌───┐
                │ 0 │
                └───┘
                Found minimum! ✓
```

## Peak Finding

### Find Peak Element
```
arr = [1, 2, 3, 1]

A peak is an element greater than its neighbors

Visual:
    3
  2
1       1

Step 1:
L       M       R
↓       ↓       ↓
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 1 │
└───┴───┴───┴───┘
arr[M]=2 < arr[M+1]=3
Peak is to the right →

Step 2:
        L   M,R
        ↓   ↓
        ┌───┬───┐
        │ 3 │ 1 │
        └───┴───┘
        arr[M]=3 > arr[M+1]=1
        3 is a peak! ✓
```

## Binary Search in 2D

### Search 2D Matrix
```
matrix = [
  [1,  3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 60]
]
target = 3

Treat as 1D array:
Index:  0  1  2  3  4  5  6  7  8  9  10 11
Value:  1  3  5  7 10 11 16 20 23 30 34 60

Binary search on virtual 1D array:
Convert index to 2D:
  row = index // cols
  col = index % cols

Step 1: mid = 5
┌───┬───┬───┬────┐
│ 1 │ 3 │ 5 │  7 │
├───┼───┼───┼────┤
│10 │11 │16 │ 20 │  mid[5] = 11
├───┼───┼───┼────┤
│23 │30 │34 │ 60 │
└───┴───┴───┴────┘
     ↑
   row=1, col=1: value=11 > 3
   Search left ←

Step 2: mid = 1
┌───┬───┬───┬────┐
│ 1 │ 3 │ 5 │  7 │  mid[1] = 3
├───┼───┼───┼────┤         ↑
│10 │11 │16 │ 20 │  Found! ✓
├───┼───┼───┼────┤
│23 │30 │34 │ 60 │
└───┴───┴───┴────┘
```

## Time and Space Complexity

### Time Complexity
- **Best Case**: O(1) - target is at middle
- **Average Case**: O(log n)
- **Worst Case**: O(log n)

### Space Complexity
- **Iterative**: O(1)
- **Recursive**: O(log n) - recursion stack

### Comparison with Linear Search
```
Array size: 1,000,000

Linear Search:
Worst case: 1,000,000 comparisons
┌─┬─┬─┬─┬─┬...┬─┬─┬─┐
│ │ │ │ │ │...│ │ │X│
└─┴─┴─┴─┴─┴...┴─┴─┴─┘
                    ↑ Found after checking all

Binary Search:
Worst case: log₂(1,000,000) ≈ 20 comparisons

Iteration 1: 1,000,000 elements
Iteration 2: 500,000 elements
Iteration 3: 250,000 elements
...
Iteration 20: 1 element ✓
```

## Common Pitfalls

### 1. Off-by-One Errors
```
Wrong: while left < right vs while left <= right

arr = [1, 2, 3], target = 3

Using left < right:
L       M   R
↓       ↓   ↓
┌───┬───┬───┐
│ 1 │ 2 │ 3 │
└───┴───┴───┘
        L,R
        ↓
        ┌───┐
        │ 3 │
        └───┘
Loop exits! Missed target ✗

Using left <= right:
Checks when L == R, finds target ✓
```

### 2. Infinite Loop
```
Wrong mid calculation when left = mid:

left = 0, right = 1
mid = (0 + 1) // 2 = 0

If we do: left = mid
Then left = 0 (no progress) → Infinite loop!

Fix: left = mid + 1
```

## Python Implementation

```python
# Basic binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Find first occurrence
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

# Binary search on answer
def binary_search_answer(low, high, is_valid):
    result = -1

    while low <= high:
        mid = low + (high - low) // 2

        if is_valid(mid):
            result = mid
            high = mid - 1  # Try to find smaller
        else:
            low = mid + 1

    return result
```

## Key Takeaways

1. **Requirements**:
   - Array must be sorted (or rotated sorted)
   - Random access to elements

2. **Time Complexity**: O(log n)
   - Halves search space each iteration
   - Extremely efficient for large datasets

3. **Common Patterns**:
   - Search in sorted array
   - Find first/last occurrence
   - Search in rotated array
   - Binary search on answer space
   - Peak finding

4. **When to Use**:
   - Sorted data
   - Need O(log n) search
   - Finding boundaries
   - Optimization problems (min/max)

5. **Variants**:
   - Lower bound (first >= target)
   - Upper bound (first > target)
   - Search in 2D matrix
   - Ternary search (for unimodal functions)
