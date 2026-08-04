# 287. Find the Duplicate Number

**Medium** · [LeetCode](https://leetcode.com/problems/find-the-duplicate-number/)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array `nums` of `n + 1` integers where each integer is in the range `[1, n]` inclusive, there is **exactly one repeated number**. Return that number.

You must solve the problem **without modifying** the array and using only **constant extra space**.

```
nums = [1,3,4,2,2]    →  2
nums = [3,1,3,4,2]    →  3
nums = [3,3,3,3,3]    →  3
```

**Constraints:** `1 <= n <= 10⁵` · `nums.length == n + 1` · `1 <= nums[i] <= n` · exactly one value repeats, possibly **many times**

> **Try it yourself first.** This one is a genuine leap — the sections below build up to it.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `n + 1` integers, values in `[1, n]` | **Pigeonhole principle** — more items than slots, so a repeat is guaranteed |
| "**without modifying** the array" | ⚠️ Rules out sorting, and rules out the classic index-marking trick |
| "**constant extra space**" | ⚠️ Rules out a hash set. Together these two constraints are the whole problem |
| "exactly one repeated number" | But it "may be repeated **more than once**" — `[3,3,3,3,3]` is legal |
| values in `[1, n]`, **never 0** | ⚠️ Quietly essential. Index 0 is never a pointer *target*, so it can't be inside a cycle |
| n up to 10⁵ | O(n) or O(n log n); O(n²) is dead |

Take away sorting and hashing and there's nothing obvious left. The unlock is a **reframe**:

> **Treat each value as a pointer to an index.**

From index `i`, "follow" to index `nums[i]`. Since every value is in `[1, n]` and the array has `n+1` slots, every value is a valid index — so you can follow this chain forever.

```
nums = [1,3,4,2,2]
index:  0 1 2 3 4

0 → nums[0]=1 → nums[1]=3 → nums[3]=2 → nums[4]=2 → nums[2]=4 → nums[4]=2 → ...

      0 → 1 → 3 → 2 → 4
                  ↑     │
                  └─────┘   a cycle
```

**Why a duplicate forces a cycle.** If value `d` appears at two different indices, then two different nodes both point *to* index `d`. A node with two things pointing at it is where a chain merges — and a merging chain in a finite space must loop. **The entrance to that cycle is the duplicate value.**

**Why index 0 is safe as a starting point:** values are `1..n`, never 0, so nothing points *at* index 0. It's outside the cycle, which is what the algorithm needs.

Now the problem reads: *find where a cycle begins in a linked list* — with no linked list anywhere in sight. That's [Floyd's algorithm](../algorithms/floyd-cycle-detection.md), from [problem 141](141-linked-list-cycle.md).

🤔 **Before you open the next section:** why does having two indices point to the same place guarantee a loop, rather than just a fork?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Modifies? | Verdict |
|---|---|---|---|---|---|
| Hash set | Track values seen | O(n) | **O(n)** | no | ❌ Violates constant space |
| Sort, check neighbours | Duplicates become adjacent | O(n log n) | O(1) | **yes** | ❌ Violates "don't modify" |
| Negate visited indices | Mark `nums[abs(v)]` negative | O(n) | O(1) | **yes** | ❌ Violates "don't modify" |
| Binary search on the **value** | Count elements ≤ mid; pigeonhole | O(n log n) | O(1) | no | ✅ Good fallback! |
| **Floyd's cycle detection** | Values as pointers | **O(n)** | **O(1)** | no | ✅ |

