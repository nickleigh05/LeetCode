# 380. Insert Delete GetRandom O(1)

**Medium** · [LeetCode](https://leetcode.com/problems/insert-delete-getrandom-o1/) · [Solution file (no hints)](../../problems/0001-0499/380.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Implement `RandomizedSet` supporting **average O(1)** for all three operations:

- `insert(val)` — insert if not present; return `true` if inserted, `false` if already there
- `remove(val)` — remove if present; return `true` if removed, `false` if absent
- `getRandom()` — return a random element; **every element must be equally likely**

```
insert(1)    → true    set = {1}
remove(2)    → false   not present
insert(2)    → true    set = {1,2}
getRandom()  → 1 or 2, each with probability ½
remove(1)    → true    set = {2}
insert(2)    → false   already present
getRandom()  → 2
```

**Constraints:** `-2³¹ <= val <= 2³¹-1` · at most `2·10⁵` calls · `getRandom` is only called when non-empty

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**average O(1)**" for all three | Hashing is allowed (that's where "average" comes from), but no sorting, no scanning, no trees |
| `insert` / `remove` return booleans | You must know **membership** in O(1) → that's a [hash](../data-structures/hashset.md) |
| `getRandom` is **uniform** | You must pick a random *index* from a **dense, gapless** range → that's an [array](../data-structures/array.md) |
| "at most 2·10⁵ calls" | Any O(n) operation would give O(n²) overall — 4·10¹⁰. Confirms O(1) is mandatory |
| `getRandom` only when non-empty | No empty-collection edge case to defend |
| it's a **design** problem | The answer is a *combination* of structures, not a clever algorithm |

Here's the tension, and recognizing it *is* the problem:

| Structure | O(1) membership? | O(1) uniform random? |
|---|---|---|
| Hash set / dict | ✅ | ❌ — no indexing, and Python's internal order isn't uniform-samplable |
| Dynamic array (list) | ❌ — O(n) search | ✅ — `random.choice` on an index |

Neither one does both. The move — and it's a genuinely important one to internalize — is that you don't have to pick.

> **Use both, and keep them in sync.**

The array provides dense indices for random sampling; the hash map provides O(1) lookup **and** stores each value's position in the array so the two stay linked.

The remaining hurdle: deleting from the *middle* of an array is O(n), because everything after shifts left. That would break `remove`.

🤔 **Before you open the next section:** if the array's *order* doesn't matter — and nothing here says it does — is there a way to delete a middle element without shifting anything?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | insert | remove | getRandom | Verdict |
|---|---|---|---|---|
| Hash set only | O(1) | O(1) | **O(n)** — must materialize to sample | ❌ |
| Array only | O(n) dup check | O(n) search + O(n) shift | O(1) | ❌ |
| Array + hash set | O(1) | O(n) shift | O(1) | ❌ |
| Sorted structure | O(log n) | O(log n) | O(1) | ❌ Violates O(1) |
| **Array + hash map (value → index), swap-with-last on remove** | **O(1)** | **O(1)** | **O(1)** | ✅ |

**The decision: a list of values plus a dict mapping value → its index in that list.**

```
nums       = [ 7,  3,  9 ]      # dense, gapless — perfect for random.choice
              0   1   2
val_to_idx = { 7:0, 3:1, 9:2 }  # O(1) membership AND position
```

Every value appears in both structures, and the dict's value is the array position. Keeping that invariant true after every operation is the entire implementation.

**The swap-with-last trick** is what makes `remove` O(1), and it's the idea worth remembering long after this problem:

> To delete from the middle of an array in O(1) **when order doesn't matter**: overwrite the doomed slot with the **last** element, then pop the last slot.

Removing `3` from `[7, 3, 9]`:

```
[7, 3, 9]   →   [7, 9, 9]   →   [7, 9]
             copy last over      pop the tail
             the hole (idx 1)    (now a duplicate)
```

Popping from the end of a Python list is **O(1) amortized** — no shifting, because nothing lives after it. Popping from the middle is O(n). That asymmetry is the whole reason this works.

The bookkeeping: after the swap you must **update the moved element's index** in the dict, or it will point at the stale position and silently corrupt every future operation.

**Why not just `random.choice(list(hash_set))`?** Building the list is O(n) per call — 2·10⁵ calls at O(n) each is quadratic. And Python sets have no index-based access at all, precisely because their internal layout has holes.

**Why does the array need to be dense?** `random.choice` picks a uniform index in `[0, len-1]`. If the array had holes (from tombstone deletion, say), some indices would be empty and sampling would either return garbage or need retries — breaking both correctness and the O(1) guarantee. Swap-with-last keeps it gapless by construction.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import random

class RandomizedSet:

    def __init__(self):
        self.nums = []
        self.val_to_idx = {}
```

The two halves of the design:

- `nums` — dense list of the values, giving `getRandom` a clean index range
- `val_to_idx` — value → its index in `nums`, giving O(1) membership *and* the position needed for the swap

**The invariant to hold onto:** for every `v` in the set, `nums[val_to_idx[v]] == v`. Every method below preserves it, and every bug in this problem is a violation of it.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [random-module](../syntax/random-module.md)

```python
    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False
```

Duplicate check first — O(1) on a dict, and it's the whole reason we're not scanning the list.
→ [membership-operators](../syntax/membership-operators.md)

```python
        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)
        return True
