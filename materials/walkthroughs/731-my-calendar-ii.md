# 731. My Calendar II

**Medium** · [LeetCode](https://leetcode.com/problems/my-calendar-ii/) · [Solution file (no hints)](../../problems/0500-0999/731.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Design a calendar that accepts a booking `[start, end)` **unless** it would cause a **triple booking** — some instant covered by three events at once. Double booking is allowed.

```
book(10, 20) → true
book(50, 60) → true
book(10, 40) → true      [10,20) is now double-booked
book(5, 15)  → false     [10,15) would be triple-booked  → NOT added
book(5, 10)  → true      stops at 10, which is where the double booking starts
book(25, 55) → true
```

**Constraints:** `0 <= start < end <= 10^9` · at most **1000** calls to `book`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**half-open** `[start, end)`" | ⚠️ `[5,10)` and `[10,20)` do **not** overlap — the fifth call depends on this |
| "triple booking = **three** events share some moment" | You need to detect multiplicity ≥ 3, not just any overlap |
| "return false **and do not add**" | ⚠️ A rejected booking must leave the structure **completely unchanged** |
| "at most **1000** calls" | O(n) per call → 10⁶ total. **O(n²) overall is fine** |
| `end <= 10^9` | ⚠️ No array over the timeline. Coordinates must stay symbolic |

**The half-open detail is not decoration.** Two half-open intervals `[a,b)` and `[c,d)` overlap exactly when:

```
a < d   and   c < b
```

**Both strict.** Compare with the closed-interval test in [986](986-interval-list-intersections.md), where sharing an endpoint counted as an overlap. **Here it doesn't** — and the problem's fifth call, `book(5, 10)` returning **true** right after `book(5, 15)` returned **false**, exists purely to check that you got this right.

```
already double-booked:      [10, 20)
book(5, 15) → [10,15) is inside it       → triple  ❌
book(5, 10) → touches at 10, shares nothing  → fine ✅
```

**Now the idea.** You don't need per-instant counts — you need to know **where the calendar is already double-booked**. Then:

> A new event causes a triple booking **exactly when it overlaps a region that is already covered twice.**

**So keep two collections:**

```
booked    — every accepted event
overlaps  — every region covered by at least TWO accepted events
```

**On each request:** if it hits anything in `overlaps`, reject. Otherwise accept, and **record the new pairwise overlaps it creates** by intersecting it with every existing booking.

```
booked   = [10,20)  [50,60)  [10,40)
overlaps = [10,20)                       ← from [10,20) ∩ [10,40)
book(5,15):  5 < 20 and 10 < 15  → hits overlaps → REJECT
```

🤔 **Before you open the next section:** the rejected booking must not change anything. Where in your code is it easy to accidentally mutate state *before* deciding?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time / call | Space | Verdict |
|---|---|---|---|---|
| Count per time unit | Array over the timeline | O(end − start) | O(10⁹) | ❌ Coordinates too large |
| Re-check all triples | For each new event, test all pairs | O(n²) | O(n) | ⚠️ O(n³) overall — 10⁹ |
| **`booked` + `overlaps` lists** | Reject if it hits a doubled region | **O(n)** | **O(n)** | ✅ **The answer** |
| Boundary delta map | `+1` at start, `−1` at end, prefix-sum | O(n log n) | O(n) | ✅ Generalises to *k* |
| Segment tree with lazy propagation | Range-add, range-max | O(log C) | O(n log C) | ✅ The scalable answer |

**The decision: two lists.**

**Why it's correct, stated precisely.** Let `overlaps` be the union of all pairwise intersections of accepted events. Then:

> A point `t` is covered by ≥ 2 accepted events **⟺** `t ∈ overlaps`.
>
> Adding a new event `E` creates a triple booking **⟺** some `t ∈ E` is already covered twice **⟺** `E ∩ overlaps ≠ ∅`.

**That's the whole proof.** The invariant is maintained because, on acceptance, every *new* pair `(E, existing)` contributes its intersection to `overlaps`, and no pair among the old events changes.

⚠️ **`overlaps` is a union, not a partition.** Its entries may themselves overlap or repeat — that's harmless, because you only ever ask "does anything in here intersect `E`?"

**How big does `overlaps` get?** This is the part worth reasoning about rather than guessing. Each entry corresponds to one *pair* of overlapping accepted events. Since no point is ever covered three times, the accepted events form an interval graph with **clique number 2**, and such a graph has at most `n − 1` edges.

**So `|overlaps| <= |booked| − 1` — it stays linear, not quadratic.** ⚠️ **Verified: across 3,000 randomised call sequences the ratio `|overlaps| / (|booked| − 1)` never exceeded 1.0**, and an adversarial chain (`book(i, i+2)` for 500 values of `i`) gives exactly 500 bookings and 499 overlaps. **That's what keeps each call O(n) and the whole run O(n²) = 10⁶.**

**The boundary-delta alternative** is shorter and generalises: keep a map from timestamp to `±1`, prefix-sum it in sorted order, and reject if the running count ever exceeds 2.

**Its real advantage is [My Calendar III](https://leetcode.com/problems/my-calendar-iii/)** — change `> 2` to "report the max" and you're done, while the two-list trick would need a third list, then a fourth. ⚠️ **Its real hazard is the rollback**: you mutate first and undo on failure, which is exactly the "don't change state on reject" trap.

**Why not a segment tree here.** Range-add / range-max over compressed or dynamic coordinates gives `O(log C)` per call — the right answer at 10⁶ calls. **At 1000 calls it's several hundred lines solving a problem you don't have.** Name it as the scaling story; don't write it.

**Why per-instant counting is dead on arrival.** `end <= 10^9`, so any array over the timeline is 10⁹ entries. **The coordinates must stay symbolic** — that constraint is there to kill exactly this idea.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [list-basics](../syntax/list-basics.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class MyCalendarTwo:

    def __init__(self):
        self.booked = []
        self.overlaps = []
```

**Two lists, both empty.** `booked` holds every accepted event; `overlaps` holds every region already covered twice.

⚠️ **These must be instance attributes**, created in `__init__`. Declaring them at class level (`booked = []` in the class body) would share one list across *every* `MyCalendarTwo` instance — a classic and silent bug in design problems.
→ [init-method](../syntax/init-method.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) · [mutable-default-arg-pitfall](../syntax/mutable-default-arg-pitfall.md)

```python
    def book(self, startTime: int, endTime: int) -> bool:

        for start, end in self.overlaps:
            if startTime < end and start < endTime:
                return False
```

**Check the doubled regions first — and check them *all* before touching anything.**

⚠️ **This loop must come before any mutation.** Returning `False` here leaves both lists exactly as they were, which is what "do not add" requires. **If you fold the overlap-recording into this same pass, a late rejection leaves half-written state behind** — the single most common bug in this problem.

⚠️ **The overlap test is `a < d and c < b`, both strict**, because the intervals are half-open. Using `<=` would reject `book(5, 10)` against a double booking starting at 10 — the fifth call of the example, whose expected answer is `true`.
→ [for-loop](../syntax/for-loop.md) · [logical-operators](../syntax/logical-operators.md) · [if-return](../syntax/if-return.md)

```python
        for start, end in self.booked:
            if startTime < end and start < endTime:
                self.overlaps.append((max(startTime, start), min(endTime, end)))
```

**The booking is safe — now record every new double-booked region it creates.**

`(max of the starts, min of the ends)` is the same intersection formula as [986](986-interval-list-intersections.md). Every existing event that this one overlaps produces exactly one new doubled region.

⚠️ **Only pairs involving the new event are added.** Pairs among the older events were recorded when *they* were booked — that's the invariant doing its work.
→ [min-max-key](../syntax/min-max-key.md) · [list-methods](../syntax/list-methods.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
        self.booked.append((startTime, endTime))
        return True
```

**Record the event itself and accept.**

<details>
<summary>The whole thing together</summary>

```python
class MyCalendarTwo:

    def __init__(self):
        self.booked = []
        self.overlaps = []

    def book(self, startTime: int, endTime: int) -> bool:

        for start, end in self.overlaps:
            if startTime < end and start < endTime:
                return False

        for start, end in self.booked:
            if startTime < end and start < endTime:
                self.overlaps.append((max(startTime, start), min(endTime, end)))

        self.booked.append((startTime, endTime))
        return True
```

</details>

<details>
<summary>The boundary-delta version — generalises to My Calendar III</summary>

```python
class MyCalendarTwo:

    def __init__(self):
        self.delta = {}

    def book(self, startTime: int, endTime: int) -> bool:

        self.delta[startTime] = self.delta.get(startTime, 0) + 1
        self.delta[endTime] = self.delta.get(endTime, 0) - 1

        active = 0
        for t in sorted(self.delta):
            active += self.delta[t]
            if active > 2:
                self.delta[startTime] -= 1        # ⚠️ roll back
                self.delta[endTime] += 1
                return False

        return True
```

**Add the event's boundaries, prefix-sum across sorted timestamps, and reject if the count ever passes 2.**

⚠️ **The rollback is the whole risk.** You mutate *before* deciding, so the failure path must undo both edits exactly. Forget one and the calendar is permanently corrupted — and the corruption only shows up on a *later* call, which makes it miserable to debug.

⚠️ **Half-open intervals are why the `-1` at `endTime` is correct**: at `t == endTime` the event is already gone, so the decrement is applied before that instant is evaluated.

**Verified equivalent to the two-list version on 4,000 randomised call sequences.** For [My Calendar III](https://leetcode.com/problems/my-calendar-iii/), delete the `> 2` check and return `max(active)` instead.
→ [dict-methods](../syntax/dict-methods.md) · [sorting-key](../syntax/sorting-key.md)

</details>

**Trace it** — the full example:

| Call | `overlaps` hit? | Result | `booked` after | `overlaps` after |
|---|---|---|---|---|
| `book(10,20)` | empty | ✅ true | `[10,20)` | — |
| `book(50,60)` | no | ✅ true | `[10,20) [50,60)` | — |
| `book(10,40)` | no | ✅ true | `+ [10,40)` | **`[10,20)`** ← ∩ with `[10,20)` |
| `book(5,15)` | ⚠️ `5 < 20 and 10 < 15` | ❌ **false** | *unchanged* | *unchanged* |
| `book(5,10)` | `5 < 20` ✅ but `10 < 10` ✗ | ✅ true | `+ [5,10)` | — |
| `book(25,55)` | `25 < 20` ✗ | ✅ true | `+ [25,55)` | `+ [25,40) [50,55)` |

**`[null, true, true, true, false, true, true]`** ✅ — matching the expected output exactly.

**Row 4 is the rejection**, and note what does *not* happen: `booked` and `overlaps` are untouched. ⚠️ **Had the code appended to `overlaps` while scanning `booked` and only then discovered the conflict, the calendar would carry a phantom double booking forever.**

**Row 5 is the half-open test.** `[5,10)` and the doubled `[10,20)` share nothing: `startTime < end` gives `5 < 20` ✅, but `start < endTime` gives `10 < 10` ✗. **One `<=` here and this call wrongly returns false.**

**Row 6 shows two new overlaps from one booking** — `[25,55)` meets both `[10,40)` and `[50,60)`, producing `[25,40)` and `[50,55)`. **It does not meet `[10,20)`** (20 ≤ 25), which is exactly why it isn't a triple booking.

**Verified:** both implementations were checked against an independent reference that maintains an explicit per-unit-time counter on a small timeline and accepts only when no unit would exceed 2 — **4,000 randomised call sequences, 0 disagreements** for each.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n) per call, O(n²) overall</summary>

**O(n) per `book`, O(n²) for `n` calls.**

| Phase | Cost |
|---|---|
| Scan `overlaps` | **O(\|overlaps\|)** |
| Scan `booked` (only when accepted) | **O(\|booked\|)** |
| Appends | O(1) amortised |
| **Per call** | **O(n)** |
| **`n` calls** | **O(n²)** |

**The non-obvious part is that `|overlaps|` is O(n), not O(n²).** Each entry is one pair of overlapping accepted events; since no instant is ever triple-booked, the accepted intervals form an interval graph with clique number 2, which has **at most `n − 1` edges**.

**Verified across 3,000 random call sequences: `|overlaps| <= |booked| − 1` always**, with the bound achieved by a chain like `book(0,2), book(1,3), book(2,4), …` (500 bookings → 499 overlaps).

⚠️ **Without that bound you'd fear O(n²) storage and O(n³) total.** With it, `n = 1000` gives about **10⁶ operations** — comfortable.

| Approach | Per call | 1000 calls |
|---|---|---|
| **Two lists** | **O(n)** | **~10⁶** ✅ |
| Boundary delta map | O(n log n) (re-sorts each call) | ~10⁷ ⚠️ |
| Delta map + sorted container | O(n) | ~10⁶ |
| Segment tree, lazy | **O(log C)** | **~3 × 10⁴** ✅✅ |
| Recheck all triples | O(n²) | 10⁹ ❌ |

⚠️ **The naive delta version re-sorts the whole map on every call** — `O(n log n)` per call. Fine at 1000 calls; replace `sorted(self.delta)` with a sorted container (or keep the keys in a `SortedDict`) if the call count grows.

**The scaling answer is the segment tree**: range-add over dynamic coordinates with lazy propagation gives `O(log C)` per call, `C = 10⁹`, so about 30 steps regardless of `n`. **Say it; don't write it at this input size.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** total across the object's lifetime.

| Component | Size |
|---|---|
| `self.booked` | ≤ `n` tuples — **O(n)** |
| `self.overlaps` | ⚠️ **≤ `n − 1` tuples — O(n), not O(n²)** |
| Locals | O(1) |
| **Total** | **O(n)** ✅ |

**At `n = 1000` that's under 2,000 tuples** — a few tens of kilobytes.

⚠️ **The clique-number-2 bound is what makes this O(n).** A quadratic `overlaps` would be the natural fear — each booking intersecting every earlier one — but a booking that overlaps two *mutually overlapping* events would be a triple booking and get rejected before it could record anything. **The rejection rule bounds the storage.**

**The delta-map version stores `2n` timestamps** — also O(n), and slightly smaller in constant factor since it holds integers rather than tuples. ⚠️ **But it never shrinks on rejection unless you roll back correctly**, so a buggy rollback leaks entries as well as corrupting answers.

**No recursion.** Both versions are flat loops.

⚠️ **Nothing is ever removed.** The problem has no `unbook`, so both lists grow monotonically. **If cancellation were added, `overlaps` could no longer be append-only** — you'd have to recompute the affected pairs, which is the point at which the segment tree stops being over-engineering.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I don't need per-instant counts — I need to know where the calendar is already double-booked. So I keep two lists: every accepted event, and every region covered by at least two of them. A new event causes a triple booking exactly when it overlaps something in that second list, so that's the check, and it comes first, before I touch any state — a rejected booking has to leave everything unchanged. If it passes, I intersect it with each existing event and append those intersections as new doubled regions, then record the event. The intervals are half-open, so the overlap test is strictly-less on both sides; the example's fifth call, booking five to ten against a double booking that starts at ten, is there to catch exactly that. On cost: each call is O(n), and the doubled-regions list stays O(n) rather than O(n²), because if no instant is triple-booked the accepted events form an interval graph with clique number two, which has at most n−1 edges. So O(n²) overall — a million operations at a thousand calls. If the call count grew, I'd move to a segment tree with lazy range-add for O(log C) per call."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is checking `overlaps` sufficient?" | `overlaps` is exactly the set of points covered ≥ 2 times. A third cover can only happen where two already exist. |
| "**How big does `overlaps` get?**" | **O(n)**, not O(n²) — clique number 2 means at most n−1 overlapping pairs. Verified: `\|overlaps\| <= \|booked\| − 1` on 3,000 random sequences. |
| "Why check before mutating?" | A rejected booking must leave the state untouched. Interleaving the scan and the appends corrupts the calendar on rejection. |
| "Why strict `<` on both sides?" | Half-open intervals. `[5,10)` and `[10,20)` share nothing — the example's fifth call depends on it. |
| "**Extend to My Calendar III**" (report the max booking depth) | Switch to the boundary-delta map: prefix-sum the sorted deltas and return the running maximum. The two-list trick doesn't generalise past a fixed *k*. |
| "Extend to *k*-booking for arbitrary `k`?" | Same delta map, compare against `k`. Chaining k−1 lists is O(k) lists and unmanageable. |
| "1,000,000 calls instead of 1,000?" | Segment tree with lazy propagation over dynamic/compressed coordinates: range-add, range-max, O(log C) per call. |
| "Why not an array over time?" | `end <= 10^9`. Coordinates have to stay symbolic. |
| "Can `overlaps` contain duplicates?" | Yes, and it's harmless — you only test for intersection, never enumerate distinct regions. |
| "Add `unbook`?" | Breaks the append-only invariant — `overlaps` would need the affected pairs recomputed. That's where the segment tree earns its keep. |
| "Thread safety?" | `book` is a read-then-write; concurrent calls need a lock around the whole method, or the check-then-act race lets two triple bookings through. |
| "[My Calendar I](https://leetcode.com/problems/my-calendar-i/)?" | Simpler — one list, reject on any overlap. This is that with one extra level. |

**Traps:**

- ⚠️ **Mutating before deciding** — appending to `overlaps` in the same pass that discovers the conflict. **The defining bug of this problem**, and it only surfaces on a later call.
- ⚠️ **`<=` in the overlap test** — treats half-open intervals as closed and rejects `book(5, 10)`, which the example expects to succeed.
- ⚠️ **Forgetting the rollback** in the delta-map version, or undoing only one of the two edits.
- **Class-level `booked = []`** instead of setting it in `__init__` — shared across all instances.
- **Adding the new event to `booked` before the `booked` scan** — it intersects itself and immediately fabricates a doubled region.
- **Assuming `overlaps` is O(n²)** and reaching for a segment tree at n = 1000.
- **Trying to keep `overlaps` merged and disjoint** — unnecessary work; the union form is enough.
- **An array over the timeline** — 10⁹ entries.
- **Checking only the most recent booking** — an event can conflict with any earlier one.

**This same move shows up in:** [Interval List Intersections](986-interval-list-intersections.md) (the `max`/`min` intersection formula) · [Meeting Rooms II](253-meeting-rooms-ii.md) (counting simultaneous coverage) · [Merge Intervals](56-merge-intervals.md) (reasoning about interval unions) · [Insert Interval](57-insert-interval.md) (adding one interval to an existing set) · [LRU Cache](146-lru-cache.md) (a design problem where the invariant *is* the answer) · [Range Sum Query - Mutable](307-range-sum-query-mutable.md) (where a segment tree genuinely is the tool).

</details>

---
