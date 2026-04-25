# Intervals

## 16. Intervals (6 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 57 | Medium | Insert Interval | [Link](https://leetcode.com/problems/insert-interval/) |
| 56 | Medium | Merge Intervals | [Link](https://leetcode.com/problems/merge-intervals/) |
| 435 | Medium | Non-overlapping Intervals | [Link](https://leetcode.com/problems/non-overlapping-intervals/) |
| 252 | Easy | Meeting Rooms | [Link](https://leetcode.com/problems/meeting-rooms/) |
| 253 | Medium | Meeting Rooms II | [Link](https://leetcode.com/problems/meeting-rooms-ii/) |
| 1851 | Hard | Minimum Interval to Include Each Query | [Link](https://leetcode.com/problems/minimum-interval-to-include-each-query/) |

---

## Data Structures

### Sorted List of Intervals
Sorting intervals by start time is the prerequisite for almost every interval problem. Once sorted, you only need to compare each interval against the last merged/processed one.

### Min-Heap
Used when you need to track which intervals are still "active" at a given point in time. The heap key is the end time — you can quickly check if the earliest-ending interval has ended by the current start time. Used in Meeting Rooms II, Minimum Interval to Include Each Query.

---

## Core Patterns

### Sort + Merge
Sort by start time. Scan through intervals, maintaining the current merged interval. If the next interval's start ≤ current end, extend the current end. Otherwise, finalize the current interval and start a new one. Used in Merge Intervals.

### Insert into Sorted List
Three phases: collect all intervals that end before the new one starts (no overlap, keep as-is), merge all intervals that overlap with the new one (update new interval's start/end), then collect the rest. Used in Insert Interval.

### Greedy Removal (Non-overlapping Intervals)
To remove the minimum number of intervals, keep the interval that ends earliest among overlapping ones — it leaves the most room for future intervals. Sort by end time. Greedily keep an interval if it doesn't overlap with the previous kept interval.

### Sweep Line / Event-Based (Meeting Rooms II)
Create events: +1 at each start time, -1 at each end time. Sort events by time. Scan through, tracking the running count of active meetings. The maximum count is the minimum number of rooms needed.

### Offline Query Processing (Minimum Interval to Include Each Query)
Sort both intervals and queries. Process queries in sorted order. Add intervals whose start ≤ query to a min-heap (keyed by size). Pop intervals from the heap whose end < query. The heap's top is the smallest valid interval for the current query. Store results indexed by original query position.
