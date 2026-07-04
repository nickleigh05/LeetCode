# 00c. Big O Notation

*The language for "how does the work grow as the input grows?"*

[← Prev](00b-algorithms.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00d-time-complexity.md)

---

## Why not just time it?

You can't judge code by how fast it runs on *your* laptop with *10* items. The real question is: **as the input grows, how does the work grow?** **Big O notation** answers that, ignoring constants and small details to capture the *shape* of the growth.

## The classes you'll actually meet

| Big O | Name | "If input doubles, work…" | Example |
|-------|------|---------------------------|---------|
| O(1) | constant | stays the same | look up `arr[5]`, hash-map get |
| O(log n) | logarithmic | grows by one step | binary search |
| O(n) | linear | doubles | scan a list once |
| O(n log n) | linearithmic | a bit more than doubles | good sorting |
| O(n²) | quadratic | quadruples | compare every pair (nested loop) |
| O(2ⁿ) | exponential | *squares* — explodes | try every subset (naive) |

A quick picture of how fast these pull apart as `n` grows:

```
work
 │                                        O(2ⁿ)   O(n²)
 │                                      ·        /
 │                                   ·         /
 │                                ·          /
 │                             ·           /
 │                          ·            /            O(n log n)
 │                       ·             /          ___/
 │                    ·              /        ___/          O(n)
 │                 ·               /     ___/      _________/
 │              ·                /  ___/  ________/
 │         ·    ·    ·    ·    /__/______/________________  O(log n)
 │   · · ·  ____________________________________________   O(1)
 └────────────────────────────────────────────────────────► n  (input size)
```

The lesson: an O(n²) solution that's fine for 100 items can be hopeless at 100,000. Interviewers care about Big O because it predicts what happens at scale.

## The three rules of writing Big O

1. **Drop constants.** 3n steps and n steps grow the same way → both are O(n).
2. **Keep only the dominant term.** n² + n + 40 → O(n²); the smaller terms vanish as n grows.
3. **Assume the worst case** unless someone says otherwise. "It's fast when we get lucky" doesn't count.

## Two things Big O measures

Big O describes **time** (steps) and **space** (extra memory) *separately* — the next two lessons take one each. A classic trade is spending O(n) memory (a hash map) to cut time from O(n²) to O(n). That trade-off is the heartbeat of [Lesson 01](01-arrays-hashing.md).

## Check Yourself

- [ ] I can rank O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) from fastest to slowest without looking.
- [ ] I can explain why 5n + 20 is "just" O(n).
- [ ] I know Big O tracks growth as input scales — not milliseconds on one machine.

---

**Up next:** [Time Complexity](00d-time-complexity.md) — how to look at real code and *determine* its Big O.

[← Prev](00b-algorithms.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00d-time-complexity.md)
