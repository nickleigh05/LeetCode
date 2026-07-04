# Boyer-Moore Voting Algorithm

```python
def majority_element(nums):        # element appearing > n/2 times (guaranteed to exist)
    count = 0
    candidate = None
    for x in nums:
        if count == 0:
            candidate = x          # previous candidate fully cancelled — adopt x
        count += 1 if x == candidate else -1
    return candidate
```

Finds the majority element in one pass and **O(1) space** — no [Counter](../syntax/counter.md), no sort. Intuition: let every non-candidate vote *against* the current candidate. Each cancellation kills one candidate copy and one challenger copy — and an element with more than n/2 copies can't be fully cancelled even if everything else gangs up on it, so it's the one left standing. If a majority isn't *guaranteed*, add a second pass to verify the survivor actually exceeds n/2. Generalizes: at most two elements can exceed n/3, so LC 229 runs the same dance with two candidates and two counters.

**Complexity:** O(n) time · O(1) space.

**Related:** [counter (syntax)](../syntax/counter.md) · [kadane-algorithm](kadane-algorithm.md) · [Arrays & Hashing lesson](../learning/01-arrays-hashing.md)
