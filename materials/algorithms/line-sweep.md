# Line Sweep (Events + Delta Counting)

```python
def min_meeting_rooms(intervals):          # max simultaneous meetings
    events = []
    for start, end in intervals:
        events.append((start, +1))         # meeting begins → one more room
        events.append((end, -1))           # meeting ends   → one room back
    events.sort()                          # ties: -1 before +1 ← end frees first
    rooms = best = 0
    for _, delta in events:
        rooms += delta
        best = max(best, rooms)
    return best
```

Turn intervals into **events** (+1 at start, −1 at end), sort, and sweep a line across time keeping a running count — "how many intervals cover this point?" becomes a cumulative sum. This one shape solves Meeting Rooms II, Car Pooling, My Calendar, Number of Flowers in Bloom, and skyline-adjacent problems; with coordinates instead of counts (and a [heap](../data-structures/heap.md)/[sorted list](../data-structures/sorted-list.md) tracking active items), it scales to The Skyline Problem itself. Two details carry all the difficulty: **tie order** (does an interval ending at t free its slot before one starting at t claims it? decide per problem) and, when the axis is bounded and dense, the array variant — a *difference array* you prefix-sum at the end.

**Complexity:** O(n log n) for the sort · O(n) sweep · difference-array variant O(n + range).

**Related:** [Intervals lesson](../learning/17-intervals.md) · [Prefix Sums lesson](../learning/01b-prefix-sums.md) · [heap (data-structures)](../data-structures/heap.md) · [sorting-key (syntax)](../syntax/sorting-key.md)
