# 278. First Bad Version

**Easy** · [LeetCode](https://leetcode.com/problems/first-bad-version/) · [Solution file (no hints)](../../problems/0001-0499/278.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

You have `n` versions `[1, 2, …, n]` and want to find the **first bad** one, which causes all following versions to be bad. You're given an API `isBadVersion(version)` returning whether a version is bad. **Minimize the number of API calls.**

```
n = 5, first bad = 4
isBadVersion(3) → false
isBadVersion(5) → true
isBadVersion(4) → true
                    →  4
```

**Constraints:** `1 <= bad <= n <= 2³¹ - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "all following versions are **also bad**" | ⚠️ **Monotonicity.** The sequence is `good, good, …, good, bad, bad, …, bad` — it flips exactly once and never flips back |
| "find the **first** bad" | You're locating a **boundary**, not searching for a value |
| "**minimize** API calls" | The API is the expensive operation — O(log n), not O(n) |
| `n` up to 2³¹ − 1 | ~2·10⁹. A linear scan is hopeless; `log₂(2³¹)` ≈ **31 calls** |
| `1 <= bad <= n` | A bad version always exists, so there's no "not found" case |

**The reframe:** there's no array here, but the versions form a sorted sequence of booleans:

```
version:  1      2      3      4      5
isBad:  false  false  false  true   true
                            ↑
                     the boundary — the answer
```

That monotonic false→true pattern is *exactly* the precondition binary search needs. You don't need sorted numbers; you need a **predicate that switches once and stays switched**.

This is the mental shift the problem teaches:

> **Binary search isn't about arrays. It's about any monotonic predicate over an ordered domain.**

Once you see it that way, [Koko Eating Bananas](875-koko-eating-bananas.md), [Capacity To Ship Packages](1011-capacity-to-ship-packages-within-d-days.md), and [Split Array Largest Sum](410-split-array-largest-sum.md) all become the same problem with a different predicate.

🤔 **Before you open the next section:** if `isBadVersion(mid)` returns true, can you rule out `mid` itself as the answer — or must you keep it as a candidate?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | API calls | Verdict |
|---|---|---|---|
| Linear scan | Test 1, 2, 3, … until bad | O(n) ≈ 2·10⁹ | ❌ Hopeless |
| Exponential then binary | Double until bad, then search | O(log n) | ⚠️ Useful when `n` is unknown; unnecessary here |
| **Binary search on the boundary** | Halve the candidate range | **O(log n)** ≈ 31 | ✅ |

**The decision: binary search using the boundary-finding convention.**

This variant differs from value-searching binary search ([Search Insert Position](35-search-insert-position.md)) in three linked ways, and they must be adopted **together**:

| | Value search | **Boundary search** |
|---|---|---|
| Loop condition | `left <= right` | **`left < right`** |
| On "too far right" | `right = mid - 1` | **`right = mid`** |
| Return | `mid` on match, or `left` | **`left` after the loop** |

**Why `right = mid` and not `mid - 1`.** If `mid` is bad, it *could itself be the first bad version* — you cannot discard it. Setting `right = mid` keeps it in the range while still shrinking. Writing `mid - 1` would step past the answer and return the wrong version.

**Why `left = mid + 1` when `mid` is good.** A good version definitively is **not** the answer, so exclude it. This asymmetry — one branch keeps `mid`, the other excludes it — is what makes boundary search work.

**Why `left < right` and not `<=`.** The range shrinks until exactly one candidate remains, and that candidate is the answer. With `<=`, once `left == right` you'd compute `mid == left`, and if `isBadVersion(mid)` were true you'd set `right = mid` — no change — and loop forever. **The `<` is what guarantees termination given `right = mid`.**

This is the general pairing to memorize:

> `right = mid` **requires** `left < right`.
> `right = mid - 1` **requires** `left <= right`.

Mixing them gives either an infinite loop or a skipped answer.

**Why the loop always terminates.** When `left < right`, `mid = (left + right) // 2` satisfies `left <= mid < right`. So `right = mid` strictly decreases `right`, and `left = mid + 1` strictly increases `left`. Either way the range shrinks, so it must reach `left == right`.

**Why no separate found-check.** Unlike value search, there's no early return. The answer is wherever the pointers converge, and a bad version is guaranteed to exist — so `left` is always valid.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
low = 1
high = n
```

Versions are **1-indexed**, so the range starts at 1 rather than 0. Both bounds are candidates.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while low < high:
```

**`<`, not `<=`** — the loop runs until exactly one candidate remains. Pairing this with `high = mid` below is what makes it both correct and terminating.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = (low + high) // 2
```

The midpoint. In Python this is safe; in C++/Java, `low + high` could overflow at `n = 2³¹ - 1`, so the portable form is `low + (high - low) // 2`. Worth flagging given this problem's constraint sits right at the `int32` limit.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if isBadVersion(mid):
        high = mid
```

**`mid` is bad, so it's a candidate — keep it.**

`high = mid`, **not** `mid - 1`. The first bad version might be `mid` itself, and discarding it would overshoot. Everything to the right of `mid` is also bad (monotonicity) and therefore can't be *first*, so the range safely narrows to `[low, mid]`.
→ [if-return](../syntax/if-return.md)

```python
    else:
        low = mid + 1
```

**`mid` is good, so it's definitively not the answer — exclude it.**

The first bad version must be strictly after `mid`, so `low = mid + 1`.
→ [elif-else](../syntax/elif-else.md)

```python
return low
```

The loop ended with `low == high` — a single surviving candidate, which is the first bad version.

Returning `high` would be equally correct at this point, since they're equal. `low` is the convention.

<details>
<summary>The whole thing together</summary>

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:

        low = 1
        high = n

        while low < high:
            mid = (low + high) // 2

            if isBadVersion(mid):
                high = mid
            else:
                low = mid + 1

        return low
```

</details>

**Trace it** — `n = 5`, first bad version is **4**:

| `low` | `high` | `mid` | `isBadVersion(mid)` | Action | Range after |
|---|---|---|---|---|---|
| 1 | 5 | 3 | `false` | `low = 4` | `[4, 5]` |
| 4 | 5 | 4 | **`true`** | `high = 4` ⭐ | `[4, 4]` |
| 4 | 4 | — | — | `low == high` → exit | — |

`return low` = **4** ✅ — in **2 API calls** rather than 5.

The starred step is the critical one: `mid = 4` was bad, and `high = mid` **kept it in the range**. Had the code used `high = mid - 1`, the range would have become `[4, 3]`, the loop would exit, and it would return 4 by luck — but on `n = 2` with first bad = 1, `high = mid - 1` gives `high = 0` and returns `low = 1`… also by luck. The failure shows up clearly on larger ranges: try `n = 5, bad = 5` mentally with `mid - 1` and watch it exclude the answer.

**A second trace** — `n = 5`, first bad is **1**:

| `low` | `high` | `mid` | Bad? | Action |
|---|---|---|---|---|
| 1 | 5 | 3 | `true` | `high = 3` |
| 1 | 3 | 2 | `true` | `high = 2` |
| 1 | 2 | 1 | `true` | `high = 1` |
| 1 | 1 | — | — | exit |

`return 1` ✅ — 3 calls, and `high = mid` preserved the answer at every step.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n) API calls** — exactly one per iteration, and the range halves each time.

