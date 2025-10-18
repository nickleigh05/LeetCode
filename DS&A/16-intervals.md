# Intervals

## What are Interval Problems?
Interval problems involve ranges or periods, typically represented as [start, end]. Common tasks include merging overlapping intervals, finding conflicts, inserting new intervals, and scheduling.

## Core Concepts

### Interval Representation

```
Interval: [start, end]

Visual:
    0  1  2  3  4  5  6  7  8  9
    |──────|                        [0, 3]
          |────────|                [2, 6]
                   |──────|         [5, 8]

Relationships:
1. Overlapping:
   [1, 5] and [3, 7]
    |────|
       |────|
       ^^^^ overlap

2. Disjoint:
   [1, 3] and [5, 7]
    |──|    |──|
    No overlap

3. Contained:
   [1, 7] contains [3, 5]
    |────────|
       |──|

4. Adjacent:
   [1, 3] and [3, 5]
    |──|──|
    Can merge to [1, 5]
```

### Common Operations

```
1. Overlap check:
   interval1.end > interval2.start AND
   interval2.end > interval1.start

2. Merge:
   [1, 4] + [3, 6] = [1, 6]
   new_start = min(start1, start2)
   new_end = max(end1, end2)

3. Sort intervals:
   Usually by start time
   [(3,5), (1,4), (6,8)] → [(1,4), (3,5), (6,8)]

4. Point in interval:
   point ≥ start AND point ≤ end
```

## Classic Interval Problems

### 1. Merge Intervals

```
Problem: Merge overlapping intervals
intervals = [[1,3],[2,6],[8,10],[15,18]]

Step 1: Sort by start time
    [[1,3],[2,6],[8,10],[15,18]]
    Already sorted

Step 2: Merge overlaps

Visual:
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
    ═══════════════════
    [1,3]
       ═══════════════════════
       [2,6]
                               ═══════════
                               [8,10]
                                                    ═══════════════
                                                    [15,18]

Merge [1,3] and [2,6]:
    Overlap: 3 ≥ 2 ✓
    Merged: [1, max(3,6)] = [1,6]

    ═══════════════════════
    [1,6]

Check [1,6] and [8,10]:
    No overlap: 6 < 8
    Keep separate

Check [8,10] and [15,18]:
    No overlap: 10 < 15
    Keep separate

Result: [[1,6],[8,10],[15,18]]

Visual result:
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
    ═══════════════════════
    [1,6]
                               ═══════════
                               [8,10]
                                                    ═══════════════
                                                    [15,18]

Algorithm:
merged = [intervals[0]]
for interval in intervals[1:]:
    if merged[-1][1] >= interval[0]:
        merged[-1][1] = max(merged[-1][1], interval[1])
    else:
        merged.append(interval)

Time: O(n log n) for sorting
Space: O(n)
```

### 2. Insert Interval

```
Problem: Insert new interval and merge
intervals = [[1,3],[6,9]]
newInterval = [2,5]

Step 1: Find position
    [1,3] [6,9]
        ^
    Insert [2,5] here

Step 2: Merge overlaps

Before:
    0  1  2  3  4  5  6  7  8  9
    ═══════
    [1,3]
                   ═══════════
                   [6,9]

Insert [2,5]:
       ═══════════
       [2,5]

After merge:
    0  1  2  3  4  5  6  7  8  9
    ═══════════════
    [1,5]
                   ═══════════
                   [6,9]

Three parts:
1. Before new interval (no overlap)
   [1,3] overlaps with [2,5]

2. Merge overlapping
   [1,3] + [2,5] = [1,5]

3. After new interval (no overlap)
   [6,9] doesn't overlap

Result: [[1,5],[6,9]]

Example 2:
intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]
newInterval = [4,8]

Visual:
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
    ═══
    [1,2]
          ═══════
          [3,5]
                   ═══
                   [6,7]
                         ═══════
                         [8,10]
                                        ═══════════════
                                        [12,16]

Insert [4,8]:
                ═══════════
                [4,8]

Overlaps with [3,5], [6,7], [8,10]
Merge: [3,10]

Result:
    ═══
    [1,2]
          ═══════════════════
          [3,10]
                                        ═══════════════
                                        [12,16]

[[1,2],[3,10],[12,16]]

Time: O(n)
Space: O(n)
```

### 3. Non-Overlapping Intervals

```
Problem: Minimum removals to make non-overlapping
intervals = [[1,2],[2,3],[3,4],[1,3]]

Sort by end time:
[[1,2],[2,3],[1,3],[3,4]]

Greedy: Keep interval with earliest end

Visual:
    0  1  2  3  4
    ═══
    [1,2]
       ═══
       [2,3]
    ═══════
    [1,3]    ← Remove (conflicts with [1,2])
          ═══
          [3,4]

Step 1: Keep [1,2]
    end = 2

Step 2: [2,3] starts at 2 ≥ end
    Keep [2,3]
    end = 3

Step 3: [1,3] starts at 1 < end (2)
    Remove [1,3]
    count = 1

Step 4: [3,4] starts at 3 ≥ end
    Keep [3,4]

Result: Remove 1 interval

Final intervals:
    0  1  2  3  4
    ═══
    [1,2]
       ═══
       [2,3]
          ═══
          [3,4]

Time: O(n log n)
Space: O(1)
```

