# 2709. Greatest Common Divisor Traversal

**Hard** · [LeetCode](https://leetcode.com/problems/greatest-common-divisor-traversal/) · [Solution file (no hints)](../../problems/2500-2999/2709.py)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

You are given `nums`. You may move between indices `i` and `j` (`i != j`) if `gcd(nums[i], nums[j]) > 1`. Return `True` if **every pair of indices** is connected by some sequence of such moves, otherwise `False`.

```
nums = [2, 3, 6]      →  True     (2↔6 share 2, 3↔6 share 3)
nums = [3, 9, 5]      →  False    (5 shares no factor with the others)
nums = [4, 3, 12, 8]  →  True
```

**Constraints:** `1 <= nums.length <= 10⁵` · `1 <= nums[i] <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "traverse between `i` and `j` if `gcd > 1`" | An **undirected graph** where numbers sharing a prime factor are connected |
| "every pair connected" | The whole graph is **one connected component** |
| `n` up to `10⁵` | Comparing all pairs (`10¹⁰`) is out. You need near-linear |
| values up to `10⁵` | Factorising every value is cheap with a **sieve** |

**The trick: connect through primes, not through each other.** Two numbers have `gcd > 1` exactly when they share a **prime factor**. So instead of linking numbers pairwise, link each number to **each of its prime factors**. Two numbers sharing a prime end up in the same component through that prime. The number of edges is the total number of distinct prime factors (at most about 6 per number), not `n²`.

Then it's a [union-find](../data-structures/union-find.md) question: after uniting every number with its primes, is everything in one component?

**Edge cases:**

- `n == 1`: trivially `True`.
- Any `1` in the array (with `n > 1`): `gcd(1, x) = 1`, so `1` can't connect to anything. `False`.

🤔 **Before you open the next section:** `6 = 2 × 3` and `10 = 2 × 5`. Which union operations connect them, and through which node?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Compare every pair with `gcd`, then BFS | O(n² log m) | ❌ `10¹⁰` |
| For each number, enumerate divisors up to √v | O(n √m) | ⚠️ About 3×10⁷ operations: borderline in Python |
| **Smallest-prime-factor sieve + union-find over primes** | **O(m log log m + n log m · α)** | ✅ |

**The decision: a smallest-prime-factor (SPF) [sieve](../algorithms/sieve-of-eratosthenes.md) plus union-find.**

- The sieve fills `spf[x]` with the smallest prime dividing `x`. Factorising any number is then repeated division by `spf`, at most `log₂ m` steps.
- Union-find nodes are the integers up to `max(nums)`: each number and each prime it contains are unioned.
- Finally, every number must share the root of the first one.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(nums)
if n == 1:
    return True
if 1 in nums:
    return False
```

A single element has no pairs to connect. A `1` is isolated (gcd with anything is 1), so with two or more elements the answer is `False`.
→ [if-return](../syntax/if-return.md) · [membership-operators](../syntax/membership-operators.md)

```python
m = max(nums)
spf = list(range(m + 1))
i = 2
while i * i <= m:
    if spf[i] == i:
        for j in range(i * i, m + 1, i):
            if spf[j] == j:
                spf[j] = i
    i += 1
```

The **SPF sieve.** Every number starts as its own "smallest prime factor". For each prime `i` (still `spf[i] == i`), mark its multiples from `i²` upward, **only if not already marked** by a smaller prime. At the end `spf[x]` is the smallest prime dividing `x`, and `spf[p] == p` for primes.
→ [sieve-of-eratosthenes](../algorithms/sieve-of-eratosthenes.md) · [range-function](../syntax/range-function.md) · [while-loop](../syntax/while-loop.md)

```python
parent = list(range(m + 1))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
```

[Union-find](../data-structures/union-find.md) over the integers `0..m`. `find` uses path halving, so chains stay short.
→ [closures](../syntax/closures.md) · [union-find](../data-structures/union-find.md)

```python
for num in nums:
    x = num
    while x > 1:
        p = spf[x]
        root_a, root_b = find(num), find(p)
        if root_a != root_b:
            parent[root_a] = root_b
        while x % p == 0:
            x //= p
```

**Factorise and unite.** Peel off the smallest prime `p` of `x`, and union `num` with `p`. Then divide `p` out completely (`while x % p == 0`) so the next `spf[x]` is a *new* prime. Two numbers that share a prime both union with that prime, so they land in the same component.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [while-loop](../syntax/while-loop.md)

```python
root = find(nums[0])
return all(find(num) == root for num in nums)
```

Everything is connected exactly when every number has the same root as the first.
→ [any-all](../syntax/any-all.md) · [generator-expressions](../syntax/generator-expressions.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        if 1 in nums:
            return False

        m = max(nums)
        spf = list(range(m + 1))
        i = 2
        while i * i <= m:
            if spf[i] == i:
                for j in range(i * i, m + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        parent = list(range(m + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for num in nums:
            x = num
            while x > 1:
                p = spf[x]
                root_a, root_b = find(num), find(p)
                if root_a != root_b:
                    parent[root_a] = root_b
                while x % p == 0:
                    x //= p

        root = find(nums[0])
        return all(find(num) == root for num in nums)
```

</details>

**Trace it.** `nums = [2, 3, 6]`:

| Number | Primes | Unions |
|---|---|---|
| 2 | 2 | `2 ~ 2` (already itself) |
| 3 | 3 | `3 ~ 3` |
| 6 | 2, 3 | `6 ~ 2`, `6 ~ 3` |

Now 2, 6 and 3 are all in one set. `find(2) == find(3) == find(6)` → **`True`** ✅.

`nums = [3, 9, 5]`: 3 and 9 join via 3, and 5 sits alone → `False`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m log log m + n log m)</summary>

- Sieve: **O(m log log m)**.
- Each number is factorised in at most `log₂ m` steps, each with an almost-O(1) union-find operation: **O(n log m · α)**.

For `m = n = 10⁵` that's a few million basic operations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** for the `spf` and `parent` arrays, `m = max(nums)`.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two numbers connect when they share a prime factor, so comparing every pair would be 10¹⁰. Instead I connect each number to its own prime factors in a union-find: numbers that share a prime end up in the same component through that prime. I get the primes quickly using a smallest-prime-factor sieve up to the maximum. Special cases: one element is trivially true, and a 1 can't connect to anything. After all unions, the answer is whether every number has the same root. About O(m log log m + n log m)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not pairwise gcd?" | O(n²) pairs: far too slow at `10⁵` |
| "Why union with the *prime*, not with another number?" | It keeps edges to O(n log m) total, while still joining every pair that shares that prime |
| "BFS instead of union-find?" | Possible with a bipartite graph of numbers and primes, but union-find is shorter |
| "Why divide out `p` completely?" | Otherwise `spf[x]` returns the same prime forever, or you union it repeatedly: an infinite or wasteful loop |
| "Trial division instead of a sieve?" | O(√v) per number, up to 3×10⁷ steps. The sieve cuts each factorisation to O(log v) |

**Traps:**

- **Forgetting the `1` case.** `[1]` is `True` but `[1, 2]` is `False`.
- **Forgetting `n == 1`.** A lone `1` or a lone prime is trivially fine.
- **Not removing all copies of `p`** before moving to the next prime.
- **Sieving only up to `√m`** and then reading `spf` of larger values: initialise `spf[i] = i` for every `i`.

**This same move shows up in:** [Number of Provinces](547-number-of-provinces.md) · [Accounts Merge](721-accounts-merge.md) (union through a shared key) · [Redundant Connection](684-redundant-connection.md).

</details>

---
