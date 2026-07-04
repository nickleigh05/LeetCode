# Reservoir Sampling

```python
import random

def pick_random(stream):               # uniform pick from a stream of unknown length
    chosen = None
    for count, x in enumerate(stream, 1):
        if random.randint(1, count) == 1:   # keep x with probability 1/count
            chosen = x
    return chosen
```

Pick a uniformly random element from a sequence **whose length you don't know**, in one pass, O(1) memory: keep the i-th element with probability 1/i. The induction is tidy — element i is kept with 1/i, then survives each later challenger with (j−1)/j, and the product telescopes to exactly 1/n for everyone. Generalizes to sampling k items: fill a k-slot reservoir, then accept element i with probability k/i and evict a random resident.

This is the intended answer to Linked List Random Node (LC 382) and Random Pick Index (LC 398) *when the follow-up says "the input is huge / a stream"* — otherwise honestly just store the list and `random.choice` it. Real home: sampling from data too big to hold, which makes it a systems-interview talking point too.

**Complexity:** O(n) time · O(1) space (O(k) for k samples).

**Related:** [fisher-yates-shuffle](fisher-yates-shuffle.md) · [random-module (syntax)](../syntax/random-module.md) · [linked-list (data-structures)](../data-structures/linked-list.md)
