# 09. Heap / Priority Queue — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

---

### 703. Kth Largest Element in a Stream — Easy
[LeetCode](https://leetcode.com/problems/kth-largest-element-in-a-stream/)  
[Solution file (no hints)](../../problems/0500-0999/703.py)

Design a class that returns the kth largest element after each new value is added. Why does keeping a [heap](../data-structures/heap.md) of exactly size k, rather than sorting everything each time, make each `add` cheap?

<details>
<summary>Hint</summary>

Keep a min-[heap](../data-structures/heap.md) of the k largest values seen so far. The smallest value in that heap (the root) is always the kth largest overall; push new values in and pop the smallest back out once the heap exceeds size k.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)              # build the heap once
        while len(self.heap) > k:               # trim down to size k
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:              # keep the heap capped at size k
            heapq.heappop(self.heap)
        return self.heap[0]                     # root = kth largest
```

Building blocks: [class-basics](../syntax/class-basics.md) · [while-loop](../syntax/while-loop.md) · [heap](../data-structures/heap.md) (`heapq.heapify/heappush/heappop`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log k)** per `add` call.
**Space: O(k)** — the heap never grows beyond size k.
</details>

---

### 1046. Last Stone Weight — Easy
[LeetCode](https://leetcode.com/problems/last-stone-weight/)  
[Solution file (no hints)](../../problems/1000-1499/1046.py)

Repeatedly smash the two heaviest stones together until at most one remains. Why does always needing the current *two largest* values scream "max-heap"?

<details>
<summary>Hint</summary>

Python's `heapq` is a min-heap, so negate values to simulate a max-[heap](../data-structures/heap.md). Pop the two largest, push back their difference (if nonzero), and repeat.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

stones = [-s for s in stones]          # negate for a max-heap using heapq
heapq.heapify(stones)

while len(stones) > 1:                  # while loop, smash the two heaviest
    first = -heapq.heappop(stones)
    second = -heapq.heappop(stones)
    if first != second:                    # leftover weight goes back in
        heapq.heappush(stones, -(first - second))

return -stones[0] if stones else 0
```

