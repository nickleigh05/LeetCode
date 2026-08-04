# 355. Design Twitter

**Medium** · [LeetCode](https://leetcode.com/problems/design-twitter/)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Design a simplified version of Twitter supporting four operations:

- **`postTweet(userId, tweetId)`** — compose a new tweet
- **`getNewsFeed(userId)`** — return the **10 most recent** tweet IDs in the user's feed: their own tweets **plus** those of everyone they follow, **most recent first**
- **`follow(followerId, followeeId)`** / **`unfollow(followerId, followeeId)`**

```
postTweet(1, 5)
getNewsFeed(1)   →  [5]
follow(1, 2)
postTweet(2, 6)
getNewsFeed(1)   →  [6, 5]        ← merged, newest first
unfollow(1, 2)
getNewsFeed(1)   →  [5]
```

**Constraints:** `1 <= userId, tweetId <= 10⁴` · up to 3·10⁴ calls total

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Design**" | Multiple structures cooperating — like [LRU Cache](146-lru-cache.md) |
| "**10 most recent**" | ⚠️ A fixed, small k. You never need the full feed — just the top 10 |
| "own tweets **plus** followees'" | Merge several users' tweet lists into one ordered result |
| "most **recent** first" | Needs a global ordering across users, so a per-user counter won't do |
| a user follows themselves implicitly | Their own tweets always appear; handle it without a special case |
| up to 3·10⁴ calls | Feed construction should not scan every tweet ever posted |

**The key structural observation.** Each user's tweets are stored in the order they were posted, so **each user's list is already sorted by time** (newest at the end).

Building a feed means merging several sorted lists and taking the first 10 — which is **exactly [Merge k Sorted Lists](23-merge-k-sorted-lists.md)**, with users in place of linked lists.

And you already know the tool for that: a **heap holding one candidate per list**, popping the best and refilling from the same list.

**The second observation: you only need 10.** Merging *all* tweets from all followees would be O(total tweets). Stopping after 10 pops means the cost depends on the number of *followees*, not the volume of tweets — which is what makes this scale.

**The timestamp problem.** Tweets must be ordered across users, so a per-user index isn't enough. A single global counter incremented on every post gives every tweet a unique, comparable time.

⚠️ And a Python wrinkle: `heapq` is a min-heap, but you want the **newest** (largest timestamp) first. This solution handles it by making time count **downward** — so newer tweets have *smaller* numbers and the min-heap surfaces them naturally.

🤔 **Before you open the next section:** when you pop the newest tweet from some user, which tweet should replace it in the heap — and how do you know where to find it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `getNewsFeed` | Verdict |
|---|---|---|
| One global tweet list, filter by followees | O(total tweets) | ❌ Rescans all history every call |
| Collect all followees' tweets, sort | O(T log T) for T tweets | ⚠️ Correct; sorts far more than the 10 needed |
| Keep a materialized feed per user | O(1) read | ⚠️ But `follow`/`unfollow` become expensive — a real design trade |
| **Heap of one tweet per followee** | **O(f + 10 log f)** | ✅ |

**The decision: per-user tweet lists, a follow-set per user, and a k-way merge via heap for the feed.**

The state:

| Structure | Purpose |
|---|---|
| `tweets: user → [(time, tweetId), …]` | Per-user history, naturally sorted by time |
| `following: user → set of followees` | O(1) follow, unfollow, and membership |
| `time` | A global counter making tweets comparable across users |

**The feed algorithm** is [Merge k Sorted Lists](23-merge-k-sorted-lists.md) applied to users:

1. Seed the heap with each followed user's **most recent** tweet (their list's last element).
2. Pop the newest overall, append it to the feed.
3. Push that same user's **next-newest** tweet, so the user stays represented.
4. Stop at 10 results, or when the heap empties.

**Why the heap never exceeds `f` entries** (the number of followees): only one candidate per user is live at a time, because everything older in that user's list is provably not next. Same reasoning as [Merge k Sorted Lists](23-merge-k-sorted-lists.md) — **keep only the frontier**.

**The countdown-timestamp trick.** Rather than negating on every push, `self.time -= 1` makes newer tweets have smaller values, so Python's min-heap pops them first with no negation anywhere. Equivalent to storing `-time`; slightly cleaner because the inversion happens once, at the source.

**Why the heap entry is a 4-tuple `(time, tweetId, user, index)`.** `time` orders it; `tweetId` is the payload; `user` and `index` are the **bookmark** saying where to fetch that user's next tweet. Without them you couldn't refill the heap. Same "payload plus position" idea as [Merge k Sorted Lists](23-merge-k-sorted-lists.md)'s `(value, list_index, node)`.

