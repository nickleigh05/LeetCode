# Bloom Filter

```python
# k hash functions set k bits per added item
bits = [0] * m

def add(x):
    for h in hashes(x):          # k different hash functions
        bits[h % m] = 1

def might_contain(x):
    return all(bits[h % m] for h in hashes(x))
    # False → x is DEFINITELY not present
    # True  → x is PROBABLY present (could be a false positive)
```

A probabilistic [hash set](hashset.md) that trades certainty for absurdly little memory: a bit array plus k hash functions, no stored elements at all. "No" answers are guaranteed correct; "yes" answers are only *probably* right, because other items' bits can collide (tunable — sizing m and k for, say, 1% false positives takes ~10 bits per item, versus 100+ bytes for a real Python set entry). Deletion is impossible (clearing a bit might erase someone else's evidence).

Never required on LeetCode — it's a **systems** tool (Chrome's malicious-URL prescreen, databases skipping disk reads, caches deduplicating) and a favorite "how would you check membership in a billion items?" system-design talking point. Filed here because knowing it exists is the whole battle.

**Complexity:** add/query O(k) ≈ O(1) · space O(m) bits · false positives possible, false negatives never.

**Related:** [hashset](hashset.md) · [hashmap](hashmap.md) · [whats-next (guides)](../guides/whats-next.md)
