# 217. Contains Duplicate

**Easy** · [LeetCode](https://leetcode.com/problems/contains-duplicate/) · [Solution file (no hints)](../../problems/0001-0499/217.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums`, return `true` if any value appears **at least twice**, and `false` if every element is distinct.

```
nums = [1, 2, 3, 1]  →  true      (1 appears at indices 0 and 3)
nums = [1, 2, 3, 4]  →  false     (all distinct)
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

Read it a second time, but hunt for *signal words* instead of meaning:

| The statement says | Which really means |
|---|---|
| "any value **appears at least twice**" | This is **duplicate detection**. You need to know whether you've *seen a value before* |
| "return `true` / `false`" | You need **existence** — not the position, not the count. You can bail the instant you find one |
| "`nums.length` up to 10⁵" | O(n²) would be ~10¹⁰ operations. **Dead.** You need O(n) or O(n log n) |
| nothing about order or sortedness | Input is unsorted, and you're never asked to preserve order — so you're **free to reorder it** |
| "integer array", values up to ±10⁹ | The *range* is huge but the *count* is small — you can't index by value, but you can hash it |

Strip the story away and the whole problem is one question, asked once per element:

> **"Have I seen this number before?"**

🤔 **Before you open the next section:** what data structures can answer "have I seen this before?", and how fast is each one? Try to name three.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Four honest candidates for "have I seen this before?":

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each element, scan the rest looking for a match | O(n²) | O(1) | ❌ ~10¹⁰ ops at n = 10⁵ |
| Sort first | Sort, then check neighbors — duplicates land adjacent | O(n log n) | O(1)\* | ⚠️ Correct, but slower than needed and it mutates the input |
| Hash **map** | Count each value, then look for any count ≥ 2 | O(n) | O(n) | ⚠️ Correct, but a count is more than you were asked for |
| Hash **set** | Add as you go; check membership *before* adding | O(n) | O(n) | ✅ |

\* O(1) only if you're allowed to sort in place; a sorted copy costs O(n).

**The decision: a [hashset](../data-structures/hashset.md).**

It answers membership in O(1) average — which is *exactly* the one question the problem asks, and nothing more. The hash map works too, but it stores counts you never read. Reaching for the **minimal structure that answers the question** is a small thing interviewers consistently notice.

**Why not sort?** Sorting is the right instinct when you need order, neighbours, or O(1) space. Here you need none of those, so you'd be paying an extra log n factor for nothing. But keep it in your back pocket — the moment the interviewer says *"now do it in O(1) extra space"*, sorting becomes the answer.

**The general move:** you're repeatedly *searching* for something you've already seen. That smell always points at a hash structure — see the pattern table in [how-to-approach-a-problem](../guides/how-to-approach-a-problem.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
hashset = set()
```

The memory. It holds every value seen **so far** — the running record we interrogate on each step. Empty at the start because we haven't seen anything yet.
→ [set-basics](../syntax/set-basics.md)

```python
for num in nums:
```

**One** pass. Notice there's no second loop anywhere in this solution — collapsing the nested loop into a single pass *is* the optimization.
→ [for-loop](../syntax/for-loop.md)

```python
    if num in hashset:
        return True
```

The check — and it comes **before** the insert. That ordering is the entire trick: at this exact moment `hashset` contains only *earlier* elements, so a hit is a genuine duplicate. Flip these two lines and every element finds itself, and the function returns `True` for every input.

`in` on a set is an O(1) hash lookup, not the O(n) scan the same keyword does on a list.
→ [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
    hashset.add(num)
```

Only now do we record it, so future iterations can see it.
→ [set-operations](../syntax/set-operations.md)

```python
return False
```

The loop ran to completion without ever taking that early exit ⇒ no value repeated ⇒ every element is distinct.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:

        hashset = set()

        for num in nums:
            if num in hashset:
                return True
            hashset.add(num)
        return False
```

</details>

**Trace it** — `nums = [1, 2, 3, 1]`:

| `num` | `hashset` before | In it? | Action |
|---|---|---|---|
| 1 | `{}` | no | add → `{1}` |
| 2 | `{1}` | no | add → `{1, 2}` |
| 3 | `{1, 2}` | no | add → `{1, 2, 3}` |
| 1 | `{1, 2, 3}` | **yes** | `return True` |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The loop body runs at most once per element → at most n iterations.
- Each iteration does one membership test and one insert, both **O(1) average** on a hash set.
- n × O(1) = **O(n)**.

**Best case is much better than the bound suggests.** If `nums[0] == nums[1]` you return on the second iteration. O(n) describes the worst case — an array with no duplicates at all, where you're forced to look at everything.

**The honest asterisk:** hash operations are O(1) *average*, not worst case. With pathological inputs engineered to collide into the same bucket, each operation degrades toward O(n) and the whole thing toward O(n²). No interviewer will fault you for saying O(n) — but mentioning the caveat unprompted reads as depth.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The set is the only thing that grows, and in the worst case — all values distinct — it ends up holding all n of them. (The `false` case is the expensive one here: finding a duplicate early lets you return before the set gets big.)

This is the [arrays & hashing](../learning/01-arrays-hashing.md) bargain in its purest form:

> **You spent O(n) memory to buy back a factor of n in time.**

That trade is the pattern's entire identity, and it's almost always worth taking — memory is cheap and 10¹⁰ operations are not. Recognizing when to make it is most of what Unit 01 is teaching you.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The brute force compares every pair — O(n²) — and with n up to 10⁵ that's 10¹⁰ operations, so it won't run in time. The repeated work is *searching* for a value I've already seen, so I'll trade memory for lookup speed: keep a hash set of everything seen so far, one pass, checking before I insert. That's O(n) time and O(n) space."

Four beats, and they're the same four every time: **name the brute force → name the bottleneck → name the swap → state the complexity.**

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it in O(1) extra space?" | Sort in place, then scan for adjacent equals. O(n log n) time, O(1) space — you've traded back the other way. |
| "What if the array is already sorted?" | Drop the set entirely: one pass comparing `nums[i]` to `nums[i-1]`. O(n) time, O(1) space — strictly better than the hash set. |
| "Return *which* value repeats." | Same loop, `return num` instead of `return True`. |
| "How many times does each value repeat?" | Now you need counts, so the set is no longer enough — swap in a [hash map](../data-structures/hashmap.md) or [`Counter`](../syntax/counter.md). |
| "What if it doesn't fit in memory?" | That's a systems answer: external sort on disk, or a [bloom filter](../data-structures/bloom-filter.md) if a small false-positive rate is acceptable. |

**Traps:**

- **Inserting before checking.** The #1 bug here — every element then finds itself and you return `True` for everything. Worse, it *looks* right at a glance.
- **Grabbing a `dict` out of habit** when a `set` states your intent precisely. Use a dict the moment you need *where* or *how many*; not before.
- **`return len(set(nums)) != len(nums)`** is a genuine one-liner and fine to mention as a Pythonic aside — but write the loop in an interview. It shows the mechanism, and it can exit early instead of always building the whole set.

**This same move shows up in:** [Two Sum](1-two-sum.md) (store value → index, look up the complement) · [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) (set membership to find where a run starts) · [Valid Sudoku](36-valid-sudoku.md) (one set per row, column, and box).

</details>

---
