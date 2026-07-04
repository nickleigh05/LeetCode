# 09. Heap / Priority Queue — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md)

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

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []

        for num in nums:
            heapq.heappush(self.heap, num)
            if len(self.heap) > self.k:
                heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

Building blocks: [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [for-loop](../syntax/for-loop.md) · [heap](../data-structures/heap.md) (`heapq.heappush/heappop`)
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

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:

        heap = [-s for s in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            first = -heapq.heappop(heap)
            second = -heapq.heappop(heap)
            if first != second:
                heapq.heappush(heap, -(first - second))

        return -heap[0] if heap else 0
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

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:

        heap = []

        for x, y in points:
            dist = x * x + y * y
            heapq.heappush(heap, (-dist, x, y))
            if len(heap) > k:
                heapq.heappop(heap)

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

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:

        heap = []

        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]
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

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:

        counts = Counter(tasks)
        max_heap = [-count for count in counts.values()]
        heapq.heapify(max_heap)

        time = 0
        queue = deque()

        while max_heap or queue:
            time += 1

            if max_heap:
                count = 1 + heapq.heappop(max_heap)   # counts are negative, +1 uses one occurrence
                if count:
                    queue.append((count, time + n))

            if queue and queue[0][1] == time:
                heapq.heappush(max_heap, queue.popleft()[0])

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
        self.tweets = defaultdict(list)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time -= 1   # time counts down so the min-heap pops the newest tweet first

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []
        users = self.following[userId] | {userId}

        for user in users:
            if self.tweets[user]:
                index = len(self.tweets[user]) - 1
                time, tweet_id = self.tweets[user][index]
                heapq.heappush(heap, (time, tweet_id, user, index - 1))

        feed = []
        while heap and len(feed) < 10:
            time, tweet_id, user, index = heapq.heappop(heap)
            feed.append(tweet_id)

            if index >= 0:
                time, tweet_id = self.tweets[user][index]
                heapq.heappush(heap, (time, tweet_id, user, index - 1))

        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
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
        self.small = []   # max-heap (negated values), lower half
        self.large = []   # min-heap, upper half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)

        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2.0
```

Building blocks: [class-basics](../syntax/class-basics.md) · [heap](../data-structures/heap.md) · [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** per `addNum`; **O(1)** per `findMedian`.
**Space: O(n)** — both heaps together hold every number added.
</details>