**The design trade worth naming:** this is **read-heavy work at query time** (fan-out on read). The alternative — maintaining a precomputed feed per user (fan-out on write) — makes reads O(1) but makes posting cost O(followers), which for a celebrity account is millions of writes. Real systems use hybrids. **Mentioning this shows systems awareness.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.time = 0
    self.tweets = defaultdict(list)
    self.following = defaultdict(set)
```

`defaultdict` means a user's list or follow-set springs into existence on first access — no "does this key exist?" checks anywhere else in the class.
→ [defaultdict](../syntax/defaultdict.md) · [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
def postTweet(self, userId: int, tweetId: int) -> None:
    self.tweets[userId].append((self.time, tweetId))
    self.time -= 1   # time counts down so the min-heap pops the newest tweet first
```

Append to the user's history, then **decrement** the clock.

Counting **down** means newer tweets have smaller timestamps, so a min-heap pops the newest first — no negation needed at the heap. The inversion is applied once, at the source.

Appending keeps each user's list in posting order, which is what makes the merge possible.
→ [list-methods](../syntax/list-methods.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
def getNewsFeed(self, userId: int) -> List[int]:
    heap = []
    users = self.following[userId] | {userId}
```

`|` is set union — the followees **plus the user themselves**, so their own tweets appear without a special case.
→ [set-operations](../syntax/set-operations.md) · [set-basics](../syntax/set-basics.md)

```python
    for user in users:
        if self.tweets[user]:
            index = len(self.tweets[user]) - 1
            time, tweet_id = self.tweets[user][index]
            heapq.heappush(heap, (time, tweet_id, user, index - 1))
```

**Seed the heap with each user's newest tweet** — the last element of their list.

The tuple carries four things: `time` (the sort key), `tweet_id` (the payload), and `user` + `index - 1` (a **bookmark** pointing at that user's next-newest tweet, for the refill step).

`if self.tweets[user]` skips users who've never posted.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [heapq-module](../syntax/heapq-module.md)

```python
    feed = []
    while heap and len(feed) < 10:
        time, tweet_id, user, index = heapq.heappop(heap)
        feed.append(tweet_id)
```

**Pop the newest overall.** Because time counts down, the min-heap's root is the most recent tweet across all followed users.

`len(feed) < 10` is the **early exit** that keeps this cheap — you stop after ten regardless of how many tweets exist.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
        if index >= 0:
            time, tweet_id = self.tweets[user][index]
            heapq.heappush(heap, (time, tweet_id, user, index - 1))
```

**Refill from the same user.** Having consumed one of their tweets, push the next-newest so that user stays represented — walking *backwards* through their list, since newest is at the end.

`index >= 0` stops when that user's history is exhausted. This is what bounds the heap at `f` entries.
→ [if-return](../syntax/if-return.md)

```python
    return feed
```

At most 10 tweet IDs, newest first — the heap popped them in order, so no sorting is needed.

```python
def follow(self, followerId: int, followeeId: int) -> None:
    self.following[followerId].add(followeeId)

def unfollow(self, followerId: int, followeeId: int) -> None:
    self.following[followerId].discard(followeeId)
```

Both O(1) on a set. **`.discard()` rather than `.remove()`** — it's a no-op if the element is absent, so unfollowing someone you never followed doesn't raise `KeyError`.

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — the example sequence:

| Call | State change |
|---|---|
| `postTweet(1, 5)` | `tweets[1] = [(0, 5)]`, time → −1 |
| `getNewsFeed(1)` | users = {1}; heap seeded with `(0, 5, 1, −1)`; pop → feed `[5]` ✅ |
| `follow(1, 2)` | `following[1] = {2}` |
| `postTweet(2, 6)` | `tweets[2] = [(-1, 6)]`, time → −2 |

**`getNewsFeed(1)`** — now users = `{1, 2}`:

| Step | Heap | Pop | Feed |
|---|---|---|---|
| seed | `(0,5,1,−1)`, `(−1,6,2,−1)` | — | — |
| 1 | | **`(−1, 6)`** ← smaller time = newer | `[6]` |
| 2 | | `(0, 5)` | `[6, 5]` ✅ |

Both users' indices hit −1, so no refills. Result `[6, 5]` — newest first ✅

| `unfollow(1, 2)` | `following[1] = {}` |
| `getNewsFeed(1)` | users = {1} only → `[5]` ✅ |

The countdown clock is doing the work: tweet 6 has time **−1** and tweet 5 has **0**, so the min-heap pops 6 first — correctly, since it's newer.

</details>

<details>
<summary><b>4 · Time complexity</b></summary>

| Operation | Cost |
|---|---|
| `postTweet` | **O(1)** — one append |
| `follow` / `unfollow` | **O(1)** — set add/discard |
| `getNewsFeed` | **O(f + 10 log f)** where f = number of followees |

**Breaking down the feed:**
- Seeding: f pushes at O(log f) each → O(f log f).
- The merge: at most 10 iterations, each one pop and one push at O(log f) → **O(10 log f)**.

Written more simply, **O(f log f)**, dominated by the seeding.

**The crucial property: the cost is independent of how many tweets exist.** A user following 20 people gets their feed in ~20 heap operations, whether those people have posted 20 tweets or 20 million. **The early exit at 10 is what buys that** — you never merge the full history.

**Versus the alternatives:**

| Approach | `getNewsFeed` |
|---|---|
| Scan all tweets, filter | O(total tweets) — grows forever |
| Collect + sort followees' tweets | O(T log T) for T total tweets across followees |
| **Heap with early exit** | **O(f log f)** |

The heap wins because it exploits both facts the problem hands you: each user's list is **already sorted**, and you only need **10** results.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total tweets + follows)</summary>

**O(N + F)**, where N is the total tweets posted and F the total follow relationships.

- `tweets`: every tweet stored once → O(N).
- `following`: one entry per follow edge → O(F).
- `heap` during a feed: at most f entries → **O(f)**, transient.

**Nothing is ever deleted**, so storage grows with usage — appropriate for this problem, though a real system would cap or archive per-user history.

**A cheap optimization worth mentioning:** since a feed never returns more than 10 tweets, you only ever need each user's **most recent 10**. Truncating the stored lists would bound memory at O(users × 10) — a real design decision with a real trade (you lose history).

**The design axis worth raising**, and the thing that turns this from a coding answer into a systems answer:

| Strategy | `postTweet` | `getNewsFeed` |
|---|---|---|
| **Fan-out on read** (this solution) | **O(1)** | O(f log f) |
| Fan-out on write (precomputed feeds) | **O(followers)** | **O(1)** |

Fan-out on write is great for ordinary users but catastrophic for accounts with millions of followers — one post triggers millions of writes. Production systems use a **hybrid**: precompute for normal accounts, merge on read for celebrities. Naming that trade-off is exactly what a "Design Twitter" question is fishing for.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each user's tweets are stored in posting order, so they're already sorted by time — which makes building a feed a k-way merge of sorted lists, exactly like Merge k Sorted Lists but with users instead of lists. I keep per-user tweet lists, a follow-set per user, and a global counter so tweets are comparable across users. For the feed I seed a heap with each followed user's newest tweet, then repeatedly pop the newest overall and push that user's next-newest, stopping after 10. The heap holds only one candidate per user, so it's O(f log f) regardless of how many tweets exist — the early exit at 10 is what makes it independent of history size. I have the timestamp count *down* so Python's min-heap pops the newest first without any negation. This is fan-out on read; the alternative is precomputing feeds, which makes reads O(1) but posting O(followers)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a heap rather than sorting all the tweets?" | Each user's list is already sorted, and you need only 10 — so merge the frontiers instead of sorting everything. |
| "How does this scale for a user with a million followees?" | The heap is O(f), so feed construction degrades. You'd cap followees, shard, or precompute. |
| "Fan-out on read vs on write?" | **The systems question.** Read-side merging keeps posts O(1) but reads O(f); write-side precomputation flips it. Real systems hybridize by follower count. |
| "Why count time downward?" | It inverts the ordering once at the source, so the min-heap surfaces the newest tweet with no negation at the heap. |
| "Why `.discard()` and not `.remove()`?" | `.remove()` raises `KeyError` if absent; unfollowing someone you never followed should be a no-op. |
| "Bound the memory." | Keep only each user's most recent 10 tweets — a feed can never need more. |
| "What if tweets could be deleted?" | Mark them tombstoned and skip them during the merge, or remove from the list at O(len). |

**Traps:**

- **Forgetting to include the user themselves** in the merge — their own tweets vanish from their feed.
- **Using a per-user counter** instead of a global one — tweets from different users become incomparable.
- **Not carrying `user` and `index` in the heap tuple** — you can't refill, so each user contributes only one tweet.
- **Merging everything before truncating.** Correct but wasteful; the early exit is the point.
- **Walking the tweet list forwards.** Newest is at the **end**, so you iterate backwards.
- **`.remove()` on unfollow** → `KeyError`.

**This same move shows up in:** [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (the identical k-way merge, with the same tuple-bookmark technique) · [LRU Cache](146-lru-cache.md) (a design problem pairing structures) · [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (a heap holding only the relevant frontier) · [heap](../data-structures/heap.md).

</details>
