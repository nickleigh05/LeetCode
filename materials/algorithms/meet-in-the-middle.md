# Meet in the Middle

```python
def closest_subset_sum(nums, goal):        # LC 1755 flavor, n up to 40
    from bisect import bisect_left

    def all_sums(arr):                     # 2^(n/2) subset sums of one half
        sums = [0]
        for x in arr:
            sums += [s + x for s in sums]
        return sums

    left  = all_sums(nums[:len(nums) // 2])
    right = sorted(all_sums(nums[len(nums) // 2:]))
    best = float('inf')
    for s in left:                          # for each left sum, binary-search the
        i = bisect_left(right, goal - s)    # right sum that lands nearest goal
        for j in (i - 1, i):
            if 0 <= j < len(right):
                best = min(best, abs(s + right[j] - goal))
    return best
```

When n ≈ 40, brute force (2⁴⁰ ≈ 10¹²) is dead but 2²⁰ ≈ 10⁶ is trivial — so **split the input in half**, enumerate each half's 2^(n/2) possibilities separately, then combine the two lists cleverly (sort one, [binary search](binary-search.md) or two-pointer from the other). Exponent halved, which is astronomically better than a constant-factor win. The tell is unmistakable: *n between ~30 and 45*, subset-flavored question, no polynomial structure in sight ([constraints table](../guides/constraints-cheatsheet.md)). LeetCode appearances: Closest Subsequence Sum (1755), Partition Array Into Two Arrays to Minimize Sum Difference (2035), Fair Distribution of Cookies-adjacent hards.

**Complexity:** O(2^(n/2) · n) time · O(2^(n/2)) space — versus O(2ⁿ) brute force.

**Related:** [backtracking](backtracking.md) · [binary-search](binary-search.md) · [bisect-module (syntax)](../syntax/bisect-module.md) · [Bit Manipulation lesson](../learning/18-bit-manipulation.md)