At `n = 2³¹ - 1` ≈ 2.1·10⁹, that's **31 calls**. A linear scan would need up to 2.1 billion.

| n | Calls |
|---|---|
| 10 | 4 |
| 1000 | 10 |
| 10⁶ | 20 |
| 2³¹ | **31** |

**Why "minimize API calls" is the framing.** The problem is modelled on a real scenario where each check is expensive — running a test suite, deploying a build, bisecting a git history. The *number of probes* is the cost, not CPU cycles. `git bisect` is literally this algorithm.

**Is O(log n) optimal?** Yes. Each boolean answer yields at most one bit of information, and distinguishing among `n` possible boundaries requires `log₂ n` bits. You cannot do better with a yes/no oracle.

That's a genuinely satisfying lower-bound argument, and worth stating if asked whether it can be improved.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integers, independent of `n`.

Note the algorithm never materializes the versions — there's no array of size `n`, which matters given `n` can be 2·10⁹. You're binary-searching an **implicit** sequence defined by a function, not a stored one.

That's the key structural point:

> **Binary search needs an ordered domain and a monotonic predicate — not a data structure.** The domain here is `[1, n]` and the predicate is `isBadVersion`. Nothing is stored.

The same idea powers "binary search on the answer" problems, where the domain is a range of possible answers and the predicate is a feasibility check — see [Koko Eating Bananas](875-koko-eating-bananas.md), [Capacity To Ship Packages](1011-capacity-to-ship-packages-within-d-days.md), and [Split Array Largest Sum](410-split-array-largest-sum.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because every version after the first bad one is also bad, the predicate is monotonic — false then true, flipping exactly once. That's all binary search needs; there's no array involved. I search the range `[1, n]` for the boundary. If `mid` is bad, it might itself be the first bad version, so I set `high = mid` to keep it as a candidate. If `mid` is good, it definitely isn't the answer, so `low = mid + 1`. The loop condition is `low < high`, which pairs with `high = mid` — using `<=` there would loop forever once the range hit one element. When they converge, `low` is the answer. That's O(log n) API calls, about 31 at the maximum `n`, and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `high = mid` instead of `mid - 1`?" | **The key question.** A bad `mid` could itself be the first bad version; discarding it overshoots. |
| "Why `low < high` instead of `<=`?" | With `high = mid`, `<=` never shrinks the range once `low == high` — infinite loop. The two conventions must be paired. |
| "What if `n` were unknown?" | Exponential (galloping) search: probe 1, 2, 4, 8, … until bad, then binary search the last interval. Still O(log n). |
| "Can you beat O(log n)?" | No. Each boolean gives one bit; distinguishing `n` boundaries needs `log₂ n` bits. |
| "Overflow concerns?" | `n` can be 2³¹ − 1, so `low + high` overflows `int32`. Use `low + (high - low) // 2` outside Python. |
| "What if bad versions weren't monotonic?" | Binary search is invalid — you'd have to check all `n`. Monotonicity is the whole precondition. |
| "Where does this appear in practice?" | `git bisect` — exactly this algorithm over commits, with the build/test as the oracle. |

**Traps:**

- **`high = mid - 1`.** Excludes a candidate that might be the answer. *The* bug for boundary search.
- **`low <= high` paired with `high = mid`.** Infinite loop once the range reaches one element.
- **Starting `low = 0`.** Versions are 1-indexed; version 0 doesn't exist.
- **Adding an early `return mid` on a bad version.** `mid` being bad doesn't make it *first* — you must keep narrowing.
- **Returning `high` after mixing conventions.** They're equal here, but only because the pairing is correct.
- **Calling the API more than once per iteration.** Store the result if you need it twice; each call is the cost being minimized.

**This same move shows up in:** [Search Insert Position](35-search-insert-position.md) (value search, where the `<=` / `mid - 1` convention applies instead) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (boundary search with the same `right = mid` discipline) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search on the answer with a monotonic feasibility predicate) · [Capacity To Ship Packages](1011-capacity-to-ship-packages-within-d-days.md) (the same predicate-based search, on a different domain).

</details>

---