```

Append to the end, and record that index.

**Order matters here:** `len(self.nums)` is read *before* the append, so it equals the index the value is about to occupy. Swap these two lines and the index is off by one. (Alternatively append first and use `len(self.nums) - 1` — just be deliberate about which.)
→ [list-methods](../syntax/list-methods.md) · [dict-basics](../syntax/dict-basics.md)

```python
    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False
```

Absent ⇒ nothing to do.

```python
        idx_to_remove = self.val_to_idx[val]
        last_val = self.nums[-1]
```

Grab the hole's position and the element that will fill it.
→ [list-slicing](../syntax/list-slicing.md)

```python
        self.nums[idx_to_remove] = last_val
        self.val_to_idx[last_val] = idx_to_remove
```

**The swap, both halves.** Overwrite the hole with the last value — *and* update that value's recorded index. Skipping the second line is the number-one bug on this problem: the list is right, the dict is stale, and everything after it quietly breaks.
→ [list-basics](../syntax/list-basics.md)

```python
        self.nums.pop()
        del self.val_to_idx[val]
        return True
```

Drop the now-duplicated tail (O(1) amortized), then remove the dead key.

**A subtlety worth checking:** when `val` *is* the last element, `last_val == val`, so line 1 writes it onto itself and line 2 sets `val_to_idx[val] = idx_to_remove` — momentarily re-pointing the key we're about to delete. Then `pop()` removes it from the list and `del` removes the key. Still correct, no special case needed. Trace it once and you'll trust it.
→ [dict-methods](../syntax/dict-methods.md)

```python
    def getRandom(self) -> int:
        return random.choice(self.nums)
```

Uniform by construction: `nums` is dense, so `random.choice` picks a uniform index, and every element occupies exactly one.
→ [random-module](../syntax/random-module.md)

<details>
<summary>The whole thing together</summary>

```python
import random