**The decision: [Floyd's cycle detection](../algorithms/floyd-cycle-detection.md) on the implicit "linked list" formed by `i → nums[i]`.**

Two phases:

**Phase 1 — find a meeting point.** `slow` takes one step (`slow = nums[slow]`), `fast` takes two. Inside the cycle the gap closes by one per step, so they must collide — the same argument as [141](141-linked-list-cycle.md).

**Phase 2 — find the cycle's entrance.** Reset a second pointer to the start, then advance *both* one step at a time. **They meet exactly at the cycle's entrance**, which is the duplicate.

**Why phase 2 works.** Let `μ` be the distance from the start to the cycle entrance, `C` the cycle length, and `k` the distance from the entrance to the meeting point. When they meet, `slow` has travelled `μ + k` and `fast` has travelled `2(μ + k)`. Since `fast` covered exactly some whole number of extra laps: `2(μ+k) − (μ+k) = μ + k` is a multiple of `C`. So walking a further `μ` steps from the meeting point lands you `μ + k + μ` from the start — and because `μ + k` is a whole number of laps, that's the same as walking `μ` from the start: **the entrance**. Hence two pointers, one at the start and one at the meeting point, converge there.

You don't need to reproduce that proof under pressure — but knowing *why* the reset works separates understanding from memorization.

**The binary-search alternative is worth knowing.** Binary search the *value* range `[1, n]`: for a candidate `m`, count how many array elements are `<= m`. If that count exceeds `m`, pigeonhole says the duplicate is in `[1, m]`. O(n log n) time, O(1) space, no modification. **If Floyd's doesn't come to you, this one is far easier to derive from scratch** — say it out loud rather than stalling.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
slow = nums[0]
fast = nums[0]
```

Both start at the first "node" after index 0. Starting at `nums[0]` rather than `0` keeps the two phases symmetric — phase 2 will also start from `nums[0]`.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while True:
    slow = nums[slow]
    fast = nums[nums[fast]]
    if slow == fast:
        break
```

**Phase 1 — Floyd's tortoise and hare.** `slow` follows one pointer per step; `fast` follows two by indexing twice.

`while True` with a `break` rather than a condition, because the loop's exit *is* the collision — and a collision is guaranteed, since a cycle must exist by the pigeonhole principle. There's no "reached the end" case to handle here, unlike [141](141-linked-list-cycle.md): this chain never terminates.

The `if` comes **after** both moves, so the shared starting position doesn't count as a meeting.
→ [while-loop](../syntax/while-loop.md) · [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
slow2 = nums[0]
while slow != slow2:
    slow = nums[slow]
    slow2 = nums[slow2]
```

**Phase 2 — find the entrance.** Reset a second pointer to the start while `slow` stays at the meeting point, then advance **both at the same speed**.

By the argument in section 2, they converge exactly at the cycle's entrance. Note the speeds are now equal — this phase is *not* fast/slow.

```python
return slow
```

The entrance node. Its **index** is the duplicated value — which is why we return the pointer itself rather than `nums[slow]`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:

        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        slow2 = nums[0]
        while slow != slow2:
            slow = nums[slow]
            slow2 = nums[slow2]

        return slow
```

</details>

**Trace it** — `nums = [1,3,4,2,2]`:

The chain from index 0: `0 → 1 → 3 → 2 → 4 → 2 → 4 → …` — cycle entrance at **2**.

**Phase 1** (both start at `nums[0] = 1`):

| Step | `slow` | `fast` | Met? |
|---|---|---|---|
| start | 1 | 1 | (not tested) |
| 1 | `nums[1]`=3 | `nums[nums[1]]`=`nums[3]`=2 | no |
| 2 | `nums[3]`=2 | `nums[nums[2]]`=`nums[4]`=2 | ✅ **meet at 2** |

**Phase 2** (`slow` = 2, `slow2` = `nums[0]` = 1):

| Step | `slow` | `slow2` | Equal? |
|---|---|---|---|
| start | 2 | 1 | no |
| 1 | `nums[2]`=4 | `nums[1]`=3 | no |
| 2 | `nums[4]`=2 | `nums[3]`=2 | ✅ **both at 2** |

Return **2** ✅ — and indeed 2 appears twice in `[1,3,4,2,2]`.

**The binary-search alternative:**

```python
left, right = 1, len(nums) - 1
while left < right:
    mid = (left + right) // 2
    count = sum(1 for x in nums if x <= mid)
    if count > mid:
        right = mid
    else:
        left = mid + 1
return left
```
→ [generator-expressions](../syntax/generator-expressions.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- **Phase 1:** `slow` walks at most the full chain before entering the cycle, then meets `fast` within one lap → O(n).
- **Phase 2:** both pointers walk at most `μ + C ≤ n` steps → O(n).

Two sequential linear phases → **O(n)**.

Each step is a single array index — genuinely constant work, no allocation.

**Versus the alternatives:**

| Approach | Time | Space | Modifies |
|---|---|---|---|
| Hash set | O(n) | O(n) | no |
| Sorting | O(n log n) | O(1) | **yes** |
| Binary search on value | O(n log n) | O(1) | no |
| **Floyd's** | **O(n)** | **O(1)** | **no** |

Floyd's is the only one satisfying all three requirements optimally — which is exactly why the problem imposes both constraints. **Each constraint exists to eliminate one easy solution**, and noticing that is the tell that something unusual is wanted.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integer variables, and the array is only read.

**The array is never modified**, which is worth stating explicitly since the popular index-negation trick (`nums[abs(v)] *= -1`) is O(1) space but *mutates* the input — a genuine violation, not a technicality. If the array is shared, read-only, or reused, that solution corrupts it.

**How constant space was achieved.** The hash set stores every value seen. Floyd's stores **nothing** — the duplicate is discovered through the *geometry of the traversal*, not from history. The information lives in the relationship between two moving pointers.

This is the same idea as [141](141-linked-list-cycle.md), and it's the sharpest example in the roadmap of a recurring theme:

| Strategy | Space |
|---|---|
| Remember what you've seen | **O(n)** |
| Exploit structure / relationships | **O(1)** |

**The transferable insight:** *anything with a "next" function forms an implicit linked list.* Arrays where values are indices, state machines, pseudo-random generators, hash chains — all support Floyd's, and none of them look like linked lists.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The constraints are the clue — no modification rules out sorting, and constant space rules out a hash set. So I reframe: every value is in `[1, n]`, so every value is a valid *index*. Treating `i → nums[i]` as a next-pointer turns the array into an implicit linked list. A duplicate means two indices point at the same place, and a merging chain in a finite space must form a cycle — whose entrance is the duplicate. So I run Floyd's: phase one, slow and fast pointers meet inside the cycle; phase two, reset one pointer to the start and advance both at the same speed, and they converge exactly at the entrance. O(n) time, O(1) space, array untouched. A simpler alternative is binary searching the value range and counting elements ≤ mid — O(n log n), also constant space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does a duplicate create a cycle?" | **The question.** Two indices holding value `d` both point at index `d` — a merge point. Following pointers forward in a finite set with a merge must eventually repeat. |
| "Why does resetting to the start find the entrance?" | Distance to the meeting point is a multiple of the cycle length, so walking `μ` more steps from there lands on the entrance — same as walking `μ` from the start. |
| "Why is starting at index 0 safe?" | Values are `1..n`, never 0, so nothing points at index 0 — it's guaranteed to be outside the cycle. |
| "Show a solution that doesn't need Floyd's." | Binary search the value range, counting elements ≤ mid. O(n log n), O(1) space, no mutation. Much easier to derive. |
| "What if modifying were allowed?" | Negate `nums[abs(v)]`; when you hit an already-negative slot, `abs(v)` is the duplicate. O(n)/O(1), but destructive. |
| "What if there were **multiple** distinct duplicates?" | Floyd's finds only one cycle. You'd need a hash set or sorting — O(n) space or mutation. |
| "How does this relate to problem 141?" | Same algorithm. There the pointers are real; here they're array indices. Recognizing the isomorphism is the whole skill. |

**Traps:**

- **Returning `nums[slow]`** instead of `slow`. The *index* is the duplicate value.
- **Skipping phase 2** and returning the meeting point. That's a node inside the cycle, generally **not** the entrance.
- **Using fast/slow speeds in phase 2.** Both must move one step at a time.
- **Starting phase 1 at `0` but phase 2 at `nums[0]`** (or vice versa). They must be consistent.
- **Comparing before moving** in phase 1 — both start equal, so it breaks immediately.
- **Assuming the duplicate appears exactly twice.** `[3,3,3,3,3]` is valid; the algorithm handles it, but reasoning that assumes exactly two occurrences may not.

**This same move shows up in:** [Linked List Cycle](141-linked-list-cycle.md) (the same algorithm on a real list) · [floyd-cycle-detection](../algorithms/floyd-cycle-detection.md) (the reference page) · [Missing Number](268-missing-number.md) (another values-as-indices trick) · [Koko Eating Bananas](875-koko-eating-bananas.md) (the binary-search-the-answer alternative).

</details>