Building blocks: [list-comprehension](../syntax/list-comprehension.md) · [while-loop](../syntax/while-loop.md) · [heap](../data-structures/heap.md) · [ternary-expression](../syntax/ternary-expression.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — up to n pops/pushes, each O(log n).
**Space: O(n)** — the heap holds all the stones.
</details>

---

### 973. K Closest Points to Origin — Medium
[LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/)  
Solution: not yet solved in this repo.

Return the k points closest to the origin. Why is a max-heap of size k (evicting the farthest point) more efficient than sorting all n points when k is much smaller than n?

<details>
<summary>Hint</summary>

Use a max-[heap](../data-structures/heap.md) (negate distances) capped at size k: push each point's squared distance, and if the heap exceeds k, pop the farthest. What remains is exactly the k closest points.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

heap = []
for x, y in points:                     # for loop over every point
    dist = x * x + y * y                  # squared distance, avoids sqrt
    heapq.heappush(heap, (-dist, x, y))     # negate for a max-heap
    if len(heap) > k:
        heapq.heappop(heap)                   # evict the farthest point

return [[x, y] for _, x, y in heap]
```

Building blocks: [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md) · [heap](../data-structures/heap.md) · [list-comprehension](../syntax/list-comprehension.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log k)** — n points, each heap operation O(log k) since the heap is capped at size k.
**Space: O(k)** — the heap never grows beyond size k.
</details>

---

### 215. Kth Largest Element in an Array — Medium
[LeetCode](https://leetcode.com/problems/kth-largest-element-in-an-array/)  
[Solution file (no hints)](../../problems/0001-0499/215.py)

Find the kth largest element without fully sorting. How does a min-heap of size k, similar to [703](#703-kth-largest-element-in-a-stream--easy), answer this in one pass?

<details>
<summary>Hint</summary>

Keep a min-[heap](../data-structures/heap.md) of the k largest values seen so far; once it exceeds size k, pop the smallest. After processing every number, the heap's root is the kth largest.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

heap = []
for num in nums:                        # for loop over the array
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)                # keep only the k largest so far

return heap[0]                          # root of the size-k min-heap
```

Building blocks: [for-loop](../syntax/for-loop.md) · [heap](../data-structures/heap.md) (`heapq.heappush/heappop`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log k)** — n numbers, each heap operation O(log k).
**Space: O(k)** — the heap never grows beyond size k.
</details>

---

### 621. Task Scheduler — Medium
[LeetCode](https://leetcode.com/problems/task-scheduler/)  
Solution: not yet solved in this repo.

Given tasks and a cooldown `n` between identical tasks, find the minimum time to finish them all. Why does always scheduling the *most frequent remaining* task next (a max-heap) minimize idle time?

<details>
<summary>Hint</summary>

Count task frequencies, then greedily pull from a max-[heap](../data-structures/heap.md) of counts, processing up to `n + 1` different tasks per "round" and pushing back any tasks that still have remaining count, tracking idle slots when fewer than `n + 1` tasks are available.
</details>

<details>
<summary>Solution</summary>

```python
import heapq
from collections import Counter, deque

counts = Counter(tasks)
max_heap = [-c for c in counts.values()]   # negate for a max-heap
heapq.heapify(max_heap)

time = 0
q = deque()                              # (count, ready_time) waiting out cooldown

while max_heap or q:                      # while loop until all tasks scheduled
    time += 1

    if max_heap:                            # run the most frequent remaining task
        cnt = 1 + heapq.heappop(max_heap)     # one less occurrence remaining (still negative or 0)
        if cnt:                                 # more of this task left: cooldown before reuse
            q.append((cnt, time + n))

    if q and q[0][1] == time:               # a cooled-down task becomes available again
        heapq.heappush(max_heap, q.popleft()[0])

return time
```

Building blocks: [counter](../syntax/counter.md) · [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md) · [heap](../data-structures/heap.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log 26)** = **O(n)** — n tasks, heap bounded by 26 distinct task types.
**Space: O(26)** = **O(1)** — the heap and queue are bounded by the number of distinct task types.
</details>

---

### 355. Design Twitter — Medium
[LeetCode](https://leetcode.com/problems/design-twitter/)  
Solution: not yet solved in this repo.

Design a simplified Twitter: post tweets, follow/unfollow, and get the 10 most recent tweets from a user's own feed (self + followees). Why is merging several users' already-time-ordered tweet lists a textbook use of a max-heap?

<details>
<summary>Hint</summary>

Give each tweet a global increasing timestamp. To build a feed, push the most recent tweet from each followed user (plus self) into a max-[heap](../data-structures/heap.md) keyed by timestamp, then pop the top and push that user's next tweet, repeating until you have 10 or run out.
</details>

<details>
<summary>Solution</summary>

```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)      # user -> list of (time, tweetId), newest last
        self.following = defaultdict(set)    # user -> set of followees

    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.time, tweetId))
        self.time -= 1                          # decreasing "time" so heap pops newest first

    def getNewsFeed(self, userId):
        heap = []
        users = self.following[userId] | {userId}   # self + followees

        for u in users:                            # seed heap with each user's most recent tweet
            if self.tweets[u]:
                idx = len(self.tweets[u]) - 1
                t, tweet_id = self.tweets[u][idx]
                heapq.heappush(heap, (t, tweet_id, u, idx - 1))

        res = []
        while heap and len(res) < 10:               # pull the 10 most recent overall
            t, tweet_id, u, idx = heapq.heappop(heap)
            res.append(tweet_id)
            if idx >= 0:                               # push that user's next-most-recent tweet
                nt, ntweet_id = self.tweets[u][idx]
                heapq.heappush(heap, (nt, ntweet_id, u, idx - 1))

        return res

    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [set-operations](../syntax/set-operations.md) (`|`, `.discard()`) · [heap](../data-structures/heap.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(f log f)** per `getNewsFeed`, where f = number of followees (heap of size f).
**Space: O(n)** — total tweets stored across all users.
</details>

---

### 295. Find Median from Data Stream — Hard
[LeetCode](https://leetcode.com/problems/find-median-from-data-stream/)  
[Solution file (no hints)](../../problems/0001-0499/295.py)

Support adding numbers one at a time and finding the running median in O(log n). Why do two heaps — a max-heap for the lower half and a min-heap for the upper half — let the median be found in O(1)?

<details>
<summary>Hint</summary>

Keep a max-[heap](../data-structures/heap.md) for the smaller half of numbers and a min-heap for the larger half, always rebalanced so their sizes differ by at most 1. The median is then either the top of the larger heap, or the average of both tops.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []                   # max-heap (negated), lower half
        self.large = []                   # min-heap, upper half

    def addNum(self, num):
        heapq.heappush(self.small, -num)

        # ensure every value in small <= every value in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # rebalance sizes so they differ by at most 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2
```

Building blocks: [class-basics](../syntax/class-basics.md) · [heap](../data-structures/heap.md) · [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** per `addNum`; **O(1)** per `findMedian`.
**Space: O(n)** — both heaps together hold every number added.
</details>