class RandomizedSet:

    def __init__(self):
        self.nums = []
        self.val_to_idx = {}

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False

        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)

        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False

        idx_to_remove = self.val_to_idx[val]
        last_val = self.nums[-1]
        self.nums[idx_to_remove] = last_val
        self.val_to_idx[last_val] = idx_to_remove
        self.nums.pop()
        del self.val_to_idx[val]

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
```

</details>

**Trace a middle removal** — start from `nums = [7, 3, 9]`, `val_to_idx = {7:0, 3:1, 9:2}`, call `remove(3)`:

| Step | Action | `nums` | `val_to_idx` |
|---|---|---|---|
| — | start | `[7, 3, 9]` | `{7:0, 3:1, 9:2}` |
| 1 | `idx_to_remove = 1`, `last_val = 9` | `[7, 3, 9]` | unchanged |
| 2 | `nums[1] = 9` | `[7, **9**, 9]` | unchanged |
| 3 | `val_to_idx[9] = 1` | `[7, 9, 9]` | `{7:0, 3:1, **9:1**}` |
| 4 | `nums.pop()` | `[7, 9]` | `{7:0, 3:1, 9:1}` |
| 5 | `del val_to_idx[3]` | `[7, 9]` | `{7:0, **9:1**}` |

Invariant check: `nums[0]==7` and `val_to_idx[7]==0` ✅ · `nums[1]==9` and `val_to_idx[9]==1` ✅

Skip step 3 and you'd be left with `{7:0, 9:2}` — pointing at an index that no longer exists. The next `remove(9)` would raise `IndexError`, or worse, corrupt a different slot.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) average, all three</summary>

| Operation | Complexity | Why |
|---|---|---|
| `insert` | **O(1) avg** | One dict lookup, one dict insert, one `append` (amortized O(1)) |
| `remove` | **O(1) avg** | One lookup, two dict writes, one array write, one `pop()` from the end |
| `getRandom` | **O(1)** | One uniform index draw, one array read |

**Two different "amortized" claims are in play** — being able to separate them is a real signal of depth:

1. **Hash operations are O(1) *average*** because of possible collisions. Adversarial keys could degrade a dict toward O(n).
2. **`list.append` / `list.pop()` are O(1) *amortized*** because CPython over-allocates: most calls are a pointer write, with occasional O(n) resizes that average out to constant.

`getRandom` is the only one that's *unconditionally* O(1) — no hashing involved at all.

**What the design bought:** every alternative forces one operation to O(n) — a set can't sample in O(1), an array can't look up in O(1), and naive middle deletion shifts. Composing two structures removes the trade entirely.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)**, where n is the number of elements currently stored.

Each value is stored **twice**: once in the list, once as a dict key (plus its integer index). That's a constant factor of ~2–3× compared to a single set — and it's the price of the design.

| | Space | insert | remove | getRandom |
|---|---|---|---|---|
| Hash set alone | O(n) | O(1) | O(1) | **O(n)** |
| List alone | O(n) | O(n) | O(n) | O(1) |
| **Both** | **O(n)** ×2 | **O(1)** | **O(1)** | **O(1)** |

Same asymptotic space, all operations constant. Doubling memory to eliminate an O(n) operation is almost always correct at this scale, and it's the same bargain as [Contains Duplicate](217-contains-duplicate.md) and [LRU Cache](146-lru-cache.md) — the latter being the other canonical "two structures, kept in sync" design.

**The generalizable lesson:**

> When no single data structure has all the properties you need, **compose two and maintain an invariant linking them.** The difficulty moves from "find the clever structure" to "keep both consistent on every mutation."

That's the real skill this problem tests, and it's why the bugs here are all synchronization bugs.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "No single structure does all three. A hash set gives O(1) insert and remove but can't sample uniformly in O(1); an array samples in O(1) but searches in O(n). So I'll use both: a list holding the values, and a dict mapping each value to its index in that list. Insert appends and records the index. The tricky one is remove — deleting from the middle of an array is O(n) because of shifting, so instead I overwrite the removed slot with the last element, update *that* element's index in the dict, and pop the tail. Order doesn't matter here, so the swap is free. That keeps the array dense, which is what makes `random.choice` uniform. All three are O(1) average, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Allow **duplicates**." | [LeetCode 381](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/) — map value → **set of indices**. Remove pops any one index and swaps as before. Considerably fiddlier. |
| "Why swap with the last element?" | Middle deletion is O(n) from shifting; tail deletion is O(1). Order is unspecified, so the swap costs nothing. |
| "Why must the array stay dense?" | `random.choice` needs a gapless index range for uniformity. Tombstones would break both uniformity and the O(1) bound. |
| "What if you removed the last element?" | Handled without a special case — the swap becomes a self-assignment, then `pop` and `del` clean up. Worth tracing to show it. |
| "Weighted random instead of uniform?" | Prefix sums over weights + binary search — O(log n) per pick, and O(n) to rebuild after updates. A Fenwick tree keeps updates at O(log n). |
| "`getRandom` without replacement?" | That's a shuffle — [Fisher–Yates](../algorithms/fisher-yates-shuffle.md), or swap the picked element to the end and shrink a live-region boundary. |
| "Is it thread-safe?" | No. Concurrent mutation breaks the invariant between the two structures. You'd need a lock, or a lock-free design that's substantially harder. |

**Traps:**

- **Forgetting to update the moved element's index.** *The* bug. The list looks right and the dict is stale; failures show up several operations later, far from the cause.
- **Popping before overwriting.** If you `pop()` first, `nums[idx_to_remove]` may no longer be valid — especially when removing the last element.
- **Using `nums.remove(val)`.** O(n) search plus O(n) shift. It looks like the obvious call and defeats the entire design.
- **`random.choice(list(some_set))`.** O(n) per call.
- **Off-by-one on the insert index.** Read `len(nums)` *before* appending, or use `len(nums) - 1` after — pick one deliberately.
- **Assuming the array preserves insertion order.** It doesn't, after any middle removal. Nothing requires it to — but don't write code that assumes it.

**This same move shows up in:** [LRU Cache](146-lru-cache.md) (the other canonical two-structures-in-sync design — hash map + doubly linked list) · [Design Twitter](355-design-twitter.md) (composing structures to hit per-operation bounds) · [Remove Element](27-remove-element.md) (the same "swap with the last element when order doesn't matter" trick, in array form) · [Contains Duplicate](217-contains-duplicate.md) (the O(1)-membership primitive underneath).

</details>

---