### 4. Meeting Rooms

```
Problem 1: Can attend all meetings?
intervals = [[0,30],[5,10],[15,20]]

Sort by start:
[[0,30],[5,10],[15,20]]

Visual:
    0    5    10   15   20   25   30
    |─────────────────────────────|
         |────|
              |────|

Check overlaps:
[0,30] and [5,10]: 30 > 5 → overlap ✗

Answer: False (cannot attend all)

Problem 2: Minimum meeting rooms needed
Same intervals

Sort by start:
[[0,30],[5,10],[15,20]]

Use min heap for end times:

Step 1: [0,30]
    heap = [30]
    rooms = 1

    Room 1: |─────────────────────────────|

Step 2: [5,10]
    5 < 30 (conflict)
    heap = [10, 30]
    rooms = 2

    Room 1: |─────────────────────────────|
    Room 2:      |────|

Step 3: [15,20]
    15 > 10 (room freed)
    Pop 10, push 20
    heap = [20, 30]
    rooms = 2 (max)

    Room 1: |─────────────────────────────|
    Room 2:      |────|     |────|

Answer: 2 rooms needed

Time: O(n log n)
Space: O(n)
```

### 5. Interval List Intersections

```
Problem: Find intersections of two interval lists
A = [[0,2],[5,10],[13,23],[24,25]]
B = [[1,5],[8,12],[15,24],[25,26]]

Two pointers approach:

Visual:
    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 ... 23 24 25 26
A:  ═══════
              ═══════════════
                                        ═══════════════════════
                                                                ═══
B:     ═══════════
                      ═══════════════
                                           ═══════════════════════
                                                                   ═══

Step 1: A[0]=[0,2], B[0]=[1,5]
    Overlap: [max(0,1), min(2,5)] = [1,2]

    Result: [[1,2]]

    0  1  2
    ═══════
       ═══
       intersection

Step 2: A[1]=[5,10], B[0]=[1,5]
    Overlap: [max(5,1), min(10,5)] = [5,5]

    Result: [[1,2],[5,5]]

Step 3: A[1]=[5,10], B[1]=[8,12]
    Overlap: [max(5,8), min(10,12)] = [8,10]

    Result: [[1,2],[5,5],[8,10]]

Continue for all pairs...

Final result:
[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]

Algorithm:
i = j = 0
while i < len(A) and j < len(B):
    start = max(A[i][0], B[j][0])
    end = min(A[i][1], B[j][1])

    if start <= end:
        result.append([start, end])

    if A[i][1] < B[j][1]:
        i += 1
    else:
        j += 1

Time: O(n + m)
Space: O(1)
```

### 6. Employee Free Time

```
Problem: Common free time across all employees
schedule = [
    [[1,3],[4,6]],  # Employee 1
    [[2,4]],        # Employee 2
    [[2,5],[7,9]]   # Employee 3
]

Flatten and sort:
[[1,3],[2,4],[2,5],[4,6],[7,9]]

Merge busy intervals:
    0  1  2  3  4  5  6  7  8  9
    ═══════                        [1,3]
       ═══════                     [2,4]
       ═══════════                 [2,5]
             ═══════               [4,6]
                         ═══════   [7,9]

After merge:
    0  1  2  3  4  5  6  7  8  9
    ═══════════════               [1,6]
                         ═══════   [7,9]

Free time = gaps between busy intervals:
    0  1  2  3  4  5  6  7  8  9
    ═══════════════               Busy
                   ███             Free [6,7]
                         ═══════   Busy

Result: [[6,7]]

Time: O(n log n)
Space: O(n)
```

### 7. My Calendar

```
Problem: Book events without double booking

Approach 1: Simple list
calendar = []

Book [10, 20]:
    calendar = [[10, 20]]

    10 11 12 13 14 15 16 17 18 19 20
    ═══════════════════════════════

Book [15, 25]:
    Check overlap with [10, 20]
    15 < 20 → overlaps ✗

Book [20, 30]:
    Check overlap with [10, 20]
    20 ≥ 20 → no overlap ✓
    calendar = [[10, 20], [20, 30]]

    10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
    ══════════════════════════════════════════════════════════════

Approach 2: Balanced BST (TreeMap)
Store start → end mappings

Book [10, 20]:
    tree = {10: 20}

Book [20, 30]:
    Check floor: 10 → ends at 20 ≤ 20 ✓
    tree = {10: 20, 20: 30}

Book [15, 25]:
    Check floor: 10 → ends at 20 > 15 ✗

Time: O(n) simple, O(log n) BST
Space: O(n)
```

## Interval Patterns

### Pattern 1: Sort by Start
```
Use when:
- Merging intervals
- Finding gaps
- Sequential processing

Example: Merge intervals
```

### Pattern 2: Sort by End
```
Use when:
- Greedy scheduling
- Maximum non-overlapping

Example: Non-overlapping intervals
```

### Pattern 3: Two Pointers
```
Use when:
- Comparing two lists
- Finding intersections

Example: Interval intersections
```

### Pattern 4: Priority Queue
```
Use when:
- Managing active intervals
- Resource allocation

Example: Meeting rooms II
```

### Pattern 5: Line Sweep
```
Use when:
- Event-based processing
- Point queries

Mark start as +1, end as -1
Scan timeline
```

## Time and Space Complexity

```
Problem                      Time        Space
Merge Intervals              O(n log n)  O(n)
Insert Interval              O(n)        O(n)
Non-Overlapping              O(n log n)  O(1)
Meeting Rooms                O(n log n)  O(1)
Meeting Rooms II             O(n log n)  O(n)
Interval Intersections       O(n + m)    O(1)
Employee Free Time           O(n log n)  O(n)
My Calendar                  O(n log n)  O(n)
```

## Python Implementation

```python
# Merge Intervals
def merge(intervals):
    """
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for interval in intervals[1:]:
        if merged[-1][1] >= interval[0]:
            merged[-1][1] = max(merged[-1][1], interval[1])
        else:
            merged.append(interval)

    return merged


# Insert Interval
def insert(intervals, newInterval):
    """
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1

    result.append(newInterval)

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


# Non-Overlapping Intervals
def erase_overlap_intervals(intervals):
    """
    Time: O(n log n), Space: O(1)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 0

    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]

    return count


# Meeting Rooms
def can_attend_meetings(intervals):
    """
    Time: O(n log n), Space: O(1)
    """
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False

    return True


# Meeting Rooms II
import heapq

def min_meeting_rooms(intervals):
    """
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap = []

    for interval in intervals:
        if heap and heap[0] <= interval[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, interval[1])

    return len(heap)


# Interval List Intersections
def interval_intersection(A, B):
    """
    Time: O(n + m), Space: O(1)
    """
    i = j = 0
    result = []

    while i < len(A) and j < len(B):
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        if start <= end:
            result.append([start, end])

        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result


# Employee Free Time
def employee_free_time(schedule):
    """
    Time: O(n log n), Space: O(n)
    """
    intervals = []
    for employee in schedule:
        intervals.extend(employee)

    intervals.sort(key=lambda x: x[0])

    # Merge busy time
    merged = [intervals[0]]
    for interval in intervals[1:]:
        if merged[-1][1] >= interval[0]:
            merged[-1][1] = max(merged[-1][1], interval[1])
        else:
            merged.append(interval)

    # Find gaps (free time)
    result = []
    for i in range(1, len(merged)):
        result.append([merged[i-1][1], merged[i][0]])

    return result


# My Calendar I
class MyCalendar:
    def __init__(self):
        self.calendar = []

    def book(self, start, end):
        """
        Time: O(n), Space: O(n)
        """
        for s, e in self.calendar:
            if start < e and end > s:
                return False

        self.calendar.append((start, end))
        return True


# My Calendar II (allow double booking, not triple)
class MyCalendarTwo:
    def __init__(self):
        self.calendar = []
        self.overlaps = []

    def book(self, start, end):
        """
        Time: O(n), Space: O(n)
        """
        # Check for triple booking
        for s, e in self.overlaps:
            if start < e and end > s:
                return False

        # Add to double bookings
        for s, e in self.calendar:
            if start < e and end > s:
                self.overlaps.append((max(start, s), min(end, e)))

        self.calendar.append((start, end))
        return True


# Maximum CPU Load
def max_cpu_load(jobs):
    """
    Jobs: [[start, end, load]]
    Time: O(n log n), Space: O(n)
    """
    jobs.sort(key=lambda x: x[0])
    heap = []
    max_load = current_load = 0

    for start, end, load in jobs:
        # Remove finished jobs
        while heap and heap[0][0] <= start:
            _, job_load = heapq.heappop(heap)
            current_load -= job_load

        # Add current job
        heapq.heappush(heap, (end, load))
        current_load += load
        max_load = max(max_load, current_load)

    return max_load


# Minimum Number of Arrows to Burst Balloons
def find_min_arrow_shots(points):
    """
    Time: O(n log n), Space: O(1)
    """
    if not points:
        return 0

    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]

    for start, e in points[1:]:
        if start > end:
            arrows += 1
            end = e

    return arrows
```

## Key Takeaways

1. **Common Approaches**:
   - Sort by start/end time
   - Two pointers
   - Priority queue (heap)
   - Line sweep

2. **Overlap Detection**:
   - interval1.end > interval2.start AND
   - interval2.end > interval1.start

3. **Sorting Strategy**:
   - Start time: merging, sequential processing
   - End time: greedy scheduling, max non-overlapping

4. **Optimization**:
   - Sort once: O(n log n)
   - Process linearly: O(n)
   - Use heap for active intervals: O(log n) per operation

5. **Common Patterns**:
   - Merge: combine overlapping
   - Intersect: find common parts
   - Schedule: greedy by end time
   - Resources: track with heap

6. **Edge Cases**:
   - Empty intervals
   - Single interval
   - All overlapping
   - None overlapping
   - Adjacent intervals

7. **When to Use**:
   - Scheduling problems
   - Resource allocation
   - Range queries
   - Timeline analysis
